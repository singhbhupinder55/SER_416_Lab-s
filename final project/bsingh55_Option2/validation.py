"""
SER 416 – Software Enterprise Projects & Process
Final Project – Option 2 (Developer Route)

Author: Bhupinder Singh (bsingh55)
Date Completed: December 4th 2025

File: validation.py
Purpose:
    Provides reusable input validation functions for safely collecting
    user data in the CERT Disaster Preparedness Application.

    Functions:
        • ask_int()      – Validated integer input with range support.
        • ask_yes_no()   – Yes/No prompts with optional defaults.
        • ask_text()     – Generic text input with optional blank.
        • ask_email()    – Basic email format validation.
        • ask_phone()    – Basic phone number validation (10–15 digits).
"""


def ask_int(prompt, allow_blank=False, min_value=None, max_value=None, default=None):
    """
    Asks the user for an integer with validation.

    Parameters:
        prompt (str)        – The input prompt shown to the user.
        allow_blank (bool)  – If True, user may press Enter to return default.
        min_value (int)     – Minimum allowed value (optional).
        max_value (int)     – Maximum allowed value (optional).
        default (int)       – Returned when blank is allowed.

    Returns:
        int or None – A validated integer or default value.
    """
    while True:
        val = input(prompt).strip()

        if allow_blank and val == "":
            return default

        if not val.isdigit():
            print("Please enter a valid number.")
            continue

        num = int(val)

        if min_value is not None and num < min_value:
            print(f"Value must be at least {min_value}.")
            continue

        if max_value is not None and num > max_value:
            print(f"Value must be no more than {max_value}.")
            continue

        return num


def ask_yes_no(prompt, allow_blank=False, default=None):
    """
    Asks a yes/no question and returns True or False.

    Parameters:
        prompt (str)        – Message shown to the user.
        allow_blank (bool)  – If True, blank returns default.
        default (bool)      – Returned when blank is allowed.

    Returns:
        bool or None
    """
    while True:
        val = input(prompt + " (yes/no): ").strip().lower()

        if allow_blank and val == "":
            return default

        if val in ["y", "yes"]:
            return True
        if val in ["n", "no"]:
            return False

        print("Please answer yes or no.")


def ask_text(prompt, allow_blank=False, default=None):
    """
    Collects a text response from the user.

    Parameters:
        prompt (str)        – Displayed prompt.
        allow_blank (bool)  – If True, blank returns default.
        default (str)       – Default value when blank.

    Returns:
        str
    """
    while True:
        val = input(prompt).strip()

        if allow_blank and val == "":
            return default

        if val == "":
            print("Please enter a value.")
            continue

        return val


def ask_email(prompt, allow_blank=False, default=None):
    """
    Validates basic email formatting.

    Parameters:
        prompt (str)
        allow_blank (bool)
        default (str)

    Returns:
        str or None
    """
    while True:
        val = input(prompt).strip()

        if allow_blank and val == "":
            return default

        if "@" in val and "." in val:
            return val

        print("Please enter a valid email address.")


def ask_phone(prompt, allow_blank=False, default=None):
    """
    Validates a phone number based on digit count (10–15 digits).

    Parameters:
        prompt (str)
        allow_blank (bool)
        default (str)

    Returns:
        str or None
    """
    while True:
        val = input(prompt).strip()

        if allow_blank and val == "":
            return default

        digits = "".join(ch for ch in val if ch.isdigit())

        if 10 <= len(digits) <= 15:
            return val

        print("Please enter a valid phone number (10–15 digits).")