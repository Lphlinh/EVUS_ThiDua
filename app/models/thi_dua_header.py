"""Data model for worksheet TH_ThiDua."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class ThiDuaHeader:
    ID: str
    NamHoc: str
    Thang: str
    MaGV: str
    TrangThai: int
    TongDiem: float
    KhoaGV: bool
    KhoaBGH: bool
    NgayTao: str
    NgayCapNhat: str
    NgayNop: str
    NguoiCapNhatCuoi: str
    NguoiNop: str
    GhiChuBGH: str
    LanNop: int
    LanMoKhoa: int

    def to_row(self) -> dict[str, Any]:
        """Return a Google Sheets-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "ThiDuaHeader":
        """Create model from a Google Sheets record."""
        return cls(
            ID=str(record.get("ID", "")).strip(),
            NamHoc=str(record.get("NamHoc", "")).strip(),
            Thang=str(record.get("Thang", "")).strip(),
            MaGV=str(record.get("MaGV", "")).strip(),
            TrangThai=int(record.get("TrangThai") or 0),
            TongDiem=float(record.get("TongDiem") or 0),
            KhoaGV=_parse_bool(record.get("KhoaGV")),
            KhoaBGH=_parse_bool(record.get("KhoaBGH")),
            NgayTao=str(record.get("NgayTao", "")).strip(),
            NgayCapNhat=str(record.get("NgayCapNhat", "")).strip(),
            NgayNop=str(record.get("NgayNop", "")).strip(),
            NguoiCapNhatCuoi=str(record.get("NguoiCapNhatCuoi", "")).strip(),
            NguoiNop=str(record.get("NguoiNop", "")).strip(),
            GhiChuBGH=str(record.get("GhiChuBGH", "")).strip(),
            LanNop=int(record.get("LanNop") or 0),
            LanMoKhoa=int(record.get("LanMoKhoa") or 0),
        )


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y", "x", "co", "có"}
