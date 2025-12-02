import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import math

st.set_page_config(page_title="Tạo đề Toán 6-9 theo SGK KNTT (CV 7991)", page_icon="📝", layout="wide")
st.title("📝 Tạo đề kiểm tra môn Toán (Lớp 6-9) theo CV 7991 (Cấu hình Thủ công)")

st.markdown("""
Hệ thống sử dụng ma trận câu hỏi mẫu được **tổng hợp đầy đủ từ mục lục sách giáo khoa Toán 6, 7, 8, 9 (Tập 1 - Kết nối tri thức với cuộc sống)**.
**👉 Vui lòng Chọn Chương/Bài và nhập số lượng câu hỏi mong muốn (từ 0 trở lên) trực tiếp vào bảng Ma trận bên dưới.**
""")

# -------------------- DỮ LIỆU MOCK THEO MỤC LỤC SGK TOÁN 6-9 KNTT TẬP 1 (Đầy đủ) --------------------
# *** (GIỮ NGUYÊN PHẦN KHAI BÁO full_data VÀ add_lesson) ***

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

# -------------------- HÀM TẠO MA TRẬN VÀ XUẤT ĐỀ (Đã chỉnh sửa) --------------------

def create_ma_tran_cv7991_manual(df_input_with_count):
    """Tạo DataFrame Ma trận theo cấu trúc Phụ lục 1 từ dữ liệu người dùng nhập."""
    
    df_temp = df_input_with_count.copy()
    
    # Cột ma trận 9 ô 
    matrix_cols_9 = [
        'NL - Biết', 'NL - Hiểu', 'NL - Vận dụng',
        'DS - Biết', 'DS - Hiểu', 'DS - Vận dụng',
        'TL - Biết', 'TL - Hiểu', 'TL - Vận dụng'
    ]
    
    # Tính Tổng số câu trên từng dòng (tổng 9 cột)
    df_temp['Tổng số câu'] = df_temp[matrix_cols_9].sum(axis=1)
    
    # Tạo Pivot Table (Ma trận)
    index_cols = ['ChuDe', 'NoiDung']
    pivot_table = df_temp.groupby(index_cols)[matrix_cols_9 + ['Tổng số câu']].sum()
    
    # Tính Tổng cuối cùng (Hàng Tổng)
    tong_so_cau_hang = pivot_table.sum().to_frame().T 

    # --- Tính Tỉ lệ & Điểm dựa trên tổng số câu đã nhập ---
    
    tong_cau = tong_so_cau_hang['Tổng số câu'].iloc[0]
    tong_diem = 10.0 # Giả định tổng điểm là 10.0

    # Tính Tổng số câu theo Mức độ (Biết, Hiểu, Vận dụng)
    tong_theo_muc_do = {}
    tong_theo_muc_do['Tổng Biết'] = tong_so_cau_hang[['NL - Biết', 'DS - Biết', 'TL - Biết']].sum(axis=1).iloc[0]
    tong_theo_muc_do['Tổng Hiểu'] = tong_so_cau_hang[['NL - Hiểu', 'DS - Hiểu', 'TL - Hiểu']].sum(axis=1).iloc[0]
    tong_theo_muc_do['Tổng Vận dụng'] = tong_so_cau_hang[['NL - Vận dụng', 'DS - Vận dụng', 'TL - Vận dụng']].sum(axis=1).iloc[0]
    
    # Tỉ lệ %
    ti_le_muc_do = {k: round((v / tong_cau) * 100, 1) if tong_cau > 0 else 0.0 for k, v in tong_theo_muc_do.items()}
    ti_le_muc_do['Tổng'] = round(sum(ti_le_muc_do.values()), 1)
    
    # Tính điểm
    diem_muc_do = {k: round((v / 100) * tong_diem, 1) for k, v in ti_le_muc_do.items() if k != 'Tổng'}
    diem_muc_do['Tổng'] = round(sum(diem_muc_do.values()), 1)
    
    # Điều chỉnh điểm để tổng là 10.0
    if tong_diem > 0 and abs(diem_muc_do['Tổng'] - tong_diem) > 0.05:
        diff = tong_diem - diem_muc_do['Tổng']
        # Điều chỉnh vào mức điểm Vận dụng (thường là mức độ cao nhất)
        max_key = 'Tổng Vận dụng' if 'Tổng Vận dụng' in diem_muc_do else max(diem_muc_do, key=diem_muc_do.get)
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
ma_tran_df_final = pd.DataFrame()
df_dac_ta_display = pd.DataFrame()
df_input_ma_tran = pd.DataFrame()

