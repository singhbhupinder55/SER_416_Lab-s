# Earned Value Analysis – Interpretation  
**Author:** Bhupinder Singh (bsingh55)  
**Course:** SER 416 – Module 8  
**Assignment:** Homework – Earned Value Analysis  

All values and observations below are based on the **EVA_Analysis.csv** file generated from the PV, AC, and EV data for **Modules A and B** over **weeks 1–7**.

## A. Weeks When the Project Was Ahead of Schedule (SPI > 1)

A project is considered **ahead of schedule** when the **Schedule Performance Index (SPI)** is **greater than 1.0**, meaning more work was earned (EV) than planned (PV) for that week.

Based on the EVA results, the following weeks show **SPI > 1**:

### **Module A**
- **Module A – Task 2**
  - **Week 2:** SPI = **1.021**
  - **Week 3:** SPI = **1.906**
  - **Week 4:** SPI = **4.043**
  - **Week 5:** SPI = **1.838**

- **Module A – Task 3**
  - **Week 3:** SPI = **1.636**
  - **Week 4:** SPI = **1.246**
  - **Week 5:** SPI = **2.25**
  - **Week 6:** SPI = **3.032**

### **Module B**
- **Module B – Task 1**
  - **Week 4:** SPI = **1.133**
  - **Week 6:** SPI = **2.583**
  - **Week 7:** SPI = **10.333**

- **Module B – Task 2**
  - **Week 7:** SPI = **3.0**

### **Reasoning**
In all the weeks listed above, the EV (Earned Value) exceeded the PV (Planned Value), which mathematically results in **SPI = EV ÷ PV > 1**.  
This indicates that the work completed by those weeks was greater than what the project plan expected, meaning the schedule was ahead during those periods.


## B. Weeks When the Project Was Under Budget (CPI > 1)

A project is considered **under budget** when the **Cost Performance Index (CPI)** is **greater than 1.0**.  
This means the project is earning more value (EV) per dollar spent (AC), indicating cost efficiency.

Based on the EVA results, the following weeks show **CPI > 1**:

---

### **Module A**

#### **Module A – Task 2**
- **Week 2:** CPI = **2.45**
- **Week 3:** CPI = **2.144**
- **Week 4:** CPI = **3.593**
- **Week 5:** CPI = **1.838**

#### **Module A – Task 3**
- **Week 3:** CPI = **1.385**
- **Week 4:** CPI = **1.246**
- **Week 5:** CPI = **1.385**
- **Week 6:** CPI = **3.032**

---

### **Module B**

#### **Module B – Task 1**
- **Week 4:** CPI = **1.31**
- **Week 5:** CPI = **0.861** *(not under budget, ignore)*
- **Week 6:** CPI = **3.321**
- **Week 7:** CPI = **5.167**

#### **Module B – Task 2**
- **Week 5:** CPI = **0.0** *(not under budget)*
- **Week 6:** CPI = **0.625** *(not under budget)*
- **Week 7:** CPI = **3.0**

---

### **Reasoning**

All weeks listed above have **CPI > 1**, meaning:
- The **EV (Earned Value)** was **greater than the AC (Actual Cost)**.
- The teams delivered more value than the money spent.
- These weeks represent periods of **cost efficiency** and **under-budget performance**.


## C. End-of-Week-7 Project Status (Schedule + Cost Summary)

At the end of **Week 7**, the overall project status can be evaluated using the EVA metrics:  
**SPI**, **CPI**, **SV**, and **CV**.

Below is a clear summary based on all Week-7 rows in the EVA_Analysis.csv dataset.

---

### **1. Schedule Status (SPI)**  
- A project is **ahead of schedule** when **SPI > 1**.  
- A project is **behind schedule** when **SPI < 1**.

From Week-7 data:
- **Module A – Task 1:** SPI = 0.0 → behind schedule  
- **Module A – Task 2:** SPI = 1.0 → on schedule  
- **Module A – Task 3:** SPI = 0.0 → behind schedule  
- **Module B – Task 1:** SPI = **10.333** → *significantly* ahead of schedule  
- **Module B – Task 2:** SPI = **3.0** → ahead of schedule  

**Overall Schedule Summary:**
- **Module A** ends the project **behind or just on schedule** (mostly SPI = 0 or 1).  
- **Module B** ends **far ahead of schedule**, with very high SPI values at Week 7.

**Final Schedule Verdict:**  
➡️ **The project is ahead of schedule overall** because Module B’s extremely high earned value pushes the final SPI upward.

---

