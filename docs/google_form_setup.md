# Configuración del Google Form

El Google Form es la forma en que los médicos agregan nuevos pacientes a la base de datos **sin acceder directamente al Google Sheet**. Las respuestas del Form caen automáticamente como filas nuevas en el Sheet.

---

## Por qué un Form y no edición directa del Sheet

- **Seguridad:** el Sheet contiene datos sensibles (DNI, celulares, diagnósticos). Si compartieras el link del Sheet, cualquier médico podría ver o editar los pacientes de otros médicos.
- **Control de calidad:** el Form valida los campos (formato de DNI, fechas, opciones cerradas) antes de que entren al Sheet.
- **Cero curva de aprendizaje:** el médico solo llena un formulario, no aprende a usar Sheets.

---

## Paso 1: Crear el Form

1. Ve a [forms.google.com](https://forms.google.com) y crea un **Form en blanco**.
2. Nómbralo: **"KAYLA — Registro de paciente"**
3. En la pestaña **Settings (Configuración)**:
   - **Responses → Collect email addresses**: opcional (puedes requerirlo si quieres saber qué médico llena el form).
   - **Presentation → Confirmation message**: "Paciente registrado. El sistema enviará el recordatorio automáticamente."

---

## Paso 2: Crear las preguntas

Agrega estas preguntas **en este orden** (el orden de las columnas del Sheet debe coincidir):

| # | Pregunta | Tipo de pregunta | Obligatorio | Notas |
|---|----------|------------------|-------------|-------|
| 1 | DNI del paciente | Respuesta corta | Sí | Validación: texto, 8 caracteres |
| 2 | Nombres | Respuesta corta | Sí | |
| 3 | Apellidos | Respuesta corta | Sí | |
| 4 | Celular (9 dígitos) | Respuesta corta | Sí | |
| 5 | Diagnóstico | Desplegable | Sí | Opciones: HTA, DM, DM2, EPOC, ASMA, OTRO |
| 6 | Fecha de recojo de medicamento | Fecha | No | Formato YYYY-MM-DD |
| 7 | Fecha de próximo control | Fecha | No | Formato YYYY-MM-DD |
| 8 | Posta | Respuesta corta | Sí | |
| 9 | Médico a cargo | Respuesta corta | Sí | |
| 10 | Correo del médico | Respuesta corta | Sí | Validación: email |
| 11 | Chat ID de Telegram del médico | Respuesta corta | No | Ver cómo obtenerlo abajo |
| 12 | Observaciones | Párrafo | No | |

> **Nota sobre `estado`:** el Form no pregunta el estado porque todos los pacientes nuevos empiezan como `activo`. Tendrás que agregar la columna `estado` manualmente en el Sheet con valor `activo` para las filas que vengan del Form, o agregar una columna default en el Sheet.

> **Nota sobre `telegram_chat_id`:** cada médico debe obtener su chat ID una vez. Ver sección abajo.

---

## Paso 3: Vincular el Form al Google Sheet

> **Importante:** Google Forms **siempre crea una hoja nueva** ("Form Responses 1") al vincularse — no escribe en tu hoja "Pacientes" existente. Esto es comportamiento normal. La solución es un Apps Script (Paso 3b) que copia cada respuesta nueva a "Pacientes" con las columnas correctas.

1. En el Form, ve a la pestaña **Responses (Respuestas)**.
2. Haz clic en el ícono de **Google Sheets** (verde, arriba a la derecha).
3. Selecciona **"Select existing spreadsheet"** → elige el spreadsheet de KAYLA.
4. Google Forms creará una hoja nueva llamada **"Form Responses 1"** dentro de tu spreadsheet. No la borres.

### Paso 3b: Instalar el Apps Script (copia respuestas a "Pacientes")

Para que cada respuesta del Form caiga automáticamente en la hoja "Pacientes" con las columnas correctas:

1. Abre tu Google Sheet (el de KAYLA, no el Form).
2. Ve a **Extensions → Apps Script** (se abre una pestaña nueva).
3. Borra el código que haya y pega este:

```javascript
function onFormSubmit(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var pacientesSheet = ss.getSheetByName("Pacientes");
  if (!pacientesSheet || !e || !e.values) return;

  var values = e.values;
  // values[0] = timestamp
  // Si "Collect email addresses" está activado, values[1] = email y las respuestas se desplazan +1.
  // Lo detectamos leyendo los headers de la hoja de respuestas.
  var responseSheet = e.range.getSheet();
  var lastCol = responseSheet.getLastColumn();
  var headers = responseSheet.getRange(1, 1, 1, lastCol).getValues()[0];
  var secondHeader = String(headers[1] || "").toLowerCase();
  var hasEmailCol = secondHeader.indexOf("email") >= 0 || secondHeader.indexOf("correo") >= 0;

  var i = hasEmailCol ? 2 : 1; // índice donde empiezan las respuestas reales

  var newRow = [
    values[i]      || "",  // dni
    values[i + 1]  || "",  // nombres
    values[i + 2]  || "",  // apellidos
    values[i + 3]  || "",  // celular
    values[i + 4]  || "",  // diagnostico
    values[i + 5]  || "",  // fecha_recojo_medicamento
    values[i + 6]  || "",  // fecha_proximo_control
    values[i + 7]  || "",  // posta
    values[i + 8]  || "",  // medico_a_cargo
    values[i + 9]  || "",  // correo_medico
    values[i + 10] || "",  // telegram_chat_id
    "activo",              // estado (default para pacientes nuevos)
    values[i + 11] || ""   // observaciones
  ];

  pacientesSheet.appendRow(newRow);
}
```

4. **Guarda**: ícono de diskette (o ⌘S). Nómbralo "KAYLA Form Sync".
5. **Crea el trigger**:
   - En el menú izquierdo del editor, clic en el ícono de **reloj** ("Triggers", alarmas).
   - Botón **Add Trigger** (abajo a la derecha).
   - Configura:
     - Choose which function to run: `onFormSubmit`
     - Choose which deployment should run: `Head`
     - Select event source: **From spreadsheet**
     - Select event type: **On form submit**
   - **Save**.
6. **Autoriza**: Google te pedirá permisos. Clic en tu cuenta → Advanced → Go to project → Allow. Es normal que pida acceso a tus Sheets.
7. Cierra el editor de Apps Script.

### Probar el Form

1. Abre el link del Form en una ventana de incógnito.
2. Llena una respuesta de prueba.
3. Revisa tu Google Sheet: debe aparecer una fila nueva en **"Form Responses 1"** (el Form la crea) Y una fila nueva en **"Pacientes"** (el Apps Script la copia).
4. Si no aparece en "Pacientes", revisa las ejecuciones del trigger en Apps Script (Triggers → última ejecución → ver log de errores).

> **Nota:** el orden de las preguntas del Form debe ser exactamente el del Paso 2 (DNI, Nombres, Apellidos, Celular, Diagnóstico, Fecha recojo, Fecha control, Posta, Médico, Correo, Chat ID, Observaciones). El Apps Script mapea por posición, no por título — así puedes poner títulos bonitos en el Form sin romper el mapeo.

---

## Paso 4: Cómo obtener el `telegram_chat_id` de cada médico

Cada médico debe obtener su chat ID de Telegram **una sola vez** y dártelo para que lo pongas en el Sheet (o lo ingresen ellos mismos en el Form).

### Método 1 (rápido, para el médico)

1. El médico abre Telegram y busca **@userinfobot**.
2. Le envía cualquier mensaje.
3. El bot responde con su chat ID (un número como `123456789`).
4. El médico te pasa ese número.

### Método 2 (vía tu bot de KAYLA)

1. Cada médico busca tu bot en Telegram y le envía `/start` (o cualquier mensaje).
2. Tú ejecutas en tu terminal:
   ```bash
   python backend/get_chat_id.py
   ```
3. El script lista los chat IDs de quienes le escribieron al bot.
4. Copias el chat ID al campo `telegram_chat_id` del Sheet para ese médico.

---

## Paso 5: Compartir el Form con los médicos

1. En el Form, botón **Send (Enviar)**.
2. Copia el link.
3. Compártelo con los médicos por WhatsApp, correo o grupos de Telegram.
4. Los médicos **no necesitan cuenta de Google** para llenarlo (a menos que actives "Collect email addresses").

> **Seguridad:** el link del Form es público por defecto. Si quieres restringirlo a médicos específicos, activa "Restrict to users in [tu dominio]" o requerir inicio de sesión. Para el MVP, un link público es suficiente.

---

## Flujo completo después de esta configuración

```
Médico llena Google Form
        ↓
Respuesta cae como fila nueva en Google Sheet (hoja "Pacientes")
        ↓
GitHub Actions corre el scheduler cada mañana
        ↓
Script Python lee el Sheet, filtra por fecha, agrupa por médico
        ↓
Cada médico recibe SUS recordatorios en SU chat de Telegram
```
