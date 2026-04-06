# OPENLAB Knowledge Base: arquitectura, distribución y organización

Documento de diseño completo para organizar el conocimiento de OPENLAB en Google Drive, distribuirlo al equipo y hacerlo consultable con Claude Code y Obsidian.

**Estado:** prácticamente completado — Fases 0, 1, 2, 3 y 6 implementadas. Fase 4 descartada. Fase 5 parcial (pipeline ha cambiado).
**Última actualización:** 2026-04-06

---

## 🔖 Estado actual (2026-04-06)

### Completado
- **Fase 0 ✓:** briefs/ e insights/ sacados del tracking de git. `.gitignore` verificado en VPS (briefs/, insights/, data/logs/). Drive sincronizado en el laptop de Rafael en `/Users/gavalle/Library/CloudStorage/GoogleDrive-rafa@openlabstudio.com/Shared drives/OPENLAB-RADAR`.
- **Fase 1 ✓:** rclone instalado y configurado en el VPS como usuario `openlab`. Config en `/home/openlab/.config/rclone/rclone.conf` apuntando al Team Drive **OPENLAB-RADAR**. Rutas: `gdrive:briefs` y `gdrive:insights`. Primer sync ejecutado: 33 briefs + 1 insight en Drive. Scripts `run_daily.sh` y `run_weekly.sh` actualizados con Paso 5 de sync automático.
- **Fase 2 ✓:** creados en la estructura Drive actual (antes de la reorganización /OPENLAB/):
  - `OPENLAB-RADAR/CLAUDE.md` → instrucciones de consulta optimizadas con patrón grep-first y taxonomía de tags
  - `COMERCIAL/proposals-index.yaml` → catálogo de 18 proposals con estados y rutas
  - `COMERCIAL/OPENLAB Strategy/CLAUDE.md` → ya existía con skill co-CEO completo
  - Symlink `~/OPENLAB` → `Shared drives/` creado en laptop de Rafael. `OPENLAB_KB=~/OPENLAB` en `~/.zshrc`.
  - Obsidian vault configurado en `OPENLAB-RADAR/`, plugin Dataview, `dashboard.md` con queries.
- **Fase 3 ✓:** `config/tags.yaml` creado en el VPS, prompts actualizados con frontmatter YAML, fix de strip frontmatter en `scripts/publish_telegraph.py`. Frontmatter aplicado retroactivamente a 29 ficheros (28 briefs + 1 insight). Telegraph verifica OK.
- **Fase 6 ✓:** `kb_viewer.html` generado diariamente por `generate_kb_viewer.py`, integrado en `run_daily.sh` (Paso 4b) y sincronizado a Drive (Paso 5). Accesible también en `openlabstudio.com/radar/`.

### Fase 5 — CLAUDE.md en clientes del Pipeline (parcial, pipeline actualizado)
CLAUDE.md creados:
  - `COMERCIAL/Pipeline/Dabo/CLAUDE.md` (cubre Dabo Consulting + OPCARS) ✓
  - `COMERCIAL/Pipeline/Iberostar/CLAUDE.md` ✓
  - `COMERCIAL/Pipeline/Mapfre/CLAUDE.md` ✓
  - `COMERCIAL/Pipeline/FINAVE/CLAUDE.md` — ⚠️ deal caído (2026-04-05)
  - `COMERCIAL/Pipeline/Nae/CLAUDE.md` — ⚠️ deal caído (2026-04-05)

Leads nuevos sin CLAUDE.md (pendiente cuando haya contexto suficiente):
  - COEXPHAL, Grupo DAMM, Tech Barcelona, Abac Capital

### Fase 4 — Skill "gestionar propuesta" → descartada
No se construyó. Con el volumen actual del equipo (4 personas), la gestión manual de `proposals-index.yaml` es suficiente. Se reevaluará si el pipeline crece significativamente.

### Pendiente — Rafael manualmente
- **Fase 2:** instalar Drive for Desktop en los laptops de Alberto, Carlos y Pepe.

---

---

## Contexto para nuevas sesiones de Claude Code

Este documento es la referencia central de un proyecto de reorganización del conocimiento de OPENLAB. Si estás leyendo esto en una sesión nueva — ya sea en el VPS o en el laptop de Rafael — aquí tienes lo que necesitas saber para orientarte.

### Qué es OPENLAB

