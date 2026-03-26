#!/bin/bash
# OPENLAB Radar — Añadir vídeo manualmente
# Uso: ./scripts/add_video.sh "https://www.youtube.com/watch?v=VIDEO_ID"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TODAY=$(date -u +%Y-%m-%d)

if [ $# -eq 0 ]; then
    echo "Uso: $0 <youtube-url>"
    exit 1
fi

URL="$1"

# Cargar variables de entorno
if [ -f "$PROJECT_DIR/config/.env" ]; then
    set -a
    source "$PROJECT_DIR/config/.env"
    set +a
fi

echo "=========================================="
echo "OPENLAB Radar — Añadir vídeo manual"
echo "Fecha: $TODAY"
echo "URL:   $URL"
echo "=========================================="

# --- Paso 1: Evaluación ---
echo ""
echo ">>> Evaluando vídeo..."

BRIEF_OUTPUT=$(claude -p "$(cat "$PROJECT_DIR/prompts/evaluate-manual.md")

URL: $URL
Fecha: $TODAY" \
  --allowedTools "Read,Write,Glob,Bash,mcp__youtube-transcript__get_transcript" \
  --output-format text)

echo "$BRIEF_OUTPUT"

# Extraer ruta del brief del output (línea que empieza con "  Brief:")
BRIEF_FILE=$(echo "$BRIEF_OUTPUT" | grep "Brief:" | sed 's/.*Brief: //' | tr -d '[:space:]')

if [ -z "$BRIEF_FILE" ]; then
    echo ""
    echo "INFO: No se generó brief (vídeo descartado en triage o error)."
    exit 0
fi

BRIEF_PATH="$PROJECT_DIR/$BRIEF_FILE"

if [ ! -f "$BRIEF_PATH" ]; then
    echo "WARN: Brief indicado pero no encontrado en disco: $BRIEF_PATH"
    exit 0
fi

# --- Paso 2: Publicar en Telegraph ---
echo ""
echo ">>> Publicando en Telegraph..."
TELEGRAPH_OUTPUT=$(python3 "$PROJECT_DIR/scripts/publish_telegraph.py" "$BRIEF_PATH" 2>/dev/null || echo "")

if [ -n "$TELEGRAPH_OUTPUT" ]; then
    TELEGRAPH_URL=$(echo "$TELEGRAPH_OUTPUT" | awk '{print $2}')
    echo "  Telegraph: $TELEGRAPH_URL"

    # Notificar por Telegram con el link Telegraph
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
        TITLE=$(head -1 "$BRIEF_PATH" | sed 's/^# //')
        MSG="📌 Vídeo añadido manualmente
$TITLE
$TELEGRAPH_URL"
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d chat_id="${TELEGRAM_CHAT_ID}" \
            --data-urlencode "text=${MSG}" \
            > /dev/null
        echo "  Telegram: notificado."
    fi
else
    echo "  WARN: Telegraph no disponible. Brief guardado en disco."
fi

echo ""
echo "=========================================="
echo "Completado: $(date -u +%H:%M:%S) UTC"
echo "=========================================="
