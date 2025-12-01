# app.py — Ứng dụng Streamlit: Tổng hợp kiến thức Toán + xuất DOCX/PDF
import re
import io
import json
import requests
import streamlit as st
from docx import Document
from docx.shared import Inches
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
import matplotlib.pyplot as plt

# -----------------------
# Cấu hình page
# -----------------------
st.set_page_config(page_title="Tổng hợp kiến thức Toán - Đa phương tiện", layout="wide", page_icon="🎓")
st.title("🎓 Tổng hợp kiến thức Toán (Gemini API) — Ổn định, không lỗi")

st.markdown("""
<style>
.block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# -----------------------
# API Key
# -----------------------
# Lấy từ secrets nếu có, nếu không yêu cầu nhập
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Nhập Google API Key:", type="password")

MODEL_DEFAULT = st.sidebar.selectbox("Chọn model (nếu không sure, giữ mặc định):",
                                     ["models/gemini-2.0-flash", "models/gemini-2.0", "models/text-bison-001"])

# -----------------------
# Hỗ trợ LaTeX → ảnh
# -----------------------
LATEX_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)

def find_latex_blocks(text):
    return [(m.span(), m.group(0), m.group(1)) for m in LATEX_RE.finditer(text)]

def render_latex_png_bytes(latex_code, fontsize=20, dpi=200):
    # Tạo ảnh PNG từ LaTeX (matplotlib)
    fig = plt.figure()
    fig.patch.set_alpha(0.0)
    fig.text(0, 0, f"${latex_code}$", fontsize=fontsize)
    buf = io.BytesIO()
    plt.axis('off')
    plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', pad_inches=0.02, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf.read()

# -----------------------
# Xuất DOCX / PDF
# -----------------------
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
        except Exception as e:
            # nếu render lỗi thì chèn nguyên block latex
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
        except Exception as e:
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

# -----------------------
# HÀM GIÚP: TÌM TEXT TRONG JSON (để phòng model trả khác cấu trúc)
# -----------------------
def extract_text_from_api_response(data):
    """
    Cố gắng lấy string text hữu dụng từ response JSON của Gemini.
    Trả về None nếu không tìm thấy.
    """
    # 1) Nếu có 'candidates' list
    if isinstance(data, dict) and "candidates" in data:
        cands = data.get("candidates") or []
        for cand in cands:
            # thường có cand["content"] hoặc cand["text"]
            # dò sâu trong cand để tìm key 'text' chứa string
            text = deep_find_first_string(cand, keys=["text", "output", "content"])
            if text:
                return text

    # 2) Nếu có 'output' trực tiếp
    text = deep_find_first_string(data, keys=["text", "output", "content"])
    if text:
        return text

    return None

def deep_find_first_string(obj, keys=None):
    """
    Duyệt đệ quy object JSON để tìm giá trị chuỗi đầu tiên của các keys thường dùng.
    Trả về string hoặc None.
    """
    if keys is None:
        keys = ["text", "output", "content"]

    if isinstance(obj, dict):
        # ưu tiên keys được liệt kê
        for k in keys:
            if k in obj and isinstance(obj[k], str):
                return obj[k]
        # nếu là list hoặc dict lồng, duyệt tiếp
        for v in obj.values():
            res = deep_find_first_string(v, keys)
            if res:
                return res
        return None
    elif isinstance(obj, list):
        for item in obj:
            res = deep_find_first_string(item, keys)
            if res:
                return res
        return None
    else:
        return None

# -----------------------
# GỌI API: đã chỉnh để an toàn
# -----------------------
def generate_with_gemini(api_key, prompt, model=MODEL_DEFAULT, timeout=60):
    if not api_key:
        return {"ok": False, "message": "Thiếu API Key."}

    model = model or MODEL_DEFAULT
    url = f"https://generativelanguage.googleapis.com/v1/{model}:generateContent?key={api_key}"
    payload = {"contents":[{"role":"user","parts":[{"text":prompt}]}]}

    # Headers (nếu cần)
    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
    except Exception as e:
        return {"ok": False, "message": f"Lỗi kết nối tới API: {e}"}

    # Cố gắng parse JSON (nếu không parse được, show status + text)
    try:
        data = resp.json()
    except Exception:
        return {"ok": False, "message": f"API trả về non-JSON. HTTP {resp.status_code}: {resp.text}"}

    # Nếu lỗi từ API (Google thường trả 'error')
    if isinstance(data, dict) and data.get("error"):
        err_msg = data["error"].get("message", str(data["error"]))
        return {"ok": False, "message": f"API trả lỗi: {err_msg}", "raw": data}

    # Thử lấy text theo nhiều cách
    text = extract_text_from_api_response(data)
    if text:
        return {"ok": True, "text": text}

    # Nếu không tìm được, trả về raw data để debug
    return {"ok": False, "message": "Không tìm được trường text trong response API.", "raw": data}

# -----------------------
# Build prompt
# -----------------------
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

# -----------------------
# UI: chọn lớp + nút tổng hợp
# -----------------------
st.header("📘 Tổng hợp kiến thức Toán theo chủ đề")

lop_options = [f"Lớp {i}" for i in range(1, 10)] + ["Tất cả lớp"]
lop = st.selectbox("Chọn lớp để tổng hợp kiến thức", lop_options)

if st.button("📄 Tổng hợp kiến thức theo chủ đề"):
    if not api_key:
        st.error("Thiếu API Key! Vui lòng điền API Key ở sidebar.")
    else:
        prompt = build_prompt_summary_theo_chu_de(lop)
        with st.spinner("AI đang tổng hợp..."):
            res = generate_with_gemini(api_key, prompt, model=MODEL_DEFAULT)
        if not res.get("ok"):
            st.error(res.get("message", "Lỗi không rõ"))
            # nếu có raw JSON thì hiển thị để debug (chỉ hiển thị trong development)
            if "raw" in res:
                st.subheader("🔍 JSON trả về (debug):")
                st.json(res["raw"])
        else:
            summary = res["text"]
            st.success("🎉 Hoàn tất tổng hợp kiến thức!")
            # Hiển thị an toàn (HTML cho xuống dòng)
            st.markdown(summary.replace("\n", "<br>"), unsafe_allow_html=True)

            # Xuất DOCX
            try:
                docx_io = create_docx_bytes(summary)
                st.download_button("📥 Tải DOCX", data=docx_io.getvalue(),
                                   file_name=f"Tong_hop_KT_{lop}.docx",
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            except Exception as e:
                st.error(f"Lỗi khi tạo DOCX: {e}")

            # Xuất PDF
            try:
                pdf_io = create_pdf_bytes(summary)
                st.download_button("📥 Tải PDF", data=pdf_io.getvalue(),
                                   file_name=f"Tong_hop_KT_{lop}.pdf",
                                   mime="application/pdf")
            except Exception as e:
                st.error(f"Lỗi khi tạo PDF: {e}")

# -----------------------
# Gợi ý debug nếu vẫn lỗi
# -----------------------
st.markdown("---")
st.markdown("**Gợi ý:** nếu vẫn gặp lỗi, bật `st.write(r.json())` hoặc xem log Streamlit Cloud. "
            "Bạn có thể gửi cho mình phần JSON debug (nếu xuất hiện) để mình hỗ trợ tiếp.")
