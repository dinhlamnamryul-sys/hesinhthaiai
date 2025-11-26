import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import io

# ==========================
# Google API Setup
# ==========================
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="AI Hỗ trợ giáo viên", layout="wide")
st.title("🎓 AI hỗ trợ giáo viên tạo hình ảnh và video")

menu = st.sidebar.radio(
    "Chọn chức năng",
    ["Tạo hình minh hoạ", "Tạo video AI"]
)

# ======================================================
# 1. IMAGE GENERATOR — GOOGLE IMAGEN
# ======================================================
if menu == "Tạo hình minh hoạ":
    st.header("🖼️ Tạo hình minh hoạ bằng Google Imagen 2")

    prompt = st.text_input("Nhập mô tả hình ảnh:")
    if st.button("Tạo hình ảnh"):
        if not prompt.strip():
            st.warning("Bạn phải nhập mô tả!")
        else:
            st.info("⏳ Đang tạo hình ảnh bằng Google AI…")

            img = genai.GenerativeModel("imagen-2.0").generate_image(
                prompt=prompt
            )

            # Chuyển base64 → ảnh
            image_bytes = base64.b64decode(img.images[0])
            image = Image.open(io.BytesIO(image_bytes))

            st.image(image, caption="Kết quả AI tạo", use_column_width=True)

            st.download_button(
                "Tải ảnh xuống",
                data=image_bytes,
                file_name="ai_image.png",
                mime="image/png"
            )

# ======================================================
# 2. VIDEO GENERATOR — GOOGLE VIDEOFX
# ======================================================
elif menu == "Tạo video AI":
    st.header("🎬 Tạo video từ mô tả bằng Google VideoFX")

    prompt = st.text_area("Nhập mô tả video (prompt):", height=150)

    if st.button("Tạo video"):
        if not prompt.strip():
            st.warning("Bạn phải nhập mô tả!")
        else:
            st.info("⏳ Google đang tạo video (khoảng 5–15 giây)…")

            model = genai.GenerativeModel("veo-2.0")  # Model video mới nhất

            result = model.generate_video(
                prompt=prompt,
                duration_seconds=5  # video ngắn, đủ minh họa bài giảng
            )

            video_bytes = result.video

            st.video(video_bytes)

            st.download_button(
                "Tải video",
                data=video_bytes,
                file_name="ai_video.mp4",
                mime="video/mp4"
            )
