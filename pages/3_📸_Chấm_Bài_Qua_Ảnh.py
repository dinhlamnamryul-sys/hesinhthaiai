import streamlit as st
import requests
import json
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Chấm Bài AI Thật", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Real AI)")

# --- 1. LẤY KEY TỪ HỆ THỐNG ---
api_key = None
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]

# Nếu chưa có Key trong hệ thống thì hiện ô nhập
if not api_key:
    st.warning("⚠️ Chưa cấu hình Key hệ thống.")
    api_key = st.text_input("Nhập Google API Key của bạn:", type="password")

# --- 2. HÀM GỬI ẢNH TRỰC TIẾP (KHÔNG QUA THƯ VIỆN) ---
def analyze_real_image(api_key, image, prompt):
    # Xử lý ảnh: Chuyển nền trong suốt thành trắng (Tránh lỗi RGBA)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    # Mã hóa ảnh thành chuỗi ký tự
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Đường dẫn chuẩn của Google (Model Flash ổn định nhất)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # Đóng gói dữ liệu gửi đi
    payload = {
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
    headers = {'Content-Type': 'application/json'}

    # Gửi đi và chờ phản hồi
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            # Lấy nội dung trả lời
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            # Báo lỗi cụ thể nếu Key sai hoặc hết tiền
            return f"❌ Lỗi từ Google ({response.status_code}): {response.text}"
    except Exception as e:
        return f"❌ Lỗi đường truyền: {str(e)}"

# --- 3. GIAO DIỆN ---
uploaded_file = st.file_uploader("Tải ảnh bài làm thật lên (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns([1, 1.5])
    
    # Hiện ảnh vừa tải
    image = Image.open(uploaded_file)
    with col1:
        st.image(image, caption="Ảnh thực tế", use_column_width=True)
    
    with col2:
        st.subheader("Kết quả phân tích:")
        if st.button("🔍 Phân tích ngay", type="primary"):
            if not api_key:
                st.error("Thiếu API Key! Vui lòng nhập Key để AI hoạt động.")
            else:
                with st.spinner("AI đang đọc ảnh của bạn..."):
                    # Câu lệnh cho AI
                    prompt_text = """
                    Bạn là một giáo viên Toán tận tâm. Hãy nhìn vào bức ảnh này và:
                    1. Gõ lại đề bài (dùng LaTeX cho công thức).
                    2. Kiểm tra bài làm trong ảnh (nếu có) xem đúng hay sai.
                    3. Giải chi tiết bài toán đó từng bước một.
                    4. Dịch một câu nhận xét ngắn sang tiếng H'Mông.
                    """
                    
                    # Gọi hàm xử lý thật
                    ket_qua = analyze_real_image(api_key, image, prompt_text)
                    
                    # Hiển thị
                    if "❌" in ket_qua:
                        st.error(ket_qua) # Hiện lỗi đỏ nếu có
                    else:
                        st.success("Đã phân tích xong!")
                        st.markdown(ket_qua)
