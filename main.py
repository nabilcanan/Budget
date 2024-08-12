import tkinter as tk
from debt_calculator import open_debt_calculator
from salary_setup import configure_styles, setup_income_input_fields, setup_buttons, setup_prebuilt_table, \
    setup_total_label, setup_remaining_label, setup_export_button, calculate_income_after_taxes, add_expense_prompt, \
    on_double_click, export_to_excel
from schedule_planner import open_schedule_planner  # Import the schedule planner

# Global variables
total_expenses = 0
monthly_income_after_taxes = 0
remaining_amount = 0
total_label = None
remaining_label = None

def main():
    global total_expenses, monthly_income_after_taxes, total_label, remaining_label
    total_expenses = 0
    monthly_income_after_taxes = 0

    root = tk.Tk()

    configure_styles()

    salary_entry, state_combobox = setup_income_input_fields(
        root,
        lambda: calculate_income_after_taxes(salary_entry, state_combobox)
    )
    setup_buttons(
        root,
        lambda: add_expense_prompt(root, tree),
        lambda: open_debt_calculator(root),
        lambda: open_schedule_planner(root)  # Call the new schedule planner function here
    )

    tree = setup_prebuilt_table(root)
    tree.bind('<Double-1>', lambda event: on_double_click(event, tree))

    setup_total_label(root)
    setup_remaining_label(root)

    setup_export_button(
        root,
        lambda: export_to_excel(salary_entry, state_combobox, tree)
    )

    root.mainloop()

if __name__ == "__main__":
    main()
