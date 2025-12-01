import streamlit as st
import os
import base64

# --- CẤU HÌNH LOGO VÀ ẢNH NỀN ---
LOGO_PATH = "image_2.png.png" # Lưu ý: Kiểm tra lại tên file logo của bạn
LOGO_URL_ONLINE = "https://cdn-icons-png.flaticon.com/512/2997/2997235.png"

# --- KHAI BÁO VÀ HÀM XỬ LÝ ẢNH NỀN (ĐÃ ĐƯA LÊN ĐẦU ĐỂ KHÔNG BỊ LỖI NAMERROR) ---
BACKGROUND_IMAGE_PATH = "bantrang.jpg" # Tên file ảnh nền của bạn (Phải nằm cùng thư mục)

def get_base64_image(image_path):
    """Hàm chuyển ảnh local thành Base64 để nhúng vào CSS"""
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            # Bỏ qua lỗi nếu không đọc được file ảnh nền
            return ""
    return ""

# --- GỌI HÀM ĐỂ TẠO BIẾN TRƯỚC KHI DÙNG ---
base64_image = get_base64_image(BACKGROUND_IMAGE_PATH)


# --- KHỞI TẠO CẤU HÌNH CHUNG ---
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

# --- 2. CSS GIAO DIỆN (ĐÃ CẬP NHẬT TRANG TRÍ VÀ DÙNG F-STRING) ---
st.markdown(f"""
<style>
    /* BẮT ĐẦU PHẦN ĐẶT ẢNH NỀN VÀ NỀN CHUNG */
    .stApp {{ 
        margin-bottom: 60px;
        /* Thêm ảnh nền nếu chuỗi Base64 tồn tại */
        {"background-image: url(data:image/jpg;base64," + base64_image + ");" if base64_image else "background-color: #f8f9fa;"}
        background-size: cover; 
        background-position: center; 
        background-attachment: fixed;
    }}
    
    /* 1. THANH BÊN (SIDEBAR) - LÀM MỜ, NỔI BẬT HƠN */
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.7); /* Rất mờ */
        border-right: 5px solid #d32f2f; /* Thêm đường viền đỏ */
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }}
    
    /* Các thành phần cố định */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{ 
        background-color: rgba(0,0,0,0); color: transparent; 
        visibility: hidden !important; display: none !important;
    }}
    [data-testid="stSidebarCollapsedControl"] {{
        visibility: visible !important; display: block !important;
        color: white !important; background-color: #d32f2f; border-radius: 50%;
        padding: 5px; z-index: 999999;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }}

    /* 2. HEADER CHÍNH - LÀM DỊU, TRONG SUỐT VÀ BO GÓC SẮC NÉT HƠN */
    .main-header {{
        background: rgba(183, 28, 28, 0.8); /* Màu đỏ đậm bán trong suốt */
        color: white; 
        padding: 25px; 
        border-radius: 15px; 
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3); 
        border-bottom: 4px solid #fdd835;
        margin-bottom: 30px; 
        margin-top: -10px;
    }}
    .main-header h1 {{ font-size: 2.8rem; font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.4); }}
    .main-header h3 {{ font-weight: 500; margin-top: 5px; }}

    /* 3. FEATURE CARDS MỚI: NỔI BẬT VÀ PHÙ HỢP NỀN */
    .feature-card {{
        background: rgba(255, 255, 255, 0.9); /* Gần như trong suốt, dễ đọc */
        padding: 25px; 
        border-radius: 20px; /* Bo góc mềm mại hơn */
        text-align: center;
        border: 2px solid #ddd; /* Viền xám nhẹ */
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); /* Đổ bóng nổi bật */
        height: 380px; 
        display: flex; flex-direction: column; justify-content: space-between;
        transition: all 0.3s ease-in-out;
    }}
    .feature-card:hover {{ 
        transform: translateY(-10px); /* Nhấc lên mạnh mẽ hơn */
        box-shadow: 0 15px 30px rgba(255, 111, 0, 0.3); /* Đổ bóng màu cam khi hover */
        border: 2px solid #ff6f00; /* Viền màu cam khi hover */
    }}
    .icon-box {{ 
        font-size: 4.8rem; /* Icon lớn hơn */
        margin-bottom: 15px; 
    }}
    .card-title {{ 
        color: #d84315; /* Màu chữ tiêu đề */
        font-weight: 900; 
        font-size: 1.5rem; /* Tiêu đề lớn hơn */
        margin-bottom: 10px; 
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }}
    
    /* Nút bấm (Link Page) */
    .stButton>button {{
        width: 100%; border-radius: 50px; 
        background: linear-gradient(90deg, #ff6f00 0%, #ffca28 100%);
        border: none; color: white; font-weight: bold; padding: 12px 0;
        box-shadow: 0 4px 10px rgba(255, 111, 0, 0.4);
    }}
    .stButton>button:hover {{ transform: scale(1.03); background: linear-gradient(90deg, #ff9800 0%, #ffca28 100%); }}

    /* 4. FOOTER - LÀM TRONG SUỐT NHẸ */
    .footer {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: rgba(255, 255, 255, 0.9); 
        color: #555; text-align: center;
        padding: 10px; font-size: 14px; border-top: 3px solid #b71c1c;
        z-index: 999; box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }}
    .footer p {{ margin: 0; font-family: sans-serif; line-height: 1.5; }}
    
    /* CSS cho trình phát nhạc */
    audio {{
        width: 60%; 
        border-radius: 30px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
</style>
""", unsafe_allow_html=True)

