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

# Helper: enviar estado por Telegram (no falla el pipeline si Telegram falla)
notify_status() {
    python3 "$PROJECT_DIR/scripts/notify.py" --status "$1" 2>/dev/null || true
}

# Trap: notificar si el pipeline muere inesperadamente
trap 'notify_status "🚨 ERROR — Pipeline diario $TODAY ha fallado inesperadamente. Revisar log: data/logs/run-$TODAY.log"' ERR

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

# --- Check previo: youtube-transcript-api ---
echo ""
echo ">>> CHECK: youtube-transcript-api"
TRANSCRIPT_CHECK=$(python3 - <<'PYEOF' 2>&1
import os, sys
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import IpBlocked
    from youtube_transcript_api.proxies import WebshareProxyConfig, GenericProxyConfig

    username = os.environ.get("WEBSHARE_USERNAME", "").strip()
    password = os.environ.get("WEBSHARE_PASSWORD", "").strip()
    proxy_url = os.environ.get("YOUTUBE_PROXY_URL", "").strip()

    if username and password:
        proxy_config = WebshareProxyConfig(proxy_username=username, proxy_password=password, retries_when_blocked=3)
    elif proxy_url:
        proxy_config = GenericProxyConfig(http_url=proxy_url, https_url=proxy_url)
    else:
        proxy_config = None

    api = YouTubeTranscriptApi(proxy_config=proxy_config)
    # Video de test: TED Talk corto, siempre disponible con transcripts
    t = api.fetch("8S0FDjFBj8o", languages=["en"])
    snippets = t.to_raw_data()
    if snippets:
        print("OK")
    else:
        print("EMPTY")
except IpBlocked:
    print("IP_BLOCKED")
except Exception as e:
    print(f"ERROR:{e}")
PYEOF
)

echo "Resultado check transcript: $TRANSCRIPT_CHECK"
if [[ "$TRANSCRIPT_CHECK" != "OK" ]]; then
    notify_status "⚠️ ALERTA — youtube-transcript-api ($TODAY): $TRANSCRIPT_CHECK. Los briefs de hoy se generarán solo con título + descripción (calidad reducida). Revisar config o actualizar librería."
    echo "WARN: Transcript check fallido — continuando pipeline con calidad reducida."
else
    echo "Transcript API: OK"
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

# --- Paso 2: Evaluador (con retry) ---
echo ""
echo ">>> PASO 2: Evaluador"
BRIEFING_FILE="$PROJECT_DIR/briefs/daily-briefings/$TODAY-briefing.md"
mkdir -p "$PROJECT_DIR/briefs/daily-briefings"

MAX_RETRIES=3
RETRY_WAIT=900  # 15 minutos
EVALUADOR_OK=false

for attempt in $(seq 1 $MAX_RETRIES); do
    echo "  Intento $attempt/$MAX_RETRIES..."
    if claude -p "$(cat "$PROJECT_DIR/prompts/evaluate-daily.md")

Fecha de hoy: $TODAY
Fichero de candidatos: $CANDIDATES_FILE

Lee el fichero de candidatos y genera el briefing. Guarda el resultado en: $BRIEFING_FILE" \
      --allowedTools "Read,Write,Glob,mcp__youtube-transcript__get_transcript" \
      --output-format text; then
        EVALUADOR_OK=true
        break
    else
        echo "  WARN: Evaluador falló (intento $attempt/$MAX_RETRIES)"
        if [ $attempt -lt $MAX_RETRIES ]; then
            notify_status "⚠️ Evaluador falló (intento $attempt/$MAX_RETRIES, $TODAY) — reintentando en 15 min"
            sleep $RETRY_WAIT
        fi
    fi
done

if [ "$EVALUADOR_OK" = false ]; then
    notify_status "🚨 ERROR — Evaluador falló tras $MAX_RETRIES intentos ($TODAY). Pipeline abortado. Revisar log."
    echo "ERROR: Evaluador falló tras $MAX_RETRIES intentos. Abortando."
    exit 1
