import requests
import streamlit as st
from datetime import datetime
import base64
from io import BytesIO
import re

# ===============================
# ⚙️ CẤU HÌNH TRANG (Phải để đầu tiên)
# ===============================
st.set_page_config(page_title="Math Gen Pro - KNTT", layout="wide", page_icon="🧮")

# ===============================
# 🔑 NHẬP GOOGLE API KEY
# ===============================

with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key:
1. Truy cập: **https://aistudio.google.com/app/apikey**
2. Đăng nhập Gmail.
3. Nhấn **Create API key**.
4. Copy API Key.
5. Dán vào ô bên dưới.
""")

st.subheader("🔐 Nhập Google API Key:")
api_key = st.text_input("Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Vui lòng nhập API Key để tiếp tục.")
else:
    st.success("✅ API Key hợp lệ!")

# ===============================
# 📚 DỮ LIỆU CHƯƠNG TRÌNH HỌC (ĐÃ CẬP NHẬT FULL)
# ===============================

chuong_options_lop = {
    "Lớp 6": [
        "Chương I: Tập hợp các số tự nhiên",
        "Chương II: Tính chia hết trong tập hợp các số tự nhiên",
        "Chương III: Số nguyên",
        "Chương IV: Một số hình phẳng trong thực tiễn",
        "Chương V: Tính đối xứng của hình phẳng trong tự nhiên",
        "Chương VI: Phân số",
        "Chương VII: Số thập phân",
        "Chương VIII: Những hình hình học cơ bản",
        "Chương IX: Dữ liệu và xác suất thực nghiệm",
        "Hoạt động thực hành trải nghiệm"
    ],
    "Lớp 7": [
        "Chương I: Số hữu tỉ",
        "Chương II: Số thực",
        "Chương III: Góc và đường thẳng song song",
        "Chương IV: Tam giác bằng nhau",
        "Chương V: Thu thập và biểu diễn dữ liệu",
        "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ",
        "Chương VII: Biểu thức đại số và đa thức một biến",
        "Chương VIII: Làm quen với biến cố và xác suất",
        "Chương IX: Quan hệ giữa các yếu tố trong một tam giác",
        "Chương X: Một số hình khối trong thực tiễn",
        "Bài tập ôn tập cuối năm"
    ],
    "Lớp 8": [
        "Chương I: Đa thức",
        "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
        "Chương III: Tứ giác",
        "Chương IV: Định lí Thalès",
        "Chương V: Dữ liệu và biểu đồ",
        "Chương VI: Phân thức đại số",
        "Chương VII: Phương trình bậc nhất và hàm số bậc nhất",
        "Chương VIII: Mở đầu về tính xác suất của biến cố",
        "Chương IX: Tam giác đồng dạng",
        "Chương X: Một số hình khối trong thực tiễn",
        "Bài tập ôn tập cuối năm"
    ],
    "Lớp 9": [
        "Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn",
        "Chương II: Phương trình và bất phương trình bậc nhất một ẩn",
        "Chương III: Căn bậc hai và căn bậc ba",
        "Chương IV: Hệ thức lượng trong tam giác vuông",
        "Chương V: Đường tròn",
        "Hoạt động thực hành trải nghiệm",
        "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn",
        "Chương VII: Tần số và tần số tương đối",
        "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản",
        "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp",
        "Chương X: Một số hình khối trong thực tiễn"
    ]
}

bai_options_lop = {
    "Lớp 6": {
        "Chương I: Tập hợp các số tự nhiên": ["Bài 1. Tập hợp", "Bài 2. Cách ghi số tự nhiên", "Bài 3. Thứ tự trong tập hợp các số tự nhiên", "Bài 4. Phép cộng và phép trừ số tự nhiên", "Bài 5. Phép nhân và phép chia số tự nhiên", "Luyện tập chung", "Bài tập cuối chương I"],
        "Chương II: Tính chia hết trong tập hợp các số tự nhiên": ["Bài 8. Quan hệ chia hết và tính chất", "Bài 9. Dấu hiệu chia hết", "Bài 10. Số nguyên tố", "Bài 11. Ước chung. Ước chung lớn nhất", "Bài 12. Bội chung. Bội chung nhỏ nhất", "Luyện tập chung", "Bài tập cuối chương II"],
        "Chương III: Số nguyên": ["Bài 13. Tập hợp các số nguyên", "Bài 14. Phép cộng và phép trừ số nguyên", "Bài 15. Quy tắc dấu ngoặc", "Bài 16. Phép nhân số nguyên", "Bài 17. Phép chia hết. Ước và bội của một số nguyên", "Ôn tập chương III"],
        "Chương IV: Một số hình phẳng trong thực tiễn": ["Bài 18. Hình tam giác đều. Hình vuông. Hình lục giác đều", "Bài 19. Hình chữ nhật. Hình thoi. Hình bình hành. Hình thang cân", "Bài 20. Chu vi và diện tích của một số tứ giác đã học", "Luyện tập chung", "Bài tập cuối chương IV"],
        "Chương V: Tính đối xứng của hình phẳng trong tự nhiên": ["Bài 21. Hình có trục đối xứng", "Bài 22. Hình có tâm đối xứng", "Luyện tập chung", "Bài tập cuối chương V"],
        "Chương VI: Phân số": ["Bài 23. Mở rộng phân số", "Bài 24. So sánh phân số. Hỗn số dương", "Bài 25. Phép cộng và phép trừ phân số", "Bài 26. Phép nhân và phép chia phân số", "Bài 27. Hai bài toán về phân số", "Luyện tập chung", "Bài tập cuối chương VI"],
        "Chương VII: Số thập phân": ["Bài 28. Số thập phân", "Bài 29. Tính toán với số thập phân", "Bài 30. Làm tròn và ước lượng", "Bài 31. Một số bài toán về tỉ số và tỉ số phần trăm", "Luyện tập chung", "Bài tập cuối chương VII"],
        "Chương VIII: Những hình hình học cơ bản": ["Bài 32. Điểm và đường thẳng", "Bài 33. Điểm nằm giữa hai điểm. Tia", "Bài 34. Đoạn thẳng. Độ dài đoạn thẳng", "Bài 35. Trung điểm của đoạn thẳng", "Bài 36. Góc", "Bài 37. Số đo góc", "Luyện tập chung", "Bài tập cuối chương VIII"],
        "Chương IX: Dữ liệu và xác suất thực nghiệm": ["Bài 38. Dữ liệu và thu thập dữ liệu", "Bài 39. Bảng thống kê và biểu đồ tranh", "Bài 40. Biểu đồ cột", "Bài 41. Biểu đồ cột kép", "Bài 42. Kết quả có thể và sự kiện trong trò chơi, thí nghiệm", "Bài 43. Xác suất thực nghiệm", "Luyện tập chung", "Bài tập cuối chương IX"],
        "Hoạt động thực hành trải nghiệm": ["Bài 44. Kế hoạch chi tiêu cá nhân", "Bài 45. Biểu đồ cột kép biểu diễn số liệu về trường lớp"]
    },
    "Lớp 7": {
        "Chương I: Số hữu tỉ": ["Bài 1. Tập hợp các số hữu tỉ", "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ", "Bài 3. Luỹ thừa với số mũ tự nhiên của một số hữu tỉ", "Bài 4. Thứ tự thực hiện các phép tính. Quy tắc chuyển vế", "Ôn tập chương I"],
        "Chương II: Số thực": ["Bài 5. Làm quen với số thập phân vô hạn tuần hoàn", "Bài 6. Số vô tỉ. Căn bậc hai số học", "Bài 7. Tập hợp các số thực", "Ôn tập chương II"],
        "Chương III: Góc và đường thẳng song song": ["Bài 8. Góc ở vị trí đặc biệt. Tia phân giác của một góc", "Bài 9. Hai đường thẳng song song và dấu hiệu nhận biết", "Bài 10. Tiên đề Euclid. Tính chất của hai đường thẳng song song", "Bài 11. Định lí và chứng minh định lí", "Ôn tập chương III"],
        "Chương IV: Tam giác bằng nhau": ["Bài 12. Tổng các góc trong một tam giác", "Bài 13. Hai tam giác bằng nhau. Trường hợp bằng nhau thứ nhất của tam giác", "Bài 14. Trường hợp bằng nhau thứ hai và thứ ba của tam giác", "Bài 15. Các trường hợp bằng nhau của tam giác vuông", "Bài 16. Tam giác cân. Đường trung trực của đoạn thẳng", "Ôn tập chương IV"],
        "Chương V: Thu thập và biểu diễn dữ liệu": ["Bài 17. Thu thập và phân loại dữ liệu", "Bài 18. Biểu đồ hình quạt tròn", "Bài 19. Biểu đồ đoạn thẳng", "Ôn tập chương V"],
        "Chương VI: Tỉ lệ thức và đại lượng tỉ lệ": ["Bài 20. Tỉ lệ thức", "Bài 21. Tính chất của dãy tỉ số bằng nhau", "Bài 22. Đại lượng tỉ lệ thuận", "Bài 23. Đại lượng tỉ lệ nghịch", "Ôn tập chương VI"],
        "Chương VII: Biểu thức đại số và đa thức một biến": ["Bài 24. Biểu thức đại số", "Bài 25. Đa thức một biến", "Bài 26. Phép cộng và phép trừ đa thức một biến", "Bài 27. Phép nhân đa thức một biến", "Bài 28. Phép chia đa thức một biến", "Ôn tập chương VII"],
        "Chương VIII: Làm quen với biến cố và xác suất": ["Bài 29. Làm quen với biến cố", "Bài 30. Làm quen với xác suất của biến cố", "Ôn tập chương VIII"],
        "Chương IX: Quan hệ giữa các yếu tố trong một tam giác": ["Bài 31. Quan hệ giữa góc và cạnh đối diện trong một tam giác", "Bài 32. Quan hệ giữa đường vuông góc và đường xiên", "Bài 33. Quan hệ giữa ba cạnh của một tam giác", "Bài 34. Sự đồng quy của ba đường trung tuyến, ba đường phân giác trong một tam giác", "Bài 35. Sự đồng quy của ba đường trung trực, ba đường cao trong một tam giác", "Ôn tập chương IX"],
        "Chương X: Một số hình khối trong thực tiễn": ["Bài 36. Hình hộp chữ nhật và hình lập phương", "Bài 37. Hình lăng trụ đứng tam giác và hình lăng trụ đứng tứ giác", "Ôn tập chương X"],
        "Bài tập ôn tập cuối năm": []
    },
    "Lớp 8": {
        "Chương I: Đa thức": ["Bài 1. Đơn thức", "Bài 2. Đa thức", "Bài 3. Phép cộng và phép trừ đa thức", "Bài 4. Phép nhân đa thức", "Bài 5. Phép chia đa thức cho đơn thức", "Ôn tập chương I"],
        "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng": ["Bài 6. Hiệu hai bình phương. Bình phương của một tổng hay một hiệu", "Bài 7. Lập phương của một tổng. Lập phương của một hiệu", "Bài 8. Tổng và hiệu hai lập phương", "Bài 9. Phân tích đa thức thành nhân tử", "Ôn tập chương II"],
        "Chương III: Tứ giác": ["Bài 10. Tứ giác", "Bài 11. Hình thang cân", "Bài 12. Hình bình hành", "Bài 13. Hình chữ nhật", "Bài 14. Hình thoi và hình vuông", "Ôn tập chương III"],
        "Chương IV: Định lí Thalès": ["Bài 15. Định lí Thalès trong tam giác", "Bài 16. Đường trung bình của tam giác", "Bài 17. Tính chất đường phân giác của tam giác", "Ôn tập chương IV"],
        "Chương V: Dữ liệu và biểu đồ": ["Bài 18. Thu thập và phân loại dữ liệu", "Bài 19. Biểu diễn dữ liệu bằng bảng, biểu đồ", "Bài 20. Phân tích số liệu thống kê dựa vào biểu đồ", "Ôn tập chương V"],
        "Chương VI: Phân thức đại số": ["Bài 21. Phân thức đại số", "Bài 22. Tính chất cơ bản của phân thức đại số", "Bài 23. Phép cộng và phép trừ phân thức đại số", "Bài 24. Phép nhân và phép chia phân thức đại số", "Ôn tập chương VI"],
        "Chương VII: Phương trình bậc nhất và hàm số bậc nhất": ["Bài 25. Phương trình bậc nhất một ẩn", "Bài 26. Giải bài toán bằng cách lập phương trình", "Bài 27. Khái niệm hàm số và đồ thị của hàm số", "Bài 28. Hàm số bậc nhất và đồ thị của hàm số bậc nhất", "Bài 29. Hệ số góc của đường thẳng", "Ôn tập chương VII"],
        "Chương VIII: Mở đầu về tính xác suất của biến cố": ["Bài 30. Kết quả có thể và kết quả thuận lợi", "Bài 31. Cách tính xác suất của biến cố bằng tỉ số", "Bài 32. Mối liên hệ giữa xác suất thực nghiệm với xác suất và ứng dụng", "Ôn tập chương VIII"],
        "Chương IX: Tam giác đồng dạng": ["Bài 33. Hai tam giác đồng dạng", "Bài 34. Ba trường hợp đồng dạng của hai tam giác", "Bài 35. Định lí Pythagore và ứng dụng", "Bài 36. Các trường hợp đồng dạng của hai tam giác vuông", "Bài 37. Hình đồng dạng", "Ôn tập chương IX"],
        "Chương X: Một số hình khối trong thực tiễn": ["Bài 38. Hình chóp tam giác đều", "Bài 39. Hình chóp tứ giác đều", "Ôn tập chương X"],
        "Bài tập ôn tập cuối năm": []
    },
    "Lớp 9": {
        "Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn": ["Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn", "Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn", "Luyện tập chung", "Bài 3. Giải bài toán bằng cách lập hệ phương trình", "Bài tập cuối chương I"],
        "Chương II: Phương trình và bất phương trình bậc nhất một ẩn": ["Bài 4. Phương trình quy về phương trình bậc nhất một ẩn", "Bài 5. Bất đẳng thức và tính chất", "Luyện tập chung", "Bài 6. Bất phương trình bậc nhất một ẩn", "Bài tập cuối chương II"],
        "Chương III: Căn bậc hai và căn bậc ba": ["Bài 7. Căn bậc hai và căn thức bậc hai", "Bài 8. Khai căn bậc hai với phép nhân và phép chia", "Luyện tập chung", "Bài 9. Biến đổi đơn giản và rút gọn biểu thức chứa căn thức bậc hai", "Bài 10. Căn bậc ba và căn thức bậc ba", "Luyện tập chung", "Bài tập cuối chương III"],
        "Chương IV: Hệ thức lượng trong tam giác vuông": ["Bài 11. Tỉ số lượng giác của góc nhọn", "Bài 12. Một số hệ thức giữa cạnh, góc trong tam giác vuông và ứng dụng", "Luyện tập chung", "Bài tập cuối chương IV"],
        "Chương V: Đường tròn": ["Bài 13. Mở đầu về đường tròn", "Bài 14. Cung và dây của một đường tròn", "Bài 15. Độ dài của cung tròn. Diện tích hình quạt tròn và hình vành khuyên", "Luyện tập chung", "Bài 16. Vị trí tương đối của đường thẳng và đường tròn", "Bài 17. Vị trí tương đối của hai đường tròn", "Luyện tập chung", "Bài tập cuối chương V"],
        "Hoạt động thực hành trải nghiệm": ["Pha chế dung dịch theo nồng độ yêu cầu", "Tính chiều cao và xác định khoảng cách"],
        "Chương VI: Hàm số y = ax^2 (a khác 0). Phương trình bậc hai một ẩn": ["Bài 18. Hàm số y = ax2 (a ≠ 0)", "Bài 19. Phương trình bậc hai một ẩn", "Luyện tập chung", "Bài 20. Định lí Viète và ứng dụng", "Bài 21. Giải bài toán bằng cách lập phương trình", "Luyện tập chung", "Bài tập cuối chương VI"],
        "Chương VII: Tần số và tần số tương đối": ["Bài 22. Bảng tần số và biểu đồ tần số", "Bài 23. Bảng tần số tương đối và biểu đồ tần số tương đối", "Luyện tập chung", "Bài 24. Bảng tần số, tần số tương đối ghép nhóm và biểu đồ", "Bài tập cuối chương VII"],
        "Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản": ["Bài 25. Phép thử ngẫu nhiên và không gian mẫu", "Bài 26. Xác suất của biến cố liên quan tới phép thử", "Luyện tập chung", "Bài tập cuối chương VIII"],
        "Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp": ["Bài 27. Góc nội tiếp", "Bài 28. Đường tròn ngoại tiếp và đường tròn nội tiếp của một tam giác", "Luyện tập chung", "Bài 29. Tứ giác nội tiếp", "Bài 30. Đa giác đều", "Luyện tập chung", "Bài tập cuối chương IX"],
        "Chương X: Một số hình khối trong thực tiễn": ["Bài 31. Hình trụ và hình nón", "Bài 32. Hình cầu", "Luyện tập chung", "Bài tập cuối chương X"]
    }
}

# ===============================
# 🛠️ CÁC HÀM XỬ LÝ (CORE)
# ===============================

def format_fix_final(text):
    """
    Hàm xử lý hậu kỳ bắt buộc xuống dòng bằng Regex.
    Chạy hàm này trước khi st.markdown để đảm bảo hiển thị đẹp.
    """
    # 1. Xử lý phần Trắc nghiệm (A. B. C. D.)
    # Tìm A., B., C., D. đứng đầu dòng hoặc sau khoảng trắng -> Thêm 2 dấu xuống dòng
    text = re.sub(r'(\s)([A-D]\.)', r'\n\n\2', text)
    
    # 2. Xử lý phần Đúng/Sai (a) b) c) d))
    # Tìm a), b)... hoặc a., b. -> Thêm 2 dấu xuống dòng
    text = re.sub(r'(\s)([a-d][\)\.])', r'\n\n\2', text)
    
    # 3. Xử lý khoảng cách giữa các câu hỏi (Câu 1., Câu 2...) để đề thoáng hơn
    text = re.sub(r'(\s)(Câu \d+)', r'\n\n\n\2', text)
    
    return text

def create_math_prompt_v2(lop, chuong, bai, 
                          nl_nb, nl_th, nl_vd, 
                          ds_nb, ds_th, ds_vd, 
                          tlngan_nb, tlngan_th, tlngan_vd,
                          tl_nb, tl_th, tl_vd, 
                          dan_ap_text):
    """Hàm tạo prompt chi tiết theo ma trận nhận thức"""
    
    prompt = f"""
