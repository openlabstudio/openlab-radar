#!/usr/bin/env python3
"""Convierte el briefing diario de OPENLAB Radar a HTML newsletter para email."""

import sys, re, os, glob
from html import escape

LOGO_SRC = "data:image/png;base64,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UmVhZHlxyWU8AAADe2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgOS4wLWMwMDAgNzkuMTcxYzI3ZmFiLCAyMDIyLzA4LzE2LTIyOjM1OjQxICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSIyQTkzNTlDMDY1N0YxQTc2Qzk1NEIxNkJFODk5Qjg2QiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpFNEYyQzA0ODlEQkYxMUVFQTMzRkE1ODlCQUQyRTgyOSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpFNEYyQzA0NzlEQkYxMUVFQTMzRkE1ODlCQUQyRTgyOSIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxNyAoV2luZG93cykiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDplMjUxYWNhOS1iYjlmLWVmNGYtYTMzMy03NTE0ZGI5MTI0NDEiIHN0UmVmOmRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDpmOTdmOWY1Ny05ZDM4LTM2NDctOTljMC0xYjdlN2IxOTljM2IiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5b2jy6AAANP0lEQVR42uzd/VEbRxgH4MXjAuQKIiqIqMByBcEVICowVECowFABooKQCiz/7xnjCqxUEDpQbqNTIpwYo4+9j93nmblxknEk9O7u6X7s7t3Bp0Xoo3F1jKpjUB2v6/+2+vfneKiO+/qfP679+ywAAADQaQc9CLIxnB7XgXVUHynd10cMuHd1yAUAAECQfdKwDq8nDQTX5wTb2zrUznUZAAAAQXZlNfP6rgPh9alQex3M1AIAABQdZId1eJ2E5+9xbVsMsdM61M51IwAAgDKCbAywF3WA7bMYaC97GGgXun+3xqL21b4ttu9BYe2x0L74/sX3b6vu62vnL2F5s9WZktCHIDuoA+xZZrWMYfYq9GfJsROtL1K0ryCrffH96/ysfbsibt37PdjCR0eD7FkdYgeZ1jMOuvOwnKX1RYovUgQdQVb74vzs/Mzm19PX9fX0XDloO8gOq+MmLJ//WoJZdZx2fPA50foiRfsKstoX37/Oz9q364G2TyseadCLBt4jzsJ+LijEhvqzxs880cUAAGBjq+2I8Zr6WDloMsjGzvdbdbwP+S4l/tHnv6mPga4GAAAbG9aZwjU1jQTZ+BxYvz1ZmlTHh3oQAgAArqnpYJA91sm+G+xHSgEAAK6p6VaQnYTl1L9p//8aBPtmAQBg12vqD8Is+wyyv4bl2nWediPMAgCAMEv7QTaGswvlFGYBAKDBMDtUCkFWKBNmAQCgT2HWtkZBdiu/CmPCLAAAtCQuL36vDILsJmIAs5xYmAUAgDbFa2mP/RRkn+U4uLHTvsOszeoAALCdOCtribEg+6SREJuEzeoAALCdeB19pgyC7PfYUJ2O2gIAwPbeBRNDxXi54d+/6WDneKiO++r4uPbPT4kzyj/Vf446FhxXm9VPdU0AANhIvK6fhOUNacncwafFs//uWejOHcFiWL2tjtkzgutzwuO4Ok5Cd/apvq2Ou8TvsdD9uzUWta/2bbF9Dwprj4X2JaP+h+9fHosTW6+UQZBdGVbH59Du7GXslNfVMa2OeaL3iJ8zLkmYdOCzHiX8nE60vkjRvoKs9kWQxfdvrk7rzIAg+/eNiMYthrrzsJyhfGjoPWOIPatDbVuBdlYdbwq+kHMhrH3p74XSgfFr/KJ9jV/tu2aVI+LqxyZWQcbc8NbpRpBtc0nxZXVcNRhg/y/QXoT27oCWcomxE60vUu2r/wmyxi/6n/pp37aC7fvEgda5r/AgG4Pc19D8rGTc93oadt//ui+rRw41vYc2BvjDREHeidYXqfbV/wRZ4xf9T/20b1sGdZidJHr9uLJx5pSTrx89fueihRAbZ2CPOhRiV8E6DoZpCwPc87AAAMhNnKhJuZd1rMTlBtlhwyFq1ZnPOz7Ymn40judhAQCQq3jtP0/wuj8rbblB9qLhkNjGjOc2pvXP2uSNpy50VQAAMrSaLNq3odLm7Xt7ZGPDf204xN73rHZxv+yH0NzS67hXdr7H17OHI+/6aV/9r9XvFuPX+EX7Gr/ad0Ofw/7vR+P8l7Hvzci+E2J/aLVvtqmZ2YnuCgBApm6VgF2D7KCh0NTnELseZpt6RlWbz7QFAIDU19WwU5A9bigwnWfSYWehmRtADeq2AQAAEGS/0cSy4viInWlGdZw29HlOdFkAAECQfWwY9r/J+ltxFvY8w1o2McM8Du7ABgAACLKPNLF09TTTWj409NksLwYAIDcjJWCXIJt66eplyHsjd/xsV4nfw/JiAABy4xqXjaw/RzbeTOjPhO8VZywPQ3OPq2lLrOPXkPaGWa/2UEfPOcu7ftpX/2v1u8X4NX7Rvsav9t3AuDo+7Pk14wTTkVNOvtZnZFMvWT0vIMSuAvt14vewvBgAgBzEyZ+bBK87V9pyguzrxOHurqC6XiUO7a91XQAAMgixv4U0NzP9orzlBNmUG6yvQxmzsevBfZrw9W2GBwAghxA7TvT6MyXO2/oe2ZR7ruLe2HlhtR2G5V7ZZG234/9vD0fe9dO++l+r3y3Gr/GL9jV+te8TYni9CWkfK+ncl7mXa50plftQ5hr1ef3ZRwlPADNdGACAjovXw4P6z5OQfnXhnZKXE2RTdqbbgut7m7C2w4591oXhlDUzgHl70/H+on3B96/2ZRO/K0E5QTblo2JmBdc35Wcf6r6A8zQAPFLaTWaLtbrZ0+uEHem+4Preh3Q3uXLnYgAAeGwayrrJbPFBNmWQK50aAABAM66VoKwgm2of50clThZkPYIHAAD+dRXKvMls0UE21R5Z0/oh/JHodQdKCwAA/+SOS2UoL8imYlmtGgAAQGqnwSSaIAsAANATd8GdigVZAACAnoirH0+VocwgO1QGAACgZx6CJcVFB9l54s4FAAAAew2yKbmzLgAAkCpr3MgcgiwAAECfjOowiyALAADQG8f1gSC7NyMlVgMAAEjMEuNCg2yqmzL9pMTJauBGWgAAsBRD7IUylBdk7xO9vtnIdDW4V1oAAPjHWfBo0eKCbN9CXJ+MlQAAABphVrawIPsx0esPCg+zKT/7R90XAAAeOQ72yhYVZFPutxwXPpBSmeu+AADwyCC4g3ERXtZ/ptxveVIdV4XW95eCguyB4ZQ17csm3uz59RZKCs7PhZ4PcmnfUfh3peZJSL9iM16DT50eMh8cnxaNnBgOQ3kziMPq+NrhE9uiYz8P3f6i177a14Vrc/Uzfo1f7dvf+mnf5xlXx/vEgda5L3PrN3tKOSv7rsDapvzM7lgMAEBfzcJy9c40cVhGkN3ZJJS16XpQf+aUgx8AAPoq3qPnNGGYFWQLCrIp74Ibg91ZQXU9Sxzcv+i6AABk4Dyk2YL4s9LmbX2PbAxefyZ8r/hbl8OQ9g7JXRDr+DVxkH21hzraw5E37at9c2pfe2SNX+NX+/alftp3O+Pq+LDn14yrTY+ccvL14pugmXJ5cQx2JTyg+CJxiL0v4JcBAACUY5Ygh4yUtZwgG90mfr+zzDvVOKRfQn2r2wIAkBnXuOwUZO8aeM+bkOeNnwb1Z0vtTrcFACAznsrBTkF23kAnijOy7zOsZfxMw8TvMQvlPY8XAADgySAbXTfwvpOQ9vE0TTtr6PNYcgEAAAiy//Pf4tLVJm4mFJfhjjOoYQywTcwwxzaZ6rIAAIAg225g+i30++ZPx6GZfbHRte4KAECm3GWYnYNsk6Ep3iDpQ0877qQO4k250l0BAMjUiRKwjyA7D83Nyq7C7LhnIfamwfeLbeHZsQAA5CjmgH1PbLkLcqFBNrps8OdYhdlJD2p21nCIjQH2XFcFACBDqR5hOVfacoPsvOEwG+pO3NXnzK4GWdOPDroOZmMBAMgzxMatesMEr/1FecsNstFVCyFqErq3b3ZcHZ9D8zPG82BvLAAA+YbYcaLXnylx2UG2rWWtozo4vg/tzs4O6p8hButhC+9/HszGAgCQl3F9rT9O+B6CbOYOPi2e9ffavBlTDHJxeW2Ts8MxwMa9sO9aDNLxeb5vE77+Yt99yXDqFO2rfXNq30XHf74D7Yv2VT/t++R19WqlZfzzJKRfeZn6OpoeBdlhWP7WpM3Z0dXzbWOonSd6j2EdXicd+KyHiYO7E60vegQdF8JltC/Gr/Fr/JbmNKR5Aov27WGQDaH5R848Jd5O+zYslwzsemvt+Buh4+r4JXRnX278DdJd4V8EONG6EDZ+XQhj/Bq/xi+bSjkhpH075OUGf3daHa9DNx6RM1oLnQ91mI3HH88ItvH/+2ntNbp2h+SrBkIsAADkyBM/CrHJjGwI/z7vdaR0ScQQftTQe/mNcN78xrBj51rjN+vxYUbH+DV+jV/jtxtSb8/Tvh3yYovO8Tb4LUeqgfdGGQAAYCtmYwXZJ80FrmQh1sADAIDtMsqVMgiyPxKXwJ4q3968DbvftAoAAEp1HkwKCbLPNBVm9yLWcKYMAACwFTdLFWSF2RZC7FQZAABgK3FV46UyCLLCrBALAAB94Ea0gqwwK8QCAECvQmy8WepcKcr0co+vtQpmN8r65ICLvzWaKQUAAOwUYt0stWAv9vx6McweBdP7Tw04IRYAAIRYOhRkQ92pjnSu/9TkUE0AAEDOoJtBNpqH5W9Kpkr89+3AzVIDAMD2psGeWBoIsqEObvGmRqXeSWy1H/ZcNwMAgK3M62vq02BiiIaC7Ep8OHGckZwVVNf4mQ+DBzMDAMA2Ymi9rHOEa2paCbLRPCyXAuQ+OzuvP6PnWQEAwG4B9lfX1LQdZFdWM5WXmXVKvzECAIDdckJcPvyqDrBzJeEpB58Wrb33sDouqmPS8xpOw3IfbN+C+b5b/sBwyrp96db4MH7zrp/xa/wav8Zv7u7roPolLLcfzlxf0acgux5oY5h9Vx2DntQthtbrsLwjseUOAAAAhQXZlRhij6vjpDrGHa3XrDpug8cKAQAACLLfGK6F2lHLP8t9HV7juv25LgMAACDI/shqpvZ1HWpTB9sYXGdhuWY/hldLhwEAAATZnY3DctZ2WAfcUAfc5+6xfagDa/QxLGda56GsZ90CAAD00l8CDAA6R88K0ZDQ1AAAAABJRU5ErkJggg=="

