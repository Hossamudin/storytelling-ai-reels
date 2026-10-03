# Shared building blocks for the "OPUS 5.5 TIPS" reel series (9:16, dark preset).
# Each part (tip1/tip2/tip3) has its own build_scenes.py that imports this module.
# All times are GLOBAL seconds on the part's edited voice (transcript/<part>_words.json).
import json
import math
import re
from pathlib import Path

PROJ = Path(__file__).resolve().parent
CLAUDE = "#D97757"  # Claude's brand terracotta — used ONLY for the Claude logo and Claude-app UI accents

# ---------------------------------------------------------------- Claude spark (logo) symbol
def spark_symbol():
    """Claude spark: 12 rounded rays with slightly irregular angles / lengths (drawn in code, no download)."""
    rays = []
    lens = [44, 38, 46, 36, 43, 40, 45, 37, 42, 39, 46, 35]
    jit = [0, 3, -2, 4, -3, 2, 0, -4, 3, -1, 2, -3]
    for i in range(12):
        a = math.radians(i * 30 + jit[i] - 90)
        L = lens[i]
        x2, y2 = L * math.cos(a), L * math.sin(a)
        rays.append(f'<line x1="0" y1="0" x2="{x2:.2f}" y2="{y2:.2f}" />')
    return (f'<symbol id="i-claude" viewBox="-50 -50 100 100"><g stroke="{CLAUDE}" stroke-width="9.5" stroke-linecap="round">'
            + "".join(rays) + '</g><circle r="9" fill="' + CLAUDE + '" /></symbol>')


