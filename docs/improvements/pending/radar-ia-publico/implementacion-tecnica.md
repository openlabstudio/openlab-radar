# Radar IA Público: implementación técnica multi-perfil

Plan técnico para convertir el OPENLAB Radar en un sistema multi-perfil que soporte simultáneamente la KB interna y un Radar público orientado a empresas.

**Estado:** pendiente de implementación
**Última actualización:** 2026-04-09
**Doc complementario:** [gtm-radar-ia.md](gtm-radar-ia.md) — estrategia comercial, pricing y plan de lanzamiento

---

## Contexto

El Radar hoy es una herramienta interna de inteligencia sobre IA. El objetivo es añadir un **perfil público** orientado a empresas que funcione como demo del producto y top of funnel para vender el Radar como servicio personalizado. Ver [gtm-radar-ia.md](gtm-radar-ia.md) para el modelo de negocio completo.

---

## Decisión arquitectónica: multi-perfil, NO clonar

Un solo repositorio, una sola instancia, dos perfiles de configuración. Un vídeo entra por el scraper y se evalúa con ambos perfiles. Puede acabar en la KB interna, en la pública, en ambas, o en ninguna.

| Aspecto | Clonar el repo | Multi-perfil (elegido) |
|---|---|---|
| Mantenimiento | Doble | Uno solo |
| Scraper | Duplicado | Compartido (scrape once, evaluate twice) |
| Base de datos | 2 SQLites | 1 SQLite con campo `profile` |
| Coste Claude | 2× | ~1.3× (scrape una vez, evalúa dos veces solo lo relevante) |
| KB Viewer | 2 instancias | 1 instancia con filtro por perfil |
| Google Drive sync | Hay que desactivar en el clon | Solo sincroniza `internal` |

---

## Diferencias entre perfil interno y público

Cada fila es un componente que se comporta distinto según el perfil.

| Componente | `internal` (actual) | `public` (nuevo) |
|---|---|---|
| **Canales YouTube** | Técnicos (Anthropic, IndyDevDan, Karpathy, Cole Medin...) | Empresariales (Harvard BR, McKinsey, a16z, Gartner, consultoras...) |
| **Keywords** | context engineering, BMAD, agentic, MCP, skills... | adopción IA, ROI, transformación digital, casos de uso, gobernanza... |
| **Tags** | 43 tags técnicos (context-engineering, token-optimization, skill-design...) | Tags empresariales nuevos (roi, caso-de-uso, industria, adopción...) |
| **Prompt evaluador** | Scoring ponderado por aplicabilidad a OPENLAB (×3) | Scoring ponderado por valor para decisores empresariales |
| **Categorías de briefs** | context-engineering, claude-code-advanced, agentic-systems, enterprise-ai, cli-vs-platforms, delivery-adoption | estrategia-ia, casos-de-uso, herramientas, tendencias, gobernanza, adopción |
| **Umbral mínimo score** | 7.0 | 7.0 (puede ajustarse) |
| **Idioma contenido** | EN/ES mezclado | ES preferente (audiencia empresarial española) |
| **KB Viewer** | `radar.openlabstudio.com` (acceso equipo) | `radar-ia.openlabstudio.com` (acceso público) |
| **Branding KB Viewer** | Logo OPENLAB, sin CTA | Logo OPENLAB + CTA registro newsletter + disclaimer "demo" |
| **Telegraph** | Publica briefs individuales | Publica briefs individuales (cuenta Telegraph separada o compartida) |
| **Telegram** | Notificaciones al canal interno del equipo | NO — el canal público es la newsletter |
| **Email briefing diario** | A `rafa@openlabstudio.com` vía gws | NO — la distribución pública es semanal |
| **Digest semanal** | Al equipo vía gws (pendiente) | A suscriptores vía Beehiiv API |
| **CTA en digest** | Ninguno | "¿Quieres un Radar para tu empresa? Hablemos" |
| **Google Drive sync** | ✅ Sincroniza briefs/ e insights/ | ❌ NO sincroniza a Drive |
| **rclone** | Activo | Desactivado para este perfil |
| **Exclusiones scraper** | Tutoriales básicos, "getting started", "what is AI" | Contenido muy técnico (code-level), clickbait, opinión sin datos |

