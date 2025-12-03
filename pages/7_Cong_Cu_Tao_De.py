import os
import io
import math
import json
import pdfplumber
import tempfile
import streamlit as st
import openai
import requests
from docx import Document
from bs4 import BeautifulSoup
from zipfile import ZipFile
from typing import Tuple, List

# ------------------------- CONFIG -------------------------
st.set_page_config(page_title="Tạo đề & Ma trận (AI)", page_icon="📝", layout="wide")
st.title("📝 Tạo ma trận & đề kiểm tra — upload sách, công văn, mẫu đề → AI trả về ma trận & đề")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # bạn có thể thay model ở env

if not OPENAI_API_KEY:
    st.error("Cần thiết lập biến môi trường OPENAI_API_KEY trước khi chạy.")
    st.stop()
openai.api_key = OPENAI_API_KEY

# ------------------------- HELPERS: TẬP TIN -> TEXT -------------------------
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception as e:
        st.warning(f"Không thể đọc PDF bình thường: {e}.")
    return "\n".join(text_parts)

def extract_text_from_docx(file_bytes: bytes) -> str:
    # python-docx cần file path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        doc = Document(tmp.name)
        paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n".join(paragraphs)

def extract_text_from_file(uploaded) -> Tuple[str, str]:
    """
    Trả về (mime_hint, text)
    uploaded: Streamlit UploadedFile
    """
    raw = uploaded.read()
    name_lower = uploaded.name.lower()
    # heuristics
    if name_lower.endswith(".pdf"):
        return ("application/pdf", extract_text_from_pdf(raw))
    if name_lower.endswith(".docx"):
        return ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", extract_text_from_docx(raw))
    if name_lower.endswith(".doc"):
        # try docx extraction fallback (some .doc can't read)
        try:
            return ("application/msword", extract_text_from_docx(raw))
        except Exception:
            return ("application/msword", raw.decode(errors="ignore"))
    # otherwise try to decode as text
    try:
        return ("text/plain", raw.decode("utf-8"))
    except Exception:
        return ("application/octet-stream", raw.decode(errors="ignore"))

# ------------------------- HELPERS: KHOẢNG CẮT/TÓM TẮT -------------------------
def chunk_text(text: str, max_chars: int = 30000) -> List[str]:
    """Chia text lớn thành các chunk <= max_chars theo khoảng xuống dòng."""
    if not text:
        return []
    parts = []
    cur = ""
    for paragraph in text.split("\n\n"):
        if len(cur) + len(paragraph) + 2 <= max_chars:
            cur += paragraph + "\n\n"
        else:
            if cur:
                parts.append(cur)
            # nếu paragraph quá dài vẫn phải chia
            while len(paragraph) > max_chars:
                parts.append(paragraph[:max_chars])
                paragraph = paragraph[max_chars:]
            cur = paragraph + "\n\n"
    if cur.strip():
        parts.append(cur)
    return parts

def summarize_long_texts(chunks: List[str]) -> str:
    """
    Gọi OpenAI để tóm tắt từng chunk rồi ghép lại.
    Trả về một bản tóm tắt hợp nhất.
    """
    summaries = []
    system = "Bạn là trợ lý tóm tắt văn bản, giữ lại các ý chính, chủ đề, tiêu đề chương/bài nếu có."
    for c in chunks:
        prompt = f"Tóm tắt nội dung sau thành đoạn ngắn 3-6 câu, liệt kê các chủ đề chính (nếu có):\n\n{c[:60000]}"
        try:
            resp = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.2
            )
            text = resp.choices[0].message.content.strip()
            summaries.append(text)
        except Exception as e:
            summaries.append(c[:1000])  # fallback: giữ đoạn đầu
    # Ghép các summary
    joined = "\n\n".join(summaries)
    # Nếu vẫn quá dài, cắt ngắn
    if len(joined) > 30000:
        return joined[:30000]
    return joined

