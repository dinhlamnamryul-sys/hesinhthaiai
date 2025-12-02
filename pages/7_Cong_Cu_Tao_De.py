import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import docx
import math

st.set_page_config(page_title="Tạo đề tự động theo SGK KNTT (CV 7991)", page_icon="📝", layout="wide")
st.title("📝 Tạo đề kiểm tra tự động theo CV 7991 (SGK Kết nối tri thức)")

st.markdown("""
Upload Excel (.xlsx) hoặc Word (.docx) chứa ma trận câu hỏi.
Hệ thống sẽ tự động nhận diện cột và cho phép:
- Chọn môn, chương, bài, chủ đề
- **Cấu hình tổng số câu và tỉ lệ phân bổ theo 4 mức độ nhận thức (CV 7991).**
- Tạo đề theo cấu trúc đã chọn.
""")

# -------------------- HÀM CHUẨN HÓA CỘT --------------------
def normalize_columns(df):
    """Chuẩn hóa tên cột của DataFrame để khớp với các trường yêu cầu."""
    col_map = {}
    for col in df.columns:
        lc = str(col).lower().strip()
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
    
    # Đảm bảo các cột quan trọng được xử lý
    df = df.rename(columns=col_map)
    return df

# -------------------- HÀM ĐỌC WORD --------------------
def read_matrix_from_docx(file):
    """Đọc ma trận từ bảng đầu tiên trong file Word DOCX."""
    doc = docx.Document(file)
    data = []
    table_found = False
    
    for table in doc.tables:
        if len(table.rows) < 2:
            continue
        
        # Lấy keys từ hàng đầu tiên, bỏ qua nếu hàng đầu tiên trống
        keys = [cell.text.strip() for cell in table.rows[0].cells]
        if all(not k for k in keys) or len(keys) < 2:
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
    """Thêm các cột bắt buộc nếu thiếu và điền giá trị mặc định."""
    required_cols = ["Mon", "Chuong", "Bai", "ChuDe", "NoiDung", "MucDo", "SoCau"]
    for col in required_cols:
        if col not in df.columns:
            if col == "SoCau":
                df[col] = 1 # Mặc định 1 câu
            elif col == "MucDo":
                df[col] = "Nhận biết" # Mức độ mặc định
            else:
                df[col] = "Chưa xác định"
    
    # Chuyển SoCau về dạng số (xử lý lỗi)
    def to_int(val):
        try:
            return int(float(str(val).strip()))
        except:
            return 1
            
    df['SoCau'] = df['SoCau'].apply(to_int)
    return df

# -------------------- FILE UPLOAD --------------------
uploaded_matrix = st.file_uploader("📤 Tải lên ma trận (Excel hoặc Word)", type=["xlsx", "docx"])

