# Claude Code SKILLS.md are a token trap.

- **Fuente:** [https://www.youtube.com/watch?v=pBK7RjrtCPw](https://www.youtube.com/watch?v=pBK7RjrtCPw)
- **Canal:** Tim Carambat
- **Categoría:** context-engineering
- **Duración:** 19min
- **Fecha:** 2026-03-23
- **Score OPENLAB Radar:** 8.2
  - Aplicabilidad: 8
  - Novedad: 9
  - Calidad: 7

---

## Resumen ejecutivo

Tim Carambat (creador de AnythingLLM) argumenta que los ficheros SKILLS.md en Claude Code son intencionalmente un "dark pattern" que infla el consumo de tokens. Su tesis: cada skill se carga en el contexto completo en cada invocación, multiplicando el coste sin que el usuario sea consciente. Propone alternativas más eficientes como carga bajo demanda y herramientas externas que no contaminen la ventana de contexto.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** Este vídeo es una **amenaza narrativa** que OPENLAB debe saber contestar. Nuestro negocio se basa en skills .md complejos (>8K chars). Si la narrativa "skills = token trap" se extiende, clientes potenciales podrían cuestionar el approach. Pero también refuerza nuestro diferenciador: OPENLAB usa **progressive disclosure** (carga dinámica de contexto según necesidad), no carga monolítica. Esto es exactamente lo que Carambat dice que falta.
- **Referencias que conectan:** El agente de **Market Due Diligence** (7 fases) es un buen contra-ejemplo: cada fase carga solo el contexto que necesita, no el skill completo. El coste por ejecución es predecible y el ROI (de días a horas) justifica ampliamente el consumo de tokens.
- **Capacidades de plataforma:** Claude Code CLI ya soporta progressive disclosure (documentado en platform-capabilities.md). La arquitectura OPENLAB con `context/` separado del `SKILL.md` principal es precisamente el patrón que mitiga la objeción de Carambat: el contexto pesado (fuentes, templates, referencias) se carga solo cuando la fase lo requiere.
- **Oportunidades nuevas:** Preparar un **one-pager de respuesta** a la objeción "token trap" para el equipo comercial. Incluir: cómo funciona progressive disclosure, coste real por ejecución vs. valor entregado, comparación con alternativas (Custom GPTs con 8K de límite vs. skills OPENLAB con 50K+ de precisión).
- **Argumento comercial:** "Sí, nuestros skills consumen más tokens que un prompt simple. También un informe de McKinsey cuesta más que una búsqueda en Google. La pregunta no es cuántos tokens usas, sino cuánto vale el output."

---

## Contenido detallado

### Ideas y argumentos principales

**1. Los SKILLS.md son simplemente system prompts con mejor marketing.** Carambat abre el vídeo desmontando la narrativa: los ficheros markdown son ficheros de texto, nada más. La industria los ha reempaquetado como un "nuevo paradigma" pero son system prompts de toda la vida. Lo compara con el ciclo del "prompt engineer" de 2023: misma tecnología, PR diferente.

**2. El token trap es intencional, no accidental.** Su tesis central es que los grandes players (Anthropic, OpenAI, NVIDIA) tienen un incentivo estructural para que los usuarios inflen sus ventanas de contexto. Los skills pesados, la carga acumulativa de herramientas, el historial de chat que nunca se limpia: todo se acumula. Cuando el modelo llega al límite y comprime su propio contexto, eso también cuesta tokens.

**3. El coste real es a nivel de tarea, no a nivel de token.** Los modelos de razonamiento y thinking han reducido el precio unitario del token, pero han multiplicado el número de tokens por tarea. El usuario medio paga más que antes, no menos. "Token level, the number is numerically smaller. At the task level, you're actually paying more, which to the end consumer is actually the only thing that matters."

**4. La subsidiación actual es una trampa de lock-in.** Claude Code y herramientas similares funcionan ahora con tarifa plana porque los VCs están subsidiando el coste. Cuando ese grifo se cierre, los usuarios que han construido sus flujos de trabajo sobre context windows de un millón de tokens no podrán migrar a modelos locales (que tienen 256K como máximo en hardware top), ni podrán permitirse las tarifas reales. La dependencia habrá sido construida deliberadamente.

**5. MCP como alternativa infrautilizada.** Carambat señala que los MCP servers son una alternativa mucho más eficiente en tokens porque encapsulan acciones en llamadas a función con parámetros definidos, en lugar de dejar que el modelo explote tokens resolviendo lo mismo con razonamiento libre. Sin embargo, los MCP no se promueven tanto precisamente porque consumen menos tokens.

**6. Los modelos locales no son solución si el usuario nunca construyó la disciplina.** Los usuarios que prueban a sustituir Claude por un modelo local (Llama, Qwen K2) tienen experiencias horribles porque están acostumbrados a "cramming garbage into the context window". La herramienta local no está diseñada para ese patrón de uso.

### Datos y evidencia

- El system prompt de OpenCode para Anthropic: ~3.200 tokens.
- El skill oficial de Anthropic para co-documentación de código en Claude Code: otros ~3.200 tokens.
- El skill "find" de Vercel's Skill Hub: ~1.000 tokens.
- El skill "browser" de Vercel: ~6.000 tokens.
- El fichero `plan-ceo-review` del repositorio GStack (Gary Tan, presidente de YC): **21.000 tokens** para un único skill, antes de que llame a ningún otro skill.
- GStack tiene 38.000 estrellas en GitHub al momento del vídeo.
- Hardware local top (M4 Ultra, buena cuantización): ~256K de contexto máximo, frente al millón de tokens de Claude Code.
- Carambat estuvo en YC Summer 2022 y menciona que Sam Altman prometió en ese evento que los costes de tokens bajarían. Su conclusión: bajaron a nivel unitario, pero subieron a nivel de tarea.
- El clip embebido (Dario Amodei / Anthropic): un ingeniero de $500K debería gastar al menos $250K en tokens al año. Carambat interpreta esto como una señal de que Anthropic no tiene planes de abaratar el coste neto en el largo plazo.

### Citas textuales (2-4 máx)

> "Skills are just system prompts with better marketing." — Timothy Carambat

> "Token level, the number is numerically smaller. At the task level, you're actually paying more, which to the end consumer is actually the only thing that matters." — Timothy Carambat

> "It's a huge token trap and I feel like nobody's talking about it." — Timothy Carambat

> "If you just keep bloating your context windows infinitely, then you can't leave their tools and there's no chance that you ever will because the friction would be too high — and then all they have to do is just turn on the money faucet." — Timothy Carambat

### Ejemplos concretos

- **GStack** (https://github.com/garytan/gstack — mencionado por nombre): repositorio de markdown files de Gary Tan (presidente de YC). El skill `plan-ceo-review` pesa 21.000 tokens. Usado como caso extremo del problema.
- **OpenCode**: herramienta de AI coding. Carambat analiza su system prompt para Anthropic (~3.200 tokens) como ejemplo de baseline ya pesado.
- **Vercel Skill Hub**: plataforma de distribución de skills markdown. Skills de ejemplo: "find" (~1.000 tokens), "browser" (~6.000 tokens).
- **Skill de co-documentación oficial de Anthropic** para Claude Code: ~3.200 tokens adicionales.
- **Reddit r/LocalLLaMA y subreddits de OpenClaw**: menciona que todos los usuarios que intentan sustituir Claude por modelos locales en estos foros reportan experiencias horribles, atribuidas al mismo patrón de uso.
- **Clip embebido de Dario Amodei** (o directivo de Anthropic): debate sobre el ROI en tokens de un ingeniero de $500K. No se proporciona URL pero el vídeo lo muestra en pantalla.

---

## Temas clave

### 1. La tesis del "token trap"
Carambat argumenta que Anthropic diseñó SKILLS.md para que los usuarios creen instrucciones largas que se cargan en cada interacción, inflando el consumo de tokens (y por tanto los ingresos de Anthropic). Su evidencia: no hay mecanismo nativo de carga selectiva, todo el .md se inyecta siempre.

### 2. Progressive disclosure como solución
La solución que Carambat sugiere (cargar contexto bajo demanda) es exactamente lo que OPENLAB ya implementa con la separación SKILL.md + context/ + templates/. El skill principal es ligero (~2-5K tokens), y las fases cargan dinámicamente lo que necesitan de context/.

### 3. Comparación con herramientas externas
Carambat menciona MCP servers y herramientas externas como alternativa a skills pesados. Esto es complementario, no sustitutivo: los MCP servers son herramientas (hacen cosas), los skills son procedimientos (saben cómo usar las herramientas). OPENLAB combina ambos.


**Telegraph:** https://telegra.ph/Claude-Code-Self-Improving-Skills-Are-the-Smarter-Way-to-Build-With-AI-03-25
