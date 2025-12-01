# pages/6_Danh_Gia_Thong_Tu_22.py
import streamlit as st
import pandas as pd
import io
import base64

st.set_page_config(page_title="Đánh giá theo Thông tư 22", layout="wide")

st.title("📝 Trang Giáo Viên — Đánh giá tự động (theo Thông tư 22)")

st.markdown("""
Hướng dẫn: Tải lên file Excel mẫu của lớp. Chọn cột chứa tên học sinh, chọn các cột điểm (miệng/15p/1tiết/CK hoặc cột năng lực, phẩm chất).
Bạn có thể đặt trọng số cho từng cột, chọn phương pháp tổng hợp, sau đó nhấn 'Chấm tự động' → file Excel có thêm cột kết quả sẽ được tạo và có thể tải về.
""")

uploaded_file = st.file_uploader("1) Tải file Excel lên (xlsx hoặc xls)", type=["xlsx", "xls"])
if not uploaded_file:
    st.info("Vui lòng tải lên một file Excel để bắt đầu.")
    st.stop()

# Đọc file Excel (lấy sheet đầu tiên)
try:
    df = pd.read_excel(uploaded_file, sheet_name=0)
except Exception as e:
    st.error(f"Lỗi khi đọc file Excel: {e}")
    st.stop()

st.subheader("2) Xem trước dữ liệu (vài hàng đầu tiên)")
st.dataframe(df.head(10))

# Bắt tên cột
cols = df.columns.tolist()

st.subheader("3) Chọn cột")
name_col = st.selectbox("Chọn cột 'Tên học sinh' / mã HS", options=cols, index=0)
# Chọn cột điểm (có thể nhiều cột)
score_cols = st.multiselect("Chọn các cột 'điểm' (miệng/15p/1 tiết/CK hoặc các cột mức độ)", options=cols)

if len(score_cols) == 0:
    st.warning("Bạn cần chọn ít nhất 1 cột điểm để tính toán.")
    st.stop()

# Nếu có cột dạng text (Tốt/Đạt/Chưa), cho phép map sang số
st.subheader("4) Xử lý cột dạng văn bản (nếu có)")
text_cols = st.multiselect("Trường hợp có cột dạng văn bản (ví dụ: 'Tốt','Đạt',...), chọn các cột đó để map sang số (tùy chọn)", options=score_cols)
mapping_info = {}
if len(text_cols) > 0:
    st.write("Định nghĩa mapping cho các giá trị văn bản sang số (giá trị số dùng trong tính trung bình).")
    # Hiển thị 1 bảng mapping mặc định, cho phép giáo viên chỉnh
    # Mặc định: Tốt=9, Khá=7.5, Đạt=5.5, Chưa đạt=3 (giáo viên có thể sửa)
    default_map = {"Tốt": 9.0, "Khá": 7.5, "Đạt": 5.5, "Chưa đạt": 3.0}
    for col in text_cols:
        st.markdown(f"**Mapping cho cột:** `{col}`")
        # show text input for keys & values as comma separated pairs
        txt = st.text_area(f"Nhập mapping cho `{col}` (định dạng: GiáTrị=Điểm, ngăn cách bởi dấu phẩy). Ví dụ: Tốt=9,Khá=7.5,Đạt=5.5,Chưa đạt=3", value=", ".join([f"{k}={v}" for k, v in default_map.items()]))
        # parse
        mp = {}
        try:
            parts = [p.strip() for p in txt.split(",") if p.strip()]
            for p in parts:
                if "=" in p:
                    k, v = p.split("=", 1)
                    mp[k.strip()] = float(v.strip())
        except Exception:
            st.error("Sai định dạng mapping. Hãy nhập lại theo dạng Tốt=9,Khá=7.5,...")
        mapping_info[col] = mp

# 5) Trọng số
st.subheader("5) Đặt trọng số cho các cột điểm (nếu để trống => trọng số đều nhau)")
weights = {}
if len(score_cols) > 0:
    st.write("Nhập trọng số tương ứng cho từng cột (tổng không nhất thiết phải là 1; hệ thống sẽ chuẩn hoá).")
    cols_layout = st.columns(2)
    for i, c in enumerate(score_cols):
        default = 1.0
        weights[c] = cols_layout[i % 2].number_input(f"Trọng số cho `{c}`", min_value=0.0, value=float(default), step=0.1, key=f"w_{c}")

# Chọn phương pháp tổng hợp
st.subheader("6) Chọn phương pháp tổng hợp điểm")
method = st.selectbox("Phương pháp", options=["Trung bình (mean)", "Trọng số (weighted)", "Trung vị (median)"], index=0)

