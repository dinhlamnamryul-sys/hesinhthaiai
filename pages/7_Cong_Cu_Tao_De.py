import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import math

st.set_page_config(page_title="Tạo đề Toán 6-9 (Tối giản & Chuẩn Output)", page_icon="📝", layout="wide")
st.title("📝 Tạo đề kiểm tra môn Toán (Tối giản - Theo CV 7991 & Format Mẫu)")

st.markdown("""
Hệ thống sử dụng dữ liệu mục lục SGK Toán 6-9 KNTT.
**🔥 Yêu cầu của bạn: Thao tác tối thiểu!**
Bạn chỉ cần chọn **Lớp** và **Chương**; hệ thống sẽ tự động phân bổ **21 câu hỏi** (10 điểm, tỉ lệ điểm 25/25/50) vào các nội dung đã chọn và tạo Ma trận/Đặc tả/Đề thi & Đáp án theo format chuẩn.
""")

# -------------------- DỮ LIỆU MOCK (Đã sửa lỗi TypeError) --------------------
full_data = {
    'Mon': [], 'Chuong': [], 'Bai': [], 'ChuDe': [], 'NoiDung': [], 'MucDo': [], 'SoCau': []
}

def add_lesson(mon, chuong, bai, chude, noidung, mucdo, socau):
    """Hàm thêm dữ liệu với 7 tham số: Môn, Chương, Bài, Chủ đề, Nội dung, Mức độ, Số câu."""
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
add_lesson(mon, 'Chương I: Tập hợp các số tự nhiên', 'Bài 4. Phép cộng và phép trừ', 'Phép toán số tự nhiên', 'Thực hiện phép cộng/trừ số tự nhiên', 'Thông hiểu', 4)
add_lesson(mon, 'Chương I: Tập hợp các số tự nhiên', 'Bài 6. Luỹ thừa với số mũ tự nhiên', 'Lũy thừa', 'Tính giá trị biểu thức lũy thừa', 'Vận dụng', 2)
add_lesson(mon, 'Chương II: Tính chia hết', 'Bài 9. Dấu hiệu chia hết', 'Dấu hiệu chia hết', 'Vận dụng dấu hiệu chia hết', 'Vận dụng', 3)
add_lesson(mon, 'Chương II: Tính chia hết', 'Bài 12. Ước chung lớn nhất. Bội chung nhỏ nhất', 'ƯCLN và BCNN', 'Giải bài toán thực tế dùng ƯCLN/BCNN', 'Vận dụng cao', 2)
add_lesson(mon, 'Chương III: Số nguyên', 'Bài 14. Phép cộng và phép trừ số nguyên', 'Cộng/Trừ số nguyên', 'Thực hiện phép tính cộng, trừ số nguyên', 'Thông hiểu', 3)
add_lesson(mon, 'Chương IV: Hình học thực tiễn', 'Bài 20. Chu vi và diện tích', 'Tính diện tích', 'Tính chu vi/diện tích các hình đã học', 'Vận dụng', 2)

# --- TOÁN 7 - TẬP 1 (Chương I - V) ---
mon = 'Toán 7'
add_lesson(mon, 'Chương I: Số hữu tỉ', 'Bài 2. Cộng, trừ, nhân, chia số hữu tỉ', 'Phép toán số hữu tỉ', 'Thực hiện các phép toán với số hữu tỉ', 'Thông hiểu', 4)
# Dòng lỗi (Sửa lỗi thiếu tham số): Thêm Chủ đề 'Đường thẳng song song'
add_lesson(mon, 'Chương III: Góc và đường thẳng song song', 'Bài 9. Hai đường thẳng song song', 'Đường thẳng song song', 'Sử dụng dấu hiệu nhận biết hai đường thẳng song song', 'Vận dụng', 3)
# Dòng lỗi (Sửa lỗi thiếu tham số): Thêm Chủ đề 'Tam giác bằng nhau'
add_lesson(mon, 'Chương IV: Tam giác bằng nhau', 'Bài 13. Hai tam giác bằng nhau', 'Tam giác bằng nhau', 'Chứng minh hai tam giác bằng nhau theo c.c.c', 'Vận dụng', 3)

