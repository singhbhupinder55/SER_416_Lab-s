#!/usr/bin/env python3
"""
SER 416 – HW: Network Diagram
Author: Bhupinder Singh (bsingh55)

This script:
  1. Prompts the user for a CSV file that describes a project network.
  2. Verifies the header row is "SER416,1".
  3. Parses all tasks (name, duration, predecessors) into an internal graph.
  4. Computes:
       - ES (Early Start)
       - EF (Early Finish)
       - LS (Late Start)
       - LF (Late Finish)
       - Free Float (FF)
       - Total Float (TF)
  5. Determines:
       - Minimum total project duration
       - All tasks that lie on at least one critical path (TF == 0)
       - All critical path sequences from start node to terminal node
  6. Writes all data to an output CSV file: network_analysis_output.csv

Notes:
  - No hard-coded task names or counts; everything comes from the input file.
  - The input network may list tasks in any order and is assumed to be a DAG
    with exactly one logical start and one logical terminal task.
"""

import csv
from collections import deque
from typing import Dict, List, Set, Tuple


def read_network_from_csv(filename: str):
    """
    Read the network configuration from the given CSV file.

    Returns:
        tasks: dict mapping task name -> task info dict
        order: list of task names in the same order they appeared in the file
    Raises:
        ValueError if header line is not 'SER416,1'
    """
    tasks: Dict[str, dict] = {}
    order: List[str] = []

    try:
        with open(filename, newline="") as f:
            reader = csv.reader(f)

            # ---- Verify first line: SER416,1 ----
            try:
                first_row = next(reader)
            except StopIteration:
                raise ValueError("File is empty, expected SER416,1 header.")

            if len(first_row) < 2:
                raise ValueError("Header row must have at least two columns: SER416,1")

            if first_row[0].strip() != "SER416" or first_row[1].strip() != "1":
                raise ValueError(
                    "Invalid header. First line must be: SER416,1 "
                    f"(got: {','.join(first_row)})"
                )

            # ---- Skip column headers row ----
            try:
                headers = next(reader)
            except StopIteration:
                raise ValueError("Missing header row after SER416,1 line.")

            # ---- Parse each task row ----
            for row in reader:
                if not row or all(not cell.strip() for cell in row):
                    # skip completely empty rows
                    continue

                name = row[0].strip()
                if not name:
                    raise ValueError("Found task row with empty task name.")

                try:
                    duration = float(row[1])
                except (IndexError, ValueError):
                    raise ValueError(f"Invalid or missing duration for task '{name}'.")

                # Remaining columns are predecessor names (could be blank)
                preds: List[str] = []
                for cell in row[2:]:
                    cell = cell.strip()
                    if cell:
                        preds.append(cell)

                tasks[name] = {
                    "duration": duration,
                    "pred": preds,
                    "succ": set(),   # to be filled
                    "ES": 0.0,
                    "EF": 0.0,
                    "LS": 0.0,
                    "LF": 0.0,
                    "FF": 0.0,
                    "TF": 0.0,
                }
                order.append(name)

    except FileNotFoundError:
        raise FileNotFoundError(f"Could not open file '{filename}'.")

    # ---- Build successor lists from predecessors ----
    for name, info in tasks.items():
        for p in info["pred"]:
            if p not in tasks:
                raise ValueError(
                    f"Task '{name}' has predecessor '{p}' which is not defined."
                )
            tasks[p]["succ"].add(name)

    return tasks, order


