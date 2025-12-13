# SER416 – HW Network Diagram Solver  
Critical Path | ES/EF/LS/LF | Float | Multi-Path Detection

This project analyzes a network diagram from CSV input and computes total project duration, float values, and all critical paths — without any hard-coded values.

---

## Files Included
| File | Purpose |
|------|---------|
| `network_diagram_solver.py` | Main CPM solver program |
| `network_analysis_output.csv` | Auto-generated output after execution |
| *Screenshots* | Prob-1 results, Prob-2 results, bad-file validation |

---

## How to Run

```bash
# (Optional) activate virtual environment
source .venv/bin/activate

# Run program
python3 network_diagram_solver.py
```

- You will be prompted to enter a CSV file name, such as:
 - HW9-part1-prob1-1.csv
 - HW9-part1-prob2-1.csv

### Output Generated
- The program automatically creates:
- 📄 network_analysis_output.csv

- At the bottom of the file, the solver also prints:
- Minimum project duration
- List of tasks with zero total float
- All critical path sequences

#### Example:
Minimum project duration: 26 weeks
Critical tasks: start, A, B, C, D, F, G, H, J
Critical paths:
  start -> A -> B -> D -> G -> J
  start -> A -> B -> D -> H -> J
  start -> A -> C -> F -> G -> J

