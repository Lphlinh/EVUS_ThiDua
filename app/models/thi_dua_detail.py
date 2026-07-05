"""Data model for worksheet CT_ThiDua."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class ThiDuaDetail:
    ID: str
    IDPhieu: str
    MaTC: str
    DiemMacDinh: float
    DiemGV: float
    DiemBGH: str
    GhiChuGV: str
    GhiChuBGH: str
    NgayCapNhat: str
    NguoiCapNhat: str

    def to_row(self) -> dict[str, Any]:
        """Return a Google Sheets-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "ThiDuaDetail":
        """Create model from a Google Sheets record."""
        return cls(
            ID=str(record.get("ID", "")).strip(),
            IDPhieu=str(record.get("IDPhieu", "")).strip(),
            MaTC=str(record.get("MaTC", "")).strip(),
            DiemMacDinh=float(record.get("DiemMacDinh") or 0),
            DiemGV=float(record.get("DiemGV") or 0),
            DiemBGH=str(record.get("DiemBGH", "")).strip(),
            GhiChuGV=str(record.get("GhiChuGV", "")).strip(),
            GhiChuBGH=str(record.get("GhiChuBGH", "")).strip(),
            NgayCapNhat=str(record.get("NgayCapNhat", "")).strip(),
            NguoiCapNhat=str(record.get("NguoiCapNhat", "")).strip(),
        )
