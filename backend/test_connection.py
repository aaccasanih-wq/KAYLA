import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sheets_client import SheetsClient


def main() -> None:
    print("Probando conexión con Google Sheets...\n")

    try:
        client = SheetsClient()
        print(f"  Credenciales cargadas desde: {client.credentials_path}")
        print(f"  Spreadsheet ID: {client.spreadsheet_id}")

        spreadsheet = client.spreadsheet
        print(f"  Spreadsheet abierto: {spreadsheet.title}")

        worksheets = client.list_worksheets()
        print(f"  Hojas disponibles: {worksheets}")

        if "Pacientes" in worksheets:
            records = client.get_all_records()
            print(f"  Registros en 'Pacientes': {len(records)}")
            if records:
                print(f"  Primer registro: {records[0]}")
        else:
            print("  (La hoja 'Pacientes' aún no existe. Se creará en la Etapa 3.)")

        print("\n  Conexión exitosa con Google Sheets.")

    except Exception as e:
        print(f"\n  Error: {e}")
        print("\n  Revisa docs/google_sheets_setup.md para la configuración.")
        raise


if __name__ == "__main__":
    main()
