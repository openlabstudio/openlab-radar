#!/bin/bash
# OPENLAB Radar - Envío de email via Claude Code + Gmail MCP (OBSOLETO)
# Uso: bash notify_email.sh <briefing_file>

BRIEFING_FILE="$1"

if [ -z "$BRIEFING_FILE" ] || [ ! -f "$BRIEFING_FILE" ]; then
    echo "ERROR: Fichero de briefing no encontrado: $BRIEFING_FILE" >&2
    exit 1
fi

BRIEFING_CONTENT=$(cat "$BRIEFING_FILE")
TODAY=$(date +%Y-%m-%d)

# Invocar Claude Code en modo headless para enviar email via Gmail MCP
claude -p "Envía un email draft usando Gmail MCP con estos datos:
- To: rafa@openlabstudio.com
- Subject: OPENLAB Radar Briefing - $TODAY
- Body: el contenido del briefing que te pego a continuación. Formatea como HTML limpio.

BRIEFING:
$BRIEFING_CONTENT

Usa la herramienta gmail_create_draft para crear el borrador. Luego confirma que se ha creado." \
  --allowedTools "mcp__claude_ai_Gmail__gmail_create_draft" \
  --output-format text \
  2>/dev/null

exit $?
