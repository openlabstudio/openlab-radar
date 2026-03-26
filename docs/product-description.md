# OPENLAB Radar — Descripción de Producto

Sistema de inteligencia continua que monitoriza YouTube diariamente para detectar contenido avanzado relevante para OPENLAB. Filtra, evalúa y prioriza vídeos según su aplicabilidad directa al trabajo de context engineering y delivery de skills en empresas.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│  CRON DIARIO (08:00 UTC / 09:00 CET) — Solo Rafael      │
│                                                         │
│  1. Scraper (Python)                                    │
│     YouTube Data API → 15 canales + 18 keywords          │
│     Filtro: duración, exclusiones                       │
│     Output: data/candidates-FECHA.json                  │
│                                                         │
│  2. Evaluador (Claude Code headless + Telegram Channel) │
│     Etapa 1 — Triage: título+canal → SÍ/QUIZÁ/NO       │
│     Etapa 2 — Transcript (youtube-transcript MCP)       │
│              Solo supervivientes del triage              │
│     Etapa 3 — Scoring con transcript completo           │
│              + contexto OPENLAB (sales, capabilities,   │
│                references, pilots)                      │
│     Etapa 4 — Briefing + resúmenes .md por categoría    │
│                                                         │
│  3. Briefing → chat privado Rafael (Telegram Channel)   │
│     Bidireccional: Rafael responde, Claude procesa      │
│                                                         │
│  4. Email HTML (branded, Montserrat) → rafa@openlab     │
│     Generado con md_to_email_html.py vía gws CLI        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  CRON SEMANAL viernes 08:30 UTC / 09:30 CET             │
│  Equipo: Rafa, Alberto, Carlos, Pepe                    │
│                                                         │
│  1. Analiza briefings y resúmenes de la semana          │
│  2. Genera digest: tendencias, top 5, gaps, recs        │
│  3. Publica en Canal Telegram (t.me/openlabRadar)       │
│  4. Email HTML al equipo (md_to_weekly_html.py + gws)   │
│     · Títulos → YouTube · Botón → Telegraph            │
│  5. Avisa a Rafael por chat privado Telegram             │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  ADICIÓN MANUAL (Claude Code, en VPS o laptop)          │
│                                                         │
│  "añade este vídeo al radar: URL"                       │
│                                                         │
│  Desde el VPS → skill radar-add-video                   │
│    transcript → triage → scoring → brief → DB           │
│    → Telegraph + Telegram                               │
│                                                         │
│  Desde el laptop → skill radar-add-video-remote         │
│    SSH transparente al VPS → mismo pipeline             │
│    Sin SSH manual, sin navegar carpetas                 │
│                                                         │
│  El brief se guarda en briefs/CATEGORÍA/ con la marca   │
│  "Añadido: manualmente". No toca el briefing del día.   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  CONSULTA (Claude Code, sin límites)                    │
│                                                         │
│  "¿Qué dicen los vídeos sobre context engineering?"     │
│  → Grep busca en briefs/ → lee los relevantes           │
│  → Sintetiza respuesta con citas de los .md             │
│                                                         │
│  Sin límite de queries ni de fuentes.                   │
│  1M tokens de contexto = ~400 resúmenes de golpe.       │
└─────────────────────────────────────────────────────────┘
```

---

## Categorías de búsqueda

| Categoría | Carpeta en briefs/ | Qué busca |
|-----------|-------------------|-----------|
| `context_engineering` | `context-engineering/` | CLAUDE.md, skills architecture, context window, prompt design |
| `claude_code_advanced` | `claude-code-advanced/` | BMAD, SPARC, hooks, MCP, headless, multi-agent, worktrees |
| `agentic_systems` | `agentic-systems/` | Orchestration, pipelines, reliability, observability en producción |
| `enterprise_ai` | `enterprise-ai/` | Procesos de conocimiento, automatización documental, IA cadena de valor |
| `cli_agents_vs_platforms` | `cli-vs-platforms/` | CLI agents vs n8n/Zapier/LangGraph, zero-dependency agents |
| `delivery_adoption` | `delivery-adoption/` | Delivery de skills a clientes, adopción CLI en empresa, Cowork como puente GUI, pricing/packaging |

---

## Sistema de evaluación (4 etapas)

### Etapa 1 — Triage rápido

**Input:** Solo título + canal + descripción corta (del JSON de candidatos).
**Output:** SÍ / QUIZÁ / NO con motivo.

Criterios de descarte (→ NO):
- Tutoriales básicos ("Getting started", "Qué es Claude Code", "for beginners")
- Solo muestra UI sin profundidad técnica
- Vibe coding sin metodología
- Repetición de announcements sin análisis propio
- Coding puro sin aplicación a procesos de negocio
- Agentes tipo n8n/Zapier/plataformas no-code
- "AI automation" genérica sin relación con CLI agents o skills en lenguaje natural
- Clickbait sin sustancia

Señales de SÍ rápido:
- Menciona context engineering, CLAUDE.md, skills, Claude Code CLI en contexto avanzado
- Experiencia real de delivery/adopción de CLI agents en empresa
- Claude Cowork para no-técnicos en contexto enterprise
- Nuevo framework/método/patrón para Claude Code
- Comparativa profunda CLI agents vs plataformas

El modelo es **opt-out**: QUIZÁ también pasa al scoring. Solo se descarta lo claramente irrelevante.

### Etapa 2 — Transcript

Solo para supervivientes del triage. Extrae transcript completo vía youtube-transcript MCP. Sin coste de quota YouTube API.

Si el transcript no está disponible, se usa título + descripción para el scoring.

### Etapa 3 — Scoring completo

Tres dimensiones ponderadas (1-10):

**A. Aplicabilidad directa a OPENLAB (×3)**
- 9-10: Integrable directamente en un skill o en el pitch a un cliente
- 7-8: Requiere adaptación pero tiene camino claro
- 5-6: Interesante pero teórico
- 1-4: Tangencial

**B. Novedad (×2)**
- 9-10: Completamente nuevo, no documentado
- 7-8: Combinación nueva o profundización significativa
- 5-6: Conocido pero bien explicado
- 1-4: Repetición

**C. Calidad de la fuente (×1)**
- 9-10: Experiencia real en producción con datos/resultados
- 7-8: Demo funcional con explicación técnica sólida
- 5-6: Buen análisis sin evidencia práctica
- 1-4: Opinión sin soporte

**Score final** = (A×3 + B×2 + C×1) / 6

Señales que suben el score A:
- Técnicas avanzadas no documentadas en docs oficiales
- Nuevos frameworks/métodos para Claude Code (BMAD, SPARC, etc.)
- Patrones de agent orchestration en producción
- Context engineering aplicado a procesos de negocio
- Casos reales de agentes en enterprise (no demos toy)
- Nuevas capacidades de MCP servers relevantes
- Argumentos de por qué CLI agents reemplazan n8n/Zapier/LangGraph
- Experiencias de agencias/freelancers entregando skills o CLI agents a clientes
- Adopción de CLI agents en empresas: training, champions, onboarding
- Claude Cowork como puente GUI para no-técnicos
- Pricing/packaging de servicios de IA agéntica basados en skills
- Governance y escalado de skills en organizaciones

### Etapa 4 — Output

**A. Briefing del día** → `briefs/daily-briefings/FECHA-briefing.md`
- Top 5 vídeos con score >= 7 (briefing completo)
- Menciones rápidas (6º-10º): una línea cada uno
- Tendencias del día

**B. Resumen individual por vídeo** → `briefs/CATEGORÍA/FECHA-slug.md`
- Solo para vídeos con score >= 7
- Incluye obligatoriamente: fecha, link, resumen ejecutivo, aplicabilidad OPENLAB, temas clave

---

## Sección "Aplicabilidad OPENLAB" en cada resumen

El evaluador lee los ficheros de contexto de OPENLAB antes de generar los resúmenes:

```
~/.claude/skills/opportunity-assessment/context/
├── openlab-sales-context.md      # Quiénes somos, qué entregamos, diferenciadores
├── platform-capabilities.md      # Stack técnico, capacidades del runtime
├── project-references.md         # Proyectos reales referenciables
└── pilot-templates.md            # Catálogo de pilots por categoría
```

Para cada vídeo genera:

- **Servicios que se refuerzan:** Qué pilot template o línea de servicio se beneficia del contenido del vídeo.
- **Referencias que conectan:** Proyectos reales de OPENLAB (Iberostar, VCs, etc.) que se relacionan.
- **Capacidades de plataforma:** Conexión con lo que ya soporta el stack (Claude Code CLI, MCP, skills, headless, etc.).
- **Oportunidades nuevas:** Servicios, pilots o argumentos comerciales que OPENLAB no tiene pero debería considerar.
- **Argumento comercial:** Una frase lista para usar con un cliente.

---

## Quota de YouTube Data API

Límite diario: 10.000 unidades.

| Operación | Coste | Cantidad | Total |
|-----------|-------|----------|-------|
| Resolver canal (channels.list) | 1 unit | 15 canales | 15 |
| Buscar vídeos por canal (search.list) | 100 units | 15 canales | 1.500 |
| Buscar por keywords (search.list) | 100 units | 18 keywords | 1.800 |
| Detalles de vídeos (videos.list) | 1 unit | ~3 calls | 3 |
| **Total estimado** | | | **~3.318** |

Margen amplio (~67% de la quota libre). Los transcripts se extraen vía MCP, sin coste de quota.

---

## Canales monitorizados

### Oficiales / Expertos de referencia
| Canal | Handle | Foco | Prioridad |
|-------|--------|------|-----------|
| Anthropic | @AnthropicAI | Releases oficiales, deep dives, Claude Code | Alta |
| Andrej Karpathy | @AndrejKarpathy | Context engineering, fundamentos LLM | Alta |

### Power users Claude Code / Agentic
| Canal | Handle | Foco | Prioridad |
|-------|--------|------|-----------|
| IndyDevDan | @indydevdan | Claude Code power user, skills, hooks, MCP | Alta |
| David Ondrej | @DavidOndrej | Claude Cowork, agent tools, comparativas | Alta |
| AI Jason | @AIJasonZ | Workflows agénticos, multi-agent | Alta |
| Sam Witteveen | @samwitteveen | Agent patterns avanzados, MCP | Media |
| Cole Medin | @ColeMedin | MCP servers, agent architectures, RAG, Claude Code infra | Alta |

### Curación y tendencias
| Canal | Handle | Foco | Prioridad |
|-------|--------|------|-----------|
| Matt Wolfe | @MattWolfe | Radar semanal de novedades IA | Media |
| Fireship | @Fireship | Resúmenes densos de tendencias tech/IA | Media |
| Latent Space | @LatentSpacePod | Entrevistas técnicas profundas | Media |
| AI Engineer | @aidotengineer | Conferencias, talks técnicas | Media |

### Español
| Canal | Handle | Foco | Prioridad |
|-------|--------|------|-----------|
| Dot CSV | @DotCSV | Divulgación IA técnica en español | Media |
| AI Agents Podcast | @aiagentspodcast | Casos de uso enterprise, Claude Cowork, adopción | Media |

### AI Agency / Delivery / Business
| Canal | Handle | Foco | Prioridad |
|-------|--------|------|-----------|
| Liam Ottley | @LiamOttley | AI automation agency, delivery, scaling | Media |
| Greg Isenberg | @gregisenberg | AI business ideas, productización | Media |

---

## Keywords (18, optimizadas para quota)

### context_engineering (5)
`context engineering`, `CLAUDE.md skills`, `skills architecture agent`, `context window optimization LLM`, `agent skills standard`

### claude_code_advanced (8)
`BMAD method claude`, `SPARC methodology claude`, `claude code hooks MCP`, `claude code headless automation`, `claude-flow worktree agents`, `Model Context Protocol server`, `claude code multi-agent`, `Claude Cowork enterprise`

### agentic_systems (5)
`multi-agent pipeline production`, `agent orchestration patterns`, `agent evaluation reliability`, `agentic RAG production`, `agent handoff memory patterns`

### enterprise_ai (4)
`AI knowledge worker enterprise`, `AI due diligence automation`, `AI competitive intelligence automation`, `generative AI enterprise workflows`

### cli_agents_vs_platforms (4)
`claude code vs cursor vs copilot`, `CLI agents vs n8n zapier langchain`, `zero dependency AI agents`, `plain text markdown agents`

### delivery_adoption (4)
`claude code enterprise deployment`, `AI agency claude code skills`, `AI skills governance scale`, `AI automation agency pricing model`

---

## Deduplicación

SQLite (`data/radar.db`) con `video_id` como primary key y `INSERT OR IGNORE`. Los vídeos ya encontrados no se reprocesan. Las búsquedas diarias son necesarias para descubrir contenido nuevo (últimas 24h).

---

## Filtros de calidad

- Duración mínima: 5 minutos (descarta shorts y clips)
- Duración máxima: 120 minutos (descarta streams sin editar)
- Términos de exclusión: "beginner tutorial", "getting started", "what is claude", "for beginners", etc.

---

## UX — Día a día

### Adición manual (en cualquier momento)

Desde el VPS o desde el laptop con Claude Code:

```
> añade este vídeo al radar: https://youtube.com/watch?v=XXX
```

Claude evalúa el vídeo con el mismo pipeline que el cron (transcript → triage → scoring → brief), lo guarda en la carpeta de categoría correcta y notifica por Telegram. No aparece en el briefing del día — entra directamente a la base de conocimiento.

Los briefs manuales llevan la marca `**Añadido:** manualmente` para distinguirlos.

### Mañana (2 minutos)

Mensaje de Telegram a las ~09:00 UTC:

```
OPENLAB Radar — Briefing 2026-04-02

