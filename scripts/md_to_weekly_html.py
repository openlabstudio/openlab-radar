#!/usr/bin/env python3
"""
OPENLAB Radar — Weekly Digest Markdown to HTML Email Newsletter
Converts the weekly digest markdown format to a styled HTML email.
"""

import sys
import re
import markdown as md_lib
from datetime import datetime


CATEGORY_STYLES = {
    "agentic-systems":      ("🤖", "#CCFF00", "#000000"),
    "claude-code-advanced": ("⚡", "#CCFF00", "#000000"),
    "delivery-adoption":    ("🚀", "#CCFF00", "#000000"),
    "context-engineering":  ("🧠", "#CCFF00", "#000000"),
    "cli-vs-platforms":     ("🔧", "#CCFF00", "#000000"),
    "enterprise-ai":        ("🏢", "#CCFF00", "#000000"),
}

LOGO_URL = ""


def score_color(score_val):
    """Return (text_color, bg_color) tuple based on score."""
    try:
        s = float(score_val)
    except (ValueError, TypeError):
        return ("#374151", "#F3F4F6")
    if s >= 8.0:
        return ("#16A34A", "#DCFCE7")
    elif s >= 7.0:
        return ("#D97706", "#FEF3C7")
    else:
        return ("#DC2626", "#FEE2E2")


def parse_date_range(title_line):
    """Extract date range from the H1 title line."""
    m = re.search(r'(\d{4}-\d{2}-\d{2})\s+a\s+(\d{4}-\d{2}-\d{2})', title_line)
    if m:
        return m.group(1), m.group(2)
    return "", ""


def parse_resumen(section_text):
    """
    Parse the Resumen section into structured data.
    Returns dict with videos, selected, avg_score, categories.
    """
    data = {
        "videos": "",
        "selected": "",
        "avg_score": "",
        "categories": {}
    }

    # Videos evaluados
    m = re.search(r'\*\*Vídeos evaluados esta semana:\*\*\s*([\d]+)', section_text)
    if m:
        data["videos"] = m.group(1)

    # Seleccionados
    m = re.search(r'\*\*Seleccionados:\*\*\s*([\d]+)\s+briefs?', section_text)
    if m:
        data["selected"] = m.group(1)

    # Media score
    m = re.search(r'\*\*Media score estimada:\*\*\s*~?([\d.]+)', section_text)
    if m:
        data["avg_score"] = m.group(1)

    # Categories — look for lines like `category-name`: N
    cat_section = re.search(r'\*\*Por categoría:\*\*(.*?)(?=\n---|\Z)', section_text, re.DOTALL)
    if cat_section:
        cat_text = cat_section.group(1)
        # Match backtick-wrapped category names with counts
        cats = re.findall(r'`([^`]+)`[:\s]*([\d]+)', cat_text)
        for cat, count in cats:
            data["categories"][cat.strip()] = count.strip()
        # Also match plain category: N pattern (bold or plain)
        if not cats:
            cats = re.findall(r'\*\*([\w-]+)\*\*[:\s]*([\d]+)', cat_text)
            for cat, count in cats:
                data["categories"][cat.strip()] = count.strip()

    return data


def parse_tendencias(section_text):
    """
    Parse Tendencias section into list of dicts: {num, title, body, implicacion}.
    """
    trends = []
    # Split by ### N. Title
    parts = re.split(r'###\s+(\d+)\.\s+(.+)', section_text)
    # parts = [preamble, num, title, body, num, title, body, ...]
    i = 1
    while i < len(parts) - 2:
        num = parts[i].strip()
        title = parts[i+1].strip()
        body = parts[i+2].strip()

        # Extract "Implicación para OPENLAB:" callout
        implicacion = ""
        impl_match = re.search(
            r'\*\*Implicaci[oó]n para OPENLAB:\*\*\s*(.+?)(?=\n\n|\Z)',
            body, re.DOTALL
        )
        if impl_match:
            implicacion = impl_match.group(1).strip()
            # Remove from body
            body = body[:impl_match.start()].strip()

        trends.append({
            "num": num,
            "title": title,
            "body": body,
            "implicacion": implicacion
        })
        i += 3

    return trends


