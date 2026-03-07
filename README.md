# 40th PROJECT Stremio Addon

A community-maintained Stremio addon that provides access to the [40th PROJECT](https://40thproject.ai) Dragon Ball restoration project.

## Disclaimer

This addon is **independent and unofficial**. It is not affiliated with, maintained by, or endorsed by the 40th PROJECT team.

If you are the content that should be removed from this repository, please contact: ederr@ederr.com

## What is this?

A Stremio addon that provides Dragon Ball and Dragon Ball Z episodes from the 40th PROJECT restoration. The videos are:
- **1080p NTSC 23.976fps** (original frame rate)
- **H.264 video**
- **5.1 surround audio** (Japanese, English, Latin American Spanish, Portuguese)
- **Multiple subtitle tracks**

## How it works

The addon is **static** - no server required. It consists of:
1. A Python script scrapes the 40th PROJECT website daily
2. Generates JSON files for each episode
3. Deploys to GitHub Pages
4. Stremio fetches these JSON files directly

5. **proxyHeaders** with `Referer: https://40thproject.ai/` to Stremio's streaming server to handle the video requests

## Stack

- **Python 3.11** - stdlib only, no dependencies
- **GitHub Actions** - daily builds at 06:00 UTC
- **GitHub Pages** - free static hosting

## Files

```
40thproject-stremio-addon/
├── src/
│   ├── config.py      # URLs, constants, data models
│   ├── scraper.py     # HTML parsing logic
│   ├── generator.py   # JSON file generation
│   └── main.py         # Entry point
├── .github/workflows/
│   └── build.yml      # CI/CD pipeline
└── README.md
```

## Install in Stremio

1. Open Stremio
2. Go to Settings (gear icon)
3. Click "Add addon"
4. Paste: `https://YOUR_USERNAME.github.io/40thproject-stremio-addon/manifest.json`
5. Click "Install"

## Local Development

```bash
cd 40thproject-stremio-addon/src
python main.py
cd dist
python -m http.server 8080
```

Open: `http://localhost:8080/manifest.json`

## License

MIT License