# 7) Ngưỡng xếp loại (mặc định, giáo viên có thể điều chỉnh)
st.subheader("7) Cấu hình ngưỡng xếp loại (có thể điều chỉnh để phù hợp Thông tư 22)")
st.write("Các ngưỡng dưới là mặc định. Bạn có thể điều chỉnh để phù hợp quy định/trường bạn.")
col1, col2, col3 = st.columns(3)
giỏi_min = col1.number_input("Giỏi >= ", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
khá_min = col2.number_input("Khá >= ", min_value=0.0, max_value=10.0, value=6.5, step=0.1)
đạt_min = col3.number_input("Đạt >= ", min_value=0.0, max_value=10.0, value=5.0, step=0.1)

# 8) Nhận xét tự động
st.subheader("8) Mẫu nhận xét (sử dụng {ten}, {diem}, {xeploai})")
default_comment = "Học sinh {ten} đạt điểm {diem:.2f} — Xếp loại: {xeploai}."
comment_template = st.text_area("Mẫu nhận xét", value=default_comment, height=80)

# Nút thực hiện chấm
if st.button("🔍 Chấm tự động theo cấu hình trên"):
    # Copy dataframe
    df_proc = df.copy()

    # Map text columns if có
    for col in text_cols:
        mp = mapping_info.get(col, {})
        # apply mapping: if value in mp keys -> mapped value; else try convert to float; else NaN
        def map_val(v):
            if pd.isna(v):
                return pd.NA
            if isinstance(v, (int, float)):
                return float(v)
            s = str(v).strip()
            if s in mp:
                return mp[s]
            # try convert
            try:
                return float(s)
            except:
                return pd.NA
        df_proc[col + "_mapped_temp"] = df_proc[col].apply(map_val)
        # replace column in score_cols with mapped version
        # We'll use the new name for processing
        score_cols = [col + "_mapped_temp" if sc == col else sc for sc in score_cols]

    # Ensure numeric for score columns
    for sc in score_cols:
        df_proc[sc + "_numeric"] = pd.to_numeric(df_proc[sc], errors='coerce')
    numeric_cols = [sc + "_numeric" for sc in score_cols]

    # Build weight vector (normalize)
    w_vals = [weights.get(sc, 1.0) for sc in score_cols]
    # if all zero, set equal
    if sum(w_vals) == 0:
        w_vals = [1.0] * len(w_vals)
    # normalize
    total_w = sum(w_vals)
    norm_w = [w / total_w for w in w_vals]

    # Compute aggregated score
    import numpy as np

    def compute_row(row):
        vals = []
        for nc in numeric_cols:
            v = row.get(nc, None)
            if pd.isna(v):
                vals.append(np.nan)
            else:
                vals.append(float(v))
        vals = np.array(vals, dtype=float)
        if method == "Trung bình (mean)":
            return float(np.nanmean(vals)) if len(vals) > 0 else float("nan")
        elif method == "Trọng số (weighted)":
            # apply normalized weights; ignore NaN by renormalizing weights for present values
            mask = ~np.isnan(vals)
            if mask.sum() == 0:
                return float("nan")
            w_present = np.array(norm_w)[mask]
            w_present = w_present / w_present.sum()
            return float(np.nansum(vals[mask] * w_present))
        elif method == "Trung vị (median)":
            return float(np.nanmedian(vals)) if len(vals) > 0 else float("nan")
        else:
            return float(np.nanmean(vals))

    df_proc["Điểm_trung_bình"] = df_proc.apply(compute_row, axis=1)

    # Xếp loại theo ngưỡng
    def xep_loai(d):
        try:
            if pd.isna(d):
                return "Chưa có điểm"
            d = float(d)
            if d >= giỏi_min:
                return "Giỏi"
            elif d >= khá_min:
                return "Khá"
            elif d >= đạt_min:
                return "Đạt"
            else:
                return "Chưa đạt"
        except:
            return "Chưa có điểm"

    df_proc["Xếp_loại"] = df_proc["Điểm_trung_bình"].apply(xep_loai)

    # Nhận xét
    def make_comment(row):
        ten = row.get(name_col, "")
        diem = row.get("Điểm_trung_bình", float("nan"))
        xeploai = row.get("Xếp_loại", "")
        try:
            return comment_template.format(ten=ten, diem=diem, xeploai=xeploai)
        except Exception:
            return f"{ten} - {xeploai} - {diem}"

    df_proc["Nhận_xét"] = df_proc.apply(make_comment, axis=1)

    # Hiển thị kết quả tóm tắt
    st.success("Hoàn tất chấm tự động ✅")
    st.subheader("Một vài kết quả đầu")
    st.dataframe(df_proc[[name_col, "Điểm_trung_bình", "Xếp_loại", "Nhận_xét"]].head(20))

    # Chuẩn bị file excel để tải: lưu sheet gốc + sheet kết quả
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        try:
            # Ghi sheet gốc (tên: "Dữ liệu gốc")
            df.to_excel(writer, index=False, sheet_name="Dữ liệu gốc")
        except Exception:
            pass
        # Ghi sheet kết quả
        df_proc.to_excel(writer, index=False, sheet_name="Kết quả_đánh_giá")
        writer.save()
    processed_data = output.getvalue()

    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Ketqua_DanhGia_ThongTu22.xlsx">⬇ Tải file kết quả (Excel)</a>'
    st.markdown(href, unsafe_allow_html=True)

    # CUNG CẤP CSV nếu cần
    csv = df_proc.to_csv(index=False).encode('utf-8')
    st.download_button("Tải CSV kết quả", data=csv, file_name="Ketqua_DanhGia_ThongTu22.csv", mime="text/csv")

else:
    st.info("Nhấn 'Chấm tự động' để hệ thống tính toán và tạo file kết quả.")
