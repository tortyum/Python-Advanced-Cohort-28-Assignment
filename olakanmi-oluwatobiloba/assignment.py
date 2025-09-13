#Import the datetime class from the datetime module
from datetime import datetime

# Define a custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
  def __init__(self, name):
    # Set a custom message if a visitor tries to sign in twice in a row
    self.message = f"Visitor '{name}' already signed in last! No back to back visits allowed."
    # Call the base Exception class with this message
    super().__init__(self.message)

# Define the main function that runs the program
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
  visitor = input("Enter visitor's name ")
  
  try:
    # Open the file to read the existing visitors' records
    with open(filename, "r", encoding="utf-8") as f:
      # Read all lines into a list
      lines = f.readlines()
      # Get the name of the last visitor
    if lines:
        last_line = lines[-1].strip().split(" | ") # Split the last line into name and timestamp
        last_visitor = last_line[0]
        last_time = datetime.fromisoformat(last_line[1])
    else:
        last_visitor = None
        last_time = None

      
    # Check if the new visitor is the same as last
    if visitor == last_visitor:
      # If yes, raise our custom DuplicateVisitorError
      raise DuplicateVisitorError(visitor)
    
    if last_time:
     # Calculate the time difference in minutes between now and the last visit
        now = datetime.now()
        minutes_diff = (now - last_time).total_seconds() / 60
    
        # If the last visit was less than 5 minutes ago, show an error and exit
    if last_time and minutes_diff < 5:
        print(f"Error: You must wait {round(5 - minutes_diff, 1)} minute(s) before signing in again.")
        return
    
    # If not a duplicate, open the file in append mode
    with open(filename, "a", encoding="utf-8") as f:
      # write the visitor's name and the current date and time
      f.write(f"{visitor} | {datetime.now()}\n")
      
    # Tell the user everything worked fine
    print("Visitor added successfully!")
    

  
  # Catch the custom error if a duplicate user was detected
  except DuplicateVisitorError as e:
    # Print out the error message
    print("Error:", e)
    
# Run the program
main()