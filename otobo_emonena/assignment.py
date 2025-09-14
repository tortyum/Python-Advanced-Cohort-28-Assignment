from datetime import datetime, timedelta
import os

# Custom Exceptions
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        super().__init__(f"Duplicate entry detected: {name}")


class WaitTimeError(Exception):
    def __init__(self, minutes):
        super().__init__(f"Please wait {minutes} minutes before another visitor can sign in.")


def main():
    filename = "visitors.txt"
    visitor_name = input("Enter visitor's name: ").strip()

    last_name = None
    last_time = None

    # ✅ Step 1: Check if file exists, else create it
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            pass  # create empty file

    # ✅ Step 2: Read last record
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1].strip()
            try:
                # Format: "Name | 2025-09-14 10:15:30"
                last_name, last_time_str = last_line.split(" | ")
                last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass  # if line is corrupted, ignore

    try:
        # ✅ Step 3: Check duplicate
        if visitor_name == last_name:
            raise DuplicateVisitorError(visitor_name)

        # ✅ Step 4: Check 5-minute rule
        if last_time and datetime.now() - last_time < timedelta(minutes=5):
            raise WaitTimeError(5)

        # ✅ Step 5: Append visitor with timestamp
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{visitor_name} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        print("Visitor added successfully!")

    except (DuplicateVisitorError, WaitTimeError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

        