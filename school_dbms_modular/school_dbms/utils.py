from prettytable import PrettyTable

def print_table(rows, columns):
    if not rows:
        print("No records found.")
        return
    t = PrettyTable()
    t.field_names = columns
    for r in rows:
        t.add_row(r)
    print(t)

def prompt_int(label: str) -> int:
    while True:
        try:
            return int(input(label))
        except ValueError:
            print("Please enter a valid integer.")

def prompt_str(label: str) -> str:
    return input(label).strip()

def pause():
    input("\nPress Enter to continue...")
