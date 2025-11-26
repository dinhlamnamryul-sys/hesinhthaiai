import streamlit as st
import time

def app():
    # --- CẤU HÌNH CSS CHO GIAO DIỆN VĂN HÓA H'MÔNG ---
    st.markdown("""
        <style>
        /* Màu nền và font chữ */
        .main {
            background-color: #fcfcfc;
        }
        
        /* Tiêu đề chính mang màu sắc vải chàm và đỏ thổ cẩm */
        .culture-header {
            font-family: 'Arial', sans-serif;
            color: #1a237e; /* Màu chàm đậm */
            text-align: center;
            padding: 20px;
            border-bottom: 3px solid #d84315; /* Màu đỏ đất nung */
            margin-bottom: 20px;
            background-image: linear-gradient(to right, #e8eaf6, #ffffff, #e8eaf6);
            border-radius: 10px;
        }
        
        /* Card chứa nội dung */
        .culture-card {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid #eee;
            margin-bottom: 15px;
        }

        /* Nút bấm phong cách vùng cao */
        .stButton>button {
            background-color: #d84315;
            color: white;
            border-radius: 20px;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #bf360c;
        }
        
        /* Trang trí Tab */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #f0f2f6;
            border-radius: 10px 10px 0 0;
            color: #1a237e;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1a237e;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
        <div class="culture-header">
            <h1>🏛️ BẢO TÀNG VĂN HÓA SỐ NA Ư</h1>
            <p><i>"Lắng nghe hồn núi - Gìn giữ sắc hoa"</i></p>
        </div>
    """, unsafe_allow_html=True)

    # --- KHỞI TẠO STATE (Ví dụ: Điểm bắp ngô) ---
    if 'corn_points' not in st.session_state:
        st.session_state.corn_points = 150 # Điểm giả lập ban đầu

    # Hiển thị số bắp ngô hiện có
    col_info, col_point = st.columns([8, 2])
    with col_point:
        st.metric(label="Kho Bắp Ngô", value=f"{st.session_state.corn_points} 🌽")

    # --- CÁC TAB CHỨC NĂNG CHÍNH ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔥 Chuyện kể bên bếp lửa", 
        "🧵 Hoa văn biết nói", 
        "🎵 Giai điệu bản Mường", 
        "🏆 Thử thách Người giữ lửa"
    ])

    # --- TAB 1: CHUYỆN KỂ (AUDIO SONG NGỮ) ---
    with tab1:
        st.markdown("### 📖 Kho tàng cổ tích H'Mông")
        st.caption("Nghe già làng kể chuyện bằng tiếng mẹ đẻ và học tiếng Việt.")
        
        # Mô phỏng một câu chuyện
        col_text, col_audio = st.columns([1, 1])
        
        with col_text:
            st.info("**Truyện: Sự tích cây Khèn (Qeej)**")
            with st.expander("Xem lời thoại (Song ngữ)", expanded=True):
                st.markdown("""
                **H'Mông:**
                *Puaz thaus u, muaz ib tug tub...* (Đoạn này cần nhờ thầy cô bản địa nhập liệu)
                
                ---
                **Tiếng Việt:**
                *Ngày xưa, có một chàng trai tài giỏi nhưng cha mẹ mất sớm. Anh tạo ra cây khèn để gửi gắm tâm tư của mình vào tiếng gió...*
                """)
        
        with col_audio:
            st.image("https://images.unsplash.com/photo-1596464716127-f2a82984de30?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60", caption="Già làng kể chuyện bên bếp lửa")
            # Placeholder Audio (Bạn thay đường dẫn file mp3 thật vào đây)
            # st.audio("link_audio_o_day.mp3", format='audio/mp3')
            st.success("💡 Mẹo: Nhấn nút Play để nghe giọng đọc truyền cảm!")

    # --- TAB 2: HOA VĂN (THƯ VIỆN ẢNH) ---
    with tab2:
        st.markdown("### 🧵 Giải mã ngôn ngữ trên trang phục")
        
        col_img1, col_img2, col_img3 = st.columns(3)
        
        with col_img1:
            st.image("https://cdn.pixabay.com/photo/2017/08/30/12/45/fabric-2696860_1280.jpg", use_container_width=True)
            with st.popover("🔍 Giải mã Hoa văn 1"):
                st.markdown("**Hoa văn: Hình xoắn ốc**\n\nÝ nghĩa: Tượng trưng cho con ốc sên, biểu hiện sự sinh sôi, nảy nở và sự kiên trì của người vùng cao.")

        with col_img2:
            st.image("https://cdn.pixabay.com/photo/2016/11/23/18/26/border-1854203_1280.jpg", use_container_width=True)
            with st.popover("🔍 Giải mã Hoa văn 2"):
                st.markdown("**Hoa văn: Chân chó**\n\nÝ nghĩa: Người H'Mông coi chó là con vật trung thành, giúp giữ nhà và xua đuổi tà ma.")

        with col_img3:
            st.image("https://cdn.pixabay.com/photo/2014/04/03/10/38/pattern-310963_1280.png", use_container_width=True)
            with st.popover("🔍 Giải mã Hoa văn 3"):
                st.markdown("**Hoa văn: Bông bí**\n\nÝ nghĩa: Cầu mong mùa màng bội thu, nương rẫy xanh tốt.")

    # --- TAB 3: GIAI ĐIỆU (VIDEO) ---
    with tab3:
        st.markdown("### 🎵 Âm vang núi rừng")
        # Video Youtube demo
        st.video("https://www.youtube.com/watch?v=ysz5S6PUM-U") 
        st.caption("Video: Hướng dẫn múa Khèn cơ bản cho học sinh nam.")

    # --- TAB 4: THỬ THÁCH (QUIZ) ---
    with tab4:
        st.markdown("### 🏆 Thử thách kiến thức: Người giữ lửa")
        st.write("Trả lời đúng để nhận thêm **Bắp ngô** đổi quà nhé!")
        
        with st.form("quiz_culture"):
            q1 = st.radio(
                "Câu 1: Trong lễ hội Gâu Tào, cây nêu được dựng lên có ý nghĩa gì?",
                ("Để phơi quần áo", "Cầu mong sức khỏe, may mắn", "Để trang trí cho đẹp"),
                index=None
            )
            
            q2 = st.radio(
                "Câu 2: Nhạc cụ nào được xem là 'linh hồn' của người đàn ông H'Mông?",
                ("Đàn Guitar", "Cây Sáo", "Cây Khèn"),
                index=None
            )
            
            submitted = st.form_submit_button("Gửi câu trả lời")
            
            if submitted:
                if q1 == "Cầu mong sức khỏe, may mắn" and q2 == "Cây Khèn":
                    st.balloons()
                    st.success("Tuyệt vời! Bạn đã trả lời đúng hết.")
                    # Cộng điểm (Logic giả lập)
                    st.toast("Bạn nhận được +10 Bắp ngô! 🌽")
                else:
                    st.error("Chưa chính xác lắm, hãy thử lại nhé!")

# Vì file này là module con trong thư mục pages, ta chỉ cần hàm app()
# Nếu chạy độc lập để test thì bỏ comment dòng dưới:
# if __name__ == "__main__":
#     app()
