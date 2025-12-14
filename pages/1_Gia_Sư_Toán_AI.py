import streamlit as st
import random
import re
from deep_translator import GoogleTranslator

# ===============================
# CẤU HÌNH TRANG
# ===============================
st.set_page_config(
    page_title="Gia sư Toán AI - Bản Mường",
    page_icon="🏔️",
    layout="wide"
)

st.title("🏫 GIA SƯ TOÁN AI – BẢN MƯỜNG")
st.caption("Hỗ trợ học sinh vùng cao | Dịch tiếng Mông, giữ nguyên công thức Toán")

# ===============================
# HÀM DỊCH TIẾNG MÔNG (AN TOÀN)
# ===============================
def dich_tieng_mong_giu_latex(text):
    parts = re.split(r'(\$.*?\$)', str(text))
    result = []

    for part in parts:
        # Giữ nguyên công thức LaTeX
        if part.startswith('$') and part.endswith('$'):
            result.append(str(part))
        else:
            if part.strip():
                try:
                    trans = GoogleTranslator(
                        source='vi',
                        target='hmn'
                    ).translate(part)

                    if trans is None:
                        result.append(str(part))
                    else:
                        result.append(str(trans))

                except Exception:
                    result.append(str(part))
            else:
                result.append(str(part))

    return "".join(result)

# ===============================
# SINH CÂU HỎI LỚP 6 (MẪU)
# ===============================
def sinh_cau_hoi_lop_6(bai):
    # -------- BÀI 1: TẬP HỢP --------
    if bai == "Bài 1. Tập hợp":
        tap = sorted(random.sample(range(1, 10), 5))
        dung = random.choice(tap)
        sai = random.choice([x for x in range(1, 12) if x not in tap])

        cau_hoi = (
            f"Cách viết nào đúng với tập hợp "
            f"$A = \\{{{';'.join(map(str, tap))}\\}}$?"
        )

        dap_an_dung = f"${dung} \\in A$"

        options = [
            dap_an_dung,
            f"${sai} \\in A$",
            f"${dung} \\notin A$",
            f"${tap[0]} \\subset {tap[1]}$"
        ]
        random.shuffle(options)

        goi_y_viet = (
            "Dấu $\\in$ có nghĩa là 'thuộc'. "
            "Một số thuộc tập hợp nếu nó xuất hiện trong danh sách "
            "các phần tử của tập hợp đó."
        )

        goi_y_latex = f"{dung} \\in \\{{{';'.join(map(str, tap))}\\}}"

        return cau_hoi, dap_an_dung, options, goi_y_viet, goi_y_latex

    # -------- BÀI 6: LŨY THỪA --------
    if bai == "Bài 6. Lũy thừa":
        a = random.randint(2, 4)
        n = random.randint(2, 3)

        cau_hoi = f"Tính giá trị của $ {a}^{n} $"

        dap_an_dung = str(a ** n)

        options = [
            str(a ** n),
            str(a * n),
            str(a + n),
            str(a ** (n + 1))
        ]
        random.shuffle(options)

        goi_y_viet = (
            "Lũy thừa nghĩa là nhân một số với chính nó nhiều lần. "
            f"$ {a}^{n} $ nghĩa là lấy {a} nhân với chính nó {n} lần."
        )

        goi_y_latex = f"{a}^{n} = " + " \\times ".join([str(a)] * n)

        return cau_hoi, dap_an_dung, options, goi_y_viet, goi_y_latex

    return None

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("📚 Chọn bài học")

lop = st.sidebar.selectbox("Lớp", ["Lớp 6"])
bai = st.sidebar.selectbox(
    "Bài học",
    ["Bài 1. Tập hợp", "Bài 6. Lũy thừa"]
)

if st.sidebar.button("✨ Tạo câu hỏi"):
    data = sinh_cau_hoi_lop_6(bai)
    if data:
        st.session_state.data = data
        st.session_state.checked = False

# ===============================
# HIỂN THỊ CÂU HỎI
# ===============================
if "data" in st.session_state:
    cau_hoi, dap_an_dung, options, goi_y_viet, goi_y_latex = st.session_state.data

    st.markdown("## ❓ Câu hỏi")
    st.markdown(cau_hoi)

    # ---- DỊCH TIẾNG MÔNG ----
    if st.button("🌏 Dịch câu hỏi sang tiếng Mông"):
        st.info(dich_tieng_mong_giu_latex(cau_hoi))

    # ---- TRẢ LỜI ----
    chon = st.radio("Chọn đáp án đúng:", options)

    if st.button("✅ Kiểm tra"):
        st.session_state.checked = True
        if chon == dap_an_dung:
            st.success("🎉 Chính xác! (Yog lawm)")
        else:
            st.error(f"❌ Chưa đúng. Đáp án đúng là {dap_an_dung}")

    # ===============================
    # GỢI Ý
    # ===============================
    if st.session_state.checked:
        st.markdown("---")
        st.markdown("## 💡 Gợi ý")

        st.markdown("### 🇻🇳 Tiếng Việt")
        st.markdown(goi_y_viet)

        st.markdown("### 📐 Công thức Toán")
        st.latex(goi_y_latex)

        st.markdown("### 🏔️ Tiếng Mông")
        st.markdown(dich_tieng_mong_giu_latex(goi_y_viet))
