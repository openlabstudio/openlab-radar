#!/usr/bin/env python3
"""
OPENLAB Radar — Utilidades compartidas.
Funciones de parseo de frontmatter usadas por múltiples scripts.
"""

import re
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def parse_frontmatter(filepath):
    """Extrae frontmatter YAML y body de un brief markdown.

    Retorna (dict, body_str). Si no hay frontmatter válido → ({}, full_text).
    Soporta campos nested (score_breakdown) vía yaml.safe_load.
    """
    path = Path(filepath)
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r'^---\n(.*?)\n---\s*\n?(.*)', text, re.DOTALL)
    if not m:
        return {}, text

    raw_yaml = m.group(1)
    body = m.group(2)
    fm = {}

    if HAS_YAML:
        try:
            fm = yaml.safe_load(raw_yaml) or {}
        except Exception:
            pass
    else:
        # Fallback sin pyyaml: parsear key: value simples + listas
        current_key = None
        for line in raw_yaml.splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                if current_key is not None:
                    fm.setdefault(current_key, []).append(
                        stripped[2:].strip().strip('"').strip("'")
                    )
                continue
            if ":" in stripped:
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if val:
                    fm[key] = val
                    current_key = None
                else:
                    current_key = key
                    fm.setdefault(key, [])

    return fm, body


def dump_frontmatter(fm_dict, body):
    """Reconstruye el fichero markdown con frontmatter YAML + body original.

    Mantiene orden de claves y caracteres Unicode (tildes, eñes).
    """
    if not HAS_YAML:
        raise RuntimeError("PyYAML requerido para dump_frontmatter")

    yaml_str = yaml.dump(
        fm_dict,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=200,
    )
    return f"---\n{yaml_str}---\n{body}"


def load_briefs(briefs_dir, include_daily=False, include_weekly=False):
    """Carga briefs con frontmatter desde el directorio de briefs.

    Por defecto excluye daily-briefings y weekly-digests.
    """
    briefs_dir = Path(briefs_dir)
    briefs = []
    exclude = set()
    if not include_daily:
        exclude.add("daily-briefings")
    if not include_weekly:
        exclude.add("weekly-digests")

    for cat_dir in sorted(briefs_dir.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name in exclude:
            continue
        if cat_dir.name == "index.md":
            continue
        for md in sorted(cat_dir.glob("*.md")):
            fm, body = parse_frontmatter(md)
            if fm:
                fm["_category_dir"] = cat_dir.name
                fm["_path"] = str(md)
                briefs.append(fm)
    return briefs
