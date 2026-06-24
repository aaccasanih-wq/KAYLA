# Schema del Google Sheet — Base de Pacientes

Este documento define la estructura de datos de la hoja `Pacientes` del Google Sheet usado por KAYLA.

---

## Hoja principal: `Pacientes`

### Columnas (en orden)

| # | Columna | Tipo | Obligatorio | Descripción |
|---|---------|------|-------------|-------------|
| 1 | `dni` | texto (8 dígitos) | Sí | DNI del paciente. Clave primaria. |
| 2 | `nombres` | texto | Sí | Nombres del paciente. |
| 3 | `apellidos` | texto | Sí | Apellidos del paciente. |
| 4 | `celular` | texto | Sí | Número de celular (9 dígitos en Perú). |
| 5 | `diagnostico` | texto | Sí | Código de diagnóstico: `HTA`, `DM`, `DM2`, `EPOC`, `ASMA`, `OTRO`. |
| 6 | `fecha_recojo_medicamento` | fecha | No | Fecha del próximo recojo de medicamento (`YYYY-MM-DD`). |
| 7 | `fecha_proximo_control` | fecha | No | Fecha del próximo control médico (`YYYY-MM-DD`). |
| 8 | `posta` | texto | Sí | Nombre o código de la posta de salud. |
| 9 | `medico_a_cargo` | texto | Sí | Nombre del médico responsable. |
| 10 | `correo_medico` | texto | Sí | Correo del médico (para envío de reportes). |
| 11 | `telegram_chat_id` | texto | No | Chat ID de Telegram del médico (para enviarle sus recordatorios). Si está vacío, se usa `TELEGRAM_CHAT_ID_MEDICO` como fallback. |
| 12 | `estado` | texto | Sí | `activo`, `inactivo`, `fallecido`. Default: `activo`. |
| 13 | `observaciones` | texto | No | Notas libres (alergias, condiciones especiales, etc.). |

### Formato de fechas

Todos los campos de fecha se almacenan como **`YYYY-MM-DD`** (ej. `2026-06-25`).

El sistema acepta también `DD/MM/YYYY` y `DD-MM-YYYY` al ingresar datos, pero los normaliza a ISO 8601 al procesarlos.

### Códigos de diagnóstico

| Código | Significado |
|--------|-------------|
| `HTA` | Hipertensión arterial |
| `DM` | Diabetes mellitus (genérico) |
| `DM2` | Diabetes mellitus tipo 2 |
| `EPOC` | Enfermedad pulmonar obstructiva crónica |
| `ASMA` | Asma |
| `OTRO` | Otro diagnóstico (especificar en observaciones) |

### Estado del paciente

| Estado | Significado |
|--------|-------------|
| `activo` | Paciente en seguimiento activo |
| `inactivo` | Paciente dado de baja o trasladado |
| `fallecido` | Paciente fallecido |

---

## Hoja secundaria (futura): `Recordatorios`

Registro de los recordatorios enviados. Se implementará en una etapa posterior.

| # | Columna | Tipo | Descripción |
|---|---------|------|-------------|
| 1 | `fecha_envio` | datetime | Fecha y hora del envío |
| 2 | `dni` | texto | DNI del paciente |
| 3 | `tipo` | texto | `recojo` o `control` |
| 4 | `fecha_evento` | fecha | Fecha del recojo o control |
| 5 | `medico_a_cargo` | texto | Médico notificado |
| 6 | `estado` | texto | `enviado`, `confirmado`, `sin_respuesta` |

---

## Datos de ejemplo

Ver `data/sample_pacientes.csv` para un ejemplo con 5 pacientes ficticios (sin datos reales).

---

## Notas de seguridad

- El Google Sheet **no debe contener datos sensibles sin consentimiento** (Ley 29733 — Ley de Protección de Datos Personales del Perú).
- Para el MVP, los pacientes ficticios de ejemplo usan DNIs y celulares inventados.
- **Acceso al Sheet restringido:** el Sheet se comparte solo con el `client_email` de la service account (Editor) y la propietaria (Editor). Los médicos **no tienen acceso directo** al Sheet — solo pueden agregar pacientes mediante el Google Form vinculado.
- **Routing por médico:** cada médico recibe sus recordatorios en su propio chat de Telegram (campo `telegram_chat_id`). Si el campo está vacío, se usa `TELEGRAM_CHAT_ID_MEDICO` como fallback.
