import streamlit as st
import base64
from groq import Groq
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Chấm Bài AI (Groq)", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Siêu Tốc)")

# --- CẤU HÌNH API ---
# Thử lấy key từ hệ thống, nếu không có thì hiện ô nhập
api_key = None
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]

with st.sidebar:
    if not api_key:
        st.warning("Chưa có Key Groq.")
        api_key = st.text_input("Nhập Groq API Key:", type="password")
        st.markdown("[👉 Lấy Key Groq Miễn Phí](https://console.groq.com/keys)")
    else:
        st.success("✅ Đã kết nối Groq AI")

# --- HÀM XỬ LÝ ẢNH CHO GROQ ---
def encode_image(image):
    buffered = BytesIO()
    # Chuyển RGBA sang RGB nếu cần
    if image.mode == "RGBA":
        image = image.convert("RGB")
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- GIAO DIỆN ---
uploaded_file = st.file_uploader("Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải", use_column_width=True)
    
    if st.button("🔍 Phân tích ngay", type="primary"):
        try:
            with st.spinner("AI đang chấm bài (Tốc độ cao)..."):
                # 1. Chuẩn bị dữ liệu
                base64_image = encode_image(image)
                client = Groq(api_key=api_key)
                
                # 2. Gửi yêu cầu sang Groq (Model Llama-3.2 Vision)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Bạn là giáo viên Toán Việt Nam. Hãy nhìn ảnh và: 1. Viết lại đề bài bằng LaTeX. 2. Kiểm tra bài làm đúng hay sai. 3. Giải chi tiết từng bước. 4. Dịch lời nhận xét sang tiếng H'Mông. Hãy trả lời hoàn toàn bằng tiếng Việt."},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                    },
                                },
                            ],
                        }
                    ],
                    model="llama-3.2-11b-vision-preview",
                )
                
                # 3. Hiển thị kết quả
                result = chat_completion.choices[0].message.content
                st.success("Đã xong!")
                st.markdown(result)
                
        except Exception as e:
            st.error(f"Lỗi: {e}")
            st.info("Mẹo: Kiểm tra lại Key Groq của bạn.")
