"""Teacher service for EVUS_ThiDua.

This module handles teacher-related business logic based on DM_GiaoVien.
"""

from __future__ import annotations

from app.services.google_sheets_service import read_dm_giaovien


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
    records = read_dm_giaovien()
    return [normalize_teacher_record(record) for record in records]


def get_teacher_by_username(username: str) -> dict | None:
    """Find one teacher by username."""
    normalized_username = str(username).strip().lower()

    for teacher in get_all_teachers():
        if teacher["ten_dang_nhap"].lower() == normalized_username:
            return teacher

    return None

def get_teacher_by_magv(ma_gv: str) -> dict | None:
    """Find one teacher by MaGV from DM_GiaoVien."""
    normalized_ma_gv = str(ma_gv).strip().lower()
    if not normalized_ma_gv:
        return None

    for teacher in get_all_teachers():
        if str(teacher.get("ma_gv", "")).strip().lower() == normalized_ma_gv:
            return teacher

    return None

