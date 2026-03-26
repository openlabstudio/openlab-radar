# Buenas prácticas: estructura de skills en Claude Code

**Generado:** 2026-03-26
**Fuentes:** 11 briefs de OPENLAB Radar (2026-03-23 a 2026-03-26)
**Uso:** checklist para auditar skills globales en laptop y proyectos de clientes

---

## Cómo usar este documento

Cada sección tiene un bloque **✅ Checklist** al final. Úsalo para revisar tus skills globales en `~/.claude/skills/` uno a uno. El objetivo no es cumplir el 100% — es identificar qué skills tienen deuda técnica o riesgo de degradar rendimiento.

---

## 1. Arquitectura de tres capas (progressive disclosure)

El patrón más consistente en todos los briefs. Un skill bien construido tiene tres niveles que se cargan progresivamente, no todo de golpe.

| Capa | Qué contiene | Cuándo se carga | Coste en tokens |
|------|-------------|-----------------|-----------------|
| **1 — Metadata** | `name` + `description` en frontmatter | Siempre, en cada prompt | ~30-50 tokens |
| **2 — Instrucciones** | Cuerpo del SKILL.md | Solo cuando el skill se activa | 500-2.000 tokens |
| **3 — Recursos** | `references/`, `scripts/`, `assets/` | Solo cuando la ejecución lo requiere | Variable, bajo demanda |

**Por qué importa:** un CLAUDE.md de 2.000 líneas consume 20.000+ tokens antes de que empiece el trabajo. Con progressive disclosure, el mismo contenido cuesta 30-50 tokens hasta que se necesita.

**✅ Checklist**
- [ ] El SKILL.md es conciso (menos de ~300 líneas / ~2.000 tokens)
- [ ] El contenido voluminoso (listas largas, documentación, ejemplos extensos) está en `references/`, no en el cuerpo del SKILL.md
- [ ] La `description` en el frontmatter es suficientemente específica para que Claude active el skill en el contexto correcto y no lo active en contextos incorrectos

---

## 2. El principio "Point, don't dump"

El SKILL.md referencia recursos externos — no los contiene. Un skill no es un repositorio de información; es un procedimiento que sabe dónde encontrar la información cuando la necesita.

**Ejemplos concretos:**
- ❌ SKILL.md con 139 tácticas de marketing inline
- ✅ SKILL.md con categorías + referencia a `references/marketing-tactics.md` que Claude carga solo si la tarea lo requiere

- ❌ SKILL.md con todas las plantillas de output embebidas
- ✅ SKILL.md que apunta a `assets/templates/` y los carga en la fase de generación

**Antipatrón nombrado — "Token trap"** (Timothy Carambat):
> "Skills are just system prompts with better marketing. It's a huge token trap and I feel like nobody's talking about it."

El riesgo real: skills que pesan 5.000-21.000 tokens se cargan completos en cada invocación. En workflows con múltiples skills encadenados, los costes se multiplican.

**✅ Checklist**
- [ ] El SKILL.md no contiene listas de más de ~20 items (si las hay, moverlas a `references/`)
- [ ] Las plantillas de output están en `assets/`, no inline en el SKILL.md
- [ ] La documentación de referencia (APIs, schemas, guías) está en `references/`, no en el cuerpo

---

## 3. El CLAUDE.md como enrutador, no como depósito

Lo que aplica a skills aplica también al CLAUDE.md de proyecto: debe ser ligero y enrutar hacia skills, no acumular instrucciones.

**Patrón correcto:**
- CLAUDE.md: ~500 tokens — quién eres, cómo priorizas, qué skills globales usar y cuándo
- Skills: contienen el procedimiento específico
- References: contienen el conocimiento específico

**Antipatrón:** CLAUDE.md con secciones largas de instrucciones que deberían estar en un skill o reference file. Cada línea del CLAUDE.md se consume en cada prompt.

**✅ Checklist**
- [ ] El CLAUDE.md global en el laptop no excede ~500 tokens (aprox. 400 palabras)
- [ ] Las instrucciones específicas por dominio (cómo escribir código Python, cómo revisar PRs, etc.) están en skills separados, no en el CLAUDE.md
- [ ] El CLAUDE.md menciona qué skills existen y en qué contexto usarlos

---

## 4. Sweet spot: 20-30 skills

Dato de Simon Scrapes con respaldo cuantitativo:

