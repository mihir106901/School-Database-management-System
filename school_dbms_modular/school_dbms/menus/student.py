from ..db import exec_query
from ..utils import prompt_int, prompt_str, print_table

def student_menu(cnx):
    while True:
        print("\n--- STUDENT RECORDS ---")
        print("1. Add new student")
        print("2. Update student")
        print("3. Add new column (advanced)")
        print("4. Search student by GR number")
        print("5. Back")

        cho = prompt_int("Your choice: ")

        if cho == 1:
            add_student(cnx)
        elif cho == 2:
            update_student(cnx)
        elif cho == 3:
            add_column(cnx)
        elif cho == 4:
            search_student(cnx)
        elif cho == 5:
            break
        else:
            print("Invalid choice.")

def add_student(cnx):
    g = prompt_int("GR number: ")
    r = prompt_int("Roll number: ")
    n = prompt_str("Name: ")
    m = prompt_str("Mobile number: ")
    a = prompt_str("Address: ")
    ca = prompt_int("Class: ")
    s = prompt_str("Section: ")

    sql = """INSERT INTO student
    (GR_number, Roll_number, Name, Mobile_Number, Address, Class, Section)
    VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    exec_query(cnx, sql, (g, r, n, m, a, ca, s))
    print("✅ Student added successfully.")

def update_student(cnx):
    g = prompt_int("Enter GR number: ")
    row = exec_query(cnx, "SELECT GR_number, Roll_number, Name, Mobile_Number, Address, Class, Section FROM student WHERE GR_number=%s", (g,), fetch="one")
    if row is None:
        print("Student not found.")
        return

    print("Current details:")
    print(f"Name: {row[2]}")
    print(f"Roll Number: {row[1]}")
    print(f"Mobile Number: {row[3]}")
    print(f"Address: {row[4]}")
    print(f"Class: {row[5]}")
    print(f"Section: {row[6]}")

    def skip(field):
        val = input(f"Updated {field} (press Enter to skip): ").strip()
        return val if val != "" else None

    new_name = skip("name")
    new_roll = skip("roll number")
    new_mobile = skip("mobile number")
    new_address = skip("address")
    new_class = skip("class")
    new_section = skip("section")

    updates = []
    params = []
    if new_name is not None:
        updates.append("Name=%s"); params.append(new_name)
    if new_roll is not None:
        updates.append("Roll_number=%s"); params.append(int(new_roll))
    if new_mobile is not None:
        updates.append("Mobile_Number=%s"); params.append(new_mobile)
    if new_address is not None:
        updates.append("Address=%s"); params.append(new_address)
    if new_class is not None:
        updates.append("Class=%s"); params.append(int(new_class))
    if new_section is not None:
        updates.append("Section=%s"); params.append(new_section)

    if not updates:
        print("No changes made.")
        return

    sql = "UPDATE student SET " + ", ".join(updates) + " WHERE GR_number=%s"
    params.append(g)
    exec_query(cnx, sql, tuple(params))
    print("✅ Student updated successfully.")

def add_column(cnx):
    print("⚠️ Advanced: This executes ALTER TABLE. Use carefully.")
    name = prompt_str("New column name: ")
    col_type = prompt_str("New column SQL type (e.g., VARCHAR(50), INT, DATE): ")
    # Can't parameterize identifiers; we minimally validate.
    import re
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        print("Invalid column name.")
        return
    sql = f"ALTER TABLE student ADD COLUMN {name} {col_type}"
    exec_query(cnx, sql)
    print("✅ Column added successfully.")

def search_student(cnx):
    g = prompt_int("Enter GR number: ")
    rows, cols = exec_query(cnx, "SELECT * FROM student WHERE GR_number=%s", (g,), fetch="all")
    print_table(rows, cols)
