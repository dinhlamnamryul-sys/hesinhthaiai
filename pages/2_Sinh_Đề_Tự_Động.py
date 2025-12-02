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

# Cấu hình matplotlib để hiển thị công thức toán
plt.rcParams['mathtext.fontset'] = 'cm'

st.set_page_config(page_title="Sinh Đề KNTC Tự Động", page_icon="📝", layout="wide")
st.title("📝 Sinh Đề Tự Động – Theo Ma Trận Đặc Tả Tối Giản")

# --- API KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- DỮ LIỆU MOCK (Giữ nguyên) ---
lop_options = [
    "Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5",
    "Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"
]

chuong_options = {
    "Lớp 1": ["Chủ đề 1: Các số đến 10", "Chủ đề 2: Các số đến 20", "Chủ đề 3: Các số đến 100", "Chủ đề 4: Hình học và đo lường", "Chủ đề 5: Giải toán"],
    "Lớp 6": ["Chương 1: Số tự nhiên", "Chương 2: Số nguyên", "Chương 3: Phân số", "Chương 4: Biểu thức – Đại số", "Chương 5: Hình học trực quan"],
    "Lớp 9": ["Chương 1: Căn bậc hai – Căn thức", "Chương 2: Hàm số bậc nhất", "Chương 3: Hàm số bậc hai", "Chương 4: Phương trình bậc hai", "Chương 5: Hình học không gian – Trụ – Nón – Cầu"],
    # ... Thêm các lớp khác ...
}

