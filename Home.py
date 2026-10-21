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

# --- HÀM MỚI: XỬ LÝ ĐẾM LƯỢT TRUY CẬP TOÀN CỤC ---
def update_global_visit_count():
    count_file = "visit_count.txt"
    
    # 1. Đọc số hiện tại từ file, nếu chưa có file thì tạo mới bắt đầu từ 500
    if not os.path.exists(count_file):
        current_count = 500
        with open(count_file, "w") as f:
            f.write(str(current_count))
    else:
        with open(count_file, "r") as f:
            try:
                current_count = int(f.read())
            except:
                current_count = 500

    # 2. Logic tăng đếm: Chỉ tăng nếu phiên làm việc này chưa được đếm (tránh F5 liên tục bị tăng ảo)
    if 'has_counted' not in st.session_state:
        current_count += 1
        st.session_state.has_counted = True # Đánh dấu người này đã được đếm
        # Lưu số mới vào file
        with open(count_file, "w") as f:
            f.write(str(current_count))
            
    return current_count

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
    page_title="Hệ thống Trợ lý Giáo dục AI Sam Mứn",
    page_icon=app_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. TẠO CSS CHO HEADER DỰA TRÊN VIỆC CÓ ẢNH NỀN HAY KHÔNG ---
# [ĐIỀU CHỈNH QUAN TRỌNG]: Thay đổi độ mờ lớp phủ để ảnh nét hơn
if base64_image:
    header_css = f"""
    .main-header {{
        /* Giảm độ tối từ 0.6 xuống 0.2 để ảnh gốc hiện rõ nét như thật */
        background-image: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)), url("data:image/jpg;base64,{base64_image}");
        background-size: cover; /* Đảm bảo ảnh phủ kín khung */
        background-position: center center; /* Căn giữa ảnh để lấy trọng tâm */
        background-repeat: no-repeat;
        color: white; 
        padding: 60px 20px; 
        border-radius: 25px; 
        text-align: center;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5); 
        border-bottom: 8px solid #fdd835;
        margin-bottom: 30px; 
        margin-top: -20px;
        position: relative;
        overflow: hidden;
    }}
    .main-header h1 {{
        z-index: 10; 
        position: relative;
        /* Tăng đổ bóng cho chữ để đọc rõ trên nền ảnh sáng */
        text-shadow: 3px 3px 8px #000000; 
        font-size: 3.5rem !important;
    }}
    .main-header h3 {{
        z-index: 10; 
        position: relative;
        text-shadow: 2px 2px 6px #000000; 
        font-weight: 600;
        background-color: rgba(0,0,0,0.3); /* Thêm nền mờ nhẹ riêng cho dòng slogan */
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
    }}
    """
else:
    header_css = """
    .main-header {
        background: linear-gradient(135deg, #b71c1c 0%, #ff6f00 100%);
        color: white; padding: 50px; border-radius: 25px; text-align: center;
        box-shadow: 0 15px 40px rgba(183, 28, 28, 0.5); border-bottom: 8px solid #fdd835;
        margin-bottom: 30px; margin-top: -20px;
    }
    """

