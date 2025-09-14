from add_visitor import add_visitor, DuplicateVisitorError, VisitorIntervalError

def main() -> None:
    """
    Main entry point for the visitor logging system.
    Handles user interaction and error reporting.
    """
    print("=== Visitor Registration ===")
    try:
        name: str = input("Enter visitor's name: ").strip()
        if not name:
            print("Name cannot be empty.")  # Validation for empty input
            return
        add_visitor(name)
    except DuplicateVisitorError as e:
        print("Error:", e)
    except VisitorIntervalError as e:
        print("Error:", e)
    except Exception as e:
        # Catch-all safety net for unexpected errors
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()
