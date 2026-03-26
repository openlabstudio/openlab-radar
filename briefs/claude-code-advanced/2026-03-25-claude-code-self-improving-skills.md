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

Guía práctica sobre cómo crear y mejorar Claude skills usando el flujo Claude.ai dashboard → descarga como .md → renombra a skill.md → importa en Antigravity. Introduce la integración de evals JSON dentro del propio skill.md para crear un bucle de auto-mejora sin infraestructura adicional. La analogía más potente del vídeo: CLAUDE.md es el trabajador, el skill.md es la herramienta que usa. Un worker sin herramientas es ineficiente; una herramienta sin worker no hace nada.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** El flujo skill.md + evals JSON + Antigravity es el stack de delivery estándar de OPENLAB en formato tutorial. Este vídeo sirve como material de referencia para el onboarding de clientes que necesitan entender la arquitectura de skills antes de que OPENLAB empiece a construir. Ahorra 20 minutos de explicación en la primera reunión.
- **Referencias que conectan:** La analogía CLAUDE.md = trabajador / skill = herramienta es la mejor explicación visual para clientes no técnicos — reemplaza o complementa el pitch narrativo que OPENLAB usa actualmente. Especialmente útil en el contexto DIBEX para audiencias sin background técnico.
- **Capacidades de plataforma:** El vídeo valida el stack de OPENLAB: Claude Code CLI + skill files en markdown + Antigravity como harness de ejecución. El dato de eficiencia — skills usan menos tokens que respuestas sin skill — es un argumento operativo que OPENLAB puede usar en conversaciones sobre coste con clientes enterprise.
- **Oportunidades nuevas:** La integración de evals JSON directamente en el skill.md (en vez de en un fichero separado) simplifica el proceso de QA de skills en delivery. OPENLAB puede estandarizar esta práctica: cada skill entregado lleva su eval suite embebido. Complementa el patrón AutoResearch de Karpathy descrito en el vídeo de Rutkiewicz del mismo día.
- **Argumento comercial:** "Cada skill que entregamos incluye su criterio de calidad integrado. Puedes medir si funciona sin preguntarnos, y el sistema puede mejorar el skill automáticamente si los resultados degradan."

---

## Contenido detallado

### Ideas y argumentos principales

El speaker parte de un problema frecuente: Claude produce outputs inconsistentes — a veces excelentes, a veces "bloated". La causa no es el modelo sino la ausencia de skills. Un skill es una instrucción persistente y especializada que guía al modelo hacia outputs consistentes.

**Flujo de creación de skills:**
1. Abrir Claude.ai con memoria del usuario activada
2. Mantener conversaciones con Claude hasta que "aprende" el estilo y preferencias deseadas
3. Pedirle que genere el skill file basado en esa conversación
4. Descargar el resultado como .md
5. Renombrar a skill.md
6. Importar en Antigravity (el harness de Claude Code)

Este flujo es más rápido que escribir el skill desde cero porque aprovecha la memoria conversacional que Claude ya ha acumulado.

**La analogía central:**
- CLAUDE.md = el trabajador (quién es, cómo piensa, qué valores tiene)
- skill.md = la herramienta (qué hace, cómo lo hace, con qué criterios)

Un CLAUDE.md sin skills produce outputs genéricos. Un skill sin CLAUDE.md no tiene contexto de quién lo usa. La combinación es donde se produce consistencia.

**Evals JSON integrados en el skill:**
El speaker propone añadir un bloque de evaluación directamente al skill.md:
```json
{
  "eval": {
    "criteria": [
      "Does the output match the required format?",
      "Is the tone appropriate for the target audience?",
      "Does it include the mandatory sections?"
    ],
    "scoring": "yes/no per criterion"
  }
}
```
Este bloque permite que Claude Code evalúe sus propios outputs antes de entregarlos. Si el output falla más de N criterios, el agente puede regenerar automáticamente.

**Eficiencia de tokens:** Un skill bien definido reduce el número de tokens necesarios porque el modelo no necesita "deducir" el contexto desde cero. Las instrucciones están precompiladas. En uso intensivo (múltiples invocaciones por día), esto se traduce en reducción de costes y menor latencia.

**Auto-mejora:** La combinación de evals JSON + Claude Code permite crear un bucle donde el agente:
1. Ejecuta el skill
2. Evalúa el output contra los criterios
3. Si falla, modifica el skill.md y reintenta
4. Si mejora, guarda los cambios

Sin intervención humana para casos simples.

### Datos y evidencia

- Skills usan menos tokens que respuestas equivalentes sin skill (no cuantificado exactamente, pero demostrado en demo)
- Flujo de creación: 5 pasos desde Claude.ai hasta Antigravity
- Evals JSON: 3-10 criterios sí/no por skill recomendados
- Antigravity como harness de ejecución de skills en Claude Code CLI

### Citas textuales

> "If Claude keeps giving you bloated or inconsistent outputs, you're missing one thing: Skills." — Adrian Szramowski

> "CLAUDE.md is the worker. The skill is the tool the worker uses. A worker without tools is inefficient. A tool without a worker does nothing." — Adrian Szramowski

### Ejemplos concretos

- **Demo de creación:** Skill de generación de posts para LinkedIn creado desde la memoria de conversaciones en Claude.ai
- **Evals integrados:** Bloque JSON en el skill.md que evalúa criterios de formato, tono y estructura
- **Antigravity:** Harness mencionado como entorno de ejecución de skills para Claude Code
- **Loop de auto-mejora:** Demostración de cómo el agente modifica su propio skill.md para mejorar el score de evaluación

---

## Temas clave

### 1. Claude.ai como entorno de diseño de skills

La memoria conversacional de Claude.ai actúa como un "briefing orgánico": al mantener conversaciones sobre el tipo de outputs deseados, Claude aprende el estilo antes de que el diseñador escriba una sola instrucción formal. El skill generado a partir de esa memoria refleja preferencias reales, no preferencias asumidas. Este flujo es más rápido y más preciso que escribir skills desde cero.

### 2. Evals embebidos como estándar de calidad en el entregable

Incluir el eval suite dentro del propio skill.md convierte el skill en un entregable auto-verificable. El cliente no necesita saber cómo funciona el skill por dentro — puede ejecutarlo y ver si pasa sus propios criterios. Esto reduce la dependencia del cliente en el proveedor para QA y aumenta la confianza en el sistema.

### 3. Eficiencia de tokens como argumento operativo

En deployments con muchas invocaciones diarias, la diferencia de tokens entre "con skill" y "sin skill" se convierte en diferencia de coste y velocidad. Un skill bien diseñado precompila el contexto necesario, eliminando el overhead de contexto en cada llamada. Para clientes enterprise con volumen alto, este argumento puede ser más convincente que la calidad del output.


**Telegraph:** https://telegra.ph/Claude-Code-Self-Improving-Skills-Are-the-Smarter-Way-to-Build-With-AI-03-25
