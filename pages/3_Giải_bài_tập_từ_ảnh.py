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

st.title("📸 Chấm Bài & Giải Toán Việt – H’Mông (FULL AI Gemini)")

# ==========================================================
#   HÀM CHECK LIST MODELS (Google yêu cầu để chọn model hợp lệ)
# ==========================================================
def get_available_models(api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url, timeout=20)
        data = response.json()

        if response.status_code != 200:
            return None, f"❌ Lỗi lấy model: {data}"

        models = data.get("models", [])

        # Lọc model có hỗ trợ generateContent
        usable = [
            m["name"]
            for m in models
            if "generateContent" in m.get("supportedGenerationMethods", [])
        ]

        return usable, None

    except Exception as e:
        return None, f"❌ Lỗi ListModels: {str(e)}"


# ==========================================================
#   HÀM PHÂN TÍCH ẢNH (CALL GEMINI)
# ==========================================================
def analyze_real_image(api_key, model_name, image, prompt):
    try:
        if image.mode == "RGBA":
            image = image.convert("RGB")

        # Encode ảnh
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # API endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

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

        # ---- Xử lý JSON ----
        try:
            data = response.json()
        except:
            return f"❌ API trả về dữ liệu không phải JSON: {response.text}"

        if response.status_code != 200:
            err = data.get("error", {}).get("message", response.text)
            return f"❌ Lỗi HTTP {response.status_code}: {err}"

        # ---- Lấy nội dung text ----
        try:
            parts = data["candidates"][0]["content"]["parts"]
            text = "".join([p.get("text", "") for p in parts])
            return text
        except:
            return f"❌ Cấu trúc phản hồi không đúng:\n{json.dumps(data, indent=2)}"

    except Exception as e:
        return f"❌ Lỗi gọi API: {str(e)}"


# ==========================================================
#   SIDEBAR — NHẬP API KEY & CHỌN MODEL
# ==========================================================
api_key = None
selected_model = None

with st.sidebar:
    st.title("⚙️ Cấu hình Gemini API")

    # Tự lấy key từ secrets hoặc biến môi trường
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key đã lấy từ st.secrets")
    elif "GEMINI_API_KEY" in os.environ:
        api_key = os.environ["GEMINI_API_KEY"]
        st.success("API Key đã lấy từ biến môi trường")
    else:
        api_key_input = st.text_input("Nhập Google API Key:", type="password")
        if api_key_input:
            api_key = api_key_input

    if not api_key:
        st.error("⛔ Chưa có API Key!")
    else:
        st.success("✔ API Key hợp lệ!")

        # ---- LOAD MODEL ----
        st.subheader("📡 Kiểm tra model khả dụng")

        if st.button("🔍 Tải danh sách model"):
            with st.spinner("Đang tải danh sách model từ Google..."):
                models, err = get_available_models(api_key)

                if err:
                    st.error(err)
                else:
                    st.success("✔ Tải thành công!")

                    if len(models) == 0:
                        st.error("❌ API Key của bạn không có model generateContent!")
                    else:
                        st.info("📌 Các model bạn có thể dùng:")
                        for m in models:
                            st.code(m)

                        selected_model = st.selectbox(
                            "Chọn model để sử dụng:",
                            options=models
                        )

        # Cho phép nhập model thủ công nếu cần
        st.subheader("✏ Nhập model thủ công (nếu đã biết):")
        manual = st.text_input("Model (ví dụ: gemini-2.5-flash)")
        if manual:
            selected_model = manual


# ==========================================================
#   GIAO DIỆN CHÍNH — UPLOAD ẢNH
# ==========================================================
st.header("🖼️ 1. Tải ảnh bài làm")

image = None

mode = st.radio("Chọn nguồn ảnh", ["Chụp ảnh", "Tải từ máy"])

if mode == "Chụp ảnh":
    cam = st.camera_input("Chụp ảnh bài làm")
    if cam:
        image = Image.open(cam)
else:
    up = st.file_uploader("Chọn ảnh", type=["png", "jpg", "jpeg"])
    if up:
        image = Image.open(up)

if image:
    st.image(image, caption="Ảnh đã tải", use_container_width=True)

# ==========================================================
#   NÚT XỬ LÝ
# ==========================================================
st.header("🤖 2. AI Chấm bài")

if st.button("🚀 Bắt đầu chấm"):
    if not api_key:
        st.error("❌ Chưa có API Key!")
    elif not selected_model:
        st.error("❌ Bạn chưa chọn model!")
    elif not image:
        st.error("❌ Chưa có ảnh bài làm!")
    else:
        with st.spinner("⏳ AI đang chấm bài..."):
            prompt = """
            Phân tích ảnh bài làm toán:
            1. Chép lại đề bằng LaTeX (song ngữ Việt - H'Mông).
            2. Chấm Đúng/Sai từng bước (song ngữ).
            3. Giải lại bài đúng nhất bằng LaTeX (song ngữ).
            Dùng 🇻🇳 cho tiếng Việt và 🟦 cho tiếng H'Mông.
            Định dạng Markdown, rõ ràng 3 phần.
            """

            result = analyze_real_image(api_key, selected_model, image, prompt)

            if result.startswith("❌"):
                st.error(result)
            else:
                st.markdown(result)
