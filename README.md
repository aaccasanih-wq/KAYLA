# KAYLA

> **One-liner:** Automatizamos los recordatorios de medicamentos y controles médicos para pacientes crónicos de postas de salud vía Telegram, reduciendo la pérdida de pacientes y mejorando las métricas de las micro-redes de salud pública en Perú.

KAYLA es un sistema que lee la base de datos de pacientes desde Google Sheets, identifica quién tiene fecha de recojo de medicamentos o control médico próximo, y envía recordatorios automáticos por Telegram al médico o técnico a cargo. Incluye un dashboard web (Streamlit) para visualizar el estado de todos los pacientes y recordatorios.

---

## Tabla de contenidos

- [Problema](#problema)
- [Solución](#solución)
- [Arquitectura](#arquitectura)
- [Stack y herramientas del curso](#stack-y-herramientas-del-curso)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Cómo ejecutar localmente](#cómo-ejecutar-localmente)
- [Variables de entorno](#variables-de-entorno)
- [Despliegue](#despliegue)
- [Modelo de negocio](#modelo-de-negocio)
- [Roadmap](#roadmap)
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
├── .env.example           # Variables de entorno (valores dummy)
├── .gitignore
├── requirements.txt       # Dependencias Python
├── docs/                  # Pitch deck, capturas, diagramas, video
├── frontend/              # Dashboard Streamlit
│   └── app.py
├── backend/               # Lógica de negocio, Sheets, Telegram
│   ├── main.py
│   ├── sheets_client.py
│   ├── telegram_bot.py
│   ├── reminder_service.py
│   └── models.py
├── app/                   # Aplicación principal (orquestador)
├── tests/                 # Tests básicos
├── ai/                    # Prompts, agentes (futuro)
├── data/                  # Muestras chicas; datasets grandes en releases
├── notebooks/             # Exploración y EDA
├── landing/               # Landing page HTML/CSS
└── .github/workflows/     # CI + scheduler
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
| `GOOGLE_SHEETS_CREDENTIALS_PATH` | Ruta al archivo JSON de credenciales de servicio de Google |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | ID del Google Sheet con la base de datos de pacientes |
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram (de @BotFather) |
| `TELEGRAM_CHAT_ID_MEDICO` | Chat ID de Telegram del médico/técnico a notificar |

---

## Despliegue

| Componente | Plataforma | Estado |
|------------|-----------|--------|
| Repositorio | GitHub | Activo |
| Dashboard | Streamlit Community Cloud | Por desplegar |
| Landing page | GitHub Pages | Por desplegar |
| Video demo | YouTube/Loom | Por grabar |

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

## Autor

**Axel Aaron Ccasani Huachua** — Solo Founder

- Curso: Data Science con Python – 2026-I
- Universidad del Pacífico – Departamento de Economía
- Docente: Alexander Quispe

Construido con asistencia de Claude Code como co-founder técnico.

---

## Licencia

[MIT](LICENSE) © 2026 Axel Aaron Ccasani Huachua
