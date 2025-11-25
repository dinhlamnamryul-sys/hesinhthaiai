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

# --- 2. HÀM GỌI TRỰC TIẾP (HARDCORE) ---
def analyze_image_direct(api_key, image, prompt):
    # 1. Xử lý ảnh (Sửa lỗi RGBA -> RGB)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # --- ĐÂY LÀ CHÌA KHÓA: GỌI ĐÍCH DANH MODEL 1.5 FLASH ---
    # Không dùng 'latest', không dùng 'auto', dùng chính xác tên này
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
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

    # Gửi đi
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Không có phản hồi.")
    elif response.status_code == 429:
        return "⚠️ Quá tải hệ thống (429). Vui lòng đợi 30 giây rồi thử lại."
    else:
        return f"Lỗi kết nối ({response.status_code}): {response.text}"

# --- 3. GIAO DIỆN ---
uploaded_file = st.file_uploader("Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải", use_column_width=True)
    
    if st.button("🔍 Phân tích ngay", type="primary"):
        with st.spinner("AI đang chấm bài..."):
            try:
                prompt = """
                Bạn là giáo viên Toán. Hãy nhìn ảnh và thực hiện:
                1. Viết lại đề bài và bài làm (dùng LaTeX).
                2. Kiểm tra bài làm đúng hay sai. Chỉ rõ lỗi.
                3. Giải chi tiết từng bước.
                4. Dịch lời nhận xét sang tiếng H'Mông.
                """
                
                result = analyze_image_direct(api_key, image, prompt)
                
                if "Lỗi kết nối" in result or "Quá tải" in result:
                    st.error(result)
                else:
                    st.success("Đã xong!")
                    st.markdown(result)
                
            except Exception as e:
                st.error(f"Lỗi lạ: {e}")
