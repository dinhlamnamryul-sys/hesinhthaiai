import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Chấm Bài AI Thật", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Real AI)")

# --- LẤY KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")

if not api_key:
    st.warning("⚠️ Chưa có API Key trong hệ thống.")
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- HÀM PHÂN TÍCH ẢNH ---
def analyze_real_image(api_key, image, prompt):

    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
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

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return f"❌ Lỗi API {response.status_code}: {response.text}"

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# --- GIAO DIỆN ---
uploaded_file = st.file_uploader("📤 Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns([1, 1.5])
    image = Image.open(uploaded_file)

    with col1:
        st.image(image, caption="Ảnh thực tế", use_column_width=True)

    with col2:
        st.subheader("🔍 Kết quả:")

        if st.button("Phân tích ngay", type="primary"):
            if not api_key:
                st.error("Thiếu API Key!")
            else:
                with st.spinner("⏳ AI đang xử lý..."):

                    # --- PROMPT NGẮN GỌN ---
                    prompt_text = """
Bạn là giáo viên Toán giỏi, đọc ảnh bài làm. 

Yêu cầu:

1️⃣ Chép lại đề bài bằng **LaTeX**.

2️⃣ Chấm bài:
- Nói học sinh **Đúng / Sai**.
- Nếu sai, ghi **Sai ở bước nào & lý do** ngắn gọn.

3️⃣ Giải chi tiết:
- Viết **từng bước bằng LaTeX**.
- Nếu học sinh sai → giải lại đúng.

4️⃣ Phản hồi song ngữ:
🇻🇳 Nhận xét ngắn: Con sai ở bước …, lý do …, cần làm thế này …
🟦 H’Mông: Koj ua yuam kev hauv kauj ruam …, vim …, yuav tsum làm thế này …

MỌI CÂU TRẢ LỜI RÕ, ĐỦ, TUÂN THỦ THỨ TỰ.
"""

                    result = analyze_real_image(api_key, image, prompt_text)
                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")
                        st.markdown(result)
