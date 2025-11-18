"""
SER 416 – Module 8: Class Case Study – Cost Estimate
Author: Bhupinder Singh
Phase: 1 (Excel Property Management Web Ledger)

Purpose:
    This program estimates total project costs for Phase 1 by combining:
        - Labor costs for each WBS task (using WBS_Phase1.csv)
        - Non-labor costs (hardware, software, and tool fees)
        - Recurring post-deployment monthly costs

Outputs:
    1. Development_Costs.csv
       - Detailed breakdown of:
         * Each WBS task (labor: hours, rate, cost)
         * Non-labor items (hardware/software/tools: quantity, unit cost, total)
    2. Recurring_Costs.csv
       - Monthly recurring costs for operating the web solution
       - 3-month totals + overall summary row
    3. Console summary
       - Total labor cost
       - Total non-labor cost
       - One-time development cost
       - Monthly recurring cost
       - 3-month recurring cost
       - Grand total (development + 3 months recurring)
       - Assumptions / methodology

Methodology:
    - WBS_Phase1.csv provides:
        id, task, role, weeks
    - Each task’s person-hours:
        hours = weeks * 40  (assuming full-time allocation)
    - Cost per task:
        cost = hours * hourly_rate(role)
    - Hardware / software / tool fees are modeled as one-time
      Phase 1 costs and calculated entirely in Python.
    - Recurring monthly costs represent hosting, support, and
      observability after deployment, and are multiplied by 3 months
      to show short-term operational impact.
"""

import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# CONFIGURATION: HOURLY RATES (ENGINEERING RESOURCES)
# ---------------------------------------------------------
# These rates are reasonable market-style estimates and are used
# to compute labor costs per WBS task.
RATES = {
    "Project Manager": 60,      # $/hour
    "Backend Engineer": 55,     # $/hour
    "Frontend Engineer": 50,    # $/hour
    "Database Engineer": 50,    # $/hour
    "QA Engineer": 45,          # $/hour
}

# ---------------------------------------------------------
# NON-LABOR COSTS: HARDWARE, SOFTWARE, TOOLS (ONE-TIME)
# ---------------------------------------------------------
#   - Hardware (developer equipment, test server)
#   - Software (JetBrains, Postman workspace)
#   - Tools / platforms (Jira, GitHub Team)
NON_LABOR_ITEMS = [
    # Hardware
    {
        "type": "Hardware",
        "category": "Developer Laptops",
        "description": "Laptops for engineers (Phase 1)",
        "quantity": 3,
        "unit_cost": 1500,
    },
    {
        "type": "Hardware",
        "category": "Office Furniture",
        "description": "Desks and chairs for dev team",
        "quantity": 3,
        "unit_cost": 300,
    },
    {
        "type": "Hardware",
        "category": "Test Server",
        "description": "External test / staging server",
        "quantity": 1,
        "unit_cost": 500,
    },

    # Software (COTS) – option B
    {
        "type": "Software",
        "category": "JetBrains All Products",
        "description": "Backend + Frontend IDE licenses (2 developers)",
        "quantity": 2,
        "unit_cost": 249,
    },
    {
        "type": "Software",
        "category": "Postman Workspace",
        "description": "API testing workspace (5 users × $12/mo × 3 months)",
        "quantity": 1,
        "unit_cost": 5 * 12 * 3,  # 5 users, 12$/mo, 3 months
    },

    # Tool / platform fees
    {
        "type": "Tool",
        "category": "Jira Cloud",
        "description": "Issue tracking (5 users × $10/mo × 3 months)",
        "quantity": 1,
        "unit_cost": 5 * 10 * 3,
    },
    {
        "type": "Tool",
        "category": "GitHub Team Plan",
        "description": "Source control (5 users × $4/mo × 3 months)",
        "quantity": 1,
        "unit_cost": 5 * 4 * 3,
    },
]

