# exercise3.py
# Exercise 3 - Multiplication Quiz
# Author: Bhupinder Singh (bsingh55)
# Description:
#   This program prompts the user for number of multiplication questions.
#   Generates random problems (1-15), validates input, gives feedback,
#   and shows final score. All input is validated as required.

import random

def get_valid_integer(prompt):
    """Keeps prompting until the user enters a valid integer."""
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if value <= 0:
                print("❌ Please enter a positive whole number.")
            else:
                return value
        except ValueError:
            print("❌ Invalid input. Please enter a whole number.")

def multiplication_quiz():
    print("--Welcome to the Multiplication Quiz!--")

    # Step 1: Ask for valid number of questions
    total_questions = get_valid_integer("How many questions would you like to attempt? ")

    correct_count = 0

    # Step 2: Loop through each question
    for i in range(1, total_questions + 1):
        num1 = random.randint(1, 15)
        num2 = random.randint(1, 15)
        correct_answer = num1 * num2

        # Step 3: Keep prompting until valid integer is entered
        while True:
            user_input = input(f"Q{i}: What is {num1} × {num2}? ")
            try:
                user_answer = int(user_input)
                break
            except ValueError:
                print("❌ Invalid input. Please enter a number.")

        # Step 4: Check if answer is correct
        if user_answer == correct_answer:
            print("✅ Correct!\n")
            correct_count += 1
        else:
            print(f"❌ Incorrect. The correct answer is {correct_answer}.\n")

    # Step 5: Final result
    print("🎉 Quiz Finished!")
    print(f"You answered {correct_count} out of {total_questions} questions correctly.")

# Run the quiz
if __name__ == "__main__":
    multiplication_quiz()