SERIES_CSS = """
      /* OPUS55:CSS:BEGIN — series styles (build_lib.py) */
      .cl-spark { position: absolute; }
      .cl-spark svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
      .cl-bloom { position: absolute; left: -70%; top: -70%; width: 240%; height: 240%; border-radius: 50%;
        background: radial-gradient(circle, rgba(217,119,87,.55) 0%, rgba(255,236,92,.14) 38%, transparent 68%); pointer-events: none; }
      .op-en { font-family: var(--font-en); direction: ltr; unicode-bidi: isolate; font-weight: 900; }
      .op-y { color: var(--yellow); } .op-l { color: var(--lime); } .op-o { color: var(--orange); } .op-c { color: #e8977c; }
      .op-tag { position: absolute; font-family: var(--font-en); font-weight: 800; letter-spacing: .2em; font-size: 24px; color: var(--lime);
        direction: ltr; white-space: nowrap; }
      .op-src { position: absolute; left: 0; right: 0; text-align: center; font-family: var(--font-en); font-weight: 700; font-size: 22px;
        letter-spacing: .14em; color: var(--fg-muted); direction: ltr; white-space: nowrap; }
      .op-card { position: absolute; border-radius: 34px; background: linear-gradient(160deg, #0f3d35 0%, #082a24 100%);
        border: 3px solid rgba(179,206,101,.55); box-shadow: 0 30px 70px rgba(0,0,0,.45); overflow: hidden; }
      .op-card.back { background: repeating-linear-gradient(45deg, #0b332c 0 18px, #0d3a32 18px 36px); border-color: rgba(179,206,101,.3); }
      .op-phone { position: absolute; border-radius: 56px; background: #050505; padding: 16px; box-shadow: 0 40px 90px rgba(0,0,0,.6), 0 0 0 3px rgba(255,255,255,.08); }
      .op-phone .scr { position: relative; width: 100%; height: 100%; border-radius: 42px; overflow: hidden; background: #111; }
      .op-phone .scr img { position: absolute; left: 0; top: 0; width: 100%; }
      .op-shot { position: absolute; border-radius: 26px; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,.55), 0 0 0 2px rgba(255,255,255,.08); background: #111; }
      .op-shot img, .op-shot video { position: absolute; left: 0; top: 0; width: 100%; }
      .op-win { position: absolute; border-radius: 26px; overflow: hidden; background: #141414; box-shadow: 0 40px 90px rgba(0,0,0,.6), 0 0 0 2px rgba(255,255,255,.08); }
      .op-win .bar { position: absolute; left: 0; right: 0; top: 0; height: 54px; background: #1d1d1b; display: flex; align-items: center; gap: 12px; padding: 0 22px; direction: ltr; }
      .op-win .bar i { width: 16px; height: 16px; border-radius: 50%; background: #3a3a37; }
      .op-win .bar b { margin-left: 14px; font-family: var(--font-en); font-size: 20px; font-weight: 700; color: #9a988f; letter-spacing: .04em; }
      .op-win .body { position: absolute; left: 0; right: 0; top: 54px; bottom: 0; overflow: hidden; }
      .op-win .body video, .op-win .body img { position: absolute; left: 0; top: 0; }
      /* mock Claude composer (styled after the real Claude app, dark) */
      .op-input { position: absolute; border-radius: 30px; background: #30302e; border: 2px solid #46453f; box-shadow: 0 24px 60px rgba(0,0,0,.45); }
      .op-input .txt { position: absolute; left: 34px; right: 34px; top: 30px; font-family: var(--font-ar); font-size: 40px; font-weight: 600; color: #ecebe4;
        direction: rtl; text-align: right; line-height: 1.5; white-space: nowrap; overflow: hidden; }
      .op-input .ph { color: #8f8d85; }
      .op-input .foot { position: absolute; left: 26px; right: 26px; bottom: 22px; height: 60px; display: flex; align-items: center; justify-content: space-between; direction: ltr; }
      .op-input .plus { font-family: var(--font-en); font-size: 40px; color: #b9b7ae; width: 54px; text-align: center; }
      .op-input .mdl { display: flex; align-items: center; gap: 14px; font-family: var(--font-en); font-size: 26px; font-weight: 700; color: #dcdad1; }
      .op-input .mdl em { font-style: normal; color: #8f8d85; font-weight: 600; }
      .op-input .send { width: 60px; height: 60px; border-radius: 16px; background: """ + CLAUDE + """; display: flex; align-items: center; justify-content: center; }
      .op-input .send svg { width: 30px; height: 30px; }
      .op-chip { position: absolute; height: 82px; padding: 0 34px; border-radius: 41px; background: #0b2f29; border: 3px solid var(--lime); color: var(--fg);
        font-family: var(--font-ar); font-weight: 800; font-size: 38px; display: flex; align-items: center; gap: 16px; white-space: nowrap; direction: rtl; }
      .op-chip .ic { width: 50px; height: 50px; border-radius: 50%; background: var(--lime); color: var(--ink); display: flex; align-items: center; justify-content: center;
        font-family: var(--font-en); font-weight: 900; font-size: 24px; }
      .op-chip.y { border-color: var(--yellow); } .op-chip.y .ic { background: var(--yellow); }
      .op-chip.o { border-color: var(--orange); } .op-chip.o .ic { background: var(--orange); color: #fff; }
      .op-big { position: absolute; left: 0; right: 0; text-align: center; font-family: var(--font-en); font-weight: 900; direction: ltr; white-space: nowrap; }
      .op-track { position: absolute; height: 40px; border-radius: 20px; background: rgba(255,255,255,.08); overflow: hidden; }
      .op-fill { position: absolute; top: 0; bottom: 0; right: 0; width: 100%; border-radius: 20px; transform-origin: 100% 50%; }
      .op-doc { position: absolute; border-radius: 26px; background: #f3f1e7; box-shadow: 0 30px 70px rgba(0,0,0,.45); overflow: hidden; }
      .op-doc .ln { position: absolute; right: 44px; height: 18px; border-radius: 9px; background: #c9c6b6; }
      .op-hossam { position: absolute; }
      .op-hossam img { position: absolute; left: 0; top: 0; width: 100%; filter: drop-shadow(0 30px 50px rgba(0,0,0,.55)); }
      .op-name { position: absolute; left: 0; right: 0; text-align: center; }
      .op-btn { position: absolute; height: 104px; padding: 0 56px; border-radius: 52px; background: var(--red); color: #fff; font-family: var(--font-ar); font-weight: 900;
        font-size: 46px; display: flex; align-items: center; gap: 18px; white-space: nowrap; box-shadow: 0 20px 50px rgba(217,58,43,.4); }
      .op-btn.on { background: #2b2a28; border: 3px solid var(--lime); color: var(--lime); box-shadow: none; }
      .op-hl { position: absolute; border-radius: 18px; border: 6px solid var(--lime); box-shadow: 0 0 0 3000px rgba(4,22,20,.55), 0 0 40px rgba(180,207,102,.5); }
      /* OPUS55:CSS:END */"""

