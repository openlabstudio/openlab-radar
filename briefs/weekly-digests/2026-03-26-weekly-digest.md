# OPENLAB Radar — Digest Semanal 2026-03-20 a 2026-03-26

---

## Resumen

- **Vídeos evaluados esta semana:** 71 (3 días de pipeline activo: 24, 25 y 26 de marzo)
- **Seleccionados:** 25 briefs individuales generados | **Media score estimada:** ~7.8
- **Por categoría:**
  - `agentic-systems`: 9 briefs
  - `claude-code-advanced`: 6 briefs
  - `context-engineering`: 5 briefs
  - `delivery-adoption`: 3 briefs
  - `enterprise-ai`: 1 brief
  - `cli-vs-platforms`: 1 brief

---

## Tendencias de la Semana

### 1. Skills como arquitectura, no como hack

Tres días consecutivos con múltiples vídeos sobre skills en Claude Code — incluyendo una crítica directa (Tim Carambat, "SKILLS.md are a token trap", score 8.2). El dato más significativo: la crítica misma es evidencia de que el concepto ya es suficientemente mainstream para generar anticuerpos. La comunidad está en el momento de transición entre adopción temprana y consolidación.

Lo que habla la comunidad: cómo estructurar skills para agentes autónomos, cómo auto-mejorarlos (Karpathy AutoResearch aplicado a ficheros .md), y cómo enseñarlos a clientes no técnicos (medellinJS, LangWatch, Claude Cowork). El vocabulario se está estandarizando: "skill repository", "harness", "intent engineering", "agent kernel".

**Implicación para OPENLAB:** El momento de escribir el marco de referencia propio es ahora. El ecosistema lleva tres días generando vocabulario; OPENLAB debería apropiarse del que ya usa internamente y publicarlo. La frase del vídeo de Intuition Machine — *"prompting is prose, agent engineering is architecture"* — es el argumento de venta que OPENLAB no ha escrito todavía.

---

### 2. De "cómo construir" a "cómo mantener y mejorar en producción"

La semana pasada la pregunta era "¿cómo se hace un skill?". Esta semana la pregunta es "¿cómo sé si funciona y cómo mejora solo?". Tres señales claras:

- **AutoResearch aplicado a skills**: Kacper Rutkiewicz demuestra un bucle generate → evaluate → modify que pasa de 60-70% de outputs buenos a 95% con 100 iteraciones overnight (score 8.5).
- **Evaluaciones en producción**: Supercharging AI agents with evaluations (Voxel51) y Agent Identity Protocol (AIP) para governance a escala.
- **Context poisoning**: Michel Tricot (co-fundador Airbyte) acuña el concepto de contexto acumulado que corrompe silenciosamente agentes en sesiones largas (score 7.2, calidad editorial 8).

**Implicación para OPENLAB:** El catálogo OLAF necesita un skill de "eval suite" — criterios objetivos + preguntas sí/no + palanca (el skill.md) — para que los clientes puedan saber que sus agentes mejoran. Sin métricas, los agentes en producción son una caja negra. Esto es un hueco en el catálogo actual.

---

### 3. El stack CLI se vuelve accesible sin terminal

Claude Code Channels (control vía Discord/Telegram nativo), Oh My Claude Code (11k+ stars, 32 agentes, 6 modos de orquestación), y Claude Cowork (demos de "primer AI team member en 15 minutos sin código") están eliminando la fricción técnica del stack CLI. La semana ha sido la más densa en herramientas de democratización del acceso.

El caso más potente: LangWatch demuestra live cómo un CEO describe en lenguaje natural cómo debe comportarse un agente y genera 40 casos de test en minutos vía MCP server — sin tocar ningún terminal.

**Implicación para OPENLAB:** El argumento "los dueños del proceso definen el agente, no los desarrolladores" tiene ahora evidencia externa grabada y publicada. Usar el vídeo de LangWatch como asset comercial en demos.

---

## Top 5 Vídeos de la Semana

### 1. Skill vs Agent: The Architecture That Makes Openclaw Systems Work
**Score: 9.0** | Zero Team AI | 7 min | agentic-systems

Framework de 4 ficheros core por agente (Identity, Soul, Heartbeat, Memory) + "one writer rule" + datos de producción real: 9 agentes en VPS de $5/mes durante 3 meses. El benchmark que lo cambia todo: **markdown files (74%) > vector databases (68.5%)** en memoria de agentes. Es el argumento definitivo para el enfoque OPENLAB, con datos propios de producción.

→ [Ver brief completo](../agentic-systems/2026-03-25-skill-vs-agent-openclaw-architecture.md)

---

### 2. Pi CEO Agents. Claude 1M Context. Multi-Agent Teams.
**Score: 8.7** | IndyDevDan | 40 min | agentic-systems

Patrón "CEO Agent" que delega y orquesta en vez de ejecutar, con uso real del contexto de 1M tokens para mantener coherencia entre sub-agentes. Directamente aplicable al BMad Master y a la arquitectura multi-agente de OPENLAB. Uno de los vídeos más citados de la semana.

→ [Ver brief completo](../agentic-systems/2026-03-24-pi-ceo-agents-1m-context.md)

---

### 3. Andrej Karpathy en No Priors
**Score: 8.5** | No Priors | largo | agentic-systems

La entrevista más densa de la semana. El cambio de ratio 80/20 (código propio/agente) a 20/80 de Karpathy, el concepto de AutoResearch overnight que encuentra mejoras que él no encontró en 20 años, y la tesis de que "markdown para agentes, no documentación HTML para humanos" — todo ello apunta al modelo OPENLAB. La paradoja de Jevons aplicada al software es el argumento comercial más sólido disponible: más IA = más demanda de software = más demanda de skills.

