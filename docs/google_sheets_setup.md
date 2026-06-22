# Configuración de Google Sheets

Esta guía describe cómo configurar Google Cloud Console y un Google Sheet para que KAYLA pueda leer y escribir datos de pacientes.

---

## 1. Crear un proyecto en Google Cloud Console

1. Ir a [Google Cloud Console](https://console.cloud.google.com/).
2. Click en el selector de proyectos (arriba a la izquierda) → **New Project**.
3. Nombre del proyecto: `kayla-sheets` (o el que prefieras).
4. Click **Create**.

## 2. Habilitar las APIs necesarias

1. En el proyecto creado, ir a **APIs & Services → Library**.
2. Buscar y habilitar:
   - **Google Sheets API**
   - **Google Drive API**

## 3. Crear una Service Account

1. Ir a **APIs & Services → Credentials**.
2. Click **Create Credentials → Service account**.
3. Nombre: `kayla-service-account`.
4. Click **Create and Continue → Done** (no es necesario asignar roles).
5. En la lista de service accounts, click sobre la creada.
6. Ir a la pestaña **Keys** → **Add Key → Create new key**.
7. Seleccionar **JSON** → **Create**.
8. Se descargará un archivo JSON. **Renombrarlo a `credentials.json`** y colocarlo en la raíz del proyecto.

> **IMPORTANTE:** `credentials.json` está en `.gitignore` y **nunca** debe subirse al repositorio.

## 4. Crear el Google Sheet

1. Ir a [Google Sheets](https://sheets.google.com) y crear una nueva hoja.
2. Nombrarla `KAYLA - Base de Pacientes` (o similar).
3. Renombrar la primera hoja (worksheet) a `Pacientes`.
4. Copiar el **Spreadsheet ID** desde la URL:
   ```
   https://docs.google.com/spreadsheets/d/ESTE_ES_EL_SPREADSHEET_ID/edit
                                              ^^^^^^^^^^^^^^^^^^^^^^^^
   ```

## 5. Compartir el Sheet con la Service Account

1. Abrir el archivo `credentials.json` descargado y buscar el campo `client_email`:
   ```json
   "client_email": "kayla-service-account@kayla-sheets.iam.gserviceaccount.com"
   ```
2. En el Google Sheet, click **Share** (arriba a la derecha).
3. Pegar el `client_email` y asignar rol **Editor**.
4. Desmarcar "Notify people" → **Share**.

## 6. Configurar variables de entorno

1. Copiar `.env.example` a `.env` (en la raíz del proyecto):
   ```bash
   cp .env.example .env
   ```
2. Editar `.env` con los valores reales:
   ```
   GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
   GOOGLE_SHEETS_SPREADSHEET_ID=<pegar_el_spreadsheet_id_del_paso_4>
   TELEGRAM_BOT_TOKEN=tu_token_aqui
   TELEGRAM_CHAT_ID_MEDICO=tu_chat_id_aqui
   ```

## 7. Probar la conexión

Con el entorno virtual activo y las dependencias instaladas:

```bash
pip install -r requirements.txt
python backend/test_connection.py
```

Salida esperada:
```
Probando conexión con Google Sheets...

  Credenciales cargadas desde: credentials.json
  Spreadsheet ID: <tu_id>
  Spreadsheet abierto: KAYLA - Base de Pacientes
  Hojas disponibles: ['Pacientes']
  Registros en 'Pacientes': 0

  Conexión exitosa con Google Sheets.
```

---

## Estructura del Sheet (se define en la Etapa 3)

El schema completo de columnas se documenta en `data/schema.md` y se implementa en `backend/models.py`.
