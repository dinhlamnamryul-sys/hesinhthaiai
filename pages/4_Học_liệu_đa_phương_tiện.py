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
        ]
    }

    if st.button("Tạo worksheet"):
        topic_lower = topic.lower()
        if topic_lower not in question_bank:
            st.warning("Chưa có câu hỏi cho chủ đề này. Hãy thử: toán")
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

    # Dữ liệu Toán mẫu cho tất cả lớp 1 → 9
    knowledge_math = {
        "1": {
            "Số học": {"Lý thuyết":"Số tự nhiên, cộng trừ", "Ví dụ":"2+3=5", "Công thức":"-", "Bài tập mẫu":["Tính 3+4","Tính 7-5"]},
            "Hình học": {"Lý thuyết":"Hình vuông, chữ nhật", "Ví dụ":"Diện tích= dài x rộng", "Công thức":"S=dài x rộng", "Bài tập mẫu":["Tính diện tích hình chữ nhật 4x3"]}
        },
        "2": {
            "Số học": {"Lý thuyết":"Cộng trừ nhân chia số nhỏ", "Ví dụ":"5x2=10", "Công thức":"-", "Bài tập mẫu":["Tính 6x3","Tính 15÷5"]},
            "Hình học": {"Lý thuyết":"Hình tam giác, tròn", "Ví dụ":"Diện tích tam giác=1/2 x đáy x cao", "Công thức":"S=1/2 x đáy x cao", "Bài tập mẫu":["Tính diện tích tam giác đáy 6cm cao 4cm"]}
        },
        "3": {
            "Số học": {"Lý thuyết":"Số thập phân, phân số", "Ví dụ":"0.5+0.3=0.8", "Công thức":"-", "Bài tập mẫu":["Tính 0.7+0.2","Tính 1/4+1/2"]},
            "Hình học": {"Lý thuyết":"Chu vi, diện tích cơ bản", "Ví dụ":"Chu vi hình vuông=4 x cạnh", "Công thức":"S=cạnh x cạnh", "Bài tập mẫu":["Tính chu vi hình vuông cạnh 5cm"]}
        },
        "4": {"Số học": {"Lý thuyết":"Số tự nhiên, phân số cơ bản", "Ví dụ":"3/4 + 1/4 = 1", "Công thức":"-", "Bài tập mẫu":["Tính 1/2 + 1/3"]}, "Hình học":{"Lý thuyết":"Hình chữ nhật, tam giác", "Ví dụ":"Diện tích hình chữ nhật= dài x rộng", "Công thức":"S=dài x rộng", "Bài tập mẫu":["Tính diện tích hình chữ nhật 5x4"]}},
        "5": {"Số học": {"Lý thuyết":"Phép cộng, trừ, nhân, chia số lớn", "Ví dụ":"123+456", "Công thức":"-", "Bài tập mẫu":["Tính 123+456"]}, "Hình học":{"Lý thuyết":"Diện tích hình chữ nhật, hình vuông", "Ví dụ":"S= dài x rộng", "Công thức":"S=dài x rộng", "Bài tập mẫu":["Tính diện tích hình vuông cạnh 6"]}},
        "6": {"Số học":{"Lý thuyết":"Số nguyên, phân số, thập phân", "Ví dụ":"1/2 + 0.3", "Công thức":"-", "Bài tập mẫu":["Tính 1/2+0.3"]}, "Hình học":{"Lý thuyết":"Chu vi, diện tích, hình học cơ bản", "Ví dụ":"S= dài x rộng", "Công thức":"S=dài x rộng", "Bài tập mẫu":["Tính diện tích hình chữ nhật 7x3"]}},
        "7": {"Số học":{"Lý thuyết":"Số nguyên, phân số, tỉ lệ", "Ví dụ":"2/3 x 3/4", "Công thức":"-", "Bài tập mẫu":["Tính 2/3 x 3/4"]}, "Hình học":{"Lý thuyết":"Hình học phẳng cơ bản", "Ví dụ":"Chu vi, diện tích", "Công thức":"S= ...", "Bài tập mẫu":["Tính diện tích hình tam giác đáy 5 cao 4"]}},
        "8": {"Số học":{"Lý thuyết":"Hàm số, đại số cơ bản", "Ví dụ":"y=2x+3", "Công thức":"-", "Bài tập mẫu":["Tính giá trị khi x=5"]}, "Hình học":{"Lý thuyết":"Hình học phẳng nâng cao", "Ví dụ":"Chu vi, diện tích", "Công thức":"S= ...", "Bài tập mẫu":["Tính diện tích hình thang đáy 6, đáy 4, cao 3"]}},
        "9": {"Số học":{"Lý thuyết":"Hàm số, phương trình bậc hai", "Ví dụ":"x^2-5x+6=0", "Công thức":"-", "Bài tập mẫu":["Giải phương trình x^2-5x+6=0"]}, "Hình học":{"Lý thuyết":"Hình học không gian cơ bản", "Ví dụ":"Thể tích, diện tích", "Công thức":"V= ...", "Bài tập mẫu":["Tính thể tích hình lập phương cạnh 3"]}}
    }

    if st.button("Xem kiến thức"):
        if grade not in knowledge_math:
            st.warning(f"Chưa có dữ liệu Toán cho lớp {grade}")
        else:
            st.subheader(f"✅ Kiến thức Toán lớp {grade}")
            for topic, info in knowledge_math[grade].items():
                st.markdown(f"### {topic}")
                st.write(f"**Lý thuyết:** {info['Lý thuyết']}")
                st.write(f"**Ví dụ:** {info['Ví dụ']}")
                st.write(f"**Công thức:** {info['Công thức']}")
                st.write("**Bài tập mẫu:**")
                for bt in info['Bài tập mẫu']:
                    st.write(f"- {bt}")
