"""Sync a motion project's index.html from its JSON plans (idempotent; safe to re-run).

Usage: python engine/pipeline/motion_sync.py <name> [--part composition]

scenes.json  [{"id": "s1", "start": 0, "duration": 5.35, "beat": "hook: shelved podcast",
               "title": "optional placeholder text"}]
             -> sub-composition hosts (alternating tracks) + creates missing compositions/<id>.html
                from kit/motion/templates/scene.html (existing scene files are never overwritten)
cues.json    [{"id": "vo", "t": 0, "src": "assets/voice/intro.wav", "dur": 66.39, "voice": true},
              {"t": 10.37, "sfx": "library/impact-bass-1", "accent": 1.7, "dur": 2.0},
              {"t": 41.0, "sfx": "library/riser", "media_start": 6.7, "dur": 3.3},
              {"t": 5.2, "sfx": "higgsfield/podcast-shelf-thud"}]
             -> <audio> tags; SFX gain = levels.json gain x accent (run sfx_levels.py after adding SFX)
chrome.json  {"enabled": true, "series": "VIBE AUTOMATION",
              "sections": [{"t": 0, "label": "THE PROBLEM"}, {"t": 20.5, "label": "THE PIPELINE"}],
              "wipes": [20.4, 44.5], "grain": false,      # grain off: required for screen recordings
              "steps": [{"t0": 30, "t1": 60, "items": [{"t": 30, "label": "اعمل حساب"}, {"t": 42, "label": "مشروع جديد"}]}]}
             sections may carry "title" (chapter title in the video language) and "chapter": false (pipeline/chapters.py)
scenes.json items may set "template": "quiz" | "recap" + "data": {...} (kit/motion/templates).
Root duration = max(scene ends, voice end + motion.tail_s).
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

KIT = C.KIT


def between(html, tag, body, js=False):
    a, b = (f"// {tag}:BEGIN", f"// {tag}:END") if js else (f"<!-- {tag}:BEGIN", f"<!-- {tag}:END -->")
    i = html.index(a)
    j = html.index(b)
    head_end = html.index("\n", i) + 1
    indent = re.match(r"\s*", html[j - 40:j].split("\n")[-1]).group(0)
    return html[:head_end] + body + ("\n" if body else "") + indent + html[j:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--part", default="composition")
    a = ap.parse_args()
    cfg = C.load_config()
    m = cfg.get("motion", {})
    out = C.project_path(a.name) / a.part
    html = (out / "index.html").read_text(encoding="utf-8")
    W = int(re.search(r'data-width="(\d+)"', html).group(1))
    H = int(re.search(r'data-height="(\d+)"', html).group(1))
    scenes = json.loads((out / "scenes.json").read_text(encoding="utf-8"))
    cues = json.loads((out / "cues.json").read_text(encoding="utf-8"))
    chrome = json.loads((out / "chrome.json").read_text(encoding="utf-8"))
    levels_p = out / "assets/sfx/levels.json"
    levels = json.loads(levels_p.read_text(encoding="utf-8")) if levels_p.exists() else {}

    # hosts + scene files
    hosts = []
    tpl = (KIT / "templates/scene.html").read_text(encoding="utf-8")
    for i, s in enumerate(scenes):
        sid, st, du = s["id"], float(s["start"]), float(s["duration"])
        hosts.append(f'      <div id="{sid}-host" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{st}" data-duration="{du}" data-track-index="{1 + i % 2}" data-width="{W}" data-height="{H}"></div>')
        f = out / "compositions" / f"{sid}.html"
        if not f.exists():
            body = tpl
            if s.get("template"):  # e.g. "quiz" / "recap" -> kit/motion/templates/<template>.html
                body = (KIT / "templates" / f"{s['template']}.html").read_text(encoding="utf-8")
                for k, v in {**(s.get("data") or {}), "ID": sid, "W": W, "H": H, "DUR": du, "START": st}.items():
                    body = body.replace("{{" + k + "}}", str(v))
            for k, v in {"ID": sid, "W": W, "H": H, "DUR": du, "START": st, "BEAT": s.get("beat", ""),
                         "PLACEHOLDER": s.get("title", s.get("beat", sid)), "TITLE_TOP": int(H * 0.4)}.items():
                body = body.replace("{{" + k + "}}", str(v))
            f.write_text(body, encoding="utf-8")
            print(f"  + scene file {f.name}")
    html = between(html, "HOSTS", "\n".join(hosts))

    # audio
    tags, n, ends = [], 0, [0.0]
    for c in cues:
        if c.get("voice"):
            tags.append(f'      <audio id="{c.get("id", "vo")}" src="{c["src"]}" data-start="{c["t"]}" data-duration="{c["dur"]}" '
                        f'data-track-index="20" data-volume="{c.get("vol", 1.0)}"></audio>')
            ends.append(c["t"] + c["dur"] + m.get("tail_s", 0.8))
            continue
        n += 1
        key = c["sfx"] if "." in c["sfx"].split("/")[-1] else c["sfx"] + ".mp3"
        if not (out / "assets/sfx" / key).exists() and (out / "assets/sfx" / key.replace(".mp3", ".wav")).exists():
            key = key.replace(".mp3", ".wav")
        lv = levels.get(key, {})
        gain = round(min(1.0, lv.get("gain", 0.3) * c.get("accent", 1.0)), 3)
        dur = c.get("dur", lv.get("duration", 1.0))
        ms = f' data-media-start="{c["media_start"]}"' if "media_start" in c else ""
        tags.append(f'      <audio id="fx{n:02d}" src="assets/sfx/{key}" data-start="{c["t"]}" data-duration="{dur}"{ms} '
                    f'data-track-index="{20 + n}" data-volume="{gain}"></audio>')
        if not lv:
            print(f"  ! no level for {key} (run: python engine/pipeline/sfx_levels.py --dir {out / 'assets/sfx'})")
    html = between(html, "AUDIO", "\n".join(tags))

    # chrome + wipes
    total = round(max([float(s["start"]) + float(s["duration"]) for s in scenes] + ends), 2)
    ccfg = {"enabled": chrome.get("enabled", True), "series": chrome.get("series", ""), "duration": total,
            "sections": chrome.get("sections", [])}
    html = between(html, "CHROME", f"        window.HF_CHROME(tl, {json.dumps(ccfg, ensure_ascii=False)});", js=True)
    html = between(html, "WIPES", "\n".join(f"        window.HF_WIPE(tl, {t});" for t in chrome.get("wipes", [])), js=True)
    if "// STEPS:BEGIN" not in html:  # older roots: add the marker after the wipes block
        html = html.replace("        // WIPES:END", "        // WIPES:END\n        // STEPS:BEGIN (generated)\n        // STEPS:END", 1)
    steps = chrome.get("steps", [])  # [{"t0","t1","items":[{"t","label"}]}]
    html = between(html, "STEPS", "\n".join(f"        window.HF_STEPS(tl, {json.dumps(st, ensure_ascii=False)});" for st in steps), js=True)
    m = re.search(r'<div[^>]*?\sid="root"[^>]*>', html)  # Studio may reorder attributes
    root_tag = re.sub(r'data-duration="[^"]+"', f'data-duration="{total}"', m.group(0))
    html = html[:m.start()] + root_tag + html[m.end():]
    html = re.sub(r"window\.HF_GRAIN\(tl, [\d.]+\)", f"window.HF_GRAIN(tl, {total})", html)
    # grain: off for screen recordings (it dirties UI text) -> chrome.json "grain": false
    grain_tag = '<div id="grain" style="display: none"></div>' if chrome.get("grain", True) is False else '<div id="grain"></div>'
    html = re.sub(r'<div[^>]*\sid="grain"[^>]*></div>', grain_tag, html, count=1)
    (out / "index.html").write_text(html, encoding="utf-8")
    print(f"OK: {len(scenes)} scenes, {n} sfx, duration {total}s -> {out / 'index.html'}")
    print(f"Next: cd {out} && npx hyperframes check")


if __name__ == "__main__":
    main()
