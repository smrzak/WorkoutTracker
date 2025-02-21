import csv
import tkinter as tk
from tkinter import messagebox

class WorkoutTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Tracker")
        self.root.geometry("500x600")  # Set window size
        self.root.configure(bg="#2C3E50")  # Dark blue background

        # Title Label
        tk.Label(root, text="Workout Tracker", font=("Arial", 20, "bold"), fg="#ECF0F1", bg="#2C3E50").pack(pady=20)

        # Buttons Frame
        button_frame = tk.Frame(root, bg="#2C3E50")
        button_frame.pack(pady=10)

        # Activity Buttons with style
        btn_style = {"font": ("Arial", 15), "bg": "#3498DB", "fg": "white", "width": 18, "bd": 0, "activebackground": "#2980B9"}
        tk.Button(button_frame, text="Gym", command=self.show_gym, **btn_style).pack(pady=5)
        tk.Button(button_frame, text="Run", command=self.show_run, **btn_style).pack(pady=5)
        tk.Button(button_frame, text="Swim", command=self.show_swim, **btn_style).pack(pady=5)
        tk.Button(button_frame, text="Walk", command=self.show_walking, **btn_style).pack(pady=5)

        # Input Frame
        self.input_frame = tk.Frame(root, bg="#2C3E50")
        self.input_frame.pack(pady=20)

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
        
        if self.activity_type == "Gym":  # Updated to match button
            sets = self.sets_entry.get()
            reps = self.reps_entry.get()
            weight = self.weight_entry.get()
            row = [exercise, sets, reps, weight, "", ""]
        elif self.activity_type in ["Run", "Walk"]:  # Updated to match buttons
            distance = self.distance_entry.get()
            pace = self.pace_entry.get()
            row = [exercise, "", "", "", distance, pace]
        elif self.activity_type == "Swim":  # Updated to match button
            distance = float(self.distance_entry.get())
            time = float(self.time_entry.get())
            pace = (time / distance) * 100
            row = [exercise, "", "", "", distance, pace]

        with open("workouts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
        
        messagebox.showinfo("Success", f"Activity logged! Pace: {pace if self.activity_type == 'Swim' else ''} min/100m" if self.activity_type == "Swim" else "Activity logged!")
        self.clear_frame()

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