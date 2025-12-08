import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

# --- Cấu hình Trang ---
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông)")

# Khởi tạo Session State cho API Key
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None

# --- HÀM PHÂN TÍCH ẢNH với Groq ---
def analyze_real_image_groq(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # URL và headers Groq
    url = "https://api.groq.com/v1/ai/generate"  # ví dụ Groq endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "groq-math-1",  # ví dụ model Groq
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "data": img_base64}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            if response.status_code == 401:
                del st.session_state['api_key']
                st.session_state['api_key'] = None
                return f"❌ Lỗi API {response.status_code}: API Key không hợp lệ hoặc hết hạn."
            if response.status_code == 429:
                return f"❌ Lỗi API {response.status_code}: Bạn đã vượt quota. Vui lòng kiểm tra kế hoạch sử dụng API Groq."
            return f"❌ Lỗi API {response.status_code}: {response.text}"
        data = response.json()
        # Groq trả kết quả text trong data["output"][0]["text"]
        return data["output"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# =======================================================
# 🔑 Quản lý API Key
# =======================================================
if not st.session_state.get('api_key'):
    st.markdown("---")
    st.subheader("🔑 Nhập Groq API Key")
    st.warning("⚠️ Ứng dụng yêu cầu Groq API Key để hoạt động.")

    with st.form("api_key_form"):
        new_api_key = st.text_input("Nhập Groq API Key:", type="password", key="key_input")
        submit_button = st.form_submit_button("Sử dụng Key")

        if submit_button and new_api_key:
            st.session_state['api_key'] = new_api_key
            st.success("✅ Đã lưu Key thành công!")
            st.rerun()
        elif submit_button and not new_api_key:
            st.error("Vui lòng nhập Key để tiếp tục.")

    st.markdown("Bạn có thể nhận Key miễn phí tại [Groq API](https://www.groq.com/get-api-key).")
    st.markdown("---")

else:
    api_key = st.session_state['api_key']
    st.success("✅ Đã kết nối với API Key. Bắt đầu chấm bài!")

    st.subheader("📷 Chụp trực tiếp từ Camera")
    camera_photo = st.camera_input("Chụp ảnh bài làm tại đây")

    st.subheader("📤 Hoặc tải ảnh bài làm (PNG, JPG)")
    uploaded_file = st.file_uploader("Chọn ảnh:", type=["png", "jpg", "jpeg"])

    # Chọn ảnh ưu tiên
    image = None
    if camera_photo is not None:
        image = Image.open(camera_photo)
    elif uploaded_file is not None:
        image = Image.open(uploaded_file)

    if image:
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.image(image, caption="Ảnh bài làm", use_column_width=True)

        with col2:
            st.subheader("🔍 Kết quả:")
            if st.button("Phân tích ngay", type="primary"):
                with st.spinner("⏳ AI đang xử lý..."):
                    prompt_text = """
Bạn là giáo viên Toán giỏi, đọc ảnh bài làm của học sinh. 
Yêu cầu:

1️⃣ Chép lại đề bài bằng LaTeX song song:
🇻🇳 (Tiếng Việt)
🟦 (Tiếng H’Mông)

2️⃣ Chấm bài từng bước:
- Nói học sinh Đúng / Sai từng bước.
- Nếu sai, ghi ngắn gọn Sai ở bước nào & lý do.
- Hiển thị song song: Việt – H’Mông

3️⃣ Giải chi tiết từng bước bằng LaTeX, song song Việt – H’Mông.
"""
                    result = analyze_real_image_groq(api_key, image, prompt_text)
                    st.markdown(result)
