import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Chấm Bài AI Song Ngữ", page_icon="📸", layout="wide")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh (Việt – H’Mông)")
st.caption("Sử dụng Gemini API để phân tích hình ảnh, chấm bài, và giải chi tiết bằng hai ngôn ngữ (Việt - H'Mông) với công thức LaTeX chuẩn.")

# --- LẤY KEY ---
# Cố gắng lấy key từ st.secrets trước, nếu không có sẽ yêu cầu nhập
api_key = st.secrets.get("GOOGLE_API_KEY", "")

if not api_key:
    st.warning("⚠️ Chưa tìm thấy Google API Key trong `st.secrets`. Vui lòng nhập key của bạn bên dưới.")
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- HÀM PHÂN TÍCH ẢNH BẰNG GEMINI API ---
def analyze_real_image(api_key, image, prompt):
    """
    Gửi ảnh và prompt tới Gemini API để phân tích.
    """
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Mã hóa ảnh sang base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

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
        
        # Xử lý các mã lỗi HTTP
        if response.status_code != 200:
            return f"❌ Lỗi API {response.status_code}: {response.text}"
        
        data = response.json()
        
        # Kiểm tra nếu API trả về lỗi hoặc cấu trúc không hợp lệ
        if "candidates" not in data or not data["candidates"]:
             return f"❌ Lỗi: API không trả về nội dung (Có thể do lỗi lọc nội dung hoặc thiếu permissions). Chi tiết: {data}"
             
        return data["candidates"][0]["content"]["parts"][0]["text"]
        
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# -----------------------------
# 🚀 PROMPT TỐI ƯU (Đảm bảo LaTeX và Cấu trúc Song Ngữ)
# -----------------------------
# Sử dụng Prompt đã được tối ưu hóa ở bước trước
prompt_text = """
Bạn là **Giáo viên Toán cấp cao**, chuyên chấm bài và giải toán song ngữ **Việt (🇻🇳)** và **H’Mông (🟦)**.

**Mục tiêu:** Phân tích ảnh bài làm, chấm điểm, giải chi tiết, và trình bày kết quả bằng cấu trúc Markdown rõ ràng, dễ đọc, và đặc biệt là dễ copy vào Word/Overleaf.

### 1. 📋 Đề Bài Gốc (Problem Statement)
- Trích xuất đề bài từ ảnh.
- **Bắt buộc:** Viết toàn bộ đề bài bằng LaTeX, hiển thị song song hai ngôn ngữ.
$$
\\begin{array}{|l|l|}
\\hline
\\text{🇻🇳 Tiếng Việt} & \\text{🟦 Tiếng H'Mông} \\\\
\\hline
[Toàn bộ đề bài bằng tiếng Việt] & [Toàn bộ đề bài bằng tiếng H'Mông] \\\\
\\hline
\\end{array}
$$

### 2. ✅ Chấm Bài và Nhận Xét (Grading and Review)
- Chấm bài **từng bước** của học sinh.
- Sử dụng danh sách đánh số **(a, b, c...)** để tương ứng với các bước giải.
- **Bắt buộc:** Luôn hiển thị song song nhận xét:

(a)
| 🇻🇳 **Nhận xét (Việt)** | 🟦 **Nhận xét (H'Mông)** |
|:---|:---|
| **[Đúng/Sai]** Lý do: [Giải thích ngắn gọn] | **[Đúng/Sai H'Mông]** Tswv yim: [Giải thích ngắn gọn H'Mông] |

### 3. 💡 Lời Giải Chi Tiết (Detailed Solution)
- Viết lại lời giải hoàn chỉnh, chính xác.
- **QUY TẮC BẮT BUỘC VỀ LA $\TeX$:**
    - **TẤT CẢ** các công thức toán học phải được viết dưới dạng **LaTeX** (Inline: `\(...\)`, Block: `$$...$$`).
    - **TẤT CẢ** các bước giải phải được hiển thị song song, sử dụng cấu trúc:

#### Bước A: [Tóm tắt bước]

$$
\\begin{array}{|l|l|}
\\hline
\\text{🇻🇳 Công thức / Bước (Việt)} & \\text{🟦 Công thức / Bước (H'Mông)} \\\\
\\hline
\\text{🇻🇳 [Giải thích công thức bằng Tiếng Việt]} & \\text{🟦 [Giải thích công thức bằng Tiếng H'Mông]} \\\\
\\hline
[Công thức LaTeX Tiếng Việt] & [Công thức LaTeX Tiếng H'Mông] \\\\
\\hline
\\end{array}
$$

**Ví dụ Công thức trong Bước:**
**🇻🇳 Ta có:** \(A = \frac{x}{y+1}\).
**🟦 Peb muaj:** \(A = \frac{x}{y+1}\).

**Ví dụ Công thức Khối:**
$$
\\text{🇻🇳 Áp dụng công thức...} \\quad S = \pi r^2 \\quad \\text{🟦 Siv tus qauv...} \\quad S = \pi r^2
$$

### 4. 🔑 Kết Luận (Final Answer)
- Nêu rõ đáp số cuối cùng (hoặc chứng minh).
- **Bắt buộc:** Hiển thị đáp án cuối cùng bằng LaTeX và song ngữ.

---
**HÃY BẮT ĐẦU PHÂN TÍCH ẢNH BÀI LÀM TRÊN!**
"""

