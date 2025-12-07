import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ---------------------
# CẤU HÌNH GEMINI API
# ---------------------
API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

# ---------------------
# HÀM GIẢI BÀI TẬP TỪ ẢNH
# ---------------------
def solve_image(image_data):
    response = model.generate_content(
        [
            "Hãy giải chi tiết bài toán trong ảnh sau:",
            image_data
        ]
    )
    return response.text


# ---------------------
# GIAO DIỆN STREAMLIT
# ---------------------
st.title("🧮 Giải bài tập từ ảnh – Gemini 2.0 Free")

uploaded = st.file_uploader("Tải ảnh bài tập lên:", type=["png", "jpg", "jpeg"])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Ảnh bạn đã tải lên", use_column_width=True)

    # Chuyển ảnh sang dạng Bytes để gửi cho API
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    if st.button("Giải bài tập"):
        with st.spinner("Đang giải bằng Gemini 2.0..."):
            try:
                result = solve_image(img_bytes)
                st.success("🎉 Đã giải xong!")
                st.markdown(result)
            except Exception as e:
                st.error(f"Lỗi: {e}")
