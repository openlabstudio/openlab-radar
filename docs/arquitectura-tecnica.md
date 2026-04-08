# Arquitectura Técnica — OPENLAB Radar

> Documento de referencia para construir sistemas equivalentes en clientes.
> Versión: 2026-04-01

---

## 1. Qué es este sistema

Sistema de inteligencia continua que monitoriza YouTube diariamente para detectar contenido relevante para un dominio de conocimiento específico. Evalúa vídeos con Claude Code en modo headless y genera resúmenes estructurados en Markdown con aplicabilidad directa al negocio del cliente.

**Piezas:**
- Scraper de YouTube (Python + YouTube Data API v3)
- Evaluador con IA (Claude Code CLI headless)
- MCP server propio para transcripts (Python + FastMCP)
- Knowledge base en Markdown con frontmatter YAML
- Dashboard HTML self-contained (KB Viewer)
- Distribución vía Telegram, Telegraph, email HTML, Google Drive y web (`openlabstudio.com/radar/`)

**Stack:**
```
Python 3.12 + Bash + Claude Code CLI + MCP + SQLite
YouTube Data API v3 + youtube-transcript-api + Webshare proxy
Telegram Bot API + Telegraph API + rclone + Google Drive
nginx + Let's Encrypt + WordPress/Elementor (iframe embed)
```

---

## 2. Infraestructura

### 2.1 Tres nodos sincronizados

```
┌─────────────────────────────────────────────────────┐
│  VPS (Ubuntu 22.04) — FUENTE DE VERDAD              │
│  /home/openlab/openlab-radar/                       │
│                                                     │
│  Toda la ejecución ocurre aquí:                     │
│  crons, scraper, Claude headless, MCP server        │
└─────────────────────────────────────────────────────┘
         │ git push                    │ rclone sync
         ▼                             ▼
┌──────────────────┐     ┌─────────────────────────────┐
│  GitHub repo     │     │  Google Shared Drive         │
│                  │     │                             │
│  Código, docs,   │     │  briefs/, insights/,        │
│  prompts,        │     │  kb_viewer.html             │
│  CLAUDE.md       │     │  (contenido generado)       │
│  (sin .env ni    │     └─────────────────────────────┘
│  briefs)         │                  │ Drive for Desktop
└──────────────────┘                  ▼
         │ git pull         ┌──────────────────────────┐
         ▼                  │  Laptop del cliente      │
┌──────────────────┐        │  Acceso local a briefs   │
│  Laptop (ref.)   │        │  e insights sin SSH      │
│  Solo docs y     │        └──────────────────────────┘
│  config          │
└──────────────────┘
```

**Regla clave:** toda ejecución ocurre en el VPS. El laptop es solo consulta.

### 2.2 Requisitos del VPS

- Ubuntu 22.04 LTS (mínimo 2GB RAM, 20GB disco)
- Python 3.12
- Claude Code CLI instalado y autenticado
- rclone configurado con Google Drive
- crontab activo para usuario no-root

---

## 3. Estructura del proyecto

