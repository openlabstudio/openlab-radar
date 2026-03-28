# OPENLAB Sales Context

> Contexto curado para generación de Opportunity Assessments y propuestas comerciales.
> Fuente: `openlab-offering-agentes-ia.md` v5.0 (2026-03-17)

---

## 1. Quiénes Somos

**OPENLAB** es una empresa de **context engineering**. Diseñamos procedimientos operativos para agentes de IA y los dejamos funcionando en el entorno del cliente.

**No vendemos:**
- Prompts ni configuraciones simples
- Software custom (bots, apps, backends)
- Formación puntual sin entregable
- Horas de consultoría tradicional

**Sí entregamos:**
- Skills completos (SKILL.md + context/ + templates/) adaptados al proceso del cliente
- Scripts de soporte (Python/Bash) para procesamiento de datos, integraciones con APIs del cliente, entrega automatizada, scraping y post-procesamiento (markdown → DOCX/PDF, dashboards)
- Sistemas agénticos multi-fase que producen resultados consistentes, repetibles y auditables
- Setup del entorno + piloto + formación en 4-7 semanas
- Zero lock-in: ficheros de texto plano en el entorno del cliente, portables entre plataformas

---

## 2. Equipo

| Persona | Rol | Expertise |
|---------|-----|-----------|
| **Alberto Villalobos** | CEO, Founder | 25+ años innovación tecnológica. Serial entrepreneur: 5G, ciberseguridad, movilidad, IA, robótica, blockchain. |
| **Rafael López García del Valle** | AI Innovation Architect, Founder | 20+ años I+D e innovación digital. Experto en lean, agentes IA, knowledge scaling, automatización de procesos. |
| **Antonio Salido** | Strategic Consultant | Digitalización e innovación en sector financiero: banca, inversión, consulting. |
| **Carlos de Mundi** | Senior Enterprise Data Lead | 17+ años Enterprise Intelligence e integración de sistemas. Senior SAP BI Consultant, ex-Deloitte. |
| **Pepe Cortés** | CLO, AI & Legal Tech | Derecho Mercantil, Legal Tech e IA. Compliance desde la fase de diseño. |

**Modelo:** Founders directamente involucrados en cada proyecto. Sin juniors.

---

## 3. Propuesta de Valor

### Elevator Pitch

> *"Venimos de Venture Building. Cuando llegó la IA Generativa, nos obsesionamos con una cosa: cómo aplicarla masivamente a los procesos de negocio. Las grandes consultoras venden horas. Nosotros construimos sistemas de IA que virtualizan tareas intensivas en conocimiento — y os los dejamos funcionando. En semanas, no en meses. Todo se queda en vuestro entorno: sin lock-in, sin dependencia."*

### Cinco Diferenciadores

1. **Context engineering, no prompt engineering.** Miles de líneas de ingeniería de contexto por agente. No una frase escrita a mano.
2. **Zero lock-in.** Ficheros de texto plano auditables. Si OPENLAB desaparece, los agentes siguen funcionando.
3. **De la estrategia al agente funcionando — en semanas.** No entregamos PowerPoints. Entregamos sistemas que producen resultados desde el día siguiente.
4. **Infra del cliente, skills nuestros.** OPENLAB nunca toca datos del cliente.
5. **Founders en cada proyecto.** Boutique. Sin capa de juniors.

### Analogía para el cliente

- **ChatGPT con prompt** = explicar a un becario cada vez
- **Custom GPT / Copilot Studio** = chuleta de media página
- **Sistema OPENLAB** = manual de operaciones completo para un analista senior con acceso a internet, herramientas, documentos y otros analistas en paralelo

---

## 4. Arquitectura de Delivery

### Decisión de arquitectura

| Arquitectura | Decisión | Motivo |
|---|---|---|
| Bot Teams + Claude API via Foundry | ❌ Descartada | OPENLAB mantendría software en producción |
| Gemini Gems nativo | ❌ Descartada | Calidad insuficiente (~80-85%), sin diferenciación |
| **Skills + VPS + Claude Code CLI** | **✅ Seleccionada** | Máxima calidad (95-100%), zero infra propia |

### Cómo funciona

```
Lo que pone OPENLAB:
  └── Ficheros .md en un repo git (instrucciones en lenguaje natural)

Lo que pone el cliente:
  ├── VPS o entorno de ejecución (su Azure/AWS/on-prem)
  ├── Cuenta del runtime (Claude Max/Team/Enterprise)
  └── Entrega hacia sus sistemas (Teams webhook, email, SharePoint)
```