# -------------------- CHỌN LỌC DỮ LIỆU ĐẦU VÀO --------------------
st.subheader("1. Chọn Chủ đề và Nội dung")
col1, col2 = st.columns(2)
with col1:
    lop = st.selectbox("Chọn lớp:", ["6", "7", "8", "9"], index=0)
    mon = f"Toán {lop}"
    st.write(f"Chọn Môn: **{mon}**")
    df = pd.DataFrame(full_data) if isinstance(full_data, dict) else df
    df_mon = df[df['Mon']==mon]
    chuong_list = sorted(df_mon['Chuong'].unique())
    chuong = st.multiselect("Chọn các chương (có thể nhiều):", chuong_list, default=chuong_list)

with col2:
    df_chuong = df_mon[df_mon['Chuong'].isin(chuong)]
    bai_list = sorted(df_chuong['Bai'].unique())
    bai = st.multiselect("Chọn các bài (có thể nhiều):", bai_list, default=bai_list)
    
    df_bai = df_chuong[df_chuong['Bai'].isin(bai)]
    chu_de_list = sorted(df_bai['ChuDe'].unique())
    chu_de = st.multiselect("Chọn Chủ đề/Nội dung (có thể nhiều):", chu_de_list, default=chu_de_list)

# Lọc DataFrame cuối cùng và gộp các mức độ cho cùng 1 Nội dung
df_filtered = df[(df['Mon']==mon) & 
                 (df['Chuong'].isin(chuong)) & 
                 (df['Bai'].isin(bai)) & 
                 (df['ChuDe'].isin(chu_de))].copy().sort_values(by=['Chuong', 'Bai', 'ChuDe', 'MucDo'])

