import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd

FEDERAL_TAX_RATE = 0.22
STATE_TAX_RATES = {
    "Massachusetts": 0.05,
    "Florida": 0.0,
}

# Global variables
total_expenses = 0
monthly_income_after_taxes = 0
remaining_amount = 0
total_label = None
remaining_label = None


def configure_styles():
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
    style.configure("Treeview", rowheight=25, font=("Helvetica", 12), background="#f0f8ff", fieldbackground="#f0f8ff")


def setup_income_input_fields(root, calculate_income_callback):
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill=tk.X)

    salary_label = ttk.Label(frame, text="Annual Salary:")
    salary_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    salary_entry = ttk.Entry(frame, font=("Helvetica", 12))
    salary_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

    state_label = ttk.Label(frame, text="State:")
    state_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    state_combobox = ttk.Combobox(frame, values=list(STATE_TAX_RATES.keys()), font=("Helvetica", 12))
    state_combobox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

    calculate_income_button = ttk.Button(frame, text="Calculate Income After Taxes", command=calculate_income_callback)
    calculate_income_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    frame.columnconfigure(1, weight=1)  # Make the second column expandable

    return salary_entry, state_combobox


def setup_buttons(root, add_expense_callback, open_debt_calculator_callback):
    frame = tk.Frame(root, padx=20, pady=10)
    frame.pack(fill=tk.X)

    add_expense_button = ttk.Button(frame, text="Add Expense", command=add_expense_callback)
    add_expense_button.pack(side=tk.LEFT, padx=5)

    debt_calculator_button = ttk.Button(frame, text="Debt Payoff Calculator", command=open_debt_calculator_callback)
    debt_calculator_button.pack(side=tk.LEFT, padx=5)


def setup_prebuilt_table(root):
    frame = tk.Frame(root, padx=20, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("Expense", "Cost"), show='headings', height=9)  # Adjust height as needed
    tree.heading("Expense", text="Expense")
    tree.heading("Cost", text="Cost")
    tree.column("Expense", anchor=tk.W, width=300)
    tree.column("Cost", anchor=tk.E, width=150)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    expenses = ["Rent", "Car Insurance", "Groceries", "Utilities", "Savings", "Electricity", "Internet",
                "Miscellaneous", "Send to Dad"]
    for expense in expenses:
        tree.insert("", "end", values=(expense, "$0.00"))

    return tree


def setup_total_label(root):
    frame = tk.Frame(root, padx=20, pady=10)
    frame.pack(fill=tk.X)

    global total_label
    total_label = ttk.Label(frame, text="Total Expenses: $0.00", font=("Helvetica", 14, "bold"))
    total_label.pack(anchor=tk.E)


def setup_remaining_label(root):
    frame = tk.Frame(root, padx=20, pady=10)
    frame.pack(fill=tk.X)

    global remaining_label
    remaining_label = ttk.Label(frame, text="Remaining Amount: $0.00", font=("Helvetica", 14, "bold"))
    remaining_label.pack(anchor=tk.E)


def setup_export_button(root, export_callback):
    frame = tk.Frame(root, padx=20, pady=10)
    frame.pack(fill=tk.X)

    export_button = ttk.Button(frame, text="Export to Excel", command=export_callback)
    export_button.pack(anchor=tk.E)


def update_remaining_amount():
    global remaining_amount, remaining_label, monthly_income_after_taxes, total_expenses
    remaining_amount = monthly_income_after_taxes - total_expenses
    if remaining_label is not None:
        remaining_label.config(text=f"Remaining Amount: ${remaining_amount:.2f}")


def calculate_income_after_taxes(salary_entry, state_combobox):
    global monthly_income_after_taxes
    try:
        annual_salary = float(salary_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid annual salary")
        return

    state = state_combobox.get()
    if state not in STATE_TAX_RATES:
        messagebox.showerror("Invalid input", "Please select a valid state")
        return

    federal_tax = annual_salary * FEDERAL_TAX_RATE
    state_tax = annual_salary * STATE_TAX_RATES[state]
    annual_income_after_taxes = annual_salary - federal_tax - state_tax
    monthly_income_after_taxes = annual_income_after_taxes / 12

    messagebox.showinfo("Income After Taxes", f"Your monthly income after taxes is: ${monthly_income_after_taxes:.2f}")
    update_remaining_amount()


def on_double_click(event, tree):
    item = tree.selection()[0]
    column = tree.identify_column(event.x)
    if column == '#2':
        x, y, width, height = tree.bbox(item, column)
        entry_edit = ttk.Entry(tree)
        entry_edit.place(x=x, y=y, width=width, height=height)
        entry_edit.focus()

        def save_edit(event):
            try:
                cost = float(entry_edit.get())
                tree.item(item, values=(tree.item(item, "values")[0], f"${cost:.2f}"))
                update_total_expenses(tree)
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter a valid cost")
            entry_edit.destroy()

        entry_edit.bind('<Return>', save_edit)
        entry_edit.bind('<FocusOut>', lambda e: entry_edit.destroy())


def add_expense_prompt(root, tree):
    top = tk.Toplevel(root)
    top.title("Add New Expense")

    ttk.Label(top, text="Expense Name:").pack(padx=10, pady=5)
    expense_name_entry = ttk.Entry(top, font=("Helvetica", 12))
    expense_name_entry.pack(padx=10, pady=5)

    ttk.Label(top, text="Expense Cost:").pack(padx=10, pady=5)
    expense_cost_entry = ttk.Entry(top, font=("Helvetica", 12))
    expense_cost_entry.pack(padx=10, pady=5)

    def add_new_expense():
        expense_name = expense_name_entry.get()
        try:
            expense_cost = float(expense_cost_entry.get())
            tree.insert("", "end", values=(expense_name, f"${expense_cost:.2f}"))
            update_total_expenses(tree)
            top.destroy()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid cost")

    ttk.Button(top, text="Add", command=add_new_expense).pack(pady=10)


def update_total_expenses(tree):
    global total_expenses
    global total_label
    total_expenses = sum(float(tree.item(item, "values")[1][1:]) for item in tree.get_children())
    if total_label is not None:
        total_label["text"] = f"Total Expenses: ${total_expenses:.2f}"
    update_remaining_amount()


def export_to_excel(salary_entry, state_combobox, tree):
    data = [(tree.item(item)["values"][0], float(tree.item(item)["values"][1][1:])) for item in tree.get_children()]
    df_expenses = pd.DataFrame(data, columns=["Expense", "Cost"])

    try:
        with pd.ExcelWriter("expenses.xlsx") as writer:
            # Writing salary information and calculations
            df_info = pd.DataFrame({
                "Annual Salary": [float(salary_entry.get())],
                "State": [state_combobox.get()],
                "Monthly Income After Taxes": [monthly_income_after_taxes],
                "Total Expenses": [total_expenses],
                "Remaining Amount": [remaining_amount]
            })
            df_info.to_excel(writer, sheet_name="Summary", index=False)
            df_expenses.to_excel(writer, sheet_name="Expenses", index=False)
        messagebox.showinfo("Export Successful", "Expenses exported to expenses.xlsx successfully!")
    except Exception as e:
        messagebox.showerror("Export Failed", f"Failed to export expenses: {e}")
