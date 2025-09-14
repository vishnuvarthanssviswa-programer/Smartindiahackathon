from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect("portal.db")
    c = conn.cursor()
    # Student table
    c.execute("""CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE,
                password TEXT)""")
    # Faculty table
    c.execute("""CREATE TABLE IF NOT EXISTS faculty (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                faculty_id TEXT UNIQUE,
                password TEXT)""")
    # Feedback table
    c.execute("""CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                message TEXT)""")
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------
@app.route("/")
def home():
    return "Backend is running! Go to frontend index.html."

# Student Register
@app.route("/register/student", methods=["POST"])
def register_student():
    data = request.form
    student_id = data.get("student_id")
    password = data.get("password")
    try:
        conn = sqlite3.connect("portal.db")
        c = conn.cursor()
        c.execute("INSERT INTO students (student_id, password) VALUES (?, ?)", (student_id, password))
        conn.commit()
        conn.close()
        return "Student registered successfully!"
    except:
        return "Student ID already exists!"

# Faculty Register
@app.route("/register/faculty", methods=["POST"])
def register_faculty():
    data = request.form
    faculty_id = data.get("faculty_id")
    password = data.get("password")
    try:
        conn = sqlite3.connect("portal.db")
        c = conn.cursor()
        c.execute("INSERT INTO faculty (faculty_id, password) VALUES (?, ?)", (faculty_id, password))
        conn.commit()
        conn.close()
        return "Faculty registered successfully!"
    except:
        return "Faculty ID already exists!"

# Student Login
@app.route("/login/student", methods=["POST"])
def login_student():
    student_id = request.form.get("student_id")
    password = request.form.get("password")
    conn = sqlite3.connect("portal.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id=? AND password=?", (student_id, password))
    user = c.fetchone()
    conn.close()
    if user:
        session["student"] = student_id
        return "Student login successful!"
    return "Invalid credentials!"

# Faculty Login
@app.route("/login/faculty", methods=["POST"])
def login_faculty():
    faculty_id = request.form.get("faculty_id")
    password = request.form.get("password")
    conn = sqlite3.connect("portal.db")
    c = conn.cursor()
    c.execute("SELECT * FROM faculty WHERE faculty_id=? AND password=?", (faculty_id, password))
    user = c.fetchone()
    conn.close()
    if user:
        session["faculty"] = faculty_id
        return "Faculty login successful!"
    return "Invalid credentials!"

# Feedback
@app.route("/feedback", methods=["POST"])
def feedback():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    conn = sqlite3.connect("portal.db")
    c = conn.cursor()
    c.execute("INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()
    return "Feedback submitted successfully!"

# Reports (Dummy API for charts)
@app.route("/api/reports")
def reports():
    data = {
        "participation": [120, 150, 180, 100, 200],
        "outcomes": {"completed": 60, "pending": 25, "progress": 15},
        "engagement": [30, 50, 70, 90]
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
