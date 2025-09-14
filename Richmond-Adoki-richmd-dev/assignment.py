import os
import datetime

# custom error for same visitor


class DuplicateVisitorError(Exception):
    pass

# custom error for visitors coming too soon


class TooSoonError(Exception):
    pass


def get_last_entry(file):
    if not os.path.exists(file):
        return None, None

    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) == 0:
        return None, None

    last_line = lines[-1].strip()
    if last_line.startswith("Name:"):
        try:
            # "Name: John, Timestamp: 2025-09-14 12:34:56"
            parts = last_line.split(", Timestamp:")
            name = parts[0].split("Name:")[1].strip()
            timestamp = parts[1].strip()
            return name, timestamp
        except:
            return None, None
    return None, None


def main():
    filename = "visitors.txt"
    name = input("Enter visitor name: ").strip()

    if name == "":
        print("No name entered!")
        return

    try:
        last_name, last_time = get_last_entry(filename)

        # check duplicate name
        if last_name and last_name.lower() == name.lower():
            raise DuplicateVisitorError(
                f"{name} was already the last visitor.")

        # check time difference
        if last_time:
            last_dt = datetime.datetime.strptime(
                last_time, "%Y-%m-%d %H:%M:%S")
            now_dt = datetime.datetime.now()
            diff = (now_dt - last_dt).total_seconds() / 60.0  # in minutes
            if diff < 0:
                # Handle negative time difference due to system clock changes
                print("Warning: Negative time difference detected between now and last visitor timestamp. Skipping 'too soon' check.")
            elif diff < 5:
                raise TooSoonError(
                    f"New visitor not allowed yet. Wait {5-int(diff)} more minutes.")

        # log new visitor
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = "Name: " + name + ", Timestamp: " + now + "\n"

        f = open(filename, "a", encoding="utf-8")
        f.write(entry)
        f.close()

        print("New visitor logged:", name)

    except DuplicateVisitorError as e:
        print("Error:", e)
    except TooSoonError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
