# utils.py
import streamlit as st
import random
import math
import io
import base64
import re
from deep_translator import GoogleTranslator
from gtts import gTTS

# --- 1. DỮ LIỆU CHƯƠNG TRÌNH HỌC ---
CHUONG_TRINH_HOC = {
    "Lớp 1": {
        "Chủ đề 1: Các số từ 0 đến 10": ["Đếm số lượng", "So sánh số", "Tách gộp số (Mấy và mấy)"],
        "Chủ đề 2: Phép cộng, trừ phạm vi 10": ["Phép cộng trong phạm vi 10", "Phép trừ trong phạm vi 10"],
        "Chủ đề 3: Hình học đơn giản": ["Nhận biết hình vuông, tròn, tam giác"]
    },
    "Lớp 2": {
        "Chủ đề 1: Phép cộng, trừ (có nhớ)": ["Phép cộng qua 10", "Phép trừ qua 10", "Bài toán nhiều hơn/ít hơn"],
        "Chủ đề 2: Đơn vị đo lường": ["Ki-lô-gam (kg)", "Lít (l)", "Xem ngày giờ"],
        "Chủ đề 3: Hình học": ["Đường thẳng, đoạn thẳng", "Hình tứ giác"]
    },
    "Lớp 3": {
        "Chủ đề 1: Phép nhân và chia": ["Bảng nhân 6, 7, 8, 9", "Bảng chia 6, 7, 8, 9", "Phép chia có dư"],
        "Chủ đề 2: Các số đến 1000": ["Cộng trừ số có 3 chữ số", "Tìm x (Tìm thành phần chưa biết)"],
        "Chủ đề 3: Hình học & Đơn vị": ["Diện tích hình chữ nhật, hình vuông", "Đơn vị đo độ dài (mm, cm, m, km)"]
    },
    "Lớp 4": {
        "Chủ đề 1: Số tự nhiên lớp triệu": ["Đọc viết số lớn", "Làm tròn số"],
        "Chủ đề 2: Bốn phép tính": ["Phép nhân số có 2 chữ số", "Phép chia cho số có 2 chữ số", "Trung bình cộng"],
        "Chủ đề 3: Phân số": ["Rút gọn phân số", "Quy đồng mẫu số", "Cộng trừ phân số"]
    },
    "Lớp 5": {
        "Chủ đề 1: Số thập phân": ["Đọc, viết, so sánh số thập phân", "Chuyển phân số thành số thập phân"],
        "Chủ đề 2: Các phép tính số thập phân": ["Cộng trừ số thập phân", "Nhân chia số thập phân"],
        "Chủ đề 3: Hình học": ["Diện tích hình tam giác", "Chu vi, diện tích hình tròn"]
    },
    "Lớp 6": {
        "Chương 1: Số tự nhiên": ["Lũy thừa", "Thứ tự thực hiện phép tính", "Dấu hiệu chia hết", "Số nguyên tố, Hợp số"],
        "Chương 2: Số nguyên": ["Cộng trừ số nguyên", "Nhân chia số nguyên", "Quy tắc dấu ngoặc"],
        "Chương 3: Hình học trực quan": ["Hình có trục đối xứng", "Hình có tâm đối xứng"]
    },
    "Lớp 7": {
        "Chương 1: Số hữu tỉ": ["Cộng trừ nhân chia số hữu tỉ", "Lũy thừa số hữu tỉ"],
        "Chương 2: Số thực": ["Căn bậc hai số học", "Giá trị tuyệt đối"],
        "Chương 3: Hình học": ["Góc đối đỉnh", "Tổng ba góc trong tam giác", "Các trường hợp bằng nhau của tam giác"]
    },
    "Lớp 8": {
        "Chương 1: Đa thức": ["Cộng trừ đa thức", "Nhân đa thức", "Chia đa thức cho đơn thức"],
        "Chương 2: Hằng đẳng thức": ["Bình phương của tổng/hiệu", "Hiệu hai bình phương"],
        "Chương 3: Phân thức đại số": ["Rút gọn phân thức", "Cộng trừ phân thức"],
        "Chương 4: Hàm số bậc nhất": ["Tính giá trị hàm số", "Hệ số góc"]
    },
    "Lớp 9": {
        "Chương 1: Căn thức": ["Điều kiện xác định của căn", "Rút gọn biểu thức chứa căn"],
        "Chương 2: Hàm số bậc nhất": ["Đồ thị hàm số y=ax+b", "Đường thẳng song song, cắt nhau"],
        "Chương 3: Hệ phương trình": ["Giải hệ phương trình bậc nhất 2 ẩn"],
        "Chương 4: Phương trình bậc hai": ["Công thức nghiệm (Delta)", "Định lý Vi-ét"],
        "Chương 5: Hình học (Đường tròn & Lượng giác)": ["Tỉ số lượng giác", "Góc nội tiếp"]
    }
}

