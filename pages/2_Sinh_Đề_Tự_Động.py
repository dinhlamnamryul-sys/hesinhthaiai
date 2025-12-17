import requests
import streamlit as st
from datetime import datetime
import re

# ===============================
# ⚙️ CẤU HÌNH TRANG
# ===============================
st.set_page_config(
    page_title="Math Gen Pro - KNTT",
    layout="wide",
    page_icon="🧮"
)

# ===============================
# 🔑 NHẬP GOOGLE API KEY
# ===============================
with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key:
1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập Gmail.
3. Nhấn **Create API key**.
4. Copy API Key.
5. Dán vào ô bên dưới.
""")

st.subheader("🔐 Nhập Google API Key:")
api_key = st.text_input("Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Vui lòng nhập API Key để tiếp tục.")
else:
    st.success("✅ API Key đã được nhập.")

# ===============================
# 📚 DỮ LIỆU CHƯƠNG TRÌNH
# ===============================

chuong_options_lop = {
    "Lớp 6": [
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
    ],
    "Lớp 7": [
        "Chương I: Số hữu tỉ",
        "Chương II: Số thực",
        "Chương III: Góc và đường thẳng song song",
        "Chương IV: Tam giác bằng nhau",
        "Chương V: Thu thập và biểu diễn dữ liệu",
        "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ",
        "Chương VII: Biểu thức đại số và đa thức một biến",
        "Chương VIII: Làm quen với biến cố và xác suất",
        "Chương IX: Quan hệ giữa các yếu tố trong một tam giác",
        "Chương X: Một số hình khối trong thực tiễn",
        "Bài tập ôn tập cuối năm"
    ],
    "Lớp 8": [
        "Chương I: Đa thức",
        "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
        "Chương III: Tứ giác",
        "Chương IV: Định lí Thalès",
        "Chương V: Dữ liệu và biểu đồ",
        "Chương VI: Phân thức đại số",
        "Chương VII: Phương trình bậc nhất và hàm số bậc nhất",
        "Chương VIII: Mở đầu về tính xác suất của biến cố",
        "Chương IX: Tam giác đồng dạng",
        "Chương X: Một số hình khối trong thực tiễn",
        "Bài tập ôn tập cuối năm"
    ],
    "Lớp 9": [
        "Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn",
        "Chương II: Phương trình và bất phương trình bậc nhất một ẩn",
        "Chương III: Căn bậc hai và căn bậc ba",
        "Chương IV: Hệ thức lượng trong tam giác vuông",
        "Chương V: Đường tròn",
        "Hoạt động thực hành trải nghiệm",
        "Chương VI: Hàm số y = ax² (a ≠ 0). Phương trình bậc hai một ẩn",
        "Chương VII: Tần số và tần số tương đối",
        "Chương VIII: Xác suất của biến cố",
        "Chương IX: Đường tròn ngoại tiếp và nội tiếp",
        "Chương X: Một số hình khối trong thực tiễn"
    ]
}

# ===============================
# 🛠️ HÀM XỬ LÝ ĐỊNH DẠNG
# ===============================

def format_fix_final(text: str) -> str:
    text = re.sub(r'(\s)([A-D]\.)', r'\n\n\2', text)
    text = re.sub(r'(\s)([a-d][\)\.])', r'\n\n\2', text)
    text = re.sub(r'(\s)(Câu \d+)', r'\n\n\n\2', text)
    return text

def create_math_prompt_v2(
    lop, chuong, bai,
    nl_nb, nl_th, nl_vd,
    ds_nb, ds_th, ds_vd,
    tlngan_nb, tlngan_th, tlngan_vd,
    tl_nb, tl_th, tl_vd,
    dan_ap_text
):
    return f"""
Bạn là giáo viên Toán lớp {lop}, soạn đề kiểm tra theo chương trình GDPT 2018 (SGK Kết nối tri thức).

Nội dung: {", ".join(bai)} thuộc {", ".join(chuong)}

Yêu cầu cấu trúc đề:
- Trắc nghiệm nhiều lựa chọn: {nl_nb + nl_th + nl_vd} câu
- Đúng/Sai: {ds_nb + ds_th + ds_vd} câu
- Trả lời ngắn: {tlngan_nb + tlngan_th + tlngan_vd} câu
- Tự luận: {tl_nb + tl_th + tl_vd} câu

Quy định:
- Công thức Toán phải đặt trong $$...$$
- Mỗi đáp án, mỗi ý phải xuống dòng

{dan_ap_text}
"""

def generate_questions(api_key, prompt):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }

    models = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-pro"
    ]

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            if r.status_code == 200:
                data = r.json()
                return True, data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            pass

    return False, "❌ Không thể kết nối Gemini API. Kiểm tra API Key."

# ===============================
# 🎛️ SIDEBAR
# ===============================

with st.sidebar:
    st.header("1. Chọn nội dung")
    lop = st.selectbox("Chọn lớp", list(chuong_options_lop.keys()), index=3)
    chuong = st.multiselect("Chọn chương", chuong_options_lop[lop])
    bai = st.multiselect("Nhập tên bài (có thể gõ tay)", [])

    co_dap_an = st.radio(
        "Chế độ đáp án",
        ["Có đáp án chi tiết", "Không đáp án"]
    )

# ===============================
# 🚀 SINH ĐỀ
# ===============================

if st.button("🚀 Sinh đề", type="primary"):
    if not api_key:
        st.warning("⚠️ Chưa nhập API Key.")
    elif not chuong:
        st.warning("⚠️ Chưa chọn chương.")
    else:
        dan_ap = (
            "Cuối đề phải có đáp án và lời giải chi tiết."
            if co_dap_an == "Có đáp án chi tiết"
            else "KHÔNG hiển thị đáp án."
        )

        prompt = create_math_prompt_v2(
            lop, chuong, bai,
            4, 4, 4,
            1, 2, 1,
            1, 2, 3,
            0, 1, 1,
            dan_ap
        )

        with st.spinner("⏳ Đang sinh đề..."):
            ok, result = generate_questions(api_key, prompt)

        if ok:
            result = format_fix_final(result)
            st.success("✅ Sinh đề thành công")
            st.markdown(result, unsafe_allow_html=True)

            filename = f"De_Toan_{lop}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            st.download_button(
                "📥 Tải đề (Markdown)",
                result,
                file_name=filename
            )
        else:
            st.error(result)
