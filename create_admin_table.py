import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "abc_telecom.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

admin = cursor.execute(
    "SELECT * FROM admins WHERE username = ?",
    ("admin",)
).fetchone()

if not admin:
    cursor.execute(
        "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
        ("admin", generate_password_hash("admin123"))
    )

conn.commit()
conn.close()

print("Admin table created successfully!")