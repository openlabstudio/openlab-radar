# Supercharging AI agents with evaluations

- **Fuente:** [https://www.youtube.com/watch?v=GLwy1TCmGDA](https://www.youtube.com/watch?v=GLwy1TCmGDA)
- **Canal:** Voxel51
- **Categoría:** agentic-systems
- **Duración:** 39min
- **Fecha:** 2026-03-23
- **Score OPENLAB Radar:** 7.0
  - Aplicabilidad: 7
  - Novedad: 7
  - Calidad: 7

---

## Resumen ejecutivo

Talk sobre la importancia de evaluar agentes IA de forma rigurosa antes y durante el deployment en producción. Argumenta que la evaluación debe pasar de ser un paso de QA opcional a un componente central del ciclo de vida del agente. Cubre métricas de evaluación, frameworks de testing y patrones para monitorizar agentes en producción.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** Aplicable al workflow del agente **Quinn (QA)** del catálogo OAF y al pipeline `qa-generate-e2e-tests`. También relevante para la fase de **piloto + iteración** de cualquier proyecto OPENLAB (semanas 5-7), donde se necesita medir si el agente produce outputs de calidad consistente.
- **Referencias que conectan:** El **Market Due Diligence** incluye auto-evaluación en su fase final. Los patrones de evaluación del vídeo podrían formalizarse como un checklist estándar para la entrega de cualquier skill OPENLAB.
- **Capacidades de plataforma:** Claude Code CLI permite ejecución de tests (Bash/Python). Se podrían crear scripts de evaluación que corran automáticamente post-ejecución de un skill y alerten si la calidad baja de un umbral.
- **Oportunidades nuevas:** Definir un **estándar de evaluación OPENLAB** para skills entregados: métricas de calidad, tests de regresión, y monitorización post-entrega. Esto reforzaría la propuesta de valor "95-100% de calidad" con evidencia medible.
- **Argumento comercial:** "No solo construimos el agente — lo evaluamos con métricas objetivas y te dejamos los tests para que puedas verificar la calidad vosotros mismos."

---

## Contenido detallado

### Ideas y argumentos principales

**La evaluación de agentes es fundamentalmente diferente a la evaluación de sistemas de IA anteriores.** Los sistemas no-agénticos tienen entrada, salida y lógica de puntuación lineal. Los agentes invocan múltiples herramientas, modifican el estado del entorno y se adaptan en función de resultados intermedios. Los errores se componen: un fallo en el paso 10 puede descarrilar los 190 pasos siguientes.

**El "problema de volar a ciegas" (flying blind problem).** Sin una suite de evaluación automatizada, los equipos dependen del dogtfooding manual y el "vibing". Esto no escala: cada comportamiento inesperado se parchea ad hoc en el prompt, pero aparece otro, y el proceso es insostenible en equipos que quieren iterar rápido hacia producción.

**La paradoja de la evaluación de agentes.** Las mismas capacidades que hacen útil a un agente (autonomía, inteligencia, capacidad de encontrar soluciones novedosas) son exactamente las que hacen que sea una pesadilla evaluarlo con criterios estáticos. El ejemplo del vuelo de Opus 4.5: el agente encontró un atajo por el backend y reservó el vuelo sin seguir el flujo de clics esperado, consiguiendo el resultado perfecto para el usuario pero fallando según el grader, que evaluaba pasos específicos.

**Evaluaciones de capacidad vs. evaluaciones de regresión.** Las primeras miden qué puede hacer el agente (se mejoran con el tiempo hasta alcanzar un umbral de calidad). Las segundas se ejecutan cada vez que se actualiza el agente para detectar si retrocede en algo que antes hacía bien. La diferencia es conceptual pero crítica para el ciclo de vida del agente.

**La métrica pass@K vs. pass^K.** Pass@K mide si el agente acierta en al menos uno de K intentos. Pass^K (pass elevado a K) mide si acierta en todos los intentos. Con un 75% de tasa de éxito por intento, tres ejecuciones encadenadas dan solo un 42% de fiabilidad global. Para aplicaciones financieras o médicas, ese 42% es inaceptable.

**Las evaluaciones como acelerador competitivo, no como freno.** Un equipo sin suite de evaluación tarda semanas en validar un nuevo modelo. Un equipo con suite automatizada puede cambiar las claves de API, correr los tests en un fin de semana, ajustar prompts donde el nuevo modelo falla y hacer el upgrade en días.

**El modelo del queso suizo para la calidad.** Tres capas de evaluación apiladas: (1) suite de evals automatizados que establece la línea base y detecta regresiones antes del despliegue; (2) revisión manual de transcripts en producción (últimas horas); (3) monitorización en producción y feedback de usuario (última semana). Si una capa tiene un agujero, las otras lo capturan.

**Hoja de ruta práctica para construir evals robustos:**
- Empezar pronto y pequeño: 20-30 escenarios reales antes de construir el agente.
- Escribir la "descripción del trabajo" del agente (qué debe y no debe hacer).
- Usar bugs de QA y tickets de soporte para convertirlos en casos de test, priorizados por impacto al usuario.
- Incluir ejemplos negativos: no solo cuándo el agente debe responder, sino cómo NO debe responder.
- Cada instrucción de prompt debe tener un test asociado que valide que el LLM la sigue.
- Evitar premiar en exceso el uso de herramientas específicas: el agente aprenderá a abusar de ellas aunque no sean necesarias.

### Datos y evidencia

- **75%** de tasa de éxito por intento es el umbral habitual en la industria para considerar que un agente funciona bien.
- Tres ejecuciones encadenadas con 75% de éxito individual resultan en un **42%** de fiabilidad compuesta, lo cual es inaceptable para producción en dominios críticos.
- Anthropic publicó resultados con **Opus 4.5** en un benchmark de reserva de vuelos donde el agente descubrió un atajo por el backend, superando al grader basado en pasos discretos.
- La speaker menciona haber desplegado "varios" agentes agénticos en Intuit para TurboTax y otras aplicaciones financieras con "cientos de miles o millones de clientes".

### Citas textuales (2-4 máx)

> "The exact capabilities that make an agent so incredibly useful — their autonomy, their intelligence, their ability to find novel solutions — those are the exact same traits that make it a total nightmare to evaluate." — Priya Wenat

> "There are things that can happen in production environment that you have never seen in your testing environment before." — Priya Wenat

> "If you write a prompt, you also have to write a test to validate that that prompt instruction is actually being followed by the LLM." — Priya Wenat

> "It may feel slow in week one but in my experience it's the ultimate accelerator for development and model adoption." — Priya Wenat

### Ejemplos concretos

- **Caso Opus 4.5 (Anthropic):** Benchmark de reserva de vuelos en el que el agente encontró un atajo por el backend de la aerolínea, ignorando el flujo de clics de la UI. El grader (basado en verificación de pasos) lo marcó como fallo aunque el resultado para el usuario era correcto. Citado por la speaker a partir de un blog público de Anthropic.
- **Intuit / TurboTax:** La speaker trabaja como Senior Manager of AI en Intuit. Sus equipos han desplegado múltiples aplicaciones agénticas para TurboTax y otras aplicaciones financieras, con clientes de pago. No se mencionan repos ni URLs específicos.
- **Ejemplo de agente de calendario:** Usado como caso ilustrativo para capability evals (enviar invitaciones, detectar disponibilidad, proponer horarios).
- **Ejemplo de agente de reembolsos:** Usado para ilustrar el concepto de "outcome" en evaluación agéntica: ¿el reembolso se procesó realmente?

---

## Temas clave

### 1. Evaluación como componente central, no como paso final
El vídeo argumenta que evaluar un agente después de construirlo es demasiado tarde. La evaluación debe guiar el diseño: primero defines qué es un "buen output", luego construyes el agente para que lo produzca.

### 2. Métricas para agentes IA
Propone métricas específicas: completitud del output, adherencia a instrucciones, ausencia de alucinaciones, consistencia entre ejecuciones. Estas métricas son directamente aplicables a la validación de skills OPENLAB.

### 3. Monitorización en producción
Patrones para detectar cuando un agente degrada en calidad (data drift, cambios en fuentes, evolución del modelo). Relevante para el servicio de mantenimiento post-entrega de OPENLAB.


**Telegraph:** https://telegra.ph/Automate-Your-Business-with-AI-OpenClaw-Sub-Agents-03-26
