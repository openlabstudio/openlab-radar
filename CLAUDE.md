# OPENLAB Radar

Sistema de inteligencia continua que monitoriza YouTube diariamente para detectar contenido avanzado relevante para OPENLAB. Evalúa vídeos con Claude Code y genera resúmenes .md con aplicabilidad directa al negocio.

## Qué es OPENLAB

Empresa de **context engineering**. Diseña skills (ficheros .md) que se ejecutan en Claude Code CLI como agentes de IA para procesos de conocimiento intensivo en empresas. Stack: Claude Code CLI + skills en lenguaje natural + MCP. Zero lock-in, zero código propio.

## Estructura del proyecto

```
briefs/                  → base de conocimiento (sincronizar con Drive)
  daily-briefings/       → briefings diarios generados por el cron
  context-engineering/
  claude-code-advanced/
  agentic-systems/
  enterprise-ai/
  cli-vs-platforms/
  delivery-adoption/
insights/                → análisis y síntesis generados a petición (sincronizar con Drive)
config/
  .env                   → credenciales (YouTube API, Telegram, email)
  channels.yaml          → 15 canales monitorizados
  keywords.yaml          → 30 keywords en 6 categorías
prompts/
  evaluate-daily.md      → prompt del evaluador diario (headless)
  evaluate-manual.md     → prompt para añadir un vídeo a mano (headless)
  weekly-digest.md       → prompt del digest semanal
scripts/
  scraper.py               → YouTube Data API scraper
  add_video.sh             → añadir un vídeo manualmente al pipeline
  run_daily.sh             → pipeline diario + email HTML a Rafael (cron 08:00 UTC)
  run_weekly.sh            → digest semanal + email HTML al equipo (cron viernes 08:30 UTC)
  publish_telegraph.py     → publica briefs en Telegraph (Instant View en Telegram)
  md_to_email_html.py      → convierte briefing diario a HTML newsletter para email
  md_to_weekly_html.py     → convierte digest semanal a HTML newsletter para email
  notify.py                → envía notificaciones por Telegram
  generate_kb_viewer.py    → genera data/kb_viewer.html (dashboard visual del KB)
data/
  kb_viewer.html           → dashboard HTML del knowledge base (sincronizado con Drive)
data/
  radar.db               → SQLite con todos los vídeos procesados
  candidates-FECHA.json  → candidatos del scraper por día
docs/
  product-description.md → documentación completa del sistema
  improvements/          → mejoras pendientes de implementar
```

## Crons activos (root)

```
0  8 * * *   run_daily.sh   → pipeline diario 09:00 CET (email a Rafael)
30 8 * * 5   run_weekly.sh  → digest semanal viernes 09:30 CET (email al equipo)
```

## Cómo añadir un vídeo manualmente

Desde esta sesión:
> "añade este vídeo: URL"

El skill `radar-add-video` hace transcript → triage → scoring → brief en `briefs/CATEGORÍA/` → Telegraph → Telegram. No toca el briefing del día.

## Cómo hacer consultas sobre los briefs

Puedes preguntar directamente:
> "¿Qué dicen los briefs sobre context engineering esta semana?"
> "¿Qué vídeos hablan de delivery de skills a clientes?"

Claude busca en `briefs/` y sintetiza con citas de los .md.

## Cómo pedir un insight

> "Analiza los briefs y genera un doc sobre X en insights/"

Los insights generados se guardan en `insights/` y se sincronizan con Google Drive (cuando esté configurado).

## Pendiente de configurar

Ver `docs/improvements/` para los pasos detallados:
- `setup-rclone-google-drive.md` → sync briefs/ e insights/ con Drive
- `setup-email-digest-semanal.md` → auth gws para envío de email semanal
- `remote-add-video-desde-laptop.md` → skill en el laptop para añadir vídeos sin SSH manual
