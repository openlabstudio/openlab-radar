# Guía de uso — OPENLAB Radar

Todo lo que puedes hacer con el radar y cómo hacerlo.

---

## El radar en piloto automático

Cada mañana a las **09:00 CET** el sistema hace solo su trabajo:

1. Rastrea los 12 canales activos de YouTube monitorizados + 34 búsquedas por keywords
2. Evalúa cada vídeo en 4 etapas: triage → transcript → scoring 3D → brief
3. Te manda el **briefing del día** por email con los mejores vídeos ordenados por score
4. Actualiza el **KB Viewer** en HTML y sincroniza todo con **Google Drive**

Los viernes a las **09:30 CET** hace lo mismo pero en modo digest semanal, y el email va al equipo.

Cada día a las **10:30 CET** un health check automático revisa cobertura por categoría, distribución de scores, salud de tags y rendimiento de canales. Si detecta anomalías, te avisa por Telegram. Los viernes, el informe completo se integra en el digest semanal.

No tienes que hacer nada. Solo leer.

---

## Las 3 interfaces del radar

### 1. Email (uso diario)
El briefing llega cada mañana. Formato HTML con los vídeos del día ordenados por score. Lectura de 3-5 minutos.

Los viernes llega el digest semanal con el resumen de toda la semana.

### 2. KB Viewer — web + Drive (escaneo visual)
Dashboard interactivo con todos los briefs del radar. Tres formas de acceder:

