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
    saved_key = st.secrets.get("GOOGLE_API_KEY", "")
    api_key = st.text_input("Dán Google API Key của bạn:", value=saved_key, type="password")
    
    if not api_key:
        st.warning("⚠️ Vui lòng nhập API Key để bắt đầu.")
    else:
        st.success("✅ Đã nhận API Key")

    st.divider()
    st.info("Sản phẩm dự thi Sáng tạo AI\nHỗ trợ học tập song ngữ Việt - H'Mông")

# --- HÀM PHÂN TÍCH ẢNH ---
def analyze_real_image(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Cấu trúc URL chuẩn để tránh lỗi 404
    MODEL = "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        if response.status_code == 429:
            return "❌ Lỗi 429: Key của bạn đã hết hạn mức yêu cầu. Vui lòng đợi 1 phút rồi thử lại."
        elif response.status_code != 200:
            error_msg = data.get("error", {}).get("message", "Lỗi không xác định")
            return f"❌ Lỗi API {response.status_code}: {error_msg}"
            
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh")
st.write("Dành cho học sinh vùng cao hỗ trợ song ngữ **Việt – H’Mông**")

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
        st.image(image, caption="Ảnh bài làm đã chọn", use_container_width=True)

with col_output:
    st.subheader("🔍 Kết quả chấm bài")
    
    if st.button("🚀 Bắt đầu phân tích", type="primary"):
        if not api_key:
            st.error("Bạn chưa nhập API Key ở thanh bên (Sidebar)!")
        elif not image:
            st.warning("Vui lòng chụp ảnh hoặc tải ảnh lên trước.")
        else:
            with st.spinner("⏳ AI đang chấm bài (Việt - H'Mông)..."):
                # PROMPT TỐI ƯU
                prompt_text = """
Bạn là giáo viên Toán giỏi hỗ trợ học sinh vùng cao. Đọc ảnh bài làm và thực hiện:
1. Chép lại đề bằng LaTeX. Hiển thị song song Việt - H'Mông.
2. Chấm điểm chi tiết: Đúng/Sai ở đâu. Nhận xét bằng cả 2 ngôn ngữ.
3. Giải lại đúng hoàn toàn bằng LaTeX, trình bày từng bước song ngữ.
Ký hiệu: 🇻🇳 Tiếng Việt | 🟦 Tiếng H'Mông.
                """
                
                result = analyze_real_image(api_key, image, prompt_text)
                
                if "❌" in result:
                    st.error(result)
                else:
                    st.success("Hoàn thành!")
                    st.markdown(result)

# --- CHÂN TRANG ---
st.divider()
st.caption("Ghi chú: Kết quả do AI tạo ra có thể cần kiểm tra lại bởi giáo viên.")
