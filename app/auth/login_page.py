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
.ev-login-account-box {
    border: 1px solid rgba(128, 128, 128, 0.22);
    border-radius: 0.5rem;
    padding: 0.65rem 0.75rem;
    margin: 0.25rem 0 0.75rem 0;
    background: rgba(128, 128, 128, 0.04);
    font-size: 0.95rem;
}
.ev-login-account-code {
    font-size: 1.2rem;
    font-weight: 800;
    color: #b91c1c;
}
/* Make the login form compact instead of full screen width. */
div[data-testid="stForm"] {
    border: 1px solid rgba(128, 128, 128, 0.25);
    border-radius: 0.75rem;
    padding: 1.25rem 1.25rem 1rem 1.25rem;
}
</style>
"""


LOGIN_ROLE_TO_USERNAME = {
    "Giáo viên": "GV",
    "Ban Giám hiệu": "BGH",
}


def render_login_page() -> None:
    """Render compact login form.

    Users choose the account type instead of typing the shared account name.
    Streamlit form supports pressing Enter in the password field to submit.
    The login button remains available for phone/tablet users.
    """
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    st.markdown('<div class="ev-login-title">EVUS Thi Đua</div>', unsafe_allow_html=True)
    st.markdown('<div class="ev-login-subtitle">Đăng nhập để tự chấm phiếu thi đua tháng</div>', unsafe_allow_html=True)

    left, center, right = st.columns([1.4, 1, 1.4])
    with center:
        with st.form("login_form", clear_on_submit=False):
            role_label = st.selectbox(
                "Đăng nhập với",
                list(LOGIN_ROLE_TO_USERNAME.keys()),
                key="login_role_label",
            )
            username = LOGIN_ROLE_TO_USERNAME[role_label]
            st.markdown(
                f'''
                <div class="ev-login-account-box">
                    Tài khoản<br>
                    <span class="ev-login-account-code">{username}</span>
                </div>
                ''',
                unsafe_allow_html=True,
            )
            password_label = "Mật khẩu (Mã GV)" if username == "GV" else "Mật khẩu"
            password = st.text_input(password_label, type="password", key="login_password")
            submitted = st.form_submit_button("Đăng nhập", use_container_width=True)

        if submitted:
            teacher = authenticate(username, password)
            if teacher is None:
                st.error("Tài khoản hoặc mật khẩu không đúng.")
                return

            st.session_state["teacher"] = teacher
            st.session_state["user"] = teacher
            st.rerun()
