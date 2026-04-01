#!/usr/bin/env python3
"""
MCP server para transcripts de YouTube con soporte de proxy residencial.
Implementa la tool: get_transcript(url, lang)

Configuración via variables de entorno (config/.env):
  YOUTUBE_PROXY_URL  — URL del proxy residencial (opcional)
                       Formato: http://usuario:password@host:puerto

Uso como MCP server (stdio):
  python3 scripts/mcp_transcript_server.py
"""

import os
import re
import sys
from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    IpBlocked,
)

# Cargar .env si existe
_env_path = os.path.join(os.path.dirname(__file__), "..", "config", ".env")
if os.path.exists(_env_path):
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                value = value.strip().strip('"').strip("'")
                os.environ.setdefault(key.strip(), value)

mcp = FastMCP("youtube-transcript")


def _extract_video_id(url: str) -> str:
    """Extrae el video ID de una URL de YouTube."""
    patterns = [
        r"(?:v=|youtu\.be/|embed/|shorts/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"No se pudo extraer el video ID de: {url}")


def _build_proxies() -> dict | None:
    """Construye el dict de proxies si YOUTUBE_PROXY_URL está configurado."""
    proxy_url = os.environ.get("YOUTUBE_PROXY_URL", "").strip()
    if not proxy_url:
        return None
    return {"http": proxy_url, "https": proxy_url}


@mcp.tool()
def get_transcript(url: str, lang: str = "en") -> str:
    """
    Obtiene el transcript de un vídeo de YouTube.

    Args:
        url:  URL del vídeo o video ID directo.
        lang: Código de idioma preferido (ej: 'en', 'es'). Fallback automático.

    Returns:
        Transcript completo como texto plano.
    """
    try:
        video_id = _extract_video_id(url)
    except ValueError as e:
        return f"ERROR: {e}"

    proxies = _build_proxies()
    api = YouTubeTranscriptApi(proxies=proxies)

    # Intentar idioma solicitado, luego inglés, luego cualquier disponible
    langs_to_try = [lang]
    if lang != "en":
        langs_to_try.append("en")

    transcript_data = None
    error_msg = None

    for attempt_lang in langs_to_try:
        try:
            transcript_data = api.fetch(video_id, languages=[attempt_lang])
            break
        except NoTranscriptFound:
            error_msg = f"No hay transcript en idioma '{attempt_lang}'"
            continue
        except TranscriptsDisabled:
            return "ERROR: Los transcripts están desactivados para este vídeo."
        except VideoUnavailable:
            return "ERROR: El vídeo no está disponible."
        except IpBlocked:
            proxy_hint = "" if proxies else " Configura YOUTUBE_PROXY_URL en config/.env."
            return f"ERROR: IP bloqueada por YouTube.{proxy_hint}"
        except Exception as e:
            return f"ERROR inesperado: {e}"

    # Fallback: cualquier transcript disponible
    if transcript_data is None:
        try:
            transcript_list = api.list(video_id)
            transcript_data = transcript_list.find_transcript(
                langs_to_try
            ).fetch()
        except Exception:
            try:
                # Último recurso: primer transcript disponible
                first = next(iter(transcript_list))
                transcript_data = first.fetch()
            except Exception as e:
                return f"ERROR: No se pudo obtener ningún transcript. {error_msg or e}"

    # Convertir a texto plano
    snippets = transcript_data.to_raw_data()
    text = " ".join(s["text"] for s in snippets)
    return text


if __name__ == "__main__":
    mcp.run(transport="stdio")
