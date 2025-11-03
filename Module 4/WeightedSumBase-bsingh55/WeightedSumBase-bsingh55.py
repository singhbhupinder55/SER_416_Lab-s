import csv

# Some constants from the assignment description
POINTS_POSIBLE_QUIZZES = 120
POINTS_POSSIBLE_HOMEWORK = 150
POINTS_POSSIBLE_TEAM_PROJECT = 55
POINTS_POSSIBLE_FINAL_EXAM = 80
WEIGHT_QUIZ = 0.15
WEIGHT_HOMEWORK = 0.25
WEIGHT_TEAM_PROJECT = 0.25
WEIGHT_FINAL_EXAM = 0.35

# If you renamed the file you will need to update this to match
FILE_NAME = "Python-HW-WeightedSums-Data.csv"


def csv_read() -> list:
    """
        Reads the data from the csv and compiles it into a LIST OF DICTIONARIES!
        This means every entry in the list is a dict which can be accessed like a map from Java
        Each entry in the list will be one student from the data
        Each key in the dicts will be the columns names from the csv (name, and the four asessments)
        Example: print(results[0]["Name"]) would print "Student 1"

        You are NOT expected to edit this function at all

    :return: The list of dicts of student data
    """
    with open(FILE_NAME, 'r') as data:
        csv_reader = csv.DictReader(data)
        results = [row for row in csv_reader]
    return results

def question_one_grade_calculation(data) -> None:
    for student in data:
        name = student["Name"]
        quizzes = int(student["Quizzes"])
        homework = int(student["Homework"])
        team_project = int(student["Team Project"])
        final_exam = int(student["Final Exam"])

        # Calculate weighted score
        weighted_score = (
            (quizzes/ POINTS_POSIBLE_QUIZZES) * WEIGHT_QUIZ + 
            (homework/POINTS_POSSIBLE_HOMEWORK) * WEIGHT_HOMEWORK +
            (team_project/POINTS_POSSIBLE_TEAM_PROJECT) * WEIGHT_TEAM_PROJECT +
            (final_exam/POINTS_POSSIBLE_FINAL_EXAM) * WEIGHT_FINAL_EXAM
        )

        final_percent = weighted_score * 100
        print(f"{name} has a grade of {final_percent:.2f} in the course.")



def question_two_grade_needed_on_final(data) -> None:
    any_student_needs_final = False

    for student in data:
        name = student["Name"]
        quizzes = int(student["Quizzes"])
        homework = int(student["Homework"])
        team_project = int(student["Team Project"])
        final_exam = int(student["Final Exam"])

        # Check if student does not have a final exam score
        if final_exam == 0:
            any_student_needs_final = True

            # Calculate how much weighted percentage student already has (excluding final)
            current_weighted_score = (
                (quizzes / POINTS_POSIBLE_QUIZZES) * WEIGHT_QUIZ +
                (homework / POINTS_POSSIBLE_HOMEWORK) * WEIGHT_HOMEWORK +
                (team_project / POINTS_POSSIBLE_TEAM_PROJECT) * WEIGHT_TEAM_PROJECT
            )

            # Subtract from 90% (0.90) and solve for required final_exam score
            required_score_fraction = (0.90 - current_weighted_score) / WEIGHT_FINAL_EXAM
            required_final_exam_score = required_score_fraction * POINTS_POSSIBLE_FINAL_EXAM

            if required_final_exam_score > POINTS_POSSIBLE_FINAL_EXAM:
                print(f"{name} cannot get an A in the course.")
            else:
                print(f"{name} needs a score of at least {required_final_exam_score:.2f} on the final to get an A.")

    if not any_student_needs_final:
        print("All students have a Final score.")

def question_three_weakness(data) -> None:
    for student in data:
        name = student["Name"]
        quizzes = int(student["Quizzes"])
        homework = int(student["Homework"])
        team_project = int(student["Team Project"])
        final_exam = int(student["Final Exam"])

        # Calculate weighted earned scores
        earned_quiz = (quizzes / POINTS_POSIBLE_QUIZZES) * WEIGHT_QUIZ
        earned_homework = (homework / POINTS_POSSIBLE_HOMEWORK) * WEIGHT_HOMEWORK
        earned_project = (team_project / POINTS_POSSIBLE_TEAM_PROJECT) * WEIGHT_TEAM_PROJECT
        earned_final = (final_exam / POINTS_POSSIBLE_FINAL_EXAM) * WEIGHT_FINAL_EXAM

        # Calculate weighted losses
        lost_quiz = WEIGHT_QUIZ - earned_quiz
        lost_homework = WEIGHT_HOMEWORK - earned_homework
        lost_project = WEIGHT_TEAM_PROJECT - earned_project
        lost_final = WEIGHT_FINAL_EXAM - earned_final

        losses = {
            "Quizzes": lost_quiz,
            "Homework": lost_homework,
            "Team Project": lost_project,
            "Final Exam": lost_final
        }

        max_loss = max(losses.values())
        loss_sources = [k for k, v in losses.items() if abs(v - max_loss) < 1e-6]  # Handles floating point tie

        if all(abs(v) < 1e-6 for v in losses.values()):
            print(f"{name} got a perfect score in the course.")
        elif len(loss_sources) > 1:
            print(f"{name} had multiple areas that held them back.")
        else:
            print(f"{name} lost the most score in {loss_sources[0]}.")

def question_four_equal_students(data) -> None:
    found_match = False

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            s1 = data[i]
            s2 = data[j]

            if (
                s1["Quizzes"] == s2["Quizzes"] and
                s1["Homework"] == s2["Homework"] and
                s1["Team Project"] == s2["Team Project"] and
                s1["Final Exam"] == s2["Final Exam"]
            ):
                print(f"Match found: {s1['Name']} and {s2['Name']} have the same scores.")
                found_match = True
                return  # stop after first match, as per instructions

    if not found_match:
        print("No matches found: No students had matching scores.")

def main() -> None:
    """
    The main function, used to grab the data and pass it to
    your answer functions. You are not expected to edit this
    as part of the assignment. Feel free to edit it if needed
    while testing, but remember that the graders will be using
    this exact version when grading your answers.
    :return:
    """
    data = csv_read()
    question_one_grade_calculation(data)
    question_two_grade_needed_on_final(data)
    question_three_weakness(data)
    question_four_equal_students(data)

# Run main automatically if this file is run directly - DO NOT EDIT
if __name__ == '__main__':
    main()
