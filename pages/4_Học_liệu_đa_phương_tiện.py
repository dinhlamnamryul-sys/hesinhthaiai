import streamlit as st
import base64
from pptx import Presentation
from pptx.util import Inches, Pt
from moviepy.editor import TextClip, ImageClip, CompositeVideoClip
import os
from io import BytesIO
from PIL import Image


st.set_page_config(page_title="Hỗ trợ giáo viên soạn giảng AI", layout="wide")

st.title("🎓 Hỗ trợ giáo viên soạn giảng bằng AI")
st.write("Tạo hình ảnh – video – slide bài giảng nhanh chóng và dễ dàng.")

menu = st.sidebar.radio(
    "Chọn chức năng",
    ["Tạo hình minh hoạ", "Tạo video từ văn bản", "Tạo slide bài giảng"]
)


# ================================
# 1. IMAGE GENERATOR (AI Placeholder)
# ================================
if menu == "Tạo hình minh hoạ":
    st.header("🖼️ Tạo hình minh hoạ cho bài giảng")
    prompt = st.text_input("Nhập mô tả hình ảnh cần tạo")

    if st.button("Tạo ảnh"):
        if not prompt.strip():
            st.warning("Hãy nhập mô tả trước nhé!")
        else:
            # Placeholder: tạo ảnh đơn giản (không dùng AI thật)
            img = Image.new("RGB", (800, 500), color=(240, 240, 240))
            st.image(img, caption="Ảnh minh họa (sample)")
            st.info("Bạn có thể tích hợp API OpenAI hoặc Stable Diffusion để tạo ảnh thật!")



# ================================
# 2. VIDEO GENERATOR FROM TEXT
# ================================
elif menu == "Tạo video từ văn bản":
    st.header("🎬 Tạo video bài giảng từ văn bản")

    text = st.text_area("Nhập nội dung bài giảng (sẽ hiển thị trong video)", height=200)

    if st.button("Tạo video"):
        if not text.strip():
            st.warning("Hãy nhập văn bản!")
        else:
            st.info("Đang tạo video… vui lòng chờ")

            clip = TextClip(text, fontsize=40, color='white', bg_color='black', size=(1280, 720))
            clip = clip.set_duration(6)

            video_path = "output_video.mp4"
            clip.write_videofile(video_path, fps=24)

            with open(video_path, "rb") as f:
                st.video(f.read())
                st.download_button("Tải xuống video", data=f, file_name="video_bai_giang.mp4")

            os.remove(video_path)



# ================================
# 3. SLIDE GENERATOR
# ================================
elif menu == "Tạo slide bài giảng":
    st.header("📑 Tạo slide bài giảng (.pptx)")

    title = st.text_input("Tiêu đề bài giảng")
    content = st.text_area("Nội dung chính mỗi slide (mỗi dòng = 1 slide)", height=200)

    if st.button("Tạo slide"):
        if not title or not content.strip():
            st.warning("Nhập đủ tiêu đề và nội dung.")
        else:
            prs = Presentation()

            # Slide tiêu đề
            slide_layout = prs.slide_layouts[0]
            slide = prs.slides.add_slide(slide_layout)
            slide.shapes.title.text = title
            slide.placeholders[1].text = "Bài giảng được tạo tự động bằng AI"

            # Slide nội dung
            for line in content.split("\n"):
                if line.strip() == "":
                    continue

                slide_layout = prs.slide_layouts[1]
                slide = prs.slides.add_slide(slide_layout)
                slide.shapes.title.text = line[:40]  # Title = first 40 chars
                body = slide.placeholders[1].text = line

            # Xuất file
            output = BytesIO()
            prs.save(output)
            st.success("Tạo slide thành công!")

            st.download_button(
                "Tải file PPTX",
                data=output.getvalue(),
                file_name="slide_bai_giang.pptx"
            )
