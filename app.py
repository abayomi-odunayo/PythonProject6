from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

app.secret_key = "abc_telecom_secure_2026_secret_key_12345"

DATABASE = "/home/abayomiodunayo6/PythonProject6/abc_telecom.db"

# ==========================
# DATABASE CONNECTION
# ==========================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# ABOUT PAGE
# ==========================

@app.route("/about")
def about():
    return render_template("about.html")


# ==========================
# SERVICES PAGE
# ==========================

@app.route("/services")
def services():
    return render_template("services.html")


# ==========================
# PRICING PAGE
# ==========================

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


# ==========================
# SUPPORT PAGE
# ==========================

@app.route("/support")
def support():
    return render_template("support.html")


# ==========================
# CONTACT PAGE
# ==========================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# ==========================
# REGISTER
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:

            cursor.execute("""
            INSERT INTO users
            (fullname,email,phone,password_hash)
            VALUES (?,?,?,?)
            """,
            (fullname,email,phone,password_hash))

            conn.commit()

            flash("Registration Successful!")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            flash("Email already exists!")

        finally:

            conn.close()

    return render_template("register.html")


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
                user["password_hash"], password):

            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]

            flash("Login Successful!")

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password")

    return render_template("login.html")


# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        fullname=session["fullname"]
    )


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully")

    return redirect(url_for("login"))


# ==========================
# CONTACT FORM SUBMISSION
# ==========================

@app.route("/send-message", methods=["POST"])
def send_message():

    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    print("CONTACT FORM")
    print(name)
    print(email)
    print(message)

    flash("Message Sent Successfully!")

    return redirect(url_for("contact"))


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)