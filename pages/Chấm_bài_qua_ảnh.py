import streamlit as st
import openai

# --- Cấu hình OpenAI ---
openai.api_key = st.secrets.get("OPENAI_API_KEY")  # Lấy từ Streamlit Secrets

# --- Curriculum: Lớp 6 → Lớp 9 ---
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

# --- Hàm gọi OpenAI GPT để tạo câu hỏi ---
def generate_question(lesson_name):
    prompt = f"""
    Bạn là giáo viên Toán dạy theo SGK Kết nối tri thức. 
    Tạo 1 câu hỏi Toán ngắn, có đáp án, liên quan đến bài học '{lesson_name}'.
    Trả lời theo định dạng:
    Câu hỏi: ...
    Đáp án: ...
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là giáo viên toán tạo câu hỏi cho học sinh."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        result = response['choices'][0]['message']['content'].strip()
        # Tách câu hỏi và đáp án nếu có
        parts = result.split("Đáp án:")
        question_text = parts[0].replace("Câu hỏi:", "").strip()
        answer_text = parts[1].strip() if len(parts) > 1 else "Học sinh tự trả lời"
        return question_text, answer_text
    except Exception as e:
        return f"Lỗi khi tạo câu hỏi: {e}", ""

# --- Giao diện Streamlit ---
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
        st.session_state.answer = None

    if load and grade and chapter and lesson:
        st.info("Đang tạo câu hỏi, vui lòng chờ...")
        question, answer = generate_question(lesson)
        st.session_state.question = question
        st.session_state.answer = answer

    if st.session_state.question:
        st.write("### ❓ " + st.session_state.question)
        ans = st.text_input("Nhập đáp án:", key="ans_question")
        if st.button("Kiểm tra đáp án"):
            if ans.strip() == st.session_state.answer:
                st.success("🎉 Đúng rồi!")
            else:
                st.info(f"Đáp án tham khảo: {st.session_state.answer}")
