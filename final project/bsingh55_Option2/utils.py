"""
SER 416 – Software Enterprise Projects & Process
Final Project – Option 2 (Developer Route)

Author: Bhupinder Singh (bsingh55)
Date Completed: December 1st 2025

File: utils.py
Purpose:
    This module contains reusable utility functions for improving
    console output formatting and user interaction in the
    CERT Disaster Preparedness Application.

    Functions:
        • print_divider() – Renders a horizontal divider line.
        • press_enter_to_continue() – Pauses execution until
          the user presses Enter.
"""

def print_divider():
    """
    Prints a horizontal divider line used for separating sections
    of the console UI.
    """
    print("-" * 50)


def press_enter_to_continue():
    """
    Pauses program execution so the user can read messages
    before returning to the previous menu.
    """
    input("\nPress Enter to continue...")