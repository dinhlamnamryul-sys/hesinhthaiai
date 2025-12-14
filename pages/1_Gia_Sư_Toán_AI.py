import streamlit as st
import random
from deep_translator import GoogleTranslator

# ================== CẤU HÌNH ==================
st.set_page_config(
    page_title="Gia sư Toán AI – Bản Mường",
    page_icon="🏔️",
    layout="wide"
)

# ================== DỊCH H’MÔNG (CHỈ GỢI Ý) ==================
def dich_hmong(text):
    try:
        return GoogleTranslator(source="vi", target="hmn").translate(text)
    except:
        return "(Không dịch được – kiểm tra mạng)"

# ================== TRỘN ĐÁP ÁN ==================
def tron_dap_an(dung, sai):
    ds = sai + [dung]
    random.shuffle(ds)
    return ds

# ================== SINH CÂU HỎI ==================
def tao_de_toan(lop, bai):
    de = ""
    dap_an = ""
    options = []
    goi_y = ""
    muc_do = ""

    # ================= LỚP 6 =================
    if lop == "Lớp 6":

        # ---- BÀI 1. TẬP HỢP ----
        if bai == "Bài 1. Tập hợp":
            tap = sorted(random.sample(range(1, 10), 5))
            dung = random.choice(tap)
            sai = random.choice([x for x in range(1, 12) if x not in tap])

            de = "Cách viết nào đúng?"
            dap_an = f"{dung} ∈ {{{';'.join(map(str, tap))}}}"
            options = tron_dap_an(dap_an, [
                f"{sai} ∈ {{{';'.join(map(str, tap))}}}",
                f"{dung} ∉ {{{';'.join(map(str, tap))}}}",
                f"{tap[0]} ⊂ {tap[1]}"
            ])
            goi_y = f"{dung} là phần tử thuộc tập hợp."
            muc_do = "NB"

        # ---- BÀI 6. LŨY THỪA ----
        elif bai == "Bài 6. Lũy thừa":
            a = random.randint(2, 5)
            n = random.randint(2, 3)
            de = f"Tính giá trị: {a}^{n}"
            dap_an = str(a ** n)
            options = tron_dap_an(dap_an, [
                str(a * n),
                str(a + n),
                str(a ** (n + 1))
            ])
            goi_y = "Lũy thừa là nhân số đó với chính nó nhiều lần."
            muc_do = "TH"

    # ================= LỚP 7 =================
    elif lop == "Lớp 7":
        a = random.randint(2, 9)
        de = f"Tính: (-{a})²"
        dap_an = str(a * a)
        options = tron_dap_an(dap_an, [
            str(-a * a),
            str(a),
            str(a * 2)
        ])
        goi_y = "Bình phương của số âm là số dương."
        muc_do = "TH"

    # ================= LỚP 8 =================
    elif lop == "Lớp 8":
        a = random.randint(2, 6)
        de = f"Rút gọn: x(x + {a}) − x²"
        dap_an = f"{a}x"
        options = tron_dap_an(dap_an, [
            "x²",
            f"{a}",
            f"-{a}x"
        ])
        goi_y = "Khai triển biểu thức rồi thu gọn."
        muc_do = "VD"

    # ================= LỚP 9 =================
    elif lop == "Lớp 9":
        a = random.randint(1, 9)
        de = f"Điều kiện xác định của √(x − {a}) là:"
        dap_an = f"x ≥ {a}"
        options = tron_dap_an(dap_an, [
            f"x > {a}",
            f"x ≤ {a}",
            f"x < {a}"
        ])
        goi_y = "Biểu thức trong căn bậc hai phải không âm."
        muc_do = "VD"

    return de, dap_an, options, goi_y, muc_do

# ================== GIAO DIỆN ==================
st.markdown(
    "<h1 style='text-align:center'>🏫 GIA SƯ TOÁN AI – BẢN MƯỜNG</h1>",
    unsafe_allow_html=True
)

lop = st.selectbox("📘 Chọn lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"])
bai = st.selectbox(
    "📗 Chọn bài",
    ["Bài 1. Tập hợp", "Bài 6. Lũy thừa"]
    if lop == "Lớp 6" else ["Bài ôn tập"]
)

if "cau_hoi" not in st.session_state:
    st.session_state.cau_hoi = None

if st.button("✨ Tạo câu hỏi"):
    st.session_state.cau_hoi = tao_de_toan(lop, bai)

if st.session_state.cau_hoi:
    de, dap_an, options, goi_y, muc_do = st.session_state.cau_hoi

    st.markdown(f"### ❓ {de}")
    st.caption(f"Mức độ: {muc_do}")

    chon = st.radio("Chọn đáp án:", options)

    if st.button("✅ Kiểm tra"):
        if chon == dap_an:
            st.success("🎉 Chính xác!")
        else:
            st.error(f"❌ Sai rồi. Đáp án đúng là: {dap_an}")
            st.info(f"💡 Gợi ý (Tiếng Việt): {goi_y}")
            st.info(f"🌱 Gợi ý (H’Mông): {dich_hmong(goi_y)}")

st.markdown("---")
st.caption("© 2025 – Gia sư Toán AI cho học sinh vùng cao")
