#!/usr/bin/env python3
# Shebang line (mainly for Linux/Mac). Lets you run this script directly if it has execute permissions.

"""
visitor_logger.py
Simple visitor logger with:
 - visitors.txt file (one "Name | YYYY-MM-DD HH:MM:SS" per line)
 - DuplicateVisitorError if the last name equals the new name (case-insensitive)
 - VisitorLockedError if last visit was less than lock_minutes ago
 - Safe 'with' file handling and graceful messages
"""

from datetime import datetime, timedelta  # datetime for timestamps, timedelta for "5 minute lock"
from pathlib import Path  # Path gives easy file existence checks and file operations

# File where visitor names and timestamps will be stored.
# By default, it's created in the same folder where you run this script.
VISITOR_FILE = "visitors.txt"

# --- Custom exceptions (for clearer error handling) ---
class DuplicateVisitorError(Exception):
    """Raised when the new visitor name matches the last recorded name."""
    pass

class VisitorLockedError(Exception):
    """Raised when a new visitor is not allowed due to minimum wait time (5 mins by default)."""
    pass

# --- Helper functions ---
def parse_entry_line(line: str):
    """
    Parse a single line of the visitor file.
    Expected format: "<Name> | YYYY-MM-DD HH:MM:SS"
    Returns (name, datetime) if valid, or None if line is invalid/corrupt.
    """
    if not line:
        return None
    line = line.strip()
    if not line:
        return None
    try:
        # rsplit splits only at the last '|'
        # This avoids breaking names that might contain '|'
        name_part, ts_part = line.rsplit('|', 1)
        name = name_part.strip()
        ts_str = ts_part.strip()
        # Parse the timestamp string into a datetime object
        ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        return name, ts
    except Exception:
        # If parsing fails, treat line as invalid
        return None

def get_last_entry(file_path: str):
    """
    Return (name, timestamp) of the last valid entry in file_path,
    or None if file doesn't exist or has no valid lines.
    """
    p = Path(file_path)
    if not p.exists():
        return None  # No file yet → no previous visitors

    try:
        with p.open("r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        # Re-raise file reading errors so caller can handle (e.g. permissions issue)
        raise

    # Loop through lines in reverse order to find the most recent valid entry
    for line in reversed(lines):
        parsed = parse_entry_line(line)
        if parsed:
            return parsed
    return None  # If no valid lines found

def add_visitor(name: str, file_path: str = VISITOR_FILE, lock_minutes: int = 5):
    """
    Try to add a visitor. Raises:
      - DuplicateVisitorError if name matches last visitor (case-insensitive)
      - VisitorLockedError if last visitor was less than lock_minutes ago
      - ValueError for empty name
      - OSError for file write errors
    Returns the appended entry string on success.
    """
    # --- Input validation ---
    if not isinstance(name, str):
        raise ValueError("Name must be a string.")
    name = name.strip()
    if not name:
        raise ValueError("Visitor name cannot be empty.")

    now = datetime.now()  # Current local time
    last = get_last_entry(file_path)  # Fetch the last visitor entry (if any)

    if last:
        last_name, last_ts = last

        # --- Duplicate check (case-insensitive) ---
        if last_name.lower() == name.lower():
            raise DuplicateVisitorError(
                f"'{name}' is already the last recorded visitor (was recorded at {last_ts})."
            )

        # --- Lock-time check (5 minutes default) ---
        wait_delta = timedelta(minutes=lock_minutes)
        if now - last_ts < wait_delta:
            # Calculate how much longer to wait
            remaining = wait_delta - (now - last_ts)
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            raise VisitorLockedError(
                f"Please wait {minutes} minute(s) and {seconds} second(s) "
                f"before adding another visitor."
            )

    # If all checks pass → prepare the new entry
    entry = f"{name} | {now.strftime('%Y-%m-%d %H:%M:%S')}\n"

    # --- Write entry to file ---
    try:
        # "a" = append mode → file will be created if it doesn't exist
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry)
    except OSError as e:
        raise  # Re-raise file writing errors to caller

    return entry  # Return the string for confirmation

# --- Script entry point ---
if __name__ == "__main__":
    print("=== Visitor Logger ===")
    try:
        visitor_name = input("Enter visitor name: ").strip()
        added = add_visitor(visitor_name)
        print("Success — visitor recorded:")
        print(added.strip())
    except DuplicateVisitorError as e:
        print("DuplicateVisitorError:", e)
    except VisitorLockedError as e:
        print("VisitorLockedError:", e)
    except ValueError as e:
        print("Input error:", e)
    except OSError as e:
        print("File I/O error:", e)
    except Exception as e:
        print("Unexpected error:", e)
