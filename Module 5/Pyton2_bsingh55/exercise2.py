"""
Author: Bhupinder Singh
Course: SER 416 - Software Enterprise Projects & Process
Module 5 - Python Exercises 2
Exercise 2: Student Class Standing

Description:
This program defines a Student class that represents a student’s basic information 
and determines their class standing based on the total number of credit hours earned.

The program demonstrates the following:
1. Encapsulation using private attributes (first_name, last_name, credits)
2. Methods for adding credit hours and determining class standing
3. A driver program that creates multiple Student objects with predefined data
4. A neatly formatted table displaying each student’s name, credits, and standing

Class Standing Criteria:
- Freshman: 24 or fewer credits
- Sophomore: 25 to 55 credits
- Junior: 56 to 86 credits
- Senior: 87 or more credits

Expected Output Example:
---------------------------------------------------------
Student Name         Credits    Class Standing
---------------------------------------------------------
Alice Johnson        20         Freshman
Brian Smith          40         Sophomore
Carla Lopez          75         Junior
David Kim            100        Senior
---------------------------------------------------------
"""

class Student:
    def __init__(self, first_name, last_name, credits=0):
        # Private attributes
        self.__first_name = first_name
        self.__last_name = last_name
        self.__credits = credits

    def add_credits(self, amount):
        """Add credit hours to the student’s record."""
        if amount < 0:
            print("Error: Credit hours cannot be negative.")
        else:
            self.__credits += amount

    def get_class_standing(self):
        """Return the class standing based on the number of credits earned."""
        if self.__credits <= 24:
            return "Freshman"
        elif 25 <= self.__credits <= 55:
            return "Sophomore"
        elif 56 <= self.__credits <= 86:
            return "Junior"
        else:
            return "Senior"

    def get_full_name(self):
        """Return the student’s full name."""
        return f"{self.__first_name} {self.__last_name}"

    def get_credits(self):
        """Return the total credits earned."""
        return self.__credits


# -------- DRIVER PROGRAM -------- #
def main():
    # Create Student objects with distinct credit ranges
    students = [
        Student("Alice", "Johnson", 20),   # Freshman
        Student("Brian", "Smith", 40),     # Sophomore
        Student("Carla", "Lopez", 75),     # Junior
        Student("David", "Kim", 100)       # Senior
    ]

    # Print header
    print("{:<20} {:<10} {:<15}".format("Student Name", "Credits", "Class Standing"))
    print("-" * 50)

    # Print each student's info
    for s in students:
        print("{:<20} {:<10} {:<15}".format(
            s.get_full_name(), s.get_credits(), s.get_class_standing()
        ))

    print("-" * 50)


if __name__ == "__main__":
    main()