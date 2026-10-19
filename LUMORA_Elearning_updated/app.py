from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "ganti-dengan-secret-key-acak-untuk-penggunaan-nyata"
DB_PATH = Path(__file__).with_name("lumora.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS discussions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            topic TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        if count == 0:
            conn.execute("INSERT INTO questions (user_name,title,body) VALUES (?,?,?)",
                         ("Admin Lumora", "Bagaimana cara memahami pecahan?", "Ada tips sederhana untuk belajar pecahan?"))
            conn.execute("INSERT INTO questions (user_name,title,body) VALUES (?,?,?)",
                         ("Nadia", "Tips belajar sebelum ujian", "Bagaimana cara membuat jadwal belajar yang konsisten?"))
        count = conn.execute("SELECT COUNT(*) FROM discussions").fetchone()[0]
        if count == 0:
            conn.execute("INSERT INTO discussions (user_name,topic,body) VALUES (?,?,?)",
                         ("Raka", "Belajar Matematika Bareng", "Yuk berbagi cara mudah memahami persamaan linear!"))
            conn.execute("INSERT INTO discussions (user_name,topic,body) VALUES (?,?,?)",
                         ("Alya", "Rekomendasi metode belajar", "Kalian lebih suka belajar lewat video atau rangkuman?"))

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Silakan login terlebih dahulu.", "info")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("landing.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 8:
            flash("Isi semua data. Kata sandi minimal 8 karakter.", "error")
            return render_template("register.html")
        try:
            with db() as conn:
                conn.execute("INSERT INTO users (name,email,password_hash) VALUES (?,?,?)",
                             (name, email, generate_password_hash(password)))
            flash("Akun berhasil dibuat. Silakan login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email sudah terdaftar. Gunakan email lain.", "error")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        with db() as conn:
            user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            return redirect(url_for("dashboard"))
        flash("Email atau kata sandi tidak sesuai.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Kamu sudah keluar dari akun.", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", active="dashboard")

@app.route("/profil", methods=["GET", "POST"])
@login_required
def profil():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            with db() as conn:
                conn.execute("UPDATE users SET name=? WHERE id=?", (name, session["user_id"]))
            session["user_name"] = name
            flash("Profil berhasil diperbarui.", "success")
            return redirect(url_for("profil"))
    with db() as conn:
        user = conn.execute("SELECT name,email FROM users WHERE id=?", (session["user_id"],)).fetchone()
    return render_template("profil.html", active="profil", user=user)

@app.route("/materi")
@login_required
def materi():
    level = request.args.get("level", "Semua")
    subjects = [
        {"name":"Bahasa Inggris","level":"Inggris","icon":"EN","desc":"Vocabulary, grammar, speaking, dan listening","color":"blue"},
        {"name":"Bahasa Jepang","level":"Jepang","icon":"あ","desc":"Hiragana, katakana, kanji, dan percakapan","color":"peach"},
        {"name":"Bahasa Korea","level":"Korea","icon":"한","desc":"Hangeul, kosakata, dan percakapan sehari-hari","color":"purple"},
        {"name":"Bahasa Mandarin","level":"Mandarin","icon":"文","desc":"Pinyin, hanzi, nada, dan percakapan","color":"mint"},
        {"name":"Bahasa Indonesia","level":"Indonesia","icon":"Aa","desc":"Tata bahasa, membaca, menulis, dan berbicara","color":"blue"},
        {"name":"Bahasa Arab","level":"Arab","icon":"ع","desc":"Kosakata, membaca, menulis, dan percakapan dasar","color":"peach"},
        {"name":"Bahasa Prancis","level":"Prancis","icon":"FR","desc":"Kosakata dasar dan percakapan sehari-hari","color":"purple"},
        {"name":"Bahasa Jerman","level":"Jerman","icon":"DE","desc":"Tata bahasa dan komunikasi dasar","color":"mint"},
    ]
    if level != "Semua":
        subjects = [s for s in subjects if s["level"] == level]
    return render_template("materi.html", active="materi", subjects=subjects, level=level)

@app.route("/privat")
@login_required
def privat():
    tutors = [
        {"name":"Kak Dinda","subject":"Matematika","detail":"SD – SMP · 3 tahun pengalaman","initial":"D","color":"peach"},
        {"name":"Kak Arif","subject":"Python & Informatika","detail":"SMA – Kuliah · Mentor coding","initial":"A","color":"blue"},
        {"name":"Kak Salsya","subject":"Bahasa Inggris","detail":"SD – SMA · Belajar interaktif","initial":"S","color":"mint"},
    ]
    return render_template("privat.html", active="privat", tutors=tutors)

@app.route("/tanya-jawab", methods=["GET", "POST"])
@login_required
def tanya_jawab():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        if title and body:
            with db() as conn:
                conn.execute("INSERT INTO questions (user_name,title,body) VALUES (?,?,?)",
                             (session["user_name"], title, body))
            flash("Pertanyaan berhasil dipublikasikan.", "success")
            return redirect(url_for("tanya_jawab"))
        flash("Judul dan isi pertanyaan wajib diisi.", "error")
    with db() as conn:
        questions = conn.execute("SELECT * FROM questions ORDER BY created_at DESC, id DESC").fetchall()
    return render_template("tanya_jawab.html", active="tanya", questions=questions)

@app.route("/diskusi", methods=["GET", "POST"])
@login_required
def diskusi():
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        body = request.form.get("body", "").strip()
        if topic and body:
            with db() as conn:
                conn.execute("INSERT INTO discussions (user_name,topic,body) VALUES (?,?,?)",
                             (session["user_name"], topic, body))
            flash("Topik diskusi berhasil dibuat.", "success")
            return redirect(url_for("diskusi"))
        flash("Topik dan pesan wajib diisi.", "error")
    with db() as conn:
        discussions = conn.execute("SELECT * FROM discussions ORDER BY created_at DESC, id DESC").fetchall()
    return render_template("diskusi.html", active="diskusi", discussions=discussions)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
