import streamlit as st
import random
import math
import time
import os
import pandas as pd
import io
import base64
import re  # Thư viện xử lý chuỗi quan trọng
from deep_translator import GoogleTranslator
from gtts import gTTS

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gia sư Toán AI - Bản Mường (Lớp 1-9)",
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

# --- DỮ LIỆU CHƯƠNG TRÌNH HỌC ---
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
        "Tập 1 - Chương I: Số tự nhiên": [
            "Bài 1. Tập hợp", 
            "Bài 2. Cách ghi số tự nhiên", 
            "Bài 3. Thứ tự trong tập hợp các số tự nhiên",
            "Bài 4. Phép cộng và phép trừ số tự nhiên", 
            "Bài 5. Phép nhân và phép chia số tự nhiên",
            "Bài 6. Luỹ thừa với số mũ tự nhiên", 
            "Bài 7. Thứ tự thực hiện các phép tính"
        ],
        "Tập 1 - Chương II: Tính chia hết": [
            "Bài 8. Quan hệ chia hết và tính chất", 
            "Bài 9. Dấu hiệu chia hết",
            "Bài 10. Số nguyên tố", 
            "Bài 11. Ước chung. Ước chung lớn nhất",
            "Bài 12. Bội chung. Bội chung nhỏ nhất"
        ],
        "Tập 1 - Chương III: Số nguyên": [
            "Bài 13. Tập hợp các số nguyên", 
            "Bài 14. Phép cộng và phép trừ số nguyên",
            "Bài 15. Quy tắc dấu ngoặc", 
            "Bài 16. Phép nhân số nguyên",
            "Bài 17. Phép chia hết. Ước và bội của một số nguyên"
        ],
        "Tập 1 - Chương IV: Hình phẳng thực tiễn": [
            "Bài 18. Tam giác đều. Hình vuông. Lục giác đều",
            "Bài 19. Hình chữ nhật. Hình thoi. Hình bình hành. Hình thang cân",
            "Bài 20. Chu vi và diện tích của một số tứ giác đã học"
        ],
        "Tập 1 - Chương V: Tính đối xứng": [
            "Bài 21. Hình có trục đối xứng", 
            "Bài 22. Hình có tâm đối xứng"
        ],
        "Tập 2 - Chương VI: Phân số": [
            "Bài 23. Mở rộng phân số. Phân số bằng nhau",
            "Bài 24. So sánh phân số. Hỗn số dương",
            "Bài 25. Phép cộng và phép trừ phân số",
            "Bài 26. Phép nhân và phép chia phân số",
            "Bài 27. Hai bài toán về phân số"
        ],
        "Tập 2 - Chương VII: Số thập phân": [
            "Bài 28. Số thập phân",
            "Bài 29. Tính toán với số thập phân",
            "Bài 30. Làm tròn và ước lượng",
            "Bài 31. Một số bài toán về tỉ số và tỉ số phần trăm"
        ],
        "Tập 2 - Chương VIII: Hình học cơ bản": [
            "Bài 32. Điểm và đường thẳng",
            "Bài 33. Điểm nằm giữa hai điểm. Tia",
            "Bài 34. Đoạn thẳng. Độ dài đoạn thẳng",
            "Bài 35. Trung điểm của đoạn thẳng",
            "Bài 36. Góc",
            "Bài 37. Số đo góc"
        ],
        "Tập 2 - Chương IX: Dữ liệu và Xác suất": [
            "Bài 38. Dữ liệu và thu thập dữ liệu",
            "Bài 39. Bảng thống kê và biểu đồ tranh",
            "Bài 40. Biểu đồ cột",
            "Bài 41. Kết quả có thể và sự kiện trong trò chơi",
            "Bài 42. Xác suất thực nghiệm"
        ]
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

