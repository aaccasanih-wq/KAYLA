from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from models import Paciente, Recordatorio
from reminder_service import (
    filter_and_build,
    filter_patients_by_date,
    format_reminder_message,
    group_reminders_by_medico,
)


def make_patient(
    dni: str = "12345678",
    names: str = "Juan",
    surnames: str = "Perez",
    recojo: str = "",
    control: str = "",
    medico: str = "Dr. Luis",
    estado: str = "activo",
) -> Paciente:
    return Paciente(
        dni=dni,
        nombres=names,
        apellidos=surnames,
        celular="987654321",
        diagnostico="HTA",
        fecha_recojo_medicamento=recojo,
        fecha_proximo_control=control,
        posta="Posta Test",
        medico_a_cargo=medico,
        correo_medico="medico@posta.gob.pe",
        estado=estado,
    )


def test_filter_recojo_within_window() -> None:
    today = date(2026, 6, 22)
    p = make_patient(recojo=(today + timedelta(days=1)).isoformat())
    matches = filter_patients_by_date([p], today, days_ahead=2)
    assert len(matches) == 1
    assert matches[0][1] == "recojo"
    print("  [OK] filter_recojo_within_window")


def test_filter_control_within_window() -> None:
    today = date(2026, 6, 22)
    p = make_patient(control=(today + timedelta(days=2)).isoformat())
    matches = filter_patients_by_date([p], today, days_ahead=2)
    assert len(matches) == 1
    assert matches[0][1] == "control"
    print("  [OK] filter_control_within_window")


def test_filter_both_events() -> None:
    today = date(2026, 6, 22)
    p = make_patient(
        recojo=(today + timedelta(days=1)).isoformat(),
        control=(today + timedelta(days=2)).isoformat(),
    )
    matches = filter_patients_by_date([p], today, days_ahead=2)
    assert len(matches) == 2
    print("  [OK] filter_both_events")


def test_filter_outside_window() -> None:
    today = date(2026, 6, 22)
    p = make_patient(recojo=(today + timedelta(days=5)).isoformat())
    matches = filter_patients_by_date([p], today, days_ahead=2)
    assert len(matches) == 0
    print("  [OK] filter_outside_window")


def test_filter_inactive_patient() -> None:
    today = date(2026, 6, 22)
    p = make_patient(
        recojo=(today + timedelta(days=1)).isoformat(),
        estado="inactivo",
    )
    matches = filter_patients_by_date([p], today, days_ahead=2)
    assert len(matches) == 0
    print("  [OK] filter_inactive_patient")


def test_filter_past_date_ignored() -> None:
    today = date(2026, 6, 22)
    p = make_patient(recojo=(today - timedelta(days=1)).isoformat())
    matches = filter_patients_by_date([p], today, days_ahead=2)
    assert len(matches) == 0
    print("  [OK] filter_past_date_ignored")


def test_filter_empty_dates_ignored() -> None:
    today = date(2026, 6, 22)
    p = make_patient()
    matches = filter_patients_by_date([p], today, days_ahead=2)
    assert len(matches) == 0
    print("  [OK] filter_empty_dates_ignored")


def test_filter_dd_mm_yyyy_format() -> None:
    today = date(2026, 6, 22)
    p = make_patient(recojo="24/06/2026")
    matches = filter_patients_by_date([p], today, days_ahead=2)
    assert len(matches) == 1
    print("  [OK] filter_dd_mm_yyyy_format")


def test_format_reminder_recojo() -> None:
    p = make_patient(recojo="2026-06-23")
    r = Recordatorio(paciente=p, tipo="recojo", fecha="2026-06-23")
    msg = format_reminder_message(r)
    assert "recojo de medicamento" in msg
    assert "Juan Perez" in msg
    assert "DNI: 12345678" in msg
    print("  [OK] format_reminder_recojo")


def test_format_reminder_control() -> None:
    p = make_patient(control="2026-06-24")
    r = Recordatorio(paciente=p, tipo="control", fecha="2026-06-24")
    msg = format_reminder_message(r)
    assert "control medico" in msg
    print("  [OK] format_reminder_control")


def test_group_by_medico() -> None:
    p1 = make_patient(dni="11111111", medico="Dr. A", recojo="2026-06-23")
    p2 = make_patient(dni="22222222", medico="Dr. B", recojo="2026-06-23")
    p3 = make_patient(dni="33333333", medico="Dr. A", recojo="2026-06-23")
    today = date(2026, 6, 22)
    reminders = filter_and_build([p1, p2, p3], today, days_ahead=2)
    grouped = group_reminders_by_medico(reminders)
    assert len(grouped["Dr. A"]) == 2
    assert len(grouped["Dr. B"]) == 1
    print("  [OK] group_by_medico")


def main() -> None:
    print("Ejecutando tests de reminder_service...\n")
    test_filter_recojo_within_window()
    test_filter_control_within_window()
    test_filter_both_events()
    test_filter_outside_window()
    test_filter_inactive_patient()
    test_filter_past_date_ignored()
    test_filter_empty_dates_ignored()
    test_filter_dd_mm_yyyy_format()
    test_format_reminder_recojo()
    test_format_reminder_control()
    test_group_by_medico()
    print("\n  Todos los tests pasaron.")


if __name__ == "__main__":
    main()
