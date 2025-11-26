import streamlit as st
from datetime import datetime
import base64, uuid, io
import mimetypes

st.set_page_config(page_title="Học liệu đa phương tiện", layout="wide")

# ---------------------------
# Helper utilities
# ---------------------------
def make_id():
    return str(uuid.uuid4())

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def get_mime_type(filename):
    m = mimetypes.guess_type(filename)[0]
    return m or "application/octet-stream"

def bytes_to_data_url(b, mime):
    data = base64.b64encode(b).decode()
    return f"data:{mime};base64,{data}"

# Simple flashcard generator:
def generate_flashcards_from_text(text, max_cards=8):
    """
    Heuristic:
    - Split paragraphs into sentences by '.!?'
    - Pair first clause as Q (or form cloze), remaining as A
    - Keep up to max_cards cards
    """
    import re
    sents = re.split(r'(?<=[\.\?\!])\s+', text.strip())
    cards = []
    i = 0
    while i < len(sents) and len(cards) < max_cards:
        q = sents[i].strip()
        a = ""
        if i+1 < len(sents):
            a = sents[i+1].strip()
            i += 2
        else:
            # If last sentence, create cloze-style
            words = q.split()
            if len(words) > 4:
                hide_idx = len(words)//3
                hidden = "____"
                a = q
                q = " ".join(words[:hide_idx]) + " " + hidden + " " + " ".join(words[hide_idx+1:])
            i += 1
        if q and a:
            cards.append({"q": q, "a": a})
    # If no cards, fallback: split by lines
    if not cards:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for ln in lines[:max_cards]:
            cards.append({"q": ln, "a": "(tóm tắt) " + ln})
    return cards

# ---------------------------
# Sample initial data
# ---------------------------
def sample_data():
    return {
        "Math": [
            {
                "id": make_id(),
                "title": "Toán 9 - Đại số: Phương trình bậc hai (PDF)",
                "type": "pdf",
                "tags": ["đại số", "bậc hai"],
                "uploaded_at": now(),
                "bytes": None,
                "filename": None,
                "description": "Tổng hợp lý thuyết phương trình bậc hai và bài tập."
            },
            {
                "id": make_id(),
                "title": "Ôn luyện hình học - video",
                "type": "video",
                "tags": ["hình học", "lý thuyết"],
                "uploaded_at": now(),
                "bytes": None,
                "filename": None,
                "description": "Video giải đề hình học cơ bản."
            }
        ],
        "Physics": [],
        "Chemistry": [],
        "Biology": [],
        "Literature": [],
        "History": [],
        "Geography": [],
        "English": [],
        "CS": [],
        "Art": [],
        "Music": []
    }

# Initialize session state
if "resources" not in st.session_state:
    st.session_state.resources = sample_data()
if "last_added" not in st.session_state:
    st.session_state.last_added = None

# ---------------------------
# UI
# ---------------------------
st.title("📚 Học liệu đa phương tiện")
st.write("Trang con để lưu, duyệt và tạo flashcards cho các tài liệu dạy & học từng môn.")

# Sidebar: subject + upload
with st.sidebar:
    st.header("Bộ lọc & Upload")
    subjects = list(st.session_state.resources.keys())
    subject = st.selectbox("Chọn môn", subjects)
    search = st.text_input("Tìm kiếm (tiêu đề, tag, mô tả)")
    type_filter = st.multiselect("Lọc theo loại", ["pdf", "image", "video", "audio", "text"], default=["pdf","image","video","audio","text"])

    st.markdown("---")
    st.subheader("Upload tài liệu mới")
    up_title = st.text_input("Tiêu đề")
    up_file = st.file_uploader("Chọn file (PDF, JPG, PNG, MP4, MP3, TXT)", type=["pdf","jpg","jpeg","png","mp4","mp3","txt"])
    up_tags = st.text_input("Thẻ (cách nhau dấu phẩy)")
    up_description = st.text_area("Mô tả ngắn")
    if st.button("Upload"):
        if not up_file or not up_title:
            st.warning("Cần chọn file và đặt tiêu đề trước khi upload.")
        else:
            raw = up_file.read()
            mime = get_mime_type(up_file.name)
            # Determine type
            if up_file.type.startswith("image"):
                rtype = "image"
            elif up_file.type.startswith("video"):
                rtype = "video"
            elif up_file.type.startswith("audio"):
                rtype = "audio"
            elif up_file.name.lower().endswith(".pdf"):
                rtype = "pdf"
            elif up_file.name.lower().endswith(".txt"):
                rtype = "text"
            else:
                rtype = "file"
            entry = {
                "id": make_id(),
                "title": up_title,
                "type": rtype,
                "tags": [t.strip() for t in up_tags.split(",") if t.strip()],
                "uploaded_at": now(),
                "bytes": raw,
                "filename": up_file.name,
                "description": up_description
            }
            st.session_state.resources[subject].insert(0, entry)
            st.session_state.last_added = entry
            st.success("Upload thành công!")

st.markdown("---")

# Main: show selected subject resources
col1, col2 = st.columns([3,1])

