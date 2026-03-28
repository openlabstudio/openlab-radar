# Pasos para terminar rclone auth — leer ANTES de cerrar VS Code

## Situación actual
- El terminal SSH tiene `rclone config` esperando en `config_token>`
- VS Code ocupa el puerto 53682 que necesita rclone en el laptop
- Hay que cerrar VS Code para liberar el puerto

---

## Pasos en orden

### 1. Cierra VS Code

### 2. En Terminal.app ejecuta este comando exacto:
```
rclone authorize "drive" "eyJzY29wZSI6ImRyaXZlIn0"
```
- Se abre el navegador automáticamente
- Autoriza con rafa@openlabstudio.com
- Vuelves al terminal y verás un bloque JSON con el token — cópialo entero

### 3. Ve al terminal SSH (sigue abierto con `config_token>` esperando)
Pega el token JSON y pulsa Enter

### 4. Sigue el menú de rclone config:
- Configure this as a Shared Drive (Team Drive)? → `y`
- rclone lista los Shared Drives → selecciona `OPENLAB-RADAR`
- Keep this remote? → `y`
- Quit config → `q`

### 5. Verifica que funciona:
```bash
rclone lsd gdrive:
```
Debe listar el contenido del Shared Drive OPENLAB-RADAR

### 6. Test de sync:
```bash
cd /home/openlab/openlab-radar
source config/.env
rclone sync briefs/ "$GDRIVE_BRIEFS_PATH" --dry-run -v
```
Si el dry-run parece correcto:
```bash
rclone sync briefs/ "$GDRIVE_BRIEFS_PATH" -v
rclone sync insights/ "$GDRIVE_INSIGHTS_PATH" -v
```

### 7. Reabre VS Code y reconecta al VPS
Una vez dentro, continúa con Claude Code para añadir el sync al pipeline diario.

---

## Qué queda después de esto (Claude Code lo hace)
- Añadir el sync rclone al final de `scripts/run_daily.sh`
- Añadir el sync rclone al final de `scripts/run_weekly.sh`
- Verificar en el siguiente cron que sincroniza solo

---

**Este fichero se puede borrar cuando rclone esté funcionando.**
