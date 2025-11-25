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
    /* Ẩn menu mặc định của Streamlit cho gọn */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header chính */
    .main-header {
        background-image: linear-gradient(to right, #b71c1c, #d32f2f, #ff6f00);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border-bottom: 5px solid #ffd600; /* Viền vàng thổ cẩm */
        margin-bottom: 20px;
    }
    .main-header h1 { text-shadow: 2px 2px 4px #000000; font-size: 2.8rem; }
    
    /* Thẻ tính năng */
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #eee;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        border-color: #d32f2f;
    }
    .icon-big { font-size: 4rem; margin-bottom: 10px; }
    
    /* Nút bấm đẹp hơn */
    .stButton>button {
        background: linear-gradient(90deg, #2e7d32, #43a047);
        color: white;
        border-radius: 25px;
        border: none;
        font-weight: bold;
        padding: 10px 25px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (LOGO & NHẠC) ---
with st.sidebar:
    # 1. Hiển thị Logo Trường (Thay link ảnh logo trường bạn vào đây)
    # Nếu có file logo.png thì dùng: st.image("logo.png")
    st.image("https://cdn-icons-png.flaticon.com/512/3208/3208725.png", width=120) 
    
    st.markdown("### 🏫 TRƯỜNG PTDTBT\n### TH&THCS NA Ư")
    st.markdown("---")
    
    # 2. Trình phát nhạc nền (Ẩn hoặc hiện)
    st.write("🎵 **Giai điệu bản mường:**")
    # Thay link này bằng link file mp3 nhạc trường bạn
    audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" 
    st.audio(audio_url, format='audio/mp3', start_time=0)
    
    st.info(f"👀 Lượt truy cập: **{st.session_state.visit_count}**")

# --- NỘI DUNG CHÍNH ---
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>"Tri thức vùng cao - Vươn xa thế giới"</h3>
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

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-big">📝</div>
        <h3>Sinh Đề Tự Động</h3>
        <p>Giáo viên tạo đề kiểm tra, phiếu bài tập trắc nghiệm/tự luận chỉ trong 1 giây.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-big">📸</div>
        <h3>Chấm Bài AI Vision</h3>
        <p>Công nghệ mới nhất! Chụp ảnh bài làm, AI sẽ chấm điểm và chỉ dẫn chi tiết.</p>
    </div>
    """, unsafe_allow_html=True)

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
