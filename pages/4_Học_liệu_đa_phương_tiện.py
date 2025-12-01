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

# ================================
# 1. CẤU HÌNH TRANG
# ================================
st.set_page_config(
    page_title="Công cụ Học Tập Đa Phương Tiện",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 CÔNG CỤ HỌC TẬP ĐA PHƯƠNG TIỆN CHO GIÁO VIÊN & HỌC SINH")

# ================================
# 2. THANH MENU
# ================================
menu = st.sidebar.radio(
    "Chọn chức năng",
    [
        "Tổng hợp kiến thức (AI)",
        "Video học tập",
        "Âm thanh bài giảng",
        "Flashcard công thức",
        "Tạo Quiz kiểm tra",
        "Chấm bài từ hình ảnh (OCR)",
        "Tải tài liệu"
    ]
)

# ================================
# 3. API KEY
# ================================
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Nhập Google API Key:", type="password")


# =========================================================
#                CHỨC NĂNG 1: TỔNG HỢP KIẾN THỨC
# =========================================================
if menu == "Tổng hợp kiến thức (AI)":

    st.header("📘 Tổng hợp kiến thức Toán theo chủ đề")

    lop_options = [f"Lớp {i}" for i in range(1, 10)] + ["Tất cả lớp"]
    lop = st.selectbox("Chọn lớp", lop_options)

    # Prompt AI
    def build_prompt(lop):
        if lop == "Tất cả lớp":
            lop_text = "từ lớp 1 đến lớp 9"
        else:
            lop_text = lop
        return f"""
Tổng hợp toàn bộ kiến thức Toán {lop_text} theo chủ đề:
- Số học
- Đại số
- Hình học
- Thống kê – Xác suất
Dạng trình bày:
• Khái niệm
• Công thức (LaTeX)
• Ví dụ
• Ứng dụng
"""

    # Gọi API Gemini
    def generate(ai_key, prompt):
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={ai_key}"
        payload = {"contents":[{"role":"user","parts":[{"text":prompt}]}]}
        r = requests.post(url, json=payload)
        return r.json()["candidates"][0]["content"][0]["text"]

    # Latex xử lý → ảnh → doc/pdf
    LATEX_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)

    def find_latex(text):
        return [(m.span(), m.group(0), m.group(1)) for m in LATEX_RE.finditer(text)]

    def latex_to_png(code):
        fig = plt.figure()
        fig.patch.set_alpha(0)
        fig.text(0, 0, f"${code}$", fontsize=20)
        buf = io.BytesIO()
        plt.axis('off')
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        plt.close(fig)
        buf.seek(0)
        return buf.read()

    def export_doc(text):
        doc = Document()
        pos = 0
        for span, full, inner in find_latex(text):
            start, end = span
            before = text[pos:start]
            for line in before.splitlines():
                doc.add_paragraph(line)
            try:
                img = latex_to_png(inner)
                doc.add_picture(io.BytesIO(img), width=Inches(3))
            except:
                doc.add_paragraph(full)
            pos = end
        for line in text[pos:].splitlines():
            doc.add_paragraph(line)
        out = io.BytesIO()
        doc.save(out)
        out.seek(0)
        return out

    def export_pdf(text):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        w, h = letter
        y = h - 50
        pos = 0
        for span, full, inner in find_latex(text):
            start, end = span
            for line in text[pos:start].splitlines():
                c.drawString(40, y, line)
                y -= 14
            try:
                img = latex_to_png(inner)
                img_r = ImageReader(io.BytesIO(img))
                c.drawImage(img_r, 40, y - 60, width=250, mask='auto')
                y -= 80
            except:
                c.drawString(40, y, full)
                y -= 14
            pos = end
        for line in text[pos:].splitlines():
            c.drawString(40, y, line)
            y -= 14
        c.save()
        buf.seek(0)
        return buf

    if st.button("⚡ Tổng hợp"):
        if not api_key:
            st.error("Thiếu API Key!")
        else:
            with st.spinner("AI đang xử lý..."):
                output = generate(api_key, build_prompt(lop))
            st.success("Hoàn tất!")
            st.markdown(output.replace("\n", "<br>"), unsafe_allow_html=True)

            doc = export_doc(output)
            pdf = export_pdf(output)

            st.download_button("📥 Tải DOCX", doc, "TongHop.docx")
            st.download_button("📥 Tải PDF", pdf, "TongHop.pdf")


# =========================================================
#                CHỨC NĂNG 2: VIDEO
# =========================================================
if menu == "Video học tập":
    st.header("🎬 Xem video học tập")
    url = st.text_input("Dán link video YouTube:")
    if url:
        st.video(url)


# =========================================================
#                CHỨC NĂNG 3: AUDIO
# =========================================================
if menu == "Âm thanh bài giảng":
    st.header("🎧 Nghe bài giảng / nhạc học tập")
    audio = st.text_input("URL file MP3:")
    if audio:
        st.audio(audio)


# =========================================================
#                CHỨC NĂNG 4: FLASHCARD
# =========================================================
if menu == "Flashcard công thức":
    st.header("🃏 Flashcard ôn tập")
    term = st.text_input("Khái niệm:")
    mean = st.text_input("Giải thích:")
    if st.button("Thêm flashcard"):
        st.session_state.setdefault("flashcards", []).append((term, mean))

    if "flashcards" in st.session_state:
        for t, m in st.session_state["flashcards"]:
            st.success(f"**{t}** → {m}")


# =========================================================
#                CHỨC NĂNG 5: QUIZ
# =========================================================
if menu == "Tạo Quiz kiểm tra":
    st.header("📝 Tạo câu hỏi trắc nghiệm")
    q = st.text_input("Câu hỏi")
    a = st.text_input("A")
    b = st.text_input("B")
    c = st.text_input("C")
    d = st.text_input("D")
    correct = st.selectbox("Đáp án đúng", ["A", "B", "C", "D"])

    if st.button("Thêm câu hỏi"):
        st.session_state.setdefault("quiz", []).append((q, a, b, c, d, correct))

    if "quiz" in st.session_state:
        for idx, (q, a, b, c, d, corr) in enumerate(st.session_state["quiz"]):
            st.info(f"**{idx+1}. {q}**\n- A: {a}\n- B: {b}\n- C: {c}\n- D: {d}\n✔ Đúng: {corr}")


# =========================================================
#                CHỨC NĂNG 6: OCR
# =========================================================
if menu == "Chấm bài từ hình ảnh (OCR)":
    st.header("📷 Upload hình để nhận dạng")
    img = st.file_uploader("Tải ảnh bài toán", type=["png", "jpg"])
    if img:
        st.image(img)
        st.success("Tạm thời chưa bật OCR (Tôi có thể thêm nếu bạn muốn).")


# =========================================================
#                CHỨC NĂNG 7: TÀI LIỆU
# =========================================================
if menu == "Tải tài liệu":
    st.header("📚 Tải tài liệu tham khảo")
    st.download_button("📘 Sách Toán 8 (PDF)", b"PDF content here", "book.pdf")
