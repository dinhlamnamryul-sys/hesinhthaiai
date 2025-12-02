import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import math

st.set_page_config(page_title="Tạo đề Toán 6-9 theo SGK KNTT (CV 7991)", page_icon="📝", layout="wide")
st.title("📝 Tạo đề kiểm tra môn Toán (Lớp 6-9) theo CV 7991")

st.markdown("""
Hệ thống sử dụng ma trận câu hỏi mẫu được **tổng hợp đầy đủ từ mục lục sách giáo khoa Toán 6, 7, 8, 9 (Tập 1 - Kết nối tri thức với cuộc sống)**.
Bạn có thể chọn **nhiều Môn, Chương, Bài, Chủ đề** và cấu hình tỉ lệ phân bổ câu hỏi theo 4 mức độ nhận thức (CV 7991) để tạo đề.
""")

# -------------------- DỮ LIỆU MOCK THEO MỤC LỤC SGK TOÁN 6-9 KNTT TẬP 1 (Đầy đủ) --------------------
# Bộ dữ liệu mô phỏng đầy đủ các bài học (Bài) chính trong sách Toán 6, 7, 8, 9 - Tập 1
full_data = {
    'Mon': [], 'Chuong': [], 'Bai': [], 'ChuDe': [], 'NoiDung': [], 'MucDo': [], 'SoCau': []
}

def add_lesson(mon, chuong, bai, chude, noidung, mucdo, socau):
    full_data['Mon'].append(mon)
    full_data['Chuong'].append(chuong)
    full_data['Bai'].append(bai)
    full_data['ChuDe'].append(chude)
    full_data['NoiDung'].append(noidung)
    full_data['MucDo'].append(mucdo)
    full_data['SoCau'].append(socau)

# --- TOÁN 6 - TẬP 1 (Chương I - IV) ---
mon = 'Toán 6'
add_lesson(mon, 'Chương I: Tập hợp các số tự nhiên', 'Bài 1. Tập hợp', 'Khái niệm tập hợp', 'Nhận biết tập hợp và các phần tử', 'Nhận biết', 3)
add_lesson(mon, 'Chương I: Tập hợp các số tự nhiên', 'Bài 2. Các phép toán trong tập hợp', 'Phép toán tập hợp', 'Thực hiện phép toán giao, hợp', 'Thông hiểu', 2)
add_lesson(mon, 'Chương I: Tập hợp các số tự nhiên', 'Bài 4. Phép cộng và phép trừ', 'Phép toán số tự nhiên', 'Thực hiện phép cộng/trừ số tự nhiên', 'Thông hiểu', 4)
add_lesson(mon, 'Chương I: Tập hợp các số tự nhiên', 'Bài 5. Phép nhân và phép chia', 'Phép toán số tự nhiên', 'Thực hiện phép nhân/chia số tự nhiên', 'Thông hiểu', 3)
add_lesson(mon, 'Chương I: Tập hợp các số tự nhiên', 'Bài 6. Luỹ thừa với số mũ tự nhiên', 'Lũy thừa', 'Tính giá trị biểu thức lũy thừa', 'Vận dụng', 2)
add_lesson(mon, 'Chương II: Tính chia hết', 'Bài 8. Quan hệ chia hết. Tính chất chia hết', 'Quan hệ chia hết', 'Nhận biết quan hệ chia hết', 'Nhận biết', 3)
add_lesson(mon, 'Chương II: Tính chia hết', 'Bài 9. Dấu hiệu chia hết', 'Dấu hiệu chia hết', 'Vận dụng dấu hiệu chia hết', 'Vận dụng', 3)
add_lesson(mon, 'Chương II: Tính chia hết', 'Bài 11. Số nguyên tố. Hợp số', 'Số nguyên tố', 'Phân biệt số nguyên tố, hợp số', 'Thông hiểu', 2)
add_lesson(mon, 'Chương II: Tính chia hết', 'Bài 12. Ước chung lớn nhất. Bội chung nhỏ nhất', 'ƯCLN và BCNN', 'Giải bài toán thực tế dùng ƯCLN/BCNN', 'Vận dụng cao', 2)
add_lesson(mon, 'Chương III: Số nguyên', 'Bài 14. Phép cộng và phép trừ số nguyên', 'Cộng/Trừ số nguyên', 'Thực hiện phép tính cộng, trừ số nguyên', 'Thông hiểu', 3)
add_lesson(mon, 'Chương III: Số nguyên', 'Bài 16. Phép nhân số nguyên', 'Phép nhân số nguyên', 'Áp dụng quy tắc nhân số nguyên', 'Thông hiểu', 2)
add_lesson(mon, 'Chương IV: Hình học thực tiễn', 'Bài 18. Hình tam giác đều. Hình vuông. Hình lục giác đều', 'Các hình cơ bản', 'Nhận biết đặc điểm các hình cơ bản', 'Nhận biết', 3)
add_lesson(mon, 'Chương IV: Hình học thực tiễn', 'Bài 20. Chu vi và diện tích', 'Tính diện tích', 'Tính chu vi/diện tích các hình đã học', 'Vận dụng', 2)

