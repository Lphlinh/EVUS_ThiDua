"""Google Sheets connection service for EVUS_ThiDua.

This module only handles authentication and low-level worksheet access.
It does not contain business logic.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import gspread
from google.oauth2.service_account import Credentials


SPREADSHEET_ID = "14QZmgiaZZnhhd_j0v-imBQu258FXm3MB4acjv1razd0"
SERVICE_ACCOUNT_FILE = Path("config/service_account.json")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


_CLIENT_CACHE: gspread.Client | None = None
_SPREADSHEET_CACHE: gspread.Spreadsheet | None = None
_WORKSHEET_CACHE: dict[str, "CachedWorksheet"] = {}
_WORKSHEET_CATALOG_LOADED = False
_READ_RECORDS_CACHE: dict[str, list[dict[str, Any]]] = {}

# Gioi han vung doc cho sheet danh muc nho de tranh Google Sheets tra ve qua nhieu cot trong/dinh dang.
# DM_GiaoVien hien dung 11 cot A:K theo cau truc du an.
_SHEET_READ_RANGES: dict[str, str] = {
    "DM_GiaoVien": "A:K",
}


def clear_google_sheets_connection_cache() -> None:
    """Clear cached Google Sheets client, spreadsheet, worksheets and row reads."""
    global _CLIENT_CACHE, _SPREADSHEET_CACHE, _WORKSHEET_CATALOG_LOADED
    _CLIENT_CACHE = None
    _SPREADSHEET_CACHE = None
    _WORKSHEET_CATALOG_LOADED = False
    _WORKSHEET_CACHE.clear()
    clear_sheet_records_cache()


def clear_sheet_records_cache(sheet_name: str | None = None) -> None:
    """Clear cached read_sheet_records data.

    Passing a sheet name clears only that worksheet; omitting it clears all
    cached row data. Write operations through CachedWorksheet call this
    automatically for the affected worksheet.
    """
    if sheet_name is None:
        _READ_RECORDS_CACHE.clear()
        return
    _READ_RECORDS_CACHE.pop(str(sheet_name).strip(), None)


class CachedWorksheet:
    """Small proxy around gspread.Worksheet that invalidates row-read cache on writes."""

    def __init__(self, worksheet: gspread.Worksheet, sheet_name: str) -> None:
        self._worksheet = worksheet
        self._sheet_name = str(sheet_name).strip()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._worksheet, name)

    @property
    def title(self) -> str:
        return self._worksheet.title

    def _clear_cache(self) -> None:
        clear_sheet_records_cache(self._sheet_name)

    def append_row(self, *args: Any, **kwargs: Any) -> Any:
        self._clear_cache()
        result = self._worksheet.append_row(*args, **kwargs)
        self._clear_cache()
        return result

    def append_rows(self, *args: Any, **kwargs: Any) -> Any:
        self._clear_cache()
        result = self._worksheet.append_rows(*args, **kwargs)
        self._clear_cache()
        return result

    def batch_update(self, *args: Any, **kwargs: Any) -> Any:
        self._clear_cache()
        result = self._worksheet.batch_update(*args, **kwargs)
        self._clear_cache()
        return result

    def update_cell(self, *args: Any, **kwargs: Any) -> Any:
        self._clear_cache()
        result = self._worksheet.update_cell(*args, **kwargs)
        self._clear_cache()
        return result

    def update(self, *args: Any, **kwargs: Any) -> Any:
        self._clear_cache()
        result = self._worksheet.update(*args, **kwargs)
        self._clear_cache()
        return result


def get_gspread_client() -> gspread.Client:
    """Return an authorized gspread client, cached for the Streamlit process.

    Local development uses ``config/service_account.json``.
    Streamlit Community Cloud uses ``st.secrets["gcp_service_account"]``.
    """
    global _CLIENT_CACHE
    if _CLIENT_CACHE is not None:
        return _CLIENT_CACHE

    credentials = _build_google_credentials()
    _CLIENT_CACHE = gspread.authorize(credentials)
    return _CLIENT_CACHE


def _build_google_credentials() -> Credentials:
    """Build Google credentials from Streamlit secrets or the local JSON file."""
    service_account_info = _get_streamlit_service_account_info()
    if service_account_info:
        return Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES,
        )

    if SERVICE_ACCOUNT_FILE.exists():
        return Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES,
        )

    raise FileNotFoundError(
        "Không tìm thấy cấu hình Google Service Account. "
        f"Local cần file {SERVICE_ACCOUNT_FILE}; Streamlit Cloud cần cấu hình "
        "Secrets với khóa [gcp_service_account]."
    )


def _get_streamlit_service_account_info() -> dict[str, Any] | None:
    """Return service account info from Streamlit secrets when available."""
    try:
        import streamlit as st
    except Exception:
        return None

    try:
        raw_info = st.secrets.get("gcp_service_account")
    except Exception:
        return None

    if not raw_info:
        return None

    info = dict(raw_info)
    private_key = info.get("private_key")
    if isinstance(private_key, str):
        info["private_key"] = private_key.replace("\\n", "\n")
    return info


def open_spreadsheet() -> gspread.Spreadsheet:
    """Open the main EVUS_ThiDua Google Spreadsheet, cached for the process."""
    global _SPREADSHEET_CACHE
    if _SPREADSHEET_CACHE is not None:
        return _SPREADSHEET_CACHE

    client = get_gspread_client()
    _SPREADSHEET_CACHE = client.open_by_key(SPREADSHEET_ID)
    return _SPREADSHEET_CACHE


def get_worksheet(sheet_name: str) -> CachedWorksheet:
    """Return a worksheet by name, cached for the process.

    Loads the worksheet catalog once and caches worksheet handles by title.
    This avoids repeated ``spreadsheet.worksheet(name)`` calls for each sheet
    while keeping row-data cache invalidation unchanged.
    """
    normalized_sheet_name = str(sheet_name).strip()
    cached = _WORKSHEET_CACHE.get(normalized_sheet_name)
    if cached is not None:
        return cached

    spreadsheet = open_spreadsheet()
    _populate_worksheet_cache(spreadsheet)
    cached = _WORKSHEET_CACHE.get(normalized_sheet_name)
    if cached is not None:
        return cached

    # Fallback for a worksheet created after the catalog was loaded.
    worksheet = CachedWorksheet(spreadsheet.worksheet(normalized_sheet_name), normalized_sheet_name)
    _WORKSHEET_CACHE[normalized_sheet_name] = worksheet
    return worksheet


def _populate_worksheet_cache(spreadsheet: gspread.Spreadsheet) -> None:
    """Load worksheet handles once and cache them by title."""
    global _WORKSHEET_CATALOG_LOADED
    if _WORKSHEET_CATALOG_LOADED:
        return

    for worksheet in spreadsheet.worksheets():
        title = str(worksheet.title).strip()
        if not title:
            continue
        _WORKSHEET_CACHE.setdefault(title, CachedWorksheet(worksheet, title))
    _WORKSHEET_CATALOG_LOADED = True


def warm_up_google_sheets() -> None:
    """Warm up Google Sheets client, spreadsheet object and worksheet catalog after login.

    This function intentionally does not read worksheet row data.
    """
    spreadsheet = open_spreadsheet()
    _populate_worksheet_cache(spreadsheet)


def read_sheet_records(sheet_name: str) -> list[dict[str, Any]]:
    """Read all rows from a worksheet as dictionaries, cached per process until writes.

    gspread.get_all_records() fails when a worksheet has duplicated blank
    headers. Some EVUS sheets contain extra empty columns, so this function
    reads raw values and ignores blank header columns instead.
    """
    normalized_sheet_name = str(sheet_name).strip()

    cached_records = _READ_RECORDS_CACHE.get(normalized_sheet_name)
    if cached_records is not None:
        return [dict(record) for record in cached_records]

    worksheet = get_worksheet(normalized_sheet_name)
    range_name = _SHEET_READ_RANGES.get(normalized_sheet_name)
    if range_name:
        values = worksheet.get(range_name)
    else:
        values = worksheet.get_all_values()

    if not values:
        _READ_RECORDS_CACHE[normalized_sheet_name] = []
        return []

    headers = [str(header).strip() for header in values[0]]
    valid_columns: list[tuple[int, str]] = []
    seen_headers: set[str] = set()

    for index, header in enumerate(headers):
        if not header:
            continue
        if header in seen_headers:
            continue
        seen_headers.add(header)
        valid_columns.append((index, header))

    records: list[dict[str, Any]] = []
    for row in values[1:]:
        if not any(str(cell).strip() for cell in row):
            continue

        record: dict[str, Any] = {}
        for index, header in valid_columns:
            value = row[index] if index < len(row) else ""
            record[header] = value
            normalized_header = _normalize_header_key(header)
            if normalized_header and normalized_header not in record:
                record[normalized_header] = value
        records.append(record)

    _READ_RECORDS_CACHE[normalized_sheet_name] = [dict(record) for record in records]
    return [dict(record) for record in records]


def read_dm_giaovien() -> list[dict[str, Any]]:
    """Read teacher master data."""
    return read_sheet_records("DM_GiaoVien")


def _normalize_header_key(value: str) -> str:
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
