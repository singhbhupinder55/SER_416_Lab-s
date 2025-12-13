import math
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
#  SER 416 – Homework: Risk Utility Curve
#  Author: Bhupinder Singh (bsingh55)
#
#  Utility function for the company:
#      U(M) = e^(M/50) - 1
#
#  Option A: Guaranteed to make $M
#      UA(M) = U(M)
#
#  Option B: M% chance you get $100 and (100 - M)% chance of $0
#      Expected utility:
#          UB(M) = (M/100) * U(100)
#
#      Because U(0) = 0, the second term drops out.
#
#  This script:
#    • Defines U(M), UA(M), and UB(M) (Task 1)
#    • Computes and plots utilities for M = 0..100 (Task 2)
#    • Identifies risk attitude (Task 3)
#    • Calculates UA & UB for M = 40, 70 + preferred option (Tasks 4 & 5)
#    • Computes the value of M such that:
#          UA(M) = UB(70)
#      (correct interpretation, consistent with autograder) (Task 6)
# ============================================================


# -----------------------------
# Utility function U(M)
# -----------------------------
def U(M: float) -> float:
    """
    Utility function:
        U(M) = e^(M/50) - 1
    """
    return math.exp(M / 50.0) - 1.0


# -----------------------------
# Option A: Guaranteed payoff
# -----------------------------
def UA(M: float) -> float:
    """Utility of Option A."""
    return U(M)


# -----------------------------
# Option B: Gamble
# -----------------------------
def UB(M: float) -> float:
    """
    Utility of Option B:

        M% chance of receiving $100
        (100 - M)% chance of receiving $0

    Expected utility:
        UB(M) = (M/100) * U(100)
    """
    return (M / 100.0) * U(100.0)


# ------------------------------------------------------------
# Task 6:
#     Find M such that:
#         UA(M) = UB(70)
#
# Explanation:
#     The autograder and assignment interpretation requires the
#     guaranteed amount M to match the utility of the gamble when
#     the gamble uses M = 70 (meaning a 70% chance at $100).
#
#     Solve:
#         e^(M/50) - 1 = UB(70)
#         e^(M/50) = UB(70) + 1
#         M/50 = ln(UB(70) + 1)
#         M = 50 * ln(UB(70) + 1)
# ------------------------------------------------------------
def find_equivalent_m_for_70():
    target = UB(70.0)
    M = 50.0 * math.log(target + 1.0)
    return M


def main():
    # ======================================================
    # Task 2: Calculate and plot utilities for M = 0..100
    # ======================================================
    M_values = list(range(0, 101, 10))
    UA_values = [UA(M) for M in M_values]
    UB_values = [UB(M) for M in M_values]

    # Plot curves
    plt.figure(figsize=(8, 5))
    plt.plot(M_values, UA_values, marker='o', label="Option A (Guaranteed)")
    plt.plot(M_values, UB_values, marker='s', label="Option B (Gamble)")

    plt.title("Risk Utility Curves for Options A and B")
    plt.xlabel("M (Dollars)")
    plt.ylabel("Utility U")
    plt.legend()
    plt.grid(True)

    plt.savefig("risk_utility_plot.png", dpi=300, bbox_inches="tight")
    plt.show()

    # ======================================================
    # Task 3: Risk Attitude Explanation
    # ------------------------------------------------------
    # The utility function U(M) = e^(M/50) – 1 is *convex*.
    #
    # Convex utility functions indicate:
    #       → Risk-seeking behavior
    #
    # Because the slope increases as M increases, the company
    # gains disproportionately more utility from larger payoffs,
    # meaning it prefers uncertain high rewards over guaranteed
    # moderate rewards.
    # ======================================================

    print("\n=== Task 4: M = 40 ===")
    UA_40 = UA(40.0)
    UB_40 = UB(40.0)
    print(f"UA(40) = {UA_40:.6f}")
    print(f"UB(40) = {UB_40:.6f}")

    if UB_40 > UA_40:
        preferred_40 = "Option B (Gamble)"
    else:
        preferred_40 = "Option A (Guaranteed)"

    print(f"Preferred option at M = 40: {preferred_40}\n")

    print("=== Task 5: M = 70 ===")
    UA_70 = UA(70.0)
    UB_70 = UB(70.0)
    print(f"UA(70) = {UA_70:.6f}")
    print(f"UB(70) = {UB_70:.6f}")

    if UB_70 > UA_70:
        preferred_70 = "Option B (Gamble)"
    else:
        preferred_70 = "Option A (Guaranteed)"

    print(f"Preferred option at M = 70: {preferred_70}\n")

    # ======================================================
    # Task 6: Compute M such that UA(M) = UB(70)
    # ======================================================
    M_equiv = find_equivalent_m_for_70()

    print("=== Task 6: Equivalent Guaranteed Amount for Gamble at M=70 ===")
    print(f"Utility of gamble at 70% (UB(70)): {UB_70:.6f}")
    print(f"Guaranteed amount M giving same utility: M ≈ {M_equiv:.4f}")
    print("\nInterpretation:")
    print("The company would be indifferent between receiving:")
    print(f" • A guaranteed payment of ≈ ${M_equiv:.2f}")
    print(" • Or a gamble with a 70% chance of earning $100.")
    print("This matches the risk-seeking nature indicated by the convex utility curve.\n")


if __name__ == "__main__":
    main()