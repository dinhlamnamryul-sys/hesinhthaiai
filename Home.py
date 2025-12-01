# --- 4. NỘI DUNG TRANG CHÍNH ---
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>"Tri thức vùng cao - Vươn xa thế giới"</h3>
</div>
""", unsafe_allow_html=True)


# --- Nhạc nền H'Mông ---
st.markdown(f"""
<div style="text-align:center; margin-top: -5px; margin-bottom:20px;">
<h4 style="color:#333;">🎵 Giai điệu bản Mông</h4>
<audio controls autoplay>
    {audio_source_html}
</audio>
</div>
""", unsafe_allow_html=True)


# ===== CARD CHỨC NĂNG — GỌN HƠN =====
col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    st.markdown('<div class="feature-card"><div class="icon-box">🏔️</div><div class="card-title">Gia Sư Toán AI</div><p>Học toán song ngữ thông minh.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_1):
        st.page_link(PAGE_1, label="Học ngay ➜", icon="📝", use_container_width=True)

with col2:
    st.markdown('<div class="feature-card"><div class="icon-box">⚡</div><div class="card-title">Sinh Đề Tự Động</div><p>Tạo đề kiểm tra cực nhanh.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_2):
        st.page_link(PAGE_2, label="Tạo đề ➜", icon="🚀", use_container_width=True)

with col3:
    st.markdown('<div class="feature-card"><div class="icon-box">🧿</div><div class="card-title">Giải Bài Tập Từ Ảnh</div><p>AI phân tích & giải tức thì.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_3):
        st.page_link(PAGE_3, label="Giải ngay ➜", icon="📸", use_container_width=True)

with col4:
    st.markdown('<div class="feature-card"><div class="icon-box">📽️</div><div class="card-title">Đa Phương Tiện</div><p>Học liệu văn hoá H\'Mông.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_4):
        st.page_link(PAGE_4, label="Khám phá ➜", icon="🎧", use_container_width=True)
