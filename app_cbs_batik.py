import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================
st.set_page_config(page_title="Bank Kampus Nusantara · CBS Lab", page_icon="🪷", layout="wide")

# Palet: indigo batik, emas soga, teal, magenta, hijau daun
INDIGO = "#1E2A78"
INDIGO_DARK = "#141C57"
EMAS = "#F2B134"
TEAL = "#0FA3A3"
MAGENTA = "#E2427D"
DAUN = "#4CAF6A"
LANGIT = "#F3F1FF"


def rupiah(x):
    return "Rp " + f"{x:,}".replace(",", ".")


# =====================================================
# ORNAMEN: pola kawung (SVG) sebagai latar
# =====================================================
def kawung(warna, opasitas=0.35, ukuran=56):
    r = ukuran / 4
    c = ukuran / 2
    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='{ukuran}' height='{ukuran}' viewBox='0 0 {ukuran} {ukuran}'>
    <g fill='none' stroke='{warna}' stroke-opacity='{opasitas}' stroke-width='1.4'>
    <ellipse cx='{c}' cy='{c - r}' rx='{r * 0.62}' ry='{r}'/>
    <ellipse cx='{c}' cy='{c + r}' rx='{r * 0.62}' ry='{r}'/>
    <ellipse cx='{c - r}' cy='{c}' rx='{r}' ry='{r * 0.62}'/>
    <ellipse cx='{c + r}' cy='{c}' rx='{r}' ry='{r * 0.62}'/>
    </g><circle cx='{c}' cy='{c}' r='2.4' fill='{warna}' fill-opacity='{min(opasitas + 0.25, 1)}'/></svg>"""
    return "url(\"data:image/svg+xml;utf8," + quote(svg) + "\")"


POLA_HEADER = kawung(EMAS, 0.55)
POLA_SIDEBAR = kawung("#FFFFFF", 0.14, 48)
POLA_BODY = kawung("#FFFFFF", 0.07, 64)

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=DM+Sans:wght@400;500;700&display=swap');

html, body, [class*="css"], .stApp {{ font-family: 'DM Sans', sans-serif; }}
h1, h2, h3, .judul {{ font-family: 'Bricolage Grotesque', sans-serif !important; }}

.stApp, [data-testid="stAppViewContainer"] {{
    background-color: #1A2370;
    background-image: {POLA_BODY};
}}
header[data-testid="stHeader"] {{ background: transparent; }}

/* SIDEBAR */
[data-testid="stSidebar"] {{
    background-color: #0F1547;
    background-image: {POLA_SIDEBAR};
    border-right: 5px solid {EMAS};
}}
[data-testid="stSidebar"] * {{ color: #FFFFFF; }}
[data-testid="stSidebar"] label p {{ font-weight: 500; font-size: 1.02rem; }}

.merek {{
    text-align: center; padding: 8px 0 14px 0;
}}
.merek .logo {{ font-size: 2.6rem; line-height: 1; }}
.merek .nama {{
    font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800;
    font-size: 1.35rem; color: {EMAS}; margin-top: 4px;
}}
.merek .sub {{ font-size: .8rem; opacity: .85; }}

/* BANNER */
.banner {{
    position: relative; overflow: hidden;
    background-color: #2E3FB5;
    background-image: {POLA_HEADER};
    border-radius: 22px; padding: 30px 34px; margin-bottom: 8px;
    border-bottom: 6px solid {MAGENTA};
    box-shadow: 0 10px 0 {TEAL};
}}
.banner h1 {{
    color: #fff; margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -.5px;
}}
.banner p {{ color: #E4E6FF; margin: 6px 0 0 0; font-size: .98rem; }}
.banner .lencana {{
    display: inline-block; background: {EMAS}; color: {INDIGO_DARK};
    font-weight: 700; font-size: .78rem; padding: 4px 12px; border-radius: 999px; margin-bottom: 10px;
}}
.banner .teratai {{
    position: absolute; right: 26px; top: 50%; transform: translateY(-50%);
    font-size: 5.2rem; opacity: .95; filter: drop-shadow(0 4px 0 rgba(0,0,0,.25));
}}

/* PEMISAH ORNAMEN */
.pemisah {{
    display: flex; align-items: center; gap: 10px; margin: 26px 0 14px 0;
}}
.pemisah .garis {{ flex: 1; height: 3px; border-radius: 3px;
    background: repeating-linear-gradient(90deg, {INDIGO} 0 10px, transparent 10px 16px); opacity: .35; }}
.pemisah .belah {{ width: 11px; height: 11px; transform: rotate(45deg); }}
.pemisah .teks {{ font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700;
    font-size: 1.25rem; color: {INDIGO}; padding: 0 6px; }}

/* KARTU METRIK */
.kartu {{
    background: #fff; border-radius: 18px; padding: 18px 20px; height: 100%;
    border: 2px solid var(--w); box-shadow: 6px 6px 0 var(--w); position: relative; overflow: hidden;
}}
.kartu .ikon {{
    position: absolute; right: -6px; top: -10px; font-size: 3.6rem; opacity: .16;
}}
.kartu .label {{ font-size: .85rem; color: #5b5f8a; font-weight: 500; }}
.kartu .nilai {{ font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800;
    font-size: 1.65rem; color: var(--w); margin-top: 2px; }}

/* KARTU NASABAH */
.nasabah {{
    background: linear-gradient(120deg, {TEAL}, {INDIGO});
    color: #fff; border-radius: 18px; padding: 18px 22px; margin: 8px 0 16px 0;
    border-left: 8px solid {EMAS};
}}
.nasabah .nm {{ font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.3rem; }}
.nasabah .sl {{ font-size: 1.05rem; opacity: .95; }}

/* TOMBOL */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {{
    background: linear-gradient(135deg, {MAGENTA}, #FF7A59); color: #fff; font-weight: 700;
    border: none; border-radius: 14px; padding: .6rem 1.4rem; box-shadow: 0 5px 0 #A92B5C;
    transition: transform .08s, box-shadow .08s;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {{ color: #fff; filter: brightness(1.06); }}
.stButton > button:active, .stFormSubmitButton > button:active, .stDownloadButton > button:active {{ transform: translateY(4px); box-shadow: 0 1px 0 #A92B5C; }}

/* INPUT */
.stTextInput input, .stNumberInput input {{
    border-radius: 12px !important; border: 2px solid {INDIGO}33 !important; background: #fff;
}}
.stTextInput input:focus, .stNumberInput input:focus {{ border-color: {TEAL} !important; }}

/* TAB & TABEL */
.stTabs [data-baseweb="tab"] {{ font-weight: 700; font-family: 'Bricolage Grotesque', sans-serif; }}
.stTabs [aria-selected="true"] {{ color: {MAGENTA} !important; }}
[data-testid="stDataFrame"] {{ border: 2px solid {EMAS}; border-radius: 14px; overflow: hidden; }}

/* ===== KETERBACAAN: judul & label terang, kotak pesan/input gelap di atas putih ===== */
[data-testid="stMain"], [data-testid="stMain"] p, [data-testid="stMain"] li,
[data-testid="stMain"] label, [data-testid="stMain"] span,
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p,
[data-testid="stCaptionContainer"] {{ color: #FFFFFF; }}
[data-testid="stToolbar"] * {{ color: #FFFFFF !important; }}

.banner h1, .banner p {{ color: #FFFFFF !important; }}
.banner p {{ color: #E4E6FF !important; }}
.banner .lencana {{ color: {INDIGO_DARK} !important; }}
.nasabah, .nasabah * {{ color: #FFFFFF !important; }}
.kartu .label {{ color: #3D4280 !important; }}
.kartu .nilai {{ color: var(--w) !important; }}
.pemisah .teks {{ color: #FFFFFF !important; }}
.pemisah .garis {{ background: repeating-linear-gradient(90deg, {EMAS} 0 10px, transparent 10px 16px) !important; opacity: .7; }}
[data-testid="stSidebar"], [data-testid="stSidebar"] * {{ color: #FFFFFF !important; }}
[data-testid="stSidebar"] .merek .nama {{ color: {EMAS} !important; }}

/* kolom isian data: latar putih, tulisan gelap */
.stTextInput input, .stNumberInput input {{
    color: {INDIGO_DARK} !important; background: #FFFFFF !important;
    -webkit-text-fill-color: {INDIGO_DARK} !important;
}}
.stNumberInput button {{ background: #E8E6FF !important; color: {INDIGO_DARK} !important; }}
.stNumberInput button svg {{ fill: {INDIGO_DARK} !important; }}

/* tab: terang, yang aktif emas */
.stTabs [data-baseweb="tab"] p {{ color: #FFFFFF !important; }}
.stTabs [aria-selected="true"] p {{ color: {EMAS} !important; }}
.stTabs [data-baseweb="tab-highlight"] {{ background-color: {EMAS} !important; }}

/* kotak pesan: latar putih, tulisan gelap */
[data-testid="stAlert"] {{ background: #FFFFFF !important; border: 2px solid {EMAS}; border-radius: 14px; }}
[data-testid="stAlert"] *, [data-testid="stAlert"] p {{ color: {INDIGO_DARK} !important; }}

/* TABEL: putih, tulisan gelap, header berwarna */
.tbl-wrap {{ max-height: 440px; overflow: auto; border: 3px solid {EMAS}; border-radius: 14px; background: #FFFFFF; }}
.tbl {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
.tbl thead th {{
    position: sticky; top: 0; background: linear-gradient(90deg, {TEAL}, {INDIGO});
    color: #FFFFFF !important; text-align: left; padding: 10px 14px; font-weight: 700; white-space: nowrap;
}}
.tbl tbody td {{ color: {INDIGO_DARK} !important; padding: 9px 14px; border-bottom: 1px solid #E3E0FA; background: #FFFFFF; }}
.tbl tbody tr:nth-child(even) td {{ background: #F1EFFF; }}

/* PILIHAN (selectbox): putih dengan tulisan gelap */
[data-baseweb="select"] > div {{ background: #FFFFFF !important; border: 2px solid {EMAS} !important; border-radius: 12px !important; }}
[data-baseweb="select"] *, [data-baseweb="select"] input {{ color: {INDIGO_DARK} !important; -webkit-text-fill-color: {INDIGO_DARK} !important; }}
[data-baseweb="select"] svg {{ fill: {INDIGO_DARK} !important; }}
[data-baseweb="popover"] ul, [data-baseweb="popover"] li, [data-baseweb="menu"] {{ background: #FFFFFF !important; color: {INDIGO_DARK} !important; }}
[data-baseweb="popover"] li:hover {{ background: #E8E6FF !important; }}

@media (max-width: 700px) {{
    .banner .teratai {{ display: none; }}
    .banner h1 {{ font-size: 1.6rem; }}
}}
@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>
""",
    unsafe_allow_html=True,
)


