import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import math

st.set_page_config(page_title="Tạo đề Toán 6-9 theo SGK KNTT (CV 7991)", page_icon="📝", layout="wide")
st.title("📝 Tạo đề kiểm tra môn Toán (Lớp 6-9) theo CV 7991")

st.markdown("""
Hệ thống sử dụng ma trận câu hỏi mẫu được **tổng hợp từ mục lục sách giáo khoa Toán 6, 7, 8, 9 (Tập 1 - Kết nối tri thức với cuộc sống)** để bạn lựa chọn.
Bạn có thể chọn Môn, Chương, Bài, Chủ đề và cấu hình tỉ lệ phân bổ câu hỏi theo 4 mức độ nhận thức (CV 7991) để tạo đề.
""")

# -------------------- DỮ LIỆU MOCK THEO MỤC LỤC SGK TOÁN 6-9 KNTT TẬP 1 --------------------
# Dữ liệu được trích xuất từ các file PDF sách giáo khoa Toán 6, 7, 8, 9 bạn đã gửi.
data = {'Mon': ['Toán 6', 'Toán 6', 'Toán 6', 'Toán 6', 'Toán 6', 'Toán 6', 'Toán 6', 'Toán 6', 'Toán 6', 'Toán 7', 'Toán 7', 'Toán 7', 'Toán 7', 'Toán 7', 'Toán 7', 'Toán 7', 'Toán 7', 'Toán 8', 'Toán 8', 'Toán 8', 'Toán 8', 'Toán 8', 'Toán 8', 'Toán 8', 'Toán 8', 'Toán 9', 'Toán 9', 'Toán 9', 'Toán 9', 'Toán 9', 'Toán 9', 'Toán 9', 'Toán 9', 'Toán 9'], 
        'Chuong': ['Chương I: Tập hợp các số tự nhiên', 'Chương I: Tập hợp các số tự nhiên', 'Chương I: Tập hợp các số tự nhiên', 'Chương II: Tính chia hết', 'Chương II: Tính chia hết', 'Chương III: Số nguyên', 'Chương III: Số nguyên', 'Chương IV: Hình học thực tiễn', 'Chương IV: Hình học thực tiễn', 'Chương I: Số hữu tỉ', 'Chương I: Số hữu tỉ', 'Chương II: Số thực', 'Chương III: Góc và đường thẳng song song', 'Chương III: Góc và đường thẳng song song', 'Chương IV: Tam giác bằng nhau', 'Chương IV: Tam giác bằng nhau', 'Chương V: Thu thập và biểu diễn dữ liệu', 'Chương I: Đa thức', 'Chương I: Đa thức', 'Chương II: Hằng đẳng thức', 'Chương II: Hằng đẳng thức', 'Chương III: Tứ giác', 'Chương III: Tứ giác', 'Chương IV: Định lí Thalès', 'Chương IV: Định lí Thalès', 'Chương I: Phương trình và Hệ phương trình', 'Chương I: Phương trình và Hệ phương trình', 'Chương II: Căn bậc hai và Căn bậc ba', 'Chương II: Căn bậc hai và Căn bậc ba', 'Chương III: Hệ thức lượng trong tam giác vuông', 'Chương III: Hệ thức lượng trong tam giác vuông', 'Chương IV: Đường tròn', 'Chương IV: Đường tròn', 'Chương IV: Đường tròn'], 
        'Bai': ['Bài 1. Tập hợp', 'Bài 4. Phép cộng và phép trừ', 'Bài 6. Luỹ thừa với số mũ tự nhiên', 'Bài 9. Dấu hiệu chia hết', 'Bài 12. Ước chung lớn nhất. Bội chung nhỏ nhất', 'Bài 14. Phép cộng và phép trừ số nguyên', 'Bài 16. Phép nhân số nguyên', 'Bài 18. Hình tam giác đều. Hình vuông. Hình lục giác đều', 'Bài 20. Chu vi và diện tích', 'Bài 1. Tập hợp các số hữu tỉ', 'Bài 2. Cộng, trừ, nhân, chia số hữu tỉ', 'Bài 6. Số vô tỉ. Căn bậc hai số học', 'Bài 8. Góc ở vị trí đặc biệt', 'Bài 9. Hai đường thẳng song song', 'Bài 13. Hai tam giác bằng nhau', 'Bài 15. Các trường hợp bằng nhau của tam giác vuông', 'Bài 17. Thu thập và phân loại dữ liệu', 'Bài 1. Đơn thức', 'Bài 3. Phép cộng và phép trừ đa thức', 'Bài 6. Hiệu hai bình phương', 'Bài 9. Phân tích đa thức thành nhân tử', 'Bài 10. Tứ giác', 'Bài 14. Hình thoi và hình vuông', 'Bài 15. Định lí Thalès trong tam giác', 'Bài 17. Tính chất đường phân giác', 'Bài 1. Khái niệm phương trình và hệ hai phương trình', 'Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn', 'Bài 5. Căn bậc hai và căn thức bậc hai', 'Bài 7. Các phép biến đổi căn thức bậc hai', 'Bài 10. Hệ thức về cạnh và đường cao', 'Bài 11. Tỉ số lượng giác của góc nhọn', 'Bài 13. Mở đầu về đường tròn', 'Bài 17. Góc ở tâm. Số đo cung', 'Bài 18. Góc nội tiếp'], 
        'ChuDe': ['Khái niệm tập hợp', 'Phép toán số tự nhiên', 'Lũy thừa', 'Dấu hiệu chia hết', 'ƯCLN và BCNN', 'Cộng/Trừ số nguyên', 'Phép nhân số nguyên', 'Các hình cơ bản', 'Tính diện tích', 'Khái niệm số hữu tỉ', 'Phép toán số hữu tỉ', 'Căn bậc hai', 'Góc đặc biệt', 'Dấu hiệu song song', 'Trường hợp bằng nhau c.c.c', 'Tam giác vuông', 'Thống kê', 'Khái niệm đơn thức', 'Cộng/Trừ đa thức', 'HĐT cơ bản', 'Phân tích nhân tử', 'Tính chất tứ giác', 'Hình đặc biệt', 'Định lí Thalès', 'Đường phân giác', 'Khái niệm hệ PT', 'Giải hệ PT', 'Điều kiện có nghĩa', 'Rút gọn biểu thức', 'Hệ thức lượng', 'Tỉ số lượng giác', 'Đường tròn cơ bản', 'Góc ở tâm', 'Góc nội tiếp'], 
        'NoiDung': ['Nhận biết tập hợp và các phần tử', 'Thực hiện phép cộng/trừ số tự nhiên', 'Tính giá trị biểu thức lũy thừa', 'Vận dụng dấu hiệu chia hết', 'Giải bài toán thực tế dùng ƯCLN/BCNN', 'Thực hiện phép tính cộng, trừ số nguyên', 'Áp dụng quy tắc nhân số nguyên', 'Nhận biết đặc điểm các hình cơ bản', 'Tính chu vi/diện tích các hình đã học', 'Nhận biết số hữu tỉ và biểu diễn trên trục số', 'Thực hiện các phép toán với số hữu tỉ', 'Tính toán với căn bậc hai số học', 'Nhận biết và tính góc đối đỉnh, kề bù', 'Sử dụng dấu hiệu nhận biết hai đường thẳng song song', 'Chứng minh hai tam giác bằng nhau theo c.c.c', 'Chứng minh tam giác vuông bằng nhau', 'Phân loại dữ liệu (định tính, định lượng)', 'Nhận biết đơn thức, bậc, hệ số', 'Thực hiện phép cộng, trừ đa thức', 'Khai triển HĐT (A-B)(A+B)', 'Phân tích đa thức thành nhân tử (dùng HĐT, đặt nhân tử chung)', 'Tính góc trong tứ giác', 'Chứng minh một tứ giác là hình thoi/hình vuông', 'Vận dụng định lí Thalès để tính độ dài', 'Áp dụng tính chất đường phân giác', 'Nhận biết nghiệm của hệ phương trình', 'Giải hệ phương trình bằng phương pháp thế/cộng đại số', 'Tìm điều kiện xác định của căn thức', 'Thực hiện phép biến đổi và rút gọn biểu thức', 'Áp dụng các hệ thức lượng trong tam giác vuông', 'Tính tỉ số lượng giác', 'Xác định vị trí tương đối của điểm/đường thẳng với đường tròn', 'Tính số đo cung, góc ở tâm', 'Chứng minh các hệ thức liên quan đến góc nội tiếp'], 
        'MucDo': ['Nhận biết', 'Thông hiểu', 'Vận dụng', 'Vận dụng', 'Vận dụng cao', 'Thông hiểu', 'Thông hiểu', 'Nhận biết', 'Vận dụng', 'Nhận biết', 'Thông hiểu', 'Thông hiểu', 'Nhận biết', 'Vận dụng', 'Vận dụng', 'Vận dụng cao', 'Thông hiểu', 'Nhận biết', 'Thông hiểu', 'Thông hiểu', 'Vận dụng', 'Nhận biết', 'Vận dụng', 'Vận dụng', 'Vận dụng cao', 'Nhận biết', 'Thông hiểu', 'Nhận biết', 'Vận dụng', 'Thông hiểu', 'Thông hiểu', 'Nhận biết', 'Vận dụng', 'Vận dụng cao'], 
        'SoCau': [3, 4, 2, 3, 2, 3, 2, 3, 2, 3, 4, 2, 3, 3, 3, 2, 1, 2, 3, 3, 4, 2, 3, 3, 2, 2, 4, 2, 4, 3, 2, 2, 3, 2]}

