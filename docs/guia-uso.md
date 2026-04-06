# Guía de uso — OPENLAB Radar

Todo lo que puedes hacer con el radar y cómo hacerlo.

---

## El radar en piloto automático

Cada mañana a las **09:00 CET** el sistema hace solo su trabajo:

1. Rastrea los 15 canales de YouTube monitorizados + 18 búsquedas por keywords
2. Evalúa cada vídeo en 4 etapas: triage → transcript → scoring 3D → brief
3. Te manda el **briefing del día** por email con los mejores vídeos ordenados por score
4. Actualiza el **KB Viewer** en HTML y sincroniza todo con **Google Drive**

Los viernes a las **09:30 CET** hace lo mismo pero en modo digest semanal, y el email va al equipo.

No tienes que hacer nada. Solo leer.

---

## Las 3 interfaces del radar

### 1. Email (uso diario)
El briefing llega cada mañana. Formato HTML con los vídeos del día ordenados por score. Lectura de 3-5 minutos.

Los viernes llega el digest semanal con el resumen de toda la semana.

### 2. KB Viewer — web + Drive (escaneo visual)
Dashboard interactivo con todos los briefs del radar. Tres formas de acceder:

- **Web (compartible):** [`openlabstudio.com/radar/`](https://www.openlabstudio.com/radar/) — embebido en la web de OPENLAB con header/footer del site. URL directa para compartir con quien quieras. Se actualiza automáticamente cada día.
- **Web (directa):** [`radar.openlabstudio.com`](https://radar.openlabstudio.com) — el dashboard sin embeber, a pantalla completa. Mismo contenido que la versión embebida.
- **Drive (offline):** doble clic en `kb_viewer.html` desde Drive for Desktop. Mismo contenido, funciona sin conexión.

Vistas:
- **Hot Signals** — top briefs de los últimos 7 días (score ≥ 8.0)
- **Por categoría** — context-engineering, claude-code-advanced, agentic-systems, enterprise-ai, cli-vs-platforms, delivery-adoption
- **Tag Explorer** — filtra por tags (commercial-argument, skill-pattern, case-study, etc.)
- **Buscador** — búsqueda libre en títulos y resúmenes

Stats: total briefs, score medio, briefs esta semana, canales monitorizados.

Cada card tiene links a **YouTube** (vídeo original) y **VER RESUMEN** (Telegraph, lectura rápida).

Ruta en Drive: `OPENLAB-RADAR/kb_viewer.html`

### 3. Claude Code (todo lo demás)
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

**Dónde:** desde tu laptop, en cualquier sesión de Claude Code. Los briefs ya están en el Shared Drive, así que Claude los lee directamente y guarda el insight en `insights/`. Como el Drive es compartido, el insight está disponible para todo el equipo inmediatamente.

Di simplemente:
> "Genera un insight sobre por qué los CLI agents superan a n8n para procesos de negocio"
> "Sintetiza todo lo que el radar ha captado sobre context engineering en los últimos 30 días"
> "Genera un insight sobre cómo están entregando skills a clientes las agencias que siguen el radar"

El insight incluye: síntesis de los briefs relevantes, patrones detectados, implicaciones para OPENLAB y argumentos comerciales listos para usar. Se guarda como `insights/FECHA-slug.md`.

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
| Email diario | ✅ Activo |
| rclone → Google Drive | ✅ Activo |
| KB Viewer HTML (Drive) | ✅ Activo |
| KB Viewer Web (`openlabstudio.com/radar/` + `radar.openlabstudio.com`) | ✅ Activo |
| Skill check previo (`radar-check-video`) | ✅ Activo |
| Skill añadir vídeo remoto (`radar-add-video-remote`) | ✅ Activo |
| Email digest semanal al equipo | ⏳ Pendiente auth gws |
