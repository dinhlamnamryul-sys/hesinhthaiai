# ===============================
# 🔑 NHẬP GOOGLE API KEY
# ===============================

with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key để dùng ứng dụng:

1. Truy cập: **https://aistudio.google.com/app/apikey**
2. Đăng nhập Gmail.
3. Nhấn **Create API key**.
4. Copy API Key.
5. Dán vào ô bên dưới.

⚠️ Không chia sẻ API Key cho người khác.
""")

st.subheader("🔐 Nhập Google API Key:")
api_key = st.text_input("Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Nhập API Key để tiếp tục.")
else:
    st.success("✅ API Key hợp lệ!")
import os

# ===============================
# 1. CẤU HÌNH TRANG & GIAO DIỆN
# ===============================
st.set_page_config(
    page_title="Trợ lý Toán học & Giáo dục AI",
    layout="wide",
    page_icon="🎓"
)
st.title("🎓 Trợ lý Giáo dục Đa năng (Gemini AI)")

# --- CSS giao diện ---
st.markdown("""
<style>
.block-container { padding-top: 1rem; }
.stTabs [data-baseweb="tab"] {
    height: 50px;
    border-radius: 6px;
    padding: 10px 20px;
    background-color: #f0f2f6;
}
.stTabs [aria-selected="true"] {
    background-color: #ff4b4b !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 2. 🔑 NHẬP GOOGLE API KEY
# ===============================
with st.expander("🔑 Hướng dẫn lấy Google API Key"):
    st.markdown("""
1. Truy cập: https://aistudio.google.com/app/apikey  
2. Đăng nhập Gmail  
3. Nhấn **Create API key**  
4. Copy và dán vào bên dưới  
⚠️ Không chia sẻ key cho người khác
""")

api_key = st.text_input("🔐 Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Vui lòng nhập API Key")
    st.stop()
else:
    st.success("✅ API Key đã sẵn sàng")

# ===============================
# 3. DỮ LIỆU CHƯƠNG TRÌNH
# ===============================
chuong_options_lop = {
    "Lớp 6": ["Chương I: Số tự nhiên", "Chương VI: Phân số"],
    "Lớp 7": ["Chương I: Số hữu tỉ", "Chương II: Số thực"],
    "Lớp 8": ["Chương I: Đa thức", "Chương IX: Tam giác đồng dạng"],
    "Lớp 9": ["Chương III: Căn bậc hai", "Chương VI: Phương trình bậc hai"]
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
# 4. HÀM GỌI GEMINI API (CHUẨN – KHÔNG LỖI)
# ===============================
def generate_with_gemini(api_key, prompt):
    MODEL = "gemini-1.5-flash-latest"   # ✅ MODEL ĐÚNG
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            return {
                "ok": False,
                "message": f"Lỗi API {response.status_code}: {response.text}"
            }

        data = response.json()

        if "candidates" in data and len(data["candidates"]) > 0:
            return {
                "ok": True,
                "text": data["candidates"][0]["content"]["parts"][0]["text"]
            }

        return {
            "ok": False,
            "message": "Gemini không trả về nội dung."
        }

    except Exception as e:
        return {
            "ok": False,
            "message": str(e)
        }

def create_docx_bytes(text):
    doc = Document()
    doc.add_heading("Tài liệu học tập Toán học AI", 0)
    for line in text.split("\n"):
        doc.add_paragraph(line)
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# ===============================
# 5. GIAO DIỆN TABS
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
        lop_sel = st.selectbox("Lớp:", chuong_options_lop.keys())
    with c2:
        chuong_sel = st.selectbox("Chương:", chuong_options_lop[lop_sel])
    with c3:
        bai_sel = st.selectbox(
            "Bài:",
            bai_options_lop.get(lop_sel, {}).get(chuong_sel, ["Toàn chương"])
        )

    if st.button("🚀 Tổng hợp nội dung"):
        prompt = f"""
Bạn là giáo viên Toán THCS.
Hãy soạn bài: {bai_sel} – {chuong_sel} ({lop_sel})

YÊU CẦU:
1. Công thức viết LaTeX dạng $$...$$
2. Cấu trúc:
- Khái niệm
- Công thức
- Ví dụ
- Bài tập tự luyện
"""
        with st.spinner("Đang tạo nội dung..."):
            res = generate_with_gemini(api_key, prompt)
            if res["ok"]:
                st.session_state["math_content"] = res["text"]
                st.markdown(res["text"])
                st.download_button(
                    "📥 Tải Word",
                    create_docx_bytes(res["text"]),
                    file_name="Toan_AI.docx"
                )
            else:
                st.error(res["message"])

# -------- TAB 2 ----------
with tab2:
    if "math_content" in st.session_state:
        if st.button("✍️ Soạn giáo án 5 bước"):
            prompt = f"Soạn giáo án phát triển năng lực từ nội dung sau:\n{st.session_state['math_content']}"
            res = generate_with_gemini(api_key, prompt)
            if res["ok"]:
                st.markdown(res["text"])
            else:
                st.error(res["message"])
    else:
        st.info("Hãy tạo nội dung ở Tab 1 trước.")

# -------- TAB 3 ----------
with tab3:
    style = st.selectbox("Phong cách:", ["Rap", "Vè", "Pop"])
    if st.button("🎤 Sáng tác"):
        prompt = f"Viết lời bài hát phong cách {style} giúp nhớ kiến thức Toán: {bai_sel}"
        res = generate_with_gemini(api_key, prompt)
        if res["ok"]:
            st.success(res["text"])
        else:
            st.error(res["message"])

# -------- TAB 4 ----------
with tab4:
    tts_text = st.text_area("Nhập văn bản:", "Chào các em học sinh!")
    if st.button("▶️ Đọc"):
        tts = gTTS(text=tts_text, lang="vi")
        tts.save("voice.mp3")
        st.audio("voice.mp3")
