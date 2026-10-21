import streamlit as st
import random
import os
import json
import io
import base64
import re  
import requests
from gtts import gTTS

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gia sư AI Đa Môn - Bản Mường",
    page_icon="🏔️",
    layout="wide"
)

# --- BỘ ĐẾM LƯỢT TRUY CẬP ---
def update_visit_count():
    count_file = "visit_count.txt"
    if not os.path.exists(count_file):
        with open(count_file, "w") as f:
            f.write("5383") 
            return 5383
    try:
        with open(count_file, "r") as f:
            content = f.read().strip()
            count = int(content) if content else 5383
    except Exception:
        count = 5383
    count += 1
    try:
        with open(count_file, "w") as f:
            f.write(str(count))
    except Exception:
        pass
    return count

if 'visit_count' not in st.session_state:
    st.session_state.visit_count = update_visit_count()

# --- MỤC LỤC BÀI HỌC TỔNG HỢP (LỚP 1 - LỚP 9) ---
DANH_MUC_BAI_HOC = {
    "Lớp 1": {
        "Toán học": {
            "Học kì 1": ["Các số đến 10", "Phép cộng, trừ trong phạm vi 10", "Hình vuông, hình tròn, hình tam giác"],
            "Học kì 2": ["Các số đến 100", "Phép cộng, trừ (không nhớ) trong phạm vi 100", "Đo độ dài: cm"]
        },
        "Tiếng Việt": {
            "Phần Âm - Chữ": ["Nhận biết các chữ cái", "Ghép vần đơn giản", "Tập đọc câu ngắn"],
            "Phần Luyện tập": ["Kể chuyện theo tranh", "Tập viết chữ hoa"]
        }
    },
    "Lớp 2": {
        "Toán học": {
            "Học kì 1": ["Phép cộng, trừ có nhớ trong phạm vi 100", "Bài toán về nhiều hơn, ít hơn", "Ki-lô-gam, Lít"],
            "Học kì 2": ["Phép nhân, phép chia (Bảng 2, 5)", "Các số trong phạm vi 1000", "Đường thẳng, đường cong"]
        },
        "Tiếng Việt": {
            "Đọc hiểu": ["Bài đọc về gia đình", "Bài đọc về thầy cô, trường lớp", "Bài đọc về thiên nhiên"],
            "Luyện từ và câu": ["Từ chỉ sự vật, hoạt động, đặc điểm", "Câu kiểu Ai là gì?, Ai làm gì?"]
        }
    },
    "Lớp 3": {
        "Toán học": {
            "Học kì 1": ["Bảng nhân, chia 3, 4, 6, 7, 8, 9", "Cộng trừ trong phạm vi 1000", "Làm quen với biểu thức"],
            "Học kì 2": ["Các số trong phạm vi 10.000", "Các số trong phạm vi 100.000", "Diện tích hình chữ nhật, hình vuông"]
        },
        "Tiếng Việt": {
            "Đọc hiểu & Tập làm văn": ["Viết đoạn văn kể về người thân", "Viết thư ngắn", "Kể lại một buổi biểu diễn nghệ thuật"]
        },
        "Tiếng Anh": {
            "Từ vựng cơ bản": ["Màu sắc & Đồ vật (Colors & Objects)", "Gia đình (Family)", "Sở thích (Hobbies)"]
        }
    },
    "Lớp 4": {
        "Toán học": {
            "Số tự nhiên": ["Hàng và lớp (Lớp triệu)", "Biểu thức có chứa chữ", "Trung bình cộng"],
            "Bốn phép tính": ["Nhân với số có nhiều chữ số", "Chia cho số có 2, 3 chữ số", "Dấu hiệu chia hết"],
            "Phân số": ["Rút gọn phân số", "Quy đồng mẫu số", "Cộng, trừ, nhân, chia phân số"]
        },
        "Tiếng Việt": {
            "Luyện từ và câu": ["Danh từ, Động từ, Tính từ", "Câu kể Ai làm gì?, Ai thế nào?"],
            "Tập làm văn": ["Cấu tạo bài văn miêu tả đồ vật", "Miêu tả cây cối", "Miêu tả con vật"]
        },
        "Lịch sử & Địa lý": {
            "Lịch sử": ["Nước Văn Lang, Âu Lạc", "Hơn một nghìn năm đấu tranh giành độc lập", "Buổi đầu độc lập"],
            "Địa lý": ["Thiên nhiên và con người ở Hoàng Liên Sơn", "Đồng bằng Bắc Bộ", "Đồng bằng Nam Bộ"]
        }
    },
    "Lớp 5": {
        "Toán học": {
            "Số thập phân": ["Khái niệm số thập phân", "Cộng, trừ, nhân, chia số thập phân", "Tỉ số phần trăm"],
            "Hình học": ["Diện tích tam giác, hình thang", "Chu vi, diện tích hình tròn", "Thể tích hình hộp chữ nhật"],
            "Chuyển động đều": ["Tính Vận tốc, Quãng đường, Thời gian"]
        },
        "Tiếng Việt": {
            "Luyện từ và câu": ["Từ đồng nghĩa, trái nghĩa", "Từ đồng âm, nhiều nghĩa", "Câu ghép"],
            "Tập làm văn": ["Tả cảnh", "Tả người", "Viết đơn, viết thư"]
        },
        "Khoa học": {
            "Con người và sức khỏe": ["Sự sinh sản", "Phòng tránh bệnh tật", "An toàn giao thông"],
            "Vật chất và Năng lượng": ["Sự biến đổi của chất", "Năng lượng điện"]
        }
    },
    "Lớp 6": {
        "Toán học": {
            "Số học": ["Tập hợp số tự nhiên", "Tính chia hết", "Số nguyên"],
            "Phân số & Hình học": ["Phân số", "Số thập phân", "Hình học trực quan"]
        },
        "Ngữ Văn": {
            "Đọc hiểu văn bản": ["Truyện truyền thuyết và cổ tích", "Thơ lục bát", "Ký và Hồi ký"],
            "Thực hành Tiếng Việt": ["Từ đơn, từ phức", "Biện pháp tu từ"]
        },
        "Khoa học Tự nhiên": {
            "Vật lý": ["Lực và tác dụng của lực", "Năng lượng"],
            "Sinh học": ["Tế bào - Đơn vị cơ bản của sự sống"]
        }
    },
    "Lớp 7": {
        "Toán học": {
            "Đại số": ["Số hữu tỉ", "Số thực", "Đại lượng tỉ lệ"],
            "Hình học & Thống kê": ["Góc và Đường thẳng song song", "Tam giác bằng nhau", "Biểu đồ"]
        },
        "Ngữ Văn": {
            "Đọc hiểu": ["Thơ 4 chữ, 5 chữ", "Tục ngữ", "Truyện ngụ ngôn", "Tản văn"],
            "Tiếng Việt": ["Thành ngữ", "Mở rộng thành phần câu"]
        },
        "Khoa học Tự nhiên": {
            "Hóa học": ["Nguyên tử, Nguyên tố", "Phân tử, liên kết hóa học"],
            "Sinh học": ["Trao đổi chất ở sinh vật"]
        }
    },
    "Lớp 8": {
        "Toán học": {
            "Đại số": ["Đa thức", "Hằng đẳng thức đáng nhớ", "Phân thức đại số", "Hàm số bậc nhất"],
            "Hình học": ["Tứ giác", "Định lý Thalès", "Tam giác đồng dạng"]
        },
        "Ngữ Văn": {
            "Đọc hiểu": ["Thơ trào phúng", "Truyện lịch sử", "Truyện ngắn hiện đại"],
            "Tiếng Việt": ["Từ tượng hình, từ tượng thanh", "Thành phần biệt lập"]
        },
        "Khoa học Tự nhiên": {
            "Hóa học": ["Phản ứng hóa học", "Acid, Base, Oxide, Muối"],
            "Vật lý": ["Áp suất", "Khối lượng riêng"]
        }
    },
    "Lớp 9": {
        "Toán học": {
            "Đại số": ["Phương trình, hệ phương trình", "Căn thức", "Hàm số", "Phương trình bậc hai"],
            "Hình học": ["Hệ thức lượng", "Đường tròn", "Hình trụ, hình nón, hình cầu"]
        },
        "Ngữ Văn": {
            "Đọc hiểu": ["Truyện truyền kì", "Thơ tự do", "Nghị luận văn học"],
            "Tiếng Việt": ["Biện pháp tu từ", "Câu rút gọn, câu đặc biệt"]
        },
        "Khoa học Tự nhiên": {
            "Vật lý": ["Điện trở, Định luật Ohm", "Cảm ứng điện từ"],
            "Hóa học": ["Kim loại", "Phi kim", "Hydrocarbon"],
            "Sinh học": ["Di truyền", "Tiến hóa"]
        },
        "Tiếng Anh": {
            "Ngữ pháp": ["Thì hiện tại hoàn thành", "Câu bị động", "Câu điều kiện", "Mệnh đề quan hệ"]
        }
    }
}

