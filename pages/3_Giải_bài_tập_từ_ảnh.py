import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import json  # Import json để xử lý lỗi API

st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông)")

# --- LẤY KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")

if not api_key:
    st.warning("⚠️ Chưa có API Key trong hệ thống (st.secrets).")
    if 'manual_api_key' not in st.session_state:
        st.session_state['manual_api_key'] = ""

    st.session_state['manual_api_key'] = st.text_input(
        "Nhập Google API Key:",
        type="password",
        value=st.session_state['manual_api_key']
    )
    api_key = st.session_state['manual_api_key']


# --- HÀM PHÂN TÍCH ẢNH ---
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

            return f"❌ Lỗi API **{response.status_code}** ({response.reason}): {error_details}"

        data = response.json()

        if not data.get("candidates"):
            return "❌ Lỗi: API trả về phản hồi rỗng."

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"


# --- GIAO DIỆN CHỤP CAMERA ---
st.subheader("📷 Hoặc chụp trực tiếp từ Camera")
camera_photo = st.camera_input("Chụp ảnh bài làm tại đây")

# --- GIAO DIỆN TẢI ẢNH ---
st.subheader("📤 Hoặc tải ảnh bài làm (PNG, JPG)")
uploaded_file = st.file_uploader("Chọn ảnh:", type=["png", "jpg", "jpeg"])

# --- CHỌN NGUỒN ẢNH ---
image = None
if camera_photo is not None:
    image = Image.open(camera_photo)
elif uploaded_file is not None:
    image = Image.open(uploaded_file)

# --- HIỂN THỊ & PHÂN TÍCH ---
if image:
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(image, caption="Ảnh bài làm", use_column_width=True)

    with col2:
        st.subheader("🔍 Kết quả:")

        if st.button("Phân tích ngay", type="primary"):
            if not api_key:
                st.error("Thiếu API Key! Vui lòng nhập Key.")
            else:
                with st.spinner("⏳ AI đang xử lý..."):

                    # --- PROMPT SONG NGỮ TỐI ƯU HÓA ---
                    prompt_text = """
Bạn là giáo viên Toán giỏi, nhiệm vụ là chấm ảnh bài làm và giải toán theo cách NGẮN GỌN – DỄ HIỂU – SONG NGỮ (Việt – H’Mông).

YÊU CẦU TRẢ LỜI:

1️⃣ Chép lại đề bài bằng LaTeX  
- 🇻🇳 Tiếng Việt (ngắn gọn, đúng nội dung)  
- 🟦 Tiếng H’Mông (dịch nghĩa dễ hiểu)

2️⃣ Chấm bài học sinh  
- Nêu từng bước học sinh làm → ĐÚNG / SAI  
- Nếu sai → chỉ rõ sai ở bước nào + giải thích NGẮN GỌN, dễ hiểu  
- Trình bày song ngữ:  
  🇻🇳 Nhận xét tiếng Việt  
  🟦 Nhận xét tiếng H’Mông

3️⃣ Giải lại bài toán (ngắn nhất có thể)  
- Dùng LaTeX cho biểu thức toán.  
- Mỗi bước trình bày song song:  
  🇻🇳 Giải thích tiếng Việt (ngắn – dễ hiểu)  
  🟦 Giải thích tiếng H’Mông (ngắn – dễ hiểu)

📌 QUY TẮC:
- Không viết dài dòng.  
- Chỉ nêu điều quan trọng.  
- Dùng từ đơn giản phù hợp học sinh vùng cao.  
- Công thức LaTeX rõ ràng, tách dòng gọn.  
- Mỗi bước đều song ngữ.
"""

                    result = analyze_real_image(api_key, image, prompt_text)

                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")
                        st.markdown(result)
