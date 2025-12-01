import streamlit as st
import os
import base64

# --- CẤU HÌNH LOGO VÀ HÌNH NỀN ---
LOGO_PATH = "image_2.png.png" 
LOGO_URL_ONLINE = "https://cdn-icons-png.flaticon.com/512/2997/2997235.png"
BACKGROUND_IMAGE_PATH = "bantrang.jpg" # Đường dẫn ảnh nền

if os.path.exists(LOGO_PATH):
    app_icon = LOGO_PATH
    sidebar_logo = LOGO_PATH
else:
    app_icon = LOGO_URL_ONLINE
    sidebar_logo = LOGO_URL_ONLINE

# --- HÀM XỬ LÝ ẢNH/NHẠC BASE64 ---
def get_base64_image(image_path):
    """Hàm chuyển ảnh thành Base64 để sử dụng trong CSS"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            # Gán giá trị cho biến base64_image ở đây
            return base64.b64encode(img_file.read()).decode()
    return ""

def get_audio_html(file_path):
    # ... (giữ nguyên hàm này)
    pass 

# --- GỌI HÀM VÀ KHAI BÁO BIẾN TRƯỚC KHI SỬ DỤNG ---
base64_image = get_base64_image(BACKGROUND_IMAGE_PATH) # <-- RẤT QUAN TRỌNG: Gọi hàm TẠO biến base64_image ở đây

# Gọi hàm lấy source nhạc
MUSIC_FILE = "nhac_nen.mp3"
audio_source_html = get_audio_html(MUSIC_FILE)


# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Cổng Giáo Dục Số - Trường Na Ư",
    page_icon=app_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS GIAO DIỆN (Sử dụng base64_image đã được tạo) ---
st.markdown(f"""
<style>
    /* ... (Phần CSS của bạn) ... */
    .stApp {{
        background-color: #f8f9fa; 
        margin-bottom: 60px;
        {"background-image: url(data:image/jpg;base64," + base64_image + ");" if base64_image else ""}
        background-size: cover; 
        background-position: center; 
        background-attachment: fixed; 
    }}
    /* ... (Phần CSS còn lại của bạn) ... */
</style>
""", unsafe_allow_html=True)
# ... (Phần còn lại của code) ...
