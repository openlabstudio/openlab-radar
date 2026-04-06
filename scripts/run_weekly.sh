#!/bin/bash
# OPENLAB Radar - Digest Semanal
# Genera digest + publica en canal Telegram del equipo OPENLAB
# Diseñado para cron dominical en VPS

export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TODAY=$(date -u +%Y-%m-%d)
LOG_FILE="$PROJECT_DIR/data/logs/weekly-$TODAY.log"

mkdir -p "$PROJECT_DIR/data/logs"

exec > >(tee -a "$LOG_FILE") 2>&1

# Helper: enviar estado por Telegram
notify_status() {
    python3 "$PROJECT_DIR/scripts/notify.py" --status "$1" 2>/dev/null || true
}

# Trap: notificar si el pipeline muere inesperadamente
trap 'notify_status "🚨 ERROR — Digest semanal $TODAY ha fallado inesperadamente. Revisar log: data/logs/weekly-$TODAY.log"' ERR

echo "=========================================="
echo "OPENLAB Radar - Digest Semanal"
echo "Fecha: $TODAY"
echo "=========================================="

# --- Cargar variables de entorno ---
if [ -f "$PROJECT_DIR/config/.env" ]; then
    set -a
    source "$PROJECT_DIR/config/.env"
    set +a
fi

cd "$PROJECT_DIR"

# --- Paso 1: Generar digest ---
echo ""
echo ">>> PASO 1: Generar digest semanal"

DIGEST_FILE="$PROJECT_DIR/briefs/weekly-digests/$TODAY-weekly-digest.md"

claude -p "$(cat "$PROJECT_DIR/prompts/weekly-digest.md")

Fecha de hoy: $TODAY
Directorio de briefs: $PROJECT_DIR/briefs/
Base de datos: $PROJECT_DIR/data/radar.db

Analiza los briefings de los últimos 7 días y genera el digest semanal. Guarda el resultado en: $DIGEST_FILE" \
  --allowedTools "Read,Write,Glob,Bash" \
  --output-format text \
  > "$DIGEST_FILE" 2>/dev/null

if [ ! -s "$DIGEST_FILE" ]; then
    echo "ERROR: Digest vacío."
    exit 1
fi

echo "Digest generado: $DIGEST_FILE"

# --- Paso 2: Publicar en Telegraph + canal Telegram ---
echo ""
echo ">>> PASO 2: Publicar digest en Telegraph y canal Telegram"

TELEGRAPH_URL=""

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ] || [ -z "${TELEGRAM_CHANNEL_ID:-}" ]; then
    echo "WARN: TELEGRAM_BOT_TOKEN o TELEGRAM_CHANNEL_ID no configurados. Saltando publicación."
