from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from models import Paciente
from reminder_service import filter_and_build, format_reminder_message, group_reminders_by_medico
from sheets_client import SheetsClient


@st.cache_data(ttl=60)
def load_patients_df() -> pd.DataFrame:
    """Carga pacientes desde Google Sheets y retorna un DataFrame."""
    client = SheetsClient()
    records = client.get_all_records()
    if not records:
        return pd.DataFrame(
            columns=[
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
        )
    df = pd.DataFrame(records)
    return df


def main() -> None:
    st.set_page_config(
        page_title="KAYLA - Dashboard",
        page_icon=":syringe:",
        layout="wide",
    )

    st.title("KAYLA - Dashboard de Pacientes Cronicos")
    st.caption(
        "Recordatorios automaticos de medicamentos y controles medicos "
        "para postas de salud del Peru"
    )

    try:
        df = load_patients_df()
    except Exception as e:
        st.error(f"Error al cargar datos desde Google Sheets: {e}")
        st.info("Verifica las credenciales y el SPREADSHEET_ID en `.env`.")
        return

    if df.empty:
        st.warning("No hay pacientes registrados en el Google Sheet.")
        return

    # --- Metricas principales ---
    total_pacientes = len(df)
    activos = len(df[df["estado"].str.lower() == "activo"])
    postas = df["posta"].nunique()
    medicos = df["medico_a_cargo"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pacientes totales", total_pacientes)
    col2.metric("Pacientes activos", activos)
    col3.metric("Postas", postas)
    col4.metric("Medicos", medicos)

    st.divider()

    # --- Recordatorios proximos ---
    st.header("Recordatorios proximos")

    col_days, col_date, col_run = st.columns([1, 1, 1])
    with col_days:
        days_ahead = st.number_input(
            "Dias hacia adelante",
            min_value=1,
            max_value=30,
            value=2,
            help="Ventana de dias para filtrar recordatorios",
        )
    with col_date:
        target_date_str = st.date_input(
            "Fecha de referencia",
            value=date.today(),
            help="Fecha base para el calculo de recordatorios",
        )
    with col_run:
        st.write("")  # espaciador
        st.write("")  # espaciador
        if st.button("Actualizar datos", type="secondary"):
            load_patients_df.clear()
            st.rerun()

    target_date = (
        target_date_str if isinstance(target_date_str, date) else date.today()
    )

    patients = [Paciente.from_dict(row) for row in df.to_dict("records")]
    reminders = filter_and_build(patients, target_date, int(days_ahead))

    if not reminders:
        st.info(
            f"No hay recordatorios pendientes para los proximos {days_ahead} dias "
            f"desde {target_date.isoformat()}."
        )
    else:
        st.success(f"{len(reminders)} recordatorio(s) pendiente(s).")

        grouped = group_reminders_by_medico(reminders)

        for medico, meds in grouped.items():
            with st.expander(
                f":hospital: {medico} ({len(meds)} recordatorio(s))",
                expanded=True,
            ):
                for r in meds:
                    st.code(
                        format_reminder_message(r),
                        language="markdown",
                    )

    st.divider()

    # --- Tabla de pacientes ---
    st.header("Base de pacientes")

    col_filter1, col_filter2, col_filter3 = st.columns(3)
    with col_filter1:
        posta_filter = st.selectbox(
            "Filtrar por posta",
            options=["Todas"] + sorted(df["posta"].dropna().unique().tolist()),
        )
    with col_filter2:
        medico_filter = st.selectbox(
            "Filtrar por medico",
            options=["Todos"] + sorted(df["medico_a_cargo"].dropna().unique().tolist()),
        )
    with col_filter3:
        estado_filter = st.selectbox(
            "Filtrar por estado",
            options=["Todos", "activo", "inactivo", "fallecido"],
        )

    df_filtered = df.copy()
    if posta_filter != "Todas":
        df_filtered = df_filtered[df_filtered["posta"] == posta_filter]
    if medico_filter != "Todos":
        df_filtered = df_filtered[df_filtered["medico_a_cargo"] == medico_filter]
    if estado_filter != "Todos":
        df_filtered = df_filtered[
            df_filtered["estado"].str.lower() == estado_filter
        ]

    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "dni": st.column_config.TextColumn("DNI", width="small"),
            "celular": st.column_config.TextColumn("Celular", width="small"),
            "correo_medico": st.column_config.TextColumn(
                "Correo medico", width="medium"
            ),
            "observaciones": st.column_config.TextColumn(
                "Observaciones", width="large"
            ),
        },
    )

    st.divider()

    # --- Distribucion por diagnostico ---
    st.header("Distribucion por diagnostico")
    diag_counts = df_filtered["diagnostico"].value_counts().reset_index()
    diag_counts.columns = ["Diagnostico", "Cantidad"]
    st.bar_chart(diag_counts.set_index("Diagnostico"))

    st.divider()

    # --- Proximos eventos (calendario) ---
    st.header("Proximos eventos (recojo y control)")
    eventos: list[dict] = []
    for _, row in df_filtered.iterrows():
        for tipo, col in [
            ("Recojo", "fecha_recojo_medicamento"),
            ("Control", "fecha_proximo_control"),
        ]:
            fecha_val = row.get(col, "")
            if fecha_val:
                eventos.append(
                    {
                        "Fecha": str(fecha_val),
                        "Tipo": tipo,
                        "Paciente": f"{row['nombres']} {row['apellidos']}",
                        "DNI": row["dni"],
                        "Diagnostico": row["diagnostico"],
                        "Posta": row["posta"],
                        "Medico": row["medico_a_cargo"],
                    }
                )

    if eventos:
        df_eventos = pd.DataFrame(eventos)
        df_eventos["Fecha"] = pd.to_datetime(
            df_eventos["Fecha"], errors="coerce", format="mixed"
        )
        df_eventos = df_eventos.dropna(subset=["Fecha"]).sort_values("Fecha")
        st.dataframe(df_eventos, use_container_width=True, hide_index=True)
    else:
        st.info("No hay eventos proximos registrados.")

    st.divider()

    # --- Pie de pagina ---
    st.caption("KAYLA - Data Science con Python 2026-I | Universidad del Pacifico")
    st.caption("Construido con Streamlit, gspread y Telegram Bot API")


if __name__ == "__main__":
    main()
