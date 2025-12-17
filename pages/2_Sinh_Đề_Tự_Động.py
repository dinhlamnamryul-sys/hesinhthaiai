import requests
import streamlit as st
from datetime import datetime
import base64
from io import BytesIO

# ===============================
# 🔑 NHẬP GOOGLE API KEY
# ===============================

with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key để dùng ứng dụng:

1. Truy cập: **https://aistudio.google.com/app/apikey**
2. Đăng nhập Gmail.
3. Nhấn **Create API key**.
4. Copy API Key.
5. Dán vào ô bên dưới.

⚠️ Không chia sẻ API Key cho người khác.
""")

st.subheader("🔐 Nhập Google API Key:")
api_key = st.text_input("Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Nhập API Key để tiếp tục.")
else:
    st.success("✅ API Key hợp lệ!")


# ===============================
# 📌 HÀM GỌI GEMINI (GIỮ NGUYÊN)
# ===============================
def analyze_real_image(api_key, image, prompt):
    pass 

# ===============================
# 📚 DỮ LIỆU CHƯƠNG TRÌNH HỌC (GIỮ NGUYÊN)
# ===============================
# --- MOCK DATA (Dữ liệu giả lập) ---
chuong_options_lop = {
    "Lớp 6": ["Chương I", "Chương II"], "Lớp 7": ["Chương I"], 
    "Lớp 8": ["Chương I: Đa thức", "Chương II: Hằng đẳng thức"], "Lớp 9": ["Chương I"]
}
bai_options_lop = {
    "Lớp 6": {"Chương I": ["Bài 1"]}, "Lớp 7": {"Chương I": ["Bài 1"]},
    "Lớp 8": {"Chương I: Đa thức": ["Bài 1", "Bài 2"], "Chương II: Hằng đẳng thức": ["Bài 6", "Bài 7"]},
    "Lớp 9": {"Chương I": ["Bài 1"]}
}

# ===============================
# 🎛️ SIDEBAR (CHỈ GIỮ LẠI CHỌN BÀI HỌC)
# ===============================

with st.sidebar:
    st.header("1. Thông tin sinh đề")
    lop = st.selectbox("Chọn lớp", ["Lớp 6","Lớp 7","Lớp 8","Lớp 9"], index=2)
    
    chuong_options = chuong_options_lop.get(lop, [])
    chuong = st.multiselect("Chọn chương", chuong_options)
    
    bai_list_all = []
    for c in chuong:
        bai_list_all.extend(bai_options_lop[lop].get(c, []))
    
    if bai_list_all:
        bai = st.multiselect("Chọn bài", bai_list_all, default=bai_list_all[:1])
    else:
        bai = []
    
    st.markdown("---")
    # Chọn loại đề (Giữ ở sidebar cho gọn)
    st.subheader("Tùy chọn xuất bản")
    co_dap_an = st.radio("Chế độ:", ["Có đáp án", "Không đáp án"], index=0)


# ===============================
# 🛠️ GIAO DIỆN CHÍNH: CẤU HÌNH MA TRẬN (ĐÃ SỬA THEO ẢNH)
# ===============================

st.markdown("---")
st.header("🛠️ 2. Cấu hình Ma trận đề thi")
st.write("Chỉnh số lượng câu hỏi theo mức độ nhận thức cho từng phần:")

# TẠO TABS GIAO DIỆN
tab1, tab2, tab3, tab4 = st.tabs(["TN Nhiều lựa chọn", "TN Đúng/Sai", "TN Trả lời ngắn", "Tự luận"])

# --- TAB 1: TRẮC NGHIỆM 4 LỰA CHỌN ---
with tab1:
    st.subheader("Phần 1: Trắc nghiệm (4 lựa chọn A,B,C,D)")
    c1, c2, c3 = st.columns(3)
    with c1:
        nl_nb = st.number_input("Số câu Nhận biết (NL)", min_value=0, value=4, key="nl_nb")
    with c2:
        nl_th = st.number_input("Số câu Thông hiểu (NL)", min_value=0, value=3, key="nl_th")
    with c3:
        nl_vd = st.number_input("Số câu Vận dụng (NL)", min_value=0, value=1, key="nl_vd")
    
    total_nl = nl_nb + nl_th + nl_vd
    st.info(f"👉 Tổng phần này: **{total_nl} câu**")

# --- TAB 2: ĐÚNG / SAI ---
with tab2:
    st.subheader("Phần 2: Trắc nghiệm Đúng/Sai")
    c4, c5, c6 = st.columns(3)
    with c4:
        ds_nb = st.number_input("Số câu Nhận biết (DS)", min_value=0, value=1, key="ds_nb")
    with c5:
        ds_th = st.number_input("Số câu Thông hiểu (DS)", min_value=0, value=1, key="ds_th")
    with c6:
        ds_vd = st.number_input("Số câu Vận dụng (DS)", min_value=0, value=0, key="ds_vd")
        
    total_ds = ds_nb + ds_th + ds_vd
    st.info(f"👉 Tổng phần này: **{total_ds} câu**")

# --- TAB 3: TRẢ LỜI NGẮN ---
with tab3:
    st.subheader("Phần 3: Trắc nghiệm Trả lời ngắn")
    c7, c8, c9 = st.columns(3)
    with c7:
        tn_nb = st.number_input("Số câu Nhận biết (TLN)", min_value=0, value=0, key="tn_nb")
    with c8:
        tn_th = st.number_input("Số câu Thông hiểu (TLN)", min_value=0, value=2, key="tn_th")
    with c9:
        tn_vd = st.number_input("Số câu Vận dụng (TLN)", min_value=0, value=1, key="tn_vd")

    total_tn = tn_nb + tn_th + tn_vd
    st.info(f"👉 Tổng phần này: **{total_tn} câu**")

# --- TAB 4: TỰ LUẬN ---
with tab4:
    st.subheader("Phần 4: Tự luận (Trình bày)")
    c10, c11, c12 = st.columns(3)
    with c10:
        tl_nb = st.number_input("Số câu Nhận biết (TL)", min_value=0, value=0, key="tl_nb")
    with c11:
        tl_th = st.number_input("Số câu Thông hiểu (TL)", min_value=0, value=1, key="tl_th")
    with c12:
        tl_vd = st.number_input("Số câu Vận dụng (TL)", min_value=0, value=1, key="tl_vd")

    total_tl = tl_nb + tl_th + tl_vd
    st.info(f"👉 Tổng phần này: **{total_tl} câu**")

# TỔNG KẾT CHUNG
total_questions = total_nl + total_ds + total_tn + total_tl
st.markdown("---")
st.write(f"📊 **Tổng số câu hỏi toàn đề:** `{total_questions}` câu")


# ===============================
# 📝 CÁC HÀM XỬ LÝ CHÍNH (GIỮ NGUYÊN PROMPT)
# ===============================

def create_math_prompt(lop, chuong, bai, 
                       nl_nb, nl_th, nl_vd,
                       ds_nb, ds_th, ds_vd,
                       tn_nb, tn_th, tn_vd,
                       tl_nb, tl_th, tl_vd,
                       dan_ap):
    
    prompt = f"""
