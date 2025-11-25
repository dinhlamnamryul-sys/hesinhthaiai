import streamlit as st
import random
import time
from utils import CHUONG_TRINH_HOC, tao_cau_hoi_theo_muc_do

st.set_page_config(page_title="Sinh Đề Tự Động", page_icon="📝")

st.markdown("""
<style>
    .exam-box {
        background-color: white;
        padding: 30px;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        border-radius: 5px;
        font-family: 'Times New Roman', serif;
    }
    .exam-header { text-align: center; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 10px; }
    .question-item { margin-bottom: 15px; font-size: 16px; }
    .level-label { 
        font-size: 12px; font-weight: bold; color: white; 
        padding: 2px 6px; border-radius: 4px; margin-right: 5px;
    }
    .lv-1 { background-color: #4CAF50; } /* Nhận biết - Xanh */
    .lv-2 { background-color: #2196F3; } /* Thông hiểu - Lam */
    .lv-3 { background-color: #FF9800; } /* Vận dụng - Cam */
</style>
""", unsafe_allow_html=True)

st.title("📝 Sinh Đề Tự Động (Đa Mức Độ)")
st.write("Tạo phiếu bài tập với ma trận kiến thức: Nhận biết - Thông hiểu - Vận dụng.")

# --- CẤU HÌNH ĐỀ THI ---
c1, c2 = st.columns(2)
with c1:
    lop = st.selectbox("Chọn Lớp", list(CHUONG_TRINH_HOC.keys()))
    chuong = st.selectbox("Chọn Chủ đề", list(CHUONG_TRINH_HOC[lop].keys()))
    bai_list = CHUONG_TRINH_HOC[lop][chuong]
    # Chọn bài học cụ thể hoặc Tất cả
    bai_chon = st.multiselect("Chọn bài học (Để trống sẽ lấy ngẫu nhiên cả chương)", bai_list)

with c2:
    so_cau = st.slider("Tổng số câu hỏi", 5, 30, 10)
    st.write("**Cấu trúc đề:**")
    ti_le_nb = st.number_input("% Nhận biết (Dễ)", value=40, step=10)
    ti_le_th = st.number_input("% Thông hiểu (Vừa)", value=40, step=10)
    ti_le_vd = 100 - (ti_le_nb + ti_le_th)
    st.caption(f"➡️ % Vận dụng (Khó): {ti_le_vd}%")

# --- XỬ LÝ SINH ĐỀ ---
if st.button("🚀 Sinh đề ngay", type="primary"):
    if not bai_chon: bai_chon = bai_list # Nếu không chọn bài thì lấy hết
    
    # Tính số lượng câu hỏi từng loại
    sl_nb = int(so_cau * ti_le_nb / 100)
    sl_th = int(so_cau * ti_le_th / 100)
    sl_vd = so_cau - sl_nb - sl_th
    
    # Danh sách chứa đề
    de_thi_data = []
    
    # Hàm tạo danh sách câu hỏi theo số lượng
    def generate_qs(sl, muc_do, label):
        for _ in range(sl):
            bai = random.choice(bai_chon)
            cau_hoi, dap_an = tao_cau_hoi_theo_muc_do(lop, bai, muc_do)
            de_thi_data.append({
                "cau_hoi": cau_hoi,
                "dap_an": dap_an,
                "muc_do": label,
                "color": f"lv-{muc_do}"
            })

    generate_qs(sl_nb, 1, "Nhận biết")
    generate_qs(sl_th, 2, "Thông hiểu")
    generate_qs(sl_vd, 3, "Vận dụng")
    
    # Trộn đề để không bị các câu dễ nằm hết ở đầu
    # random.shuffle(de_thi_data) # Có thể bỏ comment nếu muốn trộn lẫn lộn

    # --- HIỂN THỊ KẾT QUẢ (PREVIEW) ---
    st.markdown("---")
    st.subheader("📄 Xem trước Phiếu Bài Tập")
    
    # Tạo nội dung hiển thị HTML/Markdown đẹp mắt
    html_content = f"""
    <div class="exam-box">
        <div class="exam-header">
            <h3>TRƯỜNG PTDTBT TH&THCS NA Ư</h3>
            <h4>ĐỀ ÔN TẬP TOÁN {lop.upper()}</h4>
            <p>Chủ đề: {chuong}</p>
        </div>
    """
    
    plain_text_content = f"TRƯỜNG PTDTBT TH&THCS NA Ư\nĐỀ TOÁN {lop.upper()} - {chuong}\n{'='*40}\n\n"
    
    for i, item in enumerate(de_thi_data):
        # Hiển thị trên web (Có tag màu mức độ)
        html_content += f"""
        <div class="question-item">
            <span class="level-label {item['color']}">{item['muc_do']}</span>
            <b>Câu {i+1}:</b> {item['cau_hoi']}
        </div>
        """
        # Nội dung file tải về (Chỉ text thuần)
        clean_q = item['cau_hoi'].replace("$", "") # Xóa dấu $ cho file text dễ đọc
        plain_text_content += f"Câu {i+1} ({item['muc_do']}): {clean_q}\n\n"

    html_content += "</div>"
    
    # Render ra màn hình (Hỗ trợ công thức Toán LaTeX)
    st.markdown(html_content, unsafe_allow_html=True)
    
    # Render công thức toán học riêng lẻ (Streamlit cần cái này để vẽ đẹp các dấu $)
    # Vì HTML trên không tự render LaTeX bên trong div, ta dùng trick này để hiển thị lại cho đẹp
    # Hoặc đơn giản hơn, ta chỉ cần hiển thị text, Streamlit sẽ tự parse $...$ nếu nó nằm ngoài HTML block phức tạp.
    # Cách tốt nhất hiện tại:
    with st.expander("👁️ Xem chi tiết từng câu (Chế độ hiển thị Công thức chuẩn)"):
        for i, item in enumerate(de_thi_data):
            st.markdown(f"**Câu {i+1}** `[{item['muc_do']}]`: {item['cau_hoi']}")

    # --- KHU VỰC TẢI VỀ ---
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📥 Tải Đề bài (.txt)",
            data=plain_text_content,
            file_name=f"De_Toan_{lop}.txt",
            mime="text/plain"
        )
    with col_dl2:
        ans_content = "\n".join([f"Câu {i+1}: {item['dap_an']}" for i, item in enumerate(de_thi_data)])
        st.download_button(
            label="🔑 Tải Đáp án (.txt)",
            data=ans_content,
            file_name=f"Dap_An_{lop}.txt",
            mime="text/plain"
        )
