import streamlit as st
import random
from utils import CHUONG_TRINH_HOC, tao_de_toan

st.title("📝 Sinh Đề Tự Động")

c1, c2, c3 = st.columns(3)
with c1: lop = st.selectbox("Lớp", list(CHUONG_TRINH_HOC.keys()))
with c2: chuong = st.selectbox("Chủ đề", list(CHUONG_TRINH_HOC[lop].keys()))
with c3: so_cau = st.slider("Số câu", 5, 20, 10)

if st.button("🚀 Sinh đề ngay"):
    de_thi = f"TRƯỜNG PTDTBT TH&THCS NA Ư\nĐỀ ÔN TẬP TOÁN {lop.upper()}\nChủ đề: {chuong}\n" + "="*40 + "\n\n"
    bai_list = CHUONG_TRINH_HOC[lop][chuong]
    list_qa = []
    
    for i in range(so_cau):
        bai = random.choice(bai_list)
        db, qt, da, ops, _, _, _ = tao_de_toan(lop, bai)
        cau = f"Câu {i+1}: {db}\n" + ("\n".join([f"[ ] {o}" for o in ops]) if qt=='mcq' else "Trả lời: .......") + "\n"
        de_thi += cau
        list_qa.append((cau, da))
    
    st.text_area("Xem trước:", value=de_thi, height=300)
    st.download_button("📥 Tải về (TXT)", de_thi, f"De_{lop}.txt")
    
    with st.expander("Xem đáp án (Dành cho giáo viên)"):
        for i, (q, a) in enumerate(list_qa): st.write(f"**Câu {i+1}:** {a}")