# --- GIAO DIỆN CHỤP ẢNH / TẢI LÊN ---
st.markdown("---")
col_upload, col_camera = st.columns(2)

with col_camera:
    st.subheader("📷 Chụp trực tiếp từ Camera")
    camera_photo = st.camera_input("Chụp ảnh bài làm tại đây")

with col_upload:
    st.subheader("📤 Hoặc tải ảnh bài làm (PNG, JPG)")
    uploaded_file = st.file_uploader("Chọn ảnh:", type=["png", "jpg", "jpeg"])

# --- CHỌN NGUỒN ẢNH ƯU TIÊN ---
image = None
if camera_photo is not None:
    image = Image.open(camera_photo)
elif uploaded_file is not None:
    image = Image.open(uploaded_file)

# --- XỬ LÝ ẢNH VÀ HIỂN THỊ KẾT QUẢ ---
st.markdown("---")
if image:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🖼️ Ảnh Bài Làm")
        st.image(image, caption="Ảnh bài làm đã được chọn", use_column_width=True)
        
        # Nút Phân Tích
        if st.button("🚀 Phân tích ngay", type="primary", use_container_width=True):
            if not api_key:
                st.error("🛑 Thiếu API Key! Vui lòng nhập key ở đầu trang.")
            else:
                with st.spinner("⏳ AI đang xử lý, tạo nhận xét và lời giải LaTeX song ngữ..."):
                    result = analyze_real_image(api_key, image, prompt_text)

                if "❌" in result:
                    st.error(result)
                else:
                    st.success("🎉 Đã phân tích xong!")
                    # Lưu kết quả vào state để hiển thị ở cột 2
                    st.session_state['analysis_result'] = result
                    st.experimental_rerun() # Tải lại để kết quả hiển thị ngay cột 2

    with col2:
        st.subheader("🔍 Kết quả Chấm Bài và Lời Giải Chi Tiết")
        if 'analysis_result' in st.session_state:
            # --- Hiển thị LaTeX chuẩn ---
            # Streamlit Markdown/HTML hỗ trợ rendering LaTeX thông qua mathjax,
            # cho phép hiển thị kết quả chuẩn từ mô hình.
            st.markdown(st.session_state['analysis_result'], unsafe_allow_html=True)
        else:
             st.info("Vui lòng tải lên ảnh bài làm và nhấn nút 'Phân tích ngay' để xem kết quả.")
             
else:
    st.info("Vui lòng chụp ảnh hoặc tải lên file bài làm (PNG/JPG) để bắt đầu.")
