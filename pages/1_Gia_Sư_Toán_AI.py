import streamlit as st
import random
import re
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Gia sư Toán 6 AI", layout="wide")

# =========================
# DỊCH TIẾNG MÔNG GIỮ LATEX
# =========================
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

# =========================
# SINH CÂU HỎI TOÁN 6
# =========================
def sinh_cau_hoi(bai):
    # -------- CHƯƠNG I --------
    if bai == "Bài 1. Tập hợp":
        tap = sorted(random.sample(range(1,10),5))
        x = random.choice(tap)
        cau = f"Cách viết nào đúng?"
        dap_an = f"${x} \\in \\{{{';'.join(map(str,tap))}\\}}$"
        lua_chon = [
            dap_an,
            f"${x} \\notin \\{{{';'.join(map(str,tap))}\\}}$",
            f"${tap[0]} \\subset {tap[1]}$",
            f"${tap[0]} \\in ({tap[1]};{tap[2]})$"
        ]
        goi_y = "Phần tử thuộc tập hợp được ký hiệu là $\\in$."
    
    elif bai == "Bài 2. Cách ghi số tự nhiên":
        a = random.randint(100,999)
        cau = f"Số ${a}$ được đọc là?"
        dap_an = f"${a}$"
        lua_chon = [dap_an,
                    f"${a+10}$",
                    f"${a-10}$",
                    f"${a*10}$"]
        goi_y = "Đọc theo thứ tự: trăm – chục – đơn vị."

    elif bai == "Bài 3. Thứ tự trong tập hợp các số tự nhiên":
        ds = random.sample(range(100,600),4)
        cau = f"Số lớn nhất trong các số ${ds}$ là?"
        dap_an = f"${max(ds)}$"
        lua_chon = [f"${x}$" for x in ds]
        goi_y = "So sánh chữ số hàng trăm trước."

    elif bai == "Bài 4. Phép cộng và phép trừ số tự nhiên":
        a,b = random.randint(100,999), random.randint(100,999)
        cau = f"Tính $ {a}+{b} $"
        dap_an = f"${a+b}$"
        lua_chon = [dap_an,f"${a+b+10}$",f"${a+b-10}$",f"${a+b+1}$"]
        goi_y = "Cộng lần lượt từ hàng đơn vị."

    elif bai == "Bài 5. Phép nhân và phép chia số tự nhiên":
        a,b = random.randint(2,9), random.randint(2,9)
        cau = f"Tính $ {a}\\times {b} $"
        dap_an = f"${a*b}$"
        lua_chon = [dap_an,f"${a+b}$",f"${a*b+1}$",f"${a*b-1}$"]
        goi_y = "Phép nhân là cộng nhiều lần."

    elif bai == "Bài 6. Luỹ thừa với số mũ tự nhiên":
        a = random.randint(2,5)
        cau = f"Tính $ {a}^2 $"
        dap_an = f"${a*a}$"
        lua_chon = [dap_an,f"${a*2}$",f"${a+2}$",f"${a*a*a}$"]
        goi_y = "Luỹ thừa là nhân số đó với chính nó."

    elif bai == "Bài 7. Thứ tự thực hiện các phép tính":
        a,b,c = random.randint(2,9),random.randint(2,9),random.randint(2,9)
        cau = f"Tính $ {a}+{b}\\times {c} $"
        dap_an = f"${a+b*c}$"
        lua_chon = [dap_an,f"${(a+b)*c}$",f"${a+b+c}$",f"${a*b+c}$"]
        goi_y = "Thực hiện nhân trước, cộng sau."

    # -------- CHƯƠNG II --------
    elif bai == "Bài 10. Số nguyên tố":
        so = random.choice([11,13,17,19])
        cau = "Số nào sau đây là số nguyên tố?"
        dap_an = f"${so}$"
        lua_chon = [dap_an,"$9$","$15$","$21$"]
        goi_y = "Số nguyên tố chỉ có 2 ước."

    # -------- CHƯƠNG III --------
    elif bai == "Bài 14. Phép cộng và phép trừ số nguyên":
        a,b = random.randint(-10,-1),random.randint(1,10)
        cau = f"Tính $ {a}+{b} $"
        dap_an = f"${a+b}$"
        lua_chon = [dap_an,f"${a-b}$",f"${b-a}$",f"${abs(a+b)}$"]
        goi_y = "Cộng số âm và số dương."

    # -------- CHƯƠNG VI --------
    elif bai == "Bài 25. Phép cộng và phép trừ phân số":
        cau = "Tính $ \\frac{1}{4}+\\frac{1}{4} $"
        dap_an = "$\\frac{1}{2}$"
        lua_chon = [dap_an,"$\\frac{2}{8}$","$\\frac{1}{4}$","$\\frac{3}{4}$"]
        goi_y = "Cộng phân số cùng mẫu."

    # -------- CHƯƠNG VII --------
    elif bai == "Bài 28. Số thập phân":
        cau = "Số $0,75$ bằng phân số nào?"
        dap_an = "$\\frac{3}{4}$"
        lua_chon = [dap_an,"$\\frac{1}{2}$","$\\frac{75}{10}$","$\\frac{7}{5}$"]
        goi_y = "Đổi số thập phân ra phân số."

    # -------- CHƯƠNG VIII --------
    elif bai == "Bài 36. Góc":
        cau = "Góc vuông có số đo là?"
        dap_an = "$90^\\circ$"
        lua_chon = [dap_an,"$45^\\circ$","$60^\\circ$","$180^\\circ$"]
        goi_y = "Góc vuông bằng 90 độ."

    # -------- CHƯƠNG IX --------
    elif bai == "Bài 40. Biểu đồ cột":
        cau = "Biểu đồ dùng để so sánh số liệu là?"
        dap_an = "$\\text{Biểu đồ cột}$"
        lua_chon = [dap_an,"$\\text{Biểu đồ tranh}$","$\\text{Bảng số liệu}$","$\\text{Văn bản}$"]
        goi_y = "Biểu đồ cột so sánh số lượng."

    else:
        cau = "Câu hỏi đang được cập nhật."
        dap_an = "$0$"
        lua_chon = ["$0$"]
        goi_y = ""

    random.shuffle(lua_chon)
    return cau, dap_an, lua_chon, goi_y