# ------------------------- HELPERS: GỌI OPENAI -------------------------
def call_openai_generate_matrix_and_exam(textbook_text: str, official_doc_text: str, template_text: str, instruction: str) -> dict:
    """
    Xây prompt rõ ràng, yêu cầu trả về JSON:
    {"matrixHtml": "...", "examHtml": "..."}
    """
    # Bảo đảm không quá dài: nếu lớn, tóm tắt
    combined_len = len(textbook_text or "") + len(official_doc_text or "") + len(template_text or "")
    if combined_len > 90000:
        # chunk và summarize
        tb_chunks = chunk_text(textbook_text, max_chars=30000)
        textbook_text = summarize_long_texts(tb_chunks)
        off_chunks = chunk_text(official_doc_text, max_chars=30000)
        official_doc_text = summarize_long_texts(off_chunks)
        tpl_chunks = chunk_text(template_text, max_chars=20000)
        template_text = summarize_long_texts(tpl_chunks)

    system_msg = (
        "Bạn là một trợ lý chuyên tạo MA TRẬN (dạng bảng HTML) và ĐỀ KIỂM TRA (HTML) "
        "theo đúng MẪU đề được cung cấp. Luôn trả về đúng **JSON** hợp lệ duy nhất "
        "không có text phụ ngoài JSON, có hai khoá: matrixHtml và examHtml. "
        "matrixHtml phải là một đoạn HTML chứa bảng ma trận (các ô, tiêu đề), "
        "examHtml phải là HTML chứa đề kiểm tra đầy đủ theo mẫu."
    )

    user_msg = (
        "Dưới đây là nội dung trích xuất từ các file mà người dùng upload.\n\n"
        f"=== Textbook (SGK) ===\n{(textbook_text[:50000] + '...') if len(textbook_text)>50000 else textbook_text}\n\n"
        f"=== Official doc (Công văn) ===\n{(official_doc_text[:20000]+'...') if len(official_doc_text)>20000 else official_doc_text}\n\n"
        f"=== Template (MẪU ĐỀ) ===\n{(template_text[:20000]+'...') if len(template_text)>20000 else template_text}\n\n"
        f"=== Yêu cầu người dùng ===\n{instruction}\n\n"
        "Yêu cầu cụ thể:\n"
        "1) Sinh MA TRẬN (matrixHtml) phù hợp với nội dung và phân bổ 21 câu (theo CV/tiêu chí người dùng nếu có).\n"
        "2) Sinh ĐỀ (examHtml) đúng cấu trúc mẫu đề (tiêu đề, phần trắc nghiệm/tn, phần tự luận...), "
        "đảm bảo số câu / điểm khớp với ma trận. Không chèn thông tin bí mật.\n\n"
        "Output MUST be valid JSON, for example:\n"
        '{"matrixHtml":"<table>...</table>", "examHtml":"<div>...</div>"}\n'
        "Nếu không thể tạo đầy đủ câu hỏi vì nguồn không đủ, ghi chú trong examHtml lý do (dưới dạng comment HTML)."
    )

    try:
        resp = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=4500,
            temperature=0.2
        )
        raw = resp.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Lỗi gọi OpenAI: {e}")

    # TRY parse as JSON; nếu model trả thêm text trước/sau JSON thì cố gắng extract {...}
    try:
        parsed = json.loads(raw)
        return parsed
    except json.JSONDecodeError:
        # tìm dấu ngoặc JSON đầu tiên
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                parsed = json.loads(raw[start:end+1])
                return parsed
            except Exception:
                pass
    # Nếu không parse được, raise để debug (kèm raw)
    raise RuntimeError("OpenAI trả về không phải JSON hợp lệ. Nội dung trả về (rút gọn):\n" + raw[:2000])

# ------------------------- HELPERS: HTML -> DOCX/HTML xuất file -------------------------
def html_to_plain_text(html: str) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    # giữ một số tag tiêu đề, li, p thành text với xuống dòng
    for br in soup.find_all("br"):
        br.replace_with("\n")
    texts = []
    for el in soup.find_all(["h1","h2","h3","h4","p","li","tr","td"]):
        txt = el.get_text(separator=" ", strip=True)
        if txt:
            texts.append(txt)
    plain = "\n\n".join(texts)
    return plain

def make_docx_from_htmls(matrix_html: str, exam_html: str, meta_title: str="ĐỀ KIỂM TRA") -> bytes:
    doc = Document()
    doc.add_heading(meta_title, level=1)
    doc.add_heading("I. MA TRẬN", level=2)
    if matrix_html:
        matrix_text = html_to_plain_text(matrix_html)
        for line in matrix_text.split("\n\n"):
            doc.add_paragraph(line)
    else:
        doc.add_paragraph("Không có ma trận")

    doc.add_page_break()
    doc.add_heading("II. ĐỀ KIỂM TRA", level=2)
    if exam_html:
        exam_text = html_to_plain_text(exam_html)
        for line in exam_text.split("\n\n"):
            doc.add_paragraph(line)
    else:
        doc.add_paragraph("Không có đề")
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.read()

