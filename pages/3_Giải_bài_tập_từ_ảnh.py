import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import json

st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông)")

# =====================
# 🔑 NHẬP GOOGLE API KEY
# =====================

with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key để dùng ứng dụng:

1. Truy cập trang:  
   **https://aistudio.google.com/app/apikey**

2. Đăng nhập bằng Gmail.

3. Nhấn nút **Create API key** (Tạo khóa API).

4. Copy API Key vừa tạo.

5. Dán vào ô nhập bên dưới.

⚠️ **Lưu ý quan trọng:**  
- Không chia sẻ API Key cho người khác.  
- Nếu lộ key, bạn có thể xoá và tạo key mới trong vài giây.  
    """)

st.subheader("🔐 Nhập Google API Key của bạn để sử dụng:")

# lưu API key vào session_state
api_key = st.text_input("Nhập Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Bạn cần nhập API Key để tiếp tục sử dụng ứng dụng.")
else:
    st.success("✅ API Key đã được nhập!")

# ===============================
# 📌 HÀM PHÂN TÍCH ẢNH QUA GEMINI
# ===============================

def analyze_real_image(api_key, image, prompt):
    if not api_key:
        return "❌ Lỗi: API Key bị thiếu hoặc không được cung cấp."

    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    MODEL = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"

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
            error_details = response.text
            try:
                error_json = response.json()
                if "error" in error_json and "message" in error_json["error"]:
                    error_details = error_json["error"]["message"]
            except json.JSONDecodeError:
                pass

            return f"❌ Lỗi API **{response.status_code}**: {error_details}"

        data = response.json()

        if not data.get("candidates"):
            return "❌ Lỗi: API trả về phản hồi rỗng."

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"


# ===============================
# 📸 NHẬN ẢNH TỪ CAMERA / UPLOAD
# ===============================

st.subheader("📷 Chụp ảnh bài làm")
camera_photo = st.camera_input("Chụp trực tiếp từ camera:")

st.subheader("📤 Hoặc tải ảnh bài làm lên")
uploaded_file = st.file_uploader("Chọn ảnh (PNG/JPG):", type=["png", "jpg", "jpeg"])

image = None
if camera_photo:
    image = Image.open(camera_photo)
elif uploaded_file:
    image = Image.open(uploaded_file)


# ===============================
# 🧠 PHÂN TÍCH ẢNH
# ===============================

if image:
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(image, caption="Ảnh bài làm", use_column_width=True)

    with col2:
        st.subheader("🔍 Kết quả AI:")

        if st.button("Phân tích bài làm", type="primary"):
            if not api_key:
                st.error("❌ Bạn chưa nhập API Key!")
            else:
                with st.spinner("⏳ AI đang phân tích..."):

                    prompt_text = """
Bạn là giáo viên Toán giỏi, nhiệm vụ là chấm ảnh bài làm và giải toán theo cách NGẮN GỌN – DỄ HIỂU – SONG NGỮ (Việt – H’Mông).

YÊU CẦU TRẢ LỜI:

1️⃣ Chép lại đề bài (LaTeX + song ngữ)
Dòng 1: Đề bài tiếng Việt ngắn gọn
Dòng 2:Bản dịch tiếng H’Mông dễ hiểu
Dòng 3: Công thức LaTeX tách dòng rõ ràng
2️⃣ Chấm bài học sinh (từng bước – xuống dòng)
Dòng 1: Bước 1 học sinh làm → ghi ĐÚNG hoặc SAI
Dòng 2: Nếu sai → chỉ rõ sai ở đâu (1 câu ngắn)
Dòng 3: Dịch sang tiếng H’Mông
(→ Lặp lại cho từng bước học sinh đã làm)
3️⃣ Giải lại (ngắn – dễ hiểu – xuống dòng)
Dòng 1: Giải thích tiếng Việt
Dòng 2: Giải thích tiếng H’Mông
Dòng 3: Công thức LaTeX
(→ Lặp lại từng bước giải)
4️⃣ Quy tắc bắt buộc khi trả lời:
Viết câu ngắn.
Mỗi ý xuống dòng.
LaTeX tách dòng rõ ràng.
Dùng từ đơn giản cho học sinh vùng cao.
Luôn song ngữ Việt – H’Mông.
"""

                    result = analyze_real_image(api_key, image, prompt_text)

                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")
                        st.markdown(result)
