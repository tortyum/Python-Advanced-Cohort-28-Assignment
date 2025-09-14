import os
from datetime import datetime

# Custom exception for duplicate visitors


class DuplicateVisitorError(Exception):
    pass

# Read the last visitor from the file


def get_last_visitor(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()         # Read all lines from the file
            if lines:
                # Get the last line
                last_line = lines[-1].strip()
                if last_line:
                    # Extract name before the ','
                    return last_line.split(',')[0]
    except FileNotFoundError:        # If file doesn't exist,
        return None
    return None

# Add a new visitor with the current timestamp


def add_visitor(filename, name):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # Current timestamp
    with open(filename, 'a', encoding='utf-8') as f:  # Open file in append mode
        f.write(f"{name} | {timestamp}\n")   # Append new visitor

# Main function to handle user input and file operations


def main():
    filename = 'visitors.txt'
    # Get visitor's name from user input
    name = input('Enter visitor\'s name: ').strip()
    normalized_name = name.lower()
    try:
        # Get the last visitor from the file
        last_visitor = get_last_visitor(filename)
        normalized_last_visitor = last_visitor.strip().lower() if last_visitor else ""
        if normalized_last_visitor == normalized_name:
            # Raise error if duplicate
            raise DuplicateVisitorError(f"Duplicate visitor: {name}")
        add_visitor(filename, name)
        print(f"Visitor '{name}' added with timestamp.")  # Confirm addition
    except DuplicateVisitorError as e:
        print(f"Error: {e}")
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
