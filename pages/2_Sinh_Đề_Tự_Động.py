# file: sinh_de_kntc.py
import re
import io
import requests
import streamlit as st
from docx import Document
from docx.shared import Inches
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageFile
import matplotlib
import matplotlib.pyplot as plt
import traceback
import logging

# --- Cấu hình logging (hữu ích khi debug) ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Matplotlib backend cho môi trường server ---
matplotlib.use("Agg")
plt.rcParams['mathtext.fontset'] = 'cm'
ImageFile.LOAD_TRUNCATED_IMAGES = True

st.set_page_config(page_title="Sinh Đề KNTC Tự Động", page_icon="📝", layout="wide")
st.title("📝 Sinh Đề Tự Động – Theo Ma Trận Đặc Tả Tối Giản")

# --- API KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- DỮ LIỆU MẪU (đã sửa trùng khóa) ---
lop_options = [
    "Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5",
    "Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"
]

# --- Chuẩn hóa chương/bài theo danh sách Toán 6 → 9 ---
chuong_options = {
    "Lớp 6": [
        "Chương I: Tập hợp các số tự nhiên",
        "Chương II: Tính chia hết trong tập hợp các số tự nhiên",
        "Chương III: Số nguyên",
        "Chương IV: Một số hình phẳng trong thực tiễn",
        "Chương V: Tính đối xứng của hình phẳng trong tự nhiên",
        "Chương VI: Phân số",
        "Chương VII: Số thập phân",
        "Chương VIII: Những hình hình học cơ bản",
        "Chương IX: Dữ liệu và xác suất thực nghiệm",
        "Hoạt động thực hành trải nghiệm"
    ],
    "Lớp 7": [
        "Chương I: Số hữu tỉ",
        "Chương II: Số thực",
        "Chương III: Góc và đường thẳng song song",
        "Chương IV: Tam giác bằng nhau",
        "Chương V: Thu thập và biểu diễn dữ liệu",
        "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ",
        "Chương VII: Biểu thức đại số và đa thức một biến",
        "Chương VIII: Làm quen với biến cố và xác suất của biến cố",
        "Chương IX: Quan hệ giữa các yếu tố trong một tam giác",
        "Chương X: Một số hình khối trong thực tiễn",
        "Bài tập ôn tập cuối năm"
    ],
    "Lớp 8": [
        "Chương I: Đa thức",
        "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
        "Chương III: Tứ giác",
        "Chương IV: Định lí Thalès",
        "Chương V: Dữ liệu và biểu đồ",
        "Chương VI: Phân thức đại số",
        "Chương VII: Phương trình bậc nhất và hàm số bậc nhất",
        "Chương VIII: Mở đầu về tính xác suất của biến cố",
        "Chương IX: Tam giác đồng dạng",
        "Chương X: Một số hình khối trong thực tiễn",
        "Bài tập ôn tập cuối năm"
    ],
    "Lớp 9": [
        "Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn",
        "Chương II: Phương trình và bất phương trình bậc nhất một ẩn",
        "Chương III: Căn bậc hai và căn bậc ba",
        "Chương IV: Hệ thức lượng trong tam giác vuông",
        "Chương V: Đường tròn",
        "Chương VI: Hàm số y = ax² (a ≠ 0). Phương trình bậc hai một ẩn",
        "Chương VII: Tần số và tần số tương đối",
        "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản",
        "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp",
        "Chương X: Một số hình khối trong thực tiễn",
        "Hoạt động thực hành trải nghiệm"
    ],
}