fi

if [ ! -s "$BRIEFING_FILE" ]; then
    notify_status "🚨 ERROR — Evaluador completó sin generar briefing ($TODAY). Revisar log."
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
            # Escribir URL de vuelta al .md (frontmatter YAML + cuerpo)
            if ! grep -q "^\*\*Telegraph:\*\*" "$filepath" 2>/dev/null; then
                python3 -c "
import re, sys
sys.path.insert(0, '$(dirname "$0")')
path, url = sys.argv[1], sys.argv[2]
content = open(path).read()

# 1. Inyectar telegraph_url en frontmatter YAML
try:
    import yaml
    m = re.match(r'^---\n(.*?)\n---(\s*\n?)(.*)', content, re.DOTALL)
    if m:
        fm = yaml.safe_load(m.group(1)) or {}
        if 'telegraph_url' not in fm:
            fm['telegraph_url'] = url
            yaml_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False, width=200)
            content = '---\n' + yaml_str + '---' + m.group(2) + m.group(3)
except Exception:
    pass

# 2. Inyectar en cuerpo (antes de Fuente)
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

EMAIL_SENT=false
if [ -n "${DIGEST_EMAIL_RECIPIENTS:-}" ] && [ -f "${BRIEFING_FILE:-}" ]; then
    SUBJECT="OPENLAB Radar — Briefing $TODAY"
    HTML_BODY=$(python3 "$PROJECT_DIR/scripts/md_to_email_html.py" "$BRIEFING_FILE" 2>/dev/null)
    if [ -n "$HTML_BODY" ]; then
        if gws gmail +send \
            --to "rafa@openlabstudio.com" \
            --subject "$SUBJECT" \
            --body "$HTML_BODY" \
            --html \
            2>/dev/null; then
            echo "Email diario enviado a rafa@openlabstudio.com"
            EMAIL_SENT=true
        else
            echo "ERROR: Fallo al enviar email diario."
            notify_status "⚠️ ALERTA — Email diario ($TODAY) no pudo enviarse. Revisar auth gws."
        fi
    fi
fi

# Notificación de estado al finalizar el pipeline
BRIEF_COUNT=$(find "$PROJECT_DIR/briefs" -mindepth 2 -name "${TODAY}*.md" -not -name "*briefing*" -type f 2>/dev/null | wc -l | tr -d ' ')
TRANSCRIPT_STATUS=""
if [[ "${TRANSCRIPT_CHECK:-}" != "OK" ]]; then
    TRANSCRIPT_STATUS=$'\n'"⚠️ Transcripts: ${TRANSCRIPT_CHECK:-desconocido} (briefs sin transcript)"
fi
EMAIL_STATUS=""
if [ "$EMAIL_SENT" = true ]; then
    EMAIL_STATUS=$'\n'"📧 Email enviado a rafa@openlabstudio.com"
fi
notify_status "✅ Pipeline diario completado — $TODAY"$'\n'"📺 $CANDIDATE_COUNT candidatos → $BRIEF_COUNT briefs generados${TRANSCRIPT_STATUS}${EMAIL_STATUS}"

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

# insights/ NO se sincroniza desde el VPS — los insights se generan
# directamente en el Shared Drive desde los laptops del equipo.

# Subir KB Viewer a la raíz del directorio radar en Drive
if [ -f "$PROJECT_DIR/data/kb_viewer.html" ] && [ -n "${GDRIVE_RADAR_ROOT:-}" ]; then
    rclone copyto "$PROJECT_DIR/data/kb_viewer.html" \
        "${GDRIVE_RADAR_ROOT}/kb_viewer.html" --quiet \
        && echo "KB Viewer sincronizado con Drive: ${GDRIVE_RADAR_ROOT}/kb_viewer.html" \
        || echo "WARN: Error sincronizando KB Viewer con Drive."
fi
