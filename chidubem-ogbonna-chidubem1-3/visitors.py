from datetime import datetime, timedelta

class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = f"Visitor {name} already signed in last. No back-to-back visits."
        super().__init__(self.message)

class TimeRestrictionError(Exception):
    def __init__(self, minutes):
        self.message = f"New sign-in not allowed until {minutes} minutes have passed since the last visit."
        super().__init__(self.message)

def main():
    filename = "Visitor.txt"

    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        with open(filename, "w", encoding="utf-8") as f:
            pass

    visitor = input("Enter name: ")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                
                parts = [p.strip() for p in last_line.split("|")]
                if len(parts) == 2:
                    last_visitor, last_time_str = parts
                    try:
                        last_time = datetime.fromisoformat(last_time_str)
                    except ValueError:
                        
                        last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S.%f")
                    
                    
                    if visitor == last_visitor:
                        raise DuplicateVisitorError(visitor)

                    
                    if datetime.now() - last_time < timedelta(minutes=5):
                        raise TimeRestrictionError(5)

        
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{visitor} | {datetime.now().isoformat()}\n")

        print("Visitor added successfully.")

    except (DuplicateVisitorError, TimeRestrictionError) as e:
        print(f"Error: {e}")

main()
