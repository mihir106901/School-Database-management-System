from ..db import exec_query
from ..utils import prompt_int, prompt_str

def delete_student_menu(cnx):
    print("\n--- DELETE STUDENT + ASSOCIATED RECORDS ---")
    g = prompt_int("Enter GR number: ")
    row = exec_query(cnx, "SELECT Name FROM student WHERE GR_number=%s", (g,), fetch="one")
    if row is None:
        print("Student not found.")
        return
    name = row[0]
    co = prompt_str(f"Is the student name '{name}'? (yes/no): ").lower()
    if co == "yes":
        # With ON DELETE CASCADE, this deletes fees/library/exam automatically
        exec_query(cnx, "DELETE FROM student WHERE GR_number=%s", (g,))
        print("✅ Student and associated records deleted successfully.")
    elif co == "no":
        print("Input correct GR number.")
    else:
        print("Invalid input.")
