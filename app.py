import streamlit as st # type: ignore
import sqlite3
import pandas as pd # type: ignore
import time
from fpdf import FPDF # type: ignore
import matplotlib.pyplot as plt # type: ignore
from io import BytesIO
from karir_info import karir_info
from roadmap_karir import roadmap
from skill_karir import skill_karir
from sertifikasi_karir import sertifikasi_karir
from peluang_kerja import peluang_kerja



from model import prediksi_karir, prediksi_detail

# =====================================
# KONFIGURASI HALAMAN
# =====================================

st.set_page_config(
    page_title="Sistem Rekomendasi Karir Siswa SMK",
    layout="centered"
)

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #f8fbff,
        #e8f1ff,
        #dbeafe
    );
}

</style>
""", unsafe_allow_html=True)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

h1 {
    color: #1f4e79;
    text-align: center;
}

.stButton > button {
    width:100%;
    height:50px;
    border-radius:12px;
    font-weight:bold;
    font-size:16px;
    border:none;
    transition:0.3s;
}

.stButton > button:hover {
    transform:scale(1.02);
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-weight: bold;
    font-size: 16px;
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 10px;
}

div[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)


# =====================================
# HEADER BANNER
# =====================================

st.markdown("""
<div style="
padding:25px;
border-radius:20px;
background:linear-gradient(90deg,#1f4e79,#4a90e2);
color:white;
text-align:center;
margin-bottom:20px;
box-shadow:0 4px 10px rgba(0,0,0,0.2);
">
<h1>🎓 Sistem Rekomendasi Karir Siswa SMK</h1>
<p>Artificial Intelligence Career Recommendation System</p>
</div>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "foto" not in st.session_state:
    st.session_state.foto = None

if "step" not in st.session_state:
    st.session_state.step = 1

if "menu_login" not in st.session_state:
    st.session_state.menu_login = "Login"

if "jawaban_wawancara" not in st.session_state:
    st.session_state.jawaban_wawancara = ""

if "hasil_disimpan" not in st.session_state:
    st.session_state.hasil_disimpan = False

if "nama" not in st.session_state:
    st.session_state.nama = ""

if "jurusan" not in st.session_state:
    st.session_state.jurusan = ""

if "hasil_ai" not in st.session_state:
    st.session_state.hasil_ai = ""

if "skill" not in st.session_state:
    st.session_state.skill = ""

if "persentase_ai" not in st.session_state:
    st.session_state.persentase_ai = 0

if "user_nama" not in st.session_state:
    st.session_state.user_nama = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "step" not in st.session_state:
    st.session_state.step = 1

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("Career AI")

    st.caption(
        "Sistem Rekomendasi Karir Siswa SMK Berbasis Artificial Intelligence"
    )

    st.divider()

    st.success(
        f"Step {st.session_state.step} dari 12"
    )
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135755.png",
    width=120
)

