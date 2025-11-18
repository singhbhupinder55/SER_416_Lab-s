# SER 416 – Module 8  
## Class Case Study – Phase 1 Cost Estimate

**Author:** Bhupinder Singh  
**Project:** Excel Property Management – Web Ledger (Phase 1 only)

This folder contains the Python-based cost estimation for **Phase 1** of the Excel Property Management web ledger project. The goal is to replace manual Excel/VBA cost sheets with a reproducible Python script that reads the WBS, calculates development and recurring costs, and outputs detailed CSV reports.

---

## Files

- `cost_estimate.py`  
  Main Python script. Reads the Phase 1 WBS from CSV, calculates labor and non-labor development costs, recurring monthly costs, and prints a management-level summary.

- `WBS_Phase1.csv`  
  Input data for Phase 1. Each row represents one WBS task/subtask with:
  - `Type` (Labor / Hardware / Software / Tool)  
  - `Category` (e.g., WBS Task, Developer Laptops, JetBrains)  
  - `WBS ID`  
  - `Task`  
  - `Role` (for labor rows only)  
  - `Weeks` (effort estimate)  
  - `Rate ($/hr)` (for labor rows)  
  - `Quantity`, `Unit Cost ($)` (for hardware/software/tool rows)

- `Development_Costs.csv`  
  Generated output containing the full development cost breakdown for Phase 1:
  - Labor rows: `Weeks`, `Hours (weeks × 40)`, `Rate`, `Cost`, role, WBS ID  
  - Non-labor rows (hardware/software/tools): `Quantity`, `Unit Cost`, `Cost`  
  - A `Notes` column documents how each cost was derived.

- `Recurring_Costs.csv`  
  Generated output listing monthly and 3-month recurring costs after deployment:
  - Cloud hosting (EC2, RDS, S3, CloudWatch)  
  - Domain + SSL  
  - Maintenance engineer retainer  
  - Logging/monitoring tool  
  Includes a `TOTAL` row for quick reference.

- `Terminal_output.png`  
  Screenshot of a sample run of `cost_estimate.py`, showing totals and assumptions.

---

## How to Run

1. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install required dependency:
   ```bash
  python3 -m pip install pandas
  ```
3. Ensure the input file is present:
Place WBS_Phase1.csv in the same directory as cost_estimate.py.

4. Run:
  ```bash
  python3 cost_estimate.py
  ```
5. After execution, you will see:
	•	A console summary including:
	•	Labor total
	•	Non-labor total
	•	Development cost
	•	Monthly & 3-month recurring cost
	•	Grand total (“Ask of Management”)
	•	Resource cost breakdown by role
	•	Methodology & assumptions
	•	Two output files generated:
	•	Development_Costs.csv
	•	Recurring_Costs.csv

 ## Methodology & Assumptions

1. WBS-Driven Task Costing
	•	The script imports WBS_Phase1.csv using pandas.
	•	For each labor task:
	•	Hours = Weeks × 40
	•	Cost = Hours × Role Rate
	•	Hourly rates come from the RATES dictionary inside cost_estimate.py.
	•	This fulfills assignment requirements to:
	•	List all WBS tasks
	•	Provide effort in hours
	•	Apply hourly rates
	•	Compute per-task cost

2. Hardware / Software / Tool Costs

Items in the CSV marked as Hardware, Software, and Tool include:
	•	Developer laptops
	•	Office furniture
	•	Test server
	•	JetBrains licenses
	•	Postman Workspace
	•	Jira Cloud
	•	GitHub Team Plan

For each:
	•	Cost = Quantity × Unit Cost
	•	These rows appear as Non-Labor in Development_Costs.csv.

3. Resource Cost Summary

After all WBS labor rows are processed:
	•	Python groups rows by Role
	•	Sums:
	•	Total hours per role
	•	Total labor cost per role

The terminal output includes totals for:
	•	Backend Engineers
	•	Frontend Engineers
	•	Database Engineers
	•	QA Engineers
	•	Project Manager

4. Total Development Cost (Phase 1 Only)

  Python computes: Development Cost = Labor Total + Non-Labor Total

Phase 0 (Excel prototype) is not included because it was previously funded.

5. Recurring Monthly Costs (Post-Deployment)

The script models realistic cloud + maintenance expenses:
	•	AWS EC2
	•	AWS RDS
	•	S3 backups
	•	CloudWatch
	•	Domain + SSL
	•	Maintenance engineer retainer
	•	Logging/monitoring tool

Python computes:
	•	Monthly cost for each item
	•	A TOTAL row
	•	A 3-month operational cost to show short-term impact

These values are exported to Recurring_Costs.csv and shown in the console.

⸻

💰 Ask of Management

The script prints: ASK OF MANAGEMENT = Development Cost + 3-Month Recurring Cost
  This represents:
	•	Full Phase 1 build-out
	•	First three months of operational support
	•	All engineering + hardware/software/tool funding