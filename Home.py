# Thêm thư viện này ở đầu file nếu chưa có
import base64
import os

# Đường dẫn đến file ảnh nền (Đảm bảo file này nằm cùng thư mục với file code)
BACKGROUND_IMAGE_PATH = "bantrang.jpg" 

# Hàm chuyển ảnh thành Base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    # Nếu file không tồn tại, trả về chuỗi rỗng
    return ""

# Lấy chuỗi Base64 của ảnh nền
base64_image = get_base64_image(BACKGROUND_IMAGE_PATH)

# --- 2. CSS GIAO DIỆN (ĐÃ CẬP NHẬT) ---
st.markdown(f"""
<style>
    /* ------------------------------------------------------------------- */
    /* CẬP NHẬT: ĐẶT ẢNH NỀN */
    .stApp {{
        background-color: #f8f9fa; 
        margin-bottom: 60px;
        {"background-image: url(data:image/jpg;base64," + base64_image + ");" if base64_image else ""}
        background-size: cover; /* Đảm bảo ảnh nền phủ kín trang */
        background-position: center; /* Căn giữa ảnh nền */
        background-attachment: fixed; /* Giữ ảnh nền cố định khi cuộn */
    }}
    /* ------------------------------------------------------------------- */
    
    /* Các CSS khác của bạn */
    [data-testid="stHeader"] {{ background-color: rgba(0,0,0,0); color: transparent; }}
    [data-testid="stToolbar"] {{ visibility: hidden !important; display: none !important; }}
    [data-testid="stDecoration"] {{ visibility: hidden !important; display: none !important; }}
    [data-testid="stSidebarCollapsedControl"] {{
        visibility: visible !important; display: block !important;
        color: #b71c1c !important; background-color: white; border-radius: 50%;
        padding: 5px; z-index: 999999;
    }}
    /* Điều chỉnh các phần tử chính để nền không bị che */
    .main-header, .feature-card, [data-testid="stSidebar"], .footer {{
        background-color: rgba(255, 255, 255, 0.95); /* Giảm độ trong suốt để dễ đọc */
    }}
    /* Điều chỉnh nền Sidebar nếu cần */
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.85); /* Sidebar trong suốt hơn một chút */
    }}

    .main-header {{
        background: linear-gradient(135deg, rgba(183, 28, 28, 0.9) 0%, rgba(211, 47, 47, 0.9) 60%, rgba(255, 111, 0, 0.9) 100%);
        color: white; padding: 30px; border-radius: 20px; text-align: center;
        box-shadow: 0 10px 30px rgba(183, 28, 28, 0.4); border-bottom: 6px solid #fdd835;
        margin-bottom: 20px; margin-top: -20px;
    }}
    .main-header h1 {{ font-size: 2.5rem; font-weight: 900; margin: 0; }}
    .feature-card {{
        background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 20px; text-align: center;
        border: 1px solid #eee; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 350px; display: flex; flex-direction: column; justify-content: space-between;
        transition: transform 0.3s;
    }}
    .feature-card:hover {{ transform: translateY(-5px); border-color: #ff9800; }}
    .icon-box {{ font-size: 3.5rem; margin-bottom: 10px; }}
    .card-title {{ color: #d84315; font-weight: 800; font-size: 1.3rem; margin-bottom: 5px; }}
    .stButton>button {{
        width: 100%; border-radius: 50px; background: linear-gradient(90deg, #ff6f00, #ffca28);
        border: none; color: white; font-weight: bold; padding: 10px 0;
    }}
    .stButton>button:hover {{ transform: scale(1.05); }}
    .footer {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: rgba(255, 255, 255, 0.95); color: #555; text-align: center;
        padding: 10px; font-size: 14px; border-top: 3px solid #b71c1c;
        z-index: 999; box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }}
    .footer p {{ margin: 0; font-family: sans-serif; line-height: 1.5; }}
    
    /* CSS cho trình phát nhạc */
    audio {{
        width: 60%; 
        border-radius: 30px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
</style>
""", unsafe_allow_html=True)
