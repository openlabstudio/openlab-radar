#!/usr/bin/env python3
"""
OPENLAB Radar - Notificador
Envía el briefing diario por email (Gmail) y Telegram.

Uso: python notify.py <briefing_file>
     python notify.py briefs/2026-03-23-briefing.md

Variables de entorno requeridas:
  TELEGRAM_BOT_TOKEN  - Token del bot de Telegram
  TELEGRAM_CHAT_ID    - Chat ID donde enviar (tu chat personal con el bot)

El email se envía via Claude Code + Gmail MCP (script separado: notify_email.sh)
"""

import argparse
import os
import sys
from pathlib import Path

import requests


def send_telegram(text, bot_token, chat_id):
    """Envía mensaje por Telegram. Trocea si excede 4096 chars."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    max_len = 4000  # Margen de seguridad

    chunks = []
    if len(text) <= max_len:
        chunks = [text]
    else:
        # Partir por secciones (###)
        sections = text.split("\n### ")
        current = ""
        for i, section in enumerate(sections):
            prefix = "### " if i > 0 else ""
            candidate = current + "\n" + prefix + section if current else prefix + section
            if len(candidate) > max_len:
                if current:
                    chunks.append(current.strip())
                current = prefix + section
            else:
                current = candidate
        if current:
            chunks.append(current.strip())

    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code != 200:
            # Reintentar sin Markdown si falla el parseo
            payload["parse_mode"] = None
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code != 200:
                print(f"ERROR Telegram (chunk {i+1}): {resp.status_code} {resp.text}",
                      file=sys.stderr)
                return False
    return True


def _load_env():
    """Carga config/.env si existe (para uso standalone del modo --status)."""
    env_path = Path(__file__).parent.parent / "config" / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    value = value.strip().strip('"').strip("'")
                    os.environ.setdefault(key.strip(), value)


def send_status(text):
    """Envía un mensaje de estado simple por Telegram. Retorna True si OK."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        print("WARN: TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID no configuradas.", file=sys.stderr)
        return False
    return send_telegram(text, bot_token, chat_id)


def main():
    parser = argparse.ArgumentParser(description="OPENLAB Radar - Notificador")
    parser.add_argument("briefing_file", nargs="?", help="Path al fichero de briefing .md")
    parser.add_argument("--status", metavar="MENSAJE",
                        help="Enviar mensaje de estado por Telegram y salir")
    parser.add_argument("--telegram-only", action="store_true",
                        help="Solo enviar por Telegram")
    parser.add_argument("--email-only", action="store_true",
                        help="Solo enviar por email")
    args = parser.parse_args()

    # Modo status: enviar mensaje simple y salir
    if args.status:
        _load_env()
        ok = send_status(args.status)
        sys.exit(0 if ok else 1)

    if not args.briefing_file:
        parser.error("briefing_file es obligatorio cuando no se usa --status")

    briefing_path = Path(args.briefing_file)
    if not briefing_path.exists():
        print(f"ERROR: No existe {briefing_path}", file=sys.stderr)
        sys.exit(1)

    content = briefing_path.read_text(encoding="utf-8")
    if not content.strip():
        print("Briefing vacío, nada que enviar.")
        return

    sent_any = False

    # --- Telegram ---
    if not args.email_only:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")

        if bot_token and chat_id:
            print("Enviando por Telegram...", end=" ")
            if send_telegram(content, bot_token, chat_id):
                print("OK")
                sent_any = True
            else:
                print("FALLO")
        else:
            print("WARN: TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID no configuradas. "
                  "Telegram desactivado.", file=sys.stderr)

    # --- Email via script que invoca Claude Code + Gmail MCP ---
    if not args.telegram_only:
        email_script = Path(__file__).parent / "notify_email.sh"
        if email_script.exists():
            print("Enviando por email...")
            exit_code = os.system(f'bash "{email_script}" "{briefing_path}"')
            if exit_code == 0:
                print("Email: OK")
                sent_any = True
            else:
                print("Email: FALLO", file=sys.stderr)
        else:
            print(f"WARN: {email_script} no existe. Email desactivado.", file=sys.stderr)

    if not sent_any:
        print("WARN: No se envió por ningún canal.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
