import streamlit as st
import random
from gtts import gTTS
import tempfile
import os
from deep_translator import GoogleTranslator

# ================== CẤU HÌNH ==================
st.set_page_config(
    page_title="Gia sư Toán AI – Bản Mường",
    page_icon="🏔️",
    layout="wide"
)

# ================== DỊCH GỢI Ý H’MÔNG ==================
def dich_hmong(text):
    try:
        return GoogleTranslator(source="vi", target="hmn").translate(text)
    except:
        return "(Không dịch được – kiểm tra mạng)"

# ================== ĐỌC ĐỀ ==================
def doc_de(text):
    tts = gTTS(text=text, lang="vi")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# ================== TRỘN ĐÁP ÁN ==================
def tron_dap_an(dung, sai):
    ds = sai + [dung]
    random.shuffle(ds)
    return ds

# ================== SINH CÂU HỎI ==================
def tao_de_toan(lop):
    # -------- LỚP 6 --------
    if lop == "Lớp 6":
        a = random.randint(2, 5)
        n = random.randint(2, 3)

        de_latex = rf"Tính\ giá\ trị:\ {a}^{{{n}}}"
        dap_an = rf"{a**n}"
        options = tron_dap_an(
            dap_an,
            [rf"{a*n}", rf"{a+n}", rf"{a**(n+1)}"]
        )
        goi_y = "Lũy thừa là nhân số đó với chính nó nhiều lần."

    # -------- LỚP 7 --------
    elif lop == "Lớp 7":
        a = random.randint(2, 9)
        de_latex = rf"Tính:\ (-{a})^2"
        dap_an = rf"{a*a}"
        options = tron_dap_an(
            dap_an,
            [rf"{-a*a}", rf"{a}", rf"{2*a}"]
        )
        goi_y = "Bình phương của số âm là số dương."

    # -------- LỚP 8 --------
    elif lop == "Lớp 8":
        a = random.randint(2, 6)
        de_latex = rf"Rút\ gọn:\ x(x+{a})-x^2"
        dap_an = rf"{a}x"
        options = tron_dap_an(
            dap_an,
            [rf"x^2", rf"{a}", rf"-{a}x"]
        )
        goi_y = "Khai triển rồi thu gọn."

    # -------- LỚP 9 --------
    else:
        a = random.randint(1, 9)
        de_latex = rf"Điều\ kiện\ xác\ định\ của\ \sqrt{{x-{a}}}\ là"
        dap_an = rf"x\ge {a}"
        options = tron_dap_an(
            dap_an,
            [rf"x>{a}", rf"x\le {a}", rf"x<{a}"]
        )
        goi_y = "Biểu thức trong căn bậc hai phải không âm."

    return de_latex, dap_an, options, goi_y

# ================== GIAO DIỆN ==================
st.markdown(
    "<h1 style='text-align:center'>🏫 GIA SƯ TOÁN AI – BẢN MƯỜNG</h1>",
    unsafe_allow_html=True
)

lop = st.selectbox("📘 Chọn lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"])

if st.button("✨ Tạo câu hỏi"):
    st.session_state.cau = tao_de_toan(lop)

if "cau" in st.session_state:
    de, dap_an, options, goi_y = st.session_state.cau

    st.markdown("### ❓ Câu hỏi")
    st.latex(de)

    # ---- ĐỌC ĐỀ ----
    if st.button("🔊 Đọc đề"):
        audio_path = doc_de(de.replace("\\", "").replace("{", "").replace("}", ""))
        st.audio(audio_path)
        os.remove(audio_path)

    chon = st.radio(
        "Chọn đáp án:",
        options,
        format_func=lambda x: f"${x}$"
    )

    if st.button("✅ Kiểm tra"):
        if chon == dap_an:
            st.success("🎉 Chính xác!")
        else:
            st.error("❌ Chưa đúng")
            st.markdown("**Đáp án đúng:**")
            st.latex(dap_an)
            st.info(f"💡 Gợi ý (Việt): {goi_y}")
            st.info(f"🌱 Gợi ý (H’Mông): {dich_hmong(goi_y)}")

st.markdown("---")
st.caption("© 2025 – Gia sư Toán AI cho học sinh vùng cao")
