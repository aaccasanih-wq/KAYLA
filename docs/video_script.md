# Guion del Video Demo — KAYLA

**Duración estimada:** 2:30 - 3:00 minutos
**Formato:** Screencast (grabación de pantalla) + voz en off
**Herramienta sugerida:** Loom, OBS Studio o QuickTime Player (macOS)

---

## Preparación antes de grabar

1. Tener abiertas estas pestañas en el navegador:
   - Landing page: `https://aaccasanih-wq.github.io/KAYLA/`
   - Dashboard Streamlit: `https://kayla2026.streamlit.app`
   - Repositorio GitHub: `https://github.com/aaccasanih-wq/KAYLA`
   - Telegram (mostrar el chat con el bot)
2. Tener el Google Sheet de pacientes abierto con datos de ejemplo.
3. Preparar un paciente con fecha de recojo "mañana" para que aparezca en el recordatorio.
4. Probar el envío manual del recordatorio una vez antes de grabar.

---

## Guion

### [0:00 - 0:20] Introducción

**Pantalla:** Landing page (hero section)

**Voz en off:**
> "KAYLA es un sistema que automatiza los recordatorios de medicamentos y controles médicos para pacientes crónicos en postas de salud del Perú. El problema: según la ENDES 2022, casi el 40% de los pacientes hipertensos no se adhiere al tratamiento, y los médicos pierden horas llamándolos manualmente."

### [0:20 - 0:45] El problema

**Pantalla:** Scroll por la sección "Problema" de la landing (las 3 tarjetas: ~40% no se adhiere, horas perdidas, recursos en riesgo)

**Voz en off:**
> "Las postas de primer nivel del MINSA gestionan pacientes hipertensos y diabéticos con Excel y llamadas manuales. Si no cumplen las métricas de la Diris, la posta pierde recursos. No tienen presupuesto para software de gestión, pero sí usan Google Sheets y Telegram."

### [0:45 - 1:15] La solución — flujo completo

**Pantalla:** Sección "Solución" de la landing (4 pasos numerados)

**Voz en off:**
> "La solución funciona con lo que ya usan. Primero, el médico registra pacientes en un Google Form vinculado al Google Sheet. Segundo, cada mañana a las 8, GitHub Actions revisa quién tiene recojo o control en los próximos 2 días. Tercero, cada médico recibe en su propio chat de Telegram solo los recordatorios de los pacientes a su cargo. Cuarto, contacta al paciente y confirma."

### [1:15 - 1:45] Demo del dashboard

**Pantalla:** Cambiar al dashboard de Streamlit

**Voz en off:**
> "Este es el dashboard. Arriba vemos las métricas clave: total de pacientes, pacientes activos, número de postas y médicos registrados. En la sección de recordatorios próximos, podemos ajustar la ventana de días y la fecha de referencia. Aquí se muestran los recordatorios pendientes, agrupados por médico a cargo, con el formato exacto del mensaje que se envía por Telegram. Más abajo, en la base de pacientes, podemos filtrar por posta, por médico o por estado, y ver todos los datos en una tabla. También hay un gráfico de distribución por diagnóstico y una tabla de próximos eventos con las fechas de recojo y control."

**Acción en pantalla:** Mostrar las 4 métricas arriba, hacer scroll por los recordatorios agrupados por médico, bajar a la base de pacientes y usar los 3 filtros (posta, médico, estado), mostrar el gráfico de barras y la tabla de próximos eventos.

### [1:45 - 2:10] Demo del mensaje de Telegram

**Pantalla:** Cambiar a Telegram, mostrar el chat con el bot

**Voz en off:**
> "Así se ve el mensaje que recibe el médico cada mañana. Cada médico recibe solo los recordatorios de sus propios pacientes, en su chat de Telegram. El mensaje tiene el nombre del paciente, diagnóstico, fecha de recojo, celular y posta. Con esta información, el médico sabe exactamente a quién llamar y por qué."

**Acción en pantalla:** Mostrar el mensaje de Telegram con formato Markdown. Si hay dos médicos, mostrar que cada uno recibe un mensaje diferente con solo sus pacientes.

### [2:10 - 2:30] Arquitectura y tecnología

**Pantalla:** Cambiar al repositorio GitHub, mostrar la estructura y luego el diagrama de arquitectura

**Voz en off:**
> "El sistema está construido con Python, la API de Google Sheets con gspread, la API de Telegram, y Streamlit para el dashboard. El scheduler corre en GitHub Actions de forma gratuita, y el CI corre tests automáticos en cada push. Todo el código está en el repositorio."

### [2:30 - 2:50] Cierre y llamada a la acción

**Pantalla:** Volver a la landing page, sección de pricing o CTA final

**Voz en off:**
> "KAYLA es gratis para una posta con hasta 50 pacientes. El plan Pro, con dashboard y reportes para la Diris, cuesta S/49 al mes. El costo variable por usuario es cero: Telegram, Google Sheets y GitHub Actions son gratuitos. Si gestionas una posta con pacientes crónicos, pruébalo hoy."

**Pantalla final:** Logo de KAYLA + URLs:
- `aaccasanih-wq.github.io/KAYLA`
- `github.com/aaccasanih-wq/KAYLA`

---

## Notas para la grabación

- Habla claro y a ritmo normal. No aceleres.
- Si te equivocas, pausa y repite la sección. Puedes editar después.
- El video no necesita tu cara, solo la pantalla y tu voz.
- Si usas Loom, puedes grabar directamente desde el navegador.
- Sube el video a YouTube como "No listado" o a Loom y pon el link en el README.
