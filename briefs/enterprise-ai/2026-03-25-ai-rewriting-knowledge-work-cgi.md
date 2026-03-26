# How AI Is Rewriting the Rules of Knowledge Work

- **Fuente:** [https://www.youtube.com/watch?v=6u4nv4CeiNo](https://www.youtube.com/watch?v=6u4nv4CeiNo)
- **Canal:** Intercept (ChatB2B podcast)
- **Categoría:** enterprise-ai
- **Duración:** 38min
- **Fecha:** 2026-03-24
- **Score OPENLAB Radar:** 7.7
  - Aplicabilidad: 8
  - Novedad: 7
  - Calidad: 8

---

## Resumen ejecutivo

Entrevista con el director de marketing de CGI, firma global de consultoría con ~100,000 empleados. Explica cómo AI está pasando de herramienta de productividad individual a palanca de transformación organizacional. Distingue "single player mode" (co-pilot, 10-20% mejora) de "multiplayer mode" (sistemas agénticos, potencial 10x). Documenta casos reales en producción: proposal generator que entrega 60-70% de borrador de RFPs, deal qualification agent, y NotebookLM como base de conocimiento de marketing.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** El caso del proposal generator (RFP → 60-70% borrador + referencias + capacidades) es exactamente el tipo de pilot de alto ROI que OPENLAB puede replicar en firmas de consultoría y servicios profesionales. El deal qualification agent (análisis de RFP para decidir si pujar o no) es otro pilot de bajo riesgo y alto impacto.
- **Referencias que conectan:** La frase "tardamos 2 años desde ChatGPT hasta empezar a hacer prompt engineering bien" valida la propuesta de OPENLAB de acortar esa curva de adopción. Sin guía externa, las grandes organizaciones tardan años en llegar a donde OPENLAB puede llevarlas en meses.
- **Capacidades de plataforma:** El uso de NotebookLM como base de conocimiento de marketing (1000 case studies → un solo punto de consulta) replica el patrón que OPENLAB ya documenta en su skill de notebooklm. CGI lo está haciendo con miles de documentos de capacidades y pensamiento de liderazgo.
- **Oportunidades nuevas:** El framing "single player (10-20%) vs multiplayer (10x)" es el mejor argumento para vender el salto de co-pilot a CLI agents. OPENLAB puede usar esta terminología directamente en el pitch: "estás en single player mode — vamos a pasar a multiplayer."
- **Argumento comercial:** "CGI, con 100,000 empleados y dos años de ventaja, acaba de empezar a tener su primer agente en producción. Nosotros podemos llevarte al mismo punto en semanas, no en años."

---

## Contenido detallado

### Ideas y argumentos principales

Mahadev Sastri lleva marketing en CGI y tiene un background técnico (programador → delivery → marketing leadership). Su perspectiva es que marketing en servicios profesionales ha sido históricamente reactivo, no porque los marketers no sepan estrategizar, sino porque los recursos siempre están comprometidos.

**AI como palanca de transformación (no solo productividad):** La distinción no es semántica. Productividad = hacer lo mismo más rápido (10-20%). Transformación = cambiar qué hace el equipo y cómo crea valor (10x). La pregunta es si estás cambiando la función (qué haces) o la forma (por qué existes). CGI hoy está mayormente cambiando la función.

**Single player vs multiplayer mode:**
- **Single player:** un co-pilot por empleado. M365 Copilot, ChatGPT personal. Mejoras del 20-25% en tareas individuales (summarización, investigación, redacción). Todo el mundo está aquí hoy.
- **Multiplayer:** sistemas agénticos orquestados. Workflows que dan potencia a equipos y departamentos. El "10x" real. Requiere confianza, compliance, y arquitectura. CGI está en los primeros pasos.

**Casos reales en producción en CGI:**
1. **Proposal generator:** Input = RFP. El sistema accede a las capacidades de CGI, extrae referencias, y produce un primer borrador del 60-70% de calidad. Humanos expertos revisan y completan. Human-in-the-loop como estándar.
2. **Deal qualification agent:** En el momento en que llega una RFP, el sistema analiza si CGI debe pujar o no. Accede a múltiples sistemas para hacer el análisis. Decision support, no decisión autónoma.
3. **NotebookLM como knowledge base:** En vez de 1000 case studies y documentos de thought leadership dispersos, una sola interfaz conversacional. El equipo pregunta "¿qué diferenciadores tenemos en banca?" y obtiene respuesta inmediata.
4. **Custom GPT para AI messaging:** Un business unit creó un GPT con las instrucciones de messaging de AI para asegurar consistencia entre equipos de business development. El GPT se usa en propuestas y reuniones de cliente.

**Por qué la adopción de agentes es lenta en enterprise:**
- Confianza: se tarda en confiar en un agente como confiarías en un humano
- Regulación: clientes en sectores regulados (finanzas, gobierno) tienen restricciones on-premise
- Compliance: datos sensibles no pueden ir a la nube
- Dos años desde ChatGPT → prompt engineering bien hecho → custom GPTs → primeros agentes. Esta es la curva real.

**El trust building como proceso obligatorio:** "Igual que con los humanos, la confianza se construye con el tiempo." Los sistemas agénticos multi-orquestados son el futuro, pero requieren demostrar valor primero con un agente, luego con dos, luego con el sistema.

### Datos y evidencia

- CGI: ~100,000 empleados globales, uno de los mayores system integrators del mundo
- Mejoras actuales en tareas individuales: mínimo 20-25%
- Proposal generator: 60-70% del primer borrador automatizado
- Tiempo de adopción en enterprise: ~2 años desde ChatGPT hasta primeros agentes en producción
- Single player mode: 10-20% mejora. Multiplayer mode: potencial 10x (1,000% mejora)

### Citas textuales

> "The reality is that to adopt agents at an enterprise level, you need a lot of trust. It's taken us like two years since ChatGPT was launched to even start prompt engineering in a proper way." — Mahadev Sastri

> "To get to the thousand percent or 10x benefit and creating agentic systems — let's take a step back, let's talk about just agents itself. Even having one agent, if we have a use case where deploying one agent will be a door opener." — Mahadev Sastri

> "Instead of looking at a knowledge base with like a thousand different case studies... now that's like one go-to place for that industry and then you just ask 'what do we do in that, what's our capability, what's our differentiator.'" — Mahadev Sastri

### Ejemplos concretos

- **NotebookLM en marketing de servicios profesionales:** 1000+ documentos de capacidades, case studies y thought leadership → interfaz conversacional por vertical de industria
- **Proposal generator CGI:** RFP como input → agente que cruza capacidades + referencias + histórico → 60-70% de borrador → revisión experta humana
- **Deal qualification:** llegada de RFP → agente analiza múltiples sistemas → recomendación de pujar o no → humanos deciden

---

## Temas clave

### 1. El "multiplayer mode" como argumento de venta de sistemas agénticos

El framing de Andrew (host) — single player (co-pilot) vs multiplayer (agentic systems) — es la mejor síntesis de la propuesta de valor de CLI agents sobre co-pilots genéricos. Single player = 10-20%. Multiplayer = 10x. La pregunta para un cliente no es "¿usas AI?" sino "¿estás en single player o multiplayer?"

### 2. Human-in-the-loop como condición de confianza en enterprise

Todos los casos de CGI tienen explícitamente humanos en el loop: expertos que revisan el borrador, equipos que validan la recomendación de deal qualification. No es una limitación técnica — es la estrategia de adopción. La autonomía del agente crece a medida que crece la confianza. OPENLAB puede usar esto para posicionar pilots: "empezamos con human-in-the-loop y escalamos a partir de ahí."

### 3. La curva de 2 años como argumento para el guía externo

CGI tardó 2 años desde ChatGPT hasta tener su primer agente en producción. Sin guía externa, esa es la curva real de las grandes organizaciones. OPENLAB puede comprimir esa curva radicalmente porque ya ha recorrido el camino. El argumento comercial no es "tenemos la tecnología" — es "tenemos la experiencia de la curva."


**Telegraph:** https://telegra.ph/How-AI-Is-Rewriting-the-Rules-of-Knowledge-Work-03-25
