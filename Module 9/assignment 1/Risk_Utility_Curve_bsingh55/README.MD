# Risk Utility Curve – How to Run

This project contains the Python script required for the SER 416 Module 9 assignment.  
All explanations and analysis are already included inside the script as comments.

## Requirements

- Python 3
- Virtual environment (recommended)
- Packages:
  - matplotlib
  - numpy

## Setup Instructions

### 1. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate        # Mac/Linux
.\venv\Scripts\activate          # Windows
```

### 2. Install required dependencies
```bash
pip install matplotlib numpy
```

### 3. Run the program
```bash
python3 risk_utility.py
```

## What Happens When You Run It
- A popup window will appear showing the Risk Utility Curve (Option A vs Option B).
- The script automatically saves the graph as:
```bash
risk_utility_plot.png
```
- The terminal will print the required outputs for:
    - UA and UB at M = 40
	- UA and UB at M = 70
	- The value of M where the gamble equals the guaranteed $70

