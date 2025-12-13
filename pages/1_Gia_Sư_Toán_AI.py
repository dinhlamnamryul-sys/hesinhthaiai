# ================== IMPORT ==================
import streamlit as st
import requests
import json
import re # Bổ sung thư viện re để xử lý chuỗi
from deep_translator import GoogleTranslator

# ================== TRANG ==================
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
### 👉 Cách lấy Google API Key:

1. Truy cập: https://aistudio.google.com/app/apikey  
2. Đăng nhập Gmail  
3. Nhấn **Create API key** 4. Copy và dán vào ô bên dưới  

⚠️ Không chia sẻ API Key cho người khác
""")

api_key = st.text_input("🔐 Nhập Google API Key", type="password")

if not api_key:
    st.warning("⚠️ Vui lòng nhập API Key để sử dụng")
    st.stop()
else:
    st.success("✅ Đã nhập API Key")

# ===============================
# 📌 HÀM GỌI GEMINI (REST API)
# Đã sửa: Chuyển Key sang Header 'x-goog-api-key'
# ===============================
def call_gemini(api_key, prompt):
    # 1. Endpoint không kèm Key (Key được gửi qua Header)
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.0-flash:generateContent"
    )

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt}
            ]
        }]
    }

    # 2. Định nghĩa Headers để gửi Key
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key  # Gửi Key qua Header
    }

    try:
        # Gửi yêu cầu kèm Headers
        res = requests.post(url, headers=headers, json=payload, timeout=60)

        if res.status_code != 200:
            st.error("❌ Không gọi được Gemini API")
            st.code(f"Mã lỗi: {res.status_code}\nPhản hồi lỗi: {res.text}")
            return None

        data = res.json()

        if "candidates" not in data or not data["candidates"]:
            st.error("❌ Gemini không trả về nội dung (có thể do nội dung không an toàn)")
            st.code(data)
            return None

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        st.error("❌ Lỗi kết nối Gemini")
        st.code(str(e))
        return None

# ================== CHƯƠNG TRÌNH HỌC ==================
CHUONG_TRINH_HOC = {
    "Lớp 6": {
        "Chương I. Tập hợp các số tự nhiên": [
            "Bài 1. Tập hợp",
            "Bài 2. Cách ghi số tự nhiên",
            "Bài 3. Thứ tự trong tập hợp các số tự nhiên",
            "Bài 4. Phép cộng và phép trừ số tự nhiên",
            "Bài 5. Phép nhân và phép chia số tự nhiên",
            "Bài 6. Luỹ thừa với số mũ tự nhiên",
            "Bài 7. Thứ tự thực hiện các phép tính"
        ]
    },
    "Lớp 7": {
        "Chương I. Số hữu tỉ": [
            "Bài 1. Tập hợp các số hữu tỉ",
            "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ",
            "Bài 3. Luỹ thừa với số mũ tự nhiên",
            "Bài 4. Quy tắc chuyển vế"
        ]
    },
    "Lớp 8": {
        "Chương I. Đa thức": [
            "Bài 1. Đơn thức",
            "Bài 2. Đa thức",
            "Bài 3. Phép cộng và trừ đa thức",
            "Bài 4. Phép nhân đa thức",
            "Bài 5. Phép chia đa thức cho đơn thức"
        ]
    }
}

# ================== HÀM SINH CÂU HỎI (ĐÃ SỬA LỖI JSON DECODE) ==================
def tao_de_toan(lop, bai):
    prompt = f"""
Bạn là giáo viên Toán Việt Nam, dạy theo SGK Kết nối tri thức.

Hãy tạo 1 câu hỏi trắc nghiệm Toán {lop}
Bài: {bai}

Yêu cầu:
- 4 đáp án A, B, C, D
- Chỉ 1 đáp án đúng
- Phù hợp học sinh THCS
- Có gợi ý giải chi tiết bằng tiếng Việt

TRẢ VỀ DUY NHẤT JSON:
{{
  "question": "...",
  "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "answer": "A",
  "hint_vi": "..."
}}
"""

    text = call_gemini(api_key, prompt)
    if text is None:
        return None

    try:
        # **PHẦN SỬA LỖI JSON DECODE:** Xử lý chuỗi trả về
        # 1. Loại bỏ các thẻ Markdown code fences (```json, ```)
        text = text.strip()
        if text.startswith("```json"):
            text = text.replace("```json", "", 1).strip()
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0].strip()
        
        # 2. Thử tải JSON đã được làm sạch
        return json.loads(text)
        
    except json.JSONDecodeError as e:
        st.error(f"⚠️ AI trả về sai định dạng JSON sau khi làm sạch: {e}")
        st.code(text)
        return None
    except Exception as e:
        st.error(f"⚠️ Lỗi xử lý JSON không xác định: {e}")
        st.code(text)
        return None

# ================== HÀM DỊCH H’MÔNG ==================
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
    st.markdown(cau["question"])

    ans = st.radio("👉 Chọn đáp án", cau["options"])

    if st.button("✅ Kiểm tra"):
        # Đảm bảo ans là chuỗi, bắt đầu bằng chữ cái đáp án
        if ans and ans.startswith(cau["answer"]):
            st.success("🎉 Chính xác! Rất tốt!")
        else:
            st.error("❌ Chưa đúng")
            st.info("💡 **Gợi ý:** " + cau["hint_vi"])
            st.info("🗣️ **Tiếng H’Mông:** " + dich(cau["hint_vi"]))

st.caption("© 2025 – Gia sư Toán AI cho học sinh vùng cao")