→ [Ver brief completo](../agentic-systems/2026-03-23-karpathy-no-priors.md)

---

### 4. How My Claude Skills Improve Themselves (Autoresearch)
**Score: 8.5** | Kacper Rutkiewicz | 20 min | context-engineering

AutoResearch de Karpathy aterrizado en Claude skill files. Tres ingredientes: métrica objetiva, eval suite de preguntas sí/no, palanca (el skill.md). Pasa de 60-70% a 95% con 100 iteraciones overnight. Los ingredientes son replicables por cualquier equipo OPENLAB mañana.

→ [Ver brief completo](../context-engineering/2026-03-25-claude-skills-autoresearch.md)

---

### 5. 42 Agent Architecture Patterns: From Skill Repos to Intent & Harness Engineering
**Score: 8.2** | Intuition Machine | 19 min | agentic-systems

Un vocabulario de 42 patrones nombrados e interconectados para Claude Code — desde "Skill Repository" a "Intent Engineering Harness". La frase *"prompting is prose, agent engineering is architecture"* es el argumento de venta en sí misma. Úsalo como marco de referencia para formalizar y nombrar decisiones de arquitectura que OPENLAB ya toma.

→ [Ver brief completo](../agentic-systems/2026-03-26-42-agent-architecture-patterns.md)

---

## Gaps Detectados

| Categoría | Briefs | Observación |
|-----------|--------|-------------|
| `enterprise-ai` | 1 | Solo el caso CGI.| `cli-vs-platforms` | 1 | Cole Medin declara muerto el paradigma LangChain — pero solo desde una perspectiva. Falta análisis comparativo propio |
| Industrias verticales | 0 | Ningún vídeo de aplicación sectorial (legal, salud, real estate) más allá de finanzas (mención rápida) |
| Métricas y ROI | 0 | Ningún vídeo sobre cómo medir el valor entregado por agentes en producción |
| Seguridad y governance | 1 (mención) | Agent Identity Protocol mencionado como mención rápida — es el único brief sobre governance esta semana |

**El gap más crítico:** No hay contenido sobre cómo medir ROI de agentes. Es el hueco más frecuente en pitches a enterprise y nadie de la comunidad lo está cubriendo — oportunidad de contenido propio para OPENLAB.

---

## Recomendaciones

### Nuevos canales a añadir

| Canal | Motivo | Vídeo detectado |
|-------|--------|-----------------|
| **Intuition Machine - AGI is the Medium** | Arquitectura de agentes con vocabulario propio y alto nivel de abstracción. No es tutorial — es teoría aplicada. | 42 Agent Architecture Patterns (8.2) |
| **Zero Team AI** | Datos de producción real (3 meses, 9 agentes, VPS $5). Uno de los pocos canales con benchmarks propios. | Skill vs Agent (9.0) |
| **The Chain of Thought Podcast** | Calidad editorial alta (8/10). Acuña conceptos ("context poisoning") que la comunidad adopta rápido. | Context Poisoning (7.2, calidad 8) |

### Keywords a ajustar

- **Añadir:** `"context poisoning"`, `"agent harness"`, `"intent engineering"`, `"CEO agent"` — aparecen múltiples veces esta semana y producen señal de alta calidad.
- **Revisar:** El término `OpenClaw` aparece en vídeos de distintas cosas (arquitectura, un canal específico, un plugin). Evaluar si está generando ruido cruzado entre señales distintas.

### Temas emergentes a monitorizar

1. **Auto-mejora de skills** (bucles eval autónomos) — pasará de nicho a estándar en 4-6 semanas a este ritmo.
2. **Claude Code Channels** (control vía mensajería) — Anthropic está moviendo fichas hacia enterprise sin terminal. Observar si esto normaliza el stack CLI para perfiles técnicos intermedios.
3. **Crítica al paradigma de skills** (Tim Carambat, "token trap") — la contracorriente existe. Preparar argumentario.

---

## Aplicabilidad OPENLAB

### Para un cliente actual o propuesta en curso

- **Argumento benchmark listo:** Markdown files (74%) > vector databases (68.5%) en memoria de agentes. Dato propio de producción de Zero Team AI. Úsalo en cualquier propuesta donde el cliente pregunte "¿por qué no RAG?".
- **Caso CGI como referencia externa:** Firma de consultoría (~100k personas) con proposal generator agent (produce 60-70% de un RFP en borrador) y deal qualification agent. La adopción les tomó 2 años desde ChatGPT. Argumento de venta: OPENLAB acorta esa curva.
- **LangWatch como demo asset:** CEO describe comportamiento del agente en lenguaje natural → 40 casos de test en minutos vía MCP. Grabar y usar en próxima demo comercial.

### Para el catálogo OLAF

- **Skill de eval suite:** Crear un skill que genere métricas objetivas + preguntas sí/no evaluables para cualquier skill existente. Es el ingrediente que falta para AutoResearch propio.
- **Skill de context hygiene:** Basado en "context poisoning" de Michel Tricot — mecanismo de limpieza de contexto para agentes en sesiones largas. Aplicable a due diligence, market intelligence y cualquier skill que opere en sesiones extendidas.
- **Skill de harness arquitectónico:** El patrón "boardroom" (agentes adversariales + compute budgets + template estructurado) de Mat Siems es directamente empaquetable como skill para análisis estratégico y due diligence.

---

*Generado automáticamente por OPENLAB Radar · 2026-03-26*
*Fuentes: 3 daily briefings (2026-03-24 a 2026-03-26) + 25 briefs individuales en 6 categorías*
