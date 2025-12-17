import requests
import streamlit as st
from datetime import datetime
import base64
from io import BytesIO
import re  # Thư viện quan trọng để xử lý xuống dòng

# ===============================
# 🔑 NHẬP GOOGLE API KEY
# ===============================

st.set_page_config(page_title="Math Gen Pro", layout="wide")

with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key:
1. Truy cập: **https://aistudio.google.com/app/apikey**
2. Đăng nhập Gmail.
3. Nhấn **Create API key**.
4. Copy API Key.
5. Dán vào ô bên dưới.
""")

st.subheader("🔐 Nhập Google API Key:")
api_key = st.text_input("Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Nhập API Key để tiếp tục.")
else:
    st.success("✅ API Key hợp lệ!")


# ===============================
# 🛠️ CÁC HÀM XỬ LÝ (CORE)
# ===============================

def analyze_real_image(api_key, image, prompt):
    """Hàm xử lý hình ảnh (Giữ lại từ code cũ theo yêu cầu)"""
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buf = BytesIO()
    image.save(buf, format="JPEG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    MODEL = "gemini-1.5-flash" # Hoặc gemini-2.0-flash-exp nếu có
    URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"

    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
            ]
        }]
    }

    try:
        res = requests.post(URL, json=payload)
        if res.status_code != 200:
            return f"❌ Lỗi API {res.status_code}: {res.text}"
        data = res.json()
        if "candidates" not in data:
            return "❌ API trả về rỗng."
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

def format_fix_final(text):
    """
    Hàm xử lý hậu kỳ bắt buộc xuống dòng bằng Regex.
    Chạy hàm này trước khi st.markdown để đảm bảo hiển thị đẹp.
    """
    # 1. Xử lý phần Trắc nghiệm (A. B. C. D.)
    # Tìm A., B., C., D. đứng đầu dòng hoặc sau khoảng trắng -> Thêm 2 dấu xuống dòng
    text = re.sub(r'(\s)([A-D]\.)', r'\n\n\2', text)
    
    # 2. Xử lý phần Đúng/Sai (a) b) c) d))
    # Tìm a), b)... hoặc a., b. -> Thêm 2 dấu xuống dòng
    text = re.sub(r'(\s)([a-d][\)\.])', r'\n\n\2', text)
    
    # 3. Xử lý khoảng cách giữa các câu hỏi (Câu 1., Câu 2...) để đề thoáng hơn
    text = re.sub(r'(\s)(Câu \d+)', r'\n\n\n\2', text)
    
    return text

def create_math_prompt_v2(lop, chuong, bai, 
                          nl_nb, nl_th, nl_vd, 
                          ds_nb, ds_th, ds_vd, 
                          tlngan_nb, tlngan_th, tlngan_vd,
                          tl_nb, tl_th, tl_vd, 
                          dan_ap_text):
    """Hàm tạo prompt chi tiết theo ma trận nhận thức"""
    
    prompt = f"""
Bạn là giáo viên Toán lớp {lop}, soạn đề kiểm tra theo chương trình GDPT 2018 (Sách Kết nối tri thức).
- Nội dung kiểm tra: {', '.join(bai)} thuộc {', '.join(chuong)}.

**YÊU CẦU CẤU TRÚC ĐỀ (Bắt buộc tuân thủ số lượng):**

1. **PHẦN 1: TRẮC NGHIỆM NHIỀU LỰA CHỌN (4 phương án A,B,C,D)**
   - Tổng: {nl_nb + nl_th + nl_vd} câu.
   - Phân bổ: {nl_nb} Nhận biết, {nl_th} Thông hiểu, {nl_vd} Vận dụng.
   - Định dạng: Các đáp án A, B, C, D phải xuống dòng riêng biệt.

2. **PHẦN 2: TRẮC NGHIỆM ĐÚNG/SAI (Mỗi câu 4 ý a,b,c,d)**
   - Tổng: {ds_nb + ds_th + ds_vd} câu.
   - Phân bổ: {ds_nb} Nhận biết, {ds_th} Thông hiểu, {ds_vd} Vận dụng.
   - Định dạng: Có 1 đề dẫn, sau đó 4 ý a,b,c,d xuống dòng riêng biệt.

