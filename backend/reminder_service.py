from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Iterable

from models import Paciente, Recordatorio


def parse_date(value: str) -> date | None:
    """Parsea una fecha en varios formatos a date."""
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(str(value), fmt).date()
        except ValueError:
            continue
    return None


def filter_patients_by_date(
    patients: Iterable[Paciente],
    target_date: date,
    days_ahead: int = 2,
) -> list[tuple[Paciente, str, date]]:
    """Filtra pacientes que tienen un evento (recojo o control) en los próximos días.

    Args:
        patients: Lista de pacientes.
        target_date: Fecha de referencia (ej. hoy).
        days_ahead: Ventana de días hacia adelante (inclusive).

    Returns:
        Lista de tuplas (paciente, tipo_evento, fecha_evento).
        tipo_evento es "recojo" o "control".
    """
    start = target_date
    end = target_date + timedelta(days=days_ahead)
    result: list[tuple[Paciente, str, date]] = []

    for p in patients:
        if p.estado.lower() != "activo":
            continue

        recojo = parse_date(p.fecha_recojo_medicamento)
        control = parse_date(p.fecha_proximo_control)

        if recojo and start <= recojo <= end:
            result.append((p, "recojo", recojo))

        if control and start <= control <= end:
            result.append((p, "control", control))

    return result


def build_reminders(
    matches: list[tuple[Paciente, str, date]],
) -> list[Recordatorio]:
    """Construye objetos Recordatorio a partir de las coincidencias."""
    reminders: list[Recordatorio] = []
    for paciente, tipo, fecha in matches:
        reminder = Recordatorio(
            paciente=paciente,
            tipo=tipo,
            fecha=fecha.isoformat(),
        )
        reminders.append(reminder)
    return reminders


def filter_and_build(
    patients: Iterable[Paciente],
    target_date: date | None = None,
    days_ahead: int = 2,
) -> list[Recordatorio]:
    """Combina filter_patients_by_date y build_reminders en un solo paso."""
    if target_date is None:
        target_date = date.today()
    matches = filter_patients_by_date(patients, target_date, days_ahead)
    return build_reminders(matches)


def format_reminder_message(reminder: Recordatorio) -> str:
    """Genera el mensaje de texto formateado para Telegram (Markdown)."""
    p = reminder.paciente
    if reminder.tipo == "recojo":
        header = "*Recordatorio de recojo de medicamento*"
        label = "Fecha de recojo"
    else:
        header = "*Recordatorio de control medico*"
        label = "Fecha de control"

    return (
        f"{header}\n"
        f"  Paciente: {p.nombres} {p.apellidos} (DNI: {p.dni})\n"
        f"  Diagnostico: {p.diagnostico}\n"
        f"  {label}: {reminder.fecha}\n"
        f"  Celular: {p.celular}\n"
        f"  Posta: {p.posta}\n"
        f"  Medico a cargo: {p.medico_a_cargo}"
    )


def group_reminders_by_medico(
    reminders: list[Recordatorio],
) -> dict[str, list[Recordatorio]]:
    """Agrupa recordatorios por médico a cargo.

    Returns:
        Dict donde la clave es el nombre del médico y el valor
        es la lista de recordatorios para ese médico.
    """
    groups: dict[str, list[Recordatorio]] = {}
    for r in reminders:
        key = r.paciente.medico_a_cargo or "Sin asignar"
        groups.setdefault(key, []).append(r)
    return groups