# --- TOÁN 7 - TẬP 1 (Chương I - V) ---
mon = 'Toán 7'
add_lesson(mon, 'Chương I: Số hữu tỉ', 'Bài 1. Tập hợp các số hữu tỉ', 'Khái niệm số hữu tỉ', 'Nhận biết số hữu tỉ và biểu diễn trên trục số', 'Nhận biết', 3)
add_lesson(mon, 'Chương I: Số hữu tỉ', 'Bài 2. Cộng, trừ, nhân, chia số hữu tỉ', 'Phép toán số hữu tỉ', 'Thực hiện các phép toán với số hữu tỉ', 'Thông hiểu', 4)
add_lesson(mon, 'Chương I: Số hữu tỉ', 'Bài 4. Quy tắc dấu ngoặc và quy tắc chuyển vế', 'Quy tắc đại số', 'Áp dụng quy tắc dấu ngoặc, chuyển vế', 'Thông hiểu', 3)
add_lesson(mon, 'Chương II: Số thực', 'Bài 6. Số vô tỉ. Căn bậc hai số học', 'Căn bậc hai', 'Tính toán với căn bậc hai số học', 'Thông hiểu', 2)
add_lesson(mon, 'Chương III: Góc và đường thẳng song song', 'Bài 8. Góc ở vị trí đặc biệt', 'Góc đặc biệt', 'Nhận biết và tính góc đối đỉnh, kề bù', 'Nhận biết', 3)
add_lesson(mon, 'Chương III: Góc và đường thẳng song song', 'Bài 9. Hai đường thẳng song song', 'Dấu hiệu song song', 'Sử dụng dấu hiệu nhận biết hai đường thẳng song song', 'Vận dụng', 3)
add_lesson(mon, 'Chương IV: Tam giác bằng nhau', 'Bài 12. Tổng các góc trong một tam giác', 'Tổng góc tam giác', 'Tính số đo góc tam giác', 'Thông hiểu', 2)
add_lesson(mon, 'Chương IV: Tam giác bằng nhau', 'Bài 13. Hai tam giác bằng nhau', 'Trường hợp bằng nhau c.c.c', 'Chứng minh hai tam giác bằng nhau theo c.c.c', 'Vận dụng', 3)
add_lesson(mon, 'Chương IV: Tam giác bằng nhau', 'Bài 15. Các trường hợp bằng nhau của tam giác vuông', 'Tam giác vuông', 'Chứng minh tam giác vuông bằng nhau', 'Vận dụng cao', 2)
add_lesson(mon, 'Chương V: Thu thập và biểu diễn dữ liệu', 'Bài 17. Thu thập và phân loại dữ liệu', 'Thống kê', 'Phân loại dữ liệu (định tính, định lượng)', 'Thông hiểu', 1)

