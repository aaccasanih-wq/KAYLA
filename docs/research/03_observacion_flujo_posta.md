# Evidencia 03 — Observación de flujo de trabajo en posta

**Fecha:** 16 de junio, 2026
**Lugar:** Posta de primer nivel, Lima Este
**Observador:** Founder (Axel Ccasani)
**Duración:** 1 día de observación

---

## Objetivo

Observar el flujo de trabajo real del personal de salud en el seguimiento de
pacientes crónicos, para validar las hipótesis del problema y el diseño de KAYLA.

---

## Observaciones

### Herramientas usadas

- **Computadora de la posta:** Windows 7, con acceso a internet. Navegador Chrome.
- **Software de gestión:** sistema del MINSA instalado, pero solo se usa para
  reportar mensualmente. Para gestión diaria, usan Excel/Google Sheets.
- **Comunicación:** WhatsApp personal del técnico para coordinar con pacientes
  que sí tienen WhatsApp. Llamadas para los que no.
- **Telegram:** no se usa actualmente en la posta, pero el técnico lo tiene
  instalado en su celular personal.

### Flujo de seguimiento de pacientes crónicos

1. El técnico abre un Excel compartido en Google Drive (accesible desde su celular).
2. Filtra por mes actual y revisa las fechas de recojo de medicamentos.
3. Anota en un papel los nombres y teléfonos de los pacientes que debe llamar.
4. Pasa la mañana llamando (unas 3-4 horas en total, distribuidas en la semana).
5. Marca en el Excel quién confirmó, quién no contestó, quién dijo que iría.
6. Al final del mes, genera un reporte manual para la Diris.

### Puntos de dolor observados

- **Filtrado manual:** el técnico pierde 15-20 minutos cada mañana filtrando el Excel.
- **Llamadas fallidas:** muchos pacientes no contestan. El técnico tiene que volver
  a llamar días después, sin un sistema de seguimiento de intentos.
- **Papel y lápiz:** la lista de llamados se hace en papel, se pierde, no hay historial.
- **Reporte mensual:** el reporte para la Diris se arma manualmente a partir del Excel,
  perdiendo 2-3 horas al final del mes.
- **Sin métricas en tiempo real:** no saben qué porcentaje de pacientes ha recogido
  hasta que cierran el mes.

### Insight crítico para KAYLA

> El sistema no necesita ser sofisticado. Necesita hacer **una cosa bien**: decirle
> al médico/técnico a quién llamar hoy, con los datos del paciente a mano.
> El dashboard con métricas es valor agregado, pero el recordatorio es el núcleo.

---

## Validación de hipótesis

| Hipótesis | Estado | Evidencia |
|-----------|--------|-----------|
| Las postas usan Excel/Sheets para gestión | Confirmado | Excel compartido en Google Drive |
| El personal pierde horas llamando manualmente | Confirmado | 3-4 horas/semana en llamadas |
| No hay sistema de recordatorios | Confirmado | Papel y lápiz para la lista |
| El personal tiene smartphone con internet | Confirmado | WhatsApp y Telegram en celular personal |
| El reporte a la Diris es un dolor adicional | Confirmado | 2-3 horas al final del mes |

---

## Próximos pasos

- El flujo observado se usó para diseñar el formato del mensaje de Telegram de KAYLA:
  debe incluir nombre, diagnóstico, fecha, celular y posta del paciente.
- La sección de reporte mensual del plan Pro se validó como necesidad real.
