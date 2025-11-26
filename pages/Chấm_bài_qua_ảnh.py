import streamlit as st
import json
import random
import os

# --- ĐỌC KHUNG TOÁN ---
CUR_FILE = "curriculum.json"

if not os.path.exists(CUR_FILE):
    st.error(f"Không tìm thấy {CUR_FILE}. Vui lòng tạo file cấu trúc trước.")
    st.stop()

with open(CUR_FILE, "r", encoding="utf8") as f:
    curriculum = json.load(f)

# --- GIAO DIỆN ---
st.set_page_config(page_title="Toán – Kết nối tri thức", layout="wide")
st.title("📘 Toán – Bộ SGK \"Kết nối tri thức với cuộc sống\"")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📚 Chọn bài học")

    grade = st.selectbox("Lớp:", [""] + list(curriculum.keys()))
    chapter = None
    if grade:
        chapter = st.selectbox("Chương / Tập:", [""] + list(curriculum[grade].keys()))
    lesson = None
    if chapter:
        lesson = st.selectbox("Bài học:", [""] + curriculum[grade][chapter])

    load = st.button("Đặt bài")

with col2:
    st.subheader("✏️ Làm bài")
    if 'question' not in st.session_state:
        st.session_state.question = None

    if load and grade and chapter and lesson:
        # TẠM: tạo 1 câu hỏi ngẫu nhiên đơn giản (ví dụ cộng trừ)
        # Trong tương lai bạn / nhóm có thể thêm bộ câu hỏi cho mỗi bài
        # Ví dụ: nếu chủ đề là "Các số 0 đến 10" → sinh đếm, so sánh số, ...
        # Ở đây: sinh phép cộng 2 số nhỏ để minh hoạ
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        st.session_state.question = {
            "text": f"Tính: {a} + {b} = ?",
            "answer": a + b,
            "hintVN": "Cộng hai số lại.",
            "hintHM": "Ntxiv ob tus naj."
        }

    if st.session_state.question is None:
        st.info("Chọn lớp → chương → bài rồi nhấn “Đặt bài” để bắt đầu.")
    else:
        q = st.session_state.question
        st.write("### ❓ " + q["text"])
        ans = st.text_input("Nhập đáp án:")

        if st.button("Kiểm tra"):
            try:
                if float(ans) == q["answer"]:
                    st.success("🎉 Đúng rồi!")
                else:
                    st.error(f"❌ Sai rồi. Đáp án đúng: {q['answer']}")
                    st.info("💡 Gợi ý (Tiếng Việt): " + q["hintVN"])
                    st.warning("🧠 H'Mông: " + q["hintHM"])
            except:
                st.error("Nhập số hợp lệ nhé.")
