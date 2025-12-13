# ================== IMPORT ==================
import streamlit as st
import os, json, re, io, base64
from deep_translator import GoogleTranslator
from gtts import gTTS
import google.generativeai as genai

# ================== GEMINI ==================
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ================== TRANG ==================
st.set_page_config(
    page_title="Gia sư Toán AI (KNTT)",
    page_icon="🏔️",
    layout="wide"
)

# ================== CHƯƠNG TRÌNH ==================
CHUONG_TRINH_HOC = {

    "Lớp 6": {
        "Chương I. Tập hợp các số tự nhiên": [
            "Bài 1. Tập hợp",
            "Bài 2. Cách ghi số tự nhiên",
            "Bài 3. Thứ tự trong tập hợp các số tự nhiên",
            "Bài 4. Phép cộng và phép trừ số tự nhiên",
            "Bài 5. Phép nhân và phép chia số tự nhiên",
            "Bài 6. Luỹ thừa với số mũ tự nhiên",
            "Bài 7. Thứ tự thực hiện các phép tính"
        ],
        "Chương II. Tính chia hết trong tập hợp các số tự nhiên": [
            "Bài 8. Quan hệ chia hết và tính chất",
            "Bài 9. Dấu hiệu chia hết",
            "Bài 10. Số nguyên tố",
            "Bài 11. Ước chung. Ước chung lớn nhất",
            "Bài 12. Bội chung. Bội chung nhỏ nhất"
        ],
        "Chương III. Số nguyên": [
            "Bài 13. Tập hợp các số nguyên",
            "Bài 14. Phép cộng và phép trừ số nguyên",
            "Bài 15. Quy tắc dấu ngoặc",
            "Bài 16. Phép nhân số nguyên",
            "Bài 17. Phép chia hết. Ước và bội của một số nguyên"
        ],
        "Chương V. Tính đối xứng của hình phẳng trong tự nhiên": [
            "Bài 21. Hình có trục đối xứng",
            "Bài 22. Hình có tâm đối xứng"
        ]
    },

    "Lớp 7": {
        "Chương I. Số hữu tỉ": [
            "Bài 1. Tập hợp các số hữu tỉ",
            "Bài 2. Cộng, trừ, nhân, chia số hữu tỉ",
            "Bài 3. Luỹ thừa với số mũ tự nhiên của một số hữu tỉ",
            "Bài 4. Thứ tự thực hiện các phép tính. Quy tắc chuyển vế"
        ],
        "Chương II. Số thực": [
            "Bài 5. Làm quen với số thập phân vô hạn tuần hoàn",
            "Bài 6. Số vô tỉ. Căn bậc hai số học",
            "Bài 7. Tập hợp các số thực"
        ],
        "Chương III. Góc và đường thẳng song song": [
            "Bài 8. Góc ở vị trí đặc biệt. Tia phân giác của một góc",
            "Bài 9. Hai đường thẳng song song và dấu hiệu nhận biết",
            "Bài 10. Tiên đề Euclid. Tính chất của hai đường thẳng song song",
            "Bài 11. Định lí và chứng minh định lí"
        ],
        "Chương IV. Tam giác bằng nhau": [
            "Bài 12. Tổng các góc trong một tam giác",
            "Bài 13. Hai tam giác bằng nhau. Trường hợp bằng nhau thứ nhất",
            "Bài 14. Trường hợp bằng nhau thứ hai và thứ ba",
            "Bài 15. Các trường hợp bằng nhau của tam giác vuông",
            "Bài 16. Tam giác cân. Đường trung trực của đoạn thẳng"
        ]
    },

    "Lớp 8": {
        "Chương I. Đa thức": [
            "Bài 1. Đơn thức",
            "Bài 2. Đa thức",
            "Bài 3. Phép cộng và phép trừ đa thức",
            "Bài 4. Phép nhân đa thức",
            "Bài 5. Phép chia đa thức cho đơn thức"
        ],
        "Chương II. Hằng đẳng thức đáng nhớ và ứng dụng": [
            "Bài 6. Hiệu hai bình phương. Bình phương của một tổng hay một hiệu",
            "Bài 7. Lập phương của một tổng. Lập phương của một hiệu",
            "Bài 8. Tổng và hiệu hai lập phương",
            "Bài 9. Phân tích đa thức thành nhân tử"
        ],
        "Chương VI. Phân thức đại số": [
            "Bài 21. Phân thức đại số",
            "Bài 22. Tính chất cơ bản của phân thức đại số",
            "Bài 23. Phép cộng và phép trừ phân thức đại số",
            "Bài 24. Phép nhân và phép chia phân thức đại số"
        ],
        "Chương VII. Phương trình bậc nhất và hàm số bậc nhất": [
            "Bài 25. Phương trình bậc nhất một ẩn",
            "Bài 26. Giải bài toán bằng cách lập phương trình",
            "Bài 27. Khái niệm hàm số và đồ thị của hàm số",
            "Bài 28. Hàm số bậc nhất và đồ thị của hàm số",
            "Bài 29. Hệ số góc của đường thẳng"
        ]
    },

    "Lớp 9": {
        "Chương III. Căn bậc hai và căn bậc ba": [
            "Bài 7. Căn bậc hai và căn thức bậc hai",
            "Bài 8. Khai căn bậc hai với phép nhân và phép chia",
            "Bài 9. Biến đổi đơn giản và rút gọn biểu thức chứa căn thức bậc hai",
            "Bài 10. Căn bậc ba và căn thức bậc ba"
        ],
        "Chương IV. Hệ thức lượng trong tam giác vuông": [
            "Bài 11. Tỉ số lượng giác của góc nhọn",
            "Bài 12. Một số hệ thức giữa cạnh, góc trong tam giác vuông và ứng dụng"
        ],
        "Chương VI. Hàm số y = ax² (a ≠ 0). Phương trình bậc hai một ẩn": [
            "Bài 18. Hàm số y = ax² (a ≠ 0)",
            "Bài 19. Phương trình bậc hai một ẩn",
            "Bài 20. Định lí Viète và ứng dụng",
            "Bài 21. Giải bài toán bằng cách lập phương trình"
        ],
        "Chương IX. Đường tròn ngoại tiếp và đường tròn nội tiếp": [
            "Bài 27. Góc nội tiếp",
            "Bài 28. Đường tròn ngoại tiếp và đường tròn nội tiếp của một tam giác",
            "Bài 29. Tứ giác nội tiếp",
            "Bài 30. Đa giác đều"
        ]
    }
}
# ================== HÀM SINH CÂU HỎI (Sửa lỗi) ==================
def tao_de_toan_sua_loi(lop, bai):
    prompt = f"""
Bạn là giáo viên Toán Việt Nam, SGK Kết nối tri thức.
... (giữ nguyên prompt) ...
"""
    try:
        res = model.generate_content(prompt).text
        
        # Sửa lỗi: Trích xuất nội dung giữa hai dấu ngoặc nhọn { } lớn nhất
        # Biểu thức chính quy mạnh mẽ hơn, tìm khối JSON bao quanh.
        json_match = re.search(r"\{[\s\S]*\}", res) 
        
        if json_match:
            json_string = json_match.group(0)
            # Thử parse JSON
            data = json.loads(json_string)
            return data
        else:
            # Không tìm thấy khối JSON nào
            print("Không tìm thấy khối JSON trong phản hồi.")
            return None
            
    except json.JSONDecodeError as e:
        print(f"Lỗi JSON Decode: {e}")
        # print(f"Chuỗi JSON bị lỗi: {json_string}") 
        return None
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
        return None

# ================== HÀM DỊCH ==================
def dich(text):
    try:
        return GoogleTranslator(source="vi", target="hmn").translate(text)
    except:
        return text

# ================== GIAO DIỆN ==================
st.title("🏫 Gia sư Toán AI – SGK KNTT")

lop = st.selectbox("Chọn lớp", CHUONG_TRINH_HOC.keys())
chuong = st.selectbox("Chọn chương", CHUONG_TRINH_HOC[lop].keys())
bai = st.selectbox("Chọn bài", CHUONG_TRINH_HOC[lop][chuong])

if st.button("✨ Tạo câu hỏi"):
    cau = tao_de_toan(lop, bai)
    if cau:
        st.markdown("### ❓ Câu hỏi")
        st.markdown(cau["question"])
        ans = st.radio("Chọn đáp án", cau["options"])
        if st.button("✅ Kiểm tra"):
            if ans.startswith(cau["answer"]):
                st.success("🎉 Chính xác!")
            else:
                st.error("❌ Sai rồi")
                st.info("Gợi ý: " + cau["hint_vi"])
                st.info("H'Mông: " + dich(cau["hint_vi"]))
    else:
        st.error("AI bận, thử lại sau")

st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư")
