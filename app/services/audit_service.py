"""Audit log service for EVUS_ThiDua."""

from __future__ import annotations

from uuid import uuid4

from app.services.google_sheets_service import get_worksheet
from app.utils.date_utils import now_iso

AUDIT_SHEET_NAME = "Audit_Log"

ACTION_SUBMIT_PHIEU = "SUBMIT_PHIEU"
ACTION_BGH_UPDATE_SCORE = "BGH_UPDATE_SCORE"
ACTION_BGH_CREATE_PHIEU_AFTER_DEADLINE = "BGH_CREATE_PHIEU_AFTER_DEADLINE"
ACTION_BGH_UNLOCK_PHIEU = "BGH_UNLOCK_PHIEU"
ACTION_BGH_FINALIZE_PHIEU = "BGH_FINALIZE_PHIEU"
ACTION_BGH_SUMMARIZE_MONTH = "BGH_SUMMARIZE_MONTH"


def write_audit_log(action: str, target_id: str, actor: str, note: str = "") -> dict:
    """Append one important action to Audit_Log.

    Expected worksheet columns:
    ID, ThoiGian, HanhDong, DoiTuong, NguoiThucHien, GhiChu
    """
    row = {
        "ID": str(uuid4()),
        "ThoiGian": now_iso(),
        "HanhDong": str(action).strip(),
        "DoiTuong": str(target_id).strip(),
        "NguoiThucHien": str(actor).strip(),
        "GhiChu": str(note).strip(),
    }

    worksheet = get_worksheet(AUDIT_SHEET_NAME)
    worksheet.append_row([row[key] for key in row.keys()], value_input_option="USER_ENTERED")
    return row
