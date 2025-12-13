# ================== IMPORT ==================
import streamlit as st
import os
import json
import re
import io
import base64
from deep_translator import GoogleTranslator
from gtts import gTTS
import google.generativeai as genai

# ================== CẤU HÌNH GEMINI ==================
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.4,
        "top_p": 0.9,
        "max_output_tokens": 800
    }
)

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Gia sư Toán AI (KNTT)",
    page_icon="🏔️",
    layout="wide"
)

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
        ],
        "Chương II. Tính chia hết": [
            "Bài 8. Quan hệ chia hết",
            "Bài 9. Dấu hiệu chia hết",
            "Bài 10. Số nguyên tố",
            "Bài 11. Ước chung lớn nhất",
            "Bài 12. Bội chung nhỏ nhất"
        ]
    }
}

# ================== HÀM AI SINH CÂU HỎI ==================
def tao_de_toan(lop, bai_hoc):
    prompt = f"""
Bạn là giáo viên Toán Việt Nam dạy theo SGK Kết nối tri thức.

Hãy tạo 01 câu hỏi TRẮC NGHIỆM Toán {lop}
Bài học: {bai_hoc}

YÊU CẦU:
- Đúng kiến thức SGK
- Phù hợp học sinh vùng cao
- 4 phương án A B C D
- 1 đáp án đúng
- Có gợi ý giải ngắn gọn

TRẢ VỀ JSON:
{{
  "question": "...",
  "options": ["A ...", "B ...", "C ...", "D ..."],
  "answer": "A",
  "hint_vi": "...",
  "hint_math": ""
}}
"""

    try:
        response = model.generate_content(prompt)
        raw = response.text
        json_text = re.search(r'\{.*\}', raw, re.S).group()
        data = json.loads(json_text)

        return (
            data["question"],
            "mcq",
            data["answer"],
            data["options"],
            data["hint_vi"],
            data.get("hint_math", "")
        )

    except Exception:
        return (
            "AI đang bận, vui lòng tạo lại.",
            "mcq",
            "A",
            ["A", "B", "C", "D"],
            "Thử lại sau.",
            ""
        )

# ================== DỊCH GIỮ CÔNG THỨC ==================
def dich_sang_mong_giu_cong_thuc(text):
    parts = re.split(r'(\$.*?\$)', text)
    result = []
    for p in parts:
        if p.startswith("$"):
            result.append(p)
        else:
            try:
                result.append(GoogleTranslator(source="vi", target="hmn").translate(p))
            except:
                result.append(p)
    return "".join(result)

# ================== TEXT TO SPEECH ==================
def text_to_speech_html(text):
    clean = text.replace("$", "")
    tts = gTTS(clean, lang="vi")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    return f"""
    <audio controls autoplay>
    <source src="data:audio/mp3;base64,{b64}">
    </audio>
    """

# ================== GIAO DIỆN ==================
st.title("🏫 GIA SƯ TOÁN AI – SGK KNTT")

with st.sidebar:
    lop = st.selectbox("Lớp", CHUONG_TRINH_HOC.keys())
    chuong = st.selectbox("Chương", CHUONG_TRINH_HOC[lop].keys())
    bai = st.selectbox("Bài học", CHUONG_TRINH_HOC[lop][chuong])

if "de" not in st.session_state:
    st.session_state.de = ""

if st.button("✨ Tạo câu hỏi"):
    de, qt, da, ops, gy, gy_math = tao_de_toan(lop, bai)
    st.session_state.update({
        "de": de,
        "qt": qt,
        "da": da,
        "ops": ops,
        "gy": gy,
        "gy_math": gy_math
    })

if st.session_state.de:
    st.markdown("### ❓ Câu hỏi")
    st.markdown(st.session_state.de)

    ans = st.radio("Chọn đáp án:", st.session_state.ops)

    if st.button("✅ Kiểm tra"):
        if ans.startswith(st.session_state.da):
            st.success("🎉 Chính xác!")
            st.balloons()
        else:
            st.error("❌ Chưa đúng")
            st.markdown(f"**Đáp án đúng:** {st.session_state.da}")
            st.info(f"💡 Gợi ý: {st.session_state.gy}")
            st.info(f"🗣️ H'Mông: {dich_sang_mong_giu_cong_thuc(st.session_state.gy)}")

    if st.button("🔊 Đọc đề"):
        st.markdown(text_to_speech_html(st.session_state.de), unsafe_allow_html=True)

st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư")
