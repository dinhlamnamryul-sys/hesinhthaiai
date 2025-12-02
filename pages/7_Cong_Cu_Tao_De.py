import streamlit as st
import pandas as pd

# ==================== CẤU HÌNH GIAO DIỆN ====================
st.set_page_config(
    page_title="Công Cụ Tạo Đề Kiểm Tra Tự Động",
    page_icon="📝",
    layout="wide"
)

st.markdown("""
<style>
    .step-header {
        font-weight: bold;
        color: #0d6efd;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    .info-box {
        background-color: #e7f1ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #0d6efd;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== APP ====================
def main():

    st.title("📝 HỆ THỐNG TẠO ĐỀ KIỂM TRA TỰ ĐỘNG DỰA TRÊN MA TRẬN")
    st.caption("Giáo viên chỉ cần tải ma trận lên – Hệ thống tự sinh đề theo chuẩn 7991 & TT22.")

    st.divider()

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.header("⚙️ Thiết lập đề kiểm tra")

        subject = st.text_input("📘 Môn học", "Toán học")
        grade = st.selectbox("🎓 Khối lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"])
        time = st.selectbox("⏱ Thời gian làm bài", ["15 phút", "45 phút", "60 phút", "90 phút"])

        exam_name = st.text_input("📌 Tên bài kiểm tra", "Kiểm tra giữa học kỳ II")

        st.subheader("📥 Tải ma trận đề")
        uploaded_file = st.file_uploader("Chọn file Excel/CSV", type=["xlsx", "xls", "csv"])

    # ---------------- MAIN CONTENT ----------------
    st.markdown(f"""
        <div class="info-box">
            <b>Môn:</b> {subject} | 
            <b>{grade}</b> | 
            <b>Thời gian:</b> {time}<br>
            <b>Tên đề:</b> {exam_name}
        </div>
    """, unsafe_allow_html=True)

    # Nếu chưa tải file → thông báo
    if uploaded_file is None:
        st.warning("📌 Vui lòng tải lên ma trận để hệ thống tạo Prompt.")
        return

    # ---------------- ĐỌC FILE ----------------
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except:
        st.error("❌ Không thể đọc file. Vui lòng kiểm tra lại định dạng!")
        return

    st.success("✅ Đã tải ma trận thành công!")
    st.write("### 📊 Ma trận bạn đã tải lên:")
    st.dataframe(df, use_container_width=True)

    # ================== TẠO PROMPTS ===================

    # Prompt ma trận → mô tả
    matrix_prompt = f"""
Bạn là chuyên gia xây dựng đề kiểm tra chuẩn 7991 & Thông tư 22.
Tôi đang tạo đề môn **{subject}**, **{grade}**, thời gian **{time}**, tên đề: **{exam_name}**.

Đây là ma trận đề kiểm tra (dạng bảng):

{df.to_markdown(index=False)}

➡️ Hãy phân tích ma trận trên và mô tả lại:
- Các mạch kiến thức
- Mức độ (NB – TH – VD – VDC)
- Số câu – số điểm tương ứng
- Tỉ lệ phần trăm
"""

    # Prompt sinh đề
    generate_prompt = f"""
Dựa vào ma trận đề tôi đã gửi, hãy tạo toàn bộ đề kiểm tra môn {subject}, {grade}:

Yêu cầu:
1. Sinh đầy đủ câu hỏi đúng theo số lượng và mức độ trong ma trận.
2. Có cả trắc nghiệm + tự luận (nếu ma trận có).
3. Ghi rõ mức độ nhận thức của từng câu.
4. Viết đáp án chi tiết + thang điểm cho câu tự luận.
5. Ngôn ngữ rõ ràng, phù hợp học sinh THCS.
"""

    # Prompt đánh giá đề
    eval_prompt = """
Hãy phân tích đề vừa sinh theo hướng đánh giá năng lực:
- Tỉ lệ câu theo mức độ Bloom
- Năng lực học sinh kiểm tra (Biết – Hiểu – Vận dụng)
- Độ phân hóa – tính phù hợp – độ bao phủ kiến thức
"""

    # Prompt tạo đề số 2
    reversion_prompt = """
Hãy tạo mã đề số 2 (Đề B):
- Giữ nguyên mức độ và cấu trúc theo ma trận
- Đổi dữ kiện + bối cảnh + số liệu
- Không trùng lại câu hỏi hoặc đáp án
"""

    # Prompt xuất Word
    export_prompt = """
Hãy tổng hợp toàn bộ đề kiểm tra và đáp án để tôi copy vào Word:
- Trình bày đẹp, rõ ràng
- Có phần đáp án riêng bên dưới
- Có bảng Rubric chấm điểm tự luận theo 3 mức
"""

    # ================== GIAO DIỆN TABS ===================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📌 1. Phân tích Ma Trận",
        "📝 2. Sinh Đề Tự Động",
        "📊 3. Đánh Giá Đề",
        "🔄 4. Tạo Đề Số 2",
        "📤 5. Xuất Bản Word"
    ])

    with tab1:
        st.markdown("<div class='step-header'>Bước 1: Phân tích ma trận</div>", unsafe_allow_html=True)
        st.code(matrix_prompt, language="markdown")

    with tab2:
        st.markdown("<div class='step-header'>Bước 2: Sinh đề theo ma trận</div>", unsafe_allow_html=True)
        st.code(generate_prompt, language="markdown")

    with tab3:
        st.markdown("<div class='step-header'>Bước 3: Đánh giá năng lực</div>", unsafe_allow_html=True)
        st.code(eval_prompt, language="markdown")

    with tab4:
        st.markdown("<div class='step-header'>Bước 4: Sinh đề B (hoán vị)</div>", unsafe_allow_html=True)
        st.code(reversion_prompt, language="markdown")

    with tab5:
        st.markdown("<div class='step-header'>Bước 5: Xuất bản đề để copy sang Word</div>", unsafe_allow_html=True)
        st.code(export_prompt, language="markdown")

    st.divider()
    st.caption("© 2025 Hệ thống hỗ trợ giáo viên tạo đề tự động – PTDTBT TH&THCS NA Ư")

# RUN
if __name__ == "__main__":
    main()
