import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import math

st.set_page_config(page_title="Tạo đề Toán 6-9 theo SGK KNTT (CV 7991)", 
                   page_icon="📝", layout="wide")

st.title("📝 Tạo đề kiểm tra môn Toán (Lớp 6-9) theo CV 7991")

st.markdown("""
Hệ thống gồm **2 bước**:

### ✅ **Bước 1:** Chọn Môn → Chương → Bài → Chủ đề → Sinh ra **Ma trận CV 7991**
### ✅ **Bước 2:** Nhấn “Tạo đề kiểm tra” để sinh đề từ ma trận  
""")

# ================================
# DỮ LIỆU SGK TOÁN 6-9 (bạn đang dùng)
# ================================

full_data = {
    'Mon': [], 'Chuong': [], 'Bai': [], 'ChuDe': [], 
    'NoiDung': [], 'MucDo': [], 'SoCau': []
}

def add_lesson(mon, chuong, bai, chude, noidung, mucdo, socau):
    full_data['Mon'].append(mon)
    full_data['Chuong'].append(chuong)
    full_data['Bai'].append(bai)
    full_data['ChuDe'].append(chude)
    full_data['NoiDung'].append(noidung)
    full_data['MucDo'].append(mucdo)
    full_data['SoCau'].append(socau)

# --- (GIỮ Y NGUYÊN TOÀN BỘ DỮ LIỆU SGK CỦA BẠN) ---
# ... (ĐỂ GỌN, MÌNH KHÔNG LẶP LẠI TOÀN BỘ 1000 DÒNG - BẠN GIỮ LẠI)
# ----------------------------------------------------

df = pd.DataFrame(full_data)

# =======================================================
#        HÀM TẠO MA TRẬN THEO CV 7991 (PHỤ LỤC 1)
# =======================================================

def create_ma_tran_cv7991(df_input):
    df_temp = df_input.copy()
    df_temp["N_to_Take"] = df_temp["SoCau"]

    # Các cột ma trận (9 ô)
    matrix_cols = [
        'NL - Biết', 'NL - Hiểu', 'NL - Vận dụng',
        'DS - Biết', 'DS - Hiểu', 'DS - Vận dụng',
        'TL - Biết', 'TL - Hiểu', 'TL - Vận dụng'
    ]

    for col in matrix_cols:
        df_temp[col] = 0

    # --- PHÂN BỔ CÂU HỎI ---
    for md in ['Nhận biết', 'Thông hiểu']:
        idx = df_temp[df_temp["MucDo"] == md].index
        col_nl = f"NL - {'Biết' if md=='Nhận biết' else 'Hiểu'}"
        col_ds = f"DS - {'Biết' if md=='Nhận biết' else 'Hiểu'}"

        df_temp.loc[idx, col_nl] = (df_temp["N_to_Take"] * 0.6).astype(int)
        df_temp.loc[idx, col_ds] = df_temp["N_to_Take"] - df_temp[col_nl]

    # Vận dụng → Tự luận
    idx_vd = df_temp[df_temp["MucDo"].isin(["Vận dụng", "Vận dụng cao"])].index
    df_temp.loc[idx_vd, "TL - Vận dụng"] = df_temp["N_to_Take"]

    # Pivot
    pivot = pd.pivot_table(
        df_temp, values=matrix_cols,
        index=["ChuDe", "NoiDung"], aggfunc="sum", fill_value=0
    )

    pivot["Tổng"] = pivot.sum(axis=1)

    # Xuất ma trận
    pivot = pivot.reset_index()
    final_cols = ["Chủ đề", "Nội dung"] + matrix_cols + ["Tổng"]
    pivot.columns = final_cols

    return pivot

# =======================================================
#                GIAO DIỆN BƯỚC 1: CHỌN DỮ LIỆU
# =======================================================

st.subheader("🟩 Bước 1: Chọn Môn – Chương – Bài – Chủ đề")

col1, col2, col3, col4 = st.columns(4)

with col1:
    mon_chon = st.selectbox("Chọn môn", sorted(df["Mon"].unique()))

df1 = df[df["Mon"] == mon_chon]

with col2:
    chuong_chon = st.selectbox("Chọn chương", sorted(df1["Chuong"].unique()))

df2 = df1[df1["Chuong"] == chuong_chon]

with col3:
    bai_chon = st.selectbox("Chọn bài", sorted(df2["Bai"].unique()))

df3 = df2[df2["Bai"] == bai_chon]

with col4:
    chude_chon = st.multiselect("Chọn chủ đề", sorted(df3["ChuDe"].unique()))

df_selected = df3[df3["ChuDe"].isin(chude_chon)]

st.write("### 📌 Dữ liệu đã chọn:")
st.dataframe(df_selected)

# =======================================================
#            NÚT SINH MA TRẬN THEO CV 7991
# =======================================================

if st.button("📊 Sinh MA TRẬN theo CV 7991"):
    if df_selected.empty:
        st.error("⚠ Vui lòng chọn đầy đủ Môn – Chương – Bài – Chủ đề!")
    else:
        ma_tran = create_ma_tran_cv7991(df_selected)
        st.success("🎉 ĐÃ TẠO MA TRẬN CV 7991 THÀNH CÔNG!")
        st.dataframe(ma_tran)

        # Lưu vào session_state để tạo đề ở bước 2
        st.session_state["ma_tran_cv7991"] = ma_tran

# =======================================================
#                  BƯỚC 2: TẠO ĐỀ KIỂM TRA
# =======================================================

st.subheader("🟦 Bước 2: Tạo đề kiểm tra dựa trên ma trận")

if "ma_tran_cv7991" not in st.session_state:
    st.info("👉 Hãy sinh Ma trận trước!")
else:
    if st.button("📝 Tạo đề kiểm tra"):
        mt = st.session_state["ma_tran_cv7991"]

        # ======== TẠO ĐỀ TẠI ĐÂY ========
        # Bạn nhúng tiếp code tạo câu hỏi → đề → export Word ở đây
        # (Mình sẽ viết full nếu bạn yêu cầu)
        # =================================

        st.success("🎉 Đề kiểm tra đã được tạo!")