---

## Estructura de directorios propuesta

```
config/
  .env                          → credenciales compartidas + por perfil
  profiles/
    internal/
      channels.yaml             → (mover desde config/channels.yaml)
      keywords.yaml             → (mover desde config/keywords.yaml)
      tags.yaml                 → (mover desde config/tags.yaml)
      profile.yaml              → metadatos del perfil (nombre, descripción, flags)
    public/
      channels.yaml             → canales empresariales
      keywords.yaml             → keywords empresariales
      tags.yaml                 → taxonomía empresarial
      profile.yaml              → metadatos del perfil público

prompts/
  profiles/
    internal/
      evaluate-daily.md         → (mover desde prompts/evaluate-daily.md)
      evaluate-manual.md        → (mover desde prompts/evaluate-manual.md)
      evaluate-check.md         → (mover desde prompts/evaluate-check.md)
      weekly-digest.md          → (mover desde prompts/weekly-digest.md)
    public/
      evaluate-daily.md         → evaluador con criterios empresariales
      evaluate-manual.md        → evaluador manual para público
      weekly-digest.md          → digest con CTA de venta

briefs/
  internal/                     → (mover contenido actual de briefs/)
    daily-briefings/
    weekly-digests/
    context-engineering/
    claude-code-advanced/
    agentic-systems/
    enterprise-ai/
    cli-vs-platforms/
    delivery-adoption/
  public/
    daily-briefings/
    weekly-digests/
    estrategia-ia/
    casos-de-uso/
    herramientas/
    tendencias/
    gobernanza/
    adopcion/

data/
  radar.db                      → tabla videos + tabla video_profiles
  kb_viewer_internal.html       → generado para radar.openlabstudio.com
  kb_viewer_public.html         → generado para radar-ia.openlabstudio.com
  logs/
    internal/
    public/
```

### Fichero `profile.yaml` (ejemplo para `public`)

```yaml
name: public
display_name: "OPENLAB Radar IA"
description: "Inteligencia de IA para empresas"
lang_preference: es
min_score_briefing: 7
max_videos_briefing: 5

# Distribución
telegram_enabled: false
email_daily_enabled: false
email_weekly_enabled: false          # se usa Beehiiv, no gws
beehiiv_enabled: true
gdrive_sync: false
telegraph_enabled: true
kb_viewer_enabled: true

# Branding
kb_viewer_subdomain: "radar-ia.openlabstudio.com"
telegraph_author: "OPENLAB Radar IA"
newsletter_cta: "¿Quieres un Radar personalizado para tu empresa? Escríbenos a hola@openlabstudio.com"
```

---

## Cambios por componente

### Fase 0 — Base de datos (30 min)

**Fichero:** `scripts/scraper.py`

Añadir tabla separada `video_profiles` para que el mismo vídeo tenga scores y categorías distintas por perfil:

```sql
CREATE TABLE IF NOT EXISTS video_profiles (
    video_id TEXT NOT NULL,
    profile TEXT NOT NULL,
    status TEXT DEFAULT 'candidate',
    score REAL DEFAULT 0,
    categories TEXT DEFAULT '[]',
    briefing_date TEXT,
    PRIMARY KEY (video_id, profile),
    FOREIGN KEY (video_id) REFERENCES videos(video_id)
);
```

La tabla `videos` mantiene los datos del vídeo (título, canal, URL, etc.). La evaluación (score, status, categoría) se mueve a `video_profiles`.

### Fase 1 — Estructura de config y prompts (1-2h)

1. Crear `config/profiles/internal/` y mover `channels.yaml`, `keywords.yaml`, `tags.yaml`
2. Crear `config/profiles/public/` con ficheros vacíos (se rellenan en Fase 4)
3. Crear `prompts/profiles/internal/` y mover los 4 prompts actuales
4. Crear `prompts/profiles/public/` vacío (se rellenan en Fase 4)
5. Crear `profile.yaml` para cada perfil
6. Mantener symlinks o fallbacks en las rutas originales durante la transición
7. Crear `briefs/internal/` y `briefs/public/` en el VPS