Empresa de **context engineering**. Diseña skills (ficheros `.md`) que se ejecutan en Claude Code CLI como agentes de IA para procesos de conocimiento intensivo en empresas. Stack: Claude Code CLI + skills en lenguaje natural + MCP. Zero lock-in, zero código propio.

**El equipo son 4 personas:**
- **Alberto** — CEO, Founder. Lidera estrategia y posicionamiento.
- **Rafael** — CTO, Founder. Gatekeeper técnico: aprueba skills, gestiona el Radar y mantiene el orden en los sistemas.
- **Carlos** — Senior Consultant + Account Manager.
- **Pepe** — Senior Consultant + Account Manager.

### Qué estamos construyendo y por qué

OPENLAB tiene dos sistemas de conocimiento que hasta ahora están desconectados:

1. **OPENLAB Radar** — sistema en el VPS que monitoriza YouTube diariamente, evalúa vídeos con Claude Code y genera briefs en `briefs/` e `insights/`. Es inteligencia del sector en tiempo real. Hasta ahora solo accesible por SSH o por el email diario.

2. **Trabajo comercial** — proposals, assessments, demos, contexto de clientes. Vive en Google Drive en `/comercial/pipeline/` pero sin estructura de ciclo de vida ni conexión con la inteligencia del Radar.

El objetivo es **unificar todo bajo una única raíz `/OPENLAB/` en Google Drive**, sincronizada en los laptops del equipo, consultable con Claude Code y con Obsidian. Que cualquier miembro del equipo pueda preguntar: *"¿qué tendencias del Radar refuerzan la propuesta que le estamos mandando a este cliente?"* y obtener una respuesta cruzando ambos mundos.

### Cómo está dividido el trabajo

Este proyecto tiene tres tipos de tareas según quién las ejecuta:

**El VPS (sesión Claude Code en el servidor)** se encarga de todo lo que toca el Radar: actualizar los prompts del evaluador para que generen frontmatter con tags, instalar y configurar rclone para sincronizar con Drive, y corregir el script de Telegraph para que ignore el frontmatter al publicar.

**El laptop de Rafael (sesión Claude Code local)** se encarga de lo que vive en la carpeta compartida: crear los ficheros `CLAUDE.md` de cada zona, el `proposals-index.yaml`, y el skill "gestionar propuesta" que se añadirá al repo `openlab-catalog`.

**Rafael manualmente** hace lo que no puede hacer Claude Code: reorganizar las carpetas en Google Drive, compartirlas con el equipo, instalar Drive for Desktop en los laptops y configurar Obsidian.

Si estás en una sesión local y buscas qué hacer: ve a la sección **"Reparto de tareas por contexto de ejecución"** más abajo.

---

## El problema

El conocimiento de OPENLAB está fragmentado:
- Los briefs del Radar viven solo en el VPS
- Las proposals viven en `/comercial/pipeline/` sin estado ni índice
- La estrategia del CEO está desconectada de la inteligencia del Radar
- No hay estructura para proyectos activos ni entregados
- El equipo no puede hacer consultas cruzadas entre inteligencia, comercial y estrategia

---

## Estructura Drive objetivo

```
/OPENLAB/                                  ← raíz única compartida con todo el equipo
  │
  ├── clientes/                            ← ciclo de vida completo del cliente
  │     ├── pipeline/                      ← prospects en proceso de venta
  │     │     └── [empresa]/
  │     │           ├── inputs/            ← transcripts, docs de reuniones
  │     │           ├── propuesta-v1.md
  │     │           ├── propuesta-v2.md
  │     │           └── CLAUDE.md          ← contexto de este prospect para Claude Code
  │     │
  │     ├── activos/                       ← propuesta aceptada, proyecto en marcha
  │     │     └── [empresa]/               ← carpeta movida desde pipeline al aceptar
  │     │           ├── inputs/            ← heredado del pipeline
  │     │           ├── propuesta-final.md
  │     │           ├── entregables/       ← skills, assessments, guías, formación
  │     │           ├── seguimiento/       ← actas, iteraciones, feedback del cliente
  │     │           └── CLAUDE.md          ← contexto enriquecido con el proyecto
  │     │
  │     └── entregados/                    ← proyecto cerrado o en garantía
  │           └── [empresa]/               ← carpeta movida desde activos al cerrar
  │
  ├── comercial/                           ← herramientas del proceso de venta
  │     ├── demos/                         ← carpetas por cliente para demos en directo
  │     │     └── [empresa]/               ← skills corriendo en local + presentaciones
  │     ├── plantillas/                    ← plantillas de propuesta y assessment
  │     └── proposals-index.yaml           ← catálogo de todas las proposals con estado
  │
  ├── inteligencia/                        ← conocimiento que alimenta decisiones
  │     ├── radar/                         ← synced desde VPS via rclone
  │     │     ├── briefs/                  ← briefs diarios por categoría
  │     │     └── insights/               ← análisis generados a petición
  │     └── CLAUDE.md                      ← instrucciones para consultas sobre el Radar
  │
  ├── estrategia/                          ← workspace compartido del equipo (CEO lidera)
  │     ├── posicionamiento/
  │     ├── nuevas-lineas/                 ← lo que era /nuevos-proyectos
  │     ├── decisiones/
  │     └── CLAUDE.md                      ← co-CEO: contexto completo para decisiones
  │
  └── admin/                               ← operaciones internas (limpiar internamente)
        ├── legal/
        └── contabilidad/
```

