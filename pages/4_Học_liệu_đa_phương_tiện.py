import streamlit as st
from gtts import gTTS
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

# ================================
# Cấu hình app
# ================================
st.set_page_config(page_title="Đa phương tiện AI hỗ trợ học tập", layout="wide")
st.title("🎨 Đa phương tiện hỗ trợ giáo viên & học sinh (không cần API)")

menu = st.sidebar.radio(
    "Chọn tính năng",
    ["Tạo giọng đọc bài giảng", "Tạo Flashcards", "Tạo infographic đơn giản", 
     "Sinh worksheet bài tập", "Tổng hợp kiến thức Toán Lớp 1-9"]
)

# ================================
# 1. TEXT → VOICE
# ================================
if menu == "Tạo giọng đọc bài giảng":
    st.header("🔊 Chuyển văn bản → Giọng đọc AI")

    text = st.text_area("Nhập nội dung bài giảng:", height=200)

    if st.button("Tạo giọng đọc"):
        if not text.strip():
            st.warning("Hãy nhập văn bản!")
        else:
            tts = gTTS(text, lang="vi")
            mp3 = BytesIO()
            tts.write_to_fp(mp3)
            mp3.seek(0)

            st.audio(mp3, format="audio/mp3")
            st.download_button("Tải MP3", data=mp3, file_name="bai_giang.mp3")

# ================================
# 2. FLASHCARDS
# ================================
elif menu == "Tạo Flashcards":
    st.header("📝 Tạo Flashcards từ bài giảng")

    text = st.text_area("Nhập văn bản:", height=250)

    if st.button("Tạo flashcards"):
        if not text.strip():
            st.warning("Nhập nội dung trước!")
        else:
            lines = text.split(".")
            flashcards = [ln.strip() for ln in lines if len(ln.strip()) > 10][:10]

            for i, fc in enumerate(flashcards, 1):
                st.markdown(f"**Flashcard {i}:**")
                st.info(fc)

# ================================
# 3. INFOGRAPHIC GENERATOR
# ================================
elif menu == "Tạo infographic đơn giản":
    st.header("📊 Tạo infographic (poster) đơn giản")

    title = st.text_input("Tiêu đề infographic:")
    content = st.text_area("Nội dung:", height=150)

    if st.button("Tạo ảnh infographic"):
        if not title.strip() or not content.strip():
            st.warning("Hãy nhập tiêu đề và nội dung!")
        else:
            img = Image.new("RGB", (900, 1200), color=(255, 255, 255))
            draw = ImageDraw.Draw(img)

            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

            draw.text((50, 50), title, fill="black", font=title_font)

            wrapped = textwrap.fill(content, width=40)
            draw.text((50, 200), wrapped, fill="black", font=text_font)

            output = BytesIO()
            img.save(output, format="PNG")
            output.seek(0)

            st.image(img, caption="Infographic đã tạo")
            st.download_button("Tải ảnh", data=output, file_name="infographic.png")

# ================================
# 4. WORKSHEET GENERATOR
# ================================
elif menu == "Sinh worksheet bài tập":
    st.header("📘 Sinh worksheet bài tập tự động")

    topic = st.text_input("Chủ đề bài học:")

    # Mẫu câu hỏi cho các chủ đề
    question_bank = {
        "toán": [
            "Tính giá trị của biểu thức: 2 + 3 * 5 = ?",
            "Giải phương trình: x + 5 = 12",
            "Tìm x biết 2x - 3 = 7",
            "Tính diện tích hình chữ nhật dài 5m, rộng 3m",
            "Sắp xếp các số 3, 1, 4, 2 theo thứ tự tăng dần",
            "Tính tổng các số chẵn từ 1 đến 10",
            "Giải phương trình bậc hai: x^2 - 5x + 6 = 0",
            "Tìm giá trị x thỏa mãn 3x + 2 = 11",
            "Tính chu vi hình vuông cạnh 4cm",
            "Một tam giác có các cạnh 3, 4, 5. Tính diện tích"
        ],
        "vật lý": [
            "Nêu định luật I Newton",
            "Tính lực tác dụng lên vật khối lượng 2kg khi gia tốc 3 m/s²",
            "Thế nào là quán tính?",
            "Tính công khi lực 5N dịch chuyển vật 2m",
            "Hiện tượng nào minh họa định luật II Newton?",
            "Định nghĩa năng lượng động học",
            "Công thức tính vận tốc trung bình",
            "Ví dụ về hiện tượng lực ma sát",
            "Tính áp suất khi lực 10N tác dụng lên diện tích 2m²",
            "Nêu định luật III Newton"
        ],
        "hóa học": [
            "Viết công thức hóa học của nước",
            "Nêu nguyên tử khối của Oxi",
            "Tính số mol trong 18g H2O",
            "Phản ứng nào tạo ra CO2",
            "Viết phương trình hóa học của phản ứng Na + H2O",
            "Nêu tính chất của axit HCl",
            "Cho biết các kim loại kiềm là gì",
            "Tính khối lượng mol của CO2",
            "Ví dụ về phản ứng oxi hóa khử",
            "Giải thích hiện tượng sủi bọt khi hòa Na vào nước"
        ]
    }

    if st.button("Tạo worksheet"):
        topic_lower = topic.lower()
        if topic_lower not in question_bank:
            st.warning("Chưa có câu hỏi cho chủ đề này. Hãy thử: toán, vật lý, hóa học")
        else:
            questions = question_bank[topic_lower]

            st.subheader("✏️ Trắc nghiệm (5 câu)")
            for i, q in enumerate(random.sample(questions, 5)):
                st.write(f"{i+1}. {q}")

            st.subheader("✍️ Tự luận (5 câu)")
            for i, q in enumerate(random.sample(questions, 5)):
                st.write(f"{i+6}. Hãy giải thích: {q}")

            st.subheader("📄 Bảng ôn tập nhanh")
            st.info(f"Từ khóa quan trọng của chủ đề **{topic}**:\n- Khái niệm\n- Ví dụ\n- Ứng dụng\n- Công thức")

