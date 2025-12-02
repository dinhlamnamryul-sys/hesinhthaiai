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
        "Định nghĩa CĐ", "Tính vận tốc TB", "Phân tích lực", 
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
    ] # Trọng số số câu cho từng mục tiêu
}
df = pd.DataFrame(data)

# -------------------- KHỞI TẠO BIẾN TRÁNH NAMEERROR --------------------
# Đảm bảo các biến quan trọng được định nghĩa trước khi sử dụng 
questions = []
df_filtered = pd.DataFrame(data) 
required_q_by_level = {}


# -------------------- HÀM TẠO MA TRẬN VÀ BẢN ĐẶC TẢ --------------------

def create_ma_tran(df_input, total_cau):
    """Tạo DataFrame Ma trận theo cấu trúc Phụ lục 1 của CV 7991."""
    
    # Ánh xạ tên mức độ (CV 7991)
    level_map = {
        "Nhận biết": "Biết",
        "Thông hiểu": "Hiểu",
        "Vận dụng": "Vận dụng (M1)",
        "Vận dụng cao": "Vận dụng (M2)"
    }
    
    # 1. Tổng hợp số câu thực tế cần cho mỗi Chủ đề và Mức độ
    pivot_table = pd.pivot_table(
        df_input, 
        values='N_to_Take', # Số câu đã được tính toán cần lấy
        index=['ChuDe', 'NoiDung'], 
        columns='MucDo', 
        aggfunc='sum', 
        fill_value=0
    )
    
    # Đảm bảo có đủ 4 cột mức độ (Biết, Hiểu, VĐ, VĐC)
    all_levels_mock = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
    for level in all_levels_mock:
        if level not in pivot_table.columns:
            pivot_table[level] = 0
            
    pivot_table = pivot_table[all_levels_mock]
    pivot_table.columns = [level_map[col] for col in pivot_table.columns] # Đổi tên cột

    # 2. Thêm cột Tổng và Hàng Tổng
    pivot_table['Tổng số câu'] = pivot_table.sum(axis=1)
    
    # Hàng tổng
    tong_so_cau = pivot_table.sum().to_frame().T
    tong_so_cau.index = ['Tổng số câu']
    
    # Tỉ lệ %
    ti_le = ((tong_so_cau / total_cau) * 100).round(1)
    ti_le.index = ['Tỉ lệ % điểm']
    
    # Tính Tổng số điểm (trên thang 10)
    tong_diem = 10.0
    diem_row = (ti_le.iloc[0].drop('Tổng số câu') / 100) * tong_diem
    
    # Ghép bảng
    ma_tran_df = pd.concat([pivot_table.reset_index(), tong_so_cau.reset_index(drop=True)])
    ma_tran_df = pd.concat([ma_tran_df, ti_le.reset_index(drop=True)])
    
    # Chuẩn hóa cột Chủ đề/Nội dung cho hàng Tổng
    ma_tran_df.loc[ma_tran_df.index[-2], 'ChuDe'] = 'Tổng số câu'
    ma_tran_df.loc[ma_tran_df.index[-1], 'ChuDe'] = 'Tỉ lệ % điểm'

    # Tạo DataFrame hiển thị cuối cùng
    final_ma_tran = pd.DataFrame({
        "Nội dung/Đơn vị kiến thức": ma_tran_df['ChuDe'].astype(str) + " - " + ma_tran_df['NoiDung'].astype(str).fillna(""),
        "Biết": ma_tran_df['Biết'].astype(str).fillna(''),
        "Hiểu": ma_tran_df['Hiểu'].astype(str).fillna(''),
        "Vận dụng (M1)": ma_tran_df['Vận dụng (M1)'].astype(str).fillna(''),
        "Vận dụng (M2)": ma_tran_df['Vận dụng (M2)'].astype(str).fillna(''),
        "Tổng": ma_tran_df['Tổng số câu'].astype(str).fillna(''),
    })
    
    # Format hàng Tỉ lệ % điểm để hiển thị điểm (x,x) và % (x%)
    for col in diem_row.index:
        final_ma_tran.loc[final_ma_tran.index[-1], col] = (
            f"{diem_row[col].round(1)} ({ti_le[col].iloc[0]}%)"
        )
    
    final_ma_tran.loc[final_ma_tran.index[-1], 'Tổng'] = (
        f"{diem_row.sum().round(1)} ({ti_le['Tổng số câu'].iloc[0]}%)"
    )
    
    # Xóa NaN và Chuẩn hóa hàng Tổng
    final_ma_tran.loc[final_ma_tran.index[-2], 'Nội dung/Đơn vị kiến thức'] = 'Tổng số câu'
    final_ma_tran.loc[final_ma_tran.index[-1], 'Nội dung/Đơn vị kiến thức'] = 'Tỉ lệ % điểm'
    
    final_ma_tran = final_ma_tran.replace('nan', '')

    return final_ma_tran


