# app.py — Ứng dụng Streamlit: Tổng hợp Toán + AI Features
import re
import io
import json
import requests
import streamlit as st
from docx import Document
from docx.shared import Inches
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
import matplotlib.pyplot as plt
from gtts import gTTS  # Thư viện mới để đọc văn bản

# -----------------------
# Cấu hình page
# -----------------------
st.set_page_config(page_title="Trợ lý Toán học & Giáo dục AI", layout="wide", page_icon="🎓")
st.title("🎓 Trợ lý Giáo dục Đa năng (Gemini API)")

st.markdown("""
<style>
.block-container { padding-top: 1rem; }
.stTabs [data-baseweb="tab-list"] { gap: 2px; }
.stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 4px 4px 0 0; gap: 1px; padding-top: 10px; padding-bottom: 10px; }
.stTabs [aria-selected="true"] { background-color: #ffffff; border-top: 2px solid #ff4b4b; }
</style>
""", unsafe_allow_html=True)

# -----------------------
# API Key & Config
# -----------------------
api_key = st.secrets.get("GOOGLE_API_KEY", "")
with st.sidebar:
    st.header("⚙️ Cấu hình")
    if not api_key:
        api_key = st.text_input("Nhập Google API Key:", type="password")
    
    MODEL_DEFAULT = st.selectbox("Chọn model AI:",
                                 ["models/gemini-2.0-flash", "models/gemini-1.5-flash", "models/gemini-1.5-pro"])
    st.info("Lưu ý: Tính năng đọc văn bản cần kết nối internet.")

# -----------------------
# Hỗ trợ LaTeX → ảnh (GIỮ NGUYÊN)
# -----------------------
LATEX_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)

def find_latex_blocks(text):
    return [(m.span(), m.group(0), m.group(1)) for m in LATEX_RE.finditer(text)]

def render_latex_png_bytes(latex_code, fontsize=20, dpi=200):
    try:
        fig = plt.figure()
        fig.patch.set_alpha(0.0)
        fig.text(0, 0, f"${latex_code}$", fontsize=fontsize)
        buf = io.BytesIO()
        plt.axis('off')
        plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', pad_inches=0.02, transparent=True)
        plt.close(fig)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None

# -----------------------
# Xuất DOCX / PDF (GIỮ NGUYÊN)
# -----------------------
def create_docx_bytes(text):
    doc = Document()
    last = 0
    for span, full, inner in find_latex_blocks(text):
        start, end = span
        before = text[last:start]
        for line in before.splitlines():
            doc.add_paragraph(line)
        try:
            png_bytes = render_latex_png_bytes(inner)
            if png_bytes:
                img_stream = io.BytesIO(png_bytes)
                p = doc.add_paragraph()
                r = p.add_run()
                r.add_picture(img_stream, width=Inches(3))
            else:
                doc.add_paragraph(full)
        except Exception:
            doc.add_paragraph(full)
        last = end
    for line in text[last:].splitlines():
        doc.add_paragraph(line)
    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    return out

def create_pdf_bytes(text):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    margin = 40
    y = height - 50
    last = 0
    
    def check_page_break(current_y):
        if current_y < 60:
            c.showPage()
            return height - 50
        return current_y

    for span, full, inner in find_latex_blocks(text):
        start, end = span
        before = text[last:start]
        for line in before.splitlines():
            c.drawString(margin, y, line)
            y -= 14
            y = check_page_break(y)
        try:
            png_bytes = render_latex_png_bytes(inner)
            if png_bytes:
                img_reader = ImageReader(io.BytesIO(png_bytes))
                img = Image.open(io.BytesIO(png_bytes))
                draw_w = 300
                draw_h = img.height / img.width * draw_w
                if y - draw_h < 60:
                    c.showPage()
                    y = height - 50
                c.drawImage(img_reader, margin, y - draw_h, width=draw_w, height=draw_h, mask='auto')
                y -= draw_h + 8
            else:
                c.drawString(margin, y, full)
                y -= 14
        except Exception:
            c.drawString(margin, y, full)
            y -= 14
        y = check_page_break(y)
        last = end
    
    for line in text[last:].splitlines():
        c.drawString(margin, y, line)
        y -= 14
        y = check_page_break(y)
    
    c.save()
    buf.seek(0)
    return buf

