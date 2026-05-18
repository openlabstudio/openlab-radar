# Harness Gap: Bucle de autocorrección de briefs

## Contexto

Actualmente, si Claude genera un brief defectuoso (faltan secciones, frontmatter incorrecto, score sin sentido), no hay mecanismo para detectarlo y relanzar la generación. El brief se publica tal cual o se queda roto en disco.

En términos de harness engineering, falta un **bucle de feedback**: validar → detectar error → corregir → re-validar.

## Prerrequisito

Este improvement depende de `harness-validacion-briefs.md` (el validador `validate_brief.py`). Sin sensores no hay bucle.

## Qué hay que construir

### Opción A — Reintento completo (simple)

Si `validate_brief.py` falla para un brief, relanzar `claude -p` con el mismo prompt + el brief fallido + los errores de validación como contexto adicional.

Flujo en `run_daily.sh`:

```bash
# Después de la generación inicial
for BRIEF in $BRIEF_FILES; do
    ERRORS=$(python3 "$PROJECT_DIR/scripts/validate_brief.py" "$BRIEF" 2>&1)
    if [ $? -ne 0 ]; then
        echo "Brief con errores, reintentando: $BRIEF"
        claude -p "El siguiente brief tiene errores de validación. Corrígelo IN PLACE manteniendo todo el contenido válido.

Fichero: $BRIEF
Errores detectados:
$ERRORS

Lee el fichero, corrige SOLO los errores indicados, y reescríbelo." \
          --allowedTools "Read,Write" \
          --output-format text

        # Re-validar
        python3 "$PROJECT_DIR/scripts/validate_brief.py" "$BRIEF" 2>&1
        if [ $? -ne 0 ]; then
            notify_status "⚠️ Brief $BRIEF sigue con errores tras autocorrección. Requiere revisión manual."
        fi
    fi
done
```

**Ventaja:** simple, reutiliza el validador.
**Riesgo:** el reintento consume tokens y tiempo. Limitar a 1 reintento para evitar bucles infinitos.

### Opción B — Corrección inline en el prompt (preventiva)

Añadir una etapa final al prompt `evaluate-daily.md` que le pida al propio modelo validar su output antes de darlo por terminado:

```markdown
### ETAPA 5 — Autovalidación

Antes de terminar, para cada brief generado:
1. Verifica que el frontmatter tiene todos los campos obligatorios
2. Verifica que los tags existen en config/tags.yaml
3. Verifica que score = (A×3 + B×2 + C×1) / 6
4. Verifica que las 4 secciones obligatorias están presentes
5. Si detectas errores, corrígelos y reescribe el fichero
```

**Ventaja:** no consume un segundo `claude -p`, corre dentro de la misma sesión.
**Riesgo:** es un control inferencial (el modelo validándose a sí mismo), menos fiable que un control computacional. Funciona mejor como complemento de la Opción A, no como sustituto.

### Recomendación

Implementar **ambas**:
- Opción B como primera línea de defensa (barata, dentro del prompt)
- Opción A como red de seguridad (computacional, después del modelo)

## Límites del bucle

- Máximo **1 reintento** por brief (Opción A)
- Si el reintento falla, marcar el brief como `status: needs-review` en `radar.db` y notificar por Telegram
- Nunca publicar en Telegraph un brief que no pase validación

## Esfuerzo estimado

- Opción B (añadir etapa al prompt): ~30min
- Opción A (script de reintento + integración): ~1.5h
- Ambas: ~2h (después de tener `validate_brief.py` funcionando)
