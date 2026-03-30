#!/bin/bash
# OPENLAB Radar — Check previo de un vídeo
# Uso: ./scripts/check_video.sh "https://www.youtube.com/watch?v=VIDEO_ID"

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
echo "OPENLAB Radar — Check previo"
echo "Fecha: $TODAY"
echo "URL:   $URL"
echo "=========================================="
echo ""

claude -p "$(cat "$PROJECT_DIR/prompts/evaluate-check.md")

URL: $URL
Fecha: $TODAY" \
  --allowedTools "Read,Glob,mcp__youtube-transcript__get_transcript" \
  --output-format text
