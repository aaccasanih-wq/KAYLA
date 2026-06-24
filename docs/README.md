# Documentación de KAYLA

Esta carpeta contiene la documentación del proyecto: pitch deck, diagrama de
arquitectura, guion del video demo y evidencias de validación.

## Contenido

### Pitch deck

- **[`pitch.pdf`](pitch.pdf)** — Pitch deck en formato Y Combinator (14 slides), listo para entregar.
- **[`pitch.html`](pitch.html)** — Fuente editable. Para exportar a PDF: abrir en el navegador → ⌘P → "Guardar como PDF".

### Arquitectura

- **[`architecture.png`](architecture.png)** / **[`architecture.svg`](architecture.svg)** — Diagrama de arquitectura del sistema.
  Muestra el flujo: Google Form → Google Sheets → Script Python (GitHub Actions) →
  Telegram Bot → Médico, con Streamlit y GitHub Pages como derivaciones.

### Capturas de pantalla

- **[`screenshots/`](screenshots/)** — Capturas del dashboard, Telegram, landing y Sheet.

### Video demo

- **[`video_script.md`](video_script.md)** — Guion del video demo de 2-3 minutos
  con timestamps, instrucciones de preparación y texto para voz en off.

### Evidencias de validación

Carpeta **[`research/`](research/)** con 5 evidencias de validación:

1. [`01_entrevista_tecnico_posta.md`](research/01_entrevista_tecnico_posta.md) — Entrevista con médico de posta (Lima Este)
2. [`02_entrevista_medico_posta.md`](research/02_entrevista_medico_posta.md) — Entrevista con médico de posta (Lima Norte)
3. [`03_observacion_flujo_posta.md`](research/03_observacion_flujo_posta.md) — Observación de flujo de trabajo en posta
4. [`04_validacion_metricas_minsa.md`](research/04_validacion_metricas_minsa.md) — Validación de métricas del MINSA
5. [`05_lista_espera_demanda.md`](research/05_lista_espera_demanda.md) — Lista de espera y señales de demanda

## Cómo exportar el pitch deck a PDF

1. Abrir `docs/pitch.html` en Google Chrome o Safari.
2. Presionar ⌘P (o Ctrl+P en Windows).
3. En "Destino", seleccionar "Guardar como PDF".
4. En "Más ajustes":
   - Tamaño del papel: personalizado (1280 × 720 px) o Letter horizontal.
   - Márgenes: ninguno.
   - Sin encabezados ni pies de página.
5. Guardar como `docs/pitch.pdf`.
