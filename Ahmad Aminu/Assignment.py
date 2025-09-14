import os
import time
from datetime import datetime, timedelta

# Custom exceptions
class DuplicateVisitorError(Exception):
    pass

class WaitTimeError(Exception):
    pass

FILENAME = "visitors.txt"

def get_last_visitor():
    """Return (name, timestamp) of the last visitor or None if file empty."""
    if not os.path.exists(FILENAME):
        return None

    with open(FILENAME, "r") as file:
        lines = file.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip()
        try:
            name, timestamp = last_line.split(" | ")
            return name, datetime.fromisoformat(timestamp)
        except ValueError:
            return None

def log_visitor(name):
    """Log visitor with timestamp."""
    now = datetime.now()
    with open(FILENAME, "a") as file:
        file.write(f"{name} | {now.isoformat()}\n")
    print(f"✅ Visitor {name} added at {now.strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    try:
        visitor_name = input("Enter visitor's name: ").strip()
        last_visitor = get_last_visitor()

        if last_visitor:
            last_name, last_time = last_visitor

            # Check duplicate name
            if visitor_name.lower() == last_name.lower():
                raise DuplicateVisitorError(f"❌ {visitor_name} already visited last.")

            # Check 5-minute gap
            if datetime.now() - last_time < timedelta(minutes=5):
                wait_time = 5 - (datetime.now() - last_time).seconds // 60
                raise WaitTimeError(f"⏳ Please wait {wait_time} more minute(s) before another visitor.")

        # If no issues, log visitor
        log_visitor(visitor_name)

    except DuplicateVisitorError as e:
        print(e)
    except WaitTimeError as e:
        print(e)
    except Exception as e:
        print("⚠️ An unexpected error occurred:", e)

if __name__ == "__main__":
    main()