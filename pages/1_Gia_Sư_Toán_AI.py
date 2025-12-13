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
    page_title="Gia sư Toán AI (Lớp 1-9)",
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
    "Chương I. Tập hợp các số tự nhiên": [
      "Bài 1. Tập hợp",
      "Bài 2. Cách ghi số tự nhiên",
      "Bài 3. Thứ tự trong tập hợp các số tự nhiên",
      "Bài 4. Phép cộng và phép trừ số tự nhiên",
      "Bài 5. Phép nhân và phép chia số tự nhiên",
      "Bài 6. Luỹ thừa với số mũ tự nhiên",
      "Bài 7. Thứ tự thực hiện các phép tính"
    ],
    "Chương II. Tính chia hết trong tập hợp các số tự nhiên": [
      "Bài 8. Quan hệ chia hết và tính chất",
      "Bài 9. Dấu hiệu chia hết",
      "Bài 10. Số nguyên tố",
      "Bài 11. Ước chung. Ước chung lớn nhất",
      "Bài 12. Bội chung. Bội chung nhỏ nhất"
    ],
    "Chương III. Số nguyên": [
      "Bài 13. Tập hợp các số nguyên",
      "Bài 14. Phép cộng và phép trừ số nguyên",
      "Bài 15. Quy tắc dấu ngoặc",
      "Bài 16. Phép nhân số nguyên",
      "Bài 17. Phép chia hết. Ước và bội của một số nguyên"
    ],
    "Chương V. Tính đối xứng của hình phẳng trong tự nhiên": [
      "Bài 21. Hình có trục đối xứng",
      "Bài 22. Hình có tâm đối xứng"
    ]
  },

  "Lớp 7": {
    "Chương I. Số hữu tỉ": [
      "Bài 1. Tập hợp các số hữu tỉ",
      "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ",
      "Bài 3. Luỹ thừa với số mũ tự nhiên của một số hữu tỉ",
      "Bài 4. Thứ tự thực hiện các phép tính. Quy tắc chuyển vế"
    ],
    "Chương II. Số thực": [
      "Bài 5. Làm quen với số thập phân vô hạn tuần hoàn",
      "Bài 6. Số vô tỉ. Căn bậc hai số học",
      "Bài 7. Tập hợp các số thực"
    ],
    "Chương III. Góc và đường thẳng song song": [
      "Bài 8. Góc ở vị trí đặc biệt. Tia phân giác của một góc",
      "Bài 9. Hai đường thẳng song song và dấu hiệu nhận biết",
      "Bài 10. Tiên đề Euclid. Tính chất của hai đường thẳng song song",
      "Bài 11. Định lí và chứng minh định lí"
    ],
    "Chương IV. Tam giác bằng nhau": [
      "Bài 12. Tổng các góc trong một tam giác",
      "Bài 13. Hai tam giác bằng nhau. Trường hợp bằng nhau thứ nhất",
      "Bài 14. Trường hợp bằng nhau thứ hai và thứ ba",
      "Bài 15. Các trường hợp bằng nhau của tam giác vuông",
      "Bài 16. Tam giác cân. Đường trung trực của đoạn thẳng"
    ]
  },

  "Lớp 8": {
    "Chương I. Đa thức": [
      "Bài 1. Đơn thức",
      "Bài 2. Đa thức",
      "Bài 3. Phép cộng và phép trừ đa thức",
      "Bài 4. Phép nhân đa thức",
      "Bài 5. Phép chia đa thức cho đơn thức"
    ],
    "Chương II. Hằng đẳng thức đáng nhớ và ứng dụng": [
      "Bài 6. Hiệu hai bình phương. Bình phương của một tổng hay một hiệu",
      "Bài 7. Lập phương của một tổng. Lập phương của một hiệu",
      "Bài 8. Tổng và hiệu hai lập phương",
      "Bài 9. Phân tích đa thức thành nhân tử"
    ],
    "Chương VI. Phân thức đại số": [
      "Bài 21. Phân thức đại số",
      "Bài 22. Tính chất cơ bản của phân thức đại số",
      "Bài 23. Phép cộng và phép trừ phân thức đại số",
      "Bài 24. Phép nhân và phép chia phân thức đại số"
    ],
    "Chương VII. Phương trình bậc nhất và hàm số bậc nhất": [
      "Bài 25. Phương trình bậc nhất một ẩn",
      "Bài 26. Giải bài toán bằng cách lập phương trình",
      "Bài 27. Khái niệm hàm số và đồ thị của hàm số",
      "Bài 28. Hàm số bậc nhất và đồ thị của hàm số",
      "Bài 29. Hệ số góc của đường thẳng"
    ]
  },

  "Lớp 9": {
    "Chương III. Căn bậc hai và căn bậc ba": [
      "Bài 7. Căn bậc hai và căn thức bậc hai",
      "Bài 8. Khai căn bậc hai với phép nhân và phép chia",
      "Bài 9. Biến đổi đơn giản và rút gọn biểu thức chứa căn thức bậc hai",
      "Bài 10. Căn bậc ba và căn thức bậc ba"
    ],
    "Chương IV. Hệ thức lượng trong tam giác vuông": [
      "Bài 11. Tỉ số lượng giác của góc nhọn",
      "Bài 12. Một số hệ thức giữa cạnh, góc trong tam giác vuông và ứng dụng"
    ],
    "Chương VI. Hàm số y = ax² (a ≠ 0). Phương trình bậc hai một ẩn": [
      "Bài 18. Hàm số y = ax² (a ≠ 0)",
      "Bài 19. Phương trình bậc hai một ẩn",
      "Bài 20. Định lí Viète và ứng dụng",
      "Bài 21. Giải bài toán bằng cách lập phương trình"
    ],
    "Chương IX. Đường tròn ngoại tiếp và đường tròn nội tiếp": [
      "Bài 27. Góc nội tiếp",
      "Bài 28. Đường tròn ngoại tiếp và đường tròn nội tiếp của một tam giác",
      "Bài 29. Tứ giác nội tiếp",
      "Bài 30. Đa giác đều"
    ]
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
import random
import math

# Giả định lop và bai_lower được xác định trước.
# Ví dụ: lop = "Lớp 6"; bai_lower = "tập hợp"

# --- LỚP 6 (CHUẨN SGK KẾT NỐI TRI THỨC) ---
if "Lớp 6" in lop:
    question_type = "mcq"

    # 1. Tập hợp – phần tử (Chương I, Bài 1)
    if "tập hợp" in bai_lower:
        # Tạo tập hợp có thể có phần tử lặp
        elements = random.sample(range(1, 20), random.randint(3, 6))
        
        # Thỉnh thoảng thêm phần tử lặp để kiểm tra kiến thức về "phần tử khác nhau"
        if random.random() < 0.3:
             elements.append(random.choice(elements))
             elements.append(random.choice(elements))
        
        random.shuffle(elements)
        A = set(elements) # Số phần tử thực sự
        dap_an = len(A)
        
        # Tạo chuỗi LaTeX cho câu hỏi
        de_latex = f"Tập hợp $A = \\{{{'; '.join(map(str,elements))}\\}}$ có bao nhiêu phần tử?"
        
        # Tạo các đáp án nhiễu dựa trên đáp án đúng và số lượng phần tử viết ra (có lặp)
        options = [dap_an, len(elements)]
        
        # Thêm các đáp án nhiễu khác biệt
        while len(options) < 4:
            new_option = random.choice([dap_an + random.randint(-2, 2), dap_an + random.randint(1, 3)])
            if new_option > 0 and new_option not in options:
                options.append(new_option)
        
        options = random.sample(list(set(options)), 4)
        
        # Đảm bảo đáp án đúng có trong options
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
             
        goi_y_text = "Số phần tử của tập hợp là số lượng phần tử khác nhau được liệt kê."

    # 2. Cách ghi số tự nhiên – giá trị chữ số (Chương I, Bài 2)
    elif "cách ghi" in bai_lower or "ghi số" in bai_lower or "giá trị chữ số" in bai_lower:
        n = random.randint(100, 9999) # Số có 3 hoặc 4 chữ số
        
        # Chọn ngẫu nhiên vị trí hàng
        s_n = str(n)
        
        if len(s_n) == 3:
             hangs = {"trăm": 100, "chục": 10, "đơn vị": 1}
        else: # 4 chữ số
             hangs = {"nghìn": 1000, "trăm": 100, "chục": 10, "đơn vị": 1}
        
        hang_key = random.choice(list(hangs.keys()))
        vi_tri = int(math.log10(hangs[hang_key])) # 0, 1, 2, 3
        
        # Chữ số tại vị trí đó
        chu_so = int(s_n[len(s_n) - 1 - vi_tri])
        
        dap_an = chu_so * hangs[hang_key]
        
        de_latex = f"Trong số {n}, chữ số hàng {hang_key} có giá trị là:"
        
        # Đáp án nhiễu: chỉ là chữ số, giá trị hàng, và một giá trị ngẫu nhiên
        options = list(set([dap_an, chu_so, hangs[hang_key], random.randint(1, 9) * hangs[hang_key]]))
        
        while len(options) < 4:
             options.append(random.randint(1, 100))
             options = list(set(options))
             
        options = random.sample(options, 4)
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
        
        goi_y_text = "Giá trị của chữ số bằng chữ số đó nhân với giá trị của hàng mà nó đứng."

    # 3. Thứ tự trong tập hợp số tự nhiên (Chương I, Bài 3)
    elif "thứ tự" in bai_lower or "so sánh" in bai_lower:
        a = random.randint(100, 999)
        b = random.randint(100, 999)
        
        if a > b:
            dap_an = f"{a} > {b}"
            options = [dap_an, f"{a} < {b}", f"{a} = {b}", f"{b} > {a}" if b < a else f"{b} < {a}"]
        elif a < b:
            dap_an = f"{a} < {b}"
            options = [dap_an, f"{a} > {b}", f"{a} = {b}", f"{b} < {a}" if b > a else f"{b} > {a}"]
        else: # a == b, trường hợp hiếm nhưng cần xử lý
            dap_an = f"{a} = {b}"
            options = [dap_an, f"{a} < {b}", f"{a} > {b}", f"{b} = {a}"]

        de_latex = f"So sánh hai số tự nhiên $a={a}$ và $b={b}$:"
        options = random.sample(list(set(options)), 4)
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
             
        goi_y_text = "Trong hai số tự nhiên khác nhau, số có nhiều chữ số hơn thì lớn hơn. Nếu số chữ số bằng nhau, ta so sánh từng cặp chữ số từ trái sang phải."

    # 4. Phép cộng – phép trừ (Chương I, Bài 4)
    elif "phép cộng" in bai_lower or "phép trừ" in bai_lower:
        a = random.randint(100, 500)
        b = random.randint(50, a - 50) # Đảm bảo phép trừ không âm
        
        if random.choice([True, False]): # Ngẫu nhiên cộng hoặc trừ
            dap_an = a + b
            de_latex = f"Kết quả của phép tính {a} + {b} là:"
            options = [dap_an, a - b, dap_an + random.randint(1, 5), dap_an - random.randint(1, 5)]
        else:
            dap_an = a - b
            de_latex = f"Kết quả của phép tính {a} - {b} là:"
            options = [dap_an, a + b, dap_an + random.randint(1, 5), dap_an - random.randint(1, 5)]
            
        options = random.sample(list(set(options)), 4)
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
             
        goi_y_text = "Thực hiện phép tính theo quy tắc đặt tính hoặc tính nhẩm."

    # 5. Phép nhân – phép chia (Chương I, Bài 5)
    elif "phép nhân" in bai_lower or "phép chia" in bai_lower:
        if random.choice([True, False]): # Phép nhân
            a = random.randint(10, 30)
            b = random.randint(5, 15)
            dap_an = a * b
            de_latex = f"Kết quả của phép tính {a} \\times {b} là:"
            # Đáp án nhiễu: tổng, hoặc nhân sai một chút
            options = [dap_an, a + b, dap_an + a, dap_an - b]
            
        else: # Phép chia hết
            b = random.randint(5, 15)
            dap_an = random.randint(5, 20)
            a = dap_an * b
            de_latex = f"Kết quả của phép tính {a} : {b} là:"
            # Đáp án nhiễu: sai số một, phép trừ
            options = [dap_an, dap_an + 1, a - b, dap_an - 1]

        options = random.sample(list(set(options)), 4)
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
             
        goi_y_text = "Phép nhân là phép cộng lặp lại. Phép chia là phép toán ngược của phép nhân."

    # 6. Lũy thừa với số mũ tự nhiên (Chương I, Bài 6)
    elif "lũy thừa" in bai_lower:
        a = random.randint(2, 5) # Cơ số
        b = random.randint(2, 4) # Số mũ
        
        dap_an = a ** b
        
        de_latex = f"Giá trị của $a^{b}$ với $a={a}$ bằng:"
        
        # Đáp án nhiễu: a*b, a^(b+1), a*(b-1), a^b - a
        options = list(set([dap_an, a * b, a ** (b - 1), a ** (b + 1)]))
        
        while len(options) < 4:
             options.append(random.randint(1, 100))
             options = list(set(options))
             
        options = random.sample(options, 4)
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
             
        goi_y_text = f"Lũy thừa $a^{b}$ là tích của $b$ thừa số $a$: $\\underbrace{{a \\cdot a \\cdot \\ldots \\cdot a}}_{{b}}$."

    # 7. Thứ tự thực hiện phép tính (Chương I, Bài 7)
    elif "thứ tự thực hiện" in bai_lower or "thứ tự phép tính" in bai_lower:
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        c = random.randint(2, 5)
        
        # Biểu thức: a + b * c
        dap_an = a + b * c
        de_latex = f"Giá trị của biểu thức {a} + {b} \\times {c} là:"
        
        # Đáp án nhiễu: (a+b)*c
        options = list(set([dap_an, (a + b) * c, a * b + c, a + b + c]))
        
        while len(options) < 4:
             options.append(random.randint(1, 50))
             options = list(set(options))
             
        options = random.sample(options, 4)
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
             
        goi_y_text = "Thứ tự ưu tiên: Lũy thừa $\\rightarrow$ Nhân/Chia $\\rightarrow$ Cộng/Trừ. Nếu có ngoặc thì ưu tiên trong ngoặc trước."

    # 8. Dấu hiệu chia hết (Chương I, Bài 8)
    elif "chia hết" in bai_lower:
        ds_2 = [10, 24, 38, 52] # Chia hết cho 2
        ds_3 = [12, 27, 45, 102] # Chia hết cho 3
        ds_5 = [15, 30, 45, 70] # Chia hết cho 5
        ds_9 = [18, 36, 99, 108] # Chia hết cho 9
        
        kieu = random.choice([2, 3, 5, 9])
        
        if kieu == 2:
            n = random.choice(ds_2)
            dap_an = "Có"
            de_latex = f"Số {n} có chia hết cho 2 không?"
            options = ["Có", "Không", "Chỉ chia hết cho 5", "Không xác định"]
            goi_y_text = "Số chia hết cho 2 có chữ số tận cùng là 0, 2, 4, 6, 8."
        
        elif kieu == 3:
            n = random.choice(ds_3)
            dap_an = "Có"
            de_latex = f"Số {n} có chia hết cho 3 không?"
            options = ["Có", "Không", "Chỉ chia hết cho 9", "Không xác định"]
            goi_y_text = "Số chia hết cho 3 có tổng các chữ số chia hết cho 3."
            
        elif kieu == 5:
            n = random.choice(ds_5)
            dap_an = "Có"
            de_latex = f"Số {n} có chia hết cho 5 không?"
            options = ["Có", "Không", "Chỉ chia hết cho 2", "Không xác định"]
            goi_y_text = "Số chia hết cho 5 có chữ số tận cùng là 0 hoặc 5."
            
        else: # kieu == 9
            n = random.choice(ds_9)
            dap_an = "Có"
            de_latex = f"Số {n} có chia hết cho 9 không?"
            options = ["Có", "Không", "Chỉ chia hết cho 3", "Không xác định"]
            goi_y_text = "Số chia hết cho 9 có tổng các chữ số chia hết cho 9."

    # 9. Số nguyên tố – hợp số (Chương I, Bài 10)
    elif "nguyên tố" in bai_lower or "hợp số" in bai_lower:
        if random.choice([True, False]): # Hỏi số nguyên tố
            prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
            composite_numbers = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
            
            dap_an = str(random.choice(prime_numbers))
            de_latex = "Số nào sau đây là **số nguyên tố**?"
            
            # Chọn 3 hợp số làm đáp án nhiễu
            options_temp = random.sample([c for c in composite_numbers if str(c) != dap_an], 3)
            options = [dap_an] + [str(o) for o in options_temp]
            
            goi_y_text = "Số nguyên tố là số tự nhiên lớn hơn 1, chỉ có hai ước là 1 và chính nó."
            
        else: # Hỏi hợp số
            prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
            composite_numbers = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
            
            dap_an = str(random.choice(composite_numbers))
            de_latex = "Số nào sau đây là **hợp số**?"
            
            # Chọn 3 số nguyên tố làm đáp án nhiễu
            options_temp = random.sample([p for p in prime_numbers if str(p) != dap_an and p!=2], 3)
            options = [dap_an] + [str(o) for o in options_temp]
            
            goi_y_text = "Hợp số là số tự nhiên lớn hơn 1, có nhiều hơn hai ước."

        options = random.sample(options, 4)
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an

    # 10. Ước chung – bội chung (Chương I, Bài 13 & 14)
    elif "ước" in bai_lower or "bội" in bai_lower or "ucln" in bai_lower or "bcnn" in bai_lower:
        
        if random.choice([True, False]): # ƯCLN (Ước chung lớn nhất)
            a = random.choice([12, 18, 24, 30])
            b = random.choice([15, 20, 25, 35])
            
            dap_an = math.gcd(a, b) # ƯCLN
            de_latex = f"$\text{{ƯCLN}}({a}, {b})$ là:"
            
            # Đáp án nhiễu: 1, bội chung nhỏ nhất (thường lớn), và các ước chung khác
            bcnn = abs(a * b) // math.gcd(a, b)
            options = list(set([dap_an, 1, bcnn, dap_an * 2]))
            
            while len(options) < 4:
                 options.append(random.randint(1, 10))
                 options = list(set(options))
            
        else: # BCNN (Bội chung nhỏ nhất)
            a = random.choice([4, 6, 8, 9])
            b = random.choice([5, 10, 12, 15])
            
            dap_an = abs(a * b) // math.gcd(a, b) # BCNN
            de_latex = f"$\text{{BCNN}}({a}, {b})$ là:"
            
            # Đáp án nhiễu: ƯCLN, tích, và các bội khác
            ucln = math.gcd(a, b)
            tich = a * b
            options = list(set([dap_an, ucln, tich, dap_an // 2 if dap_an % 2 == 0 else dap_an + a]))
            
            while len(options) < 4:
                 options.append(random.randint(1, 100))
                 options = list(set(options))
                 
        options = random.sample([str(o) for o in options], 4)
        dap_an = str(dap_an) # Chuyển đáp án về chuỗi để đồng nhất với options
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
             
        goi_y_text = "Sử dụng quy tắc phân tích các số ra thừa số nguyên tố."

    # 11. Số nguyên – trục số (Chương II, Bài 15)
    elif "số nguyên" in bai_lower or "trục số" in bai_lower:
        a = random.randint(-10, 10)
        b = random.randint(-10, 10)
        
        # Chọn ngẫu nhiên phép toán: cộng hoặc trừ
        if random.choice([True, False]):
            dap_an = a + b
            de_latex = f"Kết quả của phép tính {a} + ({b}) là:"
        else:
             # Đảm bảo phép trừ tạo ra số nguyên âm hoặc dương
            dap_an = a - b
            de_latex = f"Kết quả của phép tính {a} - ({b}) là:" # {a} - (-{b}) nếu b âm

        options = list(set([dap_an, a - b, b - a, abs(a + b)]))
        
        while len(options) < 4:
             options.append(random.randint(-20, 20))
             options = list(set(options))
             
        options = random.sample([str(o) for o in options], 4)
        dap_an = str(dap_an)
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
             
        goi_y_text = "Cộng hai số nguyên cùng dấu: cộng giá trị tuyệt đối và giữ nguyên dấu. Khác dấu: trừ giá trị tuyệt đối và lấy dấu của số có giá trị tuyệt đối lớn hơn."

    # 12. Hình có trục đối xứng (Chương III, Bài 20)
    elif "trục đối xứng" in bai_lower:
        dap_an = "Hình chữ nhật"
        de_latex = "Trong các hình sau, hình nào có **trục đối xứng**?"
        options = ["Hình chữ nhật", "Hình bình hành", "Hình thang thường", "Tam giác thường"]
        random.shuffle(options)
        
        # Thêm hình ảnh minh họa cho các hình cơ bản
        goi_y_text = "Trục đối xứng là đường thẳng chia hình thành hai nửa bằng nhau mà nửa này là ảnh đối xứng của nửa kia qua đường thẳng đó. Hình chữ nhật có 2 trục đối xứng."
        
        # Trigger hình ảnh cho chủ đề này
        #  
        # (Không thể sử dụng tag trong câu trả lời hiện tại, đây là một gợi ý)
        
        # Đảm bảo đáp án đúng có trong options
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an

    # 13. Hình có tâm đối xứng (Chương III, Bài 21)
    elif "tâm đối xứng" in bai_lower or "đối xứng" in bai_lower:
        dap_an = "Hình bình hành"
        de_latex = "Trong các hình sau, hình nào có **tâm đối xứng**?"
        options = ["Hình bình hành", "Tam giác thường", "Hình thang cân", "Hình diều"]
        random.shuffle(options)
        
        goi_y_text = "Tâm đối xứng là điểm mà mọi điểm thuộc hình khi quay 180 độ quanh điểm đó sẽ trùng với chính nó. Hình bình hành có tâm đối xứng là giao điểm hai đường chéo."
        
        # Trigger hình ảnh cho chủ đề này
        # 
        
        # Đảm bảo đáp án đúng có trong options
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
             
    # Câu hỏi mặc định hoặc không khớp bài
    else:
        a, b, c = random.randint(10, 20), random.randint(1, 5), random.randint(1, 5)
        dap_an = a + b * c
        de_latex = f"Tính giá trị biểu thức: $A = {a} + {b} \\times {c}$"
        options = list(set([dap_an, (a + b) * c, a + b + c, a * b + c]))
        
        while len(options) < 4:
             options.append(random.randint(1, 50))
             options = list(set(options))
             
        options = random.sample([str(o) for o in options], 4)
        dap_an = str(dap_an)
        if dap_an not in options:
             options[random.randint(0,3)] = dap_an
        
        goi_y_text = "Thứ tự thực hiện phép tính: Nhân chia trước, cộng trừ sau."

    # In ra kết quả (ví dụ)
    print(f"Câu hỏi: {de_latex}")
    print(f"Đáp án đúng: {dap_an}")
    print(f"Các lựa chọn: {options}")
    print(f"Gợi ý: {goi_y_text}")

    # --- LỚP 7 ---
    elif "Lớp 7" in lop:
        if "số hữu tỉ" in bai_lower:
            tu = random.randint(1, 5)
            de_latex = f"Kết quả của phép tính $\\frac{{{tu}}}{{2}} + \\frac{{{tu}}}{{2}}$ là?"
            dap_an = tu
            goi_y_text = "Cộng hai phân số cùng mẫu."
        elif "căn bậc hai" in bai_lower:
            sq = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100])
            de_latex = f"Tính $\\sqrt{{{sq}}}$"
            dap_an = int(math.sqrt(sq))
            goi_y_text = "Tìm số dương bình phương lên bằng số trong căn."
        elif "tuyệt đối" in bai_lower:
            val = random.randint(-10, -1)
            de_latex = f"Tính $|{val}|$"
            dap_an = abs(val)
            goi_y_text = "Giá trị tuyệt đối của số âm là số đối của nó."
        elif "góc" in bai_lower:
            angle = random.randint(30, 150)
            de_latex = f"Hai góc đối đỉnh, góc thứ nhất bằng ${angle}^\\circ$. Góc thứ hai bằng bao nhiêu?"
            dap_an = angle
            goi_y_text = "Hai góc đối đỉnh thì bằng nhau."
        elif "tam giác" in bai_lower:
            a = random.randint(30, 80)
            b = random.randint(30, 80)
            de_latex = f"Tam giác ABC có $\\hat{{A}}={a}^\\circ, \\hat{{B}}={b}^\\circ$. Tính $\\hat{{C}}$."
            dap_an = 180 - a - b
            goi_y_text = "Tổng ba góc trong tam giác là 180 độ."
        else:
             a = random.randint(1, 5)
             de_latex = f"Tính $(-{a})^2$"
             dap_an = a**2

    # --- LỚP 8 ---
    elif "Lớp 8" in lop:
        question_type = "mcq"
        if "đa thức" in bai_lower:
            a = random.randint(2, 5)
            de_latex = f"Rút gọn biểu thức: $x(x + {a}) - x^2$"
            ans_correct = f"${a}x$"
            dap_an = ans_correct
            options = [f"${a}x$", f"$-{a}x$", f"$2x^2 + {a}x$", f"${a}$"]
            goi_y_text = "Nhân đơn thức với đa thức rồi thu gọn."
            goi_y_latex = f"x^2 + {a}x - x^2 = {a}x"
        elif "hằng đẳng thức" in bai_lower:
            a = random.randint(1, 5)
            de_latex = f"Khai triển: $(x - {a})^2$"
            ans_correct = f"$x^2 - {2*a}x + {a**2}$"
            dap_an = ans_correct
            options = [ans_correct, f"$x^2 + {2*a}x + {a**2}$", f"$x^2 - {a**2}$", f"$x^2 + {a**2}$"]
            goi_y_text = "Bình phương một hiệu:"
            goi_y_latex = "(A-B)^2 = A^2 - 2AB + B^2"
        elif "phân thức" in bai_lower:
            a = random.randint(2, 5)
            de_latex = f"Rút gọn phân thức: $\\frac{{x^2 - {a**2}}}{{x + {a}}}$"
            ans_correct = f"$x - {a}$"
            dap_an = ans_correct
            options = [f"$x - {a}$", f"$x + {a}$", f"$x^2 - {a}$", f"$1$"]
            goi_y_text = "Phân tích tử số thành nhân tử:"
            goi_y_latex = f"x^2 - {a}^2 = (x-{a})(x+{a})"
        elif "hàm số" in bai_lower:
            a = random.randint(2, 5)
            b = random.randint(1, 9)
            x_val = 2
            de_latex = f"Cho hàm số $y = {a}x + {b}$. Giá trị của y tại $x={x_val}$ là?"
            ans_correct = f"{a*x_val + b}"
            dap_an = ans_correct
            options = [f"{a*x_val + b}", f"{a*x_val - b}", f"{a + b}", f"{b}"]
            goi_y_text = "Thay giá trị x vào công thức hàm số."
        else:
            de_latex = "Bậc của đa thức $x^2y + xy^3$ là?"
            dap_an = "4"
            options = ["4", "3", "2", "5"]
            goi_y_text = "Bậc của đa thức là bậc của hạng tử có bậc cao nhất."

    # --- LỚP 9 ---
    elif "Lớp 9" in lop:
        question_type = "mcq"
        if "căn thức" in bai_lower:
            a = random.randint(2, 5)
            de_latex = f"Điều kiện xác định của $\\sqrt{{x - {a}}}$ là?"
            ans_correct = f"$x \\ge {a}$"
            dap_an = ans_correct
            options = [ans_correct, f"$x > {a}$", f"$x \\le {a}$", f"$x < {a}$"]
            goi_y_text = "Biểu thức trong căn bậc hai phải không âm."
            goi_y_latex = f"x - {a} \\ge 0 \\Leftrightarrow x \\ge {a}"
        elif "hệ phương trình" in bai_lower:
            x = random.randint(1, 3)
            y = random.randint(1, 3)
            c1 = x + y
            c2 = x - y
            de_latex = f"Nghiệm của hệ: $\\begin{{cases}} x+y={c1} \\\\ x-y={c2} \\end{{cases}}$"
            ans_correct = f"$({x}; {y})$"
            dap_an = ans_correct
            options = [ans_correct, f"$({y}; {x})$", f"$({x}; -{y})$", f"$(-{x}; {y})$"]
            goi_y_text = "Cộng đại số hai phương trình."
        elif "phương trình bậc hai" in bai_lower or "vi-ét" in bai_lower:
            x1 = random.randint(1, 5)
            x2 = random.randint(1, 5)
            S = x1 + x2
            P = x1 * x2
            de_latex = f"Phương trình $x^2 - {S}x + {P} = 0$ có tổng hai nghiệm là?"
            ans_correct = f"{S}"
            dap_an = ans_correct
            options = [f"{S}", f"-{S}", f"{P}", f"-{P}"]
            goi_y_text = "Theo định lý Vi-ét:"
            goi_y_latex = "x_1 + x_2 = -\\frac{b}{a}"
        elif "hàm số" in bai_lower:
            a = random.randint(2, 5)
            de_latex = f"Đường thẳng $y = {a}x + 1$ song song với đường thẳng nào?"
            ans_correct = f"$y = {a}x - 2$"
            dap_an = ans_correct
            options = [ans_correct, f"$y = {a}x + 1$", f"$y = -{a}x + 2$", f"$y = 2x + 1$"]
            goi_y_text = "Hai đường thẳng song song có cùng hệ số góc a."
        elif "lượng giác" in bai_lower or "hình học" in bai_lower:
            de_latex = "Trong tam giác vuông, $Sin \\alpha$ bằng?"
            ans_correct = "$\\frac{\\text{Đối}}{\\text{Huyền}}$"
            dap_an = ans_correct
            options = [ans_correct, "$\\frac{\\text{Kề}}{\\text{Huyền}}$", "$\\frac{\\text{Đối}}{\\text{Kề}}$", "$\\frac{\\text{Kề}}{\\text{Đối}}$"]
            goi_y_text = "Công thức Sin:"
            goi_y_latex = "\\sin = \\frac{\\text{Đối}}{\\text{Huyền}}"
        else:
            de_latex = "Giải phương trình $x^2 - 4 = 0$"
            ans_correct = "$x = \\pm 2$"
            dap_an = ans_correct
            options = [ans_correct, "$x = 2$", "$x = 4$", "$x = 16$"]

    # --- FALLBACK AN TOÀN ---
    else:
        a, b = random.randint(1, 20), random.randint(1, 20)
        de_latex = f"Tính: ${a} + {b} = ?$"
        dap_an = a + b
        goi_y_text = "Thực hiện phép cộng."

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
        <h2>🚀 GIA SƯ TOÁN AI </h2>
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
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư ")