### Portabilidad

Skills siguen el estándar Agent Skills (35+ plataformas): Claude Code, Codex CLI, GitHub Copilot, Gemini CLI (experimental). Si el cliente cambia de runtime, los skills se mueven con `git clone`.

### Integraciones con sistemas del cliente (MCP + CLI tools)

Los skills interactúan con los sistemas del cliente via MCP (Model Context Protocol) — el agente no solo genera outputs, los **entrega** donde se necesitan:

- **Google Workspace:** GWS CLI oficial de Google (`gws mcp`) — Gmail, Drive, Sheets, Calendar, Docs. 100+ herramientas.
- **Microsoft 365:** MCP Servers oficiales de Microsoft — SharePoint, OneDrive, Outlook, Teams. + Graph API via scripts.
- **CRM:** Salesforce (oficial), HubSpot (oficial)
- **ERP:** SAP (oficial — Build + HANA Cloud)
- **Project Management:** Jira, Linear, Asana (todos oficiales)
- **Comunicación:** Slack (oficial), Teams webhooks
- **Bases de datos:** PostgreSQL, MySQL, Supabase

Todo corre en el entorno del cliente con sus credenciales. OPENLAB diseña el skill, el cliente pone la conexión.

### Interfaces para usuarios

| Opción | UX | Para quién | Coste/usuario |
|---|---|---|---|
| **Claude Cowork + plugins** | App de escritorio, chat limpio | Usuarios de negocio | $25-90/mes |
| **VS Code + extensión Claude Code** | IDE con chat integrado | Usuarios tech-savvy | $100/mes |
| **Solo VPS (crons) + outputs en Teams/email** | Sin interacción directa | Consumidores pasivos | $0 (solo VPS) |

---

## 5. Líneas de Servicio

### Línea Principal: Context Engineering + Skills nativos

**Para quién:** Cualquier empresa que quiera automatizar procesos de conocimiento intensivo.

**Modelo de engagement:**

| Fase | Qué | Duración |
|---|---|---|
| Discovery | Sesiones con equipo, análisis de fuentes, formatos | 1 semana |
| Context engineering | Diseño de skills + context/ + templates/ por agente | 1-2 semanas |
| Setup + scripts | VPS, crons, entrega, acceso para usuarios | 3-5 días |
| Piloto + iteración | Feedback real, ajustes, formación | 2-4 semanas |
| **Total** | | **4-7 semanas** |

### Línea Secundaria: SaaS / Producto para cliente

**Para quién:** Clientes que quieren comercializar inteligencia IA a sus propios clientes (producto para venta/suscripción a terceros).

**Criterio:** Solo si el cliente tiene modelo de negocio claro y mercado validado.

### Modelo recurrente (land & expand)

| Fase | Qué | Recurrencia |
|---|---|---|
| **Diseño inicial** | Skill como entregable tangible que demuestra valor inmediato | Una vez |
| **Adopción** | Formación del equipo, onboarding de champions | Onboarding |
| **Mantenimiento** | Fuentes cambian, criterios evolucionan, el skill se actualiza | Continuo |
| **Evolutivos** | Nuevas fases, integraciones MCP, scripts, mejoras | Bajo demanda |
| **Nuevos skills** | Una vez ven el valor del primero, quieren automatizar más | Expansión |

Cada skill genera dependencia operativa legítima (no técnica — los skills son portables). El lock-in es de conocimiento: OPENLAB entiende el negocio, los criterios, las fuentes, los workflows del cliente.

**Puerta de entrada típica:** Workshop de co-creación (~4h) → del workshop salen 2-3 pilotos definidos con alcance, criterios de éxito y champions internos.

---

## 6. Casos de Uso Típicos

### Innovación corporativa e intraemprendimiento
- Sesiones de ideación estructurada con agentes de design thinking
- Scoring y filtrado automático de ideas contra criterios definidos
- Validación de mercado autónoma (TAM/SAM/SOM, competidores, red flags)
- Generación de business cases a partir de documentación existente
- Prototipado rápido: de concepto a wireframes y especificaciones

### Inteligencia estratégica y de mercado
- Market research on demand: inteligencia competitiva, tendencias, regulación
- Due diligence y deal screening para equipos de inversión (VC/PE/M&A)
- Detección de tendencias periódica con briefings automáticos
- Evaluación de riesgos operativos, regulatorios o de mercado

