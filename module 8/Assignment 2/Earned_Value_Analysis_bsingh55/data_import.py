import pandas as pd
import sqlite3
import os

# ============================================================
#  SER 416 – Homework: Earned Value Analysis
#  Task 1: Data Import + SQLite Storage
#  Author: Bhupinder Singh (bsingh55)
#
#  This script:
#   1. Reads PV, AC, EV CSV files
#   2. Cleans currency formatting
#   3. Imports them into SQLite database EVA_data.db
#   4. Creates 3 tables: PV, AC, EV
# ============================================================


# -------------------------------
# Helper: Clean currency fields
# -------------------------------
def clean_money(value):
    """Remove $, commas and convert to float. Handle empty/missing values."""
    try:
        if pd.isna(value):
            return None
        return float(str(value).replace("$", "").replace(",", ""))
    except:
        return None


# ============================================================
# Step 1 – Load CSV Files Using Pandas
# ============================================================

print("\n=== TASK 1: Importing PV, AC, EV into SQLite ===\n")

PV_PATH = "PV_data.csv"
AC_PATH = "AC_data.csv"
EV_PATH = "EV_data.csv"

# Read CSV with the first row treated as header
pv_raw = pd.read_csv(PV_PATH, header=0)
ac_raw = pd.read_csv(AC_PATH, header=0)
ev_raw = pd.read_csv(EV_PATH, header=0)

# Rename first column if it is blank/unnamed
pv_raw.rename(columns={pv_raw.columns[0]: "Task"}, inplace=True)
ac_raw.rename(columns={ac_raw.columns[0]: "Task"}, inplace=True)
ev_raw.rename(columns={ev_raw.columns[0]: "Task"}, inplace=True)

# Drop completely empty columns (automatic cleaning, not manual)
pv_df = pv_raw.dropna(axis=1, how='all')
ac_df = ac_raw.dropna(axis=1, how='all')
ev_df = ev_raw.dropna(axis=1, how='all')

# Clean numeric columns
pv_df.iloc[:, 1:] = pv_df.iloc[:, 1:].applymap(clean_money)
ac_df.iloc[:, 1:] = ac_df.iloc[:, 1:].applymap(clean_money)
ev_df.iloc[:, 1:] = ev_df.iloc[:, 1:].applymap(clean_money)


# ============================================================
# Step 2 – Create SQLite Database + Tables
# ============================================================

DB_NAME = "EVA_data.db"

# Delete old DB if it exists (avoids duplicates during testing)
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

conn = sqlite3.connect(DB_NAME)

# Store dataframes as tables
pv_df.to_sql("PV", conn, index=False)
ac_df.to_sql("AC", conn, index=False)
ev_df.to_sql("EV", conn, index=False)

conn.close()

print("Database created successfully: EVA_data.db")
print("Tables stored: PV, AC, EV")
print("Task 1 Completed.\n")