import streamlit as st
import re
import io
import base64
import requests
import unicodedata
from docx import Document
from docx.shared import Inches
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
import matplotlib.pyplot as plt
from gtts import gTTS
import os

# ===============================
# 1. CẤU HÌNH TRANG & GIAO DIỆN
# ===============================
st.set_page_config(page_title="Trợ lý Toán học & Giáo dục AI", layout="wide", page_icon="🎓")

st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        background-color: #f0f2f6; 
        border-radius: 4px; 
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #ff4b4b !important; 
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Trợ lý Giáo dục Đa năng (Gemini AI)")

# ===============================
# 2. DỮ LIỆU CHƯƠNG TRÌNH HỌC (Đã cập nhật)
# ===============================
chuong_options_lop = {
    "Lớp 6": ["Chương I: Tập hợp các số tự nhiên", "Chương II: Tính chia hết trong tập hợp các số tự nhiên", "Chương III: Số nguyên", "Chương IV: Một số hình phẳng trong thực tiễn", "Chương V: Tính đối xứng của hình phẳng trong tự nhiên", "Chương VI: Phân số", "Chương VII: Số thập phân", "Chương VIII: Những hình hình học cơ bản", "Chương IX: Dữ liệu và xác suất thực nghiệm", "Hoạt động thực hành trải nghiệm"],
    "Lớp 7": ["Chương I: Số hữu tỉ", "Chương II: Số thực", "Chương III: Góc và đường thẳng song song", "Chương IV: Tam giác bằng nhau", "Chương V: Thu thập và biểu diễn dữ liệu", "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ", "Chương VII: Biểu thức đại số và đa thức một biến", "Chương VIII: Làm quen với biến cố và xác suất", "Chương IX: Quan hệ giữa các yếu tố trong một tam giác", "Chương X: Một số hình khối trong thực tiễn", "Bài tập ôn tập cuối năm"],
    "Lớp 8": ["Chương I: Đa thức", "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng", "Chương III: Tứ giác", "Chương IV: Định lí Thalès", "Chương V: Dữ liệu và biểu đồ", "Chương VI: Phân thức đại số", "Chương VII: Phương trình bậc nhất và hàm số bậc nhất", "Chương VIII: Mở đầu về tính xác suất của biến cố", "Chương IX: Tam giác đồng dạng", "Chương X: Một số hình khối trong thực tiễn", "Bài tập ôn tập cuối năm"],
    "Lớp 9": ["Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn", "Chương II: Phương trình và bất phương trình bậc nhất một ẩn", "Chương III: Căn bậc hai và căn bậc ba", "Chương IV: Hệ thức lượng trong tam giác vuông", "Chương V: Đường tròn", "Hoạt động thực hành trải nghiệm", "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn", "Chương VII: Tần số và tần số tương đối", "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản", "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp", "Chương X: Một số hình khối trong thực tiễn"]
}