def create_dac_ta(df_input):
    """Tạo Bản Đặc tả (rút gọn) theo cấu trúc Phụ lục 2 của CV 7991."""
    
    dac_ta_df = df_input.copy()
    
    # Giả định Nội dung là Yêu cầu cần đạt
    dac_ta_df['Yêu cầu cần đạt'] = dac_ta_df['NoiDung'] 
    
    # Ánh xạ mức độ
    level_map = {
        "Nhận biết": "Biết",
        "Thông hiểu": "Hiểu",
        "Vận dụng": "Vận dụng",
        "Vận dụng cao": "Vận dụng" # Cả VĐ và VĐC đều là 'Vận dụng' trong ô lớn
    }
    
    # Tạo cột Số câu cho mỗi mức độ (theo Phụ lục 2)
    dac_ta_df['Số câu'] = dac_ta_df['N_to_Take']
    
    # Định dạng Bản Đặc tả (Rút gọn)
    df_dac_ta_display = dac_ta_df[['ChuDe', 'NoiDung', 'Yêu cầu cần đạt', 'MucDo', 'Số câu']].copy()
    
    # Đổi tên cột
    dac_ta_columns = {
        'ChuDe': 'Chủ đề/Chương',
        'NoiDung': 'Nội dung/Đơn vị kiến thức',
        'Yêu cầu cần đạt': 'Yêu cầu cần đạt (YC CĐ)',
        'MucDo': 'Mức độ',
        'Số câu': 'Số câu hỏi thực tế'
    }
    
    df_dac_ta_display.rename(columns=dac_ta_columns, inplace=True)

    return df_dac_ta_display.astype(str)

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

# Lọc DataFrame theo lựa chọn cuối cùng (được sử dụng sau khi nút bấm)
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

# -------------------- XỬ LÝ KHI BẤM NÚT TẠO ĐỀ --------------------

