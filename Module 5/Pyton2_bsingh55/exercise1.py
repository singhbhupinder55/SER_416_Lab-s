"""
Author: Bhupinder Singh
Course: SER 416 - Software Enterprise Projects & Process
Module 5 - Python Exercises 2
Exercise 1: Periodic Payment Calculation (GUI Application)

Description:
This Python script creates a Tkinter-based GUI application to calculate the 
present value of an annuity (Pvann) using the financial formula:

    Pvann = PMT * ((1 - (1 + r)^(-n)) / r)

Where:
- PMT: Periodic Payment
- r: Interest Rate (in decimal form)
- n: Number of Payments

The GUI allows users to:
- Input custom values for PMT, r, and n (with default values prefilled)
- Calculate and display the Pvann result dynamically on the form
- Reset the form to default values using a Reset button

Example:
For PMT = 10000, r = 8%, and n = 20, the output should be approximately 98181.47.
"""


import tkinter as tk
from tkinter import messagebox

def calculate_pvann():
    try:
        # Get user input and convert types
        pmt = float(entry_pmt.get())
        r = float(entry_rate.get()) /100  # Convert percentage to decimal
        n = int(entry_n.get())

        # Ensure rate is already in decimal (not percent)
        # Apply the correct formula (as shown in professor's image):
        pvann = pmt * ((1 - (1 + r) ** -n) / r)

        # Display result rounded to 2 decimal places
        result_label.config(text=f"Pvann = ${pvann:,.2f}", fg="blue")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for all fields.")

def reset_fields():
    entry_pmt.delete(0, tk.END)
    entry_pmt.insert(0, "10000")

    entry_rate.delete(0, tk.END)
    entry_rate.insert(0, "8")  # percent form, converted later to decimal

    entry_n.delete(0, tk.END)
    entry_n.insert(0, "20")

    result_label.config(text="")

# GUI Setup
root = tk.Tk()
root.title("Present Value of Annuity Calculator")

# Labels and Entry fields
tk.Label(root, text="Periodic Payment (PMT):").grid(row=0, column=0, sticky="e")
entry_pmt = tk.Entry(root)
entry_pmt.insert(0, "10000")
entry_pmt.grid(row=0, column=1)

tk.Label(root, text="Interest Rate (r):").grid(row=1, column=0, sticky="e")
entry_rate = tk.Entry(root)
entry_rate.insert(0, "8")  # Decimal, not percent
entry_rate.grid(row=1, column=1)

tk.Label(root, text="Number of Payments (n):").grid(row=2, column=0, sticky="e")
entry_n = tk.Entry(root)
entry_n.insert(0, "20")
entry_n.grid(row=2, column=1)

# Buttons
tk.Button(root, text="Calculate", command=calculate_pvann).grid(row=3, column=0, pady=10)
tk.Button(root, text="Reset", command=reset_fields).grid(row=3, column=1, pady=10)

# Result Display
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.grid(row=4, column=0, columnspan=2)

root.mainloop()