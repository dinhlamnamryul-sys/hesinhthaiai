import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import random

st.set_page_config(page_title="Tạo đề kiểm tra tự động", page_icon="📝", layout="wide")
st.title("📝 Tạo đề kiểm tra theo Chương – Bài – Chủ đề (Lớp 6 → 9)")

# ============================================================================================
# 🟦 1) DỮ LIỆU CHƯƠNG – BÀI – CHỦ ĐỀ (BẠN DÁN FULL DATA CŨ CỦA BẠN VÀO ĐÂY)
# ============================================================================================

full_data = [
    # DỮ LIỆU MẪU – BẠN ĐỔI THÀNH FULL DATA BẠN ĐÃ GỬI TRƯỚC ĐÓ
    ["Toán 6", "Chương 1", "Bài 1", "Tập hợp số tự nhiên"],
    ["Toán 6", "Chương 1", "Bài 2", "Ước và bội"],
    ["Toán 6", "Chương 2", "Bài 3", "Số nguyên"],
    ["Toán 6", "Chương 2", "Bài 4", "Phép cộng trừ số nguyên"],

    ["Toán 7", "Chương 1", "Bài 1", "Số hữu tỉ"],
    ["Toán 7", "Chương 1", "Bài 2", "Tỉ lệ thức"],
    ["Toán 7", "Chương 2", "Bài 3", "Biểu đồ"],
    ["Toán 7", "Chương 2", "Bài 4", "Hình học cơ bản"],

    ["Toán 8", "Chương 1", "Bài 1", "Phép nhân đa thức"],
    ["Toán 8", "Chương 1", "Bài 2", "Hằng đẳng thức"],
    ["Toán 8", "Chương 2", "Bài 3", "Phân thức đại số"],
    ["Toán 8", "Chương 2", "Bài 4", "Phương trình bậc nhất"],

    ["Toán 9", "Chương 1", "Bài 1", "Căn bậc hai"],
    ["Toán 9", "Chương 1", "Bài 2", "Hàm số bậc nhất"],
    ["Toán 9", "Chương 2", "Bài 3", "Hàm số bậc hai"],
    ["Toán 9", "Chương 2", "Bài 4", "Hệ phương trình"],
]

df = pd.DataFrame(full_data, columns=["Mon", "Chuong", "Bai", "ChuDe"])

# ============================================================================================
# 🟦 2) GIAO DIỆN LỌC LỚP – CHƯƠNG – BÀI – CHỦ ĐỀ
# ============================================================================================

st.subheader("🎯 Chọn nội dung để tạo đề")

lop = st.selectbox("Chọn lớp:", ["6", "7", "8", "9"])
mon_chon = f"Toán {lop}"

df_mon = df[df["Mon"] == mon_chon]

chuong_list = sorted(df_mon["Chuong"].unique())
chuong_chon = st.multiselect("Chọn Chương:", chuong_list, default=chuong_list)

df_chuong = df_mon[df_mon["Chuong"].isin(chuong_chon)]

bai_list = sorted(df_chuong["Bai"].unique())
bai_chon = st.multiselect("Chọn Bài:", bai_list, default=bai_list)

df_bai = df_chuong[df_chuong["Bai"].isin(bai_chon)]

chu_de_list = sorted(df_bai["ChuDe"].unique())
chu_de_chon = st.multiselect("Chọn Chủ đề:", chu_de_list, default=chu_de_list)

df_selected = df_bai[df_bai["ChuDe"].isin(chu_de_chon)]

st.success(f"Đã chọn **{len(df_selected)}** mục nội dung.")

# ============================================================================================
# 🟦 3) HÀM TẠO BỘ CÂU HỎI THEO ĐÚNG CẤU HÌNH 10 ĐIỂM
# ============================================================================================

def tao_cau_hoi(df):
    questions = {
        "mcq": [],
        "true_false": [],
        "short": [],
        "essay": []
    }

    # --- 12 câu trắc nghiệm 0.25 điểm ---
    for i in range(12):
        row = df.sample(1).iloc[0]
        questions["mcq"].append({
            "cau": f"Câu {i+1}: Câu hỏi trắc nghiệm về: {row['ChuDe']}",
            "a": "A. Phương án A",
            "b": "B. Phương án B",
            "c": "C. Phương án C",
            "d": "D. Phương án D",
            "diem": 0.25
        })

    # --- 2 câu đúng sai – mỗi câu 4 ý ---
    for i in range(2):
        row = df.sample(1).iloc[0]
        questions["true_false"].append({
            "cau": f"Câu {12 + i + 1}: Đúng/Sai về: {row['ChuDe']}",
            "items": [
                "a) ......... (Đ/S)",
                "b) ......... (Đ/S)",
                "c) ......... (Đ/S)",
                "d) ......... (Đ/S)"
            ],
            "diem": 1
        })

    # --- 4 câu trả lời ngắn 0.5 điểm ---
    for i in range(4):
        row = df.sample(1).iloc[0]
        questions["short"].append({
            "cau": f"Câu {14 + i + 1}: Trả lời ngắn về: {row['ChuDe']}",
            "diem": 0.5
        })

    # --- 3 câu tự luận 1 điểm ---
    for i in range(3):
        row = df.sample(1).iloc[0]
        questions["essay"].append({
            "cau": f"Câu {18 + i + 1}: Tự luận về: {row['ChuDe']}",
            "diem": 1
        })

    return questions

# ============================================================================================
# 🟦 4) HÀM XUẤT WORD
# ============================================================================================

def xuat_word(questions):
    doc = Document()
    doc.add_heading("ĐỀ KIỂM TRA", level=1)

    # --- TRẮC NGHIỆM ---
    doc.add_heading("I. TRẮC NGHIỆM (3 điểm)", level=2)
    for q in questions["mcq"]:
        doc.add_paragraph(q["cau"])
        doc.add_paragraph(q["a"])
        doc.add_paragraph(q["b"])
        doc.add_paragraph(q["c"])
        doc.add_paragraph(q["d"])
        doc.add_paragraph("")

    # --- ĐÚNG SAI ---
    doc.add_heading("II. ĐÚNG – SAI (2 điểm)", level=2)
    for q in questions["true_false"]:
        doc.add_paragraph(q["cau"])
        for item in q["items"]:
            doc.add_paragraph("   " + item)
        doc.add_paragraph("")

    # --- TRẢ LỜI NGẮN ---
    doc.add_heading("III. TRẢ LỜI NGẮN (2 điểm)", level=2)
    for q in questions["short"]:
        doc.add_paragraph(q["cau"])
        doc.add_paragraph("   ....................................................")
        doc.add_paragraph("")

    # --- TỰ LUẬN ---
    doc.add_heading("IV. TỰ LUẬN (3 điểm)", level=2)
    for q in questions["essay"]:
        doc.add_paragraph(q["cau"])
        doc.add_paragraph("   .......................................................................")
        doc.add_paragraph("")
        doc.add_paragraph("   .......................................................................")
        doc.add_paragraph("")

    # Xuất ra BytesIO
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ============================================================================================
# 🟦 5) NÚT TẠO ĐỀ
# ============================================================================================

if st.button("📄 Tạo đề kiểm tra"):
    if len(df_selected) == 0:
        st.error("⚠ Bạn chưa chọn nội dung!")
    else:
        questions = tao_cau_hoi(df_selected)
        file = xuat_word(questions)

        st.download_button(
            label="⬇ Tải xuống file Word",
            data=file,
            file_name="De_kiem_tra.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        st.success("✅ Đã tạo xong đề kiểm tra!")
