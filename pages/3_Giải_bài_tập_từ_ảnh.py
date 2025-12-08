import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# =========================
#   CẤU HÌNH TRANG
# =========================
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸", layout="wide")


# =========================
#   LẤY DANH SÁCH MODEL KHẢ DỤNG (Không cần thiết, ta dùng model cụ thể)
# =========================
# Hàm này bị loại bỏ để đơn giản hóa, ta sẽ dùng trực tiếp model hiệu quả nhất.


# =========================
#   HÀM PHÂN TÍCH ẢNH
# =========================
def analyze_real_image(api_key, model, image, prompt):
    """Gửi yêu cầu phân tích ảnh đến Gemini API."""
    try:
        # Chuyển đổi ảnh sang định dạng RGB và base64
        if image.mode == "RGBA":
            image = image.convert("RGB")

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Đường dẫn API cho generateContent
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": img_base64
                            }
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload)

        # Xử lý phản hồi
        try:
            data = response.json()
        except:
            return f"❌ API trả về dữ liệu không hợp lệ.\nPhản hồi: {response.text}"

        if response.status_code != 200:
            msg = data.get("error", {}).get("message", response.text)
            return f"❌ Lỗi {response.status_code}: {msg}"

        # Lấy nội dung phản hồi từ cấu trúc JSON
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return f"❌ API không trả về nội dung hợp lệ.\nPhản hồi: {data}"

    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"


# =========================
#   SIDEBAR
# =========================
with st.sidebar:
    st.title("⚙️ Cài đặt")
    st.warning("⚠ Để chạy được, Key cần được kích hoạt **Billing** để hưởng **Free Tier**.")
    
    api_key = st.text_input("Dán Google API Key:", type="password")
    
    # Chỉ định model flash là lựa chọn mặc định và hiệu quả nhất
    model = "models/gemini-2.5-flash"
    st.info(f"Model được chọn (Tiết kiệm chi phí): **{model}**")

    if api_key:
        st.success("API Key đã nhập!")
    else:
        st.warning("Vui lòng nhập API Key!")


# =========================
#   GIAO DIỆN CHÍNH
# =========================
st.title("📸 Chấm Bài & Giải Toán Việt – H’Mông")

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Đầu vào ảnh")
    mode = st.radio("Chọn nguồn ảnh:", ["Máy ảnh", "Tải tệp lên"])

    image = None
    if mode == "Máy ảnh":
        cam_file = st.camera_input("Chụp bài làm")
        if cam_file:
            image = Image.open(cam_file)
    else:
        up_file = st.file_uploader("Chọn ảnh bài làm", type=["png", "jpg", "jpeg"])
        if up_file:
            image = Image.open(up_file)

    if image:
        st.image(image, caption="Ảnh đã tải", use_container_width=True)


with col_out:
    st.subheader("🔍 Kết quả AI")

    if st.button("🚀 Bắt đầu chấm bài", type="primary"):
        if not api_key:
            st.error("❌ Chưa nhập API Key!")
        elif not image:
            st.warning("⚠ Hãy tải ảnh bài làm!")
        else:
            with st.spinner("⏳ Đang phân tích ảnh..."):
                prompt = """
                Phân tích ảnh bài làm toán:
                1. Chép lại đề bằng LaTeX (song ngữ Việt - H'Mông).
                2. Chấm Đúng/Sai từng bước (song ngữ).
                3. Giải lại bài đúng nhất bằng LaTeX (song ngữ).
                Dùng 🇻🇳 cho tiếng Việt và 🟦 cho tiếng H'Mông.
                """

                # Gọi hàm phân tích ảnh thực tế
                result = analyze_real_image(api_key, model, image, prompt)
                st.markdown(result)
