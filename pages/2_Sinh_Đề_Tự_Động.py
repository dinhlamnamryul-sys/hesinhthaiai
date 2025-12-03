import streamlit as st
import time
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from google import genai
from google.genai.types import Tool
import random

# -----------------------------------------------------------
# 1. DỮ LIỆU CHƯƠNG TRÌNH TOÁN LỚP 6 → 9 (KẾT NỐI TRI THỨC)
# -----------------------------------------------------------

CHUONG_TRINH = {
    "Toán 6": {
        "Tập 1": {
            "Chương 1 – Số tự nhiên": [
                "Bài 1: Tập hợp - Phần tử của tập hợp",
                "Bài 2: Số tự nhiên",
                "Bài 3: Phân tích một số ra thừa số",
                "Bài 4: Bảng chia và bội số",
                "Bài 5: Ước chung – Bội chung",
                "Bài 6: Số nguyên tố – Hợp số",
                "Bài 7: Phép chia hết – phép chia có dư"
            ],
            "Chương 2 – Số nguyên": [
                "Bài 1: Ôn tập số nguyên",
                "Bài 2: Phép cộng số nguyên",
                "Bài 3: Phép trừ số nguyên",
                "Bài 4: Phép nhân số nguyên",
                "Bài 5: Phép chia số nguyên"
            ],
            "Chương 3 – Hình học trực quan": [
                "Bài 1: Điểm – Đoạn thẳng",
                "Bài 2: Góc",
                "Bài 3: Đường thẳng – Tia"
            ]
        },
        "Tập 2": {
            "Chương 4 – Phân số": [
                "Bài 1: Phân số",
                "Bài 2: Tính chất phân số",
                "Bài 3: So sánh phân số",
                "Bài 4: Phép cộng phân số",
                "Bài 5: Phép trừ phân số",
                "Bài 6: Phép nhân phân số",
                "Bài 7: Phép chia phân số"
            ],
            "Chương 5 – Số thập phân": [
                "Bài 1: Số thập phân",
                "Bài 2: Phép tính với số thập phân",
                "Bài 3: Làm tròn số",
                "Bài 4: Đo độ dài – Khối lượng – Diện tích"
            ],
            "Chương 6 – Tỉ lệ": [
                "Bài 1: Tỉ số – Tỉ lệ",
                "Bài 2: Tỉ lệ thức",
                "Bài 3: Số phần trăm"
            ]
        }
    },

    # ---------------------------------------------------------
    # TOÁN 7
    # ---------------------------------------------------------
    "Toán 7": {
        "Tập 1": {
            "Chương 1 – Số hữu tỉ – Số thực": [
                "Bài 1: Số hữu tỉ",
                "Bài 2: Tính chất số hữu tỉ",
                "Bài 3: Giá trị tuyệt đối",
                "Bài 4: Số thực"
            ],
            "Chương 2 – Hàm số và đồ thị": [
                "Bài 1: Đại lượng tỉ lệ thuận",
                "Bài 2: Đại lượng tỉ lệ nghịch",
                "Bài 3: Hàm số – đồ thị"
            ],
            "Chương 3 – Hình học phẳng": [
                "Bài 1: Góc tạo bởi tia tiếp tuyến",
                "Bài 2: Tam giác",
                "Bài 3: Quan hệ cạnh – góc tam giác"
            ]
        },
        "Tập 2": {
            "Chương 4 – Số đại số": [
                "Bài 1: Lũy thừa",
                "Bài 2: Biến đổi biểu thức",
                "Bài 3: Tỉ lệ thức và ứng dụng"
            ],
            "Chương 5 – Thống kê": [
                "Bài 1: Thu thập và mô tả dữ liệu",
                "Bài 2: Biểu đồ",
                "Bài 3: Số trung bình cộng"
            ]
        }
    },

    # ---------------------------------------------------------
    # TOÁN 8
    # ---------------------------------------------------------
    "Toán 8": {
        "Tập 1": {
            "Chương 1 – Phép nhân và phép chia đa thức": [
                "Bài 1: Nhân đơn thức với đa thức",
                "Bài 2: Nhân đa thức với đa thức",
                "Bài 3: Hằng đẳng thức đáng nhớ",
                "Bài 4: Chia đơn thức – chia đa thức"
            ],
            "Chương 2 – Phân thức đại số": [
                "Bài 1: Phân thức",
                "Bài 2: Tính chất phân thức",
                "Bài 3: Rút gọn phân thức",
                "Bài 4: Quy đồng phân thức"
            ],
            "Chương 3 – Tam giác đồng dạng": [
                "Bài 1: Định nghĩa tam giác đồng dạng",
                "Bài 2: Các trường hợp đồng dạng",
                "Bài 3: Ứng dụng đồng dạng"
            ]
        },
        "Tập 2": {
            "Chương 4 – Phương trình bậc nhất": [
                "Bài 1: Phương trình một ẩn",
                "Bài 2: Giải phương trình bậc nhất",
                "Bài 3: Dạng toán giải phương trình"
            ],
            "Chương 5 – Tứ giác": [
                "Bài 1: Hình thang",
                "Bài 2: Hình chữ nhật",
                "Bài 3: Hình thoi – hình vuông",
                "Bài 4: Đa giác"
            ]
        }
    },

    # ---------------------------------------------------------
    # TOÁN 9
    # ---------------------------------------------------------
    "Toán 9": {
        "Tập 1": {
            "Chương 1 – Căn bậc hai – Căn bậc ba": [
                "Bài 1: Căn bậc hai",
                "Bài 2: Căn thức",
                "Bài 3: Biến đổi biểu thức chứa căn",
                "Bài 4: Căn bậc ba"
            ],
            "Chương 2 – Hàm số bậc nhất": [
                "Bài 1: Hàm số bậc nhất",
                "Bài 2: Đồ thị hàm số",
                "Bài 3: Tính chất đồ thị"
            ]
        },
        "Tập 2": {
            "Chương 3 – Hệ phương trình": [
                "Bài 1: Hệ phương trình hai ẩn",
                "Bài 2: Phương pháp thế",
                "Bài 3: Phương pháp cộng"
            ],
            "Chương 4 – Hình học": [
                "Bài 1: Đường tròn",
                "Bài 2: Tiếp tuyến",
                "Bài 3: Góc và cung"
            ]
        }
    }
}