```
proyecto-radar/
├── briefs/                          # Knowledge base (sincronizar con Drive)
│   ├── daily-briefings/             # YYYY-MM-DD-briefing.md
│   ├── CATEGORÍA-1/                 # briefs individuales por categoría
│   ├── CATEGORÍA-2/
│   └── ...
├── insights/                        # Análisis bajo demanda (sincronizar con Drive)
├── config/
│   ├── .env                         # Credenciales (en .gitignore)
│   ├── channels.yaml                # Canales a monitorizar
│   ├── keywords.yaml                # Keywords + filtros de calidad
│   └── tags.yaml                    # Taxonomía oficial de tags
├── prompts/
│   ├── evaluate-daily.md            # Evaluador diario (4 etapas)
│   ├── evaluate-manual.md           # Evaluador de un vídeo manual
│   ├── evaluate-check.md            # Check previo (sin generar brief)
│   └── weekly-digest.md             # Digest semanal
├── scripts/
│   ├── run_daily.sh                 # Pipeline diario (invocado por cron)
│   ├── run_recovery.sh              # Recuperación si el pipeline diario falló
│   ├── run_weekly.sh                # Pipeline semanal
│   ├── scraper.py                   # YouTube Data API scraper
│   ├── mcp_transcript_server.py     # MCP server para transcripts
│   ├── add_video.sh                 # Añadir vídeo manualmente
│   ├── check_video.sh               # Check previo de un vídeo
│   ├── notify.py                    # Notificaciones Telegram
│   ├── publish_telegraph.py         # Publicar en Telegraph
│   ├── generate_kb_viewer.py        # Dashboard HTML del KB
│   ├── md_to_email_html.py          # Briefing → HTML email
│   └── md_to_weekly_html.py         # Digest → HTML email
├── data/
│   ├── radar.db                     # SQLite (vídeos procesados)
│   ├── kb_viewer.html               # Dashboard HTML (sincronizar con Drive)
│   ├── logs/
│   │   ├── cron-daily.log
│   │   ├── cron-weekly.log
│   │   └── run-YYYY-MM-DD.log
│   └── candidates-YYYY-MM-DD.json   # Candidatos del scraper
├── docs/
│   └── arquitectura-tecnica.md      # Este documento
├── .mcp.json                        # Configuración MCP del proyecto
├── .gitignore                       # Excluye: config/.env, data/, briefs/
└── CLAUDE.md                        # Instrucciones del proyecto para Claude
```

---

## 4. Base de datos (SQLite)

**Fichero:** `data/radar.db`
**Tabla única:** `videos`

```sql
CREATE TABLE videos (
    video_id           TEXT PRIMARY KEY,
    title              TEXT NOT NULL,
    channel_name       TEXT,
    channel_handle     TEXT,
    description        TEXT,
    published_at       TEXT,          -- ISO 8601
    duration_seconds   INTEGER,
    url                TEXT,
    thumbnail_url      TEXT,
    view_count         INTEGER DEFAULT 0,
    lang               TEXT DEFAULT 'en',
    discovered_at      TEXT NOT NULL, -- ISO 8601 UTC
    status             TEXT DEFAULT 'candidate',
                                      -- 'candidate' | 'briefing' | 'manual'
    score              REAL DEFAULT 0,
    categories         TEXT,          -- JSON array: ["context-engineering"]
    briefing_date      TEXT,          -- YYYY-MM-DD
    ingested_to_notebooklm INTEGER DEFAULT 0
);

CREATE INDEX idx_status    ON videos(status);
CREATE INDEX idx_discovered ON videos(discovered_at);
```

**Flujo de estados:**
```
discovered → candidate → briefing   (si score ≥ umbral)
                       → descartado  (si score < umbral o triage NO)
          → manual                  (añadido manualmente con add_video.sh)
```

---

## 5. Configuración (YAML)

### 5.1 `config/channels.yaml`

```yaml
channels:
  - handle: "@NombreDelCanal"
    name: "Nombre visible"
    focus: "descripción del foco temático"
    priority: high     # high | medium
    lang: en           # en | es
```

**Criterios de selección de canales:**
- Creadores con historial de contenido avanzado (no divulgativo)
- Relevantes para el dominio del cliente
- Preferir creadores con transcripts automáticos activados

### 5.2 `config/keywords.yaml`

```yaml
# Umbrales de calidad
min_score_briefing: 7      # Score mínimo para top vídeos
max_videos_briefing: 5     # Máx en "Top del Día"
lookback_hours: 24         # Ventana de búsqueda del scraper

# Keywords organizadas por categoría
categories:
  nombre_categoria:
    keywords:
      - "término exacto 1"
      - "término exacto 2"
  otra_categoria:
    keywords:
      - ...

# Exclusiones globales (se aplican a todos los candidatos)
exclude_terms:
  - "beginner tutorial"
  - "getting started"
  - "what is X"
  - "for beginners"
  # ... términos de bajo valor

# Filtros técnicos de calidad
quality_filters:
  min_duration_minutes: 5    # Descartar vídeos muy cortos
  max_duration_minutes: 120  # Descartar directos/webinars muy largos
```

**Optimización de quota YouTube API (10.000 units/día):**
- Cada canal: ~100 units/búsqueda
- Cada keyword: ~100 units/búsqueda
- Target: < 5.000 units/día para dejar margen

