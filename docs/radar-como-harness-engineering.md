# OPENLAB Radar como ejemplo de Harness Engineering

## Qué es Harness Engineering en 2026

Harness engineering es la disciplina de diseñar **todo el sistema que envuelve a un agente de IA** para hacerlo fiable en producción. La fórmula fundamental es:

> **Agente = Modelo + Harness**

El harness (arnés) es todo lo que no es el modelo en sí: las herramientas disponibles, las restricciones sobre qué puede hacer, los mecanismos de verificación, la gestión de errores, y lo que ocurre antes de que algo se considere "terminado".

El término fue cristalizado por **Mitchell Hashimoto** (creador de Terraform/HashiCorp), formalizado por **Birgitta Böckeler** (Thoughtworks, publicado en el blog de Martin Fowler) y validado a escala por **OpenAI** (equipo Codex) y **Anthropic** a principios de 2026.

### Principio estratégico central

> *"A los agentes, a diferencia de los desarrolladores humanos, genuinamente no les importa que les micro-gestionen. Más restricciones, más comprobaciones, más estructura tiende a hacerlos rendir mejor, no peor."*
> — Birgitta Böckeler

### Evolución: Prompt → Context → Harness

| Disciplina | Período | Foco | Metáfora |
|---|---|---|---|
| **Prompt Engineering** | 2022–2024 | Optimizar la instrucción individual (few-shot, chain-of-thought) | Escribir la pregunta perfecta |
| **Context Engineering** | 2025 | Construir dinámicamente ventanas de contexto ricas (RAG, historial, herramientas) | Adjuntar todos los archivos correctos al email |
| **Harness Engineering** | 2026 | Arquitectar el sistema operativo completo alrededor del agente | El modelo es la CPU, el harness es el SO |

Context engineering es un **subconjunto** de harness engineering. Context engineering determina qué información entra al modelo. Harness engineering añade todo lo demás: lo que el sistema previene, mide, controla y repara.

### Por qué Modelo + Context no es suficiente

Si un agente es Modelo + Harness, entonces Modelo + Context **no basta**. Context engineering se ocupa de una sola cosa: **construir el input óptimo para el modelo** — qué ve, cuándo lo ve, en qué orden. Pero un agente fiable necesita mucho más que un buen input.

| Capa | Context engineering | Lo que añade el harness |
|---|---|---|
| **Antes del modelo** | ✅ Qué información recibe | Qué **no** debe recibir (filtrado, dedup, acotación de scope) |
| **Durante** | ✅ Herramientas disponibles | **Restricciones** sobre esas herramientas (permisos, sandboxing, timeouts) |
| **Después del modelo** | ❌ No se ocupa | **Validación del output** (¿es correcto? ¿tiene el formato esperado?) |
| **Si falla** | ❌ No se ocupa | **Gestión de errores** (reintentos, fallbacks, alertas) |
| **Bucle completo** | ❌ No se ocupa | **Orquestación** (qué pasa después, quién consume el resultado, cuándo se repite) |
| **A lo largo del tiempo** | ❌ No se ocupa | **Feedback loops** (el output de hoy mejora el harness de mañana) |

En concreto, lo que le falta al contexto para ser harness:

1. **Validación de outputs (sensores).** El contexto le dice al modelo "genera un brief con estos campos". El harness **verifica que el brief realmente tiene esos campos** y actúa si no los tiene.
2. **Control de flujo y orquestación.** El contexto no decide "primero scrapea, luego evalúa, luego publica, luego notifica". Eso es pipeline — es harness.
3. **Restricciones y guardrails.** El contexto le da herramientas al modelo. El harness decide **cuáles puede usar, cuándo, y con qué límites**.
4. **Gestión de errores.** Si el modelo genera basura o la API falla, el contexto no tiene respuesta. El harness sí: reintenta, alerta, escala a un humano, o descarta.
5. **Bucle de mejora continua.** El principio de Hashimoto: *"Cada vez que el agente comete un error, diseñas una solución para que nunca vuelva a cometerlo."* Eso es iterar sobre el harness, no sobre el contexto.

La analogía más clara:

> **Context engineering** = preparar el mejor briefing posible para un empleado.
> **Harness engineering** = diseñar el puesto de trabajo completo: el briefing, sí, pero también los checklists, las revisiones de calidad, el flujo de aprobación, qué hacer si algo sale mal, y cómo el sistema mejora con cada iteración.

Modelo + contexto te da un agente que **puede** funcionar bien. Modelo + harness te da un agente que **funciona bien de forma fiable y sostenida en producción**.

### Framework: controles feedforward vs feedback

- **Guías (feedforward):** Anticipan el comportamiento del agente y lo orientan *antes* de que actúe (CLAUDE.md, prompts estructurados, convenciones, scripts de bootstrap).
- **Sensores (feedback):** Observan *después* de que el agente actúa y le ayudan a autocorregirse (linters, tests, type checkers, revisión con IA).

Cada tipo puede ser **computacional** (determinista, rápido, basado en CPU) o **inferencial** (semántico, más lento, basado en LLM).

---

## ¿Es OPENLAB Radar un ejemplo de Harness Engineering?

**Sí, lo es** — y de forma bastante clara.

### Lo que cumple

