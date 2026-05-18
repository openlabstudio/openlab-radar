# QMD centralizado para despliegues de Observatorio en clientes

> Arquitectura de búsqueda semántica (RAG local) para observatorios con múltiples usuarios.
> Basado en la implementación de QMD en OPENLAB Radar (mayo 2026).

**Estado:** Diseñado, no implementado. Listo para el primer despliegue cliente.
**Fecha:** 2026-05-18

---

## Problema

Cuando desplegamos un Observatorio (arquitectura Radar) en un cliente, el equipo del cliente tiene N usuarios de Claude Code que necesitan consultar los briefs. Sin búsqueda semántica, cada consulta obliga a Claude a leer decenas o cientos de ficheros .md — lento, costoso en contexto, y no descubre relaciones semánticas entre briefs.

La alternativa de instalar QMD en cada laptop del cliente es viable pero añade fricción: setup por persona, sincronización vía Drive, modelos de ~2GB por máquina.

---

## Solución: QMD daemon centralizado en el VPS

Un único QMD corriendo en el VPS del cliente como daemon HTTP. Los usuarios se conectan vía MCP remoto sin instalar nada local.

### Arquitectura

```
┌──────────────────────────────────────────────────┐
│  N usuarios (Claude Code en laptop)               │
│                                                    │
│  MCP registrado: qmd-radar → HTTP VPS:8181        │
│  CLAUDE.md en carpeta briefs → instruye usar QMD  │
└──────────┬─────────────────────────────────────────┘
           │ HTTP
           ▼
┌──────────────────────────────────────────────────┐
│  VPS del cliente                                  │
│                                                    │
│  QMD daemon (:8181)                               │
│  ├── Colección: briefs/ (fuente de verdad)        │
│  ├── BM25 + embeddings + LLM re-ranking           │
│  ├── Auto-update post-pipeline                     │
│  └── ~14MB índice / ~250 docs                     │
│                                                    │
│  Pipeline Observatorio (crons)                     │
│  └── scraper → evaluador → briefs/ → QMD re-index │
│                                                    │
│  (Opcional) nginx reverse proxy + SSL              │
│  (Futuro) Frontend web sobre el mismo daemon       │
└──────────────────────────────────────────────────┘
```

### Flujo de usuario

```
1. Usuario abre Claude Code en la carpeta de briefs (vía Drive)
2. Claude lee CLAUDE.md → sabe que tiene QMD disponible
3. Usuario: "¿qué hemos capturado sobre regulación de IA en banca?"
4. Claude → mcp__qmd__query → HTTP → QMD daemon en VPS
5. QMD devuelve 5 briefs relevantes con score y snippets
6. Claude lee los 2-3 mejores con Read
7. Claude sintetiza y responde con citas
```

El usuario no necesita saber que hay un QMD, un VPS o un índice semántico. Solo pregunta.

---

## Setup

### 1. VPS (una vez, por OPENLAB durante el despliegue)

```bash
# Instalar QMD
npm install -g @tobilu/qmd

# Crear colección (briefs ya están en el VPS)
qmd collection add /ruta/proyecto/briefs --name radar --pattern "**/*.md"
qmd context add qmd://radar/ "Observatorio de inteligencia: briefs con análisis de contenido del dominio del cliente. Frontmatter YAML con score, categoría, tags y score_breakdown."
qmd embed

# Lanzar daemon HTTP persistente
qmd mcp --http --daemon --port 8181

# (Recomendado) Servir detrás de nginx con SSL
# /etc/nginx/sites-available/qmd-radar:
#   location /qmd/ {
#       proxy_pass http://127.0.0.1:8181/;
#   }
```

### 2. Auto-update (añadir al pipeline)

Al final de `run_daily.sh` y `run_weekly.sh`:
```bash
qmd update -q && qmd embed
```

Los briefs nuevos se re-indexan automáticamente tras cada ejecución del pipeline (~2-5s para unos pocos docs nuevos).

### 3. Setup por usuario del cliente (una vez)

```bash
# Registrar MCP server remoto en Claude Code
claude mcp add qmd-radar -s user -- npx -y @anthropic-ai/mcp-proxy http://VPS_IP:8181
```

Un solo comando. No requiere Node.js ni modelos locales — `npx` descarga el proxy MCP on-the-fly.

### 4. CLAUDE.md en la carpeta de briefs

Fichero que va en la raíz de la carpeta de briefs (sincronizada con Drive). Instruye a Claude Code a usar QMD como primera opción de búsqueda:

```markdown
# Observatorio [Cliente] — Knowledge Base

Base de conocimiento con N+ briefs de inteligencia sobre [dominio del cliente].

## Cómo buscar

Usa QMD (búsqueda semántica) como primera opción. Devuelve los briefs más
relevantes por significado sin necesidad de keywords exactos:

mcp__qmd__query(
  searches=[{type:'vec', query:'tu pregunta en lenguaje natural'}],
  collection='radar',
  intent='describe brevemente qué buscas'
)

Después lee los briefs devueltos con Read para profundizar.

Para filtros precisos (score > 8, categoría, fecha, tags), usa:
python3 scripts/radar_search.py --score-min 8 --category X --sort score

## Estructura de los briefs

Cada brief tiene frontmatter YAML con: title, date, category, score,
score_breakdown (aplicabilidad/novedad/calidad), tags, source, url.

## Categorías

- [listar categorías del cliente]
```

---

## Requisitos del VPS

- Node.js 18+ (para QMD)
- ~2GB disco adicional (modelos GGUF, se descargan la primera vez)
- ~200MB RAM adicional (daemon QMD en reposo)
- Puerto 8181 accesible (o nginx reverse proxy)

---

## Evolución: frontend web

El daemon HTTP de QMD expone los mismos endpoints que el MCP server. Se puede construir un frontend web para personas que no usan Claude Code (dirección, stakeholders):

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Claude Code │     │  Frontend    │     │  QMD daemon  │
│  (técnicos)  │────►│  web         │────►│  VPS :8181   │
│              │     │  (búsqueda)  │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                     radar.cliente.com
```

El frontend sería un buscador simple: caja de texto, resultados con score y snippet, click para leer el brief completo. Implementable en vanilla JS o cualquier framework ligero.

---

## Costes adicionales por despliegue

| Concepto | Coste |
|----------|-------|
| Node.js en VPS | $0 (ya instalado o trivial) |
| Disco (modelos QMD) | ~2GB (one-time) |
| RAM daemon QMD | ~200MB |
| Mantenimiento | $0 (auto-update vía hook post-pipeline) |
| Frontend web (si se implementa) | Desarrollo one-time |

---

## Checklist de despliegue

```
□ Node.js 18+ instalado en VPS del cliente
□ QMD instalado (npm install -g @tobilu/qmd)
□ Colección creada apuntando a briefs/
□ Contexto añadido a la colección
□ Embeddings generados (qmd embed)
□ Daemon HTTP lanzado y verificado (:8181)
□ (Opcional) nginx reverse proxy con SSL
□ Hook post-pipeline añadido a run_daily.sh y run_weekly.sh
□ CLAUDE.md colocado en la carpeta de briefs
□ MCP remoto registrado en Claude Code de cada usuario
□ Test end-to-end: usuario pregunta → QMD responde → Claude sintetiza
```