# ================================
# 5. TỔNG HỢP KIẾN THỨC TOÁN LỚP 1-9
# ================================
elif menu == "Tổng hợp kiến thức Toán Lớp 1-9":
    st.header("📚 Tổng hợp kiến thức Toán Lớp 1 → Lớp 9")

    grade = st.selectbox("Chọn lớp:", [str(i) for i in range(1, 10)])

    # Dữ liệu mẫu Toán Lớp 1-3, bạn có thể mở rộng lên Lớp 9
    knowledge_bank = {
        "1": {
            "Số học": {
                "Lý thuyết": "Số tự nhiên, phép cộng, phép trừ",
                "Ví dụ": "2 + 3 = 5, 5 - 2 = 3",
                "Công thức": "-",
                "Bài tập mẫu": ["Tính 3 + 4 = ?", "Tính 7 - 5 = ?"]
            },
            "Hình học": {
                "Lý thuyết": "Hình vuông, hình chữ nhật",
                "Ví dụ": "Diện tích hình chữ nhật = dài x rộng",
                "Công thức": "Diện tích = dài x rộng",
                "Bài tập mẫu": ["Tính diện tích hình chữ nhật dài 4cm, rộng 3cm"]
            }
        },
        "2": {
            "Số học": {
                "Lý thuyết": "Phép cộng, trừ, nhân chia các số nhỏ",
                "Ví dụ": "5 x 2 = 10, 12 ÷ 3 = 4",
                "Công thức": "-",
                "Bài tập mẫu": ["Tính 6 x 3", "Tính 15 ÷ 5"]
            },
            "Hình học": {
                "Lý thuyết": "Hình tam giác, hình tròn",
                "Ví dụ": "Diện tích tam giác = 1/2 x đáy x cao",
                "Công thức": "S = 1/2 x đáy x cao",
                "Bài tập mẫu": ["Tính diện tích tam giác đáy 6cm, cao 4cm"]
            }
        },
        "3": {
            "Số học": {
                "Lý thuyết": "Số thập phân, phân số cơ bản",
                "Ví dụ": "0.5 + 0.3 = 0.8, 1/2 + 1/3 = 5/6",
                "Công thức": "-",
                "Bài tập mẫu": ["Tính 0.7 + 0.2", "Tính 1/4 + 1/2"]
            },
            "Hình học": {
                "Lý thuyết": "Chu vi, diện tích, hình học cơ bản",
                "Ví dụ": "Chu vi hình vuông = 4 x cạnh",
                "Công thức": "S = cạnh x cạnh",
                "Bài tập mẫu": ["Tính chu vi hình vuông cạnh 5cm"]
            }
        }
    }

    if st.button("Xem kiến thức"):
        if grade not in knowledge_bank:
            st.warning("Chưa có dữ liệu cho lớp này")
        else:
            st.subheader(f"✅ Kiến thức Toán lớp {grade}")
            for topic, info in knowledge_bank[grade].items():
                st.markdown(f"### {topic}")
                st.write(f"**Lý thuyết:** {info['Lý thuyết']}")
                st.write(f"**Ví dụ:** {info['Ví dụ']}")
                st.write(f"**Công thức:** {info['Công thức']}")
                st.write("**Bài tập mẫu:**")
                for bt in info['Bài tập mẫu']:
                    st.write(f"- {bt}")
