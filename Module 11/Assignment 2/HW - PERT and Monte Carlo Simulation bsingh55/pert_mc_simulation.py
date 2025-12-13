#!/usr/bin/env python3
"""
SER 416 – HW: PERT and Monte Carlo Simulation
Author: Bhupinder Singh (bsingh55)

This script performs the full assignment pipeline:

  1. Read and validate the "Critical Path Data" file (CSV or Excel).
     - Expected logical content: for each task we have three estimates:
         * Optimistic  (Opt)
         * Most Likely (ML)
         * Pessimistic (Pess)
     - The sample file is in *wide* format:

           ,Task1,Task12,Task23,...
           Pess,5,7,9,...
           ML,  3.1,5,8,...
           Opt, 3,4,8,...

     - The script validates that all three rows contain numeric values for
       each task. Tasks with invalid data are skipped, but the program
       does NOT crash (graceful handling).

     - Cleaned, normalized data is written to:
         critical_path_clean.csv
       with columns:
         Task, Optimistic, MostLikely, Pessimistic

  2. For each task, compute:
       PERT = (O + 4*ML + P) / 6
       Min  = O
       Max  = P
     Then compute total project duration for:
       - Optimistic sum
       - Most Likely sum
       - Pessimistic sum
       - PERT sum
     All results are written to:
       pert_summary.csv

  3. Run a Monte Carlo simulation with N = 1000 iterations:
       - For each task and each iteration, sample a value from a
         triangular distribution with:
             low  = Optimistic
             mode = MostLikely
             high = Pessimistic
       - For each iteration, sum all task samples to get a total
         project duration.

     The full matrix of samples plus the total duration per iteration
     is written to:
       monte_carlo_raw.csv

  4. From the Monte Carlo results:
       - Plot a histogram of the simulated durations for Task 1
         (defined as the first task in the cleaned data) and save as:
             task1_histogram.png
       - Compute a confidence curve of percentiles from 60.0% to 99.9%
         in 0.1% increments and save as:
             confidence_curve.csv
         Also plot this curve and save as:
             confidence_plot.png
       - Extract the minimum project durations that correspond to
         70%, 80%, and 90% confidence, and write them to:
             confidence_answers.txt

  5. The script is written to avoid hard-coding the number of tasks.
     It will work for any number of task columns in the input file.

Usage:
  Place this script in the same directory as "Critical Path Data.csv"
  (or your equivalent file) and run:

      python3 pert_mc_simulation.py

  You will be prompted for the input filename; pressing Enter will use
  the default "Critical Path Data.csv".
"""

import os
import sys
from typing import Tuple, Dict, Any, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Utility: read the input file (CSV or Excel) and normalize it
# ---------------------------------------------------------------------------

