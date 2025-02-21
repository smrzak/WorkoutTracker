import csv
import tkinter as tk
from tkinter import messagebox, filedialog, ttk, colorchooser
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

        self.style = ttk.Style()
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
        self.goals_button = tk.Button(button_frame, text="Goals", command=self.show_goals, **btn_style)  # New Goals tab
        self.goals_button.pack(side="left", padx=5)
        self.plans_button = tk.Button(button_frame, text="Plans", command=self.show_plans, **btn_style)  # New Plans tab
        self.plans_button.pack(side="left", padx=5)
        self.profile_button = tk.Button(button_frame, image=self.profile_icon if self.profile_icon else None, text="Profile" if not self.profile_icon else "", compound="left", bg=self.themes[self.current_theme]["button_bg"], fg=self.themes[self.current_theme]["fg"], bd=0, command=self.show_profile)
        self.profile_button.pack(side="left", padx=5)

        self.theme_button = tk.Button(button_frame, image=self.dark_icon if self.dark_icon else None, text="Dark" if not self.dark_icon else "", compound="left", bg=self.themes[self.current_theme]["button_bg"], bd=0, command=self.switch_theme)
        self.theme_button.pack(side="right", padx=5)

        self.apply_theme()

    def load_theme(self):
        try:
            with open("settings.csv", "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                if header == ["theme"]:  # Old format
                    theme = next(reader)[0]
                    return theme if theme in self.themes else "dark"
                elif header == ["theme", "bg", "fg", "button_bg", "active_bg", "entry_bg"]:  # New custom theme format
                    for row in reader:
                        if row[0] == "custom":
                            self.themes["custom"] = {"bg": row[1], "fg": row[2], "button_bg": row[3], "active_bg": row[4], "entry_bg": row[5]}
                            return "custom"
                    return "dark"
        except (FileNotFoundError, IndexError):
            return "dark"

    def save_theme(self):
        with open("settings.csv", "w", newline="") as file:
            writer = csv.writer(file)
            if self.current_theme == "custom":
                writer.writerow(["theme", "bg", "fg", "button_bg", "active_bg", "entry_bg"])
                theme = self.themes["custom"]
                writer.writerow(["custom", theme["bg"], theme["fg"], theme["button_bg"], theme["active_bg"], theme["entry_bg"]])
            else:
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
        if self.current_theme == "dark":
            self.current_theme = "light"
        elif self.current_theme == "light":
            self.current_theme = "dark"
        else:  # Custom theme, switch to dark
            self.current_theme = "dark"
        self.save_theme()
        self.apply_theme()

    def create_custom_theme(self):
        custom_window = tk.Toplevel(self.root)
        custom_window.title("Create Custom Theme")
        custom_window.geometry("300x500")
        theme = self.themes[self.current_theme]
        custom_window.configure(bg=theme["bg"])

        colors = {"bg": "Background", "fg": "Foreground", "button_bg": "Button BG", "active_bg": "Active BG", "entry_bg": "Entry BG"}
        self.custom_colors = {key: tk.StringVar(value=self.themes[self.current_theme][key]) for key in colors}

        for key, label in colors.items():
            tk.Label(custom_window, text=f"{label}:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(pady=5)
            color_frame = tk.Frame(custom_window, bg=theme["bg"])
            color_frame.pack(pady=2)
            tk.Entry(color_frame, textvariable=self.custom_colors[key], font=("Arial", 12), width=10, bg=theme["entry_bg"]).pack(side="left", padx=5)
            tk.Button(color_frame, text="Pick", command=lambda k=key: self.pick_color(k), font=("Arial", 12), bg=theme["button_bg"], fg=theme["fg"]).pack(side="left")

        tk.Button(custom_window, text="Save Theme", command=self.save_custom_theme, font=("Arial", 12), bg="#2ECC71", fg="white", width=15, bd=0, activebackground="#27AE60").pack(pady=20)

    def pick_color(self, key):
        color = colorchooser.askcolor(title=f"Choose {key} Color", initialcolor=self.custom_colors[key].get())[1]
        if color:
            self.custom_colors[key].set(color)

    def save_custom_theme(self):
        self.themes["custom"] = {key: self.custom_colors[key].get() for key in self.custom_colors}
        self.current_theme = "custom"
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
        elif self.current_view == "goals":
            self.show_goals()
        elif self.current_view == "plans":
            self.show_plans()
        elif self.current_view == "profile":
            self.show_profile()

    def show_log(self):
        self.clear_content()
        self.current_view = "log"
        self.log_button.config(bg=self.themes[self.current_theme]["active_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.stats_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.goals_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.plans_button.config(bg=self.themes[self.current_theme]["button_bg"])
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
        self.show_run()  # Default view

    def show_history(self):
        self.clear_content()
        self.current_view = "history"
        self.log_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["active_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.stats_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.goals_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.plans_button.config(bg=self.themes[self.current_theme]["button_bg"])
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
        self.goals_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.plans_button.config(bg=self.themes[self.current_theme]["button_bg"])
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
        self.goals_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.plans_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.profile_button.config(bg=self.themes[self.current_theme]["button_bg"])

        theme = self.themes[self.current_theme]
        stats_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        stats_frame.pack(pady=20)

        tk.Label(stats_frame, text="Activity Stats", font=("Arial", 20, "bold"), fg=theme["fg"], bg=theme["bg"]).pack(pady=10)

        stats_text = tk.Text(stats_frame, height=20, width=50, font=("Arial", 12), fg=theme["fg"], bg=theme["bg"], wrap="word")
        stats_text.pack(pady=5)

        # Progress Bar for Monthly Distance (Goal: 50 km)
        progress_frame = tk.Frame(stats_frame, bg=theme["bg"])
        progress_frame.pack(pady=10)
        monthly_goal = 50.0  # Hardcoded goal for now
        self.progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(progress_frame, maximum=monthly_goal, length=200, variable=self.progress_var)
        progress_bar.pack(pady=5)
        self.progress_label = tk.Label(progress_frame, text="Distance this month: 0/50 km", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"])
        self.progress_label.pack()

        try:
            with open("workouts.csv", "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                workouts = [row for row in reader if len(row) == 8]

            if not workouts:
                stats_text.insert(tk.END, "No workout data available")
                stats_text.config(state="disabled")
                self.progress_label.config(text="Distance this month: 0/50 km")
                return

            stats = {
                "Run": {"distance": 0.0, "pace": [], "max_distance": 0.0, "min_pace": float('inf')},
                "Swim": {"distance": 0.0, "pace": [], "max_distance": 0.0, "min_pace": float('inf')},
                "Walk": {"distance": 0.0, "pace": [], "max_distance": 0.0, "min_pace": float('inf')}
            }
            current_month = datetime.now().month
            current_year = datetime.now().year
            monthly_distance = 0.0
            workout_dates = []

            for row in workouts:
                exercise = row[1].strip('"')
                distance = row[5].strip('"')
                pace = row[6].strip('"')
                date_str = row[0].strip('"')
                if exercise in stats and distance and pace:
                    dist_value = float(distance) / 1000 if exercise.lower() == "swim" else float(distance)
                    pace_value = self.parse_pace(pace)
                    stats[exercise]["distance"] += dist_value
                    stats[exercise]["pace"].append(pace_value)
                    stats[exercise]["max_distance"] = max(stats[exercise]["max_distance"], dist_value)
                    stats[exercise]["min_pace"] = min(stats[exercise]["min_pace"], pace_value)
                    # Progress bar calculation
                    date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
                    if date.month == current_month and date.year == current_year:
                        monthly_distance += dist_value
                    workout_dates.append(date.date())

            # Update progress bar
            self.progress_var.set(monthly_distance)
            self.progress_label.config(text=f"Distance this month: {monthly_distance:.2f}/{monthly_goal} km")

            # Advanced Stats: Longest Streak
            workout_dates.sort()
            max_streak = current_streak = 1
            for i in range(1, len(workout_dates)):
                if (workout_dates[i] - workout_dates[i-1]).days == 1:
                    current_streak += 1
                    max_streak = max(max_streak, current_streak)
                else:
                    current_streak = 1

            for activity in stats:
                total_dist = stats[activity]["distance"]
                pace_list = stats[activity]["pace"]
                avg_pace = sum(pace_list) / len(pace_list) if pace_list else 0.0
                max_dist = stats[activity]["max_distance"]
                min_pace = stats[activity]["min_pace"] if stats[activity]["min_pace"] != float('inf') else 0.0
                unit_dist = "km" if activity in ["Run", "Walk"] else "m"
                unit_pace = "min/km" if activity in ["Run", "Walk"] else "min/100m"
                avg_pace_str = self.format_pace(avg_pace, unit_pace)
                min_pace_str = self.format_pace(min_pace, unit_pace) if min_pace > 0 else "N/A"
                stats_text.insert(tk.END, f"{activity}:\n")
                stats_text.insert(tk.END, f"Total Distance: {total_dist:.2f} {unit_dist}\n")
                stats_text.insert(tk.END, f"Average Pace: {avg_pace_str}\n")
                stats_text.insert(tk.END, f"Fastest Pace: {min_pace_str}\n")
                stats_text.insert(tk.END, f"Longest {activity}: {max_dist:.2f} {unit_dist}\n\n")

            stats_text.insert(tk.END, f"Longest Workout Streak: {max_streak} days\n")
            stats_text.config(state="disabled")

        except FileNotFoundError:
            stats_text.insert(tk.END, "No data available")
            stats_text.config(state="disabled")
            self.progress_label.config(text="Distance this month: 0/50 km")

    def show_goals(self):
        self.clear_content()
        self.current_view = "goals"
        self.log_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.stats_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.goals_button.config(bg=self.themes[self.current_theme]["active_bg"])
        self.plans_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.profile_button.config(bg=self.themes[self.current_theme]["button_bg"])

        theme = self.themes[self.current_theme]
        goals_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        goals_frame.pack(pady=20)

        tk.Label(goals_frame, text="Goals", font=("Arial", 20, "bold"), fg=theme["fg"], bg=theme["bg"]).pack(pady=10)

        # Goal input form
        input_frame = tk.Frame(goals_frame, bg=theme["bg"])
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Activity:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(side="left", padx=5)
        self.goal_activity_var = tk.StringVar(value="Run")
        ttk.Combobox(input_frame, textvariable=self.goal_activity_var, values=["Run", "Swim", "Walk"], state="readonly", width=10).pack(side="left", padx=5)
        tk.Label(input_frame, text="Target (km/m):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(side="left", padx=5)
        self.goal_target_entry = tk.Entry(input_frame, font=("Arial", 12), width=10, bg=theme["entry_bg"])
        self.goal_target_entry.pack(side="left", padx=5)
        tk.Label(input_frame, text="Period:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(side="left", padx=5)
        self.goal_period_var = tk.StringVar(value="Weekly")
        ttk.Combobox(input_frame, textvariable=self.goal_period_var, values=["Weekly", "Monthly"], state="readonly", width=10).pack(side="left", padx=5)
        tk.Button(input_frame, text="Add Goal", command=self.add_goal, font=("Arial", 12), bg="#2ECC71", fg="white", bd=0, activebackground="#27AE60").pack(side="left", padx=10)

        # Goals display
        self.goals_tree = ttk.Treeview(goals_frame, columns=("Activity", "Target", "Period", "Progress"), show="headings", height=10)
        self.goals_tree.pack(pady=10, fill="both", expand=True)
        self.goals_tree.heading("Activity", text="Activity")
        self.goals_tree.heading("Target", text="Target")
        self.goals_tree.heading("Period", text="Period")
        self.goals_tree.heading("Progress", text="Progress")
        self.goals_tree.column("Activity", width=100)
        self.goals_tree.column("Target", width=100)
        self.goals_tree.column("Period", width=100)
        self.goals_tree.column("Progress", width=200)
        scrollbar = ttk.Scrollbar(goals_frame, orient="vertical", command=self.goals_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.goals_tree.configure(yscrollcommand=scrollbar.set)

        tk.Button(goals_frame, text="Delete Selected", command=self.delete_goal, font=("Arial", 12), bg="#E74C3C", fg="white", width=15, bd=0, activebackground="#C0392B").pack(pady=5)

        self.update_goals()

    def add_goal(self):
        activity = self.goal_activity_var.get()
        try:
            target = float(self.goal_target_entry.get())
            period = self.goal_period_var.get()
        except ValueError:
            messagebox.showerror("Error", "Target must be a number")
            return

        with open("goals.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([activity, target, period])
        
        self.goal_target_entry.delete(0, tk.END)
        self.update_goals()

    def delete_goal(self):
        selected_items = self.goals_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a goal to delete!")
            return
        
        selected_values = [self.goals_tree.item(item, "values")[:3] for item in selected_items]  # Exclude progress
        try:
            with open("goals.csv", "r") as file:
                reader = csv.reader(file)
                all_rows = list(reader)
        except FileNotFoundError:
            return

        updated_rows = [row for row in all_rows if row not in selected_values]
        with open("goals.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        
        self.update_goals()

    def update_goals(self):
        for item in self.goals_tree.get_children():
            self.goals_tree.delete(item)
        
        try:
            with open("goals.csv", "r") as file:
                reader = csv.reader(file)
                goals = list(reader)
            with open("workouts.csv", "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                workouts = [row for row in reader if len(row) == 8]
        except FileNotFoundError:
            goals = []

        current_time = datetime.now()
        for i, goal in enumerate(goals):
            if len(goal) != 3:
                continue
            activity, target, period = goal[0], float(goal[1]), goal[2]
            unit = "km" if activity in ["Run", "Walk"] else "m"
            start_date = (current_time - timedelta(days=7)) if period == "Weekly" else current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            progress = 0.0
            for row in workouts:
                date = datetime.strptime(row[0].strip('"'), "%d.%m.%Y %H:%M")
                if date >= start_date and row[1].strip('"') == activity:
                    dist_value = float(row[5].strip('"')) / 1000 if activity.lower() == "swim" else float(row[5].strip('"'))
                    progress += dist_value
            display_row = (activity, f"{target:.2f} {unit}", period, f"{progress:.2f}/{target:.2f} {unit}")
            self.goals_tree.insert("", "end", values=display_row, tags=("evenrow" if i % 2 == 0 else "oddrow",))

    def show_plans(self):
        self.clear_content()
        self.current_view = "plans"
        self.log_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.stats_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.goals_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.plans_button.config(bg=self.themes[self.current_theme]["active_bg"])
        self.profile_button.config(bg=self.themes[self.current_theme]["button_bg"])

        theme = self.themes[self.current_theme]
        plans_frame = tk.Frame(self.content_frame, bg=theme["bg"])
        plans_frame.pack(pady=20)

        tk.Label(plans_frame, text="Workout Plans", font=("Arial", 20, "bold"), fg=theme["fg"], bg=theme["bg"]).pack(pady=10)

        # Plan input form
        input_frame = tk.Frame(plans_frame, bg=theme["bg"])
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Day:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(side="left", padx=5)
        self.plan_day_var = tk.StringVar(value="Monday")
        ttk.Combobox(input_frame, textvariable=self.plan_day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], state="readonly", width=10).pack(side="left", padx=5)
        tk.Label(input_frame, text="Activity:", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(side="left", padx=5)
        self.plan_activity_var = tk.StringVar(value="Run")
        ttk.Combobox(input_frame, textvariable=self.plan_activity_var, values=["Run", "Swim", "Walk"], state="readonly", width=10).pack(side="left", padx=5)
        tk.Label(input_frame, text="Distance (km/m):", font=("Arial", 12), fg=theme["fg"], bg=theme["bg"]).pack(side="left", padx=5)
        self.plan_distance_entry = tk.Entry(input_frame, font=("Arial", 12), width=10, bg=theme["entry_bg"])
        self.plan_distance_entry.pack(side="left", padx=5)
        tk.Button(input_frame, text="Add Plan", command=self.add_plan, font=("Arial", 12), bg="#2ECC71", fg="white", bd=0, activebackground="#27AE60").pack(side="left", padx=10)

        # Plans display
        self.plans_tree = ttk.Treeview(plans_frame, columns=("Day", "Activity", "Distance", "Done"), show="headings", height=10)
        self.plans_tree.pack(pady=10, fill="both", expand=True)
        self.plans_tree.heading("Day", text="Day")
        self.plans_tree.heading("Activity", text="Activity")
        self.plans_tree.heading("Distance", text="Distance")
        self.plans_tree.heading("Done", text="Done")
        self.plans_tree.column("Day", width=100)
        self.plans_tree.column("Activity", width=100)
        self.plans_tree.column("Distance", width=100)
        self.plans_tree.column("Done", width=100)
        scrollbar = ttk.Scrollbar(plans_frame, orient="vertical", command=self.plans_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.plans_tree.configure(yscrollcommand=scrollbar.set)
        self.plans_tree.bind("<Double-1>", self.toggle_plan_done)

        tk.Button(plans_frame, text="Delete Selected", command=self.delete_plan, font=("Arial", 12), bg="#E74C3C", fg="white", width=15, bd=0, activebackground="#C0392B").pack(pady=5)

        self.update_plans()

    def add_plan(self):
        day = self.plan_day_var.get()
        activity = self.plan_activity_var.get()
        try:
            distance = float(self.plan_distance_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Distance must be a number")
            return

        unit = "km" if activity in ["Run", "Walk"] else "m"
        with open("plans.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([day, activity, f"{distance:.2f} {unit}", "No"])
        
        self.plan_distance_entry.delete(0, tk.END)
        self.update_plans()

    def delete_plan(self):
        selected_items = self.plans_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a plan to delete!")
            return
        
        selected_values = [self.plans_tree.item(item, "values") for item in selected_items]
        try:
            with open("plans.csv", "r") as file:
                reader = csv.reader(file)
                all_rows = list(reader)
        except FileNotFoundError:
            return

        updated_rows = [row for row in all_rows if tuple(row) not in selected_values]
        with open("plans.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        
        self.update_plans()

    def toggle_plan_done(self, event):
        item = self.plans_tree.identify_row(event.y)
        if item:
            values = list(self.plans_tree.item(item, "values"))
            values[3] = "Yes" if values[3] == "No" else "No"
            self.plans_tree.item(item, values=values)
            
            with open("plans.csv", "r") as file:
                reader = csv.reader(file)
                all_rows = list(reader)
            for i, row in enumerate(all_rows):
                if tuple(row) == self.plans_tree.item(item, "values"):
                    all_rows[i][3] = values[3]
            with open("plans.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(all_rows)

    def update_plans(self):
        for item in self.plans_tree.get_children():
            self.plans_tree.delete(item)
        
        try:
            with open("plans.csv", "r") as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if len(row) == 4:
                        tag = "evenrow" if i % 2 == 0 else "oddrow"
                        self.plans_tree.insert("", "end", values=row, tags=(tag,))
        except FileNotFoundError:
            pass

    def show_profile(self):
        self.clear_content()
        self.current_view = "profile"
        self.log_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.history_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.graphs_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.stats_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.goals_button.config(bg=self.themes[self.current_theme]["button_bg"])
        self.plans_button.config(bg=self.themes[self.current_theme]["button_bg"])
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
        tk.Button(profile_frame, text="Custom Theme", command=self.create_custom_theme, font=("Arial", 12), bg="#3498DB", fg="white", width=15, bd=0, activebackground="#2980B9").pack(pady=5)

        # Achievements section
        tk.Label(profile_frame, text="Achievements", font=("Arial", 16, "bold"), fg=theme["fg"], bg=theme["bg"]).pack(pady=10)
        achievements_text = tk.Text(profile_frame, height=10, width=50, font=("Arial", 12), fg=theme["fg"], bg=theme["bg"], wrap="word")
        achievements_text.pack(pady=5)
        self.update_achievements(achievements_text)
        achievements_text.config(state="disabled")

    def save_profile(self):
        profile_data = [self.profile_entries[field].get() for field in ["Name", "Age", "Weight (kg)", "Height (cm)"]]
        with open("profile.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Age", "Weight (kg)", "Height (cm)"])
            writer.writerow(profile_data)
        messagebox.showinfo("Success", "Profile saved!")

    def update_achievements(self, text_widget):
        achievements = {
            "First 10 km Run": {"type": "Run", "distance": 10, "earned": False},
            "50 Workouts": {"count": 50, "earned": False},
            "Fast Swimmer": {"type": "Swim", "pace": 1.5, "earned": False}  # Pace <= 1:30 min/100m
        }
        
        try:
            with open("workouts.csv", "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                workouts = [row for row in reader if len(row) == 8]

            for row in workouts:
                exercise = row[1].strip('"')
                distance = float(row[5].strip('"'))
                pace = self.parse_pace(row[6].strip('"'))
                if exercise == "Run" and distance >= 10:
                    achievements["First 10 km Run"]["earned"] = True
                if exercise == "Swim" and pace <= 1.5:
                    achievements["Fast Swimmer"]["earned"] = True
            if len(workouts) >= 50:
                achievements["50 Workouts"]["earned"] = True

            for name, details in achievements.items():
                status = "Earned" if details["earned"] else "Not Earned"
                text_widget.insert(tk.END, f"{name}: {status}\n")

        except FileNotFoundError:
            text_widget.insert(tk.END, "No workout data to calculate achievements")

    def parse_pace(self, pace_str):
        try:
            if ":" in pace_str:
                minutes, seconds = map(int, pace_str.split(":"))
                return minutes + seconds / 60.0
            else:
                return float(pace_str)
        except ValueError:
            raise ValueError("Pace must be in MM:SS format (e.g., 4:50) or a number")

    def format_pace(self, pace_float, unit):
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
                workouts = [row for row in reader if len(row) == 8]

            activity_filter = self.activity_var.get()
            metric = self.metric_var.get()
            metric_index = {"Distance": 5, "Pace": 6}[metric]
            unit = {"Distance": "km", "Pace": "min/km" if activity_filter in ["Run", "Walk", "All"] else "min/100m"}[metric]

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

            months_count = ((end_date.year - start_date.year) * 12 + end_date.month - start_date.month) + 1
            month_labels = []
            current_date = start_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            for _ in range(months_count):
                month_labels.append(current_date.strftime("%b %Y"))
                next_month = current_date.month + 1 if current_date.month < 12 else 1
                next_year = current_date.year + 1 if current_date.month == 12 else current_date.year
                current_date = current_date.replace(month=next_month, year=next_year)

            activities = ["Run", "Swim", "Walk"] if activity_filter == "All" else [activity_filter]
            colors = {"Run": "#3498DB", "Swim": "#2ECC71", "Walk": "#E74C3C"}
            monthly_values = {act: {month: 0.0 for month in month_labels} for act in activities}
            monthly_counts = {act: {month: 0 for month in month_labels} for act in activities}

            for row in workouts:
                date = row[0].strip('"')
                exercise = row[1].strip('"')
                value = row[metric_index].strip('"')
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
                    except ValueError:
                        continue

            lines = []
            for act in activities:
                values = []
                for month in month_labels:
                    if monthly_counts[act][month] > 0:
                        if metric == "Pace":
                            avg_value = monthly_values[act][month] / monthly_counts[act][month]
                            values.append(avg_value)
                        else:
                            values.append(monthly_values[act][month])
                    else:
                        values.append(0.0)
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
                pace_float = self.parse_pace(pace)
                row = [date, exercise, "", "", "", distance, pace, notes]
            elif self.activity_type == "Swim":
                distance = self.distance_entry.get()
                pace = self.pace_entry.get()
                if not distance or not pace:
                    raise ValueError("Distance and pace are required for Swim")
                distance = float(distance)
                pace_float = self.parse_pace(pace)
                row = [date, exercise, "", "", "", distance, pace, notes]

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
                            pace = row[6].strip('"')
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
            display_row = (row[0].strip('"'), exercise, f"{distance:.2f} {dist_unit}", f"{pace} {pace_unit}", row[7].strip('"'))
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
        try:
            datetime.strptime(new_values[0], "%d.%m.%Y %H:%M")
            float(new_values[2])
            self.parse_pace(new_values[3])
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
            display_row = (row[0].strip('"'), exercise, f"{distance:.2f} {dist_unit}", f"{pace} {pace_unit}", row[7].strip('"'))
            if display_row == old_values:
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