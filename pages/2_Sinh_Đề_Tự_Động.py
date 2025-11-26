import streamlit as st
import requests

st.set_page_config(page_title="Sinh Đề KNTC Tự Động", page_icon="📝", layout="wide")
st.title("📝 Sinh Đề Tự Động – Kết nối tri thức với cuộc sống")

# --- LẤY KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- DANH SÁCH LỚP / CHƯƠNG / BÀI ---
lop_options = [f"Lớp {i}" for i in range(1, 10)]
chuong_options = {f"Lớp {i}": [f"Chương {j}" for j in range(1, 6)] for i in range(1, 10)}
bai_options = {f"Chương {i}": [f"Bài {j}" for j in range(1, 6)] for i in range(1, 6)}

# --- GIAO DIỆN ---
with st.sidebar:
    st.header("Thông tin sinh đề")
    lop = st.selectbox("Chọn lớp", lop_options)
    chuong = st.selectbox("Chọn chương", chuong_options[lop])
    bai = st.selectbox("Chọn bài", bai_options[chuong])
    so_cau = st.number_input("Số câu hỏi", min_value=1, max_value=50, value=10)
    loai_cau = st.selectbox("Loại câu hỏi", ["Trắc nghiệm", "Tự luận", "Trộn cả hai"])
    co_dap_an = st.checkbox("Có đáp án", value=True)

# --- HÀM GỌI AI ---
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

🎯 YÊU CẦU RẤT QUAN TRỌNG:

1. Câu hỏi phải là câu hỏi HOÀN CHỈNH, có dấu hỏi "?".
2. Với TRẮC NGHIỆM:
   - Mỗi lựa chọn bắt buộc nằm trên **một dòng riêng**, theo đúng mẫu:
     A. ...
     B. ...
     C. ...
     D. ...
   - Tuyệt đối KHÔNG được viết nhiều đáp án trên cùng 1 dòng.

3. Với TỰ LUẬN:
   - Trình bày rõ ràng bằng LaTeX nếu có biểu thức.

4. Đáp án phải xuống dòng, đặt dưới câu hỏi **cách nhau đúng 2 dòng trống**.

MẪU CHUẨN (BẮT BUỘC):
1. Câu hỏi ... ?

A. ...
B. ...
C. ...
D. ...

Đáp án: ...

5. Không sinh tiếng H'Mông, chỉ sinh tiếng Việt.
6. Toàn bộ công thức phải dùng LaTeX.
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

# --- HIỂN THỊ ---
if st.button("🎯 Sinh đề ngay"):
    if not api_key:
        st.error("Thiếu API Key!")
    else:
        with st.spinner("⏳ AI đang tạo đề..."):
            result = generate_questions(api_key, lop, chuong, bai, so_cau, loai_cau, co_dap_an)

            if "❌" in result:
                st.error(result)
            else:
                st.success("🎉 Đã tạo xong đề!")

                # --- XỬ LÝ ĐỊNH DẠNG ---
                formatted = result

                formatted = formatted.replace("A.", "<br><br>A.")
                formatted = formatted.replace("B.", "<br>B.")
                formatted = formatted.replace("C.", "<br>C.")
                formatted = formatted.replace("D.", "<br>D.")

                formatted = formatted.replace("\n\n", "\n\n<br>\n\n")

                st.markdown(formatted, unsafe_allow_html=True)

                # --- TẠO FILE TẢI XUỐNG ---
                st.download_button(
                    label="📥 Tải đề xuống máy",
                    data=result,
                    file_name=f"De_{lop}_{chuong}_{bai}.txt",
                    mime="text/plain",
                )
