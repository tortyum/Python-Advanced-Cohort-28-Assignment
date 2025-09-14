import datetime

class DuplicateVisitorError(Exception):
    pass

class CooldownError(Exception):
    pass

def log_visitor():
    name = input("Enter visitor's name: ").strip()
    
    visitors = []
    try:
        with open("visitors.txt", "r") as f:
            visitors = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        pass  # file doesn’t exist yet, no problem

    # Check duplicates
    if any(name in line for line in visitors):
        raise DuplicateVisitorError(f"Visitor '{name}' already exists")

    # Check time of last visitor
    if visitors:
        last_line = visitors[-1]
        last_time_str = last_line.split(" - ")[0]  # timestamp part
        last_time = datetime.datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        diff = (now - last_time).total_seconds()

        if diff < 300:  # 300 seconds = 5 minutes
            raise CooldownError("Another visitor cannot be logged until 5 minutes have passed")

    # Log visitor with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("visitors.txt", "a") as f:
        f.write(f"{timestamp} - Visitor {name} logged successfully\n")

try:
    log_visitor()
except DuplicateVisitorError as e:
    print("Error:", e)
except CooldownError as e:
    print("Error:", e)
except Exception as e:
    print("Unexpected error:", e)
