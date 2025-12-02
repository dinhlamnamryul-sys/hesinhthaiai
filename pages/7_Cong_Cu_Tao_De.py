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
        
    # --- Logic Giả lập phân bổ cho 9 ô Ma trận (để hoàn thiện theo CV 7991) ---
    # Giả định: 
    # - Biết/Hiểu: Phân bổ 60% cho Nhiều lựa chọn (NL) và 40% cho Đúng - Sai (DS).
    # - Vận dụng/Vận dụng cao: Tập trung vào Tự luận (TL).
    
    for md in ['Nhận biết', 'Thông hiểu']:
        
        # Lọc các dòng theo Mức độ
        df_md_index = df_temp[df_temp['MucDo'] == md].index
        
        # Xác định cột Biết/Hiểu trong NL và DS
        col_nl = f'NL - {md.replace("Nhận biết", "Biết").replace("Thông hiểu", "Hiểu")}'
        col_ds = f'DS - {md.replace("Nhận biết", "Biết").replace("Thông hiểu", "Hiểu")}'

        # Phân bổ tạm thời 60% NL, 40% DS (dùng hàm floor để tránh làm tròn quá sớm)
        df_temp.loc[df_md_index, col_nl] = (df_temp['N_to_Take'] * 0.6).apply(lambda x: math.floor(x))
        df_temp.loc[df_md_index, col_ds] = df_temp['N_to_Take'] - df_temp.loc[df_md_index, col_nl]
        
        # Điều chỉnh lại nếu tổng không khớp (do làm tròn) - đảm bảo NL + DS = N_to_Take
        for index in df_md_index:
            target = df_temp.loc[index, 'N_to_Take']
            current_sum = df_temp.loc[index, col_nl] + df_temp.loc[index, col_ds]
            diff = target - current_sum
            
            if diff != 0:
                # Ưu tiên dồn phần dư vào cột NL (chiếm tỉ lệ lớn hơn)
                df_temp.loc[index, col_nl] += diff
                # Đảm bảo không có số âm do phân bổ
                df_temp.loc[index, col_nl] = max(0, df_temp.loc[index, col_nl])
                df_temp.loc[index, col_ds] = max(0, df_temp.loc[index, col_ds])

    # Vận dụng/Vận dụng cao -> Tự luận (TL - Vận dụng)
    df_vd_index = df_temp[df_temp['MucDo'].isin(['Vận dụng', 'Vận dụng cao'])].index
    df_temp.loc[df_vd_index, 'TL - Vận dụng'] = df_temp['N_to_Take']
    
    
    index_cols = ['ChuDe', 'NoiDung']
    
    # Tạo Pivot Table (Ma trận)
    pivot_table = pd.pivot_table(
        df_temp, 
        values=matrix_cols_9, 
        index=index_cols, 
        aggfunc='sum', 
        fill_value=0
    )
    
    # Tính Tổng số câu trên từng dòng
    pivot_table['Tổng số câu'] = pivot_table[matrix_cols_9].sum(axis=1)
    
    # Tính Tổng cuối cùng (Hàng Tổng)
    tong_so_cau_hang = pivot_table.sum().to_frame().T 

    # Tính Tổng theo Mức độ (Biết, Hiểu, Vận dụng - gộp 3 cột NL/DS/TL)
    tong_theo_muc_do = {}
    tong_theo_muc_do['Tổng Biết'] = tong_so_cau_hang[['NL - Biết', 'DS - Biết', 'TL - Biết']].sum(axis=1).iloc[0]
    tong_theo_muc_do['Tổng Hiểu'] = tong_so_cau_hang[['NL - Hiểu', 'DS - Hiểu', 'TL - Hiểu']].sum(axis=1).iloc[0]
    tong_theo_muc_do['Tổng Vận dụng'] = tong_so_cau_hang[['NL - Vận dụng', 'DS - Vận dụng', 'TL - Vận dụng']].sum(axis=1).iloc[0]
    
    tong_cau = tong_so_cau_hang['Tổng số câu'].iloc[0]
    ti_le_muc_do = {k: round((v / tong_cau) * 100, 1) if tong_cau > 0 else 0.0 for k, v in tong_theo_muc_do.items()}
    ti_le_muc_do['Tổng'] = round(sum(ti_le_muc_do.values()), 1)
    
    # Tính điểm
    tong_diem = 10.0
    diem_muc_do = {k: round((v / 100) * tong_diem, 1) for k, v in ti_le_muc_do.items() if k != 'Tổng'}
    diem_muc_do['Tổng'] = round(sum(diem_muc_do.values()), 1)
    
    # Điều chỉnh điểm để tổng là 10.0
    if tong_diem > 0 and abs(diem_muc_do['Tổng'] - tong_diem) > 0.05:
        diff = tong_diem - diem_muc_do['Tổng']
        max_key = max(diem_muc_do, key=diem_muc_do.get)
        if max_key != 'Tổng':
            diem_muc_do[max_key] = round(diem_muc_do[max_key] + diff, 1)
        diem_muc_do['Tổng'] = tong_diem


    final_ma_tran = pivot_table.reset_index() 
    new_cols = ['Chủ đề', 'Nội dung'] + list(pivot_table.columns) 
    final_ma_tran.columns = new_cols 

    # Thêm 3 hàng tóm tắt: Tổng số câu, Tỉ lệ %, Điểm (10đ)
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
    
    # Điền giá trị vào các ô tổng cuối cùng
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