# --- TOÁN 8 - TẬP 1 (Chương I - IV) ---
mon = 'Toán 8'
add_lesson(mon, 'Chương I: Đa thức', 'Bài 3. Phép cộng và phép trừ đa thức', 'Cộng/Trừ đa thức', 'Thực hiện phép tính cộng, trừ đa thức', 'Thông hiểu', 3)
add_lesson(mon, 'Chương II: Hằng đẳng thức', 'Bài 9. Phân tích đa thức thành nhân tử', 'Phân tích nhân tử', 'Phân tích đa thức thành nhân tử (dùng HĐT, đặt nhân tử chung)', 'Vận dụng', 4)
add_lesson(mon, 'Chương III: Tứ giác', 'Bài 14. Hình thoi và hình vuông', 'Hình đặc biệt', 'Chứng minh một tứ giác là hình thoi/hình vuông', 'Vận dụng', 3)

# --- TOÁN 9 - TẬP 1 (Chương I - IV) ---
mon = 'Toán 9'
add_lesson(mon, 'Chương I: Phương trình và Hệ phương trình', 'Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn', 'Giải hệ PT', 'Giải hệ phương trình bằng phương pháp thế/cộng đại số', 'Thông hiểu', 4)
add_lesson(mon, 'Chương II: Căn bậc hai và Căn bậc ba', 'Bài 7. Các phép biến đổi căn thức bậc hai', 'Rút gọn biểu thức', 'Thực hiện phép biến đổi và rút gọn biểu thức', 'Vận dụng', 4)
add_lesson(mon, 'Chương III: Hệ thức lượng trong tam giác vuông', 'Bài 10. Hệ thức về cạnh và đường cao', 'Hệ thức lượng', 'Áp dụng các hệ thức lượng trong tam giác vuông', 'Thông hiểu', 3)

df = pd.DataFrame(full_data)
# -------------------- END: DỮ LIỆU MOCK --------------------

# -------------------- HÀM TẠO MA TRẬN VÀ PHÂN BỔ (GIỮ NGUYÊN LOGIC) --------------------

