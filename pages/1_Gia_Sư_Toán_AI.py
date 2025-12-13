# ================== IMPORT ==================
import streamlit as st
import os, json
from deep_translator import GoogleTranslator
import google.generativeai as genai

# ================== GEMINI ==================
if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ Không tìm thấy GOOGLE_API_KEY. Vui lòng thiết lập biến môi trường.")
    st.stop()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.0-pro")


# ================== TRANG ==================
st.set_page_config(
    page_title="Gia sư Toán AI (KNTT)",
    page_icon="🏔️",
    layout="wide"
)

# ================== CHƯƠNG TRÌNH HỌC ==================
CHUONG_TRINH_HOC = {
    "Lớp 6": {
        "Chương I. Tập hợp các số tự nhiên": [
            "Bài 1. Tập hợp", "Bài 2. Cách ghi số tự nhiên",
            "Bài 3. Thứ tự trong tập hợp các số tự nhiên",
            "Bài 4. Phép cộng và phép trừ số tự nhiên",
            "Bài 5. Phép nhân và phép chia số tự nhiên",
            "Bài 6. Luỹ thừa với số mũ tự nhiên",
            "Bài 7. Thứ tự thực hiện các phép tính"
        ],
        "Chương II. Tính chia hết trong tập hợp các số tự nhiên": [
            "Bài 8. Quan hệ chia hết và tính chất",
            "Bài 9. Dấu hiệu chia hết",
            "Bài 10. Số nguyên tố",
            "Bài 11. Ước chung. Ước chung lớn nhất",
            "Bài 12. Bội chung. Bội chung nhỏ nhất"
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
        ],
        "Chương VI. Phân thức đại số": [
            "Bài 21. Phân thức đại số",
            "Bài 22. Tính chất cơ bản",
            "Bài 23. Cộng trừ phân thức",
            "Bài 24. Nhân chia phân thức"
        ]
    }
}

# ================== HÀM SINH CÂU HỎI ==================
def tao_de_toan(lop, bai):
    prompt = f"""
Bạn là giáo viên Toán Việt Nam, dạy theo SGK Kết nối tri thức.

Hãy tạo 1 câu hỏi trắc nghiệm Toán {lop}
Bài: {bai}

Yêu cầu:
- Có 4 đáp án A, B, C, D
- Chỉ có 1 đáp án đúng
- Mức độ phù hợp học sinh THCS
- Có gợi ý giải chi tiết bằng tiếng Việt

TRẢ VỀ DUY NHẤT JSON theo mẫu:
{{
  "question": "...",
  "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "answer": "A",
  "hint_vi": "..."
}}

Không thêm bất kỳ chữ nào ngoài JSON.
"""

    try:
        res = model.generate_content(prompt)
        return json.loads(res.text)

    except json.JSONDecodeError:
        st.error("⚠️ AI trả về sai định dạng JSON. Hãy bấm tạo lại.")
        st.code(res.text)
        return None

    except Exception as e:
        st.error(f"❌ Lỗi AI: {e}")
        return None

# ================== HÀM DỊCH SANG TIẾNG H’MÔNG ==================
def dich(text):
    try:
        if not text:
            return ""
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
        if ans.startswith(cau["answer"]):
            st.success("🎉 Chính xác! Làm rất tốt!")
        else:
            st.error("❌ Chưa đúng")
            st.info("💡 **Gợi ý:** " + cau["hint_vi"])
            st.info("🗣️ **Tiếng H’Mông:** " + dich(cau["hint_vi"]))

st.caption("© 2025 – Gia sư Toán AI cho học sinh vùng cao")
