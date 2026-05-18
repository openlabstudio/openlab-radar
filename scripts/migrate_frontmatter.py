#!/usr/bin/env python3
"""
OPENLAB Radar — Migración de frontmatter.
Enriquece briefs existentes y añade frontmatter a daily-briefings y weekly-digests.

Uso:
  python3 migrate_frontmatter.py --briefs-dir /path/to/briefs --mode all --dry-run
  python3 migrate_frontmatter.py --briefs-dir /path/to/briefs --mode enrich-briefs
  python3 migrate_frontmatter.py --briefs-dir /path/to/briefs --mode add-dailies
  python3 migrate_frontmatter.py --briefs-dir /path/to/briefs --mode add-weeklies
  python3 migrate_frontmatter.py --briefs-dir /path/to/briefs --mode all
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from radar_utils import parse_frontmatter, dump_frontmatter

# ──────────────────────────────────────────────────────────────────────────────
# Enriquecimiento de briefs de categoría
# ──────────────────────────────────────────────────────────────────────────────

def extract_enrichment_fields(body):
    """Extrae campos del cuerpo que faltan en el frontmatter actual."""
    fields = {}
    # Solo buscar en las primeras 35 líneas (bloque de metadatos)
    header_lines = "\n".join(body.splitlines()[:35])

    # telegraph_url
    m = re.search(r'\*\*Telegraph:\*\*\s*(https://telegra\.ph/\S+)', header_lines)
    if m:
        fields["telegraph_url"] = m.group(1)

    # score_breakdown
    a = re.search(r'Aplicabilidad:\s*(\d+)', header_lines)
    n = re.search(r'Novedad:\s*(\d+)', header_lines)
    c = re.search(r'Calidad:\s*(\d+)', header_lines)
    if a and n and c:
        fields["score_breakdown"] = {
            "aplicabilidad": int(a.group(1)),
            "novedad": int(n.group(1)),
            "calidad": int(c.group(1)),
        }

    # secondary_category
    m = re.search(r'\(secundaria:\s*([^)]+)\)', header_lines)
    if m:
        fields["secondary_category"] = m.group(1).strip()

    # duration
    m = re.search(r'\*\*Duración:\*\*\s*(\S+)', header_lines)
    if m:
        fields["duration"] = m.group(1)

    return fields


def enrich_brief(filepath, dry_run=False):
    """Enriquece un brief de categoría con campos extraídos del body.

    Retorna (changed: bool, fields_added: list[str]).
    """
    fm, body = parse_frontmatter(filepath)
    if not fm:
        return False, []

    new_fields = extract_enrichment_fields(body)
    fields_added = []

    # Determinar orden de inserción: después de los campos existentes
    for key, value in new_fields.items():
        if key not in fm:
            fm[key] = value
            fields_added.append(key)

    if not fields_added:
        return False, []

    if not dry_run:
        content = dump_frontmatter(fm, body)
        Path(filepath).write_text(content, encoding="utf-8")

    return True, fields_added


def run_enrich_briefs(briefs_dir, dry_run=False):
    """Enriquece todos los briefs de categoría."""
    briefs_dir = Path(briefs_dir)
    exclude = {"daily-briefings", "weekly-digests"}
    stats = {"processed": 0, "enriched": 0, "errors": 0, "fields": {}}

    for cat_dir in sorted(briefs_dir.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name in exclude:
            continue
        for md in sorted(cat_dir.glob("*.md")):
            if md.name == "index.md":
                continue
            stats["processed"] += 1
            try:
                changed, fields = enrich_brief(md, dry_run)
                if changed:
                    stats["enriched"] += 1
                    for f in fields:
                        stats["fields"][f] = stats["fields"].get(f, 0) + 1
                    prefix = "[DRY-RUN] " if dry_run else ""
                    print(f"  {prefix}{md.name}: +{', '.join(fields)}")
            except Exception as e:
                stats["errors"] += 1
                print(f"  ERROR {md.name}: {e}", file=sys.stderr)

    return stats


# ──────────────────────────────────────────────────────────────────────────────
# Añadir frontmatter a daily-briefings
# ──────────────────────────────────────────────────────────────────────────────

def extract_daily_frontmatter(filepath):
    """Extrae metadatos de un daily-briefing desde su contenido."""
    path = Path(filepath)
    text = path.read_text(encoding="utf-8", errors="replace")

    # Ya tiene frontmatter → skip
    if text.startswith("---\n"):
        return None, None

    fm = {"type": "daily-briefing"}

    # date: del nombre de fichero
    m = re.search(r'(\d{4}-\d{2}-\d{2})', path.name)
    if m:
        fm["date"] = m.group(1)

    # Métricas de la línea resumen (flexibe: "15 pasaron" o "15 pasaron / 8 descartados")
    m = re.search(
        r'\*\*Candidatos:\*\*\s*(\d+)\s*\|\s*\*\*Triage:\*\*\s*(\d+)\s*pasaron[^|]*\|\s*\*\*Briefing:\*\*\s*(\d+)\s*\|\s*\*\*Mención:\*\*\s*(\d+)',
        text
    )
    if m:
        fm["candidates"] = int(m.group(1))
        fm["triage_passed"] = int(m.group(2))
        fm["briefed"] = int(m.group(3))
        fm["mentions"] = int(m.group(4))

    # top_score: máximo score encontrado
    scores = re.findall(r'\*\*Score:\*\*\s*([\d.]+)', text)
    if scores:
        fm["top_score"] = max(float(s) for s in scores)

    # categories_covered
    cats = re.findall(r'\*\*Categoría:\*\*\s*([\w-]+)', text)
    if cats:
        fm["categories_covered"] = sorted(set(cats))

    return fm, text


def run_add_dailies(briefs_dir, dry_run=False):
    """Añade frontmatter a todos los daily-briefings."""
    daily_dir = Path(briefs_dir) / "daily-briefings"
    if not daily_dir.exists():
        print("  No se encontró daily-briefings/")
        return {"processed": 0, "enriched": 0, "errors": 0}

    stats = {"processed": 0, "enriched": 0, "errors": 0}

    for md in sorted(daily_dir.glob("*.md")):
        stats["processed"] += 1
        try:
            fm, text = extract_daily_frontmatter(md)
            if fm is None:
                continue  # ya tiene frontmatter

            content = dump_frontmatter(fm, text)
            if not dry_run:
                md.write_text(content, encoding="utf-8")

            stats["enriched"] += 1
            prefix = "[DRY-RUN] " if dry_run else ""
            print(f"  {prefix}{md.name}: +frontmatter ({fm.get('briefed', '?')} briefs, top {fm.get('top_score', '?')})")
        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR {md.name}: {e}", file=sys.stderr)

    return stats


# ──────────────────────────────────────────────────────────────────────────────
# Añadir frontmatter a weekly-digests
# ──────────────────────────────────────────────────────────────────────────────

def extract_weekly_frontmatter(filepath):
    """Extrae metadatos de un weekly-digest desde su contenido."""
    path = Path(filepath)
    text = path.read_text(encoding="utf-8", errors="replace")

    # Ya tiene frontmatter → skip
    if text.startswith("---\n"):
        return None, None

    fm = {"type": "weekly-digest"}

    # date_start, date_end: "2026-05-09 a 2026-05-15" o "2026-04-25 → 2026-05-01"
    m = re.search(r'(\d{4}-\d{2}-\d{2})\s+[a→]+\s+(\d{4}-\d{2}-\d{2})', text)
    if m:
        fm["date_start"] = m.group(1)
        fm["date_end"] = m.group(2)
    else:
        # Fallback: del nombre de fichero (solo date_end)
        m = re.search(r'(\d{4}-\d{2}-\d{2})', path.name)
        if m:
            fm["date_end"] = m.group(1)

    # videos_scanned: varias variantes
    for pattern in [
        r'[Vv]ídeos escaneados[^:]*:\*?\*?\s*(\d+)',
        r'[Vv]ídeos evaluados[^:]*:\*?\*?\s*(\d+)',
        r'[Vv]ídeos candidatos[^:]*:\*?\*?\s*(\d+)',
        r'[Cc]andidatos procesados[^:]*:\*?\*?\s*(\d+)',
    ]:
        m = re.search(pattern, text)
        if m:
            fm["videos_scanned"] = int(m.group(1))
            break

    # triage_passed
    for pattern in [
        r'[Pp]asaron triage[^:]*:\*?\*?\s*(\d+)',
        r'[Tt]riage aprobados[^:]*:\*?\*?\s*(\d+)',
    ]:
        m = re.search(pattern, text)
        if m:
            fm["triage_passed"] = int(m.group(1))
            break

    # briefed: varias variantes
    for pattern in [
        r'[Ss]eleccionados para briefing[^:]*:\*?\*?\s*(\d+)\s*\(media score:\s*([\d.]+)\)',
        r'[Ss]eleccionados para briefing[^:]*:\*?\*?\s*(\d+)',
        r'[Bb]riefs individuales[^:]*:\*?\*?\s*(\d+)',
        r'\*\*(\d+)\s*briefados?\*?\*?\s*\(media score:\s*([\d.]+)\)',
        r'\*\*(\d+)\s*briefados?\*?\*?',
    ]:
        m = re.search(pattern, text)
        if m:
            fm["briefed"] = int(m.group(1))
            if m.lastindex and m.lastindex >= 2:
                fm["avg_score"] = float(m.group(2))
            break

    # avg_score: fallback si no se capturó arriba
    if "avg_score" not in fm:
        for pattern in [
            r'[Ss]core medio[^:]*:\*?\*?\s*([\d.]+)',
            r'[Mm]edia score[^:]*:\*?\*?\s*([\d.]+)',
        ]:
            m = re.search(pattern, text)
            if m:
                fm["avg_score"] = float(m.group(1))
                break

    # mentions
    m = re.search(r'[Mm]enciones[^:]*:\*?\*?\s*(\d+)', text)
    if m:
        fm["mentions"] = int(m.group(1))

    # categories_covered: lista "  - category: N briefs/vídeos" o tabla "| category | N |"
    cats = re.findall(r'^\s+- ([\w-]+):\s*\d+', text, re.MULTILINE)
    if not cats:
        # Formato tabla: | category | N | score |
        cats = re.findall(r'^\|\s*([\w-]+)\s*\|', text, re.MULTILINE)
        # Filtrar headers de tabla
        cats = [c for c in cats if c not in ("Categoría", "---")]
    if cats:
        fm["categories_covered"] = sorted(set(cats))

    return fm, text


def run_add_weeklies(briefs_dir, dry_run=False):
    """Añade frontmatter a todos los weekly-digests."""
    weekly_dir = Path(briefs_dir) / "weekly-digests"
    if not weekly_dir.exists():
        print("  No se encontró weekly-digests/")
        return {"processed": 0, "enriched": 0, "errors": 0}

    stats = {"processed": 0, "enriched": 0, "errors": 0}

    for md in sorted(weekly_dir.glob("*.md")):
        stats["processed"] += 1
        try:
            fm, text = extract_weekly_frontmatter(md)
            if fm is None:
                continue

            content = dump_frontmatter(fm, text)
            if not dry_run:
                md.write_text(content, encoding="utf-8")

            stats["enriched"] += 1
            prefix = "[DRY-RUN] " if dry_run else ""
            print(f"  {prefix}{md.name}: +frontmatter ({fm.get('briefed', '?')} briefs, avg {fm.get('avg_score', '?')})")
        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR {md.name}: {e}", file=sys.stderr)

    return stats


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Migración de frontmatter OPENLAB Radar")
    parser.add_argument("--briefs-dir", required=True, help="Ruta al directorio briefs/")
    parser.add_argument("--mode", required=True,
                        choices=["enrich-briefs", "add-dailies", "add-weeklies", "all"],
                        help="Modo de migración")
    parser.add_argument("--dry-run", action="store_true",
                        help="Mostrar cambios sin escribir ficheros")
    args = parser.parse_args()

    briefs_dir = Path(args.briefs_dir)
    if not briefs_dir.exists():
        print(f"Error: {briefs_dir} no existe", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print("=== MODO DRY-RUN (no se escribirán cambios) ===\n")

    all_stats = []

    if args.mode in ("enrich-briefs", "all"):
        print("--- Enriqueciendo briefs de categoría ---")
        stats = run_enrich_briefs(briefs_dir, args.dry_run)
        all_stats.append(("Briefs categoría", stats))
        print(f"\n  Procesados: {stats['processed']} | Enriquecidos: {stats['enriched']} | Errores: {stats['errors']}")
        if stats["fields"]:
            print(f"  Campos añadidos: {stats['fields']}")
        print()

    if args.mode in ("add-dailies", "all"):
        print("--- Añadiendo frontmatter a daily-briefings ---")
        stats = run_add_dailies(briefs_dir, args.dry_run)
        all_stats.append(("Daily briefings", stats))
        print(f"\n  Procesados: {stats['processed']} | Con frontmatter: {stats['enriched']} | Errores: {stats['errors']}\n")

    if args.mode in ("add-weeklies", "all"):
        print("--- Añadiendo frontmatter a weekly-digests ---")
        stats = run_add_weeklies(briefs_dir, args.dry_run)
        all_stats.append(("Weekly digests", stats))
        print(f"\n  Procesados: {stats['processed']} | Con frontmatter: {stats['enriched']} | Errores: {stats['errors']}\n")

    # Resumen final
    total_enriched = sum(s["enriched"] for _, s in all_stats)
    total_errors = sum(s["errors"] for _, s in all_stats)
    print(f"=== TOTAL: {total_enriched} ficheros modificados, {total_errors} errores ===")

    if args.dry_run and total_enriched > 0:
        print("\nPara aplicar los cambios, ejecuta sin --dry-run")


if __name__ == "__main__":
    main()
