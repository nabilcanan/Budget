import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import pandas as pd


def open_schedule_planner(root):
    top = tk.Toplevel(root)
    top.title("Plan a Schedule")
    top.geometry("1000x700")  # Large window for Google Calendar-like layout

    # Create a large calendar to select days
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd', font=("Helvetica", 14), foreground="black")
    cal.pack(pady=20, expand=True)

    # Dictionary to store the schedule
    schedule = {}

    # Define a default time format
    default_time_format = "0:00 - 0:00"

    # Function to add/edit events
    def add_edit_event(selected_date, event_data=None):
        event_window = tk.Toplevel(top)
        event_window.title(f"Edit Schedule for {selected_date}")

        ttk.Label(event_window, text="Select Job:", font=("Helvetica", 12)).pack(padx=10, pady=10)
        job_options = ["AdventHealth", "CFA"]
        job_combobox = ttk.Combobox(event_window, values=job_options, font=("Helvetica", 12))
        job_combobox.pack(padx=10, pady=5)
        job_combobox.set(job_options[0])

        ttk.Label(event_window, text="Enter Work Hours (e.g., 0:00 - 0:00):", font=("Helvetica", 12)).pack(padx=10,
                                                                                                           pady=10)
        hours_entry = ttk.Entry(event_window, font=("Helvetica", 12))
        hours_entry.insert(0, event_data.get("hours", default_time_format) if event_data else default_time_format)
        hours_entry.pack(padx=10, pady=5)

        def save_event():
            job = job_combobox.get()
            hours = hours_entry.get()

            if selected_date not in schedule:
                schedule[selected_date] = {}

            schedule[selected_date][job] = hours
            cal.calevent_create(selected_date, f"{job}: {hours}", 'work')
            cal.tag_config('work', background='lightblue', foreground='black')
            event_window.destroy()
            messagebox.showinfo("Schedule Updated", f"Updated {hours} for {job} on {selected_date}.")

        ttk.Button(event_window, text="Save", command=save_event).pack(pady=10)

    # Handle double-click events on the calendar
    def on_day_double_click(event):
        selected_date = cal.get_date()
        event_data = schedule.get(selected_date, {})
        add_edit_event(selected_date, event_data)

    cal.bind("<Double-1>", on_day_double_click)  # Bind double-click to open the event editor

    # Copy-Paste logic
    copied_data = {"date": None, "job": None, "hours": None}

    def copy_schedule():
        selected_date = cal.get_date()
        if selected_date in schedule:
            copied_data["date"] = selected_date
            job_entries = schedule[selected_date]
            if len(job_entries) == 1:
                copied_data["job"] = list(job_entries.keys())[0]
                copied_data["hours"] = job_entries[copied_data["job"]]
                messagebox.showinfo("Copy Success",
                                    f"Copied {copied_data['hours']} for {copied_data['job']} on {copied_data['date']}.")
            else:
                messagebox.showerror("Copy Failed",
                                     "Multiple jobs scheduled for this day. Copy only supports single entries.")
        else:
            messagebox.showerror("Copy Failed", "No schedule found for the selected date.")

    def paste_schedule():
        if copied_data["hours"]:
            selected_date = cal.get_date()
            job = copied_data["job"]
            hours = copied_data["hours"]

            if selected_date not in schedule:
                schedule[selected_date] = {}

            schedule[selected_date][job] = hours
            cal.calevent_create(selected_date, f"{job}: {hours}", 'work')
            cal.tag_config('work', background='lightgreen', foreground='black')
            messagebox.showinfo("Paste Success", f"Pasted {hours} for {job} on {selected_date}.")
        else:
            messagebox.showerror("Paste Failed", "No copied schedule to paste.")

    # Copy and Paste buttons
    ttk.Button(top, text="Copy Schedule", command=copy_schedule).pack(pady=5)
    ttk.Button(top, text="Paste Schedule", command=paste_schedule).pack(pady=5)

    # Export schedule button
    ttk.Button(top, text="Export Schedule to Excel", command=lambda: export_schedule_to_excel(schedule)).pack(pady=20)


def export_schedule_to_excel(schedule):
    # Convert the schedule dictionary to a DataFrame
    data = []
    for date, jobs in schedule.items():
        for job, hours in jobs.items():
            data.append([date, job, hours])

    df = pd.DataFrame(data, columns=["Date", "Job", "Hours"])
    df = df.pivot(index='Date', columns='Job', values='Hours').fillna('No Work')

    # Export to Excel
    try:
        with pd.ExcelWriter("schedule.xlsx") as writer:
            df.to_excel(writer, sheet_name="Schedule")
        messagebox.showinfo("Export Successful", "Schedule exported to schedule.xlsx successfully!")
    except Exception as e:
        messagebox.showerror("Export Failed", f"Failed to export schedule: {e}")