**Permisos:** toda la estructura es accesible a todo el equipo. Transparencia total.

---

## Principios de diseño

### 1. El cliente tiene una carpeta que avanza con él

La misma carpeta, con todo su contexto e historia, se mueve físicamente:
```
pipeline/[empresa]/ → activos/[empresa]/ → entregados/[empresa]/
```
No hay duplicación. No hay que buscar en dos sitios. El CLAUDE.md dentro de la carpeta se enriquece a lo largo de todo el ciclo.

### 2. El estado de las proposals vive en el índice, no en el nombre de carpeta

`proposals-index.yaml` es el único sitio donde se registra el estado. La carpeta del cliente no cambia de nombre — el índice sabe dónde está y en qué estado.

### 3. El repo es la fábrica, Drive es el producto

La misma distinción que OPENLAB aplica con los clientes — el repo contiene el skill (la maquinaria), no los outputs que genera el agente — se aplica aquí:

| Sistema | Qué contiene | Analogía |
|---|---|---|
| **Git repo** (`openlab-radar`) | Scripts, prompts, config, docs | La fábrica |
| **Drive** (`inteligencia/radar/`) | Briefs, insights | El producto |

El repo no trackea `briefs/` ni `insights/`. Su canal de distribución al equipo es Drive vía rclone, no git. El cron no hace commits — los commits son siempre manuales.

**Skills del equipo:** misma lógica.
- `openlab-catalog` en GitHub → `/user/.claude/skills/` en cada laptop (git pull para actualizar)
- Para cada cliente en delivery: repo `openlab-[empresa]` en GitHub con skills personalizados, el cliente hace `git clone`

**Disciplina de edición para evitar conflictos git:**

| Dónde | Qué se edita |
|---|---|
| VPS | Scripts, prompts, config — lo que toca el pipeline del Radar |
| Laptop de Rafael | Docs, CLAUDE.md, skills de proposals — lo que toca el KB local |

Con esta separación natural cada contexto toca ficheros distintos y los conflictos de git son prácticamente imposibles.

**Limpieza pendiente del repo:** sacar `briefs/` e `insights/` del tracking de git (actualmente están trackeados por error). Tarea del VPS — ver checklist.

### 4. La inteligencia y la estrategia son ciudadanos de primera clase

No están enterradas dentro de `/comercial/`. Son carpetas raíz porque alimentan decisiones de empresa, no solo de venta.

---

## Cómo se conectan las piezas

**Para ventas y propuestas:**
```
/inteligencia/radar/briefs/       ← "¿qué está pasando en el sector?"
        +
/comercial/proposals-index.yaml   ← "¿qué estamos vendiendo y a quién?"
        +
/clientes/pipeline/[empresa]/     ← "¿qué sabemos de este cliente concreto?"
        ↓
Claude Code cruza los tres → argumentos con evidencias del Radar,
nuevos servicios relevantes para el sector, contexto para la reunión
```

**Para estrategia:**
```
/estrategia/                      ← "¿hacia dónde va OPENLAB?"
        +
/inteligencia/radar/              ← "¿qué está pasando fuera?"
        ↓
Claude Code en /estrategia/ tiene visión completa para decisiones del CEO
```

