import json
import os
from typing import Dict, List

from config import (
    ADDON_ID,
    ADDON_VERSION,
    ADDON_NAME,
    ADDON_DESCRIPTION,
    SERIES_TEMPLATES,
    DOWNLOAD_BASE_URL,
    REFERER_HEADER,
    VIDEO_SIZE_APPROX,
    STREAM_FPS,
    STREAM_RESOLUTION,
)
from scraper import ScrapedEpisode


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_manifest() -> dict:
    return {
        "id": ADDON_ID,
        "version": ADDON_VERSION,
        "name": ADDON_NAME,
        "description": ADDON_DESCRIPTION,
        "logo": "https://40thproject.ai/static/images/download/servers/40thproject.png",
        "background": "https://40thproject.ai/static/images/download/servers/40thproject.png",
        "contactEmail": "ederr@ederr.com",
        "resources": [{"name": "stream", "types": ["series"], "idPrefixes": ["tt"]}],
        "catalogs": [],
        "behaviorHints": {
            "adult": False,
            "p2p": False,
            "configurable": False,
            "configurationRequired": False,
        },
    }


def build_stream(episode: ScrapedEpisode, series_key: str) -> dict:
    template = SERIES_TEMPLATES[series_key]
    return {
        "streams": [
            {
                "url": f"{DOWNLOAD_BASE_URL}{episode.download_id}",
                "name": ADDON_NAME,
                "title": f"{STREAM_RESOLUTION} NTSC {STREAM_FPS}fps",
                "description": f"NTSC {STREAM_FPS}fps | {STREAM_RESOLUTION}\n"
                f"~6GB\n"
                f"{template['name']} Ep.{episode.episode_number:02d}",
                "behaviorHints": {
                    "notWebReady": True,
                    "videoSize": VIDEO_SIZE_APPROX,
                    "filename": f"{template['name']}.{episode.episode_number:02d}.40th.PROJECT.{STREAM_RESOLUTION}.mkv",
                    "bingeGroup": f"40thproject-{series_key}",
                    "proxyHeaders": {"request": REFERER_HEADER},
                },
            }
        ]
    }


def generate_addon_files(
    episodes_by_series: Dict[str, List[ScrapedEpisode]], output_dir: str = "dist"
) -> None:
    ensure_dir(output_dir)
    ensure_dir(f"{output_dir}/stream/series")

    write_json(f"{output_dir}/manifest.json", build_manifest())

    total_files = 0
    for series_key, episodes in episodes_by_series.items():
        if not episodes:
            continue

        template = SERIES_TEMPLATES[series_key]

        for episode in episodes:
            stream_data = build_stream(episode, series_key)
            for series_id in template["ids"]:
                stream_id = f"{series_id}:1:{episode.episode_number}"
                write_json(
                    f"{output_dir}/stream/series/{stream_id}.json",
                    stream_data,
                )
                total_files += 1

    print(f"Generated addon files in {output_dir}/")
    for key, eps in episodes_by_series.items():
        ids_count = len(SERIES_TEMPLATES[key]["ids"])
        print(
            f"  {SERIES_TEMPLATES[key]['name']}: {len(eps)} episodes x {ids_count} IDs = {len(eps) * ids_count} files"
        )
    print(f"Total stream files: {total_files}")
