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

# --- 2. HÀM GỌI TRỰC TIẾP (KHÔNG DÙNG THƯ VIỆN) ---
def analyze_image_direct(api_key, image, prompt):
    # Chuyển ảnh sang Base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Địa chỉ gửi thư cho Google (Dùng model 1.5 Flash mới nhất)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # Nội dung gửi đi
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

    # Gửi yêu cầu (Giống như gửi tin nhắn Zalo)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Lỗi kết nối: {response.text}"

# --- 3. GIAO DIỆN ---
uploaded_file = st.file_uploader("Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải", use_column_width=True)
    
    if st.button("🔍 Phân tích ngay", type="primary"):
        with st.spinner("Đang gửi dữ liệu sang Google..."):
            try:
                prompt = """
                Bạn là giáo viên Toán. Hãy nhìn ảnh và:
                1. Nhận diện đề bài và bài làm (dùng LaTeX cho công thức).
                2. Kiểm tra bài làm đúng hay sai. Chỉ rõ lỗi sai.
                3. Giải lại bài toán chi tiết.
                4. Dịch một lời khen ngắn sang tiếng H'Mông.
                """
                
                # Gọi hàm trực tiếp
                result = analyze_image_direct(api_key, image, prompt)
                
                st.success("Đã xong!")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")