# ---------------------------------------------------------
# RECURRING MONTHLY COSTS (POST-DEPLOYMENT)
# ---------------------------------------------------------
RECURRING_ITEMS = [
    {"item": "AWS EC2 (app server, t3.small)", "monthly": 45},
    {"item": "AWS RDS (db.t3.micro)",          "monthly": 29},
    {"item": "S3 Backups",                     "monthly": 8},
    {"item": "CloudWatch Monitoring",          "monthly": 10},
    {"item": "Domain + SSL Certificate",       "monthly": 10},
    {"item": "Maintenance Engineer Retainer",  "monthly": 600},
    {"item": "Logging / APM Tool (e.g., Datadog)", "monthly": 50},
]

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def load_wbs(csv_path: str = "WBS_Phase1.csv") -> pd.DataFrame:
    """
    Load WBS tasks from CSV.

    Expected columns:
        id, task, role, weeks

    Returns:
        pandas.DataFrame with numeric 'weeks' column.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Required file '{csv_path}' was not found. "
            f"Make sure it is in the same directory as cost_estimate.py."
        )

    df = pd.read_csv(csv_path)

    # Basic validation
    required_cols = {"id", "task", "role", "weeks"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise ValueError(f"WBS CSV missing required columns: {missing}")

    # Force weeks to numeric
    df["weeks"] = pd.to_numeric(df["weeks"], errors="coerce").fillna(0)

    return df


def calculate_labor_costs(df_wbs: pd.DataFrame) -> pd.DataFrame:
    """
    Given the WBS DataFrame, compute hours and cost per task.

    - hours = weeks * 40 (single FTE assumption)
    - rate  = RATES[role]
    - cost  = hours * rate
    """
    def get_rate(role: str) -> float:
        if role not in RATES:
            raise KeyError(f"Role '{role}' does not have a defined hourly rate.")
        return RATES[role]

    df = df_wbs.copy()
    df["hours"] = df["weeks"] * 40
    df["rate"] = df["role"].apply(get_rate)
    df["labor_cost"] = df["hours"] * df["rate"]
    return df


def build_development_costs_df(labor_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a single DataFrame containing:
        - All WBS tasks as Labor rows
        - All Non-labor (hardware/software/tools) rows

    Columns:
        Type, Category, WBS ID, Task, Role, Weeks, Hours, Rate ($/hr),
        Quantity, Unit Cost ($), Cost ($), Notes
    """
    rows = []

    # Labor rows from WBS
    for _, row in labor_df.iterrows():
        rows.append({
            "Type": "Labor",
            "Category": "WBS Task",
            "WBS ID": row["id"],
            "Task": row["task"],
            "Role": row["role"],
            "Weeks": row["weeks"],
            "Hours": row["hours"],
            "Rate ($/hr)": row["rate"],
            "Quantity": "",
            "Unit Cost ($)": "",
            "Cost ($)": row["labor_cost"],
            "Notes": "Cost = weeks × 40h × role rate",
        })

    # Non-labor rows
    for item in NON_LABOR_ITEMS:
        total = item["quantity"] * item["unit_cost"]
        rows.append({
            "Type": item["type"],
            "Category": item["category"],
            "WBS ID": "",
            "Task": item["description"],
            "Role": "",
            "Weeks": "",
            "Hours": "",
            "Rate ($/hr)": "",
            "Quantity": item["quantity"],
            "Unit Cost ($)": item["unit_cost"],
            "Cost ($)": total,
            "Notes": "One-time Phase 1 non-labor cost",
        })

    df_dev = pd.DataFrame(rows)

    return df_dev


