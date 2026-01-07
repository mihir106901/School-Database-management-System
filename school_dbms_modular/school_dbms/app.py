from .config import load_config
from .db import connect_db
from .menus.student import student_menu
from .menus.fees import fees_menu
from .menus.library import library_menu
from .menus.exam import exam_menu
from .menus.delete_student import delete_student_menu
from .utils import prompt_int, pause

def run():
    cfg = load_config()
    cnx = connect_db(cfg)

    try:
        while True:
            print("\n==========================")
            print("      STUDENT SYSTEM      ")
            print("==========================")
            print("1. Student Records")
            print("2. Payment Records")
            print("3. Library Records")
            print("4. Exams Records")
            print("5. Delete Student and Associated Records")
            print("6. Exit")

            ch = prompt_int("Your choice: ")

            if ch == 1:
                student_menu(cnx)
            elif ch == 2:
                fees_menu(cnx)
            elif ch == 3:
                library_menu(cnx)
            elif ch == 4:
                exam_menu(cnx)
            elif ch == 5:
                delete_student_menu(cnx)
            elif ch == 6:
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
            pause()
    finally:
        cnx.close()