# -----------------------------------------------------------
# 2. KHỞI TẠO GEMINI
# -----------------------------------------------------------

client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY", ""))

tool_markdown = Tool.from_yaml("""
type: api
api:
  openapi: googleapis/googleapis/google/generativeai/v1/generative_models.yaml
  operationId: google.ai.generativelanguage.v1.GenerativeModels.GenerateContent
""")

# -----------------------------------------------------------
# 3. HÀM GỌI AI SINH CÂU HỎI
# -----------------------------------------------------------

def goi_ai_sinh_cauhoi(noidung, so_cau, lop, tap, chuong, bai):
    prompt = f"""
Bạn là giáo viên Toán. Hãy sinh bộ {so_cau} câu hỏi theo bài học sau:

- Khối lớp: {lop}
- Tập: {tap}
- Chương: {chuong}
- Bài: {bai}

Yêu cầu:
- Mỗi câu có đáp án A,B,C,D
- Nội dung phù hợp sách Kết nối tri thức
- Không giải thích, chỉ đưa câu + đáp án
- Định dạng:

Câu 1: ...
A. ...
B. ...
C. ...
D. ...
Đáp án: ...

=== Nội dung trọng tâm bài ===
{noidung}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        tools=[tool_markdown]
    )
    return response.text

# -----------------------------------------------------------
# 4. HÀM TẠO PDF
# -----------------------------------------------------------

def tao_file_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    x = 2 * cm
    y = height - 2 * cm

    c.setFont("Helvetica", 12)

    for line in text.split("\n"):
        c.drawString(x, y, line)
        y -= 20
        if y < 2 * cm:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 2 * cm

    c.save()
    buffer.seek(0)
    return buffer

# -----------------------------------------------------------
# 5. GIAO DIỆN STREAMLIT
# -----------------------------------------------------------

st.title("📘 SINH ĐỀ TOÁN 6–9 (Kết nối tri thức)")

lop = st.selectbox("Chọn khối lớp:", list(CHUONG_TRINH.keys()))
tap = st.selectbox("Chọn Tập:", list(CHUONG_TRINH[lop].keys()))
chuong = st.selectbox("Chọn Chương:", list(CHUONG_TRINH[lop][tap].keys()))
bai = st.selectbox("Chọn Bài:", CHUONG_TRINH[lop][tap][chuong])

so_cau = st.number_input("Số câu muốn sinh:", 1, 50, 10)
noidung = st.text_area("Nội dung trọng tâm bài (tùy chọn):", "")

if st.button("✨ Sinh đề"):
    st.info("⏳ Đang sinh câu hỏi, vui lòng đợi...")

    try:
        ketqua = goi_ai_sinh_cauhoi(noidung, so_cau, lop, tap, chuong, bai)
        st.success("✔ Hoàn thành!")
        st.text_area("📄 Đề được sinh:", ketqua, height=400)

        pdf_file = tao_file_pdf(ketqua)
        st.download_button("📥 Tải file PDF", pdf_file, "de_toan.pdf")
    except Exception as e:
        st.error(f"Lỗi: {e}")

