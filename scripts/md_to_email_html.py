#!/usr/bin/env python3
"""Convierte el briefing diario de OPENLAB Radar a HTML newsletter para email."""

import sys, re
from html import escape

LOGO_SRC = ""

CATEGORY_STYLES = {
    "agentic-systems":      ("🤖", "#000000", "#F0F0F0"),
    "claude-code-advanced": ("⚡", "#000000", "#F0F0F0"),
    "delivery-adoption":    ("🚀", "#000000", "#F0F0F0"),
    "context-engineering":  ("🧠", "#000000", "#F0F0F0"),
    "cli-vs-platforms":     ("🔧", "#000000", "#F0F0F0"),
    "enterprise-ai":        ("🏢", "#000000", "#F0F0F0"),
}
DEFAULT_CAT = ("📹", "#000000", "#F0F0F0")

def score_color(s):
    try:
        f = float(s)
        return "#16A34A" if f >= 8 else ("#D97706" if f >= 7 else "#DC2626")
    except: return "#6B7280"

def score_bg(s):
    try:
        f = float(s)
        return "#DCFCE7" if f >= 8 else ("#FEF3C7" if f >= 7 else "#FEE2E2")
    except: return "#F9FAFB"

def parse_videos(text):
    videos = []
    for block in re.split(r'\n(?=### \d+\.)', text):
        m = re.match(r'### \d+\.\s+\[([^\]]+)\]\((https?://[^\)]+)\)', block)
        if not m: continue
        fields, sub = {}, {}
        for line in block.split('\n'):
            line = line.strip()
            fm = re.match(r'-\s+\*\*([^:]+):\*\*\s*(.*)', line)
            if fm: fields[fm.group(1).strip()] = fm.group(2).strip()
            sm = re.match(r'-\s+(Aplicabilidad|Novedad|Calidad):\s*(\d+)', line)
            if sm: sub[sm.group(1)] = sm.group(2)
        videos.append({
            "title": m.group(1), "url": m.group(2),
            "canal": fields.get("Canal",""),
            "categoria": fields.get("Categoría", fields.get("Categoria","")),
            "duracion": fields.get("Duración", fields.get("Duracion","")),
            "score": fields.get("Score","?"),
            "para_openlab": fields.get("Para OPENLAB",""),
            "sub": sub,
        })
    return videos

def parse_menciones(text):
    out = []
    m = re.search(r'## Menci\S+ r\S+\n(.*?)(?=\n---|\n## |\Z)', text, re.DOTALL)
    if not m: return out
    for line in m.group(1).strip().split('\n'):
        lm = re.match(r'-\s+\[([^\]]+)\]\((https?://[^\)]+)\)\s*—\s*(.+)', line.strip())
        if lm: out.append({"title": lm.group(1), "url": lm.group(2), "meta": lm.group(3)})
    return out

def parse_tendencias(text):
    m = re.search(r'## Tendencias\n(.*?)(?=\n## |\Z)', text, re.DOTALL)
    if not m: return ""
    t = m.group(1).strip()
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong style="color:#CCFF00;">\1</strong>', t)

def pill(label, value):
    return (f'<span style="display:inline-block;background:#F3F4F6;border-radius:4px;'
            f'padding:2px 7px;font-size:11px;color:#6B7280;margin:2px 3px 2px 0;">'
            f'<strong style="color:#374151;">{value}</strong> {label}</span>')

def video_card(i, v):
    cat = v["categoria"]
    emoji, cc, cb = CATEGORY_STYLES.get(cat, DEFAULT_CAT)
    sc, scol, sbg = v["score"], score_color(v["score"]), score_bg(v["score"])
    rbg = "#000000" if i == 1 else ("#1a1a1a" if i <= 3 else "#374151")
    sub_html = '<div style="margin-top:6px;">' + "".join(pill(k,val) for k,val in v["sub"].items()) + '</div>' if v["sub"] else ""
    para_html = ""
    if v["para_openlab"]:
        txt = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', escape(v["para_openlab"]))
        para_html = (f'<div style="margin-top:12px;background:#F9F9F9;border-left:3px solid #CCFF00;'
                     f'border-radius:0 6px 6px 0;padding:10px 14px;">'
                     f'<div style="font-size:10px;font-weight:700;color:#000000;text-transform:uppercase;'
                     f'letter-spacing:0.8px;margin-bottom:5px;">Para OPENLAB</div>'
                     f'<div style="font-size:13px;color:#374151;line-height:1.6;">{txt}</div></div>')
    dur = f'&nbsp;&nbsp;<span style="font-size:11px;color:#9CA3AF;">⏱ {escape(v["duracion"])}</span>' if v["duracion"] else ""
    cat_badge = (f'<span style="display:inline-block;background:#000000;color:#CCFF00;'
                 f'font-size:10px;font-weight:700;padding:2px 9px;border-radius:20px;'
                 f'letter-spacing:0.2px;">{emoji} {escape(cat)}</span>')
    score_badge = (f'<span style="display:inline-block;background:{sbg};color:{scol};'
                   f'font-size:12px;font-weight:800;padding:2px 10px;border-radius:20px;">★ {escape(sc)}</span>')
    return (f'<tr><td style="padding:0 0 14px 0;">'
            f'<table width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:10px;overflow:hidden;">'
            f'<tr>'
            f'<td width="40" valign="top" style="background:{rbg};text-align:center;padding:18px 0;">'
            f'<div style="font-size:14px;font-weight:800;color:#CCFF00;">{i}</div>'
            f'</td>'
            f'<td style="padding:14px 16px;">'
            f'<a href="{escape(v["url"])}" style="font-size:14px;font-weight:700;color:#0F0F23;text-decoration:none;line-height:1.4;display:block;">{escape(v["title"])}</a>'
            f'<div style="margin-top:6px;">'
            f'<span style="font-size:12px;color:#6B7280;">{escape(v["canal"])}</span>{dur}'
            f'</div>'
            f'<div style="margin-top:6px;">{cat_badge}&nbsp;{score_badge}</div>'
            f'{sub_html}{para_html}'
            f'</td></tr></table></td></tr>')