**⚠️ Impacto en VPS:** Los crons actuales apuntan a rutas antiguas. Hay que actualizar `run_daily.sh` y `run_weekly.sh` antes de mover ficheros, o hacerlo todo en una ventana de mantenimiento.

### Fase 2 — Modificar scraper.py (2-3h)

**Fichero:** `scripts/scraper.py`

1. Aceptar argumento `--profile <nombre>` (default: `internal`)
2. Cargar config desde `config/profiles/<profile>/channels.yaml` y `keywords.yaml`
3. Exportar candidatos a `data/<profile>/candidates-{date}.json`
4. Al registrar en DB, usar la tabla `video_profiles` con el perfil correspondiente
5. **Optimización**: Si el vídeo ya existe en `videos` (scrapeado por otro perfil), no re-scrapear metadata de YouTube API → ahorro de quota

```python
# Pseudocódigo del cambio principal
PROFILE = args.profile  # "internal" o "public"
CONFIG_DIR = PROJECT_ROOT / "config" / "profiles" / PROFILE
CANDIDATES_DIR = DATA_DIR / PROFILE
```

### Fase 3 — Modificar scripts de pipeline (3-4h)

#### `run_daily.sh`

1. Aceptar variable `PROFILE` (default: `internal`)
2. Cargar `.env` base + override de perfil si existe (`config/profiles/$PROFILE/.env`)
3. Rutas de logs: `data/logs/$PROFILE/run-$TODAY.log`
4. Rutas de briefs: `briefs/$PROFILE/daily-briefings/$TODAY-briefing.md`
5. Pasar `--profile $PROFILE` a `scraper.py`
6. Usar prompt de `prompts/profiles/$PROFILE/evaluate-daily.md`
7. **Condicionales por perfil** (leer `profile.yaml`):
   - Telegram: solo si `telegram_enabled: true`
   - Email diario: solo si `email_daily_enabled: true`
   - rclone: solo si `gdrive_sync: true`
   - KB Viewer: generar con `--profile $PROFILE` → output a `data/kb_viewer_$PROFILE.html`

**Ejecución en cron:** Dos entradas, una por perfil:

```cron
0  7 * * *   PROFILE=internal /home/openlab/openlab-radar/scripts/run_daily.sh
15 7 * * *   PROFILE=public   /home/openlab/openlab-radar/scripts/run_daily.sh
```

(15 min de offset para no solapar llamadas a Claude)

#### `run_weekly.sh`

1. Aceptar `PROFILE`
2. Leer briefs de `briefs/$PROFILE/`
3. Usar prompt de `prompts/profiles/$PROFILE/weekly-digest.md`
4. **Para `public`**: en vez de enviar email vía gws, publicar en Beehiiv vía API
5. CTA de venta incluido en el prompt del digest público

```cron
30 7 * * 5   PROFILE=internal /home/openlab/openlab-radar/scripts/run_weekly.sh
45 7 * * 5   PROFILE=public   /home/openlab/openlab-radar/scripts/run_weekly.sh
```

#### `add_video.sh`

1. Aceptar `--profile <nombre>` como primer argumento antes de la URL
2. Cargar prompt y config del perfil correspondiente
3. Condicionar Telegraph, Telegram y Drive sync según perfil

#### `generate_kb_viewer.py`

1. Aceptar `--profile <nombre>`
2. Leer briefs de `briefs/<profile>/`
3. Output a `data/kb_viewer_<profile>.html`
4. **Para `public`**: inyectar banner CTA de newsletter en el HTML
5. **Para `public`**: ajustar `CATEGORY_META` con las categorías del perfil público
6. **Para `public`**: no incluir insights (son internos de OPENLAB)

#### `publish_telegraph.py`

1. Opcionalmente aceptar `--profile` para usar token/autor distintos
2. Cambio menor: `telegraph_author` leído de `profile.yaml`

#### `notify.py`

1. Aceptar `--profile` para usar `TELEGRAM_CHAT_ID` distinto por perfil
2. Para `public`: skip completo (Telegram no se usa en público)