if st.button("📘 Tạo đề tự động", use_container_width=True):
    
    # 1. Kiểm tra đầu vào
    if df_filtered.empty:
        st.error("Không tìm thấy câu hỏi nào phù hợp với bộ lọc đã chọn. Vui lòng chọn lại Môn/Chương/Bài/Chủ đề.")
        st.stop()
    
    if total_percent == 0:
        st.error("Tổng tỉ lệ mức độ không thể bằng 0%. Vui lòng nhập tỉ lệ.")
        st.stop()

    # 2. Chuẩn hóa tỉ lệ mức độ và tính số lượng câu cần
    normalized_ti_le = {}
    for md, percent in st.session_state.ti_le_muc_do.items():
        normalized_ti_le[md] = percent / total_percent 

    required_q_by_level = {}
    remaining_total_q = so_cau_total
    
    # Tính số câu cần cho mỗi mức độ (làm tròn)
    levels = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
    
    for i, md in enumerate(levels):
        ratio = normalized_ti_le.get(md, 0)
        if i < len(levels) - 1:
            required_q = round(so_cau_total * ratio)
            required_q_by_level[md] = required_q
            remaining_total_q -= required_q
        else:
            required_q_by_level[md] = remaining_total_q

    # 3. Phân bổ câu hỏi vào DataFrame
    df_filtered['N_to_Take'] = 0
    questions = []
    q_number = 1
    
    for md in levels:
        n_cau_level = required_q_by_level.get(md, 0)
        if n_cau_level == 0:
            continue

        # Lọc các dòng có mức độ phù hợp
        df_md_index = df_filtered[df_filtered['MucDo'] == md].index
        
        if df_md_index.empty:
            continue

        # Tính tổng 'SoCau' có sẵn
        total_available_points = df_filtered.loc[df_md_index, 'SoCau'].sum()
        
        if total_available_points == 0:
            continue

        # Tính số lượng cần lấy cho từng hàng (dựa trên tỷ trọng SoCau)
        df_filtered.loc[df_md_index, 'N_Needed'] = (df_filtered.loc[df_md_index, 'SoCau'] / total_available_points) * n_cau_level
        df_filtered.loc[df_md_index, 'N_to_Take'] = df_filtered.loc[df_md_index, 'N_Needed'].apply(lambda x: math.ceil(x))
        
        # Giới hạn số câu lấy không vượt quá số câu có sẵn (SoCau)
        df_filtered.loc[df_md_index, 'N_to_Take'] = df_filtered.apply(
            lambda row: min(row['N_to_Take'], row['SoCau']) if row['MucDo'] == md else row['N_to_Take'], 
            axis=1
        )
        
        # Điều chỉnh tổng số câu lấy không vượt quá n_cau_level
        current_total_take = df_filtered.loc[df_md_index, 'N_to_Take'].sum()
        if current_total_take > n_cau_level:
            
            # Giảm dần số câu từ các dòng có N_to_Take lớn nhất cho đến khi tổng bằng n_cau_level
            rows_to_adjust = df_filtered.loc[df_md_index].sort_values(by='N_to_Take', ascending=False).index.tolist()
            
            while df_filtered.loc[df_md_index, 'N_to_Take'].sum() > n_cau_level and rows_to_adjust:
                idx = rows_to_adjust.pop(0) 
                df_filtered.loc[idx, 'N_to_Take'] -= 1
                if df_filtered.loc[idx, 'N_to_Take'] <= 0:
                    rows_to_adjust = [i for i in rows_to_adjust if i != idx]
        
        # 4. Tạo câu hỏi
        for index, row in df_filtered.loc[df_md_index].iterrows():
            n_to_take = int(row['N_to_Take'])
            for i in range(n_to_take):
                q_text = (f"Câu {q_number}. ({row.get('MucDo')}) - Chủ đề: {row.get('ChuDe')}\n"
                          f"Nội dung: {row.get('NoiDung')}\n"
                          f"→ (Lưu ý: Bạn cần thay thế Nội dung này bằng câu hỏi trắc nghiệm/tự luận thực tế.)\n"
                          f"→ Hãy trình bày câu trả lời.")
                questions.append(q_text)
                q_number += 1

    # 5. Hiển thị Ma trận Đề kiểm tra
    st.markdown("---")
    st.subheader("📊 1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 1)")
    
    df_with_n_take = df_filtered[df_filtered['N_to_Take'] > 0]
    
    if not df_with_n_take.empty:
        ma_tran_df_final = create_ma_tran(df_with_n_take, so_cau_total)
        st.dataframe(ma_tran_df_final, hide_index=True, use_container_width=True)
    else:
        st.error("Lỗi phân bổ: Không thể tạo đủ câu hỏi theo tỉ lệ đã chọn từ ma trận mẫu.")
        st.stop()
        
    # 6. Hiển thị Bản Đặc tả (Tóm tắt)
    st.markdown("---")
    st.subheader("📑 2. BẢN ĐẶC TẢ ĐỀ KIỂM TRA ĐỊNH KÌ (Theo Phụ lục 2 - Rút gọn)")
    
    df_dac_ta_display = create_dac_ta(df_with_n_take)
    st.dataframe(df_dac_ta_display, hide_index=True, use_container_width=True)
    
    # 7. Hiển thị Đề kiểm tra
    st.success(f"Đã tạo thành công {len(questions)} câu hỏi theo cấu trúc CV 7991!")
    st.subheader("📄 3. ĐỀ KIỂM TRA TỰ ĐỘNG:")
    
    output_text = ""
    for q in questions:
        st.markdown(q)
        st.markdown("---")
        output_text += q + "\n" + "---" + "\n\n"

    # 8. Xuất Word
    doc = Document()
    doc.add_heading(f"ĐỀ KIỂM TRA: {mon} - {chuong} - {bai}", 0)
    
    # Thêm bảng tóm tắt cấu trúc đề (Ma trận) vào Word
    doc.add_heading("1. MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ (Tóm tắt)", 2)
    
    table_ma_tran_word = doc.add_table(rows=ma_tran_df_final.shape[0] + 1, cols=ma_tran_df_final.shape[1])
    table_ma_tran_word.style = 'Table Grid'
    
    # Thêm tiêu đề
    for j, col_name in enumerate(ma_tran_df_final.columns):
        table_ma_tran_word.cell(0, j).text = col_name

    # Thêm dữ liệu
    for i in range(ma_tran_df_final.shape[0]):
        for j in range(ma_tran_df_final.shape[1]):
            table_ma_tran_word.cell(i + 1, j).text = str(ma_tran_df_final.iloc[i, j])

    # Thêm Bản Đặc tả vào Word
    doc.add_heading("2. BẢN ĐẶC TẢ ĐỀ KIỂM TRA ĐỊNH KÌ (Rút gọn)", 2)
    
    table_dac_ta_word = doc.add_table(rows=df_dac_ta_display.shape[0] + 1, cols=df_dac_ta_display.shape[1])
    table_dac_ta_word.style = 'Table Grid'
    
    # Thêm tiêu đề
    for j, col_name in enumerate(df_dac_ta_display.columns):
        table_dac_ta_word.cell(0, j).text = col_name

    # Thêm dữ liệu
    for i in range(df_dac_ta_display.shape[0]):
        for j in range(df_dac_ta_display.shape[1]):
            table_dac_ta_word.cell(i + 1, j).text = str(df_dac_ta_display.iloc[i, j])

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
