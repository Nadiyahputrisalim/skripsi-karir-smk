import sqlite3

conn = sqlite3.connect("siswa.db")
c = conn.cursor()

# Tabel users
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    email TEXT,
    password TEXT
)
""")

# Tabel hasil AI
c.execute("""
CREATE TABLE IF NOT EXISTS hasil_ai (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    jurusan TEXT,
    rekomendasi TEXT,
    persentase REAL
)
""")

# Tabel feedback
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