import streamlit as st
import requests

st.set_page_config(page_title="Sinh Đề KNTC Tự Động", page_icon="📝", layout="wide")
st.title("📝 Sinh Đề Tự Động – Kết nối tri thức với cuộc sống")

# ============================
# 🔑 NHẬP GOOGLE API KEY
# ============================
with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để mở)"):
    st.markdown("""
1. Truy cập: **https://aistudio.google.com/app/apikey**
2. Nhấn **Create API Key**
3. Sao chép API Key.
4. Dán vào ô bên dưới.

⚠️ Không chia sẻ API Key.
""")

api_key = st.text_input("Nhập Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Bạn cần nhập API Key để sử dụng ứng dụng.")
else:
    st.success("✅ API Key hợp lệ!")

# ============================
# 📘 DANH SÁCH LỚP / BÀI
# ============================
lop_options = [f"Lớp {i}" for i in range(1, 10)]
chuong_options = {f"Lớp {i}": [f"Chương {j}" for j in range(1, 6)] for i in range(1, 10)}
bai_options = {f"Chương {i}": [f"Bài {j}" for j in range(1, 6)] for i in range(1, 6)}

with st.sidebar:
    st.header("📌 Thông tin sinh đề")
    lop = st.selectbox("Chọn lớp", lop_options)
    chuong = st.selectbox("Chọn chương", chuong_options[lop])
    bai = st.selectbox("Chọn bài", bai_options[chuong])
    so_cau = st.number_input("Số câu hỏi", min_value=1, max_value=50, value=10)
    loai_cau = st.selectbox("Loại câu hỏi", ["Trắc nghiệm", "Tự luận", "Trộn cả hai"])
    co_dap_an = st.checkbox("Có đáp án", value=True)

# ============================
# 🤖 HÀM GỌI GOOGLE AI
# ============================
def generate_questions(api_key, lop, chuong, bai, so_cau, loai_cau, co_dap_an):

    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

    prompt = f"""
Bạn là giáo viên Toán. Hãy sinh đề kiểm tra theo sách 
"Kết nối tri thức với cuộc sống":

- Lớp: {lop}
- Chương: {chuong}
- Bài: {bai}
- Số câu hỏi: {so_cau}
- Loại câu hỏi: {loai_cau}
- {'Có đáp án' if co_dap_an else 'Không có đáp án'}

🎯 YÊU CẦU QUAN TRỌNG:

1. Mỗi câu phải có dấu hỏi “?”.
2. TRẮC NGHIỆM:
   A. ...
   B. ...
   C. ...
   D. ...
3. TỰ LUẬN: dùng LaTeX nếu có công thức.
4. Giữa câu hỏi và đáp án cách đúng **2 dòng trống**.
5. Chỉ sinh nội dung tiếng Việt, không sinh tiếng H'Mông.
"""

    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return f"❌ Lỗi API {response.status_code}: {response.text}"

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# ============================
# ▶️ CHẠY SINH ĐỀ
# ============================
if st.button("🎯 Sinh đề ngay"):
    if not api_key:
        st.error("❌ Chưa nhập API Key!")
    else:
        with st.spinner("⏳ Đang tạo đề..."):
            result = generate_questions(api_key, lop, chuong, bai, so_cau, loai_cau, co_dap_an)

            if "❌" in result:
                st.error(result)
            else:
                st.success("🎉 Đề đã tạo xong!")

                # Định dạng kết quả đẹp hơn
                formatted = result
                formatted = formatted.replace("A.", "<br><br>A.")
                formatted = formatted.replace("B.", "<br>B.")
                formatted = formatted.replace("C.", "<br>C.")
                formatted = formatted.replace("D.", "<br>D.")
                formatted = formatted.replace("\n\n", "\n\n<br>\n\n")

                st.markdown(formatted, unsafe_allow_html=True)
