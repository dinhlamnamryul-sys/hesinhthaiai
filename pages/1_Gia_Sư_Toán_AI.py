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

    # -------- BÀI 1: TẬP HỢP --------
    if bai == "Bài 1. Tập hợp":
        tap = sorted(random.sample(range(1, 10), 5))
        dung = random.choice(tap)
        sai = random.choice([x for x in range(1, 12) if x not in tap])

        cau_hoi = f"Cách viết nào đúng với tập hợp $A = \\{{{';'.join(map(str, tap))}\\}}$?"
        dap_an = f"${dung} \\in A$"
        options = [
            dap_an,
            f"${sai} \\in A$",
            f"${dung} \\notin A$",
            f"${tap[0]} \\subset {tap[1]}$"
        ]

        goi_y_viet = (
            "Dấu $\\in$ có nghĩa là 'thuộc'. "
            "Một số thuộc tập hợp nếu nó nằm trong danh sách các phần tử."
        )
        goi_y_latex = f"{dung} \\in \\{{{';'.join(map(str, tap))}\\}}"

    # -------- BÀI 2: CÁCH GHI SỐ TỰ NHIÊN --------
    elif bai == "Bài 2. Cách ghi số tự nhiên":
        tram = random.randint(1, 9)
        chuc = random.randint(0, 9)
        donvi = random.randint(0, 9)

        so = tram * 100 + chuc * 10 + donvi
        cau_hoi = f"Số đọc là '{tram} trăm {chuc} chục {donvi} đơn vị' được viết là:"
        dap_an = str(so)

        options = [
            str(so),
            str(tram * 100 + donvi * 10 + chuc),
            str(tram * 10 + chuc * 100 + donvi),
            str(tram * 100 + chuc + donvi * 10)
        ]

        goi_y_viet = (
            "Muốn viết đúng số tự nhiên, em cần xác định chữ số hàng trăm, "
            "hàng chục và hàng đơn vị."
        )
        goi_y_latex = ""

    # -------- BÀI 3: THỨ TỰ SỐ --------
    elif bai == "Bài 3. Thứ tự trong tập hợp các số tự nhiên":
        nums = random.sample(range(100, 999), 4)
        cau_hoi = f"Số lớn nhất trong các số ${', '.join(map(str, nums))}$ là:"
        dap_an = str(max(nums))
        options = list(map(str, nums))

        goi_y_viet = (
            "So sánh các số theo hàng trăm, "
            "nếu bằng nhau thì so tiếp hàng chục."
        )
        goi_y_latex = ""

    # -------- BÀI 4: CỘNG – TRỪ --------
    elif bai == "Bài 4. Phép cộng và phép trừ số tự nhiên":
        a = random.randint(100, 999)
        b = random.randint(100, 999)
        cau_hoi = f"Tính $ {a} + {b} $"
        dap_an = str(a + b)
        options = [
            str(a + b),
            str(a + b + 10),
            str(a + b - 10),
            str(abs(a - b))
        ]

        goi_y_viet = (
            "Cộng các chữ số cùng hàng từ phải sang trái, "
            "nhớ cộng thêm nếu có nhớ."
        )
        goi_y_latex = f"{a} + {b} = {a + b}"

   elif bai == "Bài 5. Phép nhân và phép chia số tự nhiên":
    a = random.randint(2, 9)
    b = random.randint(2, 9)

    cau_hoi = f"Tính ${a}\\times{b}$"
    dap_an = str(a * b)

    options = [
        str(a * b),
        str(a + b),
        str(a * b + a),
        str(a * b - b)
    ]

    goi_y_viet = (
        "Phép nhân là phép cộng lặp lại nhiều lần."
    )
    goi_y_latex = f"{a}\\times{b}={a*b}"

   elif bai == "Bài 6. Luỹ thừa với số mũ tự nhiên":
    a = random.randint(2, 4)
    n = random.randint(2, 3)

    cau_hoi = f"Tính ${a}^{{{n}}}$"
    dap_an = str(a ** n)

    options = [
        str(a ** n),
        str(a * n),
        str(a + n),
        str(a ** (n + 1))
    ]

    goi_y_viet = "Lũy thừa là nhân một số với chính nó nhiều lần."
    goi_y_latex = f"{a}^{{{n}}}=" + " \\times ".join([str(a)] * n)

   elif bai == "Bài 7. Thứ tự thực hiện các phép tính":
    a, b, c = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)

    cau_hoi = f"Tính ${a}+{b}\\times{c}$"
    dap_an = str(a + b * c)

    options = [
        str(a + b * c),
        str((a + b) * c),
        str(a * b + c),
        str(a + b + c)
    ]

    goi_y_viet = (
        "Trong biểu thức không có ngoặc, thực hiện phép nhân trước, phép cộng sau."
    )
    goi_y_latex = f"{a}+{b}\\times{c}={a}+{b*c}"

# ===============================
# SIDEBAR
# ===============================
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
