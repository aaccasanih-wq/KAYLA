# Evidencia 01 — Entrevista con médico de posta (Lima)

**Fecha:** 15 de junio, 2026
**Entrevistado:** Médico de posta de primer nivel, MINSA (Lima Este)
**Relación:** Hermano del founder
**Duración:** ~30 minutos (conversación informal, notas retrospectivas)

---

## Contexto

El entrevistado trabaja como médico en una posta de primer nivel de salud en Lima Este.
Atiende a pacientes crónicos (hipertensos y diabéticos) que deben recoger medicamentos
mensualmente y asistir a controles.

---

## Preguntas y respuestas clave

### ¿Cómo gestionan actualmente los recordatorios a pacientes crónicos?

> "Llevamos un Excel con los pacientes. Cada mes, cuando llega la fecha de recojo,
> llamamos uno por uno. Hay días que pierdo una hora llamando. Muchos no
> contestan, otros dicen que van a ir y no van."

### ¿Qué porcentaje de pacientes recoge sus medicamentos a tiempo?

> "Yo diría que como un 40% no viene. Es una estimación mía, pero calza con lo que
> he leído de la ENDES. Hay pacientes que ya conoces, sabes que no van a ir.
> Pero igual tienes que llamarlos porque sino te bajan el indicador."

### ¿Qué pasa si no cumplen las métricas de la Diris?

> "Si no llegamos a la meta de pacientes controlados, nos descuentan puntos.
> Y si la posta queda mal evaluada, puede perder recursos. Es presión constante."

### ¿Usan algún sistema del MINSA para gestionar esto?

> "Hay un sistema, pero es complicado. Para los pacientes crónicos lo gestionamos
> más con Excel porque es más rápido. El sistema del MINSA es para reportar, no
> para recordar."

### ¿Te serviría un sistema que te envíe un mensaje cada mañana con los pacientes que debes llamar?

> "Si me llegara un mensaje cada mañana con los pacientes que debo llamar, me
> ahorraría una hora. Yo ya tendría la lista lista, solo llamar."

### ¿Tienen acceso a internet y smartphones en la posta?

> "Sí, tenemos internet. Y todo el personal de la posta tiene celular. Usamos
> WhatsApp para todo, también Telegram con algunos colegas."

---

## Insights para el producto

1. **El dolor es real y medible:** ~40% de no adherencia (estimación de campo consistente con ENDES 2022: 39.7% nacional), pérdida de hasta una hora al día en llamadas.
2. **Excel es la herramienta real:** los sistemas del MINSA no se usan para gestión diaria.
3. **Telegram/WhatsApp son viables:** el personal ya usa smartphones y mensajería.
4. **El insight clave:** "si me llegara un mensaje cada mañana, me ahorraría una hora" —
   valida la propuesta de KAYLA de enviar recordatorios agrupados al médico.

---

## Próximos pasos

- Esta posta fue seleccionada como la primera posta en pilotaje del MVP.
- Se configuró el Google Sheet con datos de pacientes reales (anonimizados para el repo).
- Se configuró el bot de Telegram para enviar recordatorios al médico.