bai_options_lop = {
    "Lớp 6": {
        "Chương I: Tập hợp các số tự nhiên": ["Bài 1", "Bài 2", "Bài 3", "Bài 4", "Ôn tập"],
        "Chương II: Tính chia hết trong tập hợp các số tự nhiên": ["Bài 5", "Bài 6", "Ôn tập"],
        "Chương III: Số nguyên": ["Bài 7", "Bài 8", "Ôn tập"],
        "Chương IV: Một số hình phẳng trong thực tiễn": ["Bài 9", "Bài 10", "Ôn tập"],
        "Chương V: Tính đối xứng của hình phẳng trong tự nhiên": ["Bài 11", "Bài 12", "Ôn tập"],
        "Chương VI: Phân số": ["Bài 13", "Bài 14", "Ôn tập"],
        "Chương VII: Số thập phân": ["Bài 15", "Bài 16", "Ôn tập"],
        "Chương VIII: Những hình hình học cơ bản": ["Bài 17", "Bài 18", "Ôn tập"],
        "Chương IX: Dữ liệu và xác suất thực nghiệm": ["Bài 19", "Bài 20", "Ôn tập"],
        "Hoạt động thực hành trải nghiệm": ["Bài 21", "Bài 22", "Ôn tập"]
    },
    "Lớp 7": {
        "Chương I: Số hữu tỉ": ["Bài 1. Tập hợp các số hữu tỉ", "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ", "Bài 3. Luỹ thừa với số mũ tự nhiên của một số hữu tỉ", "Bài 4. Thứ tự thực hiện các phép tính. Quy tắc chuyển vế", "Ôn tập chương I"],
        "Chương II: Số thực": ["Bài 5. Làm quen với số thập phân vô hạn tuần hoàn", "Bài 6. Số vô tỉ. Căn bậc hai số học", "Bài 7. Tập hợp các số thực", "Ôn tập chương II"],
        "Chương III: Góc và đường thẳng song song": ["Bài 8. Góc ở vị trí đặc biệt. Tia phân giác của một góc", "Bài 9. Hai đường thẳng song song và dấu hiệu nhận biết", "Bài 10. Tiên đề Euclid. Tính chất của hai đường thẳng song song", "Bài 11. Định lí và chứng minh định lí", "Ôn tập chương III"],
        "Chương IV: Tam giác bằng nhau": ["Bài 12. Tổng các góc trong một tam giác", "Bài 13. Hai tam giác bằng nhau", "Bài 14. Trường hợp bằng nhau thứ hai và thứ ba", "Bài 15. Các trường hợp bằng nhau của tam giác vuông", "Bài 16. Tam giác cân", "Ôn tập chương IV"],
        "Chương V: Thu thập và biểu diễn dữ liệu": ["Bài 17", "Bài 18", "Bài 19", "Ôn tập"],
        "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ": ["Bài 20. Tỉ lệ thức", "Bài 21. Tính chất dãy tỉ số bằng nhau", "Bài 22. Tỉ lệ thuận", "Bài 23. Tỉ lệ nghịch", "Ôn tập"],
        "Chương VII: Biểu thức đại số và đa thức một biến": ["Bài 24", "Bài 25. Đa thức một biến", "Bài 26", "Bài 27", "Bài 28. Phép chia đa thức", "Ôn tập"],
        "Chương VIII: Làm quen với biến cố và xác suất": ["Bài 29", "Bài 30", "Ôn tập"],
        "Chương IX: Quan hệ giữa các yếu tố trong một tam giác": ["Bài 31", "Bài 32", "Bài 33", "Bài 34", "Bài 35", "Ôn tập"],
        "Chương X: Một số hình khối trong thực tiễn": ["Bài 36", "Bài 37", "Ôn tập"],
        "Bài tập ôn tập cuối năm": ["Ôn tập tổng hợp"]
    },
    "Lớp 8": {
        "Chương I: Đa thức": ["Bài 1. Đơn thức", "Bài 2. Đa thức", "Bài 3", "Bài 4", "Bài 5", "Ôn tập"],
        "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng": ["Bài 6", "Bài 7", "Bài 8", "Bài 9. Phân tích đa thức thành nhân tử", "Ôn tập"],
        "Chương III: Tứ giác": ["Bài 10. Tứ giác", "Bài 11", "Bài 12", "Bài 13", "Bài 14", "Ôn tập"],
        "Chương IV: Định lí Thalès": ["Bài 15. Định lí Thalès", "Bài 16. Đường trung bình", "Bài 17", "Ôn tập"],
        "Chương V: Dữ liệu và biểu đồ": ["Bài 18", "Bài 19", "Bài 20", "Ôn tập"],
        "Chương VI: Phân thức đại số": ["Bài 21", "Bài 22", "Bài 23", "Bài 24", "Ôn tập"],
        "Chương VII: Phương trình bậc nhất và hàm số bậc nhất": ["Bài 25. Phương trình bậc nhất một ẩn", "Bài 26", "Bài 27", "Bài 28", "Bài 29", "Ôn tập"],
        "Chương VIII: Mở đầu về tính xác suất của biến cố": ["Bài 30", "Bài 31", "Bài 32", "Ôn tập"],
        "Chương IX: Tam giác đồng dạng": ["Bài 33", "Bài 34", "Bài 35. Định lí Pythagore", "Bài 36", "Bài 37", "Ôn tập"],
        "Chương X: Một số hình khối trong thực tiễn": ["Bài 38", "Bài 39", "Ôn tập"],
        "Bài tập ôn tập cuối năm": ["Ôn tập tổng hợp"]
    },
    "Lớp 9": {
        "Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn": ["Bài 1", "Bài 2", "Bài 3", "Ôn tập"],
        "Chương II: Phương trình và bất phương trình bậc nhất một ẩn": ["Bài 4", "Bài 5", "Bài 6", "Ôn tập"],
        "Chương III: Căn bậc hai và căn bậc ba": ["Bài 7. Căn bậc hai", "Bài 8", "Bài 9", "Bài 10. Căn bậc ba", "Ôn tập"],
        "Chương IV: Hệ thức lượng trong tam giác vuông": ["Bài 11. Tỉ số lượng giác", "Bài 12", "Ôn tập"],
        "Chương V: Đường tròn": ["Bài 13", "Bài 14", "Bài 15", "Bài 16", "Bài 17", "Ôn tập"],
        "Hoạt động thực hành trải nghiệm": ["Pha chế dung dịch", "Tính chiều cao và khoảng cách"],
        "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn": ["Bài 18", "Bài 19. Phương trình bậc hai", "Bài 20. Định lí Viète", "Bài 21", "Ôn tập"],
        "Chương VII: Tần số và tần số tương đối": ["Bài 22", "Bài 23", "Bài 24", "Ôn tập"],
        "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản": ["Bài 25", "Bài 26", "Ôn tập"],
        "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp": ["Bài 27. Góc nội tiếp", "Bài 28", "Bài 29", "Bài 30", "Ôn tập"],
        "Chương X: Một số hình khối trong thực tiễn": ["Bài 31", "Bài 32", "Ôn tập"]
    }
}