### 5.3 `config/tags.yaml`

```yaml
# Taxonomía de tags para los briefs (usar solo los de esta lista)
technical:
  - context-engineering
  - skill-design
  - agent-architecture
  - multi-agent
  - mcp
  - evaluation
  - tool-use
  - knowledge-management
  - long-running-agents
  # ... tags técnicos del dominio

openlab_relevance:            # Sustituir por relevance del cliente
  - commercial-argument
  - client-delivery
  - skill-pattern
  - new-service
  - workshop-material

signal_type:
  - trend
  - technical-deep-dive
  - case-study
  - opinion
  - tutorial

entities:                     # Actores clave del dominio
  - anthropic
  - openai
  # ... empresas/proyectos relevantes
```

**Regla de aplicación:** 3-6 tags por brief: ≥1 técnico + ≥1 relevancia + 1 signal_type.

### 5.4 `config/.env`

```bash
# YouTube Data API v3
YOUTUBE_API_KEY=""

# Telegram (bot de notificaciones)
TELEGRAM_BOT_TOKEN=""
TELEGRAM_CHAT_ID=""          # Chat privado del responsable
TELEGRAM_CHANNEL_ID=""       # Canal broadcast del equipo (opcional)

# Telegraph (Instant View en Telegram)
TELEGRAPH_ACCESS_TOKEN=""    # Se genera automáticamente en primer uso

# Email digest
DIGEST_EMAIL_RECIPIENTS=""   # comma-separated

# Google Workspace CLI (para envío de email)
GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file

# Google Drive (rclone)
GDRIVE_BRIEFS_PATH="gdrive:briefs"
GDRIVE_INSIGHTS_PATH="gdrive:insights"
GDRIVE_RADAR_ROOT="gdrive:"

# Claude Code headless (NO usar ANTHROPIC_API_KEY — factura por token)
CLAUDE_CODE_OAUTH_TOKEN=""   # Generado con `claude setup-token` (~1 año)

# Proxy residencial para transcripts de YouTube
# Registrarse en webshare.io → "Residential" (rotating) proxies
WEBSHARE_USERNAME=""
WEBSHARE_PASSWORD=""
# Alternativa genérica: YOUTUBE_PROXY_URL="http://user:pass@host:port"
```

---

## 6. Pipeline diario

**Cron:** `0 8 * * *` — 08:00 UTC (09:00 CET)
**Script:** `scripts/run_daily.sh`

### Paso 1 — Scraper

```
scripts/scraper.py
```

**Proceso:**
1. Resuelve handles de canales → channel_ids (YouTube API)
2. Busca vídeos de las últimas 24h por canal (`search().list`)
3. Busca por keywords (`search().list`, 5 resultados/keyword)
4. Deduplicación por `video_id`
5. Obtiene metadatos completos (`videos().list`: duración, views)
6. Aplica filtros de calidad (duración, idioma, exclude_terms)
7. Guarda en SQLite (`status='candidate'`)
8. Exporta `data/candidates-YYYY-MM-DD.json`

**Output típico:** 10-30 candidatos/día

**Quota estimada:** N_canales × 100 + N_keywords × 100 units

### Paso 2 — Evaluador (Claude headless)

```bash
claude -p "$(cat prompts/evaluate-daily.md)

Fecha de hoy: $TODAY
Fichero de candidatos: $CANDIDATES_FILE

Lee el fichero y genera el briefing. Guarda el resultado en: $BRIEFING_FILE" \
  --allowedTools "Read,Write,Glob,mcp__youtube-transcript__get_transcript" \
  --output-format text
```

**Retry automático:** si `claude -p` falla (p.ej. API overloaded — error 529), el pipeline reintenta hasta 3 veces con 15 minutos de espera entre intentos. Tras el tercer fallo, envía alerta Telegram y aborta.

**4 etapas internas del prompt:**

**Etapa 1 — Triage rápido** (solo título + canal + descripción):
```
SÍ   → pasa a Etapa 2
QUIZÁ → pasa a Etapa 2
NO   → descartado (registra motivo)
```

Señales de descarte rápido: tutoriales básicos, vibe coding, n8n/Zapier/plataformas, clickbait, vídeo privado, idioma no soportado.

