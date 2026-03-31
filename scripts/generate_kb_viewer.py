#!/usr/bin/env python3
"""
OPENLAB Radar — Generador de KB Viewer HTML
Genera un dashboard HTML self-contained con todos los briefs e insights.

Uso:
    python3 scripts/generate_kb_viewer.py
    python3 scripts/generate_kb_viewer.py \\
        --briefs-dir ~/OPENLAB/inteligencia/radar/briefs \\
        --insights-dir ~/OPENLAB/inteligencia/radar/insights \\
        --output ~/OPENLAB/inteligencia/radar/kb_viewer.html
"""

import sys
import re
import json
import argparse
from pathlib import Path
from html import escape
from datetime import datetime, timedelta
from collections import Counter

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Logo extraído del email (mismo origen que md_to_email_html.py)
def _load_logo() -> str:
    try:
        email_script = Path(__file__).parent / "md_to_email_html.py"
        m = re.search(r'LOGO_SRC\s*=\s*"(data:image/[^"]+)"', email_script.read_text())
        if m:
            return m.group(1)
    except Exception:
        pass
    return ""

# ──────────────────────────────────────────────────────────────────────────────
# Metadatos de categorías
# ──────────────────────────────────────────────────────────────────────────────
CATEGORY_META = {
    "agentic-systems":      ("", "Agentic Systems"),
    "claude-code-advanced": ("", "Claude Code Advanced"),
    "delivery-adoption":    ("", "Delivery & Adoption"),
    "context-engineering":  ("", "Context Engineering"),
    "cli-vs-platforms":     ("", "CLI vs Platforms"),
    "enterprise-ai":        ("", "Enterprise AI"),
}
CAT_DEFAULT = ("", "General")


