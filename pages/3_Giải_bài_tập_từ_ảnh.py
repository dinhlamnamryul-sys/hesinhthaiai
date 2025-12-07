import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
from io import BytesIO

# =========================
#   CẤU HÌNH TRANG
# =========================
st.set_page_config(page_title="Chấm Bài AI Song Ngữ (OpenAI)", page_icon="📸", layout="wide")


# =========================
#   HÀM MÃ HÓA ẢNH
# =========================
def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    return img_base64


# =========================
#   HÀM PHÂN TÍCH ẢNH
# =========================
def analyze_with_openai(api_key, image, prompt):
    client = OpenAI(api_key=api_key)

    img_b64 = encode_image(image)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # HỖ TRỢ XỬ LÝ ẢNH MIỄN PHÍ
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{img_b64}"
                        }
                    ]
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Lỗi: {str(e)}"


# =========================
#   SIDEBAR
# =========================
with st.sidebar:
    st.title("⚙️ Cài đặt OpenAI")

    api_key = st.text_input("Dán OpenAI API Key của bạn:", type="password")

    if api_key:
        st.success("API Key hợp lệ (nếu sai OpenAI sẽ báo khi chạy).")
    else:
        st.warning("Vui lòng dán OpenAI API Key!")


# =========================
#   GIAO DIỆN CHÍNH
# =========================
st.title("📸 Chấm Bài Toán Việt – H’Mông (OpenAI 4o-mini Vision)")

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
        up_file = st.file_uploader("Tải ảnh bài làm", type=["png", "jpg", "jpeg"])
        if up_file:
            image = Image.open(up_file)

    if image:
        st.image(image, caption="Ảnh đã tải", use_container_width=True)


with col_out:
    st.subheader("🔍 Kết quả AI")

    if st.button("🚀 Bắt đầu chấm bài", type="primary"):
        if not api_key:
            st.error("❌ Bạn chưa nhập API Key!")
        elif not image:
            st.warning("⚠️ Vui lòng tải ảnh trước.")
        else:
            with st.spinner("⏳ AI đang phân tích..."):
                prompt = """
                Phân tích ảnh bài làm toán:

                1. Chép lại đề bằng LaTeX (song ngữ Việt Nam 🇻🇳 và H’Mông 🟦).
                2. Chấm Đúng/Sai từng bước (song ngữ).
                3. Giải lại bài đúng và trình bày bằng LaTeX (song ngữ).
                4. Gợi ý cho học sinh vùng cao, dễ hiểu, ngắn gọn.

                Dùng ký hiệu ██ 🇻🇳 cho tiếng Việt và ██ 🟦 cho tiếng H'Mông.
                """

                result = analyze_with_openai(api_key, image, prompt)
                st.markdown(result)
