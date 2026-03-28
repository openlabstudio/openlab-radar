# Pilot Templates - Catálogo de Soluciones

> Templates de pilots organizados por categoría de servicio OPENLAB. Usar como base para diseñar la solución propuesta.
> Fuente: Estrategia Líneas de Servicio v3 (2026-03-02) + implementaciones anteriores

**Última actualización:** 2026-03-09

---

## Cómo Usar Este Catálogo

1. **Identificar categoría** según los pains del cliente
2. **Evaluar complejidad del agente** — si >8K chars → proyecto OPENLAB. Si <8K → no es nuestro mercado.
3. **Seleccionar pilot** que mejor encaje con el quick win
4. **Identificar agentes base del catálogo** que aplican (ver `openlab-sales-context.md`)
5. **Adaptar** nombre y descripción al contexto del cliente
6. **Documentar** funcionalidades específicas para el caso

### Clasificación de Complejidad

| Complejidad | Instrucciones | ¿Es para OPENLAB? |
|---|---|---|
| **Simple** | <8K chars | **NO** — el cliente puede hacerlo con Copilot Studio, Custom GPTs o Gems |
| **Complejo** | >8K chars, multi-fase, web search controlado | **SÍ — ventaja competitiva de OPENLAB** |

### Modo de Ejecución

| Modo | Descripción | Cómo se implementa |
|---|---|---|
| **Interactivo** | El usuario lanza el agente y espera resultado | Cowork o VS Code + Claude Code |
| **Automático (cron)** | El agente corre solo, sin intervención humana | VPS + systemd timers + `claude --print` |
| **Ambos** | Interactivo bajo demanda + briefings automáticos periódicos | VPS (crons) + Cowork/VS Code (interacción) |

---

## Categoría: Knowledge Management

### Pilot: Knowledge Base Assistant

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Información dispersa, difícil de encontrar, conocimiento en silos |
| **Descripción** | Agente que responde preguntas sobre documentación interna, políticas, procedimientos |
| **Funcionalidades típicas** | Búsqueda semántica, citación de fuentes, resumen de documentos |
| **Complejidad** | Simple-Media |
| **Delivery recomendado** | Skills + VPS (línea principal) |
| **Valor típico** | 2-4h/semana ahorradas por usuario en búsquedas |

### Pilot: Onboarding Copilot

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Onboarding lento, inconsistente, carga para el equipo |
| **Descripción** | Agente que guía a nuevos empleados con información relevante |
| **Funcionalidades típicas** | FAQ interactivo, checklists personalizados, escalado a humanos |
| **Complejidad** | Media |
| **Delivery recomendado** | Skills + VPS (línea principal). Agente simple — el cliente puede resolver con herramientas estándar |
| **Valor típico** | 50% reducción tiempo de onboarding |

---

## Categoría: Document Processing

### Pilot: Document Analyzer

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Análisis manual de documentos largos, extracción de información |
| **Descripción** | Agente que extrae información estructurada de documentos |
| **Funcionalidades típicas** | Extracción de datos, comparación de versiones, resumen ejecutivo |
| **Complejidad** | Simple-Media |
| **Delivery recomendado** | Skills + VPS. Para análisis profundo → agente complejo OPENLAB |
| **Valor típico** | 70% reducción tiempo de análisis |

### Pilot: Contract Reviewer

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Revisión manual de contratos, inconsistencia en criterios |
| **Descripción** | Agente que analiza contratos vs. modelo institucional |
| **Funcionalidades típicas** | Detección de desviaciones, clasificación de riesgo, sugerencias |
| **Complejidad** | **Complejo** (>8K chars: reglas de negocio, criterios, templates) |
| **Delivery recomendado** | **Skills + VPS (línea principal)** — requiere prompt completo para fiabilidad |
| **Valor típico** | De 2h a 15min por contrato |

### Pilot: Report Generator

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Informes manuales repetitivos, formato inconsistente |
| **Descripción** | Agente que genera informes estructurados desde datos/inputs |
| **Funcionalidades típicas** | Templates, datos variables, formato profesional |
| **Complejidad** | Simple-Media |
| **Delivery recomendado** | Skills + VPS si requiere automatización; agente simple si no |
| **Valor típico** | 80% reducción tiempo de reporting |

---

## Categoría: Sales & Marketing

### Pilot: Proposal Generator

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Propuestas comerciales manuales, inconsistentes, lentas |
| **Descripción** | Agente que genera propuestas desde inputs del cliente |
| **Funcionalidades típicas** | Análisis de necesidades, mapeo a servicios, pricing |
| **Complejidad** | **Complejo** (contexto comercial extenso, reglas de pricing, templates) |
| **Delivery recomendado** | **Skills + VPS (línea principal)** — requiere todo el contexto comercial |
| **Valor típico** | De 3-4h a 30-60min por propuesta |

### Pilot: Content Assistant

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Creación de contenido lenta, tono inconsistente |
| **Descripción** | Agente que genera contenido alineado con brand guidelines |
| **Funcionalidades típicas** | Posts, emails, descripciones, adaptación de tono |
| **Complejidad** | Simple |
| **Delivery recomendado** | Cualquier plataforma |
| **Valor típico** | 60% reducción tiempo de creación |

### Pilot: Lead Qualifier

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Cualificación manual de leads, criterios inconsistentes |
| **Descripción** | Agente que evalúa y puntúa leads según criterios definidos |
| **Funcionalidades típicas** | Scoring, categorización, next best action |
| **Complejidad** | Media-Complejo (depende de la cantidad de criterios) |
| **Delivery recomendado** | Skills + VPS (línea principal), con integración CRM via MCP si necesario |
| **Valor típico** | 40% mejora en conversión |