df = pd.DataFrame(data)

# -------------------- HÀM TẠO MA TRẬN THEO CV 7991 (PHỤ LỤC 1) --------------------

def create_ma_tran_cv7991(df_input, total_cau):
    """Tạo DataFrame Ma trận theo cấu trúc Phụ lục 1 của CV 7991 (đã chỉnh sửa)."""
    
    df_temp = df_input.copy()
    
    matrix_cols_9 = [
        'NL - Biết', 'NL - Hiểu', 'NL - Vận dụng',
        'DS - Biết', 'DS - Hiểu', 'DS - Vận dụng',
        'TL - Biết', 'TL - Hiểu', 'TL - Vận dụng'
    ]
    
    for col in matrix_cols_9:
        df_temp[col] = 0
        
    # Ánh xạ số câu N_to_Take vào 9 cột ma trận 
    df_temp.loc[df_temp['MucDo'] == 'Nhận biết', 'NL - Biết'] = df_temp['N_to_Take']
    df_temp.loc[df_temp['MucDo'] == 'Thông hiểu', 'NL - Hiểu'] = df_temp['N_to_Take']
    df_temp.loc[df_temp['MucDo'].isin(['Vận dụng', 'Vận dụng cao']), 'TL - Vận dụng'] = df_temp['N_to_Take']
    
    index_cols = ['ChuDe', 'NoiDung']
    
    pivot_table = pd.pivot_table(
        df_temp, 
        values=matrix_cols_9, 
        index=index_cols, 
        aggfunc='sum', 
        fill_value=0
    )
    
    pivot_table['Tổng số câu'] = pivot_table[matrix_cols_9].sum(axis=1)
    
    tong_so_cau_hang = pivot_table.sum().to_frame().T 

    # Tính Tổng theo Mức độ (Biết, Hiểu, Vận dụng)
    tong_theo_muc_do = {}
    tong_theo_muc_do['Tổng Biết'] = tong_so_cau_hang[['NL - Biết', 'DS - Biết', 'TL - Biết']].sum(axis=1).iloc[0]
    tong_theo_muc_do['Tổng Hiểu'] = tong_so_cau_hang[['NL - Hiểu', 'DS - Hiểu', 'TL - Hiểu']].sum(axis=1).iloc[0]
    tong_theo_muc_do['Tổng Vận dụng'] = tong_so_cau_hang[['NL - Vận dụng', 'DS - Vận dụng', 'TL - Vận dụng']].sum(axis=1).iloc[0]
    
    tong_cau = tong_so_cau_hang['Tổng số câu'].iloc[0]
    ti_le_muc_do = {k: round((v / tong_cau) * 100, 1) if tong_cau > 0 else 0.0 for k, v in tong_theo_muc_do.items()}
    ti_le_muc_do['Tổng'] = round(sum(ti_le_muc_do.values()), 1)
    
    tong_diem = 10.0
    diem_muc_do = {k: round((v / 100) * tong_diem, 1) for k, v in ti_le_muc_do.items() if k != 'Tổng'}
    diem_muc_do['Tổng'] = round(sum(diem_muc_do.values()), 1)
    
    # Điều chỉnh điểm tổng để đảm bảo tổng là 10.0
    if tong_diem > 0 and diem_muc_do['Tổng'] != tong_diem:
        diff = tong_diem - diem_muc_do['Tổng']
        if abs(diff) > 0.05: 
            max_key = max(diem_muc_do, key=diem_muc_do.get)
            if max_key != 'Tổng':
                diem_muc_do[max_key] = round(diem_muc_do[max_key] + diff, 1)
            diem_muc_do['Tổng'] = tong_diem


    final_ma_tran = pivot_table.reset_index() 
    
    # GÁN CỘT MỚI (Đã Fix lỗi ValueError: Length mismatch)
    new_cols = ['Chủ đề', 'Nội dung'] + list(pivot_table.columns) 
    final_ma_tran.columns = new_cols 

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
    
    idx_ti_le = final_ma_tran[final_ma_tran['Chủ đề'] == 'Tỉ lệ %'].index[0]
    idx_diem = final_ma_tran[final_ma_tran['Chủ đề'] == 'Điểm (10đ)'].index[0]
    
    final_ma_tran.loc[final_ma_tran['Chủ đề'] == 'Tổng số câu', 'Nội dung'] = str(tong_cau) 
    final_ma_tran.loc[idx_ti_le, 'Nội dung'] = f"{ti_le_muc_do['Tổng']}%"
    final_ma_tran.loc[idx_diem, 'Nội dung'] = str(diem_muc_do['Tổng'])
    
    for level in ['Biết', 'Hiểu', 'Vận dụng']:
        col_list = [f'NL - {level}', f'DS - {level}', f'TL - {level}']
        percent_value = ti_le_muc_do[f'Tổng {level}']
        point_value = diem_muc_do[f'Tổng {level}']
        
        for col in col_list:
            final_ma_tran.loc[idx_ti_le, col] = f"{percent_value}%"
            final_ma_tran.loc[idx_diem, col] = point_value
    
    final_ma_tran = final_ma_tran.rename(columns={'Tổng số câu': 'Tổng'}) 

    display_cols = ['Chủ đề', 'Nội dung'] + matrix_cols_9 + ['Tổng']
    final_ma_tran = final_ma_tran[display_cols]
    
    # Tạo Multi-Index Header
    header_1_data = ['Nội dung/Đơn vị kiến thức', 'Nội dung/Đơn vị kiến thức'] + ['Nhiều lựa chọn'] * 3 + ['Đúng - Sai'] * 3 + ['Tự luận'] * 3 + ['Tổng']
    header_2_data = ['Chủ đề', 'Nội dung'] + ['Biết', 'Hiểu', 'VĐ'] * 3 + ['Số câu/điểm']
    
    final_ma_tran.columns = pd.MultiIndex.from_arrays([header_1_data, header_2_data])
    
    return final_ma_tran.astype(str).replace('0', '').replace('nan', '')

