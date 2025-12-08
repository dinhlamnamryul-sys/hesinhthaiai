import os
import streamlit as st
from groq import Groq  # thư viện chính thức của Groq
from PIL import Image
from io import BytesIO
import base64

# --- Cấu hình Streamlit ---
st.set_page_config(page_title="Chấm Bài AI Song Ngữ (Groq)", page_icon="📸")
st.title("📸 Chấm Bài & Giải Toán Qua Ảnh — thử Groq (text‑only)")

# --- Nhập API Key ---
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None

if not st.session_state['api_key']:
    st.markdown("---")
    st.subheader("🔑 Nhập Groq API Key")
    st.warning("⚠️ Ứng dụng yêu cầu Groq API Key để hoạt động.")
    with st.form("api_key_form"):
        new_key = st.text_input("GROQ API Key:", type="password")
        submitted = st.form_submit_button("Sử dụng API Key")
        if submitted:
            if new_key:
                st.session_state['api_key'] = new_key.strip()
                st.success("✅ Đã lưu API Key!")
                st.rerun()
            else:
                st.error("Vui lòng nhập API Key.")
    st.markdown("Bạn có thể lấy Key tại https://console.groq.com/keys")
    st.markdown("---")
    st.stop()

# --- Init client Groq ---
api_key = st.session_state['api_key']
client = Groq(api_key=api_key)

st.success("✅ Groq API Key đã sẵn sàng.")

# --- Giao diện nhập prompt (text) ---
st.subheader("🧠 Nhập prompt (tiếng Việt hoặc H’Mông, hoặc LaTeX…)")

user_prompt = st.text_area("Prompt cho AI:", height=200)

if st.button("Gửi prompt lên Groq"):
    with st.spinner("⏳ Đang gửi yêu cầu..."):
        try:
            resp = client.chat.completions.create(
                model="llama3-70b-8192",  # bạn có thể chọn model khác Groq hỗ trợ
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            text = resp.choices[0].message.content
            st.markdown("### ✅ Kết quả từ AI:")
            st.markdown(text)
        except Exception as e:
            st.error(f"❌ Lỗi khi gọi Groq API: {e}")