SYMBOLS = """        <!-- OPUS55:SYM:BEGIN -->
        {spark}
        <symbol id="i-target" viewBox="0 0 64 64"><circle cx="32" cy="32" r="27" fill="none" stroke="currentColor" stroke-width="5" /><circle cx="32" cy="32" r="16" fill="none" stroke="currentColor" stroke-width="5" /><circle cx="32" cy="32" r="6" fill="currentColor" /></symbol>
        <symbol id="i-bulb" viewBox="0 0 64 64"><path d="M32 6c-11 0-19 8-19 18 0 7 4 11 7 15 2 2 3 5 3 8h18c0-3 1-6 3-8 3-4 7-8 7-15 0-10-8-18-19-18z" fill="currentColor" /><rect x="23" y="50" width="18" height="5" rx="2.5" fill="currentColor" /><rect x="26" y="57" width="12" height="4" rx="2" fill="currentColor" /></symbol>
        <symbol id="i-expand" viewBox="0 0 64 64"><path d="M8 24V8h16M40 8h16v16M56 40v16H40M24 56H8V40" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" /></symbol>
        <symbol id="i-lock" viewBox="0 0 64 64"><rect x="12" y="28" width="40" height="30" rx="7" fill="currentColor" /><path d="M20 28v-8a12 12 0 0124 0v8" fill="none" stroke="currentColor" stroke-width="6" /></symbol>
        <symbol id="i-unlock" viewBox="0 0 64 64"><rect x="12" y="28" width="40" height="30" rx="7" fill="currentColor" /><path d="M20 28v-8a12 12 0 0123-5" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" /></symbol>
        <symbol id="i-film" viewBox="0 0 64 64"><rect x="8" y="12" width="48" height="40" rx="6" fill="none" stroke="currentColor" stroke-width="5" /><path d="M8 24h48M8 40h48M20 12v40M44 12v40" stroke="currentColor" stroke-width="4" /></symbol>
        <symbol id="i-sound" viewBox="0 0 64 64"><path d="M10 24h10l14-12v40L20 40H10z" fill="currentColor" /><path d="M42 22c4 3 6 6 6 10s-2 7-6 10M48 14c7 5 10 11 10 18s-3 13-10 18" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" /></symbol>
        <symbol id="i-wand" viewBox="0 0 64 64"><path d="M10 54L42 22" stroke="currentColor" stroke-width="7" stroke-linecap="round" /><path d="M46 6l3 8 8 3-8 3-3 8-3-8-8-3 8-3z" fill="currentColor" /></symbol>
        <symbol id="i-plan" viewBox="0 0 64 64"><rect x="12" y="8" width="40" height="50" rx="6" fill="none" stroke="currentColor" stroke-width="5" /><path d="M22 24h20M22 34h20M22 44h12" stroke="currentColor" stroke-width="5" stroke-linecap="round" /></symbol>
        <symbol id="i-loop" viewBox="0 0 64 64"><path d="M50 26A20 20 0 0014 22M14 38a20 20 0 0036 4" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" /><path d="M8 12l6 12 12-4M56 52l-6-12-12 4" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" /></symbol>
        <symbol id="i-box" viewBox="0 0 64 64"><path d="M8 20l24-12 24 12v26L32 58 8 46z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" /><path d="M8 20l24 12 24-12M32 32v26" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" /></symbol>
        <symbol id="i-send" viewBox="0 0 64 64"><path d="M32 52V14M16 29l16-16 16 16" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" /></symbol>
        <symbol id="i-token" viewBox="0 0 64 64"><circle cx="32" cy="32" r="26" fill="none" stroke="currentColor" stroke-width="5" /><path d="M22 24h20M32 24v20" stroke="currentColor" stroke-width="6" stroke-linecap="round" /></symbol>
        <symbol id="i-clock" viewBox="0 0 64 64"><circle cx="32" cy="32" r="26" fill="none" stroke="currentColor" stroke-width="5" /><path d="M32 16v17l11 7" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" /></symbol>
        <symbol id="i-book" viewBox="0 0 64 64"><path d="M8 12h18c4 0 6 2 6 6v36c0-3-2-5-6-5H8zM56 12H38c-4 0-6 2-6 6v36c0-3 2-5 6-5h18z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" /></symbol>
        <symbol id="i-flag" viewBox="0 0 64 64"><path d="M14 58V8" stroke="currentColor" stroke-width="6" stroke-linecap="round" /><path d="M16 10h34l-8 10 8 10H16z" fill="currentColor" /></symbol>
        <symbol id="i-copy" viewBox="0 0 64 64"><rect x="20" y="20" width="34" height="38" rx="6" fill="none" stroke="currentColor" stroke-width="5" /><path d="M14 44V12c0-3 2-5 5-5h25" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" /></symbol>
        <!-- OPUS55:SYM:END -->"""


