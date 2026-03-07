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


def build_catalog_metas(episodes_by_series: Dict[str, List[ScrapedEpisode]]) -> dict:
    metas = []
    for key, template in SERIES_TEMPLATES.items():
        if key in episodes_by_series and episodes_by_series[key]:
            metas.append(
                {
                    "id": template["id"],
                    "type": "series",
                    "name": template["name"],
                    "poster": template["poster"],
                    "background": template["poster"],
                    "description": f"{template['name']} remastered - {STREAM_RESOLUTION} NTSC {STREAM_FPS}fps",
                }
            )
    return {"metas": metas}


def build_series_meta(series_key: str, episodes: List[ScrapedEpisode]) -> dict:
    template = SERIES_TEMPLATES[series_key]
    videos = [
        {
            "id": f"{template['id']}:1:{ep.episode_number}",
            "title": f"Episode {ep.episode_number}",
            "season": 1,
            "episode": ep.episode_number,
        }
        for ep in sorted(episodes, key=lambda x: x.episode_number)
    ]

    return {
        "meta": {
            "id": template["id"],
            "type": "series",
            "name": template["name"],
            "poster": template["poster"],
            "background": template["poster"],
            "description": f"{template['name']} remastered by 40th PROJECT.\n\n"
            f"Quality: {STREAM_RESOLUTION} NTSC {STREAM_FPS}fps\n"
            f"Episodes: {len(episodes)}",
            "videos": videos,
        }
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

    for series_key, episodes in episodes_by_series.items():
        if not episodes:
            continue

        template = SERIES_TEMPLATES[series_key]

        for episode in episodes:
            stream_id = f"{template['id']}:1:{episode.episode_number}"
            write_json(
                f"{output_dir}/stream/series/{stream_id}.json",
                build_stream(episode, series_key),
            )

    print(f"Generated addon files in {output_dir}/")
    for key, eps in episodes_by_series.items():
        print(f"  {SERIES_TEMPLATES[key]['name']}: {len(eps)} episodes")
