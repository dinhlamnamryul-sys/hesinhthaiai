import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import docx
import re

st.set_page_config(page_title="Tạo đề tự động từ ma trận", page_icon="📝", layout="wide")
st.title("📝 Tạo đề kiểm tra tự động từ ma trận (tự nhận diện cột)")

st.markdown("""
Upload Excel (.xlsx) hoặc Word (.docx). Hệ thống sẽ cố gắng tự động nhận diện các cột:
- Chủ đề
- Nội dung
- Mức độ
- Số câu
""")

# -------------------- HÀM CHUẨN HÓA CỘT --------------------
def normalize_columns(df):
    col_map = {}
    for col in df.columns:
        lc = col.lower()
        if "chủ đề" in lc or "chude" in lc or "topic" in lc:
            col_map[col] = "ChuDe"
        elif "nội dung" in lc or "noidung" in lc or "content" in lc:
            col_map[col] = "NoiDung"
        elif "mức độ" in lc or "level" in lc or "mucdo" in lc:
            col_map[col] = "MucDo"
        elif "số câu" in lc or "socau" in lc or "num" in lc or "quantity" in lc:
            col_map[col] = "SoCau"
        else:
            col_map[col] = col
    df = df.rename(columns=col_map)
    return df

# -------------------- HÀM ĐỌC WORD --------------------
def read_matrix_from_docx(file):
    doc = docx.Document(file)
    data = []
    table_found = False

    for table in doc.tables:
        if len(table.rows) < 2:
            continue  # Bỏ qua bảng không có dữ liệu
        keys = [cell.text.strip() for cell in table.rows[0].cells]
        if all(not k for k in keys):
            continue
        for row in table.rows[1:]:
            item = {}
            for i, key in enumerate(keys):
                try:
                    item[key] = row.cells[i].text.strip()
                except IndexError:
                    item[key] = ""
            data.append(item)
        table_found = True
        break  # Lấy bảng đầu tiên hợp lệ

    if not table_found:
        return pd.DataFrame()
    return pd.DataFrame(data)

# -------------------- TỰ ĐỘNG XỬ LÝ CỘT THIẾU --------------------
def auto_fill_missing_columns(df):
    # Cột quan trọng
    required_cols = ["ChuDe", "NoiDung", "MucDo", "SoCau"]
    missing_cols = [c for c in required_cols if c not in df.columns]

    for col in missing_cols:
        if col == "SoCau":
            df[col] = 1
        else:
            df[col] = "Chưa xác định"
    return df

# -------------------- XỬ LÝ FILE UPLOAD --------------------
uploaded_matrix = st.file_uploader("📤 Tải lên ma trận (Excel hoặc Word)", type=["xlsx", "docx"])

if uploaded_matrix:
    df = pd.DataFrame()
    if uploaded_matrix.name.endswith(".xlsx"):
        try:
            df = pd.read_excel(uploaded_matrix, sheet_name=0)
        except:
            st.error("❌ Không đọc được file Excel!")
    elif uploaded_matrix.name.endswith(".docx"):
        try:
            df = read_matrix_from_docx(uploaded_matrix)
        except:
            st.error("❌ Không đọc được file Word!")

    if df.empty:
        st.error("❌ File không chứa dữ liệu hợp lệ!")
    else:
        df = normalize_columns(df)
        df = auto_fill_missing_columns(df)
        st.write("📋 Bảng ma trận sau khi chuẩn hóa và tự động điền cột:")
        st.dataframe(df)

        if st.button("📘 Tạo đề tự động"):
            st.success("✅ Đã tạo đề!")
            questions = []
            q_number = 1
            for _, row in df.iterrows():
                chu_de = row.get("ChuDe", "Chưa xác định")
                nd = row.get("NoiDung", "Chưa xác định")
                md = row.get("MucDo", "")
                try:
                    so_cau = int(float(row.get("SoCau", 1)))
                except:
                    so_cau = 1
                for i in range(so_cau):
                    q_text = f"Câu {q_number}. ({md}) – Chủ đề {chu_de}\nNội dung: {nd}\n→ Hãy trình bày câu trả lời."
                    questions.append(q_text)
                    q_number += 1

            # Hiển thị đề
            st.subheader("📄 Đề kiểm tra:")
            for q in questions:
                st.markdown(q)
                st.markdown("---")

            # Xuất Word
            doc = Document()
            doc.add_heading("ĐỀ KIỂM TRA TỰ ĐỘNG", 0)
            for q in questions:
                doc.add_paragraph(q)
                doc.add_paragraph("..............................................")
                doc.add_paragraph("")
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            st.download_button(
                "📥 Tải xuống file Word",
                data=buffer,
                file_name="De_Kiem_Tra_Tu_Dong.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
