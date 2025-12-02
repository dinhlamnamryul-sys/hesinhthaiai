import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import docx

st.set_page_config(page_title="Tạo đề tự động theo SGK KNTT", page_icon="📝", layout="wide")
st.title("📝 Tạo đề kiểm tra tự động (theo SGK Kết nối tri thức)")

st.markdown("""
Upload Excel (.xlsx) hoặc Word (.docx) chứa ma trận câu hỏi. 
Hệ thống sẽ tự động nhận diện cột và cho phép:
- Chọn môn, chương, bài, chủ đề
- Chọn tổng số câu, tỉ lệ câu theo chủ đề
- Tạo đề theo CV7791
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
        elif "môn" in lc or "subject" in lc:
            col_map[col] = "Mon"
        elif "chương" in lc or "chapter" in lc:
            col_map[col] = "Chuong"
        elif "bài" in lc or "lesson" in lc:
            col_map[col] = "Bai"
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
            continue
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
        break
    if not table_found:
        return pd.DataFrame()
    return pd.DataFrame(data)

# -------------------- TỰ ĐỘNG THÊM CỘT THIẾU --------------------
def auto_fill_missing_columns(df):
    required_cols = ["Mon", "Chuong", "Bai", "ChuDe", "NoiDung", "MucDo", "SoCau"]
    for col in required_cols:
        if col not in df.columns:
            if col == "SoCau":
                df[col] = 1
            else:
                df[col] = "Chưa xác định"
    return df

# -------------------- FILE UPLOAD --------------------
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
        st.write("📋 Ma trận sau khi chuẩn hóa:")
        st.dataframe(df)

        # -------------------- CHỌN MÔN / CHƯƠNG / BÀI / CHỦ ĐỀ --------------------
        mon_list = sorted(df['Mon'].unique())
        mon = st.selectbox("Chọn môn học:", mon_list)

        chuong_list = sorted(df[df['Mon']==mon]['Chuong'].unique())
        chuong = st.selectbox("Chọn chương:", chuong_list)

        bai_list = sorted(df[(df['Mon']==mon) & (df['Chuong']==chuong)]['Bai'].unique())
        bai = st.selectbox("Chọn bài:", bai_list)

        chu_de_list = sorted(df[(df['Mon']==mon) & (df['Chuong']==chuong) & (df['Bai']==bai)]['ChuDe'].unique())
        chu_de = st.multiselect("Chọn chủ đề (có thể nhiều):", chu_de_list, default=chu_de_list)

        so_cau_total = st.number_input("Tổng số câu muốn tạo:", min_value=1, max_value=100, value=10)

        st.markdown("**Tỉ lệ câu theo chủ đề (%)**")
        ti_le_dict = {}
        for cd in chu_de:
            ti_le_dict[cd] = st.slider(f"{cd} (%)", min_value=0, max_value=100, value=round(100/len(chu_de)))

        if st.button("📘 Tạo đề tự động"):
            df_filtered = df[(df['Mon']==mon) & (df['Chuong']==chuong) & (df['Bai']==bai) & (df['ChuDe'].isin(chu_de))]
            questions = []
            q_number = 1

            # Sinh câu theo tỉ lệ
            for cd in chu_de:
                n_cau = round(so_cau_total * ti_le_dict[cd] / 100)
                df_cd = df_filtered[df_filtered['ChuDe']==cd]
                for _, row in df_cd.iterrows():
                    so_cau_row = int(float(row.get("SoCau", 1)))
                    for i in range(min(so_cau_row, n_cau)):
                        q_text = f"Câu {q_number}. ({row.get('MucDo','')}) – Chủ đề {cd}\nNội dung: {row.get('NoiDung','')}\n→ Hãy trình bày câu trả lời."
                        questions.append(q_text)
                        q_number += 1
                        n_cau -= 1
                        if n_cau <= 0:
                            break
                    if n_cau <= 0:
                        break

            # Hiển thị đề
            st.subheader("📄 Đề kiểm tra:")
            for q in questions:
                st.markdown(q)
                st.markdown("---")

            # Xuất Word
            doc = Document()
            doc.add_heading(f"ĐỀ KIỂM TRA: {mon} - {chuong} - {bai}", 0)
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
                file_name=f"De_Kiem_Tra_{mon}_{chuong}_{bai}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