# -----------------------
# HÀM GIÚP: Xử lý API (GIỮ NGUYÊN & BỔ SUNG)
# -----------------------
def extract_text_from_api_response(data):
    if isinstance(data, dict) and "candidates" in data:
        cands = data.get("candidates") or []
        for cand in cands:
            text = deep_find_first_string(cand)
            if text: return text
    text = deep_find_first_string(data)
    return text if text else None

def deep_find_first_string(obj, keys=["text", "output", "content"]):
    if isinstance(obj, dict):
        for k in keys:
            if k in obj and isinstance(obj[k], str): return obj[k]
        for v in obj.values():
            res = deep_find_first_string(v, keys)
            if res: return res
    elif isinstance(obj, list):
        for item in obj:
            res = deep_find_first_string(item, keys)
            if res: return res
    return None

def generate_with_gemini(api_key, prompt, model=MODEL_DEFAULT):
    if not api_key: return {"ok": False, "message": "Thiếu API Key."}
    url = f"https://generativelanguage.googleapis.com/v1/{model}:generateContent?key={api_key}"
    payload = {"contents":[{"role":"user","parts":[{"text":prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        data = resp.json()
        if "error" in data: return {"ok": False, "message": data["error"]["message"]}
        text = extract_text_from_api_response(data)
        if text: return {"ok": True, "text": text}
        return {"ok": False, "message": "Không tìm thấy text.", "raw": data}
    except Exception as e:
        return {"ok": False, "message": str(e)}

# -----------------------
# TÍNH NĂNG MỚI: TEXT TO SPEECH
# -----------------------
def text_to_speech_bytes(text, lang='vi'):
    try:
        tts = gTTS(text=text, lang=lang)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except Exception as e:
        return None

# -----------------------
# GIAO DIỆN CHÍNH (TABS)
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Tổng hợp Kiến thức", 
    "📝 Thiết kế Giáo án", 
    "🎵 Sáng tác Lời bài hát", 
    "🎧 Đọc Văn bản (TTS)"
])

# --- TAB 1: TỔNG HỢP KIẾN THỨC (Cũ) ---
with tab1:
    st.subheader("Tổng hợp kiến thức Toán theo chủ đề")
    col1, col2 = st.columns([1, 3])
    with col1:
        lop_options = [f"Lớp {i}" for i in range(1, 10)] + ["Tất cả lớp"]
        lop_sel = st.selectbox("Chọn lớp:", lop_options, key="tab1_lop")
        
    if st.button("🚀 Tổng hợp kiến thức", key="btn_tab1"):
        prompt = f"""
        Bạn là giáo viên Toán. Hãy tổng hợp kiến thức môn Toán {lop_sel} theo CHỦ ĐỀ.
        - Phân nhóm: Số học, Đại số, Hình học, Thống kê.
        - Cấu trúc: Khái niệm – Công thức (LaTeX trong $$...$$) – Ví dụ.
        - Trình bày rõ ràng để in ấn.
        """
        with st.spinner("Đang tổng hợp..."):
            res = generate_with_gemini(api_key, prompt)
            if res["ok"]:
                st.session_state["summary_text"] = res["text"]
            else:
                st.error(res["message"])

    if "summary_text" in st.session_state:
        st.markdown(st.session_state["summary_text"].replace("\n", "<br>"), unsafe_allow_html=True)
        
        # Nút tải về
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            docx = create_docx_bytes(st.session_state["summary_text"])
            st.download_button("📥 Tải DOCX", docx, "KienThucToan.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        with col_d2:
            pdf = create_pdf_bytes(st.session_state["summary_text"])
            st.download_button("📥 Tải PDF", pdf, "KienThucToan.pdf", "application/pdf")

# --- TAB 2: THIẾT KẾ GIÁO ÁN (Mới) ---
with tab2:
    st.subheader("Trợ lý soạn giáo án (Lesson Plan)")
    c1, c2, c3 = st.columns(3)
    with c1:
        ga_lop = st.selectbox("Lớp:", [f"Lớp {i}" for i in range(1, 10)], key="ga_lop")
    with c2:
        ga_bai = st.text_input("Tên bài học:", "Phương trình bậc nhất một ẩn")
    with c3:
        ga_phut = st.number_input("Thời lượng (phút):", value=45)

    ga_yeucau = st.text_area("Yêu cầu thêm (VD: hoạt động nhóm, trò chơi, ứng dụng thực tế...):", height=100)

    if st.button("✍️ Soạn giáo án", key="btn_ga"):
        prompt_ga = f"""
        Soạn giáo án chi tiết cho bài học: "{ga_bai}" môn Toán {ga_lop}.
        Thời lượng: {ga_phut} phút.
        Yêu cầu đặc biệt: {ga_yeucau}.
        Cấu trúc giáo án (theo hướng phát triển năng lực):
        1. Mục tiêu (Kiến thức, Năng lực, Phẩm chất).
        2. Chuẩn bị (GV, HS).
        3. Tiến trình dạy học:
           - Hoạt động 1: Khởi động (Mở đầu).
           - Hoạt động 2: Hình thành kiến thức mới.
           - Hoạt động 3: Luyện tập.
           - Hoạt động 4: Vận dụng & Tìm tòi mở rộng.
        Trình bày chi tiết hoạt động của GV và HS.
        """
        with st.spinner("Đang soạn giáo án..."):
            res = generate_with_gemini(api_key, prompt_ga)
            if res["ok"]:
                st.session_state["plan_text"] = res["text"]
            else:
                st.error(res["message"])

    if "plan_text" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state["plan_text"])
        docx_ga = create_docx_bytes(st.session_state["plan_text"])
        st.download_button("📥 Tải Giáo án (DOCX)", docx_ga, f"GiaoAn_{ga_bai}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# --- TAB 3: CHẾ LỜI BÀI HÁT (Mới) ---
with tab3:
    st.subheader("Sáng tác nhạc Toán học 🎵")
    st.write("Biến công thức khô khan thành giai điệu dễ nhớ!")
    
    col_music1, col_music2 = st.columns(2)
    with col_music1:
        music_topic = st.text_input("Chủ đề toán muốn phổ nhạc:", "Bảng cửu chương 7")
    with col_music2:
        music_style = st.selectbox("Phong cách nhạc:", ["Rap sôi động", "Vè dân gian", "Hò đối đáp", "Pop Ballad nhẹ nhàng", "Thơ lục bát"])

    if st.button("🎤 Sáng tác ngay", key="btn_music"):
        prompt_music = f"""
        Hãy đóng vai một nhạc sĩ tài ba. Sáng tác lời bài hát về chủ đề toán học: "{music_topic}".
        Phong cách: {music_style}.
        Đối tượng: Học sinh.
        Yêu cầu:
        - Lời lẽ vui tươi, hóm hỉnh, dễ nhớ.
        - Lồng ghép chính xác kiến thức toán học.
        - Có phân đoạn rõ ràng (Verse, Chorus/Điệp khúc).
        """
        with st.spinner("Nhạc sĩ AI đang phiêu..."):
            res = generate_with_gemini(api_key, prompt_music)
            if res["ok"]:
                st.session_state["lyrics_text"] = res["text"]
            else:
                st.error(res["message"])

    if "lyrics_text" in st.session_state:
        st.info("💡 Gợi ý: Bạn có thể copy lời này và dùng Suno AI hoặc Udio để tạo nhạc beat!")
        st.text_area("Lời bài hát:", st.session_state["lyrics_text"], height=300)
        
        # Nút đọc thử lời bài hát
        if st.button("🔊 Nghe lời bài hát (Đọc mẫu)", key="btn_read_lyrics"):
            audio_bytes = text_to_speech_bytes(st.session_state["lyrics_text"])
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')

# --- TAB 4: ĐỌC VĂN BẢN (TTS) (Mới) ---
with tab4:
    st.subheader("Công cụ Đọc văn bản (Text-to-Speech)")
    tts_text = st.text_area("Nhập văn bản muốn đọc:", "Chào các em học sinh, hôm nay chúng ta sẽ học bài Định lý Py-ta-go.")
    
    c_tts1, c_tts2 = st.columns([1, 4])
    with c_tts1:
        lang_code = st.selectbox("Ngôn ngữ:", ["vi", "en"])
    
    if st.button("▶️ Đọc ngay", key="btn_tts"):
        if tts_text:
            with st.spinner("Đang tạo file âm thanh..."):
                audio_data = text_to_speech_bytes(tts_text, lang=lang_code)
                if audio_data:
                    st.success("Đã tạo xong!")
                    st.audio(audio_data, format='audio/mp3')
                else:
                    st.error("Lỗi khi tạo âm thanh (kiểm tra kết nối mạng).")
        else:
            st.warning("Vui lòng nhập nội dung cần đọc.")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.caption("Developed with ❤️ using Streamlit & Gemini AI.")
