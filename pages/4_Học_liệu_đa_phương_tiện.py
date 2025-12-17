import streamlit as st
import re
import io
import requests
from docx import Document
# ... (giữ các thư viện cũ của bạn)

# 1. DỮ LIỆU MỤC LỤC ĐÃ TÍCH HỢP [cite: 1, 21, 44, 61]
INDEX_DATA = {
    "6": [
        {"chapter": "CHƯƠNG I. TẬP HỢP CÁC SỐ TỰ NHIÊN", "lessons": ["Bài 1. Tập hợp", "Bài 2. Cách ghi số tự nhiên", "Bài 6. Luỹ thừa với số mũ tự nhiên", "Bài 7. Thứ tự thực hiện các phép tính"]},
        {"chapter": "CHƯƠNG II. TÍNH CHIA HẾT", "lessons": ["Bài 10. Số nguyên tố", "Bài 11. Ước chung lớn nhất", "Bài 12. Bội chung nhỏ nhất"]},
        {"chapter": "CHƯƠNG III. SỐ NGUYÊN", "lessons": ["Bài 14. Phép cộng và phép trừ số nguyên", "Bài 16. Phép nhân số nguyên"]},
        {"chapter": "CHƯƠNG VI. PHÂN SỐ", "lessons": ["Bài 23. Mở rộng phân số", "Bài 25. Phép cộng và trừ phân số"]},
        {"chapter": "CHƯƠNG VII. SỐ THẬP PHÂN", "lessons": ["Bài 28. Số thập phân", "Bài 31. Tỉ số phần trăm"]}
    ],
    "7": [
        {"chapter": "CHƯƠNG I. SỐ HỮU TỈ", "lessons": ["Bài 1. Tập hợp số hữu tỉ", "Bài 3. Luỹ thừa số hữu tỉ"]},
        {"chapter": "CHƯƠNG II. SỐ THỰC", "lessons": ["Bài 6. Căn bậc hai số học", "Bài 7. Tập hợp số thực"]},
        {"chapter": "CHƯƠNG IV. TAM GIÁC BẰNG NHAU", "lessons": ["Bài 12. Tổng các góc trong tam giác", "Bài 16. Tam giác cân"]},
        {"chapter": "CHƯƠNG VII. BIỂU THỨC ĐẠI SỐ", "lessons": ["Bài 25. Đa thức một biến", "Bài 28. Phép chia đa thức"]}
    ],
    "8": [
        {"chapter": "CHƯƠNG I. ĐA THỨC", "lessons": ["Bài 1. Đơn thức", "Bài 2. Đa thức"]},
        {"chapter": "CHƯƠNG II. HẰNG ĐẲNG THỨC ĐÁNG NHỚ", "lessons": ["Bài 6. Hiệu hai bình phương", "Bài 9. Phân tích đa thức thành nhân tử"]},
        {"chapter": "CHƯƠNG IX. TAM GIÁC ĐỒNG DẠNG", "lessons": ["Bài 33. Hai tam giác đồng dạng", "Bài 35. Định lí Pythagore"]}
    ],
    "9": [
        {"chapter": "CHƯƠNG III. CĂN BẬC HAI, CĂN BẬC BA", "lessons": ["Bài 7. Căn bậc hai", "Bài 10. Căn bậc ba"]},
        {"chapter": "CHƯƠNG IV. HỆ THỨC LƯỢNG TRONG TAM GIÁC VUÔNG", "lessons": ["Bài 11. Tỉ số lượng giác góc nhọn"]},
        {"chapter": "CHƯƠNG VI. PHƯƠNG TRÌNH BẬC HAI", "lessons": ["Bài 19. Phương trình bậc hai một ẩn", "Bài 20. Định lí Viète"]}
    ]
}

# ... (Các hàm call API Gemini và xử lý file của bạn giữ nguyên)

# 2. GIAO DIỆN CHỌN BÀI HỌC THEO MỤC LỤC
with tab1:
    st.subheader("📘 Tổng hợp Kiến thức Toán 6-9")
    
    col1, col2 = st.columns(2)
    with col1:
        lop_sel = st.selectbox("Chọn lớp:", ["6", "7", "8", "9"])
    with col2:
        # Lấy danh sách chương dựa trên lớp đã chọn [cite: 3, 23, 46, 63]
        chapters = [c["chapter"] for c in INDEX_DATA[lop_sel]]
        chapter_sel = st.selectbox("Chọn chương:", chapters)

    # Lấy danh sách bài dựa trên chương đã chọn
    lessons = []
    for c in INDEX_DATA[lop_sel]:
        if c["chapter"] == chapter_sel:
            lessons = c["lessons"]
    
    lesson_sel = st.selectbox("Chọn bài học:", lessons)

    if st.button("🚀 Tạo nội dung kiến thức"):
        # PROMPT ÉP AI TRẢ VỀ LATEX CHUẨN
        prompt = f"""
        Bạn là chuyên gia Toán học. Hãy soạn nội dung chi tiết cho: {lesson_sel} thuộc {chapter_sel} (Toán lớp {lop_sel}).
        
        YÊU CẦU TRÌNH BÀY:
        1. Khái niệm: Giải thích ngắn gọn.
        2. Công thức: BẮT BUỘC dùng LaTeX nằm trong cặp $$ $$. 
           Ví dụ: Với căn bậc hai, viết $$\\sqrt{{a}}$$. Với phân số, viết $$\\frac{{a}}{{b}}$$.
        3. Ví dụ minh họa: Có lời giải chi tiết.
        4. Bài tập tự luyện: 3 bài tập từ dễ đến khó.
        
        Ngôn ngữ: Tiếng Việt. Đảm bảo các ký hiệu toán học hiển thị đẹp.
        """
        
        with st.spinner("Đang trích xuất kiến thức..."):
            res = generate_with_gemini(api_key, prompt)
            if res["ok"]:
                st.session_state["result"] = res["text"]
            else:
                st.error(res["message"])

    # HIỂN THỊ KẾT QUẢ
    if "result" in st.session_state:
        # Sử dụng container để hiển thị Markdown hỗ trợ LaTeX
        st.markdown("---")
        st.markdown(st.session_state["result"])
        
        # Nút tải file
        st.download_button("📥 Tải giáo án (DOCX)", create_docx_bytes(st.session_state["result"]), "BaiHocToan.docx")
