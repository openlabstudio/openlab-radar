# Agent Identity Protocol (AIP): Securing AI Agents & MCP Servers at Scale

- **Fuente:** [https://www.youtube.com/watch?v=UaJkKDFnulc](https://www.youtube.com/watch?v=UaJkKDFnulc)
- **Canal:** MCP Developers Summit
- **Categoría:** agentic-systems
- **Duración:** 40min
- **Fecha:** 2026-03-23
- **Score OPENLAB Radar:** 7.5
  - Aplicabilidad: 7
  - Novedad: 8
  - Calidad: 8

---

## Resumen ejecutivo

Episodio del podcast "The Context" del MCP Developers Summit con James Cao sobre el Agent Identity Protocol (AIP) — un protocolo para autenticar y autorizar agentes IA que interactúan con MCP servers. Aborda el problema de seguridad fundamental: cuando un agente accede a sistemas empresariales vía MCP, ¿cómo verificas quién es el agente, qué puede hacer y quién es responsable de sus acciones?

---

## Aplicabilidad OPENLAB

- **Servicios que se refuerzan:** Relevante para la **fase de setup** de cualquier proyecto OPENLAB donde el agente interactúa con sistemas del cliente vía MCP (Gmail, SharePoint, Salesforce, etc.). AIP podría convertirse en requisito enterprise conforme los clientes maduren en governance de IA. Refuerza el argumento de que OPENLAB diseña sistemas "enterprise-ready".
- **Referencias que conectan:** El **Observatorio Iberostar** corre en Azure con acceso a Google Drive. Si Iberostar escala a más agentes, necesitará governance sobre qué agente accede a qué. AIP es el tipo de protocolo que se necesitará.
- **Capacidades de plataforma:** MCP es parte central del stack OPENLAB (platform-capabilities.md lista 10.000+ servers públicos + oficiales de Google, Microsoft, Salesforce). AIP se integraría como capa de seguridad sobre MCP sin cambiar la arquitectura.
- **Oportunidades nuevas:** Cuando AIP madure, OPENLAB podría ofrecer **setup de governance** como servicio adicional en proyectos enterprise: configurar identidades de agentes, permisos por MCP server, audit trail. Es un upsell natural post-piloto.
- **Argumento comercial:** "Nuestros agentes no son cajas negras. Cada agente tiene identidad verificable, permisos definidos y trazabilidad completa de sus acciones."

---

## Contenido detallado

### Ideas y argumentos principales

El speaker James Cao (CEO de Ironwood Cyber, maintainer principal del proyecto) presenta AIP como respuesta directa al problema de que los agentes IA operan con "modo dios": cuando corres un agente en tu sistema, este se ejecuta con tus permisos de usuario, accede a tus API keys y puede llamar cualquier herramienta sin restricción. No hay distinción entre el humano y el agente.

La tesis central es que la seguridad de agentes requiere dos capas complementarias: **autenticación** (¿quién es este agente?) y **autorización** (¿qué está permitido hacer?). AIP las combina en una arquitectura de dos capas:

- **Capa 1 — Identidad:** Un token de atestación del agente (Agent Attestation Token) que certifica quién controla al agente, qué puede hacer y durante cuánto tiempo. Basado en un registro raíz que firma identidades. El estándar exacto está aún en evolución (se está coordinando con el IETF, el Internet Engineering Task Force, que trabaja actualmente en estándares de autenticación agéntica).

- **Capa 2 — Enforcement:** Un proxy transparente que se sitúa entre el agente y el MCP server. Opera en denegación implícita (principio de mínimo privilegio): todo está bloqueado por defecto, solo se permite lo explícitamente autorizado. Incluye DLP scanning (detección de exfiltración de datos mediante regex), human-in-the-loop (el proxy puede pausar y pedir aprobación humana antes de ejecutar herramientas de alto riesgo) y audit trail inmutable.

El argumento sobre el surface de ataque es concreto: un agente ingiere un documento envenenado, sufre prompt injection indirecto, y una herramienta queda secuestrada para hacer algo malicioso — exfiltrando datos mientras completa la tarea asignada. El caso "GeminiJack" se menciona como ejemplo real de exfiltración.

Durante el Q&A se desarrolla una tensión interesante: el moderador (Shannon) argumenta que los agentes modernos son cada vez más desestructurados (generan código dinámicamente, llaman herramientas de forma opaca) y que las políticas basadas en reglas estructuradas pueden quedarse cortas. La respuesta de James es pragmática: AIP no pretende ser la solución total, sino una capa adicional que evita los casos más claros ("nunca toques mi base de datos", "nunca ejecutes delete en mi carpeta del sistema"). Para los casos más complejos, reconoce que quizá haga falta IA en el propio data path evaluando políticas en lenguaje natural.

### Datos y evidencia

- AIP empezó hace "un par de meses" (desde el momento de la charla, ~enero 2026).
- La implementación actual es un proxy local escrito en Go.
- El proyecto vive en GitHub bajo la organización `open-agent-identity-protocol`.
- La documentación está en `agentidentityprotocol.io`.
- El IETF celebró IETF125 esa semana en Shenzhen, con sesiones dedicadas a autenticación y autorización agéntica.
- El proyecto está coordinando su estándar de identidad con grupos de trabajo del IETF.
- Implementaciones planificadas en Rust, Python y otros lenguajes, además de SDKs.

Sin benchmarks cuantitativos de rendimiento o adopción.

### Citas textuales

> "MCP servers are mainly more agentic AI having god mode for most things or everything. When you have agents running your system they're running as you — they have access to your user permissions, any API keys and secrets that you give it access to." — James Cao

> "The agent should never be able to access a tool by design because it is untrusted. So anything that we want to add in is explicitly allowed." — James Cao

> "It started off as: I want to protect my database, so I don't want my AI to ever touch my database at all. And then now it's kind of evolving to be like: how do we secure scale with these agents as it moves around." — James Cao

> "I really don't think there's any way to solve this except using AI in the data path — you have to develop models, you need natural language policies. This is an unstructured problem and it requires an unstructured solution." — Shannon (moderador), durante el Q&A

### Ejemplos concretos

- **Demo en vivo con Cursor + proxy Go:** Se muestra cómo el proxy AIP se integra con Cursor como cliente MCP. El agente puede llamar `list_my_emails` (permitido explícitamente) pero no `list_all_emails` (denegado implícitamente). La llamada bloqueada devuelve un error estándar. La configuración se genera como binario + archivo de política YAML en el directorio local, y se referencia en `mcp.json` de Cursor.
- **Tutorial 6 del repositorio:** "External enforcement with our Go proxy" — el tutorial de referencia usado en la demo.
- **GeminiJack:** Caso de exfiltración de datos mencionado como ejemplo de ataque real que AIP busca mitigar.
- **GitHub:** `github.com/open-agent-identity-protocol/agent-identity-protocol`
- **Docs:** `agentidentityprotocol.io`

---

## Temas clave

### 1. El problema de identidad en agentes IA
Cuando un agente accede a un MCP server (p.ej. Salesforce), el servidor no puede distinguir si es un agente autorizado o un prompt injection. AIP propone un sistema de identidad donde cada agente tiene credenciales verificables.

### 2. Permisos granulares por MCP server
AIP permite definir qué puede hacer cada agente en cada MCP server: lectura, escritura, acceso a qué recursos. Esto es fundamental para clientes enterprise que necesitan segregación de accesos.

### 3. Audit trail y responsabilidad
Cada acción del agente queda registrada con su identidad. Esto resuelve la pregunta "¿quién es responsable si el agente hace algo mal?" — fundamental para compliance en sectores regulados.
