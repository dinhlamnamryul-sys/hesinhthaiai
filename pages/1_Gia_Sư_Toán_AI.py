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
# SINH CÂU HỎI LỚP 6 (BÀI 1–7)
# ===============================
def sinh_cau_hoi_lop_6(bai):

  # ===== BÀI 1. TẬP HỢP =====
elif bai == "Bài 1. Tập hợp":

    dang = random.choice([1, 2])

    # ---- DẠNG 1: PHẦN TỬ THUỘC TẬP HỢP ----
    if dang == 1:
        tap = sorted(random.sample(range(1, 10), 5))
        x_dung = random.choice(tap)
        x_sai = random.choice([x for x in range(1, 12) if x not in tap])

        cau_hoi = (
            f"Cho tập hợp $A=\\{{{';'.join(map(str, tap))}\\}}$. "
            f"Cách viết nào đúng?"
        )

        dap_an = f"${x_dung}\\in A$"

        options = [
            f"${x_dung}\\in A$",
            f"${x_sai}\\in A$",
            f"${x_dung}\\notin A$",
            f"${tap[0]}\\subset{tap[1]}$"
        ]

        goi_y_viet = (
            "Dấu $\\in$ có nghĩa là 'thuộc'. "
            "Một số thuộc tập hợp nếu nó nằm trong danh sách các phần tử của tập hợp đó."
        )

        goi_y_latex = f"{x_dung}\\in\\{{{';'.join(map(str, tap))}\\}}"

    # ---- DẠNG 2: VIẾT TẬP HỢP ----
    else:
        n = random.randint(4, 7)
        cau_hoi = (
            f"Tập hợp $A$ gồm các số tự nhiên nhỏ hơn ${n}$ là:"
        )

        dap_an = "$A=\\{0;1;2;3\\}$" if n == 4 else f"$A=\\{{0;1;2;\\ldots;{n-1}\\}}$"

        options = [
            dap_an,
            f"$A=\\{{1;2;3;\\ldots;{n}\\}}$",
            f"$A=\\{{1;2;3;\\ldots;{n-1}\\}}$",
            f"$A=\\{{0;1;2;\\ldots;{n}\\}}$"
        ]

        goi_y_viet = (
            "Số tự nhiên bao gồm cả số 0. "
            "Cụm từ 'nhỏ hơn' nghĩa là không lấy số đó."
        )

        goi_y_latex = f"A=\\{{0;1;2;\\ldots;{n-1}\\}}"

    random.shuffle(options)

    return cau_hoi, dap_an, options, goi_y_viet, goi_y_latex

st.sidebar.header("📚 Chọn bài học (Lớp 6)")

bai = st.sidebar.selectbox(
    "Bài học",
    [
        "Bài 1. Tập hợp",
        "Bài 2. Cách ghi số tự nhiên",
        "Bài 3. Thứ tự trong tập hợp các số tự nhiên",
        "Bài 4. Phép cộng và phép trừ số tự nhiên",
        "Bài 5. Phép nhân và phép chia số tự nhiên",
        "Bài 6. Luỹ thừa với số mũ tự nhiên",
        "Bài 7. Thứ tự thực hiện các phép tính"
    ]
)

if st.sidebar.button("✨ Tạo câu hỏi"):
    st.session_state.data = sinh_cau_hoi_lop_6(bai)
    st.session_state.checked = False

# ===============================
# HIỂN THỊ CÂU HỎI
# ===============================
if "data" in st.session_state and st.session_state.data:
    cau_hoi, dap_an, options, goi_y_viet, goi_y_latex = st.session_state.data

    st.markdown("## ❓ Câu hỏi")
    st.markdown(cau_hoi)

    if st.button("🌏 Dịch câu hỏi sang tiếng Mông"):
        st.info(dich_tieng_mong_giu_latex(cau_hoi))

    chon = st.radio("Chọn đáp án:", options)

    if st.button("✅ Kiểm tra"):
        st.session_state.checked = True
        if chon == dap_an:
            st.success("🎉 Chính xác!")
        else:
            st.error(f"❌ Chưa đúng. Đáp án đúng là {dap_an}")

    if st.session_state.checked:
        st.markdown("---")
        st.markdown("## 💡 Gợi ý")
        st.markdown("### 🇻🇳 Tiếng Việt")
        st.markdown(goi_y_viet)

        if goi_y_latex:
            st.markdown("### 📐 Công thức")
            st.latex(goi_y_latex)

        st.markdown("### 🏔️ Tiếng Mông")
        st.markdown(dich_tieng_mong_giu_latex(goi_y_viet))
