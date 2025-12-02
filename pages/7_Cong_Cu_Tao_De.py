# ... (Phần code thiết lập UI và lọc data giữ nguyên) ...

def create_ma_tran(df_filtered, required_q_by_level, total_cau):
    """Tạo DataFrame Ma trận theo cấu trúc Phụ lục 1 của CV 7991."""
    
    # 1. Tổng hợp số câu thực tế cần cho mỗi Chủ đề và Mức độ
    pivot_table = pd.pivot_table(
        df_filtered, 
        values='N_to_Take', # Số câu đã được tính toán cần lấy
        index=['ChuDe', 'NoiDung'], 
        columns='MucDo', 
        aggfunc='sum', 
        fill_value=0
    ).rename(columns={
        "Nhận biết": "Biết (NB)",
        "Thông hiểu": "Hiểu (TH)",
        "Vận dụng": "Vận dụng (VD)",
        "Vận dụng cao": "Vận dụng cao (VDC)"
    })
    
    # Đảm bảo có đủ 4 cột mức độ (Biết, Hiểu, VĐ, VĐC)
    all_levels = ["Biết (NB)", "Hiểu (TH)", "Vận dụng (VD)", "Vận dụng cao (VDC)"]
    for level in all_levels:
        if level not in pivot_table.columns:
            pivot_table[level] = 0
            
    pivot_table = pivot_table[all_levels]

    # 2. Thêm cột Tổng và Hàng Tổng
    pivot_table['Tổng số câu'] = pivot_table.sum(axis=1)
    
    # Hàng tổng
    tong_so_cau = pivot_table.sum().to_frame().T
    tong_so_cau.index = ['Tổng']
    
    # Tính Tỉ lệ %
    ti_le = ((tong_so_cau / total_cau) * 100).round(1)
    ti_le.index = ['Tỉ lệ %']

    # Ghép bảng
    ma_tran_df = pd.concat([pivot_table, tong_so_cau, ti_le])
    ma_tran_df.insert(0, 'Nội dung/Đơn vị kiến thức', ma_tran_df.index)
    ma_tran_df.reset_index(drop=True, inplace=True)
    ma_tran_df.loc[ma_tran_df.index[-2], 'Nội dung/Đơn vị kiến thức'] = 'Tổng số câu'
    ma_tran_df.loc[ma_tran_df.index[-1], 'Nội dung/Đơn vị kiến thức'] = 'Tỉ lệ %'
    
    ma_tran_df.columns.name = None
    
    # Tạo tiêu đề bảng ma trận
    header_data = {
        "Mức độ đánh giá": ["", "Biết (NB)", "Hiểu (TH)", "Vận dụng (VD)", "Vận dụng cao (VDC)", "Tổng"],
        "Nội dung/đơn vị kiến thức": ["Chủ đề/Nội dung", "", "", "", "", ""]
    }
    
    # Lấy tiêu đề cột theo Phụ lục 1 (Bỏ TNKQ và TL)
    header_data_cv = {
        "Nội dung/đơn vị kiến thức": ma_tran_df['Nội dung/Đơn vị kiến thức'],
        "Biết": ma_tran_df['Biết (NB)'],
        "Hiểu": ma_tran_df['Hiểu (TH)'],
        "Vận dụng (Mức 1)": ma_tran_df['Vận dụng (VD)'],
        "Vận dụng (Mức 2)": ma_tran_df['Vận dụng cao (VDC)'],
        "Tổng số câu": ma_tran_df['Tổng số câu']
    }
    
    # Chuyển đổi hàng Tổng số câu và Tỉ lệ % sang định dạng điểm
    # Ví dụ: 30% -> 3.0 điểm, 40% -> 4.0 điểm, với tổng 10 điểm
    diem_ty_le_row = ma_tran_df.loc[ma_tran_df.index[-1]].drop('Nội dung/Đơn vị kiến thức') # Hàng tỉ lệ %
    tong_diem = 10.0 # Quy ước tổng điểm là 10
    diem_row = (diem_ty_le_row / 100) * tong_diem
    diem_row.name = 'Tổng số điểm (Quy ước 10đ)'
    
    # Tỉ lệ điểm
    ti_le_diem = diem_row.to_frame().T
    
    # Bảng hiển thị cuối cùng (Ma trận rút gọn chỉ lấy số câu)
    final_ma_tran = pd.DataFrame({
        "Nội dung/Đơn vị kiến thức": ma_tran_df.iloc[:-2]['Nội dung/Đơn vị kiến thức'].tolist() + ['Tổng số câu', 'Tỉ lệ % điểm (10đ)'],
        "Biết": ma_tran_df['Biết (NB)'].iloc[:-2].tolist() + [tong_so_cau['Biết (NB)'].iloc[0], f"{diem_row['Biết (NB)'].round(1)} ({ma_tran_df['Biết (NB)'].iloc[-1]}%)"],
        "Hiểu": ma_tran_df['Hiểu (TH)'].iloc[:-2].tolist() + [tong_so_cau['Hiểu (TH)'].iloc[0], f"{diem_row['Hiểu (TH)'].round(1)} ({ma_tran_df['Hiểu (TH)'].iloc[-1]}%)"],
        "Vận dụng (Mức 1)": ma_tran_df['Vận dụng (VD)'].iloc[:-2].tolist() + [tong_so_cau['Vận dụng (VD)'].iloc[0], f"{diem_row['Vận dụng (VD)'].round(1)} ({ma_tran_df['Vận dụng (VD)'].iloc[-1]}%)"],
        "Vận dụng (Mức 2)": ma_tran_df['Vận dụng cao (VDC)'].iloc[:-2].tolist() + [tong_so_cau['Vận dụng cao (VDC)'].iloc[0], f"{diem_row['Vận dụng cao (VDC)'].round(1)} ({ma_tran_df['Vận dụng cao (VDC)'].iloc[-1]}%)"],
        "Tổng": ma_tran_df['Tổng số câu'].iloc[:-2].tolist() + [tong_so_cau['Tổng số câu'].iloc[0], f"{diem_row.sum().round(1)} ({ma_tran_df['Tổng số câu'].iloc[-1]}%)"],
    })

    return final_ma_tran.astype(str)

