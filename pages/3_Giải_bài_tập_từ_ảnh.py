import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
import os

# ============================================
# GOOGLE OAUTH CONFIG
# ============================================
CLIENT_SECRET_FILE = "client_secret.json"
SCOPES = ["openid", "email", "profile"]

if "google_user" not in st.session_state:
    st.session_state.google_user = None

# ============================================
# STREAMLIT PAGE
# ============================================
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸", layout="wide")

st.title("📸 Chấm Bài & Giải Toán Việt – H’Mông")

# ============================================
# LOGIN LOGIC
# ============================================
def login_button():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:8501"
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    st.markdown(f"[➡️ Đăng nhập Google để sử dụng ứng dụng]({auth_url})")


def check_google_login():
    if "code" in st.query_params:
        code = st.query_params["code"]

        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=SCOPES,
            redirect_uri="http://localhost:8501"
        )
        flow.fetch_token(code=code)

        credentials = flow.credentials
        req = google.auth.transport.requests.Request()
        id_info = id_token.verify_oauth2_token(credentials.id_token, req)

        st.session_state.google_user = id_info


# ============================================
# GEMINI API CALL — dùng API Key hệ thống
# ============================================
API_KEY = os.getenv("GEMINI_API_KEY")  # <== bạn đặt API Key trong môi trường !!!

def analyze_real_image(model, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"

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
    data = response.json()

    if response.status_code != 200:
        return f"❌ Lỗi {response.status_code}: {data}"

    return data["candidates"][0]["content"]["parts"][0]["text"]


# ============================================
# MAIN UI
# ============================================

check_google_login()

if st.session_state.google_user is None:
    st.warning("⚠️ Bạn cần đăng nhập Google để sử dụng ứng dụng.")
    login_button()
    st.stop()

# Nếu đã đăng nhập
st.success(f"✔️ Đã đăng nhập: {st.session_state.google_user['email']}")

# Danh sách model
models = [
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-lite",
    "models/gemini-1.5-flash-8b",
]

model = st.sidebar.selectbox("Chọn model:", models)

# =========================
#   GIAO DIỆN CHÍNH
# =========================
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
        if not image:
            st.warning("⚠️ Hãy tải ảnh bài làm!")
        else:
            with st.spinner("⏳ Đang phân tích ảnh..."):
                prompt = """
                Phân tích ảnh bài làm toán:
                1. Chép lại đề bằng LaTeX (song ngữ Việt - H'Mông).
                2. Chấm Đúng/Sai từng bước (song ngữ).
                3. Giải lại bài đúng nhất bằng LaTeX (song ngữ).
                Dùng 🇻🇳 cho tiếng Việt và 🟦 cho tiếng H'Mông.
                """
                result = analyze_real_image(model, image, prompt)
                st.markdown(result)