Candidatos: 34 | Triage: 11 pasaron | Briefing: 4

---

1. Advanced Context Engineering Patterns for Enterprise Skills
   Canal: IndyDevDan | 18min
   Score: 8.7 | Aplicabilidad: 9 | Novedad: 9 | Calidad: 7
   Para OPENLAB: Patrón de progressive disclosure en skills multi-fase
   que resuelve el problema de contexto en due diligence largas.
   https://youtube.com/watch?v=xxx

2. ...

Mención rápida:
- How I deliver Claude Code to non-tech teams — Liam Ottley — 7.2
  https://youtube.com/watch?v=yyy
```

Respuestas posibles desde el móvil:
- "ok" → Claude confirma y cierra
- "el 1 y el 3 me interesan, descarta el resto"
- "añade también este: [URL de un vídeo encontrado manualmente]"

### Consulta (Claude Code)

```
> ¿Qué se ha dicho esta semana sobre context engineering?
```

Claude Code busca en `briefs/`, lee los resúmenes relevantes y sintetiza con citas. Sin límites, sin dependencias externas.

### Viernes — Digest semanal

Publicación automática en Canal Telegram (`t.me/openlabRadar`) + email al equipo (`gws gmail +send`). Rafael recibe aviso en chat privado.

```
OPENLAB Radar — Digest Semanal 24-30 mar 2026

