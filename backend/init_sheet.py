from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from models import COLUMNS, Paciente
from sheets_client import SheetsClient


SAMPLE_CSV = Path(__file__).parent.parent / "data" / "sample_pacientes.csv"


def init_worksheet(client: SheetsClient, worksheet_name: str = "Pacientes") -> None:
    """Crea la hoja 'Pacientes' con las columnas definidas si no existe."""
    worksheets = client.list_worksheets()
    print(f"  Hojas actuales: {worksheets}")

    if worksheet_name in worksheets:
        print(f"  La hoja '{worksheet_name}' ya existe. No se sobrescribe.")
        return

    spreadsheet = client.spreadsheet
    worksheet = spreadsheet.add_worksheet(
        title=worksheet_name, rows=100, cols=len(COLUMNS)
    )
    worksheet.append_row(COLUMNS, value_input_option="USER_ENTERED")
    print(f"  Hoja '{worksheet_name}' creada con columnas: {COLUMNS}")


def load_sample_data(
    client: SheetsClient,
    csv_path: Path = SAMPLE_CSV,
    worksheet_name: str = "Pacientes",
) -> None:
    """Carga pacientes ficticios desde un CSV al Google Sheet."""
    if not csv_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {csv_path}")

    worksheet = client.get_worksheet(worksheet_name)
    existing = worksheet.get_all_records()
    if existing:
        print(f"  La hoja ya tiene {len(existing)} registros. No se carga el sample.")
        return

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        pacientes = [Paciente.from_dict(row) for row in reader]

    for p in pacientes:
        errors = p.validate()
        if errors:
            print(f"  WARN: Paciente {p.dni} con errores: {errors}")
        client.append_record(p.to_dict(), worksheet_name=worksheet_name)

    print(f"  {len(pacientes)} pacientes ficticios cargados desde {csv_path.name}")


def main() -> None:
    print("Inicializando hoja 'Pacientes'...\n")

    client = SheetsClient()
    print(f"  Spreadsheet: {client.spreadsheet_id}")

    init_worksheet(client)
    load_sample_data(client)

    records = client.get_all_records()
    print(f"\n  Total de registros en 'Pacientes': {len(records)}")
    if records:
        print(f"  Primer registro: {records[0]}")

    print("\n  Inicialización completa.")


if __name__ == "__main__":
    main()
