#!/bin/bash
# OPENLAB Radar - Pipeline de recuperación
# Se ejecuta 2h después del pipeline diario (09:00 UTC).
# Si el briefing de hoy no existe, relanza evaluador + KB Viewer + sync Drive.
# No reenvía email.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TODAY=$(date -u +%Y-%m-%d)
LOG_FILE="$PROJECT_DIR/data/logs/cron-recovery.log"

mkdir -p "$PROJECT_DIR/data/logs"
exec >> "$LOG_FILE" 2>&1

# Cargar variables de entorno
if [ -f "$PROJECT_DIR/config/.env" ]; then
    set -a
    source "$PROJECT_DIR/config/.env"
    set +a
fi

BRIEFING_FILE="$PROJECT_DIR/briefs/daily-briefings/$TODAY-briefing.md"

# Si el briefing ya existe y tiene contenido, nada que hacer
if [ -s "$BRIEFING_FILE" ]; then
    exit 0
fi

echo ""
echo "=========================================="
echo "OPENLAB Radar - Pipeline de Recuperación"
echo "Fecha: $TODAY $(date -u +%H:%M:%S) UTC"
echo "=========================================="

notify_status() {
    python3 "$PROJECT_DIR/scripts/notify.py" --status "$1" 2>/dev/null || true
}

trap 'notify_status "🚨 ERROR — Recovery $TODAY falló inesperadamente. Revisar log: data/logs/cron-recovery.log"' ERR

notify_status "⚠️ Recovery — El briefing de $TODAY no fue generado por el pipeline principal. Relanzando evaluador."

# Si tampoco hay candidatos, relanzar el scraper primero
CANDIDATES_FILE="$PROJECT_DIR/data/candidates-$TODAY.json"
if [ ! -f "$CANDIDATES_FILE" ]; then
    echo "No hay candidatos. Relanzando scraper..."
    cd "$PROJECT_DIR"
    python3 scripts/scraper.py
fi

if [ ! -f "$CANDIDATES_FILE" ]; then
    notify_status "🚨 Recovery — Scraper no generó candidatos ($TODAY). Abortando."
    exit 1
fi

# Evaluador
echo "Relanzando evaluador..."
cd "$PROJECT_DIR"
claude -p "$(cat "$PROJECT_DIR/prompts/evaluate-daily.md")

Fecha de hoy: $TODAY
Fichero de candidatos: $CANDIDATES_FILE

Lee el fichero de candidatos y genera el briefing. Guarda el resultado en: $BRIEFING_FILE" \
  --allowedTools "Read,Write,Glob,mcp__youtube-transcript__get_transcript" \
  --output-format text

if [ ! -s "$BRIEFING_FILE" ]; then
    notify_status "🚨 Recovery — Evaluador no generó briefing ($TODAY). Revisar manualmente."
    exit 1
fi

# Telegram
python3 "$PROJECT_DIR/scripts/notify.py" "$BRIEFING_FILE" --telegram-only

# Telegraph
BRIEF_FILES=$(find "$PROJECT_DIR/briefs" -mindepth 2 -name "${TODAY}*.md" -type f 2>/dev/null | sort)
if [ -n "$BRIEF_FILES" ]; then
    python3 "$PROJECT_DIR/scripts/publish_telegraph.py" $BRIEF_FILES 2>/dev/null || true
fi

# KB Viewer
python3 "$PROJECT_DIR/scripts/generate_kb_viewer.py" \
    --briefs-dir "$PROJECT_DIR/briefs" \
    --insights-dir "$PROJECT_DIR/insights" \
    --output "$PROJECT_DIR/data/kb_viewer.html" \
    && echo "KB Viewer generado." \
    || echo "WARN: Error generando KB Viewer."

# Sync Drive
if [ -n "${GDRIVE_BRIEFS_PATH:-}" ]; then
    rclone sync "$PROJECT_DIR/briefs/" "$GDRIVE_BRIEFS_PATH" --quiet \
        && echo "briefs/ sincronizado." || echo "WARN: Error sync briefs."
fi
if [ -n "${GDRIVE_INSIGHTS_PATH:-}" ]; then
    rclone sync "$PROJECT_DIR/insights/" "$GDRIVE_INSIGHTS_PATH" --quiet \
        && echo "insights/ sincronizado." || echo "WARN: Error sync insights."
fi
if [ -f "$PROJECT_DIR/data/kb_viewer.html" ] && [ -n "${GDRIVE_RADAR_ROOT:-}" ]; then
    rclone copyto "$PROJECT_DIR/data/kb_viewer.html" "${GDRIVE_RADAR_ROOT}/kb_viewer.html" --quiet \
        && echo "KB Viewer sincronizado con Drive." || echo "WARN: Error sync KB Viewer."
fi

notify_status "✅ Recovery completado — Briefing $TODAY generado y sincronizado."
echo "Recovery completado: $(date -u +%H:%M:%S) UTC"
