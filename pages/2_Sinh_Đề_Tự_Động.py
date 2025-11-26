import re
import io
import tempfile
import os
import requests
import streamlit as st
from docx import Document
from docx.shared import Inches
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sinh Đề KNTC Tự Động", page_icon="📝", layout="wide")
st.title("📝 Sinh Đề Tự Động – Render công thức bằng ảnh (LaTeX → PNG)")

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


# --- Prompt: YÊU CẦU AI TRẢ CÔNG THỨC DẠNG LaTeX giữa $$...$$ ---
def build_prompt(lop, chuong, bai, so_cau, loai_cau, co_dap_an):
    return f"""
Bạn là giáo viên Toán. Hãy sinh đề kiểm tra theo sách "Kết nối tri thức với cuộc sống":
- Lớp: {lop}
- Chương: {chuong}
- Bài: {bai}
- Số câu hỏi: {so_cau}
- Loại câu hỏi: {loai_cau}
- {'Có đáp án' if co_dap_an else 'Không có đáp án'}

YÊU CẦU QUAN TRỌNG:
1) Toàn bộ công thức toán phải được viết bằng LaTeX và **phải** đặt trong delimiters $$...$$ (ví dụ: $$\\frac{a}{b}$$).
2) Câu trắc nghiệm phải theo định dạng:
A. ...
B. ...
C. ...
D. ...
3) Câu trả lời ngắn là một dòng.
4) Đáp án phải nằm dưới câu hỏi, cách nhau đúng 2 dòng trống.
5) Không dùng MathML. Không sử dụng ngôn ngữ khác ngoài tiếng Việt.
6) Ví dụ mẫu bắt buộc:
1. Viết câu hỏi ... ?

A. ...
B. ...
C. ...
D. ...

Đáp án: ...
"""
# --- GỌI API (Google Generative Language) ---
def generate_questions(api_key, lop, chuong, bai, so_cau, loai_cau, co_dap_an):
    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"
    prompt = build_prompt(lop, chuong, bai, so_cau, loai_cau, co_dap_an)
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    try:
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code != 200:
            return f"❌ Lỗi API {resp.status_code}: {resp.text}"
        j = resp.json()
        return j["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {e}"

# --- TÌM CÁC BIỂU THỨC LaTeX TRONG VĂN BẢN ---
LATEX_PATTERNS = [
    re.compile(r"\$\$(.+?)\$\$", re.DOTALL),   # $$...$$
    re.compile(r"\\\((.+?)\\\)", re.DOTALL),   # \(...\)
    re.compile(r"\\\[(.+?)\\\]", re.DOTALL),   # \[...\]
]

def find_all_latex_blocks(text):
    blocks = []
    for pat in LATEX_PATTERNS:
        for m in pat.finditer(text):
            blocks.append((m.span(), m.group(0), m.group(1)))
    # sort by start index
    blocks.sort(key=lambda x: x[0][0])
    return blocks

# --- RENDER LaTeX -> PNG ---
def render_latex_to_png(latex_code, dpi=200):
    """
    latex_code: string (without $$ delimiters ideally)
    returns: bytes PNG
    """
    # Use matplotlib mathtext rendering
    fig = plt.figure(figsize=(0.01,0.01))
    text = f"${latex_code}$"
    # create invisible axes
    fig.text(0, 0, text, fontsize=14)
    buf = io.BytesIO()
    # tight bbox
    plt.axis('off')
    plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', pad_inches=0.05, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf.read()

# --- CHÈN ẢNH VÀO DOCX ---
def create_docx_with_images(text, latex_blocks):
    doc = Document()
    last_index = 0
    for span, raw_delim, inner in latex_blocks:
        start, end = span
        # text before formula
        before = text[last_index:start]
        for line in before.splitlines():
            doc.add_paragraph(line)
        # render formula
        try:
            png_bytes = render_latex_to_png(inner)
            img_stream = io.BytesIO(png_bytes)
            # add a small paragraph and image
            p = doc.add_paragraph()
            r = p.add_run()
            r.add_picture(img_stream, width=Inches(2))  # adjust size
        except Exception as e:
            # if render fail, insert raw latex fallback
            doc.add_paragraph(raw_delim)
        last_index = end
    # remaining text
    rest = text[last_index:]
    for line in rest.splitlines():
        doc.add_paragraph(line)
    # save to temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp.name)
    return tmp.name

# --- TẠO PDF (vẽ text và chèn ảnh) ---
def create_pdf_with_images(text, latex_blocks):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=letter)
    width, height = letter
    y = height - 50
    last_index = 0
    for span, raw_delim, inner in latex_blocks:
        start, end = span
        before = text[last_index:start]
        for line in before.splitlines():
            # simple wrapping: if line too long, split
            c.drawString(40, y, line)
            y -= 14
            if y < 60:
                c.showPage()
                y = height - 50
        # render image
        try:
            png_bytes = render_latex_to_png(inner, dpi=200)
            img = Image.open(io.BytesIO(png_bytes))
            # save to temp png to use reportlab
            img_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            img.save(img_tmp.name, format="PNG")
            # calculate size to draw
            draw_w = 200  # px
            draw_h = (img.height / img.width) * draw_w
            if y - draw_h < 60:
                c.showPage()
                y = height - 50
            c.drawImage(img_tmp.name, 40, y - draw_h, width=draw_w, height=draw_h, mask='auto')
            y -= draw_h + 6
            os.unlink(img_tmp.name)
        except Exception as e:
            c.drawString(40, y, raw_delim)
            y -= 14
        last_index = end
    # remaining text
    rest = text[last_index:]
    for line in rest.splitlines():
        c.drawString(40, y, line)
        y -= 14
        if y < 60:
            c.showPage()
            y = height - 50
    c.save()
    return tmp.name

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
            st.success("🎉 Đã tạo xong đề (tạm hiển thị raw).")
            # show raw (with HTML line breaks)
            st.markdown(result.replace("\n", "<br>"), unsafe_allow_html=True)

            # Find LaTeX blocks (priority)
            latex_blocks = find_all_latex_blocks(result)

            # If no LaTeX found, try to detect MathML <math>...</math> and optionally extract textual fallback
            if not latex_blocks:
                mathml_matches = list(re.finditer(r"(<math[\s\S]*?>[\s\S]*?<\/math>)", result, re.IGNORECASE))
                if mathml_matches:
                    st.warning("Không tìm thấy LaTeX ( $$...$$ ). Văn bản chứa MathML. Vì chuyển MathML→ảnh không được hỗ trợ tự động, hãy thay đổi AI để xuất LaTeX (đặt trong $$...$$).")
                    # We'll fallback to exporting raw docx/pdf (no rendered formulas)
                    # create simple docx/pdf without images
                    doc_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                    Document().save(doc_tmp.name)  # empty doc
                    # quick simple export of raw text
                    doc = Document()
                    for line in result.splitlines():
                        doc.add_paragraph(line)
                    doc.save(doc_tmp.name)
                    with open(doc_tmp.name, "rb") as f:
                        st.download_button("📥 Tải DOCX (raw, có MathML)", f, file_name=f"De_{lop}_{chuong}_{bai}_raw.docx")
                    pdf_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    # generate raw pdf
                    c = canvas.Canvas(pdf_tmp.name, pagesize=letter)
                    y = 750
                    for line in result.splitlines():
                        c.drawString(40, y, line)
                        y -= 14
                        if y < 60:
                            c.showPage()
                            y = 750
                    c.save()
                    with open(pdf_tmp.name, "rb") as f:
                        st.download_button("📥 Tải PDF (raw, có MathML)", f, file_name=f"De_{lop}_{chuong}_{bai}_raw.pdf")
                    st.stop()

            # If we have latex blocks, create files with rendered images
            if latex_blocks:
                try:
                    docx_path = create_docx_with_images(result, latex_blocks)
                    with open(docx_path, "rb") as f:
                        st.download_button("📥 Tải DOCX (công thức dưới dạng ảnh)", f, file_name=f"De_{lop}_{chuong}_{bai}.docx")
                except Exception as e:
                    st.error(f"Không tạo được DOCX có ảnh: {e}")

                try:
                    pdf_path = create_pdf_with_images(result, latex_blocks)
                    with open(pdf_path, "rb") as f:
                        st.download_button("📥 Tải PDF (công thức dưới dạng ảnh)", f, file_name=f"De_{lop}_{chuong}_{bai}.pdf")
                except Exception as e:
                    st.error(f"Không tạo được PDF có ảnh: {e}")

            st.info("Ghi chú: phương pháp này yêu cầu AI trả công thức ở dạng LaTeX giữa $$...$$ để tự động render và chèn ảnh. Nếu AI vẫn trả MathML, hãy thay đổi prompt để yêu cầu LaTeX.")
