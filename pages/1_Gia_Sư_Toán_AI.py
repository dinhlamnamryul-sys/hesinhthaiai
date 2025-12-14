import streamlit as st
import random
import re
from deep_translator import GoogleTranslator

# ===============================
# CẤU HÌNH TRANG
# ===============================
st.set_page_config(
    page_title="Gia sư Toán 6 – Bài 1 đến 7",
    layout="wide"
)

# =================================================
# DỊCH TIẾNG MÔNG – GIỮ NGUYÊN CÔNG THỨC TOÁN (LaTeX)
# =================================================
def dich_tieng_mong_giu_latex(text):
    parts = re.split(r'(\$.*?\$)', text)
    ket_qua = []
    for p in parts:
        if p.startswith("$") and p.endswith("$"):
            ket_qua.append(p)
        else:
            if p.strip():
                try:
                    ket_qua.append(
                        GoogleTranslator(source="vi", target="hmn").translate(p)
                    )
                except:
                    ket_qua.append(p)
            else:
                ket_qua.append(p)
    return "".join(ket_qua)

# =================================================
# SINH CÂU HỎI TOÁN 6 – BÀI 1 → 7
# =================================================
def sinh_cau_hoi(bai):

    # ---------- BÀI 1 ----------
    if bai == "Bài 1. Tập hợp":
        tap = sorted(random.sample(range(1, 10), 5))
        x = random.choice(tap)
        cau = "Cách viết nào đúng?"
        dap_an = f"${x} \\in \\{{{';'.join(map(str, tap))}\\}}$"
        lua_chon = [
            dap_an,
            f"${x} \\notin \\{{{';'.join(map(str, tap))}\\}}$",
            f"${tap[0]} \\subset {tap[1]}$",
            f"${tap[0]} \\in ({tap[1]};{tap[2]})$"
        ]
        goi_y = (
            "Dấu $\\in$ dùng để chỉ phần tử thuộc tập hợp. "
            "Dấu $\\subset$ dùng để chỉ tập hợp con."
        )

    # ---------- BÀI 2 ----------
     elif bai == "Bài 2. Cách ghi số tự nhiên":
        tram = random.randint(1, 9)
        chuc = random.randint(0, 9)
        donvi = random.randint(0, 9)

        so = tram * 100 + chuc * 10 + donvi

        # Đọc số bằng chữ (chuẩn SGK Toán 6)
        doc_so = f"{tram} trăm"
        if chuc == 0 and donvi != 0:
            doc_so += " linh"
        elif chuc != 0:
            doc_so += f" {chuc} mươi"
        if donvi != 0:
            doc_so += f" {donvi}"

        cau = f"Số được đọc là “{doc_so}” được viết là:"

        dap_an = f"${so}$"

        lua_chon = [
            dap_an,
            f"${tram * 100 + donvi * 10 + chuc}$",
            f"${tram * 100 + chuc * 10}$",
            f"${tram * 100 + chuc + donvi}$"
        ]

        goi_y = (
            "Số tự nhiên có ba chữ số gồm: "
            "chữ số hàng trăm, hàng chục và hàng đơn vị."
        )


    # ---------- BÀI 3 ----------
    elif bai == "Bài 3. Thứ tự trong tập hợp các số tự nhiên":
        ds = random.sample(range(100, 600), 4)
        cau = f"Số lớn nhất trong các số $ {ds} $ là:"
        dap_an = f"${max(ds)}$"
        lua_chon = [f"${x}$" for x in ds]
        goi_y = (
            "So sánh các số theo thứ tự: hàng trăm → hàng chục → hàng đơn vị."
        )

    # ---------- BÀI 4 ----------
    elif bai == "Bài 4. Phép cộng và phép trừ số tự nhiên":
        a = random.randint(100, 999)
        b = random.randint(100, 999)
        cau = f"Tính $ {a} + {b} $"
        dap_an = f"${a + b}$"
        lua_chon = [
            dap_an,
            f"${a + b + 10}$",
            f"${a + b - 10}$",
            f"${a + b + 1}$"
        ]
        goi_y = (
            "Cộng lần lượt từ hàng đơn vị, nhớ nếu tổng lớn hơn 9."
        )

    # ---------- BÀI 5 ----------
    elif bai == "Bài 5. Phép nhân và phép chia số tự nhiên":
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        cau = f"Tính $ {a} \\times {b} $"
        dap_an = f"${a * b}$"
        lua_chon = [
            dap_an,
            f"${a + b}$",
            f"${a * b + 1}$",
            f"${a * b - 1}$"
        ]
        goi_y = (
            "Phép nhân là phép cộng nhiều lần cùng một số."
        )

    # ---------- BÀI 6 ----------
    elif bai == "Bài 6. Luỹ thừa với số mũ tự nhiên":
        a = random.randint(2, 5)
        cau = f"Tính $ {a}^2 $"
        dap_an = f"${a * a}$"
        lua_chon = [
            dap_an,
            f"${a * 2}$",
            f"${a + 2}$",
            f"${a * a * a}$"
        ]
        goi_y = (
            "Luỹ thừa $a^2$ nghĩa là $a \\times a$."
        )

    # ---------- BÀI 7 ----------
    elif bai == "Bài 7. Thứ tự thực hiện các phép tính":
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        c = random.randint(2, 9)
        cau = f"Tính $ {a} + {b} \\times {c} $"
        dap_an = f"${a + b * c}$"
        lua_chon = [
            dap_an,
            f"${(a + b) * c}$",
            f"${a + b + c}$",
            f"${a * b + c}$"
        ]
        goi_y = (
            "Trong biểu thức: nhân và chia làm trước, cộng và trừ làm sau."
        )

    random.shuffle(lua_chon)
    return cau, dap_an, lua_chon, goi_y

# ===============================
# GIAO DIỆN
# ===============================
st.title("📘 Gia sư Toán 6 – Bài 1 → 7")

BAI_6 = [
    "Bài 1. Tập hợp",
    "Bài 2. Cách ghi số tự nhiên",
    "Bài 3. Thứ tự trong tập hợp các số tự nhiên",
    "Bài 4. Phép cộng và phép trừ số tự nhiên",
    "Bài 5. Phép nhân và phép chia số tự nhiên",
    "Bài 6. Luỹ thừa với số mũ tự nhiên",
    "Bài 7. Thứ tự thực hiện các phép tính"
]

bai = st.selectbox("📚 Chọn bài học:", BAI_6)

if st.button("✨ Tạo câu hỏi mới"):
    cau, dap_an, lua_chon, goi_y = sinh_cau_hoi(bai)
    st.session_state.cau = cau
    st.session_state.dap_an = dap_an
    st.session_state.lua_chon = lua_chon
    st.session_state.goi_y = goi_y

if "cau" in st.session_state:
    st.markdown("### ❓ Câu hỏi")
    st.markdown(st.session_state.cau)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌏 Dịch đề sang tiếng Mông"):
            st.info(dich_tieng_mong_giu_latex(st.session_state.cau))
    with col2:
        if st.button("💡 Gợi ý tiếng Mông"):
            st.info(dich_tieng_mong_giu_latex(st.session_state.goi_y))

    chon = st.radio("✍️ Chọn đáp án:", st.session_state.lua_chon)

    if st.button("✅ Kiểm tra"):
        if chon == st.session_state.dap_an:
            st.success("🎉 Chính xác! (Yog lawm)")
        else:
            st.error("❌ Chưa đúng")
            st.markdown(f"**Đáp án đúng:** {st.session_state.dap_an}")
            st.markdown(f"💡 *Gợi ý:* {st.session_state.goi_y}")
