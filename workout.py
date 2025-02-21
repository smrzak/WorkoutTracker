import csv
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import mplcursors
import shutil

class WorkoutTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Tracker")
        self.root.geometry("1000x1000")
        # Theme settings
        self.themes = {
            "dark": {"bg": "#2C3E50", "fg": "#ECF0F1", "button_bg": "#34495E", "active_bg": "#3498DB", "entry_bg": "#ECF0F1"},
            "light": {"bg": "#ECF0F1", "fg": "#2C3E50", "button_bg": "#D5D8DC", "active_bg": "#3498DB", "entry_bg": "#FFFFFF"}
        }
        self.current_theme = self.load_theme()
        self.current_view = "log"

        # Load theme icons with fallback
        try:
            self.dark_icon = ImageTk.PhotoImage(Image.open("pics/night.png").resize((20, 20)))
        except FileNotFoundError:
            self.dark_icon = None
            print("Warning: night.png not found, using text fallback")
        try:
            self.light_icon = ImageTk.PhotoImage(Image.open("pics/sun.png").resize((20, 20)))
        except FileNotFoundError:
            self.light_icon = None
            print("Warning: sun.png not found, using text fallback")
        try:
            self.profile_icon = ImageTk.PhotoImage(Image.open("pics/profile.png").resize((20, 20)))
        except FileNotFoundError:
            self.profile_icon = None
            print("Warning: profile.png not found, using text fallback")

        # Style configuration
        self.style = ttk.Style()

        # Initialize UI components
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
        self.stats_button = tk.Button(button_frame, text="Stats", command=self.show_stats, **btn_style)
        self.stats_button.pack(side="left", padx=5)
        self.profile_button = tk.Button(button_frame, image=self.profile_icon if self.profile_icon else None, text="Profile" if not self.profile_icon else "", compound="left", bg=self.themes[self.current_theme]["button_bg"], fg=self.themes[self.current_theme]["fg"], bd=0, command=self.show_profile)
        self.profile_button.pack(side="left", padx=5)

        # Theme switcher button
        self.theme_button = tk.Button(button_frame, image=self.dark_icon if self.dark_icon else None, text="Dark" if not self.dark_icon else "", compound="left", bg=self.themes[self.current_theme]["button_bg"], bd=0, command=self.switch_theme)
        self.theme_button.pack(side="right", padx=5)

        # Apply theme after UI setup
        self.apply_theme()

    def load_theme(self):
        try:
            with open("settings.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                theme = next(reader)[0]
                return theme if theme in self.themes else "dark"
        except (FileNotFoundError, IndexError):
            return "dark"

    def save_theme(self):
        with open("settings.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["theme"])
            writer.writerow([self.current_theme])

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])
            elif isinstance(widget, tk.Button):
                if widget == self.theme_button:
                    if self.current_theme == "dark":
                        widget.configure(image=self.light_icon if self.light_icon else None, text="Light" if not self.light_icon else "", bg=theme["button_bg"], fg=theme["fg"], activebackground=theme["active_bg"])
                    else:
                        widget.configure(image=self.dark_icon if self.dark_icon else None, text="Dark" if not self.dark_icon else "", bg=theme["button_bg"], fg=theme["fg"], activebackground=theme["active_bg"])
                else:
                    widget.configure(bg=theme["button_bg"], fg=theme["fg"], activebackground=theme["active_bg"])
        self.update_style()
        self.refresh_view()

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

    def switch_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.save_theme()
        self.apply_theme()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def refresh_view(self):
        self.clear_content()
        if self.current_view == "log":
            self.show_log()
        elif self.current_view == "history":
            self.show_history()
        elif self.current_view == "graphs":
            self.show_graphs()
        elif self.current_view == "stats":
            self.show_stats()
        elif self.current_view == "profile":
            self.show_profile()

    def show_log(self):
        self.clear_content()
        self.current_view = "log"
        self.log_button.config(bg=self.themes[self.current_theme]["active_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.stats_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.profile_button.config(bg=self.themes[self.current_theme]["button_bg"])

        theme = self.themes[self.current_theme]
        button_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        button_frame.pack(pady=10)
        btn_style = {"font": ("Arial", 15), "bg": theme["active_bg"], "fg": "white", "width": 18, "bd": 0, "activebackground": "#2980B9"}
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
        self.stats_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.profile_button.config(bg=self.themes[self.current_theme]["button_bg"])

        theme = self.themes[self.current_theme]
        filter_frame = tk.Frame(self.content_frame, bg=theme["button_bg"], bd=2, relief="groove")
        filter_frame.pack(pady=10, padx=10, fill="x")
        tk.Label(filter_frame, text="Filter by Activity:", font=("Arial", 12, "bold"), fg=theme["fg"], bg=theme["button_bg"]).pack(side="left", padx=10, pady=5)
        self.filter_var = tk.StringVar(value="All")
        filter_options = ["All", "Run", "Swim", "Walk"]
        self.filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filter_options, state="readonly", width=15)
        self.filter_dropdown.pack(side="left", padx=10, pady=5)
        self.filter_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_history())

        self.tree = ttk.Treeview(self.content_frame, columns=("Date", "Exercise", "Distance", "Pace", "Notes"), show="headings", height=15, selectmode="extended")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)
        self.tree.heading("Date", text="Date")
        self.tree.heading("Exercise", text="Exercise")
        self.tree.heading("Distance", text="Distance")
        self.tree.heading("Pace", text="Pace")
        self.tree.heading("Notes", text="Notes")
        self.tree.column("Date", width=150)
        self.tree.column("Exercise", width=100)
        self.tree.column("Distance", width=120)
        self.tree.column("Pace", width=150)
        self.tree.column("Notes", width=200)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.tag_configure("oddrow", background=theme["entry_bg"], foreground=theme["bg"])
        self.tree.tag_configure("evenrow", background="#D5D8DC" if self.current_theme == "dark" else "#BFC9CA", foreground=theme["bg"])

        stats_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        stats_frame.pack(pady=5)
        self.stats_label = tk.Label(stats_frame, text="", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"])
        self.stats_label.pack()

        button_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Delete Selected", command=self.delete_records, font=("Arial", 12), bg="#E74C3C", fg="white", width=15, bd=0, activebackground="#C0392B").pack(side="left", padx=5)
        tk.Button(button_frame, text="Edit Selected", command=self.edit_record, font=("Arial", 12), bg="#F1C40F", fg="white", width=15, bd=0, activebackground="#D4AC0D").pack(side="left", padx=5)
        tk.Button(button_frame, text="CSV Options", command=self.csv_options, font=("Arial", 12), bg="#2ECC71", fg="white", width=15, bd=0, activebackground="#27AE60").pack(side="left", padx=5)

        self.update_history()

    def csv_options(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Export CSV", command=self.export_csv)
        menu.add_command(label="Import CSV", command=self.import_csv)
        menu.add_command(label="Backup Data", command=self.backup_data)
        menu.add_command(label="Restore Data", command=self.restore_data)
        menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def show_graphs(self):
        self.clear_content()
        self.current_view = "graphs"
        self.log_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["active_bg"])
        self.stats_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.profile_button.config(bg=self.themes[self.current_theme]["button_bg"])

        theme = self.themes[self.current_theme]
        options_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        options_frame.pack(pady=10)

        tk.Label(options_frame, text="Activity:", font=("Arial", 12, "bold"), fg=theme["fg"], bg=theme["bg"]).pack(side="left", padx=5)
        self.activity_var = tk.StringVar(value="All")
        activity_options = ["All", "Run", "Swim", "Walk"]
        self.activity_dropdown = ttk.Combobox(options_frame, textvariable=self.activity_var, values=activity_options, state="readonly", width=10)
        self.activity_dropdown.pack(side="left", padx=5)
        self.activity_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_graph())

        tk.Label(options_frame, text="Metric:", font=("Arial", 12, "bold"), fg=theme["fg"], bg=theme["bg"]).pack(side="left", padx=5)
        self.metric_var = tk.StringVar(value="Distance")
        self.metric_dropdown = ttk.Combobox(options_frame, textvariable=self.metric_var, values=["Distance", "Pace"], state="readonly", width=10)
        self.metric_dropdown.pack(side="left", padx=5)
        self.metric_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_graph())

        tk.Label(options_frame, text="From (DD.MM.YYYY):", font=("Arial", 12, "bold"), fg=theme["fg"], bg=theme["bg"]).pack(side="left", padx=5)
        self.from_date_entry = tk.Entry(options_frame, font=("Arial", 12), width=12, bg=theme["entry_bg"])
        self.from_date_entry.insert(0, (datetime.now() - timedelta(days=365)).strftime("%d.%m.%Y"))
        self.from_date_entry.pack(side="left", padx=5)

        tk.Label(options_frame, text="To (DD.MM.YYYY):", font=("Arial", 12, "bold"), fg=theme["fg"], bg=theme["bg"]).pack(side="left", padx=5)
        self.to_date_entry = tk.Entry(options_frame, font=("Arial", 12), width=12, bg=theme["entry_bg"])
        self.to_date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.to_date_entry.pack(side="left", padx=5)

        self.graph_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        self.graph_frame.pack(fill="both", expand=True)

        button_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Save Graph", command=self.save_graph, font=("Arial", 12), bg="#2ECC71", fg="white", width=15, bd=0, activebackground="#27AE60").pack(pady=5)

        self.update_graph()

    def show_stats(self):
        self.clear_content()
        self.current_view = "stats"
        self.log_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.stats_button.config(bg=self.themes[self.current_theme]["active_bg"])
        self.profile_button.config(bg=self.themes[self.current_theme]["button_bg"])

        theme = self.themes[self.current_theme]
        stats_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        stats_frame.pack(pady=20)

        tk.Label(stats_frame, text="Activity Stats", font=("Arial", 20, "bold"), fg=theme["fg"], bg=theme["bg"]).pack(pady=10)

        stats_text = tk.Text(stats_frame, height=30, width=50, font=("Arial", 12), fg=theme["fg"], bg=theme["bg"], wrap="word")
        stats_text.pack(pady=5)

        try:
            with open("workouts.csv", "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                workouts = [row for row in reader if len(row) == 8]

            if not workouts:
                stats_text.insert(tk.END, "No workout data available")
                stats_text.config(state="disabled")
                return

            stats = {"Run": {"distance": 0.0, "pace": [], "max_distance": 0.0},
                     "Swim": {"distance": 0.0, "pace": [], "max_distance": 0.0},
                     "Walk": {"distance": 0.0, "pace": [], "max_distance": 0.0}}

            for row in workouts:
                exercise = row[1].strip('"')
                distance = row[5].strip('"')
                pace = row[6].strip('"')
                if exercise in stats and distance and pace:
                    dist_value = float(distance) / 1000 if exercise.lower() == "swim" else float(distance)
                    pace_value = self.parse_pace(pace)  # Handle both MM:SS and float
                    stats[exercise]["distance"] += dist_value
                    stats[exercise]["pace"].append(pace_value)
                    stats[exercise]["max_distance"] = max(stats[exercise]["max_distance"], dist_value)

            for activity in stats:
                total_dist = stats[activity]["distance"]
                pace_list = stats[activity]["pace"]
                avg_pace = sum(pace_list) / len(pace_list) if pace_list else 0.0
                max_dist = stats[activity]["max_distance"]
                unit_dist = "km" if activity in ["Run", "Walk"] else "m"
                unit_pace = "min/km" if activity in ["Run", "Walk"] else "min/100m"
                avg_pace_str = self.format_pace(avg_pace, unit_pace)
                stats_text.insert(tk.END, f"{activity}:\n")
                stats_text.insert(tk.END, f"Total Distance: {total_dist:.2f} {unit_dist}\n")
                stats_text.insert(tk.END, f"Average Pace: {avg_pace_str}\n")
                stats_text.insert(tk.END, f"Longest {activity}: {max_dist:.2f} {unit_dist}\n\n")

            stats_text.config(state="disabled")  # Make read-only but selectable

        except FileNotFoundError:
            stats_text.insert(tk.END, "No data available")
            stats_text.config(state="disabled")

    def show_profile(self):
        self.clear_content()
        self.current_view = "profile"
        self.log_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.stats_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.profile_button.config(bg=self.themes[self.current_theme]["active_bg"])

        theme = self.themes[self.current_theme]
        profile_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        profile_frame.pack(pady=20)

        tk.Label(profile_frame, text="Profile", font=("Arial", 20, "bold"), fg=theme["fg"], bg=theme["bg"]).pack(pady=10)

        fields = ["Name", "Age", "Weight (kg)", "Height (cm)"]
        self.profile_entries = {}
        try:
            with open("profile.csv", "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                data = next(reader, [""] * len(fields))
                profile_data = dict(zip(fields, data))
        except FileNotFoundError:
            profile_data = {field: "" for field in fields}

        for field in fields:
            tk.Label(profile_frame, text=f"{field}:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
            entry = tk.Entry(profile_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
            entry.insert(0, profile_data.get(field, ""))
            entry.pack(pady=2)
            self.profile_entries[field] = entry

        tk.Button(profile_frame, text="Save Profile", command=self.save_profile, font=("Arial", 12), bg="#2ECC71", fg="white", width=15, bd=0, activebackground="#27AE60").pack(pady=10)

    def save_profile(self):
        profile_data = [self.profile_entries[field].get() for field in ["Name", "Age", "Weight (kg)", "Height (cm)"]]
        with open("profile.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Age", "Weight (kg)", "Height (cm)"])
            writer.writerow(profile_data)
        messagebox.showinfo("Success", "Profile saved!")

    def parse_pace(self, pace_str):
        """Convert MM:SS pace to float minutes, handle legacy float values."""
        try:
            if ":" in pace_str:
                minutes, seconds = map(int, pace_str.split(":"))
                return minutes + seconds / 60.0
            else:
                return float(pace_str)  # Handle old float values
        except ValueError:
            raise ValueError("Pace must be in MM:SS format (e.g., 4:50) or a number")

    def format_pace(self, pace_float, unit):
        """Convert float minutes back to MM:SS for display."""
        minutes = int(pace_float)
        seconds = int((pace_float - minutes) * 60)
        return f"{minutes}:{seconds:02d} {unit}"

    def update_graph(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        theme = self.themes[self.current_theme]
        fig, ax = plt.subplots(figsize=(5, 4), facecolor=theme["bg"])
        ax.set_facecolor(theme["button_bg"])
        ax.tick_params(colors=theme["fg"])
        ax.spines['bottom'].set_color(theme["fg"])
        ax.spines['top'].set_color(theme["fg"])
        ax.spines['left'].set_color(theme["fg"])
        ax.spines['right'].set_color(theme["fg"])
        ax.grid(True, linestyle='--', alpha=0.7, color=theme["fg"])

        try:
            with open("workouts.csv", "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                print("CSV Header:", header)
                workouts = [row for row in reader if len(row) == 8]
                print(f"Loaded {len(workouts)} workouts")

            activity_filter = self.activity_var.get()
            metric = self.metric_var.get()
            metric_index = {"Distance": 5, "Pace": 6}[metric]
            unit = {
                "Distance": "km",
                "Pace": "min/km" if activity_filter in ["Run", "Walk", "All"] else "min/100m"
            }[metric]

            # Custom date range
            try:
                start_date = datetime.strptime(self.from_date_entry.get() + " 00:00", "%d.%m.%Y %H:%M")
                end_date = datetime.strptime(self.to_date_entry.get() + " 23:59", "%d.%m.%Y %H:%M")
                if start_date > end_date:
                    raise ValueError("Start date must be before end date")
            except ValueError as e:
                messagebox.showerror("Error", str(e) if str(e) != "Start date must be before end date" else "Invalid date format (use DD.MM.YYYY)")
                start_date = datetime.now() - timedelta(days=365)
                end_date = datetime.now()
                self.from_date_entry.delete(0, tk.END)
                self.from_date_entry.insert(0, start_date.strftime("%d.%m.%Y"))
                self.to_date_entry.delete(0, tk.END)
                self.to_date_entry.insert(0, end_date.strftime("%d.%m.%Y"))

            print(f"Graph range: {start_date.strftime('%d.%m.%Y %H:%M')} to {end_date.strftime('%d.%m.%Y %H:%M')}")

            # Dynamic month range
            months_count = ((end_date.year - start_date.year) * 12 + end_date.month - start_date.month) + 1
            month_labels = []
            current_date = start_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            for _ in range(months_count):
                month_labels.append(current_date.strftime("%b %Y"))
                next_month = current_date.month + 1 if current_date.month < 12 else 1
                next_year = current_date.year + 1 if current_date.month == 12 else current_date.year
                current_date = current_date.replace(month=next_month, year=next_year)

            # Stats per activity
            activities = ["Run", "Swim", "Walk"] if activity_filter == "All" else [activity_filter]
            colors = {"Run": "#3498DB", "Swim": "#2ECC71", "Walk": "#E74C3C"}
            monthly_values = {act: {month: 0.0 for month in month_labels} for act in activities}
            monthly_counts = {act: {month: 0 for month in month_labels} for act in activities}

            for row in workouts:
                date = row[0].strip('"')
                exercise = row[1].strip('"')
                value = row[metric_index].strip('"')
                print(f"Raw row: {row}")
                print(f"Checking - Date: {date}, Exercise: {exercise}, {metric}: {value}")
                if value and exercise in activities:
                    try:
                        entry_date = datetime.strptime(date, "%d.%m.%Y %H:%M")
                        if start_date <= entry_date <= end_date:
                            month = entry_date.strftime("%b %Y")
                            if month in month_labels:
                                if metric == "Pace":
                                    converted_value = self.parse_pace(value)
                                else:
                                    converted_value = float(value) / 1000 if exercise.lower() == "swim" else float(value)
                                monthly_values[exercise][month] += converted_value
                                monthly_counts[exercise][month] += 1
                                print(f"Added {converted_value} to {month} for {exercise} {metric}")
                    except ValueError:
                        print(f"Invalid date or pace format in row: {row}")
                        continue

            lines = []
            for act in activities:
                values = []
                for month in month_labels:
                    if monthly_counts[act][month] > 0:
                        if metric == "Pace":
                            avg_value = monthly_values[act][month] / monthly_counts[act][month]
                            values.append(avg_value)
                            print(f"Averaged Pace for {act} {month}: {avg_value}")
                        else:
                            values.append(monthly_values[act][month])
                            print(f"Total Distance for {act} {month}: {monthly_values[act][month]}")
                    else:
                        values.append(0.0)
                        print(f"No data for {act} {month}")
                line, = ax.plot(range(len(month_labels)), values, color=colors[act], marker="o", label=act)
                lines.append(line)

            ax.set_title(f"{metric} Over Time", color=theme["fg"])
            ax.set_ylabel(f"{metric} ({unit})", color=theme["fg"])
            ax.set_xticks(range(len(month_labels)))
            ax.set_xticklabels(month_labels, rotation=45, ha="right")
            ax.legend()

            cursor = mplcursors.cursor(lines, hover=True)
            @cursor.connect("add")
            def on_add(sel):
                index = int(sel.target[0])
                act = sel.artist.get_label()
                value = sel.target[1]
                month = month_labels[index]
                if metric == "Pace":
                    display_value = self.format_pace(value, unit.split()[0])
                else:
                    display_value = f"{value:.2f} {unit}"
                sel.annotation.set_text(f"{act} {month}: {display_value}")
                sel.annotation.get_bbox_patch().set_facecolor(theme["button_bg"])
                sel.annotation.get_bbox_patch().set_alpha(0.9)

        except FileNotFoundError:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center", color=theme["fg"])
            print("workouts.csv not found")

        self.current_fig = fig
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def save_graph(self):
        if hasattr(self, 'current_fig'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.current_fig.savefig(file_path, dpi=100, bbox_inches="tight")
                messagebox.showinfo("Success", "Graph saved successfully!")
        else:
            messagebox.showerror("Error", "No graph to save!")

    def clear_frame(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

    def show_run(self):
        self.clear_frame()
        self.activity_type = "Run"
        theme = self.themes[self.current_theme]
        tk.Label(self.input_frame, text="Date (DD.MM.YYYY HH:MM):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.date_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y %H:%M"))
        self.date_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.exercise_entry.insert(0, "Run")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Distance (km):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.distance_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.distance_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Pace (MM:SS min/km):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.pace_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.pace_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Notes:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.notes_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.notes_entry.pack(pady=2)
        tk.Button(self.input_frame, text="Log", command=self.log_activity, font=("Arial", 12), bg="#E74C3C", fg="white", width=10, bd=0, activebackground="#C0392B").pack(pady=10)

    def show_swim(self):
        self.clear_frame()
        self.activity_type = "Swim"
        theme = self.themes[self.current_theme]
        tk.Label(self.input_frame, text="Date (DD.MM.YYYY HH:MM):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.date_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y %H:%M"))
        self.date_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.exercise_entry.insert(0, "Swim")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Distance (m):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.distance_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.distance_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Pace (MM:SS min/100m):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.pace_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.pace_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Notes:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.notes_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.notes_entry.pack(pady=2)
        tk.Button(self.input_frame, text="Log", command=self.log_activity, font=("Arial", 12), bg="#E74C3C", fg="white", width=10, bd=0, activebackground="#C0392B").pack(pady=10)

    def show_walking(self):
        self.clear_frame()
        self.activity_type = "Walk"
        theme = self.themes[self.current_theme]
        tk.Label(self.input_frame, text="Date (DD.MM.YYYY HH:MM):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.date_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y %H:%M"))
        self.date_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Activity name:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.exercise_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.exercise_entry.insert(0, "Walk")
        self.exercise_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Distance (km):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.distance_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.distance_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Pace (MM:SS min/km):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.pace_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.pace_entry.pack(pady=2)
        tk.Label(self.input_frame, text="Notes:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
        self.notes_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20, bg=theme["entry_bg"])
        self.notes_entry.pack(pady=2)
        tk.Button(self.input_frame, text="Log", command=self.log_activity, font=("Arial", 12), bg="#E74C3C", fg="white", width=10, bd=0, activebackground="#C0392B").pack(pady=10)

    def log_activity(self):
        exercise = self.exercise_entry.get() or self.activity_type
        date = self.date_entry.get()
        notes = self.notes_entry.get()
        
        try:
            datetime.strptime(date, "%d.%m.%Y %H:%M")
            if self.activity_type in ["Run", "Walk"]:
                distance = self.distance_entry.get()
                pace = self.pace_entry.get()
                if not distance or not pace:
                    raise ValueError("Distance and pace are required for Run/Walk")
                distance = float(distance)
                pace_float = self.parse_pace(pace)  # Validate MM:SS
                row = [date, exercise, "", "", "", distance, pace, notes]  # Store pace as MM:SS
            elif self.activity_type == "Swim":
                distance = self.distance_entry.get()
                pace = self.pace_entry.get()
                if not distance or not pace:
                    raise ValueError("Distance and pace are required for Swim")
                distance = float(distance)
                pace_float = self.parse_pace(pace)  # Validate MM:SS
                row = [date, exercise, "", "", "", distance, pace, notes]  # Store pace as MM:SS

            with open("workouts.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(row)
            
            messagebox.showinfo("Success", f"Activity logged! Distance: {distance:.2f} {'m' if self.activity_type == 'Swim' else 'km'}")
            self.clear_frame()
            if self.current_view == "history":
                self.update_history()
        except ValueError as e:
            messagebox.showerror("Error", str(e) if str(e).startswith("Distance") else "Invalid input: Use DD.MM.YYYY HH:MM for date, numeric distance, and MM:SS for pace")

    def update_history(self):
        if self.current_view == "history" and hasattr(self, 'tree'):
            for item in self.tree.get_children():
                self.tree.delete(item)
            total_distance_km = 0.0
            try:
                with open("workouts.csv", "r") as file:
                    reader = csv.reader(file)
                    header = next(reader)
                    filter_type = self.filter_var.get()
                    for i, row in enumerate(reader):
                        if len(row) < 8:
                            continue
                        exercise = row[1].strip('"')
                        if filter_type == "All" or filter_type.lower() in exercise.lower():
                            tag = "evenrow" if i % 2 == 0 else "oddrow"
                            distance = float(row[5].strip('"'))
                            pace = row[6].strip('"')  # Keep as MM:SS
                            notes = row[7].strip('"')
                            dist_unit = "m" if exercise.lower() == "swim" else "km"
                            pace_unit = "min/100m" if exercise.lower() == "swim" else "min/km"
                            display_row = [row[0].strip('"'), exercise, f"{distance:.2f} {dist_unit}", f"{pace} {pace_unit}", notes]
                            self.tree.insert("", "end", values=display_row, tags=(tag,))
                            total_distance_km += distance / 1000 if exercise.lower() == "swim" else distance
                    self.stats_label.config(text=f"Total Distance: {total_distance_km:.2f} km")
            except FileNotFoundError:
                self.stats_label.config(text="No data available")

    def delete_records(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select at least one record to delete!")
            return
        
        selected_values = [self.tree.item(item, "values") for item in selected_items]
        
        with open("workouts.csv", "r") as file:
            reader = csv.reader(file)
            header = next(reader)
            all_rows = list(reader)
        
        updated_rows = []
        for row in all_rows:
            distance = float(row[5].strip('"'))
            pace = row[6].strip('"')
            exercise = row[1].strip('"')
            dist_unit = "m" if exercise.lower() == "swim" else "km"
            pace_unit = "min/100m" if exercise.lower() == "swim" else "min/km"
            display_row = (
                row[0].strip('"'),
                exercise,
                f"{distance:.2f} {dist_unit}",
                f"{pace} {pace_unit}",
                row[7].strip('"')
            )
            
            if display_row not in selected_values:
                updated_rows.append(row)
        
        with open("workouts.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(updated_rows)
        
        self.update_history()
        messagebox.showinfo("Success", f"{len(selected_items)} record(s) deleted!")

    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a record to edit!")
            return
        if len(selected_item) > 1:
            messagebox.showwarning("Multiple Selection", "Please select only one record to edit!")
            return
        selected_values = self.tree.item(selected_item[0], "values")
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Record")
        self.edit_window.geometry("300x350")
        theme = self.themes[self.current_theme]
        self.edit_window.configure(bg=theme["bg"])
        fields = ["Date", "Exercise", "Distance", "Pace", "Notes"]
        # Strip units from distance and pace for editing
        display_values = [selected_values[0], selected_values[1], selected_values[2].split()[0], selected_values[3].split()[0], selected_values[4]]
        self.edit_entries = {}
        for i, (field, value) in enumerate(zip(fields, display_values)):
            tk.Label(self.edit_window, text=f"{field}:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=2)
            entry = tk.Entry(self.edit_window, font=("Arial", 12), width=20, bg=theme["entry_bg"])
            entry.insert(0, value)
            entry.pack(pady=2)
            self.edit_entries[field] = entry
        tk.Button(self.edit_window, text="Save Changes", command=lambda: self.save_edit(selected_values), font=("Arial", 12), bg="#2ECC71", fg="white", width=15, bd=0, activebackground="#27AE60").pack(pady=10)

    def save_edit(self, old_values):
        new_values = [self.edit_entries[field].get() for field in ["Date", "Exercise", "Distance", "Pace", "Notes"]]
        
        # Validate new values
        try:
            datetime.strptime(new_values[0], "%d.%m.%Y %H:%M")  # Date validation
            float(new_values[2])  # Distance validation
            self.parse_pace(new_values[3])  # Pace validation
        except ValueError as e:
            messagebox.showerror("Error", "Invalid input: Use DD.MM.YYYY HH:MM for date, numeric distance, and MM:SS for pace")
            return

        with open("workouts.csv", "r") as file:
            reader = csv.reader(file)
            header = next(reader)
            all_rows = list(reader)
        
        updated_rows = []
        for row in all_rows:
            distance = float(row[5].strip('"'))
            pace = row[6].strip('"')
            exercise = row[1].strip('"')
            dist_unit = "m" if exercise.lower() == "swim" else "km"
            pace_unit = "min/100m" if exercise.lower() == "swim" else "min/km"
            display_row = (
                row[0].strip('"'),
                exercise,
                f"{distance:.2f} {dist_unit}",
                f"{pace} {pace_unit}",
                row[7].strip('"')
            )
            
            if display_row == old_values:
                # Replace with new values, keeping the CSV structure
                updated_rows.append([new_values[0], new_values[1], "", "", "", new_values[2], new_values[3], new_values[4]])
            else:
                updated_rows.append(row)
        
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
                header = next(reader)
                for row in reader:
                    if len(row) == 8:
                        writer = csv.writer(target)
                        writer.writerow(row)
            self.update_history()
            messagebox.showinfo("Success", "Workouts imported successfully!")

    def backup_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile="workouts_backup.csv")
        if file_path:
            shutil.copy("workouts.csv", file_path)
            messagebox.showinfo("Success", "Data backed up successfully!")

    def restore_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            shutil.copy(file_path, "workouts.csv")
            self.update_history()
            messagebox.showinfo("Success", "Data restored successfully!")

try:
    with open("workouts.csv", "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        if header != ["date", "exercise", "sets", "reps", "weight", "distance", "pace", "notes"]:
            raise ValueError("CSV format outdated")
except (FileNotFoundError, ValueError):
    with open("workouts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "exercise", "sets", "reps", "weight", "distance", "pace", "notes"])

root = tk.Tk()
app = WorkoutTrackerApp(root)
root.mainloop()