**Etapa 2 — Transcript** (solo SÍ y QUIZÁ):
```
mcp__youtube-transcript__get_transcript(url=VIDEO_URL, lang="en")
```
Si falla → continúa con título + descripción (score penalizado en C).

**Etapa 3 — Scoring** (score final = A×3 + B×2 + C×1 / 6):

| Dimensión | Peso | Criterio |
|-----------|------|----------|
| A. Aplicabilidad directa al cliente | ×3 | ¿Se usa mañana en un proyecto real? |
| B. Novedad | ×2 | ¿Es algo que el cliente no sabe? |
| C. Calidad de la fuente | ×1 | ¿Hay evidencia real o es opinión? |

**Etapa 4 — Output:**

```
briefs/daily-briefings/YYYY-MM-DD-briefing.md   ← briefing del día
briefs/CATEGORÍA/YYYY-MM-DD-slug-titulo.md       ← brief individual (score ≥ 7)
stdout                                            ← briefing (para Telegram)
```

**Formato briefing diario:**
```markdown
# Radar — Briefing YYYY-MM-DD

**Candidatos:** X | **Triage:** Y pasaron | **Briefing:** N | **Mención:** M

## Top Vídeos del Día
*(solo score ≥ 7.0)*

### 1. [Título](URL)
- **Canal:** nombre
- **Score:** X.X (Aplicabilidad: X · Novedad: X · Calidad: X)
- **Para el cliente:** qué puedes hacer con esto (no de qué va el vídeo)

## Mención rápida
*(solo score ≥ 6.0, máx 2)*
- [Título](URL) — canal — X.X — categoría — Una frase.

## Tendencias
Patrón entre los vídeos del día. 2-3 líneas.
```

**Formato brief individual:**
```markdown
---
title: "Título del vídeo"
date: YYYY-MM-DD
category: nombre-categoría
score: X.X
tags:
  - tag1
  - tag2
source: nombre del canal
url: https://youtube.com/watch?v=ID
---

# Título del vídeo

- **Score:** X.X (Aplicabilidad: X · Novedad: X · Calidad: X)

## Resumen ejecutivo
2-3 frases.

## Aplicabilidad [cliente]
- **Servicios que se refuerzan:** ...
- **Oportunidades nuevas:** ...
- **Argumento comercial:** Una frase lista para usar.

## Contenido detallado
### Ideas y argumentos principales
### Datos y evidencia
### Citas textuales (2-4 máx)
### Ejemplos concretos

## Temas clave
### 1. Tema
### 2. Tema
```

### Paso 3 — Telegraph (Instant View)

```
scripts/publish_telegraph.py [lista de briefs individuales de hoy]
```

- Convierte cada `.md` a HTML (strip frontmatter)
- Publica vía Telegraph API
- Escribe URL de vuelta en el `.md`: `- **Telegraph:** URL`
- Envía links al chat de Telegram del responsable

### Paso 4 — Email diario

```
scripts/md_to_email_html.py briefs/daily-briefings/YYYY-MM-DD-briefing.md
gws gmail +send --to responsable@cliente.com --subject "Radar — YYYY-MM-DD" --body "$HTML" --html
```

### Paso 4b — KB Viewer HTML

```
scripts/generate_kb_viewer.py --briefs-dir briefs/ --insights-dir insights/ --output data/kb_viewer.html
```

Dashboard interactivo self-contained: búsqueda, filtros, stats, hot signals.

### Paso 5 — Sync Google Drive

```bash
rclone sync ./briefs/    "${GDRIVE_BRIEFS_PATH}"   --quiet
rclone sync ./insights/  "${GDRIVE_INSIGHTS_PATH}" --quiet
rclone copyto ./data/kb_viewer.html "${GDRIVE_RADAR_ROOT}/kb_viewer.html" --quiet
```

---

## 7. Pipeline semanal

**Cron:** `30 8 * * 5` — 08:30 UTC viernes (09:30 CET)
**Script:** `scripts/run_weekly.sh`

```
1. claude -p prompts/weekly-digest.md   → briefs/weekly-digests/YYYY-MM-DD.md
2. publish_telegraph.py                 → link Telegram al canal del equipo
3. md_to_weekly_html.py + gws           → email HTML a todo el equipo
4. rclone sync                          → Drive
```