def create_ma_tran_cv7991_fixed_auto(df_input):
    """Tạo Ma trận và phân bổ cố định 21 câu: 6 NB, 8 TH, 7 VĐ/VDC. (Logic giữ nguyên)"""
    
    df_temp = df_input.copy()
    
    required_q_by_level = {
        'Nhận biết': 6, 'Thông hiểu': 8, 'Vận dụng': 4, 'Vận dụng cao': 3
    }
    TOTAL_NL = 12; TOTAL_DS = 2 
    matrix_cols_9 = [
        'NL - Biết', 'NL - Hiểu', 'NL - Vận dụng',
        'DS - Biết', 'DS - Hiểu', 'DS - Vận dụng',
        'TL - Biết', 'TL - Hiểu', 'TL - Vận dụng'
    ]
    
    # 1. Phân bổ N_to_Take
    df_temp['N_to_Take'] = 0
    levels = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
    
    for md in levels:
        n_cau_level = required_q_by_level.get(md, 0)
        if n_cau_level <= 0: continue

        df_md_index = df_temp[df_temp['MucDo'].str.contains(md.split()[0], case=False)].index
        if df_md_index.empty: continue

        total_available_points = df_temp.loc[df_md_index, 'SoCau'].sum()
        if total_available_points == 0: continue
        
        n_cau_level = min(n_cau_level, total_available_points)
        
        df_temp.loc[df_md_index, 'N_Needed'] = (df_temp.loc[df_md_index, 'SoCau'] / total_available_points) * n_cau_level
        df_temp.loc[df_md_index, 'N_to_Take'] = df_temp.loc[df_md_index, 'N_Needed'].apply(lambda x: round(x))
        
        current_total_take = df_temp.loc[df_md_index, 'N_to_Take'].sum()
        while current_total_take != n_cau_level:
            if current_total_take > n_cau_level:
                rows_to_adjust = df_temp.loc[df_md_index].sort_values(by='N_to_Take', ascending=False).index.tolist()
                idx = next((i for i in rows_to_adjust if df_temp.loc[i, 'N_to_Take'] > 0), None)
                if idx is None: break
                df_temp.loc[idx, 'N_to_Take'] -= 1
            else: # current_total_take < n_cau_level
                rows_to_adjust = df_temp.loc[df_md_index].sort_values(by='N_Needed', ascending=False).index.tolist()
                idx = next((i for i in rows_to_adjust if df_temp.loc[i, 'N_to_Take'] < df_temp.loc[i, 'SoCau']), None)
                if idx is None: break
                df_temp.loc[idx, 'N_to_Take'] += 1
                
            current_total_take = df_temp.loc[df_md_index, 'N_to_Take'].sum()
            if not df_md_index.any(): break
            
    df_with_n_take = df_temp[df_temp['N_to_Take'] > 0].copy()
    
    # 2. Phân bổ 9 ô Ma trận
    for col in matrix_cols_9:
        df_with_n_take[col] = 0
        
    df_vd_index = df_with_n_take[df_with_n_take['MucDo'].isin(['Vận dụng', 'Vận dụng cao'])].index
    df_with_n_take.loc[df_vd_index, 'TL - Vận dụng'] = df_with_n_take.loc[df_vd_index, 'N_to_Take'] 

    df_nb_index = df_with_n_take[df_with_n_take['MucDo'] == 'Nhận biết'].index
    n_nb_total = df_with_n_take.loc[df_nb_index, 'N_to_Take'].sum() 
    
    if n_nb_total > 0:
        ratio_to_total_nb = df_with_n_take.loc[df_nb_index, 'N_to_Take'] / n_nb_total
        n_nb_nl = round(n_nb_total * (12/14)) 
        n_nb_ds = n_nb_total - n_nb_nl
        
        n_nb_nl = min(n_nb_nl, 12); n_nb_ds = min(n_nb_ds, 2)
        
        df_with_n_take.loc[df_nb_index, 'NL - Biết'] = (ratio_to_total_nb * n_nb_nl).apply(lambda x: math.floor(x))
        df_with_n_take.loc[df_nb_index, 'DS - Biết'] = (ratio_to_total_nb * n_nb_ds).apply(lambda x: math.floor(x))
        for index in df_nb_index:
            diff = df_with_n_take.loc[index, 'N_to_Take'] - (df_with_n_take.loc[index, 'NL - Biết'] + df_with_n_take.loc[index, 'DS - Biết'])
            df_with_n_take.loc[index, 'NL - Biết'] += diff 
            df_with_n_take.loc[index, 'NL - Biết'] = max(0, df_with_n_take.loc[index, 'NL - Biết'])
            df_with_n_take.loc[index, 'DS - Biết'] = max(0, df_with_n_take.loc[index, 'DS - Biết'])
                
    df_th_index = df_with_n_take[df_with_n_take['MucDo'] == 'Thông hiểu'].index
    n_th_total = df_with_n_take.loc[df_th_index, 'N_to_Take'].sum()
    
    n_th_nl = TOTAL_NL - df_with_n_take['NL - Biết'].sum()
    n_th_ds = TOTAL_DS - df_with_n_take['DS - Biết'].sum()
    
    if n_th_total > 0:
        ratio_to_total_th = df_with_n_take.loc[df_th_index, 'N_to_Take'] / n_th_total
        
        df_with_n_take.loc[df_th_index, 'NL - Hiểu'] = (ratio_to_total_th * n_th_nl).apply(lambda x: math.floor(x))
        df_with_n_take.loc[df_th_index, 'DS - Hiểu'] = (ratio_to_total_th * n_th_ds).apply(lambda x: math.floor(x))
        for index in df_th_index:
            diff = df_with_n_take.loc[index, 'N_to_Take'] - (df_with_n_take.loc[index, 'NL - Hiểu'] + df_with_n_take.loc[index, 'DS - Hiểu'])
            df_with_n_take.loc[index, 'NL - Hiểu'] += diff 
            df_with_n_take.loc[index, 'NL - Hiểu'] = max(0, df_with_n_take.loc[index, 'NL - Hiểu'])
            df_with_n_take.loc[index, 'DS - Hiểu'] = max(0, df_with_n_take.loc[index, 'DS - Hiểu'])

    # 3. Tạo Ma trận hiển thị và Tính tổng/điểm
    index_cols = ['ChuDe', 'NoiDung']
    pivot_table = pd.pivot_table(
        df_with_n_take, 
        values=matrix_cols_9, 
        index=index_cols, 
        aggfunc='sum', 
        fill_value=0
    )
    
    pivot_table['Tổng số câu'] = pivot_table[matrix_cols_9].sum(axis=1)
    tong_so_cau_hang = pivot_table.sum().to_frame().T 

    ti_le_muc_do = {'Tổng Biết': 25.0, 'Tổng Hiểu': 25.0, 'Tổng Vận dụng': 50.0, 'Tổng': 100.0}
    diem_muc_do = {'Tổng Biết': 2.5, 'Tổng Hiểu': 2.5, 'Tổng Vận dụng': 5.0, 'Tổng': 10.0}

    final_ma_tran = pivot_table.reset_index() 
    new_cols = ['Chủ đề', 'Nội dung'] + list(pivot_table.columns) 
    final_ma_tran.columns = new_cols 

    summary_data = [
        {'Chủ đề': 'Tổng số câu', 'Nội dung': '', **{col: tong_so_cau_hang[col].iloc[0] for col in pivot_table.columns}},
        {'Chủ đề': 'Tỉ lệ %', 'Nội dung': '', **{col: '' for col in pivot_table.columns}},
        {'Chủ đề': 'Điểm (10đ)', 'Nội dung': '', **{col: '' for col in pivot_table.columns}},
    ]
    summary_df = pd.DataFrame(summary_data, columns=final_ma_tran.columns)
    final_ma_tran = pd.concat([final_ma_tran, summary_df], ignore_index=True)
    
    idx_ti_le = final_ma_tran[final_ma_tran['Chủ đề'] == 'Tỉ lệ %'].index[0]
    idx_diem = final_ma_tran[final_ma_tran['Chủ đề'] == 'Điểm (10đ)'].index[0]
    tong_cau_final = tong_so_cau_hang['Tổng số câu'].iloc[0]
    
    final_ma_tran.loc[final_ma_tran['Chủ đề'] == 'Tổng số câu', 'Nội dung'] = str(tong_cau_final) 
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
    
    header_1_data = ['Nội dung/Đơn vị kiến thức', 'Nội dung/Đơn vị kiến thức'] + ['Nhiều lựa chọn'] * 3 + ['Đúng - Sai'] * 3 + ['Tự luận'] * 3 + ['Tổng']
    header_2_data = ['Chủ đề', 'Nội dung'] + ['Biết', 'Hiểu', 'VĐ'] * 3 + ['Số câu/điểm']
    final_ma_tran.columns = pd.MultiIndex.from_arrays([header_1_data, header_2_data])
    
    return final_ma_tran.astype(str).replace('0', '').replace('nan', ''), df_with_n_take

