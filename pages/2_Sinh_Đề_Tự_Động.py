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
st.title("📝 Sinh Đề Tự Động – In-memory export (DOCX / PDF)")

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

# --- Prompt builder (nhắc AI xuất công thức LaTeX đặt trong $$...$$) ---
def build_prompt(lop, chuong, bai, so_cau, loai_cau, co_dap_an):
    return f"""
Bạn là giáo viên Toán. Hãy sinh đề kiểm tra theo sách "Kết nối tri thức với cuộc sống":
- Lớp: {lop}
- Chương: {chuong}
- Bài: {bai}
- Số câu hỏi: {so_cau}
- Loại câu hỏi: {loai_cau}
- {'Có đáp án' if co_dap_an else 'Không có đáp án'}

YÊU CẦU:
1) Tất cả công thức toán PHẢI ở dạng LaTeX và đặt trong $$...$$. Ví dụ: $$\\frac{a}{b}$$
2) Trắc nghiệm 4 lựa chọn phải có A./B./C./D. trên mỗi dòng.
3) Câu trả lời ngắn 1 dòng.
4) Đáp án đặt sau câu hỏi, cách 2 dòng trống.
5) Chỉ dùng tiếng Việt.
"""
# --- Gọi API ---
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

# --- Tìm latex blocks $$...$$ ---
LATEX_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)

def find_latex_blocks(text):
    blocks = []
    for m in LATEX_RE.finditer(text):
        blocks.append((m.span(), m.group(0), m.group(1)))
    return blocks

# --- Render LaTeX -> PNG bytes (matplotlib) ---
def render_latex_png_bytes(latex_code, fontsize=20, dpi=200):
    # latex_code: string WITHOUT $$ delimiters
    fig = plt.figure()
    fig.patch.set_alpha(0.0)
    # place text in figure
    fig.text(0, 0, f"${latex_code}$", fontsize=fontsize)
    buf = io.BytesIO()
    plt.axis('off')
    plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', pad_inches=0.02, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf.read()

# --- Create DOCX in-memory (BytesIO) with images in place of formulas ---
def create_docx_bytes(text):
    doc = Document()
    last = 0
    for span, full, inner in find_latex_blocks(text):
        start, end = span
        # add text before formula
        before = text[last:start]
        for line in before.splitlines():
            doc.add_paragraph(line)
        # render image
        try:
            png_bytes = render_latex_png_bytes(inner)
            img_stream = io.BytesIO(png_bytes)
            p = doc.add_paragraph()
            r = p.add_run()
            r.add_picture(img_stream, width=Inches(3))
        except Exception as e:
            doc.add_paragraph(full)  # fallback: raw latex
        last = end
    # remaining text
    rest = text[last:]
    for line in rest.splitlines():
        doc.add_paragraph(line)
    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    return out

# --- Create PDF in-memory (BytesIO) with images inserted ---
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
            # basic wrap: if line too long, write as-is and move down
            c.drawString(margin, y, line)
            y -= 14
            if y < 60:
                c.showPage()
                y = height - 50
        # render image and draw
        try:
            png_bytes = render_latex_png_bytes(inner, fontsize=20, dpi=200)
            img = Image.open(io.BytesIO(png_bytes))
            img_reader = ImageReader(io.BytesIO(png_bytes))
            # choose width in points
            draw_w = 300  # points
            draw_h = img.height / img.width * draw_w
            if y - draw_h < 60:
                c.showPage()
                y = height - 50
            c.drawImage(img_reader, margin, y - draw_h, width=draw_w, height=draw_h, mask='auto')
            y -= draw_h + 8
        except Exception as e:
            c.drawString(margin, y, full)
            y -= 14
            if y < 60:
                c.showPage()
                y = height - 50
        last = end
    # remaining text
    rest = text[last:]
    for line in rest.splitlines():
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
            st.success("🎉 Đã tạo xong đề (hiện raw trong trang).")
            st.markdown(result.replace("\n", "<br>"), unsafe_allow_html=True)

            # tìm latex
            latex_blocks = find_latex_blocks(result)
            if not latex_blocks:
                st.warning("Không tìm thấy biểu thức LaTeX ( $$...$$ ). Nếu AI trả MathML, hãy yêu cầu AI xuất LaTeX giữa $$...$$ để render chính xác.")
                # fallback: export raw text DOCX/PDF
                txt_bytes = result.encode("utf-8")
                st.download_button("📥 Tải TXT (fallback)", data=txt_bytes, file_name=f"De_{lop}_{chuong}_{bai}.txt", mime="text/plain")
            else:
                # tạo docx bytes
                try:
                    docx_io = create_docx_bytes(result)
                    st.download_button(
                        label="📥 Tải DOCX (công thức là ảnh)",
                        data=docx_io.getvalue(),
                        file_name=f"De_{lop}_{chuong}_{bai}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except Exception as e:
                    st.error(f"Không tạo DOCX: {e}")
                    # fallback txt
                    st.download_button("📥 Tải TXT (fallback)", data=result.encode("utf-8"), file_name=f"De_{lop}_{chuong}_{bai}.txt", mime="text/plain")

                # tạo pdf bytes
                try:
                    pdf_io = create_pdf_bytes(result)
                    st.download_button(
                        label="📥 Tải PDF (công thức là ảnh)",
                        data=pdf_io.getvalue(),
                        file_name=f"De_{lop}_{chuong}_{bai}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Không tạo PDF: {e}")
                    st.download_button("📥 Tải TXT (fallback)", data=result.encode("utf-8"), file_name=f"De_{lop}_{chuong}_{bai}.txt", mime="text/plain")
