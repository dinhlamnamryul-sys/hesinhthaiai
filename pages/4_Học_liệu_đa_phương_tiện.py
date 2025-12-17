import streamlit as st
import re
import io
import requests
from docx import Document

# --- DỮ LIỆU MỤC LỤC TÍCH HỢP TỪ FILE  ---
MATH_INDEX = {
    "6": [
        {"chuong": "CHƯƠNG I. TẬP HỢP CÁC SỐ TỰ NHIÊN", "bai": ["Bài 1. Tập hợp", "Bài 6. Luỹ thừa với số mũ tự nhiên", "Bài 7. Thứ tự thực hiện các phép tính"]},
        {"chuong": "CHƯƠNG II. TÍNH CHIA HẾT", "bai": ["Bài 10. Số nguyên tố", "Bài 11. Ước chung lớn nhất"]},
        {"chuong": "CHƯƠNG VI. PHÂN SỐ", "bai": ["Bài 25. Phép cộng và phép trừ phân số", "Bài 26. Phép nhân và phép chia phân số"]}
    ],
    "7": [
        {"chuong": "CHƯƠNG I. SỐ HỮU TỈ", "bai": ["Bài 1. Tập hợp các số hữu tỉ", "Bài 3. Luỹ thừa với số mũ tự nhiên của một số hữu tỉ"]},
        {"chuong": "CHƯƠNG II. SỐ THỰC", "bai": ["Bài 6. Căn bậc hai số học", "Bài 7. Tập hợp các số thực"]},
        {"chuong": "CHƯƠNG VII. BIỂU THỨC ĐẠI SỐ", "bai": ["Bài 25. Đa thức một biến", "Bài 28. Phép chia đa thức một biến"]}
    ],
    "8": [
        {"chuong": "CHƯƠNG I. ĐA THỨC", "bai": ["Bài 1. Đơn thức", "Bài 4. Phép nhân đa thức"]},
        {"chuong": "CHƯƠNG II. HẰNG ĐẲNG THỨC ĐÁNG NHỚ", "bai": ["Bài 6. Hiệu hai bình phương", "Bài 9. Phân tích đa thức thành nhân tử"]},
        {"chuong": "CHƯƠNG IX. TAM GIÁC ĐỒNG DẠNG", "bai": ["Bài 35. Định lí Pythagore và ứng dụng"]}
    ],
    "9": [
        {"chuong": "Chương III. CĂN BẬC HAI VÀ CĂN BẬC BA", "bai": ["Bài 7. Căn bậc hai", "Bài 10. Căn bậc ba"]},
        {"chuong": "Chương VI. HÀM SỐ y = ax^2. PHƯƠNG TRÌNH BẬC HAI", "bai": ["Bài 19. Phương trình bậc hai một ẩn", "Bài 20. Định lí Viète"]}
    ]
}

# --- KHỞI TẠO TABS (Để tránh lỗi NameError) ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Tổng hợp Kiến thức", 
    "📝 Thiết kế Giáo án", 
    "🎵 Sáng tác Nhạc Toán", 
    "🎧 Đọc Văn bản"
])

# --- XỬ LÝ TAB 1: TỔNG HỢP KIẾN THỨC ---
with tab1:
    st.subheader("📚 Hệ thống kiến thức Toán học 6-9")
    
    c1, c2 = st.columns(2)
    with c1:
        lop_sel = st.selectbox("Chọn lớp:", list(MATH_INDEX.keys()), format_func=lambda x: f"Toán {x}")
    
    with c2:
        chapters = [ch["chuong"] for ch in MATH_INDEX[lop_sel]]
        chuong_sel = st.selectbox("Chọn chương:", chapters)
    
    # Lấy danh sách bài tương ứng
    lessons = next(ch["bai"] for ch in MATH_INDEX[lop_sel] if ch["chuong"] == chuong_sel)
    bai_sel = st.selectbox("Chọn bài học:", lessons)

    if st.button("✨ Tổng hợp nội dung"):
        # Prompt yêu cầu trả về LaTeX chuẩn [cite: 3, 23, 47, 67, 73]
        prompt = f"""
        Bạn là giáo viên Toán. Hãy soạn nội dung cho {bai_sel} - {chuong_sel} (Toán lớp {lop_sel}).
        Yêu cầu:
        1. Định dạng công thức TOÀN BỘ bằng LaTeX đặt trong $$ (Ví dụ: $$\\frac{{a}}{{b}}$$, $$\\sqrt{{x}}$$).
        2. Cấu trúc: Khái niệm -> Công thức -> Ví dụ minh họa -> Bài tập ứng dụng.
        3. Nội dung phải bám sát chương trình phổ thông.
        """
        
        if not api_key:
            st.error("Vui lòng nhập API Key!")
        else:
            with st.spinner("Đang biên soạn..."):
                res = generate_with_gemini(api_key, prompt)
                if res["ok"]:
                    st.session_state["math_result"] = res["text"]
                else:
                    st.error(res["message"])

    if "math_result" in st.session_state:
        st.markdown("---")
        # Sử dụng st.markdown để render LaTeX tự động
        st.markdown(st.session_state["math_result"])