### **2. Cost Status (CPI)**  
- A project is **under budget** when **CPI > 1**.  
- A project is **over budget** when **CPI < 1**.

Week-7 data:
- **Module A – Task 1:** CPI = 0.0 → over budget  
- **Module A – Task 2:** CPI = 1.0 → on budget  
- **Module A – Task 3:** CPI = 0.0 → over budget  
- **Module B – Task 1:** CPI = **5.167** → under budget  
- **Module B – Task 2:** CPI = **3.0** → under budget  

**Overall Cost Summary:**
- **Module A** ends **on or over budget**, depending on the task.  
- **Module B** ends **strongly under budget**, with very efficient spending.

**Final Cost Verdict:**  
➡️ **The project is under budget overall**, primarily driven by Module B’s strong cost performance.

---

### **3. Variances (CV & SV)**  
Week-7 examples:
- **Module A – Task 1:**  
  - CV = 0.0 → cost-neutral  
  - SV = 0.0 → schedule-neutral  
- **Module A – Task 3:**  
  - CV = 0.0  
  - SV = 0.0  
- **Module B – Task 1:**  
  - CV = **2500** → under budget  
  - SV = **2800** → ahead of schedule  

**Interpretation:**
- Module A’s variances are flat because EV = PV = AC = 0 in Week 7 for those tasks.  
- Module B shows **large positive variances**, which confirms it is ahead of schedule and under budget.

---

## **Final Summary (End of Week 7)**

- **Schedule Status:**  
  ✔️ **Ahead of schedule**  
  Driven by very high SPI values in Module B (SPI = 10.333, 3.0).

- **Cost Status:**  
  ✔️ **Under budget**  
  Supported by strong CPI values in Module B (CPI = 5.167, 3.0).

- **Overall Interpretation:**  
  Even though **Module A** ended at or behind schedule with poor cost performance,  
  **Module B’s exceptional efficiencies** dominate the total project outcome, making the project overall **ahead of schedule and under budget** at the end of Week 7.


## D. Module A vs. Module B Performance Comparison  
### (Schedule Adherence & Cost Management)

To determine which team performed better, we compare **SPI, CPI, SV, and CV** across all tasks in **Module A** and **Module B**.

---

## 1. Schedule Performance (SPI)

### **Module A – SPI Summary**
- Most SPI values are **0.0 – 1.0**
- Only a few weeks show SPI > 1:
  - Module A – Task 2 (Weeks 2–5): SPI values of **1.021**, **1.906**, **4.043**, **1.838**
- Week 7 SPI:
  - Task 1: **0.0**
  - Task 2: **1.0**
  - Task 3: **0.0**

**Schedule Interpretation – Module A:**  
Module A frequently falls **behind or barely on schedule**, except for a few strong weeks in Task 2.

---

### **Module B – SPI Summary**
- Many SPI values are **significantly > 1**:
  - Module B – Task 1 (Week 7): **SPI = 10.333**
  - Module B – Task 1 (Week 5): **SPI = 1.364**
  - Module B – Task 2 (Week 6): **SPI = 0.536**
  - Module B – Task 2 (Week 7): **SPI = 3.0**

**Schedule Interpretation – Module B:**  
Module B consistently performs **ahead of schedule**, especially in Weeks 1, 2, 5, and 7 where SPI is extremely high.

---

## **Schedule Verdict:**  
### ✔ **Module B performs significantly better than Module A**  
Module B repeatedly achieves **SPI > 1**, indicating strong schedule efficiency.  
Module A frequently stays at **SPI ≤ 1**, with only brief exceptions.

---

## 2. Cost Performance (CPI)

### **Module A – CPI Summary**
- Many CPI values are **0.0** for tasks where EV = 0  
- When actual work exists:
  - Module A – Task 2 CPI values: **1.021**, **2.144**, **3.593**, **1.838**
  - Module A – Task 3 CPI values: **1.385**, **1.246**, **1.385**, **1.932**

**Cost Interpretation – Module A:**  
Module A has mixed performance:  
- Some weeks are **under budget (CPI > 1)**  
- Many weeks show no earned value → **CPI = 0**, which is poor performance

---

### **Module B – CPI Summary**
- Consistently stronger CPI values:
  - Module B – Task 1 Week 7: **CPI = 5.167**
  - Module B – Task 1 Week 6: **CPI = 3.321**
  - Module B – Task 1 Week 5: **CPI = 0.861** (slightly over budget)
  - Module B – Task 2 Week 7: **CPI = 3.0**
  - Module B – Task 2 Week 6: **CPI = 0.625**

