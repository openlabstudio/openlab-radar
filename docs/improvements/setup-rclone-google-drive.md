# Setup: sincronizar briefs/ e insights/ con Google Drive

## Qué hace esto

Sincroniza automáticamente las carpetas `briefs/` e `insights/` del VPS con una carpeta compartida de Google Drive. El equipo puede acceder a los briefs y análisis desde Drive sin conectarse al VPS.

La sincronización se ejecuta al final del pipeline diario y del semanal.

## Estado actual

- rclone: **no instalado** en el VPS
- Carpeta de Drive: **pendiente de crear y decidir ruta**
- Cron: el pipeline ya está preparado para añadirlo

---

## Paso 1 — Crear la carpeta compartida en Google Drive

1. Abre Google Drive desde tu cuenta de OPENLAB
2. Crea una carpeta llamada `OPENLAB Radar`
3. Dentro, crea dos subcarpetas: `briefs` e `insights`
4. Comparte la carpeta `OPENLAB Radar` con el equipo (Editor o Lector según necesites)
5. Abre la carpeta `OPENLAB Radar` en Drive y copia el **ID de la carpeta** de la URL:
   ```
   https://drive.google.com/drive/folders/ESTE_ES_EL_ID
   ```
   Guárdalo — lo necesitarás en el Paso 4.

---

## Paso 2 — Instalar rclone en el VPS

Conéctate al VPS y ejecuta:

```bash
curl https://rclone.org/install.sh | sudo bash
rclone --version
```

Debe mostrar algo como `rclone v1.6x.x`.

---

## Paso 3 — Autorizar rclone con Google Drive (flujo headless)

El VPS no tiene navegador, así que la autorización OAuth se hace en dos partes: una en el VPS y otra en tu laptop.

### En el VPS — iniciar configuración

```bash
rclone config
```

Sigue estos pasos en el menú interactivo:
- `n` → New remote
- Name: `gdrive`
- Storage type: escribe `drive` (Google Drive)
- client_id: dejar vacío (Enter)
- client_secret: dejar vacío (Enter)
- scope: `1` (full access)
- root_folder_id: dejar vacío (Enter)
- service_account_file: dejar vacío (Enter)
- Edit advanced config: `n`
- Use auto config: **`n`** ← importante, el VPS no tiene navegador

El VPS mostrará un mensaje como:
```
Please go to the following link: https://accounts.google.com/o/oauth2/auth?...
Log in and authorize rclone, then paste the token below.
```

**Copia esa URL completa.**

### En tu laptop — autorizar

Abre la URL en tu navegador, inicia sesión con la cuenta de Google de OPENLAB y autoriza rclone.

Google mostrará un código de verificación. Cópialo.

### En el VPS — pegar el token

Pega el código en el VPS donde espera el input y pulsa Enter.

Continúa el menú:
- Configure as a Shared Drive (Team Drive): `n`
- Keep this remote: `y`
- Quit config: `q`

---

## Paso 4 — Verificar la conexión

```bash
rclone lsd gdrive:
```

Debe listar las carpetas de tu Google Drive. Si ves error, revisar el Paso 3.

Prueba que puedes acceder a la carpeta OPENLAB Radar:

```bash
rclone lsd "gdrive:OPENLAB Radar"
```

---

## Paso 5 — Configurar las rutas en .env

Edita `/home/openlab/openlab-radar/config/.env` y añade:

```bash
# Google Drive sync
GDRIVE_BRIEFS_PATH="gdrive:OPENLAB Radar/briefs"
GDRIVE_INSIGHTS_PATH="gdrive:OPENLAB Radar/insights"
```

Sustituye `OPENLAB Radar` por el nombre exacto de tu carpeta en Drive (respeta mayúsculas y espacios), o usa directamente el ID de carpeta del Paso 1:

```bash
GDRIVE_BRIEFS_PATH="gdrive:root/OPENLAB Radar/briefs"
# alternativa con ID (más robusto):
GDRIVE_BRIEFS_PATH="gdrive:ID_DE_CARPETA_BRIEFS"
GDRIVE_INSIGHTS_PATH="gdrive:ID_DE_CARPETA_INSIGHTS"
```

Para usar IDs (recomendado, evita problemas con nombres con espacios):
```bash
# Obtener el ID de una subcarpeta
rclone lsd "gdrive:OPENLAB Radar" --drive-formats id
```

---

## Paso 6 — Test manual de sincronización

```bash
cd /home/openlab/openlab-radar

# Dry run primero (no toca nada, solo muestra qué haría)
rclone sync briefs/ "$GDRIVE_BRIEFS_PATH" --dry-run -v
rclone sync insights/ "$GDRIVE_INSIGHTS_PATH" --dry-run -v

# Si el dry run parece correcto, ejecutar de verdad
rclone sync briefs/ "$GDRIVE_BRIEFS_PATH" -v
rclone sync insights/ "$GDRIVE_INSIGHTS_PATH" -v
```

Verifica en Google Drive que los ficheros han aparecido.

---

## Paso 7 — Añadir sync al pipeline diario

Edita `/home/openlab/openlab-radar/scripts/run_daily.sh` y añade al final, antes de los últimos `echo`:

```bash
# --- Paso 4: Sync con Google Drive ---
echo ""
echo ">>> PASO 4: Sync Google Drive"

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
```

Haz lo mismo en `run_weekly.sh` (al final, antes del último `echo`).

---

## Paso 8 — Verificar en el siguiente cron

Al día siguiente, comprueba el log:

```bash
tail -30 /home/openlab/openlab-radar/data/logs/cron.log | grep -A3 "Drive"
```

Debe mostrar `briefs/ sincronizado con Drive.` e `insights/ sincronizado con Drive.`

---

## Notas

- `rclone sync` es unidireccional: VPS → Drive. Los ficheros borrados en el VPS se borran también en Drive.
- Si quieres que Drive sea solo lectura (no borrar), usa `rclone copy` en lugar de `rclone sync`.
- El token de OAuth caduca ocasionalmente. Si falla, ejecutar `rclone config reconnect gdrive:` en el VPS.
- Los logs de rclone van al log del pipeline diario (`data/logs/cron.log`).
