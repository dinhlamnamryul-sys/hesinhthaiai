import streamlit as st
import re
import io
import requests
from docx import Document
from gtts import gTTS
import os

# ===============================
# 1. CẤU HÌNH TRANG & GIAO DIỆN
# ===============================
st.set_page_config(page_title="Trợ lý Toán học & Giáo dục AI", layout="wide", page_icon="🎓")
st.title("🎓 Trợ lý Giáo dục Đa năng (Gemini AI)")

# --- CSS tùy chỉnh cho giao diện ---
st.markdown("""
<style>
.block-container { padding-top: 1rem; }
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] { 
    height: 50px; background-color: #f0f2f6; border-radius: 4px; padding: 10px 20px; 
}
.stTabs [aria-selected="true"] { 
    background-color: #ff4b4b !important; color: white !important; 
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 2. 🔑 NHẬP GOOGLE API KEY
# ===============================
with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key để dùng ứng dụng:
1. Truy cập: **https://aistudio.google.com/app/apikey**
2. Đăng nhập Gmail.
3. Nhấn **Create API key**.
4. Copy API Key.
5. Dán vào ô bên dưới.
⚠️ Không chia sẻ API Key cho người khác.
""")

st.subheader("🔐 Nhập Google API Key:")
api_key = st.text_input("Google API Key:", type="password", placeholder="Dán key của bạn vào đây...")

if not api_key:
    st.warning("⚠️ Nhập API Key để tiếp tục.")
    st.stop() # Dừng các lệnh bên dưới nếu chưa có Key
else:
    st.success("✅ API Key hợp lệ!")

# ===============================
# 3. 📚 DỮ LIỆU CHƯƠNG TRÌNH HỌC (Full 6-9)
# ===============================
chuong_options_lop = {
    "Lớp 6": ["Chương I: Tập hợp các số tự nhiên", "Chương II: Tính chia hết trong tập hợp các số tự nhiên", "Chương III: Số nguyên", "Chương IV: Một số hình phẳng trong thực tiễn", "Chương V: Tính đối xứng của hình phẳng trong tự nhiên", "Chương VI: Phân số", "Chương VII: Số thập phân", "Chương VIII: Những hình hình học cơ bản", "Chương IX: Dữ liệu và xác suất thực nghiệm", "Hoạt động thực hành trải nghiệm"],
    "Lớp 7": ["Chương I: Số hữu tỉ", "Chương II: Số thực", "Chương III: Góc và đường thẳng song song", "Chương IV: Tam giác bằng nhau", "Chương V: Thu thập và biểu diễn dữ liệu", "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ", "Chương VII: Biểu thức đại số và đa thức một biến", "Chương VIII: Làm quen với biến cố và xác suất", "Chương IX: Quan hệ giữa các yếu tố trong một tam giác", "Chương X: Một số hình khối trong thực tiễn", "Bài tập ôn tập cuối năm"],
    "Lớp 8": ["Chương I: Đa thức", "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng", "Chương III: Tứ giác", "Chương IV: Định lí Thalès", "Chương V: Dữ liệu và biểu đồ", "Chương VI: Phân thức đại số", "Chương VII: Phương trình bậc nhất và hàm số bậc nhất", "Chương VIII: Mở đầu về tính xác suất của biến cố", "Chương IX: Tam giác đồng dạng", "Chương X: Một số hình khối trong thực tiễn", "Bài tập ôn tập cuối năm"],
    "Lớp 9": ["Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn", "Chương II: Phương trình và bất phương trình bậc nhất một ẩn", "Chương III: Căn bậc hai và căn bậc ba", "Chương IV: Hệ thức lượng trong tam giác vuông", "Chương V: Đường tròn", "Hoạt động thực hành trải nghiệm", "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn", "Chương VII: Tần số và tần số tương đối", "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản", "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp", "Chương X: Một số hình khối trong thực tiễn"]
}

# Dữ liệu bài chi tiết (Rút gọn để hiển thị, bạn có thể thêm đầy đủ vào đây)
bai_options_lop = {
    "Lớp 6": {
        "Chương I: Tập hợp các số tự nhiên": ["Bài 1", "Bài 2", "Bài 3", "Bài 4", "Ôn tập"],
        "Chương VI: Phân số": ["Bài 13", "Bài 14", "Ôn tập"]
    },
    "Lớp 7": {
        "Chương I: Số hữu tỉ": ["Bài 1. Tập hợp các số hữu tỉ", "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ", "Bài 3. Luỹ thừa số hữu tỉ", "Ôn tập"],
        "Chương II: Số thực": ["Bài 5", "Bài 6. Số vô tỉ. Căn bậc hai số học", "Bài 7. Tập hợp các số thực"]
    },
    "Lớp 8": {
        "Chương I: Đa thức": ["Bài 1. Đơn thức", "Bài 2. Đa thức"],
        "Chương IX: Tam giác đồng dạng": ["Bài 33", "Bài 34", "Bài 35. Định lí Pythagore và ứng dụng"]
    },
    "Lớp 9": {
        "Chương III: Căn bậc hai và căn bậc ba": ["Bài 7. Căn bậc hai", "Bài 10. Căn bậc ba"],
        "Chương IV: Hệ thức lượng trong tam giác vuông": ["Bài 11. Tỉ số lượng giác của góc nhọn", "Bài 12. Hệ thức cạnh và góc"],
        "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn": ["Bài 19. Phương trình bậc hai", "Bài 20. Định lí Viète"]
    }
}

