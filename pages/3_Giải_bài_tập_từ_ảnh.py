# Nếu có ảnh → hiển thị + xử lý
if image:
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(image, caption="Ảnh bài làm", use_column_width=True)

    with col2:
        st.subheader("🔍 Kết quả:")

        if st.button("Phân tích ngay", type="primary"):
            if not api_key:
                st.error("Thiếu API Key!")
            else:
                with st.spinner("⏳ AI đang xử lý..."):

                    # --- PROMPT SONG NGỮ & LaTeX ---
                    prompt_text = """
Bạn là giáo viên Toán giỏi, đọc ảnh bài làm của học sinh. 
Yêu cầu:

1️⃣ Chép lại đề bài bằng **LaTeX**, hiển thị song song:
🇻🇳 (Tiếng Việt)
🟦 (Tiếng H’Mông)

2️⃣ Chấm bài từng bước:
- Nói học sinh **Đúng / Sai** từng bước.
- Nếu sai, ghi ngắn gọn **Sai ở bước nào & lý do**.
- Hiển thị song song:
🇻🇳 Nhận xét tiếng Việt
🟦 Nhận xét H’Mông

3️⃣ Giải chi tiết:
- Viết từng bước bằng **LaTeX**, hiển thị song song:
🇻🇳 Công thức / bước bằng tiếng Việt
🟦 Công thức / bước bằng tiếng H’Mông
- Nếu học sinh sai → giải lại đúng ở cả hai ngôn ngữ.

4️⃣ **QUAN TRỌNG:** Tất cả các công thức toán phải ở dạng LaTeX, ví dụ: 
- Inline: `\(x^2 + y^2 = z^2\)`
- Block: `$$x^2 + y^2 = z^2$$`

MỌI CÂU TRẢ LỜI PHẢI:
- Rõ ràng, đầy đủ, theo thứ tự.
- Song song Việt – H’Mông từng bước.
- Dễ copy vào Word hoặc Overleaf.
"""

                    result = analyze_real_image(api_key, image, prompt_text)

                    if "❌" in result:
                        st.error(result)
                    else:
                        st.success("🎉 Đã phân tích xong!")

                        # Hiển thị LaTeX đúng cách
                        # Streamlit hỗ trợ LaTeX block: st.latex() nhưng cần parse block $$...$$
                        # Đơn giản nhất là render trực tiếp markdown:
                        st.markdown(result, unsafe_allow_html=True)
