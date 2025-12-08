import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import json
import os 

# =========================
#   CẤU HÌNH TRANG
# =========================
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸", layout="wide")

GEMINI_MODEL_NAME = "gemini-2.0-pro"
API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

# =========================
#   HÀM PHÂN TÍCH ẢNH
# =========================
def analyze_real_image(api_key, image, prompt):
    try:
        if image.mode == "RGBA":
            image = image.convert("RGB")

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

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

        # ❗ Kiểm tra JSON trả về
        try:
            data = response.json()
        except:
            return f"❌ API trả về dữ liệu không phải JSON.\n{response.text}"

        # ❗ Kiểm tra lỗi HTTP
        if response.status_code != 200:
            msg = data.get("error", {}).get("message", response.text)
            return f"❌ Lỗi HTTP {response.status_code}: {msg}"

        # ⭐ LẤY NỘI DUNG THEO CẤU TRÚC MỚI ⭐
        try:
            parts = data["candidates"][0]["content"]["parts"]
            text_response = "".join([p.get("text", "") for p in parts])
            return text_response if text_response.strip() else "❌ API không trả về nội dung."
        except Exception:
            return f"❌ API không trả về đúng cấu trúc.\n{json.dumps(data, indent=2)}"

    except Exception as e:
        return f"❌ Lỗi tổng quát: {str(e)}"


# =========================
#   SIDEBAR
# =========================
api_key = None
with st.sidebar:
    st.title("⚙️ Cài đặt")
    st.warning("⚠ Gemini 2.0 Pro có thể tốn chi phí – hãy kiểm tra Billing.")

    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key đã tải từ st.secrets.")
    elif "GEMINI_API_KEY" in os.environ:
        api_key = os.environ["GEMINI_API_KEY"]
        st.success("API Key đã tải từ biến môi trường.")
    else:
        api_key_input = st.text_input("Nhập Google API Key:", type="password")
        if api_key_input:
            api_key = api_key_input

    st.info(f"Model: **{GEMINI_MODEL_NAME}**")

    if api_key:
        st.success("API Key hợp lệ!")
    else:
        st.error("Vui lòng nhập API Key!")


# =========================
#   GIAO DIỆN CHÍNH
# =========================
st.title("📸 Chấm Bài & Giải Toán Việt – H’Mông (Gemini 2.0 Pro)")

col_in, col_out = st.columns([1, 1.2])

image = None

with col_in:
    st.subheader("📥 Ảnh đầu vào")
    mode = st.radio("Chọn nguồn ảnh:", ["Máy ảnh", "Tải lên"])

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

    if st.button("🚀 Bắt đầu chấm bài"):
        if not api_key:
            st.error("❌ Chưa có API Key!")
        elif not image:
            st.warning("⚠ Hãy tải một ảnh bài làm!")
        else:
            with st.spinner("⏳ Gemini đang phân tích..."):
                prompt = """
                Phân tích ảnh bài làm toán:
                1. Chép lại đề bằng LaTeX (song ngữ Việt - H'Mông).
                2. Chấm Đúng/Sai từng bước (song ngữ).
                3. Giải lại bài đúng nhất bằng LaTeX (song ngữ).
                Dùng 🇻🇳 cho tiếng Việt và 🟦 cho tiếng H'Mông.
                Định dạng Markdown và chia rõ 3 phần.
                """

                result = analyze_real_image(api_key, image, prompt)

                if result.startswith("❌"):
                    st.error(result)
                else:
                    st.markdown(result)