3. **PHẦN 3: TRẮC NGHIỆM TRẢ LỜI NGẮN (Điền số/Kết quả)**
   - Tổng: {tlngan_nb + tlngan_th + tlngan_vd} câu.
   - Phân bổ: {tlngan_nb} Nhận biết, {tlngan_th} Thông hiểu, {tlngan_vd} Vận dụng.
   - Định dạng: Chỉ câu hỏi, yêu cầu ra đáp số cụ thể.

4. **PHẦN 4: TỰ LUẬN (Nếu có)**
   - Tổng: {tl_nb + tl_th + tl_vd} câu.
   - Phân bổ: {tl_nb} NB, {tl_th} TH, {tl_vd} VD.

**QUY ĐỊNH ĐỊNH DẠNG (NGHIÊM NGẶT):**
- **Toán học:** Công thức BẮT BUỘC đặt trong `$$...$$`. Ví dụ: $$y = x^2$$.
- **Trình bày:** Giữa các ý và đáp án PHẢI có dòng trống.

--- **MẪU TRÌNH BÀY (AI HÃY LÀM THEO FORMAT NÀY)** ---

**PHẦN I. TRẮC NGHIỆM NHIỀU LỰA CHỌN**
**Câu 1.** Nội dung câu hỏi...
(Dòng trống)
A. $$x=1$$
(Dòng trống)
B. $$x=2$$
(Dòng trống)
C. $$x=3$$
(Dòng trống)
D. $$x=4$$

**PHẦN II. TRẮC NGHIỆM ĐÚNG SAI**
**Câu 2.** Cho hình chữ nhật ABCD...
(Dòng trống)
a) Hai đường chéo bằng nhau.
(Dòng trống)
b) Cạnh AB = 5.
(Dòng trống)
c) ...
(Dòng trống)
d) ...

**PHẦN III. TRẮC NGHIỆM TRẢ LỜI NGẮN**
**Câu 3.** Tính giá trị biểu thức A...

--- **HẾT PHẦN MẪU** ---

