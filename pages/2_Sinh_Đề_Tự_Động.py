import requests
import streamlit as st
from datetime import datetime
import base64
from io import BytesIO

# ===============================
# 🔑 CẤU HÌNH TRANG & API KEY
# ===============================
st.set_page_config(page_title="Hệ Sinh Đề Toán Thông Minh", layout="wide")

with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key:
1. Truy cập: **https://aistudio.google.com/app/apikey**
2. Nhấn **Create API key**.
3. Copy API Key và dán vào ô bên dưới.
""")

st.subheader("🔐 Cấu hình hệ thống:")
api_key = st.text_input("Nhập Google API Key:", type="password")

# ===============================
# 📚 DỮ LIỆU CHƯƠNG TRÌNH HỌC ĐẦY ĐỦ
# ===============================
chuong_options_lop = {
    "Lớp 6": ["Chương I: Tập hợp các số tự nhiên", "Chương II: Tính chia hết trong tập hợp các số tự nhiên", "Chương III: Số nguyên", "Chương IV: Một số hình phẳng trong thực tiễn", "Chương V: Tính đối xứng của hình phẳng trong tự nhiên", "Chương VI: Phân số", "Chương VII: Số thập phân", "Chương VIII: Những hình hình học cơ bản", "Chương IX: Dữ liệu và xác suất thực nghiệm", "Hoạt động thực hành trải nghiệm"],
    "Lớp 7": ["Chương I: Số hữu tỉ", "Chương II: Số thực", "Chương III: Góc và đường thẳng song song", "Chương IV: Tam giác bằng nhau", "Chương V: Thu thập và biểu diễn dữ liệu", "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ", "Chương VII: Biểu thức đại số và đa thức một biến", "Chương VIII: Làm quen với biến cố và xác suất", "Chương IX: Quan hệ giữa các yếu tố trong một tam giác", "Chương X: Một số hình khối trong thực tiễn", "Bài tập ôn tập cuối năm"],
    "Lớp 8": ["Chương I: Đa thức", "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng", "Chương III: Tứ giác", "Chương IV: Định lí Thalès", "Chương V: Dữ liệu và biểu đồ", "Chương VI: Phân thức đại số", "Chương VII: Phương trình bậc nhất và hàm số bậc nhất", "Chương VIII: Mở đầu về tính xác suất của biến cố", "Chương IX: Tam giác đồng dạng", "Chương X: Một số hình khối trong thực tiễn", "Bài tập ôn tập cuối năm"],
    "Lớp 9": ["Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn", "Chương II: Phương trình và bất phương trình bậc nhất một ẩn", "Chương III: Căn bậc hai và căn bậc ba", "Chương IV: Hệ thức lượng trong tam giác vuông", "Chương V: Đường tròn", "Hoạt động thực hành trải nghiệm", "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn", "Chương VII: Tần số và tần số tương đối", "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản", "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp", "Chương X: Một số hình khối trong thực tiễn"]
}

bai_options_lop = {
    "Lớp 6": {
        "Chương I: Tập hợp các số tự nhiên": ["Bài 1","Bài 2","Bài 3","Bài 4","Ôn tập"],
        "Chương II: Tính chia hết trong tập hợp các số tự nhiên": ["Bài 5","Bài 6","Ôn tập"],
        "Chương III: Số nguyên": ["Bài 7","Bài 8","Ôn tập"],
        "Chương IV: Một số hình phẳng trong thực tiễn": ["Bài 9","Bài 10","Ôn tập"],
        "Chương V: Tính đối xứng của hình phẳng trong tự nhiên": ["Bài 11","Bài 12","Ôn tập"],
        "Chương VI: Phân số": ["Bài 13","Bài 14","Ôn tập"],
        "Chương VII: Số thập phân": ["Bài 15","Bài 16","Ôn tập"],
        "Chương VIII: Những hình hình học cơ bản": ["Bài 17","Bài 18","Ôn tập"],
        "Chương IX: Dữ liệu và xác suất thực nghiệm": ["Bài 19","Bài 20","Ôn tập"],
        "Hoạt động thực hành trải nghiệm": ["Bài 21","Bài 22","Ôn tập"]
    },
    "Lớp 7": {
        "Chương I: Số hữu tỉ": ["Bài 1. Tập hợp các số hữu tỉ","Bài 2. Cộng, trừ, nhân, chia số hữu tỉ","Bài 3. Luỹ thừa với số mũ tự nhiên của một số hữu tỉ","Bài 4. Thứ tự thực hiện các phép tính. Quy tắc chuyển vế","Ôn tập chương I"],
        "Chương II: Số thực": ["Bài 5. Làm quen với số thập phân vô hạn tuần hoàn","Bài 6. Số vô tỉ. Căn bậc hai số học","Bài 7. Tập hợp các số thực","Ôn tập chương II"],
        "Chương III: Góc và đường thẳng song song": ["Bài 8. Góc ở vị trí đặc biệt. Tia phân giác của một góc","Bài 9. Hai đường thẳng song song và dấu hiệu nhận biết","Bài 10. Tiên đề Euclid. Tính chất của hai đường thẳng song song","Bài 11. Định lí và chứng minh định lí","Ôn tập chương III"],
        "Chương IV: Tam giác bằng nhau": ["Bài 12. Tổng các góc trong một tam giác","Bài 13. Hai tam giác bằng nhau. Trường hợp bằng nhau thứ nhất của tam giác","Bài 14. Trường hợp bằng nhau thứ hai và thứ ba của tam giác","Bài 15. Các trường hợp bằng nhau của tam giác vuông","Bài 16. Tam giác cân. Đường trung trực của đoạn thẳng","Ôn tập chương IV"],
        "Chương V: Thu thập và biểu diễn dữ liệu": ["Bài 17. Thu thập và phân loại dữ liệu","Bài 18. Biểu đồ hình quạt tròn","Bài 19. Biểu đồ đoạn thẳng","Ôn tập chương V"],
        "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ": ["Bài 20. Tỉ lệ thức","Bài 21. Tính chất của dãy tỉ số bằng nhau","Bài 22. Đại lượng tỉ lệ thuận","Bài 23. Đại lượng tỉ lệ nghịch","Ôn tập chương VI"],
        "Chương VII: Biểu thức đại số và đa thức một biến": ["Bài 24. Biểu thức đại số","Bài 25. Đa thức một biến","Bài 26. Phép cộng và phép trừ đa thức một biến","Bài 27. Phép nhân đa thức một biến","Bài 28. Phép chia đa thức một biến","Ôn tập chương VII"],
        "Chương VIII: Làm quen với biến cố và xác suất": ["Bài 29. Làm quen với biến cố","Bài 30. Làm quen với xác suất của biến cố","Ôn tập chương VIII"],
        "Chương IX: Quan hệ giữa các yếu tố trong một tam giác": ["Bài 31. Quan hệ giữa góc và cạnh đối diện trong một tam giác","Bài 32. Quan hệ giữa đường vuông góc và đường xiên","Bài 33. Quan hệ giữa ba cạnh của một tam giác","Bài 34. Sự đồng quy của ba đường trung tuyến, ba đường phân giác trong một tam giác","Bài 35. Sự đồng quy của ba đường trung trực, ba đường cao trong một tam giác","Ôn tập chương IX"],
        "Chương X: Một số hình khối trong thực tiễn": ["Bài 36. Hình hộp chữ nhật và hình lập phương","Bài 37. Hình lăng trụ đứng tam giác và hình lăng trụ đứng tứ giác","Ôn tập chương X"],
        "Bài tập ôn tập cuối năm": ["Ôn tập cuối năm"]
    },
    "Lớp 8": {
        "Chương I: Đa thức": ["Bài 1. Đơn thức","Bài 2. Đa thức","Bài 3. Phép cộng và phép trừ đa thức","Bài 4. Phép nhân đa thức","Bài 5. Phép chia đa thức cho đơn thức","Ôn tập chương I"],
        "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng": ["Bài 6. Hiệu hai bình phương. Bình phương của một tổng hay một hiệu","Bài 7. Lập phương của một tổng. Lập phương của một hiệu","Bài 8. Tổng và hiệu hai lập phương","Bài 9. Phân tích đa thức thành nhân tử","Ôn tập chương II"],
        "Chương III: Tứ giác": ["Bài 10. Tứ giác","Bài 11. Hình thang cân","Bài 12. Hình bình hành","Bài 13. Hình chữ nhật","Bài 14. Hình thoi và hình vuông","Ôn tập chương III"],
        "Chương IV: Định lí Thalès": ["Bài 15. Định lí Thalès trong tam giác","Bài 16. Đường trung bình của tam giác","Bài 17. Tính chất đường phân giác của tam giác","Ôn tập chương IV"],
        "Chương V: Dữ liệu và biểu đồ": ["Bài 18. Thu thập và phân loại dữ liệu","Bài 19. Biểu diễn dữ liệu bằng bảng, biểu đồ","Bài 20. Phân tích số liệu thống kê dựa vào biểu đồ","Ôn tập chương V"],
        "Chương VI: Phân thức đại số": ["Bài 21. Phân thức đại số","Bài 22. Tính chất cơ bản của phân thức đại số","Bài 23. Phép cộng và phép trừ phân thức đại số","Bài 24. Phép nhân và phép chia phân thức đại số","Ôn tập chương VI"],
        "Chương VII: Phương trình bậc nhất và hàm số bậc nhất": ["Bài 25. Phương trình bậc nhất một ẩn","Bài 26. Giải bài toán bằng cách lập phương trình","Bài 27. Khái niệm hàm số và đồ thị của hàm số","Bài 28. Hàm số bậc nhất và đồ thị của hàm số bậc nhất","Bài 29. Hệ số góc của đường thẳng","Ôn tập chương VII"],
        "Chương VIII: Mở đầu về tính xác suất của biến cố": ["Bài 30. Kết quả có thể và kết quả thuận lợi","Bài 31. Cách tính xác suất của biến cố bằng tỉ số","Bài 32. Mối liên hệ giữa xác suất thực nghiệm với xác suất và ứng dụng","Ôn tập chương VIII"],
        "Chương IX: Tam giác đồng dạng": ["Bài 33. Hai tam giác đồng dạng","Bài 34. Ba trường hợp đồng dạng của hai tam giác","Bài 35. Định lí Pythagore và ứng dụng","Bài 36. Các trường hợp đồng dạng của hai tam giác vuông","Bài 37. Hình đồng dạng","Ôn tập chương IX"],
        "Chương X: Một số hình khối trong thực tiễn": ["Bài 38. Hình chóp tam giác đều","Bài 39. Hình chóp tứ giác đều","Ôn tập chương X"],
        "Bài tập ôn tập cuối năm": ["Ôn tập cuối năm"]
    },
    "Lớp 9": {
        "Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn": ["Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn","Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn","Luyện tập chung","Bài 3. Giải bài toán bằng cách lập hệ phương trình","Bài tập cuối chương I"],
        "Chương II: Phương trình và bất phương trình bậc nhất một ẩn": ["Bài 4. Phương trình quy về phương trình bậc nhất một ẩn","Bài 5. Bất đẳng thức và tính chất","Luyện tập chung","Bài 6. Bất phương trình bậc nhất một ẩn","Bài tập cuối chương II"],
        "Chương III: Căn bậc hai và căn bậc ba": ["Bài 7. Căn bậc hai và căn thức bậc hai","Bài 8. Khai căn bậc hai với phép nhân và phép chia","Luyện tập chung","Bài 9. Biến đổi đơn giản và rút gọn biểu thức chứa căn thức bậc hai","Bài 10. Căn bậc ba và căn thức bậc ba","Luyện tập chung","Bài tập cuối chương III"],
        "Chương IV: Hệ thức lượng trong tam giác vuông": ["Bài 11. Tỉ số lượng giác của góc nhọn","Bài 12. Một số hệ thức giữa cạnh, góc trong tam giác vuông và ứng dụng","Luyện tập chung","Bài tập cuối chương IV"],
        "Chương V: Đường tròn": ["Bài 13. Mở đầu về đường tròn","Bài 14. Cung và dây của một đường tròn","Bài 15. Độ dài của cung tròn. Diện tích hình quạt tròn và hình vành khuyên","Luyện tập chung","Bài 16. Vị trí tương đối của đường thẳng và đường tròn","Bài 17. Vị trí tương đối của hai đường tròn","Luyện tập chung","Bài tập cuối chương V"],
        "Hoạt động thực hành trải nghiệm": ["Pha chế dung dịch theo nồng độ yêu cầu","Tính chiều cao và xác định khoảng cách"],
        "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn": ["Bài 18. Hàm số y = ax2 (a ≠ 0)","Bài 19. Phương trình bậc hai một ẩn","Luyện tập chung","Bài 20. Định lí Viète và ứng dụng","Bài 21. Giải bài toán bằng cách lập phương trình","Luyện tập chung","Bài tập cuối chương VI"],
        "Chương VII: Tần số và tần số tương đối": ["Bài 22. Bảng tần số và biểu đồ tần số","Bài 23. Bảng tần số tương đối và biểu đồ tần số tương đối","Luyện tập chung","Bài 24. Bảng tần số, tần số tương đối ghép nhóm và biểu đồ","Bài tập cuối chương VII"],
        "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản": ["Bài 25. Phép thử ngẫu nhiên và không gian mẫu","Bài 26. Xác suất của biến cố liên quan tới phép thử","Luyện tập chung","Bài tập cuối chương VIII"],
        "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp": ["Bài 27. Góc nội tiếp","Bài 28. Đường tròn ngoại tiếp và đường tròn nội tiếp của một tam giác","Luyện tập chung","Bài 29. Tứ giác nội tiếp","Bài 30. Đa giác đều","Luyện tập chung","Bài tập cuối chương IX"],
        "Chương X: Một số hình khối trong thực tiễn": ["Bài 31. Hình trụ và hình nón","Bài 32. Hình cầu","Luyện tập chung","Bài tập cuối chương X"]
    }
}

# ===============================
# 🎛️ GIAO DIỆN CHỌN NỘI DUNG
# ===============================
with st.sidebar:
    st.header("⚙️ Cấu hình sinh đề")
    model_choice = st.selectbox("Chọn Model Gemini:", ["gemini-1.5-flash", "gemini-1.5-pro"], index=0)
    
    lop = st.selectbox("Chọn lớp:", list(chuong_options_lop.keys()))
    
    chuong = st.multiselect("Chọn chương:", chuong_options_lop[lop], default=chuong_options_lop[lop][0])
    
    bai_list = []
    for c in chuong:
        bai_list.extend(bai_options_lop[lop].get(c, []))
    
    bai = st.multiselect("Chọn bài:", bai_list, default=bai_list[:2] if bai_list else None)
    
    co_dap_an = st.radio("Chế độ đáp án:", ["Có đáp án chi tiết", "Không đáp án"], index=0)

# ===============================
# 📊 MA TRẬN CÂU HỎI (HÀNG NGANG)
# ===============================
st.header("📊 Ma trận câu hỏi")

st.markdown("##### 1. Theo định dạng câu hỏi:")
row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    phan_bo_nl = st.number_input("NL (4 lựa chọn)", 0, 50, 12)
with row1_col2:
    phan_bo_ds = st.number_input("DS (Đúng/Sai)", 0, 50, 2)
with row1_col3:
    phan_bo_tl = st.number_input("TL (Tự luận)", 0, 50, 7)

st.markdown("##### 2. Theo mức độ nhận thức:")
row2_col1, row2_col2, row2_col3 = st.columns(3)
with row2_col1:
    so_cau_nb = st.number_input("Nhận biết", 0, 50, 6)
with row2_col2:
    so_cau_th = st.number_input("Thông hiểu", 0, 50, 8)
with row2_col3:
    so_cau_vd = st.number_input("Vận dụng", 0, 50, 7)

total_q = phan_bo_nl + phan_bo_ds + phan_bo_tl
st.info(f"📌 Tổng số câu dự kiến: **{total_q} câu** (Khớp ma trận: {so_cau_nb + so_cau_th + so_cau_vd} câu)")

# ===============================
# 📝 XỬ LÝ LOGIC API
# ===============================

def generate_questions(api_key, prompt, model):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=180)
        if r.status_code != 200:
            return False, f"Lỗi {r.status_code}: {r.text}"
        data = r.json()
        if data.get("candidates"):
            return True, data["candidates"][0]["content"]["parts"][0]["text"]
        return False, "Không nhận được phản hồi từ AI."
    except Exception as e:
        return False, str(e)

# ===============================
# 🚀 THỰC THI SINH ĐỀ
# ===============================

if st.button("🚀 BẮT ĐẦU SINH ĐỀ", type="primary"):
    if not api_key:
        st.error("Vui lòng nhập API Key!")
    elif not chuong or not bai:
        st.warning("Vui lòng chọn Chương và Bài!")
    else:
        dan_ap = "Cuối đề thi phải có PHẦN ĐÁP ÁN VÀ HƯỚNG DẪN GIẢI CHI TIẾT." if co_dap_an == "Có đáp án chi tiết" else "Không kèm đáp án."
        
        prompt = f"""
