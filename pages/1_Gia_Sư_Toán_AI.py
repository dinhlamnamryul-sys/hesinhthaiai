# ================== IMPORT ==================
import streamlit as st
import os, json, re, io, base64
from deep_translator import GoogleTranslator
from gtts import gTTS
import google.generativeai as genai
from google.generativeai import types # Thêm import types

# ================== GEMINI ==================
# Đảm bảo GOOGLE_API_KEY được thiết lập trong môi trường
if not os.getenv("GOOGLE_API_KEY"):
    st.error("Lỗi: Không tìm thấy biến môi trường GOOGLE_API_KEY.")
else:
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
# 1. Định nghĩa JSON schema mong muốn cho đầu ra
CAU_HOI_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "question": types.Schema(type=types.Type.STRING, description="Câu hỏi trắc nghiệm Toán."),
        "options": types.Schema(
            type=types.Type.ARRAY,
            description="4 đáp án A, B, C, D.",
            items=types.Schema(type=types.Type.STRING)
        ),
        "answer": types.Schema(type=types.Type.STRING, description="Đáp án đúng (ví dụ: A, B, C, D)."),
        "hint_vi": types.Schema(type=types.Type.STRING, description="Gợi ý giải bài tập bằng tiếng Việt.")
    },
    required=["question", "options", "answer", "hint_vi"]
)

# ================== HÀM SINH CÂU HỎI (Đã tối ưu) ==================
# Đổi tên lại thành tao_de_toan để khớp với phần giao diện
def tao_de_toan(lop, bai):
    prompt = f"""
Bạn là giáo viên Toán Việt Nam, SGK Kết nối tri thức.
Tạo 1 câu hỏi trắc nghiệm Toán {lop}
Bài: {bai}

Yêu cầu:
- 4 đáp án A B C D
- 1 đáp án đúng
- Có gợi ý chi tiết

Trả về theo định dạng JSON đã yêu cầu. Tuyệt đối không thêm bất kỳ văn bản giải thích hoặc ký tự markdown (như ```json) nào.
"""
    try:
        res = model.generate_content(
            prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CAU_HOI_SCHEMA
            )
        )
        # Sử dụng thuộc tính .json để tự động parse JSON an toàn hơn
        data = json.loads(res.text) # Vẫn phải dùng json.loads(res.text) cho API hiện tại
        return data
    except Exception as e:
        # Ghi lại lỗi để debug (quan trọng)
        st.error(f"Lỗi AI/JSON: {e}")
        # if 'res' in locals():
        #     st.code(res.text, language='json')
        return None

# ================== HÀM DỊCH (Giữ nguyên) ==================
def dich(text):
    try:
        # Hạn chế dịch nếu text quá ngắn hoặc không cần thiết
        if not text:
             return ""
        return GoogleTranslator(source="vi", target="hmn").translate(text)
    except Exception:
        return "Lỗi dịch thuật."

# ================== GIAO DIỆN (Đã sửa lỗi gọi hàm) ==================
st.title("🏫 Gia sư Toán AI – SGK KNTT")

# ... (Chọn lớp, chương, bài giữ nguyên) ...

lop = st.selectbox("Chọn lớp", CHUONG_TRINH_HOC.keys())
chuong = st.selectbox("Chọn chương", CHUONG_TRINH_HOC[lop].keys())
bai = st.selectbox("Chọn bài", CHUONG_TRINH_HOC[lop][chuong])

# Khởi tạo state để lưu câu hỏi
if 'cau' not in st.session_state:
    st.session_state.cau = None

if st.button("✨ Tạo câu hỏi"):
    with st.spinner("Đang tạo câu hỏi..."):
        st.session_state.cau = tao_de_toan(lop, bai) # Gọi hàm đã tối ưu

if st.session_state.cau:
    cau = st.session_state.cau
    st.markdown("### ❓ Câu hỏi")
    st.markdown(cau["question"])
    
    # Lấy đáp án người dùng chọn
    # Sử dụng key để Streamlit không bị lỗi khi state thay đổi
    ans = st.radio("Chọn đáp án", cau["options"], key="radio_ans")
    
    if st.button("✅ Kiểm tra", key="check_button"):
        if ans.startswith(cau["answer"]):
            st.success("🎉 Chính xác!")
        else:
            st.error("❌ Sai rồi")
            st.info("**Gợi ý:** " + cau["hint_vi"])
            st.info("**H'Mông:** " + dich(cau["hint_vi"]))
else:
    # Nếu chưa có câu hỏi và người dùng chưa bấm nút (hoặc bị lỗi)
    if 'cau' in st.session_state and st.session_state.cau is None:
        st.error("AI bận, thử lại sau. (Vui lòng kiểm tra lại GOOGLE_API_KEY và logs nếu lỗi vẫn tiếp diễn)")


st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư")
