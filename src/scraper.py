import re
from dataclasses import dataclass
from typing import Dict, List
import urllib.request
import urllib.error

from config import DOWNLOAD_BASE_URL, SOURCE_URL


@dataclass
class ScrapedEpisode:
    series_key: str
    episode_number: int
    download_id: str


def fetch_html(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


# NTSC (23.976fps) modals: id="23Modal001" (DB), id="23Modalz001" (DBZ)
MODAL_RE = re.compile(r'id="23Modal(z?\d+)"')

# Download anchors inside a modal: href is followed by a server badge image
# (40thproject_fhd = 1080p, 40thproject_sd = 480p; telegram links are ignored).
LINK_RE = re.compile(
    r'href="(' + re.escape(DOWNLOAD_BASE_URL) + r'[^"]+)"[^>]*>'
    r'\s*<img[^>]*src="/static/images/download/servers/(40thproject_[a-z]+)\.png"'
)


def extract_ntsc_episodes(html: str) -> List[ScrapedEpisode]:
    modal_starts = [(m.start(), m.group(1)) for m in MODAL_RE.finditer(html)]

    episodes = []
    for i, (start, suffix) in enumerate(modal_starts):
        end = modal_starts[i + 1][0] if i + 1 < len(modal_starts) else len(html)
        links = LINK_RE.findall(html[start:end])

        if not links:
            continue

        # Prefer the 1080p FHD server when present
        fhd = [download_id for download_id, server in links if server == "40thproject_fhd"]
        download_id = (fhd[0] if fhd else links[0][0]).rsplit("/", 1)[-1]

        if suffix.startswith("z"):
            series_key = "dbz"
            ep_num = int(suffix[1:])
        else:
            series_key = "db"
            ep_num = int(suffix)

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
