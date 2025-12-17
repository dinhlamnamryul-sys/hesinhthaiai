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
# 📌 HÀM GỌI GEMINI
# ===============================

def analyze_real_image(api_key, image, prompt):
    # (Giữ nguyên hàm xử lý ảnh của bạn nếu cần dùng sau này)
    pass 

# ===============================
# 📚 DỮ LIỆU CHƯƠNG TRÌNH HỌC (GIỮ NGUYÊN)
# ===============================
# ... (Phần dữ liệu chuong_options_lop và bai_options_lop giữ nguyên như code cũ của bạn)
# Để tiết kiệm không gian hiển thị, tôi xin phép ẩn phần khai báo dữ liệu dài này. 
# Bạn hãy copy lại phần dữ liệu "chuong_options_lop" và "bai_options_lop" từ code cũ vào đây nhé.

# --- MOCK DATA (Dữ liệu giả lập để code chạy được trong ví dụ này - Hãy thay bằng dữ liệu thật của bạn) ---
chuong_options_lop = {
    "Lớp 6": ["Chương I", "Chương II"], "Lớp 7": ["Chương I"], 
    "Lớp 8": ["Chương I: Đa thức", "Chương II: Hằng đẳng thức"], "Lớp 9": ["Chương I"]
}
bai_options_lop = {
    "Lớp 6": {"Chương I": ["Bài 1"]}, "Lớp 7": {"Chương I": ["Bài 1"]},
    "Lớp 8": {"Chương I: Đa thức": ["Bài 1", "Bài 2"], "Chương II: Hằng đẳng thức": ["Bài 6", "Bài 7"]},
    "Lớp 9": {"Chương I": ["Bài 1"]}
}
# --------------------------------------------------------------------------------------------------


# ===============================
# 🎛️ SIDEBAR VÀ CẤU HÌNH ĐỀ (ĐÃ SỬA ĐỔI)
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
    st.header("2. Ma trận câu hỏi")
    st.info("Nhập số lượng câu hỏi cho từng mức độ")

    # --- CẤU HÌNH CHI TIẾT TỪNG PHẦN ---

    # 1. Trắc nghiệm 4 lựa chọn (NL)
    st.subheader("I. Trắc nghiệm (4 lựa chọn)")
    c1, c2, c3 = st.columns(3)
    nl_nb = c1.number_input("NL-NB", min_value=0, value=4, help="Nhận biết")
    nl_th = c2.number_input("NL-TH", min_value=0, value=3, help="Thông hiểu")
    nl_vd = c3.number_input("NL-VD", min_value=0, value=1, help="Vận dụng")
    total_nl = nl_nb + nl_th + nl_vd

    # 2. Đúng / Sai (DS)
    st.markdown("---")
    st.subheader("II. Đúng / Sai")
    c4, c5, c6 = st.columns(3)
    ds_nb = c4.number_input("DS-NB", min_value=0, value=1, help="Nhận biết")
    ds_th = c5.number_input("DS-TH", min_value=0, value=1, help="Thông hiểu")
    ds_vd = c6.number_input("DS-VD", min_value=0, value=0, help="Vận dụng")
    total_ds = ds_nb + ds_th + ds_vd

    # 3. Trả lời ngắn (TL Ngắn)
    st.markdown("---")
    st.subheader("III. Trả lời ngắn")
    c7, c8, c9 = st.columns(3)
    tn_nb = c7.number_input("TLN-NB", min_value=0, value=0, help="Nhận biết")
    tn_th = c8.number_input("TLN-TH", min_value=0, value=2, help="Thông hiểu")
    tn_vd = c9.number_input("TLN-VD", min_value=0, value=1, help="Vận dụng")
    total_tn = tn_nb + tn_th + tn_vd

    # 4. Tự luận (Mới thêm)
    st.markdown("---")
    st.subheader("IV. Tự luận (Trình bày)")
    c10, c11, c12 = st.columns(3)
    tl_nb = c10.number_input("TL-NB", min_value=0, value=0, help="Nhận biết")
    tl_th = c11.number_input("TL-TH", min_value=0, value=1, help="Thông hiểu")
    tl_vd = c12.number_input("TL-VD", min_value=0, value=1, help="Vận dụng")
    total_tl = tl_nb + tl_th + tl_vd

    # Tổng kết
    st.markdown("---")
    total_questions = total_nl + total_ds + total_tn + total_tl
    st.write(f"📊 **Tổng số câu hỏi:** {total_questions}")
    st.write(f"- 4 Lựa chọn: {total_nl}")
    st.write(f"- Đúng/Sai: {total_ds}")
    st.write(f"- Trả lời ngắn: {total_tn}")
    st.write(f"- Tự luận: {total_tl}")

    # Chọn loại đề
    co_dap_an = st.radio("Loại xuất bản:", ["Có đáp án", "Không đáp án"], index=0)

# ===============================
# 📝 CÁC HÀM XỬ LÝ CHÍNH (ĐÃ UPDATE PROMPT)
# ===============================

