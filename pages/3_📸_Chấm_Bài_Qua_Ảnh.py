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
            return response_pro.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Không có nội dung.")
        else:
            # Nếu cả 2 đều lỗi thì mới báo
            return f"Lỗi kết nối: {response.text} \n(Dự phòng: {response_pro.text})"

# --- 3. GIAO DIỆN ---
uploaded_file = st.file_uploader("Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải", use_column_width=True)
    
    if st.button("🔍 Phân tích ngay", type="primary"):
        with st.spinner("Đang gửi dữ liệu sang Google..."):
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
