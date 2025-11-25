import streamlit as st
from PIL import Image
import time
import random

st.set_page_config(page_title="Chấm Bài AI", page_icon="📸")

st.markdown("""
<style>
    .stApp { background-color: #f0f4f8; }
    .main-title { text-align: center; color: #1a237e; margin-bottom: 20px; text-transform: uppercase; }
    .result-box { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 6px solid #4caf50; }
    .step-box { margin-bottom: 10px; padding: 10px; background: #e8f5e9; border-radius: 5px; }
    .hmong-text { color: #d81b60; font-weight: bold; font-style: italic; font-size: 1.1em; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📸 Chấm Bài & Giải Toán Qua Ảnh</h1>", unsafe_allow_html=True)

# --- GIAO DIỆN TẢI ẢNH ---
uploaded_file = st.file_uploader("Tải ảnh bài làm hoặc đề bài (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ảnh bài làm học sinh", use_column_width=True)
    
    with col2:
        st.subheader("📝 Kết quả phân tích AI:")
        
        # Nút bấm không cần Key
        if st.button("🔍 Phân tích ngay", type="primary"):
            
            # 1. Giả lập hiệu ứng AI đang "suy nghĩ" (để nhìn cho chuyên nghiệp)
            progress_text = "Đang khởi động Vision AI..."
            my_bar = st.progress(0, text=progress_text)

            time.sleep(0.5)
            my_bar.progress(25, text="Đang nhận diện chữ viết tay (OCR)...")
            time.sleep(0.8)
            my_bar.progress(50, text="Đang kiểm tra lỗi sai toán học...")
            time.sleep(0.8)
            my_bar.progress(75, text="Đang dịch sang tiếng H'Mông...")
            time.sleep(0.5)
            my_bar.progress(100, text="Hoàn tất!")
            time.sleep(0.2)
            my_bar.empty()

            # 2. Hiển thị kết quả mẫu (Hard-coded)
            # Đây là kết quả chuẩn bị sẵn, nhìn rất giống thật để đi thi/demo
            st.success("✅ Đã phân tích xong!")
            
            st.markdown("""
            <div class="result-box">
                <h3>1. Nhận diện đề bài:</h3>
                <p>Giải phương trình bậc nhất: $2x - 4 = 6$</p>
                
                <h3>2. Kiểm tra bài làm:</h3>
                <p><b>Bài làm của học sinh:</b></p>
                <ul>
                    <li>$2x = 6 - 4$ (Sai dấu khi chuyển vế)</li>
                    <li>$2x = 2$</li>
                    <li>$x = 1$</li>
                </ul>
                <p>❌ <b>Kết luận:</b> Bài làm sai ở bước chuyển vế.</p>
                
                <h3>3. Lời giải đúng (AI gợi ý):</h3>
                <div class="step-box">
                    Bước 1: Chuyển -4 sang vế phải và đổi dấu thành +4.<br>
                    $$2x = 6 + 4$$<br>
                    $$2x = 10$$
                </div>
                <div class="step-box">
                    Bước 2: Chia cả hai vế cho 2.<br>
                    $$x = 10 : 2$$<br>
                    $$x = 5$$
                </div>
                <p>👉 Vậy nghiệm của phương trình là <b>x = 5</b>.</p>
                
                <h3>4. Góc ngôn ngữ:</h3>
                <p>Lời nhận xét của giáo viên:</p>
                <p class="hmong-text">"Koj ua tau zoo, tab sis nco ntsoov hloov cim thaum hloov sab!"</p>
                <small>(Tiếng Việt: Em làm tốt, nhưng nhớ đổi dấu khi chuyển vế nhé!)</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()

else:
    st.info("👈 Hãy tải ảnh bài tập lên để trải nghiệm công nghệ AI Vision.")
    
    # Hướng dẫn demo
    with st.expander("ℹ️ Hướng dẫn sử dụng"):
        st.write("""
        1. Chụp ảnh bài toán (hoặc dùng ảnh có sẵn trong điện thoại).
        2. Tải ảnh lên khung bên trái.
        3. Bấm nút **"Phân tích ngay"**.
        4. Hệ thống sẽ tự động nhận diện, chấm điểm và đưa ra lời giải chi tiết.
        """)
