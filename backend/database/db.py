import sqlite3

DB_NAME = "securedesk.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    domain TEXT,
    classification TEXT,
    uploaded_by TEXT
)
""")

    # DEFAULT USERS
    default_users = [
        ("hr_user", "1234", "HR"),
        ("dev_user", "1234", "DEV"),
        ("it_user", "1234", "IT"),
        ("admin", "admin", "SuperAdmin"),
    ]

    for user in default_users:
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                user
            )
        except:
            pass  # ignore if already exists

    conn.commit()
    conn.close()