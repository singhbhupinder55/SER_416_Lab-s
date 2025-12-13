"""
SER 416 – Software Enterprise Projects & Process
Final Project – Option 2 (Developer Route)

Author: Bhupinder Singh (bsingh55)
Date Completed: December 2nd 2025

File: main.py
Purpose:
    This module serves as the entry point and user interface for the CERT
    Disaster Preparedness Application. It displays a console-based menu
    and routes user actions to the appropriate features, including:

        • Viewing household records
        • Adding new household records
        • Importing records from CSV files
        • Exporting records to CSV files

    The main program loop runs until the user selects Quit. This file
    contains no business logic; it merely orchestrates feature calls
    implemented in other modules, keeping the program organized and
    maintainable.
"""

from db import create_tables
from records import add_record, view_records
from io_csv import import_records, export_records
from utils import print_divider


# -----------------------------------------------------------
# MAIN MENU LOOP
# -----------------------------------------------------------
def main_menu():
    """
    Displays the main user menu and routes selections to
    the appropriate application functions.
    """
    while True:
        print_divider()
        print("CERT DISASTER PREPAREDNESS APP")
        print_divider()
        print("1) View Records")
        print("2) Add New Record")
        print("3) Import Records from CSV")
        print("4) Export Records to CSV")
        print("5) Quit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_records()
        elif choice == "2":
            add_record()
        elif choice == "3":
            import_records()
        elif choice == "4":
            export_records()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


# -----------------------------------------------------------
# APPLICATION ENTRY POINT
# -----------------------------------------------------------
def main():
    """
    Initializes the database tables and starts the main menu loop.
    """
    create_tables()
    main_menu()


if __name__ == "__main__":
    main()