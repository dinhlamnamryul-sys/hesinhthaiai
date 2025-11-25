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
    st.warning("⚠️ Chưa có API Key. Vui lòng vào Settings -> Secrets để nhập.")
    # Ô nhập dự phòng
    api_key = st.text_input("Hoặc nhập Key trực tiếp tại đây:", type="password")

# --- XỬ LÝ ẢNH ---
uploaded_file = st.file_uploader("Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải", use_column_width=True)
    
    if st.button("🔍 Phân tích ngay", type="primary"):
        try:
            with st.spinner("Đang kết nối AI..."):
                genai.configure(api_key=api_key)
                
                # --- THAY ĐỔI QUAN TRỌNG Ở ĐÂY ---
                # Dùng model 'gemini-pro-vision' (Bản ổn định nhất cho xử lý ảnh)
                # Thay vì 1.5-flash đang bị lỗi version
                model = genai.GenerativeModel('gemini-pro-vision')
                
                prompt = "Hãy đóng vai giáo viên, giải chi tiết bài toán trong ảnh và chấm điểm bài làm của học sinh."
                
                # Cú pháp cũ chuẩn cho gemini-pro-vision là [prompt, image]
                response = model.generate_content([prompt, image])
                
                st.success("Đã xong!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Lỗi kết nối: {e}")
            st.info("Mẹo: Kiểm tra lại API Key hoặc thử ảnh khác.")
