# OPENLAB Radar

Sistema de inteligencia continua que monitoriza YouTube diariamente para detectar contenido avanzado sobre context engineering, agentic systems y delivery de skills en enterprise.

Escanea 15 canales + 18 keywords → filtra y evalúa con Claude Code → genera resúmenes .md con aplicabilidad OPENLAB → te llega al móvil por Telegram.

## Quick Start

```bash
# 1. Configurar variables de entorno
cp config/.env.example config/.env
# Rellenar: YOUTUBE_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_CHANNEL_ID

# 2. Instalar dependencias Python
pip3 install --user --break-system-packages -r scripts/requirements.txt

# 3. Test (dry run, no guarda nada)
export $(cat config/.env | grep -v '#' | xargs)
python3 scripts/scraper.py --dry-run

# 4. Pipeline completo
bash scripts/run_daily.sh
```

## Añadir un vídeo manualmente

Dos formas de añadir un vídeo fuera del ciclo diario:

**Desde el VPS** (Claude Code conectado al VPS):
> "añade este vídeo: https://youtube.com/watch?v=XXX"

El skill `radar-add-video` hace el pipeline completo: transcript → triage → scoring → brief en la categoría correcta → Telegraph → Telegram. No toca el briefing del día.

**Desde el laptop** (cualquier terminal con Claude Code):
> "añade este vídeo al radar: https://youtube.com/watch?v=XXX"

El skill `radar-add-video-remote` conecta al VPS y ejecuta el mismo pipeline de forma transparente. Requiere SSH sin contraseña al VPS (`ssh-copy-id openlab@212.227.104.123`).

También directamente desde shell en el VPS:
```bash
bash scripts/add_video.sh "https://youtube.com/watch?v=XXX"
```

## Estructura

```
openlab-radar/
├── config/
│   ├── keywords.yaml       # 30 keywords en 6 categorías
│   ├── channels.yaml       # 14 canales monitorizados
│   └── .env                # Credenciales (no compartir)
├── prompts/
│   ├── evaluate-daily.md   # Prompt evaluador (triage + scoring + resúmenes)
│   ├── evaluate-manual.md  # Prompt evaluador para un solo vídeo añadido a mano
│   └── weekly-digest.md    # Prompt digest semanal
├── scripts/
│   ├── scraper.py              # YouTube Data API scraper
│   ├── add_video.sh            # Añadir un vídeo manualmente al pipeline
│   ├── run_daily.sh            # Pipeline diario + email Rafael (cron 08:00 UTC)
│   ├── run_weekly.sh           # Digest semanal + email equipo (cron viernes 08:30 UTC)
│   ├── md_to_email_html.py     # Convierte briefing diario a HTML newsletter
│   ├── md_to_weekly_html.py    # Convierte digest semanal a HTML newsletter
│   ├── publish_telegraph.py    # Publica briefs en Telegraph
│   └── generate_kb_viewer.py   # Genera data/kb_viewer.html (dashboard visual del KB)
├── briefs/                  # Base de conocimiento (sincronizada con Google Drive)
│   ├── daily-briefings/     # Briefings diarios (email HTML a Rafael 09:00 CET)
│   ├── weekly-digests/      # Digests semanales (email HTML al equipo viernes 09:30 CET)
│   ├── context-engineering/
│   ├── claude-code-advanced/
│   ├── agentic-systems/
│   ├── enterprise-ai/
│   ├── cli-vs-platforms/
│   └── delivery-adoption/
├── insights/                # Análisis y síntesis generados desde los briefs (sincronizada con Google Drive)
├── data/                    # SQLite + candidatos JSON
├── docs/
│   ├── product-description.md      # Documentación completa del producto
│   ├── setup-acceso-vps.md         # Instrucciones acceso VS Code
│   └── improvements/               # Mejoras pendientes de implementar
├── setup.sh                # Setup VPS con crons
└── README.md
```

## KB Viewer

Dashboard visual del knowledge base generado diariamente por el cron. Disponible en Google Drive como `kb_viewer.html` — doble clic en Finder para abrirlo en el navegador.

Incluye Hot Signals (briefs con score ≥ 8.0 de la semana), vista cronológica, navegación por categoría, tag explorer y buscador. Para regenerarlo manualmente:

```bash
python3 scripts/generate_kb_viewer.py
# Con Drive local (laptop):
python3 scripts/generate_kb_viewer.py \
  --briefs-dir ~/OPENLAB/inteligencia/radar/briefs \
  --output ~/OPENLAB/inteligencia/radar/kb_viewer.html
```

## Documentación

Ver **[docs/product-description.md](docs/product-description.md)** para la documentación completa: arquitectura, sistema de evaluación, criterios de triage, formato de outputs, canales, keywords, UX y decisiones de diseño.

## Insights disponibles

Documentos de síntesis generados a petición desde los briefs acumulados:

| Fichero | Descripción |
|---------|-------------|
| [insights/buenas-practicas-estructura-skills.md](insights/buenas-practicas-estructura-skills.md) | Buenas prácticas de estructura de skills en Claude Code — checklist para auditar skills globales |
