# Guía Definitiva de Skills en Claude Code y Antigravity

- **Fuente:** [https://www.youtube.com/watch?v=ir--YLU4FiQ](https://www.youtube.com/watch?v=ir--YLU4FiQ)
- **Canal:** Josema Fernández | IA
- **Categoría:** claude-code-advanced
- **Duración:** 39min
- **Fecha:** 2026-03-23
- **Score OPENLAB Radar:** 7.5
  - Aplicabilidad: 8
  - Novedad: 7
  - Calidad: 7

---

## Resumen ejecutivo

Josema Fernández ofrece una guía exhaustiva sobre skills en Claude Code — desde la estructura básica (SKILL.md + context/ + templates/) hasta patrones avanzados. Además presenta Antigravity, un framework open-source para organizar y gestionar skills de Claude Code con convenciones predefinidas y herramientas de scaffolding.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** Confirma que la estructura de skills que usa OPENLAB (SKILL.md + context/ + templates/) es el **estándar de facto** de la comunidad. Refuerza la credibilidad del catálogo OAF y la propuesta de valor "zero lock-in, ficheros portables".
- **Referencias que conectan:** La estructura que Josema describe es idéntica a la de todos los skills OPENLAB — desde el Market Due Diligence hasta el Ideation Engine. Esto confirma que OPENLAB no usa un formato propietario sino el estándar emergente.
- **Capacidades de plataforma:** Todo lo descrito funciona nativamente en Claude Code CLI, que es el runtime de OPENLAB. No hay dependencias adicionales.
- **Oportunidades nuevas:** Evaluar **Antigravity** como posible herramienta de scaffolding para acelerar la creación de skills nuevos. Si su CLI genera la estructura SKILL.md + context/ + templates/ automáticamente, podría ahorrar tiempo en la fase de setup de nuevos proyectos. Categoría secundaria: delivery-adoption (el vídeo en español facilita la adopción en clientes hispanohablantes).
- **Argumento comercial:** "La estructura de nuestros agentes sigue el estándar abierto de la industria. No es formato OPENLAB — es el formato que 35+ plataformas entienden."

---

## Contenido detallado

### Ideas y argumentos principales

**Las skills como solución al problema de la ventana de contexto.** El argumento central del vídeo no es "las skills son útiles" sino que resuelven un problema técnico concreto: especializar a la IA sin saturar el contexto. La alternativa naive —pasarle un libro de 100 páginas sobre marketing— funciona pero es ineficiente porque ese contexto se consume en cada petición, aunque no sea necesario. Las skills cargan solo la descripción inicial de cada habilidad en el contexto base; el contenido completo de una skill solo se carga cuando la IA detecta que la necesita (o cuando el usuario la invoca explícitamente). De esta manera se pasa de una IA "notable en todo" a un "equipo de expertos" que se activa bajo demanda.

**Las skills son un estándar abierto, no un formato propietario.** Josema insiste en que la estructura `.agents/skills/` no es una invención de ninguna herramienta concreta: es el estándar emergente que ya adoptan Cursor, Open Code, Claude Code, Google Antigravity y otros entornos de vibe coding. La documentación oficial del estándar es la página `agentskill` (mencionada pero sin URL explícita). La convergencia hacia `.agents/skills/` está en curso; hoy las herramientas instalan en paralelo en `.agents/`, `.agent/` y `.claude/` por compatibilidad retroactiva, pero el destino es una única carpeta.

**Estructura mínima y opcional de una skill.** El único fichero obligatorio es `skill.md` (Markdown con nombre, descripción y pasos). Todo lo demás es opcional: carpeta `reference/` con documentos de contexto adicional, scripts ejecutables, plantillas de output. Josema categoriza dos tipos: skill básica (solo `skill.md`) y skill avanzada (con directorios adicionales). El idioma recomendado para el contenido es inglés porque la IA lo interpreta mejor.

**Instalación y gestión a través del CLI de skills.** El flujo de instalación es: buscar la skill en el repositorio de skills (web con listado y métricas de descargas), copiar el comando de instalación, ejecutarlo en la terminal del proyecto, y seleccionar herramienta destino + ámbito (proyecto vs. global). Josema recomienda siempre instalar a nivel de proyecto para mantener skills específicas por proyecto.

**El plugin "Skill Creator" de Claude Code.** Claude Code incluye un plugin que permite generar skills nuevas mediante lenguaje natural, sin escribir el Markdown manualmente. El flujo es: instalar el plugin desde "Manage Plugin", abrir una conversación nueva, invocar `/skill creator` con una descripción de la habilidad deseada. El resultado es un `skill.md` generado automáticamente que se añade a la carpeta `.claude/skills/`.

**Invocación explícita vs. automática.** En Antigravity se referencian skills con `@skill.md` seguido del nombre. En Claude Code se usa `/nombre-de-la-skill`. Si no se especifica, la IA infiere cuándo usarlas a partir de la descripción inicial. Josema recomienda especificarlas explícitamente cuando se conocen para no dejar el resultado en manos de la inferencia.

### Datos y evidencia

- **Mejora de resultados hasta 10 veces** según la promesa del canal (declaración del speaker, no estudio citado).
- La skill **Frontend Design** tenía ~95.100 estrellas en GitHub y **165.900 instalaciones en la última semana** en el momento de grabación.
- La skill **SEO Audit** tenía **45.300 descargas en la última semana**.
- El catálogo de skills del repositorio oficial supera las **20.000 habilidades** disponibles.
- Josema menciona un umbral práctico de confianza: skills con **más de 1.000 instalaciones** se pueden considerar seguras.
- Demo en vivo: landing page para agencia de IA generada en un solo prompt usando tres skills (Frontend Design + SEO Audit + Marketing Ideas), resultado: página con headline, secciones de servicios, CTA, FAQ y formulario de contacto.

### Citas textuales (2-4 máx)

> "Las skills solucionan este problema: vamos a darle más contexto, pero solamente en el momento que lo necesite." — Josema Fernández

> "Sin skills vamos a tener una generalista que va a ser un notable en todo, va a ser buena, pero no va a ser experto en nada en concreto." — Josema Fernández

> "Ahora en vez de tener una IA generalista, tenemos un equipo de expertos tanto en diseño como en SEO como en marketing." — Josema Fernández

> "Con solo ese prom y las habilidades hemos conseguido este resultado. O sea, literalmente aquí tenéis el mensaje que hemos visto y simplemente ha utilizado las habilidades y ha generado ese resultado." — Josema Fernández

### Ejemplos concretos

- **Repositorio oficial de skills** (agentskill): página web con listado de skills, métricas de instalaciones y comando de instalación CLI. Mencionada sin URL explícita.
- **Skill: Frontend Design** — skill de diseño web frontend, ~95k estrellas GitHub, 165k instalaciones/semana. Instalada vía CLI.
- **Skill: SEO Audit** — skill de auditoría SEO, 45k instalaciones/semana. Instalada vía CLI.
- **Skill: Marketing Ideas** — skill de copywriting y marketing. Instalada vía CLI.
- **Plugin "Skill Creator"** en Claude Code — plugin nativo que genera skills desde lenguaje natural. Se instala desde "Manage Plugin" y se invoca con `/skill creator` en una nueva conversación.
- **Demo de landing page** — sitio web para agencia de IA generado en un único prompt especificando las tres skills anteriores, usando HTML + CSS + JavaScript. El resultado incluye headline con propuesta de valor, secciones de servicios, metodología, resultados (ficticios), FAQ y formulario de contacto.
- **Google Drive público de Josema** — más de 30 flujos de N8N, asistentes telefónicos, plantillas y prompts de Claude Code/Antigravity, accesible desde la comunidad de Telegram (enlace en descripción del vídeo).

---

## Temas clave

### 1. Anatomía de un skill en Claude Code
Estructura canónica: SKILL.md (instrucciones principales), context/ (documentos de referencia, fuentes, datos), templates/ (formatos de output). Josema explica cuándo usar cada directorio y cómo Claude Code los carga.

### 2. Antigravity framework
Framework open-source que añade convenciones y herramientas sobre la estructura base de skills. Incluye scaffolding (crear skills desde templates), validación (verificar que la estructura es correcta) y gestión (listar, activar/desactivar skills). Pendiente evaluar si aporta valor sobre el approach manual de OPENLAB.

### 3. Patrones avanzados de skills
Josema cubre patrones como skills encadenados (un skill llama a otro), skills con inputs dinámicos (el usuario pasa parámetros), y skills con outputs múltiples (genera varios ficheros). Todos son patrones que OPENLAB ya usa pero que están bien articulados para referencia.


**Telegraph:** https://telegra.ph/Claude-Code-LangWatch-Skills-for-Product-Managers-03-26
