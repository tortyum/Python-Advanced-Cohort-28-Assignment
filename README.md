 Visitors Log Program 

 Files
- visitors.py → Main Python program  
- visitors.txt → Stores visitor names with timestamps

 How It Works
1. Each time you run the program, it asks for the visitor’s name.  
2. It checks the timestamp of the last visitor in `visitors.txt`:  
   - If the last visitor was logged **less than 5 minutes ago**, no new visitor is allowed (a `TooSoonError` is raised).  
   - Otherwise, the new visitor’s name and timestamp are added.  
3. If `visitors.txt` doesn’t exist, the program creates it automatically.

Run Instructions
python visitors.py
Enter the visitor’s name when asked.  
The program will automatically prevent any new visitor from being added if it’s less than 5 minutes since the last one.
