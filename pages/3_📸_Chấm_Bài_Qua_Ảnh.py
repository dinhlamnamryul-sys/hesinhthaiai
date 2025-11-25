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

# --- 2. HÀM GỌI TRỰC TIẾP (ĐÃ SỬA LỖI ẢNH) ---
def analyze_image_direct(api_key, image, prompt):
    # --- SỬA LỖI RGBA: Chuyển ảnh sang chế độ màu chuẩn (RGB) ---
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    # Chuyển ảnh sang Base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # URL gọi model mới nhất
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    
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

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Không có phản hồi.")
    else:
        return f"Lỗi kết nối ({response.status_code}): {response.text}"

# --- 3. GIAO DIỆN ---
uploaded_file = st.file_uploader("Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải", use_column_width=True)
    
    if st.button("🔍 Phân tích ngay", type="primary"):
        with st.spinner("Đang gửi dữ liệu sang Google (Chế độ trực tiếp)..."):
            try:
                prompt = """
                Bạn là giáo viên Toán. Hãy nhìn ảnh và thực hiện các bước:
                1. Nhận diện đề bài và bài làm trong ảnh (Viết lại đề bằng công thức LaTeX chuẩn).
                2. Chấm điểm: Kiểm tra bài làm đúng hay sai. Chỉ rõ lỗi sai nếu có.
                3. Giải chi tiết: Viết lại lời giải đúng từng bước.
                4. Dịch 1 câu nhận xét ngắn gọn sang tiếng H'Mông.
                """
                
                result = analyze_image_direct(api_key, image, prompt)
                
                if "Lỗi kết nối" in result:
                    st.error(result)
                else:
                    st.success("Đã xong!")
                    st.markdown(result)
                
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")
