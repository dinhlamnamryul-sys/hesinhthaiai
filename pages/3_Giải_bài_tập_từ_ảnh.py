import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸", layout="wide")

# --- PHẦN SIDEBAR: CẤU HÌNH & HƯỚNG DẪN ---
with st.sidebar:
    st.title("⚙️ Cấu hình Hệ thống")
    
    # 1. Hướng dẫn lấy Key
    with st.expander("🔑 Cách lấy Google API Key miễn phí"):
        st.write("""
        1. Truy cập [Google AI Studio](https://aistudio.google.com/).
        2. Đăng nhập tài khoản Google.
        3. Nhấn **'Create API key'**.
        4. Copy mã và dán vào ô bên dưới.
        """)
    
    # 2. Nhập Key
    # Lấy key mặc định từ secrets (nếu có), nếu không để trống
    default_key = st.secrets.get("GOOGLE_API_KEY", "")
    api_key = st.text_input("Dán Google API Key của bạn:", value=default_key, type="password")
    
    if not api_key:
        st.warning("⚠️ Vui lòng nhập API Key để bắt đầu.")
    else:
        st.success("✅ Đã nhận API Key")

    st.divider()
    st.info("Sản phẩm dự thi Sáng tạo AI\nHỗ trợ học tập song ngữ Việt - H'Mông")

# --- HÀM PHÂN TÍCH ẢNH (ĐÃ SỬA LỖI URL 404) ---
def analyze_real_image(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Chuẩn bị ảnh
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # URL CHUẨN: Phải có 'models/' trước tên model
    # Dùng v1beta hoặc v1 đều được nếu cấu trúc đúng
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
        
        # Xử lý các lỗi phổ biến
        if response.status_code == 429:
            return "❌ Lỗi 429: Bạn đã hết hạn mức (Quota). Vui lòng đợi 1 phút hoặc đổi Key mới."
        elif response.status_code == 404:
            return f"❌ Lỗi 404: Không tìm thấy Model. Kiểm tra lại URL API."
        elif response.status_code != 200:
            error_msg = data.get("error", {}).get("message", "Lỗi không xác định")
            return f"❌ Lỗi {response.status_code}: {error_msg}"
            
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh")
st.write("Giải pháp hỗ trợ học sinh vùng cao song ngữ **Việt – H’Mông**")

col_input, col_output = st.columns([1, 1.2])

with col_input:
    st.subheader("📷 Nguồn ảnh")
    camera_photo = st.camera_input("Chụp bài làm")
    uploaded_file = st.file_uploader("Hoặc tải ảnh lên", type=["png", "jpg", "jpeg"])

    image = None
    if camera_photo:
        image = Image.open(camera_photo)
    elif uploaded_file:
        image = Image.open(uploaded_file)

    if image:
        st.image(image, caption="Ảnh bài làm", use_container_width=True)

with col_output:
    st.subheader("🔍 Kết quả chấm bài")
    
    if st.button("🚀 Chấm bài ngay", type="primary"):
        if not api_key:
            st.error("Lỗi: Bạn chưa cung cấp API Key ở Sidebar!")
        elif not image:
            st.warning("Vui lòng cung cấp ảnh bài làm.")
        else:
            with st.spinner("⏳ AI đang phân tích dữ liệu..."):
                prompt_text = """
                Bạn là giáo viên Toán giỏi. Hãy chấm bài trong ảnh:
                1. Chép lại đề bằng LaTeX (Song ngữ Việt - H'Mông).
                2. Kiểm tra các bước giải, chỉ ra chỗ sai (Song ngữ Việt - H'Mông).
                3. Trình bày lời giải đúng bằng LaTeX (Song ngữ Việt - H'Mông).
                Sử dụng ký hiệu: 🇻🇳 (Việt) và 🟦 (H'Mông).
                """
                
                result = analyze_real_image(api_key, image, prompt_text)
                
                if "❌" in result:
                    st.error(result)
                else:
                    st.success("Phân tích hoàn tất!")
                    st.markdown(result)

# --- FOOTER ---
st.divider()
st.caption("Ứng dụng sử dụng công nghệ Gemini 1.5 Flash cho tốc độ xử lý nhanh.")
