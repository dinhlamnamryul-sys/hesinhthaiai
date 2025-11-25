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

# --- GIAO DIỆN CHỌN ---
with st.sidebar:
    st.header("Thông tin sinh đề")
    lop = st.selectbox("Chọn lớp", lop_options)
    chuong = st.selectbox("Chọn chương", chuong_options[lop])
    bai = st.selectbox("Chọn bài", bai_options[chuong])
    so_cau = st.number_input("Số câu hỏi", min_value=1, max_value=50, value=10)
    loai_cau = st.selectbox("Loại câu hỏi", ["Trắc nghiệm", "Tự luận", "Trộn cả hai"])
    co_dap_an = st.checkbox("Có đáp án", value=True)

# --- GỌI AI ---
def generate_questions(api_key, lop, chuong, bai, so_cau, loai_cau, co_dap_an):
    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

    prompt = f"""
Bạn là giáo viên Toán giỏi. Hãy sinh đề kiểm tra theo sách 
"Kết nối tri thức với cuộc sống":

- Lớp: {lop}
- Chương: {chuong}
- Bài: {bai}
- Số câu hỏi: {so_cau}
- Loại câu hỏi: {loai_cau}
- {'Có đáp án' if co_dap_an else 'Không có đáp án'}

🎯 **YÊU CẦU QUAN TRỌNG**

1. **Câu hỏi phải là dạng câu hỏi**, có dấu hỏi "?" và viết đúng cấu trúc.
2. **Đáp án phải xuống dòng**, đặt độc lập, KHÔNG cùng dòng với câu hỏi.
3. Giữa câu hỏi và đáp án **phải có đúng 2 dòng trống**.
4. Nếu là trắc nghiệm → dạng:
   - A. …
   - B. …
   - C. …
   - D. …
5. Nếu là tự luận → trình bày rõ ràng, LaTeX chuẩn.
6. KHÔNG sinh song ngữ, chỉ tiếng Việt.
7. Giữ định dạng:
   **1. Câu hỏi ... ?**

   (2 dòng trống)

   **Đáp án:** …
8. Tất cả công thức dùng LaTeX.
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
                
                # Giữ format xuống dòng đúng
                st.markdown(result.replace("\n\n", "\n\n<br>\n\n"), unsafe_allow_html=True)
