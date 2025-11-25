import streamlit as st
import requests
import json
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Chấm Bài AI Thật", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Real AI)")

# --- 1. LẤY KEY TỪ HỆ THỐNG ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")

if not api_key:
    st.warning("⚠️ Chưa cấu hình Key hệ thống.")
    api_key = st.text_input("Nhập Google API Key của bạn:", type="password")

# --- 2. HÀM GỌI API CHUẨN V1 ---
def analyze_real_image(api_key, image, prompt):

    # Xử lý ảnh nếu RGBA
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Encode ảnh
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode()

    # API mới (v1) — BẮT BUỘC
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"

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
        # Dùng json=payload (không dùng data=…)
        response = requests.post(url, json=payload)

        if response.status_code != 200:
            return f"❌ Lỗi API {response.status_code}: {response.text}"

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"


# --- 3. GIAO DIỆN ---
uploaded = st.file_uploader("📤 Tải ảnh bài làm (PNG, JPG):", type=["png", "jpg", "jpeg"])

if uploaded:
    col1, col2 = st.columns([1, 1.5])

    image = Image.open(uploaded)

    with col1:
        st.image(image, caption="Ảnh thực tế", use_column_width=True)

    with col2:
        st.subheader("🔍 Kết quả phân tích")

        if st.button("Phân tích ngay", type="primary"):
            if not api_key:
                st.error("Thiếu API Key!")
            else:
                with st.spinner("⏳ AI đang xử lý ảnh..."):
                    prompt_text = """
                    Bạn là giáo viên Toán. Hãy:
                    1) Chép lại đề bài (dùng LaTeX).
                    2) Chấm bài trong ảnh.
                    3) Giải chi tiết.
                    4) Viết 1 câu nhận xét bằng tiếng H'Mông.
                    """

                    result = analyze_real_image(api_key, image, prompt_text)

                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")
                        st.markdown(result)
