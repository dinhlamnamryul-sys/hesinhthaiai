import os
import io
import math
import json
import tempfile
import streamlit as st
import requests
from typing import Tuple, List

# --- Xử lý Import Error ---
# Phần này giúp báo lỗi rõ ràng trên giao diện nếu thiếu thư viện
try:
    import pdfplumber
    import openai
    from docx import Document
    from bs4 import BeautifulSoup
except ImportError as e:
    st.error(f"Lỗi thiếu thư viện: {e}")
    st.info("Vui lòng đảm bảo file 'requirements.txt' đã có đầy đủ: pdfplumber, openai, python-docx, beautifulsoup4")
    st.stop()

# ------------------------- CONFIG -------------------------
st.set_page_config(page_title="Tạo đề & Ma trận (AI)", page_icon="📝", layout="wide")
st.title("📝 Tạo ma trận & đề kiểm tra — upload sách, công văn, mẫu đề → AI trả về ma trận & đề")

# Lấy API Key từ Secrets hoặc biến môi trường
# Ưu tiên lấy từ st.secrets nếu chạy trên Streamlit Cloud
if "OPENAI_API_KEY" in st.secrets:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
else:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini") 

if not OPENAI_API_KEY:
    st.warning("⚠️ Chưa tìm thấy API Key.")
    st.markdown("""
    **Cách khắc phục:**
    1. Nếu chạy Local: Tạo biến môi trường `OPENAI_API_KEY`.
    2. Nếu chạy Streamlit Cloud: Vào **Settings** > **Secrets** và thêm:
    ```toml
    OPENAI_API_KEY = "sk-..."
    ```
    """)
    st.stop()
else:
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
    # python-docx cần file path hoặc file-like object
    try:
        # Cách 1: Dùng BytesIO trực tiếp (nhanh hơn, không cần tempfile)
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
        return "\n".join(paragraphs)
    except Exception:
        # Fallback: Dùng tempfile nếu cách trên lỗi
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file_bytes)
            tmp.flush()
            try:
                doc = Document(tmp.name)
                paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
                return "\n".join(paragraphs)
            finally:
                os.unlink(tmp.name)

def extract_text_from_file(uploaded) -> Tuple[str, str]:
    """
    Trả về (mime_hint, text)
    uploaded: Streamlit UploadedFile
    """
    if uploaded is None:
        return ("", "")
        
    raw = uploaded.read()
    name_lower = uploaded.name.lower()
    
    # Reset pointer sau khi read (quan trọng nếu cần đọc lại)
    uploaded.seek(0)
    
    # heuristics
    if name_lower.endswith(".pdf"):
        return ("application/pdf", extract_text_from_pdf(raw))
    if name_lower.endswith(".docx"):
        return ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", extract_text_from_docx(raw))
    if name_lower.endswith(".doc"):
        # File .doc cũ rất khó đọc bằng python thuần, thử đọc như docx hoặc text
        try:
            return ("application/msword", extract_text_from_docx(raw))
        except Exception:
            # Fallback sang text decode
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
    system = "Bạn là trợ lý tóm tắt văn bản giáo dục, giữ lại các ý chính, chủ đề, nội dung bài học."
    
    progress_text = st.empty()
    
    for i, c in enumerate(chunks):
        progress_text.text(f"Đang tóm tắt phần {i+1}/{len(chunks)}...")
        prompt = f"Tóm tắt nội dung sau thành các gạch đầu dòng chi tiết về kiến thức:\n\n{c[:50000]}"
        try:
            # Sử dụng cú pháp cũ (openai<1.0.0) như yêu cầu của user
            resp = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.2
            )
            text = resp.choices[0].message.content.strip()
            summaries.append(text)
        except Exception as e:
            summaries.append(c[:2000])  # fallback: giữ đoạn đầu
            
    progress_text.empty()
    
    # Ghép các summary
    joined = "\n\n".join(summaries)
    if len(joined) > 30000:
        return joined[:30000]
    return joined

