import os
import datetime

# simple custom error for same visitor


class DuplicateVisitorError(Exception):
    pass


def get_last_visitor(file):
    if not os.path.exists(file):
        return None

    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) == 0:
        return None

    last_line = lines[-1].strip()
    if "Name:" in last_line:
        # split by comma to ignore timestamp
        return last_line.split("Name:")[1].split(",")[0].strip()
    return None


def main():
    filename = "visitors.txt"
    name = input("Enter visitor name: ").strip()

    if name == "":
        print("No name entered!")
        return

    try:
        last = get_last_visitor(filename)
        if last and last.lower() == name.lower():
            raise DuplicateVisitorError(
                f"{name} was already the last visitor.")

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = "Name: " + name + ", Timestamp: " + now + "\n"

        f = open(filename, "a", encoding="utf-8")
        f.write(entry)
        f.close()

        print("New visitor logged:", name)

    except DuplicateVisitorError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
