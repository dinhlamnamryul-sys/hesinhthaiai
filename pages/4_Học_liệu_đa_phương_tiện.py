# file: app_gemini.py
import os
import streamlit as st

# pip install google-genai streamlit
from google import genai

# === Cấu hình Gemini API key ===
# Bạn có thể đặt biến môi trường GEMINI_API_KEY trước khi chạy:
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY is None:
    st.warning("Hãy đặt biến môi trường GEMINI_API_KEY chứa API key của Gemini.")
    st.stop()
genai.configure(api_key=API_KEY)

# Setup Streamlit
st.set_page_config(page_title="App hỗ trợ học + Gemini", layout="wide")
st.title("📚 Ứng dụng học tập + Google Gemini")

menu = st.sidebar.radio("Chọn tính năng", [
    "Tổng hợp kiến thức Toán (Gemini)",
    # ... bạn có thể thêm các tính năng khác ở đây ...
])

if menu == "Tổng hợp kiến thức Toán (Gemini)":
    st.header("🧮 Tổng hợp kiến thức Toán bằng Gemini")

    grade = st.selectbox("Chọn lớp (1–9):", [str(i) for i in range(1, 10)])
    topic = st.text_input("Chủ đề (ví dụ: phân số, diện tích, phương trình ...):", value="")

    if st.button("Lấy kiến thức từ Gemini"):
        if not topic.strip():
            st.warning("Hãy nhập chủ đề Toán bạn muốn tổng hợp.")
        else:
            prompt = f"""Bạn là một giáo viên Toán. Viết gọn, rõ, có cấu trúc cho học sinh lớp {grade}. \
Hãy tóm tắt lý thuyết về "{topic}", kèm theo:
- Phần **Lý thuyết** (định nghĩa, khái niệm)
- Một vài **ví dụ minh họa**
- Nếu có: **Công thức** liên quan
- Và đề xuất **3–5 bài tập mẫu** để luyện (với đáp án)\n\n"""
            # Gọi Gemini
            model = genai.GenerativeModel("gemini-2.5-flash")
            resp = model.generate_content(prompt)
            result = resp.text.strip()

            st.subheader(f"📄 Nội dung Toán lớp {grade} — {topic}")
            st.markdown(result)
