import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# --- CẤU HÌNH ---
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", layout="wide")

# --- SIDEBAR CÀI ĐẶT ---
with st.sidebar:
    st.title("⚙️ Cấu hình")
    # Cho phép người dùng dán key
    api_key = st.text_input("Nhập Google API Key:", type="password")
    st.markdown("[Lấy Key tại Google AI Studio](https://aistudio.google.com/)")
    st.divider()
    st.info("Sản phẩm hỗ trợ học tập song ngữ Việt - H'Mông")

# --- HÀM XỬ LÝ API (ĐÃ FIX URL) ---
def analyze_real_image(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # --- URL CHUẨN ĐÃ SỬA LỖI 404 ---
    # Phải có 'models/' và khuyến khích dùng 'v1beta' cho Gemini 1.5 Flash
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
        
        # Kiểm tra mã trạng thái để phản hồi thông minh
        if response.status_code == 404:
            return "❌ Lỗi 404: Sai cấu trúc URL. Vui lòng kiểm tra lại biến MODEL hoặc tiền tố 'models/'."
        elif response.status_code == 429:
            return "❌ Lỗi 429: Hết hạn mức yêu cầu (Quota). Vui lòng đợi 1 phút."
        elif response.status_code != 200:
            return f"❌ Lỗi {response.status_code}: {data.get('error', {}).get('message', 'Lỗi không xác định')}"
            
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📥 Đầu vào")
    mode = st.radio("Nguồn ảnh:", ["Máy ảnh", "Tải tệp"])
    
    image = None
    if mode == "Máy ảnh":
        cam_file = st.camera_input("Chụp ảnh bài làm")
        if cam_file: image = Image.open(cam_file)
    else:
        up_file = st.file_uploader("Chọn ảnh bài làm", type=["jpg", "png", "jpeg"])
        if up_file: image = Image.open(up_file)

    if image:
        st.image(image, caption="Ảnh bài làm", use_container_width=True)

with col2:
    st.subheader("🔍 Kết quả AI")
    if st.button("🚀 Phân tích", type="primary"):
        if not api_key:
            st.error("Chưa có API Key!")
        elif not image:
            st.warning("Chưa có ảnh!")
        else:
            with st.spinner("Đang chấm bài song ngữ..."):
                prompt = "Chép lại đề, chấm đúng sai bài làm trong ảnh và giải chi tiết. Mọi phản hồi đều hiển thị song ngữ Việt - H'Mông và dùng LaTeX cho công thức."
                result = analyze_real_image(api_key, image, prompt)
                st.markdown(result)
