# Harness Gap: Validación automática de briefs (sensores de feedback)

## Contexto

El Radar genera briefs vía Claude headless, pero no hay ningún mecanismo que valide que el output del modelo cumple las especificaciones. Si Claude genera un brief sin frontmatter, con campos vacíos, con un score incoherente o con tags que no existen en `config/tags.yaml`, nadie lo detecta hasta que un humano lo lee.

En términos de harness engineering, faltan **sensores de feedback computacionales** — validaciones deterministas, rápidas y baratas que corran después del modelo.

## Qué hay que construir

Un script `validate_brief.py` que reciba uno o más ficheros `.md` de brief y verifique:

### Validaciones estructurales (obligatorias)

1. **Frontmatter YAML presente y parseable** — el fichero debe empezar con `---` y tener un bloque YAML válido
2. **Campos obligatorios del frontmatter:**
   - `title` (string no vacío)
   - `date` (formato YYYY-MM-DD)
   - `category` (una de las 6 categorías válidas)
   - `score` (número entre 1.0 y 10.0)
   - `tags` (lista con 3-6 elementos)
   - `source` (string no vacío)
   - `url` (URL de YouTube válida)
3. **Tags válidos** — todos los tags deben existir en `config/tags.yaml`. Al menos 1 de `technical`, 1 de `openlab_relevance`, 1 de `signal_type`
4. **Secciones obligatorias presentes** en el cuerpo del brief:
   - `## Resumen ejecutivo`
   - `## Aplicabilidad OPENLAB`
   - `## Contenido detallado`
   - `## Temas clave`

### Validaciones de coherencia (deseables)

5. **Score coherente con subscores** — verificar que `score` ≈ (A×3 + B×2 + C×1) / 6 (tolerancia ±0.5)
6. **Categoría coherente con ruta** — el fichero debe estar en la carpeta que corresponde a su `category`
7. **Fecha coherente con nombre de fichero** — el `date` del frontmatter debe coincidir con el prefijo YYYY-MM-DD del nombre de fichero
8. **URL no duplicada** — el `url` no debe existir ya en otro brief (consultar `radar.db`)

### Output

- Exit code 0 si todo OK, exit code 1 si hay errores
- Por stdout: lista de errores con fichero, línea y descripción
- Formato parseable para que el pipeline pueda actuar sobre él

```
OK   briefs/context-engineering/2026-04-10-harness-engineering.md
FAIL briefs/agentic-systems/2026-04-10-multi-agent.md
  - frontmatter: campo 'score' ausente
  - tags: 'orchestration' no existe en tags.yaml
  - sección '## Aplicabilidad OPENLAB' no encontrada
```

## Dónde integrarlo

### Fase 1 — Post-pipeline (inmediato)

Añadir al final de `run_daily.sh`, después de la generación de briefs y antes de Telegraph/Telegram:

```bash
# Validar briefs generados hoy
BRIEF_FILES=$(find "$PROJECT_DIR/briefs" -mindepth 2 -name "${TODAY}*.md" -not -name "*briefing*" -type f)
if [ -n "$BRIEF_FILES" ]; then
    VALIDATION=$(python3 "$PROJECT_DIR/scripts/validate_brief.py" $BRIEF_FILES 2>&1)
    if [ $? -ne 0 ]; then
        notify_status "⚠️ VALIDACIÓN — Briefs con errores ($TODAY):
$VALIDATION"
    fi
fi
```

Mismo patrón para `add_video.sh` y `run_recovery.sh`.

### Fase 2 — Pre-publicación (bloqueo)

Una vez validado que el script funciona bien, convertirlo en **gate**: si la validación falla, no publicar en Telegraph ni notificar por Telegram. El brief queda en disco pero no se distribuye. Notificar el fallo para revisión manual.

## Dependencias

- `pyyaml` (ya instalado en el VPS para `generate_kb_viewer.py`)
- Acceso a `config/tags.yaml` y `data/radar.db`

## Esfuerzo estimado

Script + integración en pipelines: ~2h.
