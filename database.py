import sqlite3


def create_leave_table():

    conn = sqlite3.connect("leave.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        leave_date TEXT,
        leave_type TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_employee_table():

    conn = sqlite3.connect("leave.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id TEXT PRIMARY KEY,
        leave_balance INTEGER
    )
    """)

    conn.commit()
    conn.close()


def add_employee(employee_id, leave_balance):

    conn = sqlite3.connect("leave.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO employees
    VALUES (?, ?)
    """, (employee_id, leave_balance))

    conn.commit()
    conn.close()


def get_leave_balance(employee_id):

    conn = sqlite3.connect("leave.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT leave_balance
    FROM employees
    WHERE employee_id = ?
    """, (employee_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return 0


def deduct_leave_balance(employee_id):

    conn = sqlite3.connect("leave.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE employees
    SET leave_balance = leave_balance - 1
    WHERE employee_id = ?
    AND leave_balance > 0
    """, (employee_id,))

    conn.commit()
    conn.close()


def get_all_employees():

    conn = sqlite3.connect("leave.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM employees
    ORDER BY employee_id
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def save_request(
    employee_id,
    leave_date,
    leave_type,
    status
):

    conn = sqlite3.connect("leave.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO leave_requests
    (
        employee_id,
        leave_date,
        leave_type,
        status
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        employee_id,
        leave_date,
        leave_type,
        status
    ))

    conn.commit()
    conn.close()


def get_requests():

    conn = sqlite3.connect("leave.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM leave_requests
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def count_approved_leaves(leave_date):

    conn = sqlite3.connect("leave.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM leave_requests
    WHERE leave_date = ?
    AND status = 'Approved'
    """, (leave_date,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


create_leave_table()
create_employee_table()