# =====================================================
# KOMPONEN TAMPILAN
# =====================================================
def pemisah(teks, warna=MAGENTA):
    st.markdown(
        f"""<div class='pemisah'><div class='garis'></div>
        <div class='belah' style='background:{warna}'></div>
        <div class='teks'>{teks}</div>
        <div class='belah' style='background:{EMAS}'></div>
        <div class='garis'></div></div>""",
        unsafe_allow_html=True,
    )


KOLOM_ANGKA = ("Debit", "Kredit", "Saldo", "Jumlah", "Masuk", "Keluar", "Bunga")


def tabel(df):
    """Tabel HTML berlatar putih (tidak ikut tema gelap)."""
    d = df.copy()
    for kol in KOLOM_ANGKA:
        if kol in d.columns:
            d[kol] = d[kol].apply(lambda x: "" if pd.isna(x) else f"{int(x):,}".replace(",", "."))
    html = d.to_html(index=False, border=0, classes="tbl", escape=True)
    st.markdown(f"<div class='tbl-wrap'>{html}</div>", unsafe_allow_html=True)


def kartu(label, nilai, ikon, warna):
    return f"""<div class='kartu' style='--w:{warna}'>
        <div class='ikon'>{ikon}</div>
        <div class='label'>{label}</div>
        <div class='nilai'>{nilai}</div></div>"""