**Para un proyecto activo:**
```
/clientes/activos/[empresa]/      ← todo el contexto del cliente
        +
/inteligencia/radar/              ← tendencias relevantes para el sector del cliente
        ↓
Claude Code → recomendaciones de nuevos servicios, evolución del proyecto
```

---

## proposals-index.yaml

Fichero ligero en `/comercial/proposals-index.yaml`. Es el catálogo de todas las proposals — no duplica contenido, solo registra estado y ruta.

```yaml
- empresa: Empresa X
  sector: financiero
  contacto: Nombre Apellido
  servicios: [market-intelligence, skills-design]
  fecha_primer_contacto: 2026-02-10
  fecha_envio: 2026-03-15
  estado: en_negociacion          # ver estados posibles abajo
  path: clientes/pipeline/empresa-x/propuesta-v2.md
  notas: "Esperando aprobación del CTO"

- empresa: Empresa Y
  sector: innovacion-corporativa
  contacto: Nombre Apellido
  servicios: [workshop, skills-design]
  fecha_primer_contacto: 2026-01-20
  fecha_envio: 2026-02-28
  estado: aceptada
  path: clientes/activos/empresa-y/propuesta-final.md
  notas: "Kick-off semana del 15 de abril"
```

**Estados posibles:**
```
borrador        → en preparación, no enviada
enviada         → mandada al cliente, esperando respuesta
en_negociacion  → hay conversación activa, posibles cambios
aceptada        → proyecto arrancado, carpeta movida a activos/
rechazada       → descartada por el cliente
archivada       → antigua, sin actividad
```

---

## Skill "gestionar propuesta"

Skill que cualquier miembro del equipo puede invocar desde la carpeta del cliente:

> *"marca esta propuesta como enviada"*
> *"actualiza el estado a en negociación, añade nota: esperando al CTO"*
> *"acepta la propuesta"* → actualiza el índice + avisa de mover la carpeta a activos/

El skill hace:
1. Actualiza el estado en `proposals-index.yaml`
2. Añade frontmatter al fichero de propuesta: `status: enviada`, `fecha: hoy`
3. Si el estado es `aceptada`: indica qué carpeta mover y a dónde

El movimiento de carpeta en Drive se hace manualmente (drag & drop) — Drive no permite moverla desde Claude Code fácilmente y es una operación de 5 segundos.

---

## Sistema de tags con YAML frontmatter en los briefs

### El problema que resuelve

A medida que el knowledge base crece, cargar todos los briefs en contexto para responder una pregunta se vuelve ineficiente. Con frontmatter estructurado, Claude puede hacer `grep` para identificar qué ficheros son relevantes y cargar solo esos — patrón llamado **Context Loadability** en arquitectura agéntica.

### Formato

Bloque `---` al inicio de cada brief, antes del contenido:

```yaml
---
title: "Agent Skills: Code Beats Markdown (Here's Why)"
date: 2026-03-28
category: context-engineering
score: 8.5
tags:
  - token-optimization
  - skill-design
  - agent-architecture
  - client-delivery
  - commercial-argument
source: Sam Witteveen
url: https://www.youtube.com/watch?v=IjiaCOt7bP8
---
```

El cuerpo del brief no cambia.

### Taxonomía de tags (definida en `config/tags.yaml` en el VPS)

**Temas técnicos:**
```
context-engineering     token-optimization      skill-design
agent-architecture      multi-agent             mcp
context-window          evaluation              tool-use
knowledge-management    long-running-agents     harness-engineering
```

**Relevancia para OPENLAB:**
```
commercial-argument     → directamente usable en ventas o propuestas
client-delivery         → aplicable a cómo entregamos
skill-pattern           → patrón reutilizable en los skills que construimos
new-service             → oportunidad de nuevo servicio
workshop-material       → usable en DIBEX u otras formaciones
competitive-intel       → inteligencia sobre competidores o alternativas
```

**Tipo de señal:**
```
trend                   → tendencia emergente
technical-deep-dive     → análisis técnico profundo
case-study              → caso real con métricas
opinion                 → perspectiva del creador
tutorial                → guía práctica
```

**Entidades:**
```
anthropic   openai   google   microsoft
claude-code   langchain   cursor   n8n
```

### Patrones de grep para Claude Code

