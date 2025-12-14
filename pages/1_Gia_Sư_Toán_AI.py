import streamlit as st
import random
import re
from deep_translator import GoogleTranslator

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Gia sư Toán 6 – Bài 1 đến 7",
    layout="wide"
)

# =================================================
# DỊCH TIẾNG MÔNG – GIỮ NGUYÊN CÔNG THỨC TOÁN
# =================================================
def dich_tieng_mong_giu_latex(text):
    parts = re.split(r'(\$.*?\$)', text)
    result = []
    for p in parts:
        if p.startswith("$") and p.endswith("$"):
            result.append(p)
        else:
            if p.strip():
                try:
                    result.append(
                        GoogleTranslator(source="vi", target="hmn").translate(p)
                    )
                except:
                    result.append(p)
            else:
                result.append(p)
    return "".join(result)

# =================================================
# SINH CÂU HỎI TOÁN 6
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
            "Dấu $\\in$ chỉ phần tử thuộc tập hợp. "
            "Dấu $\\subset$ chỉ tập hợp con."
        )

    # ---------- BÀI 2 ----------
    elif bai == "Bài 2. Cách ghi số tự nhiên":
        tram = random.randint(1, 9)
        chuc = random.randint(0, 9)
        donvi = random.randint(0, 9)

        so = tram * 100 + chuc * 10 + donvi

        # Chuyển số sang chữ (chuẩn SGK)
        chu_so = {
            0: "không", 1: "một", 2: "hai", 3: "ba", 4: "bốn",
            5: "năm", 6: "sáu", 7: "bảy", 8: "tám", 9: "chín"
        }

        doc_so = chu_so[tram] + " trăm"

        if chuc == 0 and donvi != 0:
            doc_so += " linh"
        elif chuc != 0:
            doc_so += " " + chu_so[chuc] + " mươi"

        if donvi != 0:
            if donvi == 5 and chuc != 0:
                doc_so += " lăm"
            else:
                doc_so += " " + chu_so[donvi]

        cau = f"Số được đọc là “{doc_so}” được viết là:"

        dap_an = f"${so}$"

        lua_chon = [
            dap_an,
            f"${tram * 100 + donvi * 10 + chuc}$",
            f"${tram * 100 + chuc * 10}$",
            f"${tram * 100 + chuc + donvi}$"
        ]

        goi_y = (
            "Xác định chữ số hàng trăm, hàng chục và hàng đơn vị rồi viết số."
        )
    # ---------- BÀI 3 ----------
    elif bai == "Bài 3. Thứ tự trong tập hợp các số tự nhiên":
        ds = random.sample(range(100, 999), 4)
        cau = f"Số lớn nhất trong các số $ {ds} $ là:"
        dap_an = f"${max(ds)}$"
        lua_chon = [f"${x}$" for x in ds]

        goi_y = (
            "So sánh từ hàng trăm, rồi đến hàng chục, hàng đơn vị."
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
            "Cộng từ phải sang trái, nhớ nếu tổng lớn hơn 9."
        )

    # ---------- BÀI 5 ----------
   elif bai == "Bài 5. Phép nhân và phép chia số tự nhiên":
    dang = random.choice(["nhan", "chia"])

    if dang == "nhan":
        a = random.randint(6, 15)
        b = random.randint(6, 15)

        cau = (
            "Kết quả của:\n\n"
            f"$ {a} \\times {b} $\n\n"
            "là:"
        )

        dap_an = a * b

        lua_chon = [
            dap_an,
            dap_an + random.choice([-12, -10, 10, 12]),
            dap_an + random.choice([-8, 8]),
            dap_an + random.choice([-2, 2])
        ]

        goi_y = "Thực hiện phép nhân hai số tự nhiên."

    else:
        b = random.randint(6, 15)
        k = random.randint(6, 15)
        a = b * k

        cau = f"$ {a} \\div {b} = $"

        dap_an = k

        lua_chon = [
            dap_an,
            dap_an + 1,
            dap_an - 1,
            dap_an + 2
        ]

        goi_y = "Thực hiện phép chia số tự nhiên."

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
            "Thực hiện phép nhân trước, phép cộng sau."
        )

    else:
        cau, dap_an, lua_chon, goi_y = "", "", [], ""

    random.shuffle(lua_chon)
    return cau, dap_an, lua_chon, goi_y

# =========================
# GIAO DIỆN
# =========================
st.title("📘 Gia sư Toán 6 – Bài 1 đến 7")

DS_BAI = [
    "Bài 1. Tập hợp",
    "Bài 2. Cách ghi số tự nhiên",
    "Bài 3. Thứ tự trong tập hợp các số tự nhiên",
    "Bài 4. Phép cộng và phép trừ số tự nhiên",
    "Bài 5. Phép nhân và phép chia số tự nhiên",
    "Bài 6. Luỹ thừa với số mũ tự nhiên",
    "Bài 7. Thứ tự thực hiện các phép tính"
]

bai = st.selectbox("📚 Chọn bài:", DS_BAI)

if st.button("✨ Tạo câu hỏi"):
    st.session_state.cau, st.session_state.dap_an, \
    st.session_state.lua_chon, st.session_state.goi_y = sinh_cau_hoi(bai)

if "cau" in st.session_state:
    st.markdown("### ❓ Câu hỏi")
    st.markdown(st.session_state.cau)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌏 Dịch sang tiếng Mông"):
            st.info(dich_tieng_mong_giu_latex(st.session_state.cau))
    with col2:
        if st.button("💡 Gợi ý tiếng Mông"):
            st.info(dich_tieng_mong_giu_latex(st.session_state.goi_y))

    chon = st.radio("✍️ Chọn đáp án:", st.session_state.lua_chon)

    if st.button("✅ Kiểm tra"):
        if chon == st.session_state.dap_an:
            st.success("🎉 Chính xác!")
        else:
            st.error("❌ Chưa đúng")
            st.markdown(f"**Đáp án đúng:** {st.session_state.dap_an}")
            st.markdown(f"💡 *Gợi ý:* {st.session_state.goi_y}")