# -------------------- KHỞI TẠO BIẾN TRÁNH NAMEERROR --------------------
questions = []
required_q_by_level = {}
ma_tran_df_final = pd.DataFrame()
df_dac_ta_display = pd.DataFrame()


# -------------------- CHỌN LỌC DỮ LIỆU ĐẦU VÀO --------------------

col1, col2 = st.columns(2)
with col1:
    mon_list = sorted(df['Mon'].unique())
    # Chỉ có môn Toán
    mon = st.selectbox("1. Chọn môn học:", mon_list, index=0) 
    
    df_mon = df[df['Mon']==mon]
    chuong_list = sorted(df_mon['Chuong'].unique())
    chuong = st.selectbox("2. Chọn chương:", chuong_list, index=0)

with col2:
    df_chuong = df_mon[df_mon['Chuong']==chuong]
    bai_list = sorted(df_chuong['Bai'].unique())
    bai = st.selectbox("3. Chọn bài:", bai_list, index=0)
    
    df_bai = df_chuong[df_chuong['Bai']==bai]
    chu_de_list = sorted(df_bai['ChuDe'].unique())
    chu_de = st.multiselect("4. Chọn Chủ đề/Nội dung (có thể nhiều):", chu_de_list, default=chu_de_list)

df_filtered = df[(df['Mon']==mon) & 
                 (df['Chuong']==chuong) & 
                 (df['Bai']==bai) & 
                 (df['ChuDe'].isin(chu_de))].copy()