so_cau_total = st.number_input("5. Tổng số câu muốn tạo:", min_value=1, max_value=100, value=30)

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

    # 1. Chuẩn hóa tỉ lệ và tính N_to_Take
    normalized_ti_le = {md: percent / total_percent for md, percent in st.session_state.ti_le_muc_do_math.items()}
    required_q_by_level = {}
    remaining_total_q = so_cau_total
    levels = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
    
    for i, md in enumerate(levels):
        ratio = normalized_ti_le.get(md, 0)
        # Tính số câu cần (round)
        required_q = round(so_cau_total * ratio)
        required_q_by_level[md] = required_q
    
    # Điều chỉnh đảm bảo tổng số câu bằng so_cau_total (giải quyết sai số làm tròn)
    current_total_q = sum(required_q_by_level.values())
    diff = so_cau_total - current_total_q
    
    # Điều chỉnh vào mức độ có tỉ lệ cao nhất (hoặc Vận dụng/Thông hiểu)
    if diff != 0:
        if 'Thông hiểu' in required_q_by_level:
            required_q_by_level['Thông hiểu'] += diff
        elif 'Nhận biết' in required_q_by_level:
            required_q_by_level['Nhận biết'] += diff
            
    # Đảm bảo không có số âm
    required_q_by_level = {k: max(0, v) for k, v in required_q_by_level.items()}


    df_filtered['N_to_Take'] = 0
    questions = []
    q_number = 1
    
    # 2. Phân bổ câu hỏi và Tạo nội dung đề (TÍNH TOÁN BẮT BUỘC TRƯỚC KHI TẠO MA TRẬN)
    for md in levels:
        n_cau_level = required_q_by_level.get(md, 0)
        if n_cau_level <= 0: continue

        df_md_index = df_filtered[df_filtered['MucDo'] == md].index
        if df_md_index.empty: continue

        total_available_points = df_filtered.loc[df_md_index, 'SoCau'].sum()
        
        # Nếu tổng số câu tối đa có thể lấy ở mức độ này nhỏ hơn số câu cần, phải giới hạn
        if total_available_points < n_cau_level:
            st.warning(f"Cảnh báo: Mức độ **{md}** chỉ có tối đa **{total_available_points}** câu tiềm năng. Hệ thống sẽ giảm số câu cần xuống mức tối đa này. (Yêu cầu: {n_cau_level} câu)")
            n_cau_level = total_available_points
        
        if total_available_points == 0: continue
        
        # Proportional calculation (Tính N_Needed trước)
        df_filtered.loc[df_md_index, 'N_Needed'] = (df_filtered.loc[df_md_index, 'SoCau'] / total_available_points) * n_cau_level
        
        # Phân bổ N_to_Take (Làm tròn)
        df_filtered.loc[df_md_index, 'N_to_Take'] = df_filtered.loc[df_md_index, 'N_Needed'].apply(lambda x: round(x))
        
        # Đảm bảo N_to_Take không vượt quá SoCau
        df_filtered.loc[df_md_index, 'N_to_Take'] = df_filtered.apply(
            lambda row: min(row['N_to_Take'], row['SoCau']) if row['MucDo'] == md else row['N_to_Take'], axis=1)

        current_total_take = df_filtered.loc[df_md_index, 'N_to_Take'].sum()
        
        # Adjustment loop (Điều chỉnh lần cuối để tổng khớp với n_cau_level)
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
            
    # Lấy các câu hỏi đã được phân bổ
    df_with_n_take = df_filtered[df_filtered['N_to_Take'] > 0].copy()
    
    # Tính tổng số câu cuối cùng sau khi phân bổ (Có thể nhỏ hơn so_cau_total nếu bị giới hạn)
    final_total_questions = int(df_with_n_take['N_to_Take'].sum())

    if final_total_questions < so_cau_total:
        st.error(f"Lỗi phân bổ: Số câu tạo được ({final_total_questions}) **không khớp** với Tổng số câu yêu cầu ({so_cau_total}). Vui lòng **chọn thêm Chương/Bài/Chủ đề** để tăng nguồn câu hỏi hoặc **giảm Tổng số câu** yêu cầu.")
        st.stop()
        
    # 3. HIỂN THỊ VÀ TẠO MA TRẬN ĐỀ KIỂM TRA (Phụ lục 1)
    st.markdown("---")
    st.subheader("📊 1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 1 - CV 7991)")
    
    ma_tran_df_final = create_ma_tran_cv7991(df_with_n_take, final_total_questions)
    st.write(f"Ma trận cho môn: **{mon}**, Tổng số câu: **{final_total_questions}**")
    st.dataframe(ma_tran_df_final, hide_index=True, use_container_width=True)
    
    # 4. HIỂN THỊ VÀ TẠO BẢN ĐẶC TẢ (Phụ lục 2 - Rút gọn)
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

    # 5. TẠO VÀ HIỂN THỊ ĐỀ KIỂM TRA
    # Generate question text
    q_number = 1
    for md in levels:
        for index, row in df_with_n_take[df_with_n_take['MucDo']==md].iterrows():
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
                
    st.success(f"Đã tạo thành công {final_total_questions} câu hỏi theo cấu trúc CV 7991!")
    st.subheader("📄 3. ĐỀ KIỂM TRA TỰ ĐỘNG:")
    
    output_text = ""
    for q in questions:
        st.markdown(q.replace('\n', '  \n')) 
        st.markdown("---")
        output_text += q + "\n" + "---" + "\n\n"

    # 6. Xuất Word (Bao gồm Ma trận và Bản Đặc tả)
    doc = Document()
    doc.add_heading(f"ĐỀ KIỂM TRA: {mon} - Tổng hợp ({final_total_questions} câu)", 0)
    
    # --- Thêm Ma trận vào Word ---
    doc.add_heading("1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 1)", 2)
    
    num_rows = ma_tran_df_final.shape[0] + 2 
    num_cols = ma_tran_df_final.shape[1]
    table_ma_tran_word = doc.add_table(rows=num_rows, cols=num_cols)
    table_ma_tran_word.style = 'Table Grid'
    
    for j, (h1, h2) in enumerate(ma_tran_df_final.columns):
        table_ma_tran_word.cell(0, j).text = h1
        table_ma_tran_word.cell(1, j).text = h2
        
    # Merge cells cho header Multi-Index
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
        file_name=f"De_Kiem_Tra_{mon}_TongHop_{final_total_questions}cau.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