### Operaciones comerciales
- Síntesis automática de forecasts y reporting ejecutivo
- Análisis de calidad de llamadas comerciales
- Preparación de reuniones con clientes (briefings con contexto e histórico)
- Account planning: tracking de compromisos, oportunidades de upsell

### Talento, cultura y onboarding
- Onboarding acelerado: misma cultural y de producto desde cualquier oficina
- Product knowledge bots para equipos comerciales de productos complejos
- Packaging de DNA cultural en asistentes interactivos

### Operaciones y automatización de procesos
- Procesamiento de documentos: extracción, clasificación, resumen
- Orquestación de workflows multi-paso
- Quality assurance: monitorización de outputs para consistencia y compliance

---

## 7. Catálogo de Agentes y Workflows

### 7.1 Product Builder Suite (PBS) — 9 agentes

| Agente | Qué hace | Capacidades clave | Workflows que ejecuta |
|--------|----------|-------------------|----------------------|
| **Analyst (Mary)** | Market research, análisis competitivo, elicitación de requisitos | Porter's Five Forces, SWOT, competitive intelligence, domain expertise | `domain-research`, `market-research`, `technical-research` |
| **Architect (Winston)** | Diseño de sistemas, infraestructura, patrones escalables | Distributed systems, cloud infrastructure, API design, technology selection | `create-architecture` |
| **PM (John)** | Creación de PRD, discovery de requisitos, alineación de stakeholders | Jobs-to-be-Done, user interviews, opportunity scoring, market research | `create-prd`, `edit-prd`, `validate-prd` |
| **UX Designer (Sally)** | User research, diseño de interacción, estrategia de experiencia | User research, interaction design, UI patterns, AI-assisted tools | `create-ux-design` |
| **Dev (Amelia)** | Implementación con TDD, ejecución de stories | Story execution, test-driven development, code implementation | `dev-story` |
| **QA (Quinn)** | Test automation, API testing, E2E testing | Test coverage analysis, rapid test generation, standard test patterns | `qa-generate-e2e-tests` |
| **Quick Flow Solo Dev (Barry)** | Especificación rápida + implementación lean | Rapid spec creation, lean implementation, minimum ceremony | `quick-spec`, `quick-dev` |
| **SM (Bob)** | Sprint planning, gestión ágil, backlog, retrospectivas | Agile ceremonies, story preparation, sprint tracking | `sprint-planning`, `sprint-status`, `create-story`, `correct-course`, `retrospective` |
| **Tech Writer (Paige)** | Documentación técnica, diagramas, clarificación de conceptos | CommonMark, DITA, OpenAPI, Mermaid diagrams | `document-project`, `generate-project-context` |

### 7.2 Creative & Innovation Suite (CIS) — 6 agentes

| Agente | Qué hace | Capacidades clave | Workflows que ejecuta |
|--------|----------|-------------------|----------------------|
| **Brainstorming Coach (Carson)** | Facilitación de brainstorming, técnicas creativas | Creative techniques, group dynamics, systematic innovation | `brainstorming` |
| **Design Thinking Coach (Maya)** | Facilitación design thinking completa | Empathy mapping, prototyping, user insights, human-centered design | `design-thinking` |
| **Creative Problem Solver (Dr. Quinn)** | Resolución sistemática con TRIZ, Theory of Constraints | TRIZ, Systems Thinking, root cause analysis | `problem-solving` |
| **Innovation Strategist (Victor)** | Blue Ocean, Jobs-to-be-Done, modelos de negocio | Business model innovation, strategic disruption, opportunity identification | `innovation-strategy` |
| **Storyteller (Sophia)** | Narrativa persuasiva, frameworks de historia | Emotional psychology, audience engagement, brand narratives | `storytelling` |
| **Presentation Master (Caravaggio)** | Comunicación visual, pitch decks, dataviz | Visual hierarchy, audience psychology, information design, Excalidraw | — |

### 7.3 OPENLAB Skill Suite (OSS) — 4 agentes especializados

Skills propios de OPENLAB construidos como soluciones verticales completas (SKILL.md + context/ + templates/).

