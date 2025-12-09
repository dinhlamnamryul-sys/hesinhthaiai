import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import json

st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông)")

# =====================
# 🔑 NHẬP GOOGLE API KEY
# =====================

with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key để dùng ứng dụng:

1. Truy cập trang:  
   **https://aistudio.google.com/app/apikey**

2. Đăng nhập bằng Gmail.

3. Nhấn **Create API key**.

4. Copy API Key và dán vào ô bên dưới.

⚠️ **Không chia sẻ API Key cho người khác.**
    """)

st.subheader("🔐 Nhập Google API Key của bạn:")
api_key = st.text_input("Nhập Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Bạn cần nhập API Key để sử dụng ứng dụng.")
else:
    st.success("✅ API Key đã được nhập!")


# ===============================
# 📌 HÀM PHÂN TÍCH ẢNH VỚI GEMINI
# ===============================

def analyze_real_image(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buf = BytesIO()
    image.save(buf, format="JPEG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    MODEL = "gemini-2.5-flash"
    URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }
        ]
    }

    try:
        res = requests.post(URL, json=payload)
        if res.status_code != 200:
            return f"❌ Lỗi API {res.status_code}: {res.text}"

        data = res.json()
        if not data.get("candidates"):
            return "❌ Lỗi: API trả về rỗng."

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"


# ===============================
# 📸 CHỤP ẢNH / TẢI ẢNH
# ===============================

st.subheader("📷 Chụp ảnh bài làm")
photo = st.camera_input("Chụp trực tiếp:")

st.subheader("📤 Hoặc tải ảnh lên")
upload = st.file_uploader("Chọn ảnh:", type=["png", "jpg", "jpeg"])

image = None
if photo:
    image = Image.open(photo)
elif upload:
    image = Image.open(upload)


# ===============================
# 🧠 PHÂN TÍCH ẢNH
# ===============================

if image:
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(image, caption="Ảnh bài làm", use_column_width=True)

    with col2:
        st.subheader("🔍 Kết quả AI:")

        if st.button("Phân tích bài làm", type="primary"):

            if not api_key:
                st.error("❌ Bạn chưa nhập API Key!")
            else:
                with st.spinner("⏳ AI đang phân tích..."):

                    # =========================
                    # 🎯 PROMPT CHUẨN – KHÔNG LỖI LaTeX
                    # =========================
                    prompt_text = """
Bạn là giáo viên Toán giỏi. Hãy chấm ảnh bài làm và giải toán NGẮN – DỄ HIỂU – SONG NGỮ (Việt – H’Mông).

==============================
⚠️ QUY TẮC CÔNG THỨC TOÁN HỌC
==============================
- Mọi công thức必须 nằm trong khối:
  $$
  ... \\\\
  $$
- Mỗi phép toán BẮT BUỘC xuống dòng bằng \\\\
- KHÔNG được ghép nhiều công thức trên 1 dòng.
- Dùng đúng chuẩn LaTeX:
  \frac{}, \sqrt{}, ^{}, _{}, \triangle, \angle, \parallel, \perp
- KHÔNG dùng ký tự lạ như:   
- Đại số mẫu:
  $$
  x + 5 = 10 \\\\
  x = 5
  $$
- Hình học mẫu:
  $$
  \frac{AP}{AB} = \frac{150}{300} = \frac{1}{2} \\\\
  \triangle ABC,\; \angle ABC,\; AB \parallel CD
  $$

=====================
1️⃣ CHÉP LẠI ĐỀ BÀI
=====================
- Dòng 1: Tiếng Việt (ngắn).
- Dòng 2: Tiếng H’Mông.
- Dòng 3: LaTeX rõ ràng, mỗi dòng \\\\.

=========================
2️⃣ CHẤM BÀI HỌC SINH
=========================
Mỗi bước gồm 3 dòng:
- Dòng 1: “Bước X: ĐÚNG” hoặc “SAI”.
- Dòng 2: Nếu sai → nêu lỗi 1 câu.
- Dòng 3: Dịch tiếng H’Mông.

==========================
3️⃣ GIẢI LẠI BÀI TOÁN
==========================
Mỗi bước gồm:
- Dòng 1: Tiếng Việt.
- Dòng 2: Tiếng H’Mông.
- Dòng 3: LaTeX:
  $$
  AP = 150\,m \\\\
  PB = 150\,m \\\\
  AB = 300\,m \\\\
  \frac{AP}{AB} = \frac{1}{2}
  $$

==========================
4️⃣ LUÔN GHI NHỚ
==========================
- Câu ngắn.
- Xuống dòng từng ý.
- Song ngữ Việt – H’Mông.
- LaTeX sạch, chuẩn, không ký tự lạ.
"""

                    result = analyze_real_image(api_key, image, prompt_text)

                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")
                        st.markdown(result)
