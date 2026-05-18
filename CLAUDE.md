# OPENLAB Radar

## VPS — fuente de verdad

Toda ejecución ocurre en el VPS. La laptop solo consulta docs y lanza skills vía SSH.

```
VPS:    212.227.104.123  /home/openlab/openlab-radar/
Drive:  briefs/, insights/, data/kb_viewer.html  (sincronizado vía rclone)
GitHub: código y docs (no briefs ni data)
```

## Estructura

```
briefs/
  daily-briefings/       → briefings diarios
  weekly-digests/        → digests semanales
  context-engineering/
  claude-code-advanced/
  agentic-systems/
  enterprise-ai/
  cli-vs-platforms/
  delivery-adoption/
insights/                → síntesis generadas a petición
config/
  .env                   → credenciales (YouTube API, Telegram, email, tokens)
  channels.yaml          → canales monitorizados
  keywords.yaml          → keywords por categoría
  tags.yaml              → tags disponibles para briefs
prompts/
  evaluate-daily.md      → evaluador diario (headless)
  evaluate-manual.md     → evaluador para vídeo manual (headless)
  weekly-digest.md       → digest semanal
scripts/
  scraper.py             → YouTube Data API scraper
  run_daily.sh           → pipeline diario (cron 07:00 UTC)
  run_recovery.sh        → recuperación si el pipeline diario falló (cron 09:00 UTC)
  run_weekly.sh          → digest semanal (cron viernes 07:30 UTC)
  add_video.sh           → añadir un vídeo manualmente
  publish_telegraph.py   → publica briefs en Telegraph
  md_to_email_html.py    → briefing diario → HTML email
  md_to_weekly_html.py   → digest semanal → HTML email
  notify.py              → notificaciones Telegram
  generate_kb_viewer.py  → genera data/kb_viewer.html
  radar_health_check.py  → fitness functions: métricas de salud del sistema
  radar_utils.py         → utilidades compartidas (parse_frontmatter)
  radar_search.py        → búsqueda estructurada por frontmatter (CLI)
  migrate_frontmatter.py → migración retroactiva de frontmatter
data/
  radar.db               → SQLite con todos los vídeos procesados
  kb_viewer.html         → dashboard KB (sincronizado con Drive)
  health-reports/        → informes semanales de salud del sistema
docs/
  arquitectura-tecnica.md
  guia-uso.md
  product-description.md
  improvements/
    done/                → mejoras implementadas
    pending/             → mejoras pendientes
```

## Crons (usuario openlab, NO root)

```
0  7 * * *   run_daily.sh    → 09:00 CEST / 08:00 CET
30 7 * * 5   run_weekly.sh   → viernes 09:30 CEST / 08:30 CET
0  9 * * *   run_recovery.sh → 11:00 CEST (relanza evaluador si el daily falló)
30 8 * * *   radar_health_check.py --alerts-only → 10:30 CEST (alertas Telegram si hay umbrales rotos)
```

Verificar: `crontab -l`

## Autenticación Claude headless

Los crons usan `claude -p`. Token en `config/.env` → `CLAUDE_CODE_OAUTH_TOKEN`.

- Generado con `claude setup-token`. Válido ~1 año (renovar ~2027-03-31).
- ⚠️ No poner `ANTHROPIC_API_KEY` en el entorno: factura por token ignorando la suscripción Max.

## Skills disponibles

- `radar-check-video` — check previo de un vídeo (¿vale la pena? ¿ya cubierto?)
- `radar-add-video` / `radar-add-video-remote` — añadir vídeo al pipeline completo

## Búsqueda en briefs

Dos mecanismos complementarios:

- **Frontmatter (estructurada):** `python3 scripts/radar_search.py --score-min 8 --category context-engineering --sort score`
- **QMD (semántica):** colección `radar` en QMD (MCP). Busca por significado, no solo keywords. Usar `mcp__qmd__query` con `collection='radar'`. Re-indexar tras nuevos briefs: `qmd update -q && qmd embed`

## Estado del sistema

| Componente | Estado |
|---|---|
| Scraper + cron diario | ✅ Activo |
| Evaluador + briefs + Telegraph + Telegram | ✅ Activo |
| Email diario a Rafael | ✅ Activo |
| rclone → Google Drive | ✅ Activo |
| KB Viewer (`radar.openlabstudio.com`) | ✅ Activo |
| Skills `radar-check-video` / `radar-add-video-remote` | ✅ Activo |
| Health Check (fitness functions) | ✅ Activo (alertas diarias + informe semanal) |
| Frontmatter enriquecido + `radar_search.py` | ✅ Activo |
| QMD búsqueda semántica (colección `radar`) | ✅ Activo (laptop, 242 docs) |
| Email digest semanal al equipo | ⏳ Pendiente (`docs/improvements/setup-email-digest-semanal.md`) |