Bạn là giáo viên Toán chuyên soạn đề cho {lop} theo sách "Kết nối tri thức".
Nội dung: {', '.join(chuong)} - Các bài: {', '.join(bai)}.

YÊU CẦU CẤU TRÚC:
1. Trắc nghiệm (4 lựa chọn): {phan_bo_nl} câu.
2. Trắc nghiệm Đúng/Sai: {phan_bo_ds} câu.
3. Tự luận: {phan_bo_tl} câu.

PHÂN BỔ MỨC ĐỘ:
- Nhận biết: {so_cau_nb} câu
- Thông hiểu: {so_cau_th} câu
- Vận dụng: {so_cau_vd} câu

QUY ĐỊNH TRÌNH BÀY:
- Công thức Toán đặt trong $$...$$.
- Mỗi câu hỏi trắc nghiệm phải xuống dòng cho từng phương án A, B, C, D.
- Ghi rõ "Câu X: (Mức độ ...)"
- {dan_ap}
- Trả về định dạng Markdown.
"""
        
        with st.spinner(f"Đang sinh đề bằng {model_choice}... Vui lòng đợi giây lát."):
            success, result = generate_questions(api_key, prompt, model_choice)
            if success:
                st.success("✅ Đã tạo đề thành công!")
                st.markdown("---")
                st.markdown(result)
                
                # Nút tải về
                btn_name = f"De_Toan_{lop}_{datetime.now().strftime('%H%M')}.md"
                st.download_button("📥 Tải đề về (Markdown)", data=result, file_name=btn_name)
            else:
                st.error(f"Lỗi: {result}")

# Phần xử lý ảnh (giữ nguyên logic gốc của bạn)
def analyze_real_image(api_key, image, prompt):
    if image.mode == "RGBA": image = image.convert("RGB")
    buf = BytesIO()
    image.save(buf, format="JPEG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()
    MODEL = "gemini-1.5-flash"
    URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key}"
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}, {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}]}]}
    try:
        res = requests.post(URL, json=payload)
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except: return "Lỗi xử lý ảnh."
