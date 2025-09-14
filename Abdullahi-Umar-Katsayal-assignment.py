# Import the datetime and timedelta class from the datetime module
from datetime import datetime, timedelta

# Define a custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = f"Visitor '{name}' already signed in last! No back to back visits allowed."
        super().__init__(self.message)

# Define a custom exception for a time interval violation
class TimeIntervalError(Exception):
    def __init__(self, time_remaining):
        self.message = f"Please wait. The next visitor can sign in after {time_remaining:.0f} seconds."
        super().__init__(self.message)

def main():
    # The name of the file where the visitor records are stored
    filename = "visitors.txt"
    
    # Ensure the file exists before we start using it
    try:
        # Try opening the file in read mode
        with open(filename, "r", encoding="utf-8") as f:
            pass # Do nothing, just check if file exists
    except FileNotFoundError:
        # If file does not exist, create the file by opening in write mode
        print("file not found, creating a new file")
        with open(filename, "w", encoding="utf-8") as f:
            pass # Just create a new line
        
    # Ask the user to type the visitor's name
    visitor = input("Enter visitor's name: ")
    
    try:
        # Open the file to read the existing visitors' records
        with open(filename, "r", encoding="utf-8") as f:
            # Read all lines into a list
            lines = f.readlines()
            
            # Get the last visitor's name and entry time
            if lines:
                last_entry = lines[-1].strip().split(" | ")
                last_visitor = last_entry[0]
                # Parse the last visitor's timestamp from the file
                last_time = datetime.fromisoformat(last_entry[1])
            else:
                last_visitor = None
                last_time = None
            
        # Define the minimum interval between visitors
        min_interval = timedelta(minutes=5)
        
        # Get the current time
        now = datetime.now()
        
        # Check if the new visitor is the same as the last visitor
        if visitor == last_visitor:
            # If yes, raise the custom DuplicateVisitorError
            raise DuplicateVisitorError(visitor)
        
        # Check the time elapsed since the last visitor signed in
        if last_time and (now - last_time) < min_interval:
            # Calculate the time remaining before the next sign-in is allowed
            time_remaining = (min_interval - (now - last_time)).total_seconds()
            # Raise a custom TimeIntervalError if the waiting period has not passed
            raise TimeIntervalError(time_remaining)
        
        # If all checks pass, open the file in append mode
        with open(filename, "a", encoding="utf-8") as f:
            # write the visitor's name and the current date and time
            f.write(f"{visitor} | {now}\n")
            
        # Tell the user everything worked fine
        print("Visitor added successfully!")
    
    # Catch the custom time interval error
    except TimeIntervalError as e:
        # Print out the error message
        print("Error:", e)
    # Catch the custom duplicate error if a duplicate user was detected
    except DuplicateVisitorError as e:
        # Print out the error message
        print("Error:", e)
        
# Run the program
main()