def mencion_card(m):
    parts = [p.strip() for p in m["meta"].split(" — ", 3)]
    canal,score,cat = (parts+["","",""])[:3]
    desc = parts[3] if len(parts)>3 else ""
    emoji, cc, cb = CATEGORY_STYLES.get(cat, DEFAULT_CAT)
    scol = score_color(score)
    sc_bg = score_bg(score)
    desc_html = f'<div style="font-size:12px;color:#6B7280;margin-top:4px;line-height:1.5;">{escape(desc)}</div>' if desc else ""
    return (f'<tr><td style="padding:0 0 8px 0;">'
            f'<table width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="background:#F9FAFB;border:1px solid #F3F4F6;border-radius:8px;">'
            f'<tr><td style="padding:11px 14px;">'
            f'<a href="{escape(m["url"])}" style="font-size:13px;font-weight:600;color:#374151;text-decoration:none;">{escape(m["title"])}</a>'
            f'<div style="margin-top:4px;">'
            f'<span style="font-size:11px;color:#9CA3AF;">{escape(canal)}</span>'
            f'&nbsp;<span style="display:inline-block;background:#000;color:#CCFF00;font-size:10px;font-weight:700;padding:1px 7px;border-radius:20px;">{emoji} {escape(cat)}</span>'
            f'&nbsp;<span style="font-size:11px;font-weight:700;color:{scol};">★ {escape(score)}</span>'
            f'</div>{desc_html}'
            f'</td></tr></table></td></tr>')

def build_email(md):
    date_m = re.search(r'(\d{4}-\d{2}-\d{2})', md)
    date = date_m.group(1) if date_m else ""
    top_m = re.search(r'## Top V\S+ del D\S+\n(.*?)(?=\n---|\n## Menci|\Z)', md, re.DOTALL)
    videos = parse_videos(top_m.group(1) if top_m else "")
    menciones = parse_menciones(md)
    tendencias = parse_tendencias(md)

    video_rows = "".join(video_card(i+1, v) for i,v in enumerate(videos))

    men_html = ""
    if menciones:
        rows = "".join(mencion_card(m) for m in menciones)
        men_html = (f'<tr><td style="padding:8px 0 16px;">'
                    f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;'
                    f'letter-spacing:1px;color:#9CA3AF;padding-bottom:10px;">Mención Rápida</div>'
                    f'<table width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table>'
                    f'</td></tr>')

    tend_html = ""
    if tendencias:
        tend_html = (f'<tr><td style="padding:8px 0 24px;">'
                     f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;'
                     f'letter-spacing:1px;color:#9CA3AF;padding-bottom:10px;">Tendencias del Día</div>'
                     f'<div style="background:#0F0F0F;border-radius:10px;padding:20px 22px;">'
                     f'<p style="font-size:13px;color:#9CA3AF;line-height:1.75;margin:0;">{tendencias}</p>'
                     f'</div></td></tr>')

    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap" rel="stylesheet"><title>OPENLAB Radar · {date}</title></head>
<body style="margin:0;padding:0;background:#F3F4F6;font-family:'Montserrat',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F3F4F6;padding:24px 16px;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;">

  <!-- HEADER -->
  <tr><td style="background:#000000;border-radius:12px 12px 0 0;padding:24px 32px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      <td valign="middle">
        <img src="{LOGO_SRC}" alt="OPENLAB" width="150" height="auto"
             style="display:block;max-width:150px;">
      </td>
      <td align="right" valign="middle">
        <div style="font-size:20px;font-weight:800;color:#FFFFFF;line-height:1.2;">Briefing Diario</div>
        <div style="font-size:13px;color:#D1D5DB;margin-top:4px;">{date}</div>
      </td>
    </tr></table>
  </td></tr>

  <!-- LIME DIVIDER -->
  <tr><td style="background:#FFFFFF;border-left:1px solid #E5E7EB;border-right:1px solid #E5E7EB;padding:0;">
    <div style="height:3px;background:#CCFF00;"></div>
  </td></tr>

  <!-- MAIN CONTENT -->
  <tr><td style="background:#FFFFFF;border-left:1px solid #E5E7EB;border-right:1px solid #E5E7EB;padding:24px 28px 8px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr><td style="padding:0 0 16px;">
        <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#9CA3AF;">
          Top Vídeos del Día
        </div>
      </td></tr>
      {video_rows}
      {men_html}
      {tend_html}
    </table>
  </td></tr>

  <!-- FOOTER -->
  <tr><td style="background:#000000;border-radius:0 0 12px 12px;padding:18px 32px;text-align:center;">
    <p style="margin:0;font-size:11px;color:#4B5563;">
      <strong style="color:#6B7280;">OPENLAB Radar</strong>&nbsp;·&nbsp;generado automáticamente&nbsp;·&nbsp;<a href="https://openlabstudio.com" style="color:#CCFF00;text-decoration:none;">openlabstudio.com</a>
    </p>
  </td></tr>

</table></td></tr></table>
</body></html>"""

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    md = open(path).read() if path else sys.stdin.read()
    print(build_email(md))
