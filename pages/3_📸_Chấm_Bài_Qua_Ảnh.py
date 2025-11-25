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
    .login-success { background-color: #e8f5e9; color: #2e7d32; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📸 Chấm Bài & Giải Toán Qua Ảnh</h1>", unsafe_allow_html=True)

# --- XỬ LÝ ĐĂNG NHẬP TỰ ĐỘNG (SECRETS) ---
api_key = None

# 1. Kiểm tra xem Admin đã cài Key trong hệ thống chưa
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]

# 2. Nếu chưa có Key hệ thống, hiện ô nhập tay (Dự phòng)
if not api_key:
    with st.sidebar:
        st.header("🔑 Cấu hình")
        st.warning("Chưa tìm thấy Key hệ thống.")
        api_key = st.text_input("Nhập API Key cá nhân:", type="password")
        st.markdown("[👉 Lấy Key miễn phí](https://aistudio.google.com/app/apikey)")

# --- GIAO DIỆN CHÍNH ---
if api_key:
    # Chỉ hiện thông báo nếu dùng Key hệ thống
    if "GOOGLE_API_KEY" in st.secrets:
        st.markdown('<div class="login-success">🔓 Đã kích hoạt bản quyền AI Nhà trường</div>', unsafe_allow_html=True)
    
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
                try:
                    with st.spinner("Đang kết nối máy chủ Google Gemini..."):
                        # Cấu hình AI
                        genai.configure(api_key=api_key)
                        
                        # --- ĐÃ SỬA: Dùng model 'gemini-pro-vision' để tương thích tốt nhất ---
                        model = genai.GenerativeModel('gemini-pro-vision')
                        
                        prompt = """
                        Bạn là giáo viên Toán. Hãy nhìn hình ảnh và:
                        1. Viết lại đề bài và bài làm trong ảnh (dùng công thức LaTeX).
                        2. Kiểm tra xem bài làm đúng hay sai. Chỉ ra lỗi sai cụ thể (nếu có).
                        3. Giải lại bài toán thật chi tiết từng bước.
                        4. Cuối cùng, dịch một lời nhận xét/động viên ngắn sang tiếng H'Mông.
                        """
                        
                        # Gọi AI xử lý (Cú pháp cho gemini-pro-vision là [prompt, image])
                        response = model.generate_content([prompt, image])
                        
                        st.success("Đã xong!")
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Lỗi kết nối: {e}")
                    st.warning("Nếu lỗi vẫn xảy ra, hãy kiểm tra lại API Key của bạn.")
    else:
        st.info("👈 Hãy tải ảnh lên để bắt đầu chấm bài.")

else:
    # Nếu không có Key nào cả
    st.error("⚠️ Hệ thống chưa được kích hoạt. Vui lòng liên hệ Admin để nhập Key.")
    st.image("https://cdn-icons-png.flaticon.com/512/6195/6195699.png", width=100)

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư - Powered by Google Gemini")