Bạn là giáo viên Toán lớp {lop}, soạn đề kiểm tra theo chương trình GDPT 2018 (Sách Kết nối tri thức).
- Nội dung kiểm tra: {', '.join(bai)} thuộc các chương {', '.join(chuong)}.

**YÊU CẦU CẤU TRÚC ĐỀ (Bắt buộc tuân thủ số lượng):**

1. **PHẦN 1: TRẮC NGHIỆM NHIỀU LỰA CHỌN (4 phương án A,B,C,D)**
   - Tổng: {nl_nb + nl_th + nl_vd} câu.
   - Phân bổ: {nl_nb} Nhận biết, {nl_th} Thông hiểu, {nl_vd} Vận dụng.
   - Định dạng: Các đáp án A, B, C, D phải xuống dòng riêng biệt.

2. **PHẦN 2: TRẮC NGHIỆM ĐÚNG/SAI (Mỗi câu 4 ý a,b,c,d)**
   - Tổng: {ds_nb + ds_th + ds_vd} câu.
   - Phân bổ: {ds_nb} Nhận biết, {ds_th} Thông hiểu, {ds_vd} Vận dụng.
   - Định dạng: Có 1 đề dẫn, sau đó 4 ý a,b,c,d xuống dòng riêng biệt.

3. **PHẦN 3: TRẮC NGHIỆM TRẢ LỜI NGẮN (Điền số/Kết quả)**
   - Tổng: {tlngan_nb + tlngan_th + tlngan_vd} câu.
   - Phân bổ: {tlngan_nb} Nhận biết, {tlngan_th} Thông hiểu, {tlngan_vd} Vận dụng.
   - Định dạng: Chỉ câu hỏi, yêu cầu ra đáp số cụ thể.

