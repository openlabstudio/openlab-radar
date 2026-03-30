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

# ──────────────────────────────────────────────────────────────────────────────
# Metadatos de categorías
# ──────────────────────────────────────────────────────────────────────────────
CATEGORY_META = {
    "agentic-systems":      ("🤖", "Agentic Systems"),
    "claude-code-advanced": ("⚡", "Claude Code Advanced"),
    "delivery-adoption":    ("🚀", "Delivery & Adoption"),
    "context-engineering":  ("🧠", "Context Engineering"),
    "cli-vs-platforms":     ("🔧", "CLI vs Platforms"),
    "enterprise-ai":        ("🏢", "Enterprise AI"),
}
CAT_DEFAULT = ("📹", "General")


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

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<title>OPENLAB Radar — Knowledge Base</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#000000;--surface:#0F0F23;--s2:#141414;--s3:#1e1e1e;
  --accent:#CCFF00;--text:#FFFFFF;--muted:#9CA3AF;--border:#2a2a2a;
  --gh:#16A34A;--ghb:#DCFCE7;--gm:#D97706;--gmb:#FEF3C7;--gl:#DC2626;--glb:#FEE2E2;
}}
body{{background:var(--bg);color:var(--text);font-family:'Montserrat',Arial,sans-serif;font-size:14px;line-height:1.5}}
a{{color:inherit;text-decoration:none}}
/* NAV */
#nav{{position:sticky;top:0;z-index:100;background:#000;border-bottom:2px solid var(--accent);padding:10px 24px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}}
.brand{{font-size:12px;font-weight:900;letter-spacing:.15em;color:var(--accent);white-space:nowrap}}
.brand span{{color:var(--muted);font-weight:400}}
.nav-stats{{display:flex;gap:20px;flex-wrap:wrap;flex:1}}
.ns{{font-size:10px;color:var(--muted);white-space:nowrap}}
.ns strong{{color:var(--accent);font-size:16px;font-weight:900;display:block;line-height:1.1}}
#si{{background:var(--s3);border:1px solid var(--border);color:var(--text);padding:7px 14px;border-radius:6px;font-family:'Montserrat',Arial,sans-serif;font-size:12px;width:200px;outline:none}}
#si:focus{{border-color:var(--accent)}}
#si::placeholder{{color:var(--muted)}}
/* MAIN */
main{{max-width:1200px;margin:0 auto;padding:32px 24px 64px}}
section{{margin-bottom:48px}}
.sh{{display:flex;align-items:baseline;gap:10px;margin-bottom:20px;border-left:3px solid var(--accent);padding-left:14px}}
.st{{font-size:17px;font-weight:800;color:var(--text)}}
.ss{{font-size:12px;color:var(--muted)}}
/* GRID */
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
/* CARD */
.card{{background:var(--s2);border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:8px;padding:16px;transition:background .1s}}
.card:hover{{background:var(--s3)}}
.ct{{font-size:13px;font-weight:700;margin-bottom:8px;line-height:1.4}}
.ct a:hover{{color:var(--accent)}}
.cm{{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-bottom:6px}}
.bc{{background:var(--accent);color:#000;font-size:10px;font-weight:800;padding:2px 7px;border-radius:3px;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap}}
.bs{{font-size:11px;font-weight:800;padding:2px 7px;border-radius:3px;white-space:nowrap}}
.bd{{font-size:10px;color:var(--muted);margin-left:auto}}
.csrc{{font-size:11px;color:var(--muted);margin-bottom:5px}}
.cx{{font-size:11px;color:var(--muted);line-height:1.5;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}}
.tr{{margin-top:8px;display:flex;flex-wrap:wrap;gap:4px}}
.tp{{background:var(--s3);border:1px solid var(--border);color:var(--muted);font-size:10px;padding:2px 6px;border-radius:3px;cursor:pointer;transition:background .1s,color .1s}}
.tp:hover{{background:var(--accent);color:#000}}
.cl{{margin-top:10px;display:flex;gap:8px}}
.lyt{{font-size:10px;font-weight:700;padding:3px 9px;border-radius:3px;text-transform:uppercase;letter-spacing:.05em;background:#DC2626;color:#fff}}
.ltg{{font-size:10px;font-weight:700;padding:3px 9px;border-radius:3px;text-transform:uppercase;letter-spacing:.05em;background:#2AABEE;color:#fff}}
/* LISTA */
.list{{display:flex;flex-direction:column;gap:0}}
.lday{{font-size:11px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.08em;padding:12px 0 4px;border-bottom:1px solid var(--border);margin-bottom:4px}}
.li{{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:5px;transition:background .1s}}
.li:hover{{background:var(--s3)}}
.lit{{flex:1;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.lit a:hover{{color:var(--accent)}}
/* TABS */
.tabs-bar{{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:20px;border-bottom:1px solid var(--border);padding-bottom:0}}
.tb{{background:transparent;border:none;border-bottom:2px solid transparent;margin-bottom:-1px;color:var(--muted);font-family:'Montserrat',Arial,sans-serif;font-size:12px;font-weight:600;padding:8px 14px;cursor:pointer;transition:color .15s,border-color .15s;white-space:nowrap}}
.tb:hover{{color:var(--text)}}
.tb.active{{color:var(--accent);border-bottom-color:var(--accent)}}
.tc{{display:none}}
.tc.active{{display:block}}
.ch{{display:flex;gap:16px;align-items:center;margin-bottom:16px;padding:12px 16px;background:var(--s2);border-radius:8px;border:1px solid var(--border)}}
.cc{{font-size:28px;font-weight:900;color:var(--accent)}}
.cm2{{font-size:11px;color:var(--muted)}}
.cm2 strong{{color:var(--text)}}
/* TAG CLOUD */
#tc{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px}}
.ct2{{cursor:pointer;border-radius:4px;padding:4px 10px;font-weight:700;transition:background .1s,color .1s,transform .1s;border:1px solid transparent}}
.ct2:hover,.ct2.sel{{background:var(--accent)!important;color:#000!important;transform:scale(1.05)}}
/* INSIGHTS */
.ic{{background:var(--s2);border:1px solid var(--border);border-left:3px solid #6366F1;border-radius:8px;padding:16px;transition:border-left-color .15s}}
.ic:hover{{border-left-color:var(--accent)}}
.itl{{font-size:14px;font-weight:700;margin-bottom:4px}}
.id{{font-size:11px;color:var(--muted);margin-bottom:6px}}
.ix{{font-size:12px;color:var(--muted);line-height:1.5}}
/* MISC */
.empty{{text-align:center;padding:40px;color:var(--muted);font-size:13px;border:1px dashed var(--border);border-radius:8px}}
.xbtn{{background:transparent;border:1px solid var(--border);color:var(--muted);font-family:'Montserrat',Arial,sans-serif;font-size:11px;font-weight:600;padding:6px 14px;border-radius:4px;cursor:pointer;margin-top:12px;transition:border-color .1s,color .1s}}
.xbtn:hover{{border-color:var(--accent);color:var(--accent)}}
#ss{{display:none;margin-bottom:32px}}
footer{{text-align:center;padding:24px;color:var(--muted);font-size:11px;border-top:1px solid var(--border)}}
footer strong{{color:var(--accent)}}
@media(max-width:600px){{main{{padding:20px 16px 48px}}.grid{{grid-template-columns:1fr}}#si{{width:130px}}}}
</style>
</head>
<body>

<nav id="nav">
  <div class="brand">OPENLAB <span>RADAR</span></div>
  <div class="nav-stats">
    <div class="ns"><strong id="s-total">—</strong>briefs</div>
    <div class="ns"><strong id="s-score">—</strong>score medio</div>
    <div class="ns"><strong id="s-last">—</strong>último brief</div>
    <div class="ns"><strong id="s-ins">—</strong>insights</div>
  </div>
  <input type="search" id="si" placeholder="Buscar briefs…" autocomplete="off">
</nav>

<main>

  <!-- Búsqueda -->
  <section id="ss">
    <div class="sh"><span class="st">Resultados de búsqueda</span><span class="ss" id="s-count"></span></div>
    <div id="s-res" class="grid"></div>
  </section>

  <!-- Hot Signals -->
  <section>
    <div class="sh"><span class="st">⚡ Hot Signals</span><span class="ss">Score ≥ 8.0 · últimos 7 días</span></div>
    <div id="hot" class="grid"><div class="empty">Sin briefs con score ≥ 8.0 en los últimos 7 días.</div></div>
  </section>

  <!-- Nuevos esta semana -->
  <section>
    <div class="sh"><span class="st">🗓 Nuevos esta semana</span><span class="ss" id="rec-sub"></span></div>
    <div id="rec" class="list"></div>
  </section>

  <!-- Por categoría -->
  <section>
    <div class="sh"><span class="st">📂 Por categoría</span><span class="ss">Click en la pestaña para explorar</span></div>
    <div class="tabs-bar" id="cat-tabs"></div>
    <div id="cat-contents"></div>
  </section>

  <!-- Tag Explorer -->
  <section id="tags-section">
    <div class="sh"><span class="st">🏷 Tag Explorer</span><span class="ss">Click en un tag para filtrar todos los briefs relacionados</span></div>
    <div id="tc"></div>
    <div id="tag-results-wrap" style="display:none">
      <div class="ss" id="trc" style="margin-bottom:12px"></div>
      <div id="tag-res" class="grid"></div>
    </div>
  </section>

  <!-- Insights -->
  <section>
    <div class="sh"><span class="st">💡 Insights</span><span class="ss">Síntesis generadas bajo demanda</span></div>
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

function card(b){{
  const tags=b.tags.map(t=>`<span class="tp" onclick="filterTag('${{e(t)}}')">${{e(t)}}</span>`).join('');
  const links=[];
  if(b.url)links.push(`<a class="lyt" href="${{e(b.url)}}" target="_blank">▶ YouTube</a>`);
  if(b.telegraph_url)links.push(`<a class="ltg" href="${{e(b.telegraph_url)}}" target="_blank">📖 Brief</a>`);
  return`<div class="card">
  <div class="ct"><a href="${{e(b.url||'#')}}" target="_blank">${{e(b.title)}}</a></div>
  <div class="cm">${{catBadge(b.category)}}${{scoreBadge(b.score)}}${{b.date?`<span class="bd">${{e(b.date)}}</span>`:''}}</div>
  ${{b.source?`<div class="csrc">por ${{e(b.source)}}</div>`:''}}
  ${{b.excerpt?`<div class="cx">${{e(b.excerpt)}}</div>`:''}}
  ${{tags?`<div class="tr">${{tags}}</div>`:''}}
  ${{links.length?`<div class="cl">${{links.join('')}}</div>`:''}}
</div>`}}

function listItem(b){{
  return`<div class="li">${{catBadge(b.category)}}<span class="lit"><a href="${{e(b.url||'#')}}" target="_blank">${{e(b.title)}}</a></span>${{scoreBadge(b.score)}}</div>`;
}}

// Stats
function initStats(){{
  const s=KB.stats;
  document.getElementById('s-total').textContent=s.total_briefs;
  document.getElementById('s-score').textContent=s.avg_score;
  document.getElementById('s-last').textContent=s.last_date||'—';
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
  const tags=Object.entries(tc).sort((a,b)=>b[1]-a[1]);
  const max=tags[0]?.[1]||1;
  const el=document.getElementById('tc');
  tags.forEach(([tag,count])=>{{
    const r=count/max;
    const span=document.createElement('span');
    span.className='ct2';
    span.textContent=tag+' ('+count+')';
    span.style.fontSize=Math.round(10+r*8)+'px';
    span.style.color=`rgba(204,255,0,${{(0.4+r*0.6).toFixed(2)}})`;
    span.style.borderColor=`rgba(204,255,0,${{(0.15+r*0.25).toFixed(2)}})`;
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
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    html = build_html(briefs, insights, stats, generated_at)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(f"KB Viewer generado: {output}  ({len(html)//1024} KB)")


if __name__ == "__main__":
    main()
