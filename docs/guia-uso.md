# Guía de uso — OPENLAB Radar

Todo lo que puedes hacer con el radar y cómo hacerlo.

---

## El radar en piloto automático

Cada mañana a las **09:00 CET** el sistema hace solo su trabajo:

1. Rastrea los 15 canales de YouTube monitorizados + 18 búsquedas por keywords
2. Evalúa cada vídeo en 4 etapas: triage → transcript → scoring 3D → brief
3. Te manda el **briefing del día** por email con los mejores vídeos ordenados por score
4. Publica los briefs individuales (score ≥ 7) en **Telegraph** y te avisa por Telegram
5. Actualiza el **KB Viewer** en HTML y sincroniza todo con **Google Drive**

Los viernes a las **09:30 CET** hace lo mismo pero en modo digest semanal, y el email va al equipo.

No tienes que hacer nada. Solo leer.

---

## Las 5 interfaces del radar

### 1. Email (uso diario)
El briefing llega a `rafa@openlabstudio.com` cada mañana. Formato HTML con los vídeos del día ordenados por score. Lectura de 3-5 minutos.

### 2. KB Viewer — `kb_viewer.html` en Drive (escaneo visual)
Dashboard autocontenido que se abre con doble clic desde Drive for Desktop. Sin servidor, funciona offline. Vistas:
- **Hot Signals** — top 5 de los últimos 7 días
- **Por categoría** — context-engineering, claude-code-advanced, agentic-systems, enterprise-ai, cli-vs-platforms, delivery-adoption
- **Tag Explorer** — filtra por tags (commercial-argument, skill-pattern, case-study, etc.)
- **Buscador** — búsqueda libre en títulos y resúmenes
- **Insights** — documentos de análisis generados a petición

Ruta en Drive: `OPENLAB/inteligencia/radar/kb_viewer.html`

### 3. Telegram + Telegraph (lectura en móvil)
Cada brief individual se publica en Telegraph (Instant View nativo de Telegram). Recibes el link por el canal privado del radar. Ideal para leer en el móvil sin abrir el ordenador.

### 4. Obsidian (exploración del conocimiento)
El vault de Obsidian está montado sobre la raíz `OPENLAB-RADAR/` en Drive. Útil para:
- **Graph view** — ver conexiones entre briefs por tags y categorías
- **Dataview queries** — filtrar briefs por score, fecha, categoría o tag
- **Backlinks** — ver qué briefs hablan del mismo tema
- Ejemplo de query Dataview: `TABLE score, tags FROM "briefs/context-engineering" SORT score DESC`

### 5. Claude Code — esta sesión (todo lo demás)
Desde aquí puedes hacer todo lo que no es automático: añadir vídeos, consultar briefs, generar insights. Ver secciones siguientes.

---

## Añadir un vídeo manualmente

Flujo recomendado en dos pasos:

### Paso 1 — Check previo (¿vale la pena?)
Di:
> "¿vale la pena añadir este vídeo? [URL]"

El skill conecta al VPS y ejecuta allí el análisis completo: transcript → triage → score estimado → búsqueda de cobertura en los briefs existentes. Te devuelve:
- **AÑADIR / NO AÑADIR / VALORAR** con justificación
- Score estimado y categoría probable
- Si hay solapamiento: qué briefs lo cubren ya y en qué se diferencia este

Si la recomendación es positiva, te pregunta si quieres añadirlo ahora mismo.

### Paso 2 — Añadir al radar
Si saltas el check previo o confirmas desde ahí:
> "añade este vídeo al radar: [URL]"

El pipeline completo: transcript → triage → scoring → brief en `briefs/CATEGORÍA/` → Telegraph → Telegram. No toca el briefing del día ni la DB de candidatos.

---

## Consultar los briefs

Pregunta directamente y Claude busca en `briefs/` para sintetizar:

> "¿Qué dicen los briefs sobre context engineering esta semana?"
> "¿Qué vídeos hablan de delivery de skills a clientes?"
> "¿Hay algún brief con argumento comercial para vender a empresas sin código?"
> "Dame los briefs con tag commercial-argument ordenados por score"
> "¿Qué canales han publicado más contenido sobre agentic systems este mes?"

Claude cita los .md relevantes con el score y la categoría.

---

## Generar un insight

Un insight es un documento de síntesis que pides cuando quieres profundizar en un tema a partir de lo acumulado en el radar.

**Dónde:** desde esta sesión de Claude Code en el laptop, con el proyecto abierto. No hace falta SSH ni estar en el VPS.

**Cómo funciona:** Claude lee los `.md` de `briefs/` directamente (están en el proyecto local, sincronizados desde Drive), sintetiza los relevantes para el tema que pides, y guarda el resultado en `insights/`. No hace falta que le digas la ruta — ya sabe que los insights van ahí.

Di simplemente:
> "Genera un insight sobre por qué los CLI agents superan a n8n para procesos de negocio"
> "Sintetiza todo lo que el radar ha captado sobre context engineering en los últimos 30 días"
> "Genera un insight sobre cómo están entregando skills a clientes las agencias que siguen el radar"

El insight incluye: síntesis de los briefs relevantes, patrones detectados, implicaciones para OPENLAB y argumentos comerciales listos para usar. Se guarda como `insights/FECHA-slug.md` y en el siguiente pipeline se sincroniza con Drive automáticamente.

---

## Cheatsheet de frases de activación

| Qué quieres hacer | Qué decir |
|---|---|
| Check previo de un vídeo | `"¿vale la pena este vídeo? [URL]"` |
| Añadir un vídeo al radar | `"añade este vídeo: [URL]"` |
| Consultar briefs por tema | `"¿qué dicen los briefs sobre [tema]?"` |
| Consultar briefs por tag | `"dame los briefs con tag [tag]"` |
| Generar un insight | `"genera un insight sobre [tema] en insights/"` |
| Ver qué hay en el radar | `"¿cuántos briefs tenemos por categoría?"` |
| Ver los mejores briefs | `"¿cuáles son los briefs con score más alto este mes?"` |

---

## Tags disponibles para búsquedas

**Técnicos:** `context-engineering` · `token-optimization` · `skill-design` · `agent-architecture` · `multi-agent` · `mcp` · `context-window` · `evaluation` · `tool-use` · `knowledge-management` · `long-running-agents` · `harness-engineering`

**Relevancia OPENLAB:** `commercial-argument` · `client-delivery` · `skill-pattern` · `new-service` · `workshop-material` · `competitive-intel`

**Tipo de señal:** `trend` · `technical-deep-dive` · `case-study` · `opinion` · `tutorial`

**Entidades:** `anthropic` · `openai` · `google` · `claude-code` · `langchain` · `cursor` · `n8n`

---

## Estado del sistema

| Componente | Estado |
|---|---|
| Scraper YouTube + cron diario | ✅ Activo |
| Evaluador + briefs individuales | ✅ Activo |
| Telegram + Telegraph | ✅ Activo |
| Email diario a Rafael | ✅ Activo |
| rclone → Google Drive | ✅ Activo |
| KB Viewer HTML | ✅ Activo |
| Skill check previo (`radar-check-video`) | ✅ Activo |
| Skill añadir vídeo remoto (`radar-add-video-remote`) | ✅ Activo |
| Email digest semanal al equipo | ⏳ Pendiente auth gws |
| Obsidian vault completo | ✅ Configurado |