# --- 2.1. CHÈN CSS GIAO DIỆN CHUNG & TÙY CHỈNH CARD NEUMORPHISM ---
st.markdown(f"""
<style>
    {header_css}
    
    /* Thiết lập nền chung */
    .stApp {{ background-color: #ecf0f3; /* Nền Neumorphism */ margin-bottom: 60px; }}
    .main-header h1 {{ font-size: 3rem; font-weight: 900; margin: 0; }}

    /* Ẩn các thanh mặc định của Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{ 
        background-color: transparent !important; color: transparent !important; 
    }}
    
    /* Nút mở Sidebar */
    [data-testid="stSidebarCollapsedControl"] {{
        color: #b71c1c !important; background-color: #ecf0f3; border-radius: 50%;
        box-shadow: 5px 5px 10px #bec3c7, -5px -5px 10px #ffffff;
        padding: 5px; z-index: 999999;
    }}
    
    /* ------------------------------------- */
    /* CSS CHO HIỆU ỨNG NEUMORPHISM (WOW EFFECT) */
    /* ------------------------------------- */
    .feature-card {{
        /* Cấu hình Neumorphism cơ bản */
        background: #ecf0f3;
        padding: 35px 20px; 
        border-radius: 25px; 
        text-align: center;
        height: 380px; /* Tăng chiều cao để thoáng hơn */
        display: flex; flex-direction: column; justify-content: space-between;
        transition: all 0.5s ease-in-out;
        position: relative; 
        
        /* Hiệu ứng Neumorphism nổi nhẹ */
        box-shadow: 8px 8px 15px #bec3c7, -8px -8px 15px #ffffff;
        border: 1px solid rgba(255,255,255,0.8);
    }}
    .feature-card:hover {{ 
        /* Hiệu ứng Pressed/Inset khi hover */
        transform: scale(1.02); 
        cursor: pointer;
        box-shadow: inset 5px 5px 10px #bec3c7, inset -5px -5px 10px #ffffff;
    }}
    
    .icon-box {{ font-size: 4rem; margin-bottom: 15px; text-shadow: 2px 2px 5px rgba(0,0,0,0.1); }}
    .card-title {{ font-weight: 900; font-size: 1.6rem; margin-bottom: 5px; text-transform: uppercase; }}
    .feature-card p {{ color: #666; font-size: 1rem; line-height: 1.5; }}


    /* Màu sắc Gradient cho từng card */
    
    /* 1. Gia Sư Toán AI (Golden Orange) */
    .card-math .card-title {{ 
        background: linear-gradient(45deg, #ffc107, #ff6f00); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
    }}

    /* 2. Sinh Đề Tốc Độ (Electric Blue) */
    .card-quiz .card-title {{ 
        background: linear-gradient(45deg, #00d4ff, #007bff); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
    }}

    /* 3. Giải bài tập từ ảnh (Vibrant Green) */
    .card-image .card-title {{ 
        background: linear-gradient(45deg, #4ef91c, #1f9403); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
    }}
    
    /* 4. Học Liệu Đa Phương Tiện (Crimson Red) */
    .card-media .card-title {{ 
        background: linear-gradient(45deg, #ff3d00, #b71c1c); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
    }}

    
    /* Nút hành động nổi bật */
    .stButton>button {{
        width: 100%; border-radius: 50px; 
        background: linear-gradient(90deg, #ff6f00, #ffca28);
        border: none; color: white; font-weight: bold; padding: 12px 0;
        box-shadow: 4px 4px 8px #d1d9e6, -4px -4px 8px #ffffff;
        transform: translateY(0); transition: all 0.3s;
    }}
    .stButton>button:hover {{ 
        transform: translateY(-2px); 
        box-shadow: 6px 6px 12px #d1d9e6, -6px -6px 12px #ffffff;
        background: linear-gradient(90deg, #ff9800, #ffc107); 
    }}
    
    /* Chân trang và các thành phần khác */
    .footer {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #ecf0f3; color: #555; text-align: center;
        padding: 15px; font-size: 14px; border-top: 3px solid #fdd835;
        z-index: 999; box-shadow: 0 -2px 15px rgba(0,0,0,0.1);
    }}
    .footer p {{ margin: 0; font-family: sans-serif; line-height: 1.5; }}
    
    /* CSS cho trình phát nhạc */
    audio {{
        width: 60%;
        border-radius: 15px;
        box-shadow: 5px 5px 10px #bec3c7, -5px -5px 10px #ffffff;
    }}
</style>
""", unsafe_allow_html=True)

