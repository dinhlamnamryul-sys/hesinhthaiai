import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

st.set_page_config(page_title="Chấm Bài AI Vision", page_icon="📸")

st.markdown("""
<style>
    .stApp { background-color: #f0f4f8; }
    .main-title { text-align: center; color: #d32f2f; margin-bottom: 20px; }
    .result-box { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📸 Chấm Bài & Giải Toán Qua Ảnh</h1>", unsafe_allow_html=True)

# --- CẤU HÌNH API ---
with st.sidebar:
    st.header("🔑 Cấu hình AI")
    st.info("Nhập API Key để kích hoạt trí tuệ nhân tạo.")
    api_key = st.text_input("Google API Key:", type="password")
    st.markdown("[👉 Lấy Key miễn phí](https://aistudio.google.com/app/apikey)")

# --- GIAO DIỆN CHÍNH ---
uploaded_file = st.file_uploader("Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ảnh đã tải lên", use_column_width=True)
    
    with col2:
        st.subheader("📝 Kết quả phân tích:")
        analyze_btn = st.button("🔍 Phân tích ngay", type="primary")
        
        if analyze_btn:
            if not api_key:
                st.error("⚠️ Hãy nhập API Key bên trái trước!")
            else:
                try:
                    with st.spinner("Đang kết nối Google Gemini..."):
                        # Cấu hình
                        genai.configure(api_key=api_key)
                        
                        # --- QUAN TRỌNG: SỬ DỤNG MODEL CHUẨN ---
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        prompt = """
                        Bạn là giáo viên Toán. Hãy nhìn hình ảnh và:
                        1. Viết lại đề bài và bài làm trong ảnh (dùng công thức LaTeX).
                        2. Kiểm tra xem bài làm đúng hay sai. Chỉ ra lỗi sai cụ thể.
                        3. Giải lại bài toán thật chi tiết.
                        4. Dịch một lời khen sang tiếng H'Mông.
                        """
                        
                        response = model.generate_content([prompt, image])
                        
                        st.success("Đã xong!")
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Lỗi kết nối: {e}")
                    st.warning("Mẹo: Hãy thử bấm 'Reboot' ứng dụng nếu vừa cập nhật thư viện.")
else:
    st.info("👈 Tải ảnh lên để AI chấm bài.")
