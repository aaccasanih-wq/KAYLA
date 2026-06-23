"""Pruebas end-to-end del pipeline de KAYLA con datos simulados.

Valida el flujo completo sin tocar servicios reales:
  Google Sheets (mockeado) -> filtrado por fecha -> agrupado por medico
  -> formato de mensaje -> payload de Telegram (mockeado).

No requiere credenciales ni red. Se ejecuta en CI.
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from main import send_reminders  # noqa: E402
from models import Paciente  # noqa: E402
from reminder_service import (  # noqa: E402
    filter_and_build,
    format_reminder_message,
    group_reminders_by_medico,
)


def _patient(
    dni: str,
    medico: str,
    chat_id: str,
    recojo: str = "",
    control: str = "",
    estado: str = "activo",
    diagnostico: str = "HTA",
) -> Paciente:
    return Paciente(
        dni=dni,
        nombres=f"Nombre{dni}",
        apellidos=f"Apellido{dni}",
        celular="999888777",
        diagnostico=diagnostico,
        fecha_recojo_medicamento=recojo,
        fecha_proximo_control=control,
        posta="Posta Centro",
        medico_a_cargo=medico,
        correo_medico=f"{medico.lower().replace('.', '')}@posta.gob.pe",
        telegram_chat_id=chat_id,
        estado=estado,
    )


def test_e2e_full_pipeline_with_mocked_sheets() -> None:
    """Sheets (mock) -> filter -> group -> format -> send (mock Telegram)."""
    today = date(2026, 6, 23)
    records = [
        _patient(
            "11111111",
            "Dr. Luis",
            "1001",
            recojo=(today + timedelta(days=1)).isoformat(),
        ).to_dict(),
        _patient(
            "22222222",
            "Dr. Maria",
            "1002",
            control=(today + timedelta(days=2)).isoformat(),
            diagnostico="DM2",
        ).to_dict(),
        # Paciente fuera de ventana: no genera recordatorio.
        _patient(
            "33333333",
            "Dr. Luis",
            "1001",
            recojo=(today + timedelta(days=10)).isoformat(),
        ).to_dict(),
        # Paciente inactivo: ignorado.
        _patient(
            "44444444",
            "Dr. Maria",
            "1002",
            recojo=(today + timedelta(days=1)).isoformat(),
            estado="inactivo",
        ).to_dict(),
    ]

    patients = [Paciente.from_dict(r) for r in records]

    reminders = filter_and_build(patients, today, days_ahead=2)
    assert len(reminders) == 2

    grouped = group_reminders_by_medico(reminders)
    assert set(grouped.keys()) == {"Dr. Luis", "Dr. Maria"}
    assert len(grouped["Dr. Luis"]) == 1
    assert len(grouped["Dr. Maria"]) == 1

    msg_luis = format_reminder_message(grouped["Dr. Luis"][0])
    assert "recojo de medicamento" in msg_luis
    assert "Nombre11111111" in msg_luis
    assert "DNI: 11111111" in msg_luis

    msg_maria = format_reminder_message(grouped["Dr. Maria"][0])
    assert "control medico" in msg_maria
    assert "DM2" in msg_maria

    fake_bot = MagicMock()
    fake_bot.default_chat_id = "9999"
    fake_bot.send_message.return_value = {"ok": True}

    total = send_reminders(grouped, fake_bot, dry_run=False)

    assert total == 2
    assert fake_bot.send_message.call_count == 2

    calls = {c.kwargs["chat_id"]: c for c in fake_bot.send_message.call_args_list}
    assert "1001" in calls
    assert "1002" in calls
    assert calls["1001"].kwargs["parse_mode"] == "Markdown"
    assert "Dr. Luis" in calls["1001"].kwargs["text"]
    assert "Dr. Maria" in calls["1002"].kwargs["text"]
    print("  [OK] e2e_full_pipeline_with_mocked_sheets")


def test_e2e_dry_run_does_not_send() -> None:
    """En dry-run no se invoca al bot de Telegram."""
    today = date(2026, 6, 23)
    patients = [
        _patient(
            "55555555",
            "Dr. Luis",
            "1001",
            recojo=(today + timedelta(days=1)).isoformat(),
        ),
    ]
    reminders = filter_and_build(patients, today, days_ahead=2)
    grouped = group_reminders_by_medico(reminders)

    fake_bot = MagicMock()
    total = send_reminders(grouped, fake_bot, dry_run=True)

    assert total == 1
    fake_bot.send_message.assert_not_called()
    print("  [OK] e2e_dry_run_does_not_send")


def test_e2e_routing_by_chat_id() -> None:
    """Cada medico recibe el mensaje en SU chat_id, no en el de otro."""
    today = date(2026, 6, 23)
    patients = [
        _patient(
            "66666666",
            "Dr. Luis",
            "1001",
            recojo=(today + timedelta(days=1)).isoformat(),
        ),
        _patient(
            "77777777",
            "Dr. Maria",
            "1002",
            recojo=(today + timedelta(days=1)).isoformat(),
        ),
    ]
    reminders = filter_and_build(patients, today, days_ahead=2)
    grouped = group_reminders_by_medico(reminders)

    fake_bot = MagicMock()
    fake_bot.default_chat_id = "9999"
    fake_bot.send_message.return_value = {"ok": True}

    send_reminders(grouped, fake_bot, dry_run=False)

    sent_chats = {c.kwargs["chat_id"] for c in fake_bot.send_message.call_args_list}
    assert sent_chats == {"1001", "1002"}
    print("  [OK] e2e_routing_by_chat_id")


def test_e2e_load_patients_via_mocked_sheetsclient() -> None:
    """Carga de pacientes via SheetsClient mockeado end-to-end."""
    today = date(2026, 6, 23)
    records = [
        _patient(
            "88888888",
            "Dr. Luis",
            "1001",
            recojo=(today + timedelta(days=1)).isoformat(),
        ).to_dict(),
    ]

    with patch("main.SheetsClient") as MockClient:
        instance = MockClient.return_value
        instance.get_all_records.return_value = records

        from main import load_patients  # noqa: E402

        patients = load_patients(instance)
        assert len(patients) == 1
        assert patients[0].dni == "88888888"
        assert patients[0].telegram_chat_id == "1001"

        reminders = filter_and_build(patients, today, days_ahead=2)
        assert len(reminders) == 1
        print("  [OK] e2e_load_patients_via_mocked_sheetsclient")


def main() -> None:
    print("Ejecutando pruebas E2E de KAYLA...\n")
    test_e2e_full_pipeline_with_mocked_sheets()
    test_e2e_dry_run_does_not_send()
    test_e2e_routing_by_chat_id()
    test_e2e_load_patients_via_mocked_sheetsclient()
    print("\n  Todas las pruebas E2E pasaron.")


if __name__ == "__main__":
    main()
