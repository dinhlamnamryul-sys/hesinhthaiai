import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import json 

# --- PROMPT ĐÃ ĐƯỢC TÁCH RA NGOÀI (GIẢM LỖI THỤT LỀ) ---
PROMPT_TEXT = """
Thầy là giáo viên Toán giỏi, chuyên đọc và chấm bài tập của học sinh qua ảnh. 
Thầy sẽ giải đáp bài tập theo các yêu cầu nghiêm ngặt sau:

🎯 YÊU CẦU ĐỊNH DẠNG RẤT QUAN TRỌNG (ĐỂ TRÁNH LỖI HIỂN THỊ):
1. **Tuyệt đối KHÔNG** sử dụng các lệnh định dạng tài liệu LaTeX như \documentclass, \usepackage, \begin{document}, \begin{longtable}.
2. **Chỉ** sử dụng cú pháp **Markdown** (###, **bold**, *italic*, bullet points) và công thức **LaTeX toán học** ($...$ hoặc $$...$$) để hiển thị.
3. Luôn đảm bảo **Tiếng Việt** và **Tiếng H’Mông** được hiển thị rõ ràng, song song (ví dụ: sử dụng Markdown table với hai cột).

📝 YÊU CẦU VỀ NỘI DUNG (DÙNG GIỌNG THẦY):

1️⃣ **ĐỀ BÀI (Tiếng Việt & Tiếng H’Mông):**
- Chép lại đề bài bằng Markdown/LaTeX.
- Luôn hiển thị song song: 🇻🇳 (Tiếng Việt) | 🟦 (Tiếng H’Mông)

2️⃣ **CHẤM BÀI & CHỈ RA LỖI SAI (THEO TỪNG BƯỚC CỤ THỂ):**
- Phải so sánh **TỪNG BƯỚC** giải của học sinh với lời giải đúng.
- Ghi rõ ràng: **"Bước X: [ĐÚNG/SAI]"** cho từng bước.
- Nếu **SAI**: Phải chỉ ra **vị trí SAI** và **LÝ DO SAI** một cách ngắn gọn, rõ ràng, bằng cả hai ngôn ngữ.
- Hiển thị song song: 🇻🇳 Nhận xét tiếng Việt | 🟦 Nhận xét H’Mông

3️⃣ **GIẢI CHI TIẾT ĐÚNG (TỪNG BƯỚC MỘT):**
- Cung cấp **LỜI GIẢI HOÀN CHỈNH, ĐÚNG** và **RẤT CHI TIẾT** cho đề bài.
- **Mỗi bước giải** phải nằm trên **MỘT DÒNG RIÊNG** (xuống dòng liên tục, sử dụng khoảng trắng).
- Công thức Toán học **BẮT BUỘT** phải dùng **LaTeX** ($...$ hoặc $$...$$).
- Luôn hiển thị song song công thức/bước giải bằng cả hai thứ tiếng:
    * 🇻🇳 Công thức/Bước giải bằng tiếng Việt (LaTeX)
    * 🟦 Công thức/Bước giải bằng tiếng H’Mông (LaTeX)

MỌI CÂU TRẢ LỜI PHẢI:
- Rõ ràng, đầy đủ, theo thứ tự 1, 2, 3.
- Kết thúc bằng một lời khuyên ngắn gọn cho học sinh (dùng giọng Thầy).
"""
# --- HẾT PROMPT ---


st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸", layout="wide")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông)")

# --- LẤY KEY VÀ HƯỚNG DẪN ---
st.subheader("🔑 Nhập Google Gemini API Key")

if 'manual_api_key' not in st.session_state:
    st.session_state['manual_api_key'] = ""

api_key = st.secrets.get("GOOGLE_API_KEY", st.session_state['manual_api_key'])

if not api_key:
    st.session_state['manual_api_key'] = st.text_input(
        "Vui lòng dán Key của bạn vào đây:", 
        type="password",
        value=st.session_state['manual_api_key']
    )
    api_key = st.session_state['manual_api_key']
else:
    st.success("✅ Đã tìm thấy API Key.")
    
with st.expander("❓ Bạn chưa có Key? Nhấn vào đây để xem hướng dẫn lấy Key."):
    st.markdown("""
        Để sử dụng ứng dụng này, bạn cần có **Google Gemini API Key** (miễn phí ở mức cơ bản).

        1. **Truy cập trang tạo Key:** Bạn truy cập trang [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key).
        2. **Đăng nhập** bằng tài khoản Google của bạn.
        3. Nhấn vào nút **"Create API key"** (Tạo API Key).
        4. **Sao chép** chuỗi Key được tạo ra.
        5. **Dán** chuỗi Key đó vào ô nhập liệu bên trên.
    """)

# --- HÀM PHÂN TÍCH ẢNH ---
def analyze_real_image(api_key, image, prompt):
    if not api_key:
        return "❌ Lỗi: API Key bị thiếu hoặc không được cung cấp."
        
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    MODEL = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload)
        
        if response.status_code != 200:
            error_details = response.text
            try:
                error_json = response.json()
                if "error" in error_json and "message" in error_json["error"]:
                    error_details = error_json["error"]["message"]
            except json.JSONDecodeError:
                pass 
                
            return f"❌ Lỗi API **{response.status_code}** ({response.reason}): {error_details}"
            
        data = response.json()
        
        if not data.get("candidates"):
             return f"❌ Lỗi: API trả về phản hồi rỗng hoặc không có ứng cử viên (candidates)."
             
        return data["candidates"][0]["content"]["parts"][0]["text"]
        
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"


# -----------------------------
# 🚀 TÍNH NĂNG CHỤP CAMERA/TẢI ẢNH
# -----------------------------
st.markdown("---")
st.subheader("📷 Tải ảnh bài làm hoặc chụp trực tiếp")
col_upload, col_camera = st.columns(2)

with col_camera:
    camera_photo = st.camera_input("Chụp ảnh bài làm tại đây")

with col_upload:
    uploaded_file = st.file_uploader("Chọn ảnh từ máy tính (PNG, JPG)", type=["png", "jpg", "jpeg"])


# --- CHỌN NGUỒN ẢNH ƯU TIÊN ---
image = None

if camera_photo is not None:
    image = Image.open(camera_photo)
elif uploaded_file is not None:
    image = Image.open(uploaded_file)


# Nếu có ảnh → hiển thị + xử lý
if image:
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(image, caption="Ảnh bài làm", use_column_width=True)

    with col2:
        st.subheader("🔍 Kết quả Phân tích:")

        if st.button("Phân tích ngay", type="primary"):
            if not api_key:
                st.error("Thiếu API Key! Vui lòng nhập Key vào ô bên trên.")
            else:
                with st.spinner("⏳ AI đang xử lý..."):

                    # Sử dụng PROMPT_TEXT đã được định nghĩa ở trên
                    result = analyze_real_image(api_key, image, PROMPT_TEXT)

                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")
                        st.markdown(result)