**Cost Interpretation – Module B:**  
Module B repeatedly achieves **CPI > 1**, signaling **strong cost efficiency**.  
Even in weaker weeks, CPI rarely drops to zero like Module A.

---

## **Cost Verdict:**  
### ✔ **Module B outperforms Module A in cost management**  
Module B shows consistently high CPI values and fewer losses in earned value.  
Module A has more irregular cost efficiency and many weeks of ineffective spending.

---

## Final Team Performance Conclusion

### 🟩 **Winner: Module B Team**  
Module B **clearly performed better** in:

- **Schedule adherence**  
  (Higher SPI values, ahead of schedule in most weeks)

- **Cost management**  
  (Higher CPI values, significantly under budget in final weeks)

### 🟥 Module A Performance Summary
- Frequently **on or behind schedule**
- Many periods of **zero earned value work**
- Cost efficiency is inconsistent

### 🟩 Module B Performance Summary
- Repeatedly **ahead of schedule**, especially Week 7  
- Strong cost performance with CPI values up to **5.167**  
- More stable and reliable earned value production

**Overall Judgment:**  
➡️ **The Module B team performed significantly better than Module A in both schedule and cost performance.**


## E. Why TCPI Is High in Weeks 5 and 6  
### (Interpretation Based on AC, EV, and PV Trends)

During Weeks 5 and 6, the TCPI (To-Complete Performance Index) rises sharply for several tasks. A high TCPI indicates that, in order to meet the original budget at completion (BAC), the team would need to perform far more efficiently going forward.

This occurs because of the relationship between **AC**, **EV**, and **BAC** at those points.

---

## 1. **High TCPI Means:**
### \[
\text{TCPI} = \frac{BAC - EV}{BAC - AC}
\]

A **high numerator** (BAC − EV) combined with a **small denominator** (BAC − AC) produces a large TCPI value.  
This situation happens when:
- **EV (earned value) is low** → very little work has been achieved  
- **AC (actual cost) is high** → a lot of money has already been spent  
- **BAC remains fixed** → the remaining work must be done with less budget left  

Weeks **5 and 6** match this situation.

---

## 2. **What Happens in Week 5**
### Example: Module B – Task 2 (Week 5)
- **PV = 300**  
- **AC = 400**  
- **EV = 0**  
- **BAC = 1500**

**Interpretation:**
- The team spent **$400**, but achieved **$0 worth of progress** (EV = 0).  
- The remaining allowed cost = BAC − AC = **1100**, which is shrinking.  
- Remaining work (BAC − EV) = **1500**, still very large.

Therefore:

\[
TCPI = \frac{1500 - 0}{1500 - 400} = \frac{1500}{1100} \approx 1.364
\]

➡️ **The team must perform 36% more efficiently than originally planned to catch up.**

---

## 3. **What Happens in Week 6**
### Example: Module B – Task 2 (Week 6)
- **PV = 700**  
- **AC = 600**  
- **EV = 375**  
- **BAC = 1500**

Even though EV improved slightly, cost is still high relative to progress.

\[
TCPI = \frac{1500 - 375}{1500 - 600}
       = \frac{1125}{900}
       = 1.25
\]

➡️ The team needs **25% better performance** per dollar spent to reach the target BAC.

---

## 4. **General Pattern in Weeks 5–6**

Across both Module A and Module B, Weeks 5 and 6 commonly show:

### **1. AC increases sharply**
- The teams spent a major portion of their budget by Week 5–6.
- Example: AC values often rise to **650, 900, 1300, 2000**, etc.

### **2. EV grows slowly or remains at zero**
- Many tasks show **EV = 0** even after large spending.
- In some tasks, EV lags far behind PV.

### **3. PV plans more work than teams delivered**
- Planned value increases significantly in Weeks 5–6, but actual progress does not keep pace.

---

## 5. **Final Explanation**

### **TCPI becomes high in Weeks 5 and 6 because:**
- **Costs are increasing faster than value earned (AC ↑↑, EV ↑ or EV = 0)**  
- **Work is behind schedule relative to what was planned (PV > EV)**  
- **The remaining budget (BAC − AC) is shrinking too quickly**

This combination forces the project into a position where, to finish within the original BAC, the team would need to perform **much more efficiently** for the remaining duration—thus producing the **high TCPI values**.

---

### ✔ Summary  
**Weeks 5 and 6 show high TCPI because the project is simultaneously behind schedule (low EV) and over budget (high AC), while still having a fixed total work target (BAC).**  
As a result, the remaining work must be completed with **less money and higher efficiency**, leading directly to **elevated TCPI values**.