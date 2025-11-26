import streamlit as st
import os

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Cổng Giáo Dục Số - Trường Na Ư",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS GIAO DIỆN ---
st.markdown("""
<style>
    /* Ẩn menu mặc định của Streamlit (để dùng menu của mình cho đẹp) */
    [data-testid="stSidebarNav"] {display: none;}
    
    .stApp { background-color: #f8f9fa; }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 60%, #ff6f00 100%);
        color: white; padding: 30px; border-radius: 20px; text-align: center;
        box-shadow: 0 10px 30px rgba(183, 28, 28, 0.4); border-bottom: 6px solid #fdd835;
        margin-bottom: 20px; position: relative; overflow: hidden;
    }
    .main-header h1 { font-size: 2.5rem; font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    
    /* Card tính năng */
    .feature-card {
        background: white; padding: 20px; border-radius: 20px; text-align: center;
        border: 1px solid #eee; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 350px; display: flex; flex-direction: column; justify-content: space-between;
        transition: transform 0.3s;
    }
    .feature-card:hover { transform: translateY(-5px); border-color: #ff9800; }
    .icon-box { font-size: 3.5rem; margin-bottom: 10px; }
    .card-title { color: #d84315; font-weight: 800; font-size: 1.3rem; margin-bottom: 5px; min-height: 50px; display: flex; align-items: center; justify-content: center;}
    
    /* Button */
    .stButton>button {
        width: 100%; border-radius: 50px; background: linear-gradient(90deg, #ff6f00, #ffca28);
        border: none; color: white; font-weight: bold; padding: 10px 0;
        transition: 0.2s;
    }
    .stButton>button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (THANH BÊN TRÁI) - ĐÃ KHÔI PHỤC ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2997/2997235.png", width=120) 
    st.markdown("<h3 style='text-align: center; color: #b71c1c; margin: 0;'>TRƯỜNG PTDTBT<br>TH&THCS NA Ư</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # --- MENU ĐIỀU HƯỚNG (BẤM LÀ CHUYỂN TRANG) ---
    st.markdown("### 🚀 Menu Chức Năng")
    
    # Lưu ý: Các file này phải tồn tại trong thư mục 'pages' thì mới bấm được
    st.page_link("Home.py", label="Trang Chủ", icon="🏠")
    st.page_link("pages/1_Gia_Su_Toan.py", label="Gia Sư Toán AI", icon="🏔️")
    st.page_link("pages/2_Sinh_De.py", label="Sinh Đề Tự Động", icon="⚡")
    st.page_link("pages/3_Cham_Thi.py", label="Chấm Bài AI Vision", icon="🧿")
    st.page_link("pages/4_Da_Phuong_Tien.py", label="Học Đa Phương Tiện", icon="📽️")

    st.markdown("---")
    st.write("🎵 **Giai điệu bản mường:**")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3", start_time=0)
    
    # Bộ đếm (Giả lập)
    if 'visit_count' not in st.session_state: st.session_state.visit_count = 5383
    st.success(f"👥 Lượt truy cập: **{st.session_state.visit_count}**")

# --- 4. NỘI DUNG CHÍNH (MAIN PAGE) ---

st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>"Tri thức vùng cao - Vươn xa thế giới"</h3>
</div>
""", unsafe_allow_html=True)

# Lưới 4 cột
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="feature-card"><div class="icon-box">🏔️</div><div class="card-title">Gia Sư Toán AI</div><p>Học toán song ngữ. Tích lũy bắp ngô.</p></div>', unsafe_allow_html=True)
    st.write(""); st.page_link("pages/1_Gia_Su_Toan.py", label="Học ngay ➜", icon="📝", use_container_width=True)

with col2:
    st.markdown('<div class="feature-card"><div class="icon-box">⚡</div><div class="card-title">Sinh Đề Tốc Độ</div><p>Tạo đề trắc nghiệm trong 3 giây.</p></div>', unsafe_allow_html=True)
    st.write(""); st.page_link("pages/2_Sinh_De.py", label="Tạo đề ➜", icon="🚀", use_container_width=True)

with col3:
    st.markdown('<div class="feature-card"><div class="icon-box">🧿</div><div class="card-title">Chấm Thi AI</div><p>Chấm điểm bằng Camera cực nhanh.</p></div>', unsafe_allow_html=True)
    st.write(""); st.page_link("pages/3_Cham_Thi.py", label="Chấm bài ➜", icon="📸", use_container_width=True)

with col4:
    st.markdown('<div class="feature-card"><div class="icon-box">📽️</div><div class="card-title">Đa Phương Tiện</div><p>Video, Sách nói văn hóa H\'Mông.</p></div>', unsafe_allow_html=True)
    st.write(""); st.page_link("pages/4_Da_Phuong_Tien.py", label="Khám phá ➜", icon="🎧", use_container_width=True)