# --- CSS PHONG CÁCH THỔ CẨM ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    .stApp { background-color: #f0f4f8; background-image: radial-gradient(#dde1e7 1px, transparent 1px); background-size: 20px 20px; }
    .hmong-header-container { background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden; margin-bottom: 30px; border: 2px solid #e0e0e0; }
    .hmong-top-bar { background: linear-gradient(90deg, #1a237e, #3949ab); color: white; padding: 10px 20px; text-align: center; font-size: 0.9rem; letter-spacing: 1px; text-transform: uppercase; }
    .hmong-main-title { padding: 30px 20px; text-align: center; background: white; }
    .hmong-main-title h1 { color: #d32f2f; font-size: 2.5rem; font-weight: 900; margin: 0; text-shadow: 2px 2px 0px #ffcdd2; }
    .hmong-main-title h2 { color: #283593; font-size: 1.5rem; font-weight: 700; margin-top: 10px; }
    .hmong-pattern { height: 12px; background: repeating-linear-gradient(45deg, #d32f2f, #d32f2f 15px, #ffeb3b 15px, #ffeb3b 30px, #388e3c 30px, #388e3c 45px, #1976d2 45px, #1976d2 60px); width: 100%; }
    .problem-box { background-color: white; padding: 30px; border-radius: 20px; border: 2px solid #e0e0e0; border-top: 8px solid #1a237e; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: left; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(to right, #d32f2f, #b71c1c); color: white; border: none; border-radius: 30px; font-weight: bold; font-size: 16px; padding: 0.6rem 2rem; transition: transform 0.2s; width: 100%; box-shadow: 0 4px 6px rgba(211, 47, 47, 0.3); }
    .stButton>button:hover { transform: scale(1.05); color: white; }
    .hint-container { background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 15px; border-radius: 8px; margin-top: 20px; color: #1b5e20; font-size: 1.1rem; }
    .hmong-hint { background-color: #fce4ec; border-left: 5px solid #e91e63; padding: 15px; border-radius: 8px; margin-top: 10px; font-style: italic; color: #880e4f; font-size: 1.1rem; }
    .error-box { background-color: #ffebee; border: 1px solid #ef9a9a; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px; color: #c62828; font-weight: bold; }
    .stRadio > div { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #eeeeee; font-size: 1.1rem;}
</style>
""", unsafe_allow_html=True)

# --- AI: TẠO CÂU HỎI TỰ ĐỘNG BẰNG GEMINI ---
def sinh_cau_hoi_bang_ai(lop, mon, bai_hoc, api_key):
    if not api_key:
        return None, "⚠️ Vui lòng nhập API Key ở thanh menu bên trái trước để AI có thể ra đề!"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    prompt = f"""
    Bạn là một giáo viên chuyên môn xuất sắc. Hãy ra 1 câu hỏi trắc nghiệm độ khó vừa phải cho học sinh:
    - Khối: {lop}
    - Môn học: {mon}
    - Thuộc bài: {bai_hoc}

    YÊU CẦU BẮT BUỘC: 
    1. Trả về đúng 1 cấu trúc JSON hợp lệ, KHÔNG chứa ký tự markdown ```json ở đầu và cuối.
    2. Cấu trúc JSON phải chính xác như sau:
    {{
        "cau_hoi": "Nội dung câu hỏi (Nếu có công thức toán học, hãy bọc trong dấu $...$)",
        "A": "Nội dung đáp án A",
        "B": "Nội dung đáp án B",
        "C": "Nội dung đáp án C",
        "D": "Nội dung đáp án D",
        "dap_an_dung": "A", 
        "goi_y": "Giải thích chi tiết tại sao chọn đáp án đó một cách dễ hiểu nhất (Tiếng Việt)"
    }}
    (Lưu ý: "dap_an_dung" chỉ được điền 1 ký tự in hoa: "A", "B", "C", hoặc "D").
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return None, f"Lỗi từ Google API: {response.text}"
            
        data = response.json()
        raw_text = data['candidates'][0]['content']['parts'][0]['text']
        
        # Làm sạch chuỗi JSON nếu AI vô tình dính markdown
        clean_json_str = raw_text.replace("```json", "").replace("```", "").strip()
        
        question_data = json.loads(clean_json_str)
        return question_data, None
    except Exception as e:
        return None, f"Hệ thống đang quá tải hoặc AI cấu trúc sai định dạng. Thầy cô vui lòng bấm tạo lại! (Lỗi: {e})"

# --- AI: DỊCH THUẬT SANG H'MÔNG ---
def dich_sang_mong(text, api_key):
    if not api_key:
        return "⚠️ Nhập API Key để dịch."
    try:
        url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=){api_key}"
        headers = {'Content-Type': 'application/json'}
        prompt = f"""Dịch đoạn văn bản sau sang tiếng H'Mông.
Yêu cầu: Tuyệt đối giữ nguyên các con số, ký hiệu và công thức Toán/Lý/Hóa bọc trong dấu $...$. Không giải thích, chỉ xuất kết quả dịch.
Văn bản gốc: {text}"""
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            return "Lỗi dịch thuật từ máy chủ Google."
    except Exception as e:
        return f"Lỗi hệ thống: {e}"

# --- TEXT TO SPEECH ---
def text_to_speech_html(text, lang='vi'):
    clean_text = text.replace("$", "")
    clean_text = re.sub(r'\\frac\{(.+?)\}\{(.+?)\}', r'\1 phần \2', clean_text)
    clean_text = re.sub(r'(\w)\^2', r'\1 bình phương ', clean_text)
    clean_text = re.sub(r'(\w)\^3', r'\1 lập phương ', clean_text)
    clean_text = re.sub(r'(\w)\^(\d+)', r'\1 mũ \2 ', clean_text)
    tts = gTTS(text=clean_text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    return f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'


# ==========================================
#               GIAO DIỆN CHÍNH
# ==========================================

st.markdown(f"""
<div class="hmong-header-container">
    <div class="hmong-top-bar">SỞ GIÁO DỤC VÀ ĐÀO TẠO TỈNH ĐIỆN BIÊN</div>
    <div class="hmong-main-title">
        <h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>
        <h2>🚀 GIA SƯ AI ĐA MÔN - BẢN MƯỜNG</h2>
        <div style="margin-top: 10px; font-weight:bold; color: #388e3c; font-size: 1.2rem;">Hệ thống thông minh hỗ trợ tất cả các môn học từ Lớp 1 đến Lớp 9</div>
    </div>
    <div class="hmong-pattern"></div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 80px;'>🏔️</div>", unsafe_allow_html=True)
    
    st.header("🔑 Cấu hình Trí tuệ Nhân tạo")
    api_key = st.text_input("Nhập Gemini API Key:", type="password", help="Chìa khóa để AI sinh đề và dịch thuật siêu tốc.")
    if not api_key:
        st.warning("Vui lòng dán API Key vào đây để ứng dụng hoạt động!")
    st.markdown("---")

    st.header("📚 TÌM KIẾM BÀI HỌC")
    
    # Cascade Dropdowns (Chọn Lớp -> Môn -> Chương -> Bài)
    ds_lop = list(DANH_MUC_BAI_HOC.keys())
    lop_chon = st.selectbox("📌 Chọn Khối Lớp:", ds_lop)
    
    ds_mon = list(DANH_MUC_BAI_HOC[lop_chon].keys())
    mon_chon = st.selectbox("🏷️ Chọn Môn học:", ds_mon)
    
    ds_chuong = list(DANH_MUC_BAI_HOC[lop_chon][mon_chon].keys())
    chuong_chon = st.selectbox("📖 Chủ đề / Chương:", ds_chuong)
    
    ds_bai = DANH_MUC_BAI_HOC[lop_chon][mon_chon][chuong_chon]
    bai_chon = st.selectbox("📝 Bài học chi tiết:", ds_bai)
    
    st.markdown("---")
    if st.button("🔄 Đặt lại hệ thống", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key != 'visit_count':
                del st.session_state[key]
        st.rerun()

    with st.expander("👨‍🏫 Dành cho Giáo viên"):
        st.info(f"Tổng lượt học sinh truy cập: {st.session_state.visit_count}")

col_trai, col_phai = st.columns([1.5, 1.1])

# Biến lưu trữ câu hỏi hiện tại
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
    st.session_state.show_hint = False

def handle_generate_question():
    with st.spinner("🤖 Trí tuệ nhân tạo đang soạn câu hỏi, vui lòng đợi vài giây..."):
        q_data, error = sinh_cau_hoi_bang_ai(lop_chon, mon_chon, bai_chon, api_key)
        if error:
            st.error(error)
        else:
            st.session_state.current_q = q_data
            st.session_state.show_hint = False

with col_trai:
    st.subheader(f"🎯 {mon_chon} - {bai_chon}")
    
    if st.button("✨ NHỜ AI TẠO ĐỀ KIỂM TRA MỚI", type="primary", on_click=handle_generate_question):
        pass
    
    if st.session_state.current_q:
        q = st.session_state.current_q
        st.markdown('<div class="problem-box">', unsafe_allow_html=True)
        st.markdown("### ❓ Câu hỏi của Thầy giáo AI:")
        st.markdown(f"**{q['cau_hoi']}**")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### 🤖 Công cụ hỗ trợ đặc biệt:")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            if st.button("🗣️ Nghe AI đọc đề (Tiếng Việt)"):
                st.markdown(text_to_speech_html(q['cau_hoi']), unsafe_allow_html=True)
        with col_t2:
            if st.button("🌏 Dịch câu hỏi sang tiếng H'Mông"):
                with st.spinner("Đang chuyển ngữ..."):
                    trans = dich_sang_mong(q['cau_hoi'], api_key)
                    st.info(f"**H'Mông:** {trans}")

with col_phai:
    st.subheader("✍️ Khu vực làm bài")
    
    if st.session_state.current_q:
        q = st.session_state.current_q
        
        with st.form("form_lam_bai"):
            st.markdown("**Suy nghĩ kỹ và chọn đáp án đúng nhất nhé:**")
            
            # Tạo danh sách options hiển thị
            options_dict = {
                "A": f"A. {q['A']}",
                "B": f"B. {q['B']}",
                "C": f"C. {q['C']}",
                "D": f"D. {q['D']}"
            }
            
            user_choice = st.radio("Lựa chọn của bạn:", ["A", "B", "C", "D"], format_func=lambda x: options_dict[x])
            st.markdown("<br>", unsafe_allow_html=True)
            btn_nop = st.form_submit_button("✅ Nộp bài kiểm tra")
            
            if btn_nop:
                correct_choice = q['dap_an_dung']
                if user_choice == correct_choice:
                    st.balloons()
                    st.success("🎉 XUẤT SẮC! ĐÁP ÁN HOÀN TOÀN CHÍNH XÁC! (Yog lawm)")
                    st.session_state.show_hint = False
                else:
                    st.markdown(f'<div class="error-box">Chưa đúng rồi! Hãy thử lại nhé. (Tsis yog lawm)</div>', unsafe_allow_html=True)
                    st.warning(f"Đáp án chuẩn xác là: **{correct_choice}**")
                    st.session_state.show_hint = True
        
        if st.session_state.show_hint:
            st.markdown("---")
            st.markdown('<div class="hint-container">', unsafe_allow_html=True)
            st.markdown(f"**💡 Thầy giáo AI giải thích cặn kẽ:**<br>{q['goi_y']}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🌏 Dịch lời giải thích sang H'Mông"):
                with st.spinner("Đang dịch lời giải thích..."):
                    hint_trans = dich_sang_mong(q['goi_y'], api_key)
                    st.markdown('<div class="hmong-hint">', unsafe_allow_html=True)
                    st.markdown(f"**🗣️ Lời giải (H'Mông):** {hint_trans}")
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👈 Hãy chọn Môn học, Bài học bên trái và nhấn nút 'Nhờ AI tạo đề kiểm tra mới' để bắt đầu.")

st.markdown("---")
st.caption(f"© 2026 Trường PTDTBT TH&THCS Na Ư - Bản Mường. Hệ thống hỗ trợ bởi AI Gemini 2.5 Flash | Lượt truy cập: {st.session_state.visit_count}")
