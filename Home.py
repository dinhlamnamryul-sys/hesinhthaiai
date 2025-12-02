import streamlit as st
import os
import base64

# --- 0. CÁC HÀM TIỆN ÍCH (Khởi tạo trước khi Cấu hình Trang) ---
def get_base64_image(image_path):
    """Đọc file ảnh local và mã hóa thành chuỗi Base64"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

def get_audio_html(file_path):
    """Hàm đọc file nhạc local và chuyển sang mã HTML để phát"""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
    else:
        # Link dự phòng nếu chưa có file nhạc
        fallback_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        return f'<source src="{fallback_url}" type="audio/mp3">'

# --- 0.1. XỬ LÝ FILE (Thực hiện nhanh chóng) ---
LOGO_PATH = "image_2.png.png"
LOGO_URL_ONLINE = "https://cdn-icons-png.flaticon.com/512/2997/2997235.png"
HEADER_IMAGE_PATH = "bantrang.jpg" 
MUSIC_FILE = "nhac_nen.mp3"

base64_image = get_base64_image(HEADER_IMAGE_PATH)
audio_source_html = get_audio_html(MUSIC_FILE)

if os.path.exists(LOGO_PATH):
    app_icon = LOGO_PATH
    sidebar_logo = LOGO_PATH
else:
    app_icon = LOGO_URL_ONLINE
    sidebar_logo = LOGO_URL_ONLINE

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Cổng Giáo Dục Số - Trường Na Ư",
    page_icon=app_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. TẠO CSS CHO HEADER DỰA TRÊN VIỆC CÓ ẢNH NỀN HAY KHÔNG ---
if base64_image:
    header_css = f"""
    .main-header {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white; 
        padding: 40px; 
        border-radius: 20px; 
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4); 
        border-bottom: 6px solid #fdd835;
        margin-bottom: 20px; 
        margin-top: -20px;
        position: relative;
        overflow: hidden;
    }}
    .main-header h1, .main-header h3 {{
        z-index: 10; 
        position: relative;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7); 
    }}
    """
else:
    header_css = """
    .main-header {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 60%, #ff6f00 100%);
        color: white; padding: 30px; border-radius: 20px; text-align: center;
        box-shadow: 0 10px 30px rgba(183, 28, 28, 0.4); border-bottom: 6px solid #fdd835;
        margin-bottom: 20px; margin-top: -20px;
    }
    """

# --- 2.1. CHÈN CSS GIAO DIỆN CHUNG & TÙY CHỈNH CARD 3D ---
st.markdown(f"""
<style>
    {header_css}
    [data-testid="stHeader"] {{ background-color: rgba(0,0,0,0); color: transparent; }}
    [data-testid="stToolbar"] {{ visibility: hidden !important; display: none !important; }}
    [data-testid="stDecoration"] {{ visibility: hidden !important; display: none !important; }}
    [data-testid="stSidebarCollapsedControl"] {{
        visibility: visible !important; display: block !important;
        color: #b71c1c !important; background-color: white; border-radius: 50%;
        padding: 5px; z-index: 999999;
    }}
    .stApp {{ background-color: #f8f9fa; margin-bottom: 60px; }}
    .main-header h1 {{ font-size: 2.5rem; font-weight: 900; margin: 0; }}
    
    /* ------------------------------------- */
    /* CSS CHO HIỆU ỨNG 3D VÀ MÀU SẮC RỰC RỠ */
    /* ------------------------------------- */
    .feature-card {{
        /* Cấu hình cơ bản */
        padding: 30px; /* Tăng padding để rộng rãi hơn */
        border-radius: 25px; /* Bo tròn hơn */
        text-align: center;
        height: 350px; 
        display: flex; flex-direction: column; justify-content: space-between;
        transition: all 0.4s ease-in-out;
        position: relative; /* Quan trọng cho hiệu ứng 3D */
        transform: translateY(0);
        
        /* Hiệu ứng nổi lên nhẹ khi hover */
    }}
    .feature-card:hover {{ 
        transform: translateY(-8px) rotateX(2deg); 
        z-index: 10;
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
    }}
    
    /* Thiết lập lại màu chữ cho nội dung p trong card */
    .feature-card p {{ color: #444; font-size: 0.95rem; }}

    /* Màu sắc và hiệu ứng 3D chi tiết cho từng card */
    
    /* 1. Gia Sư Toán AI (Màu Vàng/Cam) */
    .card-math {{
        background: linear-gradient(145deg, #ffc107, #ff9800); 
        border: 1px solid #ffb300;
        box-shadow: 
            0 10px 0 #ff6f00, /* Màu dưới cùng (3D bottom) */
            0 10px 20px rgba(0,0,0,0.15); /* Bóng đổ chung */
    }}
    .card-math:hover {{
        box-shadow: 
            0 10px 0 #ff6f00, 
            0 20px 40px rgba(0,0,0,0.3);
    }}
    .card-math .card-title {{ color: #e65100; font-weight: 900; }}

    /* 2. Sinh Đề Tốc Độ (Màu Xanh Lá Cây) */
    .card-quiz {{
        background: linear-gradient(145deg, #8bc34a, #689f38); 
        border: 1px solid #7cb342;
        box-shadow: 
            0 10px 0 #33691e, /* Màu dưới cùng (3D bottom) */
            0 10px 20px rgba(0,0,0,0.15); 
    }}
    .card-quiz:hover {{
        box-shadow: 
            0 10px 0 #33691e, 
            0 20px 40px rgba(0,0,0,0.3);
    }}
    .card-quiz .card-title {{ color: #1b5e20; font-weight: 900; }}

    /* 3. Giải bài tập từ ảnh (Màu Xanh Dương) */
    .card-image {{
        background: linear-gradient(145deg, #4fc3f7, #29b6f6); 
        border: 1px solid #03a9f4;
        box-shadow: 
            0 10px 0 #0277bd, /* Màu dưới cùng (3D bottom) */
            0 10px 20px rgba(0,0,0,0.15); 
    }}
    .card-image:hover {{
        box-shadow: 
            0 10px 0 #0277bd, 
            0 20px 40px rgba(0,0,0,0.3);
    }}
    .card-image .card-title {{ color: #01579b; font-weight: 900; }}
    
    /* 4. Đa Phương Tiện (Màu Đỏ/Hồng) */
    .card-media {{
        background: linear-gradient(145deg, #ff8a65, #ff5722); 
        border: 1px solid #ff7043;
        box-shadow: 
            0 10px 0 #bf360c, /* Màu dưới cùng (3D bottom) */
            0 10px 20px rgba(0,0,0,0.15); 
    }}
    .card-media:hover {{
        box-shadow: 
            0 10px 0 #bf360c, 
            0 20px 40px rgba(0,0,0,0.3);
    }}
    .card-media .card-title {{ color: #880e4f; font-weight: 900; }}

    
    /* Các thành phần chung khác */
    .icon-box {{ font-size: 3.5rem; margin-bottom: 10px; }}
    
    .stButton>button {{
        width: 100%; border-radius: 50px; background: linear-gradient(90deg, #ff6f00, #ffca28);
        border: none; color: white; font-weight: bold; padding: 10px 0;
        transform: translateY(0); transition: transform 0.2s;
    }}
    .stButton>button:hover {{ transform: scale(1.05); background: linear-gradient(90deg, #ff9800, #ffc107); }}
    
    .footer {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #fff; color: #555; text-align: center;
        padding: 10px; font-size: 14px; border-top: 3px solid #b71c1c;
        z-index: 999; box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }}
    .footer p {{ margin: 0; font-family: sans-serif; line-height: 1.5; }}
    
    /* CSS cho trình phát nhạc */
    audio {{
        width: 60%;
        border-radius: 30px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
</style>
""", unsafe_allow_html=True)

# Khối CSS chạy chữ TÁCH BIỆT 
st.markdown("""
<style>
    /* CSS MỚI: Chữ chạy ngang (Marquee effect) */
    .running-text-container {
        overflow: hidden; 
        background-color: #ffffff; 
        color: #b71c1c; 
        font-weight: bold;
        padding: 8px 0; 
        margin-bottom: 10px; 
        border-bottom: 2px solid #ff9800;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .running-text {
        display: inline-block;
        white-space: nowrap;
        font-size: 1.2rem; 
        animation: marquee 30s linear infinite; 
    }
    @keyframes marquee {
        0%   { transform: translate(100%, 0); }
        100% { transform: translate(-100%, 0); }
    }
</style>
""", unsafe_allow_html=True)

# --- KHAI BÁO FILE TRANG ---
PAGE_1 = "pages/1_Gia_Sư_Toán_AI.py"
PAGE_2 = "pages/2_Sinh_Đề_Tự_Động.py"
PAGE_3 = "pages/3_Giải_bài_tập_từ_ảnh.py"
PAGE_4 = "pages/4_Học_liệu_đa_phương_tiện.py"
PAGE_5 = "pages/5_Văn_hóa_cội_nguồn.py"


# --- 3. MENU BÊN TRÁI ---
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
    
    # ĐÃ SỬA: Khởi tạo Lượt truy cập từ 500
    if 'visit_count' not in st.session_state:
        st.session_state.visit_count = 500 
    
    # Tăng lượt truy cập lên 1 mỗi khi trang được load/rerun
    st.session_state.visit_count += 1 

    st.success(f"👥 Lượt truy cập: **{st.session_state.visit_count}**")

# --- 4. NỘI DUNG TRANG CHÍNH ---

# CHÈN DÒNG CHỮ CHẠY
st.markdown("""
<div class="running-text-container">
    <div class="running-text">
        📢 Xin chào quý thầy cô và các em học sinh, chào mừng đến với Cổng Giáo Dục Số Na Ư! Chúc mọi người một ngày học tập và làm việc hiệu quả! 
    </div>
</div>
""", unsafe_allow_html=True)

# HEADER CHÍNH
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>"Tri thức vùng cao - Vươn xa thế giới"</h3>
</div>
""", unsafe_allow_html=True)

# --- THANH NHẠC H'MÔNG ---
st.markdown(f"""
<div style="text-align:center; margin-bottom:30px;">
<h4 style="color: #555;">🎵 Giai điệu bản Mông</h4>
<audio controls autoplay>
    {audio_source_html}
    Trình duyệt của bạn không hỗ trợ audio.
</audio>
</div>
""", unsafe_allow_html=True)

# --- CARD CHỨC NĂNG (ĐÃ CÓ HIỆU ỨNG 3D) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Card 1: Gia Sư Toán AI (Vàng/Cam)
    st.markdown('<div class="feature-card card-math"><div class="icon-box">🏔️</div><div class="card-title">Gia Sư Toán AI</div><p>Học toán song ngữ.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_1):
        st.page_link(PAGE_1, label="Học ngay ➜", icon="📝", use_container_width=True)

with col2:
    # Card 2: Sinh Đề Tốc Độ (Xanh Lá)
    st.markdown('<div class="feature-card card-quiz"><div class="icon-box">⚡</div><div class="card-title">Sinh Đề Tốc Độ</div><p>Tạo đề trắc nghiệm trong vài giây.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_2):
        st.page_link(PAGE_2, label="Tạo đề ➜", icon="🚀", use_container_width=True)

with col3:
    # Card 3: Giải bài tập từ ảnh (Xanh Dương)
    st.markdown('<div class="feature-card card-image"><div class="icon-box">🧿</div><div class="card-title">Giải bài tập từ ảnh</div><p>Giải bài mọi môn học bằng AI.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_3):
        st.page_link(PAGE_3, label="Giải ngay ➜", icon="📸", use_container_width=True)

with col4:
    # Card 4: Đa Phương Tiện (Đỏ)
    st.markdown('<div class="feature-card card-media"><div class="icon-box">📽️</div><div class="card-title">Đa Phương Tiện</div><p>Học liệu văn hóa H\'Mông.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_4):
        st.page_link(PAGE_4, label="Khám phá ➜", icon="🎧", use_container_width=True)

# --- 5. CHÂN TRANG (FOOTER) ---
st.markdown("""
<div class="footer">
    <p>👨‍🏫 <b>Nhóm tác giả:</b> Trường PTDTBT TH&THCS Na Ư</p>
    <p style="font-size: 12px; color: #888;">© 2025 Cổng Giáo Dục Số Na Ư</p>
</div>
""", unsafe_allow_html=True)