---

## Categoría: Research & Analysis

### Pilot: Market Research Assistant

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Investigación de mercado manual, sesgada, lenta |
| **Descripción** | Agente que investiga mercados, competidores, tendencias |
| **Funcionalidades típicas** | Web search, análisis de fuentes, síntesis, validación |
| **Complejidad** | **Complejo** (multi-fase, web search controlado, red flags, templates) |
| **Delivery recomendado** | **Skills + VPS (línea principal)** — ejemplo paradigmático de agente complejo OPENLAB (~50K chars) |
| **Valor típico** | De días a horas por análisis |

### Pilot: Trend Scouting Observatory (Headless)

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Scouting de tendencias manual, lento, sesgado; el equipo no tiene tiempo de investigar proactivamente |
| **Descripción** | Agente headless que corre automáticamente (cron semanal/mensual), investiga tendencias en fuentes abiertas, y entrega informe priorizado sin intervención humana |
| **Funcionalidades típicas** | Web search multi-fuente, análisis de relevancia vs. criterios del cliente, scoring/priorización, generación de informe estructurado, output a Google Drive/Sheets/email |
| **Modo de ejecución** | **Headless/Scheduled** — cron job, sin interacción humana por ejecución |
| **Complejidad** | **Complejo** (>8K chars: multi-fase, web search extenso 10-20 min, lógica de scoring, templates detallados) |
| **Delivery recomendado** | **Skills + VPS con cron (línea principal, modo automático)** — requiere ejecución autónoma sin límite de tiempo |
| **Valor típico** | De 0 informes proactivos a 1 informe automatizado por ciclo; equipo recibe insights priorizados sin dedicar tiempo a investigar |
| **Ejemplo real** | Caso Iberostar: Observatorio de tendencias IA para innovación hotelera. Corre semanalmente en Azure, investiga nuevas tecnologías, valora relevancia para hoteles, entrega informe a Google Drive + notificación por email. |

### Pilot: Proposal/Partner Scoring Agent

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Evaluación manual de propuestas/partners con criterios inconsistentes, sesgo, y tiempo excesivo |
| **Descripción** | Agente que evalúa propuestas/candidaturas contra criterios institucionales detallados |
| **Funcionalidades típicas** | Análisis de documentos, scoring multi-criterio, detección de red flags, clasificación de riesgo, informe estructurado |
| **Modo de ejecución** | **Interactivo o Batch** — puede correr on-demand o procesar lotes |
| **Complejidad** | **Complejo** (>8K chars: criterios detallados, pesos, lógica condicional, templates de output) |
| **Delivery recomendado** | **Skills + VPS (línea principal)** — la adherencia a instrucciones largas es crítica para scoring fiable |
| **Valor típico** | De 2-4h a 15-30 min por evaluación; criterios 100% consistentes |

### Pilot: Due Diligence Copilot

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Due diligence manual, inconsistente, lenta |
| **Descripción** | Agente que analiza empresas/proyectos según criterios de inversión |
| **Funcionalidades típicas** | Análisis financiero, competitivo, regulatorio, riesgos, red flags |
| **Complejidad** | **Complejo** (7 fases, 17 red flags, metodología detallada, auto-evaluación) |
| **Delivery recomendado** | **Skills + VPS (línea principal)** — calidad <90% es inaceptable para decisiones de inversión |
| **Valor típico** | 50% reducción tiempo de análisis |

---

## Categoría: Operations

### Pilot: Process Automation Assistant

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Procesos manuales repetitivos, errores humanos |
| **Descripción** | Agente que automatiza pasos de procesos operativos |
| **Funcionalidades típicas** | Validación de datos, routing, notificaciones |
| **Complejidad** | Media-Alta |
| **Delivery recomendado** | Skills + VPS (línea principal), con integraciones MCP según sistema del cliente |
| **Valor típico** | 70% reducción tareas manuales |

### Pilot: Customer Support Copilot

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Soporte lento, respuestas inconsistentes |
| **Descripción** | Agente que asiste en respuestas a clientes |
| **Funcionalidades típicas** | FAQ, escalado, drafts de respuesta |
| **Complejidad** | Media |
| **Delivery recomendado** | Skills + VPS (línea principal). Agente simple — el cliente puede resolver con herramientas estándar |
| **Valor típico** | 40% reducción tiempo de respuesta |

### Pilot: Call Intelligence / Conversation Analyzer

| Elemento | Detalle |
|----------|---------|
| **Pain que resuelve** | Transcripciones de llamadas que nadie lee, insights perdidos |
| **Descripción** | Agente que analiza transcripciones y extrae insights accionables |
| **Funcionalidades típicas** | Extracción de action items, sentiment analysis, categorización de temas, tendencias |
| **Complejidad** | **Complejo** (múltiples dimensiones de análisis, templates detallados) |
| **Delivery recomendado** | **Skills + VPS con cron (línea principal)** — ideal para procesamiento recurrente automatizado |
| **Valor típico** | 100% de calls analizadas (vs ~10% manual), insights en minutos |

---

## Notas

- Los valores típicos son estimaciones basadas en implementaciones anteriores
- La complejidad puede variar según integraciones requeridas
- **Para agentes complejos (>8K chars): siempre validar que la vía de delivery preserva >90% de calidad**
- Siempre validar viabilidad técnica con la plataforma elegida

---

**Versión:** 3.0
**Mantenimiento:** Añadir nuevos pilots según se implementen. Actualizar delivery recomendado si cambian las capacidades de las plataformas.
