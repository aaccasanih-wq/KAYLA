# Configuración del Bot de Telegram

Esta guía describe cómo crear un bot de Telegram y obtener el `chat_id` para enviar recordatorios.

---

## 1. Crear el bot con BotFather

1. Abrir Telegram y buscar [@BotFather](https://t.me/BotFather).
2. Enviar `/newbot`.
3. Elegir un **nombre** para el bot (ej. `KAYLA SaludCronic`).
4. Elegir un **username** único que termine en `bot` (ej. `kayla_saludcronic_bot`).
5. BotFather responderá con un **token** similar a:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
6. **Copiar el token** (no compartirlo públicamente).

## 2. Obtener el chat_id

Para que el bot pueda enviar mensajes, necesitas el `chat_id` de quien recibirá los recordatorios (el médico/técnico).

### Opción A: Usar @userinfobot (rápido)

1. Buscar [@userinfobot](https://t.me/userinfobot) en Telegram.
2. Enviar `/start`.
3. El bot responderá con tu `Id` (ese es tu `chat_id`).

### Opción B: Usar getUpdates (manual)

1. Enviar cualquier mensaje al bot creado en el paso 1 (ej. "hola").
2. En el navegador, abrir:
   ```
   https://api.telegram.org/bot<TU_TOKEN>/getUpdates
   ```
3. En la respuesta JSON, buscar:
   ```json
   "chat": {
     "id": 123456789,   // <-- este es el chat_id
     "first_name": "Axel",
     "type": "private"
   }
   ```

> **Nota:** El `chat_id` es un número (puede ser negativo para grupos).

## 3. Configurar variables de entorno

Agregar al archivo `.env` (en la raíz del proyecto):

```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID_MEDICO=123456789
```

> **IMPORTANTE:** Nunca subir `.env` al repositorio. Ya está en `.gitignore`.

## 4. Probar la conexión

Con el entorno virtual activo y las dependencias instaladas:

```bash
pip install -r requirements.txt
python backend/test_telegram.py
```

Salida esperada:
```
Probando conexión con Telegram Bot API...

  Token configurado: 12345678:wxyz
  Chat ID por defecto: 123456789

  Verificando token con getMe...
    Bot username: @kayla_saludcronic_bot
    Bot name: KAYLA SaludCronic
    Bot ID: 123456789

  Enviando mensaje de prueba...
    Mensaje enviado correctamente.
    Entregado a chat_id: 123456789

  Conexión exitosa con Telegram Bot API.
```

Y deberías recibir un mensaje en Telegram:
```
KAYLA - Mensaje de prueba
Si recibes este mensaje, la configuración del bot es correcta.
```

---

## 5. Para GitHub Actions (producción)

En el repo: **Settings → Secrets and variables → Actions → New repository secret**:

| Nombre del secret | Valor |
|-------------------|-------|
| `TELEGRAM_BOT_TOKEN` | Token del bot |
| `TELEGRAM_CHAT_ID_MEDICO` | Chat ID del médico |

Referenciar en `.github/workflows/scheduler.yml`:
```yaml
env:
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  TELEGRAM_CHAT_ID_MEDICO: ${{ secrets.TELEGRAM_CHAT_ID_MEDICO }}
```

---

## Notas

- El bot **no puede iniciar conversaciones** con usuarios que no le hayan escrito primero.
- Para grupos, agrega el bot al grupo y envíale un mensaje antes de usar `getUpdates`.
- Los mensajes de Telegram son **gratis** (sin costo por mensaje).
- El límite de la API es ~30 mensajes/segundo, suficiente para el volumen del MVP.