def create_math_prompt(lop, chuong, bai, 
                       # Nhận các biến chi tiết
                       nl_nb, nl_th, nl_vd,
                       ds_nb, ds_th, ds_vd,
                       tn_nb, tn_th, tn_vd,
                       tl_nb, tl_th, tl_vd,
                       dan_ap):
    
    total_nl = nl_nb + nl_th + nl_vd
    total_ds = ds_nb + ds_th + ds_vd
    total_tn = tn_nb + tn_th + tn_vd
    total_tl = tl_nb + tl_th + tl_vd

    prompt = f"""
Bạn là giáo viên Toán lớp {lop}, soạn đề kiểm tra theo chương trình mới (Sách "Kết nối tri thức").
- Nội dung: Chương {', '.join(chuong)}; Bài {', '.join(bai)}.

**CẤU TRÚC ĐỀ KIỂM TRA (CHI TIẾT MỨC ĐỘ):**

**PHẦN 1: TRẮC NGHIỆM NHIỀU LỰA CHỌN ({total_nl} câu)**
- Yêu cầu: Học sinh chọn A, B, C, D.
- Phân bố mức độ:
  + Nhận biết: {nl_nb} câu.
  + Thông hiểu: {nl_th} câu.
  + Vận dụng: {nl_vd} câu.

**PHẦN 2: TRẮC NGHIỆM ĐÚNG/SAI ({total_ds} câu)**
- Yêu cầu: Mỗi câu gồm 1 đề dẫn và 4 ý a, b, c, d.
- Phân bố mức độ:
  + Nhận biết: {ds_nb} câu.
  + Thông hiểu: {ds_th} câu.
  + Vận dụng: {ds_vd} câu.

**PHẦN 3: TRẮC NGHIỆM TRẢ LỜI NGẮN ({total_tn} câu)**
- Yêu cầu: Chỉ nêu câu hỏi, học sinh tự điền đáp án số hoặc kết quả ngắn gọn. KHÔNG có A, B, C, D.
- Phân bố mức độ:
  + Nhận biết: {tn_nb} câu.
  + Thông hiểu: {tn_th} câu.
  + Vận dụng: {tn_vd} câu.

**PHẦN 4: TỰ LUẬN ({total_tl} câu)**
- Yêu cầu: Câu hỏi yêu cầu học sinh trình bày lời giải chi tiết.
- Phân bố mức độ:
  + Nhận biết: {tl_nb} câu.
  + Thông hiểu: {tl_th} câu.
  + Vận dụng: {tl_vd} câu.

--- **QUY ĐỊNH ĐỊNH DẠNG (BẮT BUỘC)** ---

**1. QUY TẮC CHUNG:**
- Công thức toán phải đặt trong dấu `$$`. Ví dụ: $$y = x^2$$.
- Các phần phải được phân chia rõ ràng bằng tiêu đề in đậm.

**2. ĐỊNH DẠNG TỪNG PHẦN:**
* **PHẦN 1 (NL):** Đáp án A, B, C, D phải xuống dòng riêng biệt.
* **PHẦN 2 (DS):** 4 ý a), b), c), d) phải xuống dòng riêng biệt.
* **PHẦN 3 (TRẢ LỜI NGẮN):** Chỉ viết nội dung câu hỏi.
* **PHẦN 4 (TỰ LUẬN):** Đặt câu hỏi rõ ràng.

--- **MẪU TRÌNH BÀY (AI PHẢI LÀM THEO FORMAT NÀY)** ---

**PHẦN I. TRẮC NGHIỆM NHIỀU LỰA CHỌN**
**Câu 1.** (NB) Nội dung câu hỏi...
A. ...
B. ...
C. ...
D. ...

**PHẦN II. TRẮC NGHIỆM ĐÚNG SAI**
**Câu 2.** (TH) Cho hình chữ nhật ABCD...
a) ...
b) ...
c) ...
d) ...

**PHẦN III. TRẮC NGHIỆM TRẢ LỜI NGẮN**
**Câu 3.** (VD) Tính giá trị biểu thức...

**PHẦN IV. TỰ LUẬN**
**Câu 4.** (VD) Giải bài toán bằng cách lập phương trình: Một người đi xe đạp...

--- **HẾT PHẦN MẪU** ---

**YÊU CẦU KHÁC:**
- {dan_ap}
- Kết quả trả về định dạng **Markdown**.
"""
    return prompt

# --- Gọi API ---
def generate_questions(api_key, prompt):
    MODEL = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }]
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

if st.button("🚀 Sinh đề theo cấu hình chi tiết"):
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

        # Tạo prompt với các tham số chi tiết mới
        prompt = create_math_prompt(lop, chuong, bai,
                                    nl_nb, nl_th, nl_vd,
                                    ds_nb, ds_th, ds_vd,
                                    tn_nb, tn_th, tn_vd,
                                    tl_nb, tl_th, tl_vd,
                                    dan_ap_text)
        
        with st.spinner("Đang sinh đề... (Sẽ mất khoảng 10-20 giây)"):
            success, result = generate_questions(api_key, prompt)
            
            if success:
                st.success("✅ Sinh đề thành công!")
                st.markdown(result, unsafe_allow_html=True)
                
                # --- Tải file markdown về máy ---
                filename = f"De_{lop}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                st.download_button("📥 Tải đề về máy (.md)", data=result, file_name=filename)
            else:
                st.error(result)
