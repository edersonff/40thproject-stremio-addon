import re
from dataclasses import dataclass
from typing import Dict, List
import urllib.request
import urllib.error

from config import SOURCE_URL


@dataclass
class ScrapedEpisode:
    series_key: str
    episode_number: int
    download_id: str


def fetch_html(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def extract_ntsc_episodes(html: str) -> List[ScrapedEpisode]:
    pattern = r'id="(23Modal([^"]+))"[^>]*>.*?href="https://downloads\.40thproject\.ai/api/public/dl/([^"]+)"'
    matches = re.findall(pattern, html, re.DOTALL)

    episodes = []
    for _, modal_suffix, download_id in matches:
        if modal_suffix.startswith("z"):
            series_key = "dbz"
            ep_num = int(modal_suffix[1:])
        else:
            series_key = "db"
            ep_num = int(modal_suffix)

        episodes.append(
            ScrapedEpisode(
                series_key=series_key, episode_number=ep_num, download_id=download_id
            )
        )

    return episodes


def group_by_series(episodes: List[ScrapedEpisode]) -> Dict[str, List[ScrapedEpisode]]:
    grouped = {"db": [], "dbz": []}
    for ep in episodes:
        if ep.series_key in grouped:
            grouped[ep.series_key].append(ep)
    return grouped


def scrape_all_episodes() -> Dict[str, List[ScrapedEpisode]]:
    html = fetch_html(SOURCE_URL)
    episodes = extract_ntsc_episodes(html)
    return group_by_series(episodes)