# ------------------------- HELPERS: GỌI OPENAI -------------------------
def call_openai_generate_matrix_and_exam(textbook_text: str, official_doc_text: str, template_text: str, instruction: str) -> dict:
    # Bảo đảm không quá dài: nếu lớn, tóm tắt
    combined_len = len(textbook_text or "") + len(official_doc_text or "") + len(template_text or "")
    
    # Ngưỡng token ước tính (1 char ~ 0.25 token, 90k chars ~ 22k tokens). 
    # GPT-4o-mini context window là 128k, nhưng output bị giới hạn.
    if combined_len > 80000:
        st.info("Nội dung quá dài, hệ thống đang tự động tóm tắt bớt...")
        tb_chunks = chunk_text(textbook_text, max_chars=30000)
        textbook_text = summarize_long_texts(tb_chunks) if len(textbook_text) > 30000 else textbook_text
        
        # Chỉ tóm tắt SGK là chủ yếu, công văn và mẫu đề nên giữ nguyên nếu có thể
        if len(official_doc_text) > 30000:
             off_chunks = chunk_text(official_doc_text, max_chars=30000)
             official_doc_text = summarize_long_texts(off_chunks)

    system_msg = (
        "Bạn là một chuyên gia giáo dục chuyên tạo MA TRẬN (dạng bảng HTML) và ĐỀ KIỂM TRA (HTML) "
        "theo đúng MẪU đề được cung cấp. "
        "Output bắt buộc là JSON hợp lệ, có hai khoá: 'matrixHtml' và 'examHtml'.\n"
        "- 'matrixHtml': HTML table ma trận đặc tả kỹ thuật.\n"
        "- 'examHtml': HTML đề thi hoàn chỉnh (Trắc nghiệm + Tự luận).\n"
        "Tuyệt đối không trả về markdown block (```json), chỉ trả về raw JSON string."
    )

    user_msg = (
        "Dưới đây là tài liệu nguồn:\n\n"
        f"=== NỘI DUNG SGK (Kiến thức nguồn) ===\n{textbook_text}\n\n"
        f"=== CÔNG VĂN / KHUNG CHƯƠNG TRÌNH ===\n{official_doc_text}\n\n"
        f"=== MẪU ĐỀ (Template Format) ===\n{template_text}\n\n"
        f"=== YÊU CẦU CỦA GIÁO VIÊN ===\n{instruction}\n\n"
        "Hãy thực hiện:\n"
        "1. Xây dựng MA TRẬN đề thi (matrixHtml) phù hợp với công văn và yêu cầu.\n"
        "2. Soạn ĐỀ THI (examHtml) dựa trên ma trận vừa tạo. Nội dung câu hỏi lấy từ SGK. Hình thức trình bày giống Mẫu Đề.\n"
        "Output format: JSON { \"matrixHtml\": \"...\", \"examHtml\": \"...\" }"
    )

    try:
        resp = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            # Tăng max_tokens để đảm bảo JSON không bị cắt giữa chừng
            max_tokens=10000 if "gpt-4" in OPENAI_MODEL else 4000, 
            temperature=0.3
        )
        raw = resp.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Lỗi gọi OpenAI: {e}")

    # Xử lý làm sạch chuỗi JSON nếu model lỡ thêm markdown block
    cleaned_raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(cleaned_raw)
        return parsed
    except json.JSONDecodeError:
        # Fallback: Cố gắng tìm chuỗi JSON trong text hỗn tạp
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                parsed = json.loads(raw[start:end+1])
                return parsed
            except Exception:
                pass
        raise RuntimeError(f"OpenAI trả về không phải JSON hợp lệ.\nRaw: {raw[:500]}...")

# ------------------------- HELPERS: HTML -> DOCX -------------------------
def html_to_plain_text(html: str) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    # Thay thế br bằng xuống dòng
    for br in soup.find_all("br"):
        br.replace_with("\n")
    
    # Lấy text
    text = soup.get_text(separator="\n")
    
    # Xử lý các dòng trống quá nhiều
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)