```bash
# Briefs con argumento comercial directo
grep -rl "commercial-argument" inteligencia/radar/briefs/

# Briefs de score alto sobre delivery
grep -rl "client-delivery" inteligencia/radar/briefs/ | xargs grep -l "score: [89]"

# Qué hay relevante para el sector financiero esta semana
grep -rl "commercial-argument\|new-service" inteligencia/radar/briefs/ \
  | xargs grep -l "2026-03"
```

### Coexistencia con carpetas

Las carpetas por categoría se mantienen. Los tags añaden dimensiones transversales que las carpetas no pueden expresar.

La taxonomía oficial vive en el VPS en `config/tags.yaml` — el evaluador diario la usa como referencia para asignar tags consistentes.

---

## Capa de visualización: Obsidian

Obsidian apunta a `~/OPENLAB/` como vault único. No requiere configuración adicional.

**Qué aporta:**

| Funcionalidad | Utilidad |
|---|---|
| Graph view | Visualizar conexiones entre briefs, detectar clusters |
| Plugin Dataview | Queries: "todos los briefs con tag `commercial-argument` esta semana" |
| Backlinks | Si dos briefs mencionan el mismo concepto, Obsidian los enlaza |
| Mobile app | Acceso a todo el conocimiento desde móvil |
| Canvas | Tableros para preparar propuestas o presentaciones |

**No necesita:**
- Obsidian Sync (de pago) → Drive for Desktop sincroniza
- Plugins de AI → Claude Code CLI es mejor

**Setup por persona:** Obsidian → "Open folder as vault" → `~/OPENLAB/`. Listo.

### Estructura de carpetas en el laptop de Rafael

```
/Users/gavalle/
  ├── _dev/                     ← todos los repos de git (el _ los pone primero en Finder)
  │     ├── openlab-radar/      ← este repo (la fábrica)
  │     ├── openlab-catalog/    ← skills del equipo (pendiente de clonar)
  │     └── openlab-[cliente]/  ← repos de delivery a clientes (cuando lleguen)
  │
  └── OPENLAB/                  ← Drive for Desktop (el producto)
        ├── inteligencia/
        ├── clientes/
        ├── comercial/
        └── estrategia/
```

---

## Sincronización VPS → Drive

El VPS sincroniza `briefs/` e `insights/` a `inteligencia/radar/` en Drive via rclone.

Guía técnica paso a paso: [`setup-rclone-google-drive.md`](setup-rclone-google-drive.md)

**Cambio respecto al doc original:** la ruta de destino en Drive es `gdrive:OPENLAB/inteligencia/radar/` en lugar de `gdrive:OPENLAB Radar/`.

Configuración en `config/.env`:
```bash
GDRIVE_BRIEFS_PATH="gdrive:OPENLAB/inteligencia/radar/briefs"
GDRIVE_INSIGHTS_PATH="gdrive:OPENLAB/inteligencia/radar/insights"
```

---

## Fix en publish_telegraph.py

Con frontmatter YAML en los briefs, el script `publish_telegraph.py` renderizaría el bloque `---` como texto visible en Telegraph. Fix necesario: strip del frontmatter antes de convertir a HTML.

Añadir al inicio de la función `publish()`, antes de `html = md_to_html(md_text)`:

```python
# Strip YAML frontmatter si existe
md_text = re.sub(r'^---\n.*?\n---\n?', '', md_text, flags=re.DOTALL)
```

El email diario no requiere cambios — procesa el daily briefing, no los briefs individuales.

---

## Distribución en los laptops del equipo

**Drive for Desktop** (instalar en cada laptop):
- Mac/Windows/Linux: google.com/drive/download
- Sincronizar la carpeta `OPENLAB/` localmente
- Ruta local recomendada: configurar Drive for Desktop para que sincronice en `~/OPENLAB/`

**Symlink para consistencia de rutas en skills:**
```bash
# Si Drive for Desktop monta en una ruta larga, crear symlink estable
ln -s "/ruta-real-de-drive-en-tu-laptop/OPENLAB" ~/openlab-kb
```

Variable de entorno en cada laptop (`~/.zshrc` o `~/.bashrc`):
```bash
export OPENLAB_KB=~/openlab-kb   # o ~/OPENLAB si Drive monta directo ahí
```

Los skills que necesiten proposals o inteligencia usan `$OPENLAB_KB/` en lugar de rutas absolutas.

---

## Reparto de tareas por contexto de ejecución

### Desde el VPS — sesión Claude Code en el servidor

