import csv

def log_workout():
    print("What type of activity?")
    print("1. Workout  2. Run")
    choice = input("Enter 1 or 2: ")

    exercise = input("Enter activity name (e.g., bench press or run): ")

    # Build the row based on choice
    if choice == "1":  # Workout
        sets = input("Enter number of sets: ")
        reps = input("Enter number of reps: ")
        weight = input("Enter weight (kg): ")
        row = [exercise, sets, reps, weight, "", ""]  # Distance and pace stay empty
    elif choice == "2":  # Run
        distance = input("Enter distance (km): ")
        pace = input("Enter pace (min/km): ")
        row = [exercise, "", "", "", distance, pace]  # Sets, reps, weight stay empty
    else:
        print("Invalid choice, try again!")
        return

    # Write to CSV
    with open("workouts.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)
    
    print("Activity logged!")

# Add headers if file doesn’t exist
try:
    with open("workouts.csv", "r"):
        pass
except FileNotFoundError:
    with open("workouts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["exercise", "sets", "reps", "weight", "distance", "pace"])

while True:
    log_workout()
    again = input("Log another activity? (y/n): ")
    if again.lower() != "y":
        break