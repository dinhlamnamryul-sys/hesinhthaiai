import streamlit as st
from PIL import Image
from io import BytesIO
import time # Dùng để mô phỏng độ trễ của API

# =========================
#   CẤU HÌNH TRANG
# =========================
st.set_page_config(page_title="Chấm Bài AI Song Ngữ - DEMO", page_icon="📸", layout="wide")

# =========================
#   HÀM MÔ PHỎNG PHÂN TÍCH ẢNH
# =========================
def mock_analyze_image(image, prompt):
    """Mô phỏng hàm phân tích ảnh và trả về kết quả giả định."""
    time.sleep(3) # Mô phỏng độ trễ của API

    # Kết quả giả định (có thể thay đổi tùy ý)
    mock_result = f"""
## 🇻🇳 Kết quả Chấm Bài (DEMO) 🟦 Lus Kev Ntsuas Ntawv

---

### 1. 🇻🇳 Đề bài (Việt - H'Mông) 🟦 Cov Lus Hauv Ntawv
Đề bài trong ảnh được mô phỏng như sau:

$$\\mathbf{{VNF}}: \\text{{Giải phương trình: }} 2x + 5 = 11$$
$$\\mathbf{{HMG}}: \\text{{Xam teeb kev suav: }} 2x + 5 = 11$$

---

### 2. 🇻🇳 Chấm Đúng/Sai Từng Bước 🟦 Ntsuas Qhov Yog/Tsis Yog

* **Bước 1 (Step 1):**
    * 🇻🇳 Bài làm: $2x = 11 - 5$
    * 🟦 Lus Hauv Ntawv: $2x = 11 - 5$
    * **✅ 🇻🇳 Đúng 🟦 Yog** (Đã chuyển vế và đổi dấu chính xác. / Hloov chaw thiab pauv cim yog lawm.)

* **Bước 2 (Step 2):**
    * 🇻🇳 Bài làm: $2x = 6$
    * 🟦 Lus Hauv Ntawv: $2x = 6$
    * **✅ 🇻🇳 Đúng 🟦 Yog** (Phép trừ chính xác. / Muab rho tawm yog lawm.)

* **Bước 3 (Step 3):**
    * 🇻🇳 Bài làm: $x = 6 \\div 2$
    * 🟦 Lus Hauv Ntawv: $x = 6 \\div 2$
    * **✅ 🇻🇳 Đúng 🟦 Yog** (Đã chuyển vế và đổi phép toán chính xác. / Hloov chaw thiab pauv kev suav yog lawm.)
    
* **Bước 4 (Step 4):**
    * 🇻🇳 Bài làm: $x = 4$
    * 🟦 Lus Hauv Ntawv: $x = 4$
    * **❌ 🇻🇳 Sai 🟦 Tsis Yog** (Kết quả sai. Phải là $x=3$. / Qhov tshwm sim tsis yog. Yuav tsum yog $x=3$.)

---

### 3. 🇻🇳 Giải lại Bài Đúng 🟦 Txhim Kev Suav Kom Yog

Phép giải chính xác là:
$$\\mathbf{{VNF}}:$$
$$2x + 5 = 11$$
$$2x = 11 - 5$$
$$2x = 6$$
$$x = 6 \\div 2$$
$$x = 3$$
$$\\text{{Vậy }} x = 3$$

$$\\mathbf{{HMG}}:$$
$$2x + 5 = 11$$
$$2x = 11 - 5$$
$$2x = 6$$
$$x = 6 \\div 2$$
$$x = 3$$
$$\\text{{Li ntawd }} x = 3$$

"""
    return mock_result


# =========================
#   SIDEBAR (Đã đơn giản hóa)
# =========================
with st.sidebar:
    st.title("⚙️ Cài đặt (DEMO)")
    st.info("💡 **Gỡ bỏ yêu cầu API Key.** Chương trình này đang chạy ở chế độ mô phỏng, không cần kết nối API.")
    
    # Có thể thêm các tùy chọn giả lập
    model = st.selectbox("Chọn model (Giả lập):", ["models/gemini-1.5-flash-8b (Mô phỏng)"])
    st.success(f"Model đang chạy mô phỏng: {model}")


# =========================
#   GIAO DIỆN CHÍNH
# =========================
st.title("📸 Chấm Bài & Giải Toán Việt – H’Mông (DEMO)")

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
    st.subheader("🔍 Kết quả AI (Mô phỏng)")

    if st.button("🚀 Bắt đầu chấm bài (DEMO)", type="primary"):
        # Chỉ cần kiểm tra xem đã có ảnh chưa
        if not image:
            st.warning("⚠ Hãy tải ảnh bài làm!")
        else:
            with st.spinner("⏳ Đang phân tích ảnh (Mô phỏng độ trễ)..."):
                # Ghi đè prompt mặc dù không dùng
                prompt = """
                Phân tích ảnh bài làm toán:
                1. Chép lại đề bằng LaTeX (song ngữ Việt - H'Mông).
                2. Chấm Đúng/Sai từng bước (song ngữ).
                3. Giải lại bài đúng nhất bằng LaTeX (song ngữ).
                Dùng 🇻🇳 cho tiếng Việt và 🟦 cho tiếng H'Mông.
                """

                # Gọi hàm mô phỏng thay vì hàm API thật
                result = mock_analyze_image(image, prompt)
                st.markdown(result)
