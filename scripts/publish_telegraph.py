#!/usr/bin/env python3
"""
OPENLAB Radar - Publicador Telegraph
Convierte ficheros .md a artículos de Telegraph (telegra.ph).
Imprime por stdout: ruta_fichero\turl_telegraph

Telegraph se integra nativamente con Telegram: los links se abren
como Instant View dentro de la app, sin salir del chat.

Uso: python3 publish_telegraph.py <fichero.md> [fichero2.md ...]
"""

import sys
import os
import re
import json
import requests
from html.parser import HTMLParser

TELEGRAPH_API = "https://api.telegra.ph"

# Tags que Telegraph acepta
ALLOWED_TAGS = frozenset({
    'a', 'aside', 'b', 'blockquote', 'br', 'code', 'em',
    'figcaption', 'figure', 'h3', 'h4', 'hr', 'i', 'img',
    'li', 'ol', 'p', 'pre', 's', 'strong', 'u', 'ul'
})

# Telegraph solo soporta h3 y h4
TAG_MAP = {'h1': 'h3', 'h2': 'h3', 'h5': 'h4', 'h6': 'h4'}


class HtmlToNodes(HTMLParser):
    """Convierte HTML a array de Node objects de Telegraph."""

    def __init__(self):
        super().__init__()
        self.result = []
        self.stack = [self.result]

    def handle_starttag(self, tag, attrs):
        mapped = TAG_MAP.get(tag, tag)
        if mapped not in ALLOWED_TAGS:
            # Tag no soportado: sus hijos se añaden al padre
            return

        node = {"tag": mapped}
        attr_dict = {k: v for k, v in attrs if k in ('href', 'src')}
        if attr_dict:
            node["attrs"] = attr_dict
        node["children"] = []

        self.stack[-1].append(node)
        self.stack.append(node["children"])

    def handle_endtag(self, tag):
        mapped = TAG_MAP.get(tag, tag)
        if mapped in ALLOWED_TAGS and len(self.stack) > 1:
            self.stack.pop()

    def handle_data(self, data):
        if data.strip():
            self.stack[-1].append(data)


def format_inline(text):
    """Formatea inline markdown: bold, italic, code, links."""
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def md_to_html(md_text):
    """Convierte markdown a HTML. Usa la librería markdown si está disponible."""
    try:
        import markdown
        return markdown.markdown(md_text, extensions=['fenced_code'])
    except ImportError:
        pass

    # Fallback sin dependencias
    lines = md_text.split('\n')
    html_parts = []
    in_code = False
    in_list = False
    para = []

    def flush_para():
        if para:
            html_parts.append(f"<p>{' '.join(para)}</p>")
            para.clear()

    for line in lines:
        stripped = line.rstrip()

        # Code blocks
        if stripped.startswith('```'):
            if in_code:
                html_parts.append('</code></pre>')
                in_code = False
            else:
                flush_para()
                if in_list:
                    html_parts.append('</ul>')
                    in_list = False
                html_parts.append('<pre><code>')
                in_code = True
            continue
        if in_code:
            from html import escape
            html_parts.append(escape(stripped) + '\n')
            continue

        # Empty line
        if not stripped:
            flush_para()
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            continue

        # Headers
        hm = re.match(r'^(#{1,6})\s+(.+)', stripped)
        if hm:
            flush_para()
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            level = len(hm.group(1))
            html_parts.append(f"<h{level}>{format_inline(hm.group(2))}</h{level}>")
            continue

        # HR
        if stripped in ('---', '***', '___'):
            flush_para()
            html_parts.append('<hr>')
            continue

        # Blockquote
        if stripped.startswith('>'):
            flush_para()
            html_parts.append(
                f"<blockquote>{format_inline(stripped[1:].strip())}</blockquote>"
            )
            continue

        # List items (- or *)
        lm = re.match(r'^[\-\*]\s+(.+)', stripped)
        if lm:
            flush_para()
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            html_parts.append(f"<li>{format_inline(lm.group(1))}</li>")
            continue

        # Table rows → texto plano con separadores
        if '|' in stripped and re.match(r'^\|?.+\|', stripped):
            # Skip separator rows (|---|---|)
            if re.match(r'^[\|\s\-:]+$', stripped):
                continue
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            flush_para()
            html_parts.append(f"<p>{format_inline(' · '.join(cells))}</p>")
            continue

        # Regular text → accumulate as paragraph
        if in_list:
            html_parts.append('</ul>')
            in_list = False
        para.append(format_inline(stripped))

    flush_para()
    if in_list:
        html_parts.append('</ul>')

    return '\n'.join(html_parts)


def publish(md_path, token):
    """Publica un .md en Telegraph. Retorna la URL o None."""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Strip YAML frontmatter si existe
    md_text = re.sub(r'^---\n.*?\n---\n?', '', md_text, flags=re.DOTALL)

    # Extraer título del primer heading y eliminarlo del contenido
    m = re.search(r'^#\s+(.+)', md_text, re.MULTILINE)
    title = m.group(1).strip() if m else os.path.basename(md_path).replace('.md', '')
    title = title[:256]
    if m:
        md_text = md_text[:m.start()] + md_text[m.end():].lstrip('\n')

    html = md_to_html(md_text)
    parser = HtmlToNodes()
    parser.feed(html)
    nodes = parser.result

    if not nodes:
        nodes = [{"tag": "p", "children": ["(sin contenido)"]}]

    try:
        resp = requests.post(f"{TELEGRAPH_API}/createPage", data={
            "access_token": token,
            "title": title,
            "author_name": "OPENLAB Radar",
            "content": json.dumps(nodes),
            "return_content": "false"
        }, timeout=30)
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        print(f"Error publicando {md_path}: {e}", file=sys.stderr)
        return None

    if not result.get("ok"):
        print(f"Error Telegraph {md_path}: {result.get('error', 'desconocido')}",
              file=sys.stderr)
        return None

    return result["result"]["url"]


def get_or_create_token():
    """Obtiene token de env o crea cuenta Telegraph nueva."""
    token = os.environ.get("TELEGRAPH_ACCESS_TOKEN")
    if token:
        return token

    try:
        resp = requests.post(f"{TELEGRAPH_API}/createAccount", data={
            "short_name": "OPENLAB Radar",
            "author_name": "OPENLAB Radar"
        }, timeout=30)
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        print(f"Error creando cuenta Telegraph: {e}", file=sys.stderr)
        import sys as _sys; _sys.exit(1)
        print(f"Error creando cuenta Telegraph: {result}", file=sys.stderr)
        sys.exit(1)

    token = result["result"]["access_token"]
    print(f"Cuenta Telegraph creada. Añade a config/.env:", file=sys.stderr)
    print(f"TELEGRAPH_ACCESS_TOKEN={token}", file=sys.stderr)
    return token


def main():
    if len(sys.argv) < 2:
        print("Uso: publish_telegraph.py <fichero.md> [fichero2.md ...]", file=sys.stderr)
        print("Output: ruta_fichero\\turl_telegraph (una línea por fichero)", file=sys.stderr)
        sys.exit(1)

    token = get_or_create_token()

    for path in sys.argv[1:]:
        if not os.path.isfile(path):
            print(f"No existe: {path}", file=sys.stderr)
            continue
        url = publish(path, token)
        if url:
            print(f"{path}\t{url}")


if __name__ == "__main__":
    main()