# -------------------- THIẾT LẬP CV 7991 --------------------
st.markdown("---")
st.subheader("⚙️ Cấu hình đề kiểm tra theo CV 7991")

so_cau_total = st.number_input("5. Tổng số câu muốn tạo:", min_value=1, max_value=100, value=20)

st.markdown("**6. Tỉ lệ câu theo mức độ nhận thức (%)** (Tổng nên bằng 100%)")

if 'ti_le_muc_do_math' not in st.session_state:
    st.session_state.ti_le_muc_do_math = {
        "Nhận biết": 30,
        "Thông hiểu": 40,
        "Vận dụng": 20,
        "Vận dụng cao": 10
    }

col_nb, col_th, col_vd, col_vdc = st.columns(4)

with col_nb:
    st.session_state.ti_le_muc_do_math["Nhận biết"] = st.number_input("Nhận biết (%)", min_value=0, max_value=100, value=st.session_state.ti_le_muc_do_math["Nhận biết"])
with col_th:
    st.session_state.ti_le_muc_do_math["Thông hiểu"] = st.number_input("Thông hiểu (%)", min_value=0, max_value=100, value=st.session_state.ti_le_muc_do_math["Thông hiểu"])
with col_vd:
    st.session_state.ti_le_muc_do_math["Vận dụng"] = st.number_input("Vận dụng (%)", min_value=0, max_value=100, value=st.session_state.ti_le_muc_do_math["Vận dụng"])
