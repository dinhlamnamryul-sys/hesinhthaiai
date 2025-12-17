import streamlit as st
import requests
from io import BytesIO
from docx import Document
from gtts import gTTS

# ===============================
# CẤU HÌNH TRANG
# ===============================
st.set_page_config(
    page_title="Tro ly Giao duc AI",
    layout="wide"
)

st.title("🎓 Trợ lý Giáo dục Đa năng (Gemini AI)")

# ===============================
# NHẬP GOOGLE API KEY
# ===============================
with st.expander("Huong dan lay Google API Key"):
    st.markdown(
        "1. Truy cap https://aistudio.google.com/app/apikey\n"
        "2. Dang nhap Gmail\n"
        "3. Create API key\n"
        "4. Copy va dan vao ben duoi"
    )

api_key = st.text_input("Google API Key", type="password")

if not api_key:
    st.warning("Nhap API Key de tiep tuc")
    st.stop()

st.success("API Key hop le")

# ===============================
# HAM GOI GEMINI
# ===============================
def generate_with_gemini(prompt, api_key):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-1.5-flash-001:generateContent"
        "?key=" + api_key
    )

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    r = requests.post(url, json=payload, timeout=60)

    if r.status_code != 200:
        return "Loi API: " + r.text

    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

# ===============================
# TAB
# ===============================
tab1, tab2 = st.tabs(["Tong hop kien thuc", "Doc van ban"])

with tab1:
    if st.button("Tong hop noi dung"):
        prompt = "Hay giai thich phan so cho hoc sinh lop 6"
        with st.spinner("Dang xu ly..."):
            text = generate_with_gemini(prompt, api_key)
            st.markdown(text)

with tab2:
    txt = st.text_area("Nhap van ban", "Chao cac em hoc sinh")
    if st.button("Doc"):
        tts = gTTS(text=txt, lang="vi")
        tts.save("voice.mp3")
        st.audio("voice.mp3")
