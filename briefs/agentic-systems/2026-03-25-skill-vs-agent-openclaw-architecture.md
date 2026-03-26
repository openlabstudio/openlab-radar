# Skill vs Agent: The Architecture That Makes Openclaw Systems Work

- **Fuente:** [https://www.youtube.com/watch?v=BFMkfVSlI8s](https://www.youtube.com/watch?v=BFMkfVSlI8s)
- **Canal:** Zero Team AI
- **Categoría:** agentic-systems
- **Duración:** 7min
- **Fecha:** 2026-03-24
- **Score OPENLAB Radar:** 9.0
  - Aplicabilidad: 9
  - Novedad: 9
  - Calidad: 9

---

## Resumen ejecutivo

Un practicante con 9 agentes CLI en producción durante 3 meses expone la arquitectura que hace que los sistemas multi-agente funcionen de verdad, no en demo. Distingue skill (herramienta) de agent (worker que usa herramientas), define los 4 ficheros que constituyen un agente real, y explica por qué los ficheros markdown superan a las bases de datos vectoriales para memoria de agentes. Todo corriendo en un VPS de $5/mes.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** El framework de 4 ficheros (Identity, Soul, Heartbeat, Memory) es directamente el patrón que OPENLAB puede estandarizar en todos sus deliveries de sistemas agénticos. El "Heartbeat file" — lo que el agente hace proactivamente sin que se lo pidan — es el diferencial entre un chatbot y un sistema real. Este concepto debe entrar en el catálogo de skills de OPENLAB.
- **Referencias que conectan:** El sistema de agentes con schedules en VPS (Scout 9am/8pm, Ops 8am, Mentor 9pm) es análogo a los pilots de inteligencia de mercado continua que OPENLAB puede ofrecer como servicio. El esquema "briefing matutino automático" es exactamente el tipo de entregable que hace visible el valor del sistema al cliente.
- **Capacidades de plataforma:** El "one writer rule" (un agente escribe, muchos leen) es un patrón de gobernanza de contexto que OPENLAB puede incorporar en sus templates de diseño de sistemas multi-agente. Los ficheros compartidos (focus.md, strategy.md) como memoria de equipo es el equivalente al CLAUDE.md de proyecto extendido a múltiples agentes.
- **Oportunidades nuevas:** El dato de benchmark — markdown files (74% accuracy) vs vector databases (68.5%) en LocMo benchmark — es el argumento definitivo para el enfoque zero-infrastructure de OPENLAB. Permite decir a un cliente: "No necesitas Pinecone ni embeddings. Los ficheros markdown son más precisos y más baratos."
- **Argumento comercial:** "Nuestros sistemas multi-agente corren en un servidor de $5/mes, llevan 3 meses en producción, y la memoria en ficheros markdown es más precisa que una base de datos vectorial. Zero lock-in, zero infraestructura propia."

---

## Contenido detallado

### Ideas y argumentos principales

El speaker lleva 3 meses con 9 agentes en producción en un VPS de bajo coste. Su tesis es que la diferencia entre algo que dura un fin de semana y algo que dura meses no es el modelo — es el sistema.

**Por qué fallan la mayoría de setups:** La gente intenta construir un agente con demasiadas herramientas. Un agente con 15 skills es completamente inestable. Pierde contexto, mezcla tareas, alucina. Solución: múltiples agentes narrowos, cada uno focalizado.

**La distinción fundamental:** Una skill es una herramienta. Un agente es un worker que usa herramientas. Lo que hace a algo un agente no son las tools — es el contexto. Cada agente corre en 4 ficheros core:
- **Identity:** qué es responsable de hacer este agente
- **Soul:** cómo comunica — tono, estilo, reglas
- **Heartbeat:** qué hace proactivamente, sin que se lo pidan
- **Memory:** qué recuerda a lo largo del tiempo

Sin estos 4 ficheros, no tienes un agente. Tienes un prompt con herramientas.

**Arquitectura de equipo:** Los agentes son independientes — no hay un agente principal controlando a todos. Pero comparten contexto a través de ficheros compartidos: `focus.md` (prioridades actuales) y `strategy.md` (dirección general). Como un equipo real.

**Miller's Law aplicado a AI:** La memoria de trabajo humana gestiona 7±2 elementos. Para sistemas AI, el patrón es similar: un agente con demasiadas tools falla. Múltiples agentes narrowos funcionan como un equipo.

**Memoria: ficheros primero.** La recomendación es explícita: empieza con ficheros markdown simples. Los agentes los leen. Los agentes los escriben. Sin tools, sin integraciones. Solo ficheros. Fue suficiente para el primer mes. Los agentes recuerdan contexto, decisiones, conversaciones de hace una semana — no porque tengan buena memoria, sino porque leen esos ficheros en cada arranque.

**One writer rule:** Un agente escribe a un fichero, muchos pueden leer. Si rompes esta regla, los agentes se sobreescriben entre sí. Zero conflictos, zero problemas de coordinación.

**Benchmark que cambia el argumento:** LocMo benchmark: ficheros markdown plain = 74% de accuracy. Vector databases = 68.5%. Los modelos de AI fueron entrenados en miles de millones de ficheros de texto. Leer texto es su entorno natural. Luchar contra eso con APIs de vectores especializadas es nadar contra la corriente.

### Datos y evidencia

- 9 agentes en producción durante 3 meses en VPS de $5/mes
- 1 agente con 15 skills = completamente inestable
- LocMo benchmark: markdown files 74% accuracy vs vector DBs 68.5%
- VPS hardening básico: 30 minutos (SSH keys, firewall, fail2ban)
- 3 meses de uptime, cero incidentes de seguridad
- Scout corre 2 veces al día (9am, 8pm), monitoriza 14 cuentas en X
- Ops: brief matutino 8am + sync vespertino 6:30pm
- Mentor: review diario 9pm

### Citas textuales

> "The difference between something that works for the weekend and something that works for months — it's not the model, it's the system." — Speaker

> "Without this, you don't have an agent. You have a prompt with tools." — Speaker (sobre los 4 ficheros core)

> "Every morning I wake up to a brief that scouts and ops already wrote overnight. I didn't ask for it. It just happens. That's the difference between a chatbot and a system." — Speaker

> "Files scored 74% accuracy. Vector databases only 68.5%. AI models were trained on billions of text files. Reading text is their natural environment." — Speaker

### Ejemplos concretos

- **Scout agent:** monitoriza 14 cuentas en X, escanea señales de mercado, almacena en knowledge base compartida. Cron jobs a las 9am y 8pm.
- **Ops agent:** brief matutino (8am) + sync vespertino (6:30pm). "Chief of staff que nunca olvida."
- **Mentor agent:** review diario a las 9pm. "Brutalmente honesto. La semana pasada preguntó por qué cambié prioridades 4 veces."
- **Chief agent:** Lee focus.md, decide qué es urgente, establece dirección.
- **Heartbeat file:** agentes que despiertan cada 30 minutos solos. Comprueban si cron jobs siguen vivos, escriben status updates, promueven aprendizajes a memoria long-term.
- **Entornos dedicados:** cada agente tiene su propio email, sus propios canales. No usar cuentas personales.

---

## Temas clave

### 1. El Heartbeat File como diferencial de un agente real

El heartbeat no es un prompt — es un fichero que define qué hace el agente cuando no se lo piden. Agentes que actúan proactivamente (monitors, briefings, revisiones) son cualitativamente distintos de los que solo responden. Este concepto es el eje de lo que OPENLAB llama "inteligencia continua."

### 2. One Writer Rule para gobernanza de memoria compartida

La regla más simple y poderosa para sistemas multi-agente con memoria compartida: un solo agente tiene permiso de escritura por fichero. Muchos pueden leer. Esta restricción elimina el principal punto de fallo en arquitecturas multi-agente. Implementarla requiere diseño previo de qué agente "posee" cada fichero de memoria.

### 3. VPS como infraestructura zero-drama para CLI agents

Laptop = muere cuando duermes. VPS de $5/mes = 24/7, separación del entorno de trabajo, cron jobs independientes. La inversión en seguridad es de 30 minutos (SSH keys + firewall + fail2ban). Argumento para el cliente: es más barato que cualquier plataforma SaaS de automatización y sin vendor lock-in.


**Telegraph:** https://telegra.ph/Skill-vs-Agent-The-Architecture-That-Makes-Openclaw-Systems-Work-03-25
