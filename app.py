"""Main Streamlit entry point for EVUS_ThiDua."""

from __future__ import annotations

import streamlit as st

from app.auth.login_page import render_login_page
from app.pages.bgh_score_page import render_bgh_score_page
from app.pages.teacher_score_page import render_teacher_score_page


st.set_page_config(
    page_title="EVUS Thi Đua",
    page_icon="EVUS",
    layout="wide",
)

APP_CSS = """
<style>
.block-container {
    padding-top: 4.5rem;
    padding-bottom: 2rem;
}
.ev-app-title {
    font-size: 1.85rem;
    padding-top: 0.5rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.ev-app-subtitle {
    opacity: 0.75;
    font-size: 0.92rem;
}
.ev-user-panel {
    width: 100%;
    display: flex;
    justify-content: flex-end;
    margin-top: 0.35rem;
    margin-bottom: 0.8rem;
}
.ev-user-card {
    max-width: 100%;
    min-width: 18rem;
    border: 1px solid rgba(128, 128, 128, 0.22);
    border-radius: 0.55rem;
    padding: 0.55rem 0.75rem;
    font-size: 0.88rem;
    line-height: 1.45;
    text-align: left;
    white-space: normal;
    overflow-wrap: anywhere;
}
@media (max-width: 900px) {
    .ev-user-panel { justify-content: flex-start; }
    .ev-user-card { min-width: 0; }
}
</style>
"""


def main() -> None:
    """Render application shell."""
    st.markdown(APP_CSS, unsafe_allow_html=True)

    teacher = st.session_state.get("teacher")
    if not isinstance(teacher, dict):
        render_login_page()
        return

    _render_authenticated_shell(teacher)
    if _is_bgh_user(teacher):
        render_bgh_score_page()
    else:
        render_teacher_score_page()


def _render_authenticated_shell(teacher: dict) -> None:
    """Render common header for authenticated users without clipping user name."""
    col_title, col_logout = st.columns([8, 1.4])

    with col_title:
        st.markdown('<div class="ev-app-title">EVUS Thi Đua</div>', unsafe_allow_html=True)
        st.markdown('<div class="ev-app-subtitle">Hệ thống chấm điểm thi đua giáo viên</div>', unsafe_allow_html=True)

    with col_logout:
        if st.button("Đăng xuất", use_container_width=True):
            for key in (
                "teacher",
                "user",
                "current_user",
                "auth_user",
                "m02_confirm_submit",
                "m02_pending_changed_rows",
                "m03_bgh_selected_phieu_id",
            ):
                st.session_state.pop(key, None)
            st.rerun()

    ho_ten = teacher.get("ho_ten") or teacher.get("Họ và tên") or ""
    vai_tro = teacher.get("vai_tro") or teacher.get("Vai trò") or ""
    ma_gv = teacher.get("ma_gv") or teacher.get("Mã GV") or ""
    st.markdown(
        f"""<div class="ev-user-panel"><div class="ev-user-card">
        <b>Giáo viên:</b> {ho_ten}<br>
        <b>Mã GV:</b> {ma_gv}<br>
        <b>Vai trò:</b> {vai_tro}
        </div></div>""",
        unsafe_allow_html=True,
    )


def _normalize_role(value: object) -> str:
    """Normalize user role text for routing."""
    text = str(value or "").strip().lower()
    replacements = {
        "ã": "a", "à": "a", "á": "a", "ả": "a", "ạ": "a", "ă": "a", "ằ": "a", "ắ": "a", "ẳ": "a", "ặ": "a", "â": "a", "ầ": "a", "ấ": "a", "ẩ": "a", "ậ": "a",
        "đ": "d", "è": "e", "é": "e", "ẻ": "e", "ẹ": "e", "ê": "e", "ề": "e", "ế": "e", "ể": "e", "ệ": "e",
        "ì": "i", "í": "i", "ỉ": "i", "ị": "i", "ò": "o", "ó": "o", "ỏ": "o", "ọ": "o", "ô": "o", "ồ": "o", "ố": "o", "ổ": "o", "ộ": "o", "ơ": "o", "ờ": "o", "ớ": "o", "ở": "o", "ợ": "o",
        "ù": "u", "ú": "u", "ủ": "u", "ụ": "u", "ư": "u", "ừ": "u", "ứ": "u", "ử": "u", "ự": "u", "ỳ": "y", "ý": "y", "ỷ": "y", "ỵ": "y",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return "_".join(text.replace("(", " ").replace(")", " ").replace("/", " ").split())


def _is_bgh_user(user: dict) -> bool:
    """Return True if the authenticated user should see BGH pages."""
    role = _normalize_role(user.get("vai_tro") or user.get("Vai trò") or user.get("role") or "")
    return role in {"bgh", "ban_giam_hieu", "admin", "quan_tri", "quan_tri_vien"}


if __name__ == "__main__":
    main()
