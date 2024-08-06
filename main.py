import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Tax rates
FEDERAL_TAX_RATE = 0.22
STATE_TAX_RATES = {
    "Massachusetts": 0.05,
    "Florida": 0.0,
}


class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Manager")
        self.root.geometry("700x700")  # Set the size of the window

        self.total_expenses = 0
        self.monthly_income_after_taxes = 0
        self.remaining_amount = 0

        # Create and configure styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.style.configure("Treeview", rowheight=25, font=("Helvetica", 12), background="#f0f8ff",
                             fieldbackground="#f0f8ff")

        # Set up the input fields for salary and state
        self.setup_income_input_fields()

        # Set up the input fields and add button for expenses
        self.setup_expense_input_fields()

        # Set up the table for expenses
        self.setup_table()

        # Set up the total expenses label
        self.setup_total_label()

        # Set up the remaining amount label
        self.setup_remaining_label()

        # Set up the export button
        self.setup_export_button()

    def setup_income_input_fields(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill=tk.X)

        self.salary_label = ttk.Label(frame, text="Annual Salary:")
        self.salary_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.salary_entry = ttk.Entry(frame, font=("Helvetica", 12))
        self.salary_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        self.state_label = ttk.Label(frame, text="State:")
        self.state_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.state_combobox = ttk.Combobox(frame, values=list(STATE_TAX_RATES.keys()), font=("Helvetica", 12))
        self.state_combobox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

        self.calculate_income_button = ttk.Button(frame, text="Calculate Income After Taxes",
                                                  command=self.calculate_income_after_taxes)
        self.calculate_income_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

        frame.columnconfigure(1, weight=1)  # Make the second column expandable

    def setup_expense_input_fields(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill=tk.X)

        self.expense_name_label = ttk.Label(frame, text="Expense Name:")
        self.expense_name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.expense_name_entry = ttk.Entry(frame, font=("Helvetica", 12))
        self.expense_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        self.expense_cost_label = ttk.Label(frame, text="Expense Cost:")
        self.expense_cost_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.expense_cost_entry = ttk.Entry(frame, font=("Helvetica", 12))
        self.expense_cost_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

        self.add_button = ttk.Button(frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

        # Bind the Enter key to add_expense method
        self.expense_cost_entry.bind('<Return>', lambda event: self.add_expense())

        frame.columnconfigure(1, weight=1)  # Make the second column expandable

    def setup_table(self):
        frame = tk.Frame(self.root, padx=20, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame, columns=("Expense", "Cost"), show='headings', height=1)
        self.tree.heading("Expense", text="Expense")
        self.tree.heading("Cost", text="Cost")
        self.tree.column("Expense", anchor=tk.W, width=300)
        self.tree.column("Cost", anchor=tk.E, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def setup_total_label(self):
        frame = tk.Frame(self.root, padx=20, pady=10)
        frame.pack(fill=tk.X)

        self.total_label = ttk.Label(frame, text="Total Expenses: $0", font=("Helvetica", 14, "bold"))
        self.total_label.pack(anchor=tk.E)

    def setup_remaining_label(self):
        frame = tk.Frame(self.root, padx=20, pady=10)
        frame.pack(fill=tk.X)

        self.remaining_label = ttk.Label(frame, text="Remaining Amount: $0", font=("Helvetica", 14, "bold"))
        self.remaining_label.pack(anchor=tk.E)

    def setup_export_button(self):
        frame = tk.Frame(self.root, padx=20, pady=10)
        frame.pack(fill=tk.X)

        self.export_button = ttk.Button(frame, text="Export to Excel", command=self.export_to_excel)
        self.export_button.pack(anchor=tk.E)

    def calculate_income_after_taxes(self):
        try:
            annual_salary = float(self.salary_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid annual salary")
            return

        state = self.state_combobox.get()
        if state not in STATE_TAX_RATES:
            messagebox.showerror("Invalid input", "Please select a valid state")
            return

        federal_tax = annual_salary * FEDERAL_TAX_RATE
        state_tax = annual_salary * STATE_TAX_RATES[state]
        annual_income_after_taxes = annual_salary - federal_tax - state_tax
        self.monthly_income_after_taxes = annual_income_after_taxes / 12

        messagebox.showinfo("Income After Taxes",
                            f"Your monthly income after taxes is: ${self.monthly_income_after_taxes:.2f}")
        self.update_remaining_amount()

    def add_expense(self):
        expense_name = self.expense_name_entry.get()
        try:
            expense_cost = float(self.expense_cost_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid cost")
            return

        self.tree.insert("", "end", values=(expense_name, f"${expense_cost:.2f}"))
        self.total_expenses += expense_cost
        self.total_label.config(text=f"Total Expenses: ${self.total_expenses:.2f}")
        self.expense_name_entry.delete(0, tk.END)
        self.expense_cost_entry.delete(0, tk.END)
        self.update_remaining_amount()
        self.update_table_height()

    def update_table_height(self):
        # Adjust the tree view height based on the number of items
        row_count = len(self.tree.get_children())
        self.tree.config(height=row_count)

    def update_remaining_amount(self):
        self.remaining_amount = self.monthly_income_after_taxes - self.total_expenses
        self.remaining_label.config(text=f"Remaining Amount: ${self.remaining_amount:.2f}")

    def export_to_excel(self):
        data = [(self.tree.item(item)["values"][0], float(self.tree.item(item)["values"][1][1:])) for item in
                self.tree.get_children()]
        df_expenses = pd.DataFrame(data, columns=["Expense", "Cost"])

        try:
            with pd.ExcelWriter("expenses.xlsx") as writer:
                # Writing salary information and calculations
                df_info = pd.DataFrame({
                    "Annual Salary": [float(self.salary_entry.get())],
                    "State": [self.state_combobox.get()],
                    "Monthly Income After Taxes": [self.monthly_income_after_taxes],
                    "Total Expenses": [self.total_expenses],
                    "Remaining Amount": [self.remaining_amount]
                })
                df_info.to_excel(writer, sheet_name="Summary", index=False)
                df_expenses.to_excel(writer, sheet_name="Expenses", index=False)
            messagebox.showinfo("Export Successful", "Expenses exported to expenses.xlsx successfully!")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export expenses: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
