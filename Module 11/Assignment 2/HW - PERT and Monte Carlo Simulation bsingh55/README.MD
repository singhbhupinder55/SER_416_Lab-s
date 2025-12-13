README – PERT and Monte Carlo Simulation (SER 416)

Overview

This assignment analyzes uncertainty in project scheduling using the Program Evaluation and Review Technique (PERT) and Monte Carlo simulation.

The script reads a project’s critical path task estimates (Optimistic, Most Likely, Pessimistic), cleans and validates the data, computes PERT durations, and performs a 1,000-iteration Monte Carlo simulation using triangular distributions. It then generates:
	•	critical_path_clean.csv – cleaned task data
	•	pert_summary.csv – PERT calculations and project totals
	•	monte_carlo_raw.csv – all random samples and total durations
	•	task1_histogram.png – histogram of sampled durations for Task 1
	•	confidence_curve.csv – percentiles from 60.0% to 99.9%
	•	confidence_plot.png – confidence curve visualization
	•	confidence_answers.txt – answers for 70%, 80%, 90% confidence

The script is fully dynamic and works with any number of tasks in the input file.

⸻

Setup Instructions

1. Create and Activate a Virtual Environment
bash```
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
```

2. Install Required Packages
bash```
pip install pandas numpy matplotlib
```

⸻

How to Run the Script
	1.	Place pert_mc_simulation.py in the same folder as the file
Critical Path Data.csv
	2.	Run the script:
    bash```
    python3 pert_mc_simulation.py
    ```
    3.	When prompted, press Enter to use the default filename or type a different file name.

All output files will be generated in the same directory.
