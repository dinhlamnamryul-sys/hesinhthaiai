import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Công Cụ Tạo Đề 7991",
    page_icon="📝",
    layout="wide"
)

# --- CSS TÙY CHỈNH CHO GIAO DIỆN ĐẸP HƠN ---
st.markdown("""
<style>
    .step-header {
        font-weight: bold;
        color: #2e86de;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2e86de;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # --- HEADER ---
    st.title("📝 Trợ Lý Tạo Đề Kiểm Tra (Chuẩn 7991 & TT22)")
    st.caption("Công cụ hỗ trợ giáo viên trường PTDTBT TH&THCS NA Ư xây dựng đề thi nhanh chóng với AI.")
    
    st.divider()

    # --- SIDEBAR: NHẬP THÔNG TIN ĐỀ BÀI ---
    with st.sidebar:
        st.header("⚙️ Thiết lập thông số")
        st.info("Nhập thông tin bài kiểm tra vào đây, Prompt sẽ tự động cập nhật.")
        
        # Nhóm thông tin chung
        subject = st.text_input("📚 Môn học", value="Toán học")
        grade_level = st.selectbox("🎓 Khối lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], index=2)
        exam_time = st.selectbox("⏱ Thời gian làm bài", ["15 phút", "45 phút", "60 phút", "90 phút"], index=0)
        
        # Nhóm nội dung
        exam_topic = st.text_area("📖 Nội dung/Chủ đề kiểm tra", 
                                  value="Chương III: Tam giác đồng dạng (Định lý Talet, Tính chất đường phân giác)",
                                  height=100)
        
        # Nhóm cấu trúc đề (để Prompt 2 linh hoạt hơn)
        st.subheader("Cấu trúc đề mong muốn")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            num_tn = st.number_input("Số câu TN", value=10, min_value=0)
            score_tn = st.number_input("Điểm/câu TN", value=0.5, step=0.1)
        with col_s2:
            num_tl = st.number_input("Số câu TL", value=3, min_value=0)
            score_tl_total = st.number_input("Tổng điểm TL", value=5.0, step=0.5)

    # --- MAIN CONTENT: HIỂN THỊ PROMPT ---
    
    # Hiển thị tóm tắt cấu hình hiện tại
    st.markdown(f"""
    <div class="info-box">
        Đang tạo bộ lệnh cho: <b>{subject} - {grade_level}</b><br>
        Chủ đề: <i>{exam_topic}</i><br>
        Thời gian: {exam_time} | Cấu trúc: {num_tn} Trắc nghiệm + {num_tl} Tự luận
    </div>
    """, unsafe_allow_html=True)

    # Tạo các biến Prompt dựa trên Input (f-string)
    
    # Prompt 1: Ma trận
    prompt_1 = f"""
Bạn là chuyên gia xây dựng đề kiểm tra theo Thông tư 22 và chuẩn 7991.
Hãy tạo ma trận đề kiểm tra {exam_time} môn {subject}, {grade_level}, nội dung về "{exam_topic}".
Yêu cầu theo 4 mức độ nhận thức Bloom: Nhận biết – Thông hiểu – Vận dụng – Vận dụng cao.
Xuất ma trận dưới dạng bảng rõ ràng, gồm các cột: Mạch kiến thức | Số câu | Điểm | Tỉ lệ % | Mức độ nhận thức.
    """.strip()

    # Prompt 2: Sinh đề
    prompt_2 = f"""
Từ ma trận vừa tạo, hãy sinh ra đề kiểm tra {exam_time} môn {subject}, {grade_level}, nội dung "{exam_topic}" gồm:
- {num_tn} câu trắc nghiệm (mỗi câu {score_tn} điểm).
- {num_tl} câu tự luận (tổng {score_tl_total} điểm).
Viết đáp án chi tiết, nêu rõ mức độ nhận thức của từng câu và năng lực được đánh giá (Biết – Hiểu – Vận dụng).
    """.strip()

    # Prompt 3: Đánh giá (Cố định)
    prompt_3 = """
Phân tích đề kiểm tra trên theo hướng đánh giá năng lực.
Hãy chỉ ra:
1. Tỉ lệ câu hỏi ở từng mức độ Bloom.
2. Năng lực học sinh được kiểm tra ở 3 mức: Biết – Hiểu – Vận dụng.
3. Nhận xét tổng thể về độ cân đối – độ phân hóa – tính phù hợp chương trình.
    """.strip()

    # Prompt 4: Đề V2 (Cố định)
    prompt_4 = """
Dựa trên đề gốc ở trên, hãy tạo phiên bản 2 của đề kiểm tra (Mã đề chẵn/lẻ):
1. Giữ nguyên ma trận và độ khó tương đương.
2. Thay đổi ngữ liệu, dữ kiện, ví dụ minh họa (số liệu khác, tình huống khác).
3. Đảm bảo không trùng câu hỏi hoặc đáp án với đề 1.
Xuất kết quả ở định dạng: Câu hỏi – Đáp án – Mức độ – Gợi ý chấm.
    """.strip()

    # Prompt 5: Xuất file (Cố định)
    prompt_5 = """
Hãy tổng hợp toàn bộ nội dung của 2 đề kiểm tra (hoặc đề gốc) và đáp án chi tiết ở trên để tôi copy vào Word.
Yêu cầu trình bày:
1. Đánh số câu rõ ràng.
2. Tạo phần đáp án riêng bên dưới cùng.
3. Gợi ý rubric chấm điểm tự luận (theo 3 mức độ đạt).
4. Trình bày gọn gàng, format đẹp, dễ in và dễ dùng cho giáo viên.
    """.strip()

    # --- HIỂN THỊ TABS ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1️⃣ Tạo Ma Trận", 
        "2️⃣ Sinh Câu Hỏi", 
        "3️⃣ Đánh Giá NL", 
        "4️⃣ Tạo Đề Số 2", 
        "5️⃣ Xuất Bản"
    ])

    with tab1:
        st.markdown('<div class="step-header">Bước 1: Thiết lập khung ma trận</div>', unsafe_allow_html=True)
        st.write("Copy đoạn lệnh này gửi cho AI để xác định cấu trúc đề thi:")
        st.code(prompt_1, language="markdown")
        
    with tab2:
        st.markdown('<div class="step-header">Bước 2: Sinh nội dung đề chi tiết</div>', unsafe_allow_html=True)
        st.write("Sau khi AI đã có ma trận, gửi tiếp lệnh này để tạo câu hỏi:")
        st.code(prompt_2, language="markdown")
        
    with tab3:
        st.markdown('<div class="step-header">Bước 3: Thẩm định chất lượng đề</div>', unsafe_allow_html=True)
        st.write("Yêu cầu AI đóng vai hội đồng thẩm định để kiểm tra độ phân hóa:")
        st.code(prompt_3, language="markdown")
        
    with tab4:
        st.markdown('<div class="step-header">Bước 4: Tạo đề hoán vị (Đề B)</div>', unsafe_allow_html=True)
        st.write("Tạo thêm một mã đề nữa với độ khó tương đương để chống quay cóp:")
        st.code(prompt_4, language="markdown")
        
    with tab5:
        st.markdown('<div class="step-header">Bước 5: Hoàn thiện và In ấn</div>', unsafe_allow_html=True)
        st.write("Lệnh cuối cùng để AI trình bày lại văn bản đẹp mắt phục vụ in ấn:")
        st.code(prompt_5, language="markdown")

    # --- FOOTER ---
    st.divider()
    st.caption("© 2025 Trường PTDTBT TH&THCS NA Ư - Hệ thống hỗ trợ dạy học số.")

if __name__ == "__main__":
    main()
