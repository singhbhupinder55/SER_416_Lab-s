import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# SER 416 – Homework: Quantitative Risk Analysis
# Author: Bhupinder Singh (bsingh55)
#
# This script performs:
#   1. Expected cost & schedule delay calculations for
#      Option A and Option B.                (Task 1)
#   2. Compares options based on delay only. (Task 2)
#   3. Compares options based on cost only.  (Task 3)
#   4. Compares options with a $5,000 bonus
#      if there is NO delay.                (Task 4)
#   5. Monte Carlo simulation (>=100 iters)
#      for Option A schedule delay and
#      plots convergence of the estimated
#      expected delay.                      (Task 5)
#
# All calculations are done in Python; NO
# manual pre-computed numbers are used.
# ============================================================


# ------------------------------------------------------------
# 1. Input data – probability distributions
# ------------------------------------------------------------

# ----- Cost impact -----
# Option A: 60% chance of $6,000; 40% chance of $9,000
cost_A = np.array([6000, 9000], dtype=float)
prob_A_cost = np.array([0.60, 0.40], dtype=float)

# Option B: 20% of $4,000; 25% of $6,000; 40% of $8,000; 15% of $12,000
cost_B = np.array([4000, 6000, 8000, 12000], dtype=float)
prob_B_cost = np.array([0.20, 0.25, 0.40, 0.15], dtype=float)

# ----- Schedule impact (weeks of delay) -----
# Option A: 40% chance of 1-week delay; 60% chance of 2-week delay
delay_A = np.array([1, 2], dtype=float)
prob_A_delay = np.array([0.40, 0.60], dtype=float)

# Option B: 20% no delay; 25% 1-week; 40% 2-week; 15% 3-week
delay_B = np.array([0, 1, 2, 3], dtype=float)
prob_B_delay = np.array([0.20, 0.25, 0.40, 0.15], dtype=float)


# ------------------------------------------------------------
# Helper: expected value given outcomes + probabilities
# ------------------------------------------------------------
def expected_value(values: np.ndarray, probs: np.ndarray) -> float:
    """Return sum(values * probs)."""
    return float(np.sum(values * probs))


# ------------------------------------------------------------
# Task 1 – Expected schedule delays & additional costs
# ------------------------------------------------------------
exp_cost_A = expected_value(cost_A, prob_A_cost)
exp_cost_B = expected_value(cost_B, prob_B_cost)

exp_delay_A = expected_value(delay_A, prob_A_delay)
exp_delay_B = expected_value(delay_B, prob_B_delay)

print("\n===== Task 1: Expected Cost and Delay =====")
print(f"Option A - Expected Additional Cost : ${exp_cost_A:,.2f}")
print(f"Option B - Expected Additional Cost : ${exp_cost_B:,.2f}")
print(f"Option A - Expected Schedule Delay  : {exp_delay_A:.3f} weeks")
print(f"Option B - Expected Schedule Delay  : {exp_delay_B:.3f} weeks")
print("===========================================\n")


# ------------------------------------------------------------
# Task 2 – Choice based purely on delay
# ------------------------------------------------------------
print("===== Task 2: Choose Option Based on Delay Only =====")
if exp_delay_A < exp_delay_B:
    preferred_delay = "Option A"
elif exp_delay_B < exp_delay_A:
    preferred_delay = "Option B"
else:
    preferred_delay = "Indifferent (same expected delay)"

print(f"Expected delay (A) = {exp_delay_A:.3f} weeks")
print(f"Expected delay (B) = {exp_delay_B:.3f} weeks")
print(f"Preferred option based on delay only: {preferred_delay}\n")


# ------------------------------------------------------------
# Task 3 – Choice based purely on additional cost
# ------------------------------------------------------------
print("===== Task 3: Choose Option Based on Cost Only =====")
if exp_cost_A < exp_cost_B:
    preferred_cost = "Option A"
elif exp_cost_B < exp_cost_A:
    preferred_cost = "Option B"
else:
    preferred_cost = "Indifferent (same expected cost)"

print(f"Expected cost (A) = ${exp_cost_A:,.2f}")
print(f"Expected cost (B) = ${exp_cost_B:,.2f}")
print(f"Preferred option based on cost only: {preferred_cost}\n")


# ------------------------------------------------------------
# Task 4 – $5,000 bonus if project finishes with NO delay
# ------------------------------------------------------------
BONUS = 5000.0

# Probability of NO delay for each option
# Option A: no "0 week" outcome → probability is 0
prob_no_delay_A = float(np.sum(prob_A_delay[delay_A == 0]))  # = 0.0
# Option B: probability where delay == 0
prob_no_delay_B = float(np.sum(prob_B_delay[delay_B == 0]))

# Expected net cost = expected additional cost - BONUS * P(no delay)
net_cost_A = exp_cost_A - BONUS * prob_no_delay_A
net_cost_B = exp_cost_B - BONUS * prob_no_delay_B

print("===== Task 4: Choice with $5,000 Bonus for No Delay =====")
print(f"Probability of NO delay (A): {prob_no_delay_A:.3f}")
print(f"Probability of NO delay (B): {prob_no_delay_B:.3f}")
print(f"Expected net cost (A) with bonus: ${net_cost_A:,.2f}")
print(f"Expected net cost (B) with bonus: ${net_cost_B:,.2f}")

if net_cost_A < net_cost_B:
    preferred_bonus = "Option A"
elif net_cost_B < net_cost_A:
    preferred_bonus = "Option B"
else:
    preferred_bonus = "Indifferent (same expected net cost)"

print(f"Preferred option with bonus considered: {preferred_bonus}\n")


# ------------------------------------------------------------
# Task 5 – Monte Carlo simulation for Option A delay
# ------------------------------------------------------------
def monte_carlo_delay_option_A(num_iterations: int = 1000):
    """
    Run a Monte Carlo simulation for Option A's schedule delay.

    At each iteration:
      - Randomly sample a delay value according to prob_A_delay.
      - Update running mean of delay.

    Returns:
      delays: array of sampled delays
      running_mean: array of running means (convergence curve)
    """
    # For reproducibility
    np.random.seed(42)

    delays = np.random.choice(delay_A, size=num_iterations, p=prob_A_delay)
    running_mean = np.cumsum(delays) / np.arange(1, num_iterations + 1)
    return delays, running_mean


num_iters = 1000  # >= 100 as required
delays_sampled, running_mean = monte_carlo_delay_option_A(num_iterations=num_iters)

print("===== Task 5: Monte Carlo Simulation (Option A Delay) =====")
print(f"Number of iterations: {num_iters}")
print(f"Final estimated expected delay from simulation: "
      f"{running_mean[-1]:.3f} weeks")
print(f"Analytical expected delay (from Task 1): {exp_delay_A:.3f} weeks")
print("Simulation estimate should be close to analytical value.\n")

# Plot convergence of running mean
plt.figure(figsize=(8, 5))
plt.plot(range(1, num_iters + 1), running_mean)
plt.axhline(y=exp_delay_A, linestyle='--', label="Analytical Expected Delay")
plt.title("Monte Carlo Convergence of Expected Delay – Option A")
plt.xlabel("Number of Iterations")
plt.ylabel("Estimated Expected Delay (weeks)")
plt.legend()
plt.grid(True)

# Save chart for submission
plt.savefig("optionA_delay_convergence.png", dpi=300, bbox_inches="tight")
plt.show()

# End of script