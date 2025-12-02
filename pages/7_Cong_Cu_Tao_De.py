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
data = {
    "Mon": [
        "Toán 6", "Toán 6", "Toán 7", "Toán 7", "Toán 8", "Toán 8", "Toán 9", "Toán 9",
        "Toán 10", "Toán 10", "Toán 10", "Toán 10", 
        "Lý 10", "Lý 10", "Lý 10", 
        "Hóa 10", "Hóa 10"
    ],
    "Chuong": [
        "Chương I: Số tự nhiên", "Chương II: Số nguyên", "Chương I: Số hữu tỉ", "Chương II: Số thực", 
        "Chương I: Đa thức", "Chương II: Hình học", "Chương I: Phương trình", "Chương II: Hàm số",
        "Chương I: Tập hợp", "Chương I: Tập hợp", "Chương II: Hàm số", "Chương II: Hàm số", 
        "Chương I: Động học", "Chương I: Động học", "Chương II: Lực", 
        "Chương I: Nguyên tử", "Chương I: Nguyên tử"
    ],
    "Bai": [
        "Bài 5: Lũy thừa", "Bài 12: Phép cộng", "Bài 1: Số hữu tỉ", "Bài 7: Đại lượng tỉ lệ", 
        "Bài 3: Hằng đẳng thức", "Bài 8: Tứ giác", "Bài 2: Phương trình bậc hai", "Bài 5: Đồ thị",
        "Bài 1: Mở đầu", "Bài 2: Các phép toán", "Bài 3: Định nghĩa", "Bài 4: Khảo sát", 
        "Bài 1: Chuyển động", "Bài 2: Tốc độ", "Bài 3: Lực", 
        "Bài 1: Cấu tạo", "Bài 2: Đồng vị"
    ],
    "ChuDe": [
        "Tính toán lũy thừa", "Phép cộng số nguyên", "Biểu diễn số hữu tỉ", "Tỉ lệ thuận/nghịch",
        "Bình phương tổng", "Định nghĩa tứ giác", "Giải phương trình", "Đồ thị hàm số bậc hai",
        "Khái niệm tập hợp", "Phép toán giao/hợp", "Tìm tập xác định", "Tính đơn điệu", 
        "Khái niệm CĐ", "Tính vận tốc TB", "Xác định lực", 
        "Cấu hình e", "Khái niệm đồng vị"
    ],
    "NoiDung": [
        "Tính giá trị biểu thức lũy thừa", "Cộng hai số nguyên khác dấu", "Biểu diễn số hữu tỉ trên trục số", "Giải bài toán tỉ lệ nghịch",
        "Khai triển hằng đẳng thức", "Tính góc trong tứ giác", "Giải PT bậc hai bằng công thức", "Tìm đỉnh Parabol",
        "Nhận dạng tập hợp", "Giải bài tập giao/hợp", "Tìm TXĐ", "Khảo sát hàm số bậc hai", 
        "Định nghĩa CĐ", "Tính vận tốc TB", "Phân tích lực", 
        "Viết cấu hình", "Tính khối lượng TB"
    ],
    "MucDo": [
        "Nhận biết", "Thông hiểu", "Nhận biết", "Vận dụng", "Thông hiểu", "Nhận biết", "Vận dụng", "Vận dụng cao",
        "Nhận biết", "Thông hiểu", "Nhận biết", "Vận dụng", 
        "Nhận biết", "Thông hiểu", "Vận dụng cao", 
        "Thông hiểu", "Vận dụng"
    ],
    "SoCau": [
        3, 2, 4, 2, 3, 2, 3, 1, 
        3, 2, 4, 1, 
        3, 2, 1, 
        2, 1
    ] 
}
df = pd.DataFrame(data)

# -------------------- KHỞI TẠO BIẾN TRÁNH NAMEERROR --------------------
questions = []
required_q_by_level = {}
ma_tran_df_final = pd.DataFrame()
df_dac_ta_display = pd.DataFrame()


# -------------------- HÀM TẠO MA TRẬN THEO CV 7991 (PHỤ LỤC 1) --------------------

