from flask import Flask,request,redirect,render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

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

@app.route("/")
def form():
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
