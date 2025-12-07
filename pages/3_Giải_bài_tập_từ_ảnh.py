import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸", layout="wide")

# --- SIDEBAR: CÀI ĐẶT & HƯỚNG DẪN ---
with st.sidebar:
    st.title("⚙️ Cài đặt")
    
    with st.expander("🔑 Cách lấy API Key"):
        st.markdown("[Lấy Key tại đây](https://aistudio.google.com/)")
    
    # Cho phép người dùng nhập key vào đây
    api_key = st.text_input("Dán Google API Key của bạn:", type="password")
    
    if not api_key:
        st.warning("⚠️ Vui lòng nhập API Key!")
    else:
        st.success("✅ Đã sẵn sàng")

# --- HÀM PHÂN TÍCH ẢNH (ĐÃ SỬA URL CHUẨN) ---
def analyze_real_image(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Encode ảnh sang base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # --- ĐỊA CHỈ URL CHUẨN ĐỂ TRÁNH LỖI 404 ---
    # Lưu ý: Cấu trúc là v1beta/models/{model}:generateContent
    # Không được thiếu chữ 'models' ở giữa
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
        
        if response.status_code == 404:
            return "❌ Lỗi 404: Google không tìm thấy Model. Hãy kiểm tra lại version API trong URL."
        elif response.status_code == 429:
            return "❌ Lỗi 429: Hạn mức đã hết. Vui lòng nghỉ 60 giây rồi thử lại."
        elif response.status_code != 200:
            msg = data.get("error", {}).get("message", "Lỗi không xác định")
            return f"❌ Lỗi {response.status_code}: {msg}"
            
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
st.title("📸 Chấm Bài & Giải Toán Việt – H’Mông")

# Chia cột cho giao diện chuyên nghiệp
col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Đầu vào")
    mode = st.radio("Chọn nguồn ảnh:", ["Máy ảnh", "Tải tệp lên"])
    
    image = None
    if mode == "Máy ảnh":
        cam_file = st.camera_input("Chụp bài làm")
        if cam_file: image = Image.open(cam_file)
    else:
        up_file = st.file_uploader("Chọn ảnh bài làm", type=["png", "jpg", "jpeg"])
        if up_file: image = Image.open(up_file)

    if image:
        st.image(image, caption="Ảnh đã nạp", use_container_width=True)

with col_out:
    st.subheader("🔍 Kết quả AI")
    if st.button("🚀 Bắt đầu chấm bài", type="primary"):
        if not api_key:
            st.error("Bạn chưa nhập mã Key ở sidebar!")
        elif not image:
            st.warning("Hãy cung cấp ảnh trước.")
        else:
            with st.spinner("Đang đọc và giải bài..."):
                prompt = """
                Phân tích ảnh bài làm toán:
                1. Chép đề bằng LaTeX (Việt - H'Mông).
                2. Chấm Đúng/Sai chi tiết (Việt - H'Mông).
                3. Giải lại đúng bằng LaTeX (Việt - H'Mông).
                Sử dụng ký hiệu 🇻🇳 và 🟦.
                """
                result = analyze_real_image(api_key, image, prompt)
                st.markdown(result)
