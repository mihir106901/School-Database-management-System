from ..db import exec_query
from ..utils import prompt_int, prompt_str, print_table

def _marks(x: str):
    x = x.strip()
    if x == "":
        return None
    try:
        v = float(x)
    except ValueError:
        return None
    if v == 0:
        return None
    return v

def exam_menu(cnx):
    while True:
        print("\n--- EXAM RECORDS ---")
        print("1. Add new exam record")
        print("2. Update pending marks (fills NULLs)")
        print("3. Student marks + plot (optional)")
        print("4. Section toppers for an exam (top 3)")
        print("5. Class toppers for an exam (top 3)")
        print("6. Overall class toppers (top 3 per class)")
        print("7. Back")

        cho = prompt_int("Your choice: ")

        if cho == 1:
            add_exam(cnx)
        elif cho == 2:
            update_pending(cnx)
        elif cho == 3:
            student_marks_plot(cnx)
        elif cho == 4:
            section_toppers(cnx)
        elif cho == 5:
            class_toppers(cnx)
        elif cho == 6:
            overall_toppers(cnx)
        elif cho == 7:
            break
        else:
            print("Invalid choice.")

def add_exam(cnx):
    g = prompt_int("GR number: ")
    print("NOTE: If you don't know marks now or exam is pending, input 0 (stored as NULL).")

    fields = ["First_UT","Second_UT","Third_UT","Fourth_UT","PRE_MID_TERM","MID_TERM","POST_MID_TERM","ANNUAL"]
    vals = []
    for f in fields:
        vals.append(_marks(input(f"Enter {f} marks: ")))

    sql = """INSERT INTO exam (GR_number, First_UT, Second_UT, Third_UT, Fourth_UT, PRE_MID_TERM, MID_TERM, POST_MID_TERM, ANNUAL)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    exec_query(cnx, sql, (g, *vals))
    print("✅ Exam details added successfully.")

def update_pending(cnx):
    g = prompt_int("GR number: ")
    row = exec_query(cnx, "SELECT * FROM exam WHERE GR_number=%s", (g,), fetch="one")
    if row is None:
        print("Exam record not found.")
        return

    # Get columns
    rows, cols = exec_query(cnx, "SELECT * FROM exam WHERE GR_number=%s", (g,), fetch="all")
    row = rows[0]
    col_map = dict(zip(cols, row))

    updated = False
    for col in cols:
        if col == "GR_number":
            continue
        if col_map[col] is None:
            print(f"Pending: {col}")
            inp = input("Enter marks (0 to keep pending): ")
            val = _marks(inp)
            if val is not None:
                exec_query(cnx, f"UPDATE exam SET {col}=%s WHERE GR_number=%s", (val, g))
                updated = True

    if updated:
        print("✅ Pending marks updated.")
    else:
        print("All records are already filled (no NULLs).")

def student_marks_plot(cnx):
    g = prompt_int("GR number: ")
    rows, cols = exec_query(cnx, "SELECT * FROM exam WHERE GR_number=%s", (g,), fetch="all")
    if not rows:
        print("No exam record found.")
        return
    row = rows[0]
    data = dict(zip(cols, row))

    # Print table first
    print_table([row], cols)

    # Optional plot
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib not installed; skipping plot.")
        return

    labels = []
    percents = []
    for col in cols:
        if col == "GR_number":
            continue
        score = data[col]
        if score is None:
            continue
        out_of = 25 if "UT" in col else 70
        labels.append(col)
        percents.append((score / out_of) * 100)

    if not labels:
        print("No filled marks to plot.")
        return

    plt.plot(labels, percents, marker="o")
    plt.xlabel("Exams")
    plt.ylabel("Percent")
    plt.title("Student Marks (%)")
    plt.ylim(0)
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()

def _validate_exam_column(col: str) -> str | None:
    allowed = {"First_UT","Second_UT","Third_UT","Fourth_UT","PRE_MID_TERM","MID_TERM","POST_MID_TERM","ANNUAL"}
    if col in allowed:
        return col
    return None

def section_toppers(cnx):
    e = prompt_str("Exam column (e.g., First_UT, MID_TERM, ANNUAL): ")
    e = _validate_exam_column(e)
    if e is None:
        print("Invalid exam column.")
        return
    ca = prompt_int("Class: ")
    s = prompt_str("Section: ")

    sql = f"""SELECT st.Name, ex.{e} AS score
    FROM exam ex
    JOIN student st ON ex.GR_number = st.GR_number
    WHERE st.Class=%s AND st.Section=%s AND ex.{e} IS NOT NULL
    ORDER BY ex.{e} DESC
    LIMIT 3"""
    rows, cols = exec_query(cnx, sql, (ca, s), fetch="all")
    print_table(rows, cols)

def class_toppers(cnx):
    e = prompt_str("Exam column (e.g., First_UT, MID_TERM, ANNUAL): ")
    e = _validate_exam_column(e)
    if e is None:
        print("Invalid exam column.")
        return
    ca = prompt_int("Class: ")

    sql = f"""SELECT st.Name, st.Section, ex.{e} AS score
    FROM exam ex
    JOIN student st ON ex.GR_number = st.GR_number
    WHERE st.Class=%s AND ex.{e} IS NOT NULL
    ORDER BY ex.{e} DESC
    LIMIT 3"""
    rows, cols = exec_query(cnx, sql, (ca,), fetch="all")
    print_table(rows, cols)

def overall_toppers(cnx):
    # Overall = average(best UT pair + average terms)/95*100 (similar spirit to original)
    sql = """SELECT Name, Class, Overall
    FROM (
        SELECT st.Name, st.Class,
        (
          ( (GREATEST(COALESCE(ex.First_UT,0), COALESCE(ex.Second_UT,0)) + GREATEST(COALESCE(ex.Third_UT,0), COALESCE(ex.Fourth_UT,0))) / 2 )
          + ( (COALESCE(ex.PRE_MID_TERM,0) + COALESCE(ex.MID_TERM,0) + COALESCE(ex.POST_MID_TERM,0)) / 3 )
        ) / 95 * 100 AS Overall,
        ROW_NUMBER() OVER (PARTITION BY st.Class ORDER BY
        (
          ( (GREATEST(COALESCE(ex.First_UT,0), COALESCE(ex.Second_UT,0)) + GREATEST(COALESCE(ex.Third_UT,0), COALESCE(ex.Fourth_UT,0))) / 2 )
          + ( (COALESCE(ex.PRE_MID_TERM,0) + COALESCE(ex.MID_TERM,0) + COALESCE(ex.POST_MID_TERM,0)) / 3 )
        ) DESC) AS row_num
        FROM exam ex
        JOIN student st ON ex.GR_number = st.GR_number
    ) t
    WHERE row_num <= 3
    ORDER BY Class, Overall DESC"""
    rows, cols = exec_query(cnx, sql, fetch="all")
    print_table(rows, cols)
