from datetime import date
from ..db import exec_query
from ..utils import prompt_int, prompt_str, print_table

def library_menu(cnx):
    while True:
        print("\n--- LIBRARY RECORDS ---")
        print("1. Issue a book (add record)")
        print("2. Update return date")
        print("3. Student history: books read by GR number")
        print("4. Book history: students who read a book")
        print("5. Pending returns (15+ days)")
        print("6. Top readers (by total days borrowed, top 5)")
        print("7. Back")

        cho = prompt_int("Your choice: ")

        if cho == 1:
            issue_book(cnx)
        elif cho == 2:
            return_book(cnx)
        elif cho == 3:
            books_by_student(cnx)
        elif cho == 4:
            students_by_book(cnx)
        elif cho == 5:
            pending_returns(cnx)
        elif cho == 6:
            top_readers(cnx)
        elif cho == 7:
            break
        else:
            print("Invalid choice.")

def issue_book(cnx):
    g = prompt_int("GR number: ")
    ti = prompt_int("Ticket number: ")
    book = prompt_str("Book name: ")
    isbn = prompt_str("ISBN: ")
    d_i = date.today()
    sql = """INSERT INTO library
    (GR_number, Ticket_number, Name_of_book_issued, ISBN, Date_of_issue, Date_of_return)
    VALUES (%s,%s,%s,%s,%s,%s)"""
    exec_query(cnx, sql, (g, ti, book, isbn, d_i, None))
    print("✅ Issue details added successfully.")

def return_book(cnx):
    g = prompt_int("GR number: ")
    book = prompt_str("Book name: ")
    d_r = date.today()
    sql = """UPDATE library
    SET Date_of_return=%s
    WHERE GR_number=%s AND Name_of_book_issued=%s AND Date_of_return IS NULL"""
    exec_query(cnx, sql, (d_r, g, book))
    print("✅ Return date updated (if matching open issue existed).")

def books_by_student(cnx):
    g = prompt_int("GR number: ")
    rows, cols = exec_query(cnx, "SELECT Name_of_book_issued, Date_of_issue, Date_of_return FROM library WHERE GR_number=%s ORDER BY Date_of_issue DESC", (g,), fetch="all")
    print_table(rows, cols)

def students_by_book(cnx):
    book = prompt_str("Book name: ")
    sql = """SELECT s.Name, s.Class, s.Section, l.Date_of_issue, l.Date_of_return
    FROM library l
    JOIN student s ON l.GR_number = s.GR_number
    WHERE l.Name_of_book_issued=%s
    ORDER BY l.Date_of_issue DESC"""
    rows, cols = exec_query(cnx, sql, (book,), fetch="all")
    print_table(rows, cols)

def pending_returns(cnx):
    sql = """SELECT s.Name, CONCAT(s.Class, '-', s.Section) AS class_section, l.Name_of_book_issued, l.Date_of_issue
    FROM library l
    JOIN student s ON l.GR_number = s.GR_number
    WHERE l.Date_of_return IS NULL
      AND CURDATE() > DATE_ADD(l.Date_of_issue, INTERVAL 15 DAY)
    ORDER BY l.Date_of_issue ASC"""
    rows, cols = exec_query(cnx, sql, fetch="all")
    print_table(rows, cols)

def top_readers(cnx):
    sql = """SELECT s.Name,
    SUM(DATEDIFF(l.Date_of_return, l.Date_of_issue)) AS total_time_in_days
    FROM library l
    JOIN student s ON l.GR_number = s.GR_number
    WHERE l.Date_of_return IS NOT NULL
    GROUP BY s.Name
    ORDER BY total_time_in_days DESC
    LIMIT 5"""
    rows, cols = exec_query(cnx, sql, fetch="all")
    print_table(rows, cols)