def banner(lencana, judul, sub):
    st.markdown(
        f"""<div class='banner'><span class='lencana'>{lencana}</span>
        <h1>{judul}</h1><p>{sub}</p><div class='teratai'>🪷</div></div>""",
        unsafe_allow_html=True,
    )


# =====================================================
# BAGAN AKUN & DATABASE SEDERHANA (SESSION STATE)
# =====================================================
AKUN = {
    "101": ("Kas Teller", "Aset"),
    "201": ("Tabungan Nasabah", "Kewajiban"),
    "301": ("Modal Disetor", "Ekuitas"),
    "401": ("Pendapatan Administrasi", "Pendapatan"),
    "501": ("Beban Bunga Tabungan", "Beban"),
}
NORMAL_DEBIT = ("Aset", "Beban")
BIAYA_ADMIN = 10_000


def label(kode):
    return f"{kode} - {AKUN[kode][0]}"


def catat_jurnal(baris, ket, no_rek="-"):
    """baris = [(kode_akun, debit, kredit), ...]. Total debit harus sama dengan total kredit."""
    assert sum(b[1] for b in baris) == sum(b[2] for b in baris), "Jurnal tidak seimbang"
    st.session_state.no_jurnal += 1
    nomor = f"JU-{st.session_state.no_jurnal:04d}"
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for kode, d, k in baris:
        st.session_state.jurnal_umum.append(
            {"No Jurnal": nomor, "Waktu": waktu, "No Rek": no_rek, "Keterangan": ket,
             "Kode Akun": label(kode), "Debit": d, "Kredit": k}
        )


