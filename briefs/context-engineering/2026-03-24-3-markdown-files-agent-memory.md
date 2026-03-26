# 3 Markdown Files Fix AI Agent Memory Forever

- **Fuente:** [https://www.youtube.com/watch?v=1PRgb-0s9V4](https://www.youtube.com/watch?v=1PRgb-0s9V4)
- **Canal:** Deployed-AI
- **Categoría:** context-engineering
- **Duración:** 7min
- **Fecha:** 2026-03-23
- **Score OPENLAB Radar:** 8.2
  - Aplicabilidad: 9
  - Novedad: 8
  - Calidad: 6

---

## Resumen ejecutivo

El vídeo presenta el patrón "Agent Kernel" — una arquitectura de memoria persistente para agentes IA basada en 3 ficheros markdown: un fichero de identidad (quién es el agente), un fichero de memoria (qué ha aprendido), y un fichero de tareas (qué tiene que hacer). Sin base de datos, sin framework, sin dependencias. Solo texto plano.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** El patrón Agent Kernel es una **validación directa** de la arquitectura OPENLAB. Nuestros skills siguen exactamente este principio: SKILL.md (identidad + procedimiento), context/ (memoria/conocimiento), templates/ (formatos de output). Es la misma filosofía con más sofisticación. Refuerza el argumento de que el approach OPENLAB no es artesanal sino un patrón emergente de la industria.
- **Referencias que conectan:** Todos los proyectos OPENLAB usan este patrón. El **Market Due Diligence** tiene SKILL.md (identidad + procedimiento de 7 fases), context/ (criterios del fondo, templates de scoring), y el agente mantiene estado entre fases. El **Observatorio Iberostar** tiene el mismo pattern con contexto de sector hotelero.
- **Capacidades de plataforma:** Claude Code CLI ya soporta memoria persistente entre sesiones (platform-capabilities.md). El Agent Kernel pattern se implementa naturalmente con la estructura de directorios que OPENLAB ya usa. Zero dependencias adicionales.
- **Oportunidades nuevas:** Usar "Agent Kernel" como **concepto pedagógico** en el workshop DIBEX y en presentaciones comerciales. Es una forma simple de explicar qué es un skill OPENLAB: "Son 3 ficheros de texto que convierten a Claude en un especialista de tu proceso."
- **Argumento comercial:** "Un agente sin memoria es un becario que empieza de cero cada día. Nuestros agentes tienen identidad, conocimiento y tareas — todo en ficheros de texto que puedes leer, auditar y modificar."

---

## Contenido detallado

### Ideas y argumentos principales

La tesis central del vídeo es que el problema de amnesia de los agentes IA — el hecho de que cada sesión empieza desde cero, sin memoria de lo que ocurrió antes — no es un inconveniente menor sino un fallo arquitectónico fundamental. Y la solución no requiere infraestructura sofisticada: tres ficheros de texto plano en markdown son suficientes.

El speaker presenta el patrón "Agent Kernel" (proyecto open source de OG's Biljic) estructurado en tres ficheros con responsabilidades claras:

- **agent.md** — identidad del agente: quién es, qué herramientas tiene, cómo debe comportarse. Es la "constitución" del agente. No cambia entre ejecuciones.
- **memory.md** — conocimiento acumulado entre sesiones: preferencias del usuario, hechos descubiertos, decisiones tomadas. El agente lo escribe al aprender algo relevante y lo lee al inicio de cada prompt.
- **state.md** — log operacional en tiempo real: qué está haciendo el agente, en qué paso está, qué decisiones están pendientes. Permite retomar una tarea interrumpida exactamente donde se dejó.

El argumento de fondo es que las soluciones mainstream (vector databases, embedding pipelines, memory frameworks) están sobredimensionadas para la mayoría de casos de uso. Los desarrolladores no necesitan búsqueda semántica sobre diez millones de memorias — necesitan que el agente recuerde lo que hizo ayer. La simplicidad es el punto, no un compromiso.

El speaker también es explícito sobre los límites del patrón: no resuelve coordinación multi-agente (los ficheros no se sincronizan entre agentes paralelos), no escala a historiales muy largos (los ficheros crecen indefinidamente sin poda automática), y no incluye ningún modelo de seguridad (los ficheros son texto plano, sin cifrado ni control de acceso).

Las evoluciones naturales que anticipa: capa de summarización automática para podar memory.md, versionado nativo con Git para auditoría completa, y una capa de sincronización ligera de solo lectura para que un agente líder comparta contexto con agentes trabajadores.

### Datos y evidencia

- El sistema completo son 3 ficheros. Tiempo estimado para comprenderlo completamente: 10 minutos.
- Ejemplo concreto de valor: un agente de investigación que resume 10 papers académicos y se interrumpe tras el paper 7 — sin Agent Kernel reinicia desde el paper 1; con Agent Kernel (via state.md) retoma desde el paper 8. Ahorro de horas en tareas largas.
- El speaker menciona Digital Ocean App Platform como infraestructura de despliegue que gestiona persistencia de ficheros entre reinicios sin capa adicional.

### Citas textuales

> "Every AI agent you've ever built forgets everything the moment a session ends. Every single one." — Speaker

> "It's not magic. It's just a text file being read at the start of every prompt." — Speaker

> "The best solutions often aren't the most technically impressive. They're the ones that understand the actual problem and refuse to overengineer the fix." — Speaker

> "Agent kernel treats that as unacceptable and solves it with the most boring technology imaginable, a text file." — Speaker

### Ejemplos concretos

- **Agent Kernel** — proyecto open source de OG's Biljic. Enlace en la descripción del vídeo (no se verbaliza la URL, solo se indica que está en la descripción).
- **Ejemplo de research agent** — agente que resume papers académicos, usado para ilustrar el valor de state.md en tareas largas con posibles interrupciones.
- **Digital Ocean App Platform** — mencionado como plataforma de despliegue compatible que gestiona la persistencia de ficheros limpiamente.

---

## Temas clave

### 1. Identidad del agente (fichero 1)
Define quién es el agente, su rol, sus capacidades y sus limitaciones. Equivale al SKILL.md de OPENLAB. El punto clave: un agente con identidad clara produce outputs más consistentes que uno con solo instrucciones genéricas.

### 2. Memoria persistente (fichero 2)
El agente acumula conocimiento entre sesiones en un fichero markdown que lee al inicio de cada ejecución. Sin embeddings, sin vector databases — solo texto plano que el LLM lee directamente. Esto es exactamente lo que context/ hace en la arquitectura OPENLAB.

### 3. Zero-dependency como principio de diseño
El patrón funciona sin frameworks, sin bases de datos, sin APIs externas. Solo ficheros de texto. Esto alinea perfectamente con el principio OPENLAB de zero lock-in y portabilidad total.
