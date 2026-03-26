# Claude's 1M Context Window and Multi-Agent Team Architecture

- **Fuente:** [https://www.youtube.com/watch?v=rngDEBQuhM0](https://www.youtube.com/watch?v=rngDEBQuhM0)
- **Canal:** Mat Siems
- **Categoría:** agentic-systems
- **Duración:** 7min
- **Fecha:** 2026-03-24
- **Score OPENLAB Radar:** 7.8
  - Aplicabilidad: 8
  - Novedad: 8
  - Calidad: 7

---

## Resumen ejecutivo

Arquitectura de "boardroom" con agentes adversariales especializados para toma de decisiones estratégicas. Un custom harness rechaza prompts conversacionales y exige un template estructurado con 4 parámetros obligatorios. El 1M token context window hace viable que múltiples agentes compartan ficheros masivos de expertise simultáneamente. Hard-coded compute budgets evitan loops infinitos y fuerzan el output a un memo ejecutivo estructurado.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** El patrón "boardroom adversarial" es el esqueleto de un pilot de due diligence o análisis estratégico de alto valor. OPENLAB puede entregar este sistema como producto: el cliente aporta el brief (contexto, stakes, restricciones, preguntas clave) y el sistema produce un memo ejecutivo con tensiones resueltas y sin resolver. Es el tipo de entregable que justifica fees de consultoría senior.
- **Referencias que conectan:** El concepto de "agentic engineering" (construir los sistemas que construyen los sistemas) es la definición exacta de lo que OPENLAB hace — no código, no plataformas, sino arquitecturas de contexto en lenguaje natural que orquestan agentes especializados.
- **Capacidades de plataforma:** El 1M context window de Claude (Opus/Sonnet) elimina el incentivo de comprimir contexto y permite que cada agente del boardroom cargue ficheros completos de expertise sin degradación de rendimiento. El stack Claude Code + markdown files de OPENLAB ya está posicionado para aprovechar esto.
- **Oportunidades nuevas:** El "outlier persona" (moonshot agent) que rechaza explícitamente las apuestas seguras e incremetales es un rol de abogado del diablo que OPENLAB podría incluir en cualquier proceso de análisis estratégico para un cliente. Añade un criterio de robustez al output que los procesos humanos rara vez tienen.
- **Argumento comercial:** "No es un chatbot que responde preguntas. Es un boardroom de agentes especializados que debaten entre sí para encontrar los agujeros en tu estrategia antes de que lo haga el mercado."

---

## Contenido detallado

### Ideas y argumentos principales

El vídeo parte de un memo ejecutivo real (empresa Blendstack, oferta de adquisición de $12M) para demostrar el nivel de calidad posible con arquitectura de agentes adversariales. El argumento central: los interfaces conversacionales están limitados por diseño — la ventana abierta sin restricciones genera el output estadísticamente más probable (genérico). Para obtener outputs de nivel ejecutivo, hay que construir sistemas con restricciones estructurales.

**Los 3 pilares de la arquitectura:**

1. **Custom Agent Harness:** Wrapper de software que controla inputs, outputs y lógica de ejecución nativamente. Rechaza prompts conversacionales — si el operador intenta chatear, el código no ejecuta. Exige un template de input estricto (el "brief") con 4 parámetros obligatorios: **context** (qué está pasando), **stakes** (qué está en juego), **constraints** (restricciones explícitas), **key questions** (qué debe resolver el sistema). Falta cualquier parámetro → el fichero es rechazado antes de arrancar. Hard-coded financial y temporal constraints: un límite de compute budget por decisión que detiene la deliberación una vez alcanzado.

2. **1M Token Context Window:** Elimina el incentivo de comprimir datos. Cada board member node puede cargar ficheros masivos de expertise (métricas de negocio, overviews de producto, histórico de decisiones) sin degradación de rendimiento. El paper de LocMo exige retención fidedigna más allá de los 250,000 tokens. El pricing flat para el contexto completo cambia fundamentalmente el diseño arquitectónico.

3. **Adversarial Orchestration:** El CEO node recibe el brief y lo distribuye en paralelo a los board member nodes. Cada agente procesa independientemente, formando su opinión sin bloquearse entre sí. Cada board member tiene un system prompt único que define su sesgo:
   - Revenue agent: prioriza cash collection en 90 días
   - Compounder agent: solo se fija en ventajas competitivas multi-año
   - Moonshot agent: rechaza explícitamente las apuestas seguras e incrementales — está programado para abogar por riesgos que definen categorías

   Los agentes mantienen ficheros de expertise que registran los sesgos, compromisos y argumentos históricos de los otros agentes del board. El conflicto expone los agujeros en el brief original.

**Hard stop y síntesis:** Cuando el compute budget se agota o el tiempo límite se alcanza, el harness inyecta un comando de stop al bucle. El CEO node ejecuta el protocolo final: closing statements de cada board member, síntesis de tensiones resueltas y sin resolver, output del memo ejecutivo en markdown.

**Escalabilidad del patrón:** Como usa lógica estructural (no contenido específico), el mismo boardroom sirve para cualquier crisis. Carta de la FDA → nuevo brief → mismo sistema.

**"Agentic Engineering" como disciplina:** La progresión es: prompt engineering → agentic coding → agentic engineering. El desarrollo moderno cada vez más implica construir los sistemas que construyen los sistemas. La alta palanca está en diseñar los equipos ejecutivos digitales, no en escribir código.

### Datos y evidencia

- Demo: memo ejecutivo de Blendstack — oferta de adquisición $12M, voto del board 5-1, $1.5M retention earnout, dissenso documentado con 5 argumentos de deceleración de crecimiento
- 1M token context window en Claude Opus y Sonnet (pricing flat para el contexto completo)
- Retención fidedigna requerida más allá de 250,000 tokens según benchmark LocMo
- Compute budgets en dólares por decisión (hard-coded, no configurable en runtime)

### Citas textuales

> "Relying on these out-of-the-box platforms traps engineers in a normal distribution of average AI outputs. When the system has no structural constraints, it generates the most statistically likely generic response." — Speaker

> "The harness explicitly rejects conversational prompts. If an operator tries to chat with it, the code won't execute." — Speaker

> "Modern development increasingly involves building the systems that build the systems. High leverage AI utilization prioritizes architecting the digital executive teams that specify exactly what needs to be built." — Speaker

### Ejemplos concretos

- **Brief de Blendstack:** Template con 4 parámetros → CEO node → 5 board member nodes en paralelo → debate adversarial → hard stop por budget → memo ejecutivo final
- **Moonshot agent:** system prompt que instruye explícitamente a rechazar apuestas seguras e incrementales y abogar por riesgos que definen categorías
- **Crisis scaling:** carta de la FDA como ejemplo de re-uso del boardroom con nuevo brief pero misma arquitectura
- **Extensión PI:** mencionada como harness nativo que parsea front matter de ficheros markdown para configuración pre-boot

---

## Temas clave

### 1. Template de input obligatorio como control de calidad upstream

El harness rechaza prompts sin los 4 parámetros (context, stakes, constraints, key questions). Esto fuerza al operador a clarificar su lógica antes de gastar compute. El 80% de los outputs mediocres de AI no son culpa del modelo — son culpa de un brief sin estructura. Esta arquitectura elimina el problema en origen.

### 2. Adversarial orchestration como stress test de estrategia

Los agentes están diseñados explícitamente para desacordar entre sí. El "moonshot agent" tiene instrucciones de rechazar lo seguro. El resultado no es un consenso sino un mapa de tensiones — cuáles se resolvieron, cuáles permanecen abiertas. Es más valioso que un output convergente para decisiones estratégicas de alto stakes.

### 3. Compute budgets como mecanismo anti-loop

Los bucles de deliberación multi-agente sin restricción temporal son el principal punto de fallo en producción. La solución del speaker es hard-code un presupuesto de compute en dólares por decisión. El agente sabe cuánto puede gastar antes de arrancar. Cuando se agota, el CEO node ejecuta el protocolo de cierre forzado.


**Telegraph:** https://telegra.ph/Claudes-1M-Context-Window-and-Multi-Agent-Team-Architecture-03-25