| Agente | Qué hace | Capacidades clave |
|--------|----------|-------------------|
| **ATLAS** | Evaluación integral de pitch decks (Pre-seed a Series B). Valida claims de mercado, mapea paisaje competitivo, evalúa equipos fundadores. | Pitch deck analysis, TAM/SAM/SOM validation, competitive landscape, founder evaluation, recomendación INVERTIR/DESCARTAR/CONDICIONAL |
| **NILO** | Motor de ideación estructurada. Transforma ideas semilla en conceptos candidatos validados en sesiones de 15-20 min. | SCAMPER, First Principles, What If, Analogías. Divergencia primero, convergencia después. |
| **ARES** | Valida ideas de innovación contra la realidad del mercado. Análisis cuantitativo de tamaño de mercado, competencia y tendencias. | Market sizing (TAM/SAM/SOM), competitor analysis, trend analysis, recomendación GO/PIVOT/NO-GO |
| **IRIS** | Analiza papers académicos y proyectos de investigación para descubrir potencial de impacto real y oportunidades de transferencia tecnológica. | Academic paper analysis, technology transfer, market applications, commercialization pathways |

### 7.4 Orquestación — 1 agente

| Agente | Qué hace |
|--------|----------|
| **BMad Master** | Orquestador principal. Gestiona workflows, coordina agentes en pipelines multi-fase y administra recursos en runtime. |

### 7.5 Workflows disponibles (31 total)

Los workflows son procedimientos que los agentes ejecutan. No son entidades separadas — son capacidades del agente.

| Fase | Workflows | Agente principal |
|------|-----------|-----------------|
| **Análisis** | `domain-research`, `market-research`, `technical-research`, `create-product-brief` | Analyst, PM |
| **Planificación** | `create-prd`, `edit-prd`, `validate-prd`, `create-ux-design` | PM, UX Designer |
| **Diseño de solución** | `create-architecture`, `create-epics-and-stories`, `check-implementation-readiness` | Architect, SM |
| **Implementación** | `create-story`, `dev-story`, `sprint-planning`, `sprint-status`, `correct-course`, `retrospective`, `code-review` | SM, Dev |
| **Quick Flow** | `quick-spec`, `quick-dev` | Quick Flow Solo Dev |
| **QA y documentación** | `qa-generate-e2e-tests`, `document-project`, `generate-project-context` | QA, Tech Writer |
| **Creatividad e innovación** | `brainstorming`, `design-thinking`, `innovation-strategy`, `problem-solving`, `storytelling` | Agentes CIS |
| **Orquestación** | `party-mode` (discusión multi-agente) | BMad Master |

### 7.6 Patrones de solución probados (pipelines validados)

Combinaciones de agentes y workflows que ya están construidas y funcionan en producción. Se priorizan sobre combinaciones teóricas.

| Solución | Pipeline | Estado |
|----------|----------|--------|
| **Market Due Diligence** (VCs) | Analyst → market-research → scoring + red flags + recomendación (7 fases autónomas) | En producción |
| **Ideation Engine** (Innovación) | Brainstorming Coach → brainstorming + Design Thinking Coach → design-thinking (SCAMPER, First Principles, What If, Analogías) | En producción |

**Combinaciones naturales por área funcional:**

| Área funcional | Pipeline de agentes → workflows |
|----------------|--------------------------------|
| Investigación de mercado / tendencias | Analyst → `domain-research`, `market-research`, `technical-research` |
| Estrategia de innovación | Innovation Strategist → `innovation-strategy` |
| Ideación y creatividad | Brainstorming Coach → `brainstorming` · Design Thinking Coach → `design-thinking` |
| Validación de ideas | Analyst → `market-research` · PM → `validate-prd` |
| Definición de producto | PM → `create-prd` · Analyst (apoyo con research) |
| Diseño de solución | Architect → `create-architecture` · UX Designer → `create-ux-design` |
| Prototipado rápido | Quick Flow Solo Dev → `quick-spec` → `quick-dev` |
| Documentación | Tech Writer → `document-project` |
| Gestión ágil | SM → `sprint-planning` · `sprint-status` |
| Narrativa y comunicación | Storyteller → `storytelling` · Presentation Master |
| Problem solving estructurado | Creative Problem Solver → `problem-solving` |

**Pipeline completo ejemplo:** Brainstorming Coach → Analyst → PM → Architect → Dev

**Total: 15 agentes PBS/CIS + 4 agentes OSS + 1 orquestador = 20 agentes + 31 workflows.**

---

## 8. Pricing

### Tarifa horaria

**€120/h** — founders directamente involucrados en cada proyecto. Sin juniors.

### Línea Principal

