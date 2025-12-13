"""
SER 416 – Software Enterprise Projects & Process
Final Project – Option 2 (Developer Route)

Author: Bhupinder Singh (bsingh55)
Date Completed: December 3rd 2025

File: io_csv.py
Purpose:
    This module provides CSV import and export functionality for the
    CERT Disaster Preparedness Application. It includes:

        • export_records() – Writes the full households table
          to a timestamped CSV file inside the /output directory.

        • import_records() – Reads household data from a CSV file,
          validates required headers, and safely inserts records
          into the database.

    The module ensures clean separation between user interaction,
    file I/O operations, and database logic.
"""

import csv
import os
from datetime import datetime
from db import get_all_households, insert_household
from utils import print_divider, press_enter_to_continue


# -----------------------------------------------------------
# EXPORTING RECORDS TO CSV
# -----------------------------------------------------------
def export_records():
    """
    Exports all household records from the database into a timestamped
    CSV file stored inside the 'output/' directory.

    The exported CSV includes all database fields, including id,
    timestamps, and optional values.
    """
    print_divider()
    print("EXPORTING RECORDS TO CSV...")
    print_divider()

    rows = get_all_households()

    if not rows:
        print("No records to export.")
        press_enter_to_continue()
        return

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"output/Exported Records {timestamp}.csv"

    # Column headers (must match database schema)
    headers = [
        "id", "adults", "children", "has_pets", "has_dogs",
        "has_critical_meds", "meds_need_fridge", "special_needs",
        "large_propane", "natural_gas", "address",
        "phone", "email", "has_med_training", "know_neighbors",
        "has_neighbor_key", "wants_newsletter",
        "allow_non_disaster_contact", "created_at", "updated_at"
    ]

    # Write CSV
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)

    print(f"Records successfully exported to:\n{filename}")
    press_enter_to_continue()


# -----------------------------------------------------------
# IMPORTING RECORDS FROM CSV
# -----------------------------------------------------------
def import_records():
    """
    Imports household records from a user-provided CSV file.

    The CSV must contain at least the required fields. Extra fields
    (like id, created_at, updated_at) are ignored. This allows import
    from both hand-created CSVs and files exported by this app.
    """
    print_divider()
    print("IMPORT RECORDS FROM CSV")
    print_divider()

    print("NOTE:")
    print(" - Place your CSV file inside the 'output' folder before importing.")
    print(" - Example file path:  output/test_import.csv\n")

    path = input("Enter the path to the CSV file: ").strip()

    # Validate path
    if not path:
        print("File not found.")        
        press_enter_to_continue()
        return

    if not os.path.exists(path):
        print("File not found.")
        press_enter_to_continue()
        return

    imported = 0
    failed = 0

    # Open with utf-8-sig to automatically strip BOM if present
    with open(path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # Required import fields (data fields only)
        required_headers = {
            "adults", "children", "has_pets", "has_dogs",
            "has_critical_meds", "meds_need_fridge", "special_needs",
            "large_propane", "natural_gas", "address",
            "phone", "email", "has_med_training", "know_neighbors",
            "has_neighbor_key", "wants_newsletter",
            "allow_non_disaster_contact"
        }

        # Clean header names once: strip whitespace
        raw_headers = reader.fieldnames or []
        clean_headers = [h.strip() for h in raw_headers]
        header_map = dict(zip(raw_headers, clean_headers))

        # Check for missing required headers
        missing = required_headers - set(clean_headers)
        if missing:
            print("CSV file format is invalid.")
            print("Missing required headers:")
            for h in sorted(missing):
                print(f" - {h}")
            press_enter_to_continue()
            return

        # Process each row
        for row in reader:
            try:
                # Build a "clean_row" with sanitized keys
                clean_row = {}
                for original_key, value in row.items():
                    if original_key is None:
                        continue
                    key = header_map.get(original_key, original_key).strip()
                    clean_row[key] = (value.strip() if isinstance(value, str) else value)

                data = {
                    "adults": int(clean_row.get("adults") or 0),
                    "children": int(clean_row.get("children") or 0),
                    "has_pets": int(clean_row.get("has_pets") or 0),
                    "has_dogs": int(clean_row.get("has_dogs")) if clean_row.get("has_dogs") not in (None, "",) else None,
                    "has_critical_meds": int(clean_row.get("has_critical_meds") or 0),
                    "meds_need_fridge": int(clean_row.get("meds_need_fridge")) if clean_row.get("meds_need_fridge") not in (None, "",) else None,
                    "special_needs": clean_row.get("special_needs", ""),
                    "large_propane": int(clean_row.get("large_propane") or 0),
                    "natural_gas": int(clean_row.get("natural_gas") or 0),
                    "address": clean_row.get("address", ""),

                    "phone": clean_row.get("phone") or None,
                    "email": clean_row.get("email") or None,
                    "has_med_training": int(clean_row.get("has_med_training")) if clean_row.get("has_med_training") not in (None, "",) else None,
                    "know_neighbors": int(clean_row.get("know_neighbors")) if clean_row.get("know_neighbors") not in (None, "",) else None,
                    "has_neighbor_key": int(clean_row.get("has_neighbor_key")) if clean_row.get("has_neighbor_key") not in (None, "",) else None,
                    "wants_newsletter": int(clean_row.get("wants_newsletter")) if clean_row.get("wants_newsletter") not in (None, "",) else None,
                    "allow_non_disaster_contact": int(clean_row.get("allow_non_disaster_contact")) if clean_row.get("allow_non_disaster_contact") not in (None, "",) else None,
                }

                insert_household(data)
                imported += 1

            except Exception:
                failed += 1

    print("\nImport complete.")
    print(f"Successfully imported: {imported}")
    print(f"Failed: {failed}")
    press_enter_to_continue()