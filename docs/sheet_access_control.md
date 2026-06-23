# Control de acceso al Google Sheet

El Google Sheet contiene datos sensibles (DNI, celulares, diagnósticos). Esta guía define quién puede verlo y editarlo, y cómo configurarlo.

---

## Modelo de acceso

| Actor | Permiso | Cómo accede |
|-------|---------|-------------|
| **Propietaria (tú)** | Editor | Invitación por correo desde Google Sheets |
| **Service account de KAYLA** | Editor | Email `*.iam.gserviceaccount.com` compartido |
| **Google Form** | Editor (hereda tus permisos) | Las respuestas se escriben en el Sheet con tu cuenta |
| **Médicos** | **Sin acceso** | Solo llenan el Google Form |
| **Cualquier otra persona** | **Sin acceso** | El Sheet no es público |

---

## Configuración paso a paso

### 1. Asegurar que el Sheet sea privado

1. Abre tu Google Sheet en [sheets.google.com](https://sheets.google.com).
2. Botón **Share (Compartir)** (arriba a la derecha).
3. En **General access**, selecciona **"Restricted"** (Solo las personas añadidas).
   - Si ahora dice "Anyone with the link", cámbialo a **Restricted**.
4. Verifica que no haya personas no autorizadas en la lista.

### 2. Compartir con la service account

1. En el mismo diálogo de **Share**, pega el email de tu service account.
   - Lo encuentras en `credentials.json`, campo `client_email`.
   - Se ve así: `kayla@tu-proyecto.iam.gserviceaccount.com`.
2. Permiso: **Editor**.
3. **Send** (Enviar).

> Si ya hiciste esto en la Etapa 2, no necesitas repetirlo. Verifica que el email siga en la lista.

### 3. Verificar que los médicos NO tienen acceso

- En el diálogo de **Share**, **no debe haber** médicos ni correos de postas.
- El link del Sheet **no debe compartirse** con nadie.
- Los médicos solo reciben el link del **Google Form** (ver `google_form_setup.md`).

### 4. Opcional: proteger columnas o hojas

Si quieres evitar que tú misma edites accidentalmente columnas clave:

1. En el Sheet: **Data → Protect sheets and ranges**.
2. Selecciona columnas como `dni` o `estado`.
3. Configura permisos de edición restringidos.

Para el MVP esto no es necesario, pero es buena práctica.

---

## Qué pasa si alguien llena el Google Form

```
Persona llena el Form
      ↓
Google Forms escribe la fila en el Sheet usando TUS permisos (no los del médico)
      ↓
La fila aparece en la hoja "Pacientes"
      ↓
KAYLA lee la fila en el próximo run del scheduler
```

El médico nunca ve el Sheet. Solo llena el Form. El Sheet es tuyo y de la service account.

---

## Verificación de seguridad

Después de configurar:

- **Abre el link del Sheet en una ventana de incógnito** (sin sesión de Google). Debe pedir login o mostrar "You need permission". Si puedes verlo sin login, el Sheet está público — vuelve al paso 1.
- **Verifica que el service account tiene acceso** ejecutando `python backend/test_connection.py`. Debe conectar sin error.
- **Revisa los permisos** una vez al mes por si añadiste a alguien por error.
