"""Scaffold a 100%-motion-graphics HyperFrames project from the motion kit.

Usage:
  python pipeline/new_motion_video.py <name> --part intro --voice projects/<name>/assets/voice/intro.wav \
      [--aspect 16:9|9:16|1:1|4:5] [--preset light|dark] [--series "VIBE AUTOMATION"] [--title "..."] [--no-chrome]
      [--kit cartoon]   # also copy kit/cartoon (character rig + props: HF_CHAR / HF_PROP) and load it in the root

Creates projects/<name>/<part>/ as its own HyperFrames project (check/preview/render run per
project, so an intro and an outro are two sibling parts), with:
  assets/{fonts,css,js,sfx,voice,images,higgsfield}   copied from kit/motion
  index.html        root (chrome, wipes, flash, vignette, grain, markers for hosts/audio)
  scenes.json       [] -> fill with {id,start,duration,beat}; then run motion_sync.py
  cues.json         voice cue + [] SFX cues
  chrome.json       series + section labels (the "03 / 10" counter)
  BRIEF.md          skeleton to fill from the Creative Treatment
Next: write scenes.json/cues.json/chrome.json -> python pipeline/motion_sync.py <name> --part <part>
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "kit" / "motion"
SIZES = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080), "4:5": (1080, 1350)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--part", default="composition")
    ap.add_argument("--voice", default=None)
    ap.add_argument("--aspect", default=None)
    ap.add_argument("--preset", default=None, choices=["light", "dark"])
    ap.add_argument("--series", default=None)
    ap.add_argument("--title", default=None)
    ap.add_argument("--no-chrome", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--kit", action="append", default=[], choices=["cartoon"], help="extra kit(s) to load")
    a = ap.parse_args()

    cfg = C.load_config()
    m = cfg.get("motion", {})
    aspect = a.aspect or cfg["video_defaults"].get("aspect", "16:9")
    preset = a.preset or m.get("default_preset", "light")
    W, H = SIZES[aspect]
    pp = C.project_path(a.name)
    if not (pp / "project.json").exists():
        C.run([sys.executable, str(ROOT / "pipeline/new_project.py"), a.name, "--title", a.title or a.name])
    out = pp / a.part
    if (out / "index.html").exists() and not a.force:
        raise SystemExit(f"{out} already exists (use --force to overwrite the scaffold files).")
    for sub in ["compositions", "assets/voice", "assets/images", "assets/higgsfield", "renders"]:
        (out / sub).mkdir(parents=True, exist_ok=True)
    for sub in ["fonts", "css", "js", "sfx"]:
        shutil.copytree(KIT / sub, out / "assets" / sub, dirs_exist_ok=True)

    dur, cues = 10.0, []
    if a.voice:
        v = Path(a.voice)
        shutil.copy2(v, out / "assets/voice" / v.name)
        vd = round(C.ffprobe_duration(v), 3)
        dur = round(vd + m.get("tail_s", 0.8), 2)
        cues.append({"id": "vo", "t": 0, "src": f"assets/voice/{v.name}", "dur": vd, "vol": 1.0, "voice": True})

    html = (KIT / "templates/root.html").read_text(encoding="utf-8")
    for extra in a.kit:  # e.g. kit/cartoon/js/cartoon.js -> assets/js/, loaded right after fx.js
        for f in sorted((ROOT / "kit" / extra / "js").glob("*.js")):
            shutil.copy2(f, out / "assets/js" / f.name)
            html = html.replace('<script src="assets/js/fx.js"></script>',
                                f'<script src="assets/js/fx.js"></script>\n    <script src="assets/js/{f.name}"></script>', 1)
    for k, val in {"W": W, "H": H, "PRESET": preset, "DURATION": dur, "TITLE": a.title or f"{a.name} — {a.part}"}.items():
        html = html.replace("{{" + k + "}}", str(val))
    (out / "index.html").write_text(html, encoding="utf-8")
    (out / "scenes.json").write_text("[]\n", encoding="utf-8")
    (out / "cues.json").write_text(json.dumps(cues, ensure_ascii=False, indent=1), encoding="utf-8")
    chrome_on = (not a.no_chrome) and (preset == "dark" or m.get("chrome_on_light", False))
    (out / "chrome.json").write_text(json.dumps({"enabled": chrome_on, "series": a.series or m.get("series", ""),
                                                "sections": [], "wipes": []}, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        "media": {"autoProxy": True}, "authoringSkill": "general-video"}, indent=2), encoding="utf-8")
    ver = m.get("hyperframes_version", "0.8.97")
    (out / "package.json").write_text(json.dumps({"name": a.part, "private": True, "type": "module", "scripts": {
        "dev": f"npx --yes hyperframes@{ver} preview", "check": f"npx --yes hyperframes@{ver} check",
        "render": f"npx --yes hyperframes@{ver} render"}}, indent=2), encoding="utf-8")
    (out / "meta.json").write_text(json.dumps({"id": f"{a.name}-{a.part}", "name": a.part}, indent=2), encoding="utf-8")
    brief = out / "BRIEF.md"
    if not brief.exists():
        brief.write_text(f"""---
workflow: general-video
flow: automation
storyboard: no
message: ""
destination: {"youtube" if aspect == "16:9" else "reels"}
aspect: "{aspect}"
language: ar-EG
preset: {preset}
---

# {a.title or a.name} — {a.part}

## Creative Treatment (approved)
- Spine (one visual metaphor):
- Signature move (new this video):
- Rhythm line:
- Direction line (e.g. "a control room", "a race", "a kitchen recipe"):

## Invented / placeholder strings to flag at handoff
-

## Higgsfield / generated assets (see prompts/higgsfield_playbook.md; approval gate applies)
-
""", encoding="utf-8")
    print(f"OK: {out}  ({W}x{H}, preset={preset}, duration={dur}s, chrome={'on' if chrome_on else 'off'})")
    print(f"Next: fill {out / 'scenes.json'} + cues.json + chrome.json, then python pipeline/motion_sync.py {a.name} --part {a.part}")


if __name__ == "__main__":
    main()