bai_options = {
    # ... Dữ liệu bài học đã cho ...
    "Chủ đề 1: Các số đến 10": ["Đếm, đọc, viết số đến 10", "Cộng trong phạm vi 10", "Trừ trong phạm vi 10"],
    "Chương 1: Số tự nhiên": ["Tập hợp số tự nhiên", "Chia hết – dấu hiệu chia hết"],
    "Chương 1: Căn bậc hai – Căn thức": ["Định nghĩa căn", "Các phép biến đổi căn"],
}
# Thêm đầy đủ dữ liệu bai_options từ yêu cầu trước
bai_options.update({
    "Chủ đề 1: Các số đến 10": ["Đếm, đọc, viết số đến 10", "Cộng trong phạm vi 10", "Trừ trong phạm vi 10"],
    "Chủ đề 2: Các số đến 20": ["Số 11–20", "Cộng – trừ phạm vi 20"],
    "Chủ đề 3: Các số đến 100": ["Số tròn chục", "Phép tính trong phạm vi 100"],
    "Chủ đề 4: Hình học và đo lường": ["Hình tam giác – tròn – vuông – chữ nhật", "Độ dài – cm", "Thời gian – giờ"],
    "Chủ đề 5: Giải toán": ["Giải toán một bước", "Tìm số còn thiếu"],

    "Chủ đề 1: Số và phép tính": ["Số đến 100", "Cộng – trừ có nhớ", "Nhân – chia (làm quen)"],
    "Chủ đề 2: Đo lường": ["Độ dài (m, cm)", "Khối lượng (kg, g)", "Tiền Việt Nam"],
    "Chủ đề 3: Hình học": ["Góc vuông – không vuông", "Tứ giác đơn giản"],
    "Chủ đề 4: Giải toán có lời văn": ["Bài toán 1 bước", "Bài toán 2 bước"],

    "Chủ đề 1: Số và phép tính": ["Số đến 1000", "Nhân – chia trong phạm vi 100", "Biểu thức số"],
    "Chủ đề 2: Đo lường": ["Đơn vị độ dài", "Đơn vị khối lượng", "Diện tích cm²"],
    "Chủ đề 3: Hình học": ["Góc vuông", "Chu vi"],
    "Chủ đề 4: Giải toán": ["Toán 2 bước", "Trung bình cộng"],

    "Chủ đề 1: Số tự nhiên – Phép tính": ["Số đến 100 000", "Nhân – chia nhiều chữ số"],
    "Chủ đề 2: Phân số": ["So sánh phân số", "Phân số bằng nhau"],
    "Chủ đề 3: Đo lường": ["Đơn vị đo diện tích", "Diện tích hình chữ nhật – vuông"],
    "Chủ đề 4: Hình học": ["Hình bình hành", "Hình thoi"],

    "Chủ đề 1: Số thập phân": ["Đọc – viết số thập phân", "Tính với số thập phân"],
    "Chủ đề 2: Tỉ số – Phần trăm": ["Tỉ số", "Tỉ lệ phần trăm"],
    "Chủ đề 3: Đo lường": ["Thể tích", "Diện tích hình thang – tam giác"],
    "Chủ đề 4: Hình học": ["Hình trụ", "Hình cầu"],

    "Chương 1: Số tự nhiên": ["Tập hợp số tự nhiên", "Chia hết – dấu hiệu chia hết"],
    "Chương 2: Số nguyên": ["Số nguyên âm – dương", "Thứ tự trong Z"],
    "Chương 3: Phân số": ["So sánh phân số", "Quy đồng phân số"],
    "Chương 4: Biểu thức – Đại số": ["Biểu thức chứa chữ", "Giá trị biểu thức"],
    "Chương 5: Hình học trực quan": ["Góc", "Tam giác"],

    "Chương 1: Số hữu tỉ – Số thực": ["Số hữu tỉ", "Số thực"],
    "Chương 2: Hàm số và đồ thị": ["Hàm số y=ax", "Đồ thị hàm số"],
    "Chương 3: Hình học tam giác": ["Quan hệ cạnh – góc", "Tam giác bằng nhau"],
    "Chương 4: Thống kê": ["Bảng tần số", "Biểu đồ"],

    "Chương 1: Đại số – Đa thức": ["Nhân đa thức", "Hằng đẳng thức"],
    "Chương 2: Phân thức": ["Rút gọn", "Quy đồng phân thức"],
    "Chương 3: Phương trình bậc nhất": ["Giải phương trình bậc nhất", "Bài toán bằng phương trình"],
    "Chương 4: Hình học tứ giác – Đa giác": ["Đa giác", "Diện tích đa giác"],

    "Chương 1: Căn bậc hai – Căn thức": ["Định nghĩa căn", "Các phép biến đổi căn"],
    "Chương 2: Hàm số bậc nhất": ["Đồ thị", "Tính chất"],
    "Chương 3: Hàm số bậc hai": ["Parabol", "Tọa độ đỉnh"],
    "Chương 4: Phương trình bậc hai": ["Công thức nghiệm", "Biện luận"],
    "Chương 5: Hình học không gian – Trụ – Nón – Cầu": ["Hình trụ", "Hình nón", "Hình cầu"]
})
# Thêm đầy đủ dữ liệu chuong_options từ yêu cầu trước
chuong_options.update({
    "Lớp 2": ["Chủ đề 1: Số và phép tính", "Chủ đề 2: Đo lường", "Chủ đề 3: Hình học", "Chủ đề 4: Giải toán có lời văn"],
    "Lớp 3": ["Chủ đề 1: Số và phép tính", "Chủ đề 2: Đo lường", "Chủ đề 3: Hình học", "Chủ đề 4: Giải toán"],
    "Lớp 4": ["Chủ đề 1: Số tự nhiên – Phép tính", "Chủ đề 2: Phân số", "Chủ đề 3: Đo lường", "Chủ đề 4: Hình học"],
    "Lớp 5": ["Chủ đề 1: Số thập phân", "Chủ đề 2: Tỉ số – Phần trăm", "Chủ đề 3: Đo lường", "Chủ đề 4: Hình học"],
    "Lớp 7": ["Chương 1: Số hữu tỉ – Số thực", "Chương 2: Hàm số và đồ thị", "Chương 3: Hình học tam giác", "Chương 4: Thống kê"],
    "Lớp 8": ["Chương 1: Đại số – Đa thức", "Chương 2: Phân thức", "Chương 3: Phương trình bậc nhất", "Chương 4: Hình học tứ giác – Đa giác"]
})

# --- GIAO DIỆN VÀ THAM SỐ MA TRẬN TỐI GIẢN ---
with st.sidebar:
    st.header("Thông tin sinh đề")
    lop = st.selectbox("Chọn lớp", lop_options, index=5) # Default Lớp 6
    chuong = st.selectbox("Chọn chủ đề/chương", chuong_options.get(lop, []), index=0)
    bai_list = bai_options.get(chuong, [])
    if bai_list:
        bai = st.selectbox("Chọn bài", bai_list, index=0)
    else:
        bai = st.text_input("Chưa có bài cho chủ đề này", "")

    st.markdown("---")
    st.subheader("⚙️ Phân bổ theo Ma trận (CV 7991 Tối giản)")

    # Cấu hình số câu hỏi tổng cộng
    so_cau = st.number_input("Tổng số câu hỏi", min_value=1, max_value=50, value=21)
    
    col_nl, col_ds, col_tl = st.columns(3)
    with col_nl:
        phan_bo_nl = st.number_input("NL (Nhiều Lựa chọn)", min_value=0, value=12)
    with col_ds:
        phan_bo_ds = st.number_input("DS (Đúng - Sai)", min_value=0, value=2)
    with col_tl:
        phan_bo_tl = st.number_input("TL (Tự luận/Trả lời ngắn)", min_value=0, value=7)
    
    st.markdown("---")
    st.subheader("Độ khó (Cognitive Level)")
    
    col_nb, col_th, col_vd = st.columns(3)
    with col_nb:
        so_cau_nb = st.number_input("Nhận biết", min_value=0, value=6)
    with col_th:
        so_cau_th = st.number_input("Thông hiểu", min_value=0, value=8)
    with col_vd:
        so_cau_vd = st.number_input("Vận dụng/VDC", min_value=0, value=7)

    total_check = phan_bo_nl + phan_bo_ds + phan_bo_tl
    total_level = so_cau_nb + so_cau_th + so_cau_vd

    if total_check != so_cau:
        st.error(f"Tổng số câu ({total_check}) không khớp Tổng ({so_cau}).")
    if total_level != so_cau:
        st.error(f"Tổng cấp độ ({total_level}) không khớp Tổng ({so_cau}).")

    co_dap_an = st.checkbox("Có đáp án", value=True)

