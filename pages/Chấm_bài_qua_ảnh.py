with col1:
    st.subheader("📚 Chọn bài học")

    grade = st.selectbox("Lớp:", [""] + list(curriculum.keys()))

    # --- Nếu chọn lớp, hiển thị câu hỏi nhận biết lớp ---
    if grade and 'grade_question' not in st.session_state:
        st.session_state.grade_question = {
            "text": f"Bạn có học {grade} KNTT không?",
            "answer": "có",
            "hintVN": f"Hãy xác nhận bạn đang học {grade}.",
            "hintHM": f"Xav tau koj kawm {grade}."
        }

    # Hiển thị câu hỏi nhận biết lớp
    if grade and st.session_state.grade_question:
        qg = st.session_state.grade_question
        st.write("### ❓ " + qg["text"])
        ans_grade = st.text_input("Nhập đáp án:", key="ans_grade")
        if st.button("Kiểm tra lớp"):
            if ans_grade.strip().lower() == qg["answer"]:
                st.success("🎉 Đúng rồi! Bạn thuộc " + grade)
            else:
                st.error("❌ Sai rồi.")
                st.info("💡 Gợi ý: " + qg["hintVN"])
                st.warning("🧠 H'Mông: " + qg["hintHM"])

    # Sau khi xác nhận lớp → chọn chương/bài
    chapter = None
    if grade:
        chapter = st.selectbox("Chương / Tập:", [""] + list(curriculum[grade].keys()))
    lesson = None
    if chapter:
        lesson = st.selectbox("Bài học:", [""] + curriculum[grade][chapter])

    load = st.button("Đặt bài")