- **Web (compartible):** [`openlabstudio.com/radar/`](https://www.openlabstudio.com/radar/) — embebido en la web de OPENLAB con header/footer del site. URL directa para compartir con quien quieras. Se actualiza automáticamente cada día.
- **Web (directa):** [`radar.openlabstudio.com`](https://radar.openlabstudio.com) — el dashboard sin embeber, a pantalla completa. Mismo contenido que la versión embebida.
- **Drive (offline):** doble clic en `kb_viewer.html` desde Drive for Desktop. Mismo contenido, funciona sin conexión.

Vistas:
- **Hot Signals** — top briefs de los últimos 7 días (score ≥ 8.0)
- **Por categoría** — context-engineering, claude-code-advanced, agentic-systems, enterprise-ai, cli-vs-platforms, delivery-adoption
- **Tag Explorer** — filtra por tags (commercial-argument, skill-pattern, case-study, etc.)
- **Buscador** — búsqueda libre en títulos y resúmenes

Stats: total briefs, score medio, briefs esta semana, canales monitorizados.

Cada card tiene links a **YouTube** (vídeo original) y **VER RESUMEN** (Telegraph, lectura rápida).

Ruta en Drive: `OPENLAB-RADAR/kb_viewer.html`

### 3. Claude Code (todo lo demás)
Desde aquí puedes hacer todo lo que no es automático: añadir vídeos, consultar briefs, generar insights. Ver secciones siguientes.

---

## Añadir un vídeo manualmente

Flujo recomendado en dos pasos:

### Paso 1 — Check previo (¿vale la pena?)
Di:
> "¿vale la pena añadir este vídeo? [URL]"

El skill conecta al VPS y ejecuta allí el análisis completo: transcript → triage → score estimado → búsqueda de cobertura en los briefs existentes. Te devuelve:
- **AÑADIR / NO AÑADIR / VALORAR** con justificación
- Score estimado y categoría probable
- Si hay solapamiento: qué briefs lo cubren ya y en qué se diferencia este

Si la recomendación es positiva, te pregunta si quieres añadirlo ahora mismo.

### Paso 2 — Añadir al radar
Si saltas el check previo o confirmas desde ahí:
> "añade este vídeo al radar: [URL]"

El pipeline completo: transcript → triage → scoring → brief en `briefs/CATEGORÍA/` → Telegraph → Telegram. No toca el briefing del día ni la DB de candidatos.

---

## Consultar los briefs

### Búsqueda en lenguaje natural (Claude Code)

Pregunta directamente y Claude busca en `briefs/` para sintetizar:

> "¿Qué dicen los briefs sobre context engineering esta semana?"
> "¿Qué vídeos hablan de delivery de skills a clientes?"
> "¿Hay algún brief con argumento comercial para vender a empresas sin código?"
> "Dame los briefs con tag commercial-argument ordenados por score"
> "¿Qué canales han publicado más contenido sobre agentic systems este mes?"

Claude cita los .md relevantes con el score y la categoría.

### Búsqueda estructurada (radar_search.py)

Para filtros precisos por score, categoría, tags, fecha o sub-scores, usa el CLI de búsqueda directamente en el VPS:

```bash
# Top briefs por score
python3 scripts/radar_search.py --score-min 8.5 --sort score

# Briefs de una categoría con un tag específico
python3 scripts/radar_search.py --category context-engineering --tag mcp

# Briefs con alta aplicabilidad directa
python3 scripts/radar_search.py --aplicabilidad-min 9 --sort score

# Briefs de un canal concreto en un rango de fechas
python3 scripts/radar_search.py --source "Simon Scrapes" --date-from 2026-05-01

# Búsqueda de texto libre en el contenido
python3 scripts/radar_search.py --text "harness" --sort score

# Solo daily-briefings o weekly-digests
python3 scripts/radar_search.py --type daily-briefing
python3 scripts/radar_search.py --type weekly-digest

# Estadísticas globales del radar
python3 scripts/radar_search.py --stats

# Output JSON para automatización
python3 scripts/radar_search.py --score-min 8 --format json
```

Todos los filtros se combinan con AND. Output por defecto: tabla con fecha, score, sub-scores (A/N/C), categoría y título.

### Búsqueda semántica (QMD)

QMD es un motor de búsqueda semántica local que encuentra briefs por significado, no solo por keywords exactos. Ideal para preguntas como "¿qué briefs hablan de seguridad en agentes?" aunque ninguno use esas palabras exactas.

Si tienes QMD instalado, Claude Code lo usa automáticamente como herramienta MCP. No necesitas hacer nada especial — simplemente pregunta y Claude decidirá si usar QMD, Grep o ambos.

#### Setup QMD (una vez por miembro del equipo)

Requisitos: Node.js 18+, ~2GB de disco para modelos, acceso a los briefs vía Google Drive for Desktop.

```bash
# 1. Instalar QMD
npm install -g @tobilu/qmd

# 2. Crear colección apuntando a los briefs en Drive
#    Ajustar la ruta según tu sistema operativo:
#    macOS: /Users/TU_USUARIO/Library/CloudStorage/GoogleDrive-TU_EMAIL/Shared drives/OPENLAB-RADAR/briefs
#    Linux: ~/Google Drive compartidas/OPENLAB-RADAR/briefs (o la ruta que configure Drive)
qmd collection add "/RUTA/A/TU/DRIVE/OPENLAB-RADAR/briefs" --name radar --pattern "**/*.md"

# 3. Añadir contexto (mejora la calidad de búsqueda)
qmd context add qmd://radar/ "OPENLAB Radar knowledge base: intelligence briefs about context engineering, Claude Code, agentic systems, enterprise AI, and delivery/adoption. YAML frontmatter with score, category, tags, score_breakdown."

# 4. Generar embeddings (~36s, descarga modelos la primera vez ~2GB)
qmd embed

# 5. Registrar como MCP server en Claude Code
claude mcp add qmd -s user -- qmd mcp

# 6. Verificar
qmd status
```

Tras el setup, Claude Code puede usar QMD automáticamente en cualquier proyecto.

#### Mantener el índice actualizado

Los briefs nuevos llegan vía rclone → Drive → Drive for Desktop. Para re-indexar:

```bash
qmd update -q && qmd embed
```

Esto tarda ~2-5 segundos para unos pocos briefs nuevos. No es necesario hacerlo cada día — el índice sigue siendo útil aunque tenga 1-2 días de retraso.

---

## Generar un insight

Un insight es un documento de síntesis que pides cuando quieres profundizar en un tema a partir de lo acumulado en el radar.

**Dónde:** desde tu laptop, en cualquier sesión de Claude Code. Los briefs ya están en el Shared Drive, así que Claude los lee directamente y guarda el insight en `insights/`. Como el Drive es compartido, el insight está disponible para todo el equipo inmediatamente.

Di simplemente:
> "Genera un insight sobre por qué los CLI agents superan a n8n para procesos de negocio"
> "Sintetiza todo lo que el radar ha captado sobre context engineering en los últimos 30 días"
> "Genera un insight sobre cómo están entregando skills a clientes las agencias que siguen el radar"

El insight incluye: síntesis de los briefs relevantes, patrones detectados, implicaciones para OPENLAB y argumentos comerciales listos para usar. Se guarda como `insights/FECHA-slug.md`.

---

## Cheatsheet de frases de activación

| Qué quieres hacer | Qué decir / hacer |
|---|---|
| Check previo de un vídeo | `"¿vale la pena este vídeo? [URL]"` |
| Añadir un vídeo al radar | `"añade este vídeo: [URL]"` |
| Consultar briefs por tema | `"¿qué dicen los briefs sobre [tema]?"` |
| Consultar briefs por tag | `"dame los briefs con tag [tag]"` |
| Generar un insight | `"genera un insight sobre [tema] en insights/"` |
| Ver qué hay en el radar | `"¿cuántos briefs tenemos por categoría?"` |
| Ver los mejores briefs | `"¿cuáles son los briefs con score más alto este mes?"` |
| Búsqueda estructurada | `python3 scripts/radar_search.py --score-min 8 --sort score` |
| Filtrar por sub-score | `python3 scripts/radar_search.py --aplicabilidad-min 9` |
| Estadísticas del radar | `python3 scripts/radar_search.py --stats` |

---

## Tags disponibles para búsquedas

**Técnicos:** `context-engineering` · `token-optimization` · `skill-design` · `agent-architecture` · `multi-agent` · `mcp` · `context-window` · `evaluation` · `tool-use` · `knowledge-management` · `long-running-agents` · `harness-engineering` · `enterprise-ai` · `knowledge-capture` · `financial-analysis` · `market-intelligence` · `data-integration` · `output-formatting` · `ai-governance`

**Relevancia OPENLAB:** `commercial-argument` · `client-delivery` · `skill-pattern` · `new-service` · `workshop-material` · `competitive-intel` · `business-case-generation`

**Tipo de señal:** `trend` · `technical-deep-dive` · `case-study` · `opinion` · `tutorial`

**Entidades:** `anthropic` · `openai` · `google` · `claude-code` · `langchain` · `cursor` · `n8n`

---

## Estado del sistema

| Componente | Estado |
|---|---|
| Scraper YouTube + cron diario | ✅ Activo |
| Evaluador + briefs individuales | ✅ Activo |
| Email diario | ✅ Activo |
| rclone → Google Drive | ✅ Activo |
| KB Viewer HTML (Drive) | ✅ Activo |
| KB Viewer Web (`openlabstudio.com/radar/` + `radar.openlabstudio.com`) | ✅ Activo |
| Skill check previo (`radar-check-video`) | ✅ Activo |
| Skill añadir vídeo remoto (`radar-add-video-remote`) | ✅ Activo |
| Health Check (fitness functions) | ✅ Activo (alertas diarias + informe semanal) |
| Búsqueda estructurada (`radar_search.py`) | ✅ Activo |
| Frontmatter enriquecido (score_breakdown, duration, secondary_category) | ✅ Activo |
| Email digest semanal al equipo | ⏳ Pendiente auth gws |
