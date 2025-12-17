import requests
import streamlit as st
import time
from io import BytesIO
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
4. Copy API Key  
⚠️ Không chia sẻ API Key
""")

api_key = st.text_input("🔐 Google API Key", type="password")

if not api_key:
    st.warning("⚠️ Vui lòng nhập API Key")
    st.stop()

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
    "Lớp 6": {"Chương VI: Phân số": ["Bài 13", "Bài 14", "Ôn tập"]},
    "Lớp 7": {"Chương I: Số hữu tỉ": ["Bài 1", "Bài 2"]},
    "Lớp 8": {"Chương IX: Tam giác đồng dạng": ["Bài 33", "Bài 34"]},
    "Lớp 9": {"Chương VI: Phương trình bậc hai": ["Bài 19", "Bài 20"]}
}

# ===============================
# 4. HÀM GỌI GEMINI (XỬ LÝ 503)
# ===============================
def generate_with_gemini(prompt, api_key, retry=3):
    MODEL = "gemini-1.5-flash"  # ổn định hơn
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key}"

    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }]
    }

    for attempt in range(retry):
        try:
            response = requests.post(url, json=payload, timeout=60)

            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]

            elif response.status_code == 503:
                time.sleep(2)  # chờ rồi thử lại

            else:
                return f"❌ Lỗi API {response.status_code}\n{response.text}"

        except Exception as e:
            return f"❌ Lỗi kết nối: {e}"

    return "⚠️ Gemini đang quá tải. Thầy/cô vui lòng thử lại sau 1–2 phút."

# ===============================
# 5. TẠO FILE WORD
# ===============================
def create_docx_bytes(text):
    doc = Document()
    doc.add_heading("TÀI LIỆU TOÁN HỌC (AI)", 0)
    for line in text.split("\n"):
        doc.add_paragraph(line)

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# ===============================
# 6. GIAO DIỆN TABS
# ===============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Tổng hợp kiến thức",
    "📝 Soạn giáo án",
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
        bai = st.selectbox("Bài", bai_options_lop[lop][chuong])

    if st.button("🚀 Tổng hợp nội dung"):
        prompt = f"""
Bạn là giáo viên Toán THCS.
Soạn bài {bai} – {chuong} ({lop})

Yêu cầu:
- Ngắn gọn, dễ hiểu
- Có: khái niệm, công thức, ví dụ, bài tập
"""
        with st.spinner("⏳ Đang tạo nội dung..."):
            text = generate_with_gemini(prompt, api_key)
            st.session_state["math_content"] = text
            st.markdown(text)
            st.download_button(
                "📥 Tải file Word",
                create_docx_bytes(text),
                file_name="Toan_AI.docx"
            )

# -------- TAB 2 ----------
with tab2:
    if "math_content" in st.session_state:
        if st.button("✍️ Soạn giáo án 5 bước"):
            prompt = f"Soạn giáo án Toán 5 bước dựa trên:\n{st.session_state['math_content']}"
            with st.spinner("Đang soạn giáo án..."):
                st.markdown(generate_with_gemini(prompt, api_key))
    else:
        st.info("👉 Vui lòng tạo nội dung ở Tab 1 trước.")

# -------- TAB 3 ----------
with tab3:
    style = st.selectbox("Phong cách", ["Rap", "Vè", "Pop"])
    if st.button("🎤 Sáng tác nhạc Toán"):
        prompt = f"Viết bài hát Toán phong cách {style} cho bài {bai}"
        with st.spinner("Đang sáng tác..."):
            st.markdown(generate_with_gemini(prompt, api_key))

# -------- TAB 4 ----------
with tab4:
    tts_text = st.text_area("Nhập văn bản", "Chào các em học sinh!")
    if st.button("▶️ Đọc văn bản"):
        tts = gTTS(text=tts_text, lang="vi")
        tts.save("voice.mp3")
        st.audio("voice.mp3")
