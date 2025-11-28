# file: app_full_gemini.py
import os
import streamlit as st
from gtts import gTTS
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

# Nếu muốn dùng Gemini, cài:
# pip install google-genai

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# ================================
# Cấu hình app
# ================================
st.set_page_config(page_title="Đa phương tiện AI hỗ trợ học tập", layout="wide")
st.title("🎨 Ứng dụng học tập + Google Gemini")

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
# 5. TỔNG HỢP KIẾN THỨC TOÁN BẰNG GEMINI
# ================================
elif menu == "Tổng hợp kiến thức Toán Lớp 1-9":
    st.header("📚 Tổng hợp kiến thức Toán Lớp 1 → 9 bằng Gemini")

    if not GEMINI_AVAILABLE:
        st.warning("Chưa cài google-genai. Chạy: pip install google-genai")
        st.stop()

    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        st.warning("Hãy đặt biến môi trường GEMINI_API_KEY chứa API key của bạn.")
        st.stop()
    genai.configure(api_key=API_KEY)

    grade = st.selectbox("Chọn lớp (1–9):", [str(i) for i in range(1, 10)])
    topic = st.text_input("Chủ đề Toán (ví dụ: phân số, phương trình, diện tích…):", value="")

    if st.button("Lấy kiến thức từ Gemini"):
        if not topic.strip():
            st.warning("Hãy nhập chủ đề Toán!")
        else:
            prompt = f"""Bạn là giáo viên Toán. Viết tóm tắt đầy đủ, rõ ràng cho học sinh lớp {grade} về chủ đề "{topic}". \
Bao gồm: Lý thuyết, Ví dụ minh họa, Công thức (nếu có), 3–5 bài tập mẫu kèm đáp án."""
            
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            st.subheader(f"📄 Kiến thức Toán lớp {grade} — {topic}")
            st.markdown(response.text)