# ===============================
# 4. HÀM XỬ LÝ API & TIỆN ÍCH
# ===============================

def generate_with_gemini(api_key, prompt):
    MODEL = "models/gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        data = response.json()
        if "candidates" in data:
            return {"ok": True, "text": data["candidates"][0]["content"]["parts"][0]["text"]}
        return {"ok": False, "message": data.get("error", {}).get("message", "Lỗi API")}
    except Exception as e:
        return {"ok": False, "message": str(e)}

def create_docx_bytes(text):
    doc = Document()
    doc.add_heading('Tài liệu học tập Toán học AI', 0)
    for line in text.split('\n'):
        doc.add_paragraph(line)
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# ===============================
# 5. GIAO DIỆN CHÍNH (TABS)
# ===============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Tổng hợp Kiến thức", "📝 Thiết kế Giáo án", "🎵 Sáng tác Nhạc Toán", "🎧 Đọc Văn bản (TTS)"
])

with tab1:
    st.subheader("📚 Hệ thống kiến thức Toán học 6-9")
    c1, c2, c3 = st.columns(3)
    with c1:
        lop_sel = st.selectbox("Chọn lớp:", list(chuong_options_lop.keys()))
    with c2:
        chuong_list = chuong_options_lop.get(lop_sel, [])
        chuong_sel = st.selectbox("Chọn chương:", chuong_list)
    with c3:
        bai_list = bai_options_lop.get(lop_sel, {}).get(chuong_sel, ["Toàn chương"])
        bai_sel = st.selectbox("Chọn bài học:", bai_list)

    if st.button("🚀 Tổng hợp nội dung"):
        prompt = f"""
        Bạn là giáo viên Toán. Hãy soạn tài liệu chi tiết cho: {bai_sel} - {chuong_sel} ({lop_sel}).
        YÊU CẦU: 
        1. Dùng LaTeX trong $$...$$ cho mọi công thức. Ví dụ: $$\\sqrt{{a+b}}$$
        2. Cấu trúc: Khái niệm -> Công thức -> Ví dụ -> Bài tập.
        """
        with st.spinner("Đang soạn bài..."):
            res = generate_with_gemini(api_key, prompt)
            if res["ok"]:
                st.session_state["math_content"] = res["text"]
                st.markdown(res["text"])
                st.download_button("📥 Tải về Word (.docx)", 
                                   create_docx_bytes(res["text"]), 
                                   f"Toan_{lop_sel}_{bai_sel}.docx")
            else:
                st.error(res["message"])

with tab2:
    st.subheader("📝 Soạn giáo án bài giảng")
    if "math_content" in st.session_state:
        if st.button("✍️ Thiết kế giáo án từ nội dung trên"):
            prompt_ga = f"Soạn giáo án 5 bước phát triển năng lực cho bài học này: {st.session_state['math_content']}"
            res = generate_with_gemini(api_key, prompt_ga)
            st.markdown(res["text"])
    else:
        st.info("Hãy tạo nội dung ở Tab 1 trước để soạn giáo án.")

with tab3:
    st.subheader("🎵 Phổ nhạc kiến thức")
    style = st.selectbox("Chọn phong cách:", ["Rap vui nhộn", "Vè dân gian", "Pop"])
    if st.button("🎤 Sáng tác ngay"):
        prompt_m = f"Viết lời bài hát phong cách {style} để ghi nhớ bài {bai_sel} - {chuong_sel}."
        res = generate_with_gemini(api_key, prompt_m)
        st.success(res["text"])

with tab4:
    st.subheader("🎧 Đọc văn bản tiếng Việt")
    tts_text = st.text_area("Nhập nội dung cần đọc:", "Chào các em học sinh thân mến!")
    if st.button("▶️ Phát âm thanh"):
        tts = gTTS(text=tts_text, lang='vi')
        tts.save("voice.mp3")
        st.audio("voice.mp3")
