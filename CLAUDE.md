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
  run_weekly.sh          → digest semanal (cron viernes 07:30 UTC)
  add_video.sh           → añadir un vídeo manualmente
  publish_telegraph.py   → publica briefs en Telegraph
  md_to_email_html.py    → briefing diario → HTML email
  md_to_weekly_html.py   → digest semanal → HTML email
  notify.py              → notificaciones Telegram
  generate_kb_viewer.py  → genera data/kb_viewer.html
data/
  radar.db               → SQLite con todos los vídeos procesados
  kb_viewer.html         → dashboard KB (sincronizado con Drive)
docs/
  arquitectura-tecnica.md
  guia-uso.md
  product-description.md
  improvements/          → mejoras pendientes
```

## Crons (usuario openlab, NO root)

```
0  7 * * *   run_daily.sh   → 09:00 CEST / 08:00 CET
30 7 * * 5   run_weekly.sh  → viernes 09:30 CEST / 08:30 CET
```

Verificar: `crontab -l`

## Autenticación Claude headless

Los crons usan `claude -p`. Token en `config/.env` → `CLAUDE_CODE_OAUTH_TOKEN`.

- Generado con `claude setup-token`. Válido ~1 año (renovar ~2027-03-31).
- ⚠️ No poner `ANTHROPIC_API_KEY` en el entorno: factura por token ignorando la suscripción Max.

## Skills disponibles

- `radar-check-video` — check previo de un vídeo (¿vale la pena? ¿ya cubierto?)
- `radar-add-video` / `radar-add-video-remote` — añadir vídeo al pipeline completo

## Estado del sistema

| Componente | Estado |
|---|---|
| Scraper + cron diario | ✅ Activo |
| Evaluador + briefs + Telegraph + Telegram | ✅ Activo |
| Email diario a Rafael | ✅ Activo |
| rclone → Google Drive | ✅ Activo |
| KB Viewer (`radar.openlabstudio.com`) | ✅ Activo |
| Skills `radar-check-video` / `radar-add-video-remote` | ✅ Activo |
| Email digest semanal al equipo | ⏳ Pendiente (`docs/improvements/setup-email-digest-semanal.md`) |
