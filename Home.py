# --- GRID LAYOUT 4 CỘT (CẬP NHẬT TÍNH NĂNG CHUYỂN TRANG) ---
col1, col2, col3, col4 = st.columns(4)

# CỘT 1: GIA SƯ TOÁN
with col1:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">🏔️</div>
            <div class="card-title">Gia Sư Toán AI</div>
            <div class="card-desc">Học toán song ngữ Việt-Mông. Tích lũy bắp ngô đổi quà.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("") 
    if st.button("Học ngay ➜", key="btn1"):
        st.switch_page("pages/1_Gia_Su_Toan.py") # Chuyển sang file Gia sư

# CỘT 2: SINH ĐỀ
with col2:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">⚡</div>
            <div class="card-title">Sinh Đề Tốc Độ</div>
            <div class="card-desc">Tạo đề trắc nghiệm & tự luận 3 giây. Kho đề chuẩn SGK.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Tạo đề ➜", key="btn2"):
        st.switch_page("pages/2_Sinh_De.py") # Chuyển sang file Sinh đề

# CỘT 3: CHẤM BÀI
with col3:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">🧿</div>
            <div class="card-title">Chấm Thi AI</div>
            <div class="card-desc">Nhận diện chữ viết tay. Chụp ảnh bài làm, có điểm ngay.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Chấm bài ➜", key="btn3"):
        st.switch_page("pages/3_Cham_Thi.py") # Chuyển sang file Chấm thi

# CỘT 4: HỌC ĐA PHƯƠNG TIỆN
with col4:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">📽️</div>
            <div class="card-title">Học Đa Phương Tiện</div>
            <div class="card-desc">Kho video bài giảng, phim tài liệu văn hóa & sách nói.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Khám phá ➜", key="btn4"):
        st.switch_page("pages/4_Da_Phuong_Tien.py") # Chuyển sang file Đa phương tiện
