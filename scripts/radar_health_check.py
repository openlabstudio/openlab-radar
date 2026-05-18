#!/usr/bin/env python3
"""
OPENLAB Radar - Health Check (fitness functions arquitectónicas)
Genera informe de salud semanal con métricas computacionales.

Uso:
  python3 radar_health_check.py                          # informe completo
  python3 radar_health_check.py --alerts-only             # solo alertas por Telegram
  python3 radar_health_check.py --output path/report.md   # guardar en fichero específico
"""

import argparse
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "scripts"))

try:
    import yaml
except ImportError:
    yaml = None

from notify import send_status, _load_env


def parse_frontmatter(filepath):
    """Extrae frontmatter YAML de un brief markdown."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.+?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith("- "):
            # tag list item
            if "_current_key" in fm:
                fm.setdefault(fm["_current_key"], []).append(line[2:].strip().strip('"').strip("'"))
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val:
                fm[key] = val
            else:
                fm["_current_key"] = key
                fm.setdefault(key, [])
    fm.pop("_current_key", None)
    return fm


def load_briefs(briefs_dir):
    """Carga todos los briefs individuales (excluyendo daily-briefings y weekly-digests)."""
    briefs = []
    exclude = {"daily-briefings", "weekly-digests"}
    for cat_dir in sorted(briefs_dir.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name in exclude:
            continue
        for md in cat_dir.glob("*.md"):
            fm = parse_frontmatter(md)
            if fm and "date" in fm:
                fm["_category_dir"] = cat_dir.name
                fm["_path"] = str(md)
                briefs.append(fm)
    return briefs


def load_tags_yaml(tags_path):
    """Carga la lista oficial de tags desde tags.yaml."""
    if yaml:
        with open(tags_path) as f:
            data = yaml.safe_load(f)
        all_tags = set()
        for group_tags in data.values():
            if isinstance(group_tags, list):
                all_tags.update(group_tags)
        return all_tags
    # Fallback sin PyYAML
    all_tags = set()
    with open(tags_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                tag = line[2:].strip().split("#")[0].strip()
                if tag:
                    all_tags.add(tag)
    return all_tags


def load_channels_yaml(channels_path):
    """Carga la lista de canales monitorizados."""
    channels = []
    if yaml:
        with open(channels_path) as f:
            data = yaml.safe_load(f)
        return data.get("channels", [])
    # Fallback sin PyYAML
    with open(channels_path) as f:
        current = {}
        for line in f:
            stripped = line.strip()
            if stripped.startswith("- handle:"):
                if current:
                    channels.append(current)
                current = {"handle": stripped.split(":", 1)[1].strip().strip('"')}
            elif ":" in stripped and current:
                k, _, v = stripped.partition(":")
                current[k.strip()] = v.strip().strip('"')
        if current:
            channels.append(current)
    return channels


def bar(value, max_value, width=20):
    if max_value == 0:
        return ""
    filled = int(round(value / max_value * width))
    return "\u2501" * filled


def coverage_report(briefs, today):
    """Cobertura por categoría (7d, 30d, total)."""
    d7 = (today - timedelta(days=7)).isoformat()
    d30 = (today - timedelta(days=30)).isoformat()

    categories = defaultdict(lambda: {"7d": 0, "30d": 0, "total": 0})
    for b in briefs:
        cat = b.get("category", b.get("_category_dir", "unknown"))
        d = str(b.get("date", ""))
        categories[cat]["total"] += 1
        if d >= d30:
            categories[cat]["30d"] += 1
        if d >= d7:
            categories[cat]["7d"] += 1

    alerts = []
    lines = []
    max_total = max((v["total"] for v in categories.values()), default=1)
    total_30d = sum(v["30d"] for v in categories.values())

    lines.append(f"{'Categoría':<25} {'7d':>4} {'30d':>5} {'Total':>6}   Tendencia")
    lines.append("-" * 70)
    for cat in sorted(categories):
        v = categories[cat]
        b_str = bar(v["total"], max_total)
        flags = ""
        if v["7d"] == 0:
            flags = "  !! sin cobertura 7d"
            alerts.append(f"{cat}: 0 briefs en los ultimos 7 dias")
        if total_30d > 0 and v["30d"] / total_30d > 0.5:
            flags = "  !! >50% del mes"
            alerts.append(f"{cat}: concentra >{int(v['30d']/total_30d*100)}% de los briefs del mes")
        lines.append(f"{cat:<25} {v['7d']:>4} {v['30d']:>5} {v['total']:>6}   {b_str}{flags}")

    return "\n".join(lines), alerts


def score_report(briefs, today):
    """Distribución de scores."""
    d7 = (today - timedelta(days=7)).isoformat()
    d30 = (today - timedelta(days=30)).isoformat()
    prev_month_start = (today - timedelta(days=60)).isoformat()

    scores_7d, scores_30d, scores_prev, scores_all = [], [], [], []
    for b in briefs:
        try:
            s = float(b.get("score", 0))
        except (ValueError, TypeError):
            continue
        d = str(b.get("date", ""))
        scores_all.append(s)
        if d >= d7:
            scores_7d.append(s)
        if d >= d30:
            scores_30d.append(s)
        if d30 > d >= prev_month_start:
            scores_prev.append(s)

    def avg(lst):
        return sum(lst) / len(lst) if lst else 0

    alerts = []
    avg_7d = avg(scores_7d)
    avg_30d = avg(scores_30d)
    avg_prev = avg(scores_prev)
    avg_all = avg(scores_all)

    # Distribución
    buckets = {"9-10": 0, "7-8": 0, "5-6": 0, "<5": 0}
    for s in scores_all:
        if s >= 9:
            buckets["9-10"] += 1
        elif s >= 7:
            buckets["7-8"] += 1
        elif s >= 5:
            buckets["5-6"] += 1
        else:
            buckets["<5"] += 1

    total = len(scores_all) or 1
    lines = []
    lines.append(f"Score medio (7d):  {avg_7d:.1f}  |  30d: {avg_30d:.1f}  |  Total: {avg_all:.1f}")
    lines.append("")
    lines.append("Distribucion:")
    for label, count in buckets.items():
        pct = count / total * 100
        b = "\u2588" * int(round(pct / 3))
        lines.append(f"  {label:>5}: {b} {pct:.0f}% ({count})")

    # Alertas
    if scores_prev and avg_30d - avg_prev > 0.5:
        alerts.append(f"Score medio subio +{avg_30d - avg_prev:.1f} vs mes anterior (posible inflacion)")
    pct_78 = buckets["7-8"] / total * 100
    if pct_78 > 80:
        alerts.append(f"{pct_78:.0f}% de briefs en rango 7-8 (falta discriminacion)")

    return "\n".join(lines), alerts


def tags_report(briefs, official_tags, today):
    """Salud de tags."""
    d30 = (today - timedelta(days=30)).isoformat()
    tag_counts_all = Counter()
    tag_counts_30d = Counter()
    tag_combos = Counter()

    for b in briefs:
        tags = b.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        tag_counts_all.update(tags)
        d = str(b.get("date", ""))
        if d >= d30:
            tag_counts_30d.update(tags)
        if len(tags) >= 2:
            for i in range(len(tags)):
                for j in range(i + 1, len(tags)):
                    pair = tuple(sorted([tags[i], tags[j]]))
                    tag_combos[pair] += 1

    alerts = []
    lines = []

    # Tags oficiales sin uso en 30d
    unused_30d = sorted(official_tags - set(tag_counts_30d.keys()))
    if unused_30d:
        lines.append("Tags sin uso (30d): " + ", ".join(unused_30d))
        alerts.append(f"{len(unused_30d)} tags oficiales sin uso en 30d: {', '.join(unused_30d[:5])}")

    # Tags no oficiales encontrados en briefs
    unofficial = sorted(set(tag_counts_all.keys()) - official_tags)
    if unofficial:
        lines.append("Tags no oficiales encontrados: " + ", ".join(unofficial))

    # Top 10 tags
    lines.append("")
    lines.append("Top 10 tags (total):")
    for tag, count in tag_counts_all.most_common(10):
        lines.append(f"  {tag:<30} {count}")

    return "\n".join(lines), alerts


def channel_report(db_path, monitored_channels, briefs, today):
    """Rendimiento de canales."""
    d30 = (today - timedelta(days=30)).isoformat()
    conn = sqlite3.connect(db_path)

    lines = []
    alerts = []

    # Contar briefs por canal (source en frontmatter) en 30d
    brief_channels_30d = Counter()
    for b in briefs:
        d = str(b.get("date", ""))
        if d >= d30:
            source = b.get("source", "")
            if source:
                brief_channels_30d[source] += 1

    # Monitorizados: nombre -> handle
    monitored_names = {ch.get("name", "") for ch in monitored_channels}

    # Scrape count por canal (30d) — solo monitorizados + top 10 por volumen
    rows = conn.execute("""
        SELECT channel_name,
               COUNT(*) as total
        FROM videos
        WHERE discovered_at >= ?
        GROUP BY channel_name
        ORDER BY total DESC
    """, (d30,)).fetchall()

    # Filtrar: monitorizados + top 10 por scrape
    top_scrape = {row[0] for row in rows[:10]}
    relevant = monitored_names | top_scrape | set(brief_channels_30d.keys())
    scrape_map = {name: total for name, total in rows}

    lines.append(f"{'Canal':<35} {'Scrape':>6} {'Briefs':>7} {'Ratio':>6}")
    lines.append("-" * 60)

    # Ordenar por scrape desc, filtrar ruido (>= 2 scrapes o monitorizados o con briefs)
    shown = sorted(relevant, key=lambda n: scrape_map.get(n, 0), reverse=True)
    for name in shown:
        if not name:
            continue
        scraped = scrape_map.get(name, 0)
        briefed = brief_channels_30d.get(name, 0)
        # Saltar canales con poco volumen y no monitorizados
        if scraped < 3 and name not in monitored_names and briefed < 2:
            continue
        ratio = f"{briefed/scraped*100:.0f}%" if scraped else ("-" if not briefed else "manual")
        flag = ""
        if scraped >= 10 and briefed == 0:
            flag = "  !! alto ruido"
            alerts.append(f"Canal '{name}': {scraped} scrapeados, 0 briefs en 30d")
        lines.append(f"{name:<35} {scraped:>6} {briefed:>7} {ratio:>6}{flag}")

    # Canales monitorizados sin apariciones
    seen_names = set(scrape_map.keys())
    missing = sorted(monitored_names - seen_names - {""})
    if missing:
        lines.append("")
        lines.append("Canales monitorizados sin videos en 30d: " + ", ".join(missing))

    conn.close()
    return "\n".join(lines), alerts


def pipeline_report(logs_dir, today):
    """Tasa de fallos del pipeline."""
    d30 = today - timedelta(days=30)
    alerts = []
    lines = []

    # Días con briefing (buscamos logs run-YYYY-MM-DD.log)
    days_with_log = set()
    days_expected = set()
    for i in range(30):
        d = d30 + timedelta(days=i + 1)
        days_expected.add(d.strftime("%Y-%m-%d"))
        log_file = logs_dir / f"run-{d.strftime('%Y-%m-%d')}.log"
        if log_file.exists():
            days_with_log.add(d.strftime("%Y-%m-%d"))

    missing_days = sorted(days_expected - days_with_log)
    lines.append(f"Dias con ejecucion (30d): {len(days_with_log)}/{len(days_expected)}")
    if missing_days:
        lines.append(f"Dias sin log: {', '.join(missing_days[-10:])}")
        if len(missing_days) > 3:
            alerts.append(f"{len(missing_days)} dias sin ejecucion del pipeline en 30d")

    # Recovery runs
    recovery_log = logs_dir / "cron-recovery.log"
    recovery_count = 0
    if recovery_log.exists():
        content = recovery_log.read_text(encoding="utf-8", errors="replace")
        for line in content.splitlines():
            if d30.strftime("%Y-%m") in line or today.strftime("%Y-%m") in line:
                recovery_count += 1
    lines.append(f"Invocaciones recovery (30d): {recovery_count}")

    return "\n".join(lines), alerts


def generate_report(briefs, official_tags, db_path, monitored_channels, logs_dir, today):
    """Genera el informe completo."""
    sections = []
    all_alerts = []

    sections.append(f"# Radar Health Check — {today.strftime('%Y-%m-%d')}")
    sections.append(f"Total briefs: {len(briefs)}")

    # Cobertura
    text, alerts = coverage_report(briefs, today)
    sections.append("\n## Cobertura por categoria\n")
    sections.append(text)
    all_alerts.extend(alerts)

    # Scores
    text, alerts = score_report(briefs, today)
    sections.append("\n## Distribucion de scores\n")
    sections.append(text)
    all_alerts.extend(alerts)

    # Tags
    text, alerts = tags_report(briefs, official_tags, today)
    sections.append("\n## Salud de tags\n")
    sections.append(text)
    all_alerts.extend(alerts)

    # Canales
    text, alerts = channel_report(db_path, monitored_channels, briefs, today)
    sections.append("\n## Rendimiento de canales (30d)\n")
    sections.append(text)
    all_alerts.extend(alerts)

    # Pipeline
    text, alerts = pipeline_report(logs_dir, today)
    sections.append("\n## Pipeline\n")
    sections.append(text)
    all_alerts.extend(alerts)

    # Resumen de alertas
    if all_alerts:
        sections.append("\n## Alertas\n")
        for a in all_alerts:
            sections.append(f"- {a}")

    return "\n".join(sections), all_alerts


def format_telegram_summary(today, alerts, brief_count):
    """Resumen corto para Telegram."""
    lines = [f"Radar Health Check — {today.strftime('%Y-%m-%d')}"]
    lines.append(f"Briefs totales: {brief_count}")
    if alerts:
        for a in alerts:
            lines.append(f"!! {a}")
    else:
        lines.append("Sin alertas")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="OPENLAB Radar - Health Check")
    parser.add_argument("--db", default=str(PROJECT_DIR / "data" / "radar.db"))
    parser.add_argument("--briefs", default=str(PROJECT_DIR / "briefs"))
    parser.add_argument("--tags", default=str(PROJECT_DIR / "config" / "tags.yaml"))
    parser.add_argument("--channels", default=str(PROJECT_DIR / "config" / "channels.yaml"))
    parser.add_argument("--logs", default=str(PROJECT_DIR / "data" / "logs"))
    parser.add_argument("--output", help="Guardar informe en fichero")
    parser.add_argument("--alerts-only", action="store_true",
                        help="Solo enviar alertas por Telegram (sin generar informe)")
    args = parser.parse_args()

    today = datetime.now().date()
    briefs_dir = Path(args.briefs)
    logs_dir = Path(args.logs)

    briefs = load_briefs(briefs_dir)
    official_tags = load_tags_yaml(args.tags)
    monitored_channels = load_channels_yaml(args.channels)

    report, alerts = generate_report(
        briefs, official_tags, args.db, monitored_channels, logs_dir, today
    )

    if args.alerts_only:
        _load_env()
        if alerts:
            msg = format_telegram_summary(today, alerts, len(briefs))
            ok = send_status(msg)
            sys.exit(0 if ok else 1)
        else:
            print("Sin alertas.")
            sys.exit(0)

    # Informe completo
    output_path = args.output
    if not output_path:
        output_dir = PROJECT_DIR / "data" / "health-reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / f"{today.isoformat()}-health.md")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(report, encoding="utf-8")
    print(f"Informe guardado: {output_path}")

    # Enviar resumen por Telegram
    _load_env()
    msg = format_telegram_summary(today, alerts, len(briefs))
    send_status(msg)

    print(report)


if __name__ == "__main__":
    main()
