import os
from datetime import datetime, timedelta

# Custom Exception
class DuplicateVisitorError(Exception):
    pass

def log_visitor():
    filename = "visitors.txt"
    visitor_name = input("Enter visitor's name: ").strip()

    try:
        # If file does not exist, create it
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                pass  

        with open(filename, "r") as file:
            lines = file.readlines()

        # Check if file is not empty
        if lines:
            last_line = lines[-1].strip()
            last_name, last_time = last_line.split(" | ")

            # Check for duplicate visitor
            if last_name == visitor_name:
                raise DuplicateVisitorError(f"Duplicate entry: {visitor_name} just visited.")

            # Check time difference (5 minutes rule)
            last_time = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - last_time < timedelta(minutes=5):
                print("⏳ Another visitor is not allowed until 5 minutes have passed.")
                return

        # Log visitor with timestamp
        with open(filename, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{visitor_name} | {timestamp}\n")
            print(f" Visitor {visitor_name} logged at {timestamp}")

    except DuplicateVisitorError as e:
        print("Error:", e)

    except Exception as e:
        print(" An unexpected error occurred:", e)


# Run program
if __name__ == "_main_":
    log_visitor()