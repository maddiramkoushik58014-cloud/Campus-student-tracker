-- ============================================================
-- Student Management System - MySQL Schema
-- ============================================================
-- Note: The Python application (database.py) uses SQLite by
-- default for zero-config local use. Use this schema if you
-- want to deploy the system against a MySQL server instead.
-- ============================================================

CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE IF NOT EXISTS students (
    student_id  INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    roll_no     VARCHAR(20) UNIQUE NOT NULL,
    class       VARCHAR(20),
    dob         DATE,
    gender      VARCHAR(10),
    contact_no  VARCHAR(15),
    address     VARCHAR(255),
    email       VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS attendance (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    student_id  INT NOT NULL,
    date        DATE NOT NULL,
    status      ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marks (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    student_id      INT NOT NULL,
    subject         VARCHAR(50) NOT NULL,
    marks_obtained  INT NOT NULL,
    total_marks     INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fees (
    id            INT PRIMARY KEY AUTO_INCREMENT,
    student_id    INT NOT NULL,
    amount_paid   DECIMAL(10,2) NOT NULL,
    payment_date  DATE NOT NULL,
    status        ENUM('Paid', 'Pending', 'Partial') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Sample data (optional)
INSERT INTO students (name, roll_no, class, dob, gender, contact_no, address, email)
VALUES ('Ravi Kumar', 'R001', '10th', '2009-05-14', 'Male', '9876543210', 'Hyderabad', 'ravi@example.com');
