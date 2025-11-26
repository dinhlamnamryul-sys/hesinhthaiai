import streamlit as st
import google.generativeai as genai
import traceback

st.set_page_config(page_title="Debug Google GenerativeAI", layout="wide")
st.header("Debug Google Generative AI — kiểm tra môi trường & API")

# 1) Kiểm tra api key
try:
    key_present = "GOOGLE_API_KEY" in st.secrets
except Exception:
    key_present = False
st.write("GOOGLE_API_KEY in st.secrets?", key_present)

# 2) Phiên bản và một vài attribute
try:
    ver = getattr(genai, "__version__", "unknown")
except Exception:
    ver = "unknown"
st.write("google-generativeai __version__:", ver)

# show some attributes to understand API surface
attrs = sorted([a for a in dir(genai) if not a.startswith("_")])[:60]
st.write("Một số attribute chính của module `genai` (một lát):")
st.write(attrs)

# 3) Thử vài cách gọi "thăm dò" (không thực hiện gọi dài — dùng prompt ngắn)
prompt = "A simple test image of a red ball on white background"

results = []
def try_call(name, fn):
    try:
        res = fn()
        results.append((name, "OK", type(res).__name__))
    except Exception as e:
        tb = traceback.format_exc()
        results.append((name, "ERR", str(e), tb))

# Không gọi nếu không có key
if key_present:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    # Thử nhiều kiểu gọi mà SDK các phiên bản khác nhau có thể dùng
    try_call("GenerativeModel_generate_image", lambda: genai.GenerativeModel("imagen-2.0").generate_image(prompt=prompt))
    try_call("GenerativeModel_generate", lambda: genai.GenerativeModel("imagen-2.0").generate(prompt=prompt))
    try_call("genai.generate_image", lambda: genai.generate_image(prompt=prompt))
    try_call("genai.Image.create", lambda: genai.Image.create(prompt=prompt))
    try_call("genai.images.generate", lambda: genai.images.generate(prompt=prompt))
else:
    st.warning("Không có GOOGLE_API_KEY trong st.secrets — bỏ qua bước gọi API.")

# Hiển thị kết quả thử nghiệm
st.write("Kết quả thử nghiệm các phương thức:")
for r in results:
    if r[1] == "OK":
        st.success(f"{r[0]} => OK (return type: {r[2]})")
    else:
        st.error(f"{r[0]} => ERROR: {r[2]}")
        st.code(r[3][:2000])  # show head of traceback for privacy
