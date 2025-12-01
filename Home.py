import streamlit as st

# ======================
# CẤU HÌNH TRANG
# ======================
st.set_page_config(
    page_title="Cổng Giáo Dục Số Na Ư",
    page_icon="🏫",
    layout="wide"
)

# ======================
# CSS GIAO DIỆN
# ======================
st.markdown("""
<style>

html, body {
    margin: 0;
    padding: 0;
}

[data-testid="stAppViewContainer"] {
    background-image: url("https://i.ibb.co/ZT86Q2B/bg-muong-lay.jpg");
    background-size: cover;
    background-position: center;
}

.box-container {
    background: rgba(255,255,255,0.85);
    padding: 40px;
    border-radius: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    margin-top: 40px;
    margin-bottom: 40px;
}

.card {
    background: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    transition: 0.2s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 6px 18px rgba(0,0,0,0.2);
}

.footer {
    text-align: center;
    padding: 10px;
    color: white;
    margin-top: 30px;
    font-size: 16px;
    background: rgba(0,0,0,0.45);
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# TIÊU ĐỀ
# ======================
st.markdown("<h1 style='text-align:center; color:white;'>🏫 CỔNG GIÁO DỤC SỐ – TRƯỜNG NA Ư</h1>", unsafe_allow_html=True)
st.write("")

# ======================
# KHUNG CHỨA 4 CHỨC NĂNG
# ======================
st.markdown('<div class="box-container">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/727/727245.png", width=80)
    st.markdown("### Gia Sư Toán AI")
    st.write("Học toán song ngữ thông minh.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/9068/9068647.png", width=80)
    st.markdown("### Sinh Đề Tự Động")
    st.write("Tạo đề kiểm tra cực nhanh.")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/1828/1828919.png", width=80)
    st.markdown("### Giải Bài Tập Từ Ảnh")
    st.write("AI phân tích & giải tức thì.")
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/685/685352.png", width=80)
    st.markdown("### Đa Phương Tiện")
    st.write("Học liệu văn hoá H'Mông.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ======================
# FOOTER
# ======================
st.markdown("""
<div class="footer">
📚 Nhóm tác giả: Trường PTDTBT TH&THCS Na Ư<br>
© 2025 Cổng Giáo Dục Số Na Ư
</div>
""", unsafe_allow_html=True)
