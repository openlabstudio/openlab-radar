# Harness Gap: Fitness functions arquitectónicas

**Estado: IMPLEMENTADO** (2026-05-18)

---

## Qué se implementó

Script `scripts/radar_health_check.py` — métricas computacionales de salud del sistema (sin usar Claude, coste cero, ejecución en segundos).

### Métricas implementadas

1. **Cobertura por categoría** (7d, período configurable, total) con alertas si una categoría tiene 0 briefs en 7d o concentra >50% del período.
2. **Distribución de scores** con detección de inflación (+0.5 vs período anterior) y falta de discriminación (>80% en rango 7-8).
3. **Salud de tags** — tags oficiales sin uso, tags no oficiales encontrados en briefs, top 15 tags, tags menos usados del histórico.
4. **Rendimiento de canales** — cruce de scrapes (DB) con briefs reales (frontmatter), ratio por canal, alertas de alto ruido, canales monitorizados sin actividad.
5. **Tasa de fallos del pipeline** — días sin ejecución, invocaciones de recovery.

### Integración

Se implementaron **ambas opciones** recomendadas en el diseño original:

- **Opción A — Dentro del digest semanal:** Paso 0 en `run_weekly.sh`. Genera informe en `data/health-reports/YYYY-MM-DD-health.md` y lo inyecta como contexto al digest para que Claude comente las alertas en Recomendaciones.
- **Opción B — Cron diario:** `30 8 * * *` con `--alerts-only`, envía alertas por Telegram solo si hay umbrales rotos.

### Capacidad adicional: análisis retroactivo

Se añadió `--period N` (0 = histórico completo) para ejecutar el health check sobre todo el histórico de briefs. El primer análisis retroactivo (2026-05-18) produjo acciones concretas:

- **Tag `enterprise-ai`** añadido a `tags.yaml` (aparecía en 15 briefs sin ser oficial).
- **Canales con alto ruido bajados a `priority: low`:** David Ondrej (21 scrapes, 0 briefs), Fireship (14/0), Matt Wolfe (13/0). El scraper ahora salta canales `low`.
- **98% de briefs en rango 7-8** → recalibración de la rúbrica de scoring con rangos granulares por punto y distribución esperada explícita.
- **Recalibración con propuestas ganadoras** (MAPFRE, BTSA, DAMM Fin, DAMM Innov, Areas) → señales de scoring reorganizadas por impacto en proyectos reales, 7 tags nuevos, 4 keywords enterprise ancladas al ecosistema Claude/Anthropic.

## Ficheros

- `scripts/radar_health_check.py` — script principal
- `scripts/run_weekly.sh` — integrado como Paso 0
- `data/health-reports/` — informes generados
- `data/logs/cron-health.log` — log del cron diario

## Relación con radar-lint

Sin cambios respecto al diseño original. Son complementarios:

| | `radar_health_check.py` | `radar-lint` |
|---|---|---|
| Tipo | Computacional (Python) | Inferencial (Claude) |
| Velocidad | Segundos | Minutos |
| Coste | Cero | Tokens |
| Ejecución | Automática (cron) | Manual (skill) |
| Detecta | Anomalías cuantitativas | Gaps semánticos y conexiones |