| Tarea | Fase |
|---|---|
| Crear `config/tags.yaml` con la taxonomía oficial | 3 |
| Actualizar `prompts/evaluate-daily.md` para generar frontmatter | 3 |
| Actualizar `prompts/evaluate-manual.md` igual | 3 |
| Fix strip frontmatter en `scripts/publish_telegraph.py` | 3 |
| Instalar rclone en el VPS | 1 |
| Actualizar rutas rclone en `config/.env` y en los scripts | 1 |

La autenticación de rclone con Google es colaborativa: Claude Code inicia el proceso en el VPS y Rafael abre la URL OAuth en su navegador para autorizar.

### Desde el laptop de Rafael — sesión Claude Code local

| Tarea | Fase |
|---|---|
| Crear `OPENLAB/inteligencia/CLAUDE.md` | 2 |
| Crear `OPENLAB/estrategia/CLAUDE.md` (co-CEO) | 2 |
| Crear `OPENLAB/comercial/proposals-index.yaml` con estructura inicial | 2 |
| Diseñar e implementar el skill "gestionar propuesta" → PR a `openlab-catalog` | 4 |

### Manual — Rafael en Drive y en los laptops del equipo

| Tarea | Fase |
|---|---|
| Crear estructura de carpetas en Drive bajo `/OPENLAB/` | 0 |
| Mover contenido existente a las nuevas rutas | 0 |
| Compartir `/OPENLAB/` con Alberto, Carlos y Pepe | 0 |
| Instalar Drive for Desktop en los 4 laptops | 2 |
| Crear symlink `~/openlab-kb` en cada laptop | 2 |
| Abrir URL de autorización OAuth de rclone en el navegador | 1 |
| Abrir Obsidian vault sobre `~/OPENLAB/` en cada laptop | 2 |

**Orden recomendado para arrancar:** Rafael hace la Fase 0 en Drive (15-20 min) mientras Claude Code prepara las tareas del VPS en paralelo. Cuando Drive esté listo, el sync de rclone ya tiene destino donde escribir.

---

## Checklist de implementación

### Fase 0 — Reorganizar Drive y limpiar el repo ✓

- [x] Sacar `briefs/` e `insights/` del tracking de git (`.gitignore` verificado con briefs/, insights/, data/logs/)
- [x] Drive sincronizado en el laptop de Rafael: `/Users/gavalle/Library/CloudStorage/GoogleDrive-rafa@openlabstudio.com/Shared drives/OPENLAB-RADAR`

### Fase 1 — Sync VPS → Drive (rclone) ✓

- [x] Instalar rclone en el VPS → ver [`setup-rclone-google-drive.md`](setup-rclone-google-drive.md)
- [x] Actualizar rutas en `config/.env`: `gdrive:briefs` y `gdrive:insights` (Team Drive OPENLAB-RADAR)
- [x] Verificar que el primer sync llega correctamente a Drive (33 briefs + 1 insight)

### Fase 2 — Distribución al equipo

- [x] `OPENLAB-RADAR/CLAUDE.md` — instrucciones de consulta del Radar (optimizado con patrón grep-first y tags)
- [x] `COMERCIAL/proposals-index.yaml` — catálogo de 18 proposals con estados
- [x] Symlink `~/OPENLAB` → `Shared drives/` creado en el laptop de Rafael
- [x] `OPENLAB_KB=~/OPENLAB` añadido a `~/.zshrc` del laptop de Rafael
- [x] Obsidian vault abierto sobre `OPENLAB-RADAR/` en el laptop de Rafael — plugin Dataview instalado, `dashboard.md` creado
- [ ] Instalar Drive for Desktop en los laptops de: Alberto, Carlos, Pepe
- [ ] Crear symlink `~/OPENLAB` y añadir `OPENLAB_KB` en los laptops del equipo
- [ ] Abrir Obsidian como vault en los laptops del equipo (cuando proceda)

### Fase 3 — Sistema de tags en los briefs ✓

- [x] Crear `config/tags.yaml` en el VPS con la taxonomía oficial
- [x] Actualizar `prompts/evaluate-daily.md` para generar frontmatter
- [x] Actualizar `prompts/evaluate-manual.md` igual
- [x] Aplicar fix de strip frontmatter en `scripts/publish_telegraph.py`
- [x] Verificar que el primer brief con frontmatter se publica bien en Telegraph

### Fase 4 — Skill "gestionar propuesta" — descartada

