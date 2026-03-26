# Oh My Claude Code: Multi-Agent Orchestration with Zero Learning Curve

- **Fuente:** [https://www.youtube.com/watch?v=VOjZ8Htv9NU](https://www.youtube.com/watch?v=VOjZ8Htv9NU)
- **Canal:** Prism Labs
- **Categoría:** agentic-systems
- **Duración:** 5min
- **Fecha:** 2026-03-25
- **Score OPENLAB Radar:** 7.3
  - Aplicabilidad: 7
  - Novedad: 8
  - Calidad: 7

---

## Resumen ejecutivo

Oh My Claude Code (OMC) es un plugin de Claude Code con 11.4k+ estrellas en GitHub que transforma el CLI en una plataforma de orquestación multi-agente: 32 agentes especializados, 6 modos de orquestación, routing inteligente de modelos (Haiku para tareas simples, Opus para razonamiento complejo), cost tracking, y un HUD en tiempo real. Se instala con 2 comandos sin configuración adicional.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** OMC añade orquestación multi-agente sobre el stack base de Claude Code CLI que OPENLAB usa. Si OPENLAB necesita coordinar múltiples skills en proyectos complejos, OMC puede ser una capa de orchestration lista sin construirla desde cero.
- **Referencias que conectan:** Los 32 agentes especializados de OMC (architecture, research, design, testing, data science) son equivalentes conceptuales a skills de OPENLAB para distintas fases de un proyecto agéntico multi-fase.
- **Capacidades de plataforma:** El routing automático entre Haiku y Opus es relevante para gestión de costes en proyectos OPENLAB: tareas de extracción/formateo → Haiku; razonamiento complejo → Opus. OMC lo resuelve automáticamente.
- **Oportunidades nuevas:** Evaluar si OMC puede ser la capa de orquestación en deployments enterprise de OPENLAB, en lugar de construir la lógica de coordinación dentro de las propias skills. Potencial ahorro de tiempo de diseño.
- **Argumento comercial:** "El ecosistema de Claude Code tiene plugins enterprise con 11k+ usuarios activos que añaden orquestación multi-agente, routing de coste y control desde Telegram — nuestro stack se beneficia directamente de este crecimiento."

---

## Contenido detallado

### Ideas y argumentos principales

OMC parte de una crítica implícita a la curva de aprendizaje de Claude Code para orquestación multi-agente: en lugar de que el usuario estructure prompts, gestione el contexto y encadene tareas, OMC analiza la necesidad, enruta al agente correcto y coordina la ejecución automáticamente.

El "pitch" del plugin es directo: "Don't learn Claude Code, just use OMC." — una propuesta de valor de abstracción sobre complejidad que tiene resonancias con el modelo de OPENLAB (skills que abstraen complejidad para que el usuario de negocio solo necesite describir su intención).

Los 6 modos de orquestación permiten configurar cómo se distribuye el trabajo entre agentes. La integración con Codeex, Gemini, Telegram, Discord, Slack y OpenClaw convierte a OMC en un hub de coordinación cross-model.

### Datos y evidencia
- 11,400+ estrellas en GitHub (al momento del vídeo: 11.4k en descripción, el transcript menciona "11,000 stars")
- 32 agentes especializados preconfigurados
- 6 modos de orquestación
- Smart model routing: Haiku (simple) → Opus (complejo)
- Instalación: 2 comandos, 0 configuración adicional
- Integraciones: Codeex, Gemini, Telegram, Discord, Slack, OpenClaw

### Citas textuales

> "Don't learn Claude Code, just use OMC." — Pitch del plugin

> "11,000 stars, 32 specialized agents, six orchestration modes, smart model routing that sends simple tasks to Haiku, and complex reasoning to Opus, cost tracking, rate limit auto detection, session resumption, and a real-time HUD showing exactly what every agent is doing." — Narrator

### Ejemplos concretos
- Plugin TypeScript que corre como claude code plugin
- Repo con documentación exhaustiva: modo de orquestación, roster de agentes, features
- HUD en tiempo real mostrando estado de cada agente
- Integración nativa con OpenClaw para trabajo cross-model

---

## Temas clave

### 1. Orquestación multi-agente como plugin, no como framework
OMC demuestra que la orquestación multi-agente no requiere LangChain, LangGraph ni frameworks propietarios. Un plugin de Claude Code con routing automático y 32 agentes especializados resuelve el problema con zero lock-in adicional. Este es un argumento directo en el debate CLI agents vs plataformas.

### 2. Routing automático por coste/complejidad
El routing inteligente Haiku/Opus es un patrón de optimización de costes que OPENLAB debería incorporar en sus arquitecturas multi-skill: no toda tarea requiere el modelo más potente. OMC lo automatiza; OPENLAB puede replicarlo en sus harnesses.

### 3. El ecosistema de plugins como ventaja competitiva del stack CLI
Con 11k+ estrellas, OMC muestra que hay un ecosistema activo de plugins que extienden Claude Code sin romper el modelo de zero lock-in. Esto refuerza la apuesta de OPENLAB por Claude Code CLI como plataforma: el ecosistema crece, el stack mejora sin cambiar.


**Telegraph:** https://telegra.ph/Oh-My-Claude-Code-Multi-Agent-Orchestration-with-Zero-Learning-Curve-03-26