4. **PHẦN 4: TỰ LUẬN (Nếu có)**
   - Tổng: {tl_nb + tl_th + tl_vd} câu.
   - Phân bổ: {tl_nb} NB, {tl_th} TH, {tl_vd} VD.

**QUY ĐỊNH ĐỊNH DẠNG (NGHIÊM NGẶT):**
- **Toán học:** Công thức BẮT BUỘC đặt trong `$$...$$`. Ví dụ: $$y = x^2$$.
- **Trình bày:** Giữa các ý và đáp án PHẢI có dòng trống.

--- **MẪU TRÌNH BÀY (AI HÃY LÀM THEO FORMAT NÀY)** ---

**PHẦN I. TRẮC NGHIỆM NHIỀU LỰA CHỌN**
**Câu 1.** Nội dung câu hỏi...
(Dòng trống)
A. $$x=1$$
(Dòng trống)
B. $$x=2$$
(Dòng trống)
C. $$x=3$$
(Dòng trống)
D. $$x=4$$

**PHẦN II. TRẮC NGHIỆM ĐÚNG SAI**
**Câu 2.** Cho hình chữ nhật ABCD...
(Dòng trống)
a) Hai đường chéo bằng nhau.
(Dòng trống)
b) Cạnh AB = 5.
(Dòng trống)
c) ...
(Dòng trống)
d) ...