def topological_sort(tasks: Dict[str, dict]) -> List[str]:
    """
    Return a topological order of the tasks using Kahn's algorithm.
    Raises ValueError if a cycle is detected.
    """
    indegree = {t: len(info["pred"]) for t, info in tasks.items()}
    queue = deque([t for t, deg in indegree.items() if deg == 0])

    order: List[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for succ in tasks[node]["succ"]:
            indegree[succ] -= 1
            if indegree[succ] == 0:
                queue.append(succ)

    if len(order) != len(tasks):
        raise ValueError("Network contains a cycle or disconnected tasks.")

    return order


def forward_pass(tasks: Dict[str, dict], topo_order: List[str]) -> None:
    """
    Compute ES and EF for each task given a topological order.
    ES(task) = max(EF(preds)) or 0 if no predecessors.
    EF(task) = ES(task) + duration.
    """
    for name in topo_order:
        info = tasks[name]
        if info["pred"]:
            es = max(tasks[p]["EF"] for p in info["pred"])
        else:
            es = 0.0
        ef = es + info["duration"]
        info["ES"] = es
        info["EF"] = ef


def backward_pass(tasks: Dict[str, dict], topo_order: List[str]) -> float:
    """
    Compute LS and LF for each task using reverse topological order.
    Returns:
        project_duration (float) = minimum total project duration.
    """
    # Terminal tasks: those with no successors
    terminal_tasks = [name for name, info in tasks.items() if not info["succ"]]
    if not terminal_tasks:
        raise ValueError("No terminal task found (task with no successors).")

    # Project duration is max EF among terminal tasks
    project_duration = max(tasks[t]["EF"] for t in terminal_tasks)

    # Reverse topological order for backward pass
    for name in reversed(topo_order):
        info = tasks[name]
        if info["succ"]:
            lf = min(tasks[s]["LS"] for s in info["succ"])
        else:
            lf = project_duration
        ls = lf - info["duration"]
        info["LF"] = lf
        info["LS"] = ls

    return project_duration


def compute_floats(tasks: Dict[str, dict]) -> None:
    """
    Compute Free Float (FF) and Total Float (TF) for each task.
    TF = LS - ES
    FF = min(ES(successors)) - EF  (0 for terminal tasks)
    """
    for name, info in tasks.items():
        es = info["ES"]
        ef = info["EF"]
        ls = info["LS"]
        # total float
        tf = ls - es
        info["TF"] = tf

        # free float
        if info["succ"]:
            min_es_succ = min(tasks[s]["ES"] for s in info["succ"])
            ff = min_es_succ - ef
        else:
            ff = 0.0
        info["FF"] = ff


def find_start_task(tasks: Dict[str, dict]) -> str:
    """Return the task that has no predecessors (logical start)."""
    start_candidates = [name for name, info in tasks.items() if not info["pred"]]
    if len(start_candidates) != 1:
        # They said exactly one start; if not, raise.
        raise ValueError(
            f"Expected exactly one start task, found: {start_candidates}"
        )
    return start_candidates[0]


def find_critical_tasks(tasks: Dict[str, dict], eps: float = 1e-6) -> List[str]:
    """Return list of task names that are on at least one critical path (TF ~ 0)."""
    crit = [name for name, info in tasks.items() if abs(info["TF"]) < eps]
    return crit


def find_critical_paths(
    tasks: Dict[str, dict],
    start: str,
    eps: float = 1e-6,
) -> List[List[str]]:
    """
    Find all critical paths (sequences of tasks) from start to terminal tasks.

    We only follow edges through tasks with TF ~ 0.
    """
    critical_paths: List[List[str]] = []

    def dfs(current: str, path: List[str]):
        info = tasks[current]
        # If terminal task -> record path
        if not info["succ"]:
            critical_paths.append(path.copy())
            return

        for succ in sorted(info["succ"]):
            if abs(tasks[succ]["TF"]) < eps:
                path.append(succ)
                dfs(succ, path)
                path.pop()

    # Only start DFS if start itself is critical
    if abs(tasks[start]["TF"]) < eps:
        dfs(start, [start])

    return critical_paths


def write_output_csv(
    output_filename: str,
    tasks: Dict[str, dict],
    original_order: List[str],
    project_duration: float,
    critical_tasks: List[str],
    critical_paths: List[List[str]],
) -> None:
    """
    Write all computed data into a CSV file.

    Columns:
      Task, Duration, Predecessors, ES, EF, LS, LF, FF, TF, OnCriticalPath
    Then summary rows for project duration, critical tasks, and critical paths.
    """
    crit_set = set(critical_tasks)

    with open(output_filename, "w", newline="") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(
            [
                "Task",
                "Duration",
                "Predecessors",
                "ES",
                "EF",
                "LS",
                "LF",
                "FreeFloat",
                "TotalFloat",
                "OnCriticalPath",
            ]
        )

        for name in original_order:
            info = tasks[name]
            preds_str = ",".join(info["pred"]) if info["pred"] else ""
            writer.writerow(
                [
                    name,
                    f"{info['duration']:.4f}",
                    preds_str,
                    f"{info['ES']:.4f}",
                    f"{info['EF']:.4f}",
                    f"{info['LS']:.4f}",
                    f"{info['LF']:.4f}",
                    f"{info['FF']:.4f}",
                    f"{info['TF']:.4f}",
                    "YES" if name in crit_set else "",
                ]
            )

        # Blank line
        writer.writerow([])
        # Project duration summary
        writer.writerow(["Project Duration (weeks):", f"{project_duration:.4f}"])

        # Critical tasks
        writer.writerow([])
        writer.writerow(["Tasks on at least one critical path:"])
        writer.writerow(critical_tasks)

        # Critical paths
        writer.writerow([])
        writer.writerow(["Critical Paths (task sequences):"])
        for idx, path in enumerate(critical_paths, start=1):
            writer.writerow([f"Path {idx}", " -> ".join(path)])


def main():
    print("=== SER 416 – Network Diagram Critical Path Solver ===")
    input_filename = input("Enter input CSV filename (e.g., HW9-part1-prob1-1.csv): ").strip()
    output_filename = "network_analysis_output.csv"

    try:
        # 1) Read and validate network
        tasks, order = read_network_from_csv(input_filename)
        print(f"Loaded {len(tasks)} tasks from '{input_filename}'.")

        # 2) Topological order
        topo_order = topological_sort(tasks)

        # 3) Forward & backward passes
        forward_pass(tasks, topo_order)
        project_duration = backward_pass(tasks, topo_order)

        # 4) Floats
        compute_floats(tasks)

        # 5) Critical tasks and paths
        start_task = find_start_task(tasks)
        critical_tasks = find_critical_tasks(tasks)
        critical_paths = find_critical_paths(tasks, start_task)

        # 6) Write output CSV
        write_output_csv(
            output_filename,
            tasks,
            order,
            project_duration,
            critical_tasks,
            critical_paths,
        )

        # 7) Print key summary to terminal
        print("\n=== Summary ===")
        print(f"Minimum project duration: {project_duration:.4f} weeks")
        print("Tasks on a critical path (TF = 0):", ", ".join(critical_tasks))
        print("Critical paths:")
        for idx, path in enumerate(critical_paths, start=1):
            print(f"  Path {idx}: " + " -> ".join(path))

        print(f"\nAll detailed results written to '{output_filename}'.")

    except Exception as e:
        # Graceful error handling as requested in assignment
        print("\nERROR:", e)
        print("Program will exit gracefully.")


if __name__ == "__main__":
    main()