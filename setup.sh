#!/bin/bash
# OPENLAB Radar - Setup para VPS
# Ejecutar una vez para instalar dependencias y configurar crons

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== OPENLAB Radar Setup ==="
echo "Directorio: $PROJECT_DIR"
echo ""

# --- 1. Dependencias Python ---
echo ">>> Instalando dependencias Python..."
pip3 install --user google-api-python-client pyyaml requests markdown

# --- 2. Crear directorios ---
echo ">>> Creando directorios..."
mkdir -p "$PROJECT_DIR"/{data/logs,briefs}

# --- 3. Permisos de ejecución ---
echo ">>> Configurando permisos..."
chmod +x "$PROJECT_DIR/scripts/"*.sh
chmod +x "$PROJECT_DIR/scripts/"*.py

# --- 4. Verificar .env ---
if [ ! -f "$PROJECT_DIR/config/.env" ]; then
    echo ""
    echo "IMPORTANTE: Copia y configura el fichero de variables de entorno:"
    echo "  cp $PROJECT_DIR/config/.env.example $PROJECT_DIR/config/.env"
    echo "  nano $PROJECT_DIR/config/.env"
    echo ""
fi

# --- 5. Configurar crontab ---
echo ">>> Configurando crontab..."

# Generar las líneas de cron
CRON_DAILY="0 6 * * * cd $PROJECT_DIR && bash scripts/run_daily.sh >> data/logs/cron.log 2>&1"
CRON_WEEKLY="0 10 * * 0 cd $PROJECT_DIR && bash scripts/run_weekly.sh >> data/logs/cron.log 2>&1"

# Comprobar si ya existen
EXISTING_CRON=$(crontab -l 2>/dev/null || true)

if echo "$EXISTING_CRON" | grep -q "openlab-radar"; then
    echo "Crons de OPENLAB Radar ya existen. Saltando."
else
    echo ""
    echo "Se añadirán estos crons:"
    echo "  Diario (06:00 UTC):   $CRON_DAILY"
    echo "  Semanal (dom 10:00):  $CRON_WEEKLY"
    echo ""
    read -p "¿Confirmar? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        (echo "$EXISTING_CRON"; echo "# openlab-radar - daily"; echo "$CRON_DAILY"; echo "# openlab-radar - weekly digest"; echo "$CRON_WEEKLY") | crontab -
        echo "Crons instalados."
    else
        echo "Crons NO instalados. Puedes añadirlos manualmente con: crontab -e"
    fi
fi

# --- 6. Test rápido ---
echo ""
echo ">>> Verificando configuración..."

if [ -f "$PROJECT_DIR/config/.env" ]; then
    source "$PROJECT_DIR/config/.env"
    if [ -n "${YOUTUBE_API_KEY:-}" ] && [ "$YOUTUBE_API_KEY" != "tu-api-key-aquí" ]; then
        echo "  YouTube API key: OK"
    else
        echo "  YouTube API key: NO CONFIGURADA"
    fi
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ "$TELEGRAM_BOT_TOKEN" != "tu-bot-token-aquí" ]; then
        echo "  Telegram: OK"
    else
        echo "  Telegram: NO CONFIGURADO (opcional)"
    fi
    if [ -n "${TELEGRAPH_ACCESS_TOKEN:-}" ]; then
        echo "  Telegraph: OK"
    else
        echo "  Telegraph: NO CONFIGURADO (se creará automáticamente en la primera ejecución)"
    fi
else
    echo "  .env: NO ENCONTRADO - configúralo primero"
fi

# Verificar Claude Code
if command -v claude &>/dev/null; then
    echo "  Claude Code: OK"
else
    echo "  Claude Code: NO ENCONTRADO en PATH"
fi

echo ""
echo "=== Setup completado ==="
echo ""
echo "Próximos pasos:"
echo "  1. Configura .env:  cp config/.env.example config/.env && nano config/.env"
echo "  2. Test dry run:    python3 scripts/scraper.py --dry-run"
echo "  3. Test completo:   bash scripts/run_daily.sh"
