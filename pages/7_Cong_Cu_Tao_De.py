import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import docx

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
    # Nếu có nhiều bảng, lấy bảng đầu tiên
    table = doc.tables[0]
    data = []
    keys = [cell.text.strip() for cell in table.rows[0].cells]
    for row in table.rows[1:]:
        item = {keys[i]: row.cells[i].text.strip() for i in range(len(keys))}
        data.append(item)
    return pd.DataFrame(data)

# -------------------- UPLOAD FILE --------------------
uploaded_matrix = st.file_uploader("📤 Tải lên ma trận (Excel hoặc Word)", type=["xlsx", "docx"])

if uploaded_matrix:
    if uploaded_matrix.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_matrix)
    elif uploaded_matrix.name.endswith(".docx"):
        df = read_matrix_from_docx(uploaded_matrix)

    df = normalize_columns(df)
    st.write("📋 Bảng ma trận sau khi chuẩn hóa cột:")
    st.dataframe(df)

    # Kiểm tra các cột quan trọng
    required_cols = ["ChuDe", "NoiDung", "MucDo", "SoCau"]
    missing_cols = [c for c in required_cols if c not in df.columns]

    # Nếu thiếu cột, cho người dùng chọn cột thay thế
    col_selection = {}
    if missing_cols:
        st.warning(f"❌ Không tìm thấy các cột chuẩn: {missing_cols}")
        for col in missing_cols:
            col_selection[col] = st.selectbox(f"Chọn cột thay thế cho '{col}'", df.columns, key=col)
        # Đổi tên các cột do người dùng chọn
        df = df.rename(columns=col_selection)
        missing_cols = [c for c in required_cols if c not in df.columns]

    if not missing_cols:
        if st.button("📘 Tạo đề tự động"):
            st.success("Đã tạo đề!")
            questions = []
            q_number = 1
            for _, row in df.iterrows():
                chu_de = row.get("ChuDe", "Chưa xác định")
                nd = row.get("NoiDung", "Chưa xác định")
                md = row.get("MucDo", "")
                # Chuyển số câu về dạng int, nếu lỗi thì mặc định 1
                try:
                    so_cau = int(float(row.get("SoCau", 1)))
                except:
                    so_cau = 1
                for i in range(so_cau):
                    q_text = f"Câu {q_number}. ({md}) – Chủ đề {chu_de}\nNội dung: {nd}\n→ Hãy trình bày câu trả lời."
                    questions.append(q_text)
                    q_number += 1

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
