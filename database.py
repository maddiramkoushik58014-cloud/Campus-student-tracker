"""
database.py
------------
Handles all database connectivity and CRUD operations for the
Student Management System using SQLite (file: student_db.sqlite3).

Switching to MySQL:
    Replace `import sqlite3` with `import mysql.connector` and update
    `get_connection()` to use mysql.connector.connect(...) with your
    host/user/password/database. The rest of the code (queries) is
    written in standard SQL and needs little to no change.
"""

import sqlite3
from contextlib import contextmanager

DB_NAME = "student_db.sqlite3"


@contextmanager
def get_connection():
    """Provide a database connection as a context manager."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Create all required tables if they do not already exist."""
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                roll_no     TEXT UNIQUE NOT NULL,
                class       TEXT,
                dob         TEXT,
                gender      TEXT,
                contact_no  TEXT,
                address     TEXT,
                email       TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id  INTEGER NOT NULL,
                date        TEXT NOT NULL,
                status      TEXT NOT NULL CHECK (status IN ('Present', 'Absent')),
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS marks (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id      INTEGER NOT NULL,
                subject         TEXT NOT NULL,
                marks_obtained  INTEGER NOT NULL,
                total_marks     INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS fees (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id    INTEGER NOT NULL,
                amount_paid   REAL NOT NULL,
                payment_date  TEXT NOT NULL,
                status        TEXT NOT NULL CHECK (status IN ('Paid', 'Pending', 'Partial')),
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)


# ---------------------------------------------------------------------
# STUDENT CRUD
# ---------------------------------------------------------------------

def add_student(name, roll_no, student_class, dob, gender, contact_no, address, email):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO students
               (name, roll_no, class, dob, gender, contact_no, address, email)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, roll_no, student_class, dob, gender, contact_no, address, email),
        )


def get_all_students():
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM students ORDER BY student_id")
        return cur.fetchall()


def get_student_by_id(student_id):
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        return cur.fetchone()


def search_students(keyword):
    """Search by name, roll number, or class (partial match)."""
    like_kw = f"%{keyword}%"
    with get_connection() as conn:
        cur = conn.execute(
            """SELECT * FROM students
               WHERE name LIKE ? OR roll_no LIKE ? OR class LIKE ?""",
            (like_kw, like_kw, like_kw),
        )
        return cur.fetchall()


def update_student(student_id, **fields):
    """Update arbitrary student fields, e.g. update_student(1, name='New Name')."""
    if not fields:
        return
    set_clause = ", ".join(f"{key} = ?" for key in fields)
    values = list(fields.values()) + [student_id]
    with get_connection() as conn:
        conn.execute(f"UPDATE students SET {set_clause} WHERE student_id = ?", values)


def delete_student(student_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))


# ---------------------------------------------------------------------
# ATTENDANCE
# ---------------------------------------------------------------------

def mark_attendance(student_id, date, status):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
            (student_id, date, status),
        )


def get_attendance(student_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT date, status FROM attendance WHERE student_id = ? ORDER BY date",
            (student_id,),
        )
        return cur.fetchall()


# ---------------------------------------------------------------------
# MARKS
# ---------------------------------------------------------------------

def add_marks(student_id, subject, marks_obtained, total_marks):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO marks (student_id, subject, marks_obtained, total_marks)
               VALUES (?, ?, ?, ?)""",
            (student_id, subject, marks_obtained, total_marks),
        )


def get_marks(student_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT subject, marks_obtained, total_marks FROM marks WHERE student_id = ?",
            (student_id,),
        )
        return cur.fetchall()


def get_result_summary(student_id):
    """Return (total_obtained, total_max, percentage) for a student."""
    rows = get_marks(student_id)
    if not rows:
        return 0, 0, 0.0
    total_obtained = sum(r[1] for r in rows)
    total_max = sum(r[2] for r in rows)
    percentage = (total_obtained / total_max * 100) if total_max else 0.0
    return total_obtained, total_max, round(percentage, 2)


# ---------------------------------------------------------------------
# FEES
# ---------------------------------------------------------------------

def add_fee_record(student_id, amount_paid, payment_date, status):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO fees (student_id, amount_paid, payment_date, status)
               VALUES (?, ?, ?, ?)""",
            (student_id, amount_paid, payment_date, status),
        )


def get_fee_records(student_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT amount_paid, payment_date, status FROM fees WHERE student_id = ?",
            (student_id,),
        )
        return cur.fetchall()
