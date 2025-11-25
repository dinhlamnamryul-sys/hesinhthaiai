import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

st.set_page_config(page_title="Chấm Bài AI", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh")

# --- 1. CẤU HÌNH API KEY ---
api_key = None
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]

if not api_key:
    st.warning("⚠️ Chưa có API Key hệ thống.")
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- 2. HÀM TỰ ĐỘNG TÌM MODEL KHẢ DỤNG ---
def get_best_model():
    """Hỏi Google xem tài khoản này được dùng model nào"""
    try:
        # Lấy danh sách tất cả model
        models = genai.list_models()
        
        # Ưu tiên tìm model Flash (Nhanh) hoặc Pro (Thông minh)
        priority_models = []
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                # Lưu lại tên model (ví dụ: models/gemini-1.5-flash-001)
                priority_models.append(m.name)
        
        # Chọn model tốt nhất
        # Ưu tiên 1.5 Flash -> 1.5 Pro -> Pro Vision
        for m_name in priority_models:
            if 'flash' in m_name and '1.5' in m_name: return m_name
        
        for m_name in priority_models:
            if 'pro' in m_name and '1.5' in m_name: return m_name
            
        for m_name in priority_models:
            if 'vision' in m_name: return m_name
            
        # Nếu không tìm thấy cái nào quen thuộc, lấy cái đầu tiên trong danh sách
        if priority_models:
            return priority_models[0]
            
        return None
    except Exception as e:
        return None

# --- 3. GIAO DIỆN XỬ LÝ ---
uploaded_file = st.file_uploader("Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải", use_column_width=True)
    
    if st.button("🔍 Phân tích ngay", type="primary"):
        try:
            with st.spinner("Đang khởi động AI..."):
                # Cấu hình
                genai.configure(api_key=api_key)
                
                # --- BƯỚC QUAN TRỌNG: Tự tìm model ---
                active_model_name = get_best_model()
                
                if not active_model_name:
                    st.error("❌ Lỗi: API Key này không tìm thấy model nào khả dụng. Hãy thử tạo Key mới.")
                else:
                    # st.info(f"Đang sử dụng mô hình: `{active_model_name}`") # Hiện tên model để debug
                    
                    model = genai.GenerativeModel(active_model_name)
                    
                    prompt = """
                    Bạn là giáo viên Toán. Hãy nhìn ảnh và:
                    1. Viết lại đề bài và bài làm (dùng LaTeX cho công thức).
                    2. Kiểm tra bài làm đúng hay sai. Chỉ rõ lỗi sai.
                    3. Giải lại bài toán chi tiết.
                    4. Dịch một lời khen ngắn sang tiếng H'Mông.
                    """
                    
                    response = model.generate_content([prompt, image])
                    st.success("Đã xong!")
                    st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Vẫn có lỗi xảy ra: {e}")
            st.warning("Lời khuyên cuối cùng: Hãy vào Google AI Studio tạo một API Key mới tinh và thay thế Key cũ.")