bai_options = {
    # Lớp 6
    "Chương I: Tập hợp các số tự nhiên": [
        "Bài 1. Tập hợp",
        "Bài 2. Cách ghi số tự nhiên",
        "Bài 3. Thứ tự trong tập hợp các số tự nhiên",
        "Bài 4. Phép cộng và phép trừ số tự nhiên",
        "Bài 5. Phép nhân và phép chia số tự nhiên",
        "Bài 6. Lũy thừa với số mũ tự nhiên",
        "Bài 7. Thứ tự thực hiện các phép tính",
        "Ôn tập chương I"
    ],
    "Chương II: Tính chia hết trong tập hợp các số tự nhiên": [
        "Bài 8. Quan hệ chia hết và tính chất",
        "Bài 9. Dấu hiệu chia hết",
        "Bài 10. Số nguyên tố",
        "Bài 11. Ước chung, Ước chung lớn nhất",
        "Bài 12. Bội chung, Bội chung nhỏ nhất",
        "Ôn tập chương II"
    ],
    "Chương III: Số nguyên": [
        "Bài 13. Tập hợp các số nguyên",
        "Bài 14. Phép cộng và phép trừ số nguyên",
        "Bài 15. Quy tắc dấu ngoặc",
        "Bài 16. Phép nhân số nguyên",
        "Bài 17. Phép chia hết. Ước và bội của một số nguyên",
        "Ôn tập chương III"
    ],
    "Chương IV: Một số hình phẳng trong thực tiễn": [
        "Bài 18. Hình tam giác đều, hình vuông, hình lục giác đều",
        "Bài 19. Hình chữ nhật, hình thoi, hình bình hành, hình thang cân",
        "Bài 20. Chu vi và diện tích của một số tứ giác đã học",
        "Ôn tập chương IV"
    ],
    "Chương V: Tính đối xứng của hình phẳng trong tự nhiên": [
        "Bài 21. Hình có trục đối xứng",
        "Bài 22. Hình có tâm đối xứng",
        "Ôn tập chương V"
    ],
    "Chương VI: Phân số": [
        "Bài 23. Mở rộng phân số. Phân số bằng nhau",
        "Bài 24. So sánh phân số. Hỗn số dương",
        "Luyện tập chung",
        "Bài 25. Phép cộng và phép trừ phân số",
        "Bài 26. Phép nhân và phép chia phân số",
        "Bài 27. Hai bài toán về phân số",
        "Luyện tập chung",
        "Bài tập cuối chương VI"
    ],
    "Chương VII: Số thập phân": [
        "Bài 28. Số thập phân",
        "Bài 29. Tính toán với số thập phân",
        "Bài 30. Làm tròn và ước lượng",
        "Bài 31. Một số bài toán về tỉ số và tỉ lệ phần trăm",
        "Luyện tập chung",
        "Bài tập cuối chương VII"
    ],
    "Chương VIII: Những hình hình học cơ bản": [
        "Bài 32. Điểm và đường thẳng",
        "Bài 33. Điểm nằm giữa hai điểm. Tia",
        "Bài 34. Đoạn thẳng. Độ dài đoạn thẳng",
        "Bài 35. Trung điểm của đoạn thẳng",
        "Luyện tập chung",
        "Bài 36. Góc",
        "Bài 37. Số đo góc",
        "Luyện tập chung",
        "Bài tập cuối chương VIII"
    ],
    "Chương IX: Dữ liệu và xác suất thực nghiệm": [
        "Bài 38. Dữ liệu và thu thập dữ liệu",
        "Bài 39. Bảng thống kê và biểu đồ tranh",
        "Bài 40. Biểu đồ cột",
        "Bài 41. Biểu đồ cột kép",
        "Luyện tập chung",
        "Bài 42. Kết quả có thể và sự kiện trong trò chơi, thí nghiệm",
        "Bài 43. Xác suất thực nghiệm",
        "Luyện tập chung",
        "Bài tập cuối chương IX"
    ],
    "Hoạt động thực hành trải nghiệm": [
        "Kế hoạch chi tiêu cá nhân và gia đình",
        "Hoạt động thể thao yêu thích nhất trong hè",
        "Vẽ hình đơn giản với phần mềm GeoGebra"
    ],

    # Lớp 7
    "Chương I: Số hữu tỉ": [
        "Bài 1. Tập hợp các số hữu tỉ",
        "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ",
        "Bài 3. Lũy thừa với số mũ tự nhiên của một số hữu tỉ",
        "Bài 4. Thứ tự thực hiện các phép tính. Quy tắc chuyển vế",
        "Ôn tập chương I"
    ],
    "Chương II: Số thực": [
        "Bài 5. Làm quen với số thập phân vô hạn tuần hoàn",
        "Bài 6. Số vô tỉ. Căn bậc hai số học",
        "Bài 7. Tập hợp các số thực",
        "Ôn tập chương II"
    ],
    # ... tiếp tục đầy đủ các chương/bài 7,8,9 theo danh sách bạn gửi ...
}

# --- Sidebar: giao diện và tham số ma trận ---
with st.sidebar:
    st.header("Thông tin sinh đề")
    lop = st.selectbox("Chọn lớp", lop_options, index=5 if len(lop_options) > 5 else 0)
    chuong_list = chuong_options.get(lop, [])
    if chuong_list:
        chuong = st.selectbox("Chọn chủ đề/chương", chuong_list, index=0)
    else:
        chuong = st.text_input("Chưa có chủ đề cho lớp này", "")

    bai_list = bai_options.get(chuong, [])
    if bai_list:
        bai = st.selectbox("Chọn bài", bai_list, index=0)
    else:
        bai = st.text_input("Chưa có bài cho chủ đề này", "")

    st.markdown("---")
    st.subheader("⚙️ Phân bổ theo Ma trận (CV 7991 Tối giản)")

    # Cấu hình số câu hỏi tổng cộng
    so_cau = st.number_input("Tổng số câu hỏi", min_value=1, max_value=50, value=21)

    col_nl, col_ds, col_tl = st.columns(3)
    with col_nl:
        phan_bo_nl = st.number_input("NL (Nhiều Lựa chọn)", min_value=0, value=12)
    with col_ds:
        phan_bo_ds = st.number_input("DS (Đúng - Sai)", min_value=0, value=2)
    with col_tl:
        phan_bo_tl = st.number_input("TL (Tự luận/Trả lời ngắn)", min_value=0, value=7)

    st.markdown("---")
    st.subheader("Độ khó (Cognitive Level)")

    col_nb, col_th, col_vd = st.columns(3)
    with col_nb:
        so_cau_nb = st.number_input("Nhận biết", min_value=0, value=6)
    with col_th:
        so_cau_th = st.number_input("Thông hiểu", min_value=0, value=8)
    with col_vd:
        so_cau_vd = st.number_input("Vận dụng/VDC", min_value=0, value=7)

    total_check = int(phan_bo_nl + phan_bo_ds + phan_bo_tl)
    total_level = int(so_cau_nb + so_cau_th + so_cau_vd)

    if total_check != so_cau:
        st.error(f"Tổng số câu theo loại (NL+DS+TL) = {total_check} không khớp Tổng ({so_cau}).")
    if total_level != so_cau:
        st.error(f"Tổng cấp độ (NB+TH+VĐ) = {total_level} không khớp Tổng ({so_cau}).")

    co_dap_an = st.checkbox("Có đáp án", value=True)