Vídeos evaluados: 187 | Seleccionados: 23 | Media score: 7.8

Tendencias de la Semana:
1. Context engineering como disciplina separada de prompting...
2. Delivery de skills a enterprise como modelo de negocio...

Top 5:
1. "Enterprise Skills Governance at Scale" — IndyDevDan — 9.1
   Para OPENLAB: Framework de governance directamente aplicable
   al workshop DIBEX.
   https://youtube.com/watch?v=...

Aplicabilidad OPENLAB:
- El patrón de governance encaja con el cliente ISDI.
- Tema emergente "skills marketplace" relevante para catálogo OAF.
```

---

## Formato del resumen individual (.md)

Cada vídeo con score >= 7 genera un fichero en `briefs/CATEGORÍA/FECHA-slug.md`:

```markdown
# [Título del vídeo]

- **Fuente:** [URL](URL)
- **Canal:** nombre
- **Categoría:** categoría
- **Duración:** Xmin
- **Fecha:** YYYY-MM-DD
- **Score OPENLAB Radar:** X.X
  - Aplicabilidad: X
  - Novedad: X
  - Calidad: X

---

## Resumen ejecutivo

2-3 frases de qué va el vídeo.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** ...
- **Referencias que conectan:** ...
- **Capacidades de plataforma:** ...
- **Oportunidades nuevas:** ...
- **Argumento comercial:** ...

