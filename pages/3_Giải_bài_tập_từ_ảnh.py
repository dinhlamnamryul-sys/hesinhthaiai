import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import json
import os 

# =========================
#   CẤU HÌNH TRANG
# =========================
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸", layout="wide")

# THAY ĐỔI: Sử dụng Gemini 2.0 Pro
GEMINI_MODEL_NAME = "gemini-2.0-pro"
API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

# =========================
#   HÀM PHÂN TÍCH ẢNH
# =========================
def analyze_real_image(api_key, image, prompt):
    """Gửi yêu cầu phân tích ảnh đến Gemini API."""
    try:
        # Chuyển đổi ảnh sang định dạng RGB và base64
        if image.mode == "RGBA":
            image = image.convert("RGB")

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Đường dẫn API cho generateContent
        url = API_URL_TEMPLATE.format(model_name=GEMINI_MODEL_NAME, api_key=api_key)

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

        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)

        # 1. Xử lý phản hồi JSON
        try:
            data = response.json()
        except json.JSONDecodeError:
            return f"❌ API trả về dữ liệu không phải JSON. Code: {response.status_code}\nPhản hồi: {response.text}"

        # 2. Xử lý Lỗi HTTP (status_code không phải 200)
        if response.status_code != 200:
            msg = data.get("error", {}).get("message", response.text)
            return f"❌ Lỗi HTTP {response.status_code}: {msg}"

        # 3. Lấy nội dung phản hồi từ cấu trúc JSON
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return f"❌ API không trả về nội dung hợp lệ (Thiếu key). Vui lòng kiểm tra Prompt hoặc Model.\nPhản hồi chi tiết: {json.dumps(data, indent=2)}"

    except requests.exceptions.RequestException as req_err:
        return f"❌ Lỗi kết nối mạng/Request: {str(req_err)}"
    except Exception as e:
        return f"❌ Lỗi tổng quát: {str(e)}"

# =========================
#   SIDEBAR
# =========================
api_key = None
with st.sidebar:
    st.title("⚙️ Cài đặt")
    # Cảnh báo bổ sung về chi phí cho model Pro
    st.warning("⚠ Model **Gemini 2.0 Pro** có thể tốn chi phí và có hạn mức khác. Hãy kiểm tra Billing.")
    
    # Ưu tiên lấy key từ Streamlit secrets hoặc Biến môi trường
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key đã được tải từ **st.secrets** (Bảo mật).")
    elif "GEMINI_API_KEY" in os.environ:
        api_key = os.environ["GEMINI_API_KEY"]
        st.success("API Key đã được tải từ **Biến môi trường**.")
    else:
        # Tùy chọn nhập thủ công
        st.info("💡 Không tìm thấy Key tự động. Vui lòng nhập Key thủ công.")
        api_key_input = st.text_input("Dán Google API Key:", type="password")
        if api_key_input:
            api_key = api_key_input
    
    st.info(f"Model được chọn: **{GEMINI_MODEL_NAME}**")

    if api_key:
        st.success("API Key đã sẵn sàng!")
    else:
        st.error("Vui lòng nhập hoặc thiết lập API Key!")


# =========================
#   GIAO DIỆN CHÍNH
# =========================
st.title("📸 Chấm Bài & Giải Toán Việt – H’Mông (Dùng Gemini 2.0 Pro)")

col_in, col_out = st.columns([1, 1.2])

image = None

with col_in:
    st.subheader("📥 Đầu vào ảnh")
    mode = st.radio("Chọn nguồn ảnh:", ["Máy ảnh", "Tải tệp lên"])

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
            st.error("❌ Chưa có API Key hoặc Key không hợp lệ!")
        elif not image:
            st.warning("⚠ Hãy tải ảnh bài làm!")
        else:
            with st.spinner("⏳ Đang phân tích ảnh với Gemini 2.0 Pro..."):
                prompt = """
                Phân tích ảnh bài làm toán:
                1. Chép lại đề bằng LaTeX (song ngữ Việt - H'Mông).
                2. Chấm Đúng/Sai từng bước (song ngữ).
                3. Giải lại bài đúng nhất bằng LaTeX (song ngữ).
                Dùng 🇻🇳 cho tiếng Việt và 🟦 cho tiếng H'Mông.
                Định dạng phản hồi bằng Markdown và dùng các Heading để chia rõ 3 phần.
                """

                # Gọi hàm phân tích ảnh thực tế
                result = analyze_real_image(api_key, image, prompt)
                
                # Hiển thị kết quả
                if result.startswith("❌"):
                    st.error(result)
                else:
                    st.markdown(result)
