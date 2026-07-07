"""Authentication service."""

from __future__ import annotations

from typing import Any

import bcrypt

from app.services.teacher_service import get_all_teachers, get_teacher_by_magv, get_teacher_by_username

DEFAULT_BGH_PASSWORD = "BGH123abc456"


def authenticate(username: str, password: str) -> dict | None:
    """Authenticate a user.

    Supported production login convention:
    - Username ``GV``: teacher logs in with password equal to ``Mã GV``.
    - Username ``BGH``: BGH logs in with password ``BGH123abc456``.

    Legacy username login is kept as a fallback so existing test accounts still
    work while the school transitions DM_GiaoVien to the shared GV/BGH login.
    """
    login_name = _normalize_key(username)
    password_text = str(password or "").strip()
    if not login_name or not password_text:
        return None

    if login_name in {"gv", "giao_vien", "giao_vien_"}:
        return _authenticate_teacher_by_default_password(password_text)

    if login_name in {"bgh", "ban_giam_hieu", "admin", "quan_tri", "quan_tri_vien"}:
        return _authenticate_by_role_and_default_password(
            target_roles={"bgh", "ban_giam_hieu", "admin", "quan_tri", "quan_tri_vien"},
            password=password_text,
            bgh_mode=True,
        )

    # Dự phòng cho cách đăng nhập cũ bằng tên tài khoản riêng.
    teacher = get_teacher_by_username(username)
    if teacher is None or not teacher.get("dang_hoat_dong"):
        return None

    password_hash = str(teacher.get("mat_khau_hash", "")).strip()
    if not password_hash:
        return None

    if not _check_password(password_text, password_hash):
        return None

    return teacher


def _authenticate_teacher_by_default_password(password: str) -> dict | None:
    """Xác thực giáo viên theo quy tắc chính thức: mật khẩu bằng MaGV.

    Luồng đăng nhập chung của giáo viên không cần kiểm tra bcrypt cho từng dòng.
    Tìm trực tiếp theo MaGV giúp tránh chậm khi DM_GiaoVien có nhiều tài khoản
    đã có MatKhauHash.
    """
    teacher = get_teacher_by_magv(password)
    if teacher is None or not teacher.get("dang_hoat_dong"):
        return None

    role = _normalize_key(teacher.get("vai_tro"))
    if role not in {"giao_vien", "gv", "teacher"}:
        return None

    ma_gv = str(teacher.get("ma_gv", "")).strip()
    if ma_gv and str(password or "").strip().lower() == ma_gv.lower():
        return teacher

    return None


def _authenticate_by_role_and_default_password(
    target_roles: set[str],
    password: str,
    bgh_mode: bool,
) -> dict | None:
    """Authenticate with shared login name and per-user default password rule."""
    for teacher in get_all_teachers():
        if not teacher.get("dang_hoat_dong"):
            continue

        role = _normalize_key(teacher.get("vai_tro"))
        if role not in target_roles:
            continue

        ma_gv = str(teacher.get("ma_gv", "")).strip()
        if not ma_gv:
            continue

        default_password = DEFAULT_BGH_PASSWORD if bgh_mode else ma_gv
        password_hash = str(teacher.get("mat_khau_hash", "")).strip()

        # During migration, some rows may still have an old hash or no hash.
        # Allow the official default password rule so BGH can log in and run
        # password normalization without being blocked by stale MatKhauHash.
        if password == default_password:
            return teacher

        if password_hash and _check_password(password, password_hash):
            return teacher

    return None


def _check_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def _normalize_key(value: Any) -> str:
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
