import os
from datetime import datetime, timedelta

class DuplicateVisitorError(Exception):
    """Custom exception raised when the same visitor tries to enter consecutively."""
    pass

class VisitorTooSoonError(Exception):
    """Custom exception raised when a visitor tries to enter before 5 minutes have passed."""
    pass

def get_last_visitor_info(filename):
    """
    Read the last line from the visitors file and extract visitor name and timestamp.
    
    Returns:
        tuple: (visitor_name, timestamp) or (None, None) if file is empty or doesn't exist
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                # Format: "Name - YYYY-MM-DD HH:MM:SS"
                if ' - ' in last_line:
                    name_part, time_part = last_line.rsplit(' - ', 1)
                    try:
                        timestamp = datetime.strptime(time_part, '%Y-%m-%d %H:%M:%S')
                        return name_part, timestamp
                    except ValueError:
                        print("Warning: Invalid timestamp format in last entry")
                        return None, None
    except FileNotFoundError:
        # File doesn't exist yet, this is fine
        pass
    except Exception as e:
        print(f"Error reading file: {e}")
    
    return None, None

def add_visitor(filename, visitor_name):
    """
    Add a visitor to the file with current timestamp.
    
    Args:
        filename (str): Path to the visitors file
        visitor_name (str): Name of the visitor to add
    """
    current_time = datetime.now()
    timestamp_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # Create file if it doesn't exist, append if it does
        with open(filename, 'a') as file:
            file.write(f"{visitor_name} - {timestamp_str}\n")
        print(f"Visitor '{visitor_name}' added successfully at {timestamp_str}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        raise

def main():
    """Main function to run the visitor management system."""
    filename = "visitors.txt"
    
    print("=== Visitor Management System ===")
    print("Type 'quit' to exit the program\n")
    
    while True:
        try:
            # Get visitor name from user
            visitor_name = input("Enter visitor's name: ").strip()
            
            if visitor_name.lower() == 'quit':
                print("Goodbye!")
                break
            
            if not visitor_name:
                print("Please enter a valid name.\n")
                continue
            
            # Get information about the last visitor
            last_visitor_name, last_timestamp = get_last_visitor_info(filename)
            current_time = datetime.now()
            
            # Check for duplicate visitor (same name as last entry)
            if last_visitor_name and last_visitor_name.lower() == visitor_name.lower():
                raise DuplicateVisitorError(f"Duplicate visitor detected: '{visitor_name}' was the last visitor to enter.")
            
            # Check if 5 minutes have passed since last visitor
            if last_timestamp:
                time_diff = current_time - last_timestamp
                if time_diff < timedelta(minutes=5):
                    remaining_time = timedelta(minutes=5) - time_diff
                    remaining_seconds = int(remaining_time.total_seconds())
                    remaining_minutes = remaining_seconds // 60
                    remaining_secs = remaining_seconds % 60
                    
                    raise VisitorTooSoonError(
                        f"Please wait {remaining_minutes}m {remaining_secs}s before allowing another visitor. "
                        f"Last visitor was at {last_timestamp.strftime('%H:%M:%S')}"
                    )
            
            # If we get here, it's safe to add the visitor
            add_visitor(filename, visitor_name)
            
        except DuplicateVisitorError as e:
            print(f"Error: {e}")
            print("The same visitor cannot enter consecutively.\n")
            
        except VisitorTooSoonError as e:
            print(f"Error: {e}\n")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("The program will continue running.\n")

def display_all_visitors():
    """Utility function to display all visitors (for testing)."""
    filename = "visitors.txt"
    try:
        with open(filename, 'r') as file:
            print("\n=== All Visitors ===")
            lines = file.readlines()
            if lines:
                for i, line in enumerate(lines, 1):
                    print(f"{i}. {line.strip()}")
            else:
                print("No visitors recorded yet.")
        print()
    except FileNotFoundError:
        print("No visitor file found yet.\n")
    except Exception as e:
        print(f"Error reading visitors file: {e}\n")

if __name__ == "__main__":
   
    # display_all_visitors()
    
    main()