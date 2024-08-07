import tkinter as tk
from tkinter import ttk, messagebox


def open_debt_calculator(root):
    top = tk.Toplevel(root)
    top.title("Debt Payoff Calculator")
    top.geometry("400x400")  # Make the window larger

    ttk.Label(top, text="Select Credit Card:").pack(padx=10, pady=5)
    card_options = ["Apple Credit Card", "Amex", "Discover Credit Card"]
    card_combobox = ttk.Combobox(top, values=card_options, font=("Helvetica", 12))
    card_combobox.pack(padx=10, pady=5)
    card_combobox.set(card_options[0])

    ttk.Label(top, text="Debt Amount:").pack(padx=10, pady=5)
    debt_amount_entry = ttk.Entry(top, font=("Helvetica", 12))
    debt_amount_entry.pack(padx=10, pady=5)

    ttk.Label(top, text="Monthly Contribution:").pack(padx=10, pady=5)
    contribution_entry = ttk.Entry(top, font=("Helvetica", 12))
    contribution_entry.pack(padx=10, pady=5)

    ttk.Label(top, text="Annual Interest Rate (%):").pack(padx=10, pady=5)
    interest_rate_entry = ttk.Entry(top, font=("Helvetica", 12))
    interest_rate_entry.pack(padx=10, pady=5)

    result_label = ttk.Label(top, text="", font=("Helvetica", 12, "bold"))
    result_label.pack(padx=10, pady=10)

    def calculate_payoff_time():
        try:
            debt_amount = float(debt_amount_entry.get())
            monthly_contribution = float(contribution_entry.get())
            annual_interest_rate = float(interest_rate_entry.get()) / 100
            if monthly_contribution <= 0:
                raise ValueError("Contribution must be greater than 0")

            monthly_interest_rate = annual_interest_rate / 12
            months = 0

            while debt_amount > 0:
                interest = debt_amount * monthly_interest_rate
                debt_amount += interest - monthly_contribution
                months += 1
                if months > 1000:  # Break the loop if it takes too long
                    result_label.config(
                        text=f"It will take more than 1000 months to pay off the {card_combobox.get()}.")
                    return

            result_label.config(text=f"It will take {months} months to pay off the {card_combobox.get()}.")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for all fields")

    ttk.Button(top, text="Calculate", command=calculate_payoff_time).pack(pady=10)
