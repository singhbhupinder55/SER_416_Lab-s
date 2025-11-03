📄 README.txt – HW 3: Decision Making with External Data Input

Course: SER 416
Assignment: HW 3 – Decision Making with External Data Input (Python)
Submitted by: Bhupinder Singh
Date: November 2, 2025

⸻

🔧 Description:

This assignment processes student grade data from both a CSV file and a SQLite database, calculates weighted final scores, and outputs the results to a new CSV file. The logic follows a modular design using functions provided in the starter Python file.

⸻

✅ Features Implemented:
	1.	Data Preparation
	•	Used Python-HW-WeightedSums-Data.csv for Student1–Student3.
	•	Created StudentA_B_Data.csv manually with Student A and B data.
	2.	Database Integration
	•	Imported Student1–Student3 into SQLite database (StudentData.db) under the Students table.
	3.	Data Combination
	•	Read Student A and B from the second CSV file.
	•	Merged both data sources using pandas into a single DataFrame.
	4.	Final Score Calculation
	•	Applied weighted formula:
	•	Quizzes: 15%
	•	Homework: 25%
	•	Team Project: 30%
	•	Final Exam: 30%
	5.	Result Output
	•	Saved final grades to FinalStudentGrades.csv.
	•	Displayed results in tabular format using pandas in terminal.

⸻

💻 How to Run:
	1.	Create and activate virtual environment:
	python3 -m venv .venv  
	source .venv/bin/activate

	2.	Install dependencies:
	pip install -r requirements.txt

	3.	Run the script:
	python3 ExternalDataBase.py

📷 Screenshots Included:
	•	Terminal_Execution_and_DB_Verification.png – shows terminal output and database verification.
	•	Final_CSV_Output_Verification.png – displays contents of the generated CSV file.

