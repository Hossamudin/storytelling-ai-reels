"""05 - Assemble the HyperFrames composition scaffold for the project.

Usage: python pipeline/assemble.py <name> [--captions on|off]

Generates composition/index.html with:
  - one clip per storyboard scene (video / image / code placeholder)
  - voiceover audio track (+ low-volume audio for AI videos with SFX)
  - keyword-styled Arabic/English caption track (from captions.json)
  - brand palette + fonts, GSAP timeline (fromTo only, seek-safe)
Then the AGENT refines code scenes using the hyperframes-* skills.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

ASPECTS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080)}


def rel_to_comp(path: Path, comp: Path) -> str:
    import os
    return os.path.relpath(path, comp).replace("\\", "/")


def place_asset(src: Path, comp: Path) -> str:
    """Hard-link (or copy) a project asset into composition/assets/ and return
    a root-relative path — HyperFrames forbids ../ traversal outside the project root.
    Re-places STALE links: if src was replaced after the last assemble (e.g. audio
    recut), the old hard-link still holds the previous data — detect via size/mtime."""
    import os
    import shutil
    src = Path(src)
    rel = src.relative_to(src.parents[1]) if src.parent.name in ("voice", "images", "videos") else Path(src.name)
    dest = comp / "assets" / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        same_size = dest.stat().st_size == src.stat().st_size
        same_mtime = abs(dest.stat().st_mtime - src.stat().st_mtime) < 2
        if not (same_size and same_mtime):
            dest.unlink()
    if not dest.exists():
        try:
            os.link(src, dest)
        except OSError:
            shutil.copy2(src, dest)
    return ("assets/" + str(rel)).replace("\\", "/")


def qc_audio_sync(comp: Path, expected_duration: float):
    """Hard gate: the audio the composition will play must match the storyboard
    duration. Catches stale/mismatched voiceover assets before any render."""
    vo = comp / "assets" / "voice" / "voiceover_clean.wav"
    if not vo.exists() or not expected_duration:
        return
    actual = C.ffprobe_duration(vo)
    if abs(actual - expected_duration) > 1.0:
        raise SystemExit(
            f"QC FAILED: composition voiceover is {actual:.2f}s but storyboard expects "
            f"{expected_duration:.2f}s — stale audio asset. Re-assemble after clean_audio/recut. "
            f"(This gate prevents rendering a desynced video.)")
BG_ROTATION = [
    ("#FAF7F0", "#136052", "#2E6B4F"),  # light bg, teal headline, darker green sub (AA)
    ("#136052", "#FFFFFF", "#E8F3C8"),  # deep teal bg, white headline, pale lime sub
    ("#FFFFFF", "#0D0D0D", "#C2431D"),  # white bg, ink headline, darkened orange sub
    ("#0D2B23", "#FFEC5C", "#CFE3A0"),  # dark green bg, yellow headline, lighter lime sub
]

HTML = """<!doctype html>
<html lang="ar">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=__W__, height=__H__" />
<title>__TITLE__</title>
<script src="assets/js/gsap.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;600;800&family=Manrope:wght@500;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --punch1:#136052; --punch2:#437F3E; --punch3:#B3CE65; --punch4:#FFEC5C;
    --punch5:#FF5A33; --ink:#0D0D0D; --paper:#FAF7F0;
  }
  body { margin:0; background:#0b1210; font-family:'Noto Kufi Arabic','Manrope',sans-serif; }
  #root { position:relative; width:__W__px; height:__H__px; overflow:hidden; background:var(--paper); }
  .clip { position:absolute; inset:0; }
  .scene-fill { position:absolute; inset:0; }
  .scene-inner {
    position:absolute; inset:0; display:flex; flex-direction:column;
    align-items:center; justify-content:center; gap:28px; padding:90px 70px;
    box-sizing:border-box; text-align:center;
  }
  .scene-kicker {
    font-family:'Manrope',sans-serif; font-weight:800; font-size:26px;
    letter-spacing:0.35em; text-transform:uppercase; opacity:1;
  }
  .scene-headline {
    font-weight:800; font-size:104px; line-height:1.28; margin:0; direction:rtl;
  }
  .scene-narr {
    font-size:36px; line-height:1.75; direction:rtl; opacity:0.95; max-width:88%;
  }
  .scene-media { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
  .cap {
    position:absolute; left:0; right:0; __CAPPOS__; display:flex; justify-content:center;
    padding:0 36px; box-sizing:border-box; pointer-events:none;
  }
  .cap-inner {
    display:inline-flex; flex-wrap:wrap; justify-content:center; align-items:baseline;
    column-gap:14px; row-gap:12px; direction:rtl; max-width:100%;
  }
  .cap-w {
    display:inline-block; font-weight:800; font-size:58px; line-height:1.35;
    color:#FFFFFF; background:rgba(13,13,13,__CAPBG__); border-radius:16px;
    padding:6px 20px; white-space:nowrap;
  }
  .cap-w.kw {
    font-family:'Manrope','Noto Kufi Arabic',sans-serif; direction:ltr;
    background:__KWCOLOR__; color:#FFFFFF;
  }
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="__W__" data-height="__H__" data-duration="__DUR__" data-fps="__FPS__">
__SCENES__
__CAPTIONS__
__AUDIO__
</div>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
__TWEENS__
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--captions", default="on", choices=["on", "off"])
    args = ap.parse_args()

    cfg = C.load_config()
    pp = C.project_path(args.name)
    comp = pp / "composition"
    sb = json.loads((pp / "storyboard.json").read_text(encoding="utf-8"))
    aspect = sb.get("aspect") or cfg["video_defaults"]["aspect"]
    w, h = ASPECTS.get(aspect, ASPECTS["9:16"])
    fps = cfg["video_defaults"].get("fps", 30)
    tail = cfg["video_defaults"].get("tail_padding_s", 0.6)
    dur = round(sb["total_duration"] + tail, 2)
    palette = cfg["brand"]["palette"]

    scenes_html, tweens = [], []
    track = 1
    for idx, s in enumerate(sb["scenes"]):
        sid = s["id"]
        sdur = round(max(0.2, s["end"] - s["start"]), 2)
        assets = s.get("assets", {}) or {}
        bg, fg, sub = BG_ROTATION[idx % len(BG_ROTATION)]
        video = assets.get("video")
        image = assets.get("first_frame") or assets.get("last_frame")
        headline = s.get("headline") or ""

        if video:
            src = place_asset(pp / video, comp)
            scenes_html.append(
                f'  <video id="sc-{sid}" src="{esc(src)}" data-start="{s["start"]}" '
                f'data-duration="{sdur}" data-track-index="{track}" muted playsinline></video>')
            aud_src = src
            scenes_html.append(
                f'  <audio id="sc-{sid}-sfx" src="{esc(aud_src)}" data-start="{s["start"]}" '
                f'data-duration="{sdur}" data-track-index="20" data-volume="0.22"></audio>')
            if image:
                isrc = place_asset(pp / image, comp)
                scenes_html.append(
                    f'  <img id="sc-{sid}-poster" class="clip" src="{esc(isrc)}" '
                    f'data-start="{s["start"]}" data-duration="0.1" data-track-index="{track}" '
                    f'data-layout-ignore alt="" />')
        elif image:
            isrc = place_asset(pp / image, comp)
            scenes_html.append(
                f'  <img id="sc-{sid}" class="clip" src="{esc(isrc)}" '
                f'data-start="{s["start"]}" data-duration="{sdur}" data-track-index="{track}" '
                f'data-layout-allow-overflow alt="" />')
            scenes_html.append(
                f'  <div id="sc-{sid}-grad" class="clip" data-start="{s["start"]}" '
                f'data-duration="{sdur}" data-track-index="{track + 1}" '
                f'style="background:linear-gradient(180deg, rgba(13,43,35,0) 55%, rgba(13,43,35,0.55) 100%)"></div>')
            tweens.append(
                f'  tl.fromTo("#sc-{sid}", {{scale:1.02}}, {{scale:1.1, duration:{sdur}, ease:"none"}}, {s["start"]});')
            track += 1
        else:
            narr = esc((s.get("narration", "") or "")[:90])
            scenes_html.append(
                f'''  <div id="sc-{sid}" class="clip" data-start="{s["start"]}" data-duration="{sdur}" data-track-index="{track}" data-layout-allow-overflow>
    <div class="scene-fill" style="background:{bg}"></div>
    <div class="scene-inner" id="sc-{sid}-inner">
      <div class="scene-kicker" style="color:{sub}">{esc(sid)} &middot; {esc(s.get("beat", ""))} &middot; {esc(s.get("style", ""))}</div>
      <h2 class="scene-headline" style="color:{fg}">{esc(headline) or "SCENE " + sid}</h2>
      <div class="scene-narr" style="color:{fg}">{narr}</div>
    </div>
  </div>''')
            tweens.append(
                f'  tl.fromTo("#sc-{sid}-inner .scene-headline", {{y:60, opacity:0}}, '
                f'{{y:0, opacity:1, duration:0.55, ease:"power3.out"}}, {s["start"] + 0.15});')
            tweens.append(
                f'  tl.fromTo("#sc-{sid}-inner .scene-kicker", {{opacity:0}}, '
                f'{{opacity:1, duration:0.4}}, {s["start"]});')
            tweens.append(
                f'  tl.fromTo("#sc-{sid}-inner .scene-narr", {{y:30, opacity:0}}, '
                f'{{y:0, opacity:0.95, duration:0.5, ease:"power2.out"}}, {s["start"] + 0.35});')
        track = 3 if track >= 4 else track + 1  # keep visual tracks low, alternate

    # captions
    captions_html = []
    cap_path = pp / "transcript" / "captions.json"
    if args.captions == "on" and cap_path.exists():
        caps = json.loads(cap_path.read_text(encoding="utf-8"))
        kwc = palette.get("punch5", "#FF5A33")
        pos = "bottom:5.5%" if caps.get("position") != "top" else "top:10%"
        capbg = "0.62"
        for ch in caps["chunks"]:
            cid = f"cap-{ch['i']:03d}"
            cdur = round(max(0.2, ch["end"] - ch["start"]), 2)
            words = "".join(
                (f'<span class="cap-w kw">{esc(w["w"])}</span>' if w["kw"]
                 else f'<span class="cap-w">{esc(w["w"])}</span>')
                for w in ch["words"])
            captions_html.append(
                f'  <div id="{cid}" class="clip cap" data-start="{ch["start"]}" '
                f'data-duration="{cdur}" data-track-index="15" '
                f'data-layout-allow-overflow data-layout-allow-caption-zone '
                f'style="{pos}"><div class="cap-inner">{words}</div></div>')
            tweens.append(
                f'  tl.fromTo("#{cid} .cap-w", {{y:26, opacity:0}}, '
                f'{{y:0, opacity:1, duration:0.24, ease:"back.out(1.8)", stagger:0.045}}, {ch["start"]});')
        scenes_html += captions_html

    # voiceover
    vo = pp / "assets" / "voice" / "voiceover_clean.wav"
    audio_html = ""
    if vo.exists():
        vsrc = place_asset(vo, comp)
        audio_html = (f'  <audio id="voiceover" src="{vsrc}" data-start="0" '
                      f'data-duration="{sb["total_duration"]}" data-track-index="10" data-volume="1"></audio>')

    html = (HTML.replace("__W__", str(w)).replace("__H__", str(h))
            .replace("__DUR__", str(dur)).replace("__FPS__", str(fps))
            .replace("__TITLE__", esc(sb.get("title", "Composition")))
            .replace("__CAPPOS__", pos if args.captions == "on" and cap_path.exists() else "bottom:14%")
            .replace("__CAPBG__", capbg if args.captions == "on" else "0.42")
            .replace("__KWCOLOR__", kwc if args.captions == "on" else "#FF5A33")
            .replace("__SCENES__", "\n".join(scenes_html))
            .replace("__CAPTIONS__", "")
            .replace("__AUDIO__", audio_html)
            .replace("__TWEENS__", "\n".join(tweens) or "  // no tweens"))

    comp = pp / "composition"
    (comp / "assets/js").mkdir(parents=True, exist_ok=True)  # GSAP ships locally: renders never depend on a CDN
    import shutil as _sh
    _sh.copy2(Path(__file__).resolve().parent.parent / "kit/motion/js/gsap.min.js", comp / "assets/js/gsap.min.js")
    comp.mkdir(parents=True, exist_ok=True)
    (comp / "index.html").write_text(html, encoding="utf-8")

    # QC gate: audio placed in the composition must match the storyboard timing
    qc_audio_sync(comp, float(sb.get("total_duration") or 0))

    # assembly notes for the agent
    notes = [f"# Assembly notes — {sb.get('title', '')}", "",
             f"- Composition: composition/index.html ({w}x{h}, {dur}s, {fps}fps)",
             "- Validate: `npx hyperframes check` (run inside composition/)",
             "- Preview: `npx hyperframes preview --background`", ""]
    for s in sb["scenes"]:
        assets = s.get("assets", {}) or {}
        if s["method"] == "code":
            notes.append(f"- {s['id']} ({s['start']}-{s['end']}s): CODE scene — replace placeholder with "
                         f"real motion graphics (style: {s['style']}). {s.get('notes', '')}")
        elif s["method"] == "screenshot" and not assets:
            notes.append(f"- {s['id']}: SCREENSHOT needed — {s.get('screenshot_hint', 'capture what narration names')}; "
                         f"save to assets/images/{s['id']}_first.png then re-run assemble.py")
        elif s["method"] == "hossam_image" and not assets:
            notes.append(f"- {s['id']}: HOSSAM IMAGE needed — pick from Hossam Images/ "
                         f"({s.get('hossam_image_hint', '')}); copy to assets/images/{s['id']}_first.png then re-run assemble.py")
        elif s["method"] in ("image_animate", "text_to_video") and not assets.get("video"):
            notes.append(f"- {s['id']}: AI VIDEO missing — generate_assets.py failed or skipped; retry or downgrade to image+code motion")
    (comp / "ASSEMBLY_NOTES.md").write_text("\n".join(notes), encoding="utf-8")

    C.update_stage(args.name, "assembly", f"scaffold generated ({len(sb['scenes'])} scenes, {dur}s)")
    print(f"OK: {comp / 'index.html'} ({w}x{h}, {dur}s, {len(tweens)} tweens)")
    print(f"Next: cd composition && npx hyperframes check  ->  refine scenes (see ASSEMBLY_NOTES.md)")


if __name__ == "__main__":
    main()
