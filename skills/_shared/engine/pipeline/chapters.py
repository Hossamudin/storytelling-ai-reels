"""YouTube chapters from a motion project's chrome.json sections.

Usage: python engine/pipeline/chapters.py <name> [--part composition] [--titles titles.json]

Reads <part>/chrome.json "sections" ([{"t", "label", "title"?}]) + the root duration and writes
projects/<name>/deliverables/<part>_youtube_chapters.txt.
YouTube rules enforced: first chapter at 00:00, >= 3 chapters, each >= 10 s (short sections are
merged into the previous one). "title" (Arabic, for the description) falls back to "label".
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def ts(t):
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60:02d}:{t % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--part", default="composition")
    a = ap.parse_args()
    out = C.project_path(a.name) / a.part
    chrome = json.loads((out / "chrome.json").read_text(encoding="utf-8"))
    html = (out / "index.html").read_text(encoding="utf-8")
    root_tag = re.search(r'<div[^>]*?[ 	]id="root"[^>]*>', html).group(0)  # attribute order varies (Studio edits)
    total = float(re.search(r'data-duration="([\d.]+)"', root_tag).group(1))
    secs = sorted(chrome.get("sections", []), key=lambda s: s["t"])
    secs = [dict(s) for s in secs if s.get("chapter", True)]
    if not secs or secs[0]["t"] > 0:
        secs.insert(0, {"t": 0, "label": "INTRO"})
    secs[0]["t"] = 0
    merged = []
    for i, s in enumerate(secs):
        end = secs[i + 1]["t"] if i + 1 < len(secs) else total
        if merged and end - s["t"] < 10:
            continue  # too short for YouTube: fold into the previous chapter
        if merged and s["t"] - merged[-1]["t"] < 10:
            merged[-1] = s | {"t": merged[-1]["t"]}
            continue
        merged.append(s)
    lines = [f"{ts(s['t'])} {s.get('title') or s['label']}" for s in merged]
    if len(lines) < 3:
        print("! fewer than 3 chapters — YouTube will ignore them")
    dest = C.project_path(a.name) / "deliverables" / f"{a.part}_youtube_chapters.txt"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nOK -> {dest}")


if __name__ == "__main__":
    main()