**PHẦN III. TRẮC NGHIỆM TRẢ LỜI NGẮN**
**Câu 3.** Tính giá trị biểu thức A...

--- **HẾT PHẦN MẪU** ---

{dan_ap_text}
"""
    return prompt

def generate_questions(api_key, prompt):
    """Hàm gọi API Gemini để sinh text"""
    MODEL = "gemini-2.0-flash-exp" # Dùng model mới hoặc fallback
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        
        # Fallback logic
        if r.status_code != 200:
             url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
             r = requests.post(url, json=payload, headers=headers, timeout=120)
            
        if r.status_code != 200:
            return False, f"Lỗi API: {r.text}"
            
        j = r.json()
        if j.get("candidates"):
            return True, j["candidates"][0]["content"]["parts"][0]["text"]
        return False, "Không có dữ liệu trả về."
    except Exception as e:
        return False, f"Lỗi kết nối: {str(e)}"

# ===============================
# 🎛️ SIDEBAR VÀ CẤU HÌNH
# ===============================

with st.sidebar:
    st.header("1. Chọn nội dung")
    lop = st.selectbox("Chọn lớp", ["Lớp 6","Lớp 7","Lớp 8","Lớp 9"], index=3)
    
    # Lấy danh sách chương theo lớp
    chuong_options = chuong_options_lop.get(lop, [])
    chuong = st.multiselect("Chọn chương", chuong_options, default=[chuong_options[0]] if chuong_options else None)
    
    # Lấy danh sách bài học dựa trên các chương đã chọn
    bai_list_all = []
    if chuong:
        for c in chuong:
            # Lấy bài của từng chương và thêm vào list chung
            bai_trong_chuong = bai_options_lop.get(lop, {}).get(c, [])
            bai_list_all.extend(bai_trong_chuong)
    
    if bai_list_all:
        bai = st.multiselect("Chọn bài", bai_list_all, default=[bai_list_all[0]])
    else:
        st.info("Vui lòng chọn chương để hiện bài học.")
        bai = []
        
    st.markdown("---")
    co_dap_an = st.radio("Chế độ đáp án:", ["Có đáp án chi tiết", "Không đáp án"], index=0)

# ===============================
# 🎚️ CẤU HÌNH MA TRẬN ĐỀ (GIAO DIỆN MỚI)
# ===============================

st.header("🛠️ 2. Cấu hình Ma trận đề thi")
st.markdown("Chỉnh số lượng câu hỏi theo mức độ nhận thức cho từng phần:")

# Tạo 4 Tabs cho 4 loại câu hỏi
tab1, tab2, tab3, tab4 = st.tabs(["1. TN Nhiều lựa chọn", "2. TN Đúng/Sai", "3. TN Trả lời ngắn", "4. Tự luận"])

# 1. TRẮC NGHIỆM NHIỀU LỰA CHỌN (NL)
with tab1:
    st.subheader("Phần 1: Trắc nghiệm (4 lựa chọn A,B,C,D)")
    c1, c2, c3 = st.columns(3)
    nl_nb = c1.number_input("Số câu Nhận biết (NL)", min_value=0, value=4, key="nl_nb")
    nl_th = c2.number_input("Số câu Thông hiểu (NL)", min_value=0, value=4, key="nl_th")
    nl_vd = c3.number_input("Số câu Vận dụng (NL)", min_value=0, value=4, key="nl_vd")
    total_nl = nl_nb + nl_th + nl_vd
    st.info(f"👉 Tổng phần này: **{total_nl}** câu")

# 2. TRẮC NGHIỆM ĐÚNG SAI (DS)
with tab2:
    st.subheader("Phần 2: Trắc nghiệm Đúng/Sai (4 ý a,b,c,d)")
    c1, c2, c3 = st.columns(3)
    ds_nb = c1.number_input("Số câu Nhận biết (DS)", min_value=0, value=1, key="ds_nb")
    ds_th = c2.number_input("Số câu Thông hiểu (DS)", min_value=0, value=2, key="ds_th")
    ds_vd = c3.number_input("Số câu Vận dụng (DS)", min_value=0, value=1, key="ds_vd")
    total_ds = ds_nb + ds_th + ds_vd
    st.info(f"👉 Tổng phần này: **{total_ds}** câu (Mỗi câu gồm 4 ý nhỏ)")

# 3. TRẮC NGHIỆM TRẢ LỜI NGẮN (TNTL)
with tab3:
    st.subheader("Phần 3: Trắc nghiệm Trả lời ngắn (Điền số/kết quả)")
    c1, c2, c3 = st.columns(3)
    tlngan_nb = c1.number_input("Số câu Nhận biết (TL ngắn)", min_value=0, value=1, key="tlngan_nb")
    tlngan_th = c2.number_input("Số câu Thông hiểu (TL ngắn)", min_value=0, value=2, key="tlngan_th")
    tlngan_vd = c3.number_input("Số câu Vận dụng (TL ngắn)", min_value=0, value=3, key="tlngan_vd")
    total_tlngan = tlngan_nb + tlngan_th + tlngan_vd
    st.info(f"👉 Tổng phần này: **{total_tlngan}** câu")

# 4. TỰ LUẬN (TL)
with tab4:
    st.subheader("Phần 4: Bài tập Tự luận (Trình bày chi tiết)")
    c1, c2, c3 = st.columns(3)
    tl_nb = c1.number_input("Số câu Nhận biết (Tự luận)", min_value=0, value=0, key="tl_nb")
    tl_th = c2.number_input("Số câu Thông hiểu (Tự luận)", min_value=0, value=1, key="tl_th")
    tl_vd = c3.number_input("Số câu Vận dụng (Tự luận)", min_value=0, value=1, key="tl_vd")
    total_tl = tl_nb + tl_th + tl_vd
    st.info(f"👉 Tổng phần này: **{total_tl}** câu")

total_questions = total_nl + total_ds + total_tlngan + total_tl
st.markdown("---")
st.success(f"📊 **TỔNG CỘNG TOÀN ĐỀ:** {total_questions} câu hỏi.")

# ===============================
# 🚀 NÚT SINH ĐỀ VÀ HIỂN THỊ
# ===============================

if st.button("🚀 Sinh đề theo cấu hình chi tiết", type="primary"):
    if not api_key:
        st.warning("Vui lòng nhập API Key.")
    elif total_questions == 0:
        st.warning("Bạn chưa chọn số lượng câu hỏi nào!")
    elif not bai:
        st.warning("Vui lòng chọn bài học cần kiểm tra!")
    else:
        # Xử lý text hướng dẫn chấm
        if co_dap_an == "Có đáp án chi tiết":
            dan_ap = "Cuối đề thi phải có PHẦN ĐÁP ÁN (Bảng đáp án cho TN) và HƯỚNG DẪN GIẢI CHI TIẾT cho từng câu."
        else:
            dan_ap = "KHÔNG hiển thị đáp án và lời giải."

        # 1. Tạo prompt
        prompt = create_math_prompt_v2(
            lop, chuong, bai,
            nl_nb, nl_th, nl_vd,
            ds_nb, ds_th, ds_vd,
            tlngan_nb, tlngan_th, tlngan_vd,
            tl_nb, tl_th, tl_vd,
            dan_ap
        )
        
        with st.spinner("Đang kết nối Gemini để sinh đề... (Mất khoảng 10-20 giây)"):
            success, result = generate_questions(api_key, prompt)
            
            if success:
                # 2. QUAN TRỌNG: Gọi hàm sửa lỗi dính dòng
                result_fixed = format_fix_final(result)
                
                st.success("✅ Sinh đề thành công!")
                
                # 3. Hiển thị kết quả
                st.markdown(result_fixed, unsafe_allow_html=True)
                
                # 4. Nút tải về
                filename = f"De_{lop}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                st.download_button("📥 Tải đề về máy (Markdown)", result_fixed, file_name=filename)
            else:
                st.error(result)
