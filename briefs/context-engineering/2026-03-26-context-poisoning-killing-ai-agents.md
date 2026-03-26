# Context Poisoning Is Killing Your AI Agents: How to Stop It

- **Fuente:** [https://www.youtube.com/watch?v=tYJmgpIEd-Y](https://www.youtube.com/watch?v=tYJmgpIEd-Y)
- **Canal:** The Chain of Thought Podcast
- **Categoría:** context-engineering
- **Duración:** 44min
- **Fecha:** 2026-03-25
- **Score OPENLAB Radar:** 7.2
  - Aplicabilidad: 7
  - Novedad: 7
  - Calidad: 8

---

## Resumen ejecutivo

Episodio de podcast con Michel Tricot, co-fundador de Airbyte (plataforma de integración de datos open source, $1.5B de valoración, 600+ conectores). Tricot introduce y explica el concepto de "context poisoning": el fenómeno por el cual el contexto acumulado durante una sesión larga de agente corrompe progresivamente su comportamiento, degradando la calidad de outputs sin que el usuario sea consciente. El vídeo propone formas de detectarlo y mitigarlo. *Nota: análisis basado en título y descripción; transcript no disponible en este ciclo.*

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** El diseño de skills de larga duración (due diligence, inteligencia de mercado, onboarding de procesos complejos) en OPENLAB debe considerar el context poisoning como un riesgo real. Las skills que operan en sesiones extendidas necesitan mecanismos de limpieza y reset de contexto para mantener fiabilidad.
- **Referencias que conectan:** Conecta directamente con los principios de context engineering que OPENLAB practica. El riesgo no es solo "el contexto se llena" (problema de tamaño) sino "el contexto se envenena" (problema de calidad) — una distinción importante para el diseño de skills.
- **Capacidades de plataforma:** El CLAUDE.md y la estructura de skills de OPENLAB pueden incorporar mecanismos de "context reset" o "context hygiene" basados en los patrones que Tricot propone. Esto es un refinamiento del context engineering existente, no un cambio de paradigma.
- **Oportunidades nuevas:** Desarrollar una guía interna de OPENLAB sobre "Context Hygiene in Long-Running Skills" — cuándo hacer reset, cómo estructurar el contexto para minimizar la degradación, y cómo detectar context poisoning en producción. Podría ser un diferenciador en proyectos enterprise donde los agentes operan durante horas.
- **Argumento comercial:** "Los agentes de IA pueden degradarse silenciosamente en sesiones largas — en OPENLAB diseñamos skills con mecanismos de higiene de contexto para garantizar que el agente funciona igual en la hora 1 que en la hora 8."

---

## Contenido detallado

*Transcript no disponible. Análisis basado en título y descripción del vídeo.*

### Ideas y argumentos principales

**Context poisoning** (acuñación de Tricot): el contexto acumulado en una conversación larga con un agente no solo ocupa tokens — activamente "contamina" la capacidad del agente para razonar correctamente sobre nuevas entradas. El efecto es sutil: el agente sigue respondiendo, pero con sesgos y errores que se acumulan progresivamente.

Este fenómeno es especialmente relevante para:
- Agentes de análisis que procesan muchos documentos en secuencia
- Due diligence automatizada donde el agente lee cientos de páginas
- Pipelines de contenido donde el agente genera texto durante horas
- Workflows de investigación de mercado con múltiples iteraciones

La credibilidad del speaker es alta: Michel Tricot co-fundó Airbyte, que resolvió problemas de integración de datos a escala masiva ($1.5B valoración). Su experiencia con sistemas que procesan datos en volumen a lo largo del tiempo le da perspectiva real sobre degradación en producción.

### Datos y evidencia

- Airbyte: $1.5B valoración, 600+ conectores open source
- Michel Tricot: co-fundador de Airbyte, experiencia en sistemas de datos en producción a escala
- Sin datos cuantitativos sobre context poisoning disponibles sin transcript

### Citas textuales

Sin transcript disponible. Ver vídeo en: https://www.youtube.com/watch?v=tYJmgpIEd-Y

### Ejemplos concretos

- Airbyte como sistema de datos a escala: analogía con gestión de contexto en agentes
- Podcast "Chain of Thought": formato de entrevista de 44min con profundidad técnica

---

## Temas clave

### 1. Context poisoning como riesgo silencioso en producción
El fenómeno que Tricot describe es diferente del problema de "context window llena" (que da error explícito). Context poisoning es silencioso: el agente sigue funcionando, pero sus outputs se degradan sin señal visible. Para OPENLAB, esto implica que las skills de larga duración necesitan mecanismos de monitorización activa, no solo de tamaño.

### 2. Higiene de contexto como práctica de ingeniería
La solución al context poisoning no es solo reiniciar conversaciones — es diseñar la estructura del contexto para que la información vieja no contamine el razonamiento nuevo. Esto puede implicar: resúmenes periódicos, segmentación del contexto, o arquitecturas de multi-sesión con estado persistente controlado.

### 3. Experiencia en sistemas de datos como analogía para sistemas agénticos
La experiencia de Tricot en Airbyte (datos en flujo continuo, degradación de calidad en pipelines) es directamente transferible a agentes de larga duración. Los principios de data quality en pipelines (detección de anomalías, checkpoints, validación incremental) tienen equivalentes en context engineering para agentes.


**Telegraph:** https://telegra.ph/Context-Poisoning-Is-Killing-Your-AI-Agents-How-to-Stop-It-03-26
