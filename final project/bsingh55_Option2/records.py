"""
SER 416 – Software Enterprise Projects & Process
Final Project – Option 2 (Developer Route)

Author: Bhupinder Singh (bsingh55)
Date Completed: December 5th 2025

File: records.py
Purpose:
    Implements the core record-management workflow for the CERT Disaster
    Preparedness Application.

    Features Included:
        • Add new household records
        • View all records in summary form
        • Edit an existing record
        • Helper to convert boolean database fields into yes/no text

    This file acts as the main controller for user interaction flow.
"""

from validation import (
    ask_int, ask_yes_no, ask_text, ask_phone, ask_email
)
from db import (
    insert_household, get_all_households, get_household_by_id, update_household
)
from utils import print_divider, press_enter_to_continue


# -------------------------------------------------------
# YES/NO DISPLAY HELPER
# -------------------------------------------------------
def yesno(value):
    """
    Convert stored values (1, 0, True, False, None) into a readable
    'yes', 'no', or blank string for display in edit mode.
    """
    if value is None:
        return ""
    return "yes" if value == 1 or value is True else "no"


# -------------------------------------------------------
# ADD NEW RECORD
# -------------------------------------------------------
def add_record():
    """
    Interactive workflow to add a new household record.
    Prompts user for all required and optional fields and stores
    the completed record in the database.
    """
    print_divider()
    print("ADD NEW HOUSEHOLD RECORD")
    print_divider()

    data = {}

    # Required fields
    data["adults"] = ask_int("Number of adults in the household: ", min_value=0)
    data["children"] = ask_int("Number of children in the household: ", min_value=0)

    # Pets
    data["has_pets"] = ask_yes_no("Are there any pets?")
    if data["has_pets"]:
        data["has_dogs"] = ask_yes_no("Are there any dogs?")
    else:
        data["has_dogs"] = None

    # Critical medications
    data["has_critical_meds"] = ask_yes_no("Does anyone in the house have critical medications?")
    if data["has_critical_meds"]:
        data["meds_need_fridge"] = ask_yes_no("Do the medications require refrigeration?")
    else:
        data["meds_need_fridge"] = None

    # Special needs (required)
    data["special_needs"] = ask_text(
        "Does anyone have special needs that require assistance?"
        "\n(Enter 'no' if none): "
    )

    # Hazards & utilities
    data["large_propane"] = ask_yes_no("Does the house have a large propane tank?")
    data["natural_gas"] = ask_yes_no("Does the house have a natural gas connection?")

    # Address (required)
    data["address"] = ask_text("Household address: ")

    # Optional contact info
    data["phone"] = ask_phone("Household contact phone number (optional): ", allow_blank=True)
    data["email"] = ask_email("Household contact email (optional): ", allow_blank=True)

    # Optional yes/no values
    data["has_med_training"] = ask_yes_no(
        "Does anyone in the house have medical training? (optional)",
        allow_blank=True,
        default=None
    )
    data["know_neighbors"] = ask_yes_no(
        "Do they know their neighbors? (optional)",
        allow_blank=True,
        default=None
    )
    data["has_neighbor_key"] = ask_yes_no(
        "Do they have a neighbor's key? (optional)",
        allow_blank=True,
        default=None
    )
    data["wants_newsletter"] = ask_yes_no(
        "Do they want the CERT newsletter? (optional)",
        allow_blank=True,
        default=None
    )
    data["allow_non_disaster_contact"] = ask_yes_no(
        "Can CERT use contact info for non-disaster purposes? (optional)",
        allow_blank=True,
        default=None
    )

    # Store record
    insert_household(data)

    print("\nRecord added successfully!")
    press_enter_to_continue()


# -------------------------------------------------------
# VIEW RECORDS
# -------------------------------------------------------
def view_records():
    """
    Displays all household records in a summary list.
    Allows the user to select a record to edit.
    """
    print_divider()
    print("HOUSEHOLD RECORDS")
    print_divider()

    rows = get_all_households()

    if not rows:
        print("No records found.")
        press_enter_to_continue()
        return

    # Display summary
    for i, row in enumerate(rows, start=1):
        record_id = row[0]
        address = row[10]
        adults = row[1]
        children = row[2]
        print(f"{i}) ID {record_id} | {address} | Adults: {adults}, Children: {children}")

    print("\nPress Enter to return to the main menu.")
    choice = input("Enter a number to edit that record: ").strip()

    if choice == "":
        return

    if not choice.isdigit() or not (1 <= int(choice) <= len(rows)):
        print("Invalid selection.")
        press_enter_to_continue()
        return

    index = int(choice) - 1
    record_id = rows[index][0]

    edit_record(record_id)


