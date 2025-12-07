import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# --- CẤU HÌNH ---
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", layout="wide")

# --- SIDEBAR CÀI ĐẶT ---
with st.sidebar:
    st.title("⚙️ Cài đặt")
    api_key = st.text_input("Nhập Google API Key:", type="password")
    st.info("Hướng dẫn: Lấy key tại [Google AI Studio](https://aistudio.google.com/)")

# --- HÀM XỬ LÝ API ---
def analyze_real_image(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # --- URL CHUẨN ĐÃ SỬA LỖI 404 ---
    MODEL = "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key}"

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
            ]
        }]
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        # Kiểm tra lỗi phản hồi
        if response.status_code == 404:
            return "❌ Lỗi 404: Sai URL hoặc Model không tồn tại. Vui lòng kiểm tra lại cấu trúc URL."
        elif response.status_code == 429:
            return "❌ Lỗi 429: Hết hạn mức (Quota). Vui lòng đợi 1 phút."
        elif response.status_code != 200:
            return f"❌ Lỗi {response.status_code}: {data.get('error', {}).get('message', 'Unknown error')}"
            
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông)")

# Chụp ảnh / Tải ảnh
camera_photo = st.camera_input("Chụp bài làm")
uploaded_file = st.file_uploader("Hoặc tải ảnh lên", type=["png", "jpg", "jpeg"])

image = None
if camera_photo: image = Image.open(camera_photo)
elif uploaded_file: image = Image.open(uploaded_file)

if image:
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Bài làm của học sinh", use_container_width=True)
    with col2:
        if st.button("🚀 Phân tích ngay", type="primary"):
            if not api_key:
                st.error("Vui lòng nhập API Key ở sidebar!")
            else:
                with st.spinner("Đang chấm bài..."):
                    prompt = "Dịch đề bài sang tiếng Việt và H'Mông, chấm điểm và giải chi tiết bằng LaTeX."
                    result = analyze_real_image(api_key, image, prompt)
                    st.markdown(result)
