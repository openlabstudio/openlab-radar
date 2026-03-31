#!/bin/bash
# OPENLAB Radar - Pipeline diario
# Scraper → evaluador → briefing a Rafael via Telegram Channel (bidireccional)
# Diseñado para cron en VPS

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TODAY=$(date -u +%Y-%m-%d)
LOG_FILE="$PROJECT_DIR/data/logs/run-$TODAY.log"

mkdir -p "$PROJECT_DIR/data/logs"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "=========================================="
echo "OPENLAB Radar - Pipeline Diario"
echo "Fecha: $TODAY $(date -u +%H:%M:%S) UTC"
echo "=========================================="

# --- Cargar variables de entorno ---
if [ -f "$PROJECT_DIR/config/.env" ]; then
    set -a
    source "$PROJECT_DIR/config/.env"
    set +a
fi

# --- Paso 1: Scraper ---
echo ""
echo ">>> PASO 1: Scraper de YouTube"
cd "$PROJECT_DIR"
python3 scripts/scraper.py

CANDIDATES_FILE="$PROJECT_DIR/data/candidates-$TODAY.json"
if [ ! -f "$CANDIDATES_FILE" ]; then
    echo "No hay candidatos hoy. Fin."
    exit 0
fi

CANDIDATE_COUNT=$(python3 -c "import json; print(len(json.load(open('$CANDIDATES_FILE'))))")
if [ "$CANDIDATE_COUNT" -eq 0 ]; then
    echo "0 candidatos. Fin."
    exit 0
fi

echo "Candidatos encontrados: $CANDIDATE_COUNT"

# --- Paso 2: Evaluador ---
echo ""
echo ">>> PASO 2: Evaluador"
BRIEFING_FILE="$PROJECT_DIR/briefs/daily-briefings/$TODAY-briefing.md"
mkdir -p "$PROJECT_DIR/briefs/daily-briefings"

claude -p "$(cat "$PROJECT_DIR/prompts/evaluate-daily.md")

Fecha de hoy: $TODAY
Fichero de candidatos: $CANDIDATES_FILE

Lee el fichero de candidatos y genera el briefing. Guarda el resultado en: $BRIEFING_FILE" \
  --allowedTools "Read,Write,Glob" \
  --output-format text

if [ ! -s "$BRIEFING_FILE" ]; then
    echo "ERROR: Briefing no generado. Abortando notificación."
    exit 1
fi

# --- Paso 2b: Notificación Telegram ---
echo ""
echo ">>> PASO 2b: Notificación Telegram"
python3 "$PROJECT_DIR/scripts/notify.py" "$BRIEFING_FILE" --telegram-only

# --- Paso 3: Publicar resúmenes en Telegraph ---
# Telegraph se integra con Telegram: los links se abren como Instant View
# dentro de la app, sin salir del chat. Ideal para leer briefs desde el móvil.
echo ""
echo ">>> PASO 3: Publicar resúmenes en Telegraph"

# Buscar briefs individuales de hoy (no el briefing resumen)
BRIEF_FILES=$(find "$PROJECT_DIR/briefs" -mindepth 2 -name "${TODAY}*.md" -type f 2>/dev/null | sort)

if [ -n "$BRIEF_FILES" ]; then
    TELEGRAPH_OUTPUT=$(python3 "$PROJECT_DIR/scripts/publish_telegraph.py" $BRIEF_FILES 2>/dev/null)

    if [ -n "$TELEGRAPH_OUTPUT" ]; then
        # Construir mensaje con links Telegraph
        LINKS_MSG="Briefs completos:"$'\n'
        while IFS=$'\t' read -r filepath url; do
            TITLE=$(head -1 "$filepath" | sed 's/^# //')
            LINKS_MSG+="$TITLE"$'\n'"$url"$'\n'$'\n'
        done <<< "$TELEGRAPH_OUTPUT"

        # Enviar links por Telegram (chat privado de Rafael)
        if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
            curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
                -d chat_id="${TELEGRAM_CHAT_ID}" \
                --data-urlencode "text=${LINKS_MSG}" \
                > /dev/null
            echo "Links Telegraph enviados por Telegram."
        fi

        echo "$TELEGRAPH_OUTPUT" | while IFS=$'\t' read -r filepath url; do
            echo "  Publicado: $url"
            # Escribir URL de vuelta al .md si no está ya
            if ! grep -q "^\*\*Telegraph:\*\*" "$filepath" 2>/dev/null; then
                python3 -c "
