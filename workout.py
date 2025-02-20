def log_workout():
    exercise = input("Enter exercise name: ")
    sets = input("Enter number of sets: ")
    reps = input("Enter number of reps: ")
    weight = input("Enter weight (kg): ")
    
    with open("workouts.txt", "a") as file:
        file.write(f"{exercise}, {sets} sets, {reps} reps, {weight} kg\n")
    
    print("Workout logged!")

while True:
    log_workout()
    again = input("Log another workout? (y/n): ")
    if again.lower() != "y":
        break