# Mejora: añadir vídeo al radar desde el laptop sin SSH manual

## Problema

El skill `radar-add-video` (en `~/.claude/skills/radar-add-video/`) corre en el VPS, donde están el proyecto, la DB, los briefs y el MCP de transcripts. Desde el laptop, Claude Code es una instancia distinta sin acceso a nada de eso.

Cada vez que se quiere añadir un vídeo manualmente desde el laptop hay que conectarse por SSH, navegar al directorio y ejecutar el pipeline. El objetivo es poder decir "añade este vídeo al radar: URL" desde cualquier terminal del laptop y que ocurra solo.

---

## Diseño

### Pieza 1 — VPS: `prompts/evaluate-manual.md`

Prompt standalone equivalente a `evaluate-daily.md` pero para un solo vídeo:
- Input: una URL (inyectada en el prompt por el script)
- Hace: transcript → triage → scoring → brief en `briefs/CATEGORÍA/FECHA-slug.md`
- No toca `briefs/daily-briefings/`
- Registra el `video_id` en `data/radar.db` (INSERT OR IGNORE)
- Al terminar: publica en Telegraph + notifica por Telegram

### Pieza 2 — VPS: `scripts/add_video.sh <URL>`

```bash
#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TODAY=$(date -u +%Y-%m-%d)
URL="$1"

if [ -f "$PROJECT_DIR/config/.env" ]; then
    set -a; source "$PROJECT_DIR/config/.env"; set +a
fi

claude -p "$(cat "$PROJECT_DIR/prompts/evaluate-manual.md")

URL: $URL
Fecha: $TODAY" \
  --allowedTools "Read,Write,Glob,Bash,mcp__youtube-transcript__get_transcript" \
  --output-format text
```

### Pieza 3 — Laptop: skill global `radar-add-video-remote`

Skill en `~/.claude/skills/radar-add-video-remote/SKILL.md` en el laptop (no en el VPS).

Hace solo tres cosas:
1. Extrae la URL del mensaje del usuario
2. SSH al VPS y ejecuta `add_video.sh`
3. Muestra el output en el terminal

```bash
ssh openlab@212.227.104.123 "cd /home/openlab/openlab-radar && ./scripts/add_video.sh 'URL'"
```

El VPS hace todo el trabajo pesado. El laptop es el disparador.

---

## Flujo completo

```
Laptop (usuario)                     VPS
─────────────────                    ──────────────────────────────────
"añade este vídeo: URL"
  → skill extrae URL
  → ssh + add_video.sh   ────────►   claude headless (evaluate-manual)
                                       → transcript MCP
                                       → triage + scoring
                                       → brief en briefs/CATEGORÍA/
                                       → radar.db (INSERT OR IGNORE)
                                       → Telegraph + Telegram
  ← output del pipeline  ◄────────
```

---

## Requisito de setup

**SSH sin contraseña** entre laptop y VPS (autenticación por clave pública). Si ya se entra al VPS sin que pida password, ya está. Si no:

```bash
# En el laptop
ssh-copy-id openlab@VPS_HOST
```

---

## Alternativa descartada: Telegram como bridge

El VPS ya tiene el bot de Telegram. Sería posible que un daemon en el VPS escuche mensajes con un prefijo (`/video URL`) y lance el script — funcionaría también desde el móvil. Descartado por ahora porque añade un proceso persistente en el VPS. Retomar si se quiere añadir vídeos desde el móvil.

---

## Estado

- [ ] Crear `prompts/evaluate-manual.md` en el VPS
- [ ] Crear `scripts/add_video.sh` en el VPS
- [ ] Crear skill `radar-add-video-remote` en el laptop
- [ ] Verificar SSH sin contraseña laptop → VPS
