import sqlite3
import pandas as pd
import numpy as np

# ============================================================
#  SER 416 – Homework: Earned Value Analysis
#  Task 2: Earned Value Calculations
#  Author: Bhupinder Singh (bsingh55)
#
#  This script:
#   1. Reads PV, AC, EV data from SQLite (EVA_data.db)
#   2. Converts each dataset into long format (Task | Week | Value)
#   3. Merges PV, AC, EV using Task + Week
#   4. Converts blanks → 0 for EVM math (industry standard)
#   5. Computes:
#        CV  = EV - AC
#        SV  = EV - PV
#        CPI = EV / AC
#        SPI = EV / PV
#        TCPI = (BAC - EV) / (BAC - AC)
#   6. BAC (Budget at Completion) is computed as:
#        Sum of PV across all weeks for that task
#   7. Rounds CPI, SPI, TCPI for readability
#   8. Exports final EVA_Analysis.csv
#
# ============================================================

DB_NAME = "EVA_data.db"
OUTPUT_CSV = "EVA_Analysis.csv"


# ------------------------------------------------------------
# Load tables and remove header-artifact row
# ------------------------------------------------------------
def load_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

    # Remove header artifact row (NULL/blank Task)
    df = df[df["Task"].notna()]
    df = df[df["Task"].astype(str).str.strip() != ""]
    return df


# ------------------------------------------------------------
# Convert wide PV/AC/EV into long format based on column order
# ------------------------------------------------------------
def to_long_format(df: pd.DataFrame, value_name: str) -> pd.DataFrame:
    week_cols = [c for c in df.columns if c != "Task"]
    frames = []

    for i, col in enumerate(week_cols, start=1):
        temp = df[["Task", col]].copy()
        temp["Week"] = i
        temp.rename(columns={col: value_name}, inplace=True)
        frames.append(temp)

    long_df = pd.concat(frames, ignore_index=True)
    long_df.sort_values(by=["Task", "Week"], inplace=True)
    long_df.reset_index(drop=True, inplace=True)
    return long_df


def main():
    print("\n=== TASK 2: Running Earned Value Analysis Calculations ===\n")

    conn = sqlite3.connect(DB_NAME)

    # Step 1. Load PV, AC, EV tables
    pv_wide = load_table(conn, "PV")
    ac_wide = load_table(conn, "AC")
    ev_wide = load_table(conn, "EV")

    conn.close()

    # Step 2. Convert to long format
    pv_long = to_long_format(pv_wide, "PV")
    ac_long = to_long_format(ac_wide, "AC")
    ev_long = to_long_format(ev_wide, "EV")

    # Step 3. Merge PV + AC + EV
    df = pv_long.merge(ac_long, on=["Task", "Week"], how="outer")
    df = df.merge(ev_long, on=["Task", "Week"], how="outer")

    # Convert numeric fields to float
    for col in ["PV", "AC", "EV"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Step 4. IMPORTANT: Convert blanks to ZERO for EVM formulas
    df[["PV", "AC", "EV"]] = df[["PV", "AC", "EV"]].fillna(0)

    # Step 5. Compute BAC (sum of PV for each task)
    bac_table = (
        pv_long.groupby("Task")["PV"]
        .sum()
        .reset_index()
        .rename(columns={"PV": "BAC"})
    )

    df = df.merge(bac_table, on="Task", how="left")
    df["BAC"] = pd.to_numeric(df["BAC"], errors="coerce")

    # ------------------------------------------------------------
    # Step 6. Calculate Earned Value Metrics
    # ------------------------------------------------------------

    # Cost Variance
    df["CV"] = df["EV"] - df["AC"]

    # Schedule Variance
    df["SV"] = df["EV"] - df["PV"]

    # CPI = EV / AC
    df["CPI"] = np.where(df["AC"] != 0, df["EV"] / df["AC"], np.nan)

    # SPI = EV / PV
    df["SPI"] = np.where(df["PV"] != 0, df["EV"] / df["PV"], np.nan)

    # TCPI = (BAC - EV) / (BAC - AC)
    denom = (df["BAC"] - df["AC"])
    df["TCPI"] = np.where(denom != 0, (df["BAC"] - df["EV"]) / denom, np.nan)

    # ------------------------------------------------------------
    # Step 7. ROUNDING (improves readability)
    # ------------------------------------------------------------
    df["CPI"] = df["CPI"].round(3)
    df["SPI"] = df["SPI"].round(3)
    df["TCPI"] = df["TCPI"].round(3)

    df["CV"] = df["CV"].round(0)
    df["SV"] = df["SV"].round(0)

    # ------------------------------------------------------------
    # Step 8. Final formatting + output
    # ------------------------------------------------------------
    df["Week"] = df["Week"].astype(int)
    df = df.sort_values(by=["Task", "Week"]).reset_index(drop=True)

    final_cols = [
        "Task",
        "Week",
        "PV",
        "AC",
        "EV",
        "BAC",
        "CV",
        "SV",
        "CPI",
        "SPI",
        "TCPI",
    ]
    df = df[final_cols]

    df.to_csv(OUTPUT_CSV, index=False)

    print(f"EVA_Analysis.csv successfully created!\n")
    print(df.head(25).to_string(index=False))


if __name__ == "__main__":
    main()