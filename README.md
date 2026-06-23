# KAYLA

> **One-liner:** Automatizamos los recordatorios de medicamentos y controles médicos para pacientes crónicos de postas de salud vía Telegram, reduciendo la pérdida de pacientes y mejorando las métricas de las micro-redes de salud pública en Perú.

KAYLA es un sistema que lee la base de datos de pacientes desde Google Sheets, identifica quién tiene fecha de recojo de medicamentos o control médico próximo, y envía recordatorios automáticos por Telegram al médico o técnico a cargo. Incluye un dashboard web (Streamlit) para visualizar el estado de todos los pacientes y recordatorios.

> **Demo en vivo (sin instalar nada):**
> - Dashboard: https://kayla-demo.streamlit.app
> - Landing page: https://aaccasanih-wq.github.io/KAYLA/
> - Repositorio: https://github.com/aaccasanih-wq/KAYLA
> - Video demo: _pendiente de subir_ (guion en [`docs/video_script.md`](docs/video_script.md))

---

## Tabla de contenidos

- [Problema](#problema)
- [Solución](#solución)
- [Arquitectura](#arquitectura)
- [Stack y herramientas del curso](#stack-y-herramientas-del-curso)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Cómo ejecutar localmente](#cómo-ejecutar-localmente)
- [Variables de entorno](#variables-de-entorno)
- [Automatización con GitHub Actions](#automatización-con-github-actions)
- [Despliegue](#despliegue)
- [Modelo de negocio](#modelo-de-negocio)
- [Roadmap](#roadmap)
- [Capturas de pantalla](#capturas-de-pantalla)
- [Video demo](#video-demo)
- [Documentación y pitch](#documentación-y-pitch)
- [Autor](#autor)
- [Licencia](#licencia)

---

## Problema

El **40 % de pacientes crónicos** (hipertensos, diabéticos) en postas de primer nivel de salud del MINSA en Perú no recogen sus medicamentos ni asisten a sus controles mensuales. Los técnicos y enfermeras pierden horas llamando manualmente a ~80 pacientes al mes. Si no se cumplen las métricas de la Diris/Diresa, la posta pierde recursos o el personal recibe sanciones.

**Cómo lo resuelven hoy:** Excel + llamadas manuales + WhatsApp personal del médico. Sin sistema, sin automatización, sin métricas.

## Solución

KAYLA se integra con las herramientas que las postas **ya usan** (Google Sheets y Telegram) y automatiza el flujo de recordatorios:

1. El médico registra pacientes en un Google Form (o edita directamente el Google Sheet).
2. Cada mañana, el sistema revisa quién tiene fecha de recojo/control en los próximos 2 días.
3. Envía un mensaje de Telegram al médico/técnico a cargo con los datos del paciente.
4. El médico contacta al paciente y confirma la asistencia.
5. El dashboard de Streamlit muestra el estado de todos los pacientes y recordatorios.

**Insight:** No es un problema de "falta de tecnología en salud". Es un problema de herramientas que no llegan al primer nivel. Las postas no tienen presupuesto para software de gestión, pero sí tienen Google Sheets y Telegram. El sistema debe funcionar con lo que ya usan.

---

## Arquitectura

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Google Form    │────▶│  Google Sheets   │────▶│  Script Python  │
│  (médicos       │     │  (base de datos  │     │  (GitHub Actions│
│   llenan)       │     │   de pacientes)  │     │   cada mañana)  │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                            │
                              ┌─────────────────────────────┘
                              ▼
                    ┌─────────────────┐
                    │  Telegram Bot   │────▶ Médico/Técnico recibe:
                    │  (mensaje al    │       "Juan Pérez (HTA) debe
                    │   médico)       │        recoger medicamento
                    │                 │        el 25/06. Cel: 999888777"
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐     ┌─────────────────┐
                    │  Streamlit      │────▶│  GitHub Pages   │
                    │  (dashboard     │     │  (landing page  │
                    │   web)          │     │   con pricing)  │
                    └─────────────────┘     └─────────────────┘
```

---

## Stack y herramientas del curso

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| Backend / Script | Python 3.11 | Lenguaje del curso, amplio ecosistema |
| Base de datos | Google Sheets | Los médicos ya lo usan; cero curva de aprendizaje |
| Ingesta de datos | `gspread` + Google Forms | Lectura/escritura de Sheets desde Python |
| Mensajería | Telegram Bot API (`python-telegram-bot`) | Gratis, robusto, fácil de configurar |
| Dashboard | Streamlit | Del curso, rápido de construir, desplegable gratis |
| Landing page | HTML/CSS estático + GitHub Pages | Gratis, rápido, profesional |
| Scheduler | GitHub Actions | Gratis (500 min/mes), integrado al repo |
| Asistencia de código | Claude Code / Cursor | Co-founder técnico virtual |

### Herramientas del curso usadas (mínimo 2 requeridas)

1. **APIs (Google Sheets API + Telegram Bot API):** Tema de APIs del curso. Usamos `gspread` para interactuar con Google Sheets y `python-telegram-bot` para enviar mensajes.
2. **Streamlit:** Tema de visualización del curso. Dashboard interactivo para médicos.

**Adicionales:** Claude Code (agente de código), GitHub Actions (CI/CD básico para el scheduler).

---

## Estructura del repositorio

```
KAYLA/
├── README.md              # Este archivo
├── LICENSE                # MIT
├── requirements.txt       # Dependencias Python
├── .env.example           # Variables de entorno (valores dummy)
├── .gitignore
├── .streamlit/            # Config del dashboard
│   ├── config.toml        # Tema y opciones de la app
│   └── secrets.toml.example  # Plantilla de secrets para Streamlit Cloud
├── docs/                  # Pitch deck, diagrama, video, evidencias
│   ├── README.md          # Índice de documentación
│   ├── pitch.pdf          # Pitch deck (14 slides, YC)
│   ├── pitch.html         # Pitch deck editable
│   ├── architecture.png   # Diagrama de arquitectura (PNG)
│   ├── architecture.svg   # Diagrama de arquitectura (SVG)
│   ├── video_script.md    # Guion del video demo
│   ├── screenshots/       # Capturas de pantalla
│   └── research/          # 5 evidencias de validación
├── frontend/              # Dashboard Streamlit
│   └── app.py
├── backend/               # Lógica de negocio, Sheets, Telegram
│   ├── main.py            # Orquestador del scheduler
│   ├── sheets_client.py   # Cliente Google Sheets (env/file creds)
│   ├── telegram_bot.py    # Cliente Telegram Bot API
│   ├── reminder_service.py
│   ├── models.py
│   └── test_reminder_service.py
├── tests/                 # Tests E2E y de credenciales
│   ├── test_e2e_pipeline.py
│   └── test_sheets_credentials.py
├── app/                   # Aplicación principal (orquestador)
├── ai/                    # Prompts, agentes (futuro)
├── data/                  # Muestras chicas; datasets grandes en releases
├── notebooks/             # Exploración y EDA
├── landing/               # Landing page HTML/CSS
│   ├── index.html
│   ├── pricing.html
│   └── styles.css
└── .github/workflows/     # CI + scheduler + deploy Pages
```

---

## Cómo ejecutar localmente

### Requisitos previos

- Python 3.11+
- Una cuenta de Google con acceso a Google Sheets
- Un bot de Telegram (creado con [@BotFather](https://t.me/BotFather))
- Un Google Sheet con la base de datos de pacientes (ver `data/schema.md`)

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/aaccasanih-wq/KAYLA.git
cd KAYLA

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar el archivo de variables de entorno
cp .env.example .env
# Editar .env con tus credenciales reales (NO subir .env al repo)

# 5. Colocar credentials.json de Google Service Account en la raíz
#    (NO subir credentials.json al repo)

# 6. Ejecutar el dashboard
streamlit run frontend/app.py
```

---

## Variables de entorno

Ver `.env.example` para la lista completa. **Nunca subir `.env` ni `credentials.json` al repositorio.**

| Variable | Descripción |
|----------|-------------|
| `GOOGLE_SHEETS_CREDENTIALS_PATH` | Ruta al archivo JSON de credenciales de servicio de Google (dev local / GitHub Actions) |
| `GOOGLE_SHEETS_CREDENTIALS_JSON` | JSON de la Service Account como string (Streamlit Cloud / PaaS) |
| `GOOGLE_SHEETS_CREDENTIALS_B64` | Mismo JSON codificado en base64 (alternativa para PaaS) |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | ID del Google Sheet con la base de datos de pacientes |
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram (de @BotFather) |
| `TELEGRAM_CHAT_ID_MEDICO` | Chat ID de Telegram del médico/técnico a notificar (fallback) |

> Las credenciales se resuelven en orden: `GOOGLE_SHEETS_CREDENTIALS_JSON` → `GOOGLE_SHEETS_CREDENTIALS_B64` → archivo en `GOOGLE_SHEETS_CREDENTIALS_PATH`. En Streamlit Cloud, `frontend/app.py` mapea `st.secrets` a estas variables automáticamente.

---

## Automatización con GitHub Actions

El repositorio incluye dos workflows en `.github/workflows/`:

### Scheduler de recordatorios (`scheduler.yml`)

Ejecuta el orquestador (`backend/main.py`) todos los días a las **8:00 a.m. (hora de Perú, UTC-5)** — equivalente a `13:00 UTC` en el cron. Lee los pacientes de Google Sheets, filtra los que tienen recojo/control en los próximos 2 días y envía los recordatorios por Telegram al médico a cargo.

También se puede disparar manualmente desde la pestaña **Actions → KAYLA Scheduler → Run workflow**, con dos parámetros opcionales:

- `days`: ventana de días hacia adelante (default `2`).
- `dry_run`: si está activo, no envía mensajes a Telegram; solo los imprime en el log (útil para validar).

### CI (`ci.yml`)

Se ejecuta en cada `push` a `main` y a branches `feature/**`, y en cada `pull_request` hacia `main`. Corre:

1. **Lint** con `ruff` (reglas `F,E9`: imports no usados, nombres no definidos, errores de sintaxis).
2. **Chequeo de sintaxis** con `python -m py_compile` sobre `backend/` y `frontend/`.
3. **Tests** con `pytest` (24 tests en total):
   - `backend/test_reminder_service.py` — 11 tests del filtrado por fechas y generación de recordatorios.
   - `tests/test_e2e_pipeline.py` — 4 tests end-to-end del flujo completo (Sheets → filtro → agrupado → Telegram) con mocks, incluido el *routing* por `chat_id` y el modo *dry-run*.
   - `tests/test_sheets_credentials.py` — 9 tests de resolución de credenciales (env JSON, base64, archivo) sin tocar la red.

Los scripts `backend/test_connection.py` y `backend/test_telegram.py` son pruebas manuales que requieren credenciales reales, por eso no se ejecutan en CI.

### Secrets a configurar

En **Settings → Secrets and variables → Actions** del repo, agregar:

| Secret | Descripción | Cómo obtenerlo |
|--------|-------------|----------------|
| `GOOGLE_SHEETS_CREDENTIALS_B64` | JSON de la Service Account de Google codificado en **base64** | `base64 -i credentials.json -o creds.b64` (macOS) o `base64 credentials.json > creds.b64` (Linux); copiar el contenido |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | ID del Google Sheet de pacientes | Extraído de la URL del Sheet |
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | Desde `@BotFather` |
| `TELEGRAM_CHAT_ID_MEDICO` | Chat ID de Telegram del médico/técnico | Desde `@userinfobot` o el JSON de `getUpdates` |

El scheduler reconstruye `credentials.json` desde el secret en base64 en cada ejecución, por lo que el archivo de credenciales **nunca** se sube al repositorio.

---

## Despliegue

| Componente | Plataforma | URL / Estado |
|------------|-----------|--------------|
| Repositorio | GitHub | https://github.com/aaccasanih-wq/KAYLA |
| Scheduler de recordatorios | GitHub Actions | Activo (cron diario 8 a.m. PET) |
| CI (lint + tests) | GitHub Actions | Activo |
| Landing page | GitHub Pages | https://aaccasanih-wq.github.io/KAYLA/ |
| Dashboard | Streamlit Community Cloud | https://kayla-demo.streamlit.app |
| Video demo | YouTube/Loom | _pendiente de grabar_ |

### Dashboard en Streamlit Community Cloud

El dashboard lee los pacientes desde Google Sheets usando una Service Account. En Streamlit Cloud las credenciales **no** van en un archivo: se configuran como **secrets**.

1. Ir a [share.streamlit.io](https://share.streamlit.io) → **New app** → seleccionar el repo `aaccasanih-wq/KAYLA`, branch `main`, archivo `frontend/app.py`.
2. En **Settings → Secrets** pegar el contenido de [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example) con los valores reales:
   - `[gcp_service_account]` con el contenido completo de `credentials.json` (la Service Account con acceso al Sheet).
   - `GOOGLE_SHEETS_SPREADSHEET_ID` con el ID del Sheet de pacientes.
3. **Save** y **Reboot**. La app queda pública en `https://<app-name>.streamlit.app`.

> El dashboard no envía mensajes de Telegram (solo los muestra); los tokens de Telegram en secrets son opcionales para el dashboard pero se dejan por consistencia.

---

## Modelo de negocio

**Freemium B2B ligero** (no vendemos al Estado directamente; vendemos a profesionales de salud que luego presionan hacia arriba):

| Plan | Precio | Incluye |
|------|--------|---------|
| **Gratis** | S/0/mes | 1 posta, hasta 50 pacientes, recordatorios por Telegram, Google Sheets |
| **Pro** | S/49/mes | Hasta 3 postas, 500 pacientes, dashboard con métricas, reporte mensual para Diris |
| **Micro-red** | S/199/mes | 10 postas, pacientes ilimitados, admin centralizado, onboarding personalizado |

**Costo variable por usuario:** ~S/0 (Telegram gratis, Google Sheets gratis, GitHub Actions gratis). Margen de contribución cercano al 100 %.

---

## Roadmap

| Plazo | Hito |
|-------|------|
| **3 meses** | 3 postas activas, sistema estable con Telegram, primeros usuarios pagando (plan Pro) |
| **6 meses** | 10 postas, integración con WhatsApp Business API, dashboard con predicción de abandono |
| **12 meses** | 50 postas (1 micro-red), primer convenio institucional (ONG o municipalidad), integración con HIS del MINSA |

---

## Capturas de pantalla

Las capturas están en [`docs/screenshots/`](docs/screenshots/):

| Captura | Descripción |
|---------|-------------|
| `dashboard.png` | Dashboard de Streamlit: métricas, recordatorios agrupados por médico y base de pacientes. |
| `telegram.png` | Mensaje de recordatorio recibido por el médico en Telegram (formato Markdown). |
| `landing.png` | Landing page con hero, problema, solución y pricing. |
| `sheet.png` | Google Sheet de pacientes con el formulario vinculado. |

> Ver [`docs/screenshots/README.md`](docs/screenshots/README.md) para la guía de captura.

## Video demo

- **Guion:** [`docs/video_script.md`](docs/video_script.md) — 2-3 minutos con timestamps y voz en off.
- **Video grabado:** _pendiente de subir a YouTube (no listado) o Loom_ (link aquí tras grabar).

---

## Documentación y pitch

### Pitch deck

- **[`docs/pitch.pdf`](docs/pitch.pdf)** — Pitch deck en formato Y Combinator (14 slides: one-liner, founder, problema, solución, mercado, competencia, producto, modelo de negocio, GTM, tracción, roadmap, riesgos, the ask).
- Fuente editable: [`docs/pitch.html`](docs/pitch.html) (abrir en el navegador → ⌘P → "Guardar como PDF").
- Ver [`docs/README.md`](docs/README.md) para instrucciones detalladas.

### Diagrama de arquitectura

- **[`docs/architecture.png`](docs/architecture.png)** / **[`docs/architecture.svg`](docs/architecture.svg)** — Diagrama del flujo: Google Form → Google Sheets → Script Python (GitHub Actions) → Telegram Bot → Médico, con Streamlit y GitHub Pages como derivaciones.

### Evidencias de validación

Carpeta [`docs/research/`](docs/research/) con 5 evidencias:

| # | Evidencia | Tipo |
|---|-----------|------|
| 1 | [Entrevista con técnico de posta](docs/research/01_entrevista_tecnico_posta.md) | Entrevista |
| 2 | [Entrevista con médico de posta](docs/research/02_entrevista_medico_posta.md) | Entrevista |
| 3 | [Observación de flujo en posta](docs/research/03_observacion_flujo_posta.md) | Observación de campo |
| 4 | [Validación de métricas del MINSA](docs/research/04_validacion_metricas_minsa.md) | Investigación documental |
| 5 | [Lista de espera y señales de demanda](docs/research/05_lista_espera_demanda.md) | Tracción temprana |

---

## Autor

**Axel Aaron Ccasani Huachua** — Solo Founder

- Curso: Data Science con Python – 2026-I
- Universidad del Pacífico – Departamento de Economía
- Docente: Alexander Quispe

Construido con asistencia de Claude Code como co-founder técnico.

---

## Licencia

[MIT](LICENSE) © 2026 Axel Aaron Ccasani Huachua