# =========================
# GIAO DIỆN
# =========================
st.title("📘 Gia sư Toán 6 AI – Chuẩn SGK Kết nối tri thức")

BAI_6 = [
"Bài 1. Tập hợp","Bài 2. Cách ghi số tự nhiên","Bài 3. Thứ tự trong tập hợp các số tự nhiên",
"Bài 4. Phép cộng và phép trừ số tự nhiên","Bài 5. Phép nhân và phép chia số tự nhiên",
"Bài 6. Luỹ thừa với số mũ tự nhiên","Bài 7. Thứ tự thực hiện các phép tính",
"Bài 10. Số nguyên tố","Bài 14. Phép cộng và phép trừ số nguyên",
"Bài 25. Phép cộng và phép trừ phân số","Bài 28. Số thập phân",
"Bài 36. Góc","Bài 40. Biểu đồ cột"
]

bai = st.selectbox("📚 Chọn bài học:", BAI_6)

if st.button("✨ Tạo câu hỏi"):
    cau, dap_an, lua_chon, goi_y = sinh_cau_hoi(bai)
    st.session_state.cau = cau
    st.session_state.dap_an = dap_an
    st.session_state.lua_chon = lua_chon
    st.session_state.goi_y = goi_y

if "cau" in st.session_state:
    st.markdown("### ❓ Câu hỏi")
    st.markdown(st.session_state.cau)

    if st.button("🌏 Dịch tiếng Mông"):
        st.info(dich_tieng_mong_giu_latex(st.session_state.cau))

    chon = st.radio("Chọn đáp án:", st.session_state.lua_chon)

    if st.button("✅ Kiểm tra"):
        if chon == st.session_state.dap_an:
            st.success("Chính xác 🎉")
        else:
            st.error("Chưa đúng")
            st.markdown(f"**Đáp án đúng:** {st.session_state.dap_an}")
            st.markdown(f"💡 *Gợi ý:* {st.session_state.goi_y}")