**El digest semanal incluye:**
- Top 5 vídeos de la semana
- 2-3 tendencias detectadas
- Gaps por categoría
- Recomendaciones de acción

---

## 8. MCP Server — YouTube Transcript

### Por qué es necesario

YouTube bloquea IPs de datacenter (VPS en cloud providers: Hetzner, DigitalOcean, AWS, etc.) para peticiones de transcripts. La librería `youtube-transcript-api` lanza `IpBlocked` en estos casos.

**Solución:** proxy residencial rotativo (Webshare) que enruta las peticiones desde IPs domésticas.

### Implementación

**Fichero:** `scripts/mcp_transcript_server.py`
**Registrado en:** `.mcp.json`

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "type": "stdio",
      "command": "python3",
      "args": ["/ruta/absoluta/al/proyecto/scripts/mcp_transcript_server.py"]
    }
  }
}
```

**Tool expuesta:** `get_transcript(url: str, lang: str = "en") -> str`

**Lógica de proxy (en orden de prioridad):**
```python
from youtube_transcript_api.proxies import WebshareProxyConfig, GenericProxyConfig

def _build_proxy_config():
    # 1. Webshare rotating residential (recomendado)
    username = os.environ.get("WEBSHARE_USERNAME", "").strip()
    password = os.environ.get("WEBSHARE_PASSWORD", "").strip()
    if username and password:
        return WebshareProxyConfig(
            proxy_username=username,
            proxy_password=password,
            retries_when_blocked=5,   # reintentos automáticos con nueva IP
        )
    # 2. Proxy genérico (fallback)
    proxy_url = os.environ.get("YOUTUBE_PROXY_URL", "").strip()
    if proxy_url:
        return GenericProxyConfig(http_url=proxy_url, https_url=proxy_url)
    # 3. Sin proxy (solo funciona si la IP no está bloqueada)
    return None
```

**Fallback de idioma:**
```
lang solicitado → "en" → cualquier transcript disponible
```

**Dependencias:**
```
youtube-transcript-api==1.2.4   (clase WebshareProxyConfig built-in)
mcp==1.26.0                     (FastMCP stdio server)
```

**Instalación:**
```bash
pip install youtube-transcript-api==1.2.4 mcp --break-system-packages
```

### Setup Webshare

1. Crear cuenta en webshare.io
2. Ir a **"Residential"** → **"Rotating Residential"** (NO "Static Residential")
3. Copiar `proxy_username` y `proxy_password` del dashboard
4. Añadir a `config/.env`:
   ```bash
   WEBSHARE_USERNAME="tu-usuario"
   WEBSHARE_PASSWORD="tu-password"
   ```
5. Verificar:
   ```bash
   source config/.env && python3 -c "
   from youtube_transcript_api import YouTubeTranscriptApi
   from youtube_transcript_api.proxies import WebshareProxyConfig
   import os
   api = YouTubeTranscriptApi(proxy_config=WebshareProxyConfig(
       proxy_username=os.environ['WEBSHARE_USERNAME'],
       proxy_password=os.environ['WEBSHARE_PASSWORD'],
   ))
   t = api.fetch('dQw4w9WgXcQ')
   print('OK:', t.to_raw_data()[0]['text'][:80])
   "
   ```

**Coste estimado:** sin plan gratuito. ~$5/mes por 1 GB (suficiente para < 50 vídeos/día). Planes mayores hasta ~$20/mes.

---

## 9. Autenticación Claude Code headless

**Problema:** `claude -p` en crons usa un token OAuth interactivo que caduca.

**Solución:** `CLAUDE_CODE_OAUTH_TOKEN` generado con `claude setup-token` (~1 año de vigencia).

```bash
# Generar token (requiere sesión interactiva en el VPS)
claude setup-token

# Copiar el token generado a config/.env
CLAUDE_CODE_OAUTH_TOKEN="sk-ant-oat01-..."
```

**⚠️ No usar `ANTHROPIC_API_KEY`** en crons: si está en el entorno, `claude -p` factura por token en lugar de usar la suscripción Max.

**Renovación:** ejecutar `claude setup-token` cada ~1 año.

---

## 10. Crons

```bash
# Ver crontab: crontab -l (como usuario no-root)
# Editar: crontab -e

