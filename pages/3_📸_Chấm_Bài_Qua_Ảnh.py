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
    .debug-info { font-size: 0.8em; color: grey; text-align: center; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📸 Chấm Bài & Giải Toán Qua Ảnh</h1>", unsafe_allow_html=True)

# --- CẤU HÌNH API ---
api_key = None
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]

with st.sidebar:
    st.header("⚙️ Thông tin hệ thống")
    # Kiểm tra phiên bản thư viện
    try:
        version = genai.__version__
        st.success(f"Phiên bản AI: {version}")
        if version < "0.7.0":
            st.error("⚠️ Phiên bản quá cũ! Hãy cập nhật requirements.txt")
    except:
        st.error("Không tìm thấy thư viện AI")

    if not api_key:
        st.warning("Chưa có Key hệ thống.")
        api_key = st.text_input("Nhập API Key cá nhân:", type="password")

# --- HÀM GỌI AI THÔNG MINH (Tự động thử nhiều model) ---
def try_generate_content(api_key, prompt, image):
    genai.configure(api_key=api_key)
    
    # Danh sách các tên model để thử lần lượt
    models_to_try = [
        'gemini-1.5-flash',          # Tên chuẩn
        'models/gemini-1.5-flash',   # Tên đầy đủ
        'gemini-1.5-flash-latest',   # Bản mới nhất
        'gemini-pro-vision'          # Bản cũ (Dự phòng cuối cùng)
    ]
    
    last_error = ""
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([prompt, image])
            return response.text, model_name # Trả về kết quả và tên model thành công
        except Exception as e:
            last_error = str(e)
            continue # Thử model tiếp theo
            
    raise Exception(f"Đã thử tất cả model nhưng đều thất bại. Lỗi cuối cùng: {last_error}")

# --- GIAO DIỆN CHÍNH ---
if api_key:
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
                        
                        prompt = """
                        Bạn là giáo viên Toán. Hãy nhìn hình ảnh và:
                        1. Nhận diện đề bài và bài làm.
                        2. Kiểm tra bài làm đúng hay sai. Chỉ rõ lỗi sai.
                        3. Giải lại bài toán chi tiết từng bước.
                        4. Dịch một lời khen ngắn sang tiếng H'Mông.
                        """
                        
                        # Gọi hàm thông minh
                        result_text, success_model = try_generate_content(api_key, prompt, image)
                        
                        st.success(f"Đã chấm xong! (Sử dụng: {success_model})")
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown(result_text)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error("❌ Có lỗi xảy ra:")
                    st.code(str(e))
                    st.info("Gợi ý: Hãy thử Reboot ứng dụng trong phần Manage App.")
    else:
        st.info("👈 Hãy tải ảnh lên để bắt đầu.")
else:
    st.error("⚠️ Hệ thống chưa được kích hoạt. Vui lòng liên hệ Admin để nhập Key.")
