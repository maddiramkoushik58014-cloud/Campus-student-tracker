"""
app_gui.py
----------
Tkinter GUI for the Student Management System.
Run with: python app_gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database as db


class StudentManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("850x520")
        self.resizable(False, False)

        db.init_db()

        self._build_form()
        self._build_table()
        self._build_buttons()
        self.refresh_table()

    # ------------------------------------------------------------------
    # UI BUILDERS
    # ------------------------------------------------------------------

    def _build_form(self):
        form = ttk.LabelFrame(self, text="Student Details")
        form.place(x=10, y=10, width=420, height=330)

        labels = ["Name", "Roll No", "Class", "DOB (YYYY-MM-DD)",
                  "Gender", "Contact No", "Address", "Email"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(form, text=label + ":").grid(row=i, column=0, padx=8, pady=10, sticky="w")
            entry = ttk.Entry(form, width=30)
            entry.grid(row=i, column=1, padx=8, pady=10)
            self.entries[label] = entry

        self.selected_id = None  # Tracks currently selected student for update/delete

    def _build_table(self):
        columns = ("id", "name", "roll_no", "class", "contact")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=18)
        headings = {"id": "ID", "name": "Name", "roll_no": "Roll No",
                    "class": "Class", "contact": "Contact"}
        widths = {"id": 40, "name": 150, "roll_no": 90, "class": 70, "contact": 100}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col])

        self.tree.place(x=440, y=10, width=400, height=400)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def _build_buttons(self):
        btn_frame = ttk.Frame(self)
        btn_frame.place(x=10, y=350, width=420, height=160)

        ttk.Button(btn_frame, text="Add Student", command=self.add_student).grid(
            row=0, column=0, padx=5, pady=8, sticky="ew")
        ttk.Button(btn_frame, text="Update Selected", command=self.update_student).grid(
            row=0, column=1, padx=5, pady=8, sticky="ew")
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_student).grid(
            row=1, column=0, padx=5, pady=8, sticky="ew")
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).grid(
            row=1, column=1, padx=5, pady=8, sticky="ew")

        search_frame = ttk.LabelFrame(self, text="Search")
        search_frame.place(x=440, y=420, width=400, height=80)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=0, padx=8, pady=15)
        ttk.Button(search_frame, text="Search", command=self.search_student).grid(
            row=0, column=1, padx=5)
        ttk.Button(search_frame, text="Reset", command=self.refresh_table).grid(
            row=0, column=2, padx=5)

    # ------------------------------------------------------------------
    # DATA HANDLERS
    # ------------------------------------------------------------------

    def get_form_values(self):
        return {
            "name": self.entries["Name"].get().strip(),
            "roll_no": self.entries["Roll No"].get().strip(),
            "class": self.entries["Class"].get().strip(),
            "dob": self.entries["DOB (YYYY-MM-DD)"].get().strip(),
            "gender": self.entries["Gender"].get().strip(),
            "contact_no": self.entries["Contact No"].get().strip(),
            "address": self.entries["Address"].get().strip(),
            "email": self.entries["Email"].get().strip(),
        }

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_id = None

    def add_student(self):
        values = self.get_form_values()
        if not values["name"] or not values["roll_no"]:
            messagebox.showwarning("Missing Data", "Name and Roll No are required.")
            return
        try:
            db.add_student(**values)
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_form()
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select a student from the table first.")
            return
        values = self.get_form_values()
        db.update_student(self.selected_id, **values)
        messagebox.showinfo("Success", "Student updated successfully!")
        self.clear_form()
        self.refresh_table()

    def delete_student(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select a student from the table first.")
            return
        if messagebox.askyesno("Confirm", "Delete this student record?"):
            db.delete_student(self.selected_id)
            self.clear_form()
            self.refresh_table()

    def search_student(self):
        keyword = self.search_entry.get().strip()
        rows = db.search_students(keyword) if keyword else db.get_all_students()
        self._populate_tree(rows)

    def refresh_table(self):
        rows = db.get_all_students()
        self._populate_tree(rows)

    def _populate_tree(self, rows):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in rows:
            # r = (student_id, name, roll_no, class, dob, gender, contact_no, address, email)
            self.tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3], r[6]))

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        student_id = item["values"][0]
        student = db.get_student_by_id(student_id)
        if not student:
            return
        self.selected_id = student_id
        keys = ["Name", "Roll No", "Class", "DOB (YYYY-MM-DD)",
                "Gender", "Contact No", "Address", "Email"]
        for key, value in zip(keys, student[1:]):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value if value else "")


if __name__ == "__main__":
    app = StudentManagementApp()
    app.mainloop()