# --- TOÁN 8 - TẬP 1 (Chương I - IV) ---
mon = 'Toán 8'
add_lesson(mon, 'Chương I: Đa thức', 'Bài 1. Đơn thức', 'Khái niệm đơn thức', 'Nhận biết đơn thức, bậc, hệ số', 'Nhận biết', 2)
add_lesson(mon, 'Chương I: Đa thức', 'Bài 3. Phép cộng và phép trừ đa thức', 'Cộng/Trừ đa thức', 'Thực hiện phép cộng, trừ đa thức', 'Thông hiểu', 3)
add_lesson(mon, 'Chương I: Đa thức', 'Bài 5. Phép nhân và phép chia đa thức', 'Nhân/Chia đa thức', 'Thực hiện phép nhân, chia đa thức', 'Thông hiểu', 3)
add_lesson(mon, 'Chương II: Hằng đẳng thức', 'Bài 6. Hiệu hai bình phương', 'HĐT cơ bản', 'Khai triển HĐT (A-B)(A+B)', 'Thông hiểu', 3)
add_lesson(mon, 'Chương II: Hằng đẳng thức', 'Bài 9. Phân tích đa thức thành nhân tử', 'Phân tích nhân tử', 'Phân tích đa thức thành nhân tử (dùng HĐT, đặt nhân tử chung)', 'Vận dụng', 4)
add_lesson(mon, 'Chương III: Tứ giác', 'Bài 10. Tứ giác', 'Tính chất tứ giác', 'Tính góc trong tứ giác', 'Nhận biết', 2)
add_lesson(mon, 'Chương III: Tứ giác', 'Bài 12. Hình thang cân', 'Hình đặc biệt', 'Nhận biết và tính chất hình thang cân', 'Thông hiểu', 2)
add_lesson(mon, 'Chương III: Tứ giác', 'Bài 14. Hình thoi và hình vuông', 'Hình đặc biệt', 'Chứng minh một tứ giác là hình thoi/hình vuông', 'Vận dụng', 3)
add_lesson(mon, 'Chương IV: Định lí Thalès', 'Bài 15. Định lí Thalès trong tam giác', 'Định lí Thalès', 'Vận dụng định lí Thalès để tính độ dài', 'Vận dụng', 3)
add_lesson(mon, 'Chương IV: Định lí Thalès', 'Bài 17. Tính chất đường phân giác', 'Đường phân giác', 'Áp dụng tính chất đường phân giác', 'Vận dụng cao', 2)

# --- TOÁN 9 - TẬP 1 (Chương I - IV) ---
mon = 'Toán 9'
add_lesson(mon, 'Chương I: Phương trình và Hệ phương trình', 'Bài 1. Khái niệm phương trình và hệ hai phương trình', 'Khái niệm hệ PT', 'Nhận biết nghiệm của hệ phương trình', 'Nhận biết', 2)
add_lesson(mon, 'Chương I: Phương trình và Hệ phương trình', 'Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn', 'Giải hệ PT', 'Giải hệ phương trình bằng phương pháp thế/cộng đại số', 'Thông hiểu', 4)
add_lesson(mon, 'Chương II: Căn bậc hai và Căn bậc ba', 'Bài 5. Căn bậc hai và căn thức bậc hai', 'Điều kiện có nghĩa', 'Tìm điều kiện xác định của căn thức', 'Nhận biết', 2)
add_lesson(mon, 'Chương II: Căn bậc hai và Căn bậc ba', 'Bài 7. Các phép biến đổi căn thức bậc hai', 'Rút gọn biểu thức', 'Thực hiện phép biến đổi và rút gọn biểu thức', 'Vận dụng', 4)
add_lesson(mon, 'Chương III: Hệ thức lượng trong tam giác vuông', 'Bài 10. Hệ thức về cạnh và đường cao', 'Hệ thức lượng', 'Áp dụng các hệ thức lượng trong tam giác vuông', 'Thông hiểu', 3)
add_lesson(mon, 'Chương III: Hệ thức lượng trong tam giác vuông', 'Bài 11. Tỉ số lượng giác của góc nhọn', 'Tỉ số lượng giác', 'Tính tỉ số lượng giác', 'Thông hiểu', 2)
add_lesson(mon, 'Chương IV: Đường tròn', 'Bài 13. Mở đầu về đường tròn', 'Đường tròn cơ bản', 'Xác định vị trí tương đối của điểm/đường thẳng với đường tròn', 'Nhận biết', 2)
add_lesson(mon, 'Chương IV: Đường tròn', 'Bài 17. Góc ở tâm. Số đo cung', 'Góc ở tâm', 'Tính số đo cung, góc ở tâm', 'Vận dụng', 3)
add_lesson(mon, 'Chương IV: Đường tròn', 'Bài 18. Góc nội tiếp', 'Góc nội tiếp', 'Chứng minh các hệ thức liên quan đến góc nội tiếp', 'Vận dụng cao', 2)

