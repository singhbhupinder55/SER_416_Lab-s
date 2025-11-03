# exercise2.py
# Exercise 2 - Name Formatter
# Author: Bhupinder Singh (bsingh55)
# Description:
#   This program reads a user's first, middle, and last name,
#   and displays three formatted outputs:
#   1. Initials of the name
#   2. "Last Name, First Name, Middle Initial"
#   3. "First Name Middle Name Last Name"
#   It properly handles cases where the middle name is blank or N/A.


def format_name():
    # Step 1: Get user input
    first = input("Enter First Name: ").strip()
    middle = input("Enter Middle Name (leave blank or type N/A if none): ").strip()
    last = input("Enter Last Name: ").strip()

    # Step 2: Handle missing middle name
    has_middle = middle and middle.lower() != "n/a"

    # Step 3: Format outputs
    # 1. Initials
    initials = first[0].upper()
    if has_middle:
        initials += middle[0].upper()
    initials += last[0].upper()

    # 2. Last, First M.
    formatted_name = f"{last}, {first}"
    if has_middle:
        formatted_name += f", {middle[0].upper()}."

    # 3. Full name
    full_name = f"{first} "
    if has_middle:
        full_name += f"{middle} "
    full_name += last

    # Step 4: Print Results
    print("\n--- Name Formats ---")
    print(f"Initials: {initials}")
    print(f"Formatted: {formatted_name}")
    print(f"Full Name: {full_name}")

# Run the function
format_name()