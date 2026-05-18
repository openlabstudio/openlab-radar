# Cambio de facturación `claude -p` — 15 junio 2026

> Opciones y recomendaciones para adaptar OPENLAB Radar al nuevo modelo de billing.
> Aplica también a cualquier despliegue cliente basado en la arquitectura Radar (ej. MAPFRE Observatorio).

**Fecha:** 2026-05-18
**Estado:** Pendiente de acción (deadline: 13 junio 2026)
**Fuente:** [Anthropic Help Center](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)

---

## Qué cambia

A partir del 15 de junio, Anthropic separa la facturación de suscripciones Claude en dos pools:

| Pool | Uso | Billing |
|------|-----|---------|
| **Interactivo** | Claude Code en terminal/IDE, Cowork, claude.ai | Límites de suscripción (sin cambios) |
| **Programático (Agent SDK)** | `claude -p`, Agent SDK, GitHub Actions, apps de terceros | Crédito mensual a **precios de API** |

**Crédito Agent SDK incluido por plan:**

| Plan | Crédito/mes |
|------|------------|
| Pro ($20/mo) | $20 |
| Max 5x ($100/mo) | $100 |
| Max 20x ($200/mo) | $200 |
| Team Standard ($25/seat) | $20/seat |
| Team Premium ($100/seat) | $100/seat |

- El crédito **no se acumula** de un mes a otro
- Si se agota y "extra usage" está activado → se factura a precios de API sin límite
- Si "extra usage" está desactivado → las peticiones `claude -p` **se paran** hasta el siguiente ciclo
- Anthropic envía email el **8 de junio** para activar el crédito. Se activa el **15 de junio**

**Precios de API relevantes:**

| Modelo | Input | Output | Cache hits |
|--------|-------|--------|------------|
| Sonnet 4.6 | $3/MTok | $15/MTok | $0.30/MTok |
| Opus 4.6/4.7 | $5/MTok | $25/MTok | $0.50/MTok |
| Haiku 4.5 | $1/MTok | $5/MTok | $0.10/MTok |
| Batch API | 50% de lo anterior | 50% | 50% |

---

## Impacto en OPENLAB Radar

El Radar usa `claude -p` en `run_daily.sh`, `run_weekly.sh` y `run_recovery.sh`. **Todo ese uso pasa al pool de Agent SDK credit.**

### Estimación de consumo mensual (Sonnet 4.6)

| Pipeline | Frecuencia | Input tokens | Output tokens | Coste/mes |
|----------|-----------|-------------|---------------|-----------|
| Evaluación diaria (triage + transcript + scoring + briefing) | 30 runs | ~105K/run | ~8K/run | ~$13 |
| Digest semanal | 4 runs | ~80K/run | ~10K/run | ~$2 |
| Recovery + health checks | ~10 runs | ~20K/run | ~3K/run | ~$1 |
| **Total OPENLAB Radar** | | | | **~$16/mes** |

Con Opus: ~$28/mes. Con Haiku (solo triage): ~$5/mes.

**Veredicto:** Con Max 5x ($100/mes de crédito), el Radar cabe holgadamente. Sobran ~$84/mes.

---

## Opciones

### Opción 1: Mantener `claude -p` con crédito Agent SDK

**Recomendada a corto plazo. Menor esfuerzo.**

- No cambiar nada en el código. Solo activar el crédito el 8 de junio
- El consumo del Radar (~$16/mes) cabe en el crédito de $100/mes
- Activar "extra usage" con hard cap (e.g., $30/mes) como safety net
- Añadir `--output-format json` a los scripts para trackear `total_cost_usd` por ejecución

**Pros:**
- Zero cambios en el pipeline
- Incluido en la suscripción Max que ya se paga

**Contras:**
- Si OPENLAB añade más pipelines automatizados (otros clientes, otros crons), el crédito se comparte
- Sin visibilidad por proyecto en Anthropic Console (todo va contra la misma cuenta)

