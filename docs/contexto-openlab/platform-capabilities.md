# Platform Capabilities - Knowledge Base

> Capacidades técnicas y limitaciones de las plataformas relevantes.
> Referencia para validación técnica en assessments.

**Última actualización:** 2026-03-17

---

## Arquitectura de Delivery de OPENLAB

OPENLAB usa una única arquitectura: **Skills + VPS + Claude Code CLI**.

```
Lo que pone OPENLAB:
  └── Ficheros .md en un repo git (instrucciones en lenguaje natural)

Lo que pone el cliente:
  ├── VPS o entorno de ejecución (su Azure/AWS/on-prem)
  ├── Cuenta del runtime (Claude Max/Team/Enterprise)
  └── Entrega hacia sus sistemas (Teams webhook, email, SharePoint)
```

**Calidad:** 95-100% — los skills se ejecutan exactamente como fueron diseñados.

**Portabilidad:** Los skills siguen el estándar Agent Skills (35+ plataformas). Se mueven entre runtimes con `git clone`:
- Claude Code (gold standard)
- Codex CLI / OpenAI (paridad funcional)
- GitHub Copilot (multi-agente completo)
- Gemini CLI (experimental)

---

## Capacidades del Runtime (Claude Code CLI)

| Capacidad | Estado | Notas |
|-----------|--------|-------|
| System prompt sin límite de longitud | ✅ | 1M tokens de contexto |
| Ejecución autónoma multi-fase | ✅ | 7+ fases sin intervención del usuario |
| Sub-agentes paralelos | ✅ | Hasta 10, con contexto aislado |
| Web search y web fetch nativos | ✅ | Invocados explícitamente por fase |
| Generación de ficheros | ✅ | Outputs en .md, automáticos, auditables |
| MCP (Model Context Protocol) | ✅ | 10.000+ servers públicos. Oficiales de Google (GWS CLI), Microsoft (M365), Salesforce, HubSpot, SAP, Jira, Linear, Asana, Slack, PostgreSQL. El agente interactúa directamente con los sistemas del cliente. |
| Progressive disclosure | ✅ | Carga dinámica de contexto según necesidad |
| Ejecución headless (crons) | ✅ | Via `claude --print` en systemd timers |
| Memoria persistente | ✅ | Entre sesiones |
| Git integration | ✅ | Nativo |
| Bash/Python execution | ✅ | Cualquier script — procesamiento de datos, integraciones API, scraping, generación de gráficos, conversión de formatos |

---

## Interfaces para Usuarios

| Interfaz | Para quién | Capacidades | Coste/usuario |
|----------|-----------|-------------|---------------|
| **Claude Cowork + plugins** | Usuarios de negocio | Chat limpio, plugins custom, archivos locales | $25-90/mes |
| **VS Code + extensión Claude Code** | Usuarios tech-savvy | IDE completo, terminal, explorador de archivos | $100/mes |
| **Solo VPS (crons)** | Consumidores pasivos | Reciben outputs en Teams/email sin interactuar | $0 (solo VPS) |

---

## Entrega de Outputs

| Canal | Cómo | Complejidad |
|-------|------|-------------|
| **Teams (webhook)** | Incoming webhook — POST con el briefing. No requiere bot, ni Entra ID, ni permisos admin. | Mínima |
| **Email (SMTP)** | sendmail o relay desde el VPS | Mínima |
| **SharePoint (Graph API)** | Script Python con Microsoft Graph. Requiere App Registration mínimo (Files.ReadWrite) | Baja |
| **Google Drive** | Service account + Google Drive API | Baja |
| **Archivos locales** | Outputs en `~/workspace/[proyecto]/outputs/` | Zero |

---

## Por Qué NO Usamos Otras Plataformas

OPENLAB evaluó y descartó estas alternativas. La información se mantiene como referencia para cuando un cliente pregunte.

### Copilot Studio / Custom GPTs — Descartado
- **Límite:** 8.000 caracteres de instrucciones
- **Impacto:** Los agentes complejos de OPENLAB (~50.000 chars) no caben. Calidad baja a 65-80%.
- **Claude dentro de Copilot Studio:** El límite de 8K es de Microsoft, no del modelo. Mismo Claude, 15% de instrucciones.
- **Conclusión:** Para agentes simples (<8K) está bien. No es mercado OPENLAB.

### Gemini Gems nativo — Descartado
- **Sin límite de chars** (comparte ventana de contexto, 1M-2M tokens)
- **Pero:** Adherencia a instrucciones se degrada con prompts largos. No hay ejecución autónoma multi-fase. Workflow hay que rediseñarlo a multi-turno.
- **Calidad real:** ~80-85% con adaptación, ~70-80% raw
- **Esfuerzo de adaptación:** 10-18h por agente complejo
- **Conclusión:** Calidad insuficiente para el estándar OPENLAB. Sin diferenciación (cualquiera configura un Gem).

### Bot Teams + Claude API (Foundry) — Descartado
- **Técnicamente viable** y de buena calidad (90-95%)
- **Pero:** Requiere que OPENLAB desarrolle y mantenga software en producción (bot, backend, infra). 40-60h de template + 20-30h por cliente.
- **Riesgo:** Obsolescencia a 6-12 meses si Microsoft sube el límite de 8K o Claude se integra nativamente en Teams.
- **Conclusión:** OPENLAB no es una software factory. Construir el bot es competir donde no tenemos ventaja.

### Apps Script + Claude API — Descartado para agentes complejos
- **Límite de ejecución:** 6 min (30 min Enterprise). Insuficiente para agentes con web search extenso (10-20 min).
- **Conclusión:** Solo viable para agentes interactivos cortos. No para el tipo de agente que diferencia a OPENLAB.

---

## Compliance y Seguridad

| Aspecto | Claude Code / API | Foundry (Azure) |
|---------|-------------------|-----------------|
| Residencia datos | EE.UU. | Azure West Europe (disponible) |
| Entrenamiento con datos | NO (contractual) | NO |
| SOC 2 / ISO 27001 | ✅ | ✅ |
| GDPR | Compromiso contractual | Azure compliance |

**Para procesos de innovación (datos públicos):** Sin problema con API directa.
**Para datos sensibles/regulados:** Evaluar Azure AI Foundry o AWS Bedrock para residencia EU. Trade-off de rendimiento vs. compliance.

---

## Notas de Actualización

Las capacidades de las plataformas evolucionan rápido. Para validación técnica en un assessment, siempre ejecutar web search:

```
Claude Code capabilities 2026
[Funcionalidad específica] Claude Code
Anthropic enterprise features
```

---

**Versión:** 4.0
**Fuente:** `openlab-offering-agentes-ia.md` v5.0, `decision-arquitectura-servicios-openlab.md`