else
    # Publicar digest completo en Telegraph (Instant View en Telegram)
    TELEGRAPH_URL=$(python3 "$PROJECT_DIR/scripts/publish_telegraph.py" "$DIGEST_FILE" 2>/dev/null | cut -f2)

    if [ -n "$TELEGRAPH_URL" ]; then
        echo "Digest publicado en Telegraph: $TELEGRAPH_URL"

        # Extraer resumen corto para el mensaje de Telegram (primeras líneas)
        WEEK_START=$(date -u -d "$TODAY - 6 days" +%Y-%m-%d 2>/dev/null || date -u -v-6d +%Y-%m-%d)
        TEASER="OPENLAB Radar — Digest Semanal ${WEEK_START} a ${TODAY}"$'\n'$'\n'
        # Extraer línea de resumen si existe (Vídeos evaluados: X | ...)
        SUMMARY_LINE=$(grep -m1 "Vídeos evaluados\|evaluados esta semana" "$DIGEST_FILE" 2>/dev/null || true)
        if [ -n "$SUMMARY_LINE" ]; then
            TEASER+="${SUMMARY_LINE}"$'\n'$'\n'
        fi
        TEASER+="Digest completo:"$'\n'"${TELEGRAPH_URL}"

        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d chat_id="${TELEGRAM_CHANNEL_ID}" \
            --data-urlencode "text=${TEASER}" \
            > /dev/null
        echo "Link publicado en canal Telegram."
    else
        echo "WARN: Fallo publicando en Telegraph. Enviando digest como texto."
        # Fallback: enviar como texto (con chunking)
        DIGEST_CONTENT=$(cat "$DIGEST_FILE")
        MAX_LEN=4000
        if [ ${#DIGEST_CONTENT} -le $MAX_LEN ]; then
            curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
                -d chat_id="${TELEGRAM_CHANNEL_ID}" \
                --data-urlencode "text=${DIGEST_CONTENT}" \
                > /dev/null
        else
            REMAINING="$DIGEST_CONTENT"
            PART=1
            while [ ${#REMAINING} -gt 0 ]; do
                if [ ${#REMAINING} -le $MAX_LEN ]; then
                    CHUNK="$REMAINING"
                    REMAINING=""
                else
                    CHUNK="${REMAINING:0:$MAX_LEN}"
                    LAST_NL=$(echo "$CHUNK" | grep -aob $'\n' | tail -1 | cut -d: -f1)
                    if [ -n "$LAST_NL" ] && [ "$LAST_NL" -gt 2000 ]; then
                        CHUNK="${REMAINING:0:$LAST_NL}"
                        REMAINING="${REMAINING:$LAST_NL}"
                    else
                        REMAINING="${REMAINING:$MAX_LEN}"
                    fi
                fi
                curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
                    -d chat_id="${TELEGRAM_CHANNEL_ID}" \
                    --data-urlencode "text=${CHUNK}" \
                    > /dev/null
                PART=$((PART + 1))
                sleep 1
            done
        fi
        echo "Digest publicado como texto (fallback)."
    fi
fi

# --- Paso 3: Email digest al equipo (gws CLI) ---
echo ""
echo ">>> PASO 3: Email digest al equipo"

EMAIL_SENT=false
if [ -z "${DIGEST_EMAIL_RECIPIENTS:-}" ]; then
    echo "WARN: DIGEST_EMAIL_RECIPIENTS no configurado. Saltando email."
else
    WEEK_START=$(date -u -d "$TODAY - 6 days" +%Y-%m-%d 2>/dev/null || date -u -v-6d +%Y-%m-%d)
    SUBJECT="OPENLAB Radar — Digest Semanal $WEEK_START a $TODAY"

    HTML_BODY=$(python3 "$PROJECT_DIR/scripts/md_to_weekly_html.py" "$DIGEST_FILE" 2>/dev/null)
    if gws gmail +send \
        --to "$DIGEST_EMAIL_RECIPIENTS" \
        --subject "$SUBJECT" \
        --body "$HTML_BODY" \
        --html \
        2>/dev/null; then
        echo "Email enviado a: $DIGEST_EMAIL_RECIPIENTS"
        EMAIL_SENT=true
    else
        echo "ERROR: Fallo al enviar email. Verificar auth de gws."
        notify_status "⚠️ ALERTA — Email digest semanal ($TODAY) no pudo enviarse. Revisar auth gws."
    fi
fi

# --- Paso 4: Notificación de estado a Rafael ---
echo ""
echo ">>> PASO 4: Notificación de estado"

STATUS_MSG="✅ Digest semanal completado — $TODAY"
if [ "$EMAIL_SENT" = true ]; then
    STATUS_MSG+=$'\n'"📧 Email enviado a: ${DIGEST_EMAIL_RECIPIENTS:-equipo}"
fi
if [ -n "${TELEGRAPH_URL:-}" ]; then
    STATUS_MSG+=$'\n'"📖 Telegraph: ${TELEGRAPH_URL}"
fi
notify_status "$STATUS_MSG"
echo "Notificación de estado enviada a Rafael."

# --- Paso 5: Sync con Google Drive ---
echo ""
echo ">>> PASO 5: Sync Google Drive"

if [ -n "${GDRIVE_BRIEFS_PATH:-}" ]; then
    rclone sync "$PROJECT_DIR/briefs/" "$GDRIVE_BRIEFS_PATH" --quiet \
        && echo "briefs/ sincronizado con Drive." \
        || echo "WARN: Error sincronizando briefs/ con Drive."
fi

# insights/ NO se sincroniza desde el VPS — los insights se generan
# directamente en el Shared Drive desde los laptops del equipo.

echo ""
echo "=========================================="
echo "Digest semanal completado: $(date -u +%H:%M:%S) UTC"
echo "=========================================="
