import streamlit as st
import requests
import base64
import json
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Chấm bài qua ảnh AI (Song ngữ)", page_icon="📸", layout="wide")

st.title("📸 CHẤM BÀI QUA ẢNH – AI CHI TIẾT, SONG NGỮ (Tiếng Việt / H'Mông)")

# --- Nhập API Key ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.text_input("Nhập Google API Key:", type="password")

st.markdown("---")

# --- Giao diện nhập ---
col1, col2 = st.columns([2, 1])
with col1:
    uploaded_img = st.file_uploader("📤 Tải ảnh bài làm học sinh (JPG/PNG)", type=["jpg", "jpeg", "png"]) 
    de_bai = st.text_area("📎 (Tùy chọn) Nếu bạn gửi đề bài / yêu cầu - dán ở đây để AI hướng dẫn cách làm", height=120, placeholder="Ví dụ: Giải phương trình... hoặc 'Tính tích phân...' ")
    dap_an_gv = st.text_area(
        "📘 (Tùy chọn) Đáp án chuẩn / Đáp án mẫu (nếu có)",
        height=120,
        placeholder="1.A 2.B 3.C... hoặc lời giải mẫu cho bài tự luận"
    )
    tong_diem = st.number_input("Tổng điểm bài làm", min_value=1, value=10)
    ngon_ngu_hmong = st.checkbox("Bao gồm H'Mông (🟦) song song với Tiếng Việt (🇻🇳)", value=True)

with col2:
    st.write("**Tùy chọn hiển thị**")
    show_json = st.checkbox("Hiển thị JSON kết quả (dành cho developer)", value=False)
    download_txt = st.checkbox("Cho phép tải kết quả (.txt)", value=True)

st.markdown("---")

# --- Hàm gọi Gemini AI ---
def call_gemini_image(api_key, prompt_text, image_file, timeout=60):
    MODEL = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={api_key}"

    img_bytes = image_file.read()
    img_base64 = base64.b64encode(img_bytes).decode()

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt_text},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_base64
                        }
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=timeout)
    except Exception as e:
        return {"error": f"Lỗi khi gọi API: {e}"}

    if response.status_code != 200:
        return {"error": f"Lỗi API {response.status_code}: {response.text}"}

    data = response.json()
    # Lấy phần text trả về (nếu có)
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        text = json.dumps(data, ensure_ascii=False)

    return {"text": text, "raw": data}

# --- Tạo prompt chi tiết (song ngữ yêu cầu JSON + human-readable) ---
def build_prompt(de_bai, dap_an_gv, tong_diem, include_hmong=True):
    # Hướng dẫn AI trả về cả 2 định dạng: 1) Phần đọc & nhận xét human-readable (song song VN/H'Mông);
    # 2) 1 block JSON (để chương trình có thể parse, tính điểm xác định).
    prompt = f"""
Bạn là giáo viên Toán/Ngữ văn/Ngôn ngữ có kinh nghiệm, biết song ngữ Tiếng Việt (🇻🇳) và H'Mông (🟦).
Nhiệm vụ: từ ảnh bài làm của học sinh, thực hiện các bước sau và trả về 2 phần:

PHẦN 1 - PHÂN TÍCH & CHẤM (Human-readable):
- Đọc (OCR) nội dung bài làm trong ảnh và hiển thị (nguyên văn) trong phần "BÀI LÀM HỌC SINH".
- Nếu có đáp án chuẩn do giáo viên nhập, so sánh từng câu. Nếu không có, tự suy luận đáp án chuẩn và hiển thị.
- Phân tích từng câu:
  - Nếu đúng → ghi 'Đúng' song song (🇻🇳 / 🟦)
  - Nếu sai → ghi chi tiết: Câu số, Sai ở bước nào, Lý do sai, Gợi ý cách sửa / cách làm đúng (viết chi tiết bước-bước).
  - Mỗi câu ghi nhận điểm đạt được và tối đa (phân bố điểm theo tổng {tong_diem}).
- Nếu giáo viên có gửi đề bài (được dán ở ô 'de_bai'), hãy **thêm** phần "HƯỚNG DẪN LÀM" cho đề bài đó (bước-giải chi tiết) bằng cả 2 thứ tiếng.
- Trả lời **song song**: Mỗi đoạn nhận xét/giải thích cần có cả Tiếng Việt (🇻🇳) và H'Mông (🟦). Nếu không thể dịch chính xác sang H'Mông, hãy thông báo rõ 'H'Mông: [tạm dịch hoặc chú thích]'.

PHẦN 2 - JSON MÁY (Machine-readable):
- Ngoài phần human-readable, xuất 1 block JSON hợp lệ (độc lập) có cấu trúc như sau:
{
  "student_text": "...",
  "questions": [
    {
      "q": 1,
      "student_answer": "...",
      "correct_answer": "...",
      "is_correct": true/false,
      "score": x,  # điểm đạt cho câu
      "max_score": y,
      "comment_vi": "...",
      "comment_hmong": "..."
    }, ...
  ],
  "total_score": X,
  "total_max": Y
}

Yêu cầu formatting:
- Block JSON phải bắt đầu trên dòng riêng với EXACT token: "JSON_START" và kết thúc bằng "JSON_END". Giúp chương trình dễ parse.
- Đồng thời phần human-readable phải dễ đọc, phân đoạn rõ ràng, có tiêu đề như mẫu (BÀI LÀM HỌC SINH / NHẬN XÉT & CHẤM ĐIỂM / ĐÁP ÁN CHUẨN / HƯỚNG DẪN LÀM).

LƯU Ý:
- Phân bố điểm: nếu không có chỉ dẫn, giả sử mọi câu bằng nhau. Tổng điểm tối đa = {tong_diem}.
- Hãy chính xác, ngắn gọn khi ghi điểm, nhưng chi tiết khi giải thích lỗi và hướng dẫn sửa (nhất là các bước sai).
- Nếu thấy phần chữ trong ảnh không rõ, báo rõ chỗ mờ và ghi nhận bạn đọc như thế nào.

BẮT ĐẦU PHÂN TÍCH (trả lời cả 2 phần human-readable + JSON):
"""
    # Nếu có đề bài, thêm một câu nhắc AI dùng đề bài này để hướng dẫn
    if de_bai:
        prompt += f"\nĐỀ BÀI (giáo viên cung cấp):\n{de_bai}\n\n"
    if dap_an_gv:
        prompt += f"\nĐÁP ÁN CHUẨN GIÁO VIÊN:\n{dap_an_gv}\n\n"
    return prompt

