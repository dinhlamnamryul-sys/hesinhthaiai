import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Chấm Bài AI Song Ngữ (GPT)", page_icon="📸", layout="wide")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông) - Dùng GPT-4o")

# --- LẤY KEY TỪ SECRETS HOẶC NHẬP THỦ CÔNG ---
# ĐÃ ĐỔI TÊN BIẾN TỪ 'GOOGLE_API_KEY' SANG 'OPENAI_API_KEY'
api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    st.warning("⚠️ Chưa có API Key trong hệ thống.")
    # Cho phép người dùng nhập key nếu không tìm thấy trong secrets
    api_key = st.text_input("Nhập OpenAI API Key:", type="password")

# --- HÀM PHÂN TÍCH ẢNH (DÙNG OPENAI GPT-4o) ---
def analyze_real_image_openai(api_key, image, prompt):
    """Gửi ảnh và prompt tới OpenAI GPT-4 Vision API để phân tích."""
    
    # Chuyển đổi ảnh sang RGB nếu nó là RGBA
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Lưu ảnh vào buffer và encode sang Base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # --- CẤU HÌNH API CỦA OPENAI ---
    url = "https://api.openai.com/v1/chat/completions" # Endpoint chuẩn của OpenAI
    MODEL = "gpt-4o" # Mô hình đa phương tiện mới nhất (hoặc "gpt-4-vision-preview")
    
    # Khóa API phải được gửi qua Header
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Tạo Payload (Body của Request)
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}, # Prompt/Yêu cầu bằng văn bản
                    {
                        "type": "image_url",
                        "image_url": {
                            # OpenAI yêu cầu URL dạng Base64 Data URL
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096 # Giới hạn độ dài phản hồi
    }

    try:
        # Gửi POST request
        response = requests.post(url, headers=headers, json=payload)
        
        # Xử lý các lỗi HTTP
        if response.status_code != 200:
            return f"❌ Lỗi API {response.status_code}: {response.text}"
        
        # Trích xuất kết quả từ JSON response
        data = response.json()
        
        # Kiểm tra nếu có lỗi do API trả về
        if "error" in data:
            return f"❌ Lỗi API: {data['error']['message']}"
        
        # Trả về nội dung phản hồi của GPT
        return data["choices"][0]["message"]["content"]
        
    except Exception as e:
        return f"❌ Lỗi kết nối hoặc xử lý: {str(e)}"


# -----------------------------
# --- GIAO DIỆN STREAMLIT ---
# -----------------------------

# --- NGUỒN ẢNH: CAMERA ---
st.subheader("📷 Hoặc chụp trực tiếp từ Camera")
camera_photo = st.camera_input("Chụp ảnh bài làm tại đây")

# --- NGUỒN ẢNH: TẢI LÊN ---
st.subheader("📤 Hoặc tải ảnh bài làm (PNG, JPG, JPEG)")
uploaded_file = st.file_uploader("Chọn ảnh:", type=["png", "jpg", "jpeg"])


# --- CHỌN NGUỒN ẢNH ƯU TIÊN ---
image = None

if camera_photo is not None:
    image = Image.open(camera_photo)
elif uploaded_file is not None:
    image = Image.open(uploaded_file)


# Nếu có ảnh → hiển thị + xử lý
if image:
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(image, caption="Ảnh bài làm", use_column_width=True)

    with col2:
        st.subheader("🔍 Kết quả:")

        if st.button("Phân tích ngay", type="primary"):
            if not api_key:
                st.error("Thiếu OpenAI API Key! Vui lòng nhập khóa ở trên.")
            else:
                with st.spinner("⏳ GPT-4o đang xử lý..."):

                    # --- PROMPT SONG NGỮ (Giữ nguyên) ---
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

                    # --- GỌI HÀM OPENAI ĐÃ CHỈNH SỬA ---
                    result = analyze_real_image_openai(api_key, image, prompt_text) 

                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")
                        st.markdown(result)
