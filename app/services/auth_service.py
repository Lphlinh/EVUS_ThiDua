"""Authentication service."""

from __future__ import annotations

import bcrypt

from app.services.teacher_service import get_teacher_by_username


def authenticate(username: str, password: str) -> dict | None:
    """
    Authenticate a user.

    Returns:
        Teacher information if authentication succeeds.
        None if authentication fails.
    """

    teacher = get_teacher_by_username(username)

    if teacher is None:
        return None

    if not teacher["dang_hoat_dong"]:
        return None

    password_hash = teacher["mat_khau_hash"]

    if not password_hash:
        return None

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8"),
    ):
        return None

    return teacher