def make_docx_from_htmls(matrix_html: str, exam_html: str) -> bytes:
    doc = Document()
    doc.add_heading("KẾT QUẢ TẠO ĐỀ TỰ ĐỘNG", level=0)
    
    doc.add_heading("I. MA TRẬN ĐỀ THI", level=1)
    if matrix_html:
        # Đây là cách chuyển đổi đơn giản (text only). 
        # Để giữ bảng HTML trong Docx cần thư viện phức tạp hơn (như htmldocx)
        # Ở đây ta dùng beautifulsoup để lấy text và giữ cấu trúc cơ bản
        matrix_text = html_to_plain_text(matrix_html)
        doc.add_paragraph(matrix_text)
    else:
        doc.add_paragraph("[Không có nội dung ma trận]")

    doc.add_page_break()
    
    doc.add_heading("II. ĐỀ KIỂM TRA", level=1)
    if exam_html:
        exam_text = html_to_plain_text(exam_html)
        doc.add_paragraph(exam_text)
    else:
        doc.add_paragraph("[Không có nội dung đề]")
        
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.read()

# ------------------------- STREAMLIT UI -------------------------
st.info("💡 Mẹo: Nhập API Key trong Settings nếu chạy trên Cloud để không phải setup biến môi trường.")

col1, col2 = st.columns(2)
with col1:
    uploaded_textbook = st.file_uploader("1. Sách giáo khoa (Nguồn kiến thức)", type=['pdf','docx','doc'], key='tb')
    uploaded_official = st.file_uploader("2. Công văn / Khung chương trình", type=['pdf','docx','doc'], key='cv')

with col2:
    uploaded_template = st.file_uploader("3. Mẫu đề kiểm tra (Format)", type=['pdf','docx','doc'], key='tpl')
    instruction = st.text_area("Yêu cầu cụ thể (Số câu, tỉ lệ, mức độ...)", 
                               value="Tạo ma trận 21 câu (Trắc nghiệm 5đ, Tự luận 5đ). Tỉ lệ NB/TH/VD: 40/30/30.", 
                               height=120)

if st.button("🚀 TẠO MA TRẬN & ĐỀ", type="primary"):
    if not uploaded_textbook or not uploaded_official or not uploaded_template:
        st.error("⚠️ Vui lòng tải lên đủ 3 file: SGK, Công văn, Mẫu đề.")
    else:
        with st.status("Đang xử lý...", expanded=True) as status:
            st.write("📖 Đang đọc nội dung file...")
            tb_mime, tb_text = extract_text_from_file(uploaded_textbook)
            cv_mime, cv_text = extract_text_from_file(uploaded_official)
            tpl_mime, tpl_text = extract_text_from_file(uploaded_template)
            
            st.write(f"✅ Đã đọc xong: SGK ({len(tb_text)} ký tự), Công văn ({len(cv_text)} ký tự).")
            
            st.write("🤖 Đang gửi dữ liệu cho AI phân tích và sinh đề...")
            try:
                result = call_openai_generate_matrix_and_exam(tb_text, cv_text, tpl_text, instruction)
                status.update(label="Hoàn tất!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="Gặp lỗi!", state="error")
                st.error(f"Lỗi trong quá trình xử lý: {e}")
                st.stop()

        # Validate result
        matrix_html = result.get("matrixHtml") or result.get("matrix") or ""
        exam_html = result.get("examHtml") or result.get("exam") or ""

        if not matrix_html and not exam_html:
            st.error("AI không trả về kết quả đúng định dạng.")
            with st.expander("Xem dữ liệu trả về từ AI"):
                st.write(result)
            st.stop()

        # Hiển thị kết quả
        tab1, tab2 = st.tabs(["📊 Ma trận", "📝 Đề kiểm tra"])
        
        with tab1:
            st.markdown(matrix_html, unsafe_allow_html=True)
            st.download_button("📥 Tải HTML Ma trận", matrix_html, "matran.html", "text/html")
            
        with tab2:
            st.markdown(exam_html, unsafe_allow_html=True)
            st.download_button("📥 Tải HTML Đề", exam_html, "de_kiem_tra.html", "text/html")

        # Tải DOCX chung
        docx_bytes = make_docx_from_htmls(matrix_html, exam_html)
        st.markdown("---")
        st.download_button(
            label="📥 TẢI VỀ FILE WORD (.DOCX)",
            data=docx_bytes,
            file_name="De_Kiem_Tra_AI_Generated.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary"
        )