# ──────────────────────────────────────────────────────────────────────────────
# Parsers
# ──────────────────────────────────────────────────────────────────────────────
def parse_frontmatter(path: Path):
    """Retorna (dict, body_str). Si no hay frontmatter válido → ({}, full_text)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r'^---\n(.*?)\n---\s*\n?(.*)', text, re.DOTALL)
    if not m:
        return {}, text

    fm = {}
    if HAS_YAML:
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except Exception:
            pass
    else:
        # Fallback sin pyyaml: parsear key: value simples
        for line in m.group(1).split('\n'):
            kv = re.match(r'^([\w-]+):\s*(.+)$', line)
            if kv:
                fm[kv.group(1)] = kv.group(2).strip().strip('"\'')
    return fm, m.group(2)


def extract_title_from_body(body: str) -> str:
    m = re.search(r'^#+\s+(.+)$', body, re.MULTILINE)
    return m.group(1).strip() if m else ""


def extract_excerpt(body: str, max_chars: int = 300) -> str:
    """Extrae el primer texto narrativo del cuerpo del brief."""
    lines = []
    total = 0
    for line in body.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        if line.startswith('**Telegraph'):
            continue
        if line.startswith('---'):
            continue
        if re.match(r'^[-*]\s+\*\*', line):  # líneas de metadatos tipo "- **Score:** 8.5"
            continue
        lines.append(line)
        total += len(line)
        if total >= max_chars:
            break
    text = ' '.join(lines)
    return text[:max_chars] + ('…' if len(text) > max_chars else '')


def extract_telegraph_url(body: str) -> str:
    m = re.search(r'\*\*Telegraph:\*\*\s*(https://telegra\.ph/\S+)', body)
    return m.group(1) if m else ""


def parse_brief(path: Path) -> dict:
    fm, body = parse_frontmatter(path)

    title = str(fm.get('title', '')).strip() or extract_title_from_body(body) or path.stem

    date_val = fm.get('date', '')
    if date_val:
        date_str = str(date_val)[:10]
    else:
        dm = re.match(r'(\d{4}-\d{2}-\d{2})', path.stem)
        date_str = dm.group(1) if dm else ""

    category = str(fm.get('category', '')).strip() or path.parent.name

    try:
        score = float(fm.get('score', 0) or 0)
    except (TypeError, ValueError):
        score = 0.0

    tags_raw = fm.get('tags', [])
    if isinstance(tags_raw, list):
        tags = [str(t).strip() for t in tags_raw if t]
    elif isinstance(tags_raw, str):
        tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
    else:
        tags = []

    return {
        "title": title,
        "date": date_str,
        "category": category,
        "score": score,
        "tags": tags,
        "source": str(fm.get('source', '')).strip(),
        "url": str(fm.get('url', '')).strip(),
        "telegraph_url": extract_telegraph_url(body),
        "excerpt": extract_excerpt(body),
    }


def parse_insight(path: Path) -> dict:
    fm, body = parse_frontmatter(path)
    title = str(fm.get('title', '')).strip() or extract_title_from_body(body) or path.stem
    date_val = fm.get('date', '')
    if date_val:
        date_str = str(date_val)[:10]
    else:
        dm = re.match(r'(\d{4}-\d{2}-\d{2})', path.stem)
        date_str = dm.group(1) if dm else ""
    return {
        "title": title,
        "date": date_str,
        "excerpt": extract_excerpt(body, 400),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Collectors
# ──────────────────────────────────────────────────────────────────────────────
def collect_all_briefs(briefs_dir: Path) -> list:
    if not briefs_dir.exists():
        return []
    result = []
    for md in sorted(briefs_dir.rglob("*.md")):
        if 'daily-briefings' in md.parts:
            continue
        try:
            result.append(parse_brief(md))
        except Exception as e:
            print(f"WARN: Error parseando {md}: {e}", file=sys.stderr)
    return result


def collect_all_insights(insights_dir: Path) -> list:
    if not insights_dir.exists():
        return []
    result = []
    for md in sorted(insights_dir.rglob("*.md"), reverse=True):
        try:
            result.append(parse_insight(md))
        except Exception as e:
            print(f"WARN: Error parseando {md}: {e}", file=sys.stderr)
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Stats
# ──────────────────────────────────────────────────────────────────────────────
def is_recent(date_str: str, days: int = 7) -> bool:
    if not date_str:
        return False
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d >= datetime.now() - timedelta(days=days)
    except ValueError:
        return False


def compute_stats(briefs: list, insights: list) -> dict:
    scores = [b["score"] for b in briefs if b["score"] > 0]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
    last_date = max((b["date"] for b in briefs if b["date"]), default="")
    by_category = dict(Counter(b["category"] for b in briefs))
    tag_counts = dict(Counter(t for b in briefs for t in b["tags"]).most_common(40))

    hot = sorted(
        [b for b in briefs if is_recent(b["date"], 7) and b["score"] >= 8.0],
        key=lambda x: x["score"],
        reverse=True,
    )[:5]

    return {
        "total_briefs": len(briefs),
        "total_insights": len(insights),
        "avg_score": avg_score,
        "last_date": last_date,
        "by_category": by_category,
        "tag_counts": tag_counts,
        "hot_signals": hot,
    }


# ──────────────────────────────────────────────────────────────────────────────
# HTML
# ──────────────────────────────────────────────────────────────────────────────
def build_html(briefs: list, insights: list, stats: dict, generated_at: str) -> str:
    data_blob = json.dumps(
        {"briefs": briefs, "insights": insights, "stats": stats},
        ensure_ascii=False,
        default=str,
    )
    cat_names_js = json.dumps({k: v[1] for k, v in CATEGORY_META.items()})
    cat_icons_js = json.dumps({k: v[0] for k, v in CATEGORY_META.items()})
    nb = len(briefs)
    ni = len(insights)
    logo_src = _load_logo()
    logo_html = (
        f'<img src="{logo_src}" alt="OPENLAB" height="48" style="display:block;height:48px;width:auto;">'
        if logo_src else
        '<span style="font-size:28px;font-weight:900;letter-spacing:.1em;color:#CCFF00;font-family:Montserrat,Arial,sans-serif;">OPENLAB_</span>'
    )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<title>OPENLAB Radar Viewer</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#F3F4F6;--surface:#FFFFFF;--s2:#F9FAFB;--s3:#F3F4F6;
  --accent:#CCFF00;--text:#111111;--muted:#6B7280;--border:#E5E7EB;
  --gh:#16A34A;--ghb:#DCFCE7;--gm:#D97706;--gmb:#FEF3C7;--gl:#DC2626;--glb:#FEE2E2;
}}
body{{background:var(--bg);color:var(--text);font-family:'Montserrat',Arial,sans-serif;font-size:14px;line-height:1.5}}
a{{color:inherit;text-decoration:none}}

/* ── HEADER ── */
.header-wrap{{padding:20px 24px 0;max-width:900px;margin:0 auto}}
.header{{background:#000;border-radius:12px;padding:24px 32px;display:flex;align-items:center;justify-content:space-between;gap:16px}}
.header-right{{text-align:right;line-height:1.2}}
.header-label{{font-size:11px;font-weight:900;letter-spacing:.2em;color:#CCFF00;text-transform:uppercase}}
.header-date{{font-size:11px;color:#9CA3AF;margin-top:4px}}

/* ── STATS BAR ── */
.stats-wrap{{max-width:900px;margin:20px auto 0;padding:0 24px}}
.stats-bar{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
@media(max-width:600px){{.stats-bar{{grid-template-columns:repeat(2,1fr)}}}}
.stat-card{{background:#fff;border:1px solid var(--border);border-radius:10px;padding:16px 20px;text-align:center}}
.stat-num{{font-size:32px;font-weight:900;color:#111;line-height:1}}
.stat-label{{font-size:10px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-top:4px}}

/* ── SEARCH ── */
.search-wrap{{max-width:900px;margin:20px auto 0;padding:0 24px}}
.search-box{{background:#fff;border:2px solid var(--border);border-radius:10px;display:flex;align-items:center;gap:12px;padding:12px 18px;transition:border-color .15s}}
.search-box:focus-within{{border-color:#000}}
.search-icon{{font-size:18px;color:var(--muted);flex-shrink:0}}
#si{{flex:1;border:none;outline:none;font-family:'Montserrat',Arial,sans-serif;font-size:14px;font-weight:600;color:var(--text);background:transparent}}
#si::placeholder{{color:#C4C9D4;font-weight:400}}

/* ── MAIN ── */
main{{max-width:900px;margin:32px auto 0;padding:0 24px 64px}}
section{{margin-bottom:48px}}
.sh{{display:flex;align-items:baseline;gap:10px;margin-bottom:20px}}
.sh-line{{width:4px;height:20px;background:#000;border-radius:2px;flex-shrink:0;align-self:center}}
.st{{font-size:16px;font-weight:800;color:#111}}
.ss{{font-size:12px;color:var(--muted)}}

/* ── GRID ── */
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}}

/* ── CARD ── */
.card{{background:#fff;border:1px solid var(--border);border-left:5px solid #000;border-radius:0 8px 8px 0;display:flex;overflow:hidden;transition:box-shadow .15s}}
.card:hover{{box-shadow:0 4px 16px rgba(0,0,0,.10)}}
.card-body{{padding:16px;flex:1;min-width:0}}
.ct{{font-size:13px;font-weight:700;margin-bottom:8px;line-height:1.4;color:#111}}
.ct a:hover{{color:#000;text-decoration:underline}}
.cm{{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-bottom:6px}}
.bc{{background:#000;color:#CCFF00;font-size:9px;font-weight:800;padding:2px 7px;border-radius:3px;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap}}
.bs{{font-size:11px;font-weight:800;padding:2px 7px;border-radius:3px;white-space:nowrap}}
.bd{{font-size:10px;color:var(--muted)}}
.csrc{{font-size:11px;color:var(--muted);margin-bottom:5px}}
.cx{{font-size:12px;color:#374151;line-height:1.55;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}}
.tr{{margin-top:8px;display:flex;flex-wrap:wrap;gap:4px}}
.tp{{background:var(--s3);border:1px solid var(--border);color:var(--muted);font-size:10px;padding:2px 6px;border-radius:3px;cursor:pointer;transition:background .1s,color .1s}}
.tp:hover{{background:#000;color:#CCFF00;border-color:#000}}
.cl{{margin-top:10px;display:flex;gap:8px}}
.lyt{{font-size:10px;font-weight:700;padding:3px 9px;border-radius:3px;text-transform:uppercase;letter-spacing:.05em;background:#DC2626;color:#fff}}
.ltg{{font-size:10px;font-weight:700;padding:3px 9px;border-radius:3px;text-transform:uppercase;letter-spacing:.05em;background:#2AABEE;color:#fff}}

/* ── LISTA ── */
.list{{display:flex;flex-direction:column;gap:0}}
.lday{{font-size:11px;font-weight:700;color:#111;text-transform:uppercase;letter-spacing:.08em;padding:12px 0 4px;border-bottom:2px solid #000;margin-bottom:4px}}
.li{{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:5px;transition:background .1s}}
.li:hover{{background:#fff}}
.lit{{flex:1;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#111}}
.lit a:hover{{color:#000;text-decoration:underline}}

/* ── TABS ── */
.tabs-bar{{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:20px;border-bottom:2px solid var(--border);padding-bottom:0}}
.tb{{background:transparent;border:none;border-bottom:3px solid transparent;margin-bottom:-2px;color:var(--muted);font-family:'Montserrat',Arial,sans-serif;font-size:12px;font-weight:700;padding:8px 14px;cursor:pointer;transition:color .15s,border-color .15s;white-space:nowrap}}
.tb:hover{{color:#111}}
.tb.active{{color:#111;border-bottom-color:#000}}
.tc{{display:none}}
.tc.active{{display:block}}
.ch{{display:flex;gap:16px;align-items:center;margin-bottom:16px;padding:12px 16px;background:#fff;border-radius:8px;border:1px solid var(--border);border-left:5px solid #000}}
.cc{{font-size:28px;font-weight:900;color:#111}}
.cm2{{font-size:11px;color:var(--muted)}}
.cm2 strong{{color:#111}}

/* ── TAG CLOUD ── */
#tc{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px}}
.ct2{{cursor:pointer;border-radius:4px;padding:4px 10px;font-weight:700;transition:background .1s,color .1s,transform .1s;border:1px solid #D1D5DB;color:#374151}}
.ct2:hover,.ct2.sel{{background:#000!important;color:#CCFF00!important;border-color:#000!important;transform:scale(1.05)}}

/* ── INSIGHTS ── */
.ic{{background:#fff;border:1px solid var(--border);border-left:5px solid #6366F1;border-radius:0 8px 8px 0;padding:16px;transition:border-left-color .15s}}
.ic:hover{{border-left-color:#000}}
.itl{{font-size:14px;font-weight:700;margin-bottom:4px;color:#111}}
.id{{font-size:11px;color:var(--muted);margin-bottom:6px}}
.ix{{font-size:12px;color:#374151;line-height:1.5}}

/* ── MISC ── */
.empty{{text-align:center;padding:40px;color:var(--muted);font-size:13px;border:2px dashed var(--border);border-radius:8px;background:#fff}}
.xbtn{{background:#fff;border:2px solid #000;color:#111;font-family:'Montserrat',Arial,sans-serif;font-size:11px;font-weight:700;padding:6px 16px;border-radius:4px;cursor:pointer;margin-top:12px;transition:background .1s,color .1s}}
.xbtn:hover{{background:#000;color:#CCFF00}}
#ss{{display:none;margin-bottom:32px}}
footer{{text-align:center;padding:24px;color:var(--muted);font-size:11px;border-top:1px solid var(--border);background:var(--bg)}}
footer strong{{color:#111}}
@media(max-width:600px){{
  .stats-bar{{grid-template-columns:repeat(2,1fr)}}
  main,.stats-wrap,.search-wrap,.header-wrap{{padding-left:16px;padding-right:16px}}
  .grid{{grid-template-columns:1fr}}
  .header{{padding:20px}}
}}
</style>
</head>
<body>

<div class="header-wrap">
  <div class="header">
    {logo_html}
    <div class="header-right">
      <div class="header-label">Radar Viewer</div>
      <div class="header-date">{escape(generated_at)}</div>
    </div>
  </div>
</div>

<div class="stats-wrap">
  <div class="stats-bar">
    <div class="stat-card"><div class="stat-num" id="s-total">—</div><div class="stat-label">Briefs</div></div>
    <div class="stat-card"><div class="stat-num" id="s-score">—</div><div class="stat-label">Score medio</div></div>
    <div class="stat-card"><div class="stat-num" id="s-week">—</div><div class="stat-label">Esta semana</div></div>
    <div class="stat-card"><div class="stat-num" id="s-ins">—</div><div class="stat-label">Insights</div></div>
  </div>
</div>

<div class="search-wrap">
  <div class="search-box">
    <span class="search-icon">🔍</span>
    <input type="search" id="si" placeholder="Buscar en los briefs…" autocomplete="off">
  </div>
</div>

<main>

  <!-- Búsqueda -->
  <section id="ss">
    <div class="sh"><div class="sh-line"></div><span class="st">Resultados de búsqueda</span><span class="ss" id="s-count"></span></div>
    <div id="s-res" class="grid"></div>
  </section>

  <!-- Hot Signals -->
  <section>
    <div class="sh"><div class="sh-line"></div><span class="st">Hot Signals</span><span class="ss">Score ≥ 8.0 · últimos 7 días</span></div>
    <div id="hot" class="grid"><div class="empty">Sin briefs con score ≥ 8.0 en los últimos 7 días.</div></div>
  </section>

  <!-- Nuevos esta semana -->
  <section>
    <div class="sh"><div class="sh-line"></div><span class="st">Nuevos esta semana</span><span class="ss" id="rec-sub"></span></div>
    <div id="rec" class="list"></div>
  </section>

  <!-- Por categoría -->
  <section>
    <div class="sh"><div class="sh-line"></div><span class="st">Por categoría</span><span class="ss">Click en la pestaña para explorar</span></div>
    <div class="tabs-bar" id="cat-tabs"></div>
    <div id="cat-contents"></div>
  </section>

  <!-- Tag Explorer -->
  <section id="tags-section">
    <div class="sh"><div class="sh-line"></div><span class="st">Tag Explorer</span><span class="ss">Click en un tag para filtrar</span></div>
    <div id="tc"></div>
    <div id="tag-results-wrap" style="display:none">
      <div class="ss" id="trc" style="margin-bottom:12px"></div>
      <div id="tag-res" class="grid"></div>
    </div>
  </section>

  <!-- Insights -->
  <section>
    <div class="sh"><div class="sh-line"></div><span class="st">Insights</span><span class="ss">Síntesis generadas bajo demanda</span></div>
    <div id="ins-grid" class="grid"><div class="empty">Sin insights generados todavía.</div></div>
  </section>

</main>

<footer>
  Generado por <strong>OPENLAB Radar</strong> · {escape(generated_at)} · {nb} brief{'s' if nb != 1 else ''} · {ni} insight{'s' if ni != 1 else ''}
</footer>

<script>
const KB={data_blob};
const CN={cat_names_js};
const CI={cat_icons_js};

function cn(c){{return(CI[c]||'📹')+' '+(CN[c]||c)}}
function sc(s){{return s>=8?'#16A34A':s>=7?'#D97706':s>0?'#DC2626':'#6B7280'}}
function sb(s){{return s>=8?'#DCFCE7':s>=7?'#FEF3C7':s>0?'#FEE2E2':'#F9FAFB'}}
function e(s){{return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}}
function recent(d,days){{if(!d)return false;return(new Date()-new Date(d))/86400000<=days}}

function scoreBadge(s){{
  if(!s)return'';
  return`<span class="bs" style="background:${{sb(s)}};color:${{sc(s)}};">${{s.toFixed(1)}}</span>`;
}}
function catBadge(c){{return`<span class="bc">${{e(CI[c]||'📹')}} ${{e(CN[c]||c)}}</span>`}}

const SKIP_TAGS=new Set(['youtube','brief','briefs','video','vídeo']);
function card(b){{
  const tags=b.tags.filter(t=>!SKIP_TAGS.has(t.toLowerCase())).map(t=>`<span class="tp" onclick="filterTag('${{e(t)}}')">${{e(t)}}</span>`).join('');
  const links=[];
  if(b.url)links.push(`<a class="lyt" href="${{e(b.url)}}" target="_blank">▶ YouTube</a>`);
  if(b.telegraph_url)links.push(`<a class="ltg" href="${{e(b.telegraph_url)}}" target="_blank">Ver resumen</a>`);
  return`<div class="card"><div class="card-body">
  <div class="ct"><a href="${{e(b.url||'#')}}" target="_blank">${{e(b.title)}}</a></div>
  <div class="cm">${{catBadge(b.category)}}${{scoreBadge(b.score)}}${{b.date?`<span class="bd">${{e(b.date)}}</span>`:''}}</div>
  ${{b.source?`<div class="csrc">por ${{e(b.source)}}</div>`:''}}
  ${{b.excerpt?`<div class="cx">${{e(b.excerpt)}}</div>`:''}}
  ${{tags?`<div class="tr">${{tags}}</div>`:''}}
  ${{links.length?`<div class="cl">${{links.join('')}}</div>`:''}}
</div></div>`}}

function listItem(b){{
  return`<div class="li">${{catBadge(b.category)}}<span class="lit"><a href="${{e(b.url||'#')}}" target="_blank">${{e(b.title)}}</a></span>${{scoreBadge(b.score)}}</div>`;
}}

// Stats
function initStats(){{
  const s=KB.stats;
  document.getElementById('s-total').textContent=s.total_briefs;
  document.getElementById('s-score').textContent=s.avg_score;
  document.getElementById('s-week').textContent=KB.briefs.filter(b=>recent(b.date,7)).length;
  document.getElementById('s-ins').textContent=s.total_insights;
}}

// Hot
function initHot(){{
  const h=KB.stats.hot_signals;
  if(!h||!h.length)return;
  document.getElementById('hot').innerHTML=h.map(card).join('');
}}

// Recientes
function initRecientes(){{
  const r=KB.briefs.filter(b=>recent(b.date,7)).sort((a,b)=>b.date.localeCompare(a.date));
  document.getElementById('rec-sub').textContent=r.length+' briefs';
  const el=document.getElementById('rec');
  if(!r.length){{el.innerHTML='<div class="empty">Sin briefs nuevos esta semana.</div>';return}}
  const byDay={{}};
  r.forEach(b=>{{const d=b.date||'Sin fecha';if(!byDay[d])byDay[d]=[];byDay[d].push(b)}});
  let html='';
  Object.keys(byDay).sort().reverse().forEach(d=>{{
    html+=`<div class="lday">${{e(d)}}</div>`;
    html+=byDay[d].map(listItem).join('');
  }});
  el.innerHTML=html;
}}

// Categorías
function initCats(){{
  const cats=[...new Set(KB.briefs.map(b=>b.category))].sort();
  const bar=document.getElementById('cat-tabs');
  const cont=document.getElementById('cat-contents');
  cats.forEach((cat,i)=>{{
    const briefs=KB.briefs.filter(b=>b.category===cat).sort((a,b)=>b.score-a.score);
    const avg=briefs.length?(briefs.reduce((s,b)=>s+b.score,0)/briefs.length).toFixed(1):'—';
    const btn=document.createElement('button');
    btn.className='tb'+(i===0?' active':'');
    btn.textContent=cn(cat);
    btn.dataset.cat=cat;
    btn.onclick=()=>showCat(cat);
    bar.appendChild(btn);
    const top=briefs.slice(0,3);
    const rest=briefs.slice(3);
    const rid='cr-'+cat.replace(/[^a-z0-9]/g,'');
    const div=document.createElement('div');
    div.className='tc'+(i===0?' active':'');
    div.id='t-'+cat;
    div.innerHTML=`<div class="ch"><div class="cc">${{briefs.length}}</div><div class="cm2">briefs en <strong>${{CN[cat]||cat}}</strong><br>Score medio: <strong>${{avg}}</strong></div></div><div class="grid">${{top.map(card).join('')}}</div>${{rest.length?`<button class="xbtn" onclick="toggleRest('${{rid}}',this)">Ver ${{rest.length}} más ↓</button><div id="${{rid}}" style="display:none;margin-top:16px"><div class="grid">${{rest.map(card).join('')}}</div></div>`:''}}`;
    cont.appendChild(div);
  }});
}}

function showCat(cat){{
  document.querySelectorAll('.tb').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.tc').forEach(c=>c.classList.remove('active'));
  document.querySelector(`[data-cat="${{cat}}"]`).classList.add('active');
  document.getElementById('t-'+cat).classList.add('active');
}}

function toggleRest(id,btn){{
  const el=document.getElementById(id);
  const open=el.style.display!=='none';
  el.style.display=open?'none':'block';
  const n=el.querySelectorAll('.card').length;
  btn.textContent=open?'Ver '+n+' más ↓':'Ver menos ↑';
}}

// Tags
function initTags(){{
  const tc=KB.stats.tag_counts;
  const tags=Object.entries(tc).filter(([t])=>!SKIP_TAGS.has(t.toLowerCase())).sort((a,b)=>b[1]-a[1]);
  const max=tags[0]?.[1]||1;
  const el=document.getElementById('tc');
  tags.forEach(([tag,count])=>{{
    const r=count/max;
    const span=document.createElement('span');
    span.className='ct2';
    span.textContent=tag+' ('+count+')';
    span.style.fontSize=Math.round(10+r*8)+'px';
    span.dataset.tag=tag;
    span.onclick=()=>filterTag(tag);
    el.appendChild(span);
  }});
}}

let _selectedTag=null;
function filterTag(tag){{
  if(_selectedTag===tag){{
    _selectedTag=null;
    document.querySelectorAll('.ct2').forEach(e=>e.classList.remove('sel'));
    document.getElementById('tag-results-wrap').style.display='none';
    return;
  }}
  _selectedTag=tag;
  document.querySelectorAll('.ct2').forEach(e=>e.classList.toggle('sel',e.dataset.tag===tag));
  const res=KB.briefs.filter(b=>b.tags.includes(tag)).sort((a,b)=>b.score-a.score);
  document.getElementById('trc').textContent=res.length+' brief'+(res.length!==1?'s':'')+' con el tag "'+tag+'"';
  document.getElementById('tag-res').innerHTML=res.length?res.map(card).join(''):'<div class="empty">Sin resultados para este tag.</div>';
  document.getElementById('tag-results-wrap').style.display='block';
  document.getElementById('tags-section').scrollIntoView({{behavior:'smooth',block:'start'}});
}}

// Insights
function initInsights(){{
  const el=document.getElementById('ins-grid');
  if(!KB.insights||!KB.insights.length)return;
  el.innerHTML=KB.insights.map(i=>`<div class="ic"><div class="itl">${{e(i.title)}}</div>${{i.date?`<div class="id">${{e(i.date)}}</div>`:''}}${{i.excerpt?`<div class="ix">${{e(i.excerpt)}}</div>`:''}}</div>`).join('');
}}

// Búsqueda
function initSearch(){{
  const inp=document.getElementById('si');
  inp.addEventListener('input',()=>{{
    const q=inp.value.trim();
    const sec=document.getElementById('ss');
    if(!q){{sec.style.display='none';return}}
    const re=new RegExp(q.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&'),'i');
    const found=KB.briefs.filter(b=>re.test(b.title)||re.test(b.source)||b.tags.some(t=>re.test(t))||re.test(b.excerpt)).sort((a,b)=>b.score-a.score);
    document.getElementById('s-count').textContent=found.length+' resultado'+(found.length!==1?'s':'');
    document.getElementById('s-res').innerHTML=found.length?found.map(card).join(''):'<div class="empty">Sin resultados.</div>';
    sec.style.display='block';
    sec.scrollIntoView({{behavior:'smooth',block:'start'}});
  }});
}}

document.addEventListener('DOMContentLoaded',()=>{{
  initStats();initHot();initRecientes();initCats();initTags();initInsights();initSearch();
}});
</script>
</body>
</html>"""


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="OPENLAB Radar — Generador de KB Viewer HTML")
    parser.add_argument("--briefs-dir", default=None, help="Directorio de briefs (default: <project>/briefs)")
    parser.add_argument("--insights-dir", default=None, help="Directorio de insights (default: <project>/insights)")
    parser.add_argument("--output", default=None, help="Ruta de salida del HTML (default: <project>/data/kb_viewer.html)")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    briefs_dir = Path(args.briefs_dir).expanduser() if args.briefs_dir else project_root / "briefs"
    insights_dir = Path(args.insights_dir).expanduser() if args.insights_dir else project_root / "insights"
    output = Path(args.output).expanduser() if args.output else project_root / "data" / "kb_viewer.html"

    print(f"Leyendo briefs desde:   {briefs_dir}")
    print(f"Leyendo insights desde: {insights_dir}")

    briefs = collect_all_briefs(briefs_dir)
    insights = collect_all_insights(insights_dir)

    print(f"Briefs encontrados:  {len(briefs)}")
    print(f"Insights encontrados: {len(insights)}")

    stats = compute_stats(briefs, insights)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M CET")

    html = build_html(briefs, insights, stats, generated_at)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(f"KB Viewer generado: {output}  ({len(html)//1024} KB)")


if __name__ == "__main__":
    main()
