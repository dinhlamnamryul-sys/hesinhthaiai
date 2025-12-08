def call_gemini_api(api_key, prompt, model="models/gemini-2.0-flash", image=None):
    # ... (giữ nguyên logic gọi API, chỉ cần chỉnh sửa phần payload)
    
    parts = [{"text": prompt}]
    if image is not None:
        # Thêm logic xử lý image_base64 từ image (giống trong analyze_real_image)
        # ...
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": img_base64}})
        
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": parts
            }
        ],
        "config": {
            # Tăng nhiệt độ (temperature) để câu hỏi đa dạng hơn khi tạo đề
            "temperature": 0.8 
        }
    }
    
    # ... (giữ nguyên phần requests.post và xử lý lỗi)
    # ...
