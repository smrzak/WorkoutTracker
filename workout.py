import csv

def log_workout():
    print("What type of activity?")
    print("1. Workout  2. Run  3. Swim  4. Walking")
    choice = input("Enter 1, 2, 3, or 4: ")

    if choice == "1":
        default_exercise = "workout"
    elif choice == "2":
        default_exercise = "run"
    elif choice == "3":
        default_exercise = "swim"
    elif choice == "4":
        default_exercise = "walking"
    else:
        print("Invalid choice, try again!")
        return

    exercise = input(f"Activity name [{default_exercise}]: ") or default_exercise

    if choice == "1":  # Workout
        sets = input("Enter number of sets: ")
        reps = input("Enter number of reps: ")
        weight = input("Enter weight (kg): ")
        row = [exercise, sets, reps, weight, "", ""]
    elif choice == "2" or choice == "4":  # Run or Walking
        distance = input("Enter distance (km): ")
        pace = input("Enter pace (min/km): ")
        row = [exercise, "", "", "", distance, pace]
    elif choice == "3":  # Swim
        distance = float(input("Enter distance (m): "))
        time = float(input("Enter total time (min): "))
        pace = (time / distance) * 100  # Pace in min/100m
        row = [exercise, "", "", "", distance, pace]

    with open("workouts.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)
    
    print(f"Activity logged! Pace: {pace if choice == '3' else ''} min/100m" if choice == "3" else "Activity logged!")

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