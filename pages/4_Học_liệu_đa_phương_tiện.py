# app.py — Ứng dụng Streamlit: Tổng hợp Toán + AI Features (Cập nhật: tích hợp mục lục lớp 6-9)
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
from gtts import gTTS # Thư viện mới để đọc văn bản
import os

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
# Mục lục Toán học Lớp 6 - 9 (Đã trích xuất từ file mục lục toán.docx)
# -----------------------
index_structure = {
    "6": [
        {"chapter_title": "CHƯƠNG I. TẬP HỢP CÁC SỐ TỰ NHIÊN.", "lessons": [
            "Bài 1. Tập hợp.", "Bài 2. Cách ghi số tự nhiên.", "Bài 3. Thứ tự trong tập hợp các số tự nhiên.", "Bài 4. Phép cộng và phép trừ số tự nhiên.", "Bài 5. Phép nhân và phép chia số tự nhiên.", "Bài 6. Luỹ thừa với số mũ tự nhiên.", "Bài 7. Thứ tự thực hiện các phép tính.", "Ôn tập chương I."
        ]},
        {"chapter_title": "CHƯƠNG II. TÍNH CHIA HẾT TRONG TẬP HỢP CÁC SỐ TỰ NHIÊN.", "lessons": [
            "Bài 8. Quan hệ chia hết và tính chất.", "Bài 9. Dấu hiệu chia hết.", "Bài 10. Số nguyên tố.", "Bài 11. Ước chung. Ước chung lớn nhất.", "Bài 12. Bội chung. Bội chung nhỏ nhất.", "Ôn tập chương II."
        ]},
        {"chapter_title": "CHƯƠNG III. SỐ NGUYÊN.", "lessons": [
            "Bài 13. Tập hợp các số nguyên.", "Bài 14. Phép cộng và phép trừ số nguyên.", "Bài 15. Quy tắc dấu ngoặc.", "Bài 16. Phép nhân số nguyên.", "Bài 17. Phép chia hết. Ước và bội của một số nguyên.", "Ôn tập chương III."
        ]},
        {"chapter_title": "CHƯƠNG IV. MỘT SỐ HÌNH PHẲNG TRONG THỰC TIỄN.", "lessons": [
            "Bài 18. Hình tam giác đều. Hình vuông. Hình lục giác đều.", "Bài 19. Hình chữ nhật. Hình thoi. Hình bình hành. Hình thang cân.", "Bài 20. Chu vi và diện tích của một số tứ giác đã học.", "Ôn tập chương IV."
        ]},
        {"chapter_title": "CHƯƠNG V. TÍNH ĐỐI XỨNG CỦA HÌNH PHẲNG TRONG TỰ NHIÊN.", "lessons": [
            "Bài 21. Hình có trục đối xứng.", "Bài 22. Hình có tâm đối xứng.", "Ôn tập chương V."
        ]},
        {"chapter_title": "CHƯƠNG VI. PHÂN SỐ.", "lessons": [
            "Bài 23. Mở rộng phân số. Phân số bằng nhau.", "Bài 24. So sánh phân số. Hỗn số dương.", "Luyện tập chung.", "Bài 25. Phép cộng và phép trừ phân số.", "Bài 26. Phép nhân và phép chia phân số.", "Bài 27. Hai bài toán về phân số.", "Luyện tập chung.", "Bài tập cuối chương VI."
        ]},
        {"chapter_title": "CHƯƠNG VII. SỐ THẬP PHÂN.", "lessons": [
            "Bài 28. Số thập phân.", "Bài 29. Tính toán với số thập phân.", "Bài 30. Làm tròn và ước lượng.", "Bài 31. Một số bài toán về tỉ số và tỉ số phần trăm.", "Luyện tập chung.", "Bài tập cuối chương VII."
        ]},
        {"chapter_title": "CHƯƠNG VIII. NHỮNG HÌNH HÌNH HỌC CƠ BẢN.", "lessons": [
            "Bài 32. Điểm và đường thẳng.", "Bài 33. Điểm nằm giữa hai điểm. Tia.", "Bài 34. Đoạn thẳng. Độ dài đoạn thẳng.", "Bài 35. Trung điểm của đoạn thẳng.", "Luyện tập chung.", "Bài 36. Góc.", "Bài 37. Số đo góc.", "Luyện tập chung.", "Bài tập cuối chương VIII."
        ]},
        {"chapter_title": "CHƯƠNG IX. DỮ LIỆU VÀ XÁC SUẤT THỰC NGHIỆM.", "lessons": [
            "Bài 38. Dữ liệu và thu thập dữ liệu.", "Bài 39. Bảng thống kê và biểu đồ tranh.", "Bài 40. Biểu đồ cột.", "Bài 41. Biểu đồ cột kép.", "Luyện tập chung.", "Bài 42. Kết quả có thể và sự kiện trong trò chơi, thí nghiệm.", "Bài 43. Xác suất thực nghiệm.", "Luyện tập chung.", "Bài tập cuối chương IX."
        ]},
        {"chapter_title": "HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM.", "lessons": [
            "Kế hoạch chi tiêu cá nhân và gia đình.", "Hoạt động thể thao nào được yêu thích nhất trong hè?", "Vẽ hình đơn giản với phần mềm GeoGebra."
        ]}
    ],
    "7": [
        {"chapter_title": "CHƯƠNG I. SỐ HỮU TỈ.", "lessons": [
            "Bài 1. Tập hợp các số hữu tỉ.", "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ.", "Bài 3. Luỹ thừa với số mũ tự nhiên của một số hữu tỉ.", "Bài 4. Thứ tự thực hiện các phép tính. Quy tắc chuyển vế.", "Ôn tập chương I."
        ]},
        {"chapter_title": "CHƯƠNG II. SỐ THỰC.", "lessons": [
            "Bài 5. Làm quen với số thập phân vô hạn tuần hoàn.", "Bài 6. Số vô tỉ. Căn bậc hai số học.", "Bài 7. Tập hợp các số thực.", "Ôn tập chương II."
        ]},
        {"chapter_title": "CHƯƠNG III. GÓC VÀ ĐƯỜNG THẲNG SONG SONG.", "lessons": [
            "Bài 8. Góc ở vị trí đặc biệt. Tia phân giác của một góc.", "Bài 9. Hai đường thẳng song song và dấu hiệu nhận biết.", "Bài 10. Tiên đề Euclid. Tính chất của hai đường thẳng song song.", "Bài 11. Định lí và chứng minh định lí.", "Ôn tập chương III."
        ]},
        {"chapter_title": "CHƯƠNG IV. TAM GIÁC BẰNG NHAU.", "lessons": [
            "Bài 12. Tổng các góc trong một tam giác.", "Bài 13. Hai tam giác bằng nhau. Trường hợp bằng nhau thứ nhất của tam giác.", "Bài 14. Trường hợp bằng nhau thứ hai và thứ ba của tam giác.", "Bài 15. Các trường hợp bằng nhau của tam giác vuông.", "Bài 16. Tam giác cân. Đường trung trực của đoạn thẳng.", "Ôn tập chương IV."
        ]},
        {"chapter_title": "CHƯƠNG V. THU THẬP VÀ BIỂU DIỄN DỮ LIỆU.", "lessons": [
            "Bài 17. Thu thập và phân loại dữ liệu.", "Bài 18. Biểu đồ hình quạt tròn.", "Bài 19. Biểu đồ đoạn thẳng.", "Ôn tập chương V."
        ]},
        {"chapter_title": "CHƯƠNG VI. TỈ LỆ THỨC VÀ ĐẠI LƯỢNG TỈ LỆ.", "lessons": [
            "Bài 20. Tỉ lệ thức.", "Bài 21. Tính chất của dãy tỉ số bằng nhau.", "Bài 22. Đại lượng tỉ lệ thuận.", "Bài 23. Đại lượng tỉ lệ nghịch.", "Ôn tập chương VI."
        ]},
        {"chapter_title": "CHƯƠNG VII. BIỂU THỨC ĐẠI SỐ VÀ ĐA THỨC MỘT BIẾN.", "lessons": [
            "Bài 24. Biểu thức đại số.", "Bài 25. Đa thức một biến.", "Bài 26. Phép cộng và phép trừ đa thức một biến.", "Bài 27. Phép nhân đa thức một biến.", "Bài 28. Phép chia đa thức một biến.", "Ôn tập chương VII."
        ]},
        {"chapter_title": "CHƯƠNG VIII. LÀM QUEN VỚI BIẾN CỐ VÀ XÁC SUẤT CỦA BIẾN CỐ.", "lessons": [
            "Bài 29. Làm quen với biến cố.", "Bài 30. Làm quen với xác suất của biến cố.", "Ôn tập chương VIII."
        ]},
        {"chapter_title": "CHƯƠNG IX. QUAN HỆ GIỮA CÁC YẾU TỐ TRONG MỘT TAM GIÁC.", "lessons": [
            "Bài 31. Quan hệ giữa góc và cạnh đối diện trong một tam giác.", "Bài 32. Quan hệ giữa đường vuông góc và đường xiên.", "Bài 33. Quan hệ giữa ba cạnh của một tam giác.", "Bài 34. Sự đồng quy của ba đường trung tuyến, ba đường phân giác trong một tam giác.", "Bài 35. Sự đồng quy của ba đường trung trực, ba đường cao trong một tam giác.", "Ôn tập chương IX."
        ]},
        {"chapter_title": "CHƯƠNG X. MỘT SỐ HÌNH KHỐI TRONG THỰC TIỄN.", "lessons": [
            "Bài 36. Hình hộp chữ nhật và hình lập phương.", "Bài 37. Hình lăng trụ đứng tam giác và hình lăng trụ đứng tứ giác.", "Ôn tập chương X.", "BÀI TẬP ÔN TẬP CUỐI NĂM."
        ]}
    ],
    "8": [
        {"chapter_title": "CHƯƠNG I. ĐA THỨC.", "lessons": [
            "Bài 1. Đơn thức.", "Bài 2. Đa thức.", "Bài 3. Phép cộng và phép trừ đa thức.", "Bài 4. Phép nhân đa thức.", "Bài 5. Phép chia đa thức cho đơn thức.", "Ôn tập chương I."
        ]},
        {"chapter_title": "CHƯƠNG II. HẰNG ĐẲNG THỨC ĐÁNG NHỚ VÀ ỨNG DỤNG.", "lessons": [
            "Bài 6. Hiệu hai bình phương. Bình phương của một tổng hay một hiệu.", "Bài 7. Lập phương của một tổng. Lập phương của một hiệu.", "Bài 8. Tổng và hiệu hai lập phương.", "Bài 9. Phân tích đa thức thành nhân tử.", "Ôn tập chương II."
        ]},
        {"chapter_title": "CHƯƠNG III. TỨ GIÁC.", "lessons": [
            "Bài 10. Tứ giác.", "Bài 11. Hình thang cân.", "Bài 12. Hình bình hành.", "Bài 13. Hình chữ nhật.", "Bài 14. Hình thoi và hình vuông.", "Ôn tập chương III."
        ]},
        {"chapter_title": "CHƯƠNG IV. ĐỊNH LÍ THALÈS.", "lessons": [
            "Bài 15. Định lí Thalès trong tam giác.", "Bài 16. Đường trung bình của tam giác.", "Bài 17. Tính chất đường phân giác của tam giác.", "Ôn tập chương IV."
        ]},
        {"chapter_title": "CHƯƠNG V. DỮ LIỆU VÀ BIỂU ĐỒ.", "lessons": [
            "Bài 18. Thu thập và phân loại dữ liệu.", "Bài 19. Biểu diễn dữ liệu bằng bảng, biểu đồ.", "Bài 20. Phân tích số liệu thống kê dựa vào biểu đồ.", "Ôn tập chương V."
        ]},
        {"chapter_title": "CHƯƠNG VI. PHÂN THỨC ĐẠI SỐ.", "lessons": [
            "Bài 21. Phân thức đại số.", "Bài 22. Tính chất cơ bản của phân thức đại số.", "Bài 23. Phép cộng và phép trừ phân thức đại số.", "Bài 24. Phép nhân và phép chia phân thức đại số.", "Ôn tập chương VI."
        ]},
        {"chapter_title": "CHƯƠNG VII. PHƯƠNG TRÌNH BẬC NHẤT VÀ HÀM SỐ BẬC NHẤT.", "lessons": [
            "Bài 25. Phương trình bậc nhất một ẩn.", "Bài 26. Giải bài toán bằng cách lập phương trình.", "Bài 27. Khái niệm hàm số và đồ thị của hàm số.", "Bài 28. Hàm số bậc nhất và đồ thị của hàm số bậc nhất.", "Bài 29. Hệ số góc của đường thẳng.", "Ôn tập chương VII."
        ]},
        {"chapter_title": "CHƯƠNG VIII. MỞ ĐẦU VỀ TÍNH XÁC SUẤT CỦA BIẾN CỐ.", "lessons": [
            "Bài 30. Kết quả có thể và kết quả thuận lợi.", "Bài 31. Cách tính xác suất của biến cố bằng tỉ số.", "Bài 32. Mối liên hệ giữa xác suất thực nghiệm với xác suất và ứng dụng.", "Ôn tập chương VIII."
        ]},
        {"chapter_title": "CHƯƠNG IX. TAM GIÁC ĐỒNG DẠNG.", "lessons": [
            "Bài 33. Hai tam giác đồng dạng.", "Bài 34. Ba trường hợp đồng dạng của hai tam giác.", "Bài 35. Định lí Pythagore và ứng dụng.", "Bài 36. Các trường hợp đồng dạng của hai tam giác vuông.", "Bài 37. Hình đồng dạng.", "Ôn tập chương IX."
        ]},
        {"chapter_title": "CHƯƠNG X. MỘT SỐ HÌNH KHỐI TRONG THỰC TIỄN.", "lessons": [
            "Bài 38. Hình chóp tam giác đều.", "Bài 39. Hình chóp tứ giác đều.", "Ôn tập chương X.", "BÀI TẬP ÔN TẬP CUỐI NĂM."
        ]}
    ],
    "9": [
        {"chapter_title": "Chương I. PHƯƠNG TRÌNH VÀ HỆ HAI PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN.", "lessons": [
            "Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn.", "Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn.", "Luyện tập chung.", "Bài 3. Giải bài toán bằng cách lập hệ phương trình.", "Bài tập cuối chương I."
        ]},
        {"chapter_title": "Chương II. PHƯƠNG TRÌNH VÀ BẤT PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN.", "lessons": [
            "Bài 4. Phương trình quy về phương trình bậc nhất một ẩn.", "Bài 5. Bất đẳng thức và tính chất.", "Luyện tập chung.", "Bài 6. Bất phương trình bậc nhất một ẩn.", "Bài tập cuối chương II."
        ]},
        {"chapter_title": "Chương III. CĂN BẬC HAI VÀ CĂN BẬC BA.", "lessons": [
            "Bài 7. Căn bậc hai và căn thức bậc hai.", "Bài 8. Khai căn bậc hai với phép nhân và phép chia.", "Luyện tập chung.", "Bài 9. Biến đổi đơn giản và rút gọn biểu thức chứa căn thức bậc hai.", "Bài 10. Căn bậc ba và căn thức bậc ba.", "Luyện tập chung.", "Bài tập cuối chương III."
        ]},
        {"chapter_title": "Chương IV. HỆ THỨC LƯỢNG TRONG TAM GIÁC VUÔNG.", "lessons": [
            "Bài 11. Tỉ số lượng giác của góc nhọn.", "Bài 12. Một số hệ thức giữa cạnh, góc trong tam giác vuông và ứng dụng.", "Luyện tập chung.", "Bài tập cuối chương IV."
        ]},
        {"chapter_title": "Chương V. ĐƯỜNG TRÒN.", "lessons": [
            "Bài 13. Mở đầu về đường tròn.", "Bài 14. Cung và dây của một đường tròn.", "Bài 15. Độ dài của cung tròn. Diện tích hình quạt tròn và hình vành khuyên.", "Luyện tập chung.", "Bài 16. Vị trí tương đối của đường thẳng và đường tròn.", "Bài 17. Vị trí tương đối của hai đường tròn.", "Luyện tập chung.", "Bài tập cuối chương V."
        ]},
        {"chapter_title": "HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM (Tập 1).", "lessons": [
            "Pha chế dung dịch theo nồng độ yêu cầu.", "Tính chiều cao và xác định khoảng cách."
        ]},
        {"chapter_title": "Chương VI. HÀM SỐ y = ax2 (a khác 0). PHƯƠNG TRÌNH BẬC HAI MỘT ẨN.", "lessons": [
            "Bài 18. Hàm số y = ax2 (a ≠ 0).", "Bài 19. Phương trình bậc hai một ẩn.", "Luyện tập chung.", "Bài 20. Định lí Viète và ứng dụng.", "Bài 21. Giải bài toán bằng cách lập phương trình.", "Luyện tập chung.", "Bài tập cuối chương VI."
        ]},
        {"chapter_title": "Chương VII. TẦN SỐ VÀ TẦN SỐ TƯƠNG ĐỐI.", "lessons": [
            "Bài 22. Bảng tần số và biểu đồ tần số.", "Bài 23. Bảng tần số tương đối và biểu đồ tần số tương đối.", "Luyện tập chung.", "Bài 24. Bảng tần số, tần số tương đối ghép nhóm và biểu đồ.", "Bài tập cuối chương VII."
        ]},
        {"chapter_title": "Chương VIII. XÁC SUẤT CỦA BIẾN CỐ TRONG MỘT SỐ MÔ HÌNH XÁC SUẤT ĐƠN GIẢN.", "lessons": [
            "Bài 25. Phép thử ngẫu nhiên và không gian mẫu.", "Bài 26. Xác suất của biến cố liên quan tới phép thử.", "Luyện tập chung.", "Bài tập cuối chương VIII."
        ]},
        {"chapter_title": "Chương IX. ĐƯỜNG TRÒN NGOẠI TIẾP VÀ ĐƯỜNG TRÒN NỘI TIẾP.", "lessons": [
            "Bài 27. Góc nội tiếp.", "Bài 28. Đường tròn ngoại tiếp và đường tròn nội tiếp của một tam giác.", "Luyện tập chung.", "Bài 29. Tứ giác nội tiếp.", "Bài 30. Đa giác đều.", "Luyện tập chung.", "Bài tập cuối chương IX."
        ]},
        {"chapter_title": "Chương X. MỘT SỐ HÌNH KHỐI TRONG THỰC TIỄN.", "lessons": [
            "Bài 31. Hình trụ và hình nón.", "Bài 32. Hình cầu.", "Luyện tập chung.", "Bài tập cuối chương X."
        ]},
        {"chapter_title": "HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM (Tập 2).", "lessons": [
            "Giải phương trình, hệ phương trình và vẽ đồ thị hàm số với phần mềm GeoGebra.", "Vẽ hình đơn giản với phần mềm GeoGebra.", "Xác định tần số, tần số tương đối, vẽ các biểu đồ biểu diễn bảng tần số, tần số tướng đối bằng Excel.", "Gene trội trong các thế hệ lai."
        ]}
    ]
}