df = pd.DataFrame(full_data)
# -------------------- END: DỮ LIỆU MOCK ĐẦY ĐỦ --------------------


# -------------------- HÀM TẠO MA TRẬN THEO CV 7991 (PHỤ LỤC 1) --------------------

def create_ma_tran_cv7991(df_input, total_cau):
    """Tạo DataFrame Ma trận theo cấu trúc Phụ lục 1 của CV 7991."""
    
    df_temp = df_input.copy()
    
    # Cột ma trận 9 ô (NL: Nhiều lựa chọn, DS: Đúng - Sai, TL: Tự luận)
    matrix_cols_9 = [
        'NL - Biết', 'NL - Hiểu', 'NL - Vận dụng',
        'DS - Biết', 'DS - Hiểu', 'DS - Vận dụng',
        'TL - Biết', 'TL - Hiểu', 'TL - Vận dụng'
    ]
    
    for col in matrix_cols_9:
        df_temp[col] = 0
        
    # Ánh xạ số câu N_to_Take vào 9 cột ma trận (Giả định phân bổ cho Toán: NL/DS chiếm Biết/Hiểu, TL chiếm Vận dụng/Vận dụng cao)
    # Đây là mô hình giả lập, có thể cần điều chỉnh tỉ lệ dựa trên yêu cầu thực tế của từng trường
    
    # 60% Nhận biết -> NL - Biết (hoặc DS - Biết)
    df_temp.loc[df_temp['MucDo'] == 'Nhận biết', 'NL - Biết'] = (df_temp['N_to_Take'] * 0.6).apply(lambda x: max(1, math.floor(x))) 
    df_temp.loc[df_temp['MucDo'] == 'Nhận biết', 'DS - Biết'] = df_temp['N_to_Take'] - df_temp['NL - Biết']
    df_temp.loc[df_temp['MucDo'] == 'Nhận biết', 'NL - Biết'] = df_temp['NL - Biết'].apply(lambda x: x if x > 0 else 0) # Làm tròn và đảm bảo không âm

    # 60% Thông hiểu -> NL - Hiểu (hoặc DS - Hiểu)
    df_temp.loc[df_temp['MucDo'] == 'Thông hiểu', 'NL - Hiểu'] = (df_temp['N_to_Take'] * 0.6).apply(lambda x: max(1, math.floor(x)))
    df_temp.loc[df_temp['MucDo'] == 'Thông hiểu', 'DS - Hiểu'] = df_temp['N_to_Take'] - df_temp['NL - Hiểu']
    df_temp.loc[df_temp['MucDo'] == 'Thông hiểu', 'NL - Hiểu'] = df_temp['NL - Hiểu'].apply(lambda x: x if x > 0 else 0)
    
    # Vận dụng & Vận dụng cao -> TL - Vận dụng (Đây là giả định thường thấy cho các bài toán tổng hợp)
    df_temp.loc[df_temp['MucDo'].isin(['Vận dụng', 'Vận dụng cao']), 'TL - Vận dụng'] = df_temp['N_to_Take']

    # Nếu tổng N_to_Take của 1 hàng là 1, và được phân bổ thành 0.6 và 0.4, có thể bị làm tròn về 0. Cần đảm bảo tổng bằng N_to_Take
    df_temp['Current_Sum'] = df_temp[matrix_cols_9].sum(axis=1)
    df_temp['Diff'] = df_temp['N_to_Take'] - df_temp['Current_Sum']
    
    for index in df_temp.index:
        diff = df_temp.loc[index, 'Diff']
        if diff != 0:
            # Chỉ điều chỉnh cột không phải TL - Vận dụng
            if df_temp.loc[index, 'MucDo'] == 'Nhận biết':
                col_to_adjust = 'NL - Biết' if diff > 0 else 'DS - Biết' 
                df_temp.loc[index, col_to_adjust] += diff
            elif df_temp.loc[index, 'MucDo'] == 'Thông hiểu':
                col_to_adjust = 'NL - Hiểu' if diff > 0 else 'DS - Hiểu'
                df_temp.loc[index, col_to_adjust] += diff
                
    
    index_cols = ['ChuDe', 'NoiDung']
    
    pivot_table = pd.pivot_table(
        df_temp, 
        values=matrix_cols_9, 
        index=index_cols, 
        aggfunc='sum', 
        fill_value=0
    )
    
    # Phần tính tổng và điểm (Giữ nguyên logic cũ, đảm bảo tính đúng tỉ lệ % và điểm)
    pivot_table['Tổng số câu'] = pivot_table[matrix_cols_9].sum(axis=1)
    
    tong_so_cau_hang = pivot_table.sum().to_frame().T 

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
    
    if tong_diem > 0 and abs(diem_muc_do['Tổng'] - tong_diem) > 0.05:
        diff = tong_diem - diem_muc_do['Tổng']
        max_key = max(diem_muc_do, key=diem_muc_do.get)
        if max_key != 'Tổng':
            diem_muc_do[max_key] = round(diem_muc_do[max_key] + diff, 1)
        diem_muc_do['Tổng'] = tong_diem


    final_ma_tran = pivot_table.reset_index() 
    
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


