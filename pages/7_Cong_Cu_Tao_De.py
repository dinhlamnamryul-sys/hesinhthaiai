# Creating the advanced Streamlit app file and saving it to /mnt/data/7_Cong_Cu_Tao_De_Advanced.py
content = r'''
import streamlit as st
import pandas as pd
import json
import io
import os
from datetime import datetime
from docx import Document
from docx.shared import Pt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Công Cụ Tạo Đề (Nâng Cao)", page_icon="📝", layout="wide")

APP_TITLE = "📝 HỆ THỐNG TẠO ĐỀ KIỂM TRA TỰ ĐỘNG (BẢN NÂNG CAO)"
HISTORY_FILE = "/mnt/data/exam_history.json"
OUTPUT_DIR = "/mnt/data/generated_exams"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------- HELPERS --------------------
def read_word_table(uploaded_file):
    try:
        doc = Document(uploaded_file)
    except Exception as e:
        raise
    if len(doc.tables) == 0:
        raise ValueError("Không tìm thấy bảng trong file Word.")
    table = doc.tables[0]
    data = []
    keys = None
    for i, row in enumerate(table.rows):
        text = [cell.text.strip() for cell in row.cells]
        if i == 0:
            keys = text
        else:
            data.append(text)
    df = pd.DataFrame(data, columns=keys)
    return df

def normalize_columns(df):
    # Map common Vietnamese/English variants to canonical columns
    mapping = {}
    lower_cols = [c.lower() for c in df.columns]
    for c in df.columns:
        lc = c.lower()
        if lc in ["nội dung", "noidung", "mạch kiến thức", "mạch", "content", "topic"]:
            mapping[c] = "Content"
        elif lc in ["mức độ", "mucdo", "độ khó", "level", "level/bloom"]:
            mapping[c] = "Level"
        elif lc in ["số câu", "socau", "num", "num_questions", "questions"]:
            mapping[c] = "NumQ"
        elif lc in ["điểm", "score", "points"]:
            mapping[c] = "Points"
        elif lc in ["ghi chú", "note", "notes"]:
            mapping[c] = "Note"
        else:
            mapping[c] = c  # keep original if not matched
    df = df.rename(columns=mapping)
    return df

def required_columns_ok(df):
    return any(c in df.columns for c in ["Content"]) and any(c in df.columns for c in ["Level"]) and any(c in df.columns for c in ["NumQ"])

def parse_level(text):
    if not isinstance(text, str):
        return "NB"
    t = text.strip().lower()
    if t in ["nb", "nhận biết", "nhan biet", "nhanbiet"]:
        return "NB"
    if t in ["th", "thông hiểu", "thong hieu", "thonghieu"]:
        return "TH"
    if t in ["vd", "vận dụng", "van dung", "vandung"]:
        return "VD"
    if t in ["vdc", "vận dụng cao", "van dung cao", "vandungcao"]:
        return "VDC"
    # fallback heuristics
    if "nhận" in t or "biết" in t:
        return "NB"
    if "hiểu" in t:
        return "TH"
    if "cao" in t or "phân hóa" in t:
        return "VDC"
    return "VD"

# Simple question generators (placeholder templates)
def gen_mcq(content_text, idx, level):
    stem = f"{idx}. (TN) Cho nội dung: {content_text}\nHãy chọn đáp án đúng."
    # simple templated options using numbers as variables
    option_a = "A. Giá trị 1"
    option_b = "B. Giá trị 2"
    option_c = "C. Giá trị 3"
    option_d = "D. Giá trị 4"
    answer = "A"
    explanation = "Giải thích ngắn: dựa trên kiến thức cơ bản của nội dung."
    return {"q": stem, "type": "MCQ", "options": [option_a, option_b, option_c, option_d], "answer": answer, "explanation": explanation, "level": level}

def gen_short_answer(content_text, idx, level):
    q = f"{idx}. (TL) {content_text}\nYêu cầu: Trình bày ngắn gọn."
    answer = "Ý chính trả lời: ... (GV bổ sung chi tiết)"
    rubric = [
        {"criteria": "Nêu đúng ý chính", "points": 2},
        {"criteria": "Trình bày rõ ràng", "points": 1}
    ]
    return {"q": q, "type": "SA", "answer": answer, "rubric": rubric, "level": level}

def gen_problem(content_text, idx, level):
    q = f"{idx}. (TL) Bài toán/ứng dụng: {content_text}\nYêu cầu: Giải và nêu kết luận."
    answer = "Hướng giải và kết luận: ... (GV chi tiết hóa)"
    rubric = [
        {"criteria": "Phương pháp đúng", "points": 3},
        {"criteria": "Tính toán chính xác", "points": 2},
        {"criteria": "Kết luận rõ ràng", "points": 1}
    ]
    return {"q": q, "type": "PROB", "answer": answer, "rubric": rubric, "level": level}

def create_exam_from_matrix(df, subject, grade, exam_name, time_allowed):
    questions = []
    idx = 1
    for _, row in df.iterrows():
        content = str(row.get("Content", "")).strip()
        level = parse_level(row.get("Level", ""))
        try:
            numq = int(float(row.get("NumQ", 1)))
        except:
            numq = 1
        # distribute question types based on level
        for i in range(numq):
            if level == "NB":
                q = gen_mcq(content, idx, level)
            elif level == "TH":
                q = gen_mcq(content, idx, level)
            elif level == "VD":
                q = gen_problem(content, idx, level)
            elif level == "VDC":
                q = gen_problem(content, idx, level)
            else:
                q = gen_short_answer(content, idx, level)
            questions.append(q)
            idx += 1
    return questions

def exam_to_docx(exam_meta, questions, out_path):
    doc = Document()
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    doc.add_heading(exam_meta.get("title", "ĐỀ KIỂM TRA"), level=1)
    doc.add_paragraph(f"Môn: {exam_meta.get('subject')}    Lớp: {exam_meta.get('grade')}    Thời gian: {exam_meta.get('time')}")
    doc.add_paragraph("")

    doc.add_heading("I. Phần câu hỏi", level=2)
    for q in questions:
        p = doc.add_paragraph(q["q"])
        if q["type"] == "MCQ":
            for opt in q["options"]:
                doc.add_paragraph(opt, style='List Bullet')
        doc.add_paragraph("")

    doc.add_page_break()
    doc.add_heading("II. Đáp án & Rubric", level=2)
    for i, q in enumerate(questions, start=1):
        doc.add_paragraph(f"{i}. Loại: {q.get('type')}    Mức độ: {q.get('level')}")
        if q["type"] == "MCQ":
            doc.add_paragraph(f"Đáp án: {q.get('answer')}")
            doc.add_paragraph(f"Giải thích: {q.get('explanation')}")
        else:
            doc.add_paragraph("Đáp án mẫu:")
            doc.add_paragraph(q.get("answer", ""))
            rubric = q.get("rubric", [])
            if rubric:
                doc.add_paragraph("Rubric chấm điểm:")
                for r in rubric:
                    doc.add_paragraph(f"- {r['criteria']}: {r['points']} điểm")
        doc.add_paragraph("")
    doc.save(out_path)
    return out_path

def exam_to_pdf(exam_meta, questions, out_path):
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    y = height - margin
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, exam_meta.get("title", "ĐỀ KIỂM TRA"))
    y -= 16
    c.setFont("Helvetica", 11)
    c.drawString(margin, y, f"Môn: {exam_meta.get('subject')}    Lớp: {exam_meta.get('grade')}    Thời gian: {exam_meta.get('time')}")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "I. Phần câu hỏi")
    y -= 16
    c.setFont("Helvetica", 10)
    for q in questions:
        text = q["q"]
        for line in text.split("\n"):
            if y < margin:
                c.showPage()
                y = height - margin
            c.drawString(margin, y, line[:1000])
            y -= 12
        if q["type"] == "MCQ":
            for opt in q["options"]:
                if y < margin:
                    c.showPage()
                    y = height - margin
                c.drawString(margin + 10, y, opt)
                y -= 12
        y -= 8

    c.showPage()
    y = height - margin
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "II. Đáp án & Rubric")
    y -= 16
    c.setFont("Helvetica", 10)
    for i, q in enumerate(questions, start=1):
        lines = []
        if q["type"] == "MCQ":
            lines.append(f"{i}. Đáp án: {q.get('answer')}. Giải thích: {q.get('explanation')}")
        else:
            lines.append(f"{i}. Đáp án mẫu: {q.get('answer')}")
            if q.get("rubric"):
                for r in q.get("rubric"):
                    lines.append(f"- {r['criteria']}: {r['points']} điểm")
        for line in lines:
            if y < margin:
                c.showPage()
                y = height - margin
            c.drawString(margin, y, line[:1000])
            y -= 12
        y -= 8
    c.save()
    return out_path

def save_history(meta, docx_path, pdf_path):
    record = {
        "timestamp": datetime.now().isoformat(),
        "title": meta.get("title"),
        "subject": meta.get("subject"),
        "grade": meta.get("grade"),
        "time": meta.get("time"),
        "docx": docx_path,
        "pdf": pdf_path
    }
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    history.insert(0, record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return record

# -------------------- STREAMLIT UI --------------------
def main():
    st.title(APP_TITLE)
    st.write("Phiên bản Nâng Cao — upload ma trận (.docx/.xlsx/.csv) → hệ thống tự sinh đề, đáp án, xuất Word/PDF và lưu lịch sử.")

    with st.sidebar:
        st.header("Thiết lập")
        subject = st.text_input("Môn", value="Toán học")
        grade = st.selectbox("Khối lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"])
        time_allowed = st.selectbox("Thời gian làm bài", ["15 phút", "45 phút", "60 phút", "90 phút"])
        exam_name = st.text_input("Tên đề", value="Kiểm tra nhanh")
        uploaded = st.file_uploader("Upload ma trận (.docx/.xlsx/.csv)", type=["doc", "docx", "xlsx", "xls", "csv"])

    if uploaded is None:
        st.info("Vui lòng upload file ma trận (file có bảng chứa ít nhất các cột: Nội dung | Mức độ | Số câu).")
        return

    # Read uploaded file
    try:
        if uploaded.name.lower().endswith((".doc", ".docx")):
            df = read_word_table(uploaded)
        elif uploaded.name.lower().endswith(".csv"):
            uploaded.seek(0)
            df = pd.read_csv(uploaded)
        else:
            uploaded.seek(0)
            df = pd.read_excel(uploaded)
    except Exception as e:
        st.error(f"Không thể đọc file. Chi tiết: {e}")
        return

    # Normalize columns and validate
    df = normalize_columns(df)
    st.write("📋 Bảng ma trận đã trích xuất:")
    st.dataframe(df, use_container_width=True)

    if not required_columns_ok(df):
        st.error("File ma trận thiếu cột bắt buộc. Vui lòng đảm bảo có các cột: Nội dung (Content), Mức độ (Level), Số câu (NumQ).")
        return

    # Controls for generation
    st.markdown("---")
    st.subheader("Tùy chọn sinh đề")
    opt_shuffle = st.checkbox("Xáo câu hỏi (shuffle)", value=False)
    opt_generate = st.button("🔵 Tạo đề ngay")

    if not opt_generate:
        st.info("Nhấn 'Tạo đề ngay' để hệ thống sinh đề từ ma trận.")
        return

    # Generate exam
    with st.spinner("Đang sinh đề..."):
        try:
            questions = create_exam_from_matrix(df, subject, grade, exam_name, time_allowed)
            if opt_shuffle:
                import random
                random.shuffle(questions)
        except Exception as e:
            st.error(f"Lỗi khi sinh đề: {e}")
            return

    st.success(f"Đã sinh xong: {len(questions)} câu hỏi.")
    # Display preview
    st.write("### 🔍 Xem trước đề (văn bản)")
    preview_text = ""
    for q in questions:
        preview_text += q["q"] + "\n"
        if q["type"] == "MCQ":
            for opt in q["options"]:
                preview_text += "   " + opt + "\n"
        preview_text += "\n"
    st.text_area("Đề kiểm tra (preview)", value=preview_text, height=400)

    # Generate docx and pdf buttons
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = exam_name.replace(" ", "_")
    docx_path = os.path.join(OUTPUT_DIR, f"exam_{safe_title}_{ts}.docx")
    pdf_path = os.path.join(OUTPUT_DIR, f"exam_{safe_title}_{ts}.pdf")

    if st.button("💾 Xuất Word (.docx) và PDF (.pdf)"):
        try:
            meta = {"title": exam_name, "subject": subject, "grade": grade, "time": time_allowed}
            exam_to_docx(meta, questions, docx_path)
            exam_to_pdf(meta, questions, pdf_path)
            record = save_history(meta, docx_path, pdf_path)
            st.success("Đã xuất file Word và PDF thành công.")
            st.write("📁 File Word:", docx_path)
            st.write("📁 File PDF:", pdf_path)
            st.markdown(f"- [Tải file Word]({docx_path})")
            st.markdown(f"- [Tải file PDF]({pdf_path})")
        except Exception as e:
            st.error(f"Lỗi khi xuất file: {e}")

    # Show history
    st.markdown("---")
    st.subheader("Lịch sử đề đã sinh (gần đây)")
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    else:
        history = []

    if history:
        for rec in history[:10]:
            st.write(f"- {rec['timestamp']} | {rec['title']} | {rec['subject']} | {rec['grade']}")
            st.markdown(f"  - Word: `{rec.get('docx')}`  |  PDF: `{rec.get('pdf')}`")
    else:
        st.write("Chưa có lịch sử.")

if __name__ == '__main__':
    main()
'''

file_path = "/mnt/data/7_Cong_Cu_Tao_De_Advanced.py"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

file_path

