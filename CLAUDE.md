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
  radar.db               → SQLite con todos los vídeos procesados
  kb_viewer.html         → dashboard HTML del knowledge base (sincronizado con Drive)
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

## Casos de uso — qué puede pedir Rafael

Ver guía completa en `docs/guia-uso.md`.

### Añadir un vídeo (flujo recomendado en dos pasos)

**Paso 1 — Check previo** (¿vale la pena? ¿ya está cubierto?):
> "¿vale la pena este vídeo? URL"

Skill `radar-check-video`: SSH al VPS → `check_video.sh` → Claude headless con `evaluate-check.md`. Transcript + triage + score estimado + búsqueda de cobertura en briefs/. Todo corre en el VPS. Si recomienda añadir, pregunta confirmación y ejecuta el pipeline.

**Paso 2 — Añadir directamente** (si ya sabe que quiere añadirlo):
> "añade este vídeo al radar: URL"

Skill `radar-add-video-remote`: transcript → triage → scoring → brief en `briefs/CATEGORÍA/` → Telegraph → Telegram. No toca el briefing del día.

### Consultar briefs

> "¿Qué dicen los briefs sobre [tema]?"
> "Dame los briefs con tag [tag] ordenados por score"
> "¿Qué canales han publicado más sobre agentic systems?"

Busca en `briefs/` (local, sincronizado desde VPS vía rclone). Sintetiza con citas de los .md. Tags disponibles en `config/tags.yaml`.

### Generar un insight

> "Analiza los briefs y genera un doc sobre X en insights/"

Busca briefs relevantes, sintetiza patrones, extrae implicaciones para OPENLAB y argumentos comerciales. Guarda en `insights/FECHA-slug.md`. Se sincroniza con Drive automáticamente.

### Consultas de estado del sistema

> "¿Cuántos briefs tenemos por categoría?"
> "¿Cuáles son los briefs con score más alto este mes?"
> "¿Qué hay pendiente de configurar en el radar?"

## Estado del sistema

| Componente | Estado |
|---|---|
| Scraper + cron diario (09:00 CET) | ✅ Activo |
| Evaluador + briefs + Telegraph + Telegram | ✅ Activo |
| Email diario a Rafael | ✅ Activo |
| rclone → Google Drive | ✅ Activo |
| KB Viewer HTML (Drive) | ✅ Activo |
| Skill `radar-check-video` (check previo) | ✅ Activo |
| Skill `radar-add-video-remote` (añadir vídeo) | ✅ Activo |
| Email digest semanal al equipo | ⏳ Pendiente auth gws (`docs/improvements/setup-email-digest-semanal.md`) |
