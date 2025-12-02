import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO

st.set_page_config(page_title="Tạo đề tự động từ ma trận", page_icon="📝", layout="wide")

st.title("📝 Tạo đề kiểm tra tự động từ ma trận")

st.markdown("""
### Hướng dẫn:
1. Tải lên file **Excel ma trận** (file phải có các cột sau):
   - *ChuDe* – Tên chủ đề  
   - *NoiDung* – Nội dung trọng tâm  
   - *MucDo* – Nhận biết / Thông hiểu / Vận dụng thấp / Vận dụng cao  
   - *SoCau* – Số lượng câu cần sinh  

2. Hệ thống sẽ tự tạo đề dựa theo số lượng câu trong từng chủ đề.

--- 
""")


# ==========================================================
# 1. TẢI FILE MA TRẬN
# ==========================================================

uploaded_matrix = st.file_uploader("📤 Tải lên file Excel ma trận", type=["xlsx"])

if uploaded_matrix:
    df = pd.read_excel(uploaded_matrix)
    st.success("Đã tải ma trận thành công!")
    st.dataframe(df)

    # Kiểm tra cột
    required_cols = ["ChuDe", "NoiDung", "MucDo", "SoCau"]
    if not all(col in df.columns for col in required_cols):
        st.error("❌ File Excel thiếu cột cần thiết! Phải có: ChuDe, NoiDung, MucDo, SoCau")
    else:
        st.info("➡ Nhấn nút bên dưới để tạo đề theo ma trận.")

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
                    cau = f"Câu {question_number}. ({md}) – Thuộc chủ đề **{chu_de}**\nNội dung: {nd}\n→ Hãy trình bày câu trả lời của bạn."
                    questions.append(cau)
                    question_number += 1

            # Hiển thị đề trong trang
            st.subheader("📄 Đề kiểm tra được tạo:")
            for q in questions:
                st.markdown(q)
                st.markdown("---")

            # ==========================================================
            # 3. XUẤT FILE WORD
            # ==========================================================
            doc = Document()
            doc.add_heading("ĐỀ KIỂM TRA TỰ ĐỘNG", 0)

            for q in questions:
                doc.add_paragraph(q)
                doc.add_paragraph("..............................................................")
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