# --- BUILD PROMPT ---
def build_prompt(lop, chuong, bai, so_cau,
                 phan_bo_nl, phan_bo_ds, phan_bo_tl,
                 so_cau_nb, so_cau_th, so_cau_vd, co_dap_an):
    dan_ap = "Tạo Đáp án và Lời giải chi tiết sau mỗi câu hỏi." if co_dap_an else "Không cần Đáp án."
    prompt_ma_tran = f"""
Cấu trúc ĐỀ VÀ MA TRẬN ĐẶC TẢ TỐI GIẢN (Tổng {so_cau} câu):
1. PHẦN TRẮC NGHIỆM KHÁCH QUAN (NL/DS)
    - Số câu Nhiều Lựa chọn (NL): {phan_bo_nl} câu.
    - Số câu Đúng - Sai (DS): {phan_bo_ds} câu.
2. PHẦN TỰ LUẬN (TL) / TRẢ LỜI NGẮN
    - Số câu Tự luận/Trả lời ngắn (TL): {phan_bo_tl} câu.

PHÂN BỔ MỨC ĐỘ NHẬN THỨC:
    - Nhận biết: {so_cau_nb} câu
    - Thông hiểu: {so_cau_th} câu
    - Vận dụng/VDC: {so_cau_vd} câu

YÊU CẦU ĐỀ BÀI:
1. Tạo {so_cau} câu hỏi, trong đó:
    - {phan_bo_nl} câu Trắc nghiệm 4 lựa chọn (A, B, C, D).
    - {phan_bo_ds} câu Trắc nghiệm Đúng - Sai (mỗi câu có 4 ý a, b, c, d).
    - {phan_bo_tl} câu Tự luận hoặc Trả lời ngắn.
2. Đảm bảo tổng số câu theo từng mức độ nhận thức (NB/TH/VĐ) khớp với phân bổ trên.
3. Đặt Tiêu đề rõ ràng cho từng phần.
4. Mỗi câu hỏi phải được gắn nhãn Mức độ và Loại câu hỏi (ví dụ: Câu 1. [NL - Nhận biết]).
5. Toàn bộ công thức toán phải được viết bằng LaTeX và **phải** đặt trong delimiters $$...$$. Ví dụ: $$\\frac{{a}}{{b}}$$
6. {dan_ap}
"""
    prompt_context = f"""
Bạn là giáo viên Toán, hãy sinh đề kiểm tra cho {lop} theo sách "Kết nối tri thức với cuộc sống".
- Chủ đề/Chương: {chuong}
- Bài: {bai}
{prompt_ma_tran}
"""
    return prompt_context

# --- GỌI API (Google Generative Language) ---
def generate_questions(api_key, lop, chuong, bai, so_cau,
                       phan_bo_nl, phan_bo_ds, phan_bo_tl,
                       so_cau_nb, so_cau_th, so_cau_vd, co_dap_an):
    MODEL = "models/gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

    prompt = build_prompt(lop, chuong, bai, so_cau,
                          phan_bo_nl, phan_bo_ds, phan_bo_tl,
                          so_cau_nb, so_cau_th, so_cau_vd, co_dap_an)

    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        if r.status_code != 200:
            try:
                j_error = r.json()
                error_message = j_error.get("error", {}).get("message", r.text)
            except Exception:
                error_message = r.text
            return False, f"❌ Lỗi API {r.status_code}: {error_message}"
        j = r.json()
        if j.get("candidates") and len(j["candidates"]) > 0:
            cand = j["candidates"][0]
            content = cand.get("content", {})
            parts = content.get("parts", [])
            if parts and len(parts) > 0:
                text = parts[0].get("text", "")
                return True, text
        return False, "❌ Lỗi: AI không trả về nội dung hợp lệ."
    except requests.exceptions.Timeout:
        return False, "❌ Lỗi kết nối: Yêu cầu hết
