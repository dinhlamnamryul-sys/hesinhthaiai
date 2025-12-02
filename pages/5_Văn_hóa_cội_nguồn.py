import streamlit as st
from pathlib import Path
from datetime import datetime
import traceback

# -----------------------
# Thiết lập đường dẫn an toàn
# -----------------------
BASE = Path(__file__).parent.resolve() 
STORIES_DIR = BASE / "stories"

# -----------------------
# SỬA LẠI: NỘI DUNG TRUYỆN ĐẦY ĐỦ
# -----------------------
# Tôi đã viết đầy đủ sự tích vào đây thay vì chỉ để tóm tắt
FULL_STORY_1 = """Ngày xưa, ở một bản Mông nọ, có một chàng trai tên là Khèn và một cô gái tên là Tớ Dày. Họ yêu nhau tha thiết như đôi chim rừng quấn quýt. Chàng thổi khèn hay, nàng múa đẹp, tiếng khèn và điệu múa của họ làm say đắm cả núi rừng.

Nhưng nhà chàng Khèn nghèo quá, bố mẹ Tớ Dày không ưng thuận. Họ ép cô phải lấy con trai nhà thống lý giàu có trong vùng. Tớ Dày kiên quyết không chịu, nàng buồn bã bỏ chạy lên rừng để tìm đường đến với người yêu.

Cô cứ đi mãi, đi mãi, vượt qua bao nhiêu ngọn núi, con suối. Cuối cùng, vì kiệt sức và lạnh giá, cô đã gục xuống bên vách đá. Tại nơi cô nằm xuống, bỗng mọc lên một loài cây thân cành khẳng khiu nhưng tràn đầy sức sống.

Cứ mỗi độ xuân về, khi cái rét ngọt tràn về bản, loài cây ấy lại nở ra những bông hoa 5 cánh đỏ thắm như máu con tim, đẹp rực rỡ cả một góc trời, như vẻ đẹp rực rỡ của cô gái Tớ Dày năm nào.

Người Mông gọi đó là hoa Tớ Dày (Pang Tớ Dày). Hoa nở báo hiệu mùa xuân, mùa của tình yêu đôi lứa và mùa Tết của người Mông sắp về."""

EMBEDDED_STORIES = [
    FULL_STORY_1,
    "Truyện mẫu 2: Vào mùa xuân, hoa rực rỡ khắp nương rẫy, người Mông hát múa đón Tết. Tiếng khèn vang vọng khắp núi rừng báo hiệu một năm mới ấm no...",
    "Truyện mẫu 3: Có một em bé lên nương, gặp một cụ già; cụ truyền dạy bài học về lòng hiếu thảo và tình yêu thương thiên nhiên..."
]

# -----------------------
# Hàm đảm bảo thư mục + file mẫu
# -----------------------
def ensure_stories_folder(folder: Path, create_sample_files: bool = True):
    try:
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            if create_sample_files:
                samples = [
                    ("story_1.txt", EMBEDDED_STORIES[0]),
                    ("story_2.txt", EMBEDDED_STORIES[1]),
                    ("story_3.txt", EMBEDDED_STORIES[2]),
                ]
                for fname, content in samples:
                    fp = folder / fname
                    if not fp.exists():
                        fp.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        st.warning("⚠️ Không thể tạo thư mục `stories/`. Dùng truyện nhúng sẵn.")
        return False

# -----------------------
# Hàm đọc truyện từ thư mục
# -----------------------
def load_stories_from_folder(folder: Path):
    stories = []
    try:
        if not folder.exists(): 
            return []
        for f in sorted(folder.glob("*.txt")):
            try:
                txt = f.read_text(encoding="utf-8").strip()
                if txt: stories.append(txt)
            except: pass
        return stories
    except: return []

# -----------------------
# LOGIC CHÍNH
# -----------------------
ensure_stories_folder(STORIES_DIR, create_sample_files=True)
all_stories = load_stories_from_folder(STORIES_DIR)

if not all_stories:
    all_stories = EMBEDDED_STORIES.copy()

# Chọn truyện theo ngày
day_index = datetime.now().timetuple().tm_yday
story_today = all_stories[day_index % len(all_stories)]

# Nếu truyện hôm nay quá ngắn (do code cũ lưu file), lấy lại nội dung đầy đủ từ biến code
if len(story_today) < 100 and (day_index % len(all_stories)) == 0:
    story_today = FULL_STORY_1

DATA_STORY = {
    "title": f"🌸 Câu chuyện số {(day_index % len(all_stories)) + 1}: Sự tích hoa Tớ Dày",
    "content_viet": story_today,
    "content_mong": "Zaj dab neeg Txiv ntoo Tớ Dày (Đang cập nhật...)"
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
        "explanation": "Chính xác! Váy xòe xếp ly uyển chuyển như một bông hoa."
    },
    {
        "question": "Nhạc cụ nào sau đây KHÔNG PHẢI của người H'Mông?",
        "options": ["Khèn (Qeej)", "Đàn Đáy", "Sáo Mông"],
        "answer": "Đàn Đáy",
        "explanation": "Đúng! Đàn Đáy là nhạc cụ của người Kinh (thường dùng trong Ca Trù), không phải của người Mông."
    }
]

# -----------------------
# GIAO DIỆN (UI)
# -----------------------
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
        color: #333;
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
        
        # --- SỬA LẠI LINK AUDIO ---
        # Dùng link nhạc mẫu ổn định hơn (tiếng sáo/nhạc nhẹ)
        # Nếu muốn dùng file của bạn, hãy tải file mp3 lên cùng thư mục và đổi thành: st.audio("ten_file.mp3")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3", format="audio/mp3", start_time=0)
        st.caption("🎵 Bấm nút Play để nghe nhạc nền khi đọc truyện")

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
        # Sử dụng index để tạo key duy nhất tránh lỗi Duplicate Widget ID
        user_choice = st.radio(f"Lựa chọn câu {i+1}", item['options'], key=f"q_{i}", label_visibility="collapsed")
        
        if st.button(f"Trả lời câu {i+1}", key=f"btn_{i}"):
            if user_choice == item['answer']:
                st.balloons()
                st.success(item['explanation'])
                st.session_state.score += 10
            else:
                st.error("Tiếc quá, chưa đúng rồi. Em thử lại nhé!")