#### `md_to_email_html.py` y `md_to_weekly_html.py`

1. Para `public`: ajustar categorías y colores al perfil empresarial
2. `md_to_weekly_html.py` para público: incluir footer con CTA de venta
3. Pueden recibir perfil como argumento para seleccionar estilos

### Fase 4 — Contenido del perfil público (1 día)

Esta es la fase de mayor esfuerzo creativo, no técnico.

#### `config/profiles/public/channels.yaml`

Canales empresariales a monitorizar (propuesta inicial):

```yaml
channels:
  - handle: "@HarvardBusiness"
    name: "Harvard Business Review"
    focus: "Management, estrategia, liderazgo con IA"
    priority: high
    lang: en

  - handle: "@a16z"
    name: "a16z"
    focus: "Venture capital, tendencias tech enterprise"
    priority: high
    lang: en

  - handle: "@GoogleCloudTech"
    name: "Google Cloud"
    focus: "Enterprise AI, casos de uso cloud"
    priority: medium
    lang: en

  - handle: "@AWSEvents"
    name: "AWS"
    focus: "Enterprise AI services, casos prácticos"
    priority: medium
    lang: en

  - handle: "@MicrosoftDeveloper"
    name: "Microsoft"
    focus: "Copilot, enterprise AI adoption"
    priority: medium
    lang: en

  - handle: "@DotCSV"
    name: "Dot CSV"
    focus: "Divulgación IA en español"
    priority: high
    lang: es

  - handle: "@McKinsey"
    name: "McKinsey & Company"
    focus: "Estrategia empresarial, transformación digital"
    priority: high
    lang: en

  # ... completar con 10-15 canales más
```

#### `config/profiles/public/keywords.yaml`

```yaml
lookback_hours: 48          # ventana más amplia, menos volumen esperado
min_score_briefing: 7
max_videos_briefing: 5
max_videos_mencion: 3

categories:
  estrategia-ia:
    - AI strategy for business
    - enterprise AI adoption
    - AI transformation roadmap
    - IA para empresas
    - estrategia de inteligencia artificial

  casos-de-uso:
    - AI use cases by industry
    - AI in manufacturing
    - AI in healthcare
    - AI in financial services
    - AI in retail
    - automatización con IA

  herramientas:
    - enterprise AI tools
    - AI platforms comparison
    - Copilot vs Gemini vs Claude
    - AI for productivity
    - herramientas IA empresariales

  tendencias:
    - AI trends 2026
    - generative AI enterprise
    - AI market analysis
    - futuro de la IA

  gobernanza:
    - AI governance framework
    - responsible AI enterprise
    - AI regulation Europe
    - AI compliance
    - gobierno de IA

  adopcion:
    - AI adoption challenges
    - change management AI
    - AI ROI measurement
    - AI pilot to production

quality_filters:
  min_duration: 3           # los vídeos empresariales suelen ser más cortos
  max_duration: 90
  min_channel_subscribers: 5000

exclude_terms:
  - tutorial de código
  - coding tutorial
  - learn to code
  - programming basics
  - prompt engineering basics
  - "what is ChatGPT"
```

#### `config/profiles/public/tags.yaml`

```yaml
tags:
  tematica:
    - estrategia
    - roi
    - caso-de-uso
    - adopcion
    - gobernanza
    - regulacion
    - transformacion-digital
    - automatizacion
    - productividad

  industria:
    - finanzas
    - salud
    - retail
    - manufactura
    - legal
    - educacion
    - sector-publico
    - energia

  tipo-contenido:
    - analisis
    - caso-practico
    - prediccion
    - guia
    - comparativa
    - entrevista
    - keynote

  entidades:
    - openai
    - google
    - microsoft
    - anthropic
    - aws
    - mckinsey
    - gartner
    - deloitte
```

#### `prompts/profiles/public/evaluate-daily.md`

Prompt adaptado con estos cambios clave vs el interno:

- **Audiencia objetivo**: Directivos, mandos intermedios, responsables de innovación en PYMEs y corporaciones. NO desarrolladores.
- **Criterios de scoring**:
  - A. Valor para decisores empresariales (×3) — ¿ayuda a tomar decisiones sobre IA?
  - B. Novedad/relevancia temporal (×2) — ¿es información fresca?
  - C. Credibilidad de la fuente (×1) — ¿datos reales, casos, o solo opinión?
- **Tono del brief**: Ejecutivo, sin jerga técnica, con "so what" claro para el negocio
- **Descarte rápido**: Vídeos puramente técnicos (code-level), tutoriales de herramientas, contenido para developers

#### `prompts/profiles/public/weekly-digest.md`

Digest semanal con:

- Resumen ejecutivo de tendencias de la semana
- Top 3-5 vídeos con "qué significa para tu empresa"
- Sección de oportunidades/riesgos
- **Footer CTA**: "Este digest es generado por el OPENLAB Radar, un sistema de inteligencia continua personalizable. ¿Quieres uno para tu sector? Escríbenos a hola@openlabstudio.com"

### Fase 5 — Integración Beehiiv (2-3h)

**Nuevo fichero:** `scripts/publish_beehiiv.py`

1. Recibe el digest semanal en Markdown
2. Lo convierte a HTML con estilo newsletter (reutilizar lógica de `md_to_weekly_html.py`)
3. Lo publica como post en Beehiiv vía API (`POST /publications/{pub_id}/posts`)
4. Opcionalmente envía como email a todos los suscriptores

**Variables de entorno nuevas:**

```env
BEEHIIV_API_KEY=xxx
BEEHIIV_PUBLICATION_ID=xxx
```

**Integración en `run_weekly.sh`:**

```bash
if [ "$PROFILE" = "public" ]; then
    python3 scripts/publish_beehiiv.py "$DIGEST_FILE"
fi
```

### Fase 6 — Subdominio y Nginx (30 min)

**En el VPS:**

1. Crear entrada DNS: `radar-ia.openlabstudio.com` → `212.227.104.123`
2. Configurar Nginx para servir `data/kb_viewer_public.html` en ese subdominio
3. Certificado SSL con Let's Encrypt (certbot)

```nginx
server {
    server_name radar-ia.openlabstudio.com;
    root /home/openlab/openlab-radar/data;

    location / {
        try_files /kb_viewer_public.html =404;
        add_header Cache-Control "public, max-age=3600";
    }

    # Beehiiv subscribe form proxy (opcional, evita CORS)
    location /subscribe {
        proxy_pass https://api.beehiiv.com/...;
    }
}
```

### Fase 7 — KB Viewer público: CTA y branding (2-3h)

**Fichero:** `scripts/generate_kb_viewer.py`

1. **Banner superior** con pitch + formulario de email (embed de Beehiiv o link directo)
2. **Footer** con enlace a openlabstudio.com y CTA
3. **Sin sección de insights** (es contenido interno)
4. **Categorías y colores** adaptados al perfil empresarial
5. **Meta tags** para SEO y Open Graph (título, descripción, imagen)
6. **Sin acceso a perfil interno** desde la vista pública (sin `?profile=internal`)

---

## Skills afectados

| Skill | Cambio necesario |
|---|---|
| `radar-add-video-remote` | Aceptar `--profile` como parámetro opcional (default: `internal`) |
| `radar-check-video` | Aceptar `--profile` para evaluar contra el perfil correcto |
| `radar-rebuild-index` | Generar índice por perfil |
| `radar-lint` | Analizar ambos perfiles o uno específico |

---

## Variables de entorno nuevas en `config/.env`

```env
# --- Perfil público ---
PUBLIC_TELEGRAM_ENABLED=false
PUBLIC_EMAIL_DAILY_ENABLED=false
PUBLIC_GDRIVE_SYNC=false
PUBLIC_BEEHIIV_API_KEY=xxx
PUBLIC_BEEHIIV_PUBLICATION_ID=xxx
PUBLIC_TELEGRAPH_AUTHOR="OPENLAB Radar IA"
PUBLIC_NEWSLETTER_CTA="¿Quieres un Radar personalizado para tu empresa? hola@openlabstudio.com"
```

---

## Plan de ejecución por fases

