import streamlit as st
import base64
from PIL import Image
from io import BytesIO
from groq import Groq

st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông)")

# --- LẤY KEY ---
# Sử dụng groq_api_key thay vì google_api_key
api_key = st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    st.warning("⚠️ Chưa có Groq API Key trong hệ thống.")
    api_key = st.text_input("Nhập Groq API Key:", type="password")

# --- HÀM PHÂN TÍCH ẢNH DÙNG GROQ ---
def analyze_real_image_groq(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    # Lưu ảnh dưới định dạng JPEG (hoặc PNG tùy chọn)
    image.save(buffered, format="JPEG")
    # Mã hóa Base64 cho ảnh
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Khởi tạo Groq Client
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        return f"❌ Lỗi khởi tạo Groq Client: {str(e)}"
    
    # Chuẩn bị nội dung (text + image)
    content = [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
    ]

    # Model hỗ trợ Vision trên Groq:
    MODEL = "llama-3.1-405b-reasoning"  # Hoặc model Vision khác nếu có
    
    try:
        # Gọi API của Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            model=MODEL,
        )
        # Trả về nội dung phản hồi
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Lỗi kết nối Groq: {str(e)}"


# -----------------------------
# 🚀 **TÍNH NĂNG MỚI: CHỤP CAMERA**
# -----------------------------
st.subheader("📷 Hoặc chụp trực tiếp từ Camera")
camera_photo = st.camera_input("Chụp ảnh bài làm tại đây")


# --- GIAO DIỆN TẢI ẢNH ---
st.subheader("📤 Hoặc tải ảnh bài làm (PNG, JPG)")
uploaded_file = st.file_uploader("Chọn ảnh:", type=["png", "jpg", "jpeg"])


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
        st.subheader("🔍 Kết quả:")

        if st.button("Phân tích ngay", type="primary"):
            if not api_key:
                st.error("Thiếu Groq API Key!")
            else:
                with st.spinner("⏳ AI đang xử lý..."):

                    # --- PROMPT SONG NGỮ ---
                    prompt_text = """
Bạn là giáo viên Toán giỏi, đọc ảnh bài làm của học sinh. 
Yêu cầu:

1️⃣ Chép lại đề bài bằng **LaTeX**, hiển thị song song:
🇻🇳 (Tiếng Việt)
🟦 (Tiếng H’Mông)

2️⃣ Chấm bài từng bước:
- Nói học sinh **Đúng / Sai** từng bước.
- Nếu sai, ghi ngắn gọn **Sai ở bước nào & lý do**.
- Hiển thị song song:
🇻🇳 Nhận xét tiếng Việt
🟦 Nhận xét H’Mông

3️⃣ Giải chi tiết:
- Viết từng bước bằng **LaTeX**, hiển thị song song:
🇻🇳 Công thức / bước bằng tiếng Việt
🟦 Công thức / bước bằng tiếng H’Mông
- Nếu học sinh sai → giải lại đúng ở cả hai ngôn ngữ.

MỌI CÂU TRẢ LỜI PHẢI:
- Rõ ràng, đầy đủ, theo thứ tự.
- Song song Việt – H’Mông từng bước.
- Dễ copy vào Word hoặc Overleaf.
"""

                    # Thay đổi gọi hàm
                    result = analyze_real_image_groq(api_key, image, prompt_text)

                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")
                        st.markdown(result)
