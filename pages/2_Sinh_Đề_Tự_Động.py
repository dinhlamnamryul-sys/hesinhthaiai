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
lop_options = [
    "Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5",
    "Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"
]

chuong_options = {
    "Lớp 1": [
        "Chủ đề 1: Các số đến 10",
        "Chủ đề 2: Các số đến 20",
        "Chủ đề 3: Các số đến 100",
        "Chủ đề 4: Hình học và đo lường",
        "Chủ đề 5: Giải toán"
    ],
    "Lớp 2": [
        "Chủ đề 1: Số và phép tính",
        "Chủ đề 2: Đo lường",
        "Chủ đề 3: Hình học",
        "Chủ đề 4: Giải toán có lời văn"
    ],
    "Lớp 3": [
        "Chủ đề 1: Số và phép tính",
        "Chủ đề 2: Đo lường",
        "Chủ đề 3: Hình học",
        "Chủ đề 4: Giải toán"
    ],
    "Lớp 4": [
        "Chủ đề 1: Số tự nhiên – Phép tính",
        "Chủ đề 2: Phân số",
        "Chủ đề 3: Đo lường",
        "Chủ đề 4: Hình học"
    ],
    "Lớp 5": [
        "Chủ đề 1: Số thập phân",
        "Chủ đề 2: Tỉ số – Phần trăm",
        "Chủ đề 3: Đo lường",
        "Chủ đề 4: Hình học"
    ],
    "Lớp 6": [
        "Chương 1: Số tự nhiên",
        "Chương 2: Số nguyên",
        "Chương 3: Phân số",
        "Chương 4: Biểu thức – Đại số",
        "Chương 5: Hình học trực quan"
    ],
    "Lớp 7": [
        "Chương 1: Số hữu tỉ – Số thực",
        "Chương 2: Hàm số và đồ thị",
        "Chương 3: Hình học tam giác",
        "Chương 4: Thống kê"
    ],
    "Lớp 8": [
        "Chương 1: Đại số – Đa thức",
        "Chương 2: Phân thức",
        "Chương 3: Phương trình bậc nhất",
        "Chương 4: Hình học tứ giác – Đa giác"
    ],
    "Lớp 9": [
        "Chương 1: Căn bậc hai – Căn thức",
        "Chương 2: Hàm số bậc nhất",
        "Chương 3: Hàm số bậc hai",
        "Chương 4: Phương trình bậc hai",
        "Chương 5: Hình học không gian – Trụ – Nón – Cầu"
    ]
}