# --- 2. CÁC HÀM XỬ LÝ (LOGIC) ---

def tao_de_toan(lop, bai_hoc):
    # Hàm sinh đề toán (Rút gọn để demo, bạn hãy paste nội dung đầy đủ của hàm tao_de_toan cũ vào đây)
    de_latex = ""; question_type = "number"; dap_an = 0; options = []
    goi_y_text = ""; goi_y_latex = ""; loai_toan = ""
    bai_lower = bai_hoc.lower()

    if "Lớp 1" in lop:
        if "hình" in bai_lower:
            question_type = "mcq"; de_latex = "Hình tam giác có mấy cạnh?"
            dap_an = "3"; options = ["3", "4", "5"]
            goi_y_text = "Đếm số cạnh."; loai_toan = "hinh_hoc_1"
        elif "so sánh" in bai_lower:
            a, b = random.randint(1,10), random.randint(1,10)
            de_latex = f"So sánh {a} ... {b}"; dap_an = ">" if a>b else ("<" if a<b else "=")
            question_type = "mcq"; options = [">", "<", "="]; goi_y_text = "Số lớn hơn đứng sau."
            loai_toan = "so_sanh"
        else:
            a, b = random.randint(1, 10), random.randint(1, 10)
            de_latex = f"Tính: ${a} + {b} = ?$"; dap_an = a + b
            goi_y_text = "Gộp hai nhóm."; loai_toan = "cong_don_gian"
    else:
        # Fallback cho các lớp khác
        a, b = random.randint(1, 50), random.randint(1, 50)
        de_latex = f"Tính: ${a} + {b} = ?$"; dap_an = a + b
        loai_toan = "cong_co_ban"

    if question_type == "mcq" and options: random.shuffle(options)
    return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex, loai_toan

def ai_giai_thich_chi_tiet(loai_toan, de_bai, dap_an):
    explanation = "### 🤖 Gia sư AI giải thích chi tiết:\n"
    if loai_toan == "cong_don_gian": explanation += "- Đây là phép cộng cơ bản. Hãy dùng que tính nhé."
    elif loai_toan == "hinh_hoc_1": explanation += "- Quan sát kỹ số cạnh và hình dáng."
    else: explanation += f"- Đáp án đúng là: **{dap_an}**. Hãy kiểm tra lại các bước tính toán."
    return explanation

def text_to_speech_html(text, lang='vi'):
    clean_text = text.replace("$", "").replace("\\", " ") # Xử lý sơ bộ
    tts = gTTS(text=clean_text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    return f"""<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>"""

def dich_sang_mong_giu_cong_thuc(text):
    try: return GoogleTranslator(source='vi', target='hmn').translate(text)
    except: return text

def phan_tich_loi_sai(user_ans, true_ans, q_type):
    if q_type == "number" and str(user_ans) != str(true_ans):
        return "Chưa đúng rồi! Hãy thử lại nhé."
    return ""
