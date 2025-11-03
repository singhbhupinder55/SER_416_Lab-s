# Module 2 – Decision Making with Weighted Sums

This assignment focuses on implementing a decision-making tool using Python that processes student performance data to calculate grades based on weighted components. The logic is implemented programmatically with no hardcoding, and all edge cases are gracefully handled as per the rubric.

## 📄 Files Included

- `WeightedSumBase-bsingh55.py` – Main Python script implementing all required logic.
- `Python-HW-WeightedSums-Data.csv` – Input CSV file containing student scores.
- `HW 2 - Decision Making with Weighted Sums.pdf` – Assignment instructions and rubric.

## ✅ Functionality Implemented

1. **Final Grade Calculation**
   - For each student, their final weighted score is calculated using the following formula:

     ```
     final_score = (quiz / 120) * 15 +
                   (homework / 150) * 25 +
                   (project / 55) * 25 +
                   (final / 80) * 35
     ```

     Grades are printed in the format:  
     `Student X has a grade of Y in the course.`

2. **Final Exam Needed for A**
   - For students with a `0` in the Final Exam column, the script calculates the minimum score needed on the final to achieve an **A** (≥ 90%).

3. **Identify Weakest Area**
   - For each student, the script identifies which assessment (Quizzes, Homework, Team Project, or Final Exam) contributed the least to their final score.

4. **Detect Identical Scores**
   - The script compares all students and detects if any pair has identical scores across all categories.

## 💻 How to Run

Run the Python file with any valid CSV in the same format:

```bash
python WeightedSumBase-bsingh55.py