st.sidebar.markdown("""
<div style='text-align:center;'>

<h1 style='color:#1f4e79;'>
🎓 Career AI
</h1>

<p>
Sistem Rekomendasi Karir
Siswa SMK
</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.subheader("📍 Posisi Saat Ini")

step_nama = {
    1:"Login",
    2:"Biodata",
    3:"Wawancara",
    4:"Analisis AI",
    5:"CV",
    6:"Dashboard",
    7:"Riwayat",
    8:"Feedback",
    9:"Analisis Feedback",
    10:"Magang",
    11:"Laporan",
    12:"Selesai"
}

st.sidebar.info(
    step_nama.get(
        st.session_state.step,
        "-"
    )
)

# ==========================
# INFO USER
# ==========================

if st.session_state.user_nama != "":

    st.sidebar.markdown(f"""
    <div style="
    background:white;
    padding:15px;
    border-radius:15px;
    text-align:center;
    margin-bottom:15px;
    border:1px solid #ddd;
    ">
    <h3>👤 User</h3>
    <p>{st.session_state.user_nama}</p>
    <small>{st.session_state.user_email}</small>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# PROGRESS
# ==========================

progress = min(
    st.session_state.step / 12,
    1.0
)

st.sidebar.progress(progress)

st.sidebar.success(
    f"📊 Progress {int(progress * 100)}%"
)

st.sidebar.write(
    f"Step : {st.session_state.step}/12"
)

st.sidebar.markdown("---")

# ==========================
# STATUS SISTEM
# ==========================

st.sidebar.subheader(
    "📌 Status Sistem"
)

st.sidebar.success(
    "AI Aktif"
)

st.sidebar.success(
    "Database Aktif"
)

st.sidebar.success(
    "Laporan PDF Aktif"
)

st.sidebar.markdown("---")

# ==========================
# DASHBOARD INFO
# ==========================

st.sidebar.markdown(
    "## Dashboard Karir SMK"
)

st.sidebar.caption(
    "Version 1.0"
)

st.sidebar.caption(
    "Developed with Streamlit"
)

# =====================================
# STEP 1 - LOGIN & REGISTER
# =====================================

if st.session_state.step == 1:

    st.markdown("""
    <div style="
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.1);
    text-align:center;
    ">
    <h1 style="color:#1f4e79;">
    🎓 Career AI SMK
    </h1>

    <p>
    Sistem Rekomendasi Karir Siswa SMK
    Berbasis Artificial Intelligence
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    menu = st.radio(
        "Menu",
        ["Login", "Daftar"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("""
    <div style="
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
    margin-bottom:20px;
    ">
    <h2 style="text-align:center;color:#1f4e79;">
    🔐 Selamat Datang
    </h2>
    <p style="text-align:center;">
    Silakan login atau daftar untuk menggunakan Sistem Rekomendasi Karir SMK
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👨‍🎓 Siswa",
            "100+"
        )

    with col2:
        st.metric(
            "🤖 AI Karir",
            "Aktif"
        )

    with col3:
        st.metric(
            "📄 Laporan",
            "PDF"
        )

    # =====================
    # LOGIN
    # =====================

    if menu == "Login":

        st.subheader("🔐 Login Akun")

        email = st.text_input(
            "📧 Email"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )
        if st.button(
            "🚀 Masuk ke Dashboard",
            use_container_width=True
        ):
            conn = sqlite3.connect(
                "siswa.db"
            )

            c = conn.cursor()

            c.execute(
                """
                SELECT *
                FROM users
                WHERE email=?
                AND password=?
                """,
                (
                    email,
                    password
                )
            )

            user = c.fetchone()

            conn.close()

            if user:

                st.session_state.user_nama = user[1]
                st.session_state.user_email = user[2]

                st.success(
                    "Login berhasil"
    )

                st.session_state.step = 2

                st.rerun()

            else:

                st.error(
                    "Email atau Password salah"
                )

    # =====================
    # DAFTAR
    # =====================

    else:

        st.subheader("📝 Daftar Akun Baru")

        nama = st.text_input(
            "👤 Nama Lengkap"
        )

        email = st.text_input(
            "📧 Email"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        if st.button(
            "📝 Buat Akun Baru",
            use_container_width=True
        ):

            conn = sqlite3.connect(
                "siswa.db"
            )

            c = conn.cursor()

            try:

                c.execute(
                    """
                    INSERT INTO users
                    (nama,email,password)
                    VALUES (?,?,?)
                    """,
                    (
                        nama,
                        email,
                        password
                    )
                )

                conn.commit()

                st.success(
                    "Akun berhasil dibuat"
                )

            except:

                st.error(
                    "Email sudah digunakan"
                )

            conn.close()

# =====================================
# STEP 2 - BIODATA SISWA
# =====================================

elif st.session_state.step == 2:

    st.title("👤 Biodata Siswa")

    st.progress(2/11)

    st.info(
        "Lengkapi biodata terlebih dahulu sebelum melakukan wawancara dan analisis karir AI."
    )

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:

        nama = st.text_input(
            "👤 Nama Lengkap"
        )

        jurusan = st.selectbox(
            "🏫 Jurusan",
            [
                "TKJ",
                "RPL",
                "Multimedia",
                "Akuntansi",
                "Perkantoran"
            ]
        )

        umur = st.number_input(
            "🎂 Umur",
            min_value=15,
            max_value=30,
            value=17
        )

        skill = st.text_area(
            "🛠 Skill yang Dimiliki",
            placeholder="Contoh: Microsoft Office, Python, Desain Grafis"
        )

    with col2:

        st.subheader("📸 Foto Profil")

        foto = st.file_uploader(
            "Upload Foto",
            type=["jpg", "jpeg", "png"]
        )

        if foto is not None:

            st.session_state.foto = foto

            st.image(
                foto,
                width=200
            )

    st.markdown("---")

    st.subheader("📋 Ringkasan Biodata")

    col_a, col_b, col_c = st.columns(3)

    with col_a:

        st.metric(
            "Nama",
            nama if nama else "-"
        )

    with col_b:

        st.metric(
            "Jurusan",
            jurusan
        )

    with col_c:

        st.metric(
            "Umur",
            umur
        )

    st.markdown("---")

    if st.button(
        "💾 Simpan Biodata & Lanjut Wawancara",
        use_container_width=True
    ):

        if nama.strip() == "":

            st.error(
                "Nama wajib diisi!"
            )

        elif skill.strip() == "":

            st.warning(
                "Skill wajib diisi!"
            )

        else:

            conn = sqlite3.connect(
                "siswa.db"
            )

            c = conn.cursor()

            c.execute(
                """
                INSERT INTO siswa
                (nama,jurusan,umur,skill)
                VALUES (?,?,?,?)
                """,
                (
                    nama,
                    jurusan,
                    umur,
                    skill
                )
            )

            conn.commit()
            conn.close()

            st.session_state.nama = nama
            st.session_state.jurusan = jurusan
            st.session_state.skill = skill

            st.success(
                "✅ Biodata berhasil disimpan!"
            )

            time.sleep(1)

            st.session_state.step = 3

            st.rerun()

# =====================================
# STEP 3 - WAWANCARA
# =====================================

elif st.session_state.step == 3:

    st.title("💬 Simulasi Wawancara Karir")
    st.progress(3/11)

    st.markdown("""
    ### 🤖 AI Career Interview

    Jawab seluruh pertanyaan dengan jujur agar sistem AI
    dapat memberikan rekomendasi karir yang lebih akurat.

    💡 Semakin lengkap jawaban Anda, semakin baik hasil analisis karir.
    """)

    st.markdown("---")

    q1 = st.text_area(
    "💪 1. Ceritakan kelebihan utama yang Anda miliki"
    )
    q2 = st.text_area(
    "💼 2. Bidang pekerjaan apa yang paling Anda minati"
    )
    q3 = st.text_area(
    "🛠 3. Skill yang paling Anda kuasai"
    )
    q4 = st.text_area(
    "👥 4. Lebih suka bekerja sendiri atau dalam tim"
    )
    q5 = st.text_area(
    "🧠 5. Bagaimana cara Anda menyelesaikan masalah"
    )
    q6 = st.text_area(
    "🚀 6. Apakah Anda tertarik pada teknologi, desain, bisnis atau administrasi"
    )
    q7 = st.text_area(
    "🎯 7. Apa pekerjaan impian Anda"
    )
    q8 = st.text_area(
    "📈 8. Kelemahan apa yang ingin Anda perbaiki"
    )
    q9 = st.text_area(
    "🎤 9. Apakah Anda nyaman berbicara di depan umum"
    )
    q10 = st.text_area(
    "🏆 10. Mengapa perusahaan harus memilih Anda"
    )
    
    st.markdown("---")

    jumlah_jawaban = len(
        q1+q2+q3+q4+q5+q6+q7+q8+q9+q10
    )

    st.caption(
        f"Jumlah karakter jawaban: {jumlah_jawaban}"
    )

    if st.button(
        "🚀 Proses Analisis Karir AI",
        use_container_width=True
    ):

        jawaban = f"""
        {q1}
        {q2}
        {q3}
        {q4}
        {q5}
        {q6}
        {q7}
        {q8}
        {q9}
        {q10}
        """

        if jawaban.strip() == "":
            st.warning("Isi wawancara terlebih dahulu!")
        else:

            st.session_state.jawaban_wawancara = jawaban

            with st.spinner("AI sedang menganalisis..."):
                time.sleep(1)

            st.session_state.step = 4
            st.rerun()



# =====================================
# STEP 4 - HASIL AI
# =====================================

elif st.session_state.step == 4:

    st.title("🤖 Hasil Analisis AI")
    
    st.progress(4/11)

    st.markdown("""
    ### 🎯 Analisis Karir Berbasis Artificial Intelligence
    Sistem AI telah menganalisis jawaban wawancara dan memberikan rekomendasi karir terbaik berdasarkan minat dan kemampuan siswa.
    """)

    jawaban = st.session_state.jawaban_wawancara

    if jawaban == "":
        st.warning(
            "Silakan isi wawancara terlebih dahulu."
        )

    else:

        hasil_ai = prediksi_karir(jawaban)

        detail = prediksi_detail(jawaban)

        persen_utama = round(
            detail[0][1] * 100,
            2
        )

        st.session_state.hasil_ai = hasil_ai
        st.session_state.persentase_ai = persen_utama

        st.success(
            f"🎯 Rekomendasi Utama : {hasil_ai}"
        )

        st.markdown(f"""
        <div style="
        background:linear-gradient(90deg,#1f4e79,#4a90e2);
        padding:30px;
        border-radius:20px;
        text-align:center;
        color:white;
        box-shadow:0px 5px 15px rgba(0,0,0,0.2);
        margin-bottom:20px;
        ">
        <h1>🤖 {hasil_ai}</h1>
        <h2>Tingkat Kecocokan</h2>
        <h1>{persen_utama}%</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # ==========================
        # SIMPAN DATABASE SEKALI
        # ==========================

        if not st.session_state.hasil_disimpan:

            conn = sqlite3.connect(
                "siswa.db"
            )

            c = conn.cursor()

            c.execute(
                """
                INSERT INTO hasil_ai
                (nama,jurusan,rekomendasi,persentase)
                VALUES (?,?,?,?)
                """,
                (
                    st.session_state.nama,
                    st.session_state.jurusan,
                    hasil_ai,
                    persen_utama
                )
            )

            conn.commit()
            conn.close()

            st.session_state.hasil_disimpan = True

        # ==========================
        # TOP 3 KARIR
        # ==========================

        st.subheader(
            "🏆 Top 3 Rekomendasi Karir"
        )

        for pekerjaan, nilai in detail[:3]:

            persen = round(
                nilai * 100,
                2
            )

            st.info(
                f"🏆 {pekerjaan} — {persen}%"
            )

            st.progress(
                min(int(persen),100)
            )

        # ==========================
        # ANALISIS AI
        # ==========================

        st.subheader(
            "🧠 Analisis AI"
        )

        st.info(
            f"Siswa memiliki kecenderungan berkarir sebagai {hasil_ai}"
        )

        # ==========================
        # AI INTERVIEW SCORE
        # ==========================

        st.markdown("---")

        st.subheader("🧠 AI Interview Score")

        import random

        komunikasi = random.randint(70, 95)
        leadership = random.randint(65, 90)
        problem_solving = random.randint(75, 98)
        kerja_tim = random.randint(70, 95)
        teknis = random.randint(75, 100)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🗣 Komunikasi",
                komunikasi
            )

        with col2:
            st.metric(
                "👑 Leadership",
                leadership
            )

        with col3:
            st.metric(
                "🧩 Problem Solving",
                problem_solving
            )

        col4, col5 = st.columns(2)

        with col4:
            st.metric(
                "🤝 Kerja Tim",
                kerja_tim
            )

        with col5:
            st.metric(
                "💻 Skill Teknis",
                teknis
            )
        
        st.subheader("📊 Grafik Kemampuan Siswa")

        df_score = pd.DataFrame(
            {
                "Nilai": [
                    komunikasi,
                    leadership,
                    problem_solving,
                    kerja_tim,
                    teknis
                ]
            },
            index=[
                "Komunikasi",
                "Leadership",
                "Problem Solving",
                "Kerja Tim",
                "Skill Teknis"
            ]
        )

        st.bar_chart(df_score)
        
        # ==========================
        # ROADMAP KARIR
        # ==========================

        if hasil_ai in roadmap:

             st.subheader("🗺 Roadmap Karir")

             langkah = roadmap[hasil_ai]

             for i, item in enumerate(
                langkah,
                start=1
    ):
                st.info(
                    f"{i}. {item}"
                )

        else:

            st.warning(
                f"Roadmap untuk {hasil_ai} belum tersedia."
    )

        # ==========================
        # PROFIL KARIR
        # ==========================

        if hasil_ai in karir_info:

            info = karir_info[hasil_ai]

            st.subheader(
                "📚 Profil Karir"
            )

            st.write(
                info["deskripsi"]
            )

            st.subheader(
                "🛠 Skill yang Dibutuhkan"
            )

            col1, col2 = st.columns(2)

            for i, skill in enumerate(skill_karir[hasil_ai]):

                if i % 2 == 0:
                    col1.success(skill)
                else:
                    col2.success(skill)

            st.subheader(
                "🚀 Prospek Karir"
            )

            for prospek in info["prospek"]:

                st.write(
                    f"➡ {prospek}"
                )

        # ==========================
        # SKILL YANG DIREKOMENDASIKAN
        # ==========================

        if hasil_ai in skill_karir:

            st.subheader(
                "🎓 Skill yang Direkomendasikan"
    )

            for skill in skill_karir[hasil_ai]:

                 st.write(
                    f"✅ {skill}"
        )
                 
        # ==========================
        # SERTIFIKASI
        # ==========================

        if hasil_ai in sertifikasi_karir:

            st.subheader(
                "🏅 Sertifikasi yang Direkomendasikan"
            )

            for sertifikat in sertifikasi_karir[hasil_ai]:

                st.write(
                    f"🎖 {sertifikat}"
                )

        # ==========================
        # PELUANG PEKERJAAN
        # ==========================

        if hasil_ai in peluang_kerja:

            st.subheader(
                "💼 Peluang Pekerjaan"
            )

            for pekerjaan in peluang_kerja[hasil_ai]:

                st.info(f"💼 {pekerjaan}")

        # ==========================
        # GRAFIK
        # ==========================

        st.subheader(
            "📊 Grafik Rekomendasi Karir"
        )

        import matplotlib.pyplot as plt

        karir = []
        persentase = []

        for pekerjaan, nilai in detail[:5]:

            karir.append(
                pekerjaan
            )

            persentase.append(
                round(
                    nilai * 100,
                    2
                )
            )

        fig, ax = plt.subplots()

        ax.bar(
            karir,
            persentase
        )

        ax.set_ylabel(
            "Persentase (%)"
        )

        ax.set_title(
            "Hasil Prediksi Karir AI"
        )

        plt.xticks(
            rotation=20
        )

        st.pyplot(fig)

        # ==========================
        # BUTTON CV
        # ==========================

        if st.button(
            "📄 Buat CV Profesional",
            use_container_width=True
        ):
            st.session_state.step = 5

            st.rerun()

        if st.button(
            "🏢 Lihat Rekomendasi Magang",
            use_container_width=True
        ):

            st.session_state.step = 10
            st.rerun()
            
            st.markdown("---")

            st.subheader("📋 Ringkasan AI")

            st.success(
                f"""
                Berdasarkan analisis AI, siswa memiliki kecocokan tertinggi pada bidang {hasil_ai}
                dengan tingkat kecocokan {persen_utama}%.
                """
            )

# =====================================
# STEP 5 - CV
# =====================================

elif st.session_state.step == 5:

    st.title("📄 Curriculum Vitae Otomatis")
    st.progress(5/11)

    st.markdown("""
    ### 📑 Pembuatan CV Profesional

    Lengkapi data berikut untuk menghasilkan Curriculum Vitae (CV)
    secara otomatis berdasarkan profil siswa dan hasil analisis AI.
    """)

    nama_cv = st.text_input(
        "Nama Lengkap",
        value=st.session_state.nama
    )

    email_cv = st.text_input(
        "Email"
    )

    jurusan_cv = st.text_input(
        "Jurusan",
        value=st.session_state.jurusan
    )

    skill_cv = st.text_area(
    "Skill",
    value=st.session_state.skill
)
    

    pengalaman_cv = st.text_area(
        "Pengalaman / Organisasi"
    )

    tentang_default = f"""
    Saya merupakan siswa jurusan {st.session_state.jurusan}
    yang memiliki minat pada bidang {st.session_state.hasil_ai}.
    Saya memiliki kemampuan {st.session_state.skill}
    dan ingin mengembangkan karir profesional sesuai rekomendasi AI.
    """

    tentang_cv = st.text_area(
        "Tentang Saya",
     value=tentang_default
)
    if st.session_state.foto:

     st.image(
        st.session_state.foto,
        width=180
    )

    if st.button("Generate CV"):

        st.subheader("Preview CV")

        st.markdown(f"""
# {nama_cv}

📧 {email_cv}

🎓 Jurusan : {jurusan_cv}

## Tentang Saya
{tentang_cv}

## Skill
{skill_cv}

## Pengalaman
{pengalaman_cv}

## Rekomendasi Karir AI
{st.session_state.hasil_ai}
        """)

    # ==========================
    # CARD HASIL AI
    # ==========================
        st.markdown(f"""
        <div style="
        background:linear-gradient(90deg,#1f4e79,#4a90e2);
        padding:20px;
        border-radius:15px;
        color:white;
        text-align:center;
        margin-top:15px;
        margin-bottom:15px;
        ">
        <h2>🤖 Rekomendasi AI</h2>
        <h1>{st.session_state.hasil_ai}</h1>
        <h3>{st.session_state.persentase_ai}% Kecocokan</h3>
        </div>
        """, unsafe_allow_html=True)

        st.success("CV berhasil dibuat")
        st.info(
            f"💼 Rekomendasi Karir AI : "
            f"{st.session_state.hasil_ai}"
)

        st.info(
            f"📈 Tingkat Kecocokan : "
            f"{st.session_state.persentase_ai}%"
)

        from fpdf import FPDF

        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, nama_cv, ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"Email : {email_cv}", ln=True)
        pdf.cell(200, 10, f"Jurusan : {jurusan_cv}", ln=True)

        pdf.ln(5)

        pdf.multi_cell(
            0,
            8,
            f"""
Tentang Saya:
{tentang_cv}

Skill:
{skill_cv}

Pengalaman:
{pengalaman_cv}

Rekomendasi Karir:
{st.session_state.hasil_ai}
"""
        )

        pdf.output("cv_siswa.pdf")

        with open(
            "cv_siswa.pdf",
            "rb"
        ) as file:

            st.download_button(
                label="📥 Download CV PDF",
                data=file,
                file_name="CV_Siswa.pdf",
                mime="application/pdf"
            )

    if st.button("Lihat Riwayat"):

        st.session_state.step = 6
        st.rerun()

    
# =====================================
# STEP 6 - RIWAYAT
# =====================================

elif st.session_state.step == 6:

    st.title("📊 Riwayat Analisis")
    st.progress(6/11)

    st.markdown("""
    ### 📚 Riwayat Hasil Analisis Karir

    Halaman ini menampilkan seluruh hasil analisis karir siswa yang tersimpan di database.
    Data dapat dicari, difilter, diunduh, maupun dihapus.
    """)

    conn = sqlite3.connect("siswa.db")

    data = pd.read_sql_query(
        """
        SELECT
        nama,
        jurusan,
        rekomendasi,
        persentase
        FROM hasil_ai
        """,
        conn
    )

    conn.close()

    st.markdown("""
    <div style="
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom:20px;
    ">
    <h3>🔍 Filter Data</h3>
    <p>Cari siswa berdasarkan nama atau jurusan.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        cari_nama = st.text_input(
            "👤 Cari Nama"
        )

    with col2:

        filter_jurusan = st.selectbox(
            "🎓 Filter Jurusan",
            [
                "Semua",
                "TKJ",
                "RPL",
                "Multimedia",
                "Akuntansi",
                "Perkantoran"
            ]
        )

    if cari_nama:

        data = data[
            data["nama"].str.contains(
                cari_nama,
                case=False,
                na=False
            )
        ]

    if filter_jurusan != "Semua":

        data = data[
            data["jurusan"] == filter_jurusan
        ]

    st.metric(
        "📊 Total Data",
        len(data)
    )

    st.subheader("📋 Data Riwayat Analisis")
    st.dataframe(
        data,
        use_container_width=True
    )

    # ==========================
    # DOWNLOAD FILE
    # ==========================

    csv = data.to_csv(index=False)

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        data.to_excel(
            writer,
            index=False,
            sheet_name="Riwayat"
        )

    excel_data = output.getvalue()

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="riwayat_analisis.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:

        st.download_button(
            label="📊 Download Excel",
            data=excel_data,
            file_name="riwayat_analisis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    if st.button(
        "📈 Lihat Dashboard Statistik",
        use_container_width=True
    ):

        st.session_state.step = 7
        st.rerun()

    st.markdown("---")

    if st.checkbox(
        "Saya yakin ingin menghapus semua riwayat"
    ):

        if st.button(
            "🗑️ Hapus Semua Riwayat"
        ):

            conn = sqlite3.connect("siswa.db")

            c = conn.cursor()

            c.execute(
                "DELETE FROM hasil_ai"
            )

            conn.commit()
            conn.close()

            if st.button(
                "🗑️ Hapus Semua Riwayat",
                use_container_width=True
            ):

                st.rerun()
            st.markdown("---")

            st.subheader("⚠️ Manajemen Data")

            if st.button(
                "🔄 Mulai Analisis Baru",
                use_container_width=True
            ):

                st.session_state.hasil_disimpan = False
                st.session_state.jawaban_wawancara = ""
                st.session_state.hasil_ai = ""

                st.session_state.step = 1

                st.rerun()



# =====================================
# STEP 7 - DASHBOARD
# =====================================

elif st.session_state.step == 7:

    st.title("📈 Dashboard Statistik")
    st.progress(7/11)

    st.markdown("""
    ### 📊 Dashboard Statistik Sistem

    Dashboard ini menampilkan ringkasan seluruh hasil analisis karir siswa yang tersimpan dalam database.
    """)
    conn = sqlite3.connect("siswa.db")

    data = pd.read_sql_query(
        """
        SELECT *
        FROM hasil_ai
        """,
        conn
    )

    conn.close()
    st.markdown("""
    <div style="
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom:20px;
    ">
    <h2>📈 Ringkasan Sistem</h2>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📊 Total Analisis",
            len(data)
        )

    with col2:
        try:
            st.metric(
                "👥 Total User",
                len(user_data)
            )
        except:
            st.metric(
                "👥 Total User",
                0
            )

    try:

        conn = sqlite3.connect("siswa.db")

        user_data = pd.read_sql_query(
            """
            SELECT *
            FROM users
            """,
            conn
        )

        conn.close()

        st.metric(
            "Total User",
            len(user_data)
        )

    except:

        st.info(
            "Tabel users belum tersedia."
        )

    if not data.empty:

        st.markdown("""
        <div style="
        background:#e8f5e9;
        padding:15px;
        border-radius:15px;
        margin-top:20px;
        ">
        <h3>🏆 Karir Terpopuler</h3>
        </div>
        """, unsafe_allow_html=True)
        karir_count = (
            data["rekomendasi"]
            .value_counts()
        )

        st.bar_chart(
            karir_count
        )

        st.markdown("""
        <div style="
        background:#e3f2fd;
        padding:15px;
        border-radius:15px;
        margin-top:20px;
        ">
        <h3>🎓 Jurusan Terbanyak</h3>
        </div>
        """, unsafe_allow_html=True)
        jurusan_count = (
            data["jurusan"]
            .value_counts()
        )

        st.bar_chart(
            jurusan_count
        )

        st.markdown("""
        <div style="
        background:#fff3cd;
        padding:15px;
        border-radius:15px;
        margin-top:20px;
        ">
        <h3>📋 Analisis Per Jurusan</h3>
        </div>
        """, unsafe_allow_html=True)

        jurusan_tabel = (
            data.groupby("jurusan")
            .size()
            .reset_index(name="Jumlah")
        )

        st.dataframe(
            jurusan_tabel,
            use_container_width=True
        )

        st.markdown("""
        <div style="
        background:#f3e5f5;
        padding:15px;
        border-radius:15px;
        margin-top:20px;
        ">
        <h3>🥇 Ranking Karir Terpopuler</h3>
        </div>
        """, unsafe_allow_html=True)

        ranking = (
            karir_count
            .reset_index()
        )

        ranking.columns = [
            "Karir",
            "Jumlah"
        ]

        ranking.index = ranking.index + 1

        st.dataframe(
            ranking,
            use_container_width=True
        )

        st.markdown("""
        <div style="
        background:#fce4ec;
        padding:15px;
        border-radius:15px;
        margin-top:20px;
        ">
        <h3>🥧 Distribusi Karir Siswa</h3>
        </div>
        """, unsafe_allow_html=True)

        fig, ax = plt.subplots()

        karir_count.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax
        )

        ax.set_ylabel("")

        st.pyplot(fig)

    else:

        st.warning(
            "Belum ada data untuk ditampilkan."
        )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⭐ Beri Feedback",
            use_container_width=True
        ):

            st.session_state.step = 8
            st.rerun()

    with col2:

        if st.button(
            "⬅ Kembali ke Riwayat",
            use_container_width=True
        ):

            st.session_state.step = 6
            st.rerun()
        
        st.markdown("---")

        st.markdown("""
        <div style="
        text-align:center;
        color:gray;
        padding:10px;
        ">

        📊 Dashboard Career AI <br>
        Visualisasi Data Analisis Karir Siswa SMK

        </div>
        """, unsafe_allow_html=True)


# =====================================
# STEP 8 - FEEDBACK
# =====================================

elif st.session_state.step == 8:

    st.title("⭐ Feedback Pengguna")
    st.progress(8/11)

    st.markdown("""
    ### 💬 Penilaian Pengguna

    Masukan Anda sangat membantu untuk meningkatkan kualitas sistem rekomendasi karir berbasis Artificial Intelligence.
    """)
    nama = st.session_state.nama
    
    st.markdown(f"""
    <div style="
    background:linear-gradient(90deg,#1f4e79,#4a90e2);
    padding:25px;
    border-radius:20px;
    color:white;
    text-align:center;
    margin-bottom:20px;
    ">

    <h2>⭐ Feedback Pengguna</h2>

    <p>
    Terima kasih <b>{nama}</b> telah menggunakan sistem Career AI.
    Silakan berikan penilaian Anda.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("🌟 Berikan Rating")

    rating = st.slider(
        "Pilih Rating",
        1,
        5,
        5
    )

    st.info(f"Rating yang dipilih : ⭐ {rating}/5")

    # ==========================
    # KOMENTAR
    # ==========================

    st.subheader("📝 Komentar")

    komentar = st.text_area(
        "Tuliskan saran atau masukan Anda",
        height=150
    )

    # ==========================
    # RINGKASAN PENILAIAN
    # ==========================

    st.markdown("---")

    st.subheader("📌 Ringkasan Penilaian")

    if rating >= 4:

        st.success(
            "Terima kasih, Anda sangat puas dengan sistem ini 🎉"
        )

    elif rating == 3:

        st.warning(
            "Terima kasih atas masukan Anda 👍"
        )

    else:

        st.error(
            "Kami akan terus meningkatkan kualitas sistem 🙏"
        )

    # ==========================
    # TOMBOL
    # ==========================

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "💾 Simpan Feedback",
            use_container_width=True
        ):

            conn = sqlite3.connect("siswa.db")

            c = conn.cursor()

            c.execute(
                """
                INSERT INTO feedback
                (nama,rating,komentar)
                VALUES (?,?,?)
                """,
                (
                    nama,
                    rating,
                    komentar
                )
            )

            conn.commit()
            conn.close()

            st.success(
                "✅ Feedback berhasil disimpan"
            )

    with col2:

        if st.button(
            "📊 Analisis Feedback",
            use_container_width=True
        ):

            st.session_state.step = 9
            st.rerun()

    with col3:

        if st.button(
            "⬅ Dashboard",
            use_container_width=True
        ):

            st.session_state.step = 7
            st.rerun()
        st.markdown("---")

        st.markdown("""
        <div style="
        text-align:center;
        color:gray;
        padding:10px;
        ">

        ⭐ Feedback Center <br>
        Career AI Recommendation System

        </div>
        """, unsafe_allow_html=True)
# =====================================
# STEP 9 - ANALISIS FEEDBACK
# =====================================

elif st.session_state.step == 9:

    st.title("📊 Analisis Feedback")
    st.progress(9/11)

    st.markdown("""
    ### 💬 Dashboard Analisis Feedback

    Halaman ini menampilkan hasil evaluasi pengguna terhadap sistem Career AI.
    Semua rating dan komentar akan dianalisis secara otomatis.
    """)
    conn = sqlite3.connect("siswa.db")

    feedback_data = pd.read_sql_query(
        """
        SELECT *
        FROM feedback
        """,
        conn
    )

    conn.close()
    st.markdown("""
    <div style="
    background:linear-gradient(90deg,#1f4e79,#4a90e2);
    padding:25px;
    border-radius:20px;
    color:white;
    text-align:center;
    margin-bottom:20px;
    ">

    <h2>⭐ Dashboard Feedback Pengguna</h2>

    <p>
    Analisis kepuasan pengguna terhadap sistem rekomendasi karir.
    </p>

    </div>
    """, unsafe_allow_html=True)

    if not feedback_data.empty:

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📝 Total Feedback",
                len(feedback_data)
            )

        with col2:

            st.metric(
                "⭐ Rata-rata Rating",
                round(
                    feedback_data["rating"].mean(),
                    2
                )
            )

        st.markdown("""
            <div style="
            background:#e8f5e9;
            padding:15px;
            border-radius:15px;
            margin-top:20px;
            ">
            <h3>📈 Distribusi Rating Pengguna</h3>
            </div>
            """, unsafe_allow_html=True)
        rating_count = (
            feedback_data["rating"]
            .value_counts()
            .sort_index()
        )

        st.bar_chart(
            rating_count
        )
        rata_rating = round(
            feedback_data["rating"].mean(),
            2
        )

        if rata_rating >= 4:

            st.success(
                "Mayoritas pengguna merasa sangat puas terhadap sistem 🎉"
            )

        elif rata_rating >= 3:

            st.info(
                "Pengguna cukup puas terhadap sistem 👍"
            )

    else:

        st.warning(
            "Sistem masih membutuhkan peningkatan berdasarkan feedback pengguna."
        )

        st.markdown("""
        <div style="
        background:#fff3cd;
        padding:15px;
        border-radius:15px;
        margin-top:20px;
        ">
        <h3>💬 Komentar Pengguna</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(
            f"Menampilkan {len(feedback_data)} feedback dari pengguna sistem."
        )
        st.dataframe(
            feedback_data[
                [
                    "nama",
                    "rating",
                    "komentar"
                ]
            ],
            use_container_width=True
        )

    st.warning(
            "Belum ada feedback."
        )
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🏢 Lanjut ke Rekomendasi Magang",
            use_container_width=True
        ):

            st.session_state.step = 10
            st.rerun()

    with col2:

        if st.button(
            "⬅ Kembali ke Feedback",
            use_container_width=True
        ):

            st.session_state.step = 8
            st.rerun()
            
        st.markdown("---")

        st.markdown("""
        <div style="
        text-align:center;
        color:gray;
        padding:10px;
        ">

        ⭐ Feedback Analytics Dashboard <br>
        Career AI Recommendation System

        </div>
        """, unsafe_allow_html=True)


# =====================================
# STEP 10 - REKOMENDASI MAGANG
# =====================================

elif st.session_state.step == 10:
    
    hasil_ai = st.session_state.hasil_ai

    st.title("🏢 Rekomendasi Tempat Magang")

    st.markdown(f"""
    <div style="
    background:linear-gradient(90deg,#1f4e79,#4a90e2);
    padding:25px;
    border-radius:20px;
    text-align:center;
    color:white;
    ">
    <h1>🤖 {hasil_ai}</h1>
    <h3>Karir Rekomendasi AI</h3>
    </div>
    """, unsafe_allow_html=True)
    st.title("🏢 Rekomendasi Tempat Magang")
    st.progress(10/11)

    st.markdown("""
    ### 🎯 Rekomendasi Tempat Magang Berdasarkan AI

    Sistem memberikan rekomendasi industri dan posisi magang
    yang sesuai dengan hasil analisis karir siswa.
    """)

    st.markdown("---")

    st.markdown(f"""
    <div style="
    background:linear-gradient(90deg,#1f4e79,#4a90e2);
    padding:25px;
    border-radius:20px;
    text-align:center;
    color:white;
    margin-bottom:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.2);
    ">

    <h1>🤖 {hasil_ai}</h1>

    <h3>Karir Rekomendasi AI</h3>

    </div>
    """, unsafe_allow_html=True)

    rekomendasi_magang = {

        "IT Support": {
            "industri": [
                "Perusahaan IT",
                "ISP (Internet Service Provider)",
                "Service Komputer",
                "Divisi IT Perusahaan"
            ],
            "posisi": [
                "IT Support Intern",
                "Helpdesk Support",
                "Teknisi Jaringan",
                "Junior Network Technician"
            ]
        },

        "Programmer": {
            "industri": [
                "Software House",
                "Startup Teknologi",
                "Perusahaan Pengembang Aplikasi",
                "Digital Agency"
            ],
            "posisi": [
                "Junior Programmer",
                "Web Developer Intern",
                "Backend Intern",
                "Frontend Intern"
            ]
        },

        "Game Developer": {
            "industri": [
                "Studio Game",
                "Perusahaan Multimedia",
                "Developer Mobile Game",
                "Creative Agency"
            ],
            "posisi": [
                "Game Programmer",
                "Unity Developer Intern",
                "Game Tester",
                "Game Designer Intern"
            ]
        },

        "HRD": {
            "industri": [
                "Perusahaan Manufaktur",
                "Perusahaan Swasta",
                "Perusahaan Jasa",
                "Perkantoran"
            ],
            "posisi": [
                "HR Staff",
                "Recruitment Staff",
                "Admin HR",
                "People Development"
            ]
        },

        "Marketing": {
            "industri": [
                "Digital Agency",
                "Perusahaan Retail",
                "E-Commerce",
                "Perusahaan Jasa"
            ],
            "posisi": [
                "Marketing Staff",
                "Digital Marketing Intern",
                "Content Marketing",
                "Social Media Admin"
            ]
        },

        "Staff Administrasi": {
            "industri": [
                "Perkantoran",
                "Sekolah",
                "Rumah Sakit",
                "Instansi Pemerintah"
            ],
            "posisi": [
                "Admin Staff",
                "Data Entry",
                "Arsiparis",
                "Office Administrator"
            ]
        },

        "Akuntan": {
            "industri": [
                "Kantor Akuntan Publik",
                "Perusahaan Swasta",
                "Perbankan",
                "Konsultan Pajak"
            ],
            "posisi": [
                "Staff Akuntansi",
                "Admin Keuangan",
                "Junior Accountant",
                "Staff Pajak"
            ]
        }

    }
    # ==========================
    # RINGKASAN MAGANG
    # ==========================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🎯 Karir",
            hasil_ai
        )

    with col2:
        if hasil_ai in rekomendasi_magang:
            st.metric(
                "🏭 Industri",
                len(rekomendasi_magang[hasil_ai]["industri"])
            )

    with col3:
        if hasil_ai in rekomendasi_magang:
            st.metric(
                "💼 Posisi",
                len(rekomendasi_magang[hasil_ai]["posisi"])
            )
    if hasil_ai in rekomendasi_magang:

        data = rekomendasi_magang[hasil_ai]

        st.subheader(
            "🏭 Bidang Industri yang Cocok"
        )

        for item in data["industri"]:

            st.markdown(f"""
            <div style="
            background:white;
            padding:15px;
            border-radius:12px;
            margin-bottom:10px;
            border-left:6px solid #4a90e2;
            box-shadow:0px 2px 5px rgba(0,0,0,0.1);
            ">
            🏭 {item}
            </div>
            """, unsafe_allow_html=True)

        st.subheader(
            "💼 Posisi Magang yang Direkomendasikan"
        )

        for item in data["posisi"]:

            st.markdown(f"""
            <div style="
            background:#f8fbff;
            padding:15px;
            border-radius:12px;
            margin-bottom:10px;
            border-left:6px solid #28a745;
            box-shadow:0px 2px 5px rgba(0,0,0,0.1);
            ">
            💼 {item}
            </div>
            """, unsafe_allow_html=True)
        
        st.subheader(
            "📌 Kesimpulan"
        )

        st.markdown(f"""
        <div style="
        background:#fff3cd;
        padding:20px;
        border-radius:15px;
        border-left:8px solid #ffc107;
        margin-top:20px;
        ">

        <h3>📌 Kesimpulan Magang</h3>

        <p>
        Berdasarkan hasil analisis AI, siswa memiliki kecocokan
        tertinggi pada bidang <b>{hasil_ai}</b>.

        Tempat magang yang direkomendasikan dapat membantu
        mengembangkan skill serta pengalaman kerja sebelum lulus.
        </p>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.warning(
            f"Data rekomendasi magang untuk {hasil_ai} belum tersedia."
        )
    st.subheader(
    "📋 Ringkasan Magang"
    )
    st.progress(0.85)

    st.success(
        "🚀 Anda sudah berada pada tahap akhir proses rekomendasi karir."
)

    st.success(
        f"""
        Berdasarkan hasil AI, siswa direkomendasikan
        untuk mencari tempat magang pada bidang
        {hasil_ai} agar mendapatkan pengalaman kerja
        yang relevan dengan karir masa depan.
        """
    )
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📄 Lihat Laporan Akhir",
            use_container_width=True
        ):

            st.session_state.step = 11
            st.rerun()

    with col2:

        if st.button(
            "⬅ Kembali ke Hasil AI",
            use_container_width=True
        ):

            st.session_state.step = 4
            st.rerun()

        st.markdown("---")

        st.markdown("""
        <div style="
        text-align:center;
        color:gray;
        padding:10px;
        ">

        🏢 Internship Recommendation System <br>
        Career AI Recommendation System

        </div>
        """, unsafe_allow_html=True)
        
        
# =====================================
# STEP 11 - LAPORAN KARIR LENGKAP
# =====================================

elif st.session_state.step == 11:

    nama = st.session_state.nama
    jurusan = st.session_state.jurusan
    hasil_ai = st.session_state.get(
        "hasil_ai",
        "-"
    )

    persentase = st.session_state.get(
        "persentase_ai",
        0
    )
    skill = st.session_state.get(
        "skill",
        "-"
    )
    st.title("📄 Dashboard Laporan Karir")
    st.progress(11/11)
    st.success(
        f"""
        🎉 Analisis karir berhasil diselesaikan.

        Nama : {nama}
        Jurusan : {jurusan}

        Karir yang paling direkomendasikan AI adalah
        {hasil_ai} dengan tingkat kecocokan
        {persentase}%.
        """
    )
    
    # ==========================
    # GRAFIK RINGKASAN
    # ==========================

    st.subheader("📊 Ringkasan Hasil Analisis")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Karir Terpilih",
            hasil_ai
        )

    with col2:

        st.metric(
            "Kecocokan",
            f"{persentase}%"
        )

    st.progress(persentase / 100)

    # ==========================
    # DESKRIPSI
    # ==========================

    st.markdown("""
    ### 🎓 Laporan Akhir Analisis Karir

    Laporan ini dihasilkan secara otomatis berdasarkan
    analisis Artificial Intelligence terhadap data siswa
    dan hasil wawancara.
    """)
    # ==========================
    # HEADER
    # ==========================

    st.markdown(f"""
    <div style="
    padding:25px;
    border-radius:20px;
    background:linear-gradient(90deg,#1f4e79,#4a90e2);
    color:white;
    text-align:center;
    margin-bottom:20px;
    ">
    <h1>🎓 Laporan Analisis Karir Siswa</h1>
    <p>Artificial Intelligence Career Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)

    # ==========================
    # METRIC
    # ==========================

    col1,col2 = st.columns(2)

    with col1:
        st.metric("👤 Nama", nama)

    with col2:
        st.metric("🎓 Jurusan", jurusan)

    col3,col4 = st.columns(2)

    with col3:
        st.metric("🎯 Karir", hasil_ai)

    with col4:
        st.metric("📈 Kecocokan", f"{persentase}%")

    st.markdown("---")

    # ==========================
    # PROFIL SISWA
    # ==========================

    if "foto" in st.session_state and st.session_state.foto:
        st.image(
            st.session_state.foto,
            width=180
        )
    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#ffffff,#f8fbff);
    padding:25px;
    border-radius:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.15);
    border-left:8px solid #4a90e2;
    margin-bottom:20px;
    ">

    <h2 style="color:#1f4e79;">
    👤 Profil Siswa
    </h2>

    <hr>

    <p style="font-size:18px;">
    <b>Nama :</b> {nama}
    </p>

    <p style="font-size:18px;">
    <b>Jurusan :</b> {jurusan}
    </p>

    <p style="font-size:18px;">
    <b>Skill Awal :</b> {skill}
    </p>

    </div>
    """, unsafe_allow_html=True)

    # ==========================
    # HASIL AI
    # ==========================

    st.markdown(f"""
    <div style="
    background:linear-gradient(90deg,#1f4e79,#4a90e2);
    padding:30px;
    border-radius:20px;
    text-align:center;
    color:white;
    margin-bottom:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.2);
    ">

    <h1>
    🤖 {hasil_ai}
    </h1>

    <h3>
    Karir yang Direkomendasikan AI
    </h3>

    <h1>
    {persentase}%
    </h1>

    <p>
    Tingkat Kecocokan Karir
    </p>

    </div>
    """, unsafe_allow_html=True)
    
    st.subheader(
        "📈 Tingkat Kecocokan Karir"
    )

    st.progress(
        min(int(persentase), 100)
    )

    st.success(
        f"Siswa memiliki kecocokan sebesar {persentase}% pada bidang {hasil_ai}"
    )
    
    st.subheader("🚀 Status Kesiapan Kerja")

    if persentase >= 85:

        st.success(
            "⭐⭐⭐⭐⭐ Sangat Siap Magang dan Bekerja"
        )

    elif persentase >= 70:

        st.info(
            "⭐⭐⭐⭐ Siap Magang dengan Pengembangan Skill"
        )

    else:

        st.warning(
            "⭐⭐⭐ Perlu Peningkatan Skill"
        )

    # ==========================
    # SKILL REKOMENDASI
    # ==========================

    if hasil_ai in skill_karir:

        st.subheader(
            "🎓 Skill yang Direkomendasikan"
        )

        for item in skill_karir[hasil_ai]:

            st.success(
                item
            )

    # ==========================
    # SERTIFIKASI
    # ==========================

    if hasil_ai in sertifikasi_karir:

        st.subheader(
            "🏅 Sertifikasi yang Direkomendasikan"
        )

        for item in sertifikasi_karir[hasil_ai]:

            st.info(
                item
            )

    # ==========================
    # PELUANG PEKERJAAN
    # ==========================

    if hasil_ai in peluang_kerja:

        st.subheader(
            "💼 Peluang Pekerjaan"
        )

        for item in peluang_kerja[hasil_ai]:

            st.write(
                f"➡ {item}"
            )

    st.markdown("---")
    
    st.subheader("📊 Ringkasan Hasil")

    data_chart = {
        "Kategori": [
            "Kecocokan Karir"
        ],
        "Nilai": [
            persentase
        ]
    }

    import pandas as pd

    df_chart = pd.DataFrame(data_chart)

    st.bar_chart(
        df_chart.set_index("Kategori")
    )

    # ==========================
    # KESIMPULAN
    # ==========================

    st.markdown(f"""
    <div style="
    background:#fff3cd;
    padding:20px;
    border-radius:15px;
    border-left:8px solid #ffc107;
    ">

    <h3>🎯 Kesimpulan Akhir</h3>

    <p>
    Berdasarkan analisis Artificial Intelligence,
    siswa memiliki kecocokan tertinggi pada bidang
    <b>{hasil_ai}</b> dengan tingkat kecocokan
    <b>{persentase}%</b>.
    </p>

    <p>
    Disarankan untuk meningkatkan skill,
    mengikuti sertifikasi profesional,
    dan mencari tempat magang yang relevan
    agar lebih siap memasuki dunia kerja.
    </p>

    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # ==========================
    # DOWNLOAD PDF
    # ==========================

    st.markdown("""
    <div style="
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom:20px;
    text-align:center;
    ">

    <h2>📥 Download Laporan Karir</h2>

    <p>
    Unduh laporan hasil analisis karir siswa dalam format PDF
    untuk dokumentasi dan referensi pengembangan karir.
    </p>

    </div>
    """, unsafe_allow_html=True)
    
    if st.button(
        "📄 Generate Laporan PDF",
        key="generate_pdf",
        use_container_width=True
    ):

        pdf = FPDF()

        pdf.add_page()

        pdf.set_font(
            "Arial",
            "B",
            16
        )

        pdf.cell(
            200,
            10,
            "LAPORAN HASIL ANALISIS KARIR",
            ln=True
        )

        pdf.ln(10)

        pdf.set_font(
            "Arial",
            "",
            12
        )

        pdf.cell(
            200,
            10,
            f"Nama : {nama}",
            ln=True
        )

        pdf.cell(
            200,
            10,
            f"Jurusan : {jurusan}",
            ln=True
        )

        pdf.cell(
            200,
            10,
            f"Karir Rekomendasi : {hasil_ai}",
            ln=True
        )

        pdf.cell(
            200,
            10,
            f"Persentase Kecocokan : {persentase}%",
            ln=True
        )

        pdf.output(
            "laporan_karir_siswa.pdf"
        )

        with open(
            "laporan_karir_siswa.pdf",
            "rb"
        ) as file:

            st.download_button(
                label="📥 Download Laporan PDF",
                data=file,
                file_name="laporan_karir_siswa.pdf",
                mime="application/pdf",
                key="download_pdf"
            )

    st.markdown("---")

    st.markdown("""
    <div style="
    text-align:center;
    color:gray;
    padding:10px;
    ">

    © 2026 Career AI System <br>
    Sistem Rekomendasi Karir Siswa SMK Berbasis Artificial Intelligence

    </div>
    """, unsafe_allow_html=True)
    
    if st.button(
    "ℹ️ Tentang Aplikasi",
    use_container_width=True
    ):

        st.session_state.step = 12
        st.rerun()

    if st.button(
        "⬅ Kembali ke Rekomendasi Magang",
        key="kembali_magang",
        use_container_width=True
    ):
        st.session_state.step = 10
        st.rerun()
        
   # =====================================
# STEP 12 - TENTANG APLIKASI
# =====================================

elif st.session_state.step == 12:

    st.title("ℹ️ Tentang Aplikasi")

    st.markdown("""
    <div style="
    background:linear-gradient(90deg,#1f4e79,#4a90e2);
    padding:30px;
    border-radius:20px;
    color:white;
    text-align:center;
    box-shadow:0px 5px 15px rgba(0,0,0,0.2);
    ">
    <h1>🎓 Sistem Rekomendasi Karir Siswa SMK</h1>
    <h3>Artificial Intelligence Career Recommendation System</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ==========================
    # INFORMASI PENELITIAN
    # ==========================

    st.subheader("📌 Informasi Penelitian")

    st.info("""
    Judul Penelitian:

    Pengembangan Sistem Rekomendasi Karir Siswa SMK Berbasis Web Menggunakan Algoritma Naive Bayes
    """)

    # ==========================
    # TUJUAN DAN FITUR
    # ==========================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🎯 Tujuan Sistem")

        st.write("""
        Sistem ini dibuat untuk membantu siswa SMK
        menemukan rekomendasi karir yang sesuai
        berdasarkan minat, kemampuan, skill,
        dan hasil wawancara.
        """)

        st.subheader("🤖 Teknologi")

        st.success("Python")
        st.success("Streamlit")
        st.success("Scikit-Learn")
        st.success("Machine Learning")
        st.success("SQLite Database")

    with col2:

        st.subheader("🚀 Fitur Utama")

        st.write("""
        ✅ Analisis Karir Otomatis

        ✅ Dashboard Statistik

        ✅ Curriculum Vitae Otomatis

        ✅ Feedback Pengguna

        ✅ Rekomendasi Tempat Magang

        ✅ Laporan PDF
        """)

        st.subheader("🎯 Target Pengguna")

        st.write("""
        Siswa SMK yang ingin mengetahui
        karir yang sesuai dengan minat,
        skill, dan kemampuan mereka.
        """)

    st.markdown("---")

    # ==========================
    # DATASET
    # ==========================

    st.subheader("📊 Dataset")

    st.write("""
    Dataset berisi berbagai profesi,
    skill, minat karir, dan hasil pelatihan
    model Machine Learning yang digunakan
    untuk menghasilkan rekomendasi karir siswa.
    """)

    st.markdown("---")

    # ==========================
    # PENGEMBANG
    # ==========================

    st.subheader("👨‍🎓 Pengembang")

    st.success("""
    Nama : Nadiyah Putri Salim

    Program Studi : Teknik Informatika

    Universitas : Universitas Cendekia Abditama (UCA)
    """)

    st.markdown("---")

    # ==========================
    # STATISTIK SISTEM
    # ==========================

    st.subheader("📈 Statistik Sistem")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🎓 Jurusan",
            "5+"
        )

    with col2:
        st.metric(
            "💼 Karir",
            "7+"
        )

    with col3:
        st.metric(
            "🏢 Magang",
            "20+"
        )

    st.markdown("---")

    st.subheader("📅 Tahun")

    st.write("2026")

    st.markdown("""
    <div style="
    text-align:center;
    color:gray;
    padding:20px;
    ">

    🎓 Career AI Recommendation System

    © 2026

    </div>
    """, unsafe_allow_html=True)

    # ==========================
    # BUTTON
    # ==========================

    if st.button(
        "⬅ Kembali ke Laporan Akhir",
        use_container_width=True
    ):

        st.session_state.step = 11
        st.rerun()