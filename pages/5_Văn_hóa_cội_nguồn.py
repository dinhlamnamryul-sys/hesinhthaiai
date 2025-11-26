import streamlit as st

# --- 1. DỮ LIỆU GIẢ LẬP (DATA ĐÃ SINH SẴN) ---
# Tôi tạo một "kho dữ liệu" ở đây để bạn dễ quản lý
DATA_STORY = {
    "title": "Sự tích Hoa Tớ Dày (Pang Tớ Dày)",
    "content_viet": """
    Ngày xưa, ở một bản Mông nọ có chàng trai tên là Khèn và cô gái tên là Tớ Dày yêu nhau tha thiết. 
    Nhưng cha mẹ cô gái lại ép gả cô cho con trai nhà Thống lý giàu có.
    Không chịu khuất phục, Tớ Dày bỏ trốn vào rừng sâu đợi người yêu. 
    Nàng đợi mãi, đợi mãi cho đến khi kiệt sức và hóa thành một loài cây thân cành khẳng khiu.
    Mỗi độ xuân về, cây lại nở ra những bông hoa 5 cánh đỏ thắm như máu con tim người thiếu nữ. 
    Người Mông gọi đó là hoa Tớ Dày (đào rừng), loài hoa báo hiệu mùa xuân về trên rẻo cao.
    """,
    "content_mong": """
    (Dữ liệu mô phỏng tiếng H'Mông)
    Puaz thaus u, muaz ib tug tub npe hu ua Khèn...
    Tớ Dày tsis yuav, nwing thb khiav mus rau hauv hav zoov...
    Thaus lub caij nplooj ntoos hlav, tsob ntoo tawg paj liab vog...
    """
}

DATA_QUIZ = [
    {
        "question": "Hoa Tớ Dày (Pang Tớ Dày) thường nở vào dịp nào trong năm?",
        "options": ["Mùa gặt lúa (Tháng 9)", "Dịp Tết của người Mông (Tháng 12 - Tháng 1)", "Mùa mưa (Tháng 7)"],
        "answer": "Dịp Tết của người Mông (Tháng 12 - Tháng 1)",
        "explanation": "Đúng rồi! Hoa Tớ Dày nở báo hiệu một mùa xuân mới và Tết của người Mông sắp về."
    },
    {
        "question": "Chiếc váy của phụ nữ Mông thường có hình dáng giống cái gì?",
        "options": ["Hình bông lúa", "Hình con bướm", "Hình bông hoa xòe (như hoa bí)"],
        "answer": "Hình bông hoa xòe (như hoa bí)",
        "explanation": "Chính xác! Váy xòe xếp ly khi múa hoặc đi lại tạo nên sự uyển chuyển như một bông hoa."
    },
    {
        "question": "Nhạc cụ nào sau đây KHÔNG PHẢI của người H'Mông?",
        "options": ["Khèn (Qeej)", "Đàn Đáy", "Sáo Mông"],
        "answer": "Đàn Đáy",
        "explanation": "Đúng! Đàn Đáy thường dùng trong Ca Trù của người Kinh. Người Mông nổi tiếng với Khèn và Sáo."
    }
]