# --- BUILD PROMPT (Cập nhật để bao gồm Ma trận) ---
def build_prompt(lop, chuong, bai, so_cau, phan_bo_nl, phan_bo_ds, phan_bo_tl, so_cau_nb, so_cau_th, so_cau_vd, co_dap_an):
    prompt_ma_tran = f"""
Cấu trúc ĐỀ VÀ MA TRẬN ĐẶC TẢ TỐI GIẢN (Tổng {so_cau} câu):
1. PHẦN TRẮC NGHIỆM KHÁCH QUAN (NL/DS)
    - Số câu Nhiều Lựa chọn (NL): {phan_bo_nl} câu.
    - Số câu Đúng - Sai (DS): {phan_bo_ds} câu.
2. PHẦN TỰ LUẬN (TL) / TRẢ LỜI NGẮN
    - Số câu Tự luận/Trả lời ngắn (TL): {phan_bo_tl} câu.

PHÂN BỔ MỨC ĐỘ NHẬN THỨC:
    - Nhận biết: {so_cau_nb} câu
    - Thông hiểu: {so_cau_th} câu
    - Vận dụng/VDC: {so_cau_vd} câu

YÊU CẦU ĐỀ BÀI:
1. Tạo {so_cau} câu hỏi, trong đó:
    - {phan_bo_nl} câu Trắc nghiệm 4 lựa chọn (A, B, C, D).
    - {phan_bo_ds} câu Trắc nghiệm Đúng - Sai (mỗi câu có 4 ý a, b, c, d).
    - {phan_bo_tl} câu Tự luận hoặc Trả lời ngắn.
2. Đảm bảo tổng số câu theo từng mức độ nhận thức (NB/TH/VĐ) khớp với phân bổ trên.
3. Đặt Tiêu đề rõ ràng cho từng phần.
4. Mỗi câu hỏi phải được gắn nhãn Mức độ và Loại câu hỏi (ví dụ: Câu 1. [NL - Nhận biết]).
5. Toàn bộ công thức toán phải được viết bằng LaTeX và **phải** đặt trong delimiters $$...$$. Ví dụ: $$\\frac{{a}}{{b}}$$
6. {"Tạo Đáp án và Lời giải chi tiết sau mỗi câu hỏi." if co_dap_an else "Không cần Đáp án."}
"""

    prompt_context = f"""
Bạn là giáo viên Toán, hãy sinh đề kiểm tra cho {lop} theo sách "Kết nối tri thức với cuộc sống".
- Chủ đề/Chương: {chuong}
- Bài: {bai}
{prompt_ma_tran}
"""
    return prompt_context

