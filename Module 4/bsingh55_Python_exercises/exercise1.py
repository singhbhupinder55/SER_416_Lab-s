# exercise1.py
# Exercise 1 - String Sorting
# Author: Bhupinder Singh (bsingh55)
# Description:
#   This program reads a list of strings from strings.txt,
#   sorts them alphabetically, and writes the sorted list
#   to sorted_strings.txt. The original file remains unchanged.

def sort_strings():
    try:
        # Step 1: Read lines from the file
        with open("strings.txt", "r") as file:
            lines = file.readlines()

        # Step 2: Clean up whitespace/newlines
        cleaned_lines = [line.strip() for line in lines if line.strip()]

        # Step 3: Sort alphabetically (case-insensitive)
        sorted_lines = sorted(cleaned_lines, key=str.lower)

        # Step 4: Write to output file
        with open("sorted_strings.txt", "w") as file:
            for line in sorted_lines:
                file.write(line + "\n")

        print("Strings sorted successfully and saved to sorted_strings.txt")

    except FileNotFoundError:
        print("Error: 'strings.txt' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Run the function
sort_strings()