with col1:
    st.header(f"Tài nguyên môn: {subject}")
    # Search & filter through resources
    items = st.session_state.resources.get(subject, [])
    filtered = []
    q = search.lower().strip()
    for it in items:
        if it["type"] not in type_filter:
            continue
        hay = " ".join([it.get("title",""), " ".join(it.get("tags",[])), it.get("description","")]).lower()
        if q and q not in hay:
            continue
        filtered.append(it)

    if not filtered:
        st.info("Chưa có tài nguyên thỏa tiêu chí. Bạn có thể upload thêm ở thanh bên.")
    else:
        # display as cards (2 columns)
        cols = st.columns(2)
        for i, it in enumerate(filtered):
            c = cols[i % 2]
            with c:
                st.markdown(f"**{it['title']}**")
                st.caption(f"Loại: {it['type']} • Tags: {', '.join(it.get('tags',[]))} • {it['uploaded_at']}")
                if it["description"]:
                    st.write(it["description"])
                # Preview depending on type & availability
                if it["bytes"]:
                    mime = get_mime_type(it["filename"] or "")
                    if it["type"] == "image":
                        st.image(it["bytes"], use_column_width=True, caption=it.get("filename",""))
                        st.download_button("Tải ảnh", data=it["bytes"], file_name=it["filename"])
                    elif it["type"] == "video":
                        st.video(it["bytes"])
                        st.download_button("Tải video", data=it["bytes"], file_name=it["filename"])
                    elif it["type"] == "audio":
                        st.audio(it["bytes"])
                        st.download_button("Tải audio", data=it["bytes"], file_name=it["filename"])
                    elif it["type"] == "pdf":
                        # embed pdf via data url
                        url = bytes_to_data_url(it["bytes"], "application/pdf")
                        st.markdown(f'<iframe src="{url}" width="100%" height="300px"></iframe>', unsafe_allow_html=True)
                        st.download_button("Tải PDF", data=it["bytes"], file_name=it["filename"])
                    elif it["type"] == "text":
                        txt = it["bytes"].decode(errors="ignore")
                        with st.expander("Xem nội dung"):
                            st.text_area("Nội dung", value=txt, height=200)
                            # Flashcards
                            if st.button("Tạo flashcards từ tài liệu", key=f"fc_{it['id']}"):
                                cards = generate_flashcards_from_text(txt)
                                st.session_state[f"cards_{it['id']}"] = cards
                                st.success(f"Tạo {len(cards)} flashcards.")
                    else:
                        st.write("Tệp đã upload.")
                        st.download_button("Tải về", data=it["bytes"], file_name=it["filename"])
                else:
                    # No bytes (sample placeholders) - show type-specific placeholder
                    if it["type"] == "pdf":
                        st.info("PDF (placeholder). Upload file để xem ngay.")
                    elif it["type"] == "video":
                        st.info("Video (placeholder). Upload file để xem ngay.")
                    elif it["type"] == "image":
                        st.info("Ảnh (placeholder). Upload file để xem ngay.")
                    elif it["type"] == "text":
                        st.info("Tài liệu văn bản (placeholder). Upload file để xem ngay.")
                st.markdown("---")

with col2:
    st.header("Tiện ích nhanh")
    st.write("Các tài nguyên vừa mới thêm:")
    if st.session_state.last_added:
        la = st.session_state.last_added
        st.write(f"- **{la['title']}** ({la['type']}) • {la['uploaded_at']}")
    else:
        st.write("Chưa có tài liệu mới.")

    st.markdown("### Tạo flashcards từ văn bản nhanh")
    sample_text = st.text_area("Dán phần văn bản cần tạo flashcards (ví dụ 1 đoạn lý thuyết)", height=180)
    if st.button("Tạo flashcards"):
        if not sample_text.strip():
            st.warning("Hãy dán văn bản trước.")
        else:
            cards = generate_flashcards_from_text(sample_text, max_cards=12)
            st.session_state["tmp_cards"] = cards
            st.success(f"Tạo {len(cards)} flashcards. Xem bên dưới.")

    if "tmp_cards" in st.session_state:
        st.markdown("**Flashcards tạm**")
        for idx, c in enumerate(st.session_state["tmp_cards"]):
            st.write(f"**Q{idx+1}.** {c['q']}")
            with st.expander("Xem đáp án"):
                st.write(c["a"])

    st.markdown("---")
    st.markdown("### Xuất báo cáo môn")
    if st.button("Xuất danh sách tài nguyên (CSV)"):
        import csv, io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["subject","title","type","tags","uploaded_at","filename"])
        for subj, items in st.session_state.resources.items():
            for it in items:
                writer.writerow([subj, it.get("title",""), it.get("type",""), ";".join(it.get("tags",[])), it.get("uploaded_at",""), it.get("filename","") or ""])
        st.download_button("Tải CSV danh sách tài nguyên", data=output.getvalue().encode('utf-8'), file_name=f"resources_{subject}.csv")

st.markdown("---")
st.caption("Gợi ý: Bạn có thể mở rộng app này để: (1) kết nối database (SQLite/Postgres), (2) tích hợp NLP (summarization/QA), (3) cho phép chia sẻ công khai/nhóm, (4) thêm analytics cho GV & trường.")

# Footer quick help
with st.expander("Hướng dẫn nhanh"):
    st.markdown("""
    - Chọn môn ở thanh bên để xem tài nguyên của môn đó.  
    - Upload file (PDF/MP4/MP3/PNG/JPG/TXT) trên sidebar, chọn tiêu đề + thẻ để quản lý.  
    - Với tài liệu văn bản (.txt) bạn có thể tạo flashcards tự động.  
    - Bạn có thể mở rộng phần `generate_flashcards_from_text` để dùng model tóm tắt / tạo câu hỏi (cần API ngoài).
    """)