**Para despliegues en clientes:** Si el cliente paga sus propias licencias Max, tiene su propio crédito de $100/mes dedicado. Sin conflicto con OPENLAB.

---

### Opción 2: Migrar crons a `ANTHROPIC_API_KEY`

**Recomendada a medio plazo. Mayor control.**

- Usar API key en lugar de OAuth token para los crons del VPS
- Cambiar en `config/.env`: sustituir `CLAUDE_CODE_OAUTH_TOKEN` por `ANTHROPIC_API_KEY`
- Coste: pay-per-token, ~$16-28/mes por Radar (según modelo)

**Pros:**
- Facturación separada por proyecto en Anthropic Console
- Hard caps y alertas a nivel de API key
- El crédito Agent SDK de la suscripción queda libre para otros usos
- Escala sin conflicto: cada cliente/proyecto puede tener su propia API key

**Contras:**
- Coste adicional (~$16/mes) que antes era $0
- Requiere gestionar API key (rotación, seguridad)

**Nota:** La advertencia actual en `arquitectura-tecnica.md` — *"⚠️ No usar ANTHROPIC_API_KEY en crons"* — era correcta cuando `claude -p` con OAuth era gratis. Después del 15 de junio, `claude -p` factura por token de todas formas (contra el crédito Agent SDK). La diferencia es solo si sale del crédito mensual o de la API key. Actualizar la documentación.

---

### Opción 3: Forzar Sonnet en crons, reservar Opus para interactivo

**Combinable con Opción 1 o 2. Ahorro inmediato.**

- Añadir `--model sonnet` a `run_daily.sh`, `run_weekly.sh` y `run_recovery.sh`
- Ahorro: ~40% respecto a Opus
- Trade-off: calidad de evaluación ligeramente menor, pero Sonnet es suficiente para triage y scoring
- Opus se reserva para uso interactivo de OPENLAB (skills, análisis complejos)

**Implementación:**
```bash
# En run_daily.sh, cambiar:
claude -p "..." --allowedTools "..." --output-format text
# Por:
claude -p "..." --allowedTools "..." --output-format text --model sonnet
```

---

### Opción 4: Pipeline en 2 pasos (Haiku triage + Sonnet/Opus briefs)

**Mayor ahorro. Requiere refactoring.**

- Paso 1: Haiku hace el triage rápido (título + descripción → SÍ/QUIZÁ/NO)
- Paso 2: Sonnet o Opus solo evalúa los que pasan (con transcript)
- Ahorro: ~60-70% en la fase de triage (Haiku $1/$5 vs Sonnet $3/$15)

**Trade-off:**
- Requiere dividir `evaluate-daily.md` en dos prompts y dos invocaciones de `claude -p`
- Haiku no tiene acceso a MCP (transcript) → solo triage por metadatos
- Mayor complejidad en `run_daily.sh`

**Estimación con pipeline mixto:**

| Paso | Modelo | Candidatos | Coste/mes |
|------|--------|-----------|-----------|
| Triage (30 runs × 20 candidatos) | Haiku 4.5 | Todos | ~$2 |
| Evaluación + briefs (30 runs × 5-8 candidatos) | Sonnet 4.6 | Solo los que pasan | ~$8 |
| **Total** | | | **~$10/mes** |

---

### Opción 5: Batch API para procesamiento diferido

**Mayor ahorro posible. Mayor complejidad.**

- Usar la Batch API de Anthropic (50% descuento en todos los tokens)
- Sonnet batch: $1.50/MTok input, $7.50/MTok output

**Problemas:**
- Requiere reescribir el pipeline para usar la API de Anthropic directamente (no `claude -p`)
- Pierde las herramientas nativas de Claude Code (Read, Write, Glob, MCP)
- El evaluador necesita MCP para transcripts → no compatible con Batch API directa
- Latencia: la Batch API no es en tiempo real

**Veredicto:** No recomendable. El ahorro (~$8/mes vs ~$16/mes) no justifica la pérdida de funcionalidad y la complejidad de migración.

---

### Opción 6: Routines en lugar de crons

