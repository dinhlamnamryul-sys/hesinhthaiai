import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import math

st.set_page_config(page_title="Tạo đề tự động theo SGK KNTT (CV 7991)", page_icon="📝", layout="wide")
st.title("📝 Tạo đề kiểm tra tự động theo CV 7991 (Sử dụng Ma trận Mẫu)")

st.markdown("""
Hệ thống sử dụng ma trận câu hỏi mẫu được định nghĩa sẵn theo cấu trúc SGK Kết nối tri thức.
Bạn có thể tự chọn Môn, Chương, Bài, Chủ đề và cấu hình tỉ lệ phân bổ câu hỏi theo 4 mức độ nhận thức (CV 7991) để tạo đề.
""")

# -------------------- MOCK DATA (DỮ LIỆU GIẢ LẬP MA TRẬN) --------------------
# Đã thêm dữ liệu cho Toán 6, 7, 8, 9 (KNTT)
data = {
    "Mon": [
        # Dữ liệu Toán 6
        "Toán 6", "Toán 6",
        # Dữ liệu Toán 7
        "Toán 7", "Toán 7",
        # Dữ liệu Toán 8
        "Toán 8", "Toán 8",
        # Dữ liệu Toán 9
        "Toán 9", "Toán 9",
        # Dữ liệu hiện tại (Toán 10, Lý 10, Hóa 10)
        "Toán 10", "Toán 10", "Toán 10", "Toán 10", 
        "Lý 10", "Lý 10", "Lý 10", 
        "Hóa 10", "Hóa 10"
    ],
    "Chuong": [
        "Chương I: Số tự nhiên", "Chương II: Số nguyên",
        "Chương I: Số hữu tỉ", "Chương II: Số thực",
        "Chương I: Đa thức", "Chương II: Hình học",
        "Chương I: Phương trình", "Chương II: Hàm số",
        "Chương I: Tập hợp", "Chương I: Tập hợp", "Chương II: Hàm số", "Chương II: Hàm số", 
        "Chương I: Động học", "Chương I: Động học", "Chương II: Lực", 
        "Chương I: Nguyên tử", "Chương I: Nguyên tử"
    ],
    "Bai": [
        "Bài 5: Lũy thừa", "Bài 12: Phép cộng",
        "Bài 1: Số hữu tỉ", "Bài 7: Đại lượng tỉ lệ",
        "Bài 3: Hằng đẳng thức", "Bài 8: Tứ giác",
        "Bài 2: Phương trình bậc hai", "Bài 5: Đồ thị",
        "Bài 1: Mở đầu", "Bài 2: Các phép toán", "Bài 3: Định nghĩa", "Bài 4: Khảo sát", 
        "Bài 1: Chuyển động", "Bài 2: Tốc độ", "Bài 3: Lực", 
        "Bài 1: Cấu tạo", "Bài 2: Đồng vị"
    ],
    "ChuDe": [
        "Tính toán lũy thừa", "Phép cộng số nguyên",
        "Biểu diễn số hữu tỉ", "Tỉ lệ thuận/nghịch",
        "Bình phương tổng", "Định nghĩa tứ giác",
        "Giải phương trình", "Đồ thị hàm số bậc hai",
        "Khái niệm tập hợp", "Phép toán giao/hợp", "Tìm tập xác định", "Tính đơn điệu", 
        "Khái niệm CĐ", "Tính vận tốc TB", "Xác định lực", 
        "Cấu hình e", "Khái niệm đồng vị"
    ],
    "NoiDung": [
        "Tính giá trị biểu thức lũy thừa", "Cộng hai số nguyên khác dấu",
        "Biểu diễn số hữu tỉ trên trục số", "Giải bài toán tỉ lệ nghịch",
        "Khai triển hằng đẳng thức", "Tính góc trong tứ giác",
        "Giải PT bậc hai bằng công thức", "Tìm đỉnh Parabol",
        "Nhận dạng tập hợp", "Giải bài tập giao/hợp", "Tìm TXĐ", "Khảo sát hàm số bậc hai", 
        "Định nghĩa CĐ", "Tính toán TB", "Phân tích lực", 
        "Viết cấu hình", "Tính khối lượng TB"
    ],
    "MucDo": [
        "Nhận biết", "Thông hiểu",
        "Nhận biết", "Vận dụng",
        "Thông hiểu", "Nhận biết",
        "Vận dụng", "Vận dụng cao",
        "Nhận biết", "Thông hiểu", "Nhận biết", "Vận dụng", 
        "Nhận biết", "Thông hiểu", "Vận dụng cao", 
        "Thông hiểu", "Vận dụng"
    ],
    "SoCau": [
        3, 2, 
        4, 2, 
        3, 2,
        3, 1,
        3, 2, 4, 1, 
        3, 2, 1, 
        2, 1
    ] # Trọng số số câu cho từng mục tiêu (Tổng điểm/số câu có sẵn)
}
df = pd.DataFrame(data)

