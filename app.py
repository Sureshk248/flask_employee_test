from flask import Flask,request,redirect,render_template,session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "secret123"

def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
     CREATE TABLE IF NOT EXISTS employees(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT,
     age INTEGER,
     department TEXT
     )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        mobile = request.form["mobile"]
        password = request.form["password"]

        session["temp_mobile"] = mobile
        session["temp_password"] = password

        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (mobile, password) VALUES (?, ?)",
            (mobile, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mobile = request.form["mobile"]
        password = request.form["password"]

        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE mobile=? LIMIT 1",
            (mobile,)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = mobile
            return redirect("/first")
        else:
            return "Invalid credentials"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- HOME ----------------#
@app.route("/")
def home():
    return redirect("/login")

@app.route("/first")
def first():
    return render_template("form.html")

@app.route("/add",methods=["POST"])
def add():
    name = request.form["name"]
    age = request.form["age"]
    department = request.form["department"]

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute(
    "INSERT INTO employees (name,age,department) VALUES(?,?,?)",
    (name,age,department)
    )

    conn.commit()
    conn.close()

    return redirect("/list")

@app.route("/list")
def list():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute( "SELECT * FROM employees" )
    rows = cursor.fetchall()

    conn.close()

    return render_template("list.html",tab1 = rows)

if __name__ == "__main__":
    app.run()