# ------------------------- STREAMLIT UI -------------------------
st.markdown("""
**Hướng dẫn:** Upload 3 file (SGK, Công văn, Mẫu đề). Nhập ghi chú / yêu cầu (ví dụ: 'tạo ma trận 21 câu, 10 điểm, tỉ lệ 25/25/50; format theo mẫu để in A4'). 
Sau đó bấm **TẠO** để AI sinh ma trận và đề.
""")

col1, col2 = st.columns(2)
with col1:
    uploaded_textbook = st.file_uploader("1) Tải lên: Sách giáo khoa (PDF/DOCX)", type=['pdf','docx','doc'], key='tb')
    uploaded_official = st.file_uploader("2) Tải lên: Công văn / Công bố (PDF/DOCX)", type=['pdf','docx','doc'], key='cv')

with col2:
    uploaded_template = st.file_uploader("3) Tải lên: Mẫu đề kiểm tra (PDF/DOCX)", type=['pdf','docx','doc'], key='tpl')
    instruction = st.text_area("Yêu cầu / Ghi chú cho AI (bắt buộc)", value="Tạo ma trận 21 câu, 10 điểm; format theo mẫu; phân bổ 6 NB, 8 TH, 7 VĐ/VĐC", height=120)

if st.button("🚀 TẠO MA TRẬN & ĐỀ"):
    if not uploaded_textbook or not uploaded_official or not uploaded_template:
        st.error("Vui lòng tải lên đủ 3 file: SGK, Công văn, Mẫu đề.")
    else:
        with st.spinner("Đang trích xuất nội dung từ file..."):
            tb_mime, tb_text = extract_text_from_file(uploaded_textbook)
            cv_mime, cv_text = extract_text_from_file(uploaded_official)
            tpl_mime, tpl_text = extract_text_from_file(uploaded_template)

        # hiển thị kích thước / phần trích xuất
        st.info(f"Đã trích xuất: SGK ~{len(tb_text)} ký tự | Công văn ~{len(cv_text)} ký tự | Mẫu đề ~{len(tpl_text)} ký tự")

        try:
            with st.spinner("Gọi AI để tạo ma trận & đề... (có thể mất 10-40s tùy model)"):
                result = call_openai_generate_matrix_and_exam(tb_text, cv_text, tpl_text, instruction)
        except Exception as e:
            st.exception(e)
            st.stop()

        # Validate result
        matrix_html = result.get("matrixHtml") or result.get("matrix") or ""
        exam_html = result.get("examHtml") or result.get("exam") or ""
        if not matrix_html and not exam_html:
            st.error("AI không trả về matrixHtml hoặc examHtml.")
            st.write(result)
            st.stop()

        st.success("Hoàn tất: AI trả về kết quả. Hiển thị bên dưới.")

        # Hiển thị Ma trận
        st.markdown("---")
        st.subheader("📊 Ma trận (xem trước HTML)")
        try:
            st.components.v1.html(matrix_html, height=360, scrolling=True)
        except Exception:
            st.markdown(matrix_html, unsafe_allow_html=True)

        # Hiển thị Đề
        st.markdown("---")
        st.subheader("📄 Đề kiểm tra (xem trước HTML)")
        try:
            st.components.v1.html(exam_html, height=540, scrolling=True)
        except Exception:
            st.markdown(exam_html, unsafe_allow_html=True)

        # Tải file HTML
        st.markdown("---")
        st.download_button("📥 Tải HTML - Ma trận", data=matrix_html.encode('utf-8'), file_name="matrix.html", mime="text/html")
        st.download_button("📥 Tải HTML - Đề", data=exam_html.encode('utf-8'), file_name="exam.html", mime="text/html")

        # Tạo và tải DOCX từ HTML (chuyển HTML -> plain text -> docx)
        docx_bytes = make_docx_from_htmls(matrix_html, exam_html, meta_title=f"ĐỀ - Generated")
        st.download_button("📥 Tải DOCX (Ma trận + Đề)", data=docx_bytes, file_name=f"De_MaTran_Generated.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        # Show raw JSON (collapsed)
        with st.expander("🔧 (Raw) JSON trả về từ AI"):
            st.json(result)
