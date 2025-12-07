import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸", layout="wide")

# --- PHẦN SIDEBAR: CẤU HÌNH & HƯỚNG DẪN ---
with st.sidebar:
    st.title("⚙️ Cấu hình Hệ thống")
    
    # 1. Hướng dẫn lấy Key
    with st.expander("🔑 Cách lấy Google API Key miễn phí"):
        st.write("""
        1. Truy cập [Google AI Studio](https://aistudio.google.com/).
        2. Đăng nhập bằng tài khoản Google.
        3. Nhấn **'Create API key'**.
        4. Copy mã key và dán vào ô bên dưới.
        """)
    
    # 2. Ô nhập Key
    # Ưu tiên lấy từ secrets (nếu có), nếu không để trống cho người dùng nhập
    saved_key = st.secrets.get("GOOGLE_API_KEY", "")
    api_key = st.text_input("Dán Google API Key của bạn:", value=saved_key, type="password")
    
    if not api_key:
        st.warning("⚠️ Vui lòng nhập API Key để ứng dụng có thể hoạt động.")
    else:
        st.success("✅ Đã nhận API Key")

    st.divider()
    st.info("Sản phẩm dự thi Sáng tạo AI - Phiên bản hỗ trợ song ngữ Việt - H'Mông")

# --- NỘI DUNG CHÍNH ---
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông)")

# --- HÀM PHÂN TÍCH ẢNH (Giữ nguyên logic của bạn nhưng thêm xử lý lỗi 429 cụ thể) ---
def analyze_real_image(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Sử dụng Gemini 1.5 Flash cho tốc độ nhanh, Gemini 2.0 Flash nếu cần công nghệ mới nhất
    MODEL = "gemini-1.5-flash" # Hoặc "gemini-2.0-flash-exp"
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
        
        if response.status_code == 429:
            return "❌ Lỗi 429: Key này đã hết hạn mức (Quota). Vui lòng đợi 1 phút hoặc đổi Key mới."
        elif response.status_code != 200:
            error_msg = data.get("error", {}).get("message", "Lỗi không xác định")
            return f"❌ Lỗi API {response.status_code}: {error_msg}"
            
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# --- PHẦN CAMERA & TẢI ẢNH (Giữ nguyên) ---
st.subheader("📷 Chụp ảnh bài làm")
camera_photo = st.camera_input("Chụp ảnh trực tiếp")

st.subheader("📤 Hoặc tải ảnh lên")
uploaded_file = st.file_uploader("Chọn tệp ảnh:", type=["png", "jpg", "jpeg"])

# --- XỬ LÝ ẢNH ---
image = None
if camera_photo:
    image = Image.open(camera_photo)
elif uploaded_file:
    image = Image.open(uploaded_file)

if image:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(image, caption="Ảnh gốc", use_column_width=True)
    
    with col2:
        if st.button("🚀 Bắt đầu chấm bài", type="primary"):
            if not api_key:
                st.error("Lỗi: Bạn chưa cung cấp API Key!")
            else:
                with st.spinner("🤖 AI đang chấm bài, vui lòng đợi..."):
                    prompt_text = """
                    (Giữ nguyên prompt chuyên sâu về LaTeX và Việt - H'Mông của bạn tại đây)
                    """
                    result = analyze_real_image(api_key, image, prompt_text)
                    
                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("Kết quả phân tích:")
                        st.markdown(result)
