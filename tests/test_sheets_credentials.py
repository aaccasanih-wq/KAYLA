"""Pruebas de resolucion de credenciales de SheetsClient.

Verifica que SheetsClient acepta credenciales desde:
  - GOOGLE_SHEETS_CREDENTIALS_JSON (JSON crudo)
  - GOOGLE_SHEETS_CREDENTIALS_B64 (base64)
  - archivo en disco (fallback para dev local / GitHub Actions)

No toca la red: solo ejercita la resolucion en __init__ y
load_credentials_info().
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import pytest  # noqa: E402

from sheets_client import SheetsClient, load_credentials_info  # noqa: E402

FAKE_SA: dict = {
    "type": "service_account",
    "project_id": "kayla-test",
    "private_key_id": "abc123",
    "private_key": "-----BEGIN PRIVATE KEY-----\nfake\n-----END PRIVATE KEY-----\n",
    "client_email": "kayla-sa@kayla-test.iam.gserviceaccount.com",
    "client_id": "1234567890",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/kayla",
}


@pytest.fixture
def clean_env(monkeypatch):
    """Limpia las variables de credenciales entre tests."""
    for k in (
        "GOOGLE_SHEETS_CREDENTIALS_JSON",
        "GOOGLE_SHEETS_CREDENTIALS_B64",
        "GOOGLE_SHEETS_CREDENTIALS_PATH",
        "GOOGLE_SHEETS_SPREADSHEET_ID",
    ):
        monkeypatch.delenv(k, raising=False)
    yield monkeypatch


def test_load_credentials_info_from_json(clean_env) -> None:
    clean_env.setenv("GOOGLE_SHEETS_CREDENTIALS_JSON", json.dumps(FAKE_SA))
    info = load_credentials_info()
    assert info is not None
    assert info["project_id"] == "kayla-test"
    print("  [OK] load_credentials_info_from_json")


def test_load_credentials_info_from_b64(clean_env) -> None:
    b64 = base64.b64encode(json.dumps(FAKE_SA).encode("utf-8")).decode("utf-8")
    clean_env.setenv("GOOGLE_SHEETS_CREDENTIALS_B64", b64)
    info = load_credentials_info()
    assert info is not None
    assert info["client_email"] == FAKE_SA["client_email"]
    print("  [OK] load_credentials_info_from_b64")


def test_load_credentials_info_none(clean_env) -> None:
    info = load_credentials_info()
    assert info is None
    print("  [OK] load_credentials_info_none")


def test_load_credentials_info_json_takes_precedence_over_b64(clean_env) -> None:
    clean_env.setenv("GOOGLE_SHEETS_CREDENTIALS_JSON", json.dumps(FAKE_SA))
    clean_env.setenv(
        "GOOGLE_SHEETS_CREDENTIALS_B64",
        base64.b64encode(json.dumps({"project_id": "wrong"}).encode()).decode(),
    )
    info = load_credentials_info()
    assert info["project_id"] == "kayla-test"
    print("  [OK] json_takes_precedence_over_b64")


def test_sheetsclient_init_from_json_env(clean_env) -> None:
    clean_env.setenv("GOOGLE_SHEETS_CREDENTIALS_JSON", json.dumps(FAKE_SA))
    clean_env.setenv("GOOGLE_SHEETS_SPREADSHEET_ID", "fake_sheet_id")
    client = SheetsClient()
    assert client._credentials_info is not None
    assert client._credentials_info["project_id"] == "kayla-test"
    print("  [OK] sheetsclient_init_from_json_env")


def test_sheetsclient_init_from_b64_env(clean_env) -> None:
    b64 = base64.b64encode(json.dumps(FAKE_SA).encode("utf-8")).decode("utf-8")
    clean_env.setenv("GOOGLE_SHEETS_CREDENTIALS_B64", b64)
    clean_env.setenv("GOOGLE_SHEETS_SPREADSHEET_ID", "fake_sheet_id")
    client = SheetsClient()
    assert client._credentials_info is not None
    print("  [OK] sheetsclient_init_from_b64_env")


def test_sheetsclient_init_from_file(clean_env, tmp_path) -> None:
    creds_file = tmp_path / "creds.json"
    creds_file.write_text(json.dumps(FAKE_SA))
    clean_env.setenv("GOOGLE_SHEETS_CREDENTIALS_PATH", str(creds_file))
    clean_env.setenv("GOOGLE_SHEETS_SPREADSHEET_ID", "fake_sheet_id")
    client = SheetsClient()
    assert client._credentials_info is None
    assert client.credentials_path == str(creds_file)
    print("  [OK] sheetsclient_init_from_file")


def test_sheetsclient_missing_spreadsheet_id_raises(clean_env) -> None:
    clean_env.setenv("GOOGLE_SHEETS_CREDENTIALS_JSON", json.dumps(FAKE_SA))
    with pytest.raises(ValueError, match="SPREADSHEET_ID"):
        SheetsClient()
    print("  [OK] missing_spreadsheet_id_raises")


def test_sheetsclient_no_credentials_raises(clean_env) -> None:
    clean_env.setenv("GOOGLE_SHEETS_SPREADSHEET_ID", "fake_sheet_id")
    clean_env.setenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "/no/existe/creds.json")
    with pytest.raises(FileNotFoundError):
        SheetsClient()
    print("  [OK] no_credentials_raises")


def main() -> None:
    print("Este archivo se ejecuta con pytest: pytest tests/test_sheets_credentials.py -v")


if __name__ == "__main__":
    main()
