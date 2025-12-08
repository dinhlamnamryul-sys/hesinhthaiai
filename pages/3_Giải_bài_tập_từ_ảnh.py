#!/usr/bin/env python3
"""
check_gemini_models.py
- Lấy danh sách model từ Generative Language API (v1beta)
- Lọc model có supportedGenerationMethods chứa "generateContent"
- Lưu kết quả vào models_output.json
- Không chứa API key cứng trong mã (dùng biến môi trường hoặc nhập)
"""

import requests
import json
import os
import sys
from getpass import getpass

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

def get_api_key():
    # Ưu tiên biến môi trường
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("🔑 API Key lấy từ biến môi trường GEMINI_API_KEY")
        return api_key.strip()
    # Nếu không có, cho phép nhập (nhưng cảnh báo)
    print("⚠ Không tìm thấy biến môi trường GEMINI_API_KEY.")
    print("⚠ Nếu bạn nhập key ở đây, KHÔNG dán key lên chat hoặc kho công khai.")
    api_key = getpass("Nhập Google API Key (input ẩn): ").strip()
    if not api_key:
        print("❌ Không có API key. Thoát.")
        sys.exit(1)
    return api_key

def list_models(api_key, timeout=20):
    url = f"{BASE_URL}/models?key={api_key}"
    try:
        r = requests.get(url, timeout=timeout)
    except requests.exceptions.RequestException as e:
        return None, f"Không thể kết nối tới API: {e}"

    try:
        data = r.json()
    except Exception:
        return None, f"API trả về không phải JSON. Status: {r.status_code}, Text: {r.text}"

    if r.status_code != 200:
        # Trả về chi tiết lỗi
        return None, f"ListModels lỗi HTTP {r.status_code}: {json.dumps(data, ensure_ascii=False)}"

    return data.get("models", []), None

def filter_generation_models(models):
    gen = []
    for m in models:
        methods = m.get("supportedGenerationMethods", [])
        if "generateContent" in methods:
            gen.append(m)
    return gen

def print_summary(models, gen_models):
    print("\n=== TỔNG QUAN ===")
    print(f"• Tổng model trả về: {len(models)}")
    print(f"• Model hỗ trợ generateContent: {len(gen_models)}")
    print("=================\n")

    if gen_models:
        print("📌 Danh sách model hỗ trợ generateContent (tên):")
        for m in gen_models:
            print(" -", m.get("name"))
    else:
        print("⚠ Không tìm thấy model hỗ trợ generateContent cho API key này.")

def save_output(raw_data, filename="models_output.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Đã lưu output vào {filename}")
    except Exception as e:
        print("⚠ Lỗi khi lưu file:", e)

def test_generate(api_key, model_name):
    print(f"\n🚀 Thử generateContent với model: {model_name}")
    url = f"{BASE_URL}/models/{model_name}:generateContent?key={api_key}"
    body = {
        "contents": [
            {"parts": [{"text": "Hello test from local script. Please return any small text."}]}
        ]
    }
    try:
        r = requests.post(url, json=body, timeout=30)
    except requests.exceptions.RequestException as e:
        print("❌ Lỗi khi gọi generateContent:", e)
        return

    print("HTTP Status:", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except Exception:
        print("Raw response text:", r.text)

def main():
    api_key = get_api_key()

    models, err = list_models(api_key)
    if err:
        print("❌", err)
        print("\nHƯỚNG XỬ LÝ:")
        print(" - Nếu lỗi 401/403: kiểm tra credentials, billing, permission.")
        print(" - Nếu lỗi 404 theo dạng 'model X not found...' khi gọi generateContent: hãy xem danh sách models trả về để chọn model chính xác.")
        print(" - Nếu không có model hỗ trợ generateContent: API key của bạn không có quyền dùng Gemini text/multimodal.")
        sys.exit(1)

    # Lưu raw data đầy đủ để bạn gửi cho trợ giúp nếu cần (không dán key)
    raw = {"models": models}
    save_output(raw)

    gen_models = filter_generation_models(models)
    print_summary(models, gen_models)

    # Nếu có model generateContent, thử gọi model đầu tiên
    if gen_models:
        first = gen_models[0].get("name")
        test_generate(api_key, first)
    else:
        # In toàn bộ models (tên và supportedGenerationMethods) để tiện debug
        print("\n--- Toàn bộ models (name + supportedGenerationMethods) ---")
        for m in models:
            print("•", m.get("name"), "=>", m.get("supportedGenerationMethods", []))
        print("-----------------------------------------------------------")
        print("\nKẾT LUẬN: Bạn cần yêu cầu quyền sử dụng Gemini text/multimodal từ Google (hoặc kiểm tra Billing, project, region, quota).")

if __name__ == "__main__":
    main()