# -------------------------------------------------------
# EDIT RECORD
# -------------------------------------------------------
def edit_record(record_id):
    """
    Loads an existing record by ID, shows current values, and allows
    the user to update any field. Blank entries preserve old values.
    """
    print_divider()
    print(f"EDITING RECORD ID {record_id}")
    print_divider()

    row = get_household_by_id(record_id)

    if not row:
        print("Record not found.")
        press_enter_to_continue()
        return

    # Map database row to named fields
    fields = [
        "id", "adults", "children", "has_pets", "has_dogs",
        "has_critical_meds", "meds_need_fridge", "special_needs",
        "large_propane", "natural_gas", "address",
        "phone", "email", "has_med_training", "know_neighbors",
        "has_neighbor_key", "wants_newsletter",
        "allow_non_disaster_contact", "created_at", "updated_at"
    ]

    record = {fields[i]: row[i] for i in range(len(fields))}
    updated = {}

    print("Press Enter to keep the current value.\n")

    # Required fields
    updated["adults"] = ask_int(
        f"Adults [{record['adults']}]: ",
        allow_blank=True,
        default=record["adults"]
    )
    updated["children"] = ask_int(
        f"Children [{record['children']}]: ",
        allow_blank=True,
        default=record["children"]
    )

    # Pets
    updated["has_pets"] = ask_yes_no(
        f"Has pets? [{yesno(record['has_pets'])}]",
        allow_blank=True,
        default=record["has_pets"]
    )
    if updated["has_pets"]:
        updated["has_dogs"] = ask_yes_no(
            f"Has dogs? [{yesno(record['has_dogs'])}]",
            allow_blank=True,
            default=record["has_dogs"]
        )
    else:
        updated["has_dogs"] = None

    # Medications
    updated["has_critical_meds"] = ask_yes_no(
        f"Critical medications? [{yesno(record['has_critical_meds'])}]",
        allow_blank=True,
        default=record["has_critical_meds"]
    )
    if updated["has_critical_meds"]:
        updated["meds_need_fridge"] = ask_yes_no(
            f"Requires refrigeration? [{yesno(record['meds_need_fridge'])}]",
            allow_blank=True,
            default=record["meds_need_fridge"]
        )
    else:
        updated["meds_need_fridge"] = None

    # Other required fields
    updated["special_needs"] = ask_text(
        f"Special needs [{record['special_needs']}]: ",
        allow_blank=True,
        default=record["special_needs"]
    )
    updated["large_propane"] = ask_yes_no(
        f"Large propane tank? [{yesno(record['large_propane'])}]",
        allow_blank=True,
        default=record["large_propane"]
    )
    updated["natural_gas"] = ask_yes_no(
        f"Natural gas connection? [{yesno(record['natural_gas'])}]",
        allow_blank=True,
        default=record["natural_gas"]
    )
    updated["address"] = ask_text(
        f"Address [{record['address']}]: ",
        allow_blank=True,
        default=record["address"]
    )

    # Optional contact info
    updated["phone"] = ask_phone(
        f"Phone [{record['phone']}]: ",
        allow_blank=True,
        default=record["phone"]
    )
    updated["email"] = ask_email(
        f"Email [{record['email']}]: ",
        allow_blank=True,
        default=record["email"]
    )

    # Optional yes/no fields
    for field in [
        "has_med_training",
        "know_neighbors",
        "has_neighbor_key",
        "wants_newsletter",
        "allow_non_disaster_contact",
    ]:
        old_value = record[field]
        updated[field] = ask_yes_no(
            f"{field.replace('_', ' ').title()} [{yesno(old_value)}]: ",
            allow_blank=True,
            default=old_value
        )

    # Save final updates
    update_household(record_id, updated)

    print("\nRecord updated successfully.")
    press_enter_to_continue()