# ===============================
# 3. HÀM XỬ LÝ API GEMINI & TIỆN ÍCH
# ===============================

def generate_with_gemini(api_key, prompt, model="gemini-1.5-flash"):
    if not api_key:
        return {"ok": False, "message": "Vui lòng nhập API Key."}
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        data = response.json()
        if "candidates" in data:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"ok": True, "text": text}
        return {"ok": False, "message": data.get("error", {}).get("message", "Lỗi API")}
    except Exception as e:
        return {"ok": False, "message": str(e)}

def text_to_speech_bytes(text, lang='vi'):
    try:
        tts = gTTS(text=text, lang=lang)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except: return None

# (Hàm tạo DOCX đơn giản hỗ trợ text)
def create_docx_bytes(text):
    doc = Document()
    doc.add_heading('Tài liệu học tập Toán học', 0)
    for line in text.split('\n'):
        doc.add_paragraph(line)
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# ===============================
# 4. GIAO DIỆN CHÍNH (TABS)
# ===============================
api_key = st.sidebar.text_input("🔑 Nhập Google API Key:", type="password")

tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Tổng hợp Kiến thức", 
    "📝 Thiết kế Giáo án", 
    "🎵 Sáng tác Lời bài hát", 
    "🎧 Đọc Văn bản (TTS)"
])

# --- TAB 1: TỔNG HỢP KIẾN THỨC ---
with tab1:
    st.subheader("📚 Chuyên gia tổng hợp kiến thức Toán học")
    
    col_l, col_c, col_b = st.columns(3)
    with col_l:
        lop_sel = st.selectbox("Chọn lớp:", list(chuong_options_lop.keys()), key="t1_lop")
    with col_c:
        chuong_list = chuong_options_lop.get(lop_sel, [])
        chuong_sel = st.selectbox("Chọn chương:", chuong_list, key="t1_chuong")
    with col_b:
        bai_list = bai_options_lop.get(lop_sel, {}).get(chuong_sel, ["Toàn chương"])
        bai_sel = st.selectbox("Chọn bài học:", bai_list, key="t1_bai")

    if st.button("🚀 Bắt đầu tổng hợp", key="btn_t1"):
        prompt = f"""
        Bạn là giáo viên Toán giàu kinh nghiệm. Hãy soạn tài liệu học tập chi tiết cho {bai_sel} thuộc {chuong_sel} - {lop_sel}.
        
        YÊU CẦU ĐỊNH DẠNG:
        1. Sử dụng LaTeX cho MỌI công thức toán học, đặt trong cặp $$...$$. 
           Ví dụ: $$\\frac{{a}}{{b}}$$, $$x^2 + y^2 = z^2$$, $$\\sqrt{{25}} = 5$$.
        2. Cấu trúc bài viết:
           - Mục tiêu bài học.
           - Khái niệm & Định nghĩa quan trọng.
           - Công thức (trình bày rõ ràng bằng LaTeX).
           - 2 Ví dụ minh họa có lời giải chi tiết.
           - 3 Bài tập luyện tập (kèm đáp án tóm tắt).
        
        Phong cách: Ngôn ngữ giáo dục Việt Nam, dễ hiểu cho học sinh THCS.
        """
        
        with st.spinner("Đang biên soạn kiến thức..."):
            res = generate_with_gemini(api_key, prompt)
            if res["ok"]:
                st.session_state["t1_result"] = res["text"]
            else:
                st.error(res["message"])

    if "t1_result" in st.session_state:
        st.markdown("---")
        # Hiển thị kết quả với hỗ trợ LaTeX
        st.markdown(st.session_state["t1_result"])
        
        # Nút tải về
        st.download_button("📥 Tải về bản Word (.docx)", 
                           create_docx_bytes(st.session_state["t1_result"]), 
                           f"KienThuc_{lop_sel}_{bai_sel}.docx")

