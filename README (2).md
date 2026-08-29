# 🎓 Student Management System (Python + SQL)

A simple, complete Student Management System built with **Python** and **SQL**, offering both a **command-line interface (CLI)** and a **Tkinter GUI**. It manages student records, attendance, marks/results, and fee payments — backed by a relational database.

## ✨ Features

- Add, view, search, update, and delete student records
- Mark and view attendance
- Record and view marks, with automatic percentage calculation
- Track fee payments and status
- Two interfaces: CLI (`app_cli.py`) and GUI (`app_gui.py`)
- Runs out-of-the-box with **SQLite** — no external database server required
- Includes a **MySQL schema** (`schema.sql`) for production deployment

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **Database:** SQLite (default) / MySQL (optional, via `schema.sql`)
- **GUI:** Tkinter (built into Python)

## 📂 Project Structure

```
student-management-system/
├── app_cli.py        # Command-line interface
├── app_gui.py         # Tkinter GUI application
├── database.py         # Database connection & CRUD functions
├── schema.sql          # MySQL schema (optional, for production)
├── requirements.txt     # Project dependencies
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/student-management-system.git
cd student-management-system
```

### 2. (Optional) Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Run the application

**CLI version:**
```bash
python app_cli.py
```

**GUI version:**
```bash
python app_gui.py
```

No extra installation is needed — the project uses Python's built-in `sqlite3` and `tkinter` modules. A `student_db.sqlite3` file will be created automatically on first run.

## 🗄️ Using MySQL Instead of SQLite

1. Run `schema.sql` on your MySQL server to create the database and tables.
2. In `database.py`, replace the `sqlite3` connection logic in `get_connection()` with `mysql.connector.connect(host=..., user=..., password=..., database="student_db")`.
3. Install the connector:
   ```bash
   pip install mysql-connector-python
   ```

## 🖥️ CLI Menu Preview

```
=============================================
           STUDENT MANAGEMENT SYSTEM
=============================================
 1. Add Student
 2. View All Students
 3. Search Student
 4. Update Student
 5. Delete Student
 6. Mark Attendance
 7. View Attendance
 8. Add Marks
 9. View Result / Marksheet
 10. Add Fee Record
 11. View Fee Records
 0. Exit
```

## 📸 Database Schema

| Table | Description |
|---|---|
| `students` | Core student profile data |
| `attendance` | Daily attendance records per student |
| `marks` | Subject-wise marks per student |
| `fees` | Fee payment history per student |

## 🔮 Future Enhancements

- Web version using Flask/Django
- Role-based login (Admin, Teacher, Student)
- Online fee payment integration
- Email/SMS notifications to parents
- Exportable PDF report cards

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open a pull request.
