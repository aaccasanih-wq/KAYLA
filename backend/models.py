from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


# Columnas del Google Sheet, en orden.
COLUMNS: list[str] = [
    "dni",
    "nombres",
    "apellidos",
    "celular",
    "diagnostico",
    "fecha_recojo_medicamento",
    "fecha_proximo_control",
    "posta",
    "medico_a_cargo",
    "correo_medico",
    "estado",
    "observaciones",
]


# Valores válidos para campos cerrados
DIAGNOSTICOS_VALIDOS = {"HTA", "DM", "DM2", "EPOC", "ASMA", "OTRO"}
ESTADOS_VALIDOS = {"activo", "inactivo", "fallecido"}


@dataclass
class Paciente:
    """Representa un paciente crónico registrado en la posta de salud."""

    dni: str
    nombres: str
    apellidos: str
    celular: str
    diagnostico: str
    fecha_recojo_medicamento: str
    fecha_proximo_control: str
    posta: str
    medico_a_cargo: str
    correo_medico: str
    estado: str = "activo"
    observaciones: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {col: getattr(self, col) for col in COLUMNS}

    @staticmethod
    def from_dict(row: dict[str, Any]) -> "Paciente":
        values = {col: row.get(col, "") for col in COLUMNS}
        return Paciente(**values)

    def validate(self) -> list[str]:
        """Retorna una lista de errores de validación. Vacía si es válido."""
        errors: list[str] = []

        if not self.dni or len(self.dni) != 8:
            errors.append(f"DNI inválido: '{self.dni}' (debe tener 8 dígitos)")

        if not self.nombres:
            errors.append("Nombres es obligatorio")

        if not self.apellidos:
            errors.append("Apellidos es obligatorio")

        if not self.celular or len(self.celular) < 7:
            errors.append(f"Celular inválido: '{self.celular}'")

        if self.diagnostico.upper() not in DIAGNOSTICOS_VALIDOS:
            errors.append(
                f"Diagnóstico inválido: '{self.diagnostico}'. "
                f"Válidos: {sorted(DIAGNOSTICOS_VALIDOS)}"
            )

        for fecha_field, label in [
            ("fecha_recojo_medicamento", "fecha_recojo_medicamento"),
            ("fecha_proximo_control", "fecha_proximo_control"),
        ]:
            value = getattr(self, fecha_field)
            if value:
                if not _parse_date(value):
                    errors.append(
                        f"{label} inválida: '{value}'. "
                        "Usar formato YYYY-MM-DD o DD/MM/YYYY."
                    )

        if self.estado.lower() not in ESTADOS_VALIDOS:
            errors.append(
                f"Estado inválido: '{self.estado}'. "
                f"Válidos: {sorted(ESTADOS_VALIDOS)}"
            )

        return errors


def _parse_date(value: str) -> date | None:
    """Intenta parsear una fecha en varios formatos comunes."""
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(str(value), fmt).date()
        except ValueError:
            continue
    return None


def normalize_date(value: str) -> str:
    """Normaliza cualquier fecha aceptada a YYYY-MM-DD."""
    parsed = _parse_date(value)
    return parsed.isoformat() if parsed else str(value)


@dataclass
class Recordatorio:
    """Mensaje de recordatorio generado para un paciente."""

    paciente: Paciente
    tipo: str  # "recojo" o "control"
    fecha: str
    mensaje: str = field(init=False)

    def __post_init__(self) -> None:
        if self.tipo == "recojo":
            self.mensaje = (
                f"Recordatorio de recojo de medicamento:\n"
                f"  Paciente: {self.paciente.nombres} {self.paciente.apellidos} "
                f"(DNI: {self.paciente.dni})\n"
                f"  Diagnóstico: {self.paciente.diagnostico}\n"
                f"  Fecha de recojo: {self.fecha}\n"
                f"  Celular: {self.paciente.celular}\n"
                f"  Posta: {self.paciente.posta}\n"
                f"  Médico a cargo: {self.paciente.medico_a_cargo}"
            )
        elif self.tipo == "control":
            self.mensaje = (
                f"Recordatorio de control médico:\n"
                f"  Paciente: {self.paciente.nombres} {self.paciente.apellidos} "
                f"(DNI: {self.paciente.dni})\n"
                f"  Diagnóstico: {self.paciente.diagnostico}\n"
                f"  Fecha de control: {self.fecha}\n"
                f"  Celular: {self.paciente.celular}\n"
                f"  Posta: {self.paciente.posta}\n"
                f"  Médico a cargo: {self.paciente.medico_a_cargo}"
            )
        else:
            self.mensaje = f"Recordatorio para {self.paciente.nombres} {self.paciente.apellidos}: {self.fecha}"
