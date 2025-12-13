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

{
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
    "Chương II. Tính chia hết trong tập hợp các số tự nhiên": [
      "Bài 8. Quan hệ chia hết và tính chất",
      "Bài 9. Dấu hiệu chia hết",
      "Bài 10. Số nguyên tố",
      "Bài 11. Ước chung. Ước chung lớn nhất",
      "Bài 12. Bội chung. Bội chung nhỏ nhất"
    ],
    "Chương III. Số nguyên": [
      "Bài 13. Tập hợp các số nguyên",
      "Bài 14. Phép cộng và phép trừ số nguyên",
      "Bài 15. Quy tắc dấu ngoặc",
      "Bài 16. Phép nhân số nguyên",
      "Bài 17. Phép chia hết. Ước và bội của một số nguyên"
    ],
    "Chương V. Tính đối xứng của hình phẳng trong tự nhiên": [
      "Bài 21. Hình có trục đối xứng",
      "Bài 22. Hình có tâm đối xứng"
    ]
  },

  "Lớp 7": {
    "Chương I. Số hữu tỉ": [
      "Bài 1. Tập hợp các số hữu tỉ",
      "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ",
      "Bài 3. Luỹ thừa với số mũ tự nhiên của một số hữu tỉ",
      "Bài 4. Thứ tự thực hiện các phép tính. Quy tắc chuyển vế"
    ],
    "Chương II. Số thực": [
      "Bài 5. Làm quen với số thập phân vô hạn tuần hoàn",
      "Bài 6. Số vô tỉ. Căn bậc hai số học",
      "Bài 7. Tập hợp các số thực"
    ],
    "Chương III. Góc và đường thẳng song song": [
      "Bài 8. Góc ở vị trí đặc biệt. Tia phân giác của một góc",
      "Bài 9. Hai đường thẳng song song và dấu hiệu nhận biết",
      "Bài 10. Tiên đề Euclid. Tính chất của hai đường thẳng song song",
      "Bài 11. Định lí và chứng minh định lí"
    ],
    "Chương IV. Tam giác bằng nhau": [
      "Bài 12. Tổng các góc trong một tam giác",
      "Bài 13. Hai tam giác bằng nhau. Trường hợp bằng nhau thứ nhất",
      "Bài 14. Trường hợp bằng nhau thứ hai và thứ ba",
      "Bài 15. Các trường hợp bằng nhau của tam giác vuông",
      "Bài 16. Tam giác cân. Đường trung trực của đoạn thẳng"
    ]
  },

  "Lớp 8": {
    "Chương I. Đa thức": [
      "Bài 1. Đơn thức",
      "Bài 2. Đa thức",
      "Bài 3. Phép cộng và phép trừ đa thức",
      "Bài 4. Phép nhân đa thức",
      "Bài 5. Phép chia đa thức cho đơn thức"
    ],
    "Chương II. Hằng đẳng thức đáng nhớ và ứng dụng": [
      "Bài 6. Hiệu hai bình phương. Bình phương của một tổng hay một hiệu",
      "Bài 7. Lập phương của một tổng. Lập phương của một hiệu",
      "Bài 8. Tổng và hiệu hai lập phương",
      "Bài 9. Phân tích đa thức thành nhân tử"
    ],
    "Chương VI. Phân thức đại số": [
      "Bài 21. Phân thức đại số",
      "Bài 22. Tính chất cơ bản của phân thức đại số",
      "Bài 23. Phép cộng và phép trừ phân thức đại số",
      "Bài 24. Phép nhân và phép chia phân thức đại số"
    ],
    "Chương VII. Phương trình bậc nhất và hàm số bậc nhất": [
      "Bài 25. Phương trình bậc nhất một ẩn",
      "Bài 26. Giải bài toán bằng cách lập phương trình",
      "Bài 27. Khái niệm hàm số và đồ thị của hàm số",
      "Bài 28. Hàm số bậc nhất và đồ thị của hàm số",
      "Bài 29. Hệ số góc của đường thẳng"
    ]
  },

  "Lớp 9": {
    "Chương III. Căn bậc hai và căn bậc ba": [
      "Bài 7. Căn bậc hai và căn thức bậc hai",
      "Bài 8. Khai căn bậc hai với phép nhân và phép chia",
      "Bài 9. Biến đổi đơn giản và rút gọn biểu thức chứa căn thức bậc hai",
      "Bài 10. Căn bậc ba và căn thức bậc ba"
    ],
    "Chương IV. Hệ thức lượng trong tam giác vuông": [
      "Bài 11. Tỉ số lượng giác của góc nhọn",
      "Bài 12. Một số hệ thức giữa cạnh, góc trong tam giác vuông và ứng dụng"
    ],
    "Chương VI. Hàm số y = ax² (a ≠ 0). Phương trình bậc hai một ẩn": [
      "Bài 18. Hàm số y = ax² (a ≠ 0)",
      "Bài 19. Phương trình bậc hai một ẩn",
      "Bài 20. Định lí Viète và ứng dụng",
      "Bài 21. Giải bài toán bằng cách lập phương trình"
    ],
    "Chương IX. Đường tròn ngoại tiếp và đường tròn nội tiếp": [
      "Bài 27. Góc nội tiếp",
      "Bài 28. Đường tròn ngoại tiếp và đường tròn nội tiếp của một tam giác",
      "Bài 29. Tứ giác nội tiếp",
      "Bài 30. Đa giác đều"
    ]
  }
}

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
