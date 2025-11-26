import streamlit as st
from gtts import gTTS
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap

st.set_page_config(page_title="Đa phương tiện AI hỗ trợ học tập", layout="wide")
st.title("🎨 Đa phương tiện hỗ trợ giáo viên & học sinh (không cần API)")

menu = st.sidebar.radio(
    "Chọn tính năng",
    ["Tạo giọng đọc bài giảng", "Tạo Flashcards", "Tạo infographic đơn giản", "Sinh worksheet bài tập"]
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

    if st.button("Tạo worksheet"):
        if not topic.strip():
            st.warning("Nhập chủ đề!")
        else:
            st.subheader("✏️ Trắc nghiệm (5 câu)")
            for i in range(5):
                st.write(f"{i+1}. {topic}: Câu hỏi trắc nghiệm số {i+1}")

            st.subheader("✍️ Tự luận (5 câu)")
            for i in range(5):
                st.write(f"{i+6}. Viết đoạn giải thích về: {topic} - bài {i+1}")

            st.subheader("📄 Bảng ôn tập nhanh")
            st.info(f"Từ khóa quan trọng của chủ đề **{topic}**:\n- Khái niệm\n- Ví dụ\n- Ứng dụng\n- Công thức")
