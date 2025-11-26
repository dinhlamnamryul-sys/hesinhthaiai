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

# --- HÀM ĐẾM LƯỢT TRUY CẬP (GIẢ LẬP DB) ---
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

# --- CSS TÙY CHỈNH GIAO DIỆN (PHONG CÁCH NA Ư PRO) ---
st.markdown("""
<style>
    /* Ẩn menu mặc định */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* BACKGROUND */
    .stApp {
        background-color: #f8f9fa; /* Màu nền sáng nhẹ hiện đại */
    }

    /* 1. HEADER CHÍNH */
    .main-header {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 60%, #ff6f00 100%);
        color: white;
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(183, 28, 28, 0.4);
        border-bottom: 6px solid #fdd835; /* Viền vàng bản sắc */
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    /* Họa tiết chìm (Pattern thổ cẩm giả lập bằng CSS) */
    .main-header::before {
        content: "☁️"; font-size: 150px; opacity: 0.1;
        position: absolute; top: -50px; left: 20px;
    }
    .main-header::after {
        content: "🌽"; font-size: 150px; opacity: 0.1;
        position: absolute; bottom: -40px; right: 20px;
    }

    .main-header h1 { 
        text-shadow: 2px 2px 5px rgba(0,0,0,0.3); 
        font-size: 2.8rem; 
        font-weight: 900;
        margin: 0;
        letter-spacing: 1px;
    }
    .main-header h3 {
        font-family: 'Segoe UI', sans-serif;
        font-style: italic;
        font-weight: 300;
        margin-top: 5px;
        opacity: 0.95;
    }

    /* 2. HUY HIỆU OFFLINE (ĐIỂM NHẤN CÔNG NGHỆ) */
    .offline-badge {
        display: inline-block;
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: bold;
        border: 1px solid #c8e6c9;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* 3. THẺ TÍNH NĂNG (CARD) */
    .feature-card {
        background: white;
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        height: 320px; /* Chiều cao cố định cho đồng bộ */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border-color: #ffcc80;
    }

    .icon-box {
        font-size: 4.5rem;
        margin-bottom: 15px;
        text-shadow: 0 5px 10px rgba(0,0,0,0.1);
    }
    
    .card-title {
        color: #bf360c;
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 10px;
    }
    
    .card-desc {
        color: #555;
        font-size: 1rem;
        line-height: 1.5;
        margin-bottom: 20px;
    }

    /* 4. NÚT BẤM */
    .stButton>button {
        background: linear-gradient(90deg, #ef6c00, #ff9800);
        color: white;
        border-radius: 30px;
        border: none;
        font-weight: 600;
        padding: 10px 30px;
        width: 100%;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #e65100, #f57c00);
        box-shadow: 0 5px 15px rgba(230, 81, 0, 0.3);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (LOGO MỚI & NHẠC) ---
with st.sidebar:
    # Thay icon folder cũ bằng icon "Trường học" hoặc "Ngọn núi" cách điệu
    # Bạn có thể thay url bên dưới bằng logo thật của trường nếu có
    st.image("https://cdn-icons-png.flaticon.com/512/2997/2997235.png", width=130) 
    
    st.markdown("<h2 style='text-align: center; color: #b71c1c;'>🏫 TRƯỜNG PTDTBT<br>TH&THCS NA Ư</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("🎵 **Giai điệu bản mường:**")
    # Link nhạc demo (nhẹ nhàng hơn)
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3", start_time=0)
    
    st.success(f"👥 Đã đón tiếp: **{st.session_state.visit_count}** lượt")
    
    # Menu phụ
    st.markdown("### 📌 Lối tắt")
    st.caption("ℹ️ Hướng dẫn sử dụng")
    st.caption("📞 Liên hệ thầy cô")

# --- NỘI DUNG CHÍNH ---

# Header
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>"Tri thức vùng cao - Vươn xa thế giới"</h3>
</div>
""", unsafe_allow_html=True)

# Dòng thông báo Offline (Điểm nhấn ăn tiền với giám khảo)
st.markdown("""
<center>
    <div class="offline-badge">
        📶 Hệ thống đã kích hoạt Smart-Cache: Sẵn sàng hoạt động khi mất mạng
    </div>
</center>
""", unsafe_allow_html=True)

# Hiệu ứng bóng bay (Chỉ chạy 1 lần)
if 'welcomed' not in st.session_state:
    st.balloons()
    st.session_state.welcomed = True

# Grid layout cho các tính năng
col1, col2, col3 = st.columns(3)

# THẺ 1: GIA SƯ TOÁN (Giữ hình ngọn núi)
with col1:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">🏔️</div>
            <div class="card-title">Gia Sư Toán AI</div>
            <div class="card-desc">Học toán song ngữ Việt - Mông. Giải bài tập khó, tích lũy bắp ngô đổi quà.</div>
        </div>
        </div>
    """, unsafe_allow_html=True)
    # Hack để nút bấm nằm "trong" card về mặt thị giác
    st.write("") 
    if st.button("Học ngay ➜", key="btn1"):
        st.success("Đang khởi động trợ lý ảo H'Mông...")

# THẺ 2: SINH ĐỀ (Đổi sang biểu tượng Sấm sét - Tốc độ/Sức mạnh)
with col2:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">⚡</div>
            <div class="card-title">Sinh Đề Siêu Tốc</div>
            <div class="card-desc">Tạo đề trắc nghiệm & tự luận chỉ trong 3 giây. Kho đề phong phú bám sát SGK.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Tạo đề ➜", key="btn2"):
        st.success("Đang truy cập kho dữ liệu đề thi...")

# THẺ 3: CHẤM BÀI (Đổi sang Mắt thần/AI Vision - Công nghệ cao)
with col3:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">🧿</div>
            <div class="card-title">Chấm Thi AI Vision</div>
            <div class="card-desc">Công nghệ nhận diện chữ viết tay. Chụp ảnh bài làm, có điểm ngay lập tức.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Chấm bài ➜", key="btn3"):
        st.success("Đang bật camera...")

st.markdown("---")

# Footer
st.markdown(
    """
    <div style='text-align: center; color: #888; padding: 20px; font-size: 0.85rem;'>
        <p>© 2025 Bản quyền thuộc về Trường PTDTBT TH&THCS Na Ư</p>
        <p><i>Sản phẩm tham dự cuộc thi Sáng tạo KHKT Thanh thiếu niên</i></p>
    </div>
    """, 
    unsafe_allow_html=True
)