# Pipeline diario — 07:00 UTC (09:00 CEST)
0 7 * * * cd /ruta/proyecto && bash scripts/run_daily.sh >> data/logs/cron-daily.log 2>&1

# Digest semanal — 07:30 UTC viernes (09:30 CEST)
30 7 * * 5 cd /ruta/proyecto && bash scripts/run_weekly.sh >> data/logs/cron-weekly.log 2>&1

# Recuperación diaria — 09:00 UTC (11:00 CEST)
# Comprueba si el briefing de hoy existe; si no, relanza evaluador + KB Viewer + sync.
# Cubre fallos del pipeline principal (API overloaded, timeout, etc.)
0 9 * * * cd /ruta/proyecto && bash scripts/run_recovery.sh
```

**Logs:** `data/logs/cron-recovery.log`

---

## 11. Sistema de notificaciones

### Telegram

**Bot:** creado en @BotFather, token en `TELEGRAM_BOT_TOKEN`

**Dos destinos:**
- `TELEGRAM_CHAT_ID`: chat privado del responsable
- `TELEGRAM_CHANNEL_ID`: canal del equipo (links Telegraph + digest semanal)

**Dos tipos de mensajes:**
1. **Contenido** — briefing diario completo (vía `notify.py <briefing_file> --telegram-only`)
2. **Estado** — confirmaciones y alertas del pipeline (vía `notify.py --status "mensaje"`)

**Mensajes de estado del pipeline diario:**
- `⚠️ ALERTA` al inicio si `youtube-transcript-api` falla el health check
- `✅ Pipeline diario completado` al final con resumen: candidatos, briefs generados, estado email
- `⚠️ ALERTA` si el email falla al enviarse
- `🚨 ERROR` si el pipeline muere inesperadamente (trap ERR)

**Mensajes de estado del digest semanal:**
- `✅ Digest semanal completado` con confirmación de email y link Telegraph
- `⚠️ ALERTA` si el email falla al enviarse
- `🚨 ERROR` si el pipeline muere inesperadamente (trap ERR)

**Chunking:** si el mensaje supera 4.096 chars, se divide automáticamente.

### Health check de youtube-transcript-api

Antes de cada pipeline diario, `run_daily.sh` verifica que `youtube-transcript-api` puede obtener un transcript real (vídeo de test fijo). Si falla:
- Se envía alerta Telegram inmediata con el error específico (`IP_BLOCKED`, `ERROR:...`)
- El pipeline continúa pero los briefs se generan solo con título + descripción (calidad reducida)

Esto detecta roturas de la librería (cambios en endpoints internos de YouTube) o bloqueos de IP antes de que el pipeline completo falle silenciosamente.

### Telegraph (Instant View)

Los briefs se publican en telegra.ph para que se abran como Instant View dentro de Telegram (sin salir de la app, ideal para móvil).

**Flujo:**
```
brief.md → strip frontmatter → conversión MD→HTML → Telegraph API → URL
```
La URL se escribe de vuelta en el `.md`: `- **Telegraph:** https://telegra.ph/...`

### Email HTML

**Herramienta:** `gws` (Google Workspace CLI)
```bash
gws gmail +send --to destinatario@empresa.com --subject "..." --body "$HTML" --html
```

**Templates:**
- `md_to_email_html.py` — briefing diario
- `md_to_weekly_html.py` — digest semanal

---

## 12. KB Viewer (dashboard HTML)

**Generado por:** `scripts/generate_kb_viewer.py`
**Output:** `data/kb_viewer.html` (fichero único, self-contained, ~60KB)

**Características:**
- Sin dependencias externas (CSS y JS embebidos, logo en base64)
- Google Fonts (Montserrat) como única dependencia externa
- Búsqueda full-text client-side (regex sobre títulos, fuentes, tags y excerpts)
- Filtros por categoría, tags
- Hot signals: briefs con score ≥ 8.0 en los últimos 7 días
- Stats bar: total briefs, score medio, briefs esta semana, canales únicos
- Links directos a YouTube y Telegraph ("VER RESUMEN")
- Excerpts limpios: sin scores (Aplicabilidad/Novedad/Calidad), sin markdown, cortados en frase completa

