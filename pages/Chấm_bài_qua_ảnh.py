import streamlit as st
import json
import random
import os

# --- FILE CURRICULUM ---
CUR_FILE = "curriculum.json"

# Nếu chưa có file → tạo khung mặc định Lớp 1→9
if not os.path.exists(CUR_FILE):
    curriculum = {}
    for grade in range(1, 10):
        curriculum[f"Lớp {grade}"] = {
            f"Chương {i+1}": [f"Bài {j+1}" for j in range(5)]
            for i in range(3)
        }
    with open(CUR_FILE, "w", encoding="utf8") as f:
        json.dump(curriculum, f, ensure_ascii=False, indent=2)
    st.info(f"File {CUR_FILE} chưa tồn tại. Đã tạo khung Toán từ lớp 1 đến lớp 9 mặc định.")
else:
    with open(CUR_FILE, "r", encoding="utf8") as f:
        curriculum = json.load(f)

# --- GIAO DIỆN ---
st.set_page_config(page_title="Toán – Kết nối tri thức", layout="wide")
st.title("📘 Toán – Bộ SGK \"Kết nối tri thức với cuộc sống\"")

# --- TẠO CỘT ---
col1, col2 = st.columns([1, 2])

# ------------------ CỘT 1: Chọn lớp/chương/bài ------------------
with col1:
    st.subheader("📚 Chọn bài học")

    grade = st.selectbox("Lớp:", [""] + list(curriculum.keys()))

    # --- Câu hỏi xác nhận lớp ---
    if grade and 'grade_question' not in st.session_state:
        st.session_state.grade_question = {
            "text": f"Bạn có học {grade} KNTT không?",
            "answer": "có",
            "hintVN": f"Hãy xác nhận bạn đang học {grade}.",
            "hintHM": f"Xav tau koj kawm {grade}."
        }
        st.session_state.grade_confirmed = False

    # Hiển thị câu hỏi lớp
    if grade and st.session_state.grade_question and not st.session_state.get('grade_confirmed', False):
        qg = st.session_state.grade_question
        ans_grade = st.text_input("Nhập đáp án:", key="ans_grade")
        if st.button("Kiểm tra lớp"):
            if ans_grade.strip().lower() == qg["answer"]:
                st.success(f"🎉 Đúng rồi! Bạn thuộc {grade}")
                st.session_state.grade_confirmed = True
            else:
                st.error("❌ Sai rồi.")
                st.info("💡 Gợi ý: " + qg["hintVN"])
                st.warning("🧠 H'Mông: " + qg["hintHM"])

    # Chỉ cho chọn chương/bài khi đã xác nhận lớp
    if st.session_state.get('grade_confirmed', False):
        chapter = st.selectbox("Chương / Tập:", [""] + list(curriculum[grade].keys()))
        lesson = None
        if chapter:
            lesson = st.selectbox("Bài học:", [""] + curriculum[grade][chapter])
        load = st.button("Đặt bài")
    else:
        chapter = lesson = load = None

# ------------------ CỘT 2: Làm bài ------------------
with col2:
    st.subheader("✏️ Làm bài")

    if 'question' not in st.session_state:
        st.session_state.question = None

    # Nếu nhấn "Đặt bài" → sinh câu hỏi minh họa
    if load and grade and chapter and lesson:
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        st.session_state.question = {
            "text": f"Tính: {a} + {b} = ?",
            "answer": a + b,
            "hintVN": "Cộng hai số lại.",
            "hintHM": "Ntxiv ob tus naj."
        }

    if st.session_state.question is None:
        if st.session_state.get('grade_confirmed', False):
            st.info("Chọn chương → bài rồi nhấn “Đặt bài” để bắt đầu.")
        else:
            st.info("Chọn lớp và xác nhận trước khi làm bài.")
    else:
        q = st.session_state.question
        st.write("### ❓ " + q["text"])
        ans = st.text_input("Nhập đáp án:", key="ans_question")
        if st.button("Kiểm tra đáp án"):
            try:
                if float(ans) == q["answer"]:
                    st.success("🎉 Đúng rồi!")
                else:
                    st.error(f"❌ Sai rồi. Đáp án đúng: {q['answer']}")
                    st.info("💡 Gợi ý (Tiếng Việt): " + q["hintVN"])
                    st.warning("🧠 H'Mông: " + q["hintHM"])
            except:
                st.error("Nhập số hợp lệ nhé.")