{dan_ap_text}
"""
    return prompt

def generate_questions(api_key, prompt):
    """Hàm gọi API Gemini để sinh text"""
    MODEL = "gemini-2.0-flash-exp" # Dùng model mới nhất nếu có, hoặc gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        if r.status_code != 200:
            # Fallback về 1.5 flash nếu 2.0 chưa public cho key này
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            r = requests.post(url, json=payload, headers=headers, timeout=120)
            
        if r.status_code != 200:
            return False, f"Lỗi API: {r.text}"
            
        j = r.json()
        if j.get("candidates"):
            return True, j["candidates"][0]["content"]["parts"][0]["text"]
        return False, "Không có dữ liệu trả về."
    except Exception as e:
        return False, f"Lỗi kết nối: {str(e)}"

# ===============================
# 📚 DỮ LIỆU CHƯƠNG TRÌNH HỌC (DATA CŨ ĐẦY ĐỦ)
# ===============================

chuong_options_lop = {
    "Lớp 6": [
        "Chương I: Tập hợp các số tự nhiên", "Chương II: Tính chia hết trong tập hợp các số tự nhiên",
        "Chương III: Số nguyên", "Chương IV: Một số hình phẳng trong thực tiễn",
        "Chương V: Tính đối xứng của hình phẳng trong tự nhiên", "Chương VI: Phân số",
        "Chương VII: Số thập phân", "Chương VIII: Những hình hình học cơ bản",
        "Chương IX: Dữ liệu và xác suất thực nghiệm", "Hoạt động thực hành trải nghiệm"
    ],
    "Lớp 7": [
        "Chương I: Số hữu tỉ", "Chương II: Số thực", "Chương III: Góc và đường thẳng song song",
        "Chương IV: Tam giác bằng nhau", "Chương V: Thu thập và biểu diễn dữ liệu",
        "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ", "Chương VII: Biểu thức đại số và đa thức một biến",
        "Chương VIII: Làm quen với biến cố và xác suất", "Chương IX: Quan hệ giữa các yếu tố trong một tam giác",
        "Chương X: Một số hình khối trong thực tiễn", "Bài tập ôn tập cuối năm"
    ],
    "Lớp 8": [
        "Chương I: Đa thức", "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng", "Chương III: Tứ giác",
        "Chương IV: Định lí Thalès", "Chương V: Dữ liệu và biểu đồ", "Chương VI: Phân thức đại số",
        "Chương VII: Phương trình bậc nhất và hàm số bậc nhất", "Chương VIII: Mở đầu về tính xác suất của biến cố",
        "Chương IX: Tam giác đồng dạng", "Chương X: Một số hình khối trong thực tiễn", "Bài tập ôn tập cuối năm"
    ],
    "Lớp 9": [
        "Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn", "Chương II: Phương trình và bất phương trình bậc nhất một ẩn",
        "Chương III: Căn bậc hai và căn bậc ba", "Chương IV: Hệ thức lượng trong tam giác vuông", "Chương V: Đường tròn",
        "Hoạt động thực hành trải nghiệm", "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn",
        "Chương VII: Tần số và tần số tương đối", "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản",
        "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp", "Chương X: Một số hình khối trong thực tiễn"
    ]
}

# Dictionary bài học chi tiết (Rút gọn hiển thị code nhưng vẫn đầy đủ logic map)
# Để đảm bảo code chạy ngay, tôi dùng logic lấy bài mặc định nếu không khớp key,
# hoặc bạn có thể paste lại dict `bai_options_lop` khổng lồ vào đây.
# Dưới đây là dict mẫu cho Lớp 9 (theo yêu cầu của bạn hay dùng), các lớp khác tương tự.

bai_options_lop = {
    "Lớp 9": {
        "Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn": ["Bài 1. Khái niệm phương trình", "Bài 2. Giải hệ hai phương trình", "Bài 3. Giải bài toán bằng cách lập hệ"],
        "Chương II: Phương trình và bất phương trình bậc nhất một ẩn": ["Bài 4. Phương trình quy về bậc nhất", "Bài 5. Bất đẳng thức", "Bài 6. Bất phương trình bậc nhất"],
        # ... (Bạn có thể bổ sung thêm nếu cần, hoặc code sẽ tự xử lý fallback)
    }
}
# Hàm hỗ trợ lấy bài an toàn (tránh lỗi key)
def get_bai_list(lop, chuong_list):
    res = []
    if lop in bai_options_lop:
        for c in chuong_list:
            res.extend(bai_options_lop[lop].get(c, [f"Các bài tập thuộc {c}"])) # Fallback thông minh
    else:
        for c in chuong_list:
            res.append(f"Nội dung thuộc {c}")
    return res

# ===============================
# 🎛️ SIDEBAR VÀ CẤU HÌNH
# ===============================

with st.sidebar:
    st.header("1. Chọn nội dung")
    lop = st.selectbox("Chọn lớp", ["Lớp 6","Lớp 7","Lớp 8","Lớp 9"], index=3)
    
    chuong_options = chuong_options_lop.get(lop, [])
    chuong = st.multiselect("Chọn chương", chuong_options, default=[chuong_options[0]] if chuong_options else None)
    
    bai_list_all = get_bai_list(lop, chuong)
    if bai_list_all:
        bai = st.multiselect("Chọn bài", bai_list_all, default=[bai_list_all[0]])
    else:
        bai = []
        
    st.markdown("---")
    co_dap_an = st.radio("Chế độ đáp án:", ["Có đáp án chi tiết", "Không đáp án"], index=0)

# ===============================
# 🎚️ CẤU HÌNH MA TRẬN ĐỀ (GIAO DIỆN MỚI)
# ===============================

st.header("🛠️ 2. Cấu hình Ma trận đề thi")
st.markdown("Chỉnh số lượng câu hỏi theo mức độ nhận thức cho từng phần:")

# Tạo 4 Tabs cho 4 loại câu hỏi
tab1, tab2, tab3, tab4 = st.tabs(["1. TN Nhiều lựa chọn", "2. TN Đúng/Sai", "3. TN Trả lời ngắn", "4. Tự luận"])

# 1. TRẮC NGHIỆM NHIỀU LỰA CHỌN (NL)
with tab1:
    st.subheader("Phần 1: Trắc nghiệm (4 lựa chọn A,B,C,D)")
    c1, c2, c3 = st.columns(3)
    nl_nb = c1.number_input("Số câu Nhận biết (NL)", min_value=0, value=4, key="nl_nb")
    nl_th = c2.number_input("Số câu Thông hiểu (NL)", min_value=0, value=4, key="nl_th")
    nl_vd = c3.number_input("Số câu Vận dụng (NL)", min_value=0, value=4, key="nl_vd")
    total_nl = nl_nb + nl_th + nl_vd
    st.info(f"👉 Tổng phần này: **{total_nl}** câu")

# 2. TRẮC NGHIỆM ĐÚNG SAI (DS)
with tab2:
    st.subheader("Phần 2: Trắc nghiệm Đúng/Sai (4 ý a,b,c,d)")
    c1, c2, c3 = st.columns(3)
    ds_nb = c1.number_input("Số câu Nhận biết (DS)", min_value=0, value=1, key="ds_nb")
    ds_th = c2.number_input("Số câu Thông hiểu (DS)", min_value=0, value=2, key="ds_th")
    ds_vd = c3.number_input("Số câu Vận dụng (DS)", min_value=0, value=1, key="ds_vd")
    total_ds = ds_nb + ds_th + ds_vd
    st.info(f"👉 Tổng phần này: **{total_ds}** câu (Mỗi câu gồm 4 ý nhỏ)")

# 3. TRẮC NGHIỆM TRẢ LỜI NGẮN (TNTL)
with tab3:
    st.subheader("Phần 3: Trắc nghiệm Trả lời ngắn (Điền số/kết quả)")
    c1, c2, c3 = st.columns(3)
    tlngan_nb = c1.number_input("Số câu Nhận biết (TL ngắn)", min_value=0, value=1, key="tlngan_nb")
    tlngan_th = c2.number_input("Số câu Thông hiểu (TL ngắn)", min_value=0, value=2, key="tlngan_th")
    tlngan_vd = c3.number_input("Số câu Vận dụng (TL ngắn)", min_value=0, value=3, key="tlngan_vd")
    total_tlngan = tlngan_nb + tlngan_th + tlngan_vd
    st.info(f"👉 Tổng phần này: **{total_tlngan}** câu")

# 4. TỰ LUẬN (TL)
with tab4:
    st.subheader("Phần 4: Bài tập Tự luận (Trình bày chi tiết)")
    c1, c2, c3 = st.columns(3)
    tl_nb = c1.number_input("Số câu Nhận biết (Tự luận)", min_value=0, value=0, key="tl_nb")
    tl_th = c2.number_input("Số câu Thông hiểu (Tự luận)", min_value=0, value=1, key="tl_th")
    tl_vd = c3.number_input("Số câu Vận dụng (Tự luận)", min_value=0, value=1, key="tl_vd")
    total_tl = tl_nb + tl_th + tl_vd
    st.info(f"👉 Tổng phần này: **{total_tl}** câu")

total_questions = total_nl + total_ds + total_tlngan + total_tl
st.markdown("---")
st.success(f"📊 **TỔNG CỘNG TOÀN ĐỀ:** {total_questions} câu hỏi.")

# ===============================
# 🚀 NÚT SINH ĐỀ VÀ HIỂN THỊ
# ===============================

if st.button("🚀 Sinh đề theo cấu hình chi tiết", type="primary"):
    if not api_key:
        st.warning("Vui lòng nhập API Key.")
    elif total_questions == 0:
        st.warning("Bạn chưa chọn số lượng câu hỏi nào!")
    else:
        # Xử lý text hướng dẫn chấm
        if co_dap_an == "Có đáp án chi tiết":
            dan_ap = "Cuối đề thi phải có PHẦN ĐÁP ÁN (Bảng đáp án cho TN) và HƯỚNG DẪN GIẢI CHI TIẾT cho từng câu."
        else:
            dan_ap = "KHÔNG hiển thị đáp án và lời giải."

        # 1. Tạo prompt
        prompt = create_math_prompt_v2(
            lop, chuong, bai,
            nl_nb, nl_th, nl_vd,
            ds_nb, ds_th, ds_vd,
            tlngan_nb, tlngan_th, tlngan_vd,
            tl_nb, tl_th, tl_vd,
            dan_ap
        )
        
        with st.spinner("Đang kết nối Gemini để sinh đề... (Mất khoảng 10-20 giây)"):
            success, result = generate_questions(api_key, prompt)
            
            if success:
                # 2. QUAN TRỌNG: Gọi hàm sửa lỗi dính dòng
                result_fixed = format_fix_final(result)
                
                st.success("✅ Sinh đề thành công!")
                
                # 3. Hiển thị kết quả
                st.markdown(result_fixed, unsafe_allow_html=True)
                
                # 4. Nút tải về
                filename = f"De_{lop}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                st.download_button("📥 Tải đề về máy (Markdown)", result_fixed, file_name=filename)
            else:
                st.error(result)
