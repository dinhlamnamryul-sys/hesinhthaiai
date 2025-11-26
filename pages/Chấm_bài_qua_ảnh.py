import streamlit as st
import json
import random
import os

# --- ĐỌC KHUNG TOÁN ---
CUR_FILE = "curriculum.json"

# Nếu chưa có file curriculum.json → tạo mặc định từ lớp 1 đến lớp 9
if not os.path.exists(CUR_FILE):
    curriculum = {}
    for grade in range(1, 10):  # Lớp 1 → lớp 9
        curriculum[f"Lớp {grade}"] = {
            f"Chương {i+1}": [f"Bài {j+1}" for j in range(5)]  # Mỗi chương 5 bài ví dụ
            for i in range(3)  # Mỗi lớp 3 chương ví dụ
        }
    # Lưu vào file JSON
    with open(CUR_FILE, "w", encoding="utf8") as f:
        json.dump(curriculum, f, ensure_ascii=False, indent=2)
    st.info(f"File {CUR_FILE} chưa tồn tại. Đã tạo khung Toán từ lớp 1 đến lớp 9 mặc định.")
else:
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
