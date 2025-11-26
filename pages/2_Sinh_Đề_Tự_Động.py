import re
import io
import requests
import streamlit as st
from docx import Document
from docx.shared import Inches
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sinh Đề KNTC Tự Động", page_icon="📝", layout="wide")
st.title("📝 Sinh Đề Tự Động – LaTeX → ảnh → DOCX/PDF")

# --- API KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- GUI ---
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

# --- BUILD PROMPT ---
def build_prompt(lop, chuong, bai, so_cau, loai_cau, co_dap_an):
    prompt = """
Bạn là giáo viên Toán. Hãy sinh đề kiểm tra theo sách "Kết nối tri thức với cuộc sống":
- Lớp: {lop}
- Chương: {chuong}
- Bài: {bai}
- Số câu hỏi: {so_cau}
- Loại câu hỏi: {loai_cau}
- {dap_an}

YÊU CẦU QUAN TRỌNG:
1) Toàn bộ công thức toán phải được viết bằng LaTeX và **phải** đặt trong delimiters $$...$$.
   Ví dụ: $$\\frac{{a}}{{b}}$$
2) Câu trắc nghiệm phải theo định dạng:
A. ...
B. ...
C. ...
D. ...
3) Câu trả lời ngắn chỉ 1 dòng.
4) Đáp án đặt dưới câu hỏi, cách 2 dòng trống.
5) Chỉ dùng tiếng Việt.
"""
    return prompt.format(
        lop=lop,
        chuong=chuong,
        bai=bai,
        so_cau=so_cau,
        loai_cau=loai_cau,
        dap_an="Có đáp án" if co_dap_an else "Không có đáp án"
    )

# --- GỌI API ---
def generate_questions(api_key, lop, chuong, bai, so_cau, loai_cau, co_dap_an):
    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"
    prompt = build_prompt(lop, chuong, bai, so_cau, loai_cau, co_dap_an)
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    try:
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code != 200:
            return f"❌ Lỗi API {r.status_code}: {r.text}"
        j = r.json()
        return j["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {e}"

# --- TÌM CÁC BLOCK LaTeX $$...$$ ---
LATEX_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
def find_latex_blocks(text):
    blocks = []
    for m in LATEX_RE.finditer(text):
        blocks.append((m.span(), m.group(0), m.group(1)))
    return blocks

# --- RENDER LaTeX → PNG ---
def render_latex_png_bytes(latex_code, fontsize=20, dpi=200):
    fig = plt.figure()
    fig.patch.set_alpha(0.0)
    fig.text(0, 0, f"${latex_code}$", fontsize=fontsize)
    buf = io.BytesIO()
    plt.axis('off')
    plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', pad_inches=0.02, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf.read()

# --- TẠO DOCX IN-MEMORY ---
def create_docx_bytes(text):
    doc = Document()
    last = 0
    for span, full, inner in find_latex_blocks(text):
        start, end = span
        before = text[last:start]
        for line in before.splitlines():
            doc.add_paragraph(line)
        try:
            png_bytes = render_latex_png_bytes(inner)
            img_stream = io.BytesIO(png_bytes)
            p = doc.add_paragraph()
            r = p.add_run()
            r.add_picture(img_stream, width=Inches(3))
        except:
            doc.add_paragraph(full)
        last = end
    for line in text[last:].splitlines():
        doc.add_paragraph(line)
    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    return out

# --- TẠO PDF IN-MEMORY ---
def create_pdf_bytes(text):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    margin = 40
    y = height - 50
    last = 0
    for span, full, inner in find_latex_blocks(text):
        start, end = span
        before = text[last:start]
        for line in before.splitlines():
            c.drawString(margin, y, line)
            y -= 14
            if y < 60:
                c.showPage()
                y = height - 50
        try:
            png_bytes = render_latex_png_bytes(inner)
            img_reader = ImageReader(io.BytesIO(png_bytes))
            img = Image.open(io.BytesIO(png_bytes))
            draw_w = 300
            draw_h = img.height / img.width * draw_w
            if y - draw_h < 60:
                c.showPage()
                y = height - 50
            c.drawImage(img_reader, margin, y - draw_h, width=draw_w, height=draw_h, mask='auto')
            y -= draw_h + 8
        except:
            c.drawString(margin, y, full)
            y -= 14
            if y < 60:
                c.showPage()
                y = height - 50
        last = end
    for line in text[last:].splitlines():
        c.drawString(margin, y, line)
        y -= 14
        if y < 60:
            c.showPage()
            y = height - 50
    c.save()
    buf.seek(0)
    return buf

# --- BUTTON ---
if st.button("🎯 Sinh đề ngay"):
    if not api_key:
        st.error("Thiếu API Key!")
    else:
        with st.spinner("⏳ AI đang tạo đề..."):
            result = generate_questions(api_key, lop, chuong, bai, so_cau, loai_cau, co_dap_an)

        if isinstance(result, str) and result.startswith("❌"):
            st.error(result)
        else:
            st.success("🎉 Đã tạo xong đề (hiển thị nội dung).")
            st.markdown(result.replace("\n", "<br>"), unsafe_allow_html=True)

            latex_blocks = find_latex_blocks(result)
            if not latex_blocks:
                st.warning("Không tìm thấy LaTeX ( $$...$$ ). Xuất raw TXT làm fallback.")
                st.download_button("📥 Tải TXT", data=result.encode("utf-8"), file_name=f"De_{lop}_{chuong}_{bai}.txt", mime="text/plain")
            else:
                # DOCX
                try:
                    docx_io = create_docx_bytes(result)
                    st.download_button(
                        "📥 Tải DOCX (công thức là ảnh)",
                        data=docx_io.getvalue(),
                        file_name=f"De_{lop}_{chuong}_{bai}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except Exception as e:
                    st.error(f"Không tạo DOCX: {e}")

                # PDF
                try:
                    pdf_io = create_pdf_bytes(result)
                    st.download_button(
                        "📥 Tải PDF (công thức là ảnh)",
                        data=pdf_io.getvalue(),
                        file_name=f"De_{lop}_{chuong}_{bai}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Không tạo PDF: {e}")
