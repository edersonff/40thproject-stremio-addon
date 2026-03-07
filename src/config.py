from dataclasses import dataclass
from typing import List


@dataclass
class Episode:
    number: int
    download_id: str


@dataclass
class Series:
    id: str
    name: str
    poster: str
    episodes: List[Episode]


SOURCE_URL = "https://40thproject.ai"
DOWNLOAD_BASE_URL = "https://downloads.40thproject.ai/api/public/dl/"
REFERER_HEADER = {"Referer": "https://40thproject.ai/"}

ADDON_ID = "ai.40thproject.stremio"
ADDON_VERSION = "1.0.0"
ADDON_NAME = "40th PROJECT"
ADDON_DESCRIPTION = "Dragon Ball remastered in high quality - 1080p NTSC 23.976fps"

SERIES_TEMPLATES = {
    "db": {
        "id": "tt0088509",
        "name": "Dragon Ball",
        "poster": "https://40thproject.ai/static/images/db_logos/db.png",
    },
    "dbz": {
        "id": "tt0121220",
        "name": "Dragon Ball Z",
        "poster": "https://40thproject.ai/static/images/db_logos/dbz.png",
    },
}

VIDEO_SIZE_APPROX = 6400000000
STREAM_FPS = "23.976"
STREAM_RESOLUTION = "1080p"