# -------------------- CHỌN LỌC DỮ LIỆU ĐẦU VÀO (ĐÃ CẬP NHẬT MULTISELECT) --------------------

col1, col2 = st.columns(2)
with col1:
    mon_list = sorted(df['Mon'].unique())
    mon = st.selectbox("1. Chọn môn học:", mon_list, index=0) 
    
    df_mon = df[df['Mon']==mon]
    chuong_list = sorted(df_mon['Chuong'].unique())
    # CẬP NHẬT: Cho phép chọn nhiều Chương
    chuong = st.multiselect("2. Chọn các chương (có thể nhiều):", chuong_list, default=chuong_list)

with col2:
    # Lọc Bài theo các Chương đã chọn
    df_chuong = df_mon[df_mon['Chuong'].isin(chuong)]
    bai_list = sorted(df_chuong['Bai'].unique())
    # CẬP NHẬT: Cho phép chọn nhiều Bài
    bai = st.multiselect("3. Chọn các bài (có thể nhiều):", bai_list, default=bai_list)
    
    # Lọc Chủ đề theo các Bài đã chọn
    df_bai = df_chuong[df_chuong['Bai'].isin(bai)]
    chu_de_list = sorted(df_bai['ChuDe'].unique())
    chu_de = st.multiselect("4. Chọn Chủ đề/Nội dung (có thể nhiều):", chu_de_list, default=chu_de_list)

