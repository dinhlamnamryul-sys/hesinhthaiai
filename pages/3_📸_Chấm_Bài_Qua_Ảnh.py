import streamlit as st
import requests
import json
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Chấm Bài AI", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh")

# --- 1. CẤU HÌNH API KEY ---
api_key = None
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]

if not api_key:
    st.warning("⚠️ Chưa có API Key hệ thống.")
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- 2. HÀM GỌI TRỰC TIẾP (ĐÃ SỬA TÊN MODEL CHUẨN) ---
def analyze_image_direct(api_key, image, prompt):
    # 1. Xử lý ảnh (Sửa lỗi RGBA)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # 2. Nội dung gửi đi
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img_str
                }}
            ]
        }]
    }

    # 3. THỬ MODEL 1: GEMINI 1.5 FLASH (Nhanh nhất)
    url_flash = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    response = requests.post(url_flash, headers=headers, data=json.dumps(data))

    # Nếu thành công (200) -> Trả về kết quả ngay
    if response.status_code == 200:
        return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Không có nội dung.")
    
    # 4. NẾU FLASH LỖI (404) -> TỰ ĐỘNG THỬ MODEL 2: GEMINI PRO VISION (Ổn định nhất)
    else:
        # st.warning("Đang chuyển sang chế độ tương thích...") # (Ẩn dòng này cho gọn)
        url_pro = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={api_key}"
        response_pro = requests.post(url_pro, headers=headers, data=json.dumps(data))
        
        if response_pro.status_code == 200:
            return response_pro.json().
