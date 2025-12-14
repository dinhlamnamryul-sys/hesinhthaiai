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
st.caption("Hỗ trợ học sinh vùng cao | Lớp 6–9")

# ===============================
# HÀM DỊCH GIỮ NGUYÊN CÔNG THỨC
# ===============================
def dich_tieng_mong_giu_latex(text):
    parts = re.split(r'(\$.*?\$)', text)
    ket_qua = []

    for part in parts:
        if part.startswith('$') and part.endswith('$'):
            ket_qua.append(part)
        else:
            if part.strip():
                try:
                    trans = GoogleTranslator(source='vi', target='hmn').translate(part)
                    ket_qua.append(trans)
                except:
                    ket_qua.append(part)
            else:
                ket_qua.append(part)

    return "".join(ket_qua)

# ===============================
# SINH CÂU HỎI LỚP 6
# ===============================
def sinh_cau_hoi_lop_6(bai):
    # ---------- BÀI 1: TẬP HỢP ----------
    if bai == "Bài 1. Tập hợp":
        tap = sorted(random.sample(range(1, 10), 5))
        dung = random.choice(tap)
        sai = random.choice([x for x in range(1, 12) if x not in tap])

        question = f"Cách viết nào đúng với tập hợp $A = \\{{{';'.join(map(str, tap))}\\}}$?"

        dap_an_dung = f"${dung} \\in A$"

        dap_an_sai = [
            f"${sai} \\in A$",
            f"${dung} \\notin A$",
            f"${tap[0]} \\subset {tap[1]}$"
        ]

        options = dap_an_sai + [dap_an_dung]
        random.shuffle(options)

        goi_y_viet = (
            "Dấu ∈ có nghĩa là 'thuộc'. "
            "Muốn biết một số có thuộc tập hợp hay không, "
            "em chỉ cần kiểm tra số đó có nằm trong danh sách các phần tử hay không."
        )

        goi_y_latex = f"{dung} \\in \\{{{';'.join(map(str, tap))}\\}}"

        return question, dap_an_dung, options, goi_y_viet, goi_y_latex

    # ---------- BÀI 6: LŨY THỪA ----------
    if bai == "Bài 6. Lũy thừa":
        a = random.randint(2, 4)
        n = random.randint(2, 3)

        question = f"Tính giá trị của $ {a}^{n} $"

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
            f"${a}^{n}$ nghĩa là lấy {a} nhân với chính nó {n} lần."
        )

        goi_y_latex = f"{a}^{n} = " + " \\times ".join([str(a)] * n)

        return question, dap_an_dung, options, goi_y_viet, goi_y_latex

    return None

# ===============================
# GIAO DIỆN CHỌN BÀI
# ===============================
st.sidebar.header("📚 Chọn bài học")

lop = st.sidebar.selectbox("Chọn lớp", ["Lớp 6"])
bai = st.sidebar.selectbox(
    "Chọn bài",
    ["Bài 1. Tập hợp", "Bài 6. Lũy thừa"]
)

if st.sidebar.button("✨ Tạo câu hỏi"):
    data = sinh_cau_hoi_lop_6(bai)
    if data:
        st.session_state.cau_hoi = data
        st.session_state.da_tra_loi = False

# ===============================
# HIỂN THỊ CÂU HỎI
# ===============================
if "cau_hoi" in st.session_state:
    question, dap_an_dung, options, goi_y_viet, goi_y_latex = st.session_state.cau_hoi

    st.markdown("### ❓ Câu hỏi")
    st.markdown(question)

    # ---- NÚT DỊCH TIẾNG MÔNG ----
    if st.button("🌏 Dịch câu hỏi sang tiếng Mông"):
        st.info(dich_tieng_mong_giu_latex(question))

    # ---- TRẢ LỜI ----
    user_ans = st.radio("Chọn đáp án:", options)

    if st.button("✅ Kiểm tra"):
        st.session_state.da_tra_loi = True

        if user_ans == dap_an_dung:
            st.success("🎉 Chính xác!")
        else:
            st.error(f"❌ Chưa đúng. Đáp án đúng là {dap_an_dung}")

    # ---- GỢI Ý ----
    if st.session_state.get("da_tra_loi", False):
        st.markdown("---")
        st.markdown("### 💡 Gợi ý")

        st.markdown("**Tiếng Việt:**")
        st.write(goi_y_viet)

        st.markdown("**Công thức:**")
        st.latex(goi_y_latex)

        st.markdown("**Tiếng Mông:**")
        st.write(dich_tieng_mong_giu_latex(goi_y_viet))