def read_and_clean_input(filename: str) -> pd.DataFrame:
    """
    Read the Critical Path Data file and return a cleaned task table.

    Expected logical content:
      index/rows: ["Pess", "ML", "Opt"]   (order not critical)
      columns:    task names (e.g., "Task1", "Task12", ...)

    The function:
      - Reads CSV (default) or Excel based on extension.
      - Validates numeric data for each task.
      - Drops any task with invalid/missing numbers, but continues.
      - Returns a DataFrame with rows:
            Task, Optimistic, MostLikely, Pessimistic

    Also writes the cleaned data to "critical_path_clean.csv".
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Input file '{filename}' not found.")

    # Decide whether to treat as Excel or CSV based on file extension.
    ext = os.path.splitext(filename)[1].lower()

    try:
        if ext in [".xls", ".xlsx"]:
            # Excel file: assume first sheet, first row headers, first column labels
            raw = pd.read_excel(filename, header=0, index_col=0)
        else:
            # CSV file: header row then first column is row labels
            raw = pd.read_csv(filename, header=0, index_col=0)
    except Exception as e:
        raise ValueError(f"Failed to read '{filename}': {e}")

    if raw.empty:
        raise ValueError("Input file appears to be empty after parsing.")

    # Normalize row labels (strip whitespace, case insensitive).
    # We expect some variant of "Opt", "ML", "Pess".
    normalized_index = {idx: str(idx).strip().lower() for idx in raw.index}
    raw.index = [normalized_index[idx] for idx in raw.index]

    # Map logical names to row labels.
    row_map: Dict[str, str] = {}  # logical -> actual index label
    for logical, aliases in {
        "optimistic": ["opt", "optimistic", "o"],
        "most_likely": ["ml", "most likely", "most_likely"],
        "pessimistic": ["pess", "pessimistic", "p"],
    }.items():
        found = [idx for idx in raw.index for a in aliases if idx == a]
        if not found:
            raise ValueError(
                f"Could not find row for '{logical}' estimates in input file."
            )
        # Pick the first matching index.
        row_map[logical] = found[0]

    # Now build a cleaned table.
    tasks: List[str] = []
    optimistic: List[float] = []
    most_likely: List[float] = []
    pessimistic: List[float] = []

    for task_name in raw.columns:
        col = raw[task_name]

        try:
            o_val = float(col[row_map["optimistic"]])
            ml_val = float(col[row_map["most_likely"]])
            p_val = float(col[row_map["pessimistic"]])
        except Exception:
            # Cannot convert to float -> skip this task gracefully.
            print(
                f"[WARNING] Skipping task '{task_name}' due to non-numeric data.",
                file=sys.stderr,
            )
            continue

        # Basic sanity check: optimistic <= most likely <= pessimistic
        if not (o_val <= ml_val <= p_val):
            print(
                f"[WARNING] Estimates for task '{task_name}' are not ordered "
                f"(Opt={o_val}, ML={ml_val}, Pess={p_val}). Task will still be used.",
                file=sys.stderr,
            )

        tasks.append(task_name)
        optimistic.append(o_val)
        most_likely.append(ml_val)
        pessimistic.append(p_val)

    if not tasks:
        raise ValueError("No valid task data found in input file.")

    clean_df = pd.DataFrame(
        {
            "Task": tasks,
            "Optimistic": optimistic,
            "MostLikely": most_likely,
            "Pessimistic": pessimistic,
        }
    )

    # Save cleaned data as requested.
    clean_df.to_csv("critical_path_clean.csv", index=False)

    return clean_df


# ---------------------------------------------------------------------------
# PERT calculations and summary
# ---------------------------------------------------------------------------

def compute_pert_summary(clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Given cleaned task data, compute PERT values and project totals.

    Adds columns:
      - PERT
      - MinDuration  (same as Optimistic)
      - MaxDuration  (same as Pessimistic)

    Returns a new DataFrame that also contains a final "TOTAL" row
    with summed project durations for:
      Optimistic, MostLikely, Pessimistic, PERT.
    The summary is also written to "pert_summary.csv".
    """
    df = clean_df.copy()

    # PERT formula per task: (O + 4 * ML + P) / 6
    df["PERT"] = (
        df["Optimistic"] + 4.0 * df["MostLikely"] + df["Pessimistic"]
    ) / 6.0

    # Range: minimum and maximum estimates
    df["MinDuration"] = df["Optimistic"]
    df["MaxDuration"] = df["Pessimistic"]

    # Compute project totals by summing across tasks.
    total_row = {
        "Task": "TOTAL",
        "Optimistic": df["Optimistic"].sum(),
        "MostLikely": df["MostLikely"].sum(),
        "Pessimistic": df["Pessimistic"].sum(),
        "PERT": df["PERT"].sum(),
        "MinDuration": df["MinDuration"].sum(),
        "MaxDuration": df["MaxDuration"].sum(),
    }

    summary_df = pd.concat(
        [df, pd.DataFrame([total_row])],
        ignore_index=True,
        sort=False,
    )

    summary_df.to_csv("pert_summary.csv", index=False)
    return summary_df


