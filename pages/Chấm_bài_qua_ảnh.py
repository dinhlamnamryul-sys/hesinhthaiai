import streamlit as st

# ===========================
# DATA: SGK Kết nối tri thức
# ===========================

data = {
    "Lớp 6": {
        "Chương 2: Số nguyên": {
            "Cộng trừ số nguyên": [
                {
                    "question": "Tính: -3 + (-11)",
                    "answer": -14,
                    "hintVN": "Cộng hai số nguyên âm: Cộng hai giá trị tuyệt đối rồi đặt dấu trừ.",
                    "hintHM": "Ntxiv ob qho kev sib npaug tsis zoo: ntxiv ob qho ob cho tseem ceeb thiab tom qab muab cov paib rho tawm hauv ntej."
                }
            ]
        }
    }
}

# ===========================
# UI
# ===========================

st.set_page_config(page_title="Học Toán – Kết nối tri thức", layout="wide")

st.title("📘 HỌC TOÁN SGK – KẾT NỐI TRI THỨC")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎯 Chọn bài học")

    # CHỌN LỚP
    grade = st.selectbox("Lớp:", [""] + list(data.keys()))

    # CHỌN CHƯƠNG
    chapter = ""
    if grade:
        chapter = st.selectbox("Chương:", [""] + list(data[grade].keys()))

    # CHỌN BÀI
    lesson = ""
    if chapter:
        lesson = st.selectbox("Bài học:", [""] + list(data[grade][chapter].keys()))

    load_btn = st.button("🚀 Đặt bài")

with col2:
    st.subheader("📌 Câu hỏi")

    # LOGIC SINH CÂU HỎI
    if "currentQ" not in st.session_state:
        st.session_state.currentQ = None

    if load_btn and grade and chapter and lesson:
        st.session_state.currentQ = data[grade][chapter][lesson][0]

    if st.session_state.currentQ is None:
        st.info("Hãy chọn bài học để bắt đầu.")
    else:
        q = st.session_state.currentQ
        st.write(f"### ❓ {q['question']}")

        user_answer = st.text_input("Nhập câu trả lời:")

        if st.button("Kiểm tra"):
            try:
                if float(user_answer) == q["answer"]:
                    st.success("🎉 Đúng rồi! Giỏi lắm!")
                else:
                    st.error(f"❌ Sai rồi! Đáp án đúng: {q['answer']}")

                    st.info(f"💡 Gợi ý (Tiếng Việt): {q['hintVN']}")
                    st.warning(f"🧠 H'Mông: {q['hintHM']}")

            except:
                st.error("Vui lòng nhập số hợp lệ.")

