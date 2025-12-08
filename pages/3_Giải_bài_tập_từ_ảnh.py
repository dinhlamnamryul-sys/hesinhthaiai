import requests
import json
import sys

API_KEY = "AIzaSyDcFcm10jyHGy0iqB9Y5Nm1eFAedFG2Zsc"   # <<< NHỚ DÁN KEY VÀO ĐÂY
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"


# ============================================================
# 1. Kiểm tra API key bằng lệnh ListModels
# ============================================================
def list_models():
    url = f"{BASE_URL}/models?key={API_KEY}"
    print("\n🔍 Đang gọi ListModels...\n")

    try:
        r = requests.get(url)
    except Exception as e:
        print("❌ Không thể kết nối đến API:", e)
        sys.exit()

    if r.status_code != 200:
        print("❌ Lỗi ListModels:", r.text)
        sys.exit()

    data = r.json()

    print("=== 📌 DANH SÁCH MODEL API KEY CỦA BẠN ĐƯỢC DÙNG ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("==================================================\n")

    return data.get("models", [])


# ============================================================
# 2. Lọc model hỗ trợ generateContent
# ============================================================
def filter_generation_models(models):
    valid = []
    for m in models:
        supported = m.get("supportedGenerationMethods", [])
        if "generateContent" in supported:
            valid.append(m)
    return valid


# ============================================================
# 3. Gửi thử một request generateContent
# ============================================================
def test_generate(model_name):
    print(f"\n🚀 Thử gọi generateContent với model: {model_name}\n")

    url = f"{BASE_URL}/models/{model_name}:generateContent?key={API_KEY}"

    body = {
        "contents": [
            {
                "parts": [
                    {"text": "Xin chào! Đây là bài test từ Python."}
                ]
            }
        ]
    }

    r = requests.post(url, json=body)

    if r.status_code != 200:
        print("❌ generateContent lỗi:")
        print(r.text)
        return

    print("✅ Kết quả trả về:")
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))


# ============================================================
# 4. MAIN
# ============================================================
def main():
    if API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️ Bạn chưa dán API KEY vào code!")
        return

    models = list_models()
    if not models:
        print("❌ Không có model nào được trả về.")
        return

    print("🔎 Đang lọc model hỗ trợ generateContent...\n")
    gen_models = filter_generation_models(models)

    if not gen_models:
        print("❌ KHÔNG CÓ model nào hỗ trợ generateContent.")
        print("➡ API KEY của bạn CHƯA được cấp quyền dùng Gemini text/multimodal.")
        print("➡ Không phải lỗi code – do hạn chế từ Google.")
        return

    print("=== 📌 MODEL generateContent khả dụng ===")
    for m in gen_models:
        print("•", m["name"])
    print("=========================================\n")

    # Test model đầu tiên tìm được
    test_generate(gen_models[0]["name"])


if __name__ == "__main__":
    main()