| Concepto | Precio |
|---|---|
| Proyecto inicial (2 agentes en producción) | €16.000 |
| Agente adicional completo (skill + cron + testing) | €4.000-6.000 |
| Adaptación de agente del catálogo OPENLAB | €2.500-3.500 |
| Solo skill proactivo (sin interactivo) | €1.500-2.500 |

### Línea Secundaria (SaaS)

| Concepto | Precio |
|---|---|
| Desarrollo producto completo | €25.000-30.000 |
| Mantenimiento | €350-575/mes |

### Post-entrega y soporte

Los skills son ficheros de texto plano en lenguaje natural. No hay código que se rompa, ni dependencias que actualizar, ni servidores que monitorizar. Si nada cambia en el negocio del cliente, el skill funciona indefinidamente sin intervención.

| Concepto | Modelo | Notas |
|---|---|---|
| Garantía post-entrega | Incluida en proyecto | 4-6 semanas tras entrega. Ajustes y estabilización **sin límite de horas** durante el periodo de garantía. |
| Post-garantía (Línea Principal) | Fase 2 | Si las prioridades cambian (nuevas fuentes, criterios, ejes estratégicos), los ajustes se enmarcan en Fase 2 donde el acompañamiento estratégico incluye calibración continua. No hay bolsas de horas ni contratos de mantenimiento — o es garantía (gratis) o es Fase 2 (nuevo alcance). |
| Garantía extendida (SaaS) | 1 mes post-entrega | Solo para línea secundaria |

### Descuentos aplicables

- **Early Adopter:** -€2.000 a -€3.000
- **Proyecto Fundacional** (nuevo sector): -€2.000 a -€3.000
- **Cliente Estratégico** (referenciable): Negociable

### Modelo de facturación

- 50% a la firma (kick-off)
- 50% a la finalización de entregables

### ROI típico

Ejemplo: Analista que gasta 10h/semana en tareas manuales.
- Con agente: 10h → 2h (80% reducción)
- Ahorro: 8h/semana × €50/h = €400/semana = **€20.800/año por analista**
- Breakeven de proyecto (€16K): < 10 meses con 1 analista

---

## 9. Criterio de Decisión

| Pregunta | Respuesta correcta |
|----------|-------------------|
| ¿Requiere que OPENLAB desarrolle software? | NO. Diseñamos skills, no software. |
| ¿Requiere que OPENLAB mantenga infraestructura? | NO. La infra es del cliente. |
| ¿Degrada la calidad por debajo del 90%? | NO. Riesgo reputacional. |
| ¿Tiene riesgo de obsolescencia a 6-12 meses? | Evitar. Construir sobre estándares abiertos. |
| ¿Compite en algo que no sea context engineering? | Evitar. Ahí no tenemos ventaja. |
| ¿Es un agente simple (<8K chars)? | No es nuestro mercado. |

**Regla de oro:** Si la solución requiere que OPENLAB desarrolle y mantenga software, es la solución equivocada.

---

## 10. Compliance y Seguridad

| Aspecto | Situación |
|---------|-----------|
| Residencia de datos | Claude API procesa en EE.UU. Anthropic no entrena con datos enterprise. |
| Datos no sensibles (innovación, research) | Sin problema — datos públicos |
| Datos sensibles o regulados | Azure AI Foundry (residencia EU) o AWS Bedrock. Trade-off de rendimiento. |
| Entorno recomendado para piloto | VPS aislado, datos públicos, zero PII |

**Principio:** No sacar compliance proactivamente. Si no toca PII, la exposición es mínima.

---

## 11. Posicionamiento Competitivo

### vs. Grandes consultoras (Accenture, McKinsey)
> *"Si necesitas 20.000 agentes, llama a McKinsey. Si necesitas 2-3 que transformen un proceso real en semanas, llámanos."*

### vs. Integradores IA (WeArtificial / Liquid Lab)
> *"Ellos os enseñan a conducir. Nosotros os construimos el coche y os lo dejamos con las llaves."*

### vs. Agencias n8n / Make
> *"Si necesitas reenviar un email a un CRM, una agencia de n8n te lo resuelve. Si necesitas que un analista virtual investigue tu mercado y genere un business case, eso es lo que hacemos."*

### vs. "Esto me lo hago con ChatGPT"
> *"Claro. Como puedes hacer tu contabilidad con Excel. ¿Quieres un resultado consistente o depender de cómo te levantes para escribir el prompt?"*

---

**Última actualización:** 2026-03-17
**Fuente:** `openlab-offering-agentes-ia.md` v5.0
