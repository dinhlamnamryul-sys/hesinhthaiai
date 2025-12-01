# Home.py (phiên bản sửa lỗi NameError & sắp xếp đúng thứ tự)
import streamlit as st
import os
import base64

# --- CẤU HÌNH LOGO VÀ ẢNH NỀN ---
LOGO_PATH = "image_2.png.png"  # kiểm tra tên file logo
LOGO_URL_ONLINE = "https://cdn-icons-png.flaticon.com/512/2997/2997235.png"
BACKGROUND_IMAGE_PATH = "bantrang.jpg"  # file ảnh nền (nếu có)
MUSIC_FILE = "nhac_nen.mp3"  # file nhạc local (nếu có)

# --- HÀM TIỆN ÍCH ---
def get_base64_image(image_path):
    """Chuyển ảnh local thành Base64 để nhúng vào CSS"""
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            return ""
    return ""

def get_audio_html(file_path):
    """Trả về <source> cho thẻ audio, ưu tiên file local, fallback link online"""
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            return f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
        except Exception:
            pass
    # fallback url nếu không có file
    fallback_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    return f'<source src="{fallback_url}" type="audio/mp3">'

# --- TẠO BIẾN TRƯỚC KHI SỬ DỤNG TRONG F-STRING (RẤT QUAN TRỌNG) ---
base64_image = get_base64_image(BACKGROUND_IMAGE_PATH)
audio_source_html = get_audio_html(MUSIC_FILE)

# --- CHỌN ICON/LOGO HIỆN HỮU ---
if os.path.exists(LOGO_PATH):
    app_icon = LOGO_PATH
    sidebar_logo = LOGO_PATH
else:
    app_icon = LOGO_URL_ONLINE
    sidebar_logo = LOGO_URL_ONLINE

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Cổng Giáo Dục Số - Trường Na Ư",
    page_icon=app_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS (an toàn vì base64_image đã có giá trị rồi) ---
st.markdown(f"""
<style>

    /* ===== NỀN ỨNG DỤNG ===== */
    .stApp {{
        {"background-image: url(data:image/jpg;base64," + base64_image + ");" if base64_image else "background-color: #f0f2f6;"}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* ===== ẨN HEADER STREAMLIT ===== */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{
        display: none !important;
    }}

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.75);
        backdrop-filter: blur(4px);
        border-right: 4px solid #b71c1c;
    }}

    /* ===== HEADER CHÍNH ===== */
    .main-header {{
        background: rgba(183, 28, 28, 0.85);
        margin: 10px auto 20px auto;
        width: 70%;
        padding: 18px 10px;
        text-align: center;
        border-radius: 18px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
        border-bottom: 3px solid #ffd54f;
    }}
    .main-header h1 {{
        font-size: 2.4rem;
        color: white;
        margin: 0;
        font-weight: 900;
    }}
    .main-header h3 {{
        margin-top: 6px;
        color: #ffe082;
    }}

    /* ===== CARD CHỨC NĂNG ===== */
    .feature-card {{
        background: rgba(255,255,255,0.92);
        padding: 20px;
        border-radius: 22px;
        border: 2px solid #e0e0e0;
        height: 340px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        transition: 0.25s;
        backdrop-filter: blur(3px);
    }}
    .feature-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 14px 28px rgba(183,28,28,0.35);
        border-color: #e65100;
    }}

    .icon-box {{
        font-size: 4.2rem;
        margin-bottom: 8px;
    }}
    .card-title {{
        font-size: 1.45rem;
        font-weight: 800;
        color: #d84315;
        margin-bottom: 8px;
    }}

    /* ===== NÚT ===== */
    .stButton>button {{
        width: 100%;
        border-radius: 35px;
        padding: 10px 0;
        font-weight: 700;
        background: linear-gradient(90deg, #ff6f00, #ffca28);
        border: none;
        box-shadow: 0 4px 12px rgba(255,167,38,0.45);
        transition: 0.25s;
    }}
    .stButton>button:hover {{
        transform: scale(1.05);
    }}

    /* ===== AUDIO ===== */
    audio {{
        width: 45%;
        border-radius: 20px;
        box-shadow: 0 5px 18px rgba(0,0,0,0.25);
    }}

    /* ===== FOOTER ===== */
    .footer {{
        width: 100%;
        padding: 8px;
        background: rgba(255,255,255,0.9);
        border-top: 3px solid #b71c1c;
        text-align: center;
        font-size: 13px;
        margin-top: 30px;
    }}
</style>
""", unsafe_allow_html=True)

