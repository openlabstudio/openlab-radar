# NotebookLM Agent Skills: Build POWERFUL Claude AI Agents for ANYTHING!

- **Fuente:** [https://www.youtube.com/watch?v=I-4cJgqF_JY](https://www.youtube.com/watch?v=I-4cJgqF_JY)
- **Canal:** Universe of AI
- **Categoría:** context-engineering
- **Duración:** 15min
- **Fecha:** 2026-03-23
- **Score OPENLAB Radar:** 8.0
  - Aplicabilidad: 9
  - Novedad: 7
  - Calidad: 7

---

## Resumen ejecutivo

Josema Fernández (Dominia Academy) presenta una guía práctica sobre agent skills — ficheros .md que convierten a una IA generalista en un equipo de expertos especializados. Cubre la estructura del estándar (skill.md + reference/), la instalación desde el marketplace (+20.000 skills disponibles), y demuestra el uso combinado de tres skills (Frontend Design, SEO Audit, Marketing Ideas) para generar una landing page completa. También muestra el plugin Skill Creator de Claude Code para crear skills propias desde lenguaje natural. Nota: pese al título del vídeo, no se menciona NotebookLM en ningún momento.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** Confirma que la arquitectura de skills OPENLAB (SKILL.md + context/ + templates/) sigue el **estándar emergente** adoptado por Claude Code, Gemini, Cursor y Open Code. El vídeo valida el approach y lo explica en español — útil para clientes hispanohablantes y para el workshop DIBEX.
- **Referencias que conectan:** Todos los skills del catálogo OAF (Market Due Diligence, Ideation Engine, etc.) siguen exactamente esta estructura. El marketplace de +20.000 skills confirma que hay un ecosistema creciente alrededor de este estándar.
- **Capacidades de plataforma:** Todo lo demostrado funciona nativamente en Claude Code CLI, que es el runtime de OPENLAB. El plugin Skill Creator podría acelerar el scaffolding de nuevos skills para clientes.
- **Oportunidades nuevas:** Usar este vídeo como **material de referencia en español** para explicar a clientes qué son las skills y cómo funcionan. También evaluar si el marketplace de skills tiene componentes reutilizables para acelerar entregas.
- **Argumento comercial:** "La estructura de nuestros agentes sigue el estándar abierto de la industria — 20.000 skills públicas, múltiples herramientas compatibles. No es formato propietario, es el formato que el ecosistema entiende."

---

## Contenido detallado

### Ideas y argumentos principales

El speaker (Josema Fernández, fundador de Dominia Academy) presenta las **agent skills** como el mecanismo que permite pasar de una IA generalista a un equipo de expertos especializados. La tesis central es que dar a la IA mucho contexto de forma indiscriminada es ineficiente — satura la ventana de contexto con información que no se necesita en ese momento. Las skills resuelven esto porque solo se cargan cuando la tarea lo requiere: el agente lee únicamente la descripción inicial de cada skill (las primeras líneas), y solo carga el contenido completo si la descripción coincide con el prompt recibido.

El argumento de fondo es de optimización de contexto: no se trata de dar más contexto, sino de darlo en el momento preciso. Una skill es un fichero Markdown (`.md`) con nombre, descripción y pasos de ejecución. Puede ser básica (solo el `skill.md`) o extendida (con carpetas `reference/`, scripts o plantillas adicionales). El estándar se llama "agent skill" y está adoptado por Claude Code, Google Gemini (Antigravity en el vídeo), Cursor y Open Code: la carpeta canónica es `.agents/skills/`, aunque cada herramienta mantiene además su carpeta propia (`.claude/` para Claude Code, `.gemini/` para Gemini) mientras el estándar madura.

El speaker también demuestra que es posible crear skills propias usando el plugin "Skill Creator" de Claude Code, sin necesidad de escribirlas manualmente: se describe la habilidad en lenguaje natural y el agente genera el fichero `skill.md` correspondiente.

### Datos y evidencia

- Las skills mejoran los resultados del agente "hasta 10 veces" respecto a un agente generalista (afirmación del speaker, sin fuente externa).
- La skill de **Frontend Design** tiene 165.900 instalaciones en la última semana al momento de grabar el vídeo, y 95.100 estrellas en GitHub.
- La skill de **SEO Audit** tiene 45.300 descargas en la última semana.
- El speaker afirma que existen más de 20.000 habilidades disponibles en el repositorio oficial de agent skills.
- Claude Code (plan Pro) cuesta $X mensuales (el speaker no dice la cifra exacta). Gemini es gratuito con límites.
- La demo genera una landing page completa (HTML + CSS + JS) con un solo prompt usando tres skills (Frontend Design + SEO Audit + Marketing Ideas), obteniendo un resultado que el speaker califica de "espectacular".

### Citas textuales (2-4 máx)

> "Las skills lo que nos permite es justamente atacar a este problema: vamos a darle más contexto, pero solamente en el momento que lo necesite." — Josema Fernández

> "No solamente se trata de darle más contexto, sino hacerlo justamente en el momento en el que lo necesitamos." — Josema Fernández

> "En vez de tener una IA generalista, ahora tenemos un equipo de expertos tanto en diseño como en SEO como en marketing." — Josema Fernández

> "Literalmente con solo ese prompt y las habilidades hemos conseguido este resultado." — Josema Fernández

### Ejemplos concretos

- **Demo principal:** Creación de una landing page para una agencia de IA usando Claude Code + Gemini (Antigravity), con tres skills instaladas simultáneamente. El prompt especifica explícitamente las tres skills a usar (`/frontend-design`, `/seo-audit`, `/marketing-ideas`).
- **Sitio de referencia de skills:** El speaker muestra un repositorio/marketplace de agent skills donde buscar, valorar e instalar habilidades (no menciona URL explícitamente, pero la llama "la página de skills" o "agent skill").
- **Documentación oficial del estándar:** https://agentskills.dev o similar (el speaker no verbaliza la URL, la muestra en pantalla).
- **Skills instaladas en la demo:** `frontend-design`, `seo-audit`, `marketing-ideas` — instaladas vía terminal con el comando de instalación copiado desde el marketplace.
- **Plugin "Skill Creator"** de Claude Code: permite generar una skill nueva desde lenguaje natural. Se accede desde `Manage Plugin` dentro de Claude Code y se invoca con `/skill-creator` en una nueva conversación.
- **Google Drive con recursos gratuitos:** El speaker comparte más de 30 flujos N8N, prompts y plantillas de vibe coding a través de un formulario en la descripción del vídeo (Dominia Academy).

---

## Temas clave

### 1. Agent skills como estándar emergente
Las skills son ficheros .md con nombre, descripción y pasos que convierten a una IA generalista en un especialista. El estándar usa la carpeta `.agents/skills/` como ubicación canónica, compatible con Claude Code, Gemini, Cursor y Open Code. La estructura es: `skill.md` (instrucciones) + opcionalmente `reference/` (documentos de apoyo).

### 2. Carga selectiva de contexto
El mecanismo clave: el agente solo lee la descripción de cada skill (primeras líneas) para decidir si la activa. Solo carga el contenido completo si la descripción encaja con el prompt. Esto resuelve el problema de saturar la ventana de contexto — no se trata de dar más contexto, sino de darlo en el momento preciso.

### 3. Combinación de múltiples skills
La demo muestra cómo tres skills (Frontend Design + SEO Audit + Marketing Ideas) trabajan juntas en un solo prompt para generar una landing page completa. El agente orquesta las tres automáticamente, produciendo un resultado que ninguna skill individual lograría.


**Telegraph:** https://telegra.ph/Claude-Cowork---Build-Your-First-Agent-with-Skills-and-Plugins-03-26
