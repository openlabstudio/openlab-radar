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
    "skill-design":      ("🛠", "#CCFF00", "#000000"),
    "orchestration":     ("🤖", "#CCFF00", "#000000"),
    "market-signal":     ("📊", "#CCFF00", "#000000"),
    "delivery-adoption": ("🚀", "#CCFF00", "#000000"),
}

LOGO_URL = "data:image/png;base64,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UmVhZHlxyWU8AAADe2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgOS4wLWMwMDAgNzkuMTcxYzI3ZmFiLCAyMDIyLzA4LzE2LTIyOjM1OjQxICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSIyQTkzNTlDMDY1N0YxQTc2Qzk1NEIxNkJFODk5Qjg2QiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpFNEYyQzA0ODlEQkYxMUVFQTMzRkE1ODlCQUQyRTgyOSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpFNEYyQzA0NzlEQkYxMUVFQTMzRkE1ODlCQUQyRTgyOSIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxNyAoV2luZG93cykiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDplMjUxYWNhOS1iYjlmLWVmNGYtYTMzMy03NTE0ZGI5MTI0NDEiIHN0UmVmOmRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDpmOTdmOWY1Ny05ZDM4LTM2NDctOTljMC0xYjdlN2IxOTljM2IiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBl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"


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
    date_label = "-".join(reversed(date_to.split("-"))) if date_to else ""
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
<html lang="es" style="color-scheme:light only;">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="light only" />
  <meta name="supported-color-schemes" content="light" />
  <title>OPENLAB Radar — Digest Semanal {date_from} / {date_to}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap"
        rel="stylesheet" />
</head>
<body style="margin:0;padding:0;background:#F3F4F6;
             font-family:'Montserrat',Arial,sans-serif;
             color-scheme:light only;">

  <!-- Outer wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background:#F3F4F6;padding:32px 16px;color-scheme:light only;">
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
