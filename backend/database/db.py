import sqlite3

DB_NAME = "securedesk.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # ================= USERS TABLE =================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    # ================= DOCUMENTS TABLE =================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            domain TEXT,
            classification TEXT,
            uploaded_by TEXT,

            processed INTEGER DEFAULT 0,
            chunks INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ================= DOCUMENT CHUNKS TABLE =================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            chunk_text TEXT,

            FOREIGN KEY(document_id)
            REFERENCES documents(id)
        )
    """)

    # ================= ACCESS REQUESTS TABLE =================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_role TEXT,
            target_domain TEXT,
            classification TEXT,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        )
    """)

    # ================= DEFAULT USERS =================
    default_users = [
        ("hr", "1234", "HR"),
        ("dev", "1234", "DEV"),
        ("it", "1234", "IT"),
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