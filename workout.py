import csv  

def log_workout():
    exercise = input("Enter exercise name: ")
    sets = input("Enter number of sets: ")
    reps = input("Enter number of reps: ")
    weight = input("Enter weight (kg): ")
    
    with open("workouts.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([exercise, sets, reps, weight])
    
    print("Workout logged!")

try:
    with open("workouts.csv", "r"):
        pass  
except FileNotFoundError:
    with open("workouts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["exercise", "sets", "reps", "weight"])

while True:
    log_workout()
    again = input("Log another workout? (y/n): ")
    if again.lower() != "y":
        break


#https://github.com/smrzak/WorkoutTracker.git