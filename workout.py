import csv
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime

class WorkoutTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Tracker")
        self.root.geometry("600x700")  # Increased size for graphs

        # Theme settings
        self.themes = {
            "dark": {"bg": "#2C3E50", "fg": "#ECF0F1", "button_bg": "#34495E", "active_bg": "#3498DB", "entry_bg": "#ECF0F1"},
            "light": {"bg": "#ECF0F1", "fg": "#2C3E50", "button_bg": "#D5D8DC", "active_bg": "#3498DB", "entry_bg": "#FFFFFF"}
        }
        self.current_theme = "dark"
        self.apply_theme()

        # Style configuration
        self.style = ttk.Style()
        self.update_style()

        self.content_frame = tk.Frame(root, bg=self.themes[self.current_theme]["bg"])
        self.content_frame.pack(fill="both", expand=True)

        # Navigation buttons
        button_frame = tk.Frame(root, bg=self.themes[self.current_theme]["bg"])
        button_frame.pack(side="bottom", pady=10)
        btn_style = {"font": ("Arial", 14, "bold"), "bg": self.themes[self.current_theme]["button_bg"], "fg": self.themes[self.current_theme]["fg"], "width": 10, "bd": 0, "activebackground": self.themes[self.current_theme]["active_bg"]}
        self.log_button = tk.Button(button_frame, text="Log", command=self.show_log, **btn_style)
        self.log_button.pack(side="left", padx=5)
        self.history_button = tk.Button(button_frame, text="History", command=self.show_history, **btn_style)
        self.history_button.pack(side="left", padx=5)
        self.graphs_button = tk.Button(button_frame, text="Graphs", command=self.show_graphs, **btn_style)
        self.graphs_button.pack(side="left", padx=5)

        # Theme switcher
        self.theme_var = tk.StringVar(value="Dark")
        theme_menu = ttk.Combobox(button_frame, textvariable=self.theme_var, values=["Dark", "Light"], state="readonly", width=8)
        theme_menu.pack(side="right", padx=5)
        theme_menu.bind("<<ComboboxSelected>>", self.switch_theme)

        self.current_view = "log"
        self.show_log()

    def apply_theme(self):
        self.root.configure(bg=self.themes[self.current_theme]["bg"])

    def update_style(self):
        theme = self.themes[self.current_theme]
        self.style.theme_use("default")
        self.style.configure("Treeview", background=theme["button_bg"], foreground=theme["fg"], fieldbackground=theme["button_bg"], font=("Arial", 11))
        self.style.configure("Treeview.Heading", background=theme["active_bg"], foreground="white", font=("Arial", 12, "bold"))
        self.style.map("Treeview", background=[("selected", "#2980B9")])
        self.style.configure("Vertical.TScrollbar", background=theme["bg"], troughcolor=theme["button_bg"], arrowcolor=theme["fg"])
        self.style.configure("TCombobox", fieldbackground=theme["button_bg"], background=theme["active_bg"], foreground=theme["fg"], arrowcolor=theme["fg"], font=("Arial", 14, "bold"))
        self.style.map("TCombobox", fieldbackground=[("readonly", theme["button_bg"])], background=[("readonly", theme["active_bg"])], foreground=[("readonly", theme["fg"])])
        self.root.option_add("*TCombobox*Listbox.font", ("Arial", 14, "bold"))

    def switch_theme(self, event):
        self.current_theme = "light" if self.theme_var.get() == "Light" else "dark"
        self.apply_theme()
        self.update_style()
        self.refresh_view()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def refresh_view(self):
        if self.current_view == "log":
            self.show_log()
        elif self.current_view == "history":
            self.show_history()
        elif self.current_view == "graphs":
            self.show_graphs()

    def show_log(self):
        self.clear_content()
        self.current_view = "log"
        self.log_button.config(bg=self.themes[self.current_theme]["active_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["button_bg"])

        theme = self.themes[self.current_theme]
        button_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        button_frame.pack(pady=10)
        btn_style = {"font": ("Arial", 15), "bg": theme["active_bg"], "fg": "white", "width": 18, "bd": 0, "activebackground": "#2980B9"}
        tk.Button(button_frame, text="Gym", command=self.show_gym, **btn_style).pack(pady=5)
        tk.Button(button_frame, text="Run", command=self.show_run, **btn_style).pack(pady=5)
        tk.Button(button_frame, text="Swim", command=self.show_swim, **btn_style).pack(pady=5)
        tk.Button(button_frame, text="Walk", command=self.show_walking, **btn_style).pack(pady=5)

        self.input_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        self.input_frame.pack(pady=20)

    def show_history(self):
        self.clear_content()
        self.current_view = "history"
        self.log_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["active_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["button_bg"])

        theme = self.themes[self.current_theme]
        filter_frame = tk.Frame(self.content_frame, bg=theme["button_bg"], bd=2, relief="groove")
        filter_frame.pack(pady=10, padx=10, fill="x")
        tk.Label(filter_frame, text="Filter by Activity:", font=("Arial", 12, "bold"), fg=theme["fg"], bg=theme["button_bg"]).pack(side="left", padx=10, pady=5)
        self.filter_var = tk.StringVar(value="All")
        filter_options = ["All", "Gym", "Run", "Swim", "Walk"]
        self.filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filter_options, state="readonly", width=15)
        self.filter_dropdown.pack(side="left", padx=10, pady=5)
        self.filter_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_history())

        self.tree = ttk.Treeview(self.content_frame, columns=("Exercise", "Sets", "Reps", "Weight", "Distance", "Pace"), show="headings", height=15)
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
        self.tree.tag_configure("oddrow", background=theme["entry_bg"], foreground=theme["bg"])
        self.tree.tag_configure("evenrow", background="#D5D8DC" if self.current_theme == "dark" else "#BFC9CA", foreground=theme["bg"])

        # Stats frame
        stats_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        stats_frame.pack(pady=5)
        self.stats_label = tk.Label(stats_frame, text="", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"])
        self.stats_label.pack()

        # Buttons
        button_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Delete Selected", command=self.delete_record, font=("Arial", 12), bg="#E74C3C", fg="white", width=15, bd=0, activebackground="#C0392B").pack(side="left", padx=5)
        tk.Button(button_frame, text="Edit Selected", command=self.edit_record, font=("Arial", 12), bg="#F1C40F", fg="white", width=15, bd=0, activebackground="#D4AC0D").pack(side="left", padx=5)
        tk.Button(button_frame, text="Export CSV", command=self.export_csv, font=("Arial", 12), bg="#2ECC71", fg="white", width=15, bd=0, activebackground="#27AE60").pack(side="left", padx=5)
        tk.Button(button_frame, text="Import CSV", command=self.import_csv, font=("Arial", 12), bg="#9B59B6", fg="white", width=15, bd=0, activebackground="#8E44AD").pack(side="left", padx=5)

        self.update_history()

    def show_graphs(self):
        self.clear_content()
        self.current_view = "graphs"
        self.log_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["active_bg"])

        theme = self.themes[self.current_theme]
        fig, ax = plt.subplots(figsize=(5, 4), facecolor=theme["bg"])
        ax.set_facecolor(theme["button_bg"])
        ax.tick_params(colors=theme["fg"])
        ax.spines['bottom'].set_color(theme["fg"])
        ax.spines['top'].set_color(theme["fg"])
        ax.spines['left'].set_color(theme["fg"])
        ax.spines['right'].set_color(theme["fg"])

        try:
            with open("workouts.csv", "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                dates, distances = [], []
                for row in reader:
                    exercise = row[0]
                    distance = row[4]
                    if distance and "Run" in exercise:  # Example: Graph runs
                        dates.append(datetime.now())  # Placeholder; add date column later
                        distances.append(float(distance))
                if dates:
                    ax.plot(dates, distances, color="#3498DB", marker="o")
                    ax.set_title("Run Distance Over Time", color=theme["fg"])
                    ax.set_xlabel("Date", color=theme["fg"])
                    ax.set_ylabel("Distance (km)", color=theme["fg"])
                else:
                    ax.text(0.5, 0.5, "No run data available", ha="center", va="center", color=theme["fg"])
        except FileNotFoundError:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center", color=theme["fg"])

        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def clear_frame(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

    def show_gym(self):
        self.clear_frame()
        self.activity_type = "Gym"
        theme = self.themes[self.current_theme]
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.exercise_entry.insert(0, "Gym")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Sets:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.sets_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.sets_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Reps:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.reps_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.reps_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Weight (kg):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.weight_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.weight_entry.pack(pady=2)
        tk.Button(self.input_frame, text="Log", command=self.log_activity, font=("Arial", 12), bg="#E74C3C", fg="white", width=10, bd=0, activebackground="#C0392B").pack(pady=10)

    def show_run(self):
        self.clear_frame()
        self.activity_type = "Run"
        theme = self.themes[self.current_theme]
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.exercise_entry.insert(0, "Run")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Distance (km):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.distance_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.distance_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Pace (min/km):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.pace_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.pace_entry.pack(pady=2)
        tk.Button(self.input_frame, text="Log", command=self.log_activity, font=("Arial", 12), bg="#E74C3C", fg="white", width=10, bd=0, activebackground="#C0392B").pack(pady=10)

    def show_swim(self):
        self.clear_frame()
        self.activity_type = "Swim"
        theme = self.themes[self.current_theme]
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.exercise_entry.insert(0, "Swim")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Distance (m):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.distance_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.distance_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Time (min):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.time_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.time_entry.pack(pady=2)
        tk.Button(self.input_frame, text="Log", command=self.log_activity, font=("Arial", 12), bg="#E74C3C", fg="white", width=10, bd=0, activebackground="#C0392B").pack(pady=10)

    def show_walking(self):
        self.clear_frame()
        self.activity_type = "Walk"
        theme = self.themes[self.current_theme]
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.exercise_entry.insert(0, "Walk")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Distance (km):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.distance_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.distance_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Pace (min/km):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.pace_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
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
            total_distance = 0
            total_pace = 0
            count = 0
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
                            if row[4]:  # Distance
                                total_distance += float(row[4])
                                count += 1
                            if row[5]:  # Pace
                                total_pace += float(row[5])
                    avg_pace = total_pace / count if count > 0 else 0
                    self.stats_label.config(text=f"Total Distance: {total_distance:.2f} | Avg Pace: {avg_pace:.2f}")
            except FileNotFoundError:
                self.stats_label.config(text="No data available")

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
        theme = self.themes[self.current_theme]
        self.edit_window.configure(bg=theme["bg"])
        fields = ["Exercise", "Sets", "Reps", "Weight (kg)", "Distance", "Pace"]
        self.edit_entries = {}
        for i, (field, value) in enumerate(zip(fields, selected_values)):
            tk.Label(self.edit_window, text=f"{field}:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
            entry = tk.Entry(self.edit_window, font=("Arial", 12), width=20, bg=theme["entry_bg"])
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

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open("workouts.csv", "r") as source, open(file_path, "w", newline="") as target:
                target.write(source.read())
            messagebox.showinfo("Success", "Workouts exported successfully!")

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "r") as source, open("workouts.csv", "a", newline="") as target:
                reader = csv.reader(source)
                writer = csv.writer(target)
                header = next(reader)  # Skip header
                for row in reader:
                    writer.writerow(row)
            self.update_history()
            messagebox.showinfo("Success", "Workouts imported successfully!")

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