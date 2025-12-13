# Quantitative Risk Analysis – Run Instructions

This project analyzes two mitigation options (A & B) using Python and performs a Monte Carlo simulation to estimate expected schedule delay.

---

### 🔧 Requirements

To run this assignment you must have:

- Python 3 installed
- Dependencies installed:

```bash
pip install numpy matplotlib
```
- (Optional) Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
#### ▶ How to Run the Script
 - Navigate into the project folder and run:
 ```bash
 python3 quant_risk_analysis.py
 ```
 
 #### 📌 Output Generated

Running the script will:
	•	Display expected cost and schedule delay for Option A vs. Option B
	•	Print selection choices based on:
	•	Delay only
	•	Cost only
	•	Bonus consideration
	•	Run a Monte Carlo simulation for Option A delay
	•	Open a graph window showing convergence of expected delay over iterations