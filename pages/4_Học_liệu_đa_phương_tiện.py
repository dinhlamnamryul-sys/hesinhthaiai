import streamlit as st
import re
import io
import requests
from docx import Document
from gtts import gTTS

# ===============================
# 1. CẤU HÌNH TRANG
# ===============================
st.set_page_config(page_title="Trợ lý Toán học AI", layout="wide", page_icon="🎓")

st.markdown("""
<style>
    .stTabs [aria-selected="true"] { background-color: #ff4b4b !important; color: white !important; }
    .stMarkdown { line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Hệ sinh thái Giáo dục Toán học AI")

# ===============================
# 2. DỮ LIỆU CHƯƠNG TRÌNH HỌC (Đã cập nhật từ yêu cầu của bạn)
# ===============================
chuong_options_lop = {
    "Lớp 6": ["Chương I: Tập hợp các số tự nhiên", "Chương II: Tính chia hết trong tập hợp các số tự nhiên", "Chương III: Số nguyên", "Chương IV: Một số hình phẳng trong thực tiễn", "Chương V: Tính đối xứng của hình phẳng trong tự nhiên", "Chương VI: Phân số", "Chương VII: Số thập phân", "Chương VIII: Những hình hình học cơ bản", "Chương IX: Dữ liệu và xác suất thực nghiệm", "Hoạt động thực hành trải nghiệm"],
    "Lớp 7": ["Chương I: Số hữu tỉ", "Chương II: Số thực", "Chương III: Góc và đường thẳng song song", "Chương IV: Tam giác bằng nhau", "Chương V: Thu thập và biểu diễn dữ liệu", "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ", "Chương VII: Biểu thức đại số và đa thức một biến", "Chương VIII: Làm quen với biến cố và xác suất", "Chương IX: Quan hệ giữa các yếu tố trong một tam giác", "Chương X: Một số hình khối trong thực tiễn", "Bài tập ôn tập cuối năm"],
    "Lớp 8": ["Chương I: Đa thức", "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng", "Chương III: Tứ giác", "Chương IV: Định lí Thalès", "Chương V: Dữ liệu và biểu đồ", "Chương VI: Phân thức đại số", "Chương VII: Phương trình bậc nhất và hàm số bậc nhất", "Chương VIII: Mở đầu về tính xác suất của biến cố", "Chương IX: Tam giác đồng dạng", "Chương X: Một số hình khối trong thực tiễn"],
    "Lớp 9": ["Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn", "Chương II: Phương trình và bất phương trình bậc nhất một ẩn", "Chương III: Căn bậc hai và căn bậc ba", "Chương IV: Hệ thức lượng trong tam giác vuông", "Chương V: Đường tròn", "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn", "Chương VII: Tần số và tần số tương đối", "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản", "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp", "Chương X: Một số hình khối trong thực tiễn"]
}

bai_options_lop = {
    "Lớp 6": {
        "Chương I: Tập hợp các số tự nhiên": ["Bài 1", "Bài 2", "Bài 3", "Bài 4", "Ôn tập"],
        "Chương II: Tính chia hết trong tập hợp các số tự nhiên": ["Bài 5", "Bài 6", "Ôn tập"],
        "Chương III: Số nguyên": ["Bài 7", "Bài 8", "Ôn tập"],
        "Chương IV: Một số hình phẳng trong thực tiễn": ["Bài 9", "Bài 10", "Ôn tập"],
        "Chương VI: Phân số": ["Bài 13", "Bài 14", "Ôn tập"],
        "Chương VII: Số thập phân": ["Bài 15", "Bài 16", "Ôn tập"]
    },
    "Lớp 7": {
        "Chương I: Số hữu tỉ": ["Bài 1. Tập hợp các số hữu tỉ", "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ", "Bài 3. Luỹ thừa số hữu tỉ", "Bài 4. Thứ tự thực hiện phép tính"],
        "Chương II: Số thực": ["Bài 5", "Bài 6. Số vô tỉ. Căn bậc hai số học", "Bài 7. Tập hợp các số thực"],
        "Chương IV: Tam giác bằng nhau": ["Bài 12. Tổng các góc trong một tam giác", "Bài 16. Tam giác cân"]
    },
    "Lớp 8": {
        "Chương I: Đa thức": ["Bài 1. Đơn thức", "Bài 2. Đa thức"],
        "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng": ["Bài 6. Hiệu hai bình phương", "Bài 9. Phân tích đa thức thành nhân tử"],
        "Chương IX: Tam giác đồng dạng": ["Bài 35. Định lí Pythagore và ứng dụng"]
    },
    "Lớp 9": {
        "Chương III: Căn bậc hai và căn bậc ba": ["Bài 7. Căn bậc hai", "Bài 10. Căn bậc ba"],
        "Chương IV: Hệ thức lượng trong tam giác vuông": ["Bài 11. Tỉ số lượng giác", "Bài 12. Hệ thức giữa cạnh và góc"],
        "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn": ["Bài 19. Phương trình bậc hai", "Bài 20. Định lí Viète"]
    }
}

# ===============================
# 3. HÀM XỬ LÝ API (SỬA LỖI MODEL NOT FOUND)
# ===============================
def generate_with_gemini(api_key, prompt):
    # Sửa lỗi: Thêm 'models/' vào trước tên mô hình
    MODEL = "models/gemini-1.5-flash" 
    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if "candidates" in data:
            return {"ok": True, "text": data["candidates"][0]["content"]["parts"][0]["text"]}
        return {"ok": False, "message": data.get("error", {}).get("message", "Lỗi không xác định")}
    except Exception as e:
        return {"ok": False, "message": str(e)}

# ===============================
# 4. GIAO DIỆN STREAMLIT
# ===============================
api_key = st.sidebar.text_input("🔑 Google API Key:", type="password")
if not api_key:
    st.info("Vui lòng nhập API Key ở thanh bên để bắt đầu.")

tab1, tab2, tab3, tab4 = st.tabs(["📘 Kiến thức", "📝 Giáo án", "🎵 Nhạc Toán", "🎧 Đọc TTS"])

# --- TAB 1: TỔNG HỢP KIẾN THỨC ---
with tab1:
    st.subheader("Tổng hợp Kiến thức & Công thức")
    c1, c2, c3 = st.columns(3)
    with c1: lop = st.selectbox("Lớp:", list(chuong_options_lop.keys()))
    with c2: chuong = st.selectbox("Chương:", chuong_options_lop[lop])
    with c3: 
        list_bai = bai_options_lop.get(lop, {}).get(chuong, ["Toàn chương"])
        bai = st.selectbox("Bài:", list_bai)

    if st.button("🚀 Tạo nội dung"):
        prompt = f"""
        Bạn là chuyên gia Toán học. Hãy soạn bài học chi tiết cho: {bai} ({chuong} - {lop}).
        YÊU CẦU QUAN TRỌNG:
        - Sử dụng công thức Toán học định dạng LaTeX chuẩn, bọc trong $$...$$. 
          Ví dụ: $$\\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}}$$.
        - Cấu trúc: 1. Khái niệm, 2. Công thức quan trọng, 3. Ví dụ minh họa, 4. Bài tập.
        """
        with st.spinner("Đang xử lý..."):
            res = generate_with_gemini(api_key, prompt)
            if res["ok"]:
                st.session_state["result"] = res["text"]
                st.markdown(res["text"])
            else:
                st.error(res["message"])

# --- CÁC TAB KHÁC (GIỮ NGUYÊN LOGIC CŨ) ---
with tab2:
    st.write("Tính năng soạn giáo án tự động dựa trên mục lục.")
    if st.button("✍️ Thử soạn giáo án cho bài đã chọn"):
        if "result" in st.session_state:
            prompt_ga = f"Dựa trên nội dung này, hãy soạn giáo án 5 bước phát triển năng lực: {st.session_state['result']}"
            res = generate_with_gemini(api_key, prompt_ga)
            st.write(res["text"])

with tab3:
    st.write("Chuyển công thức thành lời bài hát.")
    if st.button("🎤 Sáng tác vè/rap"):
        prompt_m = f"Viết một bài vè vui nhộn giúp học sinh ghi nhớ kiến thức bài: {bai} - {chuong}."
        res = generate_with_gemini(api_key, prompt_m)
        st.success(res["text"])

with tab4:
    text_input = st.text_area("Nhập văn bản cần đọc:", "Chào các em, hôm nay chúng ta học về căn bậc hai.")
    if st.button("▶️ Nghe đọc"):
        tts = gTTS(text=text_input, lang='vi')
        tts.save("speech.mp3")
        st.audio("speech.mp3")
