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

# --- DỮ LIỆU MẪU (đã mở rộng chủ đề 7,8,9) ---
lop_options = [
    "Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5",
    "Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"
]

# Chuẩn hóa dữ liệu, tránh trùng khóa
chuong_options = {
    "Lớp 1": ["Chủ đề 1: Các số đến 10", "Chủ đề 2: Các số đến 20", "Chủ đề 3: Các số đến 100", "Chủ đề 4: Hình học và đo lường", "Chủ đề 5: Giải toán"],
    "Lớp 2": ["Chủ đề 1: Số và phép tính", "Chủ đề 2: Đo lường", "Chủ đề 3: Hình học", "Chủ đề 4: Giải toán có lời văn"],
    "Lớp 3": ["Chủ đề 1: Số và phép tính", "Chủ đề 2: Đo lường", "Chủ đề 3: Hình học", "Chủ đề 4: Giải toán"],
    "Lớp 4": ["Chủ đề 1: Số tự nhiên – Phép tính", "Chủ đề 2: Phân số", "Chủ đề 3: Đo lường", "Chủ đề 4: Hình học"],
    "Lớp 5": ["Chủ đề 1: Số thập phân", "Chủ đề 2: Tỉ số – Phần trăm", "Chủ đề 3: Đo lường", "Chủ đề 4: Hình học"],
    "Lớp 6": ["Chương 1: Số tự nhiên", "Chương 2: Số nguyên", "Chương 3: Phân số", "Chương 4: Biểu thức – Đại số", "Chương 5: Hình học trực quan"],
    "Lớp 7": ["Chương 1: Số hữu tỉ – Số thực", "Chương 2: Hàm số và đồ thị", "Chương 3: Hình học tam giác", "Chương 4: Thống kê"],
    "Lớp 8": ["Chương 1: Đại số – Đa thức", "Chương 2: Phân thức", "Chương 3: Phương trình bậc nhất", "Chương 4: Hình học tứ giác – Đa giác"],
    "Lớp 9": ["Chương 1: Căn bậc hai – Căn thức", "Chương 2: Hàm số bậc nhất", "Chương 3: Hàm số bậc hai", "Chương 4: Phương trình bậc hai", "Chương 5: Hình học không gian – Trụ – Nón – Cầu"],
}

# Bài học — mở rộng đầy đủ 7, 8, 9 (không trùng key)
bai_options = {
    # Lớp 7
    "Chương 1: Số hữu tỉ – Số thực": ["Cộng trừ số hữu tỉ", "Nhân chia số hữu tỉ", "Lũy thừa", "Số thực"],
    "Chương 2: Hàm số và đồ thị": ["Hàm số y=ax", "Đồ thị hàm số bậc nhất"],
    "Chương 3: Hình học tam giác": ["Tính chất tam giác", "Định lí Py-ta-go", "Tam giác vuông"],
    "Chương 4: Thống kê": ["Bảng tần số", "Biểu đồ cột", "Số trung bình cộng"],

    # Lớp 8
    "Chương 1: Đại số – Đa thức": ["Cộng trừ đa thức", "Nhân đơn thức – đa thức", "Hằng đẳng thức đáng nhớ"],
    "Chương 2: Phân thức": ["Rút gọn phân thức", "Quy đồng mẫu", "Phép toán phân thức"],
    "Chương 3: Phương trình bậc nhất": ["Giải phương trình", "Bài toán thực tế", "Phương trình chứa ẩn ở mẫu"],
    "Chương 4: Hình học tứ giác – Đa giác": ["Tính chất tứ giác", "Đa giác đều", "Diện tích đa giác"],

    # Lớp 9
    "Chương 1: Căn bậc hai – Căn thức": ["Định nghĩa căn bậc hai", "Biến đổi đơn giản căn thức", "Biến đổi nâng cao"],
    "Chương 2: Hàm số bậc nhất": ["Hệ số góc", "Đồ thị", "Tính chất"],
    "Chương 3: Hàm số bậc hai": ["Parabol", "Đồ thị hàm số y=ax^2", "Tính chất parabol"],
    "Chương 4: Phương trình bậc hai": ["Công thức nghiệm", "Biện luận", "Giải bài toán thực tế"],
    "Chương 5: Hình học không gian – Trụ – Nón – Cầu": ["Thể tích", "Diện tích", "Quan hệ hình học"],
}