**$0 adicional. Pero limitaciones críticas.**

- Routines usan el pool interactivo (no el programático) → no consumen crédito Agent SDK
- Incluidas en Max (15 runs/día)

**Problemas:**
- Routines solo acceden a repos git. No pueden:
  - Ejecutar scripts Python arbitrarios (scraper.py)
  - Gestionar SQLite (radar.db)
  - Usar MCP servers propios (mcp_transcript_server.py)
  - Ejecutar rclone sync
  - Enviar notificaciones Telegram/Teams/email
- El Radar necesita todo eso

**Veredicto:** No viable para el Radar tal como está diseñado. Viable solo si se rediseña el pipeline para que todo viva en un repo git y Claude genere outputs sin scripts auxiliares (pérdida significativa de funcionalidad).

---

## Recomendación

### Plan de acción inmediato (antes del 13 de junio)

| # | Acción | Quién | Deadline |
|---|--------|-------|----------|
| 1 | Activar crédito Agent SDK cuando llegue el email de Anthropic | OPENLAB (Rafa) | 8-13 junio |
| 2 | Activar "extra usage" con hard cap de $30/mes | OPENLAB (Rafa) | 13 junio |
| 3 | Forzar `--model sonnet` en `run_daily.sh`, `run_weekly.sh`, `run_recovery.sh` | OPENLAB (Rafa) | 13 junio |
| 4 | Añadir `--output-format json` y log de `total_cost_usd` por ejecución | OPENLAB (Rafa) | 13 junio |
| 5 | Actualizar `docs/arquitectura-tecnica.md`: eliminar advertencia sobre ANTHROPIC_API_KEY y documentar nuevo billing | OPENLAB (Rafa) | 13 junio |

### Monitorización (junio-julio)

- Revisar consumo real después de 2-3 semanas con el nuevo billing
- Si consumo < 50% del crédito → mantener Opción 1
- Si consumo > 70% del crédito → evaluar migración a API key (Opción 2)
- Si se añaden más clientes con pipelines en la misma cuenta → migrar a API key por proyecto

### Medio plazo (para despliegues en clientes)

- Cada cliente paga sus propias licencias Max → tiene su propio crédito Agent SDK ($100/mes)
- Si el cliente prefiere control granular → usar API key dedicada por proyecto
- Documentar el coste de crons (~$16/mes con Sonnet) como línea de infraestructura en las propuestas

---

## Modelos que se retiran el 15 de junio

Verificar que el Radar no usa estos model IDs (hardcoded o en prompts):

| Model ID retirado | Reemplazo |
|-------------------|-----------|
| `claude-sonnet-4-20250514` | `claude-sonnet-4-6-20260217` |
| `claude-opus-4-20250514` | `claude-opus-4-7` |

Comando de auditoría:
```bash
grep -r "claude-sonnet-4-20250514\|claude-opus-4-20250514\|@anthropic-ai/claude-code\|claude-code-sdk" /home/openlab/openlab-radar/
```

Si el Radar no especifica model ID (usa el default de la suscripción), no hay impacto.

---

## Fuentes

- [Use the Claude Agent SDK with your Claude plan — Help Center](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)
- [Run Claude Code programmatically — Claude Code Docs](https://code.claude.com/docs/en/headless)
- [Claude Code Billing Change June 15, 2026 — Build This Now](https://www.buildthisnow.com/blog/guide/mechanics/claude-billing-change-june-2026)
- [Anthropic API Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [What Anthropic's New Claude Billing Means for Zed Users](https://zed.dev/blog/anthropic-subscription-changes)
- [Anthropic puts Claude agents on a meter — InfoWorld](https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html)
- [Claude subscriptions get separate budgets — The Decoder](https://the-decoder.com/claude-subscriptions-get-separate-budgets-for-programmatic-use-billed-at-full-api-prices/)
- [Claude Code API Key vs Subscription — LaoZhang AI](https://blog.laozhang.ai/en/posts/claude-code-api-key-vs-subscription-billing)