import re, sys
path, url = sys.argv[1], sys.argv[2]
content = open(path).read()
old = re.search(r'^- \*\*Fuente:\*\*', content, re.MULTILINE)
if old:
    insert = '- **Telegraph:** ' + url + '\n'
    content = content[:old.start()] + insert + content[old.start():]
    open(path, 'w').write(content)
" "$filepath" "$url" && echo "    URL escrita en $filepath"
            fi
        done
    else
        echo "WARN: No se pudieron publicar en Telegraph."
    fi
else
    echo "No hay briefs individuales para publicar."
fi

echo ""
echo "=========================================="
echo "Pipeline completado: $(date -u +%H:%M:%S) UTC"
echo "=========================================="

# --- Paso 4: Email diario (solo Rafael) ---
echo ""
echo ">>> PASO 4: Email diario"

if [ -n "${DIGEST_EMAIL_RECIPIENTS:-}" ] && [ -f "${BRIEFING_FILE:-}" ]; then
    SUBJECT="OPENLAB Radar — Briefing $TODAY"
    HTML_BODY=$(python3 "$PROJECT_DIR/scripts/md_to_email_html.py" "$BRIEFING_FILE" 2>/dev/null)
    if [ -n "$HTML_BODY" ]; then
        gws gmail +send             --to "rafa@openlabstudio.com"             --subject "$SUBJECT"             --body "$HTML_BODY"             --html             2>/dev/null             && echo "Email diario enviado a rafa@openlabstudio.com"             || echo "ERROR: Fallo al enviar email diario."
    fi
fi

# --- Paso 4b: Generar KB Viewer HTML ---
echo ""
echo ">>> PASO 4b: KB Viewer HTML"
python3 "$PROJECT_DIR/scripts/generate_kb_viewer.py" \
    --briefs-dir "$PROJECT_DIR/briefs" \
    --insights-dir "$PROJECT_DIR/insights" \
    --output "$PROJECT_DIR/data/kb_viewer.html" \
    && echo "KB Viewer generado: data/kb_viewer.html" \
    || echo "WARN: Error generando KB Viewer (no crítico)."

# --- Paso 5: Sync con Google Drive ---
echo ""
echo ">>> PASO 5: Sync Google Drive"

if [ -n "${GDRIVE_BRIEFS_PATH:-}" ]; then
    rclone sync "$PROJECT_DIR/briefs/" "$GDRIVE_BRIEFS_PATH" --quiet \
        && echo "briefs/ sincronizado con Drive." \
        || echo "WARN: Error sincronizando briefs/ con Drive."
fi

if [ -n "${GDRIVE_INSIGHTS_PATH:-}" ]; then
    rclone sync "$PROJECT_DIR/insights/" "$GDRIVE_INSIGHTS_PATH" --quiet \
        && echo "insights/ sincronizado con Drive." \
        || echo "WARN: Error sincronizando insights/ con Drive."
fi

# Subir KB Viewer a la raíz del directorio radar en Drive
if [ -f "$PROJECT_DIR/data/kb_viewer.html" ] && [ -n "${GDRIVE_RADAR_ROOT:-}" ]; then
    rclone copyto "$PROJECT_DIR/data/kb_viewer.html" \
        "${GDRIVE_RADAR_ROOT}/kb_viewer.html" --quiet \
        && echo "KB Viewer sincronizado con Drive: ${GDRIVE_RADAR_ROOT}/kb_viewer.html" \
        || echo "WARN: Error sincronizando KB Viewer con Drive."
fi