- **< 20 skills:** gaps de cobertura, tareas recurrentes sin procedimiento definido
- **20-30 skills:** máxima fiabilidad y velocidad de invocación
- **> 30 skills:** conflictos de activación, tiempos de respuesta más lentos, tasa de invocación correcta cae hasta el ~10%

**Implicación práctica:** si tienes más de 30 skills globales, no es necesariamente un problema de cantidad — es una señal de que algunos skills son demasiado granulares y deberían consolidarse, o de que algunos ya no son relevantes.

**✅ Checklist**
- [ ] El total de skills en `~/.claude/skills/` es ≤ 30
- [ ] Si hay > 30, identificar cuáles no se han invocado en el último mes y archivarlos
- [ ] Los skills se agrupan temáticamente (no hay duplicados ni solapamientos evidentes)

---

## 5. Description: la pieza más crítica del frontmatter

La `description` en el frontmatter es lo único que Claude lee para decidir si activar el skill. Si es vaga o genérica, el skill se activa cuando no debe o no se activa cuando debe.

**Criterios para una buena description:**
- Describe **cuándo** usar el skill, no solo qué hace
- Menciona los triggers de activación (qué diría el usuario)
- Es específica enough para no colisionar con otros skills

**Ejemplos:**
- ❌ `description: Ayuda con tareas de escritura`
- ✅ `description: Redactar posts para LinkedIn siguiendo el marco hook-insight-CTA. Usar cuando el usuario pida crear contenido para LinkedIn o redes profesionales.`

**✅ Checklist**
- [ ] Cada skill tiene una `description` que incluye el contexto de activación (cuándo usarlo)
- [ ] Ninguna `description` es intercambiable con la de otro skill
- [ ] Las descriptions usan verbos de acción y mencionan el output esperado

---

## 6. Un skill = una responsabilidad

El antipatrón más común: skills que intentan hacer demasiado. Un agente con 15 skills sobrecargados es completamente inestable — pierde contexto, mezcla tareas, alucina.

**Criterio de separación:** si un skill tiene más de una sección "Workflow" con fases de naturaleza muy distinta, probablemente debería dividirse.

**Señales de que un skill hace demasiado:**
- El título del skill usa "y" (ej. "Analizar y redactar informes")
- El SKILL.md tiene más de 5 fases claramente diferenciadas
- El skill carga reference files de dominios distintos

**✅ Checklist**
- [ ] Cada skill tiene una responsabilidad principal expresable en una frase
- [ ] Los skills complejos multi-fase están diseñados con fases que comparten contexto (no son tareas independientes)
- [ ] No hay skills que sean "navaja suiza" de tareas no relacionadas

---

## 7. Idioma de las instrucciones

Los briefs coinciden: las instrucciones en inglés producen mejores resultados porque los modelos se entrenaron principalmente en inglés.

**Práctica recomendada:**
- Instrucciones (SKILL.md, reference files): en inglés
- Contenido de output dirigido al usuario final: en el idioma del usuario (configurar en el skill)
- Nombre del skill y description: en inglés para consistencia

**✅ Checklist**
- [ ] El cuerpo del SKILL.md está en inglés
- [ ] Si el skill genera outputs en español, el skill especifica explícitamente el idioma de output
- [ ] Los nombres de carpetas y ficheros de resources están en inglés

---

## 8. Evaluation criteria integrados

Para skills que generan outputs recurrentes (posts, informes, análisis), incluir criterios de evaluación en el propio skill permite que Claude autoevalúe antes de entregar.

**Formato recomendado:** preguntas sí/no, nunca puntuaciones del 1-10.

> "Una pregunta de puntuación del 1-10 invita al modelo a optimizar hacia scores altos aunque el output sea raro. Una pregunta sí/no fuerza a evaluar el criterio real." — Adrian Szramowski

**Ejemplo en SKILL.md:**
```
## Self-check before delivering
- [ ] Does the output follow the required format?
- [ ] Is the tone appropriate for the target audience?
- [ ] Are all mandatory sections present?
If any answer is NO, revise before delivering.
```

**✅ Checklist**
- [ ] Los skills que generan outputs recurrentes tienen sección de self-check
- [ ] Los criterios son preguntas sí/no, no puntuaciones
- [ ] El self-check está al final del SKILL.md, antes del output

---

## 9. Estructura de carpetas recomendada