# Khối CSS chạy chữ TÁCH BIỆT 
st.markdown("""
<style>
    /* CSS MỚI: Chữ chạy ngang (Marquee effect) */
    .running-text-container {
        overflow: hidden; 
        background-color: #fff; 
        color: #b71c1c; 
        font-weight: bold;
        padding: 10px 0; 
        margin-bottom: 20px; 
        border-bottom: 3px solid #ff9800;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .running-text {
        display: inline-block;
        white-space: nowrap;
        font-size: 1.3rem; 
        animation: marquee 35s linear infinite; 
    }
    @keyframes marquee {
        0%    { transform: translate(100%, 0); }
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
    
    st.markdown("<h3 style='text-align: center; color: #b71c1c; margin-top: 10px; font-weight: 900;'>TRƯỜNG PTDTBT<br>TH&THCS NA Ư</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🚀 Menu Chức Năng")

    if st.button("🏠 Trang Chủ", use_container_width=True):
        st.rerun()
    if os.path.exists(PAGE_1):
        st.page_link(PAGE_1, label="Gia Sư Toán AI", icon="🏔️")
    if os.path.exists(PAGE_2):
        st.page_link(PAGE_2, label="Tạo Đề Tự Động", icon="⚡")
    if os.path.exists(PAGE_3):
        st.page_link(PAGE_3, label="Giải bài tập từ ảnh", icon="🧿")
    if os.path.exists(PAGE_4):
        st.page_link(PAGE_4, label="Học liệu đa phương tiện", icon="📽️")
    if os.path.exists(PAGE_5):
        st.page_link(PAGE_5, label="Văn hóa cội nguồn", icon="🌽")

    st.markdown("---")
    
    # --- PHẦN XỬ LÝ ĐẾM LƯỢT TRUY CẬP (ĐÃ SỬA) ---
    # Gọi hàm để lấy số lượt truy cập toàn cục
    global_count = update_global_visit_count()
    st.success(f"👥 Lượt truy cập: **{global_count}**")

# --- 4. NỘI DUNG TRANG CHÍNH ---

# CHÈN DÒNG CHỮ CHẠY
st.markdown("""
<div class="running-text-container">
    <div class="running-text">
        📢 CHÀO MỪNG ĐẾN VỚI HỆ THỐNG TRỢ LÝ GIÁO DỤC AI SAM MỨN! SỬ DỤNG AI ĐỂ NÂNG CAO CHẤT LƯỢNG DẠY VÀ HỌC TẠI VÙNG CAO.
    </div>
</div>
""", unsafe_allow_html=True)

# HEADER CHÍNH
st.markdown("""
<div class="main-header">
    <h1> HỆ THỐNG TRỢ LÝ GIÁO DỤC AI SAM MỨN</h1>
    <h3>"Tri thức - Vươn xa thế giới"</h3>
</div>
""", unsafe_allow_html=True)

# --- THANH NHẠC H'MÔNG (Neumorphism style) ---
st.markdown(f"""
<div style="text-align:center; margin-bottom:40px;">
<h4 style="color: #444; font-weight: 600;">🎧 Giai điệu bản Mông</h4>
<audio controls autoplay style="box-shadow: 8px 8px 15px #bec3c7, -8px -8px 15px #ffffff; background: #ecf0f3;">
    {audio_source_html}
    Trình duyệt của bạn không hỗ trợ audio.
</audio>
</div>
""", unsafe_allow_html=True)

# --- CARD CHỨC NĂNG (NEUMORPHISM) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Card 1: Gia Sư Toán AI (Golden Orange Text)
    st.markdown('<div class="feature-card card-math"><div class="icon-box">🏔️</div><div class="card-title">Gia Sư Toán AI</div><p>Sử dụng trí tuệ nhân tạo để học tập, giải bài và ôn tập môn Toán bằng hai ngôn ngữ.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_1):
        st.page_link(PAGE_1, label="Học ngay ➜", icon="📝", use_container_width=True)

with col2:
    # Card 2: Tạo Đề Tốc Độ (Electric Blue Text)
    st.markdown('<div class="feature-card card-quiz"><div class="icon-box">⚡</div><div class="card-title">Tạo Đề Tự Động</div><p>Tự động tạo các bộ đề thi trắc nghiệm theo chương trình, giúp tiết kiệm thời gian cho giáo viên.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_2):
        st.page_link(PAGE_2, label="Tạo đề ➜", icon="🚀", use_container_width=True)

with col3:
    # Card 3: Giải bài tập từ ảnh (Vibrant Green Text)
    st.markdown('<div class="feature-card card-image"><div class="icon-box">🧿</div><div class="card-title">Giải bài tập từ ảnh</div><p>Chụp ảnh bài tập bất kỳ và nhận lời giải chi tiết, giúp học sinh tự học hiệu quả hơn.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_3):
        st.page_link(PAGE_3, label="Giải ngay ➜", icon="📸", use_container_width=True)

with col4:
    # Card 4: Học Liệu Đa Phương Tiện (Crimson Red Text)
    st.markdown('<div class="feature-card card-media"><div class="icon-box">📽️</div><div class="card-title">Học Liệu Đa Phương Tiện</div><p>Khám phá kho học liệu phong phú nhiều tính năng.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_4):
        st.page_link(PAGE_4, label="Khám phá ➜", icon="🎧", use_container_width=True)

# --- 5. CHÂN TRANG (FOOTER) ---
st.markdown("""
<div class="footer">
    <p>👨‍🏫 <b>Tác giả:</b> Đinh Công Lâm </p> </b> Trường PTNT TH&THCS Sam Mứn</p>
    <p style="font-size: 12px; color: #888;">© Năm học 2026 - 2027 - Hệ thống Trợ lý Giáo dục AI Sam Mứn </p>
</div>
""", unsafe_allow_html=True)
