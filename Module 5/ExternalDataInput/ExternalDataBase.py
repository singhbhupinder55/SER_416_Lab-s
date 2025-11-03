import pandas as pd
import sqlite3


# Grade Calculation Constants
POINTS_QUIZZES = 120
POINTS_HOMEWORK = 150
POINTS_TEAM_PROJECT = 55
POINTS_FINAL_EXAM = 80

WEIGHT_QUIZ = 0.15
WEIGHT_HOMEWORK = 0.25
WEIGHT_TEAM_PROJECT = 0.25
WEIGHT_FINAL_EXAM = 0.35

def import_to_database(csv_file: str, db_file: str) -> None:
    """
    Imports data for Student1, Student2, and Student3 from a CSV file into an SQLite database.

    """
    # Read CSV
    df = pd.read_csv(csv_file)

    # Filter only first 3 students (based on assignment instructions)
    df = df.head(3)

    # Connect to SQLite
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            Name TEXT,
            Quizzes INTEGER,
            Homework INTEGER,
            [Team Project] INTEGER,
            [Final Exam] INTEGER
        )
    """)

    # Clear old records if any
    cursor.execute("DELETE FROM Students")

    # Insert data row by row
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Students (Name, Quizzes, Homework, [Team Project], [Final Exam])
            VALUES (?, ?, ?, ?, ?)
        """, (row['Name'], row['Quizzes'], row['Homework'], row['Team Project'], row['Final Exam']))

    # Commit and close
    conn.commit()
    conn.close()

def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a pandas DataFrame.
    """
    return pd.read_csv(file_path)


def combine_data(db_file: str, csv_file: str) -> pd.DataFrame:
    """
    Combines data from an SQLite database and a CSV file into a DataFrame.
    """
    # Read from database
    conn = sqlite3.connect(db_file)
    db_df = pd.read_sql_query("SELECT * FROM Students", conn)
    conn.close()

    # Read from CSV
    csv_df = read_csv_file(csv_file)

    # Combine the two DataFrames
    combined_df = pd.concat([db_df, csv_df], ignore_index=True)

    return combined_df

def calculate_final_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the final scores for all students based on the provided weights.
    """
    df["Final Score"] = (
        (df["Quizzes"] / POINTS_QUIZZES) * WEIGHT_QUIZ +
        (df["Homework"] / POINTS_HOMEWORK) * WEIGHT_HOMEWORK +
        (df["Team Project"] / POINTS_TEAM_PROJECT) * WEIGHT_TEAM_PROJECT +
        (df["Final Exam"] / POINTS_FINAL_EXAM) * WEIGHT_FINAL_EXAM
    ) * 100
    df["Final Score"] = df["Final Score"].round(2)
    return df

def save_results(df: pd.DataFrame, output_file: str) -> None:
    """
    Saves the final results to a CSV file.
    """
    df.to_csv(output_file, index=False)

def main():
    """
    The main function, used to grab the data and pass it to
    your answer functions. You are not expected to edit this
    as part of the assignment. Feel free to edit it if needed
    while testing, but remember that the graders will be using
    this exact version when grading your answers.
    :return:
    """
    # File paths in the project directory
    first_csv_file = "Python-HW-WeightedSums-Data.csv"
    second_csv_file = "StudentA_B_Data.csv"
    db_file = "StudentData.db"

    try:
        import_to_database(first_csv_file, db_file)
        combined_data = combine_data(db_file, second_csv_file)
        final_results = calculate_final_scores(combined_data)
        save_results(final_results, "FinalStudentGrades.csv")

        # Display the final results
        print("Final Grades:\n")
        print(final_results.to_string(index=False))
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")

# Execute the main function when the script is run
if __name__ == "__main__":
    main()