def create_ma_tran_cv7991(df_input, total_cau):
    """Tạo DataFrame Ma trận theo cấu trúc Phụ lục 1 của CV 7991."""
    
    df_temp = df_input.copy()
    
    # 1. Định nghĩa 9 cột chính theo CV 7991 (Giả định DS và TL-B/H là 0)
    matrix_cols_9 = [
        'NL - Biết', 'NL - Hiểu', 'NL - Vận dụng',
        'DS - Biết', 'DS - Hiểu', 'DS - Vận dụng',
        'TL - Biết', 'TL - Hiểu', 'TL - Vận dụng'
    ]
    
    for col in matrix_cols_9:
        df_temp[col] = 0
        
    # Ánh xạ số câu N_to_Take vào 9 cột ma trận (Giả định NL là Nhận biết/Thông hiểu, TL là Vận dụng/Vận dụng cao)
    df_temp.loc[df_temp['MucDo'] == 'Nhận biết', 'NL - Biết'] = df_temp['N_to_Take']
    df_temp.loc[df_temp['MucDo'] == 'Thông hiểu', 'NL - Hiểu'] = df_temp['N_to_Take']
    df_temp.loc[df_temp['MucDo'].isin(['Vận dụng', 'Vận dụng cao']), 'TL - Vận dụng'] = df_temp['N_to_Take']
    
    # 2. Tạo bảng xoay để tổng hợp số câu theo Chủ đề
    index_cols = ['ChuDe', 'NoiDung']
    
    pivot_table = pd.pivot_table(
        df_temp, 
        values=matrix_cols_9, 
        index=index_cols, 
        aggfunc='sum', 
        fill_value=0
    )
    
    # Thêm cột Tổng số câu (theo hàng)
    pivot_table['Tổng số câu'] = pivot_table[matrix_cols_9].sum(axis=1)
    
    # 3. Tính các hàng Tổng kết
    tong_so_cau_hang = pivot_table.sum().to_frame().T 

    # Tính Tổng theo Mức độ (Biết, Hiểu, Vận dụng)
    tong_theo_muc_do = {}
    tong_theo_muc_do['Tổng Biết'] = tong_so_cau_hang[['NL - Biết', 'DS - Biết', 'TL - Biết']].sum(axis=1).iloc[0]
    tong_theo_muc_do['Tổng Hiểu'] = tong_so_cau_hang[['NL - Hiểu', 'DS - Hiểu', 'TL - Hiểu']].sum(axis=1).iloc[0]
    tong_theo_muc_do['Tổng Vận dụng'] = tong_so_cau_hang[['NL - Vận dụng', 'DS - Vận dụng', 'TL - Vận dụng']].sum(axis=1).iloc[0]
    
    tong_cau = tong_so_cau_hang['Tổng số câu'].iloc[0]
    ti_le_muc_do = {k: round((v / tong_cau) * 100, 1) for k, v in tong_theo_muc_do.items()}
    ti_le_muc_do['Tổng'] = 100.0
    
    tong_diem = 10.0
    diem_muc_do = {k: round((v / 100) * tong_diem, 1) for k, v in ti_le_muc_do.items() if k != 'Tổng'}
    diem_muc_do['Tổng'] = round(sum(diem_muc_do.values()), 1)

    # 4. Ghép các hàng Tổng vào bảng chính
    final_ma_tran = pivot_table.reset_index() 
    
    # FIX LỖI: Gán 12 tên cột cho 12 cột thực tế
    new_cols = ['Chủ đề', 'Nội dung'] + list(pivot_table.columns) # 2 + 10 = 12
    final_ma_tran.columns = new_cols 

    # Chuẩn bị dữ liệu cho 3 hàng tổng kết
    col_names_for_data = list(pivot_table.columns) 
    
    tong_cau_data = {col: tong_so_cau_hang[col].iloc[0] for col in col_names_for_data}
    ti_le_data = {col: '' for col in col_names_for_data} 
    diem_data = {col: '' for col in col_names_for_data} 

    summary_data = [
        {'Chủ đề': 'Tổng số câu', 'Nội dung': '', **tong_cau_data},
        {'Chủ đề': 'Tỉ lệ %', 'Nội dung': '', **ti_le_data},
        {'Chủ đề': 'Điểm (10đ)', 'Nội dung': '', **diem_data},
    ]

    summary_df = pd.DataFrame(summary_data, columns=final_ma_tran.columns)
    
    final_ma_tran = pd.concat([final_ma_tran, summary_df], ignore_index=True)
    
    # 5. Format dữ liệu Tỉ lệ % và Điểm vào các ô tổng kết
    idx_ti_le = final_ma_tran[final_ma_tran['Chủ đề'] == 'Tỉ lệ %'].index[0]
    idx_diem = final_ma_tran[final_ma_tran['Chủ đề'] == 'Điểm (10đ)'].index[0]
    
    # Ghi Tổng Số câu, Tổng Tỉ lệ %, Tổng Điểm vào cột Nội dung và Tổng số câu
    final_ma_tran.loc[final_ma_tran['Chủ đề'] == 'Tổng số câu', 'Nội dung'] = str(tong_cau) 
    final_ma_tran.loc[idx_ti_le, 'Nội dung'] = f"{ti_le_muc_do['Tổng']}%"
    final_ma_tran.loc[idx_diem, 'Nội dung'] = str(diem_muc_do['Tổng'])
    
    # Ghi Tỉ lệ % và Điểm theo Mức độ vào các cột ma trận
    for level in ['Biết', 'Hiểu', 'Vận dụng']:
        
        col_list = [f'NL - {level}', f'DS - {level}', f'TL - {level}']
        percent_value = ti_le_muc_do[f'Tổng {level}']
        point_value = diem_muc_do[f'Tổng {level}']
        
        for col in col_list:
            final_ma_tran.loc[idx_ti_le, col] = f"{percent_value}%"
            final_ma_tran.loc[idx_diem, col] = point_value
    
    # 6. Chuẩn bị DataFrame cuối cùng với MultiIndex Header
    
    # Đặt lại tên cột tổng cuối cùng thành 'Tổng' cho gọn
    final_ma_tran = final_ma_tran.rename(columns={'Tổng số câu': 'Tổng'}) 

    # Các cột sẽ hiển thị: 2 cột tiêu đề + 9 cột ma trận + 1 cột Tổng
    display_cols = ['Chủ đề', 'Nội dung'] + matrix_cols_9 + ['Tổng']
    final_ma_tran = final_ma_tran[display_cols]
    
    # Tạo tiêu đề Multi-Index theo CV 7991
    header_1_data = ['Nội dung/Đơn vị kiến thức', 'Nội dung/Đơn vị kiến thức'] + ['Nhiều lựa chọn'] * 3 + ['Đúng - Sai'] * 3 + ['Tự luận'] * 3 + ['Tổng']
    header_2_data = ['Chủ đề', 'Nội dung'] + ['Biết', 'Hiểu', 'VĐ'] * 3 + ['Số câu/điểm']
    
    final_ma_tran.columns = pd.MultiIndex.from_arrays([header_1_data, header_2_data])
    
    return final_ma_tran.astype(str).replace('0', '').replace('nan', '')