# -------------------- GIAO DIỆN TỐI GIẢN --------------------

col1, col2 = st.columns([1, 2])
with col1:
    lop = st.selectbox("1️⃣ Chọn lớp:", ["6", "7", "8", "9"], index=0)
    mon = f"Toán {lop}"
    df_mon = df[df['Mon']==mon]
    chuong_list = sorted(df_mon['Chuong'].unique())
    chuong = st.multiselect("2️⃣ Chọn các chương:", chuong_list, default=chuong_list)

with col2:
    st.markdown("""
    ### ⚙️ Cấu hình Tự động (CV 7991)
    Hệ thống sẽ tạo **21 câu hỏi** (Tổng 10 điểm) với phân bổ cố định:
    * **Phần I (NL):** 12 câu.
    * **Phần II (DS):** 2 câu (4 ý).
    * **Phần III (Trả lời ngắn):** 4 câu.
    * **Phần B (Tự luận):** 3 câu.
    """)

# Lọc DataFrame cuối cùng
df_filtered = df[(df['Mon']==mon) & 
                 (df['Chuong'].isin(chuong))].copy()

st.markdown("---")
if st.button("🚀 3️⃣ Bấm TẠO ĐỀ KIỂM TRA TỰ ĐỘNG", use_container_width=True, type="primary"):
    
    if df_filtered.empty:
        st.error("Lỗi: Không tìm thấy dữ liệu trong Chương đã chọn. Vui lòng kiểm tra lại mục lựa chọn.")
        st.stop()
        
    ma_tran_df_final, df_with_n_take = create_ma_tran_cv7991_fixed_auto(df_filtered)
    final_total_questions = int(ma_tran_df_final[('Tổng', 'Số câu/điểm')].iloc[-3])

    if final_total_questions < 21:
        st.warning(f"Cảnh báo: Chỉ tạo được **{final_total_questions}** câu (thiếu {21-final_total_questions} câu) do nguồn câu hỏi tiềm năng bị giới hạn. Vui lòng chọn thêm Chương/Bài.")

    if final_total_questions == 0:
        st.error("Lỗi phân bổ: Không thể tạo được câu hỏi nào từ nội dung đã chọn.")
        st.stop()
        
    st.success(f"Đã tạo thành công {final_total_questions} câu hỏi theo cấu trúc CV 7991 tối giản!")

    
    # 1. HIỂN THỊ MA TRẬN
    st.markdown("---")
    st.subheader("📊 1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ")
    st.dataframe(ma_tran_df_final, hide_index=True, use_container_width=True)
    
    # 2. HIỂN THỊ BẢN ĐẶC TẢ 
    st.markdown("---")
    st.subheader("📑 2. BẢN ĐẶC TẢ ĐỀ KIỂM TRA ĐỊNH KÌ (Rút gọn)")
    df_dac_ta_display = df_with_n_take[['Mon', 'Chuong', 'Bai', 'ChuDe', 'NoiDung', 'MucDo', 'N_to_Take']].rename(columns={
        'Mon': 'Môn', 'Chuong': 'Chương', 'Bai': 'Bài', 'ChuDe': 'Chủ đề', 'NoiDung': 'Yêu cầu cần đạt', 'MucDo': 'Mức độ', 'N_to_Take': 'Số câu hỏi thực tế'
    })
    st.dataframe(df_dac_ta_display.astype(str), hide_index=True, use_container_width=True)

    # 3. PHÂN LOẠI CÂU HỎI VÀ TẠO CHUỖI ĐỀ & ĐÁP ÁN
    
    # Lấy tổng số câu của mỗi loại từ Ma trận (đã phân bổ)
    ma_tran_summary = ma_tran_df_final.iloc[-3]
    NL_count = int(ma_tran_summary[('Nhiều lựa chọn', 'Biết')]) + int(ma_tran_summary[('Nhiều lựa chọn', 'Hiểu')]) + int(ma_tran_summary[('Nhiều lựa chọn', 'VĐ')])
    DS_count = int(ma_tran_summary[('Đúng - Sai', 'Biết')]) + int(ma_tran_summary[('Đúng - Sai', 'Hiểu')]) + int(ma_tran_summary[('Đúng - Sai', 'VĐ')])
    TL_count = int(ma_tran_summary[('Tự luận', 'Biết')]) + int(ma_tran_summary[('Tự luận', 'Hiểu')]) + int(ma_tran_summary[('Tự luận', 'VĐ')])
    
    # Tách 7 câu TL thành 4 TLN và 3 TL Essay (nếu đủ câu)
    TLN_count = min(TL_count, 4) 
    TL_Essay_count = max(0, TL_count - TLN_count)

    questions_list = [] # Danh sách tổng hợp
    q_number_global = 1
    
    # Phân loại câu hỏi theo 9 ô ma trận đã nhập
    cols_to_check = [col for col in df_with_n_take.columns if any(s in col for s in ['NL -', 'DS -', 'TL -'])]
    
    for index, row in df_with_n_take.iterrows():
        for col in cols_to_check:
            n_q_in_cell = int(row[col])
            if n_q_in_cell > 0:
                muc_do = col.split(' - ')[1].replace('Biết', 'Nhận biết').replace('Hiểu', 'Thông hiểu').replace('Vận dụng', 'Vận dụng/Vận dụng cao')
                loai_cau_hoi = col.split(' - ')[0]
                
                for i in range(n_q_in_cell):
                    questions_list.append({
                        'Q_ID': 0, 
                        'Type': loai_cau_hoi,
                        'MucDo': muc_do,
                        'ChuDe': row.get('ChuDe'),
                        'NoiDung': row.get('NoiDung')
                    })

    # Sắp xếp và đánh số lại theo thứ tự ưu tiên NL -> DS -> TL
    
    NL_questions = [q for q in questions_list if q['Type'] == 'NL'][:12]
    DS_questions_raw = [q for q in questions_list if q['Type'] == 'DS'][:DS_count]
    TL_questions_raw = [q for q in questions_list if q['Type'] == 'TL'][:TL_count]
    
    # Tách VĐ/VDC thành TLN và TL Essay
    TLN_questions = TL_questions_raw[:TLN_count]
    TL_Essay_questions = TL_questions_raw[TLN_count:TLN_count + TL_Essay_count]
    
    # Danh sách tổng hợp cuối cùng để đánh số
    final_q_list_sorted = NL_questions + DS_questions_raw + TLN_questions + TL_Essay_questions
    
    for i, q in enumerate(final_q_list_sorted):
        q['Q_ID'] = i + 1

    # --- Bắt đầu tạo nội dung Đề và Đáp án ---
    
    de_parts = []
    ans_parts = []
    
    # Phần I: Trắc nghiệm khách quan nhiều lựa chọn (NL)
    if NL_questions:
        diem_nl = 3.0 / 12 * len(NL_questions) 
        de_parts.append(f"\n**Phần I: Trắc nghiệm khách quan nhiều lựa chọn ({diem_nl:0.2f} điểm)**\n")
        de_parts.append("Thí sinh trả lời câu hỏi từ câu 1 đến câu 12 (hoặc đến hết), mỗi câu chỉ chọn một đáp án điền vào bảng sau.\n")
        
        # Bảng đáp án
        table_mc = "Câu," + ",".join([str(q['Q_ID']) for q in NL_questions]) + "\r\nĐáp án," + ",".join(['...'] * len(NL_questions))
        de_parts.append(table_mc + "\n")

        ans_parts.append(f"\n**Phần I: Trắc nghiệm khách quan nhiều lựa chọn ({diem_nl:0.2f} điểm)**\n")
        ans_parts.append(f"Mỗi câu trả lời đúng được {3.0/12:0.2f} điểm.\n")
        ans_parts.append("Gợi ý đáp án: (Giả định đáp án A cho câu lẻ, B cho câu chẵn)\n")
        ans_table_mc = "Câu," + ",".join([str(q['Q_ID']) for q in NL_questions]) + "\r\nĐáp án," + ",".join(['A' if q['Q_ID'] % 2 != 0 else 'B' for q in NL_questions])
        ans_parts.append(ans_table_mc + "\n")
        
        for q in NL_questions:
            q_text = (f"**Câu {q['Q_ID']}.** (Mức độ: {q['MucDo']})\n"
                        f"Chủ đề: {q['ChuDe']}. Yêu cầu: {q['NoiDung']}\n"
                        f"A. Đáp án A. B. Đáp án B. C. Đáp án C. D. Đáp án D.\n"
                        f"→ (Lưu ý: Bạn cần thay thế Nội dung này bằng câu hỏi trắc nghiệm thực tế.)\n")
            de_parts.append(q_text)
            
    # Phần II: Trắc nghiệm đúng sai (DS)
    if DS_questions_raw:
        ds_q_count = len(DS_questions_raw)
        diem_ds = 2.0 / 2 * ds_q_count if ds_q_count > 0 else 0.0 
        de_parts.append(f"\n**Phần II: Trắc nghiệm đúng sai ({diem_ds:0.2f} điểm)**\n")
        de_parts.append("Thí sinh trả lời từ câu 13 đến hết. Trong mỗi ý (a, b, c, d) ở mỗi câu, thí sinh chọn Đúng hoặc Sai.\n")

        ans_parts.append(f"\n**Phần II: Trắc nghiệm đúng sai ({diem_ds:0.2f} điểm)**\n")
        ans_parts.append(f"Mỗi ý trả lời đúng được {2.0/(ds_q_count*4):0.2f} điểm (giả sử mỗi câu có 4 ý).\n")

        for i, q in enumerate(DS_questions_raw):
            q_id = q['Q_ID']
            de_parts.append(f"\n**Câu {q_id}.** (Mức độ: {q['MucDo']})\n")
            de_parts.append(f"Chủ đề: {q['ChuDe']}. Yêu cầu: {q['NoiDung']}. Cho các phát biểu sau:\n")
            table_ds = ",Đúng,Sai\r\na) Phát biểu liên quan đến Chủ đề {q['ChuDe']}.,,\r\nb) Phát biểu khác liên quan.,,\r\nc) Phát biểu sai.,,\r\nd) Phát biểu sai khác.,,\n"
            de_parts.append(table_ds)
            
            ans_parts.append(f"\n**Câu {q_id}.**\n")
            ans_parts.append("a) Đúng. (Dựa trên yêu cầu: {q['NoiDung']})\n")
            ans_parts.append("b) Sai. (Hệ số sai, Bậc sai, hoặc tính chất sai.)\n")
            ans_parts.append("c) Đúng. (Cần kiểm tra kỹ phát biểu.)\n")
            ans_parts.append("d) Sai. (Phần biến hoặc điều kiện sai.)\n")
            
    # Phần III: Trắc nghiệm trả lời ngắn (TLN)
    if TLN_questions:
        diem_tln = 2.0 / 4 * len(TLN_questions)
        de_parts.append(f"\n**Phần III: Trắc nghiệm trả lời ngắn ({diem_tln:0.2f} điểm)**\n")
        de_parts.append(f"Thí sinh trả lời từ câu {TLN_questions[0]['Q_ID']} đến hết.\n")
        
        ans_parts.append(f"\n**Phần III: Trắc nghiệm trả lời ngắn ({diem_tln:0.2f} điểm)**\n")
        ans_parts.append(f"Mỗi câu trả lời đúng được {2.0/4:0.2f} điểm.\n")
        table_tln = "Câu," + ",".join([str(q['Q_ID']) for q in TLN_questions]) + "\r\nKết quả," + ",".join(['...'] * len(TLN_questions))
        ans_parts.append(table_tln + "\n")
        
        for q in TLN_questions:
            q_text = (f"**Câu {q['Q_ID']}.** (Mức độ: {q['MucDo']})\n"
                        f"Chủ đề: {q['ChuDe']}. Yêu cầu: {q['NoiDung']}\n"
                        f"→ (Lưu ý: Bạn cần thay thế Nội dung này bằng câu hỏi trả lời ngắn thực tế.)\n")
            de_parts.append(q_text)

    # Phần B: Tự luận (TL Essay)
    if TL_Essay_questions:
        diem_tl_essay = 3.0 / 3 * len(TL_Essay_questions) 
        de_parts.append(f"\n**B. Tự luận ({diem_tl_essay:0.2f} điểm)**\n")
        ans_parts.append(f"\n**B. Tự luận ({diem_tl_essay:0.2f} điểm)**\n")
        
        for q in TL_Essay_questions:
            q_id = q['Q_ID']
            diem_q = 3.0 / 3 / len(TL_Essay_questions) 
            de_parts.append(f"\n**Câu {q_id} ({diem_q:0.2f} điểm).** (Mức độ: {q['MucDo']})\n")
            de_parts.append(f"Chủ đề: {q['ChuDe']}. Yêu cầu: {q['NoiDung']}\n")
            de_parts.append(f"a) Giải quyết phần cơ bản của yêu cầu. (0,5 điểm)\n")
            de_parts.append(f"b) Giải quyết phần nâng cao hơn của yêu cầu. (0,5 điểm)\n")
            de_parts.append(f"→ (Lưu ý: Bạn cần thay thế Nội dung này bằng câu hỏi tự luận thực tế.)\n")

            ans_parts.append(f"\n**Câu {q_id} ({diem_q:0.2f} điểm).**\n")
            ans_parts.append(f"a) Nội dung đáp án cho phần cơ bản (0,5 điểm).\n")
            ans_parts.append(f"b) Nội dung đáp án cho phần nâng cao (0,5 điểm).\n")
            
    # 4. TẠO FILE WORD
    doc = Document()
    doc.add_heading(f"ĐỀ KIỂM TRA GIỮA HỌC KÌ II - Môn: {mon} - Lớp {lop}", 0)
    doc.add_paragraph("Thời gian 90 phút (Không kể thời gian giao đề)")
    doc.add_paragraph(f"Họ và tên: ......................................................... Lớp: ............ Điểm: ..............")

    # --- Phần MA TRẬN & ĐẶC TẢ ---
    doc.add_heading("I. MA TRẬN VÀ BẢN ĐẶC TẢ", 1)
    
    doc.add_heading("1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ", 2)
    
    num_rows = ma_tran_df_final.shape[0] + 2 
    num_cols = ma_tran_df_final.shape[1]
    table_ma_tran_word = doc.add_table(rows=num_rows, cols=num_cols)
    table_ma_tran_word.style = 'Table Grid'
    for j, (h1, h2) in enumerate(ma_tran_df_final.columns):
        table_ma_tran_word.cell(0, j).text = h1
        table_ma_tran_word.cell(1, j).text = h2
    try:
        table_ma_tran_word.cell(0, 0).merge(table_ma_tran_word.cell(0, 1)) 
        table_ma_tran_word.cell(0, 2).merge(table_ma_tran_word.cell(0, 4)) 
        table_ma_tran_word.cell(0, 5).merge(table_ma_tran_word.cell(0, 7)) 
        table_ma_tran_word.cell(0, 8).merge(table_ma_tran_word.cell(0, 10)) 
    except Exception: pass
    for i in range(ma_tran_df_final.shape[0]):
        for j in range(ma_tran_df_final.shape[1]):
            table_ma_tran_word.cell(i + 2, j).text = str(ma_tran_df_final.iloc[i, j])

    doc.add_heading("2. BẢN ĐẶC TẢ ĐỀ KIỂM TRA ĐỊNH KÌ", 2)
    
    table_dac_ta_word = doc.add_table(rows=df_dac_ta_display.shape[0] + 1, cols=df_dac_ta_display.shape[1])
    table_dac_ta_word.style = 'Table Grid'
    for j, col_name in enumerate(df_dac_ta_display.columns):
        table_dac_ta_word.cell(0, j).text = col_name
    for i in range(df_dac_ta_display.shape[0]):
        for j in range(df_dac_ta_display.shape[1]):
            table_dac_ta_word.cell(i + 1, j).text = str(df_dac_ta_display.iloc[i, j])


    # --- Phần ĐỀ KIỂM TRA ---
    doc.add_page_break()
    doc.add_heading("II. ĐỀ KIỂM TRA", 1)
    doc.add_heading(f"A. Trắc nghiệm ({7.0:0.1f} điểm)", 2)
    for part in de_parts:
        if part.startswith("Câu,1,"): 
            header, data = part.split('\r\n')
            h_cells = header.split(',')
            d_cells = data.split(',')
            table = doc.add_table(rows=2, cols=len(h_cells))
            table.style = 'Table Grid'
            for j in range(len(h_cells)):
                table.cell(0, j).text = h_cells[j]
                table.cell(1, j).text = d_cells[j]
        elif part.startswith(",Đúng,Sai"): 
            lines = part.split('\r\n')
            num_rows = len(lines)
            table = doc.add_table(rows=num_rows, cols=3)
            table.style = 'Table Grid'
            for i, line in enumerate(lines):
                cells = line.split(',')
                for j, cell_text in enumerate(cells):
                    table.cell(i, j).text = cell_text
        elif part.startswith("Câu,Câu"): 
            header, data = part.split('\r\n')
            h_cells = header.split(',')
            d_cells = data.split(',')
            table = doc.add_table(rows=2, cols=len(h_cells))
            table.style = 'Table Grid'
            for j in range(len(h_cells)):
                table.cell(0, j).text = h_cells[j]
                table.cell(1, j).text = d_cells[j]
        elif part.startswith("\n**B. Tự luận"):
             doc.add_heading(part.strip().replace('**', ''), 2)
        else:
            doc.add_paragraph(part.replace('\n', ''))
        
    # --- Phần ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM ---
    doc.add_page_break()
    doc.add_heading("III. ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM", 1)
    doc.add_heading(f"Môn: {mon} - Lớp {lop}", 2)

    doc.add_heading(f"A. Trắc nghiệm ({7.0:0.1f} điểm)", 2)
    for part in ans_parts:
        if part.startswith("Câu,1,"): 
            header, data = part.split('\r\n')
            h_cells = header.split(',')
            d_cells = data.split(',')
            table = doc.add_table(rows=2, cols=len(h_cells))
            table.style = 'Table Grid'
            for j in range(len(h_cells)):
                table.cell(0, j).text = h_cells[j]
                table.cell(1, j).text = d_cells[j]
        elif part.startswith("Câu,Câu"): 
            header, data = part.split('\r\n')
            h_cells = header.split(',')
            d_cells = data.split(',')
            table = doc.add_table(rows=2, cols=len(h_cells))
            table.style = 'Table Grid'
            for j in range(len(h_cells)):
                table.cell(0, j).text = h_cells[j]
                table.cell(1, j).text = d_cells[j]
        elif part.startswith("\n**B. Tự luận"):
            doc.add_heading(part.strip().replace('**', ''), 2)
        else:
            doc.add_paragraph(part.replace('\n', ''))
            
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    st.download_button(
        "📥 Tải xuống file Word (ĐỀ + ĐÁP ÁN + MA TRẬN)",
        data=buffer,
        file_name=f"De_Kiem_Tra_Chuan_CV7991_{mon}_Lop{lop}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
