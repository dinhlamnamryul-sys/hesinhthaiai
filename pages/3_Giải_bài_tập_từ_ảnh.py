import streamlit as st
import requests
import json

st.set_page_config(page_title="Check Gemini Models", page_icon="🔍", layout="wide")

st.title("🔍 Kiểm tra danh sách model của Gemini API")

api_key = st.text_input("Nhập Google API Key:", type="password")

if st.button("🔎 Kiểm tra"):
    if not api_key:
        st.error("❌ Vui lòng nhập API Key!")
    else:
        st.info("⏳ Đang kiểm tra model…")

        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

        try:
            response = requests.get(url, timeout=30)
            data = response.json()

            if response.status_code != 200:
                st.error(f"❌ Lỗi HTTP {response.status_code}: {data}")
            else:
                st.success("✔ Danh sách Model bạn được phép dùng:")
                st.json(data)

                # Lọc model có hỗ trợ generateContent
                models = data.get("models", [])
                gen_models = [
                    m["name"] for m in models 
                    if "generateContent" in m.get("supportedGenerationMethods", [])
                ]

                st.subheader("📌 Model hỗ trợ generateContent:")
                if gen_models:
                    for m in gen_models:
                        st.code(m)
                else:
                    st.error("❌ API Key của bạn KHÔNG có model nào hỗ trợ generateContent!")

        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")