# ---------------------------------------------------------------------------
# Monte Carlo simulation using triangular distributions
# ---------------------------------------------------------------------------

def run_monte_carlo(clean_df: pd.DataFrame, n_iter: int = 1000):
    """
    Run Monte Carlo simulation for the critical path.

    For each task:
      - If O < P and O <= ML <= P  -> sample from triangular(O, ML, P).
      - If O == ML == P            -> deterministic task, use constant value.
    Returns:
      mc_matrix: 2D numpy array shape (n_iter, n_tasks)
      total_durations: 1D numpy array length n_iter
    """
    task_names = clean_df["Task"].tolist()
    optimistic = clean_df["Optimistic"].to_numpy(dtype=float)
    most_likely = clean_df["MostLikely"].to_numpy(dtype=float)
    pessimistic = clean_df["Pessimistic"].to_numpy(dtype=float)

    n_tasks = len(task_names)

    # Matrix of samples: each column is a task, each row is one simulation run.
    mc_matrix = np.zeros((n_iter, n_tasks), dtype=float)

    for j in range(n_tasks):
        o = optimistic[j]
        m = most_likely[j]
        p = pessimistic[j]

        # Basic sanity check; if data is slightly off, fix it gracefully
        if p < o:
            o, p = p, o  # swap so that o <= p

        # Degenerate case: deterministic task (triangle collapses to a point)
        if np.isclose(o, m) and np.isclose(m, p):
            samples = np.full(n_iter, m, dtype=float)
        else:
            # Regular triangular sampling
            # Ensure mode is within [o, p]; if not, clamp it.
            if m < o:
                m = o
            elif m > p:
                m = p

            samples = np.random.triangular(left=o, mode=m, right=p, size=n_iter)

        mc_matrix[:, j] = samples

    # Total duration per simulation = row-wise sum
    total_durations = mc_matrix.sum(axis=1)
    return mc_matrix, total_durations

# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------

def plot_task1_histogram(df_samples: pd.DataFrame, output_file: str) -> None:
    """
    Plot a histogram of the simulated durations for Task 1 and save to file.

    "Task 1" is defined as the first task column (leftmost) in df_samples.
    This avoids hardcoding a particular task name.
    """
    # The last column is "TotalDuration"; task columns come before it.
    task_columns = [c for c in df_samples.columns if c != "TotalDuration"]
    if not task_columns:
        raise ValueError("No task columns found in Monte Carlo samples.")

    first_task = task_columns[0]
    values = df_samples[first_task].to_numpy()

    plt.figure()
    plt.hist(values, bins=30, edgecolor="black")
    plt.title(f"Histogram of simulated durations for {first_task}")
    plt.xlabel("Duration")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def build_confidence_curve(
    total_durations: np.ndarray,
    output_csv: str,
    output_plot: str,
) -> pd.DataFrame:
    """
    Build a confidence curve from total project durations.

    Percentiles:
      from 60.0% to 99.9% in 0.1% increments (inclusive).

    Writes:
      - confidence_curve.csv with columns [Percentile, Duration]
      - confidence_plot.png showing the line chart.

    Returns the DataFrame with the curve.
    """
    # Percentiles for numpy are in [0, 100].
    percentiles = np.arange(60.0, 100.0, 0.1)  # 60.0, 60.1, ..., 99.9
    durations = np.percentile(total_durations, percentiles)

    curve_df = pd.DataFrame(
        {"Percentile": percentiles, "Duration": durations}
    )
    curve_df.to_csv(output_csv, index=False)

    # Plot the curve.
    plt.figure()
    plt.plot(curve_df["Percentile"], curve_df["Duration"])
    plt.title("Project Duration Confidence Curve")
    plt.xlabel("Confidence Percentile (%)")
    plt.ylabel("Project Duration")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_plot)
    plt.close()

    return curve_df


