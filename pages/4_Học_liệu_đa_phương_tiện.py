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

st.set_page_config(page_title="Tổng hợp kiến thức Toán theo chủ đề", layout="wide")
st.title("📚 Tổng hợp kiến thức Toán từ lớp 1 đến lớp 9 theo chủ đề (Gemini API)")

# =============================
# API Key
# =============================
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.text_input("Nhập Google API Key:", type="password")

# =============================
# Chọn lớp
# =============================
lop_options = [f"Lớp {i}" for i in range(1, 10)] + ["Tất cả lớp"]
lop = st.selectbox("Chọn lớp để tổng hợp kiến thức", lop_options)

# =============================
# Build prompt tổng hợp theo chủ đề
# =============================
def build_prompt_summary_theo_chu_de(lop):
    if lop == "Tất cả lớp":
        lop_text = "từ lớp 1 đến lớp 9"
    else:
        lop_text = lop
    prompt = f"""
Bạn là giáo viên Toán. Hãy tổng hợp toàn bộ kiến thức môn Toán {lop_text} theo CHỦ ĐỀ CHÍNH.
- Phân nhóm theo các chủ đề: Số học, Đại số, Hình học, Thống kê & Xác suất (nếu có).
- Mỗi chủ đề chia thành: Khái niệm – Công thức – Ví dụ – Ứng dụng.
- Viết công thức toán bằng LaTeX trong $$...$$.
- Chỉ dùng tiếng Việt, trình bày rõ ràng để in ra DOCX/PDF.
- Nếu có ví dụ minh họa, liệt kê dạng bullet hoặc số thứ tự.
"""
    return prompt

# =============================
# Gọi Gemini API
# =============================
def generate_summary(api_key, lop, prompt_builder=build_prompt_summary_theo_chu_de):
    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"
    prompt = prompt_builder(lop)
    payload = {"contents":[{"role":"user","parts":[{"text":prompt}]}]}
    try:
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        j = r.json()
        return j["candidates"][0]["content"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối hoặc API: {e}"

# =============================
# Xử lý LaTeX → ảnh → DOCX/PDF
# =============================
LATEX_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
def find_latex_blocks(text):
    return [(m.span(), m.group(0), m.group(1)) for m in LATEX_RE.finditer(text)]

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

# =============================
# Nút tổng hợp kiến thức
# =============================
if st.button("📄 Tổng hợp kiến thức theo chủ đề"):
    if not api_key:
        st.error("Thiếu API Key!")
    else:
        with st.spinner("⏳ AI đang tổng hợp kiến thức..."):
            summary = generate_summary(api_key, lop)
        if isinstance(summary, str) and summary.startswith("❌"):
            st.error(summary)
        else:
            st.success("🎉 Hoàn tất tổng hợp kiến thức!")
            st.markdown(summary.replace("\n","<br>"), unsafe_allow_html=True)

            # Xuất DOCX
            docx_io = create_docx_bytes(summary)
            st.download_button("📥 Tải DOCX", data=docx_io.getvalue(),
                               file_name=f"Tong_hop_KT_{lop}.docx",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

            # Xuất PDF
            pdf_io = create_pdf_bytes(summary)
            st.download_button("📥 Tải PDF", data=pdf_io.getvalue(),
                               file_name=f"Tong_hop_KT_{lop}.pdf",
                               mime="application/pdf")
