import os
from datetime import datetime

class DuplicateVisitorError(Exception):
    """Custom exception for duplicate visitor."""
    pass

def get_last_visitor(filename):
    """Return the name in the last line of the file, or None if file is empty."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                return None
            last_line = lines[-1].strip()
            if not last_line:
                return None
            # Expected format: name,timestamp
            name, *_ = last_line.split(',', 1)
            return name
    except FileNotFoundError:
        # File does not exist yet
        return None

def add_visitor(filename, name):
    """Add visitor name and timestamp to file, checking for duplicates."""
    last_name = get_last_visitor(filename)
    if last_name == name:
        raise DuplicateVisitorError(f"Visitor '{name}' is already the last entry.")

    timestamp = datetime.now().isoformat(timespec='seconds')
    with open(filename, 'a') as file:
        file.write(f"{name},{timestamp}\n")

def main():
    filename = 'visitors.txt'
    try:
        name = input("Enter visitor's name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        add_visitor(filename, name)
        print(f"Visitor '{name}' added successfully.")
    except DuplicateVisitorError as e:
        print(f"Duplicate visitor: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