def parse_top5(section_text):
    """
    Parse Top 5 Vídeos section.
    Returns list of dicts: {rank, title, score, channel, duration, category, description, link, link_text}
    """
    videos = []
    # Split by ### N. Title
    parts = re.split(r'###\s+(\d+)\.\s+(.+)', section_text)
    i = 1
    while i < len(parts) - 2:
        rank = parts[i].strip()
        title = parts[i+1].strip()
        body = parts[i+2].strip()

        video = {
            "rank": rank,
            "title": title,
            "score": "",
            "channel": "",
            "duration": "",
            "category": "",
            "description": "",
            "link": "",
            "link_text": "Ver brief completo"
        }

        lines = body.split('\n')
        meta_line = ""
        desc_lines = []
        link_line = ""

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            # Meta line: **Score: X.X** | Channel | Duration | Category
            if line_stripped.startswith('**Score:'):
                meta_line = line_stripped
            elif line_stripped.startswith('→') or line_stripped.startswith('->'):
                link_line = line_stripped
            else:
                desc_lines.append(line_stripped)

        # Parse meta
        if meta_line:
            score_m = re.search(r'\*\*Score:\s*([\d.]+)\*\*', meta_line)
            if score_m:
                video["score"] = score_m.group(1)
            # The rest after score badge: | Channel | Duration | Category
            rest = re.sub(r'\*\*Score:\s*[\d.]+\*\*\s*\|?\s*', '', meta_line).strip()
            meta_parts = [p.strip() for p in rest.split('|') if p.strip()]
            if len(meta_parts) >= 1:
                video["channel"] = meta_parts[0]
            if len(meta_parts) >= 2:
                video["duration"] = meta_parts[1]
            if len(meta_parts) >= 3:
                video["category"] = meta_parts[2]

        # Parse link
        if link_line:
            link_m = re.search(r'\[([^\]]+)\]\(([^)]+)\)', link_line)
            if link_m:
                video["link_text"] = link_m.group(1)
                video["link"] = link_m.group(2)

        video["description"] = ' '.join(desc_lines)
        videos.append(video)
        i += 3

    return videos


def parse_gaps_table(section_text):
    """Parse markdown table in Gaps section. Returns (headers, rows)."""
    return parse_markdown_table(section_text)


def parse_markdown_table(text):
    """Generic markdown table parser. Returns (headers, rows)."""
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    table_lines = [l for l in lines if l.startswith('|')]

    if len(table_lines) < 3:
        return [], []

    def parse_row(line):
        cells = [c.strip() for c in line.strip('|').split('|')]
        return cells

    headers = parse_row(table_lines[0])
    # table_lines[1] is the separator
    rows = [parse_row(l) for l in table_lines[2:]]
    return headers, rows


def parse_recomendaciones(section_text):
    """
    Parse Recomendaciones section.
    Returns dict with subsections: canales (table), keywords (bullets), temas (bullets).
    """
    result = {
        "canales": {"headers": [], "rows": []},
        "keywords": [],
        "temas": []
    }

    # Split by ### subsections
    subsections = re.split(r'###\s+(.+)', section_text)
    i = 1
    while i < len(subsections) - 1:
        sub_title = subsections[i].strip().lower()
        sub_body = subsections[i+1].strip()

        if 'canal' in sub_title:
            headers, rows = parse_markdown_table(sub_body)
            result["canales"]["headers"] = headers
            result["canales"]["rows"] = rows

        elif 'keyword' in sub_title or 'palabras' in sub_title:
            bullets = re.findall(r'^[-*]\s+(.+)', sub_body, re.MULTILINE)
            result["keywords"] = bullets

        elif 'tema' in sub_title or 'emergente' in sub_title:
            bullets = re.findall(r'^[-*]\s+(.+)', sub_body, re.MULTILINE)
            result["temas"] = bullets

        i += 2

    return result


def parse_aplicabilidad(section_text):
    """
    Parse Aplicabilidad OPENLAB section.
    Returns list of {title, body_html} subsections.
    """
    subsections = []
    parts = re.split(r'###\s+(.+)', section_text)
    i = 1
    while i < len(parts) - 1:
        title = parts[i].strip()
        body = parts[i+1].strip()
        body_html = md_lib.markdown(body)
        subsections.append({"title": title, "body_html": body_html})
        i += 2
    return subsections


