import streamlit as st
import requests
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile


st.set_page_config(page_title="Sinh Đề KNTC Tự Động", page_icon="📝", layout="wide")
st.title("📝 Sinh Đề Tự Động – Kết nối tri thức với cuộc sống (MathML Version)")


# --- LẤY KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.text_input("Nhập Google API Key:", type="password")


# --- DANH SÁCH LỚP / CHƯƠNG / BÀI ---
lop_options = [f"Lớp {i}" for i in range(1, 10)]
chuong_options = {f"Lớp {i}": [f"Chương {j}" for j in range(1, 6)] for i in range(1, 10)}
bai_options = {f"Chương {i}": [f"Bài {j}" for j in range(1, 6)] for i in range(1, 6)}


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

🎯 QUY ĐỊNH QUAN TRỌNG:

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
5. TỰ LUẬN → giải thích chi tiết.
6. Công thức toán HỌC PHẢI dùng **MathML tiêu chuẩn**, KHÔNG dùng LaTeX.
Ví dụ MathML:
<math><mrow><msup><mi>a</mi><mn>2</mn></msup><mo>+</mo><msup><mi>b</mi><mn>2</mn></msup></mrow></math>

7. MẪU BẮT BUỘC:

1. Câu hỏi ... ?

A. ...
B. ...
C. ...
D. ...

Đáp án: ...

8. Đặt đáp án cách câu hỏi 2 dòng trống.
9. Không sinh tiếng H'Mông.
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


# --- XUẤT DOCX ---
def export_docx(text):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp.name)
    return tmp.name


# --- XUẤT PDF ---
def export_pdf(text):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=letter)
    y = 750
    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 16
        if y < 40:
            c.showPage()
            y = 750
    c.save()
    return tmp.name


# --- NÚT SINH ĐỀ ---
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

                # Hiển thị đề trên giao diện
                st.markdown(result.replace("\n", "<br>"), unsafe_allow_html=True)

                # Xuất DOCX
                docx_file = export_docx(result)
                with open(docx_file, "rb") as f:
                    st.download_button(
                        label="📥 Tải file DOCX",
                        data=f,
                        file_name=f"De_{lop}_{chuong}_{bai}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

                # Xuất PDF
                pdf_file = export_pdf(result)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="📥 Tải file PDF",
                        data=f,
                        file_name=f"De_{lop}_{chuong}_{bai}.pdf",
                        mime="application/pdf"
                    )