if "rekening_nasabah" not in st.session_state:
    st.session_state.rekening_nasabah = {"123456": {"nama": "Budi Santoso", "saldo": 5_000_000}}
if "jurnal_umum" not in st.session_state:
    st.session_state.jurnal_umum = []
    st.session_state.no_jurnal = 0
    # Saldo awal: kas Rp100 juta = tabungan Budi Rp5 juta + modal Rp95 juta
    catat_jurnal([("101", 100_000_000, 0), ("201", 0, 5_000_000), ("301", 0, 95_000_000)], "Saldo awal", "123456")


def df_jurnal():
    d = pd.DataFrame(st.session_state.jurnal_umum)
    d["Kode"] = d["Kode Akun"].str[:3]
    return d


def saldo_akun(kode, d=None):
    d = df_jurnal() if d is None else d
    x = d[d["Kode"] == kode]
    selisih = int(x["Debit"].sum()) - int(x["Kredit"].sum())
    return selisih if AKUN[kode][1] in NORMAL_DEBIT else -selisih


def semua_saldo():
    d = df_jurnal()
    return {k: saldo_akun(k, d) for k in AKUN}


def daftar_rekening():
    return pd.DataFrame(
        [{"No Rek": k, "Nama": v["nama"], "Saldo": v["saldo"]} for k, v in st.session_state.rekening_nasabah.items()]
    )


def unduh(df, nama_file, teks="Unduh CSV"):
    st.download_button(teks, df.to_csv(index=False).encode("utf-8"), file_name=nama_file, mime="text/csv")


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown(
        """<div class='merek'><div class='logo'>🪷</div>
        <div class='nama'>Bank Kampus Nusantara</div>
        <div class='sub'>Laboratorium Perbankan</div></div>""",
        unsafe_allow_html=True,
    )
    menu = st.radio(
        "Menu operasional",
        ["📊 Dashboard", "🏧 Teller", "🧾 Customer Service", "📒 Mutasi Rekening",
         "📜 Jurnal Umum", "📚 Buku Besar", "⚖️ Neraca Saldo", "📈 Laporan Keuangan"],
    )
    st.markdown("---")
    st.caption("Mengacu pada SEOJK No. 34/SEOJK.03/2021 tentang BPAK")

