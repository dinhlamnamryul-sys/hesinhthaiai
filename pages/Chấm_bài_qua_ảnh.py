import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Chấm bài qua ảnh AI", page_icon="📸", layout="wide")

st.title("📸 CHẤM BÀI QUA ẢNH – AI TỰ ĐỘNG CHẤM & NHẬN XÉT")

# -------- LẤY API KEY --------
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.text_input("Nhập Google API Key:", type="password")

# -------- HÀM GỌI GEMINI --------
def call_gemini_image(api_key, prompt_text, image_file):
    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

    # Mã hóa ảnh Base64
    img_bytes = image_file.read()
    img_base64 = base64.b64encode(img_bytes).decode()

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt_text},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_base64
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        return f"❌ Lỗi API {response.status_code}: {response.text}"

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

# -------- GIAO DIỆN -----------
st.subheader("📤 Tải ảnh bài làm học sinh")
uploaded_img = st.file_uploader("Chọn ảnh (JPG/PNG)", type=["jpg", "jpeg", "png"])

dap_an_gv = st.text_area(
    "📘 Nhập đáp án chuẩn (tùy chọn, nếu bỏ trống AI tự tạo đáp án)",
    height=150,
    placeholder="VD: 1.A  2.B  3.C  4.D...\nHoặc bài tự luận mẫu..."
)

if st.button("🎯 Chấm bài ngay"):
    if not api_key:
        st.error("❌ Bạn chưa nhập API Key!")
    elif not uploaded_img:
        st.error("❌ Bạn chưa tải ảnh bài làm học sinh!")
    else:
        with st.spinner("⏳ AI đang phân tích và chấm bài..."):
            prompt = f"""
Bạn là giáo viên bộ môn Toán – rất giỏi trong việc chấm bài.
Hãy chấm bài làm của học sinh theo yêu cầu sau:

1. Nhận diện nội dung trong ảnh (OCR chính xác).
2. Nếu giáo viên đã nhập đáp án chuẩn, hãy chấm theo đáp án đó.
3. Nếu giáo viên KHÔNG nhập đáp án → tự tạo đáp án đúng.
4. Kết quả xuất ra theo format:

----- BÀI LÀM HỌC SINH -----
(nội dung AI đọc từ ảnh)

----- NHẬN XÉT & CHẤM ĐIỂM -----
- Số câu đúng
- Số câu sai
- Những lỗi sai cụ thể
- Giải thích vì sao sai
- Điểm cuối cùng (thang 10)

----- ĐÁP ÁN CHUẨN -----
(danh sách đáp án rõ ràng)

Hãy trả lời ngắn gọn – rõ ràng – đúng trọng tâm.
Đáp án chuẩn giáo viên nhập:
{dap_an_gv}
"""

            result = call_gemini_image(api_key, prompt, uploaded_img)

        st.success("🎉 Đã chấm xong bài!")
        st.markdown("### 📄 Kết quả chấm bài")
        st.markdown(result)

        # Hiển thị ảnh đã upload
        st.markdown("### 🖼️ Ảnh bài làm học sinh")
        img = Image.open(uploaded_img)
        st.image(img, use_column_width=True)