# --- KHAI BÁO FILE TRANG (nếu bạn dùng pages) ---
PAGE_1 = "pages/1_Gia_Sư_Toán_AI.py"
PAGE_2 = "pages/2_Sinh_Đề_Tự_Động.py"
PAGE_3 = "pages/3_Giải_bài_tập_từ_ảnh.py"
PAGE_4 = "pages/4_Học_liệu_đa_phương_tiện.py"
PAGE_5 = "pages/5_Văn_hóa_cội_nguồn.py"

# --- SIDEBAR ---
with st.sidebar:
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2:
        st.image(sidebar_logo, width=150)

    st.markdown("<h3 style='text-align: center; color: #b71c1c; margin-top: 10px;'>TRƯỜNG PTDTBT<br>TH&THCS NA Ư</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🚀 Menu Chức Năng")

    if st.button("🏠 Trang Chủ"):
        st.rerun()
    if os.path.exists(PAGE_1):
        st.page_link(PAGE_1, label="Gia Sư Toán AI", icon="🏔️")
    if os.path.exists(PAGE_2):
        st.page_link(PAGE_2, label="Sinh Đề Tự Động", icon="⚡")
    if os.path.exists(PAGE_3):
        st.page_link(PAGE_3, label="Giải bài tập từ ảnh", icon="🧿")
    if os.path.exists(PAGE_4):
        st.page_link(PAGE_4, label="Học liệu đa phương tiện", icon="📽️")
    if os.path.exists(PAGE_5):
        st.page_link(PAGE_5, label="Văn hóa cội nguồn", icon="🌽")

    st.markdown("---")
    if 'visit_count' not in st.session_state:
        st.session_state.visit_count = 0
    st.success(f"👥 Lượt truy cập: **{st.session_state.visit_count}**")

# --- NỘI DUNG TRANG CHÍNH ---
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>"Tri thức vùng cao - Vươn xa thế giới"</h3>
</div>
""", unsafe_allow_html=True)

# --- THANH NHẠC ---
st.markdown(f"""
<div style="text-align:center; margin-top: -5px; margin-bottom:20px;">
<h4 style="color:#333;">🎵 Giai điệu bản Mông</h4>
<audio controls autoplay>
    {audio_source_html}
    Trình duyệt của bạn không hỗ trợ audio.
</audio>
</div>
""", unsafe_allow_html=True)

# --- CARDS CHỨC NĂNG ---
col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    st.markdown('<div class="feature-card"><div class="icon-box">🏔️</div><div class="card-title">Gia Sư Toán AI</div><p>Học toán song ngữ thông minh.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_1):
        st.page_link(PAGE_1, label="Học ngay ➜", icon="📝", use_container_width=True)

with col2:
    st.markdown('<div class="feature-card"><div class="icon-box">⚡</div><div class="card-title">Sinh Đề Tự Động</div><p>Tạo đề kiểm tra cực nhanh.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_2):
        st.page_link(PAGE_2, label="Tạo đề ➜", icon="🚀", use_container_width=True)

with col3:
    st.markdown('<div class="feature-card"><div class="icon-box">🧿</div><div class="card-title">Giải Bài Tập Từ Ảnh</div><p>AI phân tích & giải tức thì.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_3):
        st.page_link(PAGE_3, label="Giải ngay ➜", icon="📸", use_container_width=True)

with col4:
    st.markdown('<div class="feature-card"><div class="icon-box">📽️</div><div class="card-title">Đa Phương Tiện</div><p>Học liệu văn hoá H\'Mông.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_4):
        st.page_link(PAGE_4, label="Khám phá ➜", icon="🎧", use_container_width=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <p>👨‍🏫 <b>Nhóm tác giả:</b> Trường PTDTBT TH&THCS Na Ư</p>
    <p style="font-size: 12px; color: #888;">© 2025 Cổng Giáo Dục Số Na Ư</p>
</div>
""", unsafe_allow_html=True)
