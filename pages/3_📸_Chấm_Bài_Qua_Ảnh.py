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

st.markdown("<h1 class='main-title'>📸 Chấm Bài & Giải Toán Qua Ảnh (Real AI)</h1>", unsafe_allow_html=True)

# --- CẤU HÌNH API ---
with st.sidebar:
    st.header("🔑 Cấu hình AI")
    st.info("Để AI 'nhìn' thấy ảnh, bạn cần nhập Google API Key (Miễn phí).")
    api_key = st.text_input("Nhập Google API Key:", type="password")
    st.markdown("[👉 Lấy Key miễn phí tại đây](https://aistudio.google.com/app/apikey)")

# --- GIAO DIỆN CHÍNH ---
uploaded_file = st.file_uploader("Tải ảnh bài làm hoặc đề bài (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ảnh đã tải lên", use_column_width=True)
    
    with col2:
        st.subheader("📝 Kết quả phân tích:")
        
        analyze_btn = st.button("🔍 Phân tích ngay (Gemini AI)", type="primary")
        
        if analyze_btn:
            if not api_key:
                st.error("⚠️ Vui lòng nhập API Key ở thanh bên trái trước!")
            else:
                try:
                    with st.spinner("AI đang đọc đề và chấm bài... (Vui lòng đợi)"):
                        # Cấu hình AI
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        # Câu lệnh (Prompt) gửi cho AI
                        prompt = """
                        Bạn là một giáo viên Toán giỏi của Việt Nam. Hãy thực hiện các nhiệm vụ sau dựa trên hình ảnh được cung cấp:
                        1. Nhận diện nội dung đề bài và bài làm trong ảnh (nếu có).
                        2. Giải bài toán đó một cách chi tiết, từng bước (Step-by-step).
                        3. Nếu có bài làm của học sinh, hãy chấm điểm và chỉ ra lỗi sai (nếu có).
                        4. Đưa ra lời khuyên để học sinh làm tốt hơn.
                        5. Cuối cùng, hãy dịch một câu động viên ngắn sang tiếng H'Mông.
                        
                        Hãy trình bày kết quả đẹp mắt bằng Markdown, sử dụng công thức toán học LaTeX (dùng dấu $) nếu cần.
                        """
                        
                        # Gọi AI xử lý
                        response = model.generate_content([prompt, image])
                        
                        # Hiển thị kết quả
                        st.success("Đã phân tích xong!")
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Có lỗi xảy ra: {e}")
                    st.warning("Hãy kiểm tra lại API Key của bạn xem đã đúng chưa.")

else:
    st.info("👈 Hãy tải ảnh lên để bắt đầu.")

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư - Powered by Google Gemini")