---

## Contenido detallado

Contenido sustantivo extraído del transcript — base de conocimiento reutilizable para generar posts, preparar charlas, cruzar ideas entre vídeos y construir argumentaciones.

### Ideas y argumentos principales
Tesis centrales del speaker con su razonamiento.

### Datos y evidencia
Números, benchmarks, métricas, casos de uso concretos.

### Citas textuales (2-4 máx)
Frases literales potentes. Formato: > "cita" — Speaker

### Ejemplos concretos
Demos, herramientas, workflows, repos mencionados.

---

## Temas clave

### 1. Tema principal
Detalle extraído del transcript.

### 2. Segundo tema
...
```

---

## Skills de Claude Code

| Skill | Dónde | Invocación |
|-------|-------|-----------|
| `radar-add-video` | VPS (`~/.claude/skills/`) | "añade este vídeo: URL" — desde sesión Claude Code en el VPS |
| `radar-add-video-remote` | Laptop (`~/.claude/skills/`) | "añade este vídeo al radar: URL" — SSH transparente al VPS |

Ambos skills ejecutan el mismo pipeline: transcript → triage → scoring → brief en `briefs/CATEGORÍA/` → `radar.db` → Telegraph → Telegram. No modifican el briefing diario.

---

## Dependencias

| Herramienta | Para qué | Estado |
|-------------|----------|--------|
| YouTube Data API v3 | Scraper (quota: 10K units/día, ~4.400 usados) | Configurada |
| youtube-transcript MCP | Extraer transcripts completos (sin límite quota) | Instalado |
| Telegram Bot (OPENLAB Radar Daily) | Briefing diario bidireccional (Rafael) | Configurado |
| Canal Telegram OPENLAB Radar | Digest semanal broadcast (t.me/openlabRadar) | Configurado |
| Telegraph (telegra.ph) | Briefs como Instant View en Telegram (lectura móvil) | Configurado |
| gws CLI (Google Workspace) | Email diario (Rafael) + digest semanal (equipo) | Configurado, OAuth Desktop app |
| nginx | Assets estáticos (logo emails HTML) en VPS | Configurado |
| rclone | Sincronizar briefs/ con Google Drive | Pendiente |

---

## Insights

Carpeta `insights/` para análisis y síntesis generados a petición desde los briefs acumulados. No son outputs automáticos del pipeline — se generan en sesiones de Claude Code con el contexto del radar.

**Sincronización:** `briefs/` e `insights/` se sincronizan con Google Drive vía rclone (pendiente de configurar en VPS). Son las dos carpetas pensadas para consumo del equipo.

Ejemplos de insights:
- Buenas prácticas de estructura de skills extraídas de los briefs
- Análisis de tendencias por categoría en un periodo dado
- Comparativas de frameworks mencionados en múltiples vídeos
- Argumentarios comerciales construidos desde casos reales

Para solicitar un insight: abrir Claude Code en el proyecto y pedir el análisis directamente. Claude buscará en `briefs/` y generará el documento en `insights/`.

---

## Decisiones de diseño

1. **Sin NotebookLM.** Claude Code con 1M de contexto lee 400+ resúmenes .md directamente. Sin límite de queries (vs 50/día free), sin límite de sources (vs 50 free), sin browser automation. Plain text, zero lock-in.

2. **youtube-transcript MCP para transcripts.** Sin coste de quota YouTube API. Permite evaluación con transcript completo en vez de solo título.

3. **Keywords optimizadas (111 → 18).** YouTube Data API tiene 10.000 unidades/día. Con 18 keywords usamos ~3.315, margen amplio.

4. **Canal Telegram sin comentarios.** Broadcast limpio, sin grupo de discusión vinculado que confunda al equipo.

5. **Telegraph para lectura móvil.** Los briefs se publican en telegra.ph y se abren como Instant View dentro de Telegram — sin salir de la app, con formato limpio. Sin duplicar ficheros ni ensuciar el directorio de briefs.

6. **VPS + rclone.** Solo monta la carpeta de briefs en el Drive compartido del equipo. Ruta de Drive pendiente de decisión.

7. **Contexto OPENLAB en cada resumen.** El evaluador lee los ficheros de sales, capabilities, references y pilots para generar aplicabilidad concreta — no genérica.