# -------------------- HIỂN THỊ MA TRẬN MẪU --------------------
st.write("📋 Ma trận câu hỏi mẫu:")
st.dataframe(df[['Mon', 'Chuong', 'Bai', 'ChuDe', 'NoiDung', 'MucDo', 'SoCau']], use_container_width=True)

# -------------------- CHỌN LỌC DỮ LIỆU ĐẦU VÀO --------------------
col1, col2 = st.columns(2)
with col1:
    mon_list = sorted(df['Mon'].unique())
    mon = st.selectbox("1. Chọn môn học:", mon_list)
    
    # Lọc theo Môn
    df_mon = df[df['Mon']==mon]
    chuong_list = sorted(df_mon['Chuong'].unique())
    chuong = st.selectbox("2. Chọn chương:", chuong_list)

with col2:
    # Lọc theo Chương
    df_chuong = df_mon[df_mon['Chuong']==chuong]
    bai_list = sorted(df_chuong['Bai'].unique())
    bai = st.selectbox("3. Chọn bài:", bai_list)
    
    # Lọc theo Bài
    df_bai = df_chuong[df_chuong['Bai']==bai]
    chu_de_list = sorted(df_bai['ChuDe'].unique())
    chu_de = st.multiselect("4. Chọn Chủ đề (có thể nhiều):", chu_de_list, default=chu_de_list)

# Lọc DataFrame theo lựa chọn cuối cùng
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
        st.error("Không tìm thấy câu hỏi nào phù hợp với bộ lọc đã chọn. Vui lòng chọn lại Môn/Chương/Bài/Chủ đề.")
    else:
        # 1. Chuẩn hóa tỉ lệ mức độ và tính số lượng câu cần
        normalized_ti_le = {}
        if total_percent == 0:
            st.error("Tổng tỉ lệ mức độ không thể bằng 0%. Vui lòng nhập tỉ lệ.")
            st.stop()
            
        for md, percent in st.session_state.ti_le_muc_do.items():
            normalized_ti_le[md] = percent / total_percent 

        required_q_by_level = {}
        remaining_total_q = so_cau_total
        
        # Tính số câu cần cho mỗi mức độ
        for i, (md, ratio) in enumerate(normalized_ti_le.items()):
            if i < len(normalized_ti_le) - 1:
                required_q = round(so_cau_total * ratio)
                required_q_by_level[md] = required_q
                remaining_total_q -= required_q
            else:
                required_q_by_level[md] = remaining_total_q

        
        questions = []
        q_number = 1
        
        # 2. Bắt đầu sinh câu hỏi theo TỪNG MỨC ĐỘ
        for md in ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]:
            n_cau_level = required_q_by_level.get(md, 0)
            if n_cau_level == 0:
                continue

            # Lọc các dòng có mức độ phù hợp
            df_md = df_filtered[df_filtered['MucDo'].str.contains(md, case=False, na=False)].copy()
            
            if df_md.empty:
                st.warning(f"Không có câu hỏi mức độ **{md}** trong ma trận mẫu được chọn. Bỏ qua.")
                continue

            # Tính tổng 'SoCau' có sẵn
            total_available_points = df_md['SoCau'].sum()
            
            if total_available_points == 0:
                st.warning(f"Tổng trọng số (SoCau) cho mức độ **{md}** là 0. Bỏ qua.")
                continue

            # 3. Phân bổ n_cau_level cho các hàng (dựa trên tỷ trọng SoCau)
            df_md['N_Needed'] = (df_md['SoCau'] / total_available_points) * n_cau_level
            df_md['N_to_Take'] = df_md['N_Needed'].apply(lambda x: math.ceil(x))
            df_md['N_to_Take'] = df_md.apply(lambda row: min(row['N_to_Take'], row['SoCau']), axis=1)

            # Giới hạn tổng số câu lấy không vượt quá n_cau_level
            current_total_take = df_md['N_to_Take'].sum()
            if current_total_take > n_cau_level:
                rows_to_adjust = df_md[df_md['N_to_Take'] > 0].sort_values(by='N_to_Take', ascending=False).index.tolist()
                
                while df_md['N_to_Take'].sum() > n_cau_level and rows_to_adjust:
                    idx = rows_to_adjust.pop(0) 
                    df_md.loc[idx, 'N_to_Take'] -= 1
                    if df_md.loc[idx, 'N_to_Take'] == 0:
                        rows_to_adjust = [i for i in rows_to_adjust if i != idx]

            # 4. Tạo câu hỏi
            for _, row in df_md.iterrows():
                n_to_take = int(row['N_to_Take'])
                for i in range(n_to_take):
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
        
        # Thêm bảng tóm tắt cấu trúc đề
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
        
        try:
            import docx
        except ImportError:
            pass

        for q in questions:
            doc.add_paragraph(q)
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
