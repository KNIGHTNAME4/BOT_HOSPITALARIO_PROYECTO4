from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__, template_folder="public", static_folder="public")
app.secret_key = "CAMBIAR_POR_CLAVE_SEGURA"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        if not username or not password:
            flash("Usuario y contraseña son obligatorios.", "danger")
            return redirect(url_for("register"))
        hashed = generate_password_hash(password)
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()
            conn.close()
            flash("Usuario creado exitosamente. Inicia sesión.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("El usuario ya existe.", "danger")
            return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
        if row and check_password_hash(row[1], password):
            session["user_id"] = row[0]
            session["username"] = username
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Debes iniciar sesión primero.", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session.get("username"))

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("index"))

@app.route("/aviso")
def aviso():
    return "<h3>Derechos y aviso: © 2025. Proyecto B0REAS (prototipo)</h3>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