# -----------------------
# HỖ TRỢ LaTeX → ảnh
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
# Xuất DOCX / PDF
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
# HÀM GIÚP: Xử lý API
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

# --- TAB 1: TỔNG HỢP KIẾN THỨC (Cập nhật: chọn Chương/Bài từ mục lục) ---
with tab1:
    st.subheader("Tổng hợp kiến thức Toán theo Chương/Bài (dựa trên mục lục lớp 6-9)")
    col1, col2 = st.columns([1, 3])
    with col1:
        # lớp available from index_structure keys
        classes = sorted([f"Lớp {k}" for k in index_structure.keys()], key=lambda x: int(re.search(r'\d+', x).group()))
        classes = ["Tất cả lớp"] + classes
        lop_sel = st.selectbox("Chọn lớp:", classes, key="tab1_lop")

        # derive numeric class code if not "Tất cả lớp"
        sel_class_num = None
        if lop_sel != "Tất cả lớp":
            sel_class_num = re.search(r'\d+', lop_sel).group()

        # chapters list
        chapters_for_sel = []
        if sel_class_num:
            chapters_for_sel = index_structure.get(sel_class_num, [])
        else:
            # if all classes, combine chapters titles with class prefix
            combined = []
            for k in sorted(index_structure.keys(), key=lambda x: int(x)):
                for ch in index_structure[k]:
                    # Chỉ lấy tên chương và thêm tiền tố Lớp
                    title = ch['chapter_title'] if not ch['chapter_title'].startswith(f"(Lớp {k})") else ch['chapter_title']
                    combined.append({"chapter_title": f"(Lớp {k}) {title}", "lessons": [f"(Lớp {k}) {l}" for l in ch.get("lessons", [])]})
            chapters_for_sel = combined

        chapter_titles = ["Tất cả chương", "Toàn chương"]
        chapter_titles += [c["chapter_title"] for c in chapters_for_sel]
        chapter_sel = st.selectbox("Chọn chương:", chapter_titles, key="tab1_chapter")

        # lessons
        lessons = []
        if chapter_sel in ["Tất cả chương", "Toàn chương"]:
            # aggregate all lessons in class (or all classes)
            for c in chapters_for_sel:
                lessons.extend(c.get("lessons", []))
        else:
            # find selected chapter's lessons
            for c in chapters_for_sel:
                if c["chapter_title"] == chapter_sel:
                    lessons = c.get("lessons", [])
                    break
        lesson_options = ["Toàn bài"] + lessons if lessons else ["Toàn chương (không có bài chi tiết)"]
        lesson_sel = st.selectbox("Chọn bài (nếu muốn):", lesson_options, key="tab1_lesson")

    if st.button("🚀 Tổng hợp kiến thức", key="btn_tab1"):
        # build prompt based on selection
        if lop_sel == "Tất cả lớp":
            scope = "Toàn bộ chương trình Toán từ Lớp 6 đến Lớp 9 theo mục lục đã cung cấp."
        else:
            scope = f"Toán {lop_sel.replace('Lớp ','')}"
        if chapter_sel == "Tất cả chương":
            scope_detail = "Tổng hợp toàn bộ các chương của lớp được chọn, theo từng chương và từng bài (nêu mục tiêu, khái niệm, công thức với LaTeX $$...$$ và ví dụ minh họa)."
        elif chapter_sel == "Toàn chương":
            scope_detail = "Tổng hợp nội dung chi tiết cho toàn chương(s) đã chọn."
        else:
            # specific chapter selected
            if lesson_sel == "Toàn bài":
                scope_detail = f"Tổng hợp toàn bộ nội dung của {chapter_sel} (theo mục lục), phân chia Khái niệm – Công thức (LaTeX trong $$...$$) – Ví dụ cho từng bài."
            else:
                scope_detail = f"Tổng hợp chuyên sâu cho: {lesson_sel} (thuộc {chapter_sel}), cấu trúc: Khái niệm – Công thức (LaTeX trong $$...$$) – Ví dụ, câu hỏi luyện tập và hướng dẫn giải ngắn."

        prompt = f"""
Bạn là giáo viên Toán có kinh nghiệm. Hãy { 'soạn tài liệu' if 'Tổng hợp' in scope_detail else 'tổng hợp' } {scope}.
Yêu cầu:
- PHẠM VI: {scope_detail}
- PHÂN NHÓM nội dung (nếu phù hợp): Số học, Đại số, Hình học, Thống kê.
- CẤU TRÚC: Mỗi mục/bài trình bày theo: Mục tiêu (Kiến thức, Năng lực, Phẩm chất) – Khái niệm – Công thức (viết bằng LaTeX trong $$...$$ nếu có) – Ví dụ minh họa – Bài tập luyện tập (kèm đáp án tóm tắt).
- Trình bày rõ ràng, phù hợp để in ấn, có tiêu đề và đánh số chương/bài.
- Ngôn ngữ: tiếng Việt chuẩn, phù hợp học sinh trung học cơ sở.
- Nếu nội dung có thể minh họa bằng hình/hệ quả, hãy ghi chú chỗ cần hình (ví dụ: [Chèn hình: Hình tam giác vuông]).
Trả về kết quả dưới dạng văn bản dễ copy/paste.
        """
        with st.spinner("Đang tổng hợp..."):
            res = generate_with_gemini(api_key, prompt)
            if res["ok"]:
                st.session_state["summary_text"] = res["text"]
            else:
                st.error(res["message"])

    # hiển thị và nút tải về
    if "summary_text" in st.session_state:
        st.markdown(st.session_state["summary_text"].replace("\n", "<br>"), unsafe_allow_html=True)
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
        # Make filename safe
        safe_name = re.sub(r'[\\/*?:"<>|]',"_", ga_bai)
        st.download_button("📥 Tải Giáo án (DOCX)", docx_ga, f"GiaoAn_{safe_name}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

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
