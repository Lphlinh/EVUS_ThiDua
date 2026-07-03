"""Google Sheets connection service for EVUS_ThiDua.

This module only handles authentication and opening the configured spreadsheet.
It does not contain business logic.
"""

from __future__ import annotations

from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials


SPREADSHEET_ID = "14QZmgiaZZnhhd_j0v-imBQu258FXm3MB4acjv1razd0"
SERVICE_ACCOUNT_FILE = Path("config/service_account.json")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_gspread_client() -> gspread.Client:
    """Return an authorized gspread client."""
    if not SERVICE_ACCOUNT_FILE.exists():
        raise FileNotFoundError(
            f"Service account file not found: {SERVICE_ACCOUNT_FILE}"
        )

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )
    return gspread.authorize(credentials)


def open_spreadsheet() -> gspread.Spreadsheet:
    """Open the main EVUS_ThiDua Google Spreadsheet."""
    client = get_gspread_client()
    return client.open_by_key(SPREADSHEET_ID)
