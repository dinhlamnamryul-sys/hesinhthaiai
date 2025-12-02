# file: 5_Văn_hóa_cội_nguồn.py
import streamlit as st
from pathlib import Path
from datetime import datetime
import os
import traceback

# -----------------------
# Thiết lập đường dẫn an toàn
# -----------------------
BASE = Path(__file__).parent.resolve()  # nơi file .py đang nằm (hữu dụng khi bạn dùng pages/)
STORIES_DIR = BASE / "stories"

# -----------------------
# Mấy truyện mẫu (dùng khi không thể đọc file)
# -----------------------
EMBEDDED_STORIES = [
    "Ngày xưa, trong một bản Mông nọ có chàng trai tên là Khèn và cô gái tên Tớ Dày yêu nhau tha thiết...",
    "Truyện mẫu 2: Vào mùa xuân, hoa rực rỡ khắp nương rẫy, người Mông hát múa đón Tết...",
    "Truyện mẫu 3: Có một em bé lên nương, gặp một cụ già; cụ truyền dạy bài học về lòng hiếu thảo..."
]

# -----------------------
# Hàm đảm bảo thư mục + file mẫu
# -----------------------
def ensure_stories_folder(folder: Path, create_sample_files: bool = True):
    try:
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            if create_sample_files:
                # tạo vài file .txt mẫu để không bị lỗi
                samples = [
                    ("story_1.txt", EMBEDDED_STORIES[0]),
                    ("story_2.txt", EMBEDDED_STORIES[1]),
                    ("story_3.txt", EMBEDDED_STORIES[2]),
                ]
                for fname, content in samples:
                    fp = folder / fname
                    # chỉ tạo nếu chưa có
                    if not fp.exists():
                        fp.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        # Nếu không thể tạo thư mục (ví dụ bị readonly), ghi log cho dev và trả False
        st.warning("⚠️ Không thể tạo thư mục `stories/` tự động. Ứng dụng sẽ dùng truyện mặc định nhúng sẵn.")
        st.write("Chi tiết lỗi (đã ghi lại):")
        st.code(traceback.format_exc())
        return False

# -----------------------
# Hàm đọc truyện từ thư mục
# -----------------------
def load_stories_from_folder(folder: Path):
    stories = []
    try:
        # đảm bảo folder là Path
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder}")
        for f in sorted(folder.glob("*.txt")):
            try:
                txt = f.read_text(encoding="utf-8").strip()
                if txt:
                    stories.append(txt)
            except Exception:
                # nếu đọc 1 file lỗi, bỏ qua file đó
                st.warning(f"Không đọc được file: {f.name}. Bỏ qua file này.")
        return stories
    except Exception as e:
        # trả về rỗng để xử lý bên ngoài
        return []

# -----------------------
# TRY: tạo thư mục nếu cần, rồi đọc truyện
# -----------------------
created = ensure_stories_folder(STORIES_DIR, create_sample_files=True)
all_stories = load_stories_from_folder(STORIES_DIR)

# Nếu không lấy được file nào, fallback về EMBEDDED_STORIES
if not all_stories:
    st.info("Sử dụng truyện mẫu nhúng sẵn vì không tìm thấy file .txt hợp lệ trong 'stories/'.")
    all_stories = EMBEDDED_STORIES.copy()

# -----------------------
# Chọn truyện của ngày (xoay vòng)
# -----------------------
day_index = datetime.now().timetuple().tm_yday
story_today = all_stories[day_index % len(all_stories)]

DATA_STORY = {
    "title": f"🌸 Câu chuyện số {day_index % len(all_stories) + 1}",
    "content_viet": story_today,
    "content_mong": "Phiên bản H'Mông đang được cập nhật..."
}

# -----------------------
# Phần còn lại của app: (giữ nguyên UI, quiz, v.v.)
# -----------------------
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

# CSS + UI (bạn giữ nguyên hoặc thay đổi)
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

st.markdown(f"""
    <div class="header-box">
        <h1>🏛️ DI SẢN BẢN MÔNG</h1>
        <p>Khám phá văn hóa - Tích lũy Bắp Ngô - Đổi quà học tập</p>
    </div>
""", unsafe_allow_html=True)

if 'score' not in st.session_state:
    st.session_state.score = 150

c1, c2 = st.columns([3,1])
with c1:
    st.write(f"👋 Chào em! Hôm nay chúng ta cùng nghe **{DATA_STORY['title']}**")
with c2:
    st.info(f"🌽 Kho bắp ngô: **{st.session_state.score}**")

tab_story, tab_pattern, tab_quiz = st.tabs(["📖 Chuyện kể", "🧵 Hoa văn & Trang phục", "🏆 Thử thách lấy quà"])

with tab_story:
    col_img, col_txt = st.columns([1,2])
    with col_img:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Prunus_cerasoides_flower.jpg/640px-Prunus_cerasoides_flower.jpg", caption="Hoa Tớ Dày báo hiệu mùa xuân")
    with col_txt:
        st.subheader(DATA_STORY["title"])
        # audio placeholder
        st.audio("https://upload.wikimedia.org/wikipedia/commons/transcoded/c/c4/Guzheng_Pingshu_Lotus.ogg/Guzheng_Pingshu_Lotus.ogg.mp3", format="audio/mp3")
        with st.expander("📜 Đọc truyện hôm nay", expanded=True):
            st.markdown(f"**Tiếng Việt:**\n\n{DATA_STORY['content_viet']}")
            st.markdown("---")
            st.markdown(f"**Tiếng H'Mông:**\n\n{DATA_STORY['content_mong']}")

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
