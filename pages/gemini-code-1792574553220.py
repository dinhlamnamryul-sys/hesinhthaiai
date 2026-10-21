import streamlit as st
import json
import os
import random
from streamlit_google_auth import Authenticate

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Trò Chơi Học Tập", page_icon="🎮", layout="wide")

# --- CSS TÙY CHỈNH ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    .stApp { background-color: #f0f4f8; background-image: radial-gradient(#dde1e7 1px, transparent 1px); background-size: 20px 20px; }
    .game-card { background: linear-gradient(135deg, #ffffff, #f3e5f5); border-radius: 15px; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; border: 2px solid #ce93d8; transition: transform 0.2s; }
    .game-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
    .teacher-panel { background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1976d2; margin-top: 20px;}
    .stButton>button { background: linear-gradient(to right, #1976d2, #1565c0); color: white; border: none; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- QUẢN LÝ DỮ LIỆU CÂU HỎI ---
DATA_FILE = "game_questions.json"

def load_questions():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_questions(questions):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)

if 'questions' not in st.session_state:
    st.session_state.questions = load_questions()

# --- KHỞI TẠO SESSION TRÒ CHƠI ---
if 'user_role' not in st.session_state:
    st.session_state.user_role = "Chưa chọn"
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'enemy_score' not in st.session_state:
    st.session_state.enemy_score = 0
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0

# --- CẤU HÌNH ĐĂNG NHẬP GOOGLE ---
# Lưu ý: Yêu cầu file google_credentials.json tải từ Google Cloud Console
try:
    authenticator = Authenticate(
        secret_credentials_path='google_credentials.json',
        cookie_name='gv_na_u_cookie',
        cookie_key='na_u_secret_key_2026',
        redirect_uri='http://localhost:8501', # Đổi thành URL trang web của bạn khi deploy lên Streamlit Cloud
    )
    # Kiểm tra trạng thái đăng nhập
    authenticator.check_authentification()
    is_google_configured = True
except Exception as e:
    is_google_configured = False
    google_error = e

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='text-align: center; color: #4a148c;'>🎮 KHÔNG GIAN TRÒ CHƠI HỌC TẬP</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Đổi mới phương pháp giảng dạy - Tương tác thời gian thực</p>", unsafe_allow_html=True)
st.markdown("---")

col_role1, col_role2 = st.columns(2)
with col_role1:
    if st.button("👨‍🏫 DÀNH CHO GIÁO VIÊN", use_container_width=True):
        st.session_state.user_role = "Giáo viên"
        st.session_state.game_active = False
with col_role2:
    if st.button("👦 DÀNH CHO HỌC SINH", use_container_width=True):
        st.session_state.user_role = "Học sinh"

# ==========================================
# KHU VỰC GIÁO VIÊN (BẢO MẬT GOOGLE)
# ==========================================
if st.session_state.user_role == "Giáo viên":
    st.subheader("🔐 Cổng quản trị Giáo viên")
    
    if not is_google_configured:
        st.error("Hệ thống chưa tìm thấy file `google_credentials.json`.")
        st.info("Vui lòng truy cập Google Cloud Console, tạo OAuth 2.0 Client ID, tải file JSON về và đổi tên thành `google_credentials.json` để trong cùng thư mục gốc của dự án.")
    else:
        # Nếu chưa đăng nhập
        if not st.session_state.get('connected'):
            st.info("Khu vực này yêu cầu xác thực bằng tài khoản Google để bảo vệ ngân hàng đề thi.")
            # Nút đăng nhập Google sinh tự động từ thư viện
            authenticator.login()
        
        # Nếu đã đăng nhập thành công
        else:
            user_info = st.session_state.get('user_info', {})
            email = user_info.get('email', 'Giáo viên')
            avatar = user_info.get('picture', '')
            
            col_avt, col_info = st.columns([1, 10])
            if avatar:
                col_avt.image(avatar, width=50)
            col_info.markdown(f"**Đang đăng nhập:** {email}")
            
            if st.button("Đăng xuất"):
                authenticator.logout()
            
            st.markdown('<div class="teacher-panel">', unsafe_allow_html=True)
            st.markdown("### 📝 Soạn câu hỏi đưa lên hệ thống Trò chơi")
            
            with st.form("form_soan_cau_hoi"):
                mon_hoc = st.selectbox("Môn học:", ["Toán", "Tiếng Việt", "Lịch Sử", "Địa Lý", "Khoa học", "Tiếng Anh"])
                cau_hoi = st.text_area("Nội dung câu hỏi:")
                col_a, col_b = st.columns(2)
                da_a = col_a.text_input("Đáp án A:")
                da_b = col_b.text_input("Đáp án B:")
                col_c, col_d = st.columns(2)
                da_c = col_c.text_input("Đáp án C:")
                da_d = col_d.text_input("Đáp án D:")
                
                dap_an_dung = st.selectbox("Đáp án đúng:", ["A", "B", "C", "D"])
                
                submit_btn = st.form_submit_button("Lưu câu hỏi vào Kho")
                
                if submit_btn and cau_hoi and da_a and da_b:
                    new_q = {
                        "mon": mon_hoc,
                        "cau_hoi": cau_hoi,
                        "A": da_a, "B": da_b, "C": da_c, "D": da_d,
                        "dap_an_dung": dap_an_dung,
                        "nguoi_tao": email
                    }
                    st.session_state.questions.append(new_q)
                    save_questions(st.session_state.questions)
                    st.success("Đã thêm câu hỏi thành công! Học sinh đã có thể chơi ngay ở màn hình của các em.")
            
            with st.expander("📂 Quản lý kho câu hỏi Trò chơi"):
                if st.session_state.questions:
                    for i, q in enumerate(st.session_state.questions):
                        st.write(f"**Câu {i+1} ({q['mon']}):** {q['cau_hoi']} -> Đáp án đúng: {q['dap_an_dung']}")
                else:
                    st.write("Kho câu hỏi đang trống.")
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# KHU VỰC HỌC SINH (CHƠI GAME)
# ==========================================
elif st.session_state.user_role == "Học sinh":
    if not st.session_state.questions:
        st.warning("Thầy cô chưa đưa câu hỏi nào lên hệ thống. Em hãy quay lại sau nhé!")
    else:
        if not st.session_state.game_active:
            st.subheader("🎪 DANH SÁCH TRÒ CHƠI")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="game-card">
                    <h3 style="color:#d32f2f;">🛶 Đua Thuyền</h3>
                    <p>Trả lời đúng để giúp thuyền của bạn vượt lên trước cướp biển.</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Chơi ngay", key="btn_duathuyen", use_container_width=True):
                    st.session_state.game_active = True
                    st.session_state.player_score = 0
                    st.session_state.enemy_score = 0
                    st.session_state.current_q_index = 0
                    random.shuffle(st.session_state.questions)
                    st.rerun()
            
            with col2:
                st.markdown("""
                <div class="game-card">
                    <h3 style="color:#388e3c;">🧟 Chặn Zombie</h3>
                    <p>Sắp ra mắt! Dùng kiến thức để xây rào chắn zombie.</p>
                </div>
                """, unsafe_allow_html=True)
                st.button("Đang bảo trì", disabled=True, use_container_width=True)
                
            with col3:
                st.markdown("""
                <div class="game-card">
                    <h3 style="color:#1976d2;">🎯 Vòng Quay</h3>
                    <p>Sắp ra mắt! Trả lời đúng nhận lượt quay.</p>
                </div>
                """, unsafe_allow_html=True)
                st.button("Bảo trì", disabled=True, key="bt2", use_container_width=True)

        # --- LOGIC ĐUA THUYỀN ---
        if st.session_state.game_active:
            st.markdown("## 🛶 TRƯỜNG ĐUA KIẾN THỨC")
            
            # Thanh tiến trình
            st.write("🚣 **Thuyền của bạn:**")
            st.progress(min(st.session_state.player_score * 20, 100))
            st.write("🏴‍☠️ **Thuyền cướp biển:**")
            st.progress(min(st.session_state.enemy_score * 20, 100))
            st.markdown("---")
            
            # Check thắng thua (5 điểm là đích)
            if st.session_state.player_score >= 5:
                st.balloons()
                st.success("🏆 CHÚC MỪNG! BẠN ĐÃ VỀ ĐÍCH TRƯỚC VÀ CHIẾN THẮNG!")
                if st.button("Chơi lại từ đầu"):
                    st.session_state.game_active = False
                    st.rerun()
            elif st.session_state.enemy_score >= 5:
                st.error("💀 Rất tiếc, cướp biển đã vượt qua bạn. Hãy ôn bài và thử lại nhé!")
                if st.button("Phục thù!"):
                    st.session_state.game_active = False
                    st.rerun()
            else:
                if st.session_state.current_q_index < len(st.session_state.questions):
                    q = st.session_state.questions[st.session_state.current_q_index]
                    
                    st.markdown(f"### ❓ Câu hỏi: {q['cau_hoi']}")
                    
                    c1, c2 = st.columns(2)
                    c3, c4 = st.columns(2)
                    
                    def check_answer(ans):
                        if ans == q['dap_an_dung']:
                            st.session_state.player_score += 1
                            st.toast("✅ Chính xác! Thuyền tiến lên.")
                        else:
                            st.session_state.enemy_score += 1
                            st.toast("❌ Sai rồi! Cướp biển tiến lên.")
                        st.session_state.current_q_index += 1
                    
                    if c1.button(f"A. {q['A']}", use_container_width=True): check_answer("A"); st.rerun()
                    if c2.button(f"B. {q['B']}", use_container_width=True): check_answer("B"); st.rerun()
                    if c3.button(f"C. {q['C']}", use_container_width=True): check_answer("C"); st.rerun()
                    if c4.button(f"D. {q['D']}", use_container_width=True): check_answer("D"); st.rerun()
                else:
                    st.info("Đã hết câu hỏi trong kho! Cướp biển và bạn đang hòa nhau.")
                    if st.button("Thoát"):
                        st.session_state.game_active = False
                        st.rerun()