Descartada por innecesaria con el volumen actual (4 personas). La gestión de `proposals-index.yaml` se hace manualmente.

### Fase 5 — CLAUDE.md en cada zona

- [x] `OPENLAB-RADAR/CLAUDE.md` — cómo consultar el Radar (creado en Fase 2)
- [x] `COMERCIAL/OPENLAB Strategy/CLAUDE.md` — co-CEO, ya existía con skill completo
- [x] `COMERCIAL/Pipeline/Dabo/CLAUDE.md` — Dabo Consulting + OPCARS
- [x] `COMERCIAL/Pipeline/Iberostar/CLAUDE.md` — Hotel Digital
- [x] `COMERCIAL/Pipeline/Mapfre/CLAUDE.md` — en negociación
- [x] ~~`COMERCIAL/Pipeline/FINAVE/CLAUDE.md`~~ — deal caído (2026-04-05)
- [x] ~~`COMERCIAL/Pipeline/Nae/CLAUDE.md`~~ — deal caído (2026-04-05)
- [ ] Leads nuevos (cuando haya contexto): COEXPHAL, Grupo DAMM, Tech Barcelona, Abac Capital

---

## Roles y permisos

OPENLAB trabaja con transparencia total, pero hay un rol diferenciado: **Rafael (CTO) es el gatekeeper** de lo que entra en los sistemas compartidos. El resto del equipo son usuarios cualificados.

### Equipo

| Persona | Rol | Función en el KB |
|---|---|---|
| **Alberto** | CEO, Founder | Estrategia y posicionamiento |
| **Rafael** | CTO, Founder | Gatekeeper técnico — aprueba skills, Radar y organización |
| **Carlos** | Senior Consultant + Account Manager | Lleva cuentas de cliente |
| **Pepe** | Senior Consultant + Account Manager | Lleva cuentas de cliente |

### En Google Drive

| Carpeta | Carlos y Pepe | Alberto | Rafael |
|---|---|---|---|
| `inteligencia/radar/` | Lector | Lector | Editor |
| `estrategia/` | Lector | Editor | Editor |
| `clientes/pipeline/` | Editor — todos | Editor | Editor |
| `clientes/activos/` | Editor — todos | Editor | Editor |
| `clientes/entregados/` | Lector | Lector | Editor |
| `comercial/proposals-index.yaml` | Lector | Lector | Editor |
| `comercial/plantillas/` | Lector | Lector | Editor |
| `admin/` | Restringido | Restringido | Editor |

**Modelo de colaboración en clientes:** todo el equipo puede leer, escribir y comentar en cualquier carpeta de cliente. Las proposals y assessments se trabajan entre varios — proponer, revisar, aprobar — antes de salir al cliente. No hay silos por account manager.

### En GitHub (openlab-catalog)

El equipo puede proponer skills mediante Pull Request. Rafael revisa y hace merge. Un skill no llega a `/user/.claude/skills/` de ningún laptop hasta que Rafael lo aprueba en el repo.

Flujo:
```
Miembro del equipo crea skill → PR en openlab-catalog
  → Rafael revisa → merge
    → cada laptop hace git pull → skill disponible
```

### En el VPS (Radar)

Solo Rafael tiene acceso SSH al VPS. Los parámetros del Radar (canales monitorizados, keywords, prompts del evaluador) son decisión suya. El equipo consume los outputs pero no configura el sistema.

---

## Decisiones tomadas

| Decisión | Elección | Descartado | Motivo |
|---|---|---|---|
| Raíz del knowledge base | `/OPENLAB/` única | `/OPENLAB-Radar/` como raíz | Las proposals y la estrategia no son sub-recursos del Radar |
| Organización de clientes | Carpetas por etapa (pipeline/activos/entregados) | Todo en pipeline | El cliente avanza con su carpeta; contexto siempre accesible |
| Estado de proposals | `proposals-index.yaml` centralizado | Nombre de carpeta / frontmatter solo | Índice ligero permite queries sin cargar proposals completas |
| Skills | Git (openlab-catalog) + repo por cliente | Drive | Git es para código/skills; Drive es para documentos |
| Vault de Obsidian | Uno solo sobre `~/OPENLAB/` | Un vault por carpeta | Una sola interfaz para todo el conocimiento de empresa |
| Sync Radar | rclone VPS → `inteligencia/radar/` | Carpeta separada | Todo bajo una raíz facilita el vault único y la consulta cruzada |
| Acceso equipo | Todo compartido, transparencia total | Acceso diferenciado por área | Forma de trabajar de OPENLAB |
| Plugins AI en Obsidian | Ninguno | Smart Connections, Copilot | Claude Code CLI es mejor y ya está en el workflow |

