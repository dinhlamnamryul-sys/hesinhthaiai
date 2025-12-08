import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# --- Cấu hình Trang ---
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông)")

# Khởi tạo Session State cho API Key
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None  # Mặc định chưa có key

# --- HÀM PHÂN TÍCH ẢNH ---
def analyze_real_image(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Thay MODEL & URL nếu cần tương thích với Groq API
    MODEL = "models/gemini-2.0-flash"  # giữ nguyên model nếu vẫn dùng Google Gemini, nếu dùng Groq API cần đổi
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            if response.status_code == 400:
                del st.session_state['api_key']
                st.session_state['api_key'] = None
                return f"❌ Lỗi API {response.status_code}: API Key có vẻ không hợp lệ hoặc hết hạn. Vui lòng kiểm tra lại Key."
            return f"❌ Lỗi API {response.status_code}: {response.text}"
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# =======================================================
# 🔑 KHUNG QUẢN LÝ API KEY
# =======================================================
if not st.session_state.get('api_key'):
    st.markdown("---")
    st.subheader("🔑 Quản lý và Nhập Khóa API")
    st.warning("⚠️ Ứng dụng yêu cầu API Key từ Groq để hoạt động.")

    with st.form("api_key_form"):
        new_api_key = st.text_input("Nhập Groq API Key của bạn:", type="password", key="key_input")
        submit_button = st.form_submit_button("Sử dụng Key")

        if submit_button and new_api_key:
            st.session_state['api_key'] = new_api_key
            st.success("✅ Đã lưu Key thành công. Vui lòng bấm 'Phân tích ngay' để xác nhận hoạt động!")
            st.rerun()
        elif submit_button and not new_api_key:
            st.error("Vui lòng nhập Key để tiếp tục.")

    st.markdown("Bạn có thể nhận Key miễn phí tại [Groq API](https://www.groq.com/get-api-key).")
    st.markdown("---")
    
else:
    # =======================================================
    # 📸 GIAO DIỆN CHÍNH (Chỉ hiển thị khi có KEY)
    # =======================================================
    api_key = st.session_state['api_key']
    st.success("✅ Đã kết nối với API Key. Bắt đầu chấm bài!")

    st.subheader("📷 Hoặc chụp trực tiếp từ Camera")
    camera_photo = st.camera_input("Chụp ảnh bài làm tại đây")

    st.subheader("📤 Hoặc tải ảnh bài làm (PNG, JPG)")
    uploaded_file = st.file_uploader("Chọn ảnh:", type=["png", "jpg", "jpeg"])

    # --- CHỌN NGUỒN ẢNH ƯU TIÊN ---
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
                    # --- PROMPT SONG NGỮ ---
                    prompt_text = """
Bạn là giáo viên Toán giỏi, đọc ảnh bài làm của học sinh. 
Yêu cầu:

1️⃣ Chép lại đề bài bằng **LaTeX**, hiển thị song song:
🇻🇳 (Tiếng Việt)
🟦 (Tiếng H’Mông)

2️⃣ Chấm bài từng bước:
- Nói học sinh **Đúng / Sai** từng bước.
- Nếu sai, ghi ngắn gọn **Sai ở bước nào & lý do**.
- Hiển thị song song:
🇻🇳 Nhận xét tiếng Việt
🟦 Nhận xét H’Mông

3️⃣ Giải chi tiết:
- Viết từng bước bằng **LaTeX**, hiển thị song song:
🇻🇳 Công thức / bước bằng tiếng Việt
🟦 Công thức / bước bằng tiếng H’Mông
- Nếu học sinh sai → giải lại đúng ở cả hai ngôn ngữ.

MỌI CÂU TRẢ LỜI PHẢI:
- Rõ ràng, đầy đủ, theo thứ tự.
- Song song Việt – H’Mông từng bước.
- Dễ copy vào Word hoặc Overleaf.
"""
                    result = analyze_real_image(api_key, image, prompt_text)

                    if "❌" in result and "API Key có vẻ không hợp lệ" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")
                        st.markdown(result)
