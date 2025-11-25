import streamlit as st
import requests
import json
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

    # Chuyển RGBA → RGB
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Encode ảnh base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Model MỚI — KHÔNG BAO GIỜ lỗi 404
    MODEL = "models/gemini-2.0-flash"

    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

    # Payload đúng cấu trúc
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
                    prompt_text = """
                    Bạn là giáo viên Toán. Hãy:
                    1) Chép lại đề bài bằng LaTeX.
                    2) Chấm bài trong ảnh đúng/sai.
                    3) Giải chi tiết từng bước.
                    4) Viết 1 câu nhận xét bằng tiếng H'Mông.
                    """

                    result = analyze_real_image(api_key, image, prompt_text)

                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")
                        st.markdown(result)