# --- 2. CẤU HÌNH GIAO DIỆN ---
st.markdown("""
    <style>
    .main { background-color: #fffbf0; } /* Màu nền kem nhẹ */
    
    /* Header rực rỡ */
    .header-box {
        background: linear-gradient(90deg, #b71c1c, #d32f2f);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    
    /* Card câu hỏi */
    .quiz-card {
        background-color: white;
        padding: 15px;
        border-left: 5px solid #d32f2f;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIC CHƯƠNG TRÌNH ---

# Header
st.markdown(f"""
    <div class="header-box">
        <h1>🏛️ DI SẢN BẢN MÔNG</h1>
        <p>Khám phá văn hóa - Tích lũy Bắp Ngô - Đổi quà học tập</p>
    </div>
""", unsafe_allow_html=True)

# Quản lý điểm số (Session State)
if 'score' not in st.session_state:
    st.session_state.score = 150 # Điểm có sẵn

# Hiển thị điểm
c1, c2 = st.columns([3, 1])
with c1:
    st.write(f"👋 Chào em, hôm nay chúng ta sẽ tìm hiểu về **{DATA_STORY['title']}**")
with c2:
    st.info(f"🌽 Kho bắp ngô: **{st.session_state.score}**")

# Tabs
tab_story, tab_pattern, tab_quiz = st.tabs(["📖 Chuyện kể (Audio)", "🧵 Hoa văn & Trang phục", "🏆 Thử thách lấy quà"])

# --- TAB 1: CHUYỆN KỂ ---
with tab_story:
    col_img, col_txt = st.columns([1, 2])
    with col_img:
        # Ảnh hoa đào rừng (Tớ Dày)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Prunus_cerasoides_flower.jpg/640px-Prunus_cerasoides_flower.jpg", caption="Hoa Tớ Dày báo hiệu mùa xuân")
    
    with col_txt:
        st.subheader(DATA_STORY["title"])
        # Giả lập Audio (dùng file nhạc không lời làm nền)
        st.audio("https://upload.wikimedia.org/wikipedia/commons/transcoded/c/c4/Guzheng_Pingshu_Lotus.ogg/Guzheng_Pingshu_Lotus.ogg.mp3", format="audio/mp3")
        
        with st.expander("📜 Đọc lời kể (Song ngữ Việt - Mông)", expanded=True):
            st.markdown(f"**Tiếng Việt:**\n{DATA_STORY['content_viet']}")
            st.markdown("---")
            st.markdown(f"**Tiếng H'Mông:**\n{DATA_STORY['content_mong']}")

# --- TAB 2: HOA VĂN ---
with tab_pattern:
    st.subheader("Vẻ đẹp trên trang phục người Mông")
    
    c_p1, c_p2, c_p3 = st.columns(3)
    
    with c_p1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Hmong_girls_in_Vietnam.jpg/480px-Hmong_girls_in_Vietnam.jpg", caption="Trang phục phụ nữ Mông")
        with st.popover("🔍 Xem chi tiết"):
            st.write("Váy người Mông được làm từ vải lanh, nhuộm chàm và thêu hoa văn sặc sỡ.")
            
    with c_p2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Hmong_Khen_performance.jpg/640px-Hmong_Khen_performance.jpg", caption="Nghệ thuật múa Khèn")
        with st.popover("🔍 Xem chi tiết"):
            st.write("Cây Khèn vừa là nhạc cụ, vừa là đạo cụ múa, thể hiện sức mạnh của chàng trai.")

    with c_p3:
        st.markdown("### 💡 Bạn có biết?")
        st.info("Người Mông thường vẽ sáp ong lên vải lanh trắng trước khi nhuộm chàm để tạo ra các hoa văn trắng xanh rất bền màu.")

# --- TAB 3: QUIZ (TRẮC NGHIỆM) ---
with tab_quiz:
    st.subheader("🎯 Trả lời đúng nhận ngay 10 Bắp Ngô/câu")
    
    # Vòng lặp tạo câu hỏi tự động từ DATA_QUIZ
    for i, item in enumerate(DATA_QUIZ):
        st.markdown(f"<div class='quiz-card'><strong>Câu {i+1}:</strong> {item['question']}</div>", unsafe_allow_html=True)
        
        # Tạo key riêng cho mỗi câu hỏi để không bị lỗi
        user_choice = st.radio(f"Chọn đáp án cho câu {i+1}:", item['options'], key=f"q_{i}", label_visibility="collapsed")
        
        if st.button(f"Trả lời câu {i+1}", key=f"btn_{i}"):
            if user_choice == item['answer']:
                st.balloons()
                st.success(item['explanation'])
                # Cộng điểm ảo (trong phiên làm việc này)
                st.session_state.score += 10
            else:
                st.error("Tiếc quá, chưa đúng rồi. Em thử lại nhé!")