def build_recurring_costs_df() -> pd.DataFrame:
    """
    Build a DataFrame for recurring monthly costs and 3-month totals.

    Columns:
        Item, Monthly Cost ($), 3-Month Cost ($)
    """
    rows = []
    for item in RECURRING_ITEMS:
        monthly = item["monthly"]
        three_month = monthly * 3
        rows.append({
            "Item": item["item"],
            "Monthly Cost ($)": monthly,
            "3-Month Cost ($)": three_month,
        })

    df_recur = pd.DataFrame(rows)

    # Add a TOTAL row
    total_monthly = df_recur["Monthly Cost ($)"].sum()
    total_3month = df_recur["3-Month Cost ($)"].sum()
    df_recur.loc[len(df_recur)] = {
        "Item": "TOTAL",
        "Monthly Cost ($)": total_monthly,
        "3-Month Cost ($)": total_3month,
    }

    return df_recur


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":
    print("=== PHASE 1 COST ESTIMATION – EXCEL PROPERTY MANAGEMENT WEB LEDGER ===\n")

    # 1. Load WBS from CSV
    try:
        wbs_df = load_wbs("WBS_Phase1.csv")
        print("WBS_Phase1.csv found.")
        print("WBS data successfully loaded from CSV.\n")
    except Exception as e:
        print("ERROR: Could not load WBS_Phase1.csv")
        print(e)
        raise SystemExit(1)

    # 2. Calculate labor costs per WBS task
    labor_df = calculate_labor_costs(wbs_df)

    # 3. Build Development_Costs.csv (labor + non-labor)
    dev_df = build_development_costs_df(labor_df)
    dev_df.to_csv("Development_Costs.csv", index=False)

    # 4. Aggregate labor and non-labor totals
    labor_total = labor_df["labor_cost"].sum()
    nonlabor_total = dev_df.loc[dev_df["Type"] != "Labor", "Cost ($)"].sum()
    development_total = labor_total + nonlabor_total

    # 5. Build Recurring_Costs.csv
    recur_df = build_recurring_costs_df()
    recur_df.to_csv("Recurring_Costs.csv", index=False)

    monthly_total = recur_df.loc[recur_df["Item"] != "TOTAL", "Monthly Cost ($)"].sum()
    three_month_total = recur_df.loc[recur_df["Item"] != "TOTAL", "3-Month Cost ($)"].sum()

    grand_total = development_total + three_month_total

    # 6. summary by role (resource costs)
    role_summary = labor_df.groupby("role")[["hours", "labor_cost"]].sum()

    # 7. Print Management-Level Summary
    print(">>> DEVELOPMENT COST SUMMARY (ONE-TIME, PHASE 1)")
    print(f"  Labor Total:           ${labor_total:,.2f}")
    print(f"  Non-Labor Total:       ${nonlabor_total:,.2f}  (hardware/software/tools)")
    print(f"  Development Cost:      ${development_total:,.2f}\n")

    print(">>> RECURRING COST SUMMARY (POST-DEPLOYMENT)")
    print(f"  Monthly Recurring Cost: ${monthly_total:,.2f}")
    print(f"  3-Month Recurring Cost: ${three_month_total:,.2f}\n")

    print(">>> GRAND TOTAL (Development + 3 Months Recurring)")
    print(f"  ASK OF MANAGEMENT:     ${grand_total:,.2f}\n")

    print(">>> RESOURCE COSTS BY ROLE (Labor Only)")
    for role, row in role_summary.iterrows():
        print(f"  {role}: {row['hours']:.1f} hours, ${row['labor_cost']:,.2f}")

    print("\nAssumptions / Methodology:")
    print("- Phase 1 only (web-based ledger); Phase 0 Excel work is already funded.")
    print("- 40 hours/week per task owner; weeks taken from WBS/Gantt estimates.")
    print("- Hourly rates per role defined in RATES dictionary (see top of file).")
    print("- Development_Costs.csv includes both labor and one-time non-labor items.")
    print("- Recurring_Costs.csv models realistic monthly cloud + maintenance costs.")
    print("- 3-month recurring window used to show short-term operational impact.")
    print("- All calculations are performed in Python to satisfy assignment requirements.")