CATEGORY_STYLES = {
    "skill-design":      ("🛠", "#000000", "#F0F0F0"),
    "orchestration":     ("🤖", "#000000", "#F0F0F0"),
    "market-signal":     ("📊", "#000000", "#F0F0F0"),
    "delivery-adoption": ("🚀", "#000000", "#F0F0F0"),
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

def find_telegraph_url(date, categoria, briefs_dir):
    pattern = os.path.join(briefs_dir, categoria, f"{date}-*.md")
    for path in glob.glob(pattern):
        try:
            content = open(path).read()
            m = re.search(r'\*\*Telegraph:\*\*\s*(https://telegra\.ph/\S+)', content)
            if m:
                return m.group(1).strip()
        except Exception:
            pass
    return ""

def video_card(i, v, telegraph_url=""):
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
            + (f'<a href="{telegraph_url}" style="display:inline-block;margin-top:12px;background:#000000;color:#CCFF00;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;padding:6px 14px;border-radius:6px;text-decoration:none;">Ver resumen →</a>' if telegraph_url else "")
            + f'</td></tr></table></td></tr>')

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

    briefs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "briefs")
    video_rows = "".join(
        video_card(i+1, v, find_telegraph_url(date, v["categoria"], briefs_dir))
        for i, v in enumerate(videos)
    )

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
<html lang="es" style="color-scheme:light only;">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light only" /><meta name="supported-color-schemes" content="light" /><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap" rel="stylesheet"><title>OPENLAB Radar · {date}</title></head>
<body style="margin:0;padding:0;background:#F3F4F6;font-family:'Montserrat',Arial,sans-serif;color-scheme:light only;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F3F4F6;padding:24px 16px;color-scheme:light only;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;">

  <!-- HEADER -->
  <tr><td style="background:#000000;border-radius:12px 12px 0 0;padding:24px 32px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      <td valign="middle">
        <img src="{LOGO_SRC}" alt="OPENLAB" width="100" height="auto"
             style="display:block;max-width:100px;">
      </td>
      <td align="right" valign="middle">
        <div style="font-size:20px;font-weight:800;color:#FFFFFF;line-height:1.2;">Briefing Diario</div>
        <div style="font-size:13px;color:#D1D5DB;margin-top:4px;white-space:nowrap;">{"-".join(reversed(date.split("-"))) if date else ""}</div>
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