# Tạo khung dữ liệu cho người dùng nhập liệu
if not df_filtered.empty:
    
    # Chuẩn bị DataFrame cho Data Editor
    input_cols = [
        'Chuong', 'Bai', 'ChuDe', 'NoiDung', 'MucDo',
        'NL - Biết', 'NL - Hiểu', 'NL - Vận dụng',
        'DS - Biết', 'DS - Hiểu', 'DS - Vận dụng',
        'TL - Biết', 'TL - Hiểu', 'TL - Vận dụng'
    ]
    
    # Lấy các cột cơ bản và thêm cột nhập liệu (khởi tạo bằng 0)
    df_input_ma_tran = df_filtered.copy()
    for col in input_cols[5:]:
        df_input_ma_tran[col] = 0
        
    df_input_ma_tran = df_input_ma_tran[['Chuong', 'Bai', 'ChuDe', 'NoiDung', 'MucDo'] + input_cols[5:]]
    
    # -------------------- KHUNG NHẬP LIỆU MA TRẬN --------------------
    st.markdown("---")
    st.subheader("2. Nhập số lượng câu hỏi chi tiết vào Ma trận (KNTT CV 7991)")
    st.warning("⚠️ **Lưu ý:** Chỉ thay đổi các ô số câu (cột NL, DS, TL). Các cột Nội dung/Mức độ là cố định.")
    
    column_config = {
        'Chuong': st.column_config.TextColumn("Chương", disabled=True),
        'Bai': st.column_config.TextColumn("Bài", disabled=True),
        'ChuDe': st.column_config.TextColumn("Chủ đề", disabled=True),
        'NoiDung': st.column_config.TextColumn("Yêu cầu cần đạt", disabled=True),
        'MucDo': st.column_config.TextColumn("Mức độ", disabled=True),
        # Cấu hình các cột nhập liệu là số nguyên (min_value=0)
        **{col: st.column_config.NumberColumn(col, format="%d", min_value=0, step=1) for col in input_cols[5:]}
    }
    
    # Sử dụng st.data_editor để người dùng nhập liệu trực tiếp
    edited_df = st.data_editor(
        df_input_ma_tran,
        column_config=column_config,
        hide_index=True,
        use_container_width=True,
        key="ma_tran_editor"
    )

    # -------------------- XỬ LÝ KHI BẤM NÚT TẠO ĐỀ THỦ CÔNG --------------------
    st.markdown("---")
    if st.button("🚀 Tạo đề kiểm tra Thủ công", use_container_width=True):
        
        # Lấy dữ liệu đã chỉnh sửa
        df_final_input = edited_df.copy()
        
        # Loại bỏ các dòng mà người dùng nhập toàn bộ là 0 (để tránh làm phồng Đặc tả)
        cols_to_sum = input_cols[5:]
        df_final_input['Total_Input'] = df_final_input[cols_to_sum].sum(axis=1)
        df_with_n_take = df_final_input[df_final_input['Total_Input'] > 0].copy().drop(columns=['Total_Input'])
        
        final_total_questions = int(df_with_n_take[cols_to_sum].sum().sum())
        
        if final_total_questions == 0:
            st.error("Lỗi: Tổng số câu nhập vào Ma trận bằng 0. Vui lòng nhập số câu vào các ô cần thiết.")
            st.stop()
            
        # 3. HIỂN THỊ VÀ TẠO MA TRẬN ĐỀ KIỂM TRA (Phụ lục 1)
        st.subheader("📊 3. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ (Từ dữ liệu nhập)")
        
        ma_tran_df_final = create_ma_tran_cv7991_manual(df_with_n_take)
        st.write(f"Ma trận cho môn: **{mon}**, Tổng số câu: **{final_total_questions}**")
        st.dataframe(ma_tran_df_final, hide_index=True, use_container_width=True)
        
        # 4. HIỂN THỊ VÀ TẠO BẢN ĐẶC TẢ (Phụ lục 2 - Rút gọn)
        st.markdown("---")
        st.subheader("📑 4. BẢN ĐẶC TẢ ĐỀ KIỂM TRA ĐỊNH KÌ (Từ dữ liệu nhập)")
        
        # Chuẩn bị dữ liệu đặc tả (gộp 9 cột thành 1 cột "Số câu hỏi thực tế")
        df_dac_ta_display = df_with_n_take.copy()
        df_dac_ta_display['N_to_Take'] = df_dac_ta_display[cols_to_sum].sum(axis=1)
        
        df_dac_ta_display = df_dac_ta_display[['Mon', 'Chuong', 'Bai', 'ChuDe', 'NoiDung', 'MucDo', 'N_to_Take']].rename(columns={
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
        st.success(f"Đã tạo thành công cấu trúc cho {final_total_questions} câu hỏi theo cấu hình thủ công!")
        st.subheader("📄 5. ĐỀ KIỂM TRA TỰ ĐỘNG:")
        
        q_number = 1
        questions = []
        
        # TẠO NỘI DUNG CÂU HỎI
        for index, row in df_with_n_take.iterrows():
            total_row_q = int(row[cols_to_sum].sum())
            if total_row_q == 0: continue
            
            # Phân loại câu hỏi theo 9 ô ma trận đã nhập
            for col in cols_to_sum:
                n_q_in_cell = int(row[col])
                if n_q_in_cell > 0:
                    muc_do = col.split(' - ')[1].replace('Biết', 'Nhận biết').replace('Hiểu', 'Thông hiểu').replace('Vận dụng', 'Vận dụng/Vận dụng cao')
                    loai_cau_hoi = col.split(' - ')[0]
                    
                    if loai_cau_hoi == 'NL': loai_cau_hoi = 'Trắc nghiệm Nhiều Lựa chọn (NL)'
                    elif loai_cau_hoi == 'DS': loai_cau_hoi = 'Trắc nghiệm Đúng - Sai (DS)'
                    elif loai_cau_hoi == 'TL': loai_cau_hoi = 'Tự luận (TL)'
                    
                    for i in range(n_q_in_cell):
                        q_text = (f"Câu {q_number}. (Mức độ: {muc_do})\n"
                                    f"**Dạng: {loai_cau_hoi}**\n"
                                    f"Chủ đề: {row.get('ChuDe')} \n"
                                    f"Yêu cầu cần đạt: {row.get('NoiDung')}\n"
                                    f"→ (Lưu ý: Bạn cần thay thế Nội dung này bằng câu hỏi {loai_cau_hoi} thực tế.)\n"
                                    f"→ Hãy trình bày câu trả lời.")
                        questions.append(q_text)
                        q_number += 1


        output_text = ""
        for q in questions:
            st.markdown(q.replace('\n', '  \n')) 
            st.markdown("---")
            output_text += q + "\n" + "---" + "\n\n"

        # 6. Xuất Word (Bao gồm Ma trận và Bản Đặc tả)
        doc = Document()
        doc.add_heading(f"ĐỀ KIỂM TRA: {mon} - Thủ công ({final_total_questions} câu)", 0)
        
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
        try:
            table_ma_tran_word.cell(0, 0).merge(table_ma_tran_word.cell(0, 1)) 
            table_ma_tran_word.cell(0, 2).merge(table_ma_tran_word.cell(0, 4)) 
            table_ma_tran_word.cell(0, 5).merge(table_ma_tran_word.cell(0, 7)) 
            table_ma_tran_word.cell(0, 8).merge(table_ma_tran_word.cell(0, 10)) 
        except Exception:
            pass
        
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
            file_name=f"De_Kiem_Tra_{mon}_ThucOng_{final_total_questions}cau.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
else:
    st.info("Vui lòng chọn Chương và Bài để hiển thị các Chủ đề/Nội dung có thể cấu hình.")
