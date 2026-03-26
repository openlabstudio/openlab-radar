# How My Claude Skills Improve Themselves (Autoresearch)

- **Fuente:** [https://www.youtube.com/watch?v=aWZG6inDrpU](https://www.youtube.com/watch?v=aWZG6inDrpU)
- **Canal:** Kacper Rutkiewicz | AI Made Simple
- **Categoría:** context-engineering
- **Duración:** 20min
- **Fecha:** 2026-03-25
- **Score OPENLAB Radar:** 8.5
  - Aplicabilidad: 9
  - Novedad: 8
  - Calidad: 8

---

## Resumen ejecutivo

Aplicación del concepto "AutoResearch" de Andrej Karpathy a la mejora autónoma de Claude skill files. El agente ejecuta un bucle generate → evaluate → modify skill → repeat de forma autónoma, partiendo de un eval suite de preguntas sí/no y un skill.md como palanca. El resultado documentado: pasar de un 60-70% de outputs buenos a un 95% consistente con 100 iteraciones overnight.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** El proceso de QA y mejora continua de skills es uno de los puntos débiles no resueltos en el delivery de OPENLAB. Este patrón cierra ese gap: en vez de iterar manualmente sobre un skill hasta que funciona, el agente itera solo mientras duermes. Directamente integrable en el proceso de entrega de skills a clientes.
- **Referencias que conectan:** El enfoque de "brain dump en lenguaje natural de lo que quiero que haga el auto-research" + "criterios de evaluación como preguntas sí/no" replica exactamente lo que OPENLAB hace en el proceso de briefing con clientes: definir criterios de éxito en lenguaje natural antes de ejecutar.
- **Capacidades de plataforma:** El patrón usa Claude Code + skill files (el stack exacto de OPENLAB). No requiere infraestructura adicional. El GitHub repo de AutoResearch (mencionado en el vídeo) se puede clonar directamente en cualquier proyecto.
- **Oportunidades nuevas:** OPENLAB puede ofrecer como parte de su delivery un "eval suite" para cada skill entregado: una batería de 5-10 preguntas sí/no que el cliente puede usar para medir la calidad del skill y ejecutar ciclos de mejora autónomos. Convierte un entregable estático en un sistema que mejora solo.
- **Argumento comercial:** "Cada skill que entregamos viene con su eval suite. Si el skill empieza a degradarse, el sistema lo detecta y propone mejoras automáticamente. No dependes de nosotros para mantener la calidad."

---

## Contenido detallado

### Ideas y argumentos principales

El speaker parte de una realidad conocida: los Claude skills a veces producen outputs excelentes y a veces "straight garbage". La inconsistencia es el problema a resolver. AutoResearch de Karpathy (diseñado para redes neuronales) resuelve esto aplicado a skill files.

**El bucle AutoResearch para skills:**
1. El agente lee el skill.md actual
2. Genera un output con el skill
3. Evalúa el output contra el eval suite (preguntas sí/no con puntuación)
4. Si mejora respecto a la iteración anterior, guarda los cambios al skill.md
5. Si empeora, revierte al estado anterior y prueba otra dirección
6. Repite hasta alcanzar el score objetivo o agotar las iteraciones

**Los 3 ingredientes obligatorios:**
- **Métrica objetiva:** un número que puedes medir, no "vibes". En el ejemplo: puntuación de 0-50 (5 criterios × 10 puntos).
- **Herramienta de medición (eval suite):** preguntas sí/no automatizadas. Nunca evaluación subjetiva. El speaker usa 5-10 preguntas por skill. Sin intervención humana.
- **Palanca:** el fichero que el agente puede modificar. En este caso, el skill.md. Si no hay nada que cambiar, el bucle no tiene sentido.

Si falta cualquiera de los tres, el bucle no funciona.

**Por qué preguntas sí/no:** Porque son más difíciles de "gamear" para el AI. Una pregunta de puntuación del 1-10 invita al modelo a optimizar hacia scores altos aunque el output sea raro. Una pregunta sí/no fuerza a evaluar el criterio real.

**Regla anti-gaming:** El speaker añade explícitamente al prompt: "si el post empieza a sonar raro o artificial para pasar los criterios, señálalo. Prefiero la honestidad." Los modelos de AI optimizan métricas — hay que diseñar los criterios para que la métrica y la calidad real estén alineadas.

**Escala:** 100 iteraciones overnight (una cada 5 minutos = 12/hora). No requiere supervisión humana.

**No se reescribió el skill manualmente:** El speaker enfatiza esto. No escribió nuevas instrucciones. Solo definió criterios y el AI encontró qué cambios mejoraban el output. Los cambios finales: hooks prohibidos, enforcement de identidad, intimacy anchors, story pacing.

**Aplicabilidad más allá de skills:** El mismo bucle funciona para YouTube titles, email copy, landing pages, ad creatives — cualquier proceso con criterios medibles.

### Datos y evidencia

- Mejora documentada: de 60-70% de outputs buenos a 95% consistente
- Demo: LinkedIn post generator skill mejorado en 10 iteraciones hasta score 50/50
- Demo 2: YouTube title generator skill (en vivo)
- Eval suite: 5-10 preguntas sí/no por skill
- Score: 5 criterios × 10 puntos = 50 puntos máximo
- Velocidad: 1 iteración cada 5 minutos = 12/hora = 100+ overnight
- El agente corrió 12 iteraciones (10 de mejora + 2 de verificación anti-gaming)

### Citas textuales

> "I didn't rewrite this skill. I just gave a set of criteria and the AI ran the experiments, evaluating each iteration and improving on itself. It found the changes that mattered and made my content measurably better." — Speaker

> "Don't game the eval. If the post starts sounding weird or unnatural just to pass the criteria, flag it. I'd rather have honesty." — Speaker (regla anti-gaming en el prompt)

> "If you're missing any one of these three, the loop won't work. No metric, you can't tell if the previous iteration was better. No evaluation, you can't produce a metric. No lever, there's nothing to change." — Speaker

### Ejemplos concretos

- **LinkedIn post generator skill:** Eval suite con 5 preguntas: "Does the hook stop the scroll? Does it match the primary trigger? Would Casper say this out loud to a friend? Does every line earn its place? Does it leave the reader wanting to respond?"
- **YouTube title generator skill:** 10 preguntas: "Is it under 60 characters? Are first letters capitalized? Does it include..."
- **Setup del proyecto:** Carpeta independiente "auto-research" separada del proyecto principal para evitar context bloat de otros CLAUDE.md files. Se clona el repo de AutoResearch y se copia el skill folder a evaluar.
- **GitHub repo:** AutoResearch (de Karpathy) — mencionado en descripción del vídeo.

---

## Temas clave

### 1. Eval-driven skill improvement como proceso estándar

El framework convierte la mejora de skills de un proceso artesanal (prueba y error manual) a un proceso sistemático (bucle automatizado con criterios medibles). El prerequisito es definir el criterio de éxito antes de ejecutar — exactamente lo que un buen brief de cliente debería hacer.

### 2. Anti-gaming: alinear métricas con calidad real

El mayor riesgo de los sistemas de optimización automatizada es que optimizan la métrica, no el objetivo real. El speaker lo resuelve con dos tácticas: preguntas sí/no (más difíciles de gamear que scores numéricos) y una instrucción explícita al agente para señalar cuando el output mejora la puntuación pero pierde naturalidad.

### 3. Proyecto aislado para auto-research

El speaker descubrió que ejecutar el bucle dentro del proyecto principal causaba interferencias por los múltiples CLAUDE.md files y la memoria del proyecto. La solución: carpeta independiente limpia con solo el repo de AutoResearch y el skill a evaluar. Minimiza el context bloat y maximiza la coherencia del bucle.


**Telegraph:** https://telegra.ph/How-My-Claude-Skills-Improve-Themselves-Autoresearch-03-25
