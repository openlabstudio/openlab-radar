#!/usr/bin/env python3
"""
Fix one-off: elimina el h1 duplicado en las páginas Telegraph ya publicadas.

Para cada brief con URL telegra.ph, llama a editPage con el contenido
sin el primer heading (que ya aparece como título de la página).

Uso:
    python3 scripts/fix_telegraph_titles.py [--dry-run]

Rollback: si algo sale mal, el .md en disco es la fuente de verdad.
Revertir publish_telegraph.py al commit anterior y relanzar si hace falta.
"""

import sys
import os
import re
import json
import time
import requests
from pathlib import Path

# Añadir scripts/ al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent))
from publish_telegraph import md_to_html, HtmlToNodes

TELEGRAPH_API = "https://api.telegra.ph"
DRY_RUN = "--dry-run" in sys.argv


def get_token():
    env_path = Path(__file__).parent.parent / "config" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("TELEGRAPH_ACCESS_TOKEN="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("TELEGRAPH_ACCESS_TOKEN")


def extract_telegraph_url(md_text):
    m = re.search(r'\*\*Telegraph:\*\*\s*(https://telegra\.ph/\S+)', md_text)
    return m.group(1) if m else None


def strip_frontmatter(md_text):
    return re.sub(r'^---\n.*?\n---\n?', '', md_text, flags=re.DOTALL)


def strip_first_h1(md_text):
    """Elimina el primer # Heading del markdown. Retorna (title, md_sin_h1)."""
    m = re.search(r'^#\s+(.+)', md_text, re.MULTILINE)
    if not m:
        return None, md_text
    title = m.group(1).strip()
    md_rest = md_text[:m.start()] + md_text[m.end():].lstrip('\n')
    return title, md_rest


def edit_page(path, token, title, nodes):
    resp = requests.post(f"{TELEGRAPH_API}/editPage/{path}", data={
        "access_token": token,
        "title": title[:256],
        "author_name": "OPENLAB Radar",
        "content": json.dumps(nodes),
        "return_content": "false"
    })
    return resp.json()


def process_brief(md_path, token):
    raw = Path(md_path).read_text(encoding='utf-8')
    tg_url = extract_telegraph_url(raw)
    if not tg_url:
        return None, "sin URL Telegraph"

    tg_path = tg_url.replace("https://telegra.ph/", "")
    md_text = strip_frontmatter(raw)
    title, md_body = strip_first_h1(md_text)

    if not title:
        return None, "sin h1 en el markdown"

    html = md_to_html(md_body)
    parser = HtmlToNodes()
    parser.feed(html)
    nodes = parser.result or [{"tag": "p", "children": ["(sin contenido)"]}]

    if DRY_RUN:
        return tg_url, f"DRY-RUN — título: {title!r}, nodos: {len(nodes)}"

    for attempt in range(3):
        result = edit_page(tg_path, token, title, nodes)
        if result.get("ok"):
            return tg_url, "ok"
        error = result.get("error", "desconocido")
        # FLOOD_WAIT_N → esperar N+1 segundos y reintentar
        flood = re.match(r'FLOOD_WAIT_(\d+)', error)
        if flood and attempt < 2:
            wait = int(flood.group(1)) + 1
            time.sleep(wait)
            continue
        return tg_url, f"ERROR: {error}"
    return tg_url, "ERROR: max reintentos"


def find_briefs():
    root = Path(__file__).parent.parent / "briefs"
    return sorted(root.rglob("*.md"))


def main():
    token = get_token()
    if not token:
        print("ERROR: no se encontró TELEGRAPH_ACCESS_TOKEN", file=sys.stderr)
        sys.exit(1)

    briefs = find_briefs()
    ok = failed = skipped = 0

    for brief in briefs:
        url, status = process_brief(brief, token)
        time.sleep(1)  # evitar flood
        if url is None:
            skipped += 1
            continue

        rel = brief.relative_to(Path(__file__).parent.parent)
        if "ERROR" in status:
            print(f"FAIL  {rel}\n      {url}\n      {status}")
            failed += 1
        else:
            print(f"OK    {rel}\n      {url}\n      {status}")
            ok += 1

    print(f"\nResumen: {ok} ok / {failed} fallidos / {skipped} sin Telegraph")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