# --- Bài theo Chủ đề/Chương ---
bai_options = {
    # ----- LỚP 1 -----
    "Chủ đề 1: Các số đến 10": ["Bài 1: Đếm, đọc, viết số đến 10", "Bài 2: Cộng trong phạm vi 10", "Bài 3: Trừ trong phạm vi 10"],
    "Chủ đề 2: Các số đến 20": ["Bài 1: Số 11–20", "Bài 2: Cộng – trừ phạm vi 20"],
    "Chủ đề 3: Các số đến 100": ["Bài 1: Số tròn chục", "Bài 2: Phép tính trong phạm vi 100"],
    "Chủ đề 4: Hình học và đo lường": ["Bài 1: Hình tam giác – tròn – vuông – chữ nhật", "Bài 2: Độ dài – cm", "Bài 3: Thời gian – giờ"],
    "Chủ đề 5: Giải toán": ["Bài 1: Giải toán một bước", "Bài 2: Tìm số còn thiếu"],

    # ----- LỚP 2 -----
    "Chủ đề 1: Số và phép tính": ["Bài 1: Số đến 100", "Bài 2: Cộng – trừ có nhớ", "Bài 3: Nhân – chia (làm quen)"],
    "Chủ đề 2: Đo lường": ["Bài 1: Độ dài (m, cm)", "Bài 2: Khối lượng (kg, g)", "Bài 3: Tiền Việt Nam"],
    "Chủ đề 3: Hình học": ["Bài 1: Góc vuông – không vuông", "Bài 2: Tứ giác đơn giản"],
    "Chủ đề 4: Giải toán có lời văn": ["Bài 1: Bài toán 1 bước", "Bài 2: Bài toán 2 bước"],

    # ----- LỚP 3 -----
    "Chủ đề 1: Số và phép tính": ["Bài 1: Số đến 1000", "Bài 2: Nhân – chia trong phạm vi 100", "Bài 3: Biểu thức số"],
    "Chủ đề 2: Đo lường": ["Bài 1: Đơn vị độ dài", "Bài 2: Đơn vị khối lượng", "Bài 3: Diện tích cm²"],
    "Chủ đề 3: Hình học": ["Bài 1: Góc vuông", "Bài 2: Chu vi"],
    "Chủ đề 4: Giải toán": ["Bài 1: Toán 2 bước", "Bài 2: Trung bình cộng"],

    # ----- LỚP 4 -----
    "Chủ đề 1: Số tự nhiên – Phép tính": ["Bài 1: Số đến 100 000", "Bài 2: Nhân – chia nhiều chữ số"],
    "Chủ đề 2: Phân số": ["Bài 1: So sánh phân số", "Bài 2: Phân số bằng nhau"],
    "Chủ đề 3: Đo lường": ["Bài 1: Đơn vị đo diện tích", "Bài 2: Diện tích hình chữ nhật – vuông"],
    "Chủ đề 4: Hình học": ["Bài 1: Hình bình hành", "Bài 2: Hình thoi"],

    # ----- LỚP 5 -----
    "Chủ đề 1: Số thập phân": ["Bài 1: Đọc – viết số thập phân", "Bài 2: Tính với số thập phân"],
    "Chủ đề 2: Tỉ số – Phần trăm": ["Bài 1: Tỉ số", "Bài 2: Tỉ lệ phần trăm"],
    "Chủ đề 3: Đo lường": ["Bài 1: Thể tích", "Bài 2: Diện tích hình thang – tam giác"],
    "Chủ đề 4: Hình học": ["Bài 1: Hình trụ", "Bài 2: Hình cầu"],

    # ----- LỚP 6 -----
    "Chương 1: Số tự nhiên": ["Bài 1: Tập hợp số tự nhiên", "Bài 2: Chia hết – dấu hiệu chia hết"],
    "Chương 2: Số nguyên": ["Bài 1: Số nguyên âm – dương", "Bài 2: Thứ tự trong Z"],
    "Chương 3: Phân số": ["Bài 1: So sánh phân số", "Bài 2: Quy đồng"],
    "Chương 4: Biểu thức – Đại số": ["Bài 1: Biểu thức chứa chữ", "Bài 2: Giá trị biểu thức"],
    "Chương 5: Hình học trực quan": ["Bài 1: Góc", "Bài 2: Tam giác"],

    # ----- LỚP 7 -----
    "Chương 1: Số hữu tỉ – Số thực": ["Bài 1: Số hữu tỉ", "Bài 2: Số thực"],
    "Chương 2: Hàm số và đồ thị": ["Bài 1: Hàm số y=ax", "Bài 2: Đồ thị hàm số"],
    "Chương 3: Hình học tam giác": ["Bài 1: Quan hệ cạnh – góc", "Bài 2: Bằng nhau"],
    "Chương 4: Thống kê": ["Bài 1: Bảng tần số", "Bài 2: Biểu đồ"],

    # ----- LỚP 8 -----
    "Chương 1: Đại số – Đa thức": ["Bài 1: Nhân đa thức", "Bài 2: Hằng đẳng thức"],
    "Chương 2: Phân thức": ["Bài 1: Rút gọn", "Bài 2: Quy đồng"],
    "Chương 3: Phương trình bậc nhất": ["Bài 1: Giải PT bậc nhất", "Bài 2: Bài toán bằng phương trình"],
    "Chương 4: Hình học tứ giác – Đa giác": ["Bài 1: Đa giác", "Bài 2: Diện tích đa giác"],

    # ----- LỚP 9 -----
    "Chương 1: Căn bậc hai – Căn thức": ["Bài 1: Định nghĩa căn", "Bài 2: Các phép biến đổi căn"],
    "Chương 2: Hàm số bậc nhất": ["Bài 1: Đồ thị", "Bài 2: Tính chất"],
    "Chương 3: Hàm số bậc hai": ["Bài 1: Parabol", "Bài 2: Tọa độ đỉnh"],
    "Chương 4: Phương trình bậc hai": ["Bài 1: Công thức nghiệm", "Bài 2: Biện luận"],
    "Chương 5: Hình học không gian – Trụ – Nón – Cầu": ["Bài 1: Hình trụ", "Bài 2: Hình nón", "Bài 3: Hình cầu"]
}

# --- Sidebar ---
with st.sidebar:
    st.header("Thông tin sinh đề")
    lop = st.selectbox("Chọn lớp", lop_options)
    chuong = st.selectbox("Chọn Chủ đề/Chương", chuong_options[lop])
    bai = st.selectbox("Chọn bài", bai_options.get(chuong, []))
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
    prompt = f"""
Bạn là giáo viên Toán. Hãy sinh đề kiểm tra theo sách "Kết nối tri thức với cuộc sống":
- Lớp: {lop}
- Chủ đề/Chương: {chuong}
- Bài: {bai}
- Số câu hỏi: {so_cau}
- Loại câu hỏi: {loai_cau}
- {"Có đáp án" if co_dap_an else "Không có đáp án"}

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
    return prompt

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

# --- XỬ LÝ LaTeX ---
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

# --- BUTTON ---
if st.button("🎯 Sinh đề ngay"):
    if not api_key:
        st.error("Thiếu API Key!")
    else:
        with st.spinner("⏳ AI đang tạo đề..."):
            result = generate_questions(api_key, lop, chuong, bai, so_cau, loai_cau, co_dap_an)

        if isinstance(result, str) and result.startswith("❌"):
            st.error(result)
        else
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
                st.download_button(
                    "📥 Tải TXT",
                    data=result.encode("utf-8"),
                    file_name=f"De_{lop}_{chuong}_{bai}.txt",
                    mime="text/plain"
                )
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