if uploaded_matrix:
    df = pd.DataFrame()
    if uploaded_matrix.name.endswith(".xlsx"):
        try:
            # Chỉ đọc Sheet 1
            df = pd.read_excel(uploaded_matrix, sheet_name=0)
        except Exception as e:
            st.error(f"❌ Không đọc được file Excel! Lỗi: {e}")
    elif uploaded_matrix.name.endswith(".docx"):
        try:
            df = read_matrix_from_docx(uploaded_matrix)
        except Exception as e:
            st.error(f"❌ Không đọc được file Word! Lỗi: {e}")

    if df.empty:
        st.error("❌ File không chứa dữ liệu hợp lệ hoặc không tìm thấy bảng!")
    else:
        df = normalize_columns(df)
        df = auto_fill_missing_columns(df)
        
        # Lọc bỏ các hàng có ChuDe, NoiDung, MucDo trống
        df = df[df['ChuDe'].astype(str).str.strip() != '']
        df = df[df['NoiDung'].astype(str).str.strip() != '']
        df = df[df['MucDo'].astype(str).str.strip() != '']

        if df.empty:
             st.error("❌ Ma trận sau khi chuẩn hóa không có dữ liệu để tạo đề (Kiểm tra lại cột Chủ đề, Nội dung, Mức độ không bị trống).")
        else:
            st.write("📋 Ma trận sau khi chuẩn hóa:")
            # Giới hạn hiển thị 
            st.dataframe(df[['Mon', 'Chuong', 'Bai', 'ChuDe', 'NoiDung', 'MucDo', 'SoCau']].head(100), use_container_width=True)

            # -------------------- CHỌN LỌC DỮ LIỆU ĐẦU VÀO --------------------
            col1, col2 = st.columns(2)
            with col1:
                mon_list = sorted(df['Mon'].unique())
                mon = st.selectbox("1. Chọn môn học:", mon_list)
                
                df_mon = df[df['Mon']==mon]
                chuong_list = sorted(df_mon['Chuong'].unique())
                chuong = st.selectbox("2. Chọn chương:", chuong_list)

            with col2:
                df_chuong = df_mon[df_mon['Chuong']==chuong]
                bai_list = sorted(df_chuong['Bai'].unique())
                bai = st.selectbox("3. Chọn bài:", bai_list)
                
                df_bai = df_chuong[df_chuong['Bai']==bai]
                chu_de_list = sorted(df_bai['ChuDe'].unique())
                chu_de = st.multiselect("4. Chọn Chủ đề (có thể nhiều):", chu_de_list, default=chu_de_list)

            # Lọc DataFrame theo lựa chọn
            df_filtered = df[(df['Mon']==mon) & 
                             (df['Chuong']==chuong) & 
                             (df['Bai']==bai) & 
                             (df['ChuDe'].isin(chu_de))].copy()

            # -------------------- THIẾT LẬP CV 7991 --------------------
            st.markdown("---")
            st.subheader("⚙️ Cấu hình đề kiểm tra theo CV 7991")
            
            so_cau_total = st.number_input("5. Tổng số câu muốn tạo:", min_value=1, max_value=100, value=20)
            
            st.markdown("**6. Tỉ lệ câu theo mức độ nhận thức (%)** (Tổng nên bằng 100%)")
            
            # Khởi tạo mặc định nếu chưa có
            if 'ti_le_muc_do' not in st.session_state:
                st.session_state.ti_le_muc_do = {
                    "Nhận biết": 30,
                    "Thông hiểu": 40,
                    "Vận dụng": 20,
                    "Vận dụng cao": 10
                }
            
            # Bố trí 4 cột cho 4 mức độ
            col_nb, col_th, col_vd, col_vdc = st.columns(4)
            
            with col_nb:
                st.session_state.ti_le_muc_do["Nhận biết"] = st.number_input("Nhận biết (%)", min_value=0, max_value=100, 
                                                                              value=st.session_state.ti_le_muc_do["Nhận biết"])
            with col_th:
                st.session_state.ti_le_muc_do["Thông hiểu"] = st.number_input("Thông hiểu (%)", min_value=0, max_value=100, 
                                                                               value=st.session_state.ti_le_muc_do["Thông hiểu"])
            with col_vd:
                st.session_state.ti_le_muc_do["Vận dụng"] = st.number_input("Vận dụng (%)", min_value=0, max_value=100, 
                                                                             value=st.session_state.ti_le_muc_do["Vận dụng"])
            with col_vdc:
                st.session_state.ti_le_muc_do["Vận dụng cao"] = st.number_input("Vận dụng cao (%)", min_value=0, max_value=100, 
                                                                                 value=st.session_state.ti_le_muc_do["Vận dụng cao"])

            total_percent = sum(st.session_state.ti_le_muc_do.values())
            st.info(f"Tổng tỉ lệ đã nhập: {total_percent}%. Hệ thống sẽ tự động chuẩn hóa.")
            
            if st.button("📘 Tạo đề tự động", use_container_width=True):
                if df_filtered.empty:
                    st.error("Không tìm thấy câu hỏi nào phù hợp với bộ lọc đã chọn.")
                else:
                    # 1. Chuẩn hóa tỉ lệ mức độ và tính số lượng câu cần
                    normalized_ti_le = {}
                    if total_percent == 0:
                        st.error("Tổng tỉ lệ mức độ không thể bằng 0%. Vui lòng nhập tỉ lệ.")
                        st.stop()
                        
                    for md, percent in st.session_state.ti_le_muc_do.items():
                        # Chuẩn hóa nếu tổng không phải 100
                        normalized_ti_le[md] = percent / total_percent 

                    required_q_by_level = {}
                    remaining_total_q = so_cau_total
                    
                    # Tính số câu cần cho mỗi mức độ (dùng round để làm tròn)
                    for i, (md, ratio) in enumerate(normalized_ti_le.items()):
                        if i < len(normalized_ti_le) - 1:
                            required_q = round(so_cau_total * ratio)
                            required_q_by_level[md] = required_q
                            remaining_total_q -= required_q
                        else:
                            # Gán phần còn lại cho mức độ cuối cùng để đảm bảo tổng đúng
                            required_q_by_level[md] = remaining_total_q

                    
                    questions = []
                    q_number = 1
                    
                    # 2. Bắt đầu sinh câu hỏi theo TỪNG MỨC ĐỘ
                    for md in ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]:
                        n_cau_level = required_q_by_level.get(md, 0)
                        if n_cau_level == 0:
                            continue

                        df_md = df_filtered[df_filtered['MucDo'].str.contains(md, case=False, na=False)].copy()
                        
                        if df_md.empty:
                            st.warning(f"Không có câu hỏi mức độ **{md}** trong ma trận. Bỏ qua.")
                            continue

                        # Tính tổng 'SoCau' có sẵn trong mức độ hiện tại
                        total_available_points = df_md['SoCau'].sum()
                        
                        if total_available_points == 0:
                            st.warning(f"Tổng số câu có sẵn cho mức độ **{md}** là 0. Bỏ qua.")
                            continue

                        # 3. Phân bổ n_cau_level cho các hàng (dựa trên tỷ trọng SoCau)
                        # Tính số câu cần lấy từ mỗi hàng (quy tắc bốc thăm theo tỷ lệ)
                        df_md['N_Needed'] = (df_md['SoCau'] / total_available_points) * n_cau_level
                        
                        # Làm tròn số câu cần
                        df_md['N_to_Take'] = df_md['N_Needed'].apply(lambda x: math.ceil(x))
                        
                        # Giới hạn số câu lấy không vượt quá số câu có sẵn (SoCau)
                        df_md['N_to_Take'] = df_md.apply(lambda row: min(row['N_to_Take'], row['SoCau']), axis=1)

                        # Giới hạn tổng số câu lấy không vượt quá n_cau_level (Nếu làm tròn quá lên)
                        current_total_take = df_md['N_to_Take'].sum()
                        if current_total_take > n_cau_level:
                            # Rút bớt ngẫu nhiên từ các hàng có N_to_Take > 0 cho đến khi tổng bằng n_cau_level
                            # Để đơn giản, ta sẽ chỉ lấy các hàng đầu tiên
                            rows_to_adjust = df_md[df_md['N_to_Take'] > 0].index.tolist()
                            
                            while df_md['N_to_Take'].sum() > n_cau_level and rows_to_adjust:
                                # Lấy hàng cuối cùng có thể rút
                                idx = rows_to_adjust.pop() 
                                df_md.loc[idx, 'N_to_Take'] -= 1
                                if df_md.loc[idx, 'N_to_Take'] == 0:
                                    rows_to_adjust.remove(idx) # Ngăn không cho rút tiếp

                        # 4. Tạo câu hỏi
                        for _, row in df_md.iterrows():
                            n_to_take = int(row['N_to_Take'])
                            for i in range(n_to_take):
                                # Tạo văn bản câu hỏi
                                q_text = (f"Câu {q_number}. ({row.get('MucDo')}) - Chủ đề: {row.get('ChuDe')}\n"
                                          f"Nội dung: {row.get('NoiDung')}\n"
                                          f"→ (Lưu ý: Bạn cần thay thế Nội dung này bằng câu hỏi trắc nghiệm/tự luận thực tế.)\n"
                                          f"→ Hãy trình bày câu trả lời.")
                                questions.append(q_text)
                                q_number += 1
                    
                    
                    # 5. Hiển thị đề
                    st.success(f"Đã tạo thành công {len(questions)} câu hỏi theo cấu trúc CV 7991!")
                    st.subheader("📄 Đề kiểm tra:")
                    
                    output_text = ""
                    for q in questions:
                        st.markdown(q)
                        st.markdown("---")
                        output_text += q + "\n" + "---" + "\n\n"

                    # 6. Xuất Word
                    doc = Document()
                    doc.add_heading(f"ĐỀ KIỂM TRA: {mon} - {chuong} - {bai}", 0)
                    
                    # Thêm bảng tóm tắt cấu trúc đề (Phần mềm đã tạo)
                    doc.add_paragraph("Cấu trúc đề kiểm tra (Phần mềm đã tạo):")
                    table_summary = doc.add_table(rows=1, cols=3)
                    table_summary.style = 'Table Grid'
                    hdr_cells = table_summary.rows[0].cells
                    hdr_cells[0].text = 'Mức độ'
                    hdr_cells[1].text = 'Tỉ lệ mục tiêu'
                    hdr_cells[2].text = 'Số câu thực tế'
                    
                    for md, n_cau in required_q_by_level.items():
                        row_cells = table_summary.add_row().cells
                        row_cells[0].text = md
                        row_cells[1].text = f"{st.session_state.ti_le_muc_do.get(md, 0)}%"
                        row_cells[2].text = str(n_cau)
                        
                    doc.add_paragraph("\n")
                    doc.add_paragraph("------------------ NỘI DUNG ĐỀ KIỂM TRA ------------------")
                    doc.add_paragraph("\n")
                    
                    for q in questions:
                        # Thêm câu hỏi
                        doc.add_paragraph(q)
                        # Thêm khoảng trống để trả lời
                        doc.add_paragraph("..............................................") 
                        doc.add_paragraph("")
                    
                    buffer = BytesIO()
                    doc.save(buffer)
                    buffer.seek(0)
                    
                    st.download_button(
                        "📥 Tải xuống file Word (Bao gồm cấu trúc đề)",
                        data=buffer,
                        file_name=f"De_Kiem_Tra_{mon}_{chuong}_{bai}_{so_cau_total}cau.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
