"""Account service for EVUS_ThiDua.

This module handles password-hash initialization for DM_GiaoVien.
It does not change teacher/business identifiers.
"""

from __future__ import annotations

from typing import Any

import bcrypt

from app.services.audit_service import write_audit_log
from app.services.google_sheets_service import (
    clear_sheet_records_cache,
    get_worksheet,
    read_sheet_records,
)

SHEET_DM_GIAOVIEN = "DM_GiaoVien"
ACTION_ACCOUNT_PASSWORD_NORMALIZE = "ACCOUNT_PASSWORD_NORMALIZE"
DEFAULT_BGH_PASSWORD = "BGH123abc456"

_REQUIRED_COLUMNS = ("MaGV", "HoTen", "VaiTro", "DangHoatDong", "MatKhauHash")

_HEADER_ALIASES = {
    "MaGV": ("Mã GV", "Ma GV", "MaGV", "Mã giáo viên", "Ma giao vien"),
    "HoTen": ("Họ và tên", "Ho va ten", "HoTen", "Họ tên", "Ho ten"),
        "VaiTro": ("Vai trò", "Vai tro", "VaiTro", "Role"),
    "DangHoatDong": ("Đang hoạt động", "Dang hoat dong", "DangHoatDong", "Active"),
    "MatKhauHash": ("MatKhauHash", "Mật khẩu hash", "Mat khau hash", "PasswordHash"),
}


def normalize_missing_password_hashes(actor: str) -> dict[str, Any]:
    """Hash default passwords only for active DM_GiaoVien rows missing MatKhauHash.

    This function never overwrites an existing password hash. It is safe to run
    after adding new teachers to DM_GiaoVien.
    """
    return _apply_default_password_hashes(actor=actor)


def _apply_default_password_hashes(actor: str) -> dict[str, Any]:
    # DM_GiaoVien may be edited directly in Google Sheets while the app is running.
    # Clear the cached records before scanning so newly added teachers are included.
    clear_sheet_records_cache(SHEET_DM_GIAOVIEN)
    worksheet = get_worksheet(SHEET_DM_GIAOVIEN)
    header_map = _get_header_map(worksheet)
    missing = [column for column in _REQUIRED_COLUMNS if column not in header_map]
    if missing:
        raise ValueError("DM_GiaoVien thiếu cột bắt buộc để chuẩn hóa mật khẩu: " + ", ".join(missing))

    records = read_sheet_records(SHEET_DM_GIAOVIEN)
    pending_updates: list[dict[str, Any]] = []
    updated_users: list[str] = []
    skipped_has_hash = 0
    skipped_inactive = 0
    skipped_missing_id = 0

    password_hash_col = header_map["MatKhauHash"]

    for index, record in enumerate(records):
        row_number = index + 2
        ma_gv = _get_text(record, *_HEADER_ALIASES["MaGV"])
        ho_ten = _get_text(record, *_HEADER_ALIASES["HoTen"])
        vai_tro = _get_text(record, *_HEADER_ALIASES["VaiTro"])
        active = _parse_bool(_get_text(record, *_HEADER_ALIASES["DangHoatDong"]))
        current_hash = _get_text(record, *_HEADER_ALIASES["MatKhauHash"])

        if not active:
            skipped_inactive += 1
            continue
        if not ma_gv:
            skipped_missing_id += 1
            continue
        if current_hash:
            skipped_has_hash += 1
            continue

        default_password = _default_password_for_user(ma_gv=ma_gv, vai_tro=vai_tro)
        password_hash = _hash_password(default_password)
        pending_updates.append({"range": _a1(row_number, password_hash_col), "values": [[password_hash]]})
        updated_users.append(f"{ma_gv} - {ho_ten}" if ho_ten else ma_gv)

    if pending_updates:
        worksheet.batch_update(pending_updates, value_input_option="USER_ENTERED")
        clear_sheet_records_cache(SHEET_DM_GIAOVIEN)

    action = ACTION_ACCOUNT_PASSWORD_NORMALIZE
    note = (
        f"Khởi tạo mật khẩu cho tài khoản mới trong DM_GiaoVien. Ghi hash: {len(updated_users)}. "
        f"Bỏ qua đã có hash: {skipped_has_hash}. Bỏ qua không hoạt động: {skipped_inactive}. "
        f"Bỏ qua thiếu Mã GV: {skipped_missing_id}."
    )
    write_audit_log(action, SHEET_DM_GIAOVIEN, actor, note)

    return {
        "updated_count": len(updated_users),
        "updated_users": updated_users,
        "skipped_has_hash": skipped_has_hash,
        "skipped_inactive": skipped_inactive,
        "skipped_missing_id": skipped_missing_id,
    }


def _default_password_for_user(ma_gv: str, vai_tro: str) -> str:
    role = _normalize_key(vai_tro)
    if role in {"bgh", "ban_giam_hieu", "admin", "quan_tri", "quan_tri_vien"}:
        return DEFAULT_BGH_PASSWORD
    return str(ma_gv).strip()


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(str(password).encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _get_header_map(worksheet: Any) -> dict[str, int]:
    headers = worksheet.row_values(1)
    normalized_headers = {_normalize_key(header): index + 1 for index, header in enumerate(headers)}
    result: dict[str, int] = {}
    for canonical, aliases in _HEADER_ALIASES.items():
        for alias in aliases:
            column = normalized_headers.get(_normalize_key(alias))
            if column:
                result[canonical] = column
                break
    return result


def _get_text(record: dict, *keys: str) -> str:
    normalized = {_normalize_key(key): value for key, value in record.items()}
    for key in keys:
        value = record.get(key)
        if value is not None and str(value).strip() != "":
            return str(value).strip()
        normalized_value = normalized.get(_normalize_key(key))
        if normalized_value is not None and str(normalized_value).strip() != "":
            return str(normalized_value).strip()
    return ""


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y", "x", "co", "có"}


def _normalize_key(value: object) -> str:
    text = str(value).strip().lower()
    replacements = {
        "ã": "a", "à": "a", "á": "a", "ả": "a", "ạ": "a", "ă": "a", "ằ": "a", "ắ": "a", "ẳ": "a", "ặ": "a", "â": "a", "ầ": "a", "ấ": "a", "ẩ": "a", "ậ": "a",
        "đ": "d", "è": "e", "é": "e", "ẻ": "e", "ẹ": "e", "ê": "e", "ề": "e", "ế": "e", "ể": "e", "ệ": "e",
        "ì": "i", "í": "i", "ỉ": "i", "ị": "i", "ò": "o", "ó": "o", "ỏ": "o", "ọ": "o", "ô": "o", "ồ": "o", "ố": "o", "ổ": "o", "ộ": "o", "ơ": "o", "ờ": "o", "ớ": "o", "ở": "o", "ợ": "o",
        "ù": "u", "ú": "u", "ủ": "u", "ụ": "u", "ư": "u", "ừ": "u", "ứ": "u", "ử": "u", "ự": "u", "ỳ": "y", "ý": "y", "ỷ": "y", "ỵ": "y",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return "_".join(text.replace("(", " ").replace(")", " ").replace("/", " ").split())


def _a1(row_number: int, column_number: int) -> str:
    letters = ""
    col = int(column_number)
    while col:
        col, remainder = divmod(col - 1, 26)
        letters = chr(65 + remainder) + letters
    return f"{letters}{int(row_number)}"