**Proceso de generación:**
1. Lee todos los `.md` de `briefs/` (excepto `daily-briefings/`)
2. Parsea frontmatter YAML de cada brief
3. Limpia excerpts: elimina líneas de scoring, strips markdown (`**`, `*`), corta en frase completa (~250 chars)
4. Computa estadísticas (total, avg score, canales únicos)
5. Embebe datos como JSON en el HTML
6. Genera HTML completo con interactividad JS

**Distribución (3 vías):**

1. **Web pública:** nginx en el VPS sirve el fichero en `https://radar.openlabstudio.com/`
   - Registro DNS A: `radar.openlabstudio.com` → `212.227.104.123` (GoDaddy)
   - SSL: Let's Encrypt con auto-renewal (`certbot --nginx`)
   - Config: `/etc/nginx/sites-available/radar-viewer`
   - Headers: `Content-Security-Policy: frame-ancestors https://openlabstudio.com`
   - Cache: `max-age=3600` (1 hora)

2. **WordPress embed:** página en `openlabstudio.com/radar/` (post 949, Elementor)
   - Widget HTML con iframe apuntando a `https://radar.openlabstudio.com/`
   - Mantiene header/footer del theme de WordPress
   - No enlazada desde ninguna otra página (acceso solo por URL directa)
   - No requiere actualización: el iframe siempre carga el HTML fresco del VPS

3. **Google Drive:** `rclone copyto` sincroniza `data/kb_viewer.html` con el Shared Drive tras cada pipeline. Accesible offline vía Drive for Desktop.

---

## 13. Categorías de conocimiento

Adaptables al dominio del cliente. En OPENLAB Radar:

| Carpeta | Temática |
|---------|----------|
| `context-engineering/` | CLAUDE.md, skills, context window, prompt design |
| `claude-code-advanced/` | BMAD, SPARC, hooks, MCP, headless, multi-agent |
| `agentic-systems/` | Orchestration, pipelines, reliability, observability |
| `enterprise-ai/` | Procesos de conocimiento, automatización documental |
| `cli-vs-platforms/` | CLI agents vs n8n/Zapier/LangGraph |
| `delivery-adoption/` | Entrega de skills, adopción enterprise, pricing |

**Para adaptar a otro cliente:** redefinir carpetas + actualizar `config/keywords.yaml` + actualizar los criterios de scoring en `prompts/evaluate-daily.md`.

---

## 14. Modelo de scoring — cómo adaptarlo

El sistema de scoring tiene 3 dimensiones ponderadas. La clave para adaptarlo a un cliente es **redefinir la dimensión A (Aplicabilidad)** con los criterios del negocio del cliente.

**Estructura invariante:**
```
Score = (A×3 + B×2 + C×1) / 6

A: Aplicabilidad directa al cliente (×3) — redefinir por cliente
B: Novedad (×2)                          — genérico, pocas variaciones
C: Calidad de la fuente (×1)             — genérico, pocas variaciones
```

**Ejemplo de adaptación de A para un cliente de consultoría legal:**
```
9-10: Patrón de automatización aplicable a due diligence mañana
7-8:  Marco metodológico adaptable al proceso legal del cliente
5-6:  Referencia teórica sin aplicación inmediata
1-4:  Tangencial al negocio
```

**Umbrales de briefing** (ajustables en `config/keywords.yaml`):
- `min_score_briefing: 7` — top vídeos del día
- Menciones rápidas: 6.0-7.0 (máx 2)
- Brief individual generado: score ≥ 7

---

## 15. Dependencias Python

```bash
# Instalar todas
pip install \
  google-api-python-client \
  google-auth \
  youtube-transcript-api==1.2.4 \
  mcp \
  requests \
  pyyaml \
  --break-system-packages

# Verificar versiones críticas
pip show youtube-transcript-api mcp
```

**Dependencias clave:**

