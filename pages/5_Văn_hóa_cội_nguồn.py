import streamlit as st
import os
from datetime import datetime

# ============================
# 1. HÀM ĐỌC TRUYỆN TỪ FILE
# ============================
def load_stories(folder="stories"):
    stories = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                stories.append(f.read())
    return stories

# Lấy danh sách truyện
all_stories = load_stories()

if not all_stories:
    st.error("❌ Không tìm thấy truyện nào trong thư mục 'stories/'. Hãy thêm file .txt vào!")
    st.stop()

# Chọn truyện theo ngày (xoay vòng)
day_index = datetime.now().timetuple().tm_yday
story_today = all_stories[day_index % len(all_stories)]

# Dữ liệu story cho hôm nay
DATA_STORY = {
    "title": f"🌸 Câu chuyện số {day_index % len(all_stories) + 1}",
    "content_viet": story_today,
    "content_mong": "Phiên bản tiếng H’Mông đang được cập nhật..."
}

# ============================
# 2. QUIZ DATA
# ============================
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
        "explanation": "Chính xác! Váy xòe xếp ly uyển chuyển như một bông hoa."
    },
    {
        "question": "Nhạc cụ nào sau đây KHÔNG PHẢI của người H'Mông?",
        "options": ["Khèn (Qeej)", "Đàn Đáy", "Sáo Mông"],
        "answer": "Đàn Đáy",
        "explanation": "Đúng! Đàn Đáy là nhạc cụ của người Kinh, không phải của người Mông."
    }
]

# ============================
# 3. GIAO DIỆN CSS
# ============================
st.markdown("""
    <style>
    .main { background-color: #fffbf0; }

    .header-box {
        background: linear-gradient(90deg, #b71c1c, #d32f2f);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.25);
    }

    .quiz-card {
        background-color: white;
        padding: 15px;
        border-left: 5px solid #d32f2f;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ============================
# 4. HEADER
# ============================
st.markdown(f"""
    <div class="header-box">
        <h1>🏛️ DI SẢN BẢN MÔNG</h1>
        <p>Khám phá văn hóa - Tích lũy Bắp Ngô - Đổi quà học tập</p>
    </div>
""", unsafe_allow_html=True)

# Quản lý điểm
if 'score' not in st.session_state:
    st.session_state.score = 150

# ============================
# 5. THÔNG TIN CHUNG
# ============================
c1, c2 = st.columns([3, 1])
with c1:
    st.write(f"👋 Chào em! Hôm nay chúng ta cùng nghe **{DATA_STORY['title']}**")
with c2:
    st.info(f"🌽 Kho bắp ngô: **{st.session_state.score}**")

tab_story, tab_pattern, tab_quiz = st.tabs(["📖 Chuyện kể", "🧵 Hoa văn & Trang phục", "🏆 Thử thách lấy quà"])

# ============================
# 6. TAB 1 – STORY
# ============================
with tab_story:
    col_img, col_txt = st.columns([1, 2])
    with col_img:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Prunus_cerasoides_flower.jpg/640px-Prunus_cerasoides_flower.jpg", caption="Hoa Tớ Dày báo hiệu mùa xuân")

    with col_txt:
        st.subheader(DATA_STORY["title"])
        st.audio("https://upload.wikimedia.org/wikipedia/commons/transcoded/c/c4/Guzheng_Pingshu_Lotus.ogg/Guzheng_Pingshu_Lotus.ogg.mp3", format="audio/mp3")

        with st.expander("📜 Đọc truyện hôm nay", expanded=True):
            st.markdown(f"**Tiếng Việt:**\n\n{DATA_STORY['content_viet']}")
            st.markdown("---")
            st.markdown(f"**Tiếng H'Mông:**\n\n{DATA_STORY['content_mong']}")

# ============================
# 7. TAB 2 – HOA VĂN
# ============================
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
            st.write("Cây Khèn vừa là nhạc cụ, vừa là đạo cụ múa, thể hiện bản lĩnh của chàng trai Mông.")

    with c_p3:
        st.markdown("### 💡 Bạn có biết?")
        st.info("Người Mông dùng sáp ong vẽ hoa văn lên vải trước khi nhuộm chàm – tạo nên màu trắng xanh đặc trưng rất bền.")

# ============================
# 8. TAB 3 – QUIZ
# ============================
with tab_quiz:
    st.subheader("🎯 Trả lời đúng nhận ngay 10 Bắp Ngô/câu")

    for i, item in enumerate(DATA_QUIZ):
        st.markdown(f"<div class='quiz-card'><strong>Câu {i+1}:</strong> {item['question']}</div>", unsafe_allow_html=True)

        user_choice = st.radio(f"Đáp án câu {i+1}:", item['options'], key=f"q_{i}", label_visibility="collapsed")

        if st.button(f"Trả lời câu {i+1}", key=f"btn_{i}"):
            if user_choice == item['answer']:
                st.balloons()
                st.success(item['explanation'])
                st.session_state.score += 10
            else:
                st.error("Tiếc quá, chưa đúng rồi. Em thử lại nhé!")
