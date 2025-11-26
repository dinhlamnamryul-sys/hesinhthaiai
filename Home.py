import streamlit as st
import os
import time

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Cổng Giáo Dục Số - Trường Na Ư",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HÀM ĐẾM LƯỢT TRUY CẬP ---
def update_visit_count():
    count_file = "visit_count.txt"
    if not os.path.exists(count_file):
        with open(count_file, "w") as f: f.write("5383"); return 5383
    try:
        with open(count_file, "r") as f: count = int(f.read().strip())
    except: count = 5383
    count += 1
    with open(count_file, "w") as f: f.write(str(count))
    return count

if 'visit_count' not in st.session_state:
    st.session_state.visit_count = update_visit_count()

# --- CSS TÙY CHỈNH GIAO DIỆN (PHONG CÁCH NA Ư) ---
st.markdown("""
<style>
    /* Ẩn menu mặc định và thanh header (toolbar) của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 1. ĐẨY NỘI DUNG LÊN CAO (GIẢM KHOẢNG TRỐNG ĐẦU TRANG) */
    .block-container {
        padding-top: 1rem !important; /* Giảm padding trên cùng */
        padding-bottom: 1rem !important;
    }
    
    /* 2. Header chính được nâng cấp */
    .main-header {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 50%, #ff6f00 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(183, 28, 28, 0.3);
        border-bottom: 8px solid #ffd600; /* Viền vàng thổ cẩm dày hơn */
        margin-bottom: 20px;
        position: relative; /* Để đặt các họa tiết trang trí tuyệt đối */
        overflow: hidden;   /* Cắt bỏ phần thừa của họa tiết */
    }
    
    /* Họa tiết trang trí mờ trong Header */
    .main-header::before {
        content: "";
        position: absolute;
        top: -50px;
        left: -50px;
        width: 200px;
        height: 200px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
    }
    .main-header::after {
        content: "";
        position: absolute;
        bottom: -30px;
        right: -30px;
        width: 150px;
        height: 150px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
    }
    
    .main-header h1 { 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5); 
        font-size: 3rem; 
        font-weight: 800;
        margin-bottom: 10px;
        position: relative; z-index: 1; /* Đảm bảo chữ nổi lên trên họa tiết */
    }
    .main-header h3 {
        position: relative; z-index: 1;
        font-style: italic;
        opacity: 0.9;
    }
    
    /* 3. Style cho dòng tin tức nổi bật */
    .news-ticker {
        background-color: #fff3e0;
        color: #e65100;
        padding: 12px 20px;
        border-radius: 10px;
        border-left: 6px solid #ff6f00;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        animation: fadeIn 1s ease-in;
    }
    .news-icon { font-size: 1.2rem; margin-right: 10px; }
    
    /* Thẻ tính năng */
    .feature-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #eee;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        top: 0;
    }
    .feature-card:hover {
        top: -10px;
        box-shadow: 0 15px 30px rgba(211, 47, 47, 0.15);
        border-color: #d32f2f;
        background: linear-gradient(to bottom, #fff, #fffafafa);
    }
    .icon-big { font-size: 4rem; margin-bottom: 15px; }
    
    /* Nút bấm đẹp hơn */
    .stButton>button {
        background: linear-gradient(90deg, #2e7d32, #43a047);
        color: white;
        border-radius: 25px;
        border: none;
        font-weight: bold;
        padding: 10px 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 10px rgba(0,0,0,0.2);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (LOGO & NHẠC) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3208/3208725.png", width=120) 
    
    st.markdown("### 🏫 TRƯỜNG PTDTBT\n### TH&THCS NA Ư")
    st.markdown("---")
    
    st.write("🎵 **Giai điệu bản mường:**")
    audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" 
    st.audio(audio_url, format='audio/mp3', start_time=0)
    
    st.info(f"👀 Lượt truy cập: **{st.session_state.visit_count}**")

# --- NỘI DUNG CHÍNH ---

# Header với họa tiết mới
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>"Tri thức vùng cao - Vươn xa thế giới"</h3>
</div>
""", unsafe_allow_html=True)

# Tin tức nổi bật (Mới thêm)
st.markdown("""
<div class="news-ticker">
    <span class="news-icon">🔔</span>
    <strong>Thông báo mới:</strong>&nbsp; Chúc mừng đội tuyển Toán của trường đạt giải Nhất huyện! | Lịch thi học kỳ I sẽ bắt đầu từ tuần sau.
</div>
""", unsafe_allow_html=True)

# Hiệu ứng bóng bay chào mừng (Chỉ chạy 1 lần khi load)
if 'welcomed' not in st.session_state:
    st.balloons()
    st.session_state.welcomed = True

st.write("### 👋 Chào mừng các em học sinh và quý thầy cô!")
st.write("Hãy chọn các chức năng học tập thông minh ở thanh bên trái:")

# Grid layout cho các tính năng
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-big">🏔️</div>
        <h3>Gia Sư Toán AI</h3>
        <p>Học toán vui nhộn, tích lũy bắp ngô, đổi quà hấp dẫn. Hỗ trợ song ngữ Việt - Mông.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Truy cập ngay", key="btn1"):
        st.success("Đang chuyển đến Gia Sư Toán AI...")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-big">📝</div>
        <h3>Sinh Đề Tự Động</h3>
        <p>Giáo viên tạo đề kiểm tra, phiếu bài tập trắc nghiệm/tự luận chỉ trong 1 giây.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Truy cập ngay", key="btn2"):
        st.success("Đang chuyển đến module Sinh Đề...")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-big">📸</div>
        <h3>Chấm Bài AI Vision</h3>
        <p>Công nghệ mới nhất! Chụp ảnh bài làm, AI sẽ chấm điểm và chỉ dẫn chi tiết.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Truy cập ngay", key="btn3"):
        st.success("Đang mở Camera chấm bài...")

st.markdown("---")

# Footer đẹp
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <small>© 2025 Bản quyền thuộc về Trường PTDTBT TH&THCS Na Ư</small><br>
        <small>Phát triển bởi Đội ngũ Chuyển đổi số Giáo dục</small>
    </div>
    """, 
    unsafe_allow_html=True
)