| Paquete | Versión | Uso |
|---------|---------|-----|
| `google-api-python-client` | 2.193+ | YouTube Data API v3 |
| `youtube-transcript-api` | 1.2.4 | Transcripts + WebshareProxyConfig |
| `mcp` | 1.26+ | FastMCP stdio server |
| `requests` | 2.31+ | HTTP requests |
| `pyyaml` | any | Lectura de config/*.yaml |

---

## 16. Operativa y mantenimiento

### Logs

```bash
# Ver log del día actual
tail -f data/logs/cron-daily.log

# Ver log de una ejecución específica
cat data/logs/run-YYYY-MM-DD.log

# Ver errores
grep -i "error\|warn\|blocked" data/logs/run-YYYY-MM-DD.log
```

### Renovar token Claude

```bash
# ~1 vez al año
ssh usuario@vps
cd /ruta/proyecto
claude setup-token
# Actualizar CLAUDE_CODE_OAUTH_TOKEN en config/.env
```

### Quota YouTube API

```bash
# Ver cuántos candidatos encontró ayer
cat data/candidates-YYYY-MM-DD.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d))"

# Si quotaExceeded → reducir keywords o canales en config/keywords.yaml y config/channels.yaml
```

### Añadir un vídeo manualmente

```bash
./scripts/add_video.sh "https://youtube.com/watch?v=ID"
```

### Check previo antes de añadir

```bash
./scripts/check_video.sh "https://youtube.com/watch?v=ID"
```

---

## 17. Checklist para desplegar en un cliente

```
□ VPS provisionado (Ubuntu 22.04, Python 3.12)
□ Claude Code CLI instalado + claude setup-token ejecutado
□ youtube-transcript-api y mcp instalados (pip)
□ Cuenta Webshare creada → Rotating Residential proxies activados
□ YouTube Data API key creada en Google Cloud Console
□ Bot de Telegram creado en @BotFather → token obtenido
□ Canal Telegram del equipo creado → bot añadido como admin
□ Telegraph access token (se genera automáticamente en primer uso)
□ rclone configurado con Google Drive del cliente
□ Google Shared Drive creado y compartido con el equipo
□ gws (Google Workspace CLI) configurado para envío de email
□ config/.env rellenado con todas las credenciales
□ config/channels.yaml adaptado al dominio del cliente
□ config/keywords.yaml adaptado al dominio del cliente
□ config/tags.yaml adaptado al dominio del cliente
□ prompts/evaluate-daily.md — criterios de scoring A adaptados al cliente
□ .mcp.json creado con ruta absoluta al mcp_transcript_server.py
□ Crontab configurado (crontab -e como usuario no-root)
□ Primera ejecución manual: bash scripts/run_daily.sh
□ Verificar: briefing generado, Telegram recibido, email enviado, Drive sincronizado
```

---

## 18. Decisiones de diseño

**¿Por qué Markdown + frontmatter YAML y no una base de datos para los briefs?**
Los briefs en `.md` son legibles por humanos y por Claude directamente (con `Read`/`Glob`). La base de datos SQLite solo guarda metadatos de vídeos. Los briefs son el knowledge base real — que sean ficheros planos los hace portables, versionables en git y accesibles en Drive.

**¿Por qué Claude Code CLI headless en lugar de la API de Anthropic directamente?**
Las herramientas de Claude Code (MCP, Read, Write, Glob) permiten que el evaluador genere ficheros directamente sin código intermedio. La lógica de evaluación está en el prompt en lenguaje natural, no en código. Esto hace el sistema mantenible por personas no técnicas y adaptable sin programar.

**¿Por qué MCP server propio para transcripts en lugar de usar la librería directamente?**
El MCP server hace que el transcript sea una herramienta nativa de Claude, invocable desde cualquier contexto (cron, sesión interactiva, add_video). Además centraliza la lógica de proxy y fallback de idioma en un único lugar.

**¿Por qué Telegraph y no publicar directamente en Telegram?**
Telegram tiene límite de 4.096 caracteres por mensaje. Los briefs son mucho más largos. Telegraph permite leer el brief completo como Instant View dentro de la app de Telegram sin abrir un navegador externo.

**¿Por qué rclone para Drive y no Drive API directamente?**
rclone maneja autenticación, retry, sync diferencial y está probado en producción. La Drive API requeriría manejar OAuth2 flows y refresh tokens manualmente.
