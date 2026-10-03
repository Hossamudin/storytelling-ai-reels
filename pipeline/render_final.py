"""One command for the final deliverable: preflight -> render -> verify -> master -> chapters.

Usage: python pipeline/render_final.py <name> [--part composition] [--quality delivery]

Output: projects/<name>/deliverables/<name>-<part>.mp4 (mastered -14 LUFS / -1.2 dBTP)
        + the raw render in <part>/renders/ + YouTube chapters (videos > 60 s with sections).
Stops at the first failure with the reason. Never render from Studio for a final: Studio renders
skip the preflight (CDN scripts, preview-quality screen edits, grain, stale assets).
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

PIPE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--part", default="composition")
    ap.add_argument("--quality", default="delivery", choices=["draft", "looks", "delivery"])
    a = ap.parse_args()
    pp = C.project_path(a.name)
    part = pp / a.part

    print("1/5 preflight")
    r = subprocess.run([sys.executable, str(PIPE / "preflight.py"), a.name, "--part", a.part])
    if r.returncode:
        sys.exit("Stopped: fix the preflight problems above, then re-run.")

    print("2/5 render (this takes a while)")
    stamp = time.strftime("%Y%m%d-%H%M")
    raw = part / "renders" / f"{a.name}-{a.part}-{stamp}.mp4"
    raw.parent.mkdir(parents=True, exist_ok=True)
    r = C.run(["npx", "hyperframes", "render", "--quality", a.quality, "--strict", "-o", str(raw)], cwd=str(part), timeout=6 * 3600)
    log = (r.stdout or "") + (r.stderr or "")
    (part / "renders" / f"render-{stamp}.log").write_text(log, encoding="utf-8")
    if r.returncode or not raw.exists():
        print(log[-3000:])
        sys.exit("Stopped: render failed (log saved in renders/).")

    print("3/5 verify")
    html = (part / "index.html").read_text(encoding="utf-8")
    root = re.search(r'<div[^>]*?\sid="root"[^>]*>', html).group(0)
    want = float(re.search(r'data-duration="([\d.]+)"', root).group(1))
    got = C.ffprobe_duration(raw)
    streams = C.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(raw)]).stdout
    if abs(got - want) > 0.2 or "audio" not in streams:
        sys.exit(f"Stopped: render looks wrong (duration {got:.2f}s vs {want}s, streams: {streams.split()})")

    print("4/5 master audio (-14 LUFS / -1.2 dBTP)")
    final = pp / "deliverables" / f"{a.name}-{a.part}.mp4"
    final.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, str(PIPE / "master_audio.py"), str(raw), "--out", str(final)])
    if r.returncode:
        sys.exit("Stopped: mastering failed.")

    print("5/5 chapters")
    ch = part / "chrome.json"
    if want > 60 and ch.exists() and json.loads(ch.read_text(encoding="utf-8")).get("sections"):
        subprocess.run([sys.executable, str(PIPE / "chapters.py"), a.name, "--part", a.part])
    print(f"\nDONE: {final}  ({got:.1f}s)")


if __name__ == "__main__":
    main()
