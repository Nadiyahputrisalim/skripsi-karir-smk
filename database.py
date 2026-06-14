import sqlite3

if not st.session_state.hasil_disimpan:

    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO hasil_ai
    (nama,jurusan,rekomendasi,persentase)
    VALUES (?,?,?,?)
    """,
    (
        st.session_state.nama,
        st.session_state.jurusan,
        hasil_ai,
        persen_utama
    ))

    conn.commit()
    conn.close()

    st.session_state.hasil_disimpan = True