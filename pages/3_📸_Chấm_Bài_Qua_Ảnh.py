import streamlit as st
import base64
from groq import Groq
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Chấm Bài AI (Groq)", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán (Siêu Tốc)")

# --- CẤU HÌNH API ---
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

# --- HÀM XỬ LÝ ẢNH ---
def encode_image(image):
    buffered = BytesIO()
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
            with st.spinner("AI đang chấm bài..."):
                base64_image = encode_image(image)
                client = Groq(api_key=api_key)
                
                # --- MẸO SỬA LỖI: Gửi lệnh Tiếng Anh, yêu cầu trả lời Tiếng Việt ---
                # (Tránh lỗi mã hóa ASCII khó chịu)
                safe_prompt = """
                You are an expert Math teacher in Vietnam. Please look at the image and:
                1. Transcribe the math problem using LaTeX format.
                2. Check if the student's solution is correct or incorrect. Point out specific errors.
                3. Provide a step-by-step correct solution.
                4. Translate a short encouraging comment into Hmong language.
                
                IMPORTANT: Please respond entirely in VIETNAMESE language.
                """
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": safe_prompt},
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
                
                result = chat_completion.choices[0].message.content
                st.success("Đã xong!")
                st.markdown(result)
                
        except Exception as e:
            st.error(f"Lỗi: {e}")
            st.info("Mẹo: Kiểm tra lại Key Groq của bạn.")