---

## Fase 6 — Visualizador HTML del Knowledge Base

### Qué es

`kb_viewer.html` — fichero HTML autogenerado, self-contained, sin servidor. Diseñado para que cualquier miembro del equipo pueda abrir el knowledge base de un doble clic en Finder y escanear lo más importante en 2 minutos.

**UX:** el archivo vive en la raíz de `OPENLAB/inteligencia/radar/` en Google Drive. Los usuarios lo abren desde su copia local sincronizada. Funciona completamente offline (`file://`).

```
VPS (cron 08:00 UTC)
  └─ run_daily.sh
       ├─ Paso 4b: genera data/kb_viewer.html
       └─ Paso 5:  rclone sube kb_viewer.html → OPENLAB/inteligencia/radar/

Usuario OPENLAB (laptop, Drive sincronizado)
  └─ ~/OPENLAB/inteligencia/radar/kb_viewer.html
       └─ doble clic → se abre en el navegador
```

### Secciones del dashboard

| Sección | Propósito |
|---|---|
| **⚡ Hot Signals** | Top 5 briefs con score ≥ 8.0 de los últimos 7 días — lo más urgente |
| **🗓 Nuevos esta semana** | Todos los briefs recientes agrupados por día — cronología de la semana |
| **📂 Por categoría** | Tabs con los briefs más importantes de cada categoría + estadísticas |
| **🏷 Tag Explorer** | Nube de tags interactiva — click en un tag filtra todos los briefs relacionados |
| **💡 Insights** | Cards de los análisis en `insights/` con extracto |
| **🔍 Buscador** | Búsqueda en tiempo real sobre título, fuente, tags y extracto |
| **Stats (nav fijo)** | Total briefs · Score medio · Fecha último brief · Nº insights |

### Diseño

- **Paleta:** fondo negro (`#000000`), acento lima (`#CCFF00`), superficies `#0F0F23`/`#141414` — idéntica a los emails diarios
- **Tipografía:** Montserrat (Google Fonts CDN)
- **Datos:** JSON embebido en el HTML (`KB_DATA`). Sin requests HTTP en runtime — funciona offline
- **JS:** vanilla, sin frameworks. Tabs, filtros y búsqueda sobre el JSON local

### Generación

```bash
# Desde el VPS (automático en cron)
python3 scripts/generate_kb_viewer.py
# → data/kb_viewer.html

# Desde el laptop de Rafael (Drive local)
python3 scripts/generate_kb_viewer.py \
  --briefs-dir ~/OPENLAB/inteligencia/radar/briefs \
  --insights-dir ~/OPENLAB/inteligencia/radar/insights \
  --output ~/OPENLAB/inteligencia/radar/kb_viewer.html
```

### Integración pipeline (`run_daily.sh`)

Dos cambios en el VPS:

**Paso 4b** (nuevo, entre email y sync Drive):
```bash
python3 "$PROJECT_DIR/scripts/generate_kb_viewer.py" \
    --output "$PROJECT_DIR/data/kb_viewer.html"
```

**Paso 5** (ampliar con copia explícita del viewer):
```bash
rclone copyto "$PROJECT_DIR/data/kb_viewer.html" \
    "${GDRIVE_RADAR_ROOT}/kb_viewer.html" --quiet
```
`GDRIVE_RADAR_ROOT` apunta a `OPENLAB/inteligencia/radar` en Team Drive — añadir a `config/.env`.

### Variable de entorno nueva

```bash
# config/.env
GDRIVE_RADAR_ROOT=gdrive:OPENLAB/inteligencia/radar
```

### Checklist de implementación ✓

- [x] Crear `scripts/generate_kb_viewer.py`
- [x] Añadir variable `GDRIVE_RADAR_ROOT` en `config/.env` del VPS
- [x] Añadir Paso 4b en `run_daily.sh`
- [x] Ampliar Paso 5 en `run_daily.sh` con `rclone copyto` del viewer
- [x] Verificar que `data/kb_viewer.html` no está en `.gitignore`
- [x] Accesible también en `openlabstudio.com/radar/` (embebido en la web)
