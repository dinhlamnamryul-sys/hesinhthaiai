# Home.py (phiên bản cập nhật: box-container, audio toggle, visit_count)
import streamlit as st
import os
import base64

# --- CẤU HÌNH LOGO VÀ ẢNH NỀN ---
LOGO_PATH = "image_2.png.png"  # kiểm tra tên file logo (local)
LOGO_URL_ONLINE = "https://cdn-icons-png.flaticon.com/512/2997/2997235.png"
BACKGROUND_IMAGE_PATH = "bantrang.jpg"  # file ảnh nền (nếu có)
MUSIC_FILE = "nhac_nen.mp3"  # file nhạc local (nếu có) — điều chỉnh tên ở đây

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

# --- TĂNG visit_count mỗi lần load trang ---
if 'visit_count' not in st.session_state:
    st.session_state.visit_count = 0
st.session_state.visit_count += 1

# --- CSS GIAO DIỆN (BASE64 safe) ---
st.markdown(f"""
<style>
    /* ỨNG DỤNG NỀN */
    .stApp {{
        {"background-image: url(data:image/jpg;base64," + base64_image + ");" if base64_image else "background-color: #f0f2f6;"}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* ẨN HEADER STREAMLIT */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{
        display: none !important;
    }}

    /* SIDEBAR */
    [data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(4px);
        border-right: 4px solid #b71c1c;
        padding-top: 18px;
    }}

    /* KHUNG CHỨA CARD (ô vuông lớn) */
    .box-container {{
        background: rgba(255,255,255,0.86);
        padding: 28px;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.14);
        margin: 20px auto 24px auto;
        width: 95%;
    }}

    /* FEATURE CARD */
    .feature-card {{
        background: rgba(255,255,255,0.94);
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #e6e6e6;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: flex-start;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .feature-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 12px 26px rgba(183,28,28,0.18);
        border-color: #ff6f00;
    }}
    .icon-box {{
        font-size: 3.8rem;
        margin-bottom: 8px;
        text-align: left;
    }}
    .card-title {{
        color: #d84315;
        font-weight: 800;
        font-size: 1.4rem;
        margin-bottom: 6px;
    }}
    .card-desc {{ color: #555; }}

    /* NÚT LINK (dùng st.page_link hiển thị) */
    .link-btn {{
        width: 100%;
        border-radius: 28px;
        padding: 8px 12px;
        text-align: center;
        font-weight: 700;
    }}

    /* AUDIO */
    audio {{
        width: 60%;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    }}

    /* FOOTER */
    .footer {{
        width: 100%;
        padding: 12px;
        background: rgba(255,255,255,0.9);
        border-top: 3px solid #b71c1c;
        text-align: center;
        font-size: 13px;
        margin-top: 10px;
    }}

    /* Responsive nhỏ */
    @media (max-width: 900px) {{
        .box-container {{ width: 98%; padding: 16px; }}
        .feature-card {{ height: auto; padding: 16px; }}
        audio {{ width: 100%; }}
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
        st.image(sidebar_logo, width=140)
    st.markdown("<h3 style='text-align: center; color: #b71c1c; margin-top: 6px;'>TRƯỜNG PTDTBT<br>TH&THCS NA Ư</h3>", unsafe_allow_html=True)
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
    st.success(f"👥 Lượt truy cập: **{st.session_state.visit_count}**")

# --- NỘI DUNG TRANG CHÍNH ---
st.markdown("""
<div class="main-header" style="text-align:center; margin-top: 6px;">
    <h1 style="color: #fff; text-shadow: 1px 1px 6px rgba(0,0,0,0.6);">🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h4 style="color: #ffe082; margin-top: 4px;">"Tri thức vùng cao - Vươn xa thế giới"</h4>
</div>
""", unsafe_allow_html=True)

# --- AUDIO: cho phép bật/tắt bởi user ---
st.markdown('<div style="text-align:center; margin-top: 8px;">', unsafe_allow_html=True)
col_a1, col_a2, col_a3 = st.columns([1, 2, 1])
with col_a2:
    play_music = st.checkbox("🔊 Bật nhạc nền", value=False)
    if play_music:
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:18px;">
            <audio controls autoplay>
                {audio_source_html}
                Trình duyệt không hỗ trợ audio.
            </audio>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- BOX CONTAINER chứa 4 CARD (ô vuông) ---
st.markdown('<div class="box-container">', unsafe_allow_html=True)

cols = st.columns(4)
# Card 1
with cols[0]:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="icon-box">🏔️</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Gia Sư Toán AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-desc">Học toán song ngữ thông minh.</div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_1):
        st.markdown("<br>", unsafe_allow_html=True)
        st.page_link(PAGE_1, label="Học ngay ➜", icon="📝", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Card 2
with cols[1]:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="icon-box">⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Sinh Đề Tự Động</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-desc">Tạo đề kiểm tra cực nhanh.</div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_2):
        st.markdown("<br>", unsafe_allow_html=True)
        st.page_link(PAGE_2, label="Tạo đề ➜", icon="🚀", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Card 3
with cols[2]:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="icon-box">🧿</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Giải Bài Tập Từ Ảnh</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-desc">AI phân tích & giải tức thì.</div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_3):
        st.markdown("<br>", unsafe_allow_html=True)
        st.page_link(PAGE_3, label="Giải ngay ➜", icon="📸", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Card 4
with cols[3]:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="icon-box">📽️</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Đa Phương Tiện</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-desc">Học liệu văn hoá H\'Mông.</div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_4):
        st.markdown("<br>", unsafe_allow_html=True)
        st.page_link(PAGE_4, label="Khám phá ➜", icon="🎧", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <p>👨‍🏫 <b>Nhóm tác giả:</b> Trường PTDTBT TH&THCS Na Ư</p>
    <p style="font-size: 12px; color: #fff; opacity: 0.9;">© 2025 Cổng Giáo Dục Số Na Ư</p>
</div>
""", unsafe_allow_html=True)
