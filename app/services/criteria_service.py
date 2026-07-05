"""Criteria service for DM_TieuChi.

This module is the single normalization layer for the criterion master sheet.
Google Sheets keeps the official EVUS column names, while the rest of the
application consumes stable snake_case keys.
"""

from __future__ import annotations

from typing import Any

from app.services.google_sheets_service import read_sheet_records


SHEET_NAME = "DM_TieuChi"


def parse_bool(value: object) -> bool:
    """Convert Google Sheets boolean-like values to bool."""
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    return text in {"true", "1", "yes", "y", "x", "co", "có"}


def parse_float(value: object, default: float = 0.0) -> float:
    """Convert a sheet value to float with a safe default."""
    if value is None:
        return default
    text = str(value).strip()
    if text == "":
        return default
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return default


def parse_int(value: object, default: int = 0) -> int:
    """Convert a sheet value to int with a safe default."""
    try:
        text = str(value).strip()
        if not text:
            return default
        return int(float(text.replace(",", ".")))
    except Exception:
        return default


def normalize_criteria_record(record: dict[str, Any]) -> dict[str, Any]:
    """Normalize one DM_TieuChi row from the official sheet columns."""
    ma_tc = str(record.get("MaTC", "")).strip()
    loai = str(record.get("Loai", "")).strip().upper()
    gia_tri_lon_nhat = parse_float(record.get("GiaTriLonNhat"), 0.0)

    return {
        "ma_tc": ma_tc,
        "ma_cha": str(record.get("MaCha", "")).strip(),
        "thu_tu": parse_int(record.get("ThuTu")),
        "cap": parse_int(record.get("Cap")),
        "ma_hien_thi": str(record.get("MaHienThi", "")).strip(),
        "ten_tieu_chi": str(record.get("TenTieuChi", "")).strip(),
        "nhom": str(record.get("Nhom", "")).strip(),
        "loai": loai,
        "bat_buoc": parse_bool(record.get("BatBuoc")),
        "co_minh_chung": parse_bool(record.get("CoMinhChung")),
        "cho_phep_bgh_sua": parse_bool(record.get("ChoPhepBGHSua")),
        "cong_thuc": str(record.get("CongThuc", "")).strip(),
        "gia_tri_nho_nhat": parse_float(record.get("GiaTriNhoNhat"), 0.0),
        "gia_tri_lon_nhat": gia_tri_lon_nhat,
        "tinh_vao_tong": parse_bool(record.get("TinhVaoTong")),
        "trong_so": parse_float(record.get("TrongSo"), 1.0),
        "ghi_chu": str(record.get("GhiChu", "")).strip(),
        "diem_mac_dinh": gia_tri_lon_nhat,
        "raw": record,
    }


def get_all_criteria() -> list[dict[str, Any]]:
    """Return all criteria sorted by ThuTu."""
    records = read_sheet_records(SHEET_NAME)
    criteria = [normalize_criteria_record(record) for record in records]
    return sorted(criteria, key=lambda item: (item["thu_tu"], item["ma_tc"]))


def get_item_criteria() -> list[dict[str, Any]]:
    """Return only ITEM criteria that generate CT_ThiDua rows."""
    return [item for item in get_all_criteria() if item["loai"] == "ITEM"]


def get_criteria_by_code() -> dict[str, dict[str, Any]]:
    """Return criteria indexed by MaTC."""
    return {item["ma_tc"]: item for item in get_all_criteria() if item["ma_tc"]}
