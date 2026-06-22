from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class SheetsClient:
    """Cliente para interactuar con Google Sheets mediante una Service Account."""

    def __init__(
        self,
        credentials_path: str | None = None,
        spreadsheet_id: str | None = None,
    ) -> None:
        self.credentials_path = credentials_path or os.getenv(
            "GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json"
        )
        self.spreadsheet_id = spreadsheet_id or os.getenv(
            "GOOGLE_SHEETS_SPREADSHEET_ID"
        )

        if not self.spreadsheet_id:
            raise ValueError(
                "GOOGLE_SHEETS_SPREADSHEET_ID no está configurado. "
                "Agrega el ID del Google Sheet en .env"
            )

        if not Path(self.credentials_path).exists():
            raise FileNotFoundError(
                f"No se encontró el archivo de credenciales en '{self.credentials_path}'. "
                "Descarga el JSON desde Google Cloud Console y colócalo en la raíz del proyecto."
            )

        self._client: gspread.client.Client | None = None
        self._spreadsheet: gspread.spreadsheet.Spreadsheet | None = None

    @property
    def client(self) -> gspread.client.Client:
        if self._client is None:
            creds = Credentials.from_service_account_file(
                self.credentials_path, scopes=SCOPES
            )
            self._client = gspread.authorize(creds)
        return self._client

    @property
    def spreadsheet(self) -> gspread.spreadsheet.Spreadsheet:
        if self._spreadsheet is None:
            self._spreadsheet = self.client.open_by_key(self.spreadsheet_id)
        return self._spreadsheet

    def get_worksheet(
        self, worksheet_name: str = "Pacientes"
    ) -> gspread.worksheet.Worksheet:
        return self.spreadsheet.worksheet(worksheet_name)

    def get_all_records(
        self, worksheet_name: str = "Pacientes"
    ) -> list[dict[str, Any]]:
        worksheet = self.get_worksheet(worksheet_name)
        return worksheet.get_all_records()

    def append_record(
        self, record: dict[str, Any], worksheet_name: str = "Pacientes"
    ) -> None:
        worksheet = self.get_worksheet(worksheet_name)
        worksheet.append_row(
            [str(record.get(k, "")) for k in record.keys()],
            value_input_option="USER_ENTERED",
        )

    def find_row_by_dni(
        self, dni: str, worksheet_name: str = "Pacientes"
    ) -> dict[str, Any] | None:
        worksheet = self.get_worksheet(worksheet_name)
        cell = worksheet.find(dni, in_column=1)
        if cell is None:
            return None
        headers = worksheet.row_values(1)
        row_values = worksheet.row_values(cell.row)
        return dict(zip(headers, row_values))

    def update_cell(
        self,
        row: int,
        col: int,
        value: str,
        worksheet_name: str = "Pacientes",
    ) -> None:
        worksheet = self.get_worksheet(worksheet_name)
        worksheet.update_cell(row, col, value)

    def list_worksheets(self) -> list[str]:
        return [ws.title for ws in self.spreadsheet.worksheets()]
