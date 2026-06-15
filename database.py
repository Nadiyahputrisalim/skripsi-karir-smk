import sqlite3

def init_db():

    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS hasil_ai (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        jurusan TEXT,
        rekomendasi TEXT,
        persentase REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        rating INTEGER,
        komentar TEXT
    )
    """)

    conn.commit()
    conn.close()
