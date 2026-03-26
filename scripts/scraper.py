#!/usr/bin/env python3
"""
OPENLAB Radar - YouTube Scraper
Busca vídeos nuevos en canales monitorizados y por keywords.
Guarda candidatos en SQLite para evaluación posterior por Claude Code.

Uso: python scraper.py [--lookback HOURS] [--dry-run]
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "radar.db"


def load_config():
    """Carga configuración de canales y keywords."""
    with open(CONFIG_DIR / "channels.yaml", "r") as f:
        channels_cfg = yaml.safe_load(f)
    with open(CONFIG_DIR / "keywords.yaml", "r") as f:
        keywords_cfg = yaml.safe_load(f)
    return channels_cfg, keywords_cfg


def init_db():
    """Inicializa SQLite con tabla de vídeos."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            channel_name TEXT,
            channel_handle TEXT,
            description TEXT,
            published_at TEXT,
            duration_seconds INTEGER,
            url TEXT,
            thumbnail_url TEXT,
            view_count INTEGER DEFAULT 0,
            lang TEXT DEFAULT 'en',
            discovered_at TEXT NOT NULL,
            status TEXT DEFAULT 'candidate',
            score REAL DEFAULT 0,
            categories TEXT DEFAULT '[]',
            briefing_date TEXT,
            ingested_to_notebooklm INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_status ON videos(status)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_discovered ON videos(discovered_at)
    """)
    conn.commit()
    return conn


def get_youtube_client():
    """Crea cliente de YouTube Data API."""
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print("ERROR: YOUTUBE_API_KEY no configurada.", file=sys.stderr)
        print("Exporta tu API key: export YOUTUBE_API_KEY='tu-key-aquí'", file=sys.stderr)
        sys.exit(1)
    return build("youtube", "v3", developerKey=api_key)


def resolve_channel_id(youtube, handle):
    """Resuelve un @handle de YouTube a un channel_id."""
    try:
        # Intentar buscar por handle (sin @)
        clean_handle = handle.lstrip("@")
        response = youtube.channels().list(
            part="id,contentDetails",
            forHandle=clean_handle
        ).execute()

        if response.get("items"):
            return response["items"][0]["id"]

        # Fallback: buscar por nombre
        response = youtube.search().list(
            part="snippet",
            q=clean_handle,
            type="channel",
            maxResults=1
        ).execute()
        if response.get("items"):
            return response["items"][0]["snippet"]["channelId"]

    except HttpError as e:
        print(f"  WARN: No se pudo resolver {handle}: {e}", file=sys.stderr)
    return None


def get_channel_videos(youtube, channel_id, published_after):
    """Obtiene vídeos recientes de un canal."""
    videos = []
    try:
        response = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            publishedAfter=published_after,
            order="date",
            type="video",
            maxResults=10
        ).execute()

        for item in response.get("items", []):
            videos.append({
                "video_id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "channel_name": item["snippet"]["channelTitle"],
                "description": item["snippet"]["description"],
                "published_at": item["snippet"]["publishedAt"],
                "thumbnail_url": item["snippet"]["thumbnails"].get("high", {}).get("url", ""),
            })
    except HttpError as e:
        print(f"  WARN: Error buscando vídeos del canal {channel_id}: {e}", file=sys.stderr)
    return videos


def search_by_keywords(youtube, keywords, published_after, max_results=5):
    """Busca vídeos por keywords."""
    videos = []
    for kw in keywords:
        try:
            response = youtube.search().list(
                part="snippet",
                q=kw,
                publishedAfter=published_after,
                order="date",
                type="video",
                maxResults=max_results,
                relevanceLanguage="en"
            ).execute()

            for item in response.get("items", []):
                videos.append({
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "channel_name": item["snippet"]["channelTitle"],
                    "description": item["snippet"]["description"],
                    "published_at": item["snippet"]["publishedAt"],
                    "thumbnail_url": item["snippet"]["thumbnails"].get("high", {}).get("url", ""),
                    "matched_keyword": kw,
                })
        except HttpError as e:
            print(f"  WARN: Error buscando '{kw}': {e}", file=sys.stderr)
    return videos


def get_video_details(youtube, video_ids):
    """Obtiene duración y estadísticas de vídeos."""
    details = {}
    # API acepta hasta 50 IDs por request
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        try:
            response = youtube.videos().list(
                part="contentDetails,statistics",
                id=",".join(batch)
            ).execute()
            for item in response.get("items", []):
                duration_str = item.get("contentDetails", {}).get("duration", "PT0S")
                details[item["id"]] = {
                    "duration_seconds": parse_duration(duration_str),
                    "view_count": int(item["statistics"].get("viewCount", 0)),
                }
        except HttpError as e:
            print(f"  WARN: Error obteniendo detalles: {e}", file=sys.stderr)
    return details


def parse_duration(duration_str):
    """Parsea duración ISO 8601 (PT1H2M3S) a segundos."""
    import re
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_str)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


_NON_LATIN = re.compile(
    r'[\u0400-\u04FF'   # Cirílico
    r'\u0600-\u06FF'    # Árabe
    r'\u0590-\u05FF'    # Hebreo
    r'\u0900-\u097F'    # Devanagari
    r'\u3040-\u30FF'    # Hiragana / Katakana
    r'\u4E00-\u9FFF'    # CJK
    r'\uAC00-\uD7AF'    # Coreano
    r']'
)


def is_latin_language(title):
    """Devuelve True si el título está en escritura latina (inglés / español)."""
    return not _NON_LATIN.search(title)


def matches_exclude_terms(title, description, exclude_terms):
    """Comprueba si un vídeo contiene términos de exclusión."""
    text = f"{title} {description}".lower()
    return any(term.lower() in text for term in exclude_terms)


def save_candidates(conn, videos):
    """Guarda vídeos nuevos en SQLite. Devuelve cuántos se insertaron."""
    now = datetime.now(timezone.utc).isoformat()
    inserted = 0
    for v in videos:
        try:
            conn.execute("""
                INSERT OR IGNORE INTO videos
                (video_id, title, channel_name, channel_handle, description,
                 published_at, duration_seconds, url, thumbnail_url,
                 view_count, lang, discovered_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'candidate')
            """, (
                v["video_id"],
                v["title"],
                v["channel_name"],
                v.get("channel_handle", ""),
                v.get("description", ""),
                v.get("published_at", ""),
                v.get("duration_seconds", 0),
                f"https://www.youtube.com/watch?v={v['video_id']}",
                v.get("thumbnail_url", ""),
                v.get("view_count", 0),
                v.get("lang", "en"),
                now,
            ))
            if conn.total_changes:
                inserted += 1
        except sqlite3.Error as e:
            print(f"  WARN: Error guardando {v['video_id']}: {e}", file=sys.stderr)
    conn.commit()
    return inserted


def export_candidates_json(conn, date_str):
    """Exporta candidatos del día a JSON para el evaluador Claude."""
    cursor = conn.execute("""
        SELECT video_id, title, channel_name, description, published_at,
               duration_seconds, url, view_count, lang
        FROM videos
        WHERE status = 'candidate'
        AND date(discovered_at) = ?
        ORDER BY view_count DESC
    """, (date_str,))

    candidates = []
    for row in cursor:
        candidates.append({
            "video_id": row[0],
            "title": row[1],
            "channel": row[2],
            "description": row[3][:500],  # Truncar para no volar el contexto
            "published_at": row[4],
            "duration_minutes": round(row[5] / 60, 1),
            "url": row[6],
            "views": row[7],
            "lang": row[8],
        })

    output_path = DATA_DIR / f"candidates-{date_str}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)

    print(f"Exportados {len(candidates)} candidatos a {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="OPENLAB Radar - YouTube Scraper")
    parser.add_argument("--lookback", type=int, default=None,
                        help="Horas hacia atrás para buscar (override config)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Solo mostrar qué haría, sin guardar")
    args = parser.parse_args()

    channels_cfg, keywords_cfg = load_config()
    lookback = args.lookback or keywords_cfg.get("lookback_hours", 24)
    published_after = (datetime.now(timezone.utc) - timedelta(hours=lookback)).strftime("%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"=== OPENLAB Radar Scraper ===")
    print(f"Fecha: {today}")
    print(f"Lookback: {lookback}h (desde {published_after})")
    print()

    youtube = get_youtube_client()
    conn = init_db()
    all_videos = []

    # 1. Buscar por canales monitorizados
    print("--- Buscando en canales monitorizados ---")
    channel_ids_cache = {}
    for ch in channels_cfg.get("channels", []):
        handle = ch["handle"]
        name = ch["name"]
        print(f"  {name} ({handle})...", end=" ")

        channel_id = resolve_channel_id(youtube, handle)
        if not channel_id:
            print("NO ENCONTRADO")
            continue
        channel_ids_cache[handle] = channel_id

        videos = get_channel_videos(youtube, channel_id, published_after)
        for v in videos:
            v["channel_handle"] = handle
            v["lang"] = ch.get("lang", "en")
        all_videos.extend(videos)
        print(f"{len(videos)} vídeos")

    # 2. Buscar por keywords (todas las categorías)
    print("\n--- Buscando por keywords ---")
    all_keywords = []
    for cat_key, cat in keywords_cfg.get("categories", {}).items():
        kws = cat.get("keywords", [])
        all_keywords.extend(kws)

    # Deduplicar keywords
    all_keywords = list(set(all_keywords))
    print(f"  {len(all_keywords)} keywords únicas")

    # Buscar en lotes de 3 resultados por keyword para no quemar quota
    keyword_videos = search_by_keywords(youtube, all_keywords, published_after, max_results=3)
    all_videos.extend(keyword_videos)
    print(f"  {len(keyword_videos)} vídeos encontrados por keywords")

    # 3. Deduplicar por video_id
    seen = set()
    unique_videos = []
    for v in all_videos:
        if v["video_id"] not in seen:
            seen.add(v["video_id"])
            unique_videos.append(v)
    print(f"\n{len(unique_videos)} vídeos únicos (de {len(all_videos)} totales)")

    # 4. Obtener duración y estadísticas
    print("Obteniendo detalles de vídeos...")
    video_ids = [v["video_id"] for v in unique_videos]
    details = get_video_details(youtube, video_ids)
    for v in unique_videos:
        d = details.get(v["video_id"], {})
        v["duration_seconds"] = d.get("duration_seconds", 0)
        v["view_count"] = d.get("view_count", 0)

    # 5. Filtrar por duración y términos de exclusión
    exclude_terms = keywords_cfg.get("exclude_terms", [])
    quality = keywords_cfg.get("quality_filters", {})
    min_dur = quality.get("min_duration_minutes", 5) * 60
    max_dur = quality.get("max_duration_minutes", 120) * 60

    filtered = []
    for v in unique_videos:
        dur = v.get("duration_seconds", 0)
        if dur < min_dur:
            continue
        if dur > max_dur:
            continue
        if not is_latin_language(v.get("title", "")):
            continue
        if matches_exclude_terms(v.get("title", ""), v.get("description", ""), exclude_terms):
            continue
        filtered.append(v)

    print(f"{len(filtered)} vídeos tras filtros de calidad (de {len(unique_videos)})")

    if args.dry_run:
        print("\n[DRY RUN] Candidatos que se guardarían:")
        for v in filtered[:20]:
            dur_min = round(v.get("duration_seconds", 0) / 60, 1)
            print(f"  - [{dur_min}min] {v['title']} ({v['channel_name']})")
        return

    # 6. Guardar en SQLite
    inserted = save_candidates(conn, filtered)
    print(f"{inserted} vídeos nuevos guardados en DB")

    # 7. Exportar candidatos del día a JSON
    export_candidates_json(conn, today)

    conn.close()
    print("\n=== Scraper completado ===")


if __name__ == "__main__":
    main()
