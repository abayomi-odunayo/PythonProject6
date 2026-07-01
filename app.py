from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
app = Flask(__name__)

app.secret_key = "abc_telecom_secure_2026_secret_key_12345"


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

    conn = get_db_connection()

    wallet = conn.execute(
        "SELECT balance FROM wallets WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    balance = wallet["balance"] if wallet else 0

    return render_template(
        "dashboard.html",
        fullname=session["fullname"],
        balance=balance
    )
# ==========================
# AIRTIME PURCHASE
# ==========================

@app.route("/airtime", methods=["GET", "POST"])
def airtime():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        network = request.form["network"]
        phone = request.form["phone"]
        amount = float(request.form["amount"])

        conn = get_db_connection()

        wallet = conn.execute(
            "SELECT balance FROM wallets WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        if not wallet or wallet["balance"] < amount:
            conn.close()
            flash("Insufficient wallet balance!")
            return redirect(url_for("wallet"))

        conn.execute("""
            INSERT INTO airtime_transactions
            (user_id, network, phone, amount)
            VALUES (?, ?, ?, ?)
        """, (
            session["user_id"],
            network,
            phone,
            amount
        ))

        conn.execute(
            "UPDATE wallets SET balance = balance - ? WHERE user_id = ?",
            (amount, session["user_id"])
        )

        conn.commit()
        conn.close()

        flash("Airtime purchased successfully!")

        return redirect(url_for("airtime"))

    return render_template("airtime.html")

# ==========================
# BUY DATA
# ==========================

@app.route("/data", methods=["GET", "POST"])
def data():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        network = request.form["network"]
        data_plan = request.form["data_plan"]
        amount = float(request.form["amount"])

        conn = get_db_connection()

        wallet = conn.execute(
            "SELECT balance FROM wallets WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        if not wallet or wallet["balance"] < amount:
            conn.close()
            flash("Insufficient wallet balance!")
            return redirect(url_for("wallet"))

        conn.execute("""
            INSERT INTO data_transactions
            (user_id, network, data_plan, amount)
            VALUES (?, ?, ?, ?)
        """, (
            session["user_id"],
            network,
            data_plan,
            amount
        ))

        conn.execute(
            "UPDATE wallets SET balance = balance - ? WHERE user_id = ?",
            (amount, session["user_id"])
        )

        conn.commit()
        conn.close()

        flash("Data purchased successfully!")

        return redirect(url_for("data"))

    return render_template("data.html")
# ==========================
# BILL PAYMENT
# ==========================

@app.route("/bills", methods=["GET", "POST"])
def bills():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        bill_type = request.form["bill_type"]
        provider = request.form["provider"]
        customer_number = request.form["customer_number"]
        amount = float(request.form["amount"])

        conn = get_db_connection()

        wallet = conn.execute(
            "SELECT balance FROM wallets WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        if not wallet or wallet["balance"] < amount:
            conn.close()
            flash("Insufficient wallet balance!")
            return redirect(url_for("wallet"))

        conn.execute("""
            INSERT INTO bill_transactions
            (user_id, bill_type, provider, customer_number, amount)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            bill_type,
            provider,
            customer_number,
            amount
        ))

        conn.execute(
            "UPDATE wallets SET balance = balance - ? WHERE user_id = ?",
            (amount, session["user_id"])
        )

        conn.commit()
        conn.close()

        flash("Bill paid successfully!")

        return redirect(url_for("bills"))

    return render_template("bills.html")
# ==========================
# TRANSACTION HISTORY
# ==========================

@app.route("/transactions")
def transactions():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    transactions = conn.execute("""
    SELECT
        transaction_date,
        'Airtime' AS service,
        network,
        phone AS details,
        amount,
        status
    FROM airtime_transactions
    WHERE user_id = ?

    UNION ALL

    SELECT
        transaction_date,
        'Data' AS service,
        network,
        data_plan AS details,
        amount,
        status
    FROM data_transactions
    WHERE user_id = ?

    UNION ALL

    SELECT
        transaction_date,
        'Bill Payment' AS service,
        provider AS network,
        customer_number AS details,
        amount,
        status
    FROM bill_transactions
    WHERE user_id = ?

    ORDER BY transaction_date DESC
    """, (
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )).fetchall()
    conn.close()

    return render_template(
        "transactions.html",
        transactions=transactions
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
# WALLET
# ==========================

@app.route("/wallet", methods=["GET", "POST"])
def wallet():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":

        amount = float(request.form["amount"])

        wallet = conn.execute(
            "SELECT * FROM wallets WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        if wallet:

            conn.execute(
                "UPDATE wallets SET balance = balance + ? WHERE user_id = ?",
                (amount, session["user_id"])
            )

        else:

            conn.execute(
                "INSERT INTO wallets (user_id, balance) VALUES (?, ?)",
                (session["user_id"], amount)
            )

        conn.commit()

        flash("Wallet funded successfully!")

    wallet = conn.execute(
        "SELECT * FROM wallets WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    balance = wallet["balance"] if wallet else 0

    return render_template(
        "wallet.html",
        balance=balance
    )

# ==========================
# PROFILE
# ==========================

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]

        conn.execute("""
            UPDATE users
            SET fullname = ?, email = ?, phone = ?
            WHERE id = ?
        """, (
            fullname,
            email,
            phone,
            session["user_id"]
        ))

        conn.commit()

        session["fullname"] = fullname

        flash("Profile updated successfully!")

    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template("profile.html", user=user)

# ==========================
# NIN REGISTRATION
# ==========================

@app.route("/nin", methods=["GET", "POST"])
def nin():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":

        nin = request.form["nin"]

        existing = conn.execute(
            "SELECT * FROM nin_registration WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        if existing:
            flash("You have already registered your NIN.")

        else:
            conn.execute("""
                INSERT INTO nin_registration
                (user_id, nin)
                VALUES (?, ?)
            """, (
                session["user_id"],
                nin
            ))

            conn.commit()

            flash("NIN registered successfully!")

    nin = conn.execute(
        "SELECT * FROM nin_registration WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template("nin.html", nin=nin)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()

        admin = conn.execute(
            "SELECT * FROM admins WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if admin and check_password_hash(admin["password_hash"], password):

            session["admin"] = username

            flash("Admin login successful!")

            return redirect(url_for("admin_dashboard"))

        flash("Invalid admin username or password!")

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db_connection()

    total_users = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    airtime_count = conn.execute(
        "SELECT COUNT(*) FROM airtime_transactions"
    ).fetchone()[0]

    data_count = conn.execute(
        "SELECT COUNT(*) FROM data_transactions"
    ).fetchone()[0]

    bill_count = conn.execute(
        "SELECT COUNT(*) FROM bill_transactions"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        airtime_count=airtime_count,
        data_count=data_count,
        bill_count=bill_count
    )

@app.route("/admin/users")
def admin_users():

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "")

    conn = get_db_connection()

    if search:
        users = conn.execute("""
            SELECT * FROM users
            WHERE fullname LIKE ? OR email LIKE ? OR phone LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )).fetchall()
    else:
        users = conn.execute(
            "SELECT * FROM users ORDER BY id DESC"
        ).fetchall()

    conn.close()

    return render_template(
        "admin_users.html",
        users=users,
        search=search
    )

@app.route("/admin/customer/<int:user_id>")
def admin_customer(user_id):

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    ).fetchone()

    wallet = conn.execute(
        "SELECT * FROM wallets WHERE user_id=?",
        (user_id,)
    ).fetchone()

    nin = conn.execute(
        "SELECT * FROM nin_registration WHERE user_id=?",
        (user_id,)
    ).fetchone()

    airtime = conn.execute(
        "SELECT * FROM airtime_transactions WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()

    data = conn.execute(
        "SELECT * FROM data_transactions WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()

    bills = conn.execute(
        "SELECT * FROM bill_transactions WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()
    conn.close()

    return render_template(
        "admin_customer.html",
        user=user,
        wallet=wallet,
        nin=nin,
        airtime=airtime,
        data=data,
        bills=bills
    )
# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)