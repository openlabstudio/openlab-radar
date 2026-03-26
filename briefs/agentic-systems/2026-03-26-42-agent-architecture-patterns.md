# 42 Agent Architecture Patterns: From Skill Repos to Intent & Harness Engineering

- **Fuente:** [https://www.youtube.com/watch?v=qJE2G-Rdq9Y](https://www.youtube.com/watch?v=qJE2G-Rdq9Y)
- **Canal:** Intuition Machine - AGI is the Medium
- **Categoría:** agentic-systems
- **Duración:** 19min
- **Fecha:** 2026-03-26
- **Score OPENLAB Radar:** 8.2
  - Aplicabilidad: 9
  - Novedad: 8
  - Calidad: 6

---

## Resumen ejecutivo

Un "pattern language" al estilo Alexandrino para Claude Code: 42 patrones nombrados, interconectados y estructurados para resolver problemas recurrentes en el diseño de sistemas agénticos. Los patrones cubren desde los cimientos estructurales (Skill Repository, Context Window Management) hasta aplicaciones de larga duración. La tesis central: **el prompting es prosa; la ingeniería de agentes es arquitectura**.

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** El diseño de skills en OPENLAB (ficheros .md + context/ + templates/) encaja directamente en los patrones del "Grupo 1: Structural Foundations". Los patrones de *Skill Repository* y *Context Loadability* formalizan exactamente las decisiones que OPENLAB toma al construir skills. Pueden adoptarse como vocabulario interno del equipo.
- **Referencias que conectan:** Sin acceso a project-references.md, pero el patrón de "harness engineering" es análogo al concepto de sistema agéntico multi-fase que OPENLAB entrega a clientes en procesos de conocimiento intensivo.
- **Capacidades de plataforma:** El "Intent Engineering Harness" descrito en el vídeo es equivalente al CLAUDE.md + estructura de skills de OPENLAB. El vídeo valida externamente la arquitectura que ya usa el stack: Claude Code CLI + lenguaje natural + patrones reutilizables.
- **Oportunidades nuevas:** Crear un "catálogo de patrones OPENLAB" basado en estos 42, adaptado a procesos de negocio (no solo coding). Podría ser un activo diferencial: "OPENLAB Pattern Language for Enterprise AI Skills".
- **Argumento comercial:** "Nuestros sistemas no se construyen sobre prompts improvisados — seguimos un lenguaje de patrones de arquitectura agéntica: cada skill tiene nombre, problema que resuelve, solución estructural y relaciones con otras skills."

---

## Contenido detallado

### Ideas y argumentos principales

El vídeo presenta 42 patrones en cuatro grupos, organizados como un vocabulario interconectado. Los patrones no son plantillas a copiar — son "compressed insights" que resuelven tensiones que van a repetirse independientemente del dominio. Aplicar un patrón sin entender las fuerzas que resuelve produce imitación superficial.

**La tensión central** en todo desarrollo de sistemas agénticos es entre la necesidad del agente de tener conocimiento contextual rico y conectado, frente al límite duro de la ventana de contexto. Cada decisión estructural en un skill repository es una negociación entre completitud y loadability.

**El insight clave:** Logramos fiabilidad determinista a través de restricciones estructurales. "Taming the probabilistic machine involves applying an intent engineering harness to the probabilistic cloud." Se fuerza fiabilidad determinista desde modelos creativos mediante ingeniería de intención deliberada.

**Grupo 1 — Structural Foundations:** Incluye patrones como Skill Repository (organización del conocimiento para carga selectiva), Context Window Management, y las decisiones de completitud vs cargabilidad.

**Grupo 2-4:** Cubren patrones de orquestación, coordinación multi-agente, y aplicaciones de larga duración (long-running applications).

### Datos y evidencia
- 42 patrones identificados en 4 grupos/zonas
- El patrón language está basado en el estilo Alexandrino (Christopher Alexander's "A Pattern Language")
- Sin datos cuantitativos de producción mencionados en el tramo analizado

### Citas textuales

> "Prompting is prose. Agent engineering is architecture." — Speaker

> "Patterns are not templates to copy. They are compressed insights about how to resolve tensions that will recur regardless of domain." — Speaker

> "A pattern applied without understanding the forces it resolves produces shallow imitation. A pattern understood produces genuine variance appropriate to their context." — Speaker

> "We force deterministic reliability out of creative models through deliberate intent engineering to avoid unreliable or brittle systems." — Speaker

### Ejemplos concretos
- Pattern language estilo Christopher Alexander aplicado a Claude Code
- 4 grupos de patrones: Structural Foundations, [grupos 2-4 no visibles en el tramo disponible]
- Conceptos clave: Skill Repository, Intent Engineering Harness, Harness Engineering, Context Loadability

---

## Temas clave

### 1. Skill Repository como patrón estructural
La tensión central en sistemas agénticos: el agente necesita conocimiento rico y conectado, pero la ventana de contexto es limitada. Cada skill debe ser "loadable" — suficientemente compacta para cargarse selectivamente. El patrón Skill Repository resuelve esto organizando el conocimiento en unidades dirigidas por el contexto de la tarea, no por completitud exhaustiva.

### 2. Intent Engineering Harness
El "harness" es la capa que aplica intención deliberada sobre el modelo probabilístico para obtener comportamiento determinista. Es equivalente al sistema de CLAUDE.md + instrucciones de sistema + estructura de skills. El vídeo lo trata como patrón nombrado y reutilizable.

### 3. Arquitectura vs Prompting
La distinción central del vídeo: el prompting ad-hoc produce resultados frágiles; la arquitectura agéntica (con patrones nombrados, relaciones explícitas entre skills, y harnessing de intención) produce sistemas fiables en producción. Esta distinción es el argumento de venta de OPENLAB frente a experimentación no estructurada con IA.


**Telegraph:** https://telegra.ph/42-Agent-Architecture-Patterns-From-Skill-Repos-to-Intent--Harness-Engineering-03-26
