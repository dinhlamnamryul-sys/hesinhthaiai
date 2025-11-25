import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

st.set_page_config(page_title="Chấm Bài AI", page_icon="📸")

st.title("📸 Chấm Bài & Giải Toán Qua Ảnh")

# --- CẤU HÌNH API ---
api_key = None
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]

if not api_key:
    st.warning("⚠️ Chưa có API Key hệ thống.")
    api_key = st.text_input("Nhập Google API Key của bạn:", type="password")

# --- XỬ LÝ ẢNH ---
uploaded_file = st.file_uploader("Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải", use_column_width=True)
    
    if st.button("🔍 Phân tích ngay", type="primary"):
        try:
            with st.spinner("AI đang chấm bài..."):
                # Cấu hình AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = """
                Bạn là giáo viên Toán. Hãy nhìn ảnh và thực hiện:
                1. Nhận diện đề bài và bài làm.
                2. Kiểm tra bài làm đúng hay sai. Chỉ rõ lỗi sai.
                3. Giải lại bài toán chi tiết từng bước.
                4. Dịch một lời khen ngắn sang tiếng H'Mông.
                """
                
                response = model.generate_content([prompt, image])
                st.success("Đã xong!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Lỗi: {e}")
            st.info("Mẹo: Nếu lỗi 404, hãy Xóa App trên Streamlit và tạo lại.")
