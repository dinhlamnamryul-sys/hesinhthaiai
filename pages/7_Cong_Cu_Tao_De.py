import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import docx  # dùng để đọc file .docx

st.set_page_config(page_title="Tạo đề tự động từ ma trận", page_icon="📝", layout="wide")

st.title("📝 Tạo đề kiểm tra tự động từ ma trận")

st.markdown("""
### Hướng dẫn:
- Bạn có thể tải lên **Excel (.xlsx)** hoặc **Word (.docx)** với cấu trúc ma trận sau:
   - ChuDe  
   - NoiDung  
   - MucDo  
   - SoCau  

Hệ thống sẽ tự động đọc & sinh đề theo đúng số lượng câu trong ma trận.
---
""")


# ==========================================================
# HÀM ĐỌC MA TRẬN TỪ WORD
# ==========================================================

def read_matrix_from_docx(file):
    doc = docx.Document(file)

    data = []
    table = doc.tables[0]  # lấy bảng đầu tiên

    keys = None

    for i, row in enumerate(table.rows):
        text = [cell.text.strip() for cell in row.cells]

        if i == 0:
            keys = text  # dòng tiêu đề
        else:
            item = {keys[j]: text[j] for j in range(len(keys))}
            data.append(item)

    return pd.DataFrame(data)


# ==========================================================
# UPLOAD FILE MA TRẬN
# ==========================================================

uploaded_matrix = st.file_uploader("📤 Tải lên ma trận (Excel hoặc Word)", type=["xlsx", "docx"])

if uploaded_matrix:

    # Đọc file Excel
    if uploaded_matrix.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_matrix)

    # Đọc file Word
    elif uploaded_matrix.name.endswith(".docx"):
        df = read_matrix_from_docx(uploaded_matrix)

    st.success("Đã tải ma trận thành công!")
    st.dataframe(df)

    # Kiểm tra đủ cột không
    required_cols = ["ChuDe", "NoiDung", "MucDo", "SoCau"]
    if not all(col in df.columns for col in required_cols):
        st.error("❌ File ma trận thiếu cột! Cần có: ChuDe, NoiDung, MucDo, SoCau")
    else:
        st.info("➡ Nhấn nút để tạo đề theo ma trận.")

        if st.button("📘 Tạo đề tự động"):
            st.success("Đã tạo đề!")

            # ==========================================================
            # 2. TẠO ĐỀ KIỂM TRA
            # ==========================================================
            questions = []
            question_number = 1

            for _, row in df.iterrows():
                chu_de = row["ChuDe"]
                nd = row["NoiDung"]
                md = row["MucDo"]
                so_cau = int(row["SoCau"])

                for i in range(so_cau):
                    cau = (
                        f"Câu {question_number}. ({md}) – Chủ đề **{chu_de}**\n"
                        f"Nội dung: {nd}\n"
                        f"→ Hãy trình bày câu trả lời."
                    )
                    questions.append(cau)
                    question_number += 1

            # Hiển thị đề trong giao diện
            st.subheader("📄 Đề kiểm tra được tạo:")
            for q in questions:
                st.markdown(q)
                st.markdown("---")

            # ==========================================================
            # 3. XUẤT WORD
            # ==========================================================
            doc = Document()
            doc.add_heading("ĐỀ KIỂM TRA TỰ ĐỘNG", 0)

            for q in questions:
                doc.add_paragraph(q)
                doc.add_paragraph(".................................................")
                doc.add_paragraph("")

            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            st.download_button(
                label="📥 Tải xuống file Word",
                data=buffer,
                file_name="De_Kiem_Tra_Tu_Dong.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
