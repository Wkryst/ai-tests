#!/usr/bin/env python3
"""Buduje dashboard z youtube_videos.json.

Uzycie:
    python3 dashboard/build.py                 # -> dashboard/index.html
    python3 dashboard/build.py --fragment OUT  # strona bez <html>/<head> (do publikacji jako Artifact)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "youtube_videos.json"
TEMPLATE = ROOT / "template.html"

# Nazwy kanalow nie sa zapisane w JSON - uzupelnij, aby zastapic skrocone ID.
CHANNEL_NAMES = {}


def slim(videos):
    """Odrzuca transkrypcje (ok. 1,3 MB) i zostawia pola potrzebne dashboardowi."""
    out = []
    for v in videos:
        out.append({
            "video_id": v["video_id"],
            "channel_id": v["channel_id"],
            "title": v["title"],
            "url": v["url"],
            "published_at": v["published_at"],
            "transcript_len": len(v.get("transcript") or ""),
            "status": v.get("status") or ("processed" if v.get("news_processed") else "unprocessed"),
            "news": [
                {
                    "title": n["title"],
                    "summary": n["summary"],
                    "category": n["category"],
                    "entities": n.get("entities", []),
                    "importance": n["importance"],
                    "confidence": n["confidence"],
                }
                for n in v.get("news") or []
            ],
        })
    return out


def main():
    videos = json.loads(SRC.read_text(encoding="utf-8"))
    payload = json.dumps({"videos": slim(videos), "channelNames": CHANNEL_NAMES},
                         ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)

    if len(sys.argv) == 3 and sys.argv[1] == "--fragment":
        Path(sys.argv[2]).write_text(page, encoding="utf-8")
        print(f"zapisano {sys.argv[2]}")
        return

    doc = ('<!doctype html>\n<html lang="pl">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           '</head>\n<body>\n' + page + '\n</body>\n</html>\n')
    out = ROOT / "index.html"
    out.write_text(doc, encoding="utf-8")
    print(f"zapisano {out} ({len(videos)} filmow)")


if __name__ == "__main__":
    main()