# --- Khi người dùng nhấn nút ---
if st.button("🎯 Chấm bài ngay"):
    if not api_key:
        st.error("❌ Bạn chưa nhập API Key!")
    elif not uploaded_img:
        st.error("❌ Bạn chưa tải ảnh bài làm học sinh!")
    else:
        with st.spinner("⏳ AI đang phân tích, chấm bài, chỉ ra lỗi sai và hướng dẫn..."):
            prompt = build_prompt(de_bai, dap_an_gv, tong_diem, include_hmong=ngon_ngu_hmong)
            result = call_gemini_image(api_key, prompt, uploaded_img)

        if "error" in result:
            st.error(result["error"])
        else:
            text = result.get("text", "")
            raw = result.get("raw", {})

            # Tries to extract JSON block between JSON_START and JSON_END
            json_data = None
            if "JSON_START" in text and "JSON_END" in text:
                try:
                    j_start = text.index("JSON_START") + len("JSON_START")
                    j_end = text.index("JSON_END")
                    j_text = text[j_start:j_end].strip()
                    json_data = json.loads(j_text)
                except Exception as e:
                    json_data = None

            st.success("🎉 Đã chấm xong bài!")
            st.markdown("### 📄 Kết quả chấm bài (song ngữ + chỉ ra lỗi sai)")

            # Hiển thị phần human-readable (tất cả text trả về)
            st.text_area("Kết quả (Human-readable)", value=text, height=400)

            # Nếu có JSON, trình bày đẹp hơn
            if json_data:
                st.markdown("### 🔢 Kết quả (parsed JSON)")
                for q in json_data.get("questions", []):
                    st.markdown(f"**Câu {q.get('q')}** — Điểm: {q.get('score')}/{q.get('max_score')}")
                    st.markdown(f"- 🇻🇳 Nhận xét: {q.get('comment_vi')}")
                    if q.get('comment_hmong'):
                        st.markdown(f"- 🟦 H'Mông: {q.get('comment_hmong')}")
                    st.markdown("---")

                st.markdown(f"**Tổng điểm:** {json_data.get('total_score')}/{json_data.get('total_max')}")

            if show_json:
                st.mark_markdown = st.markdown
                st.markdown("### JSON raw từ API")
                st.code(json.dumps(raw, ensure_ascii=False, indent=2), language='json')

            # Hiển thị ảnh
            try:
                uploaded_img.seek(0)
                img = Image.open(uploaded_img)
                st.markdown("### 🖼️ Ảnh bài làm học sinh")
                st.image(img, use_column_width=True)
            except Exception:
                pass

            # Cho phép tải kết quả .txt
            if download_txt:
                txt_out = text
                if json_data:
                    txt_out += "\n\n---\nPARSED_JSON:\n" + json.dumps(json_data, ensure_ascii=False, indent=2)
                b = txt_out.encode('utf-8')
                st.download_button("⬇️ Tải kết quả (.txt)", data=b, file_name="ketqua_chambai.txt", mime="text/plain")

st.markdown("---")
st.caption("Gợi ý: để kết quả chính xác nhất, chụp ảnh rõ ràng (ánh sáng tốt, chữ không bị mờ). Nếu muốn AI chỉ chấm phần trắc nghiệm, hãy gửi ảnh với đáp án rõ ràng.")