# -------------------- CHỌN LỌC DỮ LIỆU ĐẦU VÀO --------------------
# ... (Phần code Selectbox giữ nguyên) ...

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

df_filtered = df[(df['Mon']==mon) & 
                 (df['Chuong']==chuong) & 
                 (df['Bai']==bai) & 
                 (df['ChuDe'].isin(chu_de))].copy()

# -------------------- THIẾT LẬP CV 7991 --------------------
st.markdown("---")
st.subheader("⚙️ Cấu hình đề kiểm tra theo CV 7991")

so_cau_total = st.number_input("5. Tổng số câu muốn tạo:", min_value=1, max_value=100, value=20)

st.markdown("**6. Tỉ lệ câu theo mức độ nhận thức (%)** (Tổng nên bằng 100%)")

if 'ti_le_muc_do' not in st.session_state:
    st.session_state.ti_le_muc_do = {
        "Nhận biết": 30,
        "Thông hiểu": 40,
        "Vận dụng": 20,
        "Vận dụng cao": 10
    }

col_nb, col_th, col_vd, col_vdc = st.columns(4)

with col_nb:
    st.session_state.ti_le_muc_do["Nhận biết"] = st.number_input("Nhận biết (%)", min_value=0, max_value=100, value=st.session_state.ti_le_muc_do["Nhận biết"])
