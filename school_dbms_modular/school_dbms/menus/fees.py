from ..db import exec_query
from ..utils import prompt_int, print_table

def fees_menu(cnx):
    while True:
        print("\n--- FEES / PAYMENT RECORDS ---")
        print("1. Add new fees record")
        print("2. Update fees paid")
        print("3. Search fees by GR number")
        print("4. Back")

        cho = prompt_int("Your choice: ")

        if cho == 1:
            add_fees(cnx)
        elif cho == 2:
            update_fees_paid(cnx)
        elif cho == 3:
            search_fees(cnx)
        elif cho == 4:
            break
        else:
            print("Invalid choice.")

def add_fees(cnx):
    g = prompt_int("GR number: ")
    tuition = prompt_int("Tuition fee: ")
    tech = prompt_int("Technology fee: ")
    paid = prompt_int("Fees paid amount: ")
    sql = "INSERT INTO fees (GR_number, Tuition_Fee, Technology_Fee, Fees_Paid) VALUES (%s,%s,%s,%s)"
    exec_query(cnx, sql, (g, tuition, tech, paid))
    print("✅ Fees record added successfully.")

def update_fees_paid(cnx):
    g = prompt_int("GR number: ")
    row = exec_query(cnx, "SELECT GR_number, Tuition_Fee, Technology_Fee, Fees_Paid FROM fees WHERE GR_number=%s", (g,), fetch="one")
    if row is None:
        print("Fees record not found for this student.")
        return
    total = row[1] + row[2]
    paid = row[3]
    print(f"Total fees: {total}")
    print(f"Fees paid: {paid}")
    print(f"Fees remaining: {total - paid}")

    n = prompt_int("Fees paid now: ")
    new_paid = paid + n
    print(f"Fees remaining now: {total - new_paid}")

    exec_query(cnx, "UPDATE fees SET Fees_Paid=%s WHERE GR_number=%s", (new_paid, g))
    print("✅ Fees updated successfully.")

def search_fees(cnx):
    g = prompt_int("GR number: ")
    rows, cols = exec_query(cnx, "SELECT * FROM fees WHERE GR_number=%s", (g,), fetch="all")
    print_table(rows, cols)
