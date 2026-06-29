import sqlite3

DB_PATH = "backend/permitiq.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS permits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            location TEXT NOT NULL,
            permit_type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