Bạn là giáo viên Toán lớp {lop}, soạn đề kiểm tra theo chương trình mới (Sách "Kết nối tri thức").
- Nội dung: Chương {', '.join(chuong)}; Bài {', '.join(bai)}.

**CẤU TRÚC ĐỀ KIỂM TRA (CHI TIẾT MỨC ĐỘ):**

**PHẦN 1: TRẮC NGHIỆM NHIỀU LỰA CHỌN**
- Phân bố: NB: {nl_nb}, TH: {nl_th}, VD: {nl_vd}.
- Yêu cầu: Học sinh chọn A, B, C, D.

**PHẦN 2: TRẮC NGHIỆM ĐÚNG/SAI**
- Phân bố: NB: {ds_nb}, TH: {ds_th}, VD: {ds_vd}.
- Yêu cầu: Mỗi câu gồm 1 đề dẫn và 4 ý a, b, c, d.

**PHẦN 3: TRẮC NGHIỆM TRẢ LỜI NGẮN**
- Phân bố: NB: {tn_nb}, TH: {tn_th}, VD: {tn_vd}.
- Yêu cầu: Chỉ nêu câu hỏi, học sinh tự điền đáp án.

**PHẦN 4: TỰ LUẬN**
- Phân bố: NB: {tl_nb}, TH: {tl_th}, VD: {tl_vd}.
- Yêu cầu: Trình bày lời giải chi tiết.

--- **QUY ĐỊNH ĐỊNH DẠNG (BẮT BUỘC)** ---
- Công thức toán phải đặt trong dấu `$$`.
- Các phần phải được phân chia rõ ràng bằng tiêu đề in đậm.
- {dan_ap}
- Kết quả trả về định dạng **Markdown**.
"""
    return prompt

# --- Gọi API ---
def generate_questions(api_key, prompt):
    MODEL = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=300)
        if r.status_code != 200:
            return False, f"Lỗi API {r.status_code}: {r.text}"
        j = r.json()
        if j.get("candidates") and len(j["candidates"]) > 0:
            text = j["candidates"][0]["content"]["parts"][0]["text"]
            return True, text
        return False, "AI không trả về nội dung hợp lệ."
    except requests.exceptions.Timeout:
        return False, "Lỗi kết nối: Yêu cầu hết thời gian."


# ===============================
# 🚀 NÚT BẤM SINH ĐỀ
# ===============================

st.markdown("###")
if st.button("🚀 Sinh đề theo cấu hình chi tiết", type="primary", use_container_width=True):
    if not api_key:
        st.warning("⚠️ Nhập API Key trước khi sinh đề!")
    elif not chuong or not bai:
        st.warning("⚠️ Vui lòng chọn Chương và Bài học!")
    else:
        # Xử lý yêu cầu đáp án
        if co_dap_an == "Có đáp án":
            dan_ap_text = "YÊU CẦU ĐẶC BIỆT: Cuối đề thi phải có PHẦN HƯỚNG DẪN GIẢI CHI TIẾT và ĐÁP ÁN cho từng câu."
        else:
            dan_ap_text = "YÊU CẦU ĐẶC BIỆT: KHÔNG hiển thị đáp án và lời giải."

        # Tạo prompt với các tham số từ Tabs
        prompt = create_math_prompt(lop, chuong, bai,
                                    nl_nb, nl_th, nl_vd,
                                    ds_nb, ds_th, ds_vd,
                                    tn_nb, tn_th, tn_vd,
                                    tl_nb, tl_th, tl_vd,
                                    dan_ap_text)
        
        with st.spinner("Đang sinh đề... (AI đang suy nghĩ)"):
            success, result = generate_questions(api_key, prompt)
            
            if success:
                st.success("✅ Sinh đề thành công!")
                st.markdown(result, unsafe_allow_html=True)
                
                # --- Tải file markdown về máy ---
                filename = f"De_{lop}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                st.download_button("📥 Tải đề về máy (.md)", data=result, file_name=filename)
            else:
                st.error(result)