def split_sections(content):
    """
    Split the markdown content into named top-level sections.
    Returns dict: {section_name: section_content}
    """
    sections = {}

    # Extract H1 title
    h1_match = re.match(r'^#\s+(.+)', content, re.MULTILINE)
    sections["title"] = h1_match.group(1).strip() if h1_match else ""

    # Split by ## headers (but not ###)
    parts = re.split(r'^##\s+(.+)$', content, flags=re.MULTILINE)
    # parts[0] is preamble (before first ##)
    i = 1
    while i < len(parts) - 1:
        section_name = parts[i].strip()
        section_body = parts[i+1].strip()
        sections[section_name] = section_body
        i += 2

    return sections


# ─── HTML Rendering ─────────────────────────────────────────────────────────

def render_category_badge(cat_name, count=None):
    emoji, bg, fg = CATEGORY_STYLES.get(cat_name, ("📌", "#6B7280", "#FFFFFF"))
    label = cat_name
    if count:
        label += f" · {count}"
    return (
        f'<span style="display:inline-flex;align-items:center;gap:4px;'
        f'background:{bg};color:{fg};font-size:11px;font-weight:700;'
        f'padding:3px 10px;border-radius:99px;margin:3px 4px 3px 0;'
        f'font-family:\'Courier New\',monospace;letter-spacing:0.02em;">'
        f'{label}</span>'
    )


def render_stat_pill(label, value, bg="#CCFF00", fg="#000000"):
    return ""  # unused


