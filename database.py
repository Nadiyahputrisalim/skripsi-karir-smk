import sqlite3

conn = sqlite3.connect("siswa.db")

c = conn.cursor()

# tabel hasil AI
c.execute("""
CREATE TABLE IF NOT EXISTS hasil_ai (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    jurusan TEXT,
    rekomendasi TEXT,
    persentase REAL
)
""")

# tabel feedback
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