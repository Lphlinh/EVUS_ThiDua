"""System configuration service for EVUS_ThiDua.

This module reads and writes small application-level settings from the
System_Config worksheet. It is used for operational settings controlled by BGH,
not for business transaction data.
"""

from __future__ import annotations

from typing import Any

from app.services.audit_service import write_audit_log
from app.services.google_sheets_service import (
    clear_sheet_records_cache,
    get_worksheet,
    open_spreadsheet,
    read_sheet_records,
)
from app.utils.date_utils import now_iso

SHEET_SYSTEM_CONFIG = "System_Config"
KEY_TEACHER_SCORING_DEADLINE_DAY = "TEACHER_SCORING_DEADLINE_DAY"
ACTION_SYSTEM_CONFIG_UPDATE = "SYSTEM_CONFIG_UPDATE"
DEFAULT_TEACHER_SCORING_DEADLINE_DAY = 5

_HEADERS = ["Key", "Value", "UpdatedAt", "UpdatedBy", "GhiChu"]
_HEADER_ALIASES = {
    "Key": ("Key", "Khoa", "Khóa", "TenCauHinh", "Tên cấu hình"),
    "Value": ("Value", "GiaTri", "Giá trị", "Gia tri"),
    "UpdatedAt": ("UpdatedAt", "NgayCapNhat", "Ngày cập nhật", "Thời gian cập nhật"),
    "UpdatedBy": ("UpdatedBy", "NguoiCapNhat", "Người cập nhật"),
    "GhiChu": ("GhiChu", "Ghi chú", "GhiChu"),
}


def get_teacher_scoring_deadline_day() -> int:
    """Return the final allowed day for teacher self-scoring.

    If System_Config or the key does not exist yet, return the default value 5.
    """
    try:
        records = read_sheet_records(SHEET_SYSTEM_CONFIG)
    except Exception:
        return DEFAULT_TEACHER_SCORING_DEADLINE_DAY

    for record in records:
        key = _get_text(record, *_HEADER_ALIASES["Key"])
        if str(key).strip() != KEY_TEACHER_SCORING_DEADLINE_DAY:
            continue
        value = _get_text(record, *_HEADER_ALIASES["Value"])
        return _parse_deadline_day(value)

    return DEFAULT_TEACHER_SCORING_DEADLINE_DAY


def set_teacher_scoring_deadline_day(day: int, actor: str) -> dict[str, Any]:
    """Set the final allowed day for teacher self-scoring."""
    deadline_day = _parse_deadline_day(day)
    actor = str(actor or "BGH").strip() or "BGH"
    worksheet = _get_or_create_system_config_worksheet()
    header_map = _ensure_system_config_headers(worksheet)

    clear_sheet_records_cache(SHEET_SYSTEM_CONFIG)
    records = read_sheet_records(SHEET_SYSTEM_CONFIG)
    row_number = None
    for index, record in enumerate(records):
        key = _get_text(record, *_HEADER_ALIASES["Key"])
        if str(key).strip() == KEY_TEACHER_SCORING_DEADLINE_DAY:
            row_number = index + 2
            break

    timestamp = now_iso()
    row_values = {
        "Key": KEY_TEACHER_SCORING_DEADLINE_DAY,
        "Value": deadline_day,
        "UpdatedAt": timestamp,
        "UpdatedBy": actor,
        "GhiChu": "Ngày cuối giáo viên được tự chấm trong tháng.",
    }

    if row_number is None:
        max_col = max(header_map.values()) if header_map else len(_HEADERS)
        row = [""] * max_col
        for field, value in row_values.items():
            column_number = header_map.get(field)
            if column_number:
                row[column_number - 1] = value
        worksheet.append_row(row, value_input_option="USER_ENTERED")
    else:
        pending_updates: list[dict[str, Any]] = []
        for field, value in row_values.items():
            column_number = header_map.get(field)
            if column_number:
                pending_updates.append({"range": _a1(row_number, column_number), "values": [[value]]})
        if pending_updates:
            worksheet.batch_update(pending_updates, value_input_option="USER_ENTERED")

    clear_sheet_records_cache(SHEET_SYSTEM_CONFIG)
    write_audit_log(
        ACTION_SYSTEM_CONFIG_UPDATE,
        KEY_TEACHER_SCORING_DEADLINE_DAY,
        actor,
        f"Cập nhật thời hạn tự chấm đến hết ngày {deadline_day} mỗi tháng.",
    )
    return {"key": KEY_TEACHER_SCORING_DEADLINE_DAY, "value": deadline_day}


def _get_or_create_system_config_worksheet() -> Any:
    try:
        return get_worksheet(SHEET_SYSTEM_CONFIG)
    except Exception:
        spreadsheet = open_spreadsheet()
        worksheet = spreadsheet.add_worksheet(title=SHEET_SYSTEM_CONFIG, rows=50, cols=len(_HEADERS))
        worksheet.update("A1:E1", [_HEADERS], value_input_option="USER_ENTERED")
        clear_sheet_records_cache(SHEET_SYSTEM_CONFIG)
        return get_worksheet(SHEET_SYSTEM_CONFIG)


def _ensure_system_config_headers(worksheet: Any) -> dict[str, int]:
    """Ensure System_Config has the minimal headers required by this service.

    The sheet may already exist as an empty or manually created worksheet.
    Missing headers are appended to the first row instead of failing. Existing
    data is not deleted.
    """
    header_map = _get_header_map(worksheet)
    missing = [header for header in _HEADERS if header not in header_map]
    if not missing:
        return header_map

    headers = [str(value).strip() for value in worksheet.row_values(1)]
    if not any(headers):
        worksheet.update("A1:E1", [_HEADERS], value_input_option="USER_ENTERED")
    else:
        headers.extend(missing)
        end_col = _column_letter(len(headers))
        worksheet.update(f"A1:{end_col}1", [headers], value_input_option="USER_ENTERED")

    clear_sheet_records_cache(SHEET_SYSTEM_CONFIG)
    return _get_header_map(worksheet)


def _parse_deadline_day(value: Any) -> int:
    try:
        day = int(float(str(value).strip().replace(",", ".")))
    except (TypeError, ValueError):
        raise ValueError("Ngày cuối tự chấm phải là số nguyên từ 1 đến 31.")
    if not 1 <= day <= 31:
        raise ValueError("Ngày cuối tự chấm phải nằm trong khoảng từ 1 đến 31.")
    return day


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


def _column_letter(column_number: int) -> str:
    letters = ""
    col = int(column_number)
    while col:
        col, remainder = divmod(col - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def _a1(row_number: int, column_number: int) -> str:
    letters = ""
    col = int(column_number)
    while col:
        col, remainder = divmod(col - 1, 26)
        letters = chr(65 + remainder) + letters
    return f"{letters}{int(row_number)}"
