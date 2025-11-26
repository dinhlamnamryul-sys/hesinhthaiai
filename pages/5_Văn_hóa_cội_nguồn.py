import streamlit as st

# --- CẤU HÌNH CSS (GIAO DIỆN) ---
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .culture-header {
        font-family: 'Arial', sans-serif;
        color: #1a237e;
        text-align: center;
        padding: 20px;
        border-bottom: 3px solid #d84315;
        margin-bottom: 20px;
        background-image: linear-gradient(to right, #e8eaf6, #ffffff, #e8eaf6);
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #d84315;
        color: white;
        border-radius: 20px;
        border: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- PHẦN TIÊU ĐỀ ---
st.markdown("""
    <div class="culture-header">
        <h1>🏛️ BẢO TÀNG VĂN HÓA SỐ NA Ư</h1>
        <p><i>"Lắng nghe hồn núi - Gìn giữ sắc hoa"</i></p>
    </div>
""", unsafe_allow_html=True)

# --- QUẢN LÝ ĐIỂM (BẮP NGÔ) ---
if 'corn_points' not in st.session_state:
    st.session_state.corn_points = 150

col_info, col_point = st.columns([8, 2])
with col_point:
    st.metric(label="Kho Bắp Ngô", value=f"{st.session_state.corn_points} 🌽")

# --- CÁC TAB NỘI DUNG ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🔥 Chuyện kể", 
    "🧵 Hoa văn", 
    "🎵 Giai điệu", 
    "🏆 Thử thách"
])

# TAB 1: TRUYỆN CỔ TÍCH
with tab1:
    st.header("📖 Sự tích cây Khèn (Qeej)")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format='audio/mp3')
    st.info("Bấm nút Play để nghe già làng kể chuyện.")
    
    with st.expander("Xem lời thoại song ngữ"):
        col_mong, col_viet = st.columns(2)
        with col_mong:
            st.markdown("**Tiếng H'Mông:**\n\n*Puaz thaus u, muaz ib tug tub...*")
        with col_viet:
            st.markdown("**Tiếng Việt:**\n\n*Ngày xưa, có một chàng trai...*")

# TAB 2: HOA VĂN
with tab2:
    st.header("🧵 Ý nghĩa hoa văn thổ cẩm")
    c1, c2 = st.columns(2)
    with c1:
        st.image("https://cdn.pixabay.com/photo/2017/08/30/12/45/fabric-2696860_1280.jpg", caption="Họa tiết xoắn ốc")
        st.success("Tượng trưng cho sự sinh sôi, nảy nở.")
    with c2:
        st.image("https://cdn.pixabay.com/photo/2016/11/23/18/26/border-1854203_1280.jpg", caption="Họa tiết chân chó")
        st.success("Biểu tượng lòng trung thành, giữ nhà.")

# TAB 3: VIDEO
with tab3:
    st.header("🎵 Điệu múa khèn")
    st.video("https://www.youtube.com/watch?v=ysz5S6PUM-U")

# TAB 4: QUIZ
with tab4:
    st.header("🏆 Trả lời đúng nhận Bắp Ngô")
    with st.form("my_quiz"):
        ans = st.radio("Cây nêu trong lễ hội Gâu Tào dùng để làm gì?", 
                     ["Phơi quần áo", "Cầu may mắn, sức khỏe", "Trang trí"])
        
        submit = st.form_submit_button("Gửi đáp án")
        
        if submit:
            if ans == "Cầu may mắn, sức khỏe":
                st.balloons()
                st.success("Chính xác! +10 Bắp ngô")
            else:
                st.error("Sai rồi, thử lại nhé!")
