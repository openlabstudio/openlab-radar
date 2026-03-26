# Acceso al VPS de OPENLAB Radar

## Requisitos

- VS Code con la extensión **Remote - SSH** instalada
- Claude Code activo en VS Code

## Paso 1 — Configurar tu acceso (solo una vez)

Abre Claude Code en VS Code y pégale este prompt:

> Necesito que me configures acceso SSH a un servidor remoto para poder conectarme desde VS Code Remote SSH. Los datos son:
>
> - Host: openlab-vps
> - IP: 212.227.104.123
> - Usuario: openlab
> - Key: genera una ed25519 si no tengo una en ~/.ssh/
>
> Configura mi ~/.ssh/config y al final dame mi clave pública (el contenido de ~/.ssh/id_ed25519.pub) para que se la envíe al administrador.

## Paso 2 — Enviar tu clave pública

Claude te dará una línea que empieza por `ssh-ed25519 AAAA...`. Envíasela a Rafa por Slack o email.

Rafa la añadirá al servidor y te confirmará cuando esté lista.

## Paso 3 — Conectarte desde VS Code

1. `Cmd+Shift+P` → **Remote-SSH: Connect to Host**
2. Selecciona **openlab-vps**
3. Abre la carpeta `/home/openlab/openlab-radar`
4. Ya puedes navegar los briefs, configuración y scripts del proyecto