halaman = menu.split(" ", 1)[1]

# =====================================================
# DASHBOARD
# =====================================================
if halaman == "Dashboard":
    banner("CORE BANKING SYSTEM", "Dashboard", "Ringkasan kas, tabungan, laba, dan transaksi terbaru secara langsung.")
    saldo = semua_saldo()
    d = df_jurnal()
    laba = saldo["401"] - saldo["501"]
    jml_transaksi = d["No Jurnal"].nunique() - 1  # saldo awal tidak dihitung

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kartu("Kas Teller (101)", rupiah(saldo["101"]), "💰", TEAL), unsafe_allow_html=True)
    c2.markdown(kartu("Tabungan Nasabah (201)", rupiah(saldo["201"]), "🐷", MAGENTA), unsafe_allow_html=True)
    c3.markdown(kartu("Laba Bersih Berjalan", rupiah(laba), "📈", DAUN if laba >= 0 else MAGENTA), unsafe_allow_html=True)
    c4.markdown(kartu("Transaksi Hari Ini", f"{jml_transaksi}", "🧮", INDIGO), unsafe_allow_html=True)

    pemisah("Transaksi Terbaru")
    terbaru = d[d["Keterangan"] != "Saldo awal"].iloc[::-1].head(8)
    if len(terbaru):
        tabel(terbaru[["No Jurnal", "Waktu", "Keterangan", "Kode Akun", "Debit", "Kredit"]])
    else:
        st.info("Belum ada transaksi. Buka menu Teller untuk memulai setoran atau penarikan.")

    pemisah("Daftar Rekening Nasabah", TEAL)
    tabel(daftar_rekening())

# =====================================================
# TELLER
# =====================================================
elif halaman == "Teller":
    banner("LOKET TELLER", "Transaksi Tunai", "Setor atau tarik tunai, jurnal debit-kredit terbentuk otomatis.")
    no_rek = st.text_input("Nomor rekening nasabah", "123456")

    if no_rek in st.session_state.rekening_nasabah:
        nasabah = st.session_state.rekening_nasabah[no_rek]
        st.markdown(
            f"""<div class='nasabah'><div class='nm'>👤 {nasabah['nama']}</div>
            <div class='sl'>Saldo saat ini: <b>{rupiah(nasabah['saldo'])}</b></div></div>""",
            unsafe_allow_html=True,
        )
        tab_setor, tab_tarik = st.tabs(["⬇️ Setor tunai", "⬆️ Tarik tunai"])

        with tab_setor:
            jumlah_setor = st.number_input("Jumlah setoran (Rp)", min_value=10_000, step=50_000, key="setor")
            if st.button("Proses setoran"):
                nasabah["saldo"] += jumlah_setor
                catat_jurnal([("101", jumlah_setor, 0), ("201", 0, jumlah_setor)], "Setor tunai", no_rek)
                st.success(f"Setoran {rupiah(jumlah_setor)} masuk. Jurnal otomatis sudah tercatat.")
                st.balloons()

        with tab_tarik:
            jumlah_tarik = st.number_input("Jumlah penarikan (Rp)", min_value=10_000, step=50_000, key="tarik")
            if st.button("Proses penarikan"):
                if jumlah_tarik > nasabah["saldo"]:
                    st.error(f"Saldo nasabah tidak cukup. Maksimal penarikan {rupiah(nasabah['saldo'])}.")
                elif jumlah_tarik > saldo_akun("101"):
                    st.error("Kas teller tidak cukup. Ajukan tambahan kas ke kepala cabang.")
                else:
                    nasabah["saldo"] -= jumlah_tarik
                    catat_jurnal([("201", jumlah_tarik, 0), ("101", 0, jumlah_tarik)], "Tarik tunai", no_rek)
                    st.success(f"Penarikan {rupiah(jumlah_tarik)} berhasil. Jurnal otomatis sudah tercatat.")
    else:
        st.error("Nomor rekening tidak ditemukan. Periksa kembali nomornya atau buka rekening baru di Customer Service.")

