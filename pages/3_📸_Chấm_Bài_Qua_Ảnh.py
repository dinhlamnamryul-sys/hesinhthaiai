import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Chấm Bài AI", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh")

# Lấy API Key từ Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ Chưa có API Key. Vui lòng vào Settings -> Secrets để nhập.")
    st.stop()

uploaded_file = st.file_uploader("Tải ảnh bài làm", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải", use_column_width=True)
    
    if st.button("🔍 Phân tích ngay", type="primary"):
        try:
            with st.spinner("AI đang chấm bài..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = "Giải chi tiết bài toán trong ảnh và chấm điểm nếu có bài làm."
                response = model.generate_content([prompt, image])
                
                st.success("Đã xong!")
                st.write(response.text)
        except Exception as e:
            st.error(f"Lỗi: {e}")