# --- CSS PHONG CÁCH THỔ CẨM H'MÔNG ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    .stApp { background-color: #f0f4f8; background-image: radial-gradient(#dde1e7 1px, transparent 1px); background-size: 20px 20px; }
    
    .hmong-header-container {
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        overflow: hidden;
        margin-bottom: 30px;
        border: 2px solid #e0e0e0;
    }
    
    .hmong-top-bar {
        background: linear-gradient(90deg, #1a237e, #3949ab);
        color: white;
        padding: 10px 20px;
        text-align: center;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .hmong-main-title {
        padding: 30px 20px;
        text-align: center;
        background: white;
    }
    
    .hmong-main-title h1 {
        color: #d32f2f;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 2px 0px #ffcdd2;
    }
    
    .hmong-main-title h2 {
        color: #283593;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 10px;
    }
    
    .hmong-pattern {
        height: 12px;
        background: repeating-linear-gradient(
            45deg,
            #d32f2f,
            #d32f2f 15px,
            #ffeb3b 15px,
            #ffeb3b 30px,
            #388e3c 30px,
            #388e3c 45px,
            #1976d2 45px,
            #1976d2 60px
        );
        width: 100%;
    }

    .visit-counter {
        background-color: #263238;
        color: #00e676;
        padding: 5px 15px;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin-top: 10px;
        border: 1px solid #00e676;
        box-shadow: 0 0 10px rgba(0, 230, 118, 0.3);
    }

    .problem-box {
        background-color: white; padding: 30px; border-radius: 20px;
        border: 2px solid #e0e0e0; border-top: 8px solid #1a237e;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(to right, #d32f2f, #b71c1c); 
        color: white;
        border: none; border-radius: 30px; font-weight: bold; font-size: 16px;
        padding: 0.6rem 2rem; transition: transform 0.2s; width: 100%;
        box-shadow: 0 4px 6px rgba(211, 47, 47, 0.3);
    }
    .stButton>button:hover { transform: scale(1.05); color: white; }
    .stRadio > div { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #eeeeee; }
    
    .hint-container {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        color: #1b5e20;
    }
    .hmong-hint {
        background-color: #fce4ec;
        border-left: 5px solid #e91e63;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
        font-style: italic;
        color: #880e4f;
    }
    .error-box {
        background-color: #ffebee;
        border: 1px solid #ef9a9a;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
        color: #c62828;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC SINH ĐỀ TOÀN DIỆN ---
def tao_de_toan(lop, bai_hoc):
    de_latex = ""
    question_type = "number" 
    dap_an = 0
    options = []
    goi_y_text = ""
    goi_y_latex = ""
    
    bai_lower = bai_hoc.lower()

    # --- LỚP 1 ---
    if "Lớp 1" in lop:
        if "đếm" in bai_lower or "số lượng" in bai_lower:
            n = random.randint(3, 9)
            items = ["bông hoa", "con gà", "viên bi", "cái kẹo"]
            item = random.choice(items)
            de_latex = f"An có ${n}$ {item}. Hỏi An có mấy {item}?"
            dap_an = n
            goi_y_text = "Đếm số lượng đồ vật."
        elif "so sánh" in bai_lower:
            a, b = random.randint(0, 10), random.randint(0, 10)
            while a == b: b = random.randint(0, 10)
            de_latex = f"Điền dấu thích hợp: ${a} \\dots {b}$"
            question_type = "mcq"
            ans_correct = ">" if a > b else "<"
            dap_an = ans_correct
            options = [">", "<", "="]
            goi_y_text = "Số nào đứng sau trong dãy số thì lớn hơn."
        elif "tách gộp" in bai_lower:
            total = random.randint(4, 10)
            part1 = random.randint(1, total - 1)
            de_latex = f"Gộp ${part1}$ và mấy thì được ${total}$?"
            dap_an = total - part1
            goi_y_text = f"Thực hiện phép trừ: ${total} - {part1}$"
        elif "phép cộng" in bai_lower:
            a, b = random.randint(1, 5), random.randint(0, 4)
            de_latex = f"Tính: ${a} + {b} = ?$"
            dap_an = a + b
            goi_y_text = "Gộp hai nhóm lại với nhau."
        elif "phép trừ" in bai_lower:
            a = random.randint(2, 9)
            b = random.randint(1, a)
            de_latex = f"Tính: ${a} - {b} = ?$"
            dap_an = a - b
            goi_y_text = "Bớt đi số lượng tương ứng."
        elif "hình" in bai_lower:
            question_type = "mcq"
            de_latex = "Hình nào có 3 cạnh?"
            dap_an = "Hình tam giác"
            options = ["Hình tam giác", "Hình vuông", "Hình tròn", "Hình chữ nhật"]
            goi_y_text = "Đếm số cạnh của hình."
            
    # --- LỚP 2 ---
    elif "Lớp 2" in lop:
        if "qua 10" in bai_lower:
            a = random.randint(6, 9)
            b = random.randint(5, 9)
            if "cộng" in bai_lower:
                de_latex = f"Tính nhẩm: ${a} + {b} = ?$"
                dap_an = a + b
                goi_y_text = "Gộp cho tròn 10 rồi cộng phần còn lại."
            else:
                total = random.randint(11, 18)
                sub = random.randint(2, 9)
                de_latex = f"Tính nhẩm: ${total} - {sub} = ?$"
                dap_an = total - sub
                goi_y_text = "Tách số bị trừ để trừ cho tròn 10."
        elif "nhiều hơn" in bai_lower or "ít hơn" in bai_lower:
            a = random.randint(10, 50)
            diff = random.randint(5, 20)
            if "nhiều hơn" in bai_lower:
                de_latex = f"Bao gạo tẻ nặng ${a}$ kg. Bao gạo nếp nặng hơn gạo tẻ ${diff}$ kg. Hỏi bao gạo nếp nặng bao nhiêu kg?"
                dap_an = a + diff
            else:
                de_latex = f"Lớp 2A có ${a}$ học sinh. Lớp 2B ít hơn 2A ${diff}$ bạn. Hỏi lớp 2B có bao nhiêu học sinh?"
                dap_an = a - diff
            goi_y_text = "Nhiều hơn thì cộng, ít hơn thì trừ."
        elif "ngày giờ" in bai_lower:
            h = random.randint(1, 11)
            de_latex = f"Bây giờ là ${h}$ giờ. 2 giờ nữa là mấy giờ?"
            dap_an = h + 2
            goi_y_text = "Cộng thêm số giờ."
        elif "hình" in bai_lower:
            question_type = "mcq"
            de_latex = "Hình tứ giác có bao nhiêu cạnh?"
            dap_an = "4 cạnh"
            options = ["3 cạnh", "4 cạnh", "5 cạnh", "2 cạnh"]
            goi_y_text = "Tứ giác là hình có 4 cạnh."
        else: # Mặc định cộng trừ
            a, b = random.randint(10, 80), random.randint(10, 80)
            de_latex = f"Tính: ${a} + {b}$"
            dap_an = a + b
            goi_y_text = "Đặt tính rồi tính."

    # --- LỚP 3 ---
    elif "Lớp 3" in lop:
        if "bảng nhân" in bai_lower:
            base = random.randint(6, 9)
            mult = random.randint(2, 9)
            de_latex = f"Tính: ${base} \\times {mult} = ?$"
            dap_an = base * mult
            goi_y_text = f"Nhớ lại bảng nhân {base}."
        elif "chia" in bai_lower and "dư" in bai_lower:
            b = random.randint(2, 8)
            a = random.randint(10, 50)
            while a % b == 0: a += 1 
            de_latex = f"Tìm số dư trong phép chia: ${a} : {b}$"
            dap_an = a % b
            goi_y_text = "Thực hiện phép chia và lấy phần dư."
        elif "tìm x" in bai_lower:
            x = random.randint(10, 100)
            a = random.randint(100, 500)
            res = a - x
            de_latex = f"Tìm x biết: ${a} - x = {res}$"
            dap_an = x
            goi_y_text = "Muốn tìm số trừ, ta lấy số bị trừ trừ đi hiệu."
            goi_y_latex = f"x = {a} - {res}"
        elif "diện tích" in bai_lower:
            a, b = random.randint(5, 20), random.randint(2, 10)
            de_latex = f"Tính diện tích hình chữ nhật có chiều dài ${a}$cm, chiều rộng ${b}$cm."
            dap_an = a * b
            goi_y_text = "Diện tích = Chiều dài x Chiều rộng."
        elif "đơn vị" in bai_lower:
            m = random.randint(2, 9)
            de_latex = f"Đổi: ${m}$ m = ... cm"
            dap_an = m * 100
            goi_y_text = "1 m = 100 cm."
        else:
            a, b = random.randint(100, 800), random.randint(100, 800)
            de_latex = f"Tính: ${a} + {b}$"
            dap_an = a + b
            
    # --- LỚP 4 ---
    elif "Lớp 4" in lop:
        if "lớp triệu" in bai_lower or "đọc viết" in bai_lower:
            trieu = random.randint(1, 100)
            nghin = random.randint(100, 999)
            de_latex = f"Số gồm ${trieu}$ triệu và ${nghin}$ nghìn viết là:"
            question_type = "mcq"
            ans_correct = f"{trieu}{nghin}000"
            dap_an = ans_correct
            options = [f"{trieu}{nghin}000", f"{trieu}000{nghin}", f"{trieu}{nghin}", f"{trieu}0{nghin}00"]
            goi_y_text = "Viết lần lượt từng lớp số."
        elif "trung bình cộng" in bai_lower:
            a, b, c = random.randint(10, 50), random.randint(10, 50), random.randint(10, 50)
            total = a + b + c
            rem = total % 3
            c -= rem
            de_latex = f"Tìm trung bình cộng của: ${a}, {b}, {c}$"
            dap_an = (a + b + c) // 3
            goi_y_text = "Cộng tổng rồi chia cho số các số hạng."
        elif "phân số" in bai_lower:
            tu, mau = random.randint(1, 10), random.randint(2, 10)
            k = random.randint(2, 5)
            tu_k, mau_k = tu * k, mau * k
            de_latex = f"Rút gọn phân số: $\\frac{{{tu_k}}}{{{mau_k}}}$ về tối giản (Nhập tử số của phân số tối giản)"
            dap_an = tu // math.gcd(tu, mau)
            goi_y_text = "Chia cả tử và mẫu cho ước chung lớn nhất."
        elif "phép nhân" in bai_lower:
            a, b = random.randint(100, 999), random.randint(11, 99)
            de_latex = f"Tính: ${a} \\times {b}$"
            dap_an = a * b
            goi_y_text = "Đặt tính rồi nhân lần lượt."
        else:
            a, b = random.randint(1000, 9999), random.randint(11, 99)
            kq = a * b
            de_latex = f"Tính: ${kq} : {b}$"
            dap_an = a

    # --- LỚP 5 ---
    elif "Lớp 5" in lop:
        if "số thập phân" in bai_lower and "đọc" in bai_lower:
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            de_latex = f"Số thập phân gồm {a} đơn vị, {b} phần mười viết là:"
            question_type = "mcq"
            ans_correct = f"{a},{b}"
            dap_an = ans_correct
            options = [f"{a},{b}", f"{b},{a}", f"{a}{b}", f"0,{a}{b}"]
            goi_y_text = "Phần nguyên đứng trước dấu phẩy, phần thập phân đứng sau."
        elif "chuyển phân số" in bai_lower:
            tu = random.choice([1, 2, 3, 4])
            mau = random.choice([2, 5, 4])
            de_latex = f"Viết phân số $\\frac{{{tu}}}{{{mau}}}$ dưới dạng số thập phân:"
            dap_an = tu / mau
            question_type = "number"
            goi_y_text = "Lấy tử số chia cho mẫu số."
        elif "phép tính" in bai_lower or "cộng" in bai_lower:
            a = round(random.uniform(1, 20), 2)
            b = round(random.uniform(1, 20), 2)
            de_latex = f"Tính: ${a} + {b}$"
            dap_an = round(a + b, 2)
            goi_y_text = "Đặt dấu phẩy thẳng cột."
        elif "tam giác" in bai_lower:
            a = random.randint(5, 20)
            h = random.randint(5, 20)
            de_latex = f"Diện tích tam giác có đáy ${a}$cm và chiều cao ${h}$cm là bao nhiêu $cm^2$?"
            dap_an = (a * h) / 2
            goi_y_text = "Công thức diện tích tam giác:"
            goi_y_latex = "S = \\frac{a \\times h}{2}"
        elif "tròn" in bai_lower:
            r = random.randint(1, 10)
            de_latex = f"Chu vi hình tròn bán kính r=${r}$cm là (lấy $\\pi=3.14$):"
            dap_an = round(r * 2 * 3.14, 2)
            goi_y_text = "Công thức chu vi hình tròn:"
            goi_y_latex = "C = r \\times 2 \\times 3.14"
        else:
             a = round(random.uniform(1, 10), 1)
             de_latex = f"Tính: ${a} \\times 10$"
             dap_an = a * 10

 # --- LỚP 6 (CHUYÊN BIỆT CHO CHƯƠNG I - SỐ TỰ NHIÊN) ---
    elif "Lớp 6" in lop:
        question_type = "mcq" # Trắc nghiệm khách quan 4 đáp án
        
        # ---------------------------------------------------------
        # BÀI 1. TẬP HỢP
        # ---------------------------------------------------------
        if "Bài 1." in bai_hoc:
            # Dạng: Cho tập hợp A = {x, y, z}. Chọn khẳng định đúng/sai về phần tử.
            val_start = random.randint(1, 10)
            elements = [val_start, val_start + 1, val_start + 2, val_start + 3]
            # Tạo chuỗi hiển thị tập hợp: A = {1; 2; 3; 4}
            set_str = "\\{ " + "; ".join(map(str, elements)) + " \\}"
            
            # Random chọn hỏi "thuộc" hay "không thuộc"
            if random.choice([True, False]): 
                # Hỏi cái ĐÚNG (thuộc)
                correct_ele = random.choice(elements)
                de_latex = f"Cho tập hợp $M = {set_str}$. Khẳng định nào sau đây là **ĐÚNG**?"
                ans_correct = f"${correct_ele} \\in M$"
                
                # Đáp án nhiễu
                fake_ele = val_start + 10 # Số không có trong tập hợp
                fake1 = f"${fake_ele} \\in M$"
                fake2 = f"${correct_ele} \\notin M$"
                fake3 = f"$\\emptyset \\in M$" # Bẫy ký hiệu rỗng
                
                goi_y_text = "Phần tử nằm trong dấu ngoặc nhọn thì thuộc tập hợp."
            else:
                # Hỏi cái ĐÚNG (không thuộc)
                fake_ele = val_start + 10
                de_latex = f"Cho tập hợp $M = {set_str}$. Khẳng định nào sau đây là **ĐÚNG**?"
                ans_correct = f"${fake_ele} \\notin M$"
                
                fake1 = f"${fake_ele} \\in M$"
                fake2 = f"${elements[0]} \\notin M$"
                fake3 = f"${elements[1]} \\notin M$"
                
                goi_y_text = "Phần tử không nằm trong tập hợp thì dùng ký hiệu không thuộc ($\\notin$)."

            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]

        # ---------------------------------------------------------
        # BÀI 2. CÁCH GHI SỐ TỰ NHIÊN
        # ---------------------------------------------------------
        elif "Bài 2." in bai_hoc:
            # Dạng: Giá trị của chữ số theo hàng (Hàng nghìn, trăm, chục, đơn vị)
            # Ví dụ: Số 3456, giá trị số 4 là bao nhiêu?
            thousands = random.randint(1, 9)
            hundreds = random.randint(1, 9)
            tens = random.randint(1, 9)
            units = random.randint(1, 9)
            
            number_val = thousands*1000 + hundreds*100 + tens*10 + units
            number_str = f"{thousands}{hundreds}{tens}{units}"
            
            # Chọn ngẫu nhiên một hàng để hỏi
            pos = random.choice(["nghìn", "trăm", "chục"])
            
            if pos == "nghìn":
                target_digit = thousands
                val_real = thousands * 1000
                de_latex = f"Trong số tự nhiên ${number_str}$, giá trị của chữ số {target_digit} là?"
            elif pos == "trăm":
                target_digit = hundreds
                val_real = hundreds * 100
                de_latex = f"Trong số tự nhiên ${number_str}$, giá trị của chữ số {target_digit} là?"
            else:
                target_digit = tens
                val_real = tens * 10
                de_latex = f"Trong số tự nhiên ${number_str}$, giá trị của chữ số {target_digit} là?"

            ans_correct = str(val_real)
            # Các phương án nhiễu: chính chữ số đó, hoặc sai hàng
            fake1 = str(target_digit)
            fake2 = str(val_real * 10)
            fake3 = str(val_real // 10) if val_real > 10 else str(val_real + 1)
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "Xác định hàng của chữ số (đơn vị, chục, trăm, nghìn) để tìm giá trị."

        # ---------------------------------------------------------
        # BÀI 3. THỨ TỰ TRONG TẬP HỢP CÁC SỐ TỰ NHIÊN
        # ---------------------------------------------------------
        elif "Bài 3." in bai_hoc:
            # Dạng 1: Số liền trước / Số liền sau
            num = random.randint(10, 99)
            q_type = random.choice(["trước", "sau"])
            
            if q_type == "sau":
                de_latex = f"Số liền sau của số tự nhiên ${num}$ là?"
                ans_correct = str(num + 1)
                fake1 = str(num - 1)
                fake2 = str(num)
                fake3 = str(num + 2)
                goi_y_text = "Số liền sau của số n là n + 1."
            else:
                de_latex = f"Số liền trước của số tự nhiên ${num}$ là?"
                ans_correct = str(num - 1)
                fake1 = str(num + 1)
                fake2 = str(num)
                fake3 = str(num - 2)
                goi_y_text = "Số liền trước của số n là n - 1."
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]

        # ---------------------------------------------------------
        # BÀI 4. PHÉP CỘNG VÀ PHÉP TRỪ SỐ TỰ NHIÊN
        # ---------------------------------------------------------
        elif "Bài 4." in bai_hoc:
            # Dạng: Tìm x hoặc Tính nhanh
            # a + x = b -> x = b - a
            a = random.randint(10, 50)
            b_val = random.randint(60, 100) # Tổng
            
            de_latex = f"Tìm số tự nhiên x, biết: $x + {a} = {b_val}$"
            ans_val = b_val - a
            ans_correct = str(ans_val)
            
            fake1 = str(b_val + a) # Lỗi cộng thay vì trừ
            fake2 = str(ans_val - 10)
            fake3 = str(b_val)
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "Muốn tìm số hạng chưa biết, ta lấy tổng trừ đi số hạng đã biết."
            goi_y_latex = "x = a - b"

        # ---------------------------------------------------------
        # BÀI 5. PHÉP NHÂN VÀ PHÉP CHIA SỐ TỰ NHIÊN
        # ---------------------------------------------------------
        elif "Bài 5." in bai_hoc:
            # Dạng: Tính chất phân phối phép nhân đối với phép cộng
            # a.b + a.c = a(b+c)
            common = random.choice([2, 5, 10, 25]) # Số đẹp để đặt nhân tử chung
            n1 = random.randint(10, 50)
            n2 = random.randint(10, 50)
            
            de_latex = f"Tính nhanh giá trị biểu thức: ${common} \\cdot {n1} + {common} \\cdot {n2}$"
            
            # Tính toán
            real_ans = common * (n1 + n2)
            ans_correct = str(real_ans)
            
            # Bẫy
            fake1 = str(common * n1 * n2) # Nhân hết
            fake2 = str(common + n1 + n2) # Cộng hết
            fake3 = str(real_ans + 100)
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "Sử dụng tính chất phân phối: a.b + a.c = a.(b + c)"
            goi_y_latex = f"{common} \\cdot ({n1} + {n2})"

        # ---------------------------------------------------------
        # BÀI 6. LUỸ THỪA VỚI SỐ MŨ TỰ NHIÊN (Sửa kỹ)
        # ---------------------------------------------------------
        elif "Bài 6." in bai_hoc:
            # Có 3 dạng bài nhỏ: Tính giá trị, Nhân 2 lũy thừa, Chia 2 lũy thừa
            sub_type = random.choice(["tinh_gia_tri", "nhan_luy_thua", "chia_luy_thua"])
            
            base = random.randint(2, 5) # Cơ số nhỏ để dễ tính
            
            if sub_type == "tinh_gia_tri":
                exp = random.randint(2, 3) # Mũ 2 hoặc 3
                de_latex = f"Giá trị của lũy thừa ${base}^{exp}$ là?"
                val = base ** exp
                ans_correct = str(val)
                
                fake1 = str(base * exp) # Lỗi sai phổ biến nhất (2^3 = 6)
                fake2 = str(base + exp) # Lỗi cộng (2^3 = 5)
                fake3 = str(int(f"{base}{exp}")) # Ghép số
                
                goi_y_text = f"Lũy thừa là tích của các thừa số bằng nhau. Ví dụ: $2^3 = 2 \\cdot 2 \\cdot 2$."
                
            elif sub_type == "nhan_luy_thua":
                m = random.randint(2, 5)
                n = random.randint(2, 5)
                de_latex = f"Viết tích sau dưới dạng một lũy thừa: ${base}^{m} \\cdot {base}^{n}$"
                ans_correct = f"${base}^{{{m+n}}}$"
                
                fake1 = f"${base}^{{{m*n}}}$" # Nhân mũ
                fake2 = f"${base*base}^{{{m+n}}}$" # Nhân cơ số
                fake3 = f"${base}^{{{abs(m-n)}}}$"
                
                goi_y_text = "Khi nhân hai lũy thừa cùng cơ số, ta giữ nguyên cơ số và CỘNG các số mũ."
                goi_y_latex = "a^m \\cdot a^n = a^{m+n}"
                
            else: # Chia lũy thừa
                n = random.randint(2, 4)
                diff = random.randint(1, 3)
                m = n + diff # Đảm bảo m > n
                de_latex = f"Viết thương sau dưới dạng một lũy thừa: ${base}^{m} : {base}^{n}$"
                ans_correct = f"${base}^{{{diff}}}$" # m - n
                
                fake1 = f"${base}^{{{m+n}}}$" # Cộng mũ
                fake2 = f"${base}^{{{m//n}}}$" # Chia mũ
                fake3 = f"$1$"
                
                goi_y_text = "Khi chia hai lũy thừa cùng cơ số (khác 0), ta giữ nguyên cơ số và TRỪ các số mũ."
                goi_y_latex = "a^m : a^n = a^{m-n}"

            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]

        # ---------------------------------------------------------
        # BÀI 7. THỨ TỰ THỰC HIỆN CÁC PHÉP TÍNH
        # ---------------------------------------------------------
        elif "Bài 7." in bai_hoc:
            # Dạng: Biểu thức có Lũy thừa -> Nhân -> Trừ
            # Ví dụ: 50 - 2 * 3^2
            a = random.randint(30, 60) # Số bị trừ
            b = random.randint(2, 3)   # Hệ số nhân
            c = random.randint(2, 3)   # Cơ số
            
            # Đảm bảo kết quả dương cho học sinh lớp 6 đầu cấp dễ tính
            while a < b * (c**2):
                a += 10
            
            de_latex = f"Tính giá trị biểu thức: ${a} - {b} \\cdot {c}^2$"
            val = a - (b * (c**2))
            ans_correct = str(val)
            
            # Bẫy 1: Thực hiện trừ trước nhân sau: (a-b) * c^2
            fake1 = str((a - b) * (c**2))
            # Bẫy 2: Nhân trước lũy thừa sau: a - (b*c)^2
            fake2 = str(a - ((b*c)**2))
            # Bẫy 3: Sai ngẫu nhiên
            fake3 = str(val + 10)
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "Thứ tự ưu tiên: Lũy thừa $\\rightarrow$ Nhân/Chia $\\rightarrow$ Cộng/Trừ."
        
        # ---------------------------------------------------------
        # FALLBACK (Dự phòng nếu không khớp bài nào)
        # ---------------------------------------------------------
        else:
            de_latex = "Số tự nhiên nhỏ nhất là số nào?"
            ans_correct = "0"
            options = ["0", "1", "Không có", "10"]
            dap_an = ans_correct
            goi_y_text = "Tập hợp số tự nhiên $\\mathbb{N} = \\{0; 1; 2; ...\\}$"
        # --- CHƯƠNG II: TÍNH CHIA HẾT ---
        elif "Bài 8." in bai_hoc: # Quan hệ chia hết
            a, k = random.randint(3, 8), random.randint(2, 5)
            b = a * k
            de_latex = f"Khẳng định nào sau đây đúng?"
            ans_correct = f"${b} \\vdots {a}$"
            fake1 = f"${a} \\vdots {b}$"
            fake2 = f"${b}$ là ước của ${a}$"
            fake3 = f"${a}$ là bội của ${b}$"
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "A chia hết cho B thì A là bội của B, B là ước của A."

        elif "Bài 9." in bai_hoc: # Dấu hiệu chia hết
            target = random.choice([2, 3, 5, 9])
            base_val = random.randint(10, 50) * target
            if target == 5: base_val = random.randint(10, 50) * 5
            
            de_latex = f"Số nào sau đây chia hết cho {target}?"
            ans_correct = str(base_val)
            
            opts = [ans_correct]
            while len(opts) < 4:
                v = random.randint(100, 999)
                if v % target != 0: opts.append(str(v))
            
            dap_an = ans_correct
            options = opts
            goi_y_text = {2: "Tận cùng chẵn", 3: "Tổng chữ số chia hết cho 3", 5: "Tận cùng 0 hoặc 5", 9: "Tổng chữ số chia hết cho 9"}[target]

        elif "Bài 10." in bai_hoc: # Số nguyên tố
            primes = [2, 3, 5, 7, 11, 13, 17, 19]
            composites = [4, 6, 8, 9, 10, 12, 14, 15]
            p = random.choice(primes)
            de_latex = "Số nào sau đây là số nguyên tố?"
            ans_correct = str(p)
            fakes = [str(x) for x in random.sample(composites, 3)]
            dap_an = ans_correct
            options = [ans_correct] + fakes
            goi_y_text = "Số nguyên tố chỉ có 2 ước là 1 và chính nó."

        elif "Bài 11." in bai_hoc: # ƯCLN
            a = 12
            b = 18
            de_latex = f"ƯCLN(12, 18) là?"
            ans_correct = "6"
            options = ["6", "3", "36", "2"]
            dap_an = ans_correct
            goi_y_text = "Phân tích ra thừa số nguyên tố, lấy thừa số chung với số mũ nhỏ nhất."

        elif "Bài 12." in bai_hoc: # BCNN
            a = 4
            b = 6
            de_latex = f"BCNN(4, 6) là?"
            ans_correct = "12"
            options = ["12", "24", "2", "6"]
            dap_an = ans_correct
            goi_y_text = "Phân tích ra thừa số nguyên tố, lấy thừa số chung và riêng với số mũ lớn nhất."

        # --- CHƯƠNG III: SỐ NGUYÊN ---
        elif "Bài 13." in bai_hoc: # Tập hợp số nguyên
            val = random.randint(2, 9)
            de_latex = f"Số đối của số nguyên ${-val}$ là?"
            ans_correct = str(val)
            options = [str(val), str(-val), "0", f"1/{val}"]
            dap_an = ans_correct
            goi_y_text = "Số đối của số âm là số dương tương ứng."

        elif "Bài 14." in bai_hoc: # Cộng trừ số nguyên
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            if random.random() > 0.5:
                de_latex = f"Tính: $(-{a}) + (-{b})$"
                val = -(a+b)
                goi_y_text = "Cộng hai số âm: Cộng giá trị tuyệt đối rồi đặt dấu trừ."
            else:
                de_latex = f"Tính: ${a} - {a+b}$"
                val = -b
                goi_y_text = "Phép trừ là cộng với số đối."
            ans_correct = str(val)
            dap_an = ans_correct
            options = [ans_correct, str(-val), str(a+b), str(abs(val))]

        elif "Bài 15." in bai_hoc: # Dấu ngoặc
            x = random.randint(1, 9)
            de_latex = f"Bỏ dấu ngoặc: $-({x} - x)$"
            ans_correct = f"$-{x} + x$"
            fake1 = f"${x} - x$"
            fake2 = f"$-{x} - x$"
            fake3 = "0"
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "Trước ngoặc là dấu trừ, đổi dấu tất cả các số trong ngoặc."

        elif "Bài 16." in bai_hoc: # Phép nhân
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            de_latex = f"Tính: $(-{a}) \\cdot (-{b})$"
            ans_correct = str(a*b)
            fake1 = str(-(a*b))
            fake2 = str(-(a+b))
            fake3 = str(a+b)
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "Âm nhân Âm ra Dương."

        elif "Bài 17." in bai_hoc: # Phép chia hết/Ước bội
            a = 6
            de_latex = "Tập hợp các ước nguyên của 6 là?"
            ans_correct = "\\{1; -1; 2; -2; 3; -3; 6; -6\\}"
            fake1 = "\\{1; 2; 3; 6\\}"
            fake2 = "\\{2; 3\\}"
            fake3 = "\\{1; -1; 6; -6\\}"
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "Ước của số nguyên bao gồm cả số dương và số âm."

        # --- CHƯƠNG IV: HÌNH PHẲNG ---
        elif "Bài 18." in bai_hoc: # Tam giác đều...
            de_latex = "Tam giác đều có tính chất nào sau đây?"
            ans_correct = "Ba góc bằng nhau và bằng $60^\\circ$"
            fake1 = "Có một góc vuông"
            fake2 = "Ba cạnh không bằng nhau"
            fake3 = "Hai đường chéo bằng nhau"
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]

        elif "Bài 19." in bai_hoc: # HCN, Thoi...
            de_latex = "Hình thoi có hai đường chéo như thế nào?"
            ans_correct = "Vuông góc với nhau"
            fake1 = "Bằng nhau"
            fake2 = "Song song với nhau"
            fake3 = "Không cắt nhau"
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]

        elif "Bài 20." in bai_hoc: # Chu vi diện tích
            a = random.randint(3, 8)
            de_latex = f"Diện tích hình vuông cạnh {a}cm là?"
            ans_correct = f"{a*a} $cm^2$"
            options = [ans_correct, f"{a*4} cm", f"{a*2} $cm^2$", f"{a+a} $cm^2$"]
            dap_an = ans_correct
            goi_y_text = "S = cạnh x cạnh"

        # --- CHƯƠNG V: ĐỐI XỨNG ---
        elif "Bài 21." in bai_hoc: # Trục đối xứng
            de_latex = "Hình thang cân có bao nhiêu trục đối xứng?"
            ans_correct = "1"
            options = ["1", "2", "0", "4"]
            dap_an = ans_correct
            goi_y_text = "Trục đối xứng đi qua trung điểm hai đáy."

        elif "Bài 22." in bai_hoc: # Tâm đối xứng
            de_latex = "Chữ cái nào sau đây có tâm đối xứng?"
            ans_correct = "S"
            options = ["S", "M", "A", "T"]
            dap_an = ans_correct
            goi_y_text = "Quay 180 độ hình trùng khít với chính nó."

        # ================= TẬP 2 =================
        
        # --- CHƯƠNG VI: PHÂN SỐ ---
        elif "Bài 23." in bai_hoc: # Mở rộng/Bằng nhau
            de_latex = "Phân số nào bằng phân số $\\frac{2}{-3}$?"
            ans_correct = "$\\frac{-2}{3}$"
            options = [ans_correct, "$\\frac{2}{3}$", "$\\frac{-3}{2}$", "$\\frac{3}{-2}$"]
            dap_an = ans_correct
            goi_y_text = "Chuyển dấu trừ từ mẫu lên tử."

        elif "Bài 24." in bai_hoc: # So sánh
            de_latex = "So sánh: $\\frac{-1}{5}$ và $\\frac{-3}{5}$"
            ans_correct = "$\\frac{-1}{5} > \\frac{-3}{5}$"
            fake1 = "$\\frac{-1}{5} < \\frac{-3}{5}$"
            fake2 = "Bằng nhau"
            fake3 = "Không so sánh được"
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "Mẫu dương, tử nào lớn hơn thì phân số lớn hơn (-1 > -3)."

        elif "Bài 25." in bai_hoc: # Cộng trừ
            m = random.randint(3, 7)
            de_latex = f"Tính: $\\frac{{1}}{{{m}}} + \\frac{{-2}}{{{m}}}$"
            ans_correct = f"$\\frac{{-1}}{{{m}}}$"
            options = [ans_correct, f"$\\frac{{1}}{{{m}}}$", f"$\\frac{{3}}{{{m}}}$", f"$\\frac{{-3}}{{{m}}}$"]
            dap_an = ans_correct
            goi_y_text = "Cộng tử giữ nguyên mẫu."

        elif "Bài 26." in bai_hoc: # Nhân chia
            de_latex = "Nghịch đảo của phân số $\\frac{-2}{3}$ là?"
            ans_correct = "$\\frac{3}{-2}$"
            options = [ans_correct, "$\\frac{2}{3}$", "$\\frac{-2}{3}$", "$\\frac{3}{2}$"]
            dap_an = ans_correct
            goi_y_text = "Đảo ngược tử và mẫu."

        elif "Bài 27." in bai_hoc: # Bài toán phân số
            val = random.randint(10, 30) * 2
            de_latex = f"Tìm $\\frac{{1}}{{2}}$ của {val}?"
            ans_correct = str(val // 2)
            options = [str(val // 2), str(val * 2), str(val + 2), "1"]
            dap_an = ans_correct
            goi_y_text = "Lấy số đó nhân với phân số."

        # --- CHƯƠNG VII: SỐ THẬP PHÂN ---
        elif "Bài 28." in bai_hoc: # Khái niệm
            de_latex = "Phân số thập phân $\\frac{7}{100}$ viết dưới dạng số thập phân là?"
            ans_correct = "0,07"
            options = ["0,07", "0,7", "0,007", "7,0"]
            dap_an = ans_correct
            goi_y_text = "Hai chữ số 0 ở mẫu tương ứng 2 chữ số sau dấu phẩy."

        elif "Bài 29." in bai_hoc: # Tính toán
            a = 1.2
            b = 3.0
            de_latex = f"Tính: ${a} + {b}$"
            ans_correct = "4.2"
            options = ["4.2", "3.2", "4.0", "1.5"]
            dap_an = ans_correct

        elif "Bài 30." in bai_hoc: # Làm tròn
            de_latex = "Làm tròn số 3,14159 đến hàng phần trăm?"
            ans_correct = "3,14"
            options = ["3,14", "3,15", "3,1", "3,142"]
            dap_an = ans_correct
            goi_y_text = "Chữ số sau hàng phần trăm là 1 (<5) nên giữ nguyên."

        elif "Bài 31." in bai_hoc: # Tỉ số
            de_latex = "Tỉ số phần trăm của 3 và 4 là?"
            ans_correct = "75%"
            options = ["75%", "34%", "43%", "0,75%"]
            dap_an = ans_correct
            goi_y_text = "3 chia 4 nhân 100."

        # --- CHƯƠNG VIII: HÌNH HỌC CƠ BẢN ---
        elif "Bài 32." in bai_hoc: # Điểm đường thẳng
            de_latex = "Có bao nhiêu đường thẳng đi qua 2 điểm A, B phân biệt?"
            ans_correct = "1"
            options = ["1", "2", "Vô số", "0"]
            dap_an = ans_correct

        elif "Bài 33." in bai_hoc: # Điểm nằm giữa
            de_latex = "Nếu M nằm giữa A và B thì:"
            ans_correct = "AM + MB = AB"
            fake1 = "AM = MB"
            fake2 = "AM > MB"
            fake3 = "AM - MB = AB"
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]

        elif "Bài 34." in bai_hoc: # Đoạn thẳng
            de_latex = "Đoạn thẳng AB là hình gồm?"
            ans_correct = "Điểm A, điểm B và tất cả các điểm nằm giữa A và B"
            options = [ans_correct, "Chỉ điểm A và điểm B", "Tất cả các điểm nằm cùng phía với A", "Đường thẳng đi qua A và B"]
            dap_an = ans_correct

        elif "Bài 35." in bai_hoc: # Trung điểm
            len_ab = 10
            de_latex = f"M là trung điểm đoạn thẳng AB dài {len_ab}cm. Độ dài AM là?"
            ans_correct = "5cm"
            options = ["5cm", "10cm", "20cm", "2.5cm"]
            dap_an = ans_correct
            goi_y_text = "AM = AB / 2"

        elif "Bài 36." in bai_hoc or "Bài 37." in bai_hoc: # Góc
            de_latex = "Góc bẹt có số đo bằng bao nhiêu?"
            ans_correct = "$180^\\circ$"
            options = ["$180^\\circ$", "$90^\\circ$", "$60^\\circ$", "$0^\\circ$"]
            dap_an = ans_correct

        # --- CHƯƠNG IX: DỮ LIỆU ---
        elif "Bài 38." in bai_hoc or "Bài 39." in bai_hoc: # Dữ liệu/Biểu đồ
            de_latex = "Để biểu diễn sự thay đổi của nhiệt độ theo thời gian, ta thường dùng?"
            ans_correct = "Biểu đồ đoạn thẳng (hoặc cột)"
            options = ["Biểu đồ đoạn thẳng", "Biểu đồ tranh", "Biểu đồ quạt", "Bảng số liệu"]
            dap_an = ans_correct

        elif "Bài 40." in bai_hoc: # Biểu đồ cột
            de_latex = "Trục đứng của biểu đồ cột thường biểu diễn gì?"
            ans_correct = "Số liệu (tần số)"
            options = ["Số liệu", "Đối tượng thống kê", "Tên biểu đồ", "Năm tháng"]
            dap_an = ans_correct

        elif "Bài 41." in bai_hoc or "Bài 42." in bai_hoc: # Xác suất
            de_latex = "Gieo con xúc xắc cân đối. Xác suất ra mặt 6 chấm là?"
            ans_correct = "$\\frac{1}{6}$"
            options = ["$\\frac{1}{6}$", "$\\frac{1}{2}$", "1", "0"]
            dap_an = ans_correct

        # FALLBACK
        else:
            de_latex = "Số 0 là số nguyên?"
            ans_correct = "Không âm cũng không dương"
            options = ["Không âm cũng không dương", "Dương", "Âm", "Nguyên tố"]
            dap_an = ans_correct
 # --- LỚP 7 (ĐÃ SỬA LỖI LOGIC SO SÁNH & HIỂN THỊ) ---
    elif "Lớp 7" in lop:
        question_type = "mcq" # Chuyển toàn bộ sang trắc nghiệm để tránh lỗi nhập liệu

        # 1. SỐ HỮU TỈ (CỘNG TRỪ NHÂN CHIA)
        if "cộng trừ" in bai_lower:
            # Chọn mẫu số chung nhỏ để biểu thức đẹp
            mau = random.randint(2, 9)
            tu1 = random.randint(1, 9)
            tu2 = random.randint(1, 9)
            
            if random.random() > 0.5: # Phép cộng
                de_latex = f"Tính giá trị biểu thức: $\\frac{{{tu1}}}{{{mau}}} + \\frac{{{tu2}}}{{{mau}}}$"
                # Đáp án đúng dạng Chuỗi LaTeX
                kq_tu = tu1 + tu2
                ans_correct = f"$\\frac{{{kq_tu}}}{{{mau}}}$"
                
                # Tạo phương án nhiễu
                fake1 = f"$\\frac{{{kq_tu}}}{{{mau + mau}}}$" # Sai: Cộng cả mẫu
                fake2 = f"$\\frac{{{tu1 * tu2}}}{{{mau}}}$"    # Sai: Nhân tử
                fake3 = f"$\\frac{{{abs(tu1 - tu2)}}}{{{mau}}}$" # Sai: Trừ
                
                dap_an = ans_correct
                options = [ans_correct, fake1, fake2, fake3]
                
                goi_y_text = "Muốn cộng hai phân số cùng mẫu, ta cộng các tử và giữ nguyên mẫu."
                goi_y_latex = "\\frac{A}{M} + \\frac{B}{M} = \\frac{A+B}{M}"
            else: # Phép trừ
                tu_lon = tu1 + tu2 
                de_latex = f"Tính giá trị biểu thức: $\\frac{{{tu_lon}}}{{{mau}}} - \\frac{{{tu1}}}{{{mau}}}$"
                
                kq_tu = tu2
                ans_correct = f"$\\frac{{{kq_tu}}}{{{mau}}}$"
                
                fake1 = f"$\\frac{{{kq_tu}}}{{0}}$"              # Sai: Mẫu bằng 0
                fake2 = f"$\\frac{{{tu_lon + tu1}}}{{{mau}}}$"    # Sai: Cộng thay vì trừ
                fake3 = f"$1$"
                
                dap_an = ans_correct
                options = [ans_correct, fake1, fake2, fake3]
                
                goi_y_text = "Muốn trừ hai phân số cùng mẫu, ta trừ tử số và giữ nguyên mẫu số."
                goi_y_latex = "\\frac{A}{M} - \\frac{B}{M} = \\frac{A-B}{M}"

        elif "nhân chia" in bai_lower:
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            c = random.randint(1, 5)
            d = random.randint(1, 5)
            
            if random.random() > 0.5: # Phép nhân
                de_latex = f"Tính: $\\frac{{{a}}}{{{b}}} \\cdot \\frac{{{c}}}{{{d}}}$"
                ans_correct = f"$\\frac{{{a*c}}}{{{b*d}}}$"
                
                fake1 = f"$\\frac{{{a*d}}}{{{b*c}}}$" # Nhân chéo
                fake2 = f"$\\frac{{{a+c}}}{{{b+d}}}$" # Cộng tử mẫu
                fake3 = f"$\\frac{{{a}}}{{{b}}}$"
                
                dap_an = ans_correct
                options = [ans_correct, fake1, fake2, fake3]
                
                goi_y_text = "Nhân hai phân số: Tử nhân với tử, mẫu nhân với mẫu."
                goi_y_latex = "\\frac{a}{b} \\cdot \\frac{c}{d} = \\frac{a \\cdot c}{b \\cdot d}"
            else: # Phép chia
                de_latex = f"Tính: $\\frac{{{a}}}{{{b}}} : \\frac{{{c}}}{{{d}}}$"
                ans_correct = f"$\\frac{{{a*d}}}{{{b*c}}}$"
                
                fake1 = f"$\\frac{{{a*c}}}{{{b*d}}}$" # Nhân bình thường
                fake2 = f"$\\frac{{{b*c}}}{{{a*d}}}$" # Nghịch đảo sai
                fake3 = f"$\\frac{{{c}}}{{{d}}}$"
                
                dap_an = ans_correct
                options = [ans_correct, fake1, fake2, fake3]
                
                goi_y_text = "Chia cho một phân số là nhân với phân số đảo ngược của nó."
                goi_y_latex = "\\frac{a}{b} : \\frac{c}{d} = \\frac{a}{b} \\cdot \\frac{d}{c}"

        # 2. LŨY THỪA (ĐÃ KHẮC PHỤC LỖI TRẢ VỀ 0)
        elif "lũy thừa" in bai_lower:
            base_tu = random.choice([1, 2, 3])
            base_mau = random.choice([2, 3, 4, 5])
            exp = random.choice([2, 3])
            
            de_latex = f"Giá trị của lũy thừa $(\\frac{{{base_tu}}}{{{base_mau}}})^{exp}$ là?"
            
            # Tính kết quả
            res_tu = base_tu ** exp
            res_mau = base_mau ** exp
            
            # QUAN TRỌNG: Lưu đáp án dưới dạng chuỗi LaTeX y hệt options
            ans_correct = f"$\\frac{{{res_tu}}}{{{res_mau}}}$"
            
            fake1 = f"$\\frac{{{base_tu * exp}}}{{{base_mau}}}$"       # Lỗi: Tử nhân số mũ
            fake2 = f"$\\frac{{{base_tu}}}{{{base_mau * exp}}}$"       # Lỗi: Mẫu nhân số mũ
            fake3 = f"$\\frac{{{base_tu}}}{{{res_mau}}}$"              # Lỗi: Quên lũy thừa tử
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            
            goi_y_text = "Lũy thừa của một thương bằng thương các lũy thừa."
            goi_y_latex = "(\\frac{x}{y})^n = \\frac{x^n}{y^n}"

        # 3. SỐ THỰC (CĂN BẬC HAI & GIÁ TRỊ TUYỆT ĐỐI)
        elif "căn bậc hai" in bai_lower:
            squares = [4, 9, 16, 25, 36, 49, 64, 81, 100]
            val = random.choice(squares)
            sqrt_val = int(math.sqrt(val))
            
            de_latex = f"Căn bậc hai số học của {val} là?"
            ans_correct = f"{sqrt_val}" # Lưu dạng chuỗi
            
            fake1 = f"-{sqrt_val}"           # Sai: Số âm
            fake2 = f"$\\pm {sqrt_val}$"     # Sai: Căn bậc hai đại số
            fake3 = f"{val}"                  # Sai: Chính nó
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            
            goi_y_text = "Căn bậc hai số học của số a không âm là số x không âm sao cho x bình phương bằng a."
            goi_y_latex = "x = \\sqrt{a} \\Rightarrow x^2 = a \\quad (x \\ge 0)"

        elif "tuyệt đối" in bai_lower:
            val = random.randint(1, 15)
            sign = random.choice(["-", ""])
            val_str = f"{sign}{val}"
            
            de_latex = f"Giá trị tuyệt đối $|{val_str}|$ bằng bao nhiêu?"
            ans_correct = f"{val}"
            
            fake1 = f"-{val}"
            fake2 = "0"
            fake3 = f"$\\frac{{1}}{{{val}}}$"
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            
            goi_y_text = "Giá trị tuyệt đối của một số thực x luôn luôn không âm."
            goi_y_latex = "|x| \\ge 0"

        # 4. HÌNH HỌC LỚP 7
        elif "đối đỉnh" in bai_lower:
            angle = random.randint(30, 150)
            de_latex = f"Cho góc $\\widehat{{xOy}} = {angle}^\\circ$. Góc đối đỉnh với $\\widehat{{xOy}}$ có số đo là:"
            ans_correct = f"${angle}^\\circ$"
            
            fake1 = f"${180 - angle}^\\circ$" # Kề bù
            fake2 = f"${90 - angle if angle < 90 else angle + 10}^\\circ$"
            fake3 = f"${angle * 2}^\\circ$"
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            
            goi_y_text = "Hai góc đối đỉnh thì bằng nhau."
            goi_y_latex = "\\widehat{O_1} = \\widehat{O_3} \\text{ (đối đỉnh)}"

        elif "tổng ba góc" in bai_lower:
            goc_A = random.randint(30, 80)
            goc_B = random.randint(30, 70)
            goc_C = 180 - goc_A - goc_B
            
            de_latex = f"Cho $\\Delta ABC$ có $\\hat{{A}}={goc_A}^\\circ, \\hat{{B}}={goc_B}^\\circ$. Số đo góc C là?"
            ans_correct = f"${goc_C}^\\circ$"
            
            fake1 = f"${180 - goc_A}^\\circ$"
            fake2 = f"${goc_A + goc_B}^\\circ$"
            fake3 = f"${90}^\\circ$"
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            
            goi_y_text = "Tổng ba góc trong một tam giác bằng 180 độ."
            goi_y_latex = "\\hat{A} + \\hat{B} + \\hat{C} = 180^\\circ"

        elif "bằng nhau" in bai_lower:
            # Random câu hỏi lý thuyết
            case_type = random.randint(1, 3)
            
            if case_type == 1:
                de_latex = "Trường hợp bằng nhau Cạnh - Cạnh - Cạnh (c.c.c) phát biểu rằng:"
                ans_correct = "Ba cạnh của tam giác này bằng ba cạnh của tam giác kia"
                fake1 = "Hai cạnh và góc xen giữa bằng nhau"
                fake2 = "Một cạnh và hai góc kề bằng nhau"
                fake3 = "Ba góc bằng nhau"
            elif case_type == 2:
                de_latex = "Để $\\Delta ABC = \\Delta DEF$ (c.g.c) cần có AB=DE, BC=EF và góc nào bằng nhau?"
                ans_correct = "$\\hat{B} = \\hat{E}$ (Góc xen giữa)"
                fake1 = "$\\hat{A} = \\hat{D}$"
                fake2 = "$\\hat{C} = \\hat{F}$"
                fake3 = "Góc nào cũng được"
            else:
                de_latex = "Trường hợp bằng nhau Góc - Cạnh - Góc (g.c.g) yêu cầu cạnh phải như thế nào?"
                ans_correct = "Cạnh nằm xen giữa hai góc"
                fake1 = "Cạnh đối diện góc lớn nhất"
                fake2 = "Cạnh huyền"
                fake3 = "Cạnh bất kỳ"
            
            dap_an = ans_correct
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "Nhớ kỹ vị trí của các yếu tố: Góc xen giữa 2 cạnh (c.g.c) hoặc Cạnh xen giữa 2 góc (g.c.g)."

        # FALLBACK (DỰ PHÒNG AN TOÀN)
        else:
            x = random.randint(2, 10)
            de_latex = f"Tìm x, biết: $2x - 4 = 0$"
            ans_correct = "x = 2"
            dap_an = ans_correct
            options = ["x = 2", "x = 0", "x = -2", "x = 4"]
            goi_y_text = "Chuyển vế đổi dấu."
    # --- LỚP 8 ---
    elif "Lớp 8" in lop:
        question_type = "mcq"
        
        # 1. ĐA THỨC
        if "cộng trừ đa thức" in bai_lower:
            a, b = random.randint(1, 5), random.randint(1, 9)
            c, d = random.randint(1, 5), random.randint(1, 9)
            op = random.choice(["+", "-"])

            if op == "+":
                de_latex = f"Thu gọn đa thức: $({a}x + {b}) + ({c}x + {d})$"
                res_a = a + c
                res_b = b + d
                ans_correct = f"${res_a}x + {res_b}$"
                options = [ans_correct, f"${res_a}x - {res_b}$", f"${a-c}x + {b-d}$", f"${res_a}x$"]
                dap_an = ans_correct
                goi_y_text = "Cộng các hạng tử đồng dạng (có cùng biến x) với nhau."
            else:
                de_latex = f"Thu gọn đa thức: $({a}x + {b}) - ({c}x + {d})$"
                res_a = a - c
                res_b = b - d
                sign = "+" if res_b >= 0 else ""
                ans_correct = f"${res_a}x {sign}{res_b}$"
                dap_an = ans_correct
                options = [ans_correct, f"${a+c}x + {b+d}$", f"${res_a}x + {b+d}$", f"${a}x + {res_b}$"]
                goi_y_text = "Phá ngoặc (đổi dấu nếu có dấu trừ đằng trước) rồi cộng trừ hạng tử đồng dạng."

        elif "nhân đa thức" in bai_lower:
            # Case: x(x + a)
            a = random.randint(2, 9)
            de_latex = f"Thực hiện phép nhân: $x(x + {a})$"
            ans_correct = f"$x^2 + {a}x$"
            dap_an = ans_correct
            options = [ans_correct, f"$x^2 + {a}$", f"$2x + {a}$", f"$x + {a}x$"]
            goi_y_text = "Nhân đơn thức với từng hạng tử của đa thức."

        elif "chia đa thức" in bai_lower:
            # Case: (ax^2 + bx) : x
            a = random.randint(2, 5)
            b = random.randint(2, 9)
            de_latex = f"Thực hiện phép chia: $({a}x^2 + {b}x) : x$"
            ans_correct = f"${a}x + {b}$"
            dap_an = ans_correct
            options = [ans_correct, f"${a}x^2 + {b}$", f"${a}x$", f"${a+b}x$"]
            goi_y_text = "Chia từng hạng tử của đa thức cho đơn thức."

        # 2. HẰNG ĐẲNG THỨC
        elif "bình phương" in bai_lower: # của tổng/hiệu
            a = random.randint(1, 6)
            sign = random.choice(["+", "-"])
            op_latex = "+" if sign == "+" else "-"
            de_latex = f"Khai triển hằng đẳng thức: $(x {op_latex} {a})^2$"
            mid_val = 2 * a
            sq_val = a * a
            if sign == "+":
                ans_correct = f"$x^2 + {mid_val}x + {sq_val}$"
                goi_y_latex = "(A+B)^2 = A^2 + 2AB + B^2"
            else:
                ans_correct = f"$x^2 - {mid_val}x + {sq_val}$"
                goi_y_latex = "(A-B)^2 = A^2 - 2AB + B^2"
            dap_an = ans_correct
            options = [ans_correct, f"$x^2 {op_latex} {mid_val}x - {sq_val}$", f"$x^2 + {sq_val}$", f"$x^2 - {sq_val}$"]
            goi_y_text = "Sử dụng hằng đẳng thức đáng nhớ."

        elif "hiệu hai bình phương" in bai_lower:
            a = random.randint(1, 9)
            de_latex = f"Khai triển: $(x - {a})(x + {a})$"
            ans_correct = f"$x^2 - {a*a}$"
            dap_an = ans_correct
            options = [ans_correct, f"$x^2 + {a*a}$", f"$x^2 - {2*a}x + {a*a}$", f"$x - {a*a}$"]
            goi_y_text = "Hằng đẳng thức hiệu hai bình phương:"
            goi_y_latex = "A^2 - B^2 = (A-B)(A+B)"

        # 3. PHÂN THỨC
        elif "rút gọn phân thức" in bai_lower:
            a = random.randint(1, 5)
            de_latex = f"Rút gọn phân thức: $\\frac{{2x + {2*a}}}{{x + {a}}}$"
            ans_correct = "2"
            dap_an = ans_correct
            options = ["2", f"2(x+{a})", "x", f"{a}"]
            goi_y_text = "Đặt nhân tử chung ở tử số rồi rút gọn với mẫu số."

        elif "cộng trừ phân thức" in bai_lower:
            # Simple case same denominator: (x)/(x+1) + (1)/(x+1)
            de_latex = "Kết quả của phép tính: $\\frac{x}{x+1} + \\frac{1}{x+1}$ (với $x \\ne -1$)"
            ans_correct = "1"
            dap_an = ans_correct
            options = ["1", "$\\frac{x+1}{2x+2}$", "0", "x"]
            goi_y_text = "Cộng tử số với nhau, giữ nguyên mẫu số."

        # 4. HÀM SỐ BẬC NHẤT
        elif "hệ số góc" in bai_lower:
            a = random.randint(2, 9) * random.choice([1, -1])
            b = random.randint(1, 9)
            de_latex = f"Hệ số góc của đường thẳng $y = {a}x + {b}$ là?"
            ans_correct = str(a)
            dap_an = ans_correct
            options = [str(a), str(b), str(-a), f"{a}x"]
            goi_y_text = "Trong hàm số $y=ax+b$, hệ số góc là a."

        elif "giá trị hàm số" in bai_lower:
            a = random.randint(2, 5)
            b = random.randint(1, 5)
            x_val = random.randint(0, 5)
            de_latex = f"Cho hàm số $y = {a}x - {b}$. Tính f({x_val})?"
            res = a * x_val - b
            ans_correct = str(res)
            dap_an = ans_correct
            options = [str(res), str(res+1), str(a), str(b)]
            goi_y_text = "Thay giá trị x vào công thức hàm số."

        else:
            # Fallback
            de_latex = "Giải phương trình $2x - 4 = 0$"
            dap_an = "2"
            options = ["2", "-2", "4", "0"]
            goi_y_text = "Chuyển vế đổi dấu."

    # --- LỚP 9 ---
    elif "Lớp 9" in lop:
        question_type = "mcq"  # Đa số lớp 9 dùng trắc nghiệm cho các bài lý thuyết/công thức
        
        # 1. CĂN THỨC
        if "điều kiện" in bai_lower:
            # Dạng: Căn bậc hai của (x - a) xác định khi nào?
            a = random.randint(1, 9)
            sign = random.choice([-1, 1])
            if sign == 1:
                de_latex = f"Tìm điều kiện xác định của biểu thức $\\sqrt{{x - {a}}}$"
                ans_correct = f"$x \\ge {a}$"
                dap_an = ans_correct
                options = [ans_correct, f"$x > {a}$", f"$x \\le {a}$", f"$x < {a}$"]
                goi_y_latex = f"x - {a} \\ge 0 \\Leftrightarrow x \\ge {a}"
            else:
                de_latex = f"Tìm điều kiện xác định của biểu thức $\\sqrt{{ {a} - x}}$"
                ans_correct = f"$x \\le {a}$"
                dap_an = ans_correct
                options = [ans_correct, f"$x < {a}$", f"$x \\ge {a}$", f"$x > {a}$"]
                goi_y_latex = f"{a} - x \\ge 0 \\Leftrightarrow x \\le {a}"
            goi_y_text = "Biểu thức trong căn bậc hai phải lớn hơn hoặc bằng 0."

        elif "rút gọn" in bai_lower:
            # Dạng: Rút gọn căn(a^2 * b)
            a = random.randint(2, 5)
            de_latex = f"Rút gọn biểu thức: $\\sqrt{{{a}^2 x}}$ với $x \\ge 0$"
            ans_correct = f"${a}\\sqrt{{x}}$"
            dap_an = ans_correct
            options = [ans_correct, f"${a}x$", f"${a*a}\\sqrt{{x}}$", f"$\\sqrt{{{a}x}}$"]
            goi_y_text = "Đưa thừa số ra ngoài dấu căn."
            goi_y_latex = "\\sqrt{A^2 B} = |A|\\sqrt{B}"

        # 2. HÀM SỐ BẬC NHẤT
        elif "đồ thị" in bai_lower:
            # Dạng: Điểm nào thuộc đồ thị?
            a = random.randint(1, 4) * random.choice([-1, 1])
            b = random.randint(1, 5)
            x_val = random.randint(0, 2)
            y_val = a * x_val + b
            de_latex = f"Điểm nào sau đây thuộc đồ thị hàm số $y = {a}x + {b}$?"
            ans_correct = f"$({x_val}; {y_val})$"
            dap_an = ans_correct
            fake1 = f"$({x_val}; {y_val + 1})$"
            fake2 = f"$({x_val + 1}; {y_val})$"
            fake3 = f"$(0; 0)$"
            options = [ans_correct, fake1, fake2, fake3]
            goi_y_text = "Thay toạ độ điểm vào công thức hàm số, nếu hai vế bằng nhau thì điểm đó thuộc đồ thị."

        elif "song song" in bai_lower or "cắt nhau" in bai_lower:
            a = random.randint(2, 5)
            b = random.randint(1, 5)
            de_latex = f"Đường thẳng $y = {a}x - {b}$ song song với đường thẳng nào sau đây?"
            ans_correct = f"$y = {a}x + 2$"
            dap_an = ans_correct
            options = [ans_correct, f"$y = {a+1}x - {b}$", f"$y = -{a}x + 2$", f"$y = x - {b}$"]
            goi_y_text = "Hai đường thẳng song song có hệ số góc a bằng nhau và tung độ gốc b khác nhau."

        # 3. HỆ PHƯƠNG TRÌNH
        elif "hệ phương trình" in bai_lower:
            # Dạng: Tổng hiệu đơn giản
            x = random.randint(1, 4)
            y = random.randint(1, 4)
            s = x + y
            d = x - y
            de_latex = f"Giải hệ phương trình: $\\begin{{cases}} x + y = {s} \\\\ x - y = {d} \\end{{cases}}$"
            ans_correct = f"$(x={x}; y={y})$"
            dap_an = ans_correct
            options = [ans_correct, f"$(x={y}; y={x})$", f"$(x={x}; y={-y})$", f"$(x={s}; y={d})$"]
            goi_y_text = "Cộng đại số hai phương trình để tìm x, sau đó thay vào tìm y."

        # 4. PHƯƠNG TRÌNH BẬC HAI
        elif "công thức nghiệm" in bai_lower or "delta" in bai_lower:
            # Tính Delta
            a = random.randint(1, 3)
            b = random.randint(3, 7)
            c = random.randint(1, 3)
            de_latex = f"Tính biệt thức $\\Delta$ của phương trình: ${a}x^2 + {b}x + {c} = 0$"
            delta = b*b - 4*a*c
            dap_an = delta
            question_type = "number" # Chuyển sang nhập số cho bài này
            goi_y_text = "Công thức tính Delta:"
            goi_y_latex = "\\Delta = b^2 - 4ac"

        elif "vi-ét" in bai_lower:
            # Tổng hoặc tích nghiệm
            x1 = random.randint(1, 5)
            x2 = random.randint(1, 5)
            S = x1 + x2
            P = x1 * x2
            req = random.choice(["tổng", "tích"])
            de_latex = f"Cho phương trình $x^2 - {S}x + {P} = 0$. Tính {req} hai nghiệm của phương trình."
            if req == "tổng":
                dap_an = S
                goi_y_latex = "x_1 + x_2 = -\\frac{b}{a}"
            else:
                dap_an = P
                goi_y_latex = "x_1 x_2 = \\frac{c}{a}"
            question_type = "number"
            goi_y_text = "Sử dụng định lý Vi-ét."

        # 5. HÌNH HỌC (ĐƯỜNG TRÒN & LƯỢNG GIÁC)
        elif "lượng giác" in bai_lower:
            # Định nghĩa sin, cos, tan
            funcs = {
                "sin": ("Đối", "Huyền"),
                "cos": ("Kề", "Huyền"),
                "tan": ("Đối", "Kề"),
                "cot": ("Kề", "Đối")
            }
            chon = random.choice(list(funcs.keys()))
            canh1, canh2 = funcs[chon]
            de_latex = f"Trong tam giác vuông, tỉ số lượng giác ${chon} \\alpha$ được tính bằng?"
            ans_correct = f"$\\frac{{\\text{{{canh1}}}}}{{\\text{{{canh2}}}}}$"
            dap_an = ans_correct
            
            wrong1 = f"$\\frac{{\\text{{{canh2}}}}}{{\\text{{{canh1}}}}}$" # Nghịch đảo
            wrong2 = "$\\frac{\\text{Đối}}{\\text{Huyền}}$" if chon != "sin" else "$\\frac{\\text{Kề}}{\\text{Huyền}}$"
            wrong3 = "$\\frac{\\text{Kề}}{\\text{Đối}}$" if chon != "cot" else "$\\frac{\\text{Đối}}{\\text{Kề}}$"
            
            options = [ans_correct, wrong1, wrong2, wrong3]
            # Lọc trùng
            options = list(set(options))
            
            goi_y_text = "Nhớ câu thần chú: Sin đi học, Cos không hư, Tan đoàn kết, Cot kết đoàn."

        elif "nội tiếp" in bai_lower or "đường tròn" in bai_lower:
            arc = random.randint(40, 120)
            de_latex = f"Góc nội tiếp chắn cung {arc}$^\\circ$ thì có số đo bằng bao nhiêu?"
            ans_correct = arc // 2
            dap_an = ans_correct
            question_type = "number"
            goi_y_text = "Số đo góc nội tiếp bằng một nửa số đo cung bị chắn."
            goi_y_latex = f"\\alpha = \\frac{{1}}{{2}} \\times {arc}^\\circ"

        # FALLBACK
        else:
            de_latex = "Giải phương trình $x^2 - 4 = 0$"
            ans_correct = "$x = \\pm 2$"
            dap_an = ans_correct
            options = [ans_correct, "$x = 2$", "$x = 4$", "$x = 16$"]
            goi_y_text = "Chuyển vế và khai căn."
    if question_type == "mcq" and options: random.shuffle(options)
              
    return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex

# --- HÀM PHÂN TÍCH LỖI SAI ---
def phan_tich_loi_sai(user_ans, true_ans, q_type):
    hint_msg = "Chưa đúng rồi! (Tsis yog lawm)"
    if q_type == "number" and isinstance(true_ans, (int, float)):
        try:
            diff = abs(user_ans - true_ans)
            if diff == 0: return "Tuyệt vời!"
            if user_ans == -true_ans:
                hint_msg = "Bạn bị nhầm dấu rồi! (Tsis yog, saib dua)"
            elif diff <= 2:
                hint_msg = "Gần đúng rồi! Tính lại cẩn thận nhé."
        except: pass
    return hint_msg

# --- DỊCH THUẬT THÔNG MINH (GIỮ NGUYÊN LaTeX) ---
# Hàm này tách phần text và phần latex, chỉ dịch text.
def dich_sang_mong_giu_cong_thuc(text):
    # Tách chuỗi dựa trên dấu $ (ký hiệu LaTeX)
    # Regex này tách thành: [Text1, $LaTeX1$, Text2, $LaTeX2$...]
    parts = re.split(r'(\$.*?\$)', text)
    
    translated_parts = []
    for part in parts:
        # Nếu là phần công thức (bắt đầu và kết thúc bằng $), giữ nguyên
        if part.startswith('$') and part.endswith('$'):
            translated_parts.append(part)
        else:
            # Nếu là văn bản thường và không rỗng, thì dịch
            if part.strip():
                try:
                    trans = GoogleTranslator(source='vi', target='hmn').translate(part)
                    translated_parts.append(trans)
                except:
                    translated_parts.append(part)
            else:
                translated_parts.append(part) # Giữ khoảng trắng
                
    return "".join(translated_parts)

# --- TEXT TO SPEECH (XỬ LÝ ĐỌC TOÁN HỌC) ---
def text_to_speech_html(text, lang='vi'):
    # 1. Loại bỏ ký tự LaTeX bao quanh
    clean_text = text.replace("$", "")
    
    # 2. Xử lý đọc Phân số: \frac{a}{b} -> a phần b
    clean_text = re.sub(r'\\frac\{(.+?)\}\{(.+?)\}', r'\1 phần \2', clean_text)
    
    # 3. Xử lý đọc Số mũ và Biến số (QUAN TRỌNG)
    # x^2 -> x bình phương, x^3 -> x lập phương, x^n -> x mũ n
    clean_text = re.sub(r'(\w)\^2', r'\1 bình phương ', clean_text)
    clean_text = re.sub(r'(\w)\^3', r'\1 lập phương ', clean_text)
    clean_text = re.sub(r'(\w)\^(\d+)', r'\1 mũ \2 ', clean_text) # x^5 -> x mũ 5
    
    # 4. Xử lý biến liền nhau: xy -> x y (để không đọc thành từ vô nghĩa)
    # Thêm khoảng trắng giữa các chữ cái liền nhau trong toán học
    # Ví dụ: xy -> x y, abc -> a b c
    # Logic: Tìm 2 chữ cái liền nhau và chèn khoảng trắng
    # Lưu ý: Chỉ áp dụng cho các biến đơn giản, tránh phá vỡ từ tiếng Việt
    # Ở đây ta làm đơn giản hóa: thay thế các cụm biến phổ biến trong toán
    vars_math = ["xy", "xyz", "ab", "abc"]
    for v in vars_math:
        if v in clean_text:
            spaced_v = " ".join(list(v))
            clean_text = clean_text.replace(v, spaced_v)

    # 5. Bảng thay thế ký hiệu sang tiếng Việt
    replacements = {
        "\\begin{cases}": "hệ phương trình ",
        "\\end{cases}": "",
        "\\\\": " và ",
        "\\times": " nhân ",
        "\\cdot": " nhân ",
        ":": " chia ",
        "+": " cộng ",
        "-": " trừ ",
        "\\le": " nhỏ hơn hoặc bằng ",
        "\\ge": " lớn hơn hoặc bằng ",
        "\\neq": " khác ",
        "\\approx": " xấp xỉ ",
        "\\circ": " độ ",
        "\\hat": " góc ",
        "\\sqrt": " căn bậc hai của ",
        "\\pm": " cộng trừ ",
        "\\pi": " pi ",
        ">": " lớn hơn ",
        "<": " nhỏ hơn ",
        "=": " bằng "
    }
    
    for k, v in replacements.items():
        clean_text = clean_text.replace(k, v)
    
    # Dọn dẹp dấu ngoặc thừa
    clean_text = clean_text.replace("{", "").replace("}", "")

    # Tạo audio
    tts = gTTS(text=clean_text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    md = f"""
        <audio controls autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    return md

# --- GIAO DIỆN CHÍNH ---

st.markdown(f"""
<div class="hmong-header-container">
    <div class="hmong-top-bar">SỞ GIÁO DỤC VÀ ĐÀO TỈNH ĐIỆN BIÊN</div>
    <div class="hmong-main-title">
        <h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>
        <h2>🚀 GIA SƯ TOÁN AI - BẢN MƯỜNG</h2>
        <div class="visit-counter">Lượt truy cập: {st.session_state.visit_count}</div>
    </div>
    <div class="hmong-pattern"></div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 80px;'>🏔️</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("📚 CHỌN BÀI HỌC")
    
    ds_lop = list(CHUONG_TRINH_HOC.keys())
    lop_chon = st.selectbox("Lớp:", ds_lop)
    
    du_lieu_lop = CHUONG_TRINH_HOC[lop_chon]
    ds_chuong = list(du_lieu_lop.keys())
    chuong_chon = st.selectbox("Chương/Chủ đề:", ds_chuong)
    
    ds_bai = du_lieu_lop[chuong_chon]
    bai_chon = st.selectbox("Bài học:", ds_bai)
    
    if st.button("🔄 Đặt lại"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("---")
    with st.expander("👨‍🏫 Khu vực Giáo viên"):
        st.info(f"Tổng lượt truy cập: {st.session_state.visit_count}")

col_trai, col_phai = st.columns([1.6, 1])

if 'de_bai' not in st.session_state:
    st.session_state.de_bai = ""
    st.session_state.q_type = "number"
    st.session_state.dap_an = 0
    st.session_state.options = []
    st.session_state.goi_y_text = ""
    st.session_state.goi_y_latex = ""
    st.session_state.show_hint = False
    st.session_state.submitted = False

def click_sinh_de():
    db, qt, da, ops, gyt, gyl = tao_de_toan(lop_chon, bai_chon)
    st.session_state.de_bai = db
    st.session_state.q_type = qt
    st.session_state.dap_an = da
    st.session_state.options = ops
    st.session_state.goi_y_text = gyt
    st.session_state.goi_y_latex = gyl
    st.session_state.show_hint = False
    st.session_state.submitted = False

with col_trai:
    st.subheader(f"📖 {bai_chon}")
    
    if st.button("✨ TẠO CÂU HỎI MỚI (AI Generated)", type="primary", on_click=click_sinh_de):
        pass
    
    if st.session_state.de_bai:
        st.markdown('<div class="problem-box">', unsafe_allow_html=True)
        st.markdown("### ❓ Câu hỏi:")
        st.markdown(f"## {st.session_state.de_bai}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### 🤖 Công cụ hỗ trợ AI:")
        col_tool1, col_tool2 = st.columns(2)
        with col_tool1:
            if st.button("🗣️ Đọc đề (Giọng AI)"):
                audio_html = text_to_speech_html(st.session_state.de_bai)
                st.markdown(audio_html, unsafe_allow_html=True)
        with col_tool2:
            if st.button("🌏 Dịch H'Mông"):
                # Sử dụng hàm dịch mới giữ nguyên công thức
                bd = dich_sang_mong_giu_cong_thuc(st.session_state.de_bai)
                # Hiển thị bằng markdown để render công thức LaTeX
                st.info(f"**H'Mông:** {bd}")

with col_phai:
    st.subheader("✍️ Làm bài")
    
    if st.session_state.de_bai:
        with st.form("form_lam_bai"):
            user_ans = None
            if st.session_state.q_type == "mcq":
                st.markdown("**Chọn đáp án đúng:**")
                if st.session_state.options: 
                    user_ans = st.radio("Đáp án:", st.session_state.options, label_visibility="collapsed")
            else:
                if isinstance(st.session_state.dap_an, int) or (isinstance(st.session_state.dap_an, float) and st.session_state.dap_an.is_integer()):
                    user_ans = st.number_input("Nhập đáp án (Số nguyên):", step=1, format="%d")
                else:
                    user_ans = st.number_input("Nhập đáp án:", step=0.01, format="%.2f")

            btn_nop = st.form_submit_button("✅ Kiểm tra")
            
            if btn_nop and user_ans is not None:
                st.session_state.submitted = True
                is_correct = False
                if st.session_state.q_type == "mcq":
                    if user_ans == st.session_state.dap_an: is_correct = True
                else:
                    if isinstance(st.session_state.dap_an, str):
                         if str(user_ans) == st.session_state.dap_an: is_correct = True
                    else:
                        if abs(user_ans - float(st.session_state.dap_an)) <= 0.05: is_correct = True

                if is_correct:
                    st.balloons()
                    st.success("CHÍNH XÁC! (Yog lawm) 👏")
                    st.session_state.show_hint = False
                else:
                    adaptive_msg = phan_tich_loi_sai(user_ans, st.session_state.dap_an, st.session_state.q_type)
                    st.markdown(f'<div class="error-box">{adaptive_msg}</div>', unsafe_allow_html=True)
                    
                    ans_display = st.session_state.dap_an
                    if isinstance(ans_display, float) and ans_display.is_integer():
                        ans_display = int(ans_display)
                        
                    st.markdown(f"Đáp án đúng là: **{ans_display}**")
                    st.session_state.show_hint = True
        
        if st.session_state.show_hint:
            st.markdown("---")
            # --- GỢI Ý TIẾNG VIỆT ---
            st.markdown('<div class="hint-container">', unsafe_allow_html=True)
            st.markdown(f"**💡 Gợi ý (Tiếng Việt):** {st.session_state.goi_y_text}")
            if st.session_state.goi_y_latex: st.latex(st.session_state.goi_y_latex)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # --- GỢI Ý TIẾNG H'MÔNG (DÙNG HÀM MỚI) ---
            translation = dich_sang_mong_giu_cong_thuc(st.session_state.goi_y_text)
            st.markdown('<div class="hmong-hint">', unsafe_allow_html=True)
            st.markdown(f"**🗣️ H'Mông:** {translation}")
            # Đảm bảo công thức toán học hiển thị giống hệt phần Tiếng Việt
            if st.session_state.goi_y_latex: st.latex(st.session_state.goi_y_latex)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👈 Chọn bài học và nhấn nút 'Tạo câu hỏi mới'.")

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư - Bản Mường.")
