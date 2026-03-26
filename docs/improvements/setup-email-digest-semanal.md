# Setup: envío de digest semanal por email (Gmail)

## Qué hace esto

Cada viernes a las 09:30 CET, el pipeline semanal genera el digest y lo envía por email al equipo de OPENLAB. El script `run_weekly.sh` ya tiene el paso implementado — solo falta autenticar `gws` (Google Workspace CLI) y configurar los destinatarios.

## Estado actual

- `run_weekly.sh`: el Paso 3 (email) **ya está implementado**, usa `gws gmail +send`
- `gws`: **instalado** en el VPS, **pendiente de auth**
- `DIGEST_EMAIL_RECIPIENTS`: **no configurado** en `.env`

---

## Paso 1 — Verificar que gws está instalado

```bash
gws --version
```

Si no está instalado:

```bash
# Instalar gws (Google Workspace CLI)
pip3 install --user --break-system-packages gws
# o
pip3 install gws
```

---

## Paso 2 — Autenticar gws con la cuenta de Google de OPENLAB

La autenticación requiere un navegador. Como el VPS no tiene navegador, hay que hacerlo con el flag de redirección manual.

### Opción A — Desde tu laptop (más fácil)

Si tienes `gws` instalado en el laptop:

```bash
gws auth login
```

Abre el navegador, autoriza con la cuenta de Gmail de OPENLAB y sigue el flujo. Una vez autenticado, el token se guarda en `~/.config/gws/`.

Luego copia el token al VPS:

```bash
scp -r ~/.config/gws/ openlab@212.227.104.123:~/.config/gws/
```

### Opción B — Directamente en el VPS

```bash
gws auth login --no-browser
```

Mostrará una URL. Ábrela en tu navegador local, autoriza y pega el código de verificación en el VPS.

### Verificar autenticación

```bash
gws gmail profile
```

Debe mostrar la dirección de email de la cuenta autenticada (ej. `rafa@openlabstudio.com`).

---

## Paso 3 — Configurar destinatarios en .env

Edita `/home/openlab/openlab-radar/config/.env` y añade:

```bash
# Email digest semanal
DIGEST_EMAIL_RECIPIENTS="rafa@openlabstudio.com,compañero1@openlabstudio.com,compañero2@openlabstudio.com"
```

Separa los emails con comas, sin espacios.

---

## Paso 4 — Test manual del envío

Antes de dejarlo en el cron, prueba con un digest existente:

```bash
cd /home/openlab/openlab-radar
source config/.env

# Usa el último digest generado (o cualquier briefing como prueba)
DIGEST_FILE=$(ls briefs/weekly-digests/*.md 2>/dev/null | tail -1)

# Si no hay digest semanal todavía, usa el último briefing diario
if [ -z "$DIGEST_FILE" ]; then
    DIGEST_FILE=$(ls briefs/daily-briefings/*.md | tail -1)
fi

echo "Enviando: $DIGEST_FILE"

gws gmail +send \
    --to "$DIGEST_EMAIL_RECIPIENTS" \
    --subject "TEST — OPENLAB Radar Digest" \
    --body "$(cat "$DIGEST_FILE")"
```

Comprueba que llega a los destinatarios. El email llegará en texto plano — ver Paso 5 para mejorar el formato.

---

## Paso 5 — (Opcional) Mejorar formato del email a HTML

El script actual envía el digest en texto plano (markdown). Para enviarlo en HTML con formato, sustituye el Paso 3 del `run_weekly.sh` por esta versión:

```bash
# --- Paso 3: Email digest al equipo ---
echo ""
echo ">>> PASO 3: Email digest al equipo"

if [ -z "${DIGEST_EMAIL_RECIPIENTS:-}" ]; then
    echo "WARN: DIGEST_EMAIL_RECIPIENTS no configurado. Saltando email."
else
    WEEK_START=$(date -u -d "$TODAY - 6 days" +%Y-%m-%d 2>/dev/null || date -u -v-6d +%Y-%m-%d)
    SUBJECT="OPENLAB Radar — Digest Semanal $WEEK_START a $TODAY"
    BODY="$(cat "$DIGEST_FILE")"

    # Si hay link de Telegraph, añadirlo como primera línea
    if [ -n "${TELEGRAPH_URL:-}" ]; then
        BODY="Digest completo con formato: ${TELEGRAPH_URL}"$'\n\n'"${BODY}"
    fi

    gws gmail +send \
        --to "$DIGEST_EMAIL_RECIPIENTS" \
        --subject "$SUBJECT" \
        --body "$BODY" \
        && echo "Email enviado a: $DIGEST_EMAIL_RECIPIENTS" \
        || echo "ERROR: Fallo al enviar email. Verificar: gws gmail profile"
fi
```

**Nota:** si el digest semanal se publica en Telegraph, el email incluirá el link de Telegraph como primera línea — el destinatario puede abrirlo con formato completo.

---

## Paso 6 — Verificar en el siguiente cron semanal

El cron semanal corre los **viernes a las 09:30 CET** (configurado en el crontab de root):

```bash
sudo crontab -l | grep weekly
```

Tras el primer viernes, verifica el log:

```bash
cat /home/openlab/openlab-radar/data/logs/weekly-$(date +%Y-%m-%d).log | grep -A3 "Email"
```

Debe mostrar: `Email enviado a: rafa@openlabstudio.com,...`

---

## Troubleshooting

**Error: `gws: command not found`**
```bash
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

**Error: `Authentication required` o token expirado**
```bash
gws auth login
# Repetir Paso 2
```

**El email llega vacío o con error de formato**
- Verificar que el digest existe: `ls briefs/weekly-digests/`
- Verificar que no está vacío: `wc -l briefs/weekly-digests/FECHA-weekly-digest.md`
- Probar el envío manual del Paso 4

**gws no reconoce `+send`**
- Verificar versión: `gws --version`
- El comando correcto puede variar por versión. Alternativas:
  ```bash
  gws gmail send ...
  gws gmail create-draft ...
  ```
  Consultar: `gws gmail --help`

---

## Resumen de variables necesarias en .env

```bash
# Ya debe existir (Telegram)
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
TELEGRAM_CHANNEL_ID=...

# Añadir para email
DIGEST_EMAIL_RECIPIENTS="rafa@openlabstudio.com,email2@openlabstudio.com"
```
