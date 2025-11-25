import streamlit as st
import requests

st.set_page_config(page_title="Sinh Đề Tự Động", page_icon="📝")
st.title("📝 Sinh Đề Tự Động Theo Yêu Cầu")

# --- LẤY KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    st.warning("⚠️ Chưa có API Key trong hệ thống.")
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- GIAO DIỆN NGƯỜI DÙNG ---
st.sidebar.header("Thông tin sinh đề")
mon = st.sidebar.selectbox("Chọn môn học", ["Toán", "Vật lý", "Hóa học", "Sinh học", "Tin học"])
lop = st.sidebar.selectbox("Chọn lớp", [str(i) for i in range(1, 13)])
chuong = st.sidebar.text_input("Chọn chương (ví dụ: Chương 1, 2, ...) ")
bai = st.sidebar.text_input("Chọn bài (ví dụ: Bài 1, 2, ...) ")
so_cau = st.sidebar.number_input("Số câu hỏi", min_value=1, max_value=50, value=10)
loai_cau = st.sidebar.selectbox("Loại câu hỏi", ["Trắc nghiệm", "Tự luận", "Trộn cả hai"])
co_dap_an = st.sidebar.checkbox("Có đáp án", value=True)

# --- HÀM GỌI AI SINH CÂU HỎI ---
def generate_questions(api_key, mon, lop, chuong, bai, so_cau, loai_cau, co_dap_an):
    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

    prompt = f"""
Bạn là giáo viên {mon} rất giỏi. Sinh một đề kiểm tra cho học sinh lớp {lop}:
- Chương: {chuong}
- Bài: {bai}
- Số câu hỏi: {so_cau}
- Loại câu hỏi: {loai_cau}
- { 'Bao gồm đáp án' if co_dap_an else 'Không cần đáp án' }

Yêu cầu:
- Viết câu hỏi rõ ràng, từng bước nếu là tự luận.
- Nếu có đáp án, ghi ngay sau câu hỏi.
- Dùng danh sách số thứ tự (1., 2., 3., …)
- Nếu là toán, viết công thức bằng LaTeX.
- Ngắn gọn, dễ hiểu cho học sinh.
"""

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return f"❌ Lỗi API {response.status_code}: {response.text}"
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# --- HIỂN THỊ KẾT QUẢ ---
if st.button("🎯 Sinh đề ngay"):
    if not api_key:
        st.error("Thiếu API Key!")
    else:
        with st.spinner("⏳ AI đang tạo đề..."):
            result = generate_questions(api_key, mon, lop, chuong, bai, so_cau, loai_cau, co_dap_an)
            if "❌" in result:
                st.error(result)
            else:
                st.success("🎉 Đã tạo xong đề!")
                st.markdown(result)