with col_th:
    st.session_state.ti_le_muc_do["Thông hiểu"] = st.number_input("Thông hiểu (%)", min_value=0, max_value=100, value=st.session_state.ti_le_muc_do["Thông hiểu"])
with col_vd:
    st.session_state.ti_le_muc_do["Vận dụng"] = st.number_input("Vận dụng (%)", min_value=0, max_value=100, value=st.session_state.ti_le_muc_do["Vận dụng"])
with col_vdc:
    st.session_state.ti_le_muc_do["Vận dụng cao"] = st.number_input("Vận dụng cao (%)", min_value=0, max_value=100, value=st.session_state.ti_le_muc_do["Vận dụng cao"])

total_percent = sum(st.session_state.ti_le_muc_do.values())
st.info(f"Tổng tỉ lệ đã nhập: {total_percent}%. Hệ thống sẽ tự động chuẩn hóa.")

# -------------------- XỬ LÝ KHI BẤM NÚT TẠO ĐỀ --------------------

if st.button("📘 Tạo đề tự động", use_container_width=True):
    
    if df_filtered.empty or total_percent == 0:
        st.error("Lỗi: Không tìm thấy dữ liệu hoặc Tổng tỉ lệ mức độ bằng 0%.")
        st.stop()

    # 1. Chuẩn hóa tỉ lệ và tính N_to_Take
    normalized_ti_le = {md: percent / total_percent for md, percent in st.session_state.ti_le_muc_do.items()}
    required_q_by_level = {}
    remaining_total_q = so_cau_total
    levels = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
    
    for i, md in enumerate(levels):
        ratio = normalized_ti_le.get(md, 0)
        required_q = round(so_cau_total * ratio) if i < len(levels) - 1 else remaining_total_q
        required_q_by_level[md] = required_q
        remaining_total_q -= required_q
        
    df_filtered['N_to_Take'] = 0
    questions = []
    q_number = 1
    
    # 2. Phân bổ câu hỏi và Tạo nội dung đề
    for md in levels:
        n_cau_level = required_q_by_level.get(md, 0)
        if n_cau_level == 0: continue

        df_md_index = df_filtered[df_filtered['MucDo'] == md].index
        if df_md_index.empty: continue

        total_available_points = df_filtered.loc[df_md_index, 'SoCau'].sum()
        if total_available_points == 0: continue

        df_filtered.loc[df_md_index, 'N_Needed'] = (df_filtered.loc[df_md_index, 'SoCau'] / total_available_points) * n_cau_level
        df_filtered.loc[df_md_index, 'N_to_Take'] = df_filtered.loc[df_md_index, 'N_Needed'].apply(lambda x: math.ceil(x))
        
        df_filtered.loc[df_md_index, 'N_to_Take'] = df_filtered.apply(
            lambda row: min(row['N_to_Take'], row['SoCau']) if row['MucDo'] == md else row['N_to_Take'], axis=1)
        
        current_total_take = df_filtered.loc[df_md_index, 'N_to_Take'].sum()
        if current_total_take > n_cau_level:
            rows_to_adjust = df_filtered.loc[df_md_index].sort_values(by='N_to_Take', ascending=False).index.tolist()
            while df_filtered.loc[df_md_index, 'N_to_Take'].sum() > n_cau_level and rows_to_adjust:
                idx = rows_to_adjust.pop(0) 
                df_filtered.loc[idx, 'N_to_Take'] -= 1
        
        for index, row in df_filtered.loc[df_md_index].iterrows():
            n_to_take = int(row['N_to_Take'])
            for i in range(n_to_take):
                q_text = (f"Câu {q_number}. ({row.get('MucDo')}) - Chủ đề: {row.get('ChuDe')}\n"
                          f"Nội dung: {row.get('NoiDung')}\n"
                          f"→ (Lưu ý: Bạn cần thay thế Nội dung này bằng câu hỏi trắc nghiệm/tự luận thực tế.)\n"
                          f"→ Hãy trình bày câu trả lời.")
                questions.append(q_text)
                q_number += 1

    # 3. Hiển thị Ma trận Đề kiểm tra
    st.markdown("---")
    st.subheader("📊 1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 1 - CV 7991)")
    
    df_with_n_take = df_filtered[df_filtered['N_to_Take'] > 0].copy()

    if not df_with_n_take.empty:
        ma_tran_df_final = create_ma_tran_cv7991(df_with_n_take, so_cau_total)
        st.write("Cấu trúc Ma trận:")
        st.dataframe(ma_tran_df_final, hide_index=True, use_container_width=True)
    else:
        st.error("Lỗi phân bổ: Không thể tạo đủ câu hỏi theo tỉ lệ đã chọn từ ma trận mẫu.")
        st.stop()
        
    # 4. Hiển thị Bản Đặc tả (Tóm tắt)
    st.markdown("---")
    st.subheader("📑 2. BẢN ĐẶC TẢ ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 2 - Rút gọn)")
    
    df_dac_ta_display = df_with_n_take[['ChuDe', 'NoiDung', 'MucDo', 'N_to_Take']].rename(columns={
        'ChuDe': 'Chủ đề/Chương',
        'NoiDung': 'Yêu cầu cần đạt',
        'MucDo': 'Mức độ',
        'N_to_Take': 'Số câu hỏi thực tế'
    })
    
    st.dataframe(df_dac_ta_display.astype(str), hide_index=True, use_container_width=True)
    
    # 5. Hiển thị Đề kiểm tra
    st.success(f"Đã tạo thành công {len(questions)} câu hỏi theo cấu trúc CV 7991!")
    st.subheader("📄 3. ĐỀ KIỂM TRA TỰ ĐỘNG:")
    
    output_text = ""
    for q in questions:
        st.markdown(q)
        st.markdown("---")
        output_text += q + "\n" + "---" + "\n\n"

    # 6. Xuất Word (Bao gồm Ma trận và Bản Đặc tả)
    doc = Document()
    doc.add_heading(f"ĐỀ KIỂM TRA: {mon} - {chuong} - {bai}", 0)
    
    # --- Thêm Ma trận vào Word ---
    doc.add_heading("1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 1)", 2)
    
    num_rows = ma_tran_df_final.shape[0] + 2 
    num_cols = ma_tran_df_final.shape[1]
    table_ma_tran_word = doc.add_table(rows=num_rows, cols=num_cols)
    table_ma_tran_word.style = 'Table Grid'
    
    # Ghi Multi-Index Header vào 2 hàng đầu
    for j, (h1, h2) in enumerate(ma_tran_df_final.columns):
        table_ma_tran_word.cell(0, j).text = h1
        table_ma_tran_word.cell(1, j).text = h2
        
    # Gộp ô cho header (Cần 4 ô gộp: Nội dung, NL, DS, TL)
    table_ma_tran_word.cell(0, 0).merge(table_ma_tran_word.cell(0, 1)) 
    table_ma_tran_word.cell(0, 2).merge(table_ma_tran_word.cell(0, 4)) 
    table_ma_tran_word.cell(0, 5).merge(table_ma_tran_word.cell(0, 7)) 
    table_ma_tran_word.cell(0, 8).merge(table_ma_tran_word.cell(0, 10)) 
    
    # Thêm dữ liệu (bắt đầu từ hàng thứ 3)
    for i in range(ma_tran_df_final.shape[0]):
        for j in range(ma_tran_df_final.shape[1]):
            table_ma_tran_word.cell(i + 2, j).text = str(ma_tran_df_final.iloc[i, j])

    # --- Thêm Bản Đặc tả vào Word ---
    doc.add_heading("2. BẢN ĐẶC TẢ ĐỀ KIỂM TRA ĐỊNH KÌ (Rút gọn)", 2)
    
    table_dac_ta_word = doc.add_table(rows=df_dac_ta_display.shape[0] + 1, cols=df_dac_ta_display.shape[1])
    table_dac_ta_word.style = 'Table Grid'
    
    for j, col_name in enumerate(df_dac_ta_display.columns):
        table_dac_ta_word.cell(0, j).text = col_name

    for i in range(df_dac_ta_display.shape[0]):
        for j in range(df_dac_ta_display.shape[1]):
            table_dac_ta_word.cell(i + 1, j).text = str(df_dac_ta_display.iloc[i, j])

    # --- Thêm Nội dung đề vào Word ---
    doc.add_paragraph("\n")
    doc.add_heading("3. NỘI DUNG ĐỀ KIỂM TRA", 2)
    doc.add_paragraph("\n")
    
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
