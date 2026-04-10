# Harness Gap: Fitness functions arquitectónicas

## Contexto

El Radar funciona día a día, pero no hay mecanismo que vigile que el sistema **como un todo** mantiene sus propiedades a lo largo del tiempo. Preguntas como:

- ¿Estamos cubriendo todas las categorías o hay un sesgo creciente hacia `claude-code-advanced`?
- ¿Los scores están inflados? ¿La media ha subido sin justificación?
- ¿Hay tags que nunca se usan o tags nuevos que deberían existir?
- ¿Hay canales que generan mucho ruido y poca señal?

Estas son **fitness functions arquitectónicas** — métricas que verifican que el sistema mantiene las características deseadas. El skill `radar-lint` ya responde algunas de estas preguntas, pero corre bajo demanda y depende de que alguien lo lance. Para ser harness, debe correr automáticamente.

## Qué hay que construir

Un script `radar_health_check.py` que genere un informe de salud semanal con métricas computacionales (no inferenciales — sin usar Claude).

### Métricas a calcular

#### Cobertura por categoría (últimos 7 y 30 días)

```
Categoría               7d    30d   Total   Tendencia
context-engineering      3     12     45    ━━━━━━━━
claude-code-advanced     5     18     62    ━━━━━━━━━━━
agentic-systems          1      4     23    ━━━━━
enterprise-ai            0      2     15    ━━━━      ⚠️ sin cobertura 7d
cli-vs-platforms         2      6     19    ━━━━━━
delivery-adoption        0      1      8    ━━        ⚠️ baja cobertura
```

- **Alerta** si una categoría tiene 0 briefs en los últimos 7 días
- **Alerta** si una categoría concentra >50% de los briefs del mes

#### Distribución de scores

```
Score medio (7d):  7.4  (30d: 7.2)
Score medio total: 7.1
Distribución:
  9-10: ██ 4%
  7-8:  ████████████ 58%
  5-6:  ██████ 31%
  <5:   ██ 7%
```

- **Alerta** si el score medio sube >0.5 puntos respecto al mes anterior (posible inflación)
- **Alerta** si >80% de briefs están en el rango 7-8 (falta discriminación)

#### Salud de tags

- Tags usados 0 veces en los últimos 30 días
- Tags más frecuentes (posible sobre-uso)
- Combinaciones de tags que nunca aparecen juntas (posibles gaps)

#### Rendimiento de canales

- Ratio selección/descarte por canal (últimos 30 días)
- Canales con >10 vídeos scrapeados y 0 seleccionados → candidatos a eliminar de `channels.yaml`
- Canales nuevos (aparecidos en briefs recientes pero no en `channels.yaml`) → candidatos a añadir

#### Tasa de fallos del pipeline

- Días sin briefing generado (últimos 30 días)
- Invocaciones de `run_recovery.sh` (contando entradas en `data/logs/cron-recovery.log`)
- Ratio briefs generados vs candidatos evaluados

### Output

Fichero markdown: `data/health-reports/YYYY-MM-DD-health.md`

Además, un resumen corto para Telegram:

```
📊 Radar Health Check — 2026-04-10
✅ 6/6 categorías con cobertura 30d
⚠️ enterprise-ai: 0 briefs esta semana
✅ Score medio: 7.4 (estable)
⚠️ Tag 'evaluation' sin uso en 30d
✅ Pipeline: 0 fallos en 30d
```

## Dónde integrarlo

### Opción A — Dentro del digest semanal

Añadir la ejecución de `radar_health_check.py` como paso previo en `run_weekly.sh`. Inyectar el informe como contexto para que el digest semanal lo comente:

```bash
# Antes del digest
python3 "$PROJECT_DIR/scripts/radar_health_check.py" \
    --db "$PROJECT_DIR/data/radar.db" \
    --briefs "$PROJECT_DIR/briefs" \
    --tags "$PROJECT_DIR/config/tags.yaml" \
    --channels "$PROJECT_DIR/config/channels.yaml" \
    --output "$PROJECT_DIR/data/health-reports/$TODAY-health.md"
```

Y en el prompt del digest:

```markdown
Lee también el health check de esta semana en data/health-reports/FECHA-health.md
e incluye las alertas relevantes en la sección de Recomendaciones.
```

### Opción B — Cron independiente (complementario)

Un cron diario ligero que solo calcule las métricas y envíe alertas por Telegram si hay umbrales rotos. Sin generar informe completo — solo alertas:

```
30 8 * * * radar_health_check.py --alerts-only
```

### Recomendación

Implementar **ambas**: el cron diario para alertas rápidas, y el informe completo integrado en el digest semanal para visión de conjunto.

## Relación con radar-lint

`radar-lint` es un skill inferencial (usa Claude para analizar conexiones semánticas, tendencias emergentes y gaps conceptuales). `radar_health_check.py` es **computacional** — solo mira números y estructura. Son complementarios:

| | `radar_health_check.py` | `radar-lint` |
|---|---|---|
| Tipo | Computacional (Python) | Inferencial (Claude) |
| Velocidad | Segundos | Minutos |
| Coste | Cero | Tokens |
| Ejecución | Automática (cron) | Manual (skill) |
| Detecta | Anomalías cuantitativas | Gaps semánticos y conexiones |

## Fuentes de datos

- `data/radar.db` — tabla `videos` con score, categoría, fecha, canal, status
- `briefs/` — frontmatter YAML de cada brief para tags
- `config/tags.yaml` — lista oficial de tags
- `config/channels.yaml` — canales monitorizados
- `data/logs/` — logs de ejecución para tasa de fallos

## Esfuerzo estimado

- Script con métricas básicas (cobertura + scores + tags): ~3h
- Integración con `run_weekly.sh` + alertas Telegram: ~1h
- Cron de alertas diarias: ~1h
- Total: ~5h
