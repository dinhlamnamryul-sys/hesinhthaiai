import streamlit as st
import requests
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import os

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

    loai_cau = st.selectbox(
        "Loại câu hỏi",
        [
            "Trắc nghiệm 4 lựa chọn",
            "Trắc nghiệm Đúng – Sai",
            "Câu trả lời ngắn",
            "Tự luận",
            "Trộn ngẫu nhiên"
        ]
    )

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

🎯 QUY ĐỊNH RÕ RÀNG:

1. Tất cả câu hỏi phải có dấu hỏi "?".
2. TRẮC NGHIỆM 4 LỰA CHỌN:
   A.
   B.
   C.
   D.
3. TRẮC NGHIỆM ĐÚNG – SAI:
   A. Đúng
   B. Sai
4. CÂU TRẢ LỜI NGẮN → đáp án 1 dòng.
5. TỰ LUẬN → trình bày bằng LaTeX khi có công thức.
6. GIỮ ĐÚNG MẪU SAU:

1. Câu hỏi ... ?

A. ...
B. ...
C. ...
D. ...

Đáp án: ...

7. Đặt đáp án sau câu hỏi cách nhau 2 dòng trống.
8. Không sinh tiếng H'Mông.
9. Toàn bộ công thức dùng LaTeX.
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


# --- TẠO FILE DOCX ---
def export_docx(text):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp.name)
    return temp.name

# --- TẠO FILE PDF ---
def export_pdf(text):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp.name, pagesize=letter)
    y = 750
    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 18
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    return temp.name


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

                # hiển thị lên trang web
                st.markdown(result.replace("\n", "<br>"), unsafe_allow_html=True)

                # --- TẠO FILE WORD ---
                docx_file = export_docx(result)
                with open(docx_file, "rb") as f:
                    st.download_button(
                        label="📥 Tải file DOCX",
                        data=f,
                        file_name=f"De_{lop}_{chuong}_{bai}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )

                # --- TẠO FILE PDF ---
                pdf_file = export_pdf(result)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="📥 Tải file PDF",
                        data=f,
                        file_name=f"De_{lop}_{chuong}_{bai}.pdf",
                        mime="application/pdf",
                    )

                # clean temp files when session ends
                # (streamlit tự xoá sau mỗi lần chạy)
