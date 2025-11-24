# Home.py
import streamlit as st
import os

# Cấu hình trang (Chỉ cần set ở file Home)
st.set_page_config(
    page_title="Cổng Giáo Dục Số - Trường Na Ư",
    page_icon="🏫",
    layout="wide"
)

# Đếm lượt truy cập
def update_visit_count():
    count_file = "visit_count.txt"
    if not os.path.exists(count_file):
        with open(count_file, "w") as f: f.write("5383"); return 5383
    try:
        with open(count_file, "r") as f: count = int(f.read().strip())
    except: count = 5383
    count += 1
    with open(count_file, "w") as f: f.write(str(count))
    return count

if 'visit_count' not in st.session_state:
    st.session_state.visit_count = update_visit_count()

# Giao diện Trang chủ
st.markdown("""
<div style="background: linear-gradient(90deg, #1a237e, #3949ab); color: white; padding: 20px; border-radius: 15px; text-align: center;">
    <h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>
    <h3>CỔNG THÔNG TIN GIÁO DỤC SỐ - BẢN MƯỜNG</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.write("## 👋 Chào mừng các em học sinh và thầy cô!")
st.write("Hãy chọn chức năng ở thanh bên trái (Sidebar) để bắt đầu:")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("### 🏔️ Gia Sư Toán AI\nLuyện tập từng bài, tích lũy ngô, đổi quà.")
with col2:
    st.success("### 📝 Sinh Đề Tự Động\nTạo phiếu bài tập, đề kiểm tra nhanh chóng.")
with col3:
    st.warning("### 📸 Chấm Bài Qua Ảnh\nChụp ảnh bài làm, AI nhận xét chi tiết.")

st.markdown("---")
st.caption(f"© 2025 Trường Na Ư. Tổng lượt truy cập: {st.session_state.visit_count}")