def render_header(date_from, date_to):
    date_label = f"{date_from} — {date_to}" if date_from and date_to else ""
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#000000;padding:28px 32px 22px;">
      <tr>
        <td style="vertical-align:middle;">
          <img src="{LOGO_URL}" alt="OPENLAB" height="36"
               style="display:block;height:36px;width:auto;" />
        </td>
        <td style="text-align:right;vertical-align:middle;">
          <div style="color:#CCFF00;font-size:11px;font-weight:700;
                      text-transform:uppercase;letter-spacing:0.12em;">
            Digest Semanal
          </div>
          {f'<div style="color:#9CA3AF;font-size:12px;margin-top:4px;">{date_label}</div>' if date_label else ''}
        </td>
      </tr>
    </table>
    """


def render_resumen(data):
    stats = []
    if data["videos"]: stats.append(f'<strong>{data["videos"]}</strong> vídeos evaluados')
    if data["selected"]: stats.append(f'<strong>{data["selected"]}</strong> seleccionados')
    if data["avg_score"]: stats.append(f'score medio <strong>~{data["avg_score"]}</strong>')
    line = " · ".join(stats) if stats else ""
    return f"""
    <div style="padding:0 0 20px 0;border-bottom:1px solid #F3F4F6;margin-bottom:24px;">
      <div style="font-size:13px;color:#6B7280;line-height:1.8;">{line}</div>
    </div>
    """ if line else ""


def render_tendencias(trends):
    if not trends:
        return ""

    cards = ""
    for t in trends:
        # Convert body markdown to HTML
        body_html = md_lib.markdown(t["body"])

        implicacion_block = ""
        if t["implicacion"]:
            impl_html = md_lib.markdown(t["implicacion"])
            implicacion_block = f"""
            <div style="background:#0F0F0F;border-left:4px solid #CCFF00;
                        border-radius:0 8px 8px 0;padding:14px 18px;margin-top:14px;">
              <div style="color:#CCFF00;font-size:11px;font-weight:700;
                          text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">
                Implicación para OPENLAB
              </div>
              <div style="color:#E5E7EB;font-size:14px;line-height:1.6;">{impl_html}</div>
            </div>
            """

        cards += f"""
        <table width="100%" cellpadding="0" cellspacing="0"
               style="background:#FFFFFF;border-radius:12px;
                      margin-bottom:14px;border:1px solid #E5E7EB;overflow:hidden;">
          <tr>
            <td style="background:#000000;width:48px;min-width:48px;
                       text-align:center;vertical-align:top;padding:18px 14px;">
              <div style="color:#CCFF00;font-size:20px;font-weight:900;
                          font-family:'Courier New',monospace;line-height:1;">
                {t["num"]}
              </div>
            </td>
            <td style="padding:18px 22px;vertical-align:top;">
              <div style="font-size:16px;font-weight:700;color:#111827;margin-bottom:10px;">
                {t["title"]}
              </div>
              <div style="font-size:14px;color:#374151;line-height:1.65;">{body_html}</div>
              {implicacion_block}
            </td>
          </tr>
        </table>
        """

    return f"""
    <div style="margin-bottom:28px;">
      <div style="font-size:13px;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.1em;color:#6B7280;margin-bottom:14px;">
        Tendencias de la Semana
      </div>
      {cards}
    </div>
    """


def render_top5(videos):
    if not videos:
        return ""

    cards = ""
    for v in videos:
        tc, bc = score_color(v["score"])
        score_badge = ""
        if v["score"]:
            score_badge = (
                f'<span style="display:inline-block;background:{bc};color:{tc};'
                f'font-size:12px;font-weight:800;padding:2px 10px;border-radius:20px;">'
                f'★ {v["score"]}</span>'
            )

        cat_badge = ""
        if v["category"]:
            cat_name = v["category"].strip().strip('`')
            cat_badge = render_category_badge(cat_name)

        meta_parts = []
        if v["channel"]:
            meta_parts.append(
                f'<span style="font-weight:600;color:#374151;">{v["channel"]}</span>'
            )
        if v["duration"]:
            meta_parts.append(
                f'<span style="color:#9CA3AF;">{v["duration"]}</span>'
            )
        meta_line = ' <span style="color:#D1D5DB;">·</span> '.join(meta_parts)

        # Extract YouTube and Telegraph URLs from brief file
        yt_url = ""
        telegraph_url = ""
        if v["link"] and v["link"].endswith(".md"):
            brief_path = v["link"].replace("../", "/home/openlab/openlab-radar/briefs/")
            try:
                brief_content = open(brief_path).read()
                import re as _re
                yt_m = _re.search(r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+', brief_content)
                if yt_m:
                    yt_url = yt_m.group(0)
                tg_m = _re.search(r'\*\*Telegraph:\*\*\s*(https://telegra\.ph/\S+)', brief_content)
                if tg_m:
                    telegraph_url = tg_m.group(1).strip()
            except:
                pass
        link_btn = ""
        if telegraph_url:
            link_btn = (
                f'<a href="{telegraph_url}" style="display:inline-block;margin-top:12px;'
                f'background:#000000;color:#CCFF00;font-size:11px;font-weight:700;'
                f'text-transform:uppercase;letter-spacing:0.08em;padding:6px 14px;'
                f'border-radius:6px;text-decoration:none;">Ver resumen →</a>'
            )

        desc_html = ""
        if v["description"]:
            desc_html = (
                f'<div style="font-size:14px;color:#374151;line-height:1.6;margin-top:10px;">'
                f'{v["description"]}</div>'
            )

        cards += f"""
        <table width="100%" cellpadding="0" cellspacing="0"
               style="background:#FFFFFF;border-radius:10px;
                      margin-bottom:14px;border:1px solid #E5E7EB;overflow:hidden;">
          <tr>
            <td style="background:#000000;width:40px;min-width:40px;
                       text-align:center;vertical-align:top;padding:18px 0;">
              <div style="color:#CCFF00;font-size:14px;font-weight:800;line-height:1;">
                {v["rank"]}
              </div>
            </td>
            <td style="padding:14px 16px;vertical-align:top;">
              <a href="{yt_url}" style="font-size:14px;font-weight:700;color:#0F0F23;text-decoration:none;line-height:1.4;display:block;">{v["title"]}</a>
              <div style="margin-top:6px;font-size:12px;color:#6B7280;">{meta_line}</div>
              <div style="margin-top:6px;">{cat_badge}&nbsp;{score_badge}</div>
              {desc_html}
              {link_btn}
            </td>
          </tr>
        </table>
        """

    return f"""
    <div style="margin-bottom:28px;">
      <div style="font-size:13px;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.1em;color:#6B7280;margin-bottom:14px;">
        Top 5 Vídeos de la Semana
      </div>
      {cards}
    </div>
    """


def render_styled_table(headers, rows, monospace_col=0):
    """Render a styled HTML table with black header row and lime text."""
    if not headers and not rows:
        return '<p style="color:#6B7280;font-size:13px;">Sin datos.</p>'

    th_cells = ""
    for h in headers:
        th_cells += (
            f'<th style="background:#000000;color:#CCFF00;font-size:11px;'
            f'font-weight:700;text-transform:uppercase;letter-spacing:0.08em;'
            f'padding:10px 14px;text-align:left;">{h}</th>'
        )

    tbody_rows = ""
    for idx, row in enumerate(rows):
        row_bg = "#F9FAFB" if idx % 2 == 0 else "#FFFFFF"
        td_cells = ""
        for col_i, cell in enumerate(row):
            cell_text = cell
            font = ""
            # Monospace for category-like columns (first column by default)
            if col_i == monospace_col:
                # Strip backticks if present
                cell_text = cell.strip('`')
                font = "font-family:'Courier New',monospace;font-size:12px;"
            td_cells += (
                f'<td style="background:{row_bg};padding:10px 14px;'
                f'font-size:13px;color:#374151;border-bottom:1px solid #E5E7EB;'
                f'{font}">{cell_text}</td>'
            )
        tbody_rows += f"<tr>{td_cells}</tr>"

    return f"""
    <table width="100%" cellpadding="0" cellspacing="0"
           style="border-radius:8px;overflow:hidden;border:1px solid #E5E7EB;">
      <thead><tr>{th_cells}</tr></thead>
      <tbody>{tbody_rows}</tbody>
    </table>
    """


def render_bullet_list(items, color="#374151"):
    if not items:
        return ""
    lis = ""
    for item in items:
        item_html = md_lib.markdown(item)
        # Remove wrapping <p> tags for inline rendering
        item_html = re.sub(r'^<p>(.*)</p>$', r'\1', item_html.strip(), flags=re.DOTALL)
        lis += (
            f'<li style="color:{color};font-size:14px;line-height:1.6;'
            f'margin-bottom:6px;">{item_html}</li>'
        )
    return f'<ul style="margin:8px 0;padding-left:20px;">{lis}</ul>'


def render_gaps(headers, rows):
    return f"""
    <div style="background:#FFFFFF;border-radius:12px;padding:24px 28px;
                margin-bottom:20px;border:1px solid #E5E7EB;">
      <div style="font-size:13px;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.1em;color:#6B7280;margin-bottom:16px;">
        Gaps Detectados
      </div>
      {render_styled_table(headers, rows, monospace_col=0)}
    </div>
    """


def render_recomendaciones(data):
    canales_table = render_styled_table(
        data["canales"]["headers"],
        data["canales"]["rows"],
        monospace_col=0
    )
    keywords_list = render_bullet_list(data["keywords"])
    temas_list = render_bullet_list(data["temas"])

    canales_block = f"""
    <div style="margin-bottom:20px;">
      <div style="font-size:13px;font-weight:600;color:#111827;margin-bottom:10px;">
        Nuevos canales a añadir
      </div>
      {canales_table}
    </div>
    """ if data["canales"]["rows"] else ""

    keywords_block = f"""
    <div style="margin-bottom:20px;">
      <div style="font-size:13px;font-weight:600;color:#111827;margin-bottom:8px;">
        Keywords a ajustar
      </div>
      {keywords_list}
    </div>
    """ if data["keywords"] else ""

    temas_block = f"""
    <div style="margin-bottom:20px;">
      <div style="font-size:13px;font-weight:600;color:#111827;margin-bottom:8px;">
        Temas emergentes
      </div>
      {temas_list}
    </div>
    """ if data["temas"] else ""

    return f"""
    <div style="background:#FFFFFF;border-radius:12px;padding:24px 28px;
                margin-bottom:20px;border:1px solid #E5E7EB;">
      <div style="font-size:13px;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.1em;color:#6B7280;margin-bottom:16px;">
        Recomendaciones
      </div>
      {canales_block}{keywords_block}{temas_block}
    </div>
    """


def render_aplicabilidad(subsections):
    if not subsections:
        return ""

    items = ""
    for sub in subsections:
        items += f"""
        <div style="margin-bottom:18px;">
          <div style="font-size:14px;font-weight:700;color:#111827;margin-bottom:8px;">
            {sub["title"]}
          </div>
          <div style="font-size:14px;color:#374151;line-height:1.65;">
            {sub["body_html"]}
          </div>
        </div>
        """

    return f"""
    <div style="background:#FFFFFF;border-radius:12px;padding:24px 28px;
                margin-bottom:20px;border:1px solid #E5E7EB;">
      <div style="font-size:13px;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.1em;color:#6B7280;margin-bottom:16px;">
        Aplicabilidad OPENLAB
      </div>
      {items}
    </div>
    """


def render_footer(date_to):
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0"
           style="background:#000000;border-radius:0 0 16px 16px;
                  padding:22px 32px;">
      <tr>
        <td style="color:#6B7280;font-size:12px;">
          OPENLAB Radar · Digest Semanal
          {f'· {date_to}' if date_to else ''}
        </td>
        <td style="text-align:right;">
          <a href="https://openlabstudio.com"
             style="color:#CCFF00;font-size:12px;font-weight:600;
                    text-decoration:none;">
            openlab.ai →
          </a>
        </td>
      </tr>
    </table>
    """


