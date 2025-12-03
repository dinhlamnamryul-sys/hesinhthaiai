# file: sinh_de_kntc_lop6_latex.py
import requests
import streamlit as st

st.set_page_config(page_title="Sinh Đề Lớp 6 - Toàn công thức LaTeX", page_icon="📝", layout="wide")
st.title("📝 Sinh Đề Tự Động Lớp 6 – Tất cả công thức LaTeX")

# --- API Key ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.text_input("Nhập Google API Key:", type="password")

# --- Chương và bài lớp 6 ---
chuong_options = [
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
]

bai_options = {
    "Chương I: Tập hợp các số tự nhiên": ["Bài 1", "Bài 2", "Bài 3", "Bài 4", "Ôn tập"],
    "Chương II: Tính chia hết trong tập hợp các số tự nhiên": ["Bài 5", "Bài 6", "Ôn tập"],
    "Chương III: Số nguyên": ["Bài 7", "Bài 8", "Ôn tập"],
    "Chương IV: Một số hình phẳng trong thực tiễn": ["Bài 9", "Bài 10", "Ôn tập"],
    "Chương V: Tính đối xứng của hình phẳng trong tự nhiên": ["Bài 11", "Bài 12", "Ôn tập"],
    "Chương VI: Phân số": ["Bài 13", "Bài 14", "Ôn tập"],
    "Chương VII: Số thập phân": ["Bài 15", "Bài 16", "Ôn tập"],
    "Chương VIII: Những hình hình học cơ bản": ["Bài 17", "Bài 18", "Ôn tập"],
    "Chương IX: Dữ liệu và xác suất thực nghiệm": ["Bài 19", "Bài 20", "Ôn tập"],
    "Hoạt động thực hành trải nghiệm": ["Bài 21", "Bài 22", "Ôn tập"]
}

# --- Sidebar ---
with st.sidebar:
    st.header("Thông tin sinh đề")
    lop = "Lớp 6"
    st.info(f"Chỉ sinh đề cho {lop}")
    
    chuong = st.multiselect("Chọn chương", chuong_options, default=chuong_options[0])
    bai_list_all = []
    for c in chuong:
        bai_list_all.extend(bai_options.get(c, []))
    bai = st.multiselect("Chọn bài", bai_list_all, default=bai_list_all[0])

    st.markdown("---")
    so_cau = st.number_input("Tổng số câu hỏi", min_value=1, max_value=50, value=21)
    col_nl, col_ds, col_tl = st.columns(3)
    with col_nl: phan_bo_nl = st.number_input("NL (4 lựa chọn)", min_value=0, value=12)
    with col_ds: phan_bo_ds = st.number_input("DS (Đúng/Sai)", min_value=0, value=2)
    with col_tl: phan_bo_tl = st.number_input("TL (Tự luận)", min_value=0, value=7)

    st.markdown("---")
    col_nb, col_th, col_vd = st.columns(3)
    with col_nb: so_cau_nb = st.number_input("Nhận biết", min_value=0, value=6)
    with col_th: so_cau_th = st.number_input("Thông hiểu", min_value=0, value=8)
    with col_vd: so_cau_vd = st.number_input("Vận dụng", min_value=0, value=7)

    co_dap_an = st.checkbox("Có đáp án", value=True)

# --- Build prompt ---
def build_prompt(lop, chuong, bai, so_cau, phan_bo_nl, phan_bo_ds, phan_bo_tl,
                 so_cau_nb, so_cau_th, so_cau_vd, co_dap_an):
    
    dan_ap = "Tạo đáp án chi tiết và lời giải sau mỗi câu hỏi, tất cả công thức bằng LaTeX." if co_dap_an else "Không cần đáp án, nhưng tất cả công thức bắt buộc LaTeX."
    
    prompt = f"""
Bạn là giáo viên Toán lớp 6, sinh đề kiểm tra theo sách "Kết nối tri thức với cuộc sống".
- Chương: {', '.join(chuong)}
- Bài: {', '.join(bai)}

Yêu cầu:
1. Tổng {so_cau} câu, gồm:
   - NL (4 lựa chọn): {phan_bo_nl} câu
   - DS (Đúng/Sai): {phan_bo_ds} câu
   - TL: {phan_bo_tl} câu
2. Phân bố nhận thức:
   - Nhận biết: {so_cau_nb}
   - Thông hiểu: {so_cau_th}
   - Vận dụng: {so_cau_vd}
3. **TẤT CẢ CÔNG THỨC TOÁN PHẢI VIẾT DƯỚI DẠNG LaTeX, đặt trong $$...$$**.
4. Mỗi câu phải gắn nhãn Mức độ và Loại câu hỏi.
5. {dan_ap}
"""
    return prompt

# --- Gọi API ---
def generate_questions(api_key, prompt):
    MODEL = "models/gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"
    payload = {"contents":[{"role":"user","parts":[{"text":prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=300)
        if r.status_code != 200:
            return False, f"Lỗi API {r.status_code}: {r.text}"
        j = r.json()
        if j.get("candidates") and len(j["candidates"])>0:
            text = j["candidates"][0]["content"]["parts"][0]["text"]
            return True, text
        return False, "AI không trả về nội dung hợp lệ."
    except requests.exceptions.Timeout:
        return False, "Lỗi kết nối: Yêu cầu hết thời gian."

# --- Streamlit button ---
if st.button("Sinh đề"):
    if not api_key:
        st.warning("Nhập API Key trước khi sinh đề!")
    else:
        prompt = build_prompt(lop, chuong, bai, so_cau, phan_bo_nl, phan_bo_ds, phan_bo_tl,
                              so_cau_nb, so_cau_th, so_cau_vd, co_dap_an)
        with st.spinner("Đang sinh đề (có LaTeX)..."):
            success, result = generate_questions(api_key, prompt)
            if success:
                st.success("✅ Sinh đề thành công!")
                st.text_area("Đề kiểm tra", value=result, height=600)
            else:
                st.error(result)
