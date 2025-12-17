# ===============================
# 0. IMPORT THƯ VIỆN
# ===============================
import streamlit as st
import requests
import io
import os
from docx import Document
from gtts import gTTS

# ===============================
# 1. CẤU HÌNH TRANG
# ===============================
st.set_page_config(
    page_title="Trợ lý Giáo dục AI (Gemini)",
    layout="wide",
    page_icon="🎓"
)

st.title("🎓 Trợ lý Giáo dục Đa năng (Gemini AI)")

# ===============================
# 2. NHẬP GOOGLE API KEY
# ===============================
with st.expander("🔑 Hướng dẫn lấy Google API Key"):
    st.markdown("""
1. Truy cập: https://aistudio.google.com/app/apikey  
2. Đăng nhập Gmail  
3. Nhấn **Create API key**  
4. Copy và dán vào bên dưới  
⚠️ Không chia sẻ key cho người khác
""")

api_key = st.text_input("🔐 Google API Key", type="password")

if not api_key:
    st.warning("⚠️ Vui lòng nhập API Key để tiếp tục")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key
st.success("✅ API Key đã sẵn sàng")

# ===============================
# 3. DỮ LIỆU CHƯƠNG – BÀI
# ===============================
chuong_options_lop = {
    "Lớp 6": ["Chương VI: Phân số"],
    "Lớp 7": ["Chương I: Số hữu tỉ"],
    "Lớp 8": ["Chương IX: Tam giác đồng dạng"],
    "Lớp 9": ["Chương VI: Phương trình bậc hai"]
}

bai_options_lop = {
    "Lớp 6": {
        "Chương VI: Phân số": ["Bài 13", "Bài 14", "Ôn tập"]
    },
    "Lớp 7": {
        "Chương I: Số hữu tỉ": ["Bài 1", "Bài 2"]
    },
    "Lớp 8": {
        "Chương IX: Tam giác đồng dạng": ["Bài 33", "Bài 34"]
    },
    "Lớp 9": {
        "Chương VI: Phương trình bậc hai": ["Bài 19", "Bài 20"]
    }
}

# ===============================
# 4. HÀM GỌI GEMINI API
# ===============================
def generate_with_gemini(prompt):
    MODEL = "gemini-1.5-flash-latest"
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"

    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }]
    }

    try:
        res = requests.post(url, json=payload, timeout=120)
        data = res.json()

        if "candidates" not in data:
            return None

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"Lỗi: {e}"

# ===============================
# 5. TẠO FILE WORD
# ===============================
def create_docx_bytes(text):
    doc = Document()
    doc.add_heading("TÀI LIỆU TOÁN HỌC AI", 0)
    for line in text.split("\n"):
        doc.add_paragraph(line)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# ===============================
# 6. GIAO DIỆN TABS
# ===============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Tổng hợp kiến thức",
    "📝 Thiết kế giáo án",
    "🎵 Nhạc Toán",
    "🎧 Đọc văn bản"
])

# -------- TAB 1 ----------
with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        lop = st.selectbox("Lớp", chuong_options_lop.keys())
    with c2:
        chuong = st.selectbox("Chương", chuong_options_lop[lop])
    with c3:
        bai = st.selectbox(
            "Bài",
            bai_options_lop.get(lop, {}).get(chuong, ["Toàn chương"])
        )

    if st.button("🚀 Tổng hợp nội dung"):
        prompt = f"""
Bạn là giáo viên Toán THCS.
Hãy soạn bài: {bai} – {chuong} ({lop})

Yêu cầu:
- Khái niệm
- Công thức (LaTeX $$ $$)
- Ví dụ
- Bài tập tự luyện
"""
        with st.spinner("Đang tạo nội dung..."):
            text = generate_with_gemini(prompt)
            if text:
                st.session_state["math_content"] = text
                st.markdown(text)
                st.download_button(
                    "📥 Tải Word",
                    create_docx_bytes(text),
                    "Toan_AI.docx"
                )

# -------- TAB 2 ----------
with tab2:
    if "math_content" in st.session_state:
        if st.button("✍️ Soạn giáo án 5 bước"):
            prompt = f"Soạn giáo án phát triển năng lực từ nội dung sau:\n{st.session_state['math_content']}"
            st.markdown(generate_with_gemini(prompt))
    else:
        st.info("Hãy tạo nội dung ở Tab 1 trước.")

# -------- TAB 3 ----------
with tab3:
    style = st.selectbox("Phong cách", ["Rap", "Vè", "Pop"])
    if st.button("🎤 Sáng tác"):
        prompt = f"Viết lời bài hát Toán học phong cách {style} cho bài {bai}"
        st.markdown(generate_with_gemini(prompt))

# -------- TAB 4 ----------
with tab4:
    text = st.text_area("Nhập văn bản cần đọc", "Chào các em học sinh!")
    if st.button("▶️ Đọc"):
        tts = gTTS(text=text, lang="vi")
        tts.save("voice.mp3")
        st.audio("voice.mp3")
