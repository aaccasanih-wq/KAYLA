from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from models import Paciente, Recordatorio
from reminder_service import (
    filter_and_build,
    format_reminder_message,
    group_reminders_by_medico,
)
from sheets_client import SheetsClient
from telegram_bot import TelegramBot


def load_patients(client: SheetsClient) -> list[Paciente]:
    """Carga todos los pacientes desde Google Sheets."""
    records = client.get_all_records()
    patients = [Paciente.from_dict(row) for row in records]
    print(f"  Pacientes cargados desde Sheets: {len(patients)}")
    return patients


def send_reminders(
    reminders_by_medico: dict[str, list[Recordatorio]],
    bot: TelegramBot,
    dry_run: bool = False,
) -> int:
    """Envía recordatorios agrupados por médico. Retorna el total enviados."""
    total_sent = 0

    for medico, reminders in reminders_by_medico.items():
        if not reminders:
            continue

        lines = [f"*KAYLA - Recordatorios para {medico}*\n"]
        for r in reminders:
            lines.append(format_reminder_message(r))
            lines.append("")  # separador

        message = "\n".join(lines).strip()

        if dry_run:
            print(f"\n  [DRY-RUN] Mensaje para {medico} ({len(reminders)} recordatorio(s)):")
            print("  " + "-" * 60)
            for line in message.split("\n"):
                print(f"  {line}")
            print("  " + "-" * 60)
        else:
            try:
                bot.send_message(text=message, parse_mode="Markdown")
                print(f"  Enviados {len(reminders)} recordatorio(s) a {medico}")
            except Exception as e:
                print(f"  ERROR enviando a {medico}: {e}")
                continue

        total_sent += len(reminders)

    return total_sent


def run(
    days_ahead: int = 2,
    dry_run: bool = False,
    target_date: date | None = None,
) -> None:
    """Punto de entrada principal del scheduler.

    Args:
        days_ahead: Días hacia adelante para filtrar (default 2).
        dry_run: Si True, no envía mensajes, solo los imprime.
        target_date: Fecha de referencia (default: hoy).
    """
    if target_date is None:
        target_date = date.today()

    mode = "DRY-RUN" if dry_run else "PRODUCCION"
    print(f"=== KAYLA Scheduler ({mode}) ===")
    print(f"  Fecha de referencia: {target_date.isoformat()}")
    print(f"  Ventana: +{days_ahead} dias\n")

    print("  [1/4] Conectando con Google Sheets...")
    client = SheetsClient()
    patients = load_patients(client)
    if not patients:
        print("  No hay pacientes en la base. Terminando.")
        return

    print("\n  [2/4] Filtrando pacientes por fecha...")
    reminders = filter_and_build(patients, target_date, days_ahead)
    print(f"  Recordatorios pendientes: {len(reminders)}")
    if not reminders:
        print("  No hay recordatorios para enviar. Terminando.")
        return

    print("\n  [3/4] Agrupando por medico...")
    grouped = group_reminders_by_medico(reminders)
    for medico, rs in grouped.items():
        print(f"    {medico}: {len(rs)} recordatorio(s)")

    print(f"\n  [4/4] Enviando recordatorios ({mode})...")
    if not dry_run:
        bot = TelegramBot()

    total = send_reminders(grouped, bot if not dry_run else None, dry_run=dry_run)
    print(f"\n  Total de recordatorios procesados: {total}")
    print("\n=== Scheduler finalizado ===")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="KAYLA - Scheduler de recordatorios de medicamentos"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=2,
        help="Dias hacia adelante para filtrar (default: 2)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="No envia mensajes, solo los imprime en consola",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Fecha de referencia YYYY-MM-DD (default: hoy)",
    )
    args = parser.parse_args()

    target_date = None
    if args.date:
        target_date = date.fromisoformat(args.date)

    run(days_ahead=args.days, dry_run=args.dry_run, target_date=target_date)


if __name__ == "__main__":
    main()
