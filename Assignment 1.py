
from datetime import datetime, timedelta
import os

# Errors
class DuplicateVisitorError(Exception): pass
class VisitTooSoonError(Exception): pass

def main():
    filename = "visitors.txt"

    # Make sure file exists
    if not os.path.exists(filename):
        open(filename, "w").close()

    print("Visitor logging system (type 'q' to quit)\n")

    while True:
        visitor = input("Enter visitor's name: ").strip()

        if visitor.lower() == "q":
            print("Goodbye!")
            break
        if not visitor:
            print("No name entered.\n")
            continue

        # Read last visitor (if any)
        with open(filename, "r") as f:
            lines = f.readlines()

        last_name, last_time = None, None
        if lines:
            try:
                last_name, time_str = lines[-1].split("|")
                last_name = last_name.strip()
                last_time = datetime.fromisoformat(time_str.strip())
            except:
                pass  # ignore bad line format

        now = datetime.now()

        try:
            # Rule 1: same visitor twice
            if last_name and visitor == last_name:
                raise DuplicateVisitorError(f"{visitor} just signed in already!")

            # Rule 2: 5 minutes wait
            if last_time and (now - last_time) < timedelta(minutes=5):
                wait = timedelta(minutes=5) - (now - last_time)
                raise VisitTooSoonError(f"Wait {int(wait.total_seconds()//60)}m {int(wait.total_seconds()%60)}s before next visitor.")

            # Passed checks → save
            with open(filename, "a") as f:
                f.write(f"{visitor} | {now.isoformat()}\n")

            print("Visitor added successfully.\n")

        except (DuplicateVisitorError, VisitTooSoonError) as e:
            print(e, "\n")

if __name__ == "__main__":
    main()
