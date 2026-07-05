"""Date utilities for EVUS_ThiDua M02."""

from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

DEFAULT_TIMEZONE = "Asia/Ho_Chi_Minh"
SCORING_START_DAY = 1
SCORING_END_DAY = 5


def now_vn() -> datetime:
    """Return current datetime in Vietnam timezone."""
    return datetime.now(ZoneInfo(DEFAULT_TIMEZONE))


def now_iso() -> str:
    """Return current datetime as ISO string without microseconds."""
    return now_vn().replace(microsecond=0).isoformat()


def get_previous_month(reference_date: date | None = None) -> str:
    """Return previous month in MM/YYYY format."""
    current = reference_date or now_vn().date()
    year = current.year
    month = current.month - 1

    if month == 0:
        month = 12
        year -= 1

    return f"{month:02d}/{year}"


def get_school_year_from_month(thang: str) -> str:
    """Return school year from a MM/YYYY string.

    School year starts in August. Example: 09/2025 -> 2025-2026,
    05/2026 -> 2025-2026.
    """
    month_text, year_text = str(thang).strip().split("/")
    month = int(month_text)
    year = int(year_text)

    if month >= 8:
        return f"{year}-{year + 1}"
    return f"{year - 1}-{year}"


def is_scoring_window_open(reference_date: date | None = None) -> bool:
    """Return True when teachers may self-create and score a monthly form."""
    current = reference_date or now_vn().date()
    return SCORING_START_DAY <= current.day <= SCORING_END_DAY
