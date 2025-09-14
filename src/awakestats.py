import matplotlib.pyplot as plt
import os

def save_driver_name(name, asleep, awake,filename="driver.txt"):
    # Check if file exists
    if not os.path.exists(filename):
        # Create and write driver name and stats
        with open(filename, "w") as f:
            f.write(name + " Time awake: " + str(awake) + " Time asleep: " + str(asleep) + "\n")
        print(f"File created and driver name '{name}' saved.")
    else:
        # Append driver name and stats
        with open(filename, "a") as f:
            f.write(name + " Time awake: " + str(awake) + " Time asleep: " + str(asleep) + "\n")
        print(f"Driver name '{name}' appended to file.")
    print("File will be saved at:", os.path.abspath(filename))