def patch_root(part_dir, flashes=()):
    """Inject series CSS, the icon symbols and root-level flashes into <part>/index.html (idempotent)."""
    p = part_dir / "index.html"
    h = p.read_text(encoding="utf-8")
    h = re.sub(r"\n\s*/\* OPUS55:CSS:BEGIN.*?OPUS55:CSS:END \*/", "", h, flags=re.S)
    h = h.replace("/* project-level overrides go here */", "/* project-level overrides go here */" + SERIES_CSS, 1)
    h = re.sub(r"\n\s*<!-- OPUS55:SYM:BEGIN -->.*?<!-- OPUS55:SYM:END -->", "", h, flags=re.S)
    h = re.sub(r"(<svg[^>]*width=\"0\"[^>]*>\s*<defs>.*?</defs>)", lambda m: m.group(1) + "\n" + SYMBOLS.format(spark=spark_symbol()), h, count=1, flags=re.S)
    h = re.sub(r"\n\s*// OPUS55:FLASH:BEGIN.*?// OPUS55:FLASH:END", "", h, flags=re.S)
    fl = "".join(f'\n        tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.85, duration: 0.08, ease: "none", immediateRender: false }}, {t});'
                 f'\n        tl.to("#flash", {{ opacity: 0, duration: 0.5, ease: "power2.out" }}, {t + 0.08:.2f});' for t in flashes)
    h = h.replace("// root-level moments (flashes, global transitions) go below, in GLOBAL seconds",
                  "// root-level moments (flashes, global transitions) go below, in GLOBAL seconds\n        // OPUS55:FLASH:BEGIN" + fl + "\n        // OPUS55:FLASH:END", 1)
    p.write_text(h, encoding="utf-8")


