# Home.py – Phiên bản card chuẩn + nhạc giữ nguyên + không lỗi NameError
import streamlit as st
import os
import base64

# --- CẤU HÌNH FILE ---
LOGO = "image_2.png.png"
BACKGROUND = "bantrang.jpg"
MUSIC = "nhac_nen.mp3"

# -----------------------------------------
# HÀM TIỆN ÍCH
# -----------------------------------------
def load_base64(path):
    if os.path.exists(path):
        try:
            return base64.b64encode(open(path, "rb").read()).decode()
        except:
            return ""
    return ""

def load_audio(path):
    """Nhạc local → base64, fallback khi thiếu"""
    if os.path.exists(path):
        try:
            raw = open(path, "rb").read()
            b64 = base64.b64encode(raw).decode()
            return f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
        except:
            pass
    return '<source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">'


# -----------------------------------------
# TẠO BIẾN TRƯỚC F-STRING
# -----------------------------------------
bg64 = load_base64(BACKGROUND)
audio_html = load_audio(MUSIC)

app_icon = LOGO if os.path.exists(LOGO) else "https://cdn-icons-png.flaticon.com/512/2997/2997235.png"


# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="Cổng Giáo Dục Số Na Ư",
    page_icon=app_icon,
    layout="wide"
)

# -----------------------------------------
# CSS (Đã thêm CSS cho liên kết)
# -----------------------------------------
st.markdown(f"""
<style>
.stApp {{
    {"background-image: url(data:image/jpg;base64," + bg64 + ");" if bg64 else ""}
    background-size: cover;
    background-attachment: fixed;
}}

/* GIẤU HEADER */
[data-testid="stHeader"], [data-testid="stToolbar"] {{
    display: none;
}}

.main-header {{
    width: 80%;
    margin: 20px auto;
    background: rgba(183,28,28,0.85);
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    color: white;
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
}}

.box-row {{
    display: flex;
    gap: 25px;
    justify-content: center;
    margin-top: 40px;
}}

.feature {{
    width: 270px;
    height: 330px;
    background: rgba(255,255,255,0.93);
    border-radius: 20px;
    padding: 15px;
    text-align: center;
    border: 2px solid #ffccbc;
    transition: 0.25s;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}
.feature:hover {{
    transform: translateY(-8px);
    border-color: #e65100;
    box-shadow: 0 8px 22px rgba(0,0,0,0.2);
    cursor: pointer; /* Thêm con trỏ để chỉ ra có thể nhấp chuột */
}}

/* CSS MỚI: Đảm bảo liên kết không bị gạch chân và thừa hưởng màu */
.box-row a {{
    text-decoration: none !important;
    color: inherit;
}}

.icon {{
    font-size: 55px;
    margin-bottom: 5px;
}}
.title {{
    font-size: 22px;
    font-weight: 800;
    color: #d84315;
    margin-bottom: 6px;
}}

.desc {{
    font-size: 15px;
    color: #444;
    margin-bottom: 15px;
}}

.footer {{
    margin-top: 45px;
    width: 100%;
    text-align: center;
    background: rgba(255,255,255,0.92);
    padding: 12px;
    border-top: 3px solid #b71c1c;
    color: #444;
}}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# SIDEBAR
# -----------------------------------------
with st.sidebar:
    st.image(app_icon, width=150)
    st.markdown("<h3 style='text-align:center;'>TRƯỜNG PTDTBT<br>TH&THCS NA Ư</h3>", unsafe_allow_html=True)
    st.markdown("---")

    st.page_link("Home.py", label="🏠 Trang chủ")

    pages = [
        ("pages/1_Gia_Sư_Toán_AI.py", "🏔️  Gia Sư Toán AI"),
        ("pages/2_Sinh_Đề_Tự_Động.py", "⚡  Sinh Đề Tự Động"),
        ("pages/3_Giải_bài_tập_từ_ảnh.py", "🧿  Giải Bài Tập Từ Ảnh"),
        ("pages/4_Học_liệu_đa_phương_tiện.py", "📽️  Học Liệu Đa Phương Tiện"),
    ]

    for p, label in pages:
        if os.path.exists(p):
            st.page_link(p, label=label)

    st.markdown("---")
    st.info("👥 Lượt truy cập: **1**")


# -----------------------------------------
# HEADER
# -----------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>Tri thức vùng cao – Vươn xa thế giới</h3>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------
# NHẠC NỀN
# -----------------------------------------
st.markdown(f"""
<div style='text-align:center;'>
<h4>🎵 Giai điệu bản Mông</h4>
<audio controls autoplay>
    {audio_html}
</audio>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------
# 4 Ô VUÔNG CHỨC NĂNG (Đã cập nhật hàm card)
# -----------------------------------------
st.markdown('<div class="box-row">', unsafe_allow_html=True)

def card(icon, title, desc, page):
    # Kiểm tra sự tồn tại của file và tạo đường dẫn tương đối cho Streamlit
    # Đường dẫn cần là tuyệt đối hoặc tương đối: /pages/1_Gia_Sư_Toán_AI.py
    page_url = f"/{page}" if os.path.exists(page) else "#"
    
    st.markdown(f"""
    <a href="{page_url}" style="text-decoration:none; color:inherit;">
        <div class="feature">
            <div class="icon">{icon}</div>
            <div class="title">{title}</div>
            <div class="desc">{desc}</div>
        </div>
    </a>
    """, unsafe_allow_html=True)
    # Đã loại bỏ st.page_link riêng biệt.

col1, col2, col3, col4 = st.columns(4)

with col1:
    card("🏔️", "Gia Sư Toán AI", "Học toán song ngữ thông minh.", "pages/1_Gia_Sư_Toán_AI.py")

with col2:
    card("⚡", "Sinh Đề Tự Động", "Tạo đề kiểm tra cực nhanh.", "pages/2_Sinh_Đề_Tự_Động.py")

with col3:
    card("🧿", "Giải Bài Tập Từ Ảnh", "AI phân tích & giải tức thì.", "pages/3_Giải_bài_tập_từ_ảnh.py")

with col4:
    card("📽️", "Đa Phương Tiện", "Học liệu văn hóa H'Mông.", "pages/4_Học_liệu_đa_phương_tiện.py")

st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------
# FOOTER
# -----------------------------------------
st.markdown("""
<div class='footer'>
    <p>👨‍🏫 Nhóm tác giả: Trường PTDTBT TH&THCS Na Ư</p>
    <p style='font-size:12px;color:#555;'>© 2025 Cổng Giáo Dục Số Na Ư</p>
</div>
""", unsafe_allow_html=True)
