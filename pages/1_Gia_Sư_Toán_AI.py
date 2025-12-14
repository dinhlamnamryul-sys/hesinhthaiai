import streamlit as st
import random
import math
import time
import os
import pandas as pd
import io
import base64
import re
from deep_translator import GoogleTranslator
from gtts import gTTS

# ================== CẤU HÌNH ==================
st.set_page_config(
    page_title="Gia sư Toán AI - Bản Mường (Lớp 1-9)",
    page_icon="🏔️",
    layout="wide"
)

# ================== HÀM TRỘN ĐÁP ÁN ==================
def tron_dap_an(dung, sai):
    ds = sai + [dung]
    random.shuffle(ds)
    return ds

# ================== ĐẾM TRUY CẬP ==================
def update_visit_count():
    f = "visit_count.txt"
    if not os.path.exists(f):
        with open(f, "w") as w:
            w.write("1000")
    with open(f, "r") as r:
        n = int(r.read())
    n += 1
    with open(f, "w") as w:
        w.write(str(n))
    return n

if "visit_count" not in st.session_state:
    st.session_state.visit_count = update_visit_count()

# ================== LOGIC SINH ĐỀ ==================
def tao_de_toan(lop, bai_hoc):
    question_type = "mcq"
    de_latex = ""
    dap_an = ""
    options = []
    goi_y_text = ""
    goi_y_latex = ""

    bai = bai_hoc.lower()

    # ========== LỚP 6 ==========
    if "lớp 6" in lop.lower():

        # ----- BÀI 1: TẬP HỢP -----
        if "bài 1" in bai or "tập hợp" in bai:
            if random.choice([0, 1]) == 0:
                tap = sorted(random.sample(range(1, 10), 5))
                dung = random.choice(tap)
                sai = random.choice([x for x in range(1, 12) if x not in tap])

                dap_an = f"{dung} ∈ {{{';'.join(map(str, tap))}}}"
                options = tron_dap_an(dap_an, [
                    f"{sai} ∈ {{{';'.join(map(str, tap))}}}",
                    f"{dung} ∉ {{{';'.join(map(str, tap))}}}",
                    f"{tap[0]} ⊂ {tap[1]}"
                ])

                de_latex = "Cách viết nào đúng?"
                goi_y_text = f"{dung} là phần tử của tập hợp đã cho."

            else:
                n = random.randint(3, 7)
                dap_an = "{" + ";".join(map(str, range(0, n))) + "}"
                options = tron_dap_an(dap_an, [
                    "{" + ";".join(map(str, range(1, n))) + "}",
                    "{" + ";".join(map(str, range(0, n+1))) + "}",
                    "{" + ";".join(map(str, range(1, n+1))) + "}"
                ])
                de_latex = f"Tập hợp A = {{x | x là số tự nhiên nhỏ hơn {n}}} là:"
                goi_y_text = f"Số tự nhiên nhỏ hơn {n} gồm từ 0 đến {n-1}."

        # ----- BÀI 6: LŨY THỪA -----
        elif "bài 6" in bai or "lũy thừa" in bai:
            a = random.randint(2, 4)
            n = random.randint(2, 3)
            dap_an = str(a ** n)
            options = tron_dap_an(dap_an, [
                str(a * n),
                str(a + n),
                str(a ** (n + 1))
            ])
            de_latex = f"Tính giá trị: ${a}^{n}$"
            goi_y_text = "Lũy thừa là nhân số đó với chính nó nhiều lần."

        # ----- DỰ PHÒNG -----
        else:
            a, b = random.randint(10, 99), random.randint(10, 99)
            dap_an = str(a + b)
            options = tron_dap_an(dap_an, [str(a+b+1), str(a+b-1), str(a+b+2)])
            de_latex = f"Tính: {a} + {b}"
            goi_y_text = "Cộng hai số tự nhiên."

    # ========== LỚP KHÁC ==========
    else:
        a, b = random.randint(1, 20), random.randint(1, 20)
        dap_an = str(a + b)
        options = tron_dap_an(dap_an, [str(a+b+1), str(a+b-1), str(a+b+2)])
        de_latex = f"Tính: {a} + {b}"
        goi_y_text = "Cộng hai số."

    return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex

# ================== GIAO DIỆN ==================
st.markdown(f"""
<h1 style='text-align:center'>🏫 GIA SƯ TOÁN AI – BẢN MƯỜNG</h1>
<p style='text-align:center'>Lượt truy cập: {st.session_state.visit_count}</p>
<hr>
""", unsafe_allow_html=True)

lop_chon = st.selectbox("Chọn lớp:", ["Lớp 6"])
bai_chon = st.selectbox("Chọn bài:", [
    "Bài 1. Tập hợp",
    "Bài 6. Lũy thừa với số mũ tự nhiên"
])

if "de" not in st.session_state:
    st.session_state.de = ""

if st.button("✨ Tạo câu hỏi mới"):
    st.session_state.de = tao_de_toan(lop_chon, bai_chon)

if st.session_state.de:
    de, qtype, dap_an, ops, gy, _ = st.session_state.de
    st.markdown(f"### ❓ {de}")
    user = st.radio("Chọn đáp án:", ops)

    if st.button("✅ Kiểm tra"):
        if user == dap_an:
            st.success("🎉 Chính xác!")
            st.balloons()
        else:
            st.error(f"Sai rồi ❌ — Đáp án đúng: {dap_an}")
            st.info(f"💡 Gợi ý: {gy}")

st.markdown("---")
st.caption("© 2025 – PTDTBT TH&THCS Na Ư")
