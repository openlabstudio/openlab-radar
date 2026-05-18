#!/usr/bin/env python3
"""
OPENLAB Radar — Búsqueda estructurada por frontmatter.

Uso:
  python3 radar_search.py --score-min 8.0
  python3 radar_search.py --category context-engineering --tag mcp
  python3 radar_search.py --source "Simon Scrapes" --date-from 2026-05-01
  python3 radar_search.py --aplicabilidad-min 9
  python3 radar_search.py --type daily-briefing
  python3 radar_search.py --text "context poisoning"
  python3 radar_search.py --format json
  python3 radar_search.py --sort score
  python3 radar_search.py --stats
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from radar_utils import parse_frontmatter

DEFAULT_BRIEFS_DIR = Path(__file__).resolve().parent.parent / "briefs"


def load_all_briefs(briefs_dir):
    """Carga todos los .md con frontmatter bajo briefs/."""
    briefs = []
    for md in sorted(briefs_dir.rglob("*.md")):
        if md.name == "index.md":
            continue
        fm, body = parse_frontmatter(md)
        if not fm:
            continue
        fm["_path"] = str(md)
        fm["_filename"] = md.name
        fm["_category_dir"] = md.parent.name
        fm["_body"] = body
        briefs.append(fm)
    return briefs


def apply_filters(briefs, args):
    """Aplica filtros AND sobre la lista de briefs."""
    result = briefs

    if args.type:
        result = [b for b in result if b.get("type", "brief") == args.type]

    if args.category:
        result = [b for b in result
                  if b.get("category") == args.category
                  or b.get("secondary_category") == args.category]

    if args.secondary_category:
        result = [b for b in result if b.get("secondary_category") == args.secondary_category]

    if args.tag:
        for tag in args.tag:
            result = [b for b in result if tag in (b.get("tags") or [])]

    if args.source:
        q = args.source.lower()
        result = [b for b in result if q in (b.get("source") or "").lower()]

    if args.score_min is not None:
        result = [b for b in result if _float(b.get("score")) >= args.score_min]

    if args.score_max is not None:
        result = [b for b in result if _float(b.get("score")) <= args.score_max]

    if args.aplicabilidad_min is not None:
        result = [b for b in result
                  if _breakdown(b, "aplicabilidad") >= args.aplicabilidad_min]

    if args.novedad_min is not None:
        result = [b for b in result
                  if _breakdown(b, "novedad") >= args.novedad_min]

    if args.calidad_min is not None:
        result = [b for b in result
                  if _breakdown(b, "calidad") >= args.calidad_min]

    if args.date_from:
        result = [b for b in result if _date(b) >= args.date_from]

    if args.date_to:
        result = [b for b in result if _date(b) <= args.date_to]

    if args.text:
        pattern = re.compile(args.text, re.IGNORECASE)
        result = [b for b in result if pattern.search(b.get("_body", ""))]

    return result


def _float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


def _breakdown(brief, key):
    sb = brief.get("score_breakdown")
    if isinstance(sb, dict):
        return _float(sb.get(key))
    return 0.0


def _date(brief):
    return str(brief.get("date") or brief.get("date_end") or "")


def sort_briefs(briefs, sort_key):
    if sort_key == "score":
        return sorted(briefs, key=lambda b: _float(b.get("score") or b.get("top_score")), reverse=True)
    elif sort_key == "date":
        return sorted(briefs, key=lambda b: _date(b), reverse=True)
    elif sort_key == "aplicabilidad":
        return sorted(briefs, key=lambda b: _breakdown(b, "aplicabilidad"), reverse=True)
    return briefs


def format_table(briefs):
    """Salida tabla human-readable."""
    if not briefs:
        print("Sin resultados.")
        return

    print(f"\n{'Fecha':<12} {'Score':>5} {'A':>2} {'N':>2} {'C':>2} {'Categoría':<24} {'Título'}")
    print("-" * 100)
    for b in briefs:
        date = str(b.get("date") or b.get("date_end") or "?")[:10]
        score = b.get("score") or b.get("top_score") or b.get("avg_score") or ""
        score_str = f"{float(score):.1f}" if score else "  -"
        a = _breakdown(b, "aplicabilidad")
        n = _breakdown(b, "novedad")
        c = _breakdown(b, "calidad")
        a_str = str(int(a)) if a else " -"
        n_str = str(int(n)) if n else " -"
        c_str = str(int(c)) if c else " -"
        cat = b.get("category") or b.get("type") or b.get("_category_dir") or ""
        title = b.get("title") or b.get("_filename") or ""
        if len(title) > 55:
            title = title[:52] + "..."
        print(f"{date:<12} {score_str:>5} {a_str:>2} {n_str:>2} {c_str:>2} {cat:<24} {title}")

    print(f"\n{len(briefs)} resultado(s)")


def format_json(briefs):
    """Salida JSON (sin _body para no saturar)."""
    clean = []
    for b in briefs:
        entry = {k: v for k, v in b.items() if not k.startswith("_")}
        entry["path"] = b.get("_path", "")
        clean.append(entry)
    print(json.dumps(clean, ensure_ascii=False, indent=2, default=str))


def show_stats(briefs):
    """Muestra estadísticas globales."""
    from collections import Counter

    types = Counter(b.get("type", "brief") for b in briefs)
    cats = Counter(b.get("category", "?") for b in briefs if b.get("category"))
    sources = Counter(b.get("source", "?") for b in briefs if b.get("source"))
    scores = [_float(b.get("score")) for b in briefs if b.get("score")]

    print(f"\n=== Estadísticas del Radar ===\n")
    print(f"Total documentos: {len(briefs)}")
    print(f"\nPor tipo:")
    for t, n in types.most_common():
        print(f"  {t}: {n}")
    print(f"\nPor categoría:")
    for c, n in cats.most_common():
        print(f"  {c}: {n}")
    print(f"\nTop 10 fuentes:")
    for s, n in sources.most_common(10):
        print(f"  {s}: {n}")
    if scores:
        print(f"\nScores: media={sum(scores)/len(scores):.1f}, min={min(scores):.1f}, max={max(scores):.1f}")


def main():
    parser = argparse.ArgumentParser(description="OPENLAB Radar — Búsqueda estructurada")
    parser.add_argument("--briefs-dir", type=Path, default=DEFAULT_BRIEFS_DIR,
                        help="Ruta al directorio briefs/")

    # Filtros
    parser.add_argument("--type", choices=["brief", "daily-briefing", "weekly-digest"],
                        help="Tipo de documento")
    parser.add_argument("--category", help="Categoría principal o secundaria")
    parser.add_argument("--secondary-category", help="Solo categoría secundaria")
    parser.add_argument("--tag", action="append", help="Tag (repetible, AND)")
    parser.add_argument("--source", help="Canal/fuente (búsqueda parcial)")
    parser.add_argument("--score-min", type=float, help="Score mínimo")
    parser.add_argument("--score-max", type=float, help="Score máximo")
    parser.add_argument("--aplicabilidad-min", type=float, help="Aplicabilidad mínima")
    parser.add_argument("--novedad-min", type=float, help="Novedad mínima")
    parser.add_argument("--calidad-min", type=float, help="Calidad mínima")
    parser.add_argument("--date-from", help="Fecha desde (YYYY-MM-DD)")
    parser.add_argument("--date-to", help="Fecha hasta (YYYY-MM-DD)")
    parser.add_argument("--text", help="Búsqueda de texto en body (regex)")

    # Output
    parser.add_argument("--sort", choices=["date", "score", "aplicabilidad"], default="date",
                        help="Ordenar por (default: date)")
    parser.add_argument("--format", choices=["table", "json"], default="table",
                        help="Formato de salida (default: table)")
    parser.add_argument("--limit", type=int, help="Máximo de resultados")
    parser.add_argument("--stats", action="store_true", help="Mostrar estadísticas globales")

    args = parser.parse_args()

    briefs = load_all_briefs(args.briefs_dir)

    if args.stats:
        show_stats(briefs)
        return

    filtered = apply_filters(briefs, args)
    sorted_briefs = sort_briefs(filtered, args.sort)

    if args.limit:
        sorted_briefs = sorted_briefs[:args.limit]

    if args.format == "json":
        format_json(sorted_briefs)
    else:
        format_table(sorted_briefs)


if __name__ == "__main__":
    main()