# --- KHAI BÁO FILE TRANG ---
PAGE_1 = "pages/1_Gia_Sư_Toán_AI.py"
PAGE_2 = "pages/2_Sinh_Đề_Tự_Động.py"
PAGE_3 = "pages/3_Giải_bài_tập_từ_ảnh.py"
PAGE_4 = "pages/4_Học_liệu_đa_phương_tiện.py"
PAGE_5 = "pages/5_Văn_hóa_cội_nguồn.py"

# --- XỬ LÝ NHẠC H'MÔNG (LOCAL & ONLINE) ---
MUSIC_FILE = "nhac_nen.mp3"  # Tên file nhạc bạn cần chép vào cùng thư mục code

def get_audio_html(file_path):
    """Hàm đọc file nhạc local và chuyển sang mã HTML để phát"""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
    else:
        # Link dự phòng nếu chưa có file nhạc (Tiếng sáo trúc demo)
        fallback_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" 
        return f'<source src="{fallback_url}" type="audio/mp3">'

# Gọi hàm lấy source nhạc
audio_source_html = get_audio_html(MUSIC_FILE)

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
    if 'visit_count' not in st.session_state:
        st.session_state.visit_count = 0
    st.success(f"👥 Lượt truy cập: **{st.session_state.visit_count}**")

# --- 4. NỘI DUNG TRANG CHÍNH ---
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>"Tri thức vùng cao - Vươn xa thế giới"</h3>
</div>
""", unsafe_allow_html=True)

# --- THANH NHẠC H'MÔNG (ĐÃ NÂNG CẤP) ---  
st.markdown(f"""
<div style="text-align:center; margin-bottom:30px;">
<h4 style="color: #555;">🎵 Giai điệu bản Mông</h4>
<audio controls autoplay>
  {audio_source_html}
  Trình duyệt của bạn không hỗ trợ audio.
</audio>
</div>
""", unsafe_allow_html=True)

# --- CARD CHỨC NĂNG ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="feature-card"><div class="icon-box">🏔️</div><div class="card-title">Gia Sư Toán AI</div><p>Học toán song ngữ.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_1):
        st.page_link(PAGE_1, label="Học ngay ➜", icon="📝", use_container_width=True)

with col2:
    st.markdown('<div class="feature-card"><div class="icon-box">⚡</div><div class="card-title">Sinh Đề Tốc Độ</div><p>Tạo đề trắc nghiệm trong vài giây.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_2):
        st.page_link(PAGE_2, label="Tạo đề ➜", icon="🚀", use_container_width=True)

with col3:
    st.markdown('<div class="feature-card"><div class="icon-box">🧿</div><div class="card-title">Giải bài tập từ ảnh</div><p>Giải bài mọi môn học bằng AI.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_3):
        st.page_link(PAGE_3, label="Giải ngay ➜", icon="📸", use_container_width=True)

with col4:
    st.markdown('<div class="feature-card"><div class="icon-box">📽️</div><div class="card-title">Đa Phương Tiện</div><p>Học liệu văn hóa H\'Mông.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_4):
        st.page_link(PAGE_4, label="Khám phá ➜", icon="🎧", use_container_width=True)

# --- 5. CHÂN TRANG (FOOTER) ---
st.markdown("""
<div class="footer">
    <p>👨‍🏫 <b>Nhóm tác giả:</b> Trường PTDTBT TH&THCS Na Ư</p>
    <p style="font-size: 12px; color: #888;">© 2025 Cổng Giáo Dục Số Na Ư</p>
</div>
""", unsafe_allow_html=True)
