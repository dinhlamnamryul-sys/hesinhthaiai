import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# =========================
#   CẤU HÌNH TRANG
# =========================
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸", layout="wide")


# =========================
#   HÀM LẤY DANH SÁCH MODEL
# =========================
def list_models(api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return []
        data = r.json()
        models = data.get("models", [])

        # Lọc model có hỗ trợ generateContent hoặc vision
        good_models = []
        for m in models:
            name = m.get("name", "")
            supported = m.get("supportedMethods", [])
            caps = m.get("capabilities", [])
            if "generateContent" in supported or "vision" in caps:
                good_models.append(name)

        return good_models
    except:
        return []


# =========================
#   HÀM PHÂN TÍCH ẢNH
# =========================
def analyze_real_image(api_key, model, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Encode ảnh sang base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # URL chuẩn của API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_base64
                    }}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if response.status_code == 404:
            return "❌ Lỗi 404: Model không tồn tại. Hãy chọn model khác trong sidebar."

        if response.status_code != 200:
            msg = data.get("error", {}).get("message", response.text)
            return f"❌ Lỗi {response.status_code}: {msg}"

        # Lấy nội dung trả về
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return str(data)

    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"


# =========================
#   SIDEBAR
# =========================
with st.sidebar:
    st.title("⚙️ Cài đặt")

    api_key = st.text_input("Dán Google API Key:", type="password")

    if api_key:
        st.success("API Key hợp lệ, đang tải model...")

        # Gọi list models
        models = list_models(api_key)

        if len(models) == 0:
            st.error("Không tải được model. Kiểm tra lại API Key hoặc bật billing.")
            model = None
        else:
            model = st.selectbox("Chọn model:", models)
            st.info(f"Đang dùng: **{model}**")
    else:
        model = None
        st.warning("Vui lòng nhập API Key!")


# =========================
#   GIAO DIỆN CHÍNH
# =========================
st.title("📸 Chấm Bài & Giải Toán Việt – H’Mông")

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Đầu vào")
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
        st.image(image, caption="Ảnh đã nạp", use_container_width=True)


with col_out:
    st.subheader("🔍 Kết quả AI")

    if st.button("🚀 Bắt đầu chấm bài", type="primary"):
        if not api_key:
            st.error("Bạn chưa nhập API Key!")
        elif not model:
            st.error("Bạn chưa chọn model hợp lệ.")
        elif not image:
            st.warning("Hãy cung cấp ảnh trước.")
        else:
            with st.spinner("Đang phân tích ảnh..."):
                prompt = """
                Phân tích ảnh bài làm toán:
                1. Chép lại đề bằng LaTeX (song ngữ Việt - H'Mông).
                2. Chấm Đúng/Sai từng bước (song ngữ).
                3. Giải lại bài đúng nhất bằng LaTeX (song ngữ).
                Dùng ký hiệu 🇻🇳 cho tiếng Việt và 🟦 cho tiếng H'Mông.
                """

                result = analyze_real_image(api_key, model, image, prompt)
                st.markdown(result)
