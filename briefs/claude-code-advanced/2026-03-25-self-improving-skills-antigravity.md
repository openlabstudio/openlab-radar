# Claude Code Self-Improving Skills Are the Smarter Way to Build With AI

- **Fuente:** [https://www.youtube.com/watch?v=vyaRctf_UW0](https://www.youtube.com/watch?v=vyaRctf_UW0)
- **Canal:** Adrian Szramowski
- **Categoría:** claude-code-advanced
- **Duración:** 15min
- **Fecha:** 2026-03-25
- **Score OPENLAB Radar:** 7.5
  - Aplicabilidad: 8
  - Novedad: 7
  - Calidad: 7

---

## Resumen ejecutivo

Tutorial práctico sobre creación y mejora de Claude skills usando el entorno Antigravity. Cubre dos flujos de creación (desde Claude.ai dashboard, desde el skill creator plugin), la analogía CLAUDE.md = trabajador / skills = herramientas especializadas, y el concepto de auto-evolución de skills mediante evals JSON integrados. Documenta que usar skills reduce tokens consumidos frente a respuestas sin skill.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** El flujo de creación de skills desde Claude.ai dashboard (con memoria del usuario) → exportar como .md → importar en Antigravity es el proceso más accesible para que clientes no técnicos creen sus primeros skills. OPENLAB puede enseñar este flujo en el workshop DIBEX sin requerir conocimiento de CLI.
- **Referencias que conectan:** El skill creator plugin que el speaker usa es análogo al skill-creator de OPENLAB. La demo de evals JSON que auto-evolucionan el skill conecta directamente con el vídeo de AutoResearch (aWZG6inDrpU, score 8.5) del mismo día — juntos forman un argumento completo sobre skills que se mejoran solos.
- **Capacidades de plataforma:** El dato de que skills usan menos tokens que respuestas sin skill es importante para el argumento de coste: en entornos con límites de contexto, la arquitectura de skills no solo mejora calidad sino que también es más eficiente.
- **Oportunidades nuevas:** El flujo "Claude.ai dashboard → Antigravity" puede ser el onboarding de OPENLAB para clientes que quieren empezar a crear sus propios skills sin tocar CLI. El dashboard de Claude.ai tiene acceso a la memoria del usuario → el skill generado ya incorpora el contexto del negocio del cliente.
- **Argumento comercial:** "El primer skill lo creamos nosotros. Con este proceso, tú puedes crear el siguiente en 10 minutos desde el dashboard de Claude — sin tocar código, sin configurar nada."

---

## Contenido detallado

### Ideas y argumentos principales

El speaker abre con la distinción fundamental que todo usuario de Claude Code debería tener clara:

**CLAUDE.md = el trabajador (construction worker):** Sabe cómo hacer las cosas. Tiene procedimientos. Sabe operar. Se carga en cada conversación porque es el contexto base del agente.

**Skills = herramientas especializadas (hammer, screwdriver):** Herramientas dedicadas para tareas específicas. No necesitas que el trabajador sepa escribir emails todo el tiempo — solo cuando le pides que escriba emails. Entonces va a buscar el skill y lo usa. Ventaja: el trabajador (CLAUDE.md) no necesita cargar ese conocimiento en su contexto base.

**Por qué separar:** Poner todo en CLAUDE.md es ineficiente. El trabajador carga todo ese contexto en cada pregunta, aunque no sea relevante. Con skills, el conocimiento específico solo se activa cuando se necesita.

**Flujo 1: Crear skill desde Claude.ai dashboard:**
1. Entrar al dashboard de Claude → Customize → Skills
2. Claude tiene memoria del usuario y del negocio (si se ha compartido) → genera el skill con ese contexto
3. El dashboard pregunta: ¿para qué nichos? ¿qué reglas de copy? ¿debe aplicar tus reglas específicas?
4. Genera el skill personalizado
5. Descargar como texto plano (importante: pedir explícitamente texto plano, no ZIP)
6. Renombrar a `skill.md`
7. Importar en Antigravity → carpeta skills/ → subcarpeta por tipo (e.g., copywriter/)
8. Verificar: "¿Puedes acceder a este skill?" → el agente confirma

**Flujo 2: Crear skill desde skill creator plugin en Claude Code:**
1. Plugin Manager → buscar "skill creator" → instalar (para proyecto, para usuario, o global)
2. Plan mode → "I want you to create me a skill to write emails"
3. El plugin lee templates, explora posibilidades, hace preguntas de clarificación
4. Genera el skill con plan para aprobación
5. Una vez aprobado, crea el skill con carpeta propia

**Auto-evolución con evals JSON:** El plugin skill creator puede generar automáticamente un fichero `evals.json` junto al skill. Este fichero contiene benchmarks. Claude Code usa el eval para comparar el output actual con el benchmark y propone mejoras automáticas. El speaker lo llama "auto-repair" — el skill se auto-reparará si detecta degradación.

**Beneficio de tokens:** Demo directa: el mismo prompt con skill usa significativamente menos tokens que sin skill. En entornos con límites de contexto, esto es relevante. El output con skill también está más estructurado.

### Datos y evidencia

- Demo: skill de email copywriter generado desde Claude.ai dashboard con memoria de usuario (niches, copy rules, SmartLead variables aplicados automáticamente)
- Demo: newsletter writer skill creado por skill creator plugin
- Demo comparativa de tokens: skill presente vs ausente en el mismo prompt → skill usa "mucho menos tokens" (sin dato exacto pero la comparativa es visible)
- Demo de benchmarks: localhost con comparativa side-by-side de outputs con/sin skill, historial de tokens, panel de feedback

### Citas textuales

> "Think about CLAUDE.md as your construction worker. He knows how to do things. But if you want him to do a specific task, he needs tools. Think about skills as specific dedicated tools just to fulfill your need." — Adrian Szramowski

> "You don't need this to be inside your CLAUDE.md. This is something that you will ask your specialist: 'Hey, I want you to write me emails.' And then he will go to skills, take the specific skill, and then write you an email." — Adrian Szramowski

### Ejemplos concretos

- **Skill de copywriter:** Generado desde Claude.ai dashboard con memoria del usuario. Incluye niches específicos, reglas de copy non-negociables, variables de SmartLead. El agente aplicó el contexto del negocio del usuario sin que se lo pidieran explícitamente.
- **Skill de newsletter writer:** Creado por skill creator plugin. Genera carpeta propia dentro de skills/ con el skill.md y el evals.json.
- **Skill de AI news summary:** Demo avanzada con benchmarks: localhost muestra side-by-side del output con skill vs sin skill, tokens usados, panel de feedback para entrenar al skill.
- **Antigravity:** Entorno mencionado como el environment del speaker. Plugin manager para instalar skills/herramientas en Claude Code.

---

## Temas clave

### 1. La analogía trabajador/herramienta como explicación para no técnicos

CLAUDE.md = construcción worker (sabe operar, tiene procedimientos, siempre presente) vs skill = herramienta especializada (hammer, screwdriver, activada solo cuando se necesita). Es la mejor explicación visual para un cliente sin contexto técnico. En DIBEX, esta analogía debería ser el punto de entrada para explicar la arquitectura de skills.

### 2. Claude.ai dashboard como punto de entrada para creación de skills

El flujo dashboard → exportar → importar en Antigravity democratiza la creación de skills sin CLI. El dashboard ya tiene la memoria del usuario, así que el skill generado incorpora automáticamente el contexto del negocio. Es el camino de menor resistencia para que un cliente no técnico cree su primer skill.

### 3. Evals JSON como mecanismo de auto-evolución integrado en el skill

El skill creator plugin genera automáticamente un fichero de evaluación junto al skill. Este fichero permite que Claude Code compare outputs con benchmarks y proponga mejoras autónomas. Es la versión "integrada en el producto" del AutoResearch pattern que el vídeo aWZG6inDrpU describe con más profundidad.


**Telegraph:** https://telegra.ph/Claude-Code-Self-Improving-Skills-Are-the-Smarter-Way-to-Build-With-AI-03-25
