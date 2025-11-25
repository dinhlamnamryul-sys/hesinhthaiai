import streamlit as st
import requests
import json
import base64
from PIL import Image
from io import BytesIO

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Chấm Bài AI - Na Ư", page_icon="📸", layout="centered")
st.title("📸 Chấm Bài & Giải Toán Song Ngữ (Việt - Mông)")

# --- LẤY KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")

if not api_key:
    st.warning("⚠️ Chưa có API Key.")
    api_key = st.text_input("Nhập Google API Key của bạn:", type="password")

# --- HÀM PHÂN TÍCH ẢNH ---
def analyze_real_image(api_key, image, prompt):
    # Chuyển RGBA → RGB
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Encode ảnh base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Dùng model Flash 1.5 (Ổn định, nhanh, rẻ)
    # Nếu bạn chắc chắn có quyền dùng 2.0, hãy đổi lại thành "gemini-2.0-flash"
    MODEL = "models/gemini-1.5-flash" 

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={api_key}"

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_base64
                    }
                }
            ]
        }]
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return f"❌ Lỗi API {response.status_code}: {response.text}"
        
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# --- GIAO DIỆN ---
uploaded_file = st.file_uploader("📤 Tải ảnh bài làm lên đây", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh bài làm", use_column_width=True)

    if st.button("🚀 Chấm & Phân Tích Ngay", type="primary"):
        if not api_key:
            st.error("Vui lòng nhập API Key!")
        else:
            with st.spinner("⏳ AI đang soi bài và dịch sang tiếng Mông..."):
                
                # --- PROMPT ĐƯỢC TỐI ƯU HÓA CHO TOÁN HỌC & NGẮN GỌN ---
                prompt_text = """
                Bạn là giáo viên Toán vùng cao, giỏi tiếng Việt và tiếng H'Mông.
                Nhiệm vụ: Chấm bài từ ảnh và giải thích cực kỳ NGẮN GỌN, SÚC TÍCH.

                YÊU CẦU VỀ ĐỊNH DẠNG (BẮT BUỘC):
                1. Tất cả công thức toán, biến số (x, y), con số phải viết trong định dạng LaTeX. Ví dụ: $x^2 + 2x = 0$.
                2. Không viết văn dài dòng. Dùng gạch đầu dòng.
                3. Phần tiếng H'Mông phải giữ nguyên công thức LaTeX y hệt phần tiếng Việt.

                HÃY TRẢ LỜI THEO MẪU SAU:

                ### 1. Đề bài
                (Viết lại đề bài thấy trong ảnh bằng LaTeX)

                ### 2. Kết quả: [ĐÚNG] hoặc [SAI]

                ### 3. Chữa bài (Tiếng Việt)
                * **Lỗi sai (nếu có):** Chỉ rõ dòng sai. Ví dụ: Sai ở bước chuyển vế $2x = 10$.
                * **Cách giải đúng:** (Viết ngắn gọn các bước giải bằng công thức).
                    $$ [Công thức giải bước 1] $$
                    $$ [Công thức giải bước 2] $$
                    $$ [Đáp án cuối cùng] $$

                ### 4. Chữa bài (Tiếng H'Mông - Hmoob)
                * **Qhov sai (Lỗi sai):** (Dịch ngắn gọn lỗi sai sang tiếng Mông).
                * **Ua li no thiaj yog (Cách làm đúng):**
                    (Giải thích ngắn gọn bằng tiếng Mông, chèn công thức y hệt bên trên).
                    $$ [Công thức giải bước 1] $$
                    $$ [Công thức giải bước 2] $$
                    $$ [Đáp án cuối cùng] $$
                """

                result = analyze_real_image(api_key, image, prompt_text)

                if "❌" in result:
                    st.error(result)
                else:
                    st.success("🎉 Đã xong!")
                    st.markdown(result)
