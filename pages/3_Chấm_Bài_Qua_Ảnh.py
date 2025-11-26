def build_prompt(de_bai, dap_an_gv, tong_diem, include_hmong=True):

    json_format = """
JSON_START
{
  "student_text": "...",
  "questions": [
    {
      "q": 1,
      "student_answer": "...",
      "correct_answer": "...",
      "is_correct": true,
      "score": x,
      "max_score": y,
      "comment_vi": "...",
      "comment_hmong": "..."
    }
  ],
  "total_score": X,
  "total_max": Y
}
JSON_END
"""

    prompt = f"""
Bạn là giáo viên Toán/Ngữ văn song ngữ Việt – H'Mông.

PHẦN 1 – PHÂN TÍCH HUMAN-READABLE:
- OCR bài làm
- So sánh với đáp án hoặc tự suy ra
- Phân tích từng câu: đúng/sai, lỗi sai, lý do, hướng dẫn sửa
- Ghi điểm cho từng câu và tổng điểm {tong_diem}
- Song ngữ 🇻🇳 / 🟦

PHẦN 2 – JSON MÁY (Machine-readable):
Hãy trả về thêm 1 block JSON theo đúng định dạng sau:

{json_format}

Lưu ý:
- JSON phải đặt giữa JSON_START và JSON_END
- JSON phải hợp lệ 100%

"""

    if de_bai:
        prompt += f"\nĐỀ BÀI GIÁO VIÊN CUNG CẤP:\n{de_bai}\n"

    if dap_an_gv:
        prompt += f"\nĐÁP ÁN CHUẨN:\n{dap_an_gv}\n"

    return prompt