# --- TAB 2: THIẾT KẾ GIÁO ÁN ---
with tab2:
    st.subheader("📝 Trợ lý soạn giáo án 5 bước")
    col_ga1, col_ga2 = st.columns(2)
    with col_ga1:
        ga_lop = st.selectbox("Lớp:", list(chuong_options_lop.keys()), key="ga_lop")
        ga_bai = st.text_input("Tên bài giảng:", "Định lý Pythagore")
    with col_ga2:
        ga_time = st.number_input("Thời lượng (phút):", 45, 90, 45)
        ga_kieu = st.selectbox("Hình thức:", ["Khám phá mới", "Luyện tập", "Trải nghiệm sáng tạo"])

    if st.button("✍️ Soạn giáo án ngay", key="btn_ga"):
        prompt_ga = f"Soạn giáo án chi tiết bài {ga_bai} cho {ga_lop}, thời lượng {ga_time} phút theo hướng phát triển năng lực. Bao gồm: Mục tiêu, Thiết bị dạy học, và 4 hoạt động (Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng)."
        with st.spinner("Đang lập kế hoạch bài dạy..."):
            res = generate_with_gemini(api_key, prompt_ga)
            if res["ok"]:
                st.session_state["ga_result"] = res["text"]
            else:
                st.error(res["message"])
    
    if "ga_result" in st.session_state:
        st.markdown(st.session_state["ga_result"])

# --- TAB 3: SÁNG TÁC LỜI BÀI HÁT ---
with tab3:
    st.subheader("🎵 Phổ nhạc kiến thức Toán học")
    music_topic = st.text_input("Chủ đề cần sáng tác (VD: Công thức nghiệm phương trình bậc 2):")
    music_style = st.selectbox("Giai điệu:", ["Rap vui nhộn", "Vè dân gian", "Pop Ballad", "Nhạc thiếu nhi"])
    
    if st.button("🎤 Sáng tác", key="btn_music"):
        prompt_m = f"Hãy sáng tác một bài {music_style} về chủ đề toán học: {music_topic}. Lời bài hát phải giúp học sinh dễ thuộc công thức và ghi nhớ kiến thức lâu hơn."
        with st.spinner("AI đang viết lời..."):
            res = generate_with_gemini(api_key, prompt_m)
            if res["ok"]:
                st.session_state["music_res"] = res["text"]
            else:
                st.error(res["message"])
                
    if "music_res" in st.session_state:
        st.text_area("Lời bài hát:", st.session_state["music_res"], height=300)

# --- TAB 4: ĐỌC VĂN BẢN (TTS) ---
with tab4:
    st.subheader("🎧 Chuyển đổi văn bản thành giọng nói")
    tts_input = st.text_area("Nhập văn bản cần đọc:", height=200)
    if st.button("▶️ Phát âm thanh"):
        if tts_input:
            audio = text_to_speech_bytes(tts_input)
            if audio:
                st.audio(audio)
            else:
                st.error("Lỗi tạo âm thanh.")

# ===============================
# 5. FOOTER
# ===============================
st.markdown("---")
st.caption("Ứng dụng được phát triển nhằm hỗ trợ giáo dục Toán học THCS với sức mạnh của AI.")
