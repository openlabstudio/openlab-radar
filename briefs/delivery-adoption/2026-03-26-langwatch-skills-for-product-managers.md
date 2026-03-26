# Claude Code, LangWatch Skills for Product Managers

- **Fuente:** [https://www.youtube.com/watch?v=6QsBzzFx_1k](https://www.youtube.com/watch?v=6QsBzzFx_1k)
- **Canal:** LangWatch
- **Categoría:** delivery-adoption (secundaria: enterprise-ai)
- **Duración:** 6min
- **Fecha:** 2026-03-25
- **Score OPENLAB Radar:** 7.5
  - Aplicabilidad: 8
  - Novedad: 7
  - Calidad: 7

---

## Resumen ejecutivo

Demostración de cómo un CEO o Product Manager puede usar Claude Code con un MCP server de LangWatch para definir en lenguaje natural el comportamiento de un AI agent y generar automáticamente más de 40 casos de test. Sin código, sin sprint planning, sin tickets de Jira. La tesis: las personas más cercanas a los usuarios ahora son quienes definen cómo se testean, mejoran y confían los sistemas de IA.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** Este vídeo es evidencia directa del valor de proposition de OPENLAB: skills en lenguaje natural que permiten a perfiles de negocio (PMs, CEOs) operar agentes sin depender de ingeniería. El modelo de delivery de OPENLAB (skills + context engineering) habilita exactamente lo que LangWatch demuestra aquí.
- **Referencias que conectan:** Conecta con cualquier proyecto OPENLAB en el que el cliente quiera autonomía post-entrega — este vídeo demuestra que esa autonomía es posible y real hoy.
- **Capacidades de plataforma:** El MCP server de LangWatch en Claude Code es compatible con el stack de OPENLAB (Claude Code CLI + MCP). La demo muestra configuración en settings.json de Claude Code, lo que OPENLAB ya conoce y puede replicar con MCP servers propios.
- **Oportunidades nuevas:** Crear un skill de OPENLAB "AI Agent Behavior Tester" que permita a responsables de negocio definir y testear comportamientos de sus agentes en lenguaje natural, sin intervención técnica. Es un upsell natural tras la entrega inicial de skills.
- **Argumento comercial:** "Con el stack de OPENLAB, tu CEO puede abrir Claude Code un lunes y en 20 minutos haber definido y testeado 40 escenarios de comportamiento de su agente — sin llamar a ningún desarrollador."

---

## Contenido detallado

### Ideas y argumentos principales

El vídeo abre con un escenario que "hace 18 meses habría sonado absurdo": un CEO (no desarrollador, no data scientist) abre un asistente de IA y describe en lenguaje llano cómo debe comportarse su agente o cómo está funcionando hoy. Sin especificaciones técnicas, solo intención. En minutos genera más de 40 test scenarios listos para ejecutar contra un agente que su equipo de ingeniería todavía está construyendo.

El argumento central: los que están más cerca de los usuarios son ahora los que definen cómo los sistemas de IA se testean, mejoran y en los que se confía. Esto invierte el flujo tradicional donde ingeniería define los tests y negocio espera resultados.

La demo usa LangWatch MCP server dentro de Claude Code (Claude chat environment). El PM/CEO describe el comportamiento esperado del agente en lenguaje natural, y LangWatch genera los test scenarios automáticamente, incluyendo casos de múltiple issue agent y ejemplos de fallo.

### Datos y evidencia
- 40+ test scenarios generados en minutos desde una descripción en lenguaje natural
- El proceso elimina: sprint planning, tickets de Jira, dependencia del equipo técnico para escribir tests
- Demo en producción con MCP server de LangWatch configurado en Claude Code

### Citas textuales

> "The people closest to the users are now the ones defining how AI systems are tested, improved, and trusted. And that changes everything." — Manuk, founder LangWatch

> "A CEO, not a developer, not a data scientist or an AI engineer opens an AI assistant on a certain morning. They describe in plain language how their AI agent should behave." — Manuk

### Ejemplos concretos
- Demo live: configuración de MCP server de LangWatch en settings.json de Claude Code
- Generación de 40+ test scenarios para un "complex multi-issue agent" desde lenguaje natural
- Visualización de runs de simulación y detección de errores del agente en la plataforma LangWatch
- URL: [LangWatch](https://langwatch.ai)

---

## Temas clave

### 1. El PM/CEO como operador directo de AI agents
El vídeo demuestra que el gap técnico que separa a los perfiles de negocio de la operación de AI agents está desapareciendo. Claude Code + MCP servers especializados permiten que el lenguaje natural sea la interfaz de configuración, testing y mejora de agentes. OPENLAB debe posicionarse como el enabler de este paradigma en empresas.

### 2. MCP como capa de extensión para no-técnicos
El MCP server de LangWatch en Claude Code es un patrón replicable: cualquier herramienta de negocio puede convertirse en un MCP server accesible en lenguaje natural desde Claude Code. Este es el modelo de extensión del stack de OPENLAB para clientes.

### 3. Testing como primera victoria no-técnica
Dar a un CEO la capacidad de definir y testear el comportamiento de un AI agent antes de que esté construido es una victoria rápida y visible. Es un punto de entrada ideal para proyectos OPENLAB: el cliente gana autonomía desde el primer sprint.


**Telegraph:** https://telegra.ph/Claude-Code-LangWatch-Skills-for-Product-Managers-03-26