# =====================================================
# CUSTOMER SERVICE
# =====================================================
elif halaman == "Customer Service":
    banner("MEJA CUSTOMER SERVICE", "Layanan Nasabah", "Buka rekening baru dan kreditkan bunga tabungan bulanan.")
    tab_buka, tab_bunga = st.tabs(["🆕 Buka rekening", "💹 Bunga tabungan"])

    with tab_buka:
        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.caption(f"Biaya administrasi pembukaan rekening {rupiah(BIAYA_ADMIN)} dipotong dari setoran awal.")
            with st.form("form_rekening", clear_on_submit=True):
                nama_baru = st.text_input("Nama lengkap nasabah")
                no_baru = st.text_input("Nomor rekening (6 digit)", max_chars=6)
                setoran_awal = st.number_input("Setoran awal (Rp)", min_value=50_000, step=50_000)
                kirim = st.form_submit_button("Buka rekening")

            if kirim:
                if not nama_baru.strip():
                    st.error("Nama nasabah wajib diisi.")
                elif not (no_baru.isdigit() and len(no_baru) == 6):
                    st.error("Nomor rekening harus tepat 6 digit angka.")
                elif no_baru in st.session_state.rekening_nasabah:
                    st.error("Nomor rekening sudah dipakai. Gunakan nomor lain.")
                else:
                    st.session_state.rekening_nasabah[no_baru] = {
                        "nama": nama_baru.strip(), "saldo": setoran_awal - BIAYA_ADMIN}
                    catat_jurnal([("101", setoran_awal, 0), ("201", 0, setoran_awal)],
                                 "Setoran awal pembukaan rekening", no_baru)
                    catat_jurnal([("201", BIAYA_ADMIN, 0), ("401", 0, BIAYA_ADMIN)],
                                 "Biaya administrasi pembukaan rekening", no_baru)
                    st.success(f"Rekening {no_baru} atas nama {nama_baru.strip()} berhasil dibuka. "
                               f"Saldo awal {rupiah(setoran_awal - BIAYA_ADMIN)} setelah biaya administrasi.")
                    st.balloons()
        with col_b:
            st.markdown(kartu("Total rekening aktif", f"{len(st.session_state.rekening_nasabah)}", "👥", TEAL),
                        unsafe_allow_html=True)

    with tab_bunga:
        rate = st.number_input("Suku bunga tabungan per tahun (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.5)
        rincian = [(k, v["nama"], int(v["saldo"] * rate / 100 / 12)) for k, v in st.session_state.rekening_nasabah.items()]
        rincian = [r for r in rincian if r[2] > 0]
        if rincian:
            tabel(pd.DataFrame(rincian, columns=["No Rek", "Nama", "Bunga"]))
            st.caption("Bunga bulanan = saldo × suku bunga ÷ 12. Dicatat sebagai beban bunga (501) dan menambah tabungan nasabah (201).")
            if st.button("Kreditkan bunga bulan ini"):
                for no, _, bunga in rincian:
                    st.session_state.rekening_nasabah[no]["saldo"] += bunga
                    catat_jurnal([("501", bunga, 0), ("201", 0, bunga)], "Bunga tabungan bulanan", no)
                st.success(f"Bunga total {rupiah(sum(r[2] for r in rincian))} sudah dikreditkan ke {len(rincian)} rekening.")
        else:
            st.info("Belum ada saldo yang menghasilkan bunga pada suku bunga ini.")

    pemisah("Daftar Nasabah", TEAL)
    tabel(daftar_rekening())

# =====================================================
# MUTASI REKENING
# =====================================================
elif halaman == "Mutasi Rekening":
    banner("MUTASI REKENING", "Mutasi Rekening", "Riwayat uang masuk dan keluar per nasabah, lengkap dengan saldo berjalan.")
    rek = st.session_state.rekening_nasabah
    pilihan = {f"{k} - {v['nama']}": k for k, v in rek.items()}
    no = pilihan[st.selectbox("Pilih rekening", list(pilihan.keys()))]

    d = df_jurnal()
    x = d[(d["No Rek"] == no) & (d["Kode"] == "201")].copy()
    x["Masuk"] = x["Kredit"]
    x["Keluar"] = x["Debit"]
    x["Saldo"] = (x["Masuk"] - x["Keluar"]).cumsum()

    c1, c2, c3 = st.columns(3)
    c1.markdown(kartu("Saldo akhir", rupiah(rek[no]["saldo"]), "💳", TEAL), unsafe_allow_html=True)
    c2.markdown(kartu("Total masuk", rupiah(int(x["Masuk"].sum())), "⬇️", DAUN), unsafe_allow_html=True)
    c3.markdown(kartu("Total keluar", rupiah(int(x["Keluar"].sum())), "⬆️", MAGENTA), unsafe_allow_html=True)

    pemisah("Rincian Mutasi")
    hasil = x[["Waktu", "No Jurnal", "Keterangan", "Masuk", "Keluar", "Saldo"]]
    tabel(hasil)
    unduh(hasil, f"mutasi_{no}.csv", "Unduh mutasi (CSV)")

# =====================================================
# JURNAL UMUM
# =====================================================
elif halaman == "Jurnal Umum":
    banner("PEMBUKUAN", "Jurnal Umum", "Setiap transaksi tercatat otomatis sebagai pasangan debit dan kredit.")
    d = df_jurnal()
    td, tk = int(d["Debit"].sum()), int(d["Kredit"].sum())

    c1, c2, c3 = st.columns(3)
    c1.markdown(kartu("Jumlah jurnal", f"{d['No Jurnal'].nunique()}", "🧾", INDIGO), unsafe_allow_html=True)
    c2.markdown(kartu("Total debit", rupiah(td), "➕", TEAL), unsafe_allow_html=True)
    c3.markdown(kartu("Total kredit", rupiah(tk), "➖", MAGENTA), unsafe_allow_html=True)

    pemisah("Buku Jurnal")
    hasil = d[["No Jurnal", "Waktu", "No Rek", "Keterangan", "Kode Akun", "Debit", "Kredit"]]
    tabel(hasil)
    if td == tk:
        st.success("Jurnal seimbang: total debit sama dengan total kredit.")
    else:
        st.error("Jurnal tidak seimbang. Periksa kembali transaksi yang dicatat.")
    unduh(hasil, "jurnal_umum.csv", "Unduh jurnal (CSV)")

# =====================================================
# BUKU BESAR
# =====================================================
elif halaman == "Buku Besar":
    banner("PEMBUKUAN", "Buku Besar", "Mutasi dan saldo berjalan untuk setiap akun.")
    pilih = st.selectbox("Pilih akun", [label(k) for k in AKUN])
    kode = pilih[:3]
    d = df_jurnal()
    x = d[d["Kode"] == kode].copy()
    if AKUN[kode][1] in NORMAL_DEBIT:
        x["Saldo"] = (x["Debit"] - x["Kredit"]).cumsum()
    else:
        x["Saldo"] = (x["Kredit"] - x["Debit"]).cumsum()

    c1, c2, c3 = st.columns(3)
    c1.markdown(kartu(f"Saldo akhir ({AKUN[kode][1]})", rupiah(saldo_akun(kode, d)), "📚", TEAL), unsafe_allow_html=True)
    c2.markdown(kartu("Total debit", rupiah(int(x["Debit"].sum())), "➕", INDIGO), unsafe_allow_html=True)
    c3.markdown(kartu("Total kredit", rupiah(int(x["Kredit"].sum())), "➖", MAGENTA), unsafe_allow_html=True)

    pemisah(f"Akun {pilih}")
    if x.empty:
        st.info("Belum ada transaksi pada akun ini.")
    else:
        tabel(x[["Waktu", "No Jurnal", "Keterangan", "Debit", "Kredit", "Saldo"]])

# =====================================================
# NERACA SALDO
# =====================================================
elif halaman == "Neraca Saldo":
    banner("PEMBUKUAN", "Neraca Saldo", "Daftar saldo semua akun untuk menguji keseimbangan debit dan kredit.")
    saldo = semua_saldo()
    baris = []
    for k, (nama, kel) in AKUN.items():
        net_debit = saldo[k] if kel in NORMAL_DEBIT else -saldo[k]
        baris.append({"Kode Akun": label(k), "Kelompok": kel, "Debit": max(net_debit, 0), "Kredit": max(-net_debit, 0)})
    df = pd.DataFrame(baris)
    td, tk = int(df["Debit"].sum()), int(df["Kredit"].sum())
    df.loc[len(df)] = {"Kode Akun": "TOTAL", "Kelompok": "", "Debit": td, "Kredit": tk}
    tabel(df)
    if td == tk:
        st.success(f"Seimbang: total debit {rupiah(td)} = total kredit {rupiah(tk)}")
    else:
        st.error(f"Tidak seimbang: debit {rupiah(td)}, kredit {rupiah(tk)}")

# =====================================================
# LAPORAN KEUANGAN
# =====================================================
else:
    banner("PELAPORAN", "Laporan Keuangan", "Laba rugi, perubahan ekuitas, dan posisi keuangan (neraca) dari data jurnal.")
    s = semua_saldo()
    pendapatan, beban = s["401"], s["501"]
    laba = pendapatan - beban
    aset, kewajiban, modal = s["101"], s["201"], s["301"]
    ekuitas_akhir = modal + laba

    tab_lr, tab_eq, tab_neraca = st.tabs(["📈 Laba rugi", "🏛️ Perubahan ekuitas", "⚖️ Posisi keuangan (neraca)"])

    with tab_lr:
        tabel(pd.DataFrame([
            {"Keterangan": "PENDAPATAN", "Jumlah": None},
            {"Keterangan": label("401"), "Jumlah": pendapatan},
            {"Keterangan": "Total pendapatan", "Jumlah": pendapatan},
            {"Keterangan": "BEBAN", "Jumlah": None},
            {"Keterangan": label("501"), "Jumlah": beban},
            {"Keterangan": "Total beban", "Jumlah": beban},
            {"Keterangan": "LABA (RUGI) BERSIH", "Jumlah": laba},
        ]))
        st.markdown(kartu("Laba (rugi) bersih", rupiah(laba), "📈", DAUN if laba >= 0 else MAGENTA), unsafe_allow_html=True)

    with tab_eq:
        tabel(pd.DataFrame([
            {"Keterangan": "Modal disetor awal", "Jumlah": modal},
            {"Keterangan": "Laba (rugi) bersih periode berjalan", "Jumlah": laba},
            {"Keterangan": "EKUITAS AKHIR", "Jumlah": ekuitas_akhir},
        ]))

    with tab_neraca:
        total_pasiva = kewajiban + ekuitas_akhir
        tabel(pd.DataFrame([
            {"Keterangan": "ASET", "Jumlah": None},
            {"Keterangan": label("101"), "Jumlah": aset},
            {"Keterangan": "TOTAL ASET", "Jumlah": aset},
            {"Keterangan": "KEWAJIBAN", "Jumlah": None},
            {"Keterangan": label("201"), "Jumlah": kewajiban},
            {"Keterangan": "EKUITAS", "Jumlah": None},
            {"Keterangan": label("301"), "Jumlah": modal},
            {"Keterangan": "Laba (rugi) berjalan", "Jumlah": laba},
            {"Keterangan": "TOTAL KEWAJIBAN + EKUITAS", "Jumlah": total_pasiva},
        ]))
        if aset == total_pasiva:
            st.success("Neraca seimbang: total aset sama dengan total kewajiban + ekuitas.")
        else:
            st.error(f"Neraca tidak seimbang. Selisih {rupiah(aset - total_pasiva)}.")
