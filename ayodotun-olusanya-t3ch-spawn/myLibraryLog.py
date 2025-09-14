from datetime import datetime, timedelta

# Write a program that will help a librarian handle a visitor's log to the library, but the librarian hates when the same person signs in twice
# Program should keep a file called visitors.txt
# Each time the program runs it should ask the user for the visitor's name, before adding the name, check the last line in the file
# If the last line is the same name, raise a custom exception error, otherwise add the name with a timestamp

# If the file does not exist, create it. Use with statement, handle errors

class DuplicateVisitorError(Exception):
    def __init__(self, name, time):
        self.message = f"Visitor '{name}' already signed inlast at {time}! No back to back visits allowed"

        super().__init__(self.message)

# This checks if a file exists
def doesFileExist(fileName):
    try:
        with open(fileName, 'r') as f:
            return True
    except FileNotFoundError:
        return False

# Function takes in time in a specific format and returns the amount of seconds between now and the time value which was passed
def convertTimeToSeconds(time):
    if(time == ""): return [500]
    prevTime = datetime.strptime(time, "time: %H:%M:%S, %Y-%m-%d")
    timeGap =  datetime.now() - prevTime
    timeWait = prevTime + timedelta(minutes=5)
    return [timeGap.total_seconds(), timeWait.strftime("%H:%M:%S")]
    

fileName = 'visitors.txt'

def logVisitor():

    visitorName = input("What is your name?: ")
    lastVisitor = ""
    lastVisitorTime = ""


    #Open the file and read through it  
    with open(fileName, 'r') as visitorsFile:
        visitorsList = visitorsFile.readlines()
        
        # Checking if the length of the list is greater than 1
        if(len(visitorsList) > 1):
             lastVisitor = visitorsList[-1].strip()
             lastVisitorTime = lastVisitor.split(' | ')[-1]
    
       
    # Check if the last visitor name is the same as the visitor trying to log   
    if(lastVisitor.split(' | ')[0].strip().lower() == visitorName.lower().strip() and lastVisitor != ""):
       
        raise DuplicateVisitorError(visitorName, lastVisitorTime)
    
    
    # Check if it has been up to five minutes since the last visitor has signed in     
    if(convertTimeToSeconds(lastVisitorTime)[0] < 300 and lastVisitorTime != ""):
            timeLoggedIn = lastVisitorTime.split('time: ')[1].split(',')[0]

            print(f"Error: The last visitor signed in less than 5 minutes ago at {timeLoggedIn}, wait till {convertTimeToSeconds(lastVisitorTime)[1]}")

    # If all checks pass, append the visitor's name and time to the text file
    else:
         with open(fileName, 'a') as visitorsFile:
             timeNow = datetime.now().strftime("%H:%M:%S, %Y-%m-%d")
             visitorsFile.write(f"\n{visitorName} | time: {timeNow}\n")
             print(f"{visitorName} has logged in at {timeNow}")


  
def main():
    if(doesFileExist(fileName)):
        try:
            logVisitor()
        except DuplicateVisitorError as e:
            print(f"Error: {e}")
    else:
        print(f"{fileName} file does not exist, creating one now...")
        with open(fileName, 'x') as visitorsFile:
            print('    ')
            print('    ')
            print('    ')
            logVisitor()

main()




# If a visitor visits by 10:00, no other visitor should be allowed to visit until 10:05