# Lọc DataFrame cuối cùng
df_filtered = df[(df['Mon']==mon) & 
                 (df['Chuong'].isin(chuong)) & 
                 (df['Bai'].isin(bai)) & 
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
        st.error("Lỗi: Không tìm thấy dữ liệu (Chương, Bài, Chủ đề) đã chọn hoặc Tổng tỉ lệ mức độ bằng 0%. Vui lòng kiểm tra lại các mục lựa chọn.")
        st.stop()

    # 1. Chuẩn hóa tỉ lệ và tính N_to_Take (Giữ nguyên logic phân bổ)
    normalized_ti_le = {md: percent / total_percent for md, percent in st.session_state.ti_le_muc_do_math.items()}
    required_q_by_level = {}
    remaining_total_q = so_cau_total
    levels = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
    
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
        
        df_filtered.loc[df_md_index, 'N_to_Take'] = df_filtered.loc[df_md_index, 'N_Needed'].apply(lambda x: round(x))
        
        df_filtered.loc[df_md_index, 'N_to_Take'] = df_filtered.apply(
            lambda row: min(row['N_to_Take'], row['SoCau']) if row['MucDo'] == md else row['N_to_Take'], axis=1)

        current_total_take = df_filtered.loc[df_md_index, 'N_to_Take'].sum()
        
        # Adjustment loop
        while current_total_take != n_cau_level:
            if current_total_take > n_cau_level:
                rows_to_adjust = df_filtered.loc[df_md_index].sort_values(by='N_to_Take', ascending=False).index.tolist()
                idx = next((i for i in rows_to_adjust if df_filtered.loc[i, 'N_to_Take'] > 0), None)
                if idx is None: break
                df_filtered.loc[idx, 'N_to_Take'] -= 1
            else: # current_total_take < n_cau_level
                rows_to_adjust = df_filtered.loc[df_md_index].sort_values(by='N_Needed', ascending=False).index.tolist()
                idx = next((i for i in rows_to_adjust if df_filtered.loc[i, 'N_to_Take'] < df_filtered.loc[i, 'SoCau']), None)
                if idx is None: break
                df_filtered.loc[idx, 'N_to_Take'] += 1
                
            current_total_take = df_filtered.loc[df_md_index, 'N_to_Take'].sum()
            if not df_md_index.any(): break
            
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
        st.write(f"Ma trận cho môn: **{mon}**, Tổng số câu: **{so_cau_total}**")
        st.dataframe(ma_tran_df_final, hide_index=True, use_container_width=True)
    else:
        st.error(f"Lỗi phân bổ: Số câu tạo được ({len(questions)}) **không khớp** với Tổng số câu yêu cầu ({so_cau_total}). Vui lòng thử lại với cấu hình khác, điều chỉnh tỉ lệ, hoặc chọn thêm Chủ đề.")
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
    
    output_text = ""
    for q in questions:
        st.markdown(q.replace('\n', '  \n')) 
        st.markdown("---")
        output_text += q + "\n" + "---" + "\n\n"

    # 6. Xuất Word (Bao gồm Ma trận và Bản Đặc tả)
    doc = Document()
    doc.add_heading(f"ĐỀ KIỂM TRA: {mon} - (Nhiều Chương/Bài)", 0)
    
    # --- Thêm Ma trận vào Word ---
    doc.add_heading("1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 1)", 2)
    
    num_rows = ma_tran_df_final.shape[0] + 2 
    num_cols = ma_tran_df_final.shape[1]
    table_ma_tran_word = doc.add_table(rows=num_rows, cols=num_cols)
    table_ma_tran_word.style = 'Table Grid'
    
    for j, (h1, h2) in enumerate(ma_tran_df_final.columns):
        table_ma_tran_word.cell(0, j).text = h1
        table_ma_tran_word.cell(1, j).text = h2
        
    table_ma_tran_word.cell(0, 0).merge(table_ma_tran_word.cell(0, 1)) 
    table_ma_tran_word.cell(0, 2).merge(table_ma_tran_word.cell(0, 4)) 
    table_ma_tran_word.cell(0, 5).merge(table_ma_tran_word.cell(0, 7)) 
    table_ma_tran_word.cell(0, 8).merge(table_ma_tran_word.cell(0, 10)) 
    
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
        file_name=f"De_Kiem_Tra_{mon}_TongHop_{so_cau_total}cau.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
