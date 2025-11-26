import streamlit as st
import os

# --- 1. CẤU HÌNH TRANG WEB (Bắt buộc phải ở đầu) ---
st.set_page_config(
    page_title="Cổng Giáo Dục Số - Trường Na Ư",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. HÀM ĐẾM LƯỢT TRUY CẬP ---
if 'visit_count' not in st.session_state:
    st.session_state.visit_count = 5383 # Số khởi điểm giả định

# --- 3. CSS TÙY CHỈNH GIAO DIỆN ---
st.markdown("""
<style>
    /* Ẩn menu mặc định */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp { background-color: #f8f9fa; }

    /* HEADER */
    .main-header {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 60%, #ff6f00 100%);
        color: white;
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(183, 28, 28, 0.4);
        border-bottom: 6px solid #fdd835;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    /* Trang trí Header */
    .main-header h1 { text-shadow: 2px 2px 5px rgba(0,0,0,0.3); font-size: 2.5rem; font-weight: 900; margin: 0; }
    .main-header h3 { font-style: italic; font-weight: 300; margin-top: 5px; opacity: 0.95; }

    /* CARD TÍNH NĂNG */
    .feature-card {
        background: white; padding: 20px 15px; border-radius: 20px;
        text-align: center; border: 1px solid #f0f0f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: all 0.3s; height: 350px; 
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .feature-card:hover { transform: translateY(-8px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); border-color: #ffcc80; }
    .icon-box { font-size: 3.5rem; margin-bottom: 10px; }
    .card-title { color: #bf360c; font-weight: 800; font-size: 1.3rem; margin-bottom: 5px; min-height: 50px; display: flex; align-items: center; justify-content: center;}
    .card-desc { color: #555; font-size: 0.9rem; line-height: 1.4; margin-bottom: 15px; }

    /* BUTTON */
    .stButton>button {
        background: linear-gradient(90deg, #ef6c00, #ff9800); color: white;
        border-radius: 30px; border: none; font-weight: 600;
        padding: 8px 20px; width: 100%; transition: 0.2s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(230, 81, 0, 0.3); }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2997/2997235.png", width=130) 
    st.markdown("<h2 style='text-align: center; color: #b71c1c;'>🏫 TRƯỜNG PTDTBT<br>TH&THCS NA Ư</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.success(f"👥 Lượt truy cập: **{st.session_state.visit_count}**")

# --- 5. NỘI DUNG CHÍNH ---

# Header
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>"Tri thức vùng cao - Vươn xa thế giới"</h3>
</div>
""", unsafe_allow_html=True)

# --- GRID LAYOUT 4 CỘT (KÈM CHỨC NĂNG CHUYỂN TRANG) ---
col1, col2, col3, col4 = st.columns(4)

# CỘT 1: GIA SƯ TOÁN
with col1:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">🏔️</div>
            <div class="card-title">Gia Sư Toán AI</div>
            <div class="card-desc">Học toán song ngữ Việt-Mông. Tích lũy bắp ngô đổi quà.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("") 
    if st.button("Học ngay ➜", key="btn1"):
        try:
            st.switch_page("pages/1_Gia_Su_Toan.py")
        except:
            st.error("Chưa tạo file pages/1_Gia_Su_Toan.py")

# CỘT 2: SINH ĐỀ
with col2:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">⚡</div>
            <div class="card-title">Sinh Đề Tốc Độ</div>
            <div class="card-desc">Tạo đề trắc nghiệm & tự luận 3 giây. Kho đề chuẩn SGK.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Tạo đề ➜", key="btn2"):
        try:
            st.switch_page("pages/2_Sinh_De.py")
        except:
             st.error("Chưa tạo file pages/2_Sinh_De.py")

# CỘT 3: CHẤM BÀI
with col3:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">🧿</div>
            <div class="card-title">Chấm Thi AI</div>
            <div class="card-desc">Nhận diện chữ viết tay. Chụp ảnh bài làm, có điểm ngay.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Chấm bài ➜", key="btn3"):
        try:
            st.switch_page("pages/3_Cham_Thi.py")
        except:
             st.error("Chưa tạo file pages/3_Cham_Thi.py")

# CỘT 4: HỌC ĐA PHƯƠNG TIỆN
with col4:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">📽️</div>
            <div class="card-title">Học Đa Phương Tiện</div>
            <div class="card-desc">Kho video bài giảng, phim tài liệu văn hóa & sách nói.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Khám phá ➜", key="btn4"):
        try:
            st.switch_page("pages/4_Da_Phuong_Tien.py")
        except:
             st.error("Chưa tạo file pages/4_Da_Phuong_Tien.py")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.8rem;'>© 2025 Trường PTDTBT TH&THCS Na Ư</div>", unsafe_allow_html=True)
