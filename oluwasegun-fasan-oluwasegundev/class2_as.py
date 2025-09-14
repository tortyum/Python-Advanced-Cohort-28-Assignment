# import the datetime class from the datetime modelu
from datetime import datetime


class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = f"Visitor {name} has already signed in"
        
        super().__init__(self.message)
        

def main():
    filename = "visitor.txt"
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        with open(filename, "w", encoding="utf-8") as f:
            pass
        
    visitor = input("Enter visitor's name ")
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_visitor = lines[-1].split(" | ")[0] if lines else None
        if visitor == last_visitor:
            raise DuplicateVisitorError(visitor)
        
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{visitor} | {datetime.now()}\n")
            
        print("visitor added successfully")
        
    except DuplicateVisitorError as e:
        print("Error:", e)
      
      
main()  