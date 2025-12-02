import streamlit as st
import pandas as pd
from docx import Document

# ==================== CẤU HÌNH GIAO DIỆN ====================
st.set_page_config(
    page_title="Công Cụ Tạo Đề Kiểm Tra Tự Động",
    page_icon="📝",
    layout="wide"
)

# ======== HÀM ĐỌC BẢNG TRONG FILE WORD (.docx) ========
def read_word_table(uploaded_file):
    doc = Document(uploaded_file)
    table = doc.tables[0]  # Lấy bảng đầu tiên trong file
    
    data = []
    keys = None

    for i, row in enumerate(table.rows):
        text = [cell.text.strip() for cell in row.cells]

        if i == 0:
            keys = text   # dòng đầu = tiêu đề
        else:
            data.append(text)

    df = pd.DataFrame(data, columns=keys)
    return df

# ==================== APP ====================
def main():

    st.title("📝 HỆ THỐNG TẠO ĐỀ KIỂM TRA TỰ ĐỘNG DỰA TRÊN MA TRẬN")
    st.caption("Dùng file Word hoặc Excel chứa ma trận để AI tự tạo đề chuẩn TT22 – 7991.")

    st.divider()

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.header("⚙️ Thiết lập đề kiểm tra")

        subject = st.text_input("📘 Môn học", "Toán học")
        grade = st.selectbox("🎓 Khối lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"])
        time = st.selectbox("⏱ Thời gian làm bài", ["15 phút", "45 phút", "60 phút", "90 phút"])
        exam_name = st.text_input("📌 Tên bài kiểm tra", "Kiểm tra giữa học kỳ II")

        st.subheader("📥 Tải lên ma trận")
        uploaded_file = st.file_uploader(
            "Chọn file ma trận (.doc, .docx, .xlsx, .csv)", 
            type=["doc", "docx", "xlsx", "xls", "csv"]
        )

    # ---------------- MAIN CONTENT ----------------
    if uploaded_file is None:
        st.warning("📌 Vui lòng tải lên file chứa ma trận đề để tiếp tục.")
        return

    # ---------------- ĐỌC FILE MA TRẬN ----------------
    try:
        if uploaded_file.name.endswith((".doc", ".docx")):
            df = read_word_table(uploaded_file)

        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

    except Exception as e:
        st.error(f"❌ Lỗi: Không thể đọc file.\nChi tiết: {e}")
        return

    st.success("✅ Đã tải và đọc ma trận thành công!")
    st.write("### 📊 Ma trận đề (từ file):")
    st.dataframe(df, use_container_width=True)

    # ================== TẠO PROMPTS ===================
    matrix_prompt = f"""
Bạn là chuyên gia xây dựng đề kiểm tra chuẩn 7991 & Thông tư 22.
Tôi đang tạo đề môn **{subject}**, **{grade}**, thời gian **{time}**, tên đề: **{exam_name}**.

Đây là ma trận đề kiểm tra (bảng đã được trích xuất từ file Word/Excel):

{df.to_markdown(index=False)}

➡️ Hãy phân tích ma trận trên và tóm tắt:
- Mạch kiến thức
- Mức độ (NB – TH – VD – VDC)
- Số câu – điểm – tỉ lệ %
"""

    generate_prompt = f"""
Dựa vào ma trận đề tôi đã gửi, hãy tạo đầy đủ đề kiểm tra môn {subject}, {grade}:

Yêu cầu:
- Số câu và mức độ phải theo đúng ma trận.
- Có trắc nghiệm + tự luận (nếu ma trận có).
- Ghi rõ mức độ nhận thức mỗi câu.
- Viết đáp án chi tiết + thang điểm tự luận.
"""

    eval_prompt = """
Hãy phân tích độ khó – độ phân hóa – năng lực đánh giá theo ma trận Bloom của đề vừa sinh.
"""

    reversion_prompt = """
Hãy tạo mã đề số 2 (Đề B):
- Giữ nguyên cấu trúc ma trận
- Đổi dữ kiện + bối cảnh
- Không trùng câu hoặc đáp án
"""

    export_prompt = """
Hãy trình bày đề và đáp án đẹp, chuẩn để tôi copy vào Word.
"""

    # ================== TABS ===================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📌 1. Phân tích Ma Trận",
        "📝 2. Sinh Đề",
        "📊 3. Đánh Giá",
        "🔄 4. Đề Số 2",
        "📤 5. Xuất Word"
    ])

    with tab1:
        st.code(matrix_prompt, language="markdown")

    with tab2:
        st.code(generate_prompt, language="markdown")

    with tab3:
        st.code(eval_prompt, language="markdown")

    with tab4:
        st.code(reversion_prompt, language="markdown")

    with tab5:
        st.code(export_prompt, language="markdown")

    st.divider()
    st.caption("© 2025 Hệ thống hỗ trợ giáo viên tạo đề – PTDTBT TH&THCS NA Ư")

# RUN
if __name__ == "__main__":
    main()
