import streamlit as st
import requests
import json
from deep_translator import GoogleTranslator

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Gia sư Toán AI (KNTT)",
    page_icon="🏔️",
    layout="wide"
)

# =====================
# 🔑 NHẬP GOOGLE API KEY
# =====================
with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key
1. Truy cập: https://aistudio.google.com/app/apikey  
2. Đăng nhập Gmail  
3. Nhấn **Create API key**  
4. Copy và dán vào ô bên dưới  

⚠️ Không chia sẻ API Key
""")

api_key = st.text_input("🔐 Nhập Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Vui lòng nhập API Key để tiếp tục.")
    st.stop()
else:
    st.success("✅ Đã nhập API Key")

# ===============================
# 📌 HÀM GỌI GEMINI (TEXT ONLY)
# ===============================
def call_gemini(api_key, prompt):
    url = (
        "https://generativelanguage.googleapis.com/v1/"
        f"models/gemini-1.5-flash:generateContent?key={api_key}"
    )

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    res = requests.post(url, json=payload)
    if res.status_code != 200:
        raise Exception(res.text)

    data = res.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

# ================== CHƯƠNG TRÌNH HỌC ==================
CHUONG_TRINH_HOC = {
    "Lớp 6": {
        "Chương I. Tập hợp các số tự nhiên": [
            "Bài 1. Tập hợp",
            "Bài 2. Cách ghi số tự nhiên",
            "Bài 3. Thứ tự trong tập hợp các số tự nhiên"
        ]
    },
    "Lớp 8": {
        "Chương VI. Phân thức đại số": [
            "Bài 21. Phân thức đại số",
            "Bài 22. Tính chất cơ bản",
            "Bài 23. Cộng trừ phân thức",
            "Bài 24. Nhân chia phân thức"
        ]
    }
}

# ================== SINH CÂU HỎI ==================
def tao_de_toan(lop, bai):
    prompt = f"""
Bạn là giáo viên Toán Việt Nam.

Tạo 1 câu hỏi trắc nghiệm Toán {lop}
Bài: {bai}

Yêu cầu:
- 4 đáp án A, B, C, D
- 1 đáp án đúng
- Có gợi ý giải

TRẢ VỀ DUY NHẤT JSON:
{{
  "question": "...",
  "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "answer": "A",
  "hint_vi": "..."
}}
"""

    text = call_gemini(api_key, prompt)
    return json.loads(text)

# ================== DỊCH H’MÔNG ==================
def dich(text):
    try:
        return GoogleTranslator(source="vi", target="hmn").translate(text)
    except:
        return "Không dịch được."

# ================== GIAO DIỆN ==================
st.title("🏫 Gia sư Toán AI – SGK Kết nối tri thức")

if "cau" not in st.session_state:
    st.session_state.cau = None

lop = st.selectbox("📘 Chọn lớp", CHUONG_TRINH_HOC.keys())
chuong = st.selectbox("📗 Chọn chương", CHUONG_TRINH_HOC[lop].keys())
bai = st.selectbox("📙 Chọn bài", CHUONG_TRINH_HOC[lop][chuong])

if st.button("✨ Tạo câu hỏi"):
    with st.spinner("⏳ Đang tạo câu hỏi..."):
        st.session_state.cau = tao_de_toan(lop, bai)

if st.session_state.cau:
    cau = st.session_state.cau

    st.markdown("### ❓ Câu hỏi")
    st.write(cau["question"])

    ans = st.radio("👉 Chọn đáp án", cau["options"])

    if st.button("✅ Kiểm tra"):
        if ans.startswith(cau["answer"]):
            st.success("🎉 Chính xác!")
        else:
            st.error("❌ Chưa đúng")
            st.info("💡 Gợi ý: " + cau["hint_vi"])
            st.info("🗣️ H’Mông: " + dich(cau["hint_vi"]))

st.caption("© 2025 – Gia sư Toán AI cho học sinh vùng cao")