```
~/.claude/skills/
└── nombre-del-skill/
    ├── SKILL.md              ← obligatorio, ≤ 2.000 tokens
    ├── references/           ← documentación de apoyo, cargada bajo demanda
    │   ├── domain-knowledge.md
    │   └── examples.md
    ├── scripts/              ← código ejecutable (Python, Bash)
    │   └── process.py
    └── assets/               ← plantillas y ficheros de output
        └── template.md
```

**Reglas:**
- `references/` si el contenido es documentación que Claude debe leer
- `scripts/` si es código que Claude debe ejecutar (no leer)
- `assets/` si son plantillas o ficheros que Claude usa para generar el output final
- No crear subcarpetas dentro de `references/` — mantener plano

**✅ Checklist**
- [ ] La estructura de carpetas sigue el estándar (SKILL.md + references/ + scripts/ + assets/)
- [ ] No hay ficheros sueltos fuera de las carpetas estándar
- [ ] Los scripts en `scripts/` son ejecutables (`chmod +x`)

---

## 10. Portabilidad entre herramientas

Un skill bien construido funciona en Claude Code, Cursor, Open Code y Google Antigravity sin modificaciones. El estándar emergente converge hacia `.agents/skills/` como carpeta canónica, con cada herramienta manteniendo además su propia carpeta (`.claude/skills/` para Claude Code).

**Implicación:** no usar instrucciones específicas de una herramienta dentro del SKILL.md si el skill puede ser útil en otros contextos.

**✅ Checklist**
- [ ] El SKILL.md no contiene instrucciones específicas de Claude Code si el skill es de uso general
- [ ] Las instrucciones específicas de herramienta están aisladas en una sección o reference file propio

---

## Checklist rápido por skill (para la auditoría)

Copia este bloque y rellénalo para cada skill:

```
Skill: _______________
Ruta: ~/.claude/skills/_______________/

TAMAÑO
[ ] SKILL.md < 300 líneas
[ ] No hay listas > 20 items inline

FRONTMATTER
[ ] name: específico y único
[ ] description: incluye cuándo activar, no solo qué hace

ESTRUCTURA
[ ] Contenido voluminoso en references/, no en el cuerpo
[ ] Plantillas en assets/, no inline
[ ] Si tiene scripts, están en scripts/ y son ejecutables

RESPONSABILIDAD
[ ] Una responsabilidad principal expresable en una frase
[ ] No hace cosas de dominios no relacionados

IDIOMA
[ ] Instrucciones en inglés
[ ] Idioma de output especificado si es distinto del inglés

EVALUACIÓN (solo para skills de output recurrente)
[ ] Tiene sección de self-check con preguntas sí/no

SCORE: ___/12
```

---

## Fuentes

| Brief | Score | Aporte principal |
|-------|-------|-----------------|
| [Simon Scrapes — The Easiest Way to Get Ahead With Claude Code](../briefs/claude-code-advanced/2026-03-26-the-easiest-way-to-get-ahead-with-claude-code.md) | 7.5 | Arquitectura tres capas, sweet spot 20-30, "point don't dump" |
| [Tim Carambat — Skills.md Token Trap](../briefs/context-engineering/2026-03-24-skills-md-token-trap.md) | 8.2 | Antipatrón token trap, coste real de skills pesados |
| [Adrian Szramowski — Self-Improving Skills](../briefs/claude-code-advanced/2026-03-25-claude-code-self-improving-skills.md) | 8.5 | Eval suites, criterios sí/no, bucle de auto-mejora |
| [Josema Fernández — Guía Skills Antigravity](../briefs/claude-code-advanced/2026-03-24-guia-skills-antigravity.md) | 7.3 | Invocación, instalación, skills encadenados |
| [Skill vs Agent Architecture — OpenClaw](../briefs/agentic-systems/2026-03-25-skill-vs-agent-openclaw-architecture.md) | 8.0 | One writer rule, 4 ficheros core del agente, VPS |
| [3 Markdown Files Fix Agent Memory](../briefs/context-engineering/2026-03-24-3-markdown-files-agent-memory.md) | 7.8 | Agent kernel, memoria persistente, state.md |
| [NotebookLM Agent Skills](../briefs/context-engineering/2026-03-24-notebooklm-agent-skills.md) | 7.2 | Estándar .agents/skills/, descubrimiento por descripción |
