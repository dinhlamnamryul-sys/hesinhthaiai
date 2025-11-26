import streamlit as st
import random

# --- Dữ liệu curriculum thật: lớp 6 → lớp 9 ---
curriculum = {
    'Lớp 6': {
        'Chương I. Tập hợp các số tự nhiên': [
            'Bài 1: Tập hợp', 'Bài 2: Cách ghi số tự nhiên', 'Bài 3: Thứ tự trong tập hợp các số tự nhiên',
            'Bài 4: Phép cộng và phép trừ số tự nhiên', 'Bài 5: Phép nhân và phép chia số tự nhiên',
            'Bài 6: Lũy thừa với số mũ tự nhiên', 'Bài 7: Thứ tự thực hiện các phép tính',
            'Luyện tập chung', 'Bài tập cuối chương I'
        ],
        'Chương II. Tính chia hết trong tập hợp các số tự nhiên': [
            'Bài 8: Quan hệ chia hết và tính chất', 'Bài 9: Dấu hiệu chia hết', 'Bài 10: Số nguyên tố',
            'Bài 11: ƯCLN', 'Bài 12: BCNN', 'Luyện tập chung', 'Bài tập cuối chương II'
        ]
    },
    'Lớp 7': {
        'Chương I. Số hữu tỉ': [
            'Bài 1: Tập hợp các số hữu tỉ', 'Bài 2: Cộng, trừ, nhân, chia số hữu tỉ',
            'Bài 3: Lũy thừa của số hữu tỉ', 'Bài 4: Thứ tự thực hiện phép tính & quy tắc chuyển vế',
            'Luyện tập / bài tập cuối chương'
        ],
        'Chương II. Số thực': [
            'Bài 5: Làm quen với số thập phân vô hạn tuần hoàn',
            'Bài 6: Số vô tỉ và căn bậc hai số học',
            'Bài 7: Tập hợp các số thực'
        ]
    },
    'Lớp 8': {
        'Tập 1 – Chương I. Đa thức': [
            'Bài 1: Đơn thức', 'Bài 2: Đa thức', 'Bài 3: Phép cộng & trừ đa thức',
            'Bài 4: Phép nhân đa thức', 'Bài 5: Phép chia đa thức cho đơn thức',
            'Luyện tập chung & bài tập cuối chương'
        ],
        'Tập 2 – Chương VI. Phân thức đại số': [
            'Bài 21: Phân thức đại số', 'Bài 22: Tính chất cơ bản', 'Bài 23: Phép cộng và trừ phân thức',
            'Bài 24: Phép nhân và chia phân thức', 'Luyện tập chung', 'Bài tập cuối chương VI'
        ]
    },
    'Lớp 9': {
        'Tập 1': [
            'Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn',
            'Bài 1: Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn',
            'Bài 2: Giải hệ hai phương trình bậc nhất hai ẩn'
        ],
        'Tập 2': [
            'Chương VI: Hàm số y = ax^2', 'Bài 18: Hàm số y = ax^2', 'Bài 19: Phương trình bậc hai một ẩn'
        ]
    }
}

# --- Giao diện ---
st.set_page_config(page_title="Toán KNTT", layout="wide")
st.title("📘 Toán – Kết nối tri thức với cuộc sống")

col1, col2 = st.columns([1, 2])

with col1:
    grade = st.selectbox("Lớp:", [""] + list(curriculum.keys()))
    chapter = None
    lesson = None
    if grade:
        chapter = st.selectbox("Chương / Tập:", [""] + list(curriculum[grade].keys()))
    if chapter:
        lesson = st.selectbox("Bài học:", [""] + curriculum[grade][chapter])
    load = st.button("Đặt bài")

with col2:
    if 'question' not in st.session_state:
        st.session_state.question = None

    if load and grade and chapter and lesson:
        # Sinh câu hỏi dựa trên tên bài
        st.session_state.question = {
            "text": f"Trả lời câu hỏi về bài: {lesson}",
            "answer": "ví dụ: 42",  # placeholder, có thể để học sinh tự trả lời
            "hintVN": f"Nội dung bài {lesson}",
            "hintHM": f"Cov lus {lesson}"
        }

    if st.session_state.question:
        q = st.session_state.question
        st.write("### ❓ " + q["text"])
        ans = st.text_input("Nhập đáp án:", key="ans_question")
        if st.button("Kiểm tra đáp án"):
            st.info(f"Đáp án minh họa: {q['answer']}")
            st.info("💡 Gợi ý: " + q["hintVN"])
