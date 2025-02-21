import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class WorkoutTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Tracker")
        self.root.geometry("500x650")
        self.root.configure(bg="#2C3E50")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#34495E", foreground="#ECF0F1", fieldbackground="#34495E", font=("Arial", 11))
        style.configure("Treeview.Heading", background="#3498DB", foreground="white", font=("Arial", 12, "bold"))
        style.map("Treeview", background=[("selected", "#2980B9")])
        style.configure("Vertical.TScrollbar", background="#2C3E50", troughcolor="#34495E", arrowcolor="#ECF0F1")
        
        # Updated Combobox style with larger font
        style.configure("TCombobox", fieldbackground="#34495E", background="#3498DB", foreground="#ECF0F1", arrowcolor="#ECF0F1", font=("Arial", 14, "bold"))
        style.map("TCombobox", fieldbackground=[("readonly", "#34495E")], background=[("readonly", "#3498DB")], foreground=[("readonly", "#ECF0F1")])
        # Style for the dropdown list (larger font for options)
        self.root.option_add("*TCombobox*Listbox.font", ("Arial", 14, "bold"))

        tk.Label(root, text="Workout Tracker", font=("Arial", 20, "bold"), fg="#ECF0F1", bg="#2C3E50").pack(pady=20)

        self.content_frame = tk.Frame(root, bg="#2C3E50")
        self.content_frame.pack(fill="both", expand=True)

        button_frame = tk.Frame(root, bg="#2C3E50")
        button_frame.pack(side="bottom", pady=10)

        btn_style = {"font": ("Arial", 14, "bold"), "bg": "#34495E", "fg": "#ECF0F1", "width": 10, "bd": 0, "activebackground": "#2980B9"}
        self.log_button = tk.Button(button_frame, text="Log", command=self.show_log, **btn_style)
        self.log_button.pack(side="left", padx=5)
        self.history_button = tk.Button(button_frame, text="History", command=self.show_history, **btn_style)
        self.history_button.pack(side="left", padx=5)

        self.current_view = "log"
        self.show_log()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_log(self):
        self.clear_content()
        self.current_view = "log"
        self.log_button.config(bg="#3498DB")
        self.history_button.config(bg="#34495E")

        button_frame = tk.Frame(self.content_frame, bg="#2C3E50")
        button_frame.pack(pady=10)

        btn_style = {"font": ("Arial", 15), "bg": "#3498DB", "fg": "white", "width": 18, "bd": 0, "activebackground": "#2980B9"}
        tk.Button(button_frame, text="Gym", command=self.show_gym, **btn_style).pack(pady=5)
        tk.Button(button_frame, text="Run", command=self.show_run, **btn_style).pack(pady=5)
        tk.Button(button_frame, text="Swim", command=self.show_swim, **btn_style).pack(pady=5)
        tk.Button(button_frame, text="Walk", command=self.show_walking, **btn_style).pack(pady=5)

        self.input_frame = tk.Frame(self.content_frame, bg="#2C3E50")
        self.input_frame.pack(pady=20)

    def show_history(self):
        self.clear_content()
        self.current_view = "history"
        self.log_button.config(bg="#34495E")
        self.history_button.config(bg="#3498DB")

        filter_frame = tk.Frame(self.content_frame, bg="#34495E", bd=2, relief="groove")
        filter_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(filter_frame, text="Filter by Activity:", font=("Arial", 10, "bold"), fg="#ECF0F1", bg="#34495E").pack(side="left", padx=10, pady=5)
        self.filter_var = tk.StringVar(value="All")
        filter_options = ["All", "Gym", "Run", "Swim", "Walk"]
        self.filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filter_options, state="readonly", width=15)
        self.filter_dropdown.pack(side="left", padx=10, pady=5)
        self.filter_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_history())

        self.tree = ttk.Treeview(self.content_frame, columns=("Exercise", "Sets", "Reps", "Weight", "Distance", "Pace"), show="headings", height=18)
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree.heading("Exercise", text="Exercise")
        self.tree.heading("Sets", text="Sets")
        self.tree.heading("Reps", text="Reps")
        self.tree.heading("Weight", text="Weight (kg)")
        self.tree.heading("Distance", text="Distance")
        self.tree.heading("Pace", text="Pace")

        self.tree.column("Exercise", width=100)
        self.tree.column("Sets", width=50)
        self.tree.column("Reps", width=50)
        self.tree.column("Weight", width=80)
        self.tree.column("Distance", width=80)
        self.tree.column("Pace", width=80)

        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.tag_configure("oddrow", background="#ECF0F1", foreground="#2C3E50")
        self.tree.tag_configure("evenrow", background="#D5D8DC", foreground="#2C3E50")

        button_frame = tk.Frame(self.content_frame, bg="#2C3E50")
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Delete Selected", command=self.delete_record, font=("Arial", 12), bg="#E74C3C", fg="white", width=15, bd=0, activebackground="#C0392B").pack(side="left", padx=5)
        tk.Button(button_frame, text="Edit Selected", command=self.edit_record, font=("Arial", 12), bg="#F1C40F", fg="white", width=15, bd=0, activebackground="#D4AC0D").pack(side="left", padx=5)

        self.update_history()

    def clear_frame(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

    def show_gym(self):
        self.clear_frame()
        self.activity_type = "Gym"
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.exercise_entry.insert(0, "Gym")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Sets:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.sets_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.sets_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Reps:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.reps_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.reps_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Weight (kg):", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.weight_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.weight_entry.pack(pady=2)
        tk.Button(self.input_frame, text="Log", command=self.log_activity, font=("Arial", 12), bg="#E74C3C", fg="white", width=10, bd=0, activebackground="#C0392B").pack(pady=10)

    def show_run(self):
        self.clear_frame()
        self.activity_type = "Run"
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.exercise_entry.insert(0, "Run")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Distance (km):", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.distance_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.distance_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Pace (min/km):", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.pace_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.pace_entry.pack(pady=2)
        tk.Button(self.input_frame, text="Log", command=self.log_activity, font=("Arial", 12), bg="#E74C3C", fg="white", width=10, bd=0, activebackground="#C0392B").pack(pady=10)

    def show_swim(self):
        self.clear_frame()
        self.activity_type = "Swim"
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.exercise_entry.insert(0, "Swim")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Distance (m):", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.distance_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.distance_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Time (min):", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.time_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.time_entry.pack(pady=2)
        tk.Button(self.input_frame, text="Log", command=self.log_activity, font=("Arial", 12), bg="#E74C3C", fg="white", width=10, bd=0, activebackground="#C0392B").pack(pady=10)

    def show_walking(self):
        self.clear_frame()
        self.activity_type = "Walk"
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.exercise_entry.insert(0, "Walk")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Distance (km):", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.distance_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.distance_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Pace (min/km):", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
        self.pace_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg="#ECF0F1")
        self.pace_entry.pack(pady=2)
        tk.Button(self.input_frame, text="Log", command=self.log_activity, font=("Arial", 12), bg="#E74C3C", fg="white", width=10, bd=0, activebackground="#C0392B").pack(pady=10)

    def log_activity(self):
        exercise = self.exercise_entry.get() or self.activity_type
        
        if self.activity_type == "Gym":
            sets = self.sets_entry.get()
            reps = self.reps_entry.get()
            weight = self.weight_entry.get()
            row = [exercise, sets, reps, weight, "", ""]
        elif self.activity_type in ["Run", "Walk"]:
            distance = self.distance_entry.get()
            pace = self.pace_entry.get()
            row = [exercise, "", "", "", distance, pace]
        elif self.activity_type == "Swim":
            distance = float(self.distance_entry.get())
            time = float(self.time_entry.get())
            pace = (time / distance) * 100
            row = [exercise, "", "", "", distance, pace]

        with open("workouts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
        
        messagebox.showinfo("Success", f"Activity logged! Pace: {pace if self.activity_type == 'Swim' else ''} min/100m" if self.activity_type == "Swim" else "Activity logged!")
        self.clear_frame()
        if self.current_view == "history":
            self.update_history()

    def update_history(self):
        if self.current_view == "history" and hasattr(self, 'tree'):
            for item in self.tree.get_children():
                self.tree.delete(item)
            try:
                with open("workouts.csv", "r") as file:
                    reader = csv.reader(file)
                    header = next(reader)
                    filter_type = self.filter_var.get()
                    for i, row in enumerate(reader):
                        exercise = row[0]
                        if filter_type == "All" or filter_type in exercise:
                            tag = "evenrow" if i % 2 == 0 else "oddrow"
                            self.tree.insert("", "end", values=row, tags=(tag,))
            except FileNotFoundError:
                pass

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a record to delete!")
            return

        selected_values = self.tree.item(selected_item, "values")
        with open("workouts.csv", "r") as file:
            reader = csv.reader(file)
            header = next(reader)
            all_rows = list(reader)

        updated_rows = [row for row in all_rows if row != list(selected_values)]
        with open("workouts.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(updated_rows)

        self.update_history()
        messagebox.showinfo("Success", "Record deleted!")

    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a record to edit!")
            return

        selected_values = list(self.tree.item(selected_item, "values"))
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Record")
        self.edit_window.geometry("300x400")
        self.edit_window.configure(bg="#2C3E50")

        fields = ["Exercise", "Sets", "Reps", "Weight (kg)", "Distance", "Pace"]
        self.edit_entries = {}
        for i, (field, value) in enumerate(zip(fields, selected_values)):
            tk.Label(self.edit_window, text=f"{field}:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack(pady=2)
            entry = tk.Entry(self.edit_window, font=("Arial", 12), width=20, bg="#ECF0F1")
            entry.insert(0, value)
            entry.pack(pady=2)
            self.edit_entries[field] = entry

        tk.Button(self.edit_window, text="Save Changes", command=lambda: self.save_edit(selected_values), font=("Arial", 12), bg="#2ECC71", fg="white", width=15, bd=0, activebackground="#27AE60").pack(pady=10)

    def save_edit(self, old_values):
        new_values = [self.edit_entries[field].get() for field in ["Exercise", "Sets", "Reps", "Weight (kg)", "Distance", "Pace"]]
        with open("workouts.csv", "r") as file:
            reader = csv.reader(file)
            header = next(reader)
            all_rows = list(reader)

        updated_rows = [new_values if row == old_values else row for row in all_rows]
        with open("workouts.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(updated_rows)

        self.edit_window.destroy()
        self.update_history()
        messagebox.showinfo("Success", "Record updated!")

try:
    with open("workouts.csv", "r"):
        pass
except FileNotFoundError:
    with open("workouts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["exercise", "sets", "reps", "weight", "distance", "pace"])

root = tk.Tk()
app = WorkoutTrackerApp(root)
root.mainloop()