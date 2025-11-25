import streamlit as st
import time
from PIL import Image

st.title("📸 Chấm Bài & Giải Toán Qua Ảnh")

uploaded_file = st.file_uploader("Tải ảnh bài làm (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns(2)
    with col1:
        st.image(Image.open(uploaded_file), caption="Ảnh đã tải lên", use_column_width=True)
    with col2:
        st.subheader("Kết quả phân tích (AI):")
        if st.button("🔍 Phân tích ngay"):
            with st.spinner("Đang đọc chữ viết tay..."):
                time.sleep(2) # Giả lập
                st.success("Đã chấm xong!")
                st.markdown("""
                **Đề bài nhận diện:** $2x = 10$
                **Bài làm học sinh:** $x = 5$
                **Kết luận:** ✅ Chính xác!
                **Lời khuyên:** Em làm rất tốt, nhớ trình bày sạch đẹp hơn nhé.
                """)
                st.info("Tiếng Mông: Koj ua tau zoo heev!")
