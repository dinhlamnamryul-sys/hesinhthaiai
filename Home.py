# --- NỘI DUNG CHÍNH (ĐÃ CẬP NHẬT 4 CỘT) ---

# Grid layout chia làm 4 cột đều nhau
col1, col2, col3, col4 = st.columns(4)

# THẺ 1: GIA SƯ TOÁN
with col1:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">🏔️</div>
            <div class="card-title">Gia Sư Toán AI</div>
            <div class="card-desc">Học toán song ngữ Việt - Mông. Giải bài khó, tích lũy bắp ngô đổi quà.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("") 
    if st.button("Học ngay ➜", key="btn1"):
        st.success("Đang khởi động trợ lý ảo H'Mông...")

# THẺ 2: SINH ĐỀ
with col2:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">⚡</div>
            <div class="card-title">Sinh Đề Siêu Tốc</div>
            <div class="card-desc">Tạo đề trắc nghiệm & tự luận trong 3 giây. Kho đề bám sát SGK mới.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Tạo đề ➜", key="btn2"):
        st.success("Đang truy cập kho dữ liệu đề thi...")

# THẺ 3: CHẤM BÀI
with col3:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">🧿</div>
            <div class="card-title">Chấm Thi AI Vision</div>
            <div class="card-desc">Công nghệ nhận diện chữ viết tay. Chụp ảnh bài làm, có điểm ngay lập tức.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Chấm bài ➜", key="btn3"):
        st.success("Đang bật camera...")

# THẺ 4: HỌC ĐA PHƯƠNG TIỆN (MỚI THÊM)
with col4:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="icon-box">📽️</div>
            <div class="card-title">Học Đa Phương Tiện</div>
            <div class="card-desc">Kho video bài giảng, phim tài liệu văn hóa H'Mông và thư viện sách nói.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Khám phá ➜", key="btn4"):
        st.success("Đang mở thư viện số...")
