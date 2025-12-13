# ================== IMPORT ==================
import streamlit as st
import os, json, re, io, base64
from deep_translator import GoogleTranslator
from gtts import gTTS
import google.generativeai as genai

# ================== GEMINI ==================
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ================== TRANG ==================
st.set_page_config(
    page_title="Gia sư Toán AI (KNTT)",
    page_icon="🏔️",
    layout="wide"
)

# ================== CHƯƠNG TRÌNH ==================
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
            "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ"
        ]
    },
    "Lớp 8": {
        "Chương I. Đa thức": [
            "Bài 1. Đơn thức",
            "Bài 2. Đa thức"
        ]
    },
    "Lớp 9": {
        "Chương III. Căn bậc hai": [
            "Bài 7. Căn bậc hai",
            "Bài 8. Khai căn"
        ]
    }
}

# ================== HÀM SINH CÂU HỎI ==================
def tao_de_toan(lop, bai):
    prompt = f"""
Bạn là giáo viên Toán Việt Nam, SGK Kết nối tri thức.

Tạo 1 câu hỏi trắc nghiệm Toán {lop}
Bài: {bai}

Yêu cầu:
- 4 đáp án A B C D
- 1 đáp án đúng
- Có gợi ý

Trả về JSON:
{{
 "question": "...",
 "options": ["A ...","B ...","C ...","D ..."],
 "answer": "A",
 "hint_vi": "..."
}}
"""
    try:
        res = model.generate_content(prompt).text
        data = json.loads(re.search(r"\{.*\}", res, re.S).group())
        return data
    except:
        return None

# ================== HÀM DỊCH ==================
def dich(text):
    try:
        return GoogleTranslator(source="vi", target="hmn").translate(text)
    except:
        return text

# ================== GIAO DIỆN ==================
st.title("🏫 Gia sư Toán AI – SGK KNTT")

lop = st.selectbox("Chọn lớp", CHUONG_TRINH_HOC.keys())
chuong = st.selectbox("Chọn chương", CHUONG_TRINH_HOC[lop].keys())
bai = st.selectbox("Chọn bài", CHUONG_TRINH_HOC[lop][chuong])

if st.button("✨ Tạo câu hỏi"):
    cau = tao_de_toan(lop, bai)
    if cau:
        st.markdown("### ❓ Câu hỏi")
        st.markdown(cau["question"])
        ans = st.radio("Chọn đáp án", cau["options"])
        if st.button("✅ Kiểm tra"):
            if ans.startswith(cau["answer"]):
                st.success("🎉 Chính xác!")
            else:
                st.error("❌ Sai rồi")
                st.info("Gợi ý: " + cau["hint_vi"])
                st.info("H'Mông: " + dich(cau["hint_vi"]))
    else:
        st.error("AI bận, thử lại sau")

st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư")