def build_html(content):
    sections = split_sections(content)

    title_line = sections.get("title", "")
    date_from, date_to = parse_date_range(title_line)

    # ── Parse each section ──────────────────────────────────────────────────

    # Resumen
    resumen_text = ""
    for key in sections:
        if "resumen" in key.lower():
            resumen_text = sections[key]
            break
    resumen_data = parse_resumen(resumen_text) if resumen_text else {}

    # Tendencias
    tendencias_text = ""
    for key in sections:
        if "tendencia" in key.lower():
            tendencias_text = sections[key]
            break
    trends = parse_tendencias(tendencias_text) if tendencias_text else []

    # Top 5
    top5_text = ""
    for key in sections:
        if "top" in key.lower() and "vídeo" in key.lower():
            top5_text = sections[key]
            break
        elif "top" in key.lower() and "video" in key.lower():
            top5_text = sections[key]
            break
    videos = parse_top5(top5_text) if top5_text else []

    # Gaps
    gaps_text = ""
    for key in sections:
        if "gap" in key.lower():
            gaps_text = sections[key]
            break
    gaps_headers, gaps_rows = parse_gaps_table(gaps_text) if gaps_text else ([], [])

    # Recomendaciones
    reco_text = ""
    for key in sections:
        if "recomendac" in key.lower():
            reco_text = sections[key]
            break
    reco_data = parse_recomendaciones(reco_text) if reco_text else {
        "canales": {"headers": [], "rows": []},
        "keywords": [],
        "temas": []
    }

    # Aplicabilidad
    aplic_text = ""
    for key in sections:
        if "aplicab" in key.lower():
            aplic_text = sections[key]
            break
    aplic_subsections = parse_aplicabilidad(aplic_text) if aplic_text else []

    # ── Render ───────────────────────────────────────────────────────────────
    header_html = render_header(date_from, date_to)
    resumen_html = render_resumen(resumen_data) if resumen_data else ""
    tendencias_html = render_tendencias(trends)
    top5_html = render_top5(videos)
    gaps_html = ""
    reco_html = ""
    aplic_html = render_aplicabilidad(aplic_subsections)
    footer_html = render_footer(date_to)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>OPENLAB Radar — Digest Semanal {date_from} / {date_to}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap"
        rel="stylesheet" />
</head>
<body style="margin:0;padding:0;background:#F3F4F6;
             font-family:'Montserrat',Arial,sans-serif;">

  <!-- Outer wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background:#F3F4F6;padding:32px 16px;">
    <tr>
      <td align="center">

        <!-- Card container -->
        <table width="660" cellpadding="0" cellspacing="0"
               style="max-width:660px;width:100%;background:#F3F4F6;
                      border-radius:16px;overflow:hidden;">
          <tr><td>

            <!-- Header -->
            {header_html}

            <!-- Body padding wrapper -->
            <div style="padding:24px 28px;">

              {resumen_html}
              {tendencias_html}
              {top5_html}
              {gaps_html}
              {reco_html}
              {aplic_html}

            </div>

            <!-- Footer -->
            {footer_html}

          </td></tr>
        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""


def main():
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    html = build_html(content)
    sys.stdout.write(html)


if __name__ == "__main__":
    main()