class Part:
    def __init__(self, part_dir):
        self.dir = Path(part_dir)
        self.scenes = {s["id"]: s for s in json.loads((self.dir / "scenes.json").read_text(encoding="utf-8"))}

    def make(self, sid, css, body, js, blob=("#136052", 540, 900), exit_t=None, push=1.035, bg=True, exit=True):
        s = self.scenes[sid]
        st, du = s["start"], s["duration"]
        et = exit_t if exit_t is not None else round(st + du - 0.44, 2)  # 0.22 s fade ends before the next scene (0.2 s overlap)
        bc, bx, by = blob
        back = (f'<div class="bg"></div>\n    <div id="{sid}-blob" class="blob" style="left:{bx - 380}px; top:{by - 380}px; width:760px; height:760px; background:{bc}; opacity:.55"></div>\n'
                f'    <div id="{sid}-bgp" class="dots"></div>') if bg else ""
        para = (f'fx.drift("#{sid}-bgp", {st}, {du}, 60, -40);\n      fx.drift("#{sid}-blob", {st}, {du}, -110, 60);') if bg else ""
        pin = "" if push is None else f'fx.pushIn("#{sid}-cam", {st}, {du}, {push});'
        ex = f'tl.to("#{sid}-cam", {{ opacity: 0, filter: "blur(10px)", duration: 0.22, ease: "power2.in" }}, {et});' if exit else ""
        html = f"""<!doctype html>
<html lang="ar"><head><meta charset="UTF-8" /></head><body>
<template id="{sid}-template">
  <style>
{css}
  </style>
  <div id="{sid}" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{du}">
    {back}
    <div id="{sid}-cam" class="cam">
{body}
    </div>
  </div>
  <script>
    (function () {{
      const fx = window.HF_SCENE({st});
      const {{ tl }} = fx;
      {para}
      {pin}
{js}
      {ex}
      window.__timelines["{sid}"] = tl.real;
    }})();
  </script>
</template></body></html>
"""
        (self.dir / "compositions" / f"{sid}.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- HTML helpers
def spark(id_, x, y, size, bloom=True, extra=""):
    b = f'<div class="cl-bloom" id="{id_}-bl"></div>' if bloom else ""
    return (f'<div id="{id_}" class="cl-spark" style="left:{x}px; top:{y}px; width:{size}px; height:{size}px;{extra}">{b}'
            f'<svg id="{id_}-svg" viewBox="0 0 100 100"><use href="#i-claude" width="100" height="100" /></svg></div>')


def ic(name, size, color="currentColor", id_=None, style=""):
    i = f' id="{id_}"' if id_ else ""
    return f'<svg{i} style="width:{size}px; height:{size}px; color:{color};{style}"><use href="#i-{name}" /></svg>'


def label(id_, top, text):
    return f'<div id="{id_}" class="row" style="top:{top}px"><span class="t-label" style="color:var(--lime)">{text}</span></div>'


def head(id_, top, lines, cls="t-h2", style=""):
    """lines: list of html strings; each becomes a masked line with id {id_}{n}."""
    out = []
    for n, ln in enumerate(lines, 1):
        out.append(f'<div class="row {cls}" style="top:{top}px;{style}" data-layout-allow-overlap><span class="mask"><span class="in" id="{id_}{n}">{ln}</span></span></div>')
        top += {"t-hero": 250, "t-h1": 160, "t-h2": 118, "t-h3": 84, "t-body": 70}.get(cls, 120)
    return "".join(out)


def claude_input(id_, x, y, w, h=230, model="Opus 5.5", effort="Medium", placeholder=""):
    return (f'<div id="{id_}" class="op-input" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px">'
            f'<div class="txt" id="{id_}-t"><span class="ph">{placeholder}</span></div>'
            f'<div class="foot"><span class="plus">+</span><span class="mdl" id="{id_}-m">{model} <em>{effort}</em>'
            f'<span class="send" id="{id_}-s"><svg><use href="#i-send" /></svg></span></span></div></div>')


def chip(id_, x, y, text, icon_html="", cls=""):
    return f'<div id="{id_}" class="op-chip {cls}" style="left:{x}px; top:{y}px"><span class="ic">{icon_html}</span><span>{text}</span></div>'


def phone(id_, x, y, w, h, img, img_id=None):
    ii = f' id="{img_id}"' if img_id else ""
    return f'<div id="{id_}" class="op-phone" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px"><div class="scr"><img{ii} src="{img}" /></div></div>'


def hossam(id_, x, y, w, img="assets/images/hossam_suit.png"):
    return f'<div id="{id_}" class="op-hossam" style="left:{x}px; top:{y}px; width:{w}px; height:{int(w * 2400 / 1350)}px"><img src="{img}" /></div>'


def words(part):
    d = json.loads((PROJ / "transcript" / f"{part}_words.json").read_text(encoding="utf-8"))
    return d