# --- GỌI API (Giữ nguyên) ---
def generate_questions(api_key, *args):
    # Lấy các tham số từ *args
    lop, chuong, bai, so_cau, phan_bo_nl, phan_bo_ds, phan_bo_tl, so_cau_nb, so_cau_th, so_cau_vd, co_dap_an = args
    MODEL = "models/gemini-2.5-flash" # Dùng flash để tăng tốc độ
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"
    
    prompt = build_prompt(*args) # Truyền tất cả các args
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    
    try:
        r = requests.post(url, json=payload, timeout=60)
        if r.status_code != 200:
            try:
                j_error = r.json()
                error_message = j_error.get("error", {}).get("message", r.text)
            except:
                error_message = r.text
            return f"❌ Lỗi API {r.status_code}: {error_message}"
        j = r.json()
        if j.get("candidates") and j["candidates"][0].get("content", {}).get("parts"):
            return j["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "❌ Lỗi: AI không trả về nội dung. Thử lại hoặc thay đổi nội dung."
    except requests.exceptions.Timeout:
        return "❌ Lỗi kết nối: Yêu cầu hết thời gian chờ (Timeout)."
    except Exception as e:
        return f"❌ Lỗi kết nối hoặc xử lý dữ liệu: {e}"

# --- XỬ LÝ LaTeX VÀ TẠO FILE (Giữ nguyên) ---
LATEX_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
def find_latex_blocks(text):
    return [(m.span(), m.group(0), m.group(1)) for m in LATEX_RE.finditer(text)]

def render_latex_png_bytes(latex_code, fontsize=20, dpi=200):
    fig = plt.figure()
    fig.patch.set_alpha(0.0)
    fig.text(0.05, 0.5, f"${latex_code}$", fontsize=fontsize, va='center', ha='left')
    buf = io.BytesIO()
    plt.axis('off')
    plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', pad_inches=0.1, transparent=True)
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
            r.add_picture(img_stream, width=Inches(3.5)) 
        except Exception as e:
            doc.add_paragraph(full)
            st.warning(f"Lỗi chèn LaTeX vào DOCX, chèn văn bản thay thế: {e}")
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
    line_height = 14
    
    def check_page():
        nonlocal y
        if y < margin + 20:
            c.showPage()
            y = height - 50

    last = 0
    for span, full, inner in find_latex_blocks(text):
        start, end = span
        before = text[last:start]
        for line in before.splitlines():
            check_page()
            c.drawString(margin, y, line)
            y -= line_height

        try:
            png_bytes = render_latex_png_bytes(inner)
            img_reader = ImageReader(io.BytesIO(png_bytes))
            img = Image.open(io.BytesIO(png_bytes))
            
            draw_w = 300 
            draw_h = img.height / img.width * draw_w
            
            check_page() 
            
            c.drawImage(img_reader, margin, y - draw_h, width=draw_w, height=draw_h, mask='auto')
            y -= draw_h + 8
        except Exception as e:
            st.warning(f"Lỗi chèn LaTeX vào PDF, chèn văn bản thay thế: {e}")
            check_page()
            c.drawString(margin, y, full)
            y -= line_height
            
        last = end
    
    for line in text[last:].splitlines():
        check_page()
        c.drawString(margin, y, line)
        y -= line_height
        
    c.save()
    buf.seek(0)
    return buf

# --- BUTTON ---
if st.button("🎯 Sinh đề ngay", type="primary", use_container_width=True):
    if not api_key:
        st.error("Thiếu API Key! Vui lòng nhập khóa API của bạn.")
    elif total_check != so_cau or total_level != so_cau:
        st.error("Lỗi Ma trận: Tổng số câu theo loại (NL/DS/TL) hoặc theo cấp độ (NB/TH/VĐ) phải bằng Tổng số câu.")
    else:
        with st.spinner("⏳ AI đang tạo đề dựa trên Ma trận Đặc tả..."):
            result = generate_questions(api_key, lop, chuong, bai, so_cau, phan_bo_nl, phan_bo_ds, phan_bo_tl, so_cau_nb, so_cau_th, so_cau_vd, co_dap_an)

        if isinstance(result, str) and result.startswith("❌"):
            st.error(result)
        else:
            st.success("🎉 Đã tạo xong đề theo Ma trận Đặc tả. (Hiển thị nội dung).")
            st.markdown("---")
            st.subheader("Nội dung Đề (Raw Text)")
            st.markdown(result.replace("\n", "<br>"), unsafe_allow_html=True)
            st.markdown("---")

            latex_blocks = find_latex_blocks(result)
            download_col1, download_col2, download_col3 = st.columns(3)

            if not latex_blocks:
                st.warning("Không tìm thấy công thức LaTeX ( $$...$$ ). Chỉ có thể xuất raw TXT.")
                with download_col1:
                    st.download_button(
                        "📥 Tải TXT", data=result.encode("utf-8"),
                        file_name=f"De_{lop}_{chuong}_{bai}.txt", mime="text/plain",
                        use_container_width=True
                    )
            else:
                try:
                    docx_io = create_docx_bytes(result)
                    with download_col1:
                        st.download_button(
                            "📥 Tải DOCX (công thức là ảnh)",
                            data=docx_io.getvalue(),
                            file_name=f"De_{lop}_{chuong}_{bai}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                except Exception as e:
                    with download_col1:
                        st.error(f"Lỗi tạo DOCX: {e}")

                try:
                    pdf_io = create_pdf_bytes(result)
                    with download_col2:
                        st.download_button(
                            "📥 Tải PDF (công thức là ảnh)",
                            data=pdf_io.getvalue(),
                            file_name=f"De_{lop}_{chuong}_{bai}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    with download_col2:
                        st.error(f"Lỗi tạo PDF: {e}")