| Componente del harness | Implementación en Radar |
|---|---|
| **Instrucciones de sistema (feedforward)** | `CLAUDE.md` con arquitectura, rutas y restricciones. Los prompts headless (`evaluate-daily.md`, `evaluate-manual.md`, `weekly-digest.md`) son guías feedforward puras |
| **Pipeline automatizado** | `run_daily.sh` y `run_weekly.sh` orquestan al modelo sin intervención humana — el humano diseñó el flujo, no escribe los briefs |
| **Skills como herramientas** | `radar-check-video`, `radar-add-video-remote` son extensiones del agente con lógica encapsulada |
| **Ciclo de vida completo** | Scraping → evaluación → brief → publicación Telegraph → notificación Telegram → email → sincronización Drive. El agente no "decide" el flujo, el harness lo impone |
| **Ejecución headless con cron** | El modelo corre como CPU (`claude -p`), el harness (scripts + cron + config) es el SO |
| **Controles computacionales** | `scraper.py` filtra vídeos antes de pasarlos al modelo; `radar.db` evita duplicados; `channels.yaml` / `keywords.yaml` acotan el input |
| **Gestión de errores y recuperación** | `run_recovery.sh` (cron 09:00 UTC) detecta si el pipeline diario falló, alerta por Telegram, y relanza el evaluador automáticamente. Trap ERR en ambos pipelines notifica fallos inesperados. Fallbacks en Telegraph (envío como texto si falla) y en Telegram (reintento sin Markdown si falla el parseo) |
| **Sub-agentes aislados** | Los skills usan sub-agentes con contexto separado (context firewalls) |

### Lo que le falta para ser un ejemplo completo

| Gap | Detalle |
|---|---|
| **Sensores de feedback automatizados** | No hay linters ni tests que validen la calidad del output del modelo (ej: ¿el brief tiene los campos requeridos? ¿el score es coherente con el contenido?) |
| **Bucle de autocorrección** | Si el modelo genera un brief defectuoso, no hay mecanismo que lo detecte y repita la evaluación |
| **Fitness functions arquitectónicas** | No hay verificaciones automáticas de que el sistema mantiene sus propiedades (cobertura temática, consistencia de tags). El skill `radar-lint` apunta en esa dirección, pero corre bajo demanda en vez de como parte del pipeline |

### Diagrama conceptual

```
┌─────────────────────────────────────────────────────┐
│                    HARNESS                           │
│                                                     │
│  ┌─────────────┐    ┌──────────────────────────┐    │
│  │ FEEDFORWARD  │    │       PIPELINE            │    │
│  │              │    │                          │    │
│  │ CLAUDE.md    │    │  scraper.py              │    │
│  │ prompts/     │    │    ↓                     │    │
│  │ channels.yaml│    │  claude -p (evaluate)    │    │
│  │ keywords.yaml│    │    ↓                     │    │
│  │ tags.yaml    │    │  brief .md generado      │    │
│  └──────┬───────┘    │    ↓                     │    │
│         │            │  publish_telegraph.py    │    │
│         │            │    ↓                     │    │
│         ▼            │  notify.py (Telegram)    │    │
│  ┌─────────────┐     │    ↓                     │    │
│  │   MODELO    │     │  md_to_email_html.py     │    │
│  │  (Claude)   │◄────│    ↓                     │    │
│  │   "CPU"     │     │  rclone → Google Drive   │    │
│  └─────────────┘     └──────────────────────────┘    │
│                                                     │
│  ┌─────────────┐    ┌──────────────────────────┐    │
│  │  CONTROLES  │    │      FEEDBACK             │    │
│  │             │    │                          │    │
│  │ radar.db    │    │  run_recovery.sh (cron)  │    │
│  │ (dedup)     │    │    → detecta fallo       │    │
│  │ cron timers │    │    → alerta Telegram     │    │
│  │ trap ERR    │    │    → relanza evaluador   │    │
│  │             │    │  radar-lint (manual) ⚠️   │    │
│  └─────────────┘    └──────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## Veredicto

**OPENLAB Radar es un ejemplo legítimo de harness engineering**, especialmente fuerte en controles feedforward (prompts estructurados, pipeline determinista, orquestación por scripts). El modelo es la CPU que genera los briefs; todo lo demás — scraper, cron, prompts headless, publicación, notificaciones — es el harness.

Lo que lo hace particularmente interesante como ejemplo es que **no es un coding agent** (el caso de uso más discutido), sino un **agente de inteligencia de mercado**. Demuestra que harness engineering aplica más allá del desarrollo de software.

Para ser un ejemplo de referencia, le convendría reforzar la pata de **feedback/sensores**: validación automática de outputs y bucles de autocorrección. El skill `radar-lint` ya apunta en esa dirección.

---

## Fuentes

- [Harness engineering for coding agent users — Birgitta Böckeler (Martin Fowler)](https://martinfowler.com/articles/harness-engineering.html)
- [Harness engineering: leveraging Codex in an agent-first world — OpenAI](https://openai.com/index/harness-engineering/)
- [Effective harnesses for long-running agents — Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Skill Issue: Harness Engineering for Coding Agents — HumanLayer](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents)
- [The Third Evolution: Why Harness Engineering Replaced Prompting in 2026 — Epsilla](https://www.epsilla.com/blogs/harness-engineering-evolution-prompt-context-autonomous-agents)
- [Harness Engineering vs Context Engineering — Rick Hightower (Medium)](https://medium.com/@richardhightower/harness-engineering-vs-context-engineering-the-model-is-the-cpu-the-harness-is-the-os-51b28c5bddbb)
- [Harness engineering: Structured workflows for AI-assisted development — Red Hat Developer](https://developers.redhat.com/articles/2026/04/07/harness-engineering-structured-workflows-ai-assisted-development)

---

*Análisis generado el 2026-04-10.*