with col_vdc:
    st.session_state.ti_le_muc_do_math["Vận dụng cao"] = st.number_input("Vận dụng cao (%)", min_value=0, max_value=100, value=st.session_state.ti_le_muc_do_math["Vận dụng cao"])

total_percent = sum(st.session_state.ti_le_muc_do_math.values())
st.info(f"Tổng tỉ lệ đã nhập: {total_percent}%. Hệ thống sẽ tự động chuẩn hóa.")

# -------------------- XỬ LÝ KHI BẤM NÚT TẠO ĐỀ --------------------

if st.button("📘 Tạo đề tự động", use_container_width=True):
    
    if df_filtered.empty or total_percent == 0:
        st.error("Lỗi: Không tìm thấy dữ liệu (Chủ đề, Bài) hoặc Tổng tỉ lệ mức độ bằng 0%.")
        st.stop()

    # 1. Chuẩn hóa tỉ lệ và tính N_to_Take
    normalized_ti_le = {md: percent / total_percent for md, percent in st.session_state.ti_le_muc_do_math.items()}
    required_q_by_level = {}
    remaining_total_q = so_cau_total
    levels = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
    
    # Calculate required questions
    for i, md in enumerate(levels):
        ratio = normalized_ti_le.get(md, 0)
        if i < len(levels) - 1:
            required_q = round(so_cau_total * ratio)
        else:
            required_q = remaining_total_q
        
        required_q_by_level[md] = required_q
        remaining_total_q -= required_q
        
    df_filtered['N_to_Take'] = 0
    questions = []
    q_number = 1
    
    # 2. Phân bổ câu hỏi và Tạo nội dung đề
    for md in levels:
        n_cau_level = required_q_by_level.get(md, 0)
        if n_cau_level <= 0: continue

        df_md_index = df_filtered[df_filtered['MucDo'] == md].index
        if df_md_index.empty: continue

        total_available_points = df_filtered.loc[df_md_index, 'SoCau'].sum()
        if total_available_points == 0: continue
        
        # Proportional calculation
        df_filtered.loc[df_md_index, 'N_Needed'] = (df_filtered.loc[df_md_index, 'SoCau'] / total_available_points) * n_cau_level
        
        # Simple rounding for initial take count
        df_filtered.loc[df_md_index, 'N_to_Take'] = df_filtered.loc[df_md_index, 'N_Needed'].apply(lambda x: round(x))
        
        # Ensure N_to_Take doesn't exceed mock SoCau
        df_filtered.loc[df_md_index, 'N_to_Take'] = df_filtered.apply(
            lambda row: min(row['N_to_Take'], row['SoCau']) if row['MucDo'] == md else row['N_to_Take'], axis=1)

        # Adjustment loop to match the exact required number (n_cau_level)
        current_total_take = df_filtered.loc[df_md_index, 'N_to_Take'].sum()
        
        # Adjust down if current total > required
        while current_total_take > n_cau_level:
            rows_to_adjust = df_filtered.loc[df_md_index].sort_values(by='N_to_Take', ascending=False).index.tolist()
            if not rows_to_adjust: break
            
            idx = rows_to_adjust.pop(0) 
            if df_filtered.loc[idx, 'N_to_Take'] > 0:
                df_filtered.loc[idx, 'N_to_Take'] -= 1
            current_total_take = df_filtered.loc[df_md_index, 'N_to_Take'].sum()

        # Adjust up if current total < required
        while current_total_take < n_cau_level:
            rows_to_adjust = df_filtered.loc[df_md_index].sort_values(by='N_Needed', ascending=False).index.tolist()
            if not rows_to_adjust: break
            
            idx = rows_to_adjust.pop(0) 
            if df_filtered.loc[idx, 'N_to_Take'] < df_filtered.loc[idx, 'SoCau']:
                df_filtered.loc[idx, 'N_to_Take'] += 1
            current_total_take = df_filtered.loc[df_md_index, 'N_to_Take'].sum()
            
        # Generate question text
        for index, row in df_filtered.loc[df_md_index].iterrows():
            n_to_take = int(row['N_to_Take'])
            for i in range(n_to_take):
                q_text = (f"Câu {q_number}. ({row.get('MucDo')})\n"
                          f"Chủ đề: {row.get('ChuDe')} \n"
                          f"Bài: {row.get('Bai')} \n"
                          f"Yêu cầu cần đạt: {row.get('NoiDung')}\n"
                          f"→ (Lưu ý: Bạn cần thay thế Nội dung này bằng câu hỏi trắc nghiệm/tự luận thực tế.)\n"
                          f"→ Hãy trình bày câu trả lời.")
                questions.append(q_text)
                q_number += 1

    # 3. Hiển thị Ma trận Đề kiểm tra
    st.markdown("---")
    st.subheader("📊 1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 1 - CV 7991)")
    
    df_with_n_take = df_filtered[df_filtered['N_to_Take'] > 0].copy()

    if not df_with_n_take.empty and len(questions) == so_cau_total:
        ma_tran_df_final = create_ma_tran_cv7991(df_with_n_take, so_cau_total)
        st.write(f"Ma trận cho môn: **{mon}**, Chương: **{chuong}**, Tổng số câu: **{so_cau_total}**")
        st.dataframe(ma_tran_df_final, hide_index=True, use_container_width=True)
    else:
        st.error(f"Lỗi phân bổ: Số câu tạo được ({len(questions)}) không khớp với Tổng số câu yêu cầu ({so_cau_total}). Vui lòng thử lại với cấu hình khác hoặc điều chỉnh tỉ lệ.")
        st.stop()
        
    # 4. Hiển thị Bản Đặc tả (Tóm tắt)
    st.markdown("---")
    st.subheader("📑 2. BẢN ĐẶC TẢ ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 2 - Rút gọn)")
    
    df_dac_ta_display = df_with_n_take[['Mon', 'Chuong', 'Bai', 'ChuDe', 'NoiDung', 'MucDo', 'N_to_Take']].rename(columns={
        'Mon': 'Môn',
        'Chuong': 'Chương',
        'Bai': 'Bài',
        'ChuDe': 'Chủ đề',
        'NoiDung': 'Yêu cầu cần đạt',
        'MucDo': 'Mức độ',
        'N_to_Take': 'Số câu hỏi thực tế'
    })
    
    st.dataframe(df_dac_ta_display.astype(str), hide_index=True, use_container_width=True)
    
    # 5. Hiển thị Đề kiểm tra
    st.success(f"Đã tạo thành công {len(questions)} câu hỏi theo cấu trúc CV 7991!")
    st.subheader("📄 3. ĐỀ KIỂM TRA TỰ ĐỘNG:")
    
    for q in questions:
        # Sử dụng 2 space và \n để xuống dòng trong markdown
        st.markdown(q.replace('\n', '  \n')) 
        st.markdown("---")

    # 6. Xuất Word (Bao gồm Ma trận và Bản Đặc tả)
    doc = Document()
    doc.add_heading(f"ĐỀ KIỂM TRA: {mon} - {chuong} - Bài {bai}", 0)
    
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
        
    # Gộp ô cho header
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
        doc.add_paragraph(q.replace('\n', '\r\n')) 
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