def write_confidence_answers(
    curve_df: pd.DataFrame,
    output_file: str,
    targets: List[float] = None,
) -> None:
    """
    Extract durations at specific confidence levels and write them to a
    simple text file for management.

    targets: list of percentiles (e.g., [70.0, 80.0, 90.0]).
    """
    if targets is None:
        targets = [70.0, 80.0, 90.0]

    # For each target percentile, find the nearest row in the curve_df.
    lines: List[str] = []
    for p in targets:
        # Index of row with Percentile closest to p
        idx = (curve_df["Percentile"] - p).abs().idxmin()
        row = curve_df.loc[idx]
        duration = row["Duration"]
        lines.append(
            f"Approximate minimum project duration for {p:.1f}% confidence: "
            f"{duration:.4f}"
        )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Confidence Analysis (from Monte Carlo Simulation)\n")
        f.write("------------------------------------------------\n")
        for line in lines:
            f.write(line + "\n")


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def main() -> None:
    print("=== SER 416 – PERT and Monte Carlo Simulation ===")

    # Prompt for input file, defaulting to "Critical Path Data.csv"
    default_name = "Critical Path Data.csv"
    user_input = input(
        f"Enter input filename (press Enter for '{default_name}'): "
    ).strip()
    if user_input == "":
        filename = default_name
    else:
        filename = user_input

    try:
        # 1) Read and clean the input data.
        print(f"\n[1] Reading and validating input file: {filename}")
        clean_df = read_and_clean_input(filename)
        print(
            f"    Loaded {len(clean_df)} tasks. "
            f"Cleaned data written to 'critical_path_clean.csv'."
        )

        # 2) PERT summary.
        print("\n[2] Computing PERT durations and project totals...")
        summary_df = compute_pert_summary(clean_df)
        total_row = summary_df[summary_df["Task"] == "TOTAL"].iloc[0]
        print(
            "    Project totals (from pert_summary.csv):\n"
            f"      Optimistic:  {total_row['Optimistic']:.4f}\n"
            f"      Most Likely: {total_row['MostLikely']:.4f}\n"
            f"      Pessimistic: {total_row['Pessimistic']:.4f}\n"
            f"      PERT:        {total_row['PERT']:.4f}"
        )

        # 3) Monte Carlo simulation.
        print("\n[3] Running Monte Carlo simulation (1000 iterations)...")
        mc_matrix, total_durations = run_monte_carlo(clean_df)

        # Convert to DataFrame so we can save and plot
        df_samples = pd.DataFrame(
            mc_matrix,
            columns=clean_df["Task"].tolist()
        )

        # Add total duration column
        df_samples["TotalDuration"] = total_durations

        df_samples.to_csv("monte_carlo_raw.csv", index=False)

        print(
            "    Monte Carlo samples written to 'monte_carlo_raw.csv'. "
            f"Simulated {len(total_durations)} total durations."
        )
        
        # 4) Histogram for Task 1.
        print("\n[4] Generating histogram for Task 1 samples...")
        plot_task1_histogram(df_samples, "task1_histogram.png")
        print("    Saved histogram as 'task1_histogram.png'.")

        # 5) Confidence curve and plot.
        print("\n[5] Building confidence curve from 60.0% to 99.9%...")
        curve_df = build_confidence_curve(
            total_durations,
            output_csv="confidence_curve.csv",
            output_plot="confidence_plot.png",
        )
        print(
            "    Confidence curve written to 'confidence_curve.csv' "
            "and plotted in 'confidence_plot.png'."
        )

        # 6) Management-level answers for 70/80/90%.
        print("\n[6] Extracting durations for 70%, 80%, and 90% confidence...")
        write_confidence_answers(curve_df, "confidence_answers.txt")
        print("    Answers written to 'confidence_answers.txt'.")

        print("\n=== All steps completed successfully. ===")

    except Exception as e:
        # Graceful error handling as required in the assignment.
        print("\nERROR:", e)
        print("Program will exit gracefully.")
        # Optional: non-zero exit code to indicate failure to a caller script.
        # sys.exit(1)


if __name__ == "__main__":
    main()