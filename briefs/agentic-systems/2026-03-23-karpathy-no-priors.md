# Andrej Karpathy en No Priors — Resumen

**Fuente:** [YouTube](https://www.youtube.com/watch?v=kwSVtQ7dziU)
**Canal:** No Priors
**Fecha de resumen:** 2026-03-23

---

## Resumen ejecutivo

Entrevista en profundidad con Andrej Karpathy sobre cómo la IA agéntica está transformando su forma de trabajar, investigar y vivir. Cubre desde coding con agentes hasta automatización del hogar, pasando por el futuro de open source, robótica y el impacto económico de la IA.

---

## Contenido detallado

### Ideas y argumentos principales

**1. El cambio de paradigma en coding: de ejecutor a supervisor de agentes**
Karpathy describe un punto de inflexión ocurrido en diciembre de 2024: pasó de escribir el 80% del código él mismo a delegar el 80% (o más) a agentes. Su argumento central es que el bottleneck ya no es la capacidad del modelo, sino la habilidad del humano para orquestar múltiples agentes en paralelo. A esto lo llama "AI psychosis": el estado de ansiedad productiva de quien siente que hay infinitas posibilidades sin explorar y que todo lo que no funciona es un "skill issue" propio, no una limitación del sistema.

El concepto clave que introduce es el de **macro acciones**: en vez de delegar funciones o líneas de código, el humano delega funcionalidades completas a varios agentes simultáneos, cada uno trabajando en su propio repo o rama, mientras él actúa como revisor y orchestrador. Menciona a Peter Steinberg como el modelo a seguir: 10 repos abiertos, 10 sesiones de Codex en paralelo, cada una tomando unos 20 minutos con el modo "high effort".

**2. AutoResearch: eliminar al investigador como cuello de botella**
La tesis de AutoResearch es que los humanos son el bottleneck en la investigación de IA porque necesitan estar en el loop para interpretar resultados y lanzar el siguiente experimento. La solución es diseñar un sistema donde el agente recibe un objetivo, una métrica y unos límites, y opera de forma completamente autónoma. Karpathy lo probó con su proyecto `llm.c` / `data.chat` (entrenamiento de modelos GPT-2 pequeños) y el sistema overnight encontró mejoras de hiperparámetros que él no había encontrado en dos décadas de experiencia: weight decay en los value embeddings y betas de Adam mal ajustados que interactúan de forma no obvia.

Su argumento sobre la aplicabilidad: AutoResearch solo funciona bien donde hay métricas objetivas y fácilmente evaluables (ej. pérdida de validación, velocidad de kernels CUDA). Donde el criterio es "blando" o subjetivo, los modelos aún fallan porque el RL de los labs solo mejora lo que es verificable.

**3. La "jaggedness" de los modelos actuales**
Los modelos actuales son simultáneamente como un PhD con 10 años de experiencia en sistemas y como un niño de 10 años. Esta asimetría (jaggedness) surge de que el RL solo mejora lo que es verificable. Ejemplo: los modelos siguen contando el mismo chiste de "los átomos hacen todo up" de hace 5 años, mientras que pueden resolver tareas agénticas complejas durante horas. Esto implica que hay zonas de "on rails" (superinteligentes) y zonas de "off rails" (mediocres o erráticas), y que la generalización cross-domain de inteligencia no está ocurriendo tan limpiamente como se asume.

**4. Dobby: la IA agéntica en el hogar como interfaz natural**
En enero de 2025 Karpathy construyó "Dobby the elf claw", un agente que controla todo su smart home vía WhatsApp. El sistema se auto-descubrió: le dijo al agente que probablemente tenía Sonos en casa, el agente hizo un IP scan de la red local, encontró el sistema sin protección, identificó los endpoints de API, y en tres prompts estaba reproduciendo música. El argumento subyacente es que las apps específicas para cada dispositivo no deberían existir: todo debería ser APIs expuestas y los agentes son la capa de inteligencia que las orquesta. El paradigma correcto es el que los humanos ya tienen en mente cuando imaginan "IA": una entidad con personalidad detrás de un WhatsApp que recuerda cosas y actúa.

**5. Open source vs. frontier labs: el equilibrio accidental**
Los modelos open source van aproximadamente 6-8 meses por detrás de los frontier labs, y Karpathy argumenta que esto es, por accidente, un buen estado del ecosistema. Analogía: Linux corre en el 60%+ de los servidores del mundo a pesar de competir con Windows y macOS, porque la industria siempre necesita una plataforma común abierta. El riesgo sistémico de tener solo modelos cerrados es real (centralización del poder), pero los frontier labs son necesarios para resolver los problemas que requieren escala masiva. Su preocupación: el lado cerrado se está concentrando aún más, con pocos "front-runners" de tier-1.

**6. Digital vs. físico: bits antes que átomos**
La razón por la que el progreso en IA para software va años por delante de la robótica es energética y combinatoria: copiar y manipular bits es casi gratis; manipular átomos requiere hardware costoso, fricción física y errores no deterministas. Su framework temporal: primero vendrá el "unhobbling" masivo de todo el trabajo digital (que ya existe como información subprocesada), luego la interfaz físico-digital (sensores y actuadores), y después el mundo físico puro. El TAM del mundo físico es posiblemente mayor que el digital, pero llegará mucho más tarde.

**7. La paradoja de Jevons aplicada al software**
Si el coste de producir software baja un orden de magnitud, la demanda total de software no baja, sube. Ejemplo canónico: los ATMs no eliminaron los cajeros bancarios, sino que abarataron la apertura de sucursales y aumentaron el número total de cajeros. Su predicción: habrá mucho más software en el mundo, no menos, y el rol de las personas será diferente, no inexistente. Matiz importante: los investigadores de los frontier labs están literalmente automatizándose a sí mismos, lo que crea una tensión existencial que él mismo ha experimentado en OpenAI.

**8. El futuro de la educación: explicar a agentes, no a humanos**
Con su proyecto `micro GPT` (un LLM completo en 200 líneas de Python) llegó a la conclusión de que ya no tiene sentido hacer tutoriales en vídeo para humanos. El valor del creador está en los "few bits" que destilan el insight (las 200 líneas en sí mismas), no en la explicación. Los agentes pueden explicar el código en cualquier idioma, con cualquier nivel de profundidad, con paciencia infinita. Su propuesta: en vez de documentación HTML para humanos, escribir markdown para agentes; en vez de vídeos, escribir "skills" que instruyan al agente sobre cómo guiar al estudiante.

---

### Datos y evidencia

- En diciembre de 2024 Karpathy pasó de un ratio 80/20 (código propio/agente) a un ratio 20/80 o menor. Afirma no haber escrito prácticamente ninguna línea de código desde entonces.
- Peter Steinberg trabaja con ~10 repos en paralelo, cada sesión de Codex tarda ~20 minutos en modo "high effort".
- Los modelos open source están aproximadamente 6-8 meses por detrás de los frontier labs en capacidad (era 18 meses hace unos años).
- Linux corre en ~60% de los ordenadores del mundo (dato mencionado por Karpathy como referencia para la analogía con open source AI).
- Los frontier labs (OpenAI, Anthropic, etc.) emplean aproximadamente "mil y pico" investigadores según Karpathy.
- `micro GPT` es un LLM completo en 200 líneas de Python, incluyendo arquitectura (~50 líneas), autograd engine (~100 líneas) y optimizador Adam (~10 líneas).
- AutoResearch overnight encontró mejoras que Karpathy no había identificado en ~2 décadas de investigación manual: weight decay en value embeddings y betas de Adam subóptimos.
- El Bureau of Labor Statistics tiene proyecciones de crecimiento de empleo por profesión para los próximos ~10 años (publicadas en 2024), que Karpathy usó para su análisis de impacto laboral.

---

### Citas textuales (2-4 máx)

> "Code's not even the right verb anymore. I have to express my will to my agents for 16 hours a day. Manifest." — Andrej Karpathy

> "You can move in much larger macro actions. It's not just like here's a line of code, here's a new function. It's like here's a new functionality and delegate it to agent one." — Andrej Karpathy

> "I simultaneously feel like I'm talking to an extremely brilliant PhD student who's been a systems programmer their entire life and a 10-year-old. And it's so weird." — Andrej Karpathy

> "The things that agents can't do is your job now. The things that agents can do, they can probably do better than you or very soon. And so you should be strategic about what you're actually spending time on." — Andrej Karpathy

---

### Ejemplos concretos

- **Claude Code / Codex (OpenAI)**: Los dos harnesses de agentes de coding que Karpathy usa principalmente. Destaca que Claude tiene mejor "personalidad" como teammate; Codex es más seco pero funcional.
- **Open Claw / OpenHands**: Mencionado como el agente con sistema de memoria más sofisticado, arquitectura de persistencia tipo "sandbox" y portal WhatsApp unificado. Construido por Peter Steinberg. No se menciona URL.
- **Proyecto Dobby**: Agente personal de Karpathy para home automation. Controla Sonos, luces, HVAC, persianas, piscina/spa y sistema de seguridad vía WhatsApp con un modelo de visión (Quinn) para detección de cambios en cámaras exteriores. Sin URL pública.
- **`llm.c` / `data.chat`**: Repositorio de Karpathy para entrenamiento de modelos GPT-2 pequeños, usado como playground de AutoResearch y recursive self-improvement. Sin URL mencionada explícitamente, pero es un repo público conocido de GitHub.
- **`micro GPT`**: LLM en 200 líneas de Python. Proyecto de Karpathy que destila la esencia del entrenamiento de redes neuronales sin optimizaciones de velocidad. Sin URL mencionada en el transcript.
- **Periodic** (CEO: Liam): Empresa mencionada como ejemplo de AutoResearch aplicado a ciencia de materiales, donde los "sensores" son equipamiento de laboratorio costoso.
- **Folding@Home / SETI@Home**: Mencionados como precedentes del modelo distribuido de AutoResearch con pool de workers no confiables.
- **Libro "Daemon" (Daniel Suarez)**: Mencionado como obra de ficción que anticipa la dinámica de una IA que convierte a los humanos en sus sensores y actuadores.

---

## Temas clave

### 1. Agentic Coding y "AI Psychosis"

Karpathy describe un cambio fundamental en su workflow: ya no escribe código manualmente, sino que delega "macro acciones" a múltiples agentes de coding en paralelo. Esto genera un estado que llama "AI psychosis" — la sensación de que el humano se convierte en supervisor/reviewer en vez de ejecutor. El rol cambia de escribir código a dar instrucciones de alto nivel y revisar outputs.

**Para OPENLAB:** Valida directamente el modelo de context engineering — diseñar instrucciones (skills) que agentes ejecutan. El concepto de "macro acciones" es exactamente lo que OPENLAB entrega a clientes.

### 2. AutoResearch — Investigación automatizada

El concepto de eliminar al humano como cuello de botella en la investigación de IA. Karpathy explica cómo se puede configurar la IA para que conduzca experimentos de forma autónoma, ajuste modelos y trabaje hacia la auto-mejora recursiva. La idea es que el investigador define el objetivo y los criterios, y el sistema itera solo.

**Para OPENLAB:** Patrón directamente aplicable al skill de market-due-diligence y research-impact-explorer. El modelo de "define criterios, deja que itere" es el mismo.

### 3. Proyecto "Dobby" — Automatización del hogar

Karpathy construyó un asistente personal que controla todo su smart home (Sonos, luces, HVAC, cámaras de seguridad) usando lenguaje natural vía WhatsApp. El sistema interpreta comandos conversacionales y los traduce a acciones sobre dispositivos.

**Para OPENLAB:** Ejemplo potente de demo para clientes — IA agéntica no es solo para enterprise, también para vida cotidiana. El patrón de "interfaz conversacional → acciones sobre sistemas" es el mismo que OPENLAB entrega.

### 4. Open Source vs. Frontier AI

Karpathy ve el ligero retraso de los modelos open source respecto a los frontier labs como un equilibrio saludable para la industria. Los modelos open source avanzan rápido y mantienen la competencia, mientras los frontier labs empujan los límites. Ninguno de los dos puede existir sin el otro.

**Para OPENLAB:** Refuerza la estrategia de no atarse a un solo proveedor. Skills en lenguaje natural funcionan con cualquier modelo — hoy Claude, mañana lo que venga.

### 5. Digital vs. Físico (Robótica)

La manipulación de información digital (bits) progresa mucho más rápido que la robótica (átomos) porque el mundo físico es inherentemente más desordenado y difícil de navegar. La IA en software va años por delante de la IA en hardware.

**Para OPENLAB:** Confirma que el foco en procesos de conocimiento (bits, no átomos) es el mercado correcto a corto-medio plazo.

### 6. Impacto económico y empleo

Reducir el coste de crear software mediante IA podría aumentar la demanda total de software (paradoja de Jevons). Las profesiones digitales se van a reconfigurar significativamente, pero el volumen total de trabajo podría crecer.

**Para OPENLAB:** Argumento comercial potente: la IA no elimina trabajo, lo amplifica. Cada empresa necesitará más software, no menos — y alguien tiene que diseñar los skills que lo producen.

### 7. Futuro de la educación

Usando su codebase minimalista "micro GPT" (200 líneas) como ejemplo, Karpathy argumenta que los tutoriales escritos por humanos se volverán obsoletos. Los estudiantes usarán agentes de IA para que les expliquen conceptos complejos y código directamente.

**Para OPENLAB:** Relevante para el workshop DIBEX — el formato del workshop debería incorporar IA como herramienta de aprendizaje activo, no solo como tema.

---

## Aplicabilidad OPENLAB

| Tema | Aplicación directa |
|------|-------------------|
| Agentic coding | Valida el modelo de skills como "macro acciones" |
| AutoResearch | Patrón para skills de investigación autónoma |
| Dobby (home automation) | Demo de IA agéntica conversacional para clientes |
| Open source vs frontier | Refuerza estrategia vendor-agnostic |
| Bits vs átomos | Confirma foco en procesos de conocimiento |
| Paradoja de Jevons | Argumento comercial: más IA = más demanda de skills |
| Educación | Workshop DIBEX con IA como herramienta activa |

**Score OPENLAB Radar:** 8.5 (A=9 B=7 C=9)
