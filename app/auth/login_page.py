"""Compact login page for EVUS_ThiDua."""

from __future__ import annotations

import streamlit as st

from app.services.auth_service import authenticate


LOGIN_CSS = """
<style>
.ev-login-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 2rem;
    margin-bottom: 0.25rem;
}
.ev-login-subtitle {
    text-align: center;
    opacity: 0.75;
    margin-bottom: 2rem;
}
/* Make the login form compact instead of full screen width. */
div[data-testid="stForm"] {
    border: 1px solid rgba(128, 128, 128, 0.25);
    border-radius: 0.75rem;
    padding: 1.25rem 1.25rem 1rem 1.25rem;
}
</style>
"""


def render_login_page() -> None:
    """Render compact login form.

    Streamlit form supports pressing Enter in the password field to submit.
    The login button remains available for phone/tablet users.
    """
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    st.markdown('<div class="ev-login-title">EVUS Thi Đua</div>', unsafe_allow_html=True)
    st.markdown('<div class="ev-login-subtitle">Đăng nhập để tự chấm phiếu thi đua tháng</div>', unsafe_allow_html=True)

    left, center, right = st.columns([1.4, 1, 1.4])
    with center:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Tên đăng nhập", key="login_username")
            password = st.text_input("Mật khẩu", type="password", key="login_password")
            submitted = st.form_submit_button("Đăng nhập", use_container_width=True)

        if submitted:
            teacher = authenticate(username, password)
            if teacher is None:
                st.error("Tên đăng nhập hoặc mật khẩu không đúng.")
                return

            st.session_state["teacher"] = teacher
            st.session_state["user"] = teacher
            st.rerun()