# ... (Phần code thiết lập UI và lọc data giữ nguyên) ...
# ... (Chức năng Tạo đề tự động) ...

if st.button("📘 Tạo đề tự động", use_container_width=True):
    # ... (Phần xử lý chuẩn hóa tỉ lệ và tính N_to_Take giữ nguyên) ...
    
    # 5. Hiển thị Ma trận Đề kiểm tra
    st.markdown("---")
    st.subheader("📊 1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 1)")
    
    # Chỉ tính N_to_Take khi đã có đủ dữ liệu
    df_with_n_take = df_filtered[df_filtered['N_to_Take'] > 0]
    
    if not df_with_n_take.empty:
        ma_tran_df_final = create_ma_tran(df_filtered, required_q_by_level, so_cau_total)
        st.dataframe(ma_tran_df_final, hide_index=True, use_container_width=True)
    else:
        st.warning("Không đủ dữ liệu trong ma trận mẫu để tạo câu hỏi cho tỉ lệ đã chọn.")
        st.stop()
        
    # 6. Hiển thị Bản Đặc tả (Tóm tắt)
    st.markdown("---")
    st.subheader("📑 2. BẢN ĐẶC TẢ ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 2 - Rút gọn)")
    
    # Bản đặc tả tóm tắt được lấy trực tiếp từ các hàng có N_to_Take > 0
    # và thêm cột "Yêu cầu cần đạt" bằng Nội dung/Đơn vị kiến thức đã chọn
    df_dac_ta = df_with_n_take.copy()
    df_dac_ta['Yêu cầu cần đạt'] = df_dac_ta['NoiDung'] # Giả định Nội dung là Yêu cầu cần đạt
    
    # Chọn và đổi tên cột để giống Phụ lục 2
    dac_ta_columns = {
        'ChuDe': 'Chủ đề/Chương',
        'NoiDung': 'Nội dung/Đơn vị kiến thức',
        'Yêu cầu cần đạt': 'Yêu cầu cần đạt',
        'MucDo': 'Mức độ',
        'N_to_Take': 'Số câu hỏi thực tế'
    }
    
    df_dac_ta_display = df_dac_ta[list(dac_ta_columns.keys())].rename(columns=dac_ta_columns)
    
    st.dataframe(df_dac_ta_display.astype(str), hide_index=True, use_container_width=True)
    
    # 7. Hiển thị Đề kiểm tra
    st.success(f"Đã tạo thành công {len(questions)} câu hỏi theo cấu trúc CV 7991!")
    st.subheader("📄 3. ĐỀ KIỂM TRA TỰ ĐỘNG:")
    
    # ... (Phần hiển thị đề và xuất Word giữ nguyên) ...