| Fase | Descripción | Esfuerzo | Dependencias |
|---|---|---|---|
| 0 | Migración DB: tabla `video_profiles` | 30 min | Ninguna |
| 1 | Estructura directorios `config/profiles/` y `prompts/profiles/` | 1-2h | Ninguna |
| 2 | Modificar `scraper.py` para `--profile` | 2-3h | Fases 0, 1 |
| 3 | Modificar scripts de pipeline (`run_daily.sh`, `run_weekly.sh`, `add_video.sh`, `generate_kb_viewer.py`, etc.) | 3-4h | Fases 0, 1 |
| 4 | Crear contenido del perfil público (channels, keywords, tags, prompts) | 1 día | Fase 1 |
| 5 | Integración Beehiiv (`publish_beehiiv.py`) | 2-3h | Fase 4 |
| 6 | Subdominio `radar-ia.openlabstudio.com` + Nginx + SSL | 30 min | Fase 3 |
| 7 | KB Viewer público: CTA, branding, SEO | 2-3h | Fases 3, 6 |

**Total estimado: 4-5 días de trabajo técnico**

### Orden recomendado

```
Semana 1:
  Día 1 → Fases 0 + 1 (base de datos + estructura directorios)
  Día 2 → Fases 2 + 3 (scripts con soporte --profile)
  Día 3 → Fase 4 (contenido perfil público: channels, keywords, prompts)

Semana 2:
  Día 4 → Fases 5 + 6 (Beehiiv + subdominio)
  Día 5 → Fase 7 (KB Viewer público + testing end-to-end)
```

---

## Verificación end-to-end

1. **Test perfil interno** (regresión): Ejecutar `PROFILE=internal ./scripts/run_daily.sh` y verificar que todo funciona exactamente como antes — mismos briefs, mismo Telegram, mismo Drive sync
2. **Test perfil público**: Ejecutar `PROFILE=public ./scripts/run_daily.sh` y verificar:
   - Scraper usa canales y keywords del perfil público
   - Candidatos se guardan en `data/public/candidates-*.json`
   - Evaluador usa prompt empresarial
   - Briefs se guardan en `briefs/public/`
   - NO se envía Telegram ni email diario
   - NO se sincroniza a Drive
   - KB Viewer se genera en `data/kb_viewer_public.html`
3. **Test digest semanal público**: Ejecutar `PROFILE=public ./scripts/run_weekly.sh` y verificar:
   - Digest generado en `briefs/public/weekly-digests/`
   - Se publica en Beehiiv (o dry-run)
   - Incluye CTA de venta
4. **Test web**: Verificar `radar-ia.openlabstudio.com` sirve el KB Viewer público con CTA
5. **Test add_video**: `./scripts/add_video.sh --profile public "URL"` funciona correctamente

---

## Riesgos técnicos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Romper el pipeline interno al refactorizar | Fase 1 usa symlinks/fallbacks; test de regresión antes de cada merge |
| Coste Claude se dispara con doble evaluación | Offset de 15 min entre perfiles; monitor de tokens en logs |
| Pocos vídeos empresariales de calidad | `lookback_hours: 48` en público; añadir más canales progresivamente |
| Beehiiv API cambia o tiene límites | Fallback a envío manual del digest; free tier soporta 1.000 suscriptores |

---

## Futuro: multi-tenant para clientes

La arquitectura multi-perfil sienta las bases para ofrecer el Radar como servicio. Añadir un perfil para un cliente sería:

1. Crear `config/profiles/<cliente>/` con sus canales, keywords y tags
2. Crear prompts adaptados a su dominio
3. Añadir entrada en cron (o script que itera sobre perfiles activos)
4. Generar KB Viewer del cliente en su subdominio o con acceso autenticado

Esto convertiría el Radar en un producto SaaS ligero operado por OPENLAB. Con 5-10 clientes activos, se justifica invertir en:

- Panel de administración para gestionar perfiles
- Onboarding automatizado (wizard de configuración de perfil)
- Dashboard de métricas por cliente (vídeos evaluados, scores, categorías)
- API para integraciones (Slack, Teams, email corporativo)
