"""Teacher service for EVUS_ThiDua.

This module handles teacher-related business logic based on DM_GiaoVien.
"""

from __future__ import annotations

import time
from datetime import datetime

from app.services.google_sheets_service import read_dm_giaovien

_TEACHER_SERVICE_TRACE_FALLBACK: list[dict] = []


def reset_teacher_service_trace() -> None:
    """Clear teacher-service measurement trace for the current Streamlit session."""
    _get_teacher_trace_store().clear()


def get_teacher_service_trace() -> list[dict]:
    """Return teacher-service measurement trace for display/debugging."""
    return [dict(item) for item in _get_teacher_trace_store()]


def _get_teacher_trace_store() -> list[dict]:
    try:
        import streamlit as st
        return st.session_state.setdefault("evus_teacher_service_trace", [])
    except Exception:
        return _TEACHER_SERVICE_TRACE_FALLBACK


def _record_teacher_trace(step: str, elapsed: float, count: int | None = None, note: str = "") -> None:
    store = _get_teacher_trace_store()
    store.append({
        "Lan": len(store) + 1,
        "ThoiDiem": datetime.now().strftime("%H:%M:%S"),
        "Buoc": step,
        "ThoiGian": round(float(elapsed or 0), 3),
        "SoDong": "" if count is None else int(count),
        "GhiChu": note,
    })
    if len(store) > 80:
        del store[:-80]


def parse_bool(value: object) -> bool:
    """Convert common Google Sheets boolean-like values to bool."""
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    text = str(value).strip().lower()
    return text in {"true", "1", "yes", "y", "x", "co", "có"}


def normalize_teacher_record(record: dict) -> dict:
    """Normalize one raw DM_GiaoVien record."""
    return {
        "ma_gv": str(record.get("Mã GV", "")).strip(),
        "ho_ten": str(record.get("Họ và tên", "")).strip(),
        "to_chuyen_mon": str(record.get("Tổ chuyên môn", "")).strip(),
        "email": str(record.get("Email", "")).strip(),
        "sdt": str(record.get("SĐT", "")).strip(),
        "ten_dang_nhap": str(record.get("Tên đăng nhập", "")).strip(),
        "vai_tro": str(record.get("Vai trò", "")).strip(),
        "dang_hoat_dong": parse_bool(record.get("Đang hoạt động")),
        "mat_khau_hash": str(record.get("MatKhauHash", "")).strip(),
        "lan_dang_nhap_cuoi": str(record.get("LanDangNhapCuoi", "")).strip(),
        "doi_mat_khau_lan_dau": parse_bool(record.get("DoiMatKhauLanDau")),
        "raw": record,
    }


def get_all_teachers() -> list[dict]:
    """Return all active and inactive teachers from DM_GiaoVien."""
    total_start = time.perf_counter()

    step_start = time.perf_counter()
    records = read_dm_giaovien()
    _record_teacher_trace(
        "get_all_teachers - đọc DM_GiaoVien",
        time.perf_counter() - step_start,
        len(records),
    )

    step_start = time.perf_counter()
    teachers = [normalize_teacher_record(record) for record in records]
    _record_teacher_trace(
        "get_all_teachers - chuẩn hóa từng dòng",
        time.perf_counter() - step_start,
        len(teachers),
    )

    _record_teacher_trace(
        "get_all_teachers - tổng thời gian",
        time.perf_counter() - total_start,
        len(teachers),
    )
    return teachers


def get_teacher_by_username(username: str) -> dict | None:
    """Find one teacher by username."""
    total_start = time.perf_counter()
    normalized_username = str(username).strip().lower()

    teachers = get_all_teachers()
    step_start = time.perf_counter()
    for teacher in teachers:
        if teacher["ten_dang_nhap"].lower() == normalized_username:
            _record_teacher_trace(
                "get_teacher_by_username - duyệt tìm tài khoản",
                time.perf_counter() - step_start,
                len(teachers),
                "tìm thấy",
            )
            _record_teacher_trace(
                "get_teacher_by_username - tổng thời gian",
                time.perf_counter() - total_start,
                len(teachers),
            )
            return teacher

    _record_teacher_trace(
        "get_teacher_by_username - duyệt tìm tài khoản",
        time.perf_counter() - step_start,
        len(teachers),
        "không tìm thấy",
    )
    _record_teacher_trace(
        "get_teacher_by_username - tổng thời gian",
        time.perf_counter() - total_start,
        len(teachers),
    )
    return None

def get_teacher_by_magv(ma_gv: str) -> dict | None:
    """Find one teacher by MaGV from DM_GiaoVien."""
    total_start = time.perf_counter()
    normalized_ma_gv = str(ma_gv).strip().lower()
    if not normalized_ma_gv:
        return None

    teachers = get_all_teachers()
    step_start = time.perf_counter()
    for teacher in teachers:
        if str(teacher.get("ma_gv", "")).strip().lower() == normalized_ma_gv:
            _record_teacher_trace(
                "get_teacher_by_magv - duyệt tìm mã GV",
                time.perf_counter() - step_start,
                len(teachers),
                "tìm thấy",
            )
            _record_teacher_trace(
                "get_teacher_by_magv - tổng thời gian",
                time.perf_counter() - total_start,
                len(teachers),
            )
            return teacher

    _record_teacher_trace(
        "get_teacher_by_magv - duyệt tìm mã GV",
        time.perf_counter() - step_start,
        len(teachers),
        "không tìm thấy",
    )
    _record_teacher_trace(
        "get_teacher_by_magv - tổng thời gian",
        time.perf_counter() - total_start,
        len(teachers),
    )
    return None

