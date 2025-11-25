import streamlit as st
import requests

st.set_page_config(page_title="Sinh Đề KNTC", page_icon="📝")
st.title("📝 Sinh Đề Tự Động – Kết nối tri thức với cuộc sống")

# --- LẤY KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    st.warning("⚠️ Chưa có API Key trong hệ thống.")
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- DANH SÁCH LỚP / CHƯƠNG / BÀI ---
# Ví dụ: Lớp 1 → Chương 1-5 → Bài 1-5 (có thể mở rộng cho lớp 1-9)
lop_options = [f"Lớp {i}" for i in range(1, 10)]
chuong_options = {f"Lớp {i}": [f"Chương {j}" for j in range(1, 6)] for i in range(1, 10)}
bai_options = {f"Chương {i}": [f"Bài {j}" for j in range(1, 6)] for i in range(1, 6)}

# --- GIAO DIỆN CHỌN LỚP – CHƯƠNG – BÀI ---
lop = st.selectbox("Chọn lớp", lop_options)
chuong = st.selectbox("Chọn chương", chuong_options[lop])
bai = st.selectbox("Chọn bài", bai_options[chuong])

so_cau = st.number_input("Số câu hỏi", min_value=1, max_value=50, value=10)
loai_cau = st.selectbox("Loại câu hỏi", ["Trắc nghiệm", "Tự luận", "Trộn cả hai"])
co_dap_an = st.checkbox("Có đáp án", value=True)

# --- HÀM GỌI AI ---
def generate_questions(api_key, mon, lop, chuong, bai, so_cau, loai_cau, co_dap_an):
    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

    prompt = f"""
Bạn là giáo viên {mon} rất giỏi. Sinh đề kiểm tra theo sách "Kết nối tri thức với cuộc sống":
- Lớp: {lop}
- Chương: {chuong}
- Bài: {bai}
- Số câu hỏi: {so_cau}
- Loại câu hỏi: {loai_cau}
- {'Có đáp án' if co_dap_an else 'Không có đáp án'}

Yêu cầu:
1. Mỗi câu hỏi và đáp án cách nhau rõ ràng (cách dòng hoặc cách ký hiệu "---").
2. Nếu có đáp án, viết sau câu hỏi, cách nhau ít nhất 2 dòng.
3. Nếu là toán, viết công thức bằng LaTeX.
4. Dùng danh sách số thứ tự 1., 2., 3., ...
5. Ngắn gọn, dễ hiểu cho học sinh.
"""

    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}

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
            result = generate_questions(api_key, "Toán", lop, chuong, bai, so_cau, loai_cau, co_dap_an)
            if "❌" in result:
                st.error(result)
            else:
                st.success("🎉 Đã tạo xong đề!")
                st.markdown(result.replace("\n\n", "\n<br>\n"))  # giữ khoảng cách rõ ràng giữa câu hỏi và đáp án
