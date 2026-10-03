# AI NEWS WEEKLY — 3 Oct 2026 reel (9:16, dark). Times = GLOBAL seconds on assets/voice/reel.wav (190 s edit).
# Spine: the newsroom "breaking board". Signature move: a split-flap board flips each story in (STORY 0N + name),
# and pays off on "Super Intelligence" (ARTIFICIAL flips to SUPER). Motif: a 6-story rail at the bottom (01 on the right).
# Re-run after edits:  python build_scenes.py   (writes scenes.json, cues.json, chrome.json, compositions/*.html)
#                      then: python ../../../pipeline/motion_sync.py ai-news-oct3 --part reel
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "opus55-tips"))
from build_lib import Part, patch_root, spark, ic, head  # noqa: E402  (shared series kit: spark logo, cards, phone CSS)

# ---------------------------------------------------------------- timeline (scene starts, GLOBAL s)
B = [("s1", 0.0, "hook: AI NEWS board, this week"),
     ("s2", 2.95, "OpenAI made an assistant you can call"),
     ("s3", 10.3, "24 hours, does tasks in the background"),
     ("s4", 14.8, "like ChatGPT, but a call instead of the app"),
     ("s5", 22.4, "Google answered with a model nobody can use yet"),
     ("s6", 26.35, "STORY 01 board: OpenAI Dots"),
     ("s7", 30.15, "like Muse Spark, like Grok"),
     ("s8", 36.5, "agent in the background, own computer, connects your apps"),
     ("s9", 43.25, "no model picking: it chooses per task"),
     ("s10", 50.0, "only Pro / Business Premium / Enterprise, not free"),
     ("s11", 56.85, "STORY 02 board: GPT-6.1 Sol"),
     ("s12", 62.0, "near Astra, a fifth of the price (real prices)"),
     ("s13", 66.85, "price war: Claude cut prices first"),
     ("s14", 77.5, "DevDay: 20+ more launches, full episode"),
     ("s15", 82.6, "STORY 03 board: Gemini 4 Argon"),
     ("s16", 85.5, "Google's own benchmarks: beats Opus 5.5 + Astra"),
     ("s17", 91.35, "Artificial Analysis: not #1 (real index)"),
     ("s18", 97.2, "focus 1: cybersecurity (Fairwind)"),
     ("s19", 104.05, "focus 2: scientific research"),
     ("s20", 110.45, "output up to 1M tokens vs 64K"),
     ("s21", 118.45, "STORY 04 board: Sonnet 5.5 at half the Opus price"),
     ("s22", 124.0, "my Sonnet 5.5 reel"),
     ("s23", 127.3, "Claude Code mods: Claude edits Claude Code"),
     ("s24", 136.6, "STORY 05 board: Meta Muse Charm"),
     ("s25", 140.4, "Muse Spark in a small device, not phone/computer"),
     ("s26", 150.25, "Muse Spark: easiest to connect to your tools"),
     ("s27", 156.05, "STORY 06 board: White House meeting"),
     ("s28", 162.65, "the new name: ARTIFICIAL -> SUPER intelligence"),
     ("s29", 166.1, "safety commitments"),
     ("s30", 172.5, "the gate: only big companies / governments"),
     ("s31", 181.95, "your turn: which story did you like"),
     ("s32", 185.8, "series card + follow")]
END = 192.6
scenes = []
for i, (sid, st, beat) in enumerate(B):
    nxt = B[i + 1][1] if i + 1 < len(B) else END - 0.2
    scenes.append({"id": sid, "start": st, "duration": round(nxt - st + 0.2, 2), "beat": beat})
(HERE / "scenes.json").write_text(json.dumps(scenes, ensure_ascii=False, indent=1), encoding="utf-8")

STORIES = [(26.35, "DOTS"), (56.85, "GPT-6.1 SOL"), (82.6, "GEMINI 4 ARGON"), (118.45, "ANTHROPIC"), (136.6, "META"), (156.05, "WHITE HOUSE")]
chrome = {"enabled": True, "series": "AI NEWS WEEKLY", "grain": False,
          "sections": [{"t": 0, "label": "THIS WEEK"}] + [{"t": t, "label": f"STORY 0{n} · {name}"} for n, (t, name) in enumerate(STORIES, 1)]
          + [{"t": 181.95, "label": "YOUR TURN"}],
          "wipes": [t - 0.08 for t, _ in STORIES]}
(HERE / "chrome.json").write_text(json.dumps(chrome, ensure_ascii=False, indent=1), encoding="utf-8")

CUES = [{"id": "vo", "t": 0, "src": "assets/voice/reel.wav", "dur": 189.93, "vol": 1.0, "voice": True}]


def cue(t, name, accent=1.0):
    CUES.append({"t": round(t, 2), "sfx": f"library/{name}", "accent": accent})


P = Part(HERE)
patch_root(HERE)
make = P.make

# ---------------------------------------------------------------- shared news CSS + root rail
NEWS_CSS = """
      /* NEWS:CSS:BEGIN — series styles (build_scenes.py) */
      .flap { position: absolute; left: 0; right: 0; display: flex; justify-content: center; gap: 10px; direction: ltr; }
      .fl { position: relative; display: inline-block; text-align: center; border-radius: 14px; font-family: var(--font-en); font-weight: 900; color: #f6f8f0;
        background: linear-gradient(180deg, #164a41 0%, #10392f 49.5%, #0a2924 50.5%, #0d302a 100%);
        box-shadow: 0 10px 24px rgba(0,0,0,.45), inset 0 0 0 2px rgba(255,255,255,.06); transform-origin: 50% 50%; }
      .fl::after { content: ""; position: absolute; left: 0; right: 0; top: 50%; height: 3px; margin-top: -1.5px; background: rgba(0,0,0,.45); }
      .fl.sp { background: transparent; box-shadow: none; } .fl.sp::after { display: none; }
      .fl.y { color: var(--yellow); } .fl.l { color: var(--lime); } .fl.o { color: var(--orange); }
      .co { position: absolute; left: 0; right: 0; display: flex; justify-content: center; }
      .co span { height: 64px; padding: 0 30px; border-radius: 32px; border: 3px solid var(--lime); color: var(--lime); font-family: var(--font-en);
        font-weight: 900; font-size: 28px; letter-spacing: .24em; display: flex; align-items: center; direction: ltr; white-space: nowrap; }
      .src { position: absolute; left: 0; right: 0; text-align: center; font-family: var(--font-en); font-weight: 700; font-size: 22px; letter-spacing: .14em;
        color: var(--fg-muted); direction: ltr; white-space: nowrap; }
      .src b { color: var(--lime); font-weight: 800; }
      .shot { position: absolute; border-radius: 28px; overflow: hidden; box-shadow: 0 34px 80px rgba(0,0,0,.55), 0 0 0 2px rgba(255,255,255,.1); background: #0b0b0b; }
      .shot img, .shot video { position: absolute; left: 0; top: 0; width: 100%; }
      .en { font-family: var(--font-en); direction: ltr; unicode-bidi: isolate; font-weight: 900; white-space: nowrap; }
      .y { color: var(--yellow); } .l { color: var(--lime); } .o { color: var(--orange); } .m { color: var(--fg-muted); }
      .chipn { position: absolute; height: 92px; padding: 0 36px; border-radius: 46px; background: #0b2f29; border: 3px solid rgba(179,206,101,.6);
        color: var(--fg); font-family: var(--font-ar); font-weight: 800; font-size: 40px; display: flex; align-items: center; gap: 16px; white-space: nowrap; direction: rtl; }
      .chipn .d { width: 52px; height: 52px; border-radius: 50%; background: var(--lime); color: var(--ink); display: flex; align-items: center; justify-content: center; flex: none; }
      .chipn.y { border-color: var(--yellow); } .chipn.y .d { background: var(--yellow); }
      .chipn.o { border-color: var(--orange); } .chipn.o .d { background: var(--orange); color: #fff; }
      .chipn.g { opacity: .5; filter: grayscale(1); }
      .blobby { position: absolute; border-radius: 52% 48% 50% 50% / 56% 54% 46% 44%; background: radial-gradient(circle at 38% 32%, #fff7b0 0%, var(--yellow) 42%, #f2c23a 100%);
        box-shadow: 0 30px 60px rgba(0,0,0,.4), inset -10px -16px 30px rgba(200,140,20,.35); }
      .blobby i { position: absolute; top: 40%; width: 13%; height: 17%; border-radius: 50%; background: #0d0d0d; }
      .blobby i.a { left: 30%; } .blobby i.b { left: 57%; }
      .blobby b { position: absolute; left: 41%; top: 63%; width: 18%; height: 8%; border-radius: 0 0 40px 40px; background: #0d0d0d; }
      .bar2 { position: absolute; height: 56px; border-radius: 28px; background: rgba(255,255,255,.07); overflow: hidden; }
      .bar2 > i { position: absolute; top: 0; bottom: 0; right: 0; width: 100%; border-radius: 28px; transform-origin: 100% 50%; }
      .win2 { position: absolute; border-radius: 28px; background: #0f1513; border: 2px solid rgba(255,255,255,.1); box-shadow: 0 34px 80px rgba(0,0,0,.5); overflow: hidden; }
      .win2 .bar { position: absolute; left: 0; right: 0; top: 0; height: 56px; background: #18201d; display: flex; align-items: center; gap: 12px; padding: 0 24px; direction: ltr; }
      .win2 .bar i { width: 16px; height: 16px; border-radius: 50%; background: #3a4440; }
      .win2 .bar b { margin-left: 12px; font-family: var(--font-en); font-size: 22px; font-weight: 700; color: #8fa39b; letter-spacing: .06em; }
      .tile { position: absolute; width: 120px; height: 120px; border-radius: 30px; background: #123a33; border: 2px solid rgba(179,206,101,.35); display: flex;
        align-items: center; justify-content: center; color: var(--lime); }
      .bigq { position: absolute; font-family: var(--font-ar); font-weight: 900; color: rgba(179,206,101,.06); line-height: 1; }
      #rail { position: absolute; left: 0; right: 0; bottom: 92px; z-index: 82; display: flex; justify-content: center; gap: 12px; direction: rtl; pointer-events: none; }
      #rail .rl { height: 46px; min-width: 46px; padding: 0 16px; border-radius: 23px; border: 2px solid rgba(255,255,255,.16); background: rgba(4,22,20,.72);
        font-family: var(--font-en); font-weight: 800; font-size: 20px; letter-spacing: .1em; color: var(--fg-muted); display: flex; align-items: center; justify-content: center; }
      /* NEWS:CSS:END */"""

RAIL_HTML = ('      <!-- NEWS:RAIL:BEGIN -->\n      <div id="rail">' + "".join(f'<span class="rl" id="rl{n}">0{n}</span>' for n in range(1, 7))
             + '</div>\n      <!-- NEWS:RAIL:END -->')
rail_js = ['tl.fromTo("#rail", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 1.2);',
           'tl.to("#rail", { opacity: 0, duration: 0.4 }, 185.6);']
for n, (t, _) in enumerate(STORIES, 1):
    rail_js.append(f'tl.to("#rl{n}", {{ background: "#b3ce65", color: "#0d0d0d", borderColor: "#b3ce65", scale: 1.15, duration: 0.3, ease: "back.out(2)" }}, {t + 0.2});')
    nxt = STORIES[n][0] if n < len(STORIES) else 181.95
    rail_js.append(f'tl.to("#rl{n}", {{ background: "#437f3e", color: "#f6f8f0", borderColor: "#437f3e", scale: 1, duration: 0.3 }}, {nxt + 0.1});')
FLASHES = (26.35, 56.85, 82.6, 118.45, 136.6, 156.05, 163.45)

h = (HERE / "index.html").read_text(encoding="utf-8")
h = re.sub(r"\n\s*/\* NEWS:CSS:BEGIN.*?NEWS:CSS:END \*/", "", h, flags=re.S)
h = h.replace("/* project-level overrides go here */", "/* project-level overrides go here */" + NEWS_CSS, 1)
h = re.sub(r"\n\s*<!-- NEWS:RAIL:BEGIN -->.*?<!-- NEWS:RAIL:END -->", "", h, flags=re.S)
h = h.replace('<div id="wipe"></div>', RAIL_HTML + '\n\n      <div id="wipe"></div>', 1)
if 'assets/js/news.js' not in h:
    h = h.replace('<script src="assets/js/fx.js"></script>', '<script src="assets/js/fx.js"></script>\n    <script src="assets/js/news.js"></script>', 1)
h = re.sub(r"\n\s*// NEWS:ROOT:BEGIN.*?// NEWS:ROOT:END", "", h, flags=re.S)
fl = "".join(f'\n        tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.7, duration: 0.07, ease: "none", immediateRender: false }}, {t});'
             f'\n        tl.to("#flash", {{ opacity: 0, duration: 0.45, ease: "power2.out" }}, {t + 0.07:.2f});' for t in FLASHES)
h = h.replace("// root-level moments (flashes, global transitions) go below, in GLOBAL seconds",
              "// root-level moments (flashes, global transitions) go below, in GLOBAL seconds\n        // NEWS:ROOT:BEGIN\n        "
              + "\n        ".join(rail_js) + fl + "\n        // NEWS:ROOT:END", 1)
(HERE / "index.html").write_text(h, encoding="utf-8")


# ---------------------------------------------------------------- helpers
def flap(id_, top, text, size=150, cls="", gap=None):
    w = int(size * 0.74)
    tiles = []
    for c in text:
        if c == " ":
            tiles.append(f'<span class="fl sp" style="width:{int(w * 0.4)}px; height:{size}px"></span>')
        else:
            tiles.append(f'<span class="fl {cls}" style="width:{w}px; height:{size}px; line-height:{size}px; font-size:{int(size * 0.7)}px"><i style="font-style:normal">{c}</i></span>')
    g = f" gap:{gap}px;" if gap is not None else ""
    return f'<div id="{id_}" class="flap" style="top:{top}px;{g}" data-layout-allow-overlap>{"".join(tiles)}</div>'


def co(id_, top, text):
    return f'<div id="{id_}" class="co" style="top:{top}px"><span>{text}</span></div>'


def src(id_, top, text):
    return f'<div id="{id_}" class="src" style="top:{top}px">{text}</div>'


def line(id_, top, html, cls="t-h2", style=""):
    return f'<div class="row {cls}" style="top:{top}px;{style}" data-layout-allow-overlap><span class="mask"><span class="in" id="{id_}">{html}</span></span></div>'


def shot(id_, x, y, w, h, inner):
    return f'<div id="{id_}" class="shot" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px">{inner}</div>'


def chipn(id_, x, y, text, icon="check", cls="", style=""):
    return f'<div id="{id_}" class="chipn {cls}" style="left:{x}px; top:{y}px;{style}"><span class="d">{ic(icon, 30)}</span><span>{text}</span></div>'


def blobby(id_, x, y, s):
    return f'<div id="{id_}" class="blobby" style="left:{x}px; top:{y}px; width:{s}px; height:{s}px"><i class="a"></i><i class="b"></i><b></b></div>'


def bumper(sid, n, company, name, name_t, css, body, js, size=150, blob=("#136052", 540, 760), sfx_t=None):
    """STORY 0N board flips in at the scene start, company pill, the product name flips on its spoken word."""
    st = P.scenes[sid]["start"]
    make(sid, f"""
    #{sid}-lab {{ top: 250px; }}
""" + css, f"""
      {flap(f"{sid}-n", 250, f"STORY 0{n}", 92, "l")}
      {co(f"{sid}-co", 392, company)}
      {flap(f"{sid}-t", 500, name, size, "y")}
{body}
""", f"""
      window.HF_FLAP(fx, "#{sid}-n", {st + 0.05}, {{ st: 0.035, cyc: 5 }});
      fx.pop("#{sid}-co", {st + 0.45}, {{ from: 0.4 }});
      window.HF_FLAP(fx, "#{sid}-t", {name_t - 0.25}, {{ st: 0.05 }});
{js}
""", blob=blob)
    cue(st, "whoosh", 0.8)
    cue(st + 0.05, "typing", 0.45)
    cue(name_t - 0.2, "typing", 0.55)
    cue(name_t + 0.25, "impact-bass-1", 0.9)


# extra icons used by this reel
EXTRA_SYM = """
        <symbol id="i-phone" viewBox="0 0 64 64"><path d="M20 6h10l4 14-7 5c3 7 8 12 15 15l5-7 14 4v10c0 5-4 9-9 9C30 56 8 34 8 15c0-5 4-9 9-9z" fill="currentColor" /></symbol>
        <symbol id="i-lock2" viewBox="0 0 64 64"><rect x="12" y="28" width="40" height="30" rx="7" fill="currentColor" /><path d="M20 28v-8a12 12 0 0124 0v8" fill="none" stroke="currentColor" stroke-width="6" /></symbol>
        <symbol id="i-shield" viewBox="0 0 64 64"><path d="M32 6l22 8v16c0 14-9 24-22 28C19 54 10 44 10 30V14z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" /><path d="M22 32l7 7 13-14" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" /></symbol>
        <symbol id="i-flask" viewBox="0 0 64 64"><path d="M24 6h16M27 6v18L12 50c-2 4 1 8 5 8h30c4 0 7-4 5-8L37 24V6" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" /><path d="M18 42h28" stroke="currentColor" stroke-width="5" /></symbol>
        <symbol id="i-mail" viewBox="0 0 64 64"><rect x="8" y="14" width="48" height="36" rx="6" fill="none" stroke="currentColor" stroke-width="5" /><path d="M10 18l22 16 22-16" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" /></symbol>
        <symbol id="i-cal" viewBox="0 0 64 64"><rect x="8" y="12" width="48" height="44" rx="6" fill="none" stroke="currentColor" stroke-width="5" /><path d="M8 26h48M20 6v12M44 6v12" stroke="currentColor" stroke-width="5" stroke-linecap="round" /></symbol>
        <symbol id="i-doc" viewBox="0 0 64 64"><path d="M16 6h22l12 12v40H16z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" /><path d="M24 32h18M24 42h18" stroke="currentColor" stroke-width="5" stroke-linecap="round" /></symbol>
        <symbol id="i-laptop" viewBox="0 0 64 64"><rect x="12" y="12" width="40" height="28" rx="4" fill="none" stroke="currentColor" stroke-width="5" /><path d="M4 50h56" stroke="currentColor" stroke-width="6" stroke-linecap="round" /></symbol>
        <symbol id="i-mobile" viewBox="0 0 64 64"><rect x="18" y="4" width="28" height="56" rx="6" fill="none" stroke="currentColor" stroke-width="5" /><circle cx="32" cy="50" r="3" fill="currentColor" /></symbol>
        <symbol id="i-cloud" viewBox="0 0 64 64"><path d="M18 48h30a12 12 0 000-24 16 16 0 00-30-2 12 12 0 000 26z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" /></symbol>
        <symbol id="i-gear" viewBox="0 0 64 64"><circle cx="32" cy="32" r="9" fill="none" stroke="currentColor" stroke-width="5" /><path d="M32 6v9M32 49v9M6 32h9M49 32h9M13 13l7 7M44 44l7 7M13 51l7-7M44 20l7-7" stroke="currentColor" stroke-width="5" stroke-linecap="round" /></symbol>
        <symbol id="i-wave" viewBox="0 0 64 64"><path d="M8 32h6M18 22v20M28 14v36M38 22v20M48 28v8M56 32h2" stroke="currentColor" stroke-width="5" stroke-linecap="round" /></symbol>"""
h = (HERE / "index.html").read_text(encoding="utf-8")
h = re.sub(r"\n\s*<!-- NEWS:SYM:BEGIN -->.*?<!-- NEWS:SYM:END -->", "", h, flags=re.S)
h = h.replace("<!-- OPUS55:SYM:END -->", "<!-- OPUS55:SYM:END -->\n        <!-- NEWS:SYM:BEGIN -->" + EXTRA_SYM + "\n        <!-- NEWS:SYM:END -->", 1)
(HERE / "index.html").write_text(h, encoding="utf-8")

# ================================================================= HOOK
make("s1", """
    #s1-date { position: absolute; left: 0; right: 0; top: 1130px; display: flex; justify-content: center; }
    #s1-date span { height: 70px; padding: 0 30px; border-radius: 35px; background: var(--yellow); color: var(--ink); font-family: var(--font-en); font-weight: 900;
      font-size: 30px; letter-spacing: .2em; display: flex; align-items: center; direction: ltr; }
    #s1-tick { position: absolute; left: 0; right: 0; top: 1300px; height: 84px; background: var(--orange); overflow: hidden; }
    #s1-tk { position: absolute; left: 0; top: 0; height: 84px; display: flex; align-items: center; gap: 46px; white-space: nowrap; direction: ltr;
      font-family: var(--font-en); font-weight: 900; font-size: 34px; letter-spacing: .14em; color: #fff; }
""", f"""
      {flap("s1-a", 520, "AI NEWS", 170, "")}
      {line("s1-h1", 790, "اللي حصل الأسبوع ده", "t-h1", "font-size:104px")}
      <div id="s1-date"><span>3 OCT 2026</span></div>
      <div id="s1-tick"><div id="s1-tk">BREAKING · OPENAI DOTS · GPT-6.1 SOL · GEMINI 4 ARGON · SONNET 5.5 · MUSE CHARM · SUPER INTELLIGENCE · BREAKING · OPENAI DOTS · GPT-6.1 SOL</div></div>
""", """
      fx.punch("#s1-cam", 0, 1.15);
      window.HF_FLAP(fx, "#s1-a", 0.0, { st: 0.06 });
      fx.maskUp("#s1-h1", 0.95);
      fx.pop("#s1-date", 1.7, { from: 0.5 });
      tl.fromTo("#s1-tick", { scaleY: 0 }, { scaleY: 1, duration: 0.3, ease: "power3.out" }, 1.4);
      tl.fromTo("#s1-tk", { x: 0 }, { x: -1500, duration: 1.75, ease: "none" }, 1.4);
""", blob=("#136052", 540, 700))
cue(0.0, "typing", 0.6); cue(0.55, "impact-bass-1", 0.8); cue(1.7, "pop", 0.5)

# ---------------------------------------------------------------- s2 OpenAI: an assistant you can call
make("s2", """
    #s2-ph { position: absolute; left: 290px; top: 560px; width: 500px; height: 960px; border-radius: 70px; background: #050505; padding: 18px;
      box-shadow: 0 50px 100px rgba(0,0,0,.6), 0 0 0 3px rgba(255,255,255,.1); }
    #s2-scr { position: absolute; inset: 18px; border-radius: 54px; overflow: hidden; background: radial-gradient(circle at 50% 30%, #1b5a4e 0%, #0a2622 70%); }
    #s2-nm { position: absolute; left: 0; right: 0; top: 470px; text-align: center; font-family: var(--font-en); font-weight: 800; font-size: 46px; color: #fff; }
    #s2-st { position: absolute; left: 0; right: 0; top: 540px; text-align: center; font-family: var(--font-en); font-weight: 600; font-size: 28px; color: #9fc3b7; letter-spacing: .08em; }
    #s2-acc { position: absolute; left: 172px; top: 720px; width: 120px; height: 120px; border-radius: 50%; background: #3fbf5a; color: #fff; display: flex; align-items: center; justify-content: center; }
    #s2-av { position: absolute; left: 132px; top: 150px; width: 200px; height: 200px; }
    #s2-rings .ring { border-radius: 50%; border-color: var(--yellow); }
""", f"""
      <div class="row" style="top:250px"><span id="s2-oa" class="co" style="position:relative; display:inline-flex"><span>OPENAI</span></span></div>
      {line("s2-h1", 345, "مساعد ذكي", "t-h1", "font-size:120px")}
      <div id="s2-ph"><div id="s2-scr">
        <div id="s2-rings" class="abs" style="left:132px; top:150px; width:200px; height:200px"><div class="ring" id="s2-r1"></div><div class="ring" id="s2-r2"></div></div>
        {blobby("s2-av", 132, 150, 200)}
        <div id="s2-nm">your dot</div><div id="s2-st">INCOMING CALL…</div>
        <div id="s2-acc">{ic("phone", 60)}</div>
      </div></div>
      {line("s2-h2", 1580, "بتتصل عليه", "t-h2", "color:var(--yellow)")}
""", """
      fx.pop("#s2-oa", 4.0, { from: 0.4 });
      fx.maskUp("#s2-h1", 5.3);
      tl.fromTo("#s2-ph", { opacity: 0, y: 260, rotation: -6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.7, ease: "power3.out" }, 5.6);
      fx.pop("#s2-av", 6.2, { from: 0.3 });
      fx.rise("#s2-nm, #s2-st", 6.5, { y: 20, st: 0.1 });
      fx.ringPulse("#s2-r1, #s2-r2", 7.75, { scale: 2.0, st: 0.25 });
      fx.ringPulse("#s2-r1, #s2-r2", 8.9, { scale: 2.0, st: 0.25 });
      fx.shake("#s2-ph", 7.8, 10, 8);
      fx.pop("#s2-acc", 7.9, { from: 0.3 });
      fx.click("#s2-acc", 9.3, "#s2-acc");
      tl.to("#s2-st", { color: "#b3ce65", duration: 0.1 }, 9.35);
      fx.maskUp("#s2-h2", 9.25);
""", blob=("#0f4f44", 540, 1000))
cue(4.0, "pop", 0.5); cue(5.6, "whoosh-short", 0.6); cue(7.75, "notification", 0.6); cue(9.3, "click", 0.7)
# the narration says "a phone number"; the Dots page says you can call your dot inside ChatGPT (texting coming soon) -> no number shown
P.scenes["s2"]["note"] = "call UI is illustrative"

# ---------------------------------------------------------------- s3 24 hours, in the background
make("s3", """
    #s3-ring { position: absolute; left: 290px; top: 330px; width: 500px; height: 500px; }
    #s3-num { position: absolute; left: 290px; top: 440px; width: 500px; text-align: center; font-family: var(--font-ar); font-weight: 900; font-size: 210px; line-height: 1.2; }
    #s3-u { position: absolute; left: 0; right: 0; top: 860px; text-align: center; }
    .s3-c { right: 140px; }
""", f"""
      <svg id="s3-ring" viewBox="0 0 100 100" style="overflow:visible"><circle cx="50" cy="50" r="46" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="5" />
        <circle id="s3-arc" cx="50" cy="50" r="46" fill="none" stroke="#b3ce65" stroke-width="5" stroke-linecap="round" pathLength="1" transform="rotate(-90 50 50)" /></svg>
      <div id="s3-num" class="num">٢٤</div>
      <div id="s3-u" class="t-h2">ساعة شغّال</div>
      {chipn("s3-c1", 0, 1060, "يحضّر فاتورة نسيتها", "doc", "", "right:150px; left:auto")}
      {chipn("s3-c2", 0, 1180, "يصلّح bug من Slack", "gear", "y", "right:150px; left:auto")}
      {chipn("s3-c3", 0, 1300, "يجهّز بوستات المحتوى", "mail", "", "right:150px; left:auto")}
      {line("s3-h", 1470, "في الخلفية", "t-h1", "font-size:110px; color:var(--lime)")}
      {src("s3-src", 1650, "EXAMPLES FROM <b>OPENAI.COM</b> · INTRODUCING DOTS")}
""", """
      fx.draw("#s3-arc", 10.35, 0.75, "power2.out");
      fx.counter("#s3-num", 10.4, 11.05, 0, 24);
      fx.rise("#s3-u", 11.3, { y: 30 });
      fx.rise("#s3-c1", 12.3, { y: 40 }); fx.rise("#s3-c2", 12.6, { y: 40 }); fx.rise("#s3-c3", 12.9, { y: 40 });
      fx.maskUp("#s3-h", 13.75);
      fx.rise("#s3-src", 12.5, { y: 10, b: 0 });
""", blob=("#136052", 540, 600))
cue(10.35, "whoosh-short", 0.6); cue(12.3, "pop", 0.45); cue(12.6, "pop", 0.45); cue(12.9, "pop", 0.45); cue(13.8, "chime", 0.5)

# ---------------------------------------------------------------- s4 ChatGPT, but a call instead of the app
make("s4", """
    #s4-app { position: absolute; left: 560px; top: 560px; width: 400px; height: 560px; border-radius: 40px; background: #f4f4f1; color: #0d0d0d; }
    #s4-app .b1 { position: absolute; right: 30px; top: 70px; width: 250px; height: 70px; border-radius: 35px; background: #e3e3df; }
    #s4-app .b2 { position: absolute; left: 30px; top: 170px; width: 300px; height: 110px; border-radius: 30px; background: #ececea; }
    #s4-app .b3 { position: absolute; right: 30px; top: 310px; width: 200px; height: 70px; border-radius: 35px; background: #e3e3df; }
    #s4-app .in { position: absolute; left: 24px; right: 24px; bottom: 26px; height: 80px; border-radius: 40px; border: 2px solid #d4d4cf; }
    #s4-x { position: absolute; left: 545px; top: 800px; width: 430px; height: 20px; }
    #s4-call { position: absolute; left: 120px; top: 640px; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle at 45% 40%, #2c8a4a, #13602f);
      display: flex; align-items: center; justify-content: center; color: #fff; box-shadow: 0 0 80px rgba(63,191,90,.4); }
    #s4-call .ring { border-radius: 50%; border-color: #3fbf5a; }
    #s4-al { position: absolute; left: 560px; width: 400px; top: 1150px; text-align: center; }
    #s4-cl { position: absolute; left: 120px; width: 400px; top: 1150px; text-align: center; }
""", f"""
      {line("s4-h1", 260, "زي <span class='lat'>ChatGPT</span>", "t-h1", "font-size:116px")}
      {line("s4-h2", 420, "بس من غير التطبيق", "t-h3", "color:var(--fg-muted)")}
      <div id="s4-app"><i class="b1"></i><i class="b2"></i><i class="b3"></i><i class="in"></i></div>
      <svg id="s4-x" viewBox="0 0 430 20" style="overflow:visible"><path id="s4-xp" d="M0 10 L430 10" stroke="#ff5a33" stroke-width="16" stroke-linecap="round" pathLength="1" /></svg>
      <div id="s4-al" class="t-label" style="font-size:26px">APP CHAT</div>
      <div id="s4-call">{ic("phone", 170)}<div class="ring" id="s4-r1"></div><div class="ring" id="s4-r2"></div></div>
      <div id="s4-cl" class="t-label" style="font-size:26px; color:var(--lime)">VOICE CALL</div>
      {line("s4-h3", 1330, "بتكلّمه بمكالمة", "t-h1", "font-size:112px; color:var(--yellow)")}
      {src("s4-src", 1520, "<b>OPENAI.COM</b> · CALL YOUR DOT IN CHATGPT · TEXTING COMING SOON")}
""", """
      fx.maskUp("#s4-h1", 15.9);
      fx.rise("#s4-app", 15.0, { y: 80 }); fx.rise("#s4-al", 15.3, { y: 10, b: 0 });
      fx.maskUp("#s4-h2", 16.6);
      fx.strike("#s4-xp", 17.9);
      tl.to("#s4-app", { opacity: 0.35, filter: "grayscale(1)", duration: 0.3 }, 18.1);
      fx.pop("#s4-call", 18.9, { from: 0.2, e: "back.out(1.8)" });
      fx.rise("#s4-cl", 19.1, { y: 10, b: 0 });
      fx.ringPulse("#s4-r1, #s4-r2", 19.5, { scale: 1.5, st: 0.3 });
      fx.ringPulse("#s4-r1, #s4-r2", 20.7, { scale: 1.5, st: 0.3 });
      fx.maskUp("#s4-h3", 20.4);
      fx.rise("#s4-src", 20.9, { y: 10, b: 0 });
""", blob=("#0f4f44", 540, 900))
cue(15.0, "whoosh-short", 0.5); cue(17.9, "error", 0.5); cue(18.9, "pop", 0.6); cue(19.5, "notification", 0.45)

# ---------------------------------------------------------------- s5 Google: a model nobody can use
make("s5", """
    #s5-k { left: 90px; top: 560px; width: 900px; height: 508px; }
    #s5-k img { width: 900px; }
    #s5-lock { position: absolute; left: 430px; top: 700px; width: 220px; height: 220px; border-radius: 50%; background: rgba(4,22,20,.85); border: 6px solid var(--orange);
      color: var(--orange); display: flex; align-items: center; justify-content: center; }
    #s5-st { left: 300px; top: 1110px; }
""", f"""
      {line("s5-h1", 260, "وجوجل ردّت", "t-h1", "font-size:120px")}
      {shot("s5-k", 90, 560, 900, 508, '<img id="s5-img" src="assets/images/argon_key.png" />')}
      <div id="s5-lock">{ic("lock2", 110)}</div>
      <div id="s5-st" class="stamp en" style="font-size:58px">LOCKED</div>
      {line("s5-h2", 1290, "محدش يقدر يستخدمه", "t-h2", "color:var(--orange)")}
      {line("s5-h3", 1420, "لحد دلوقتي", "t-h3", "color:var(--fg-muted)")}
""", """
      fx.maskUp("#s5-h1", 22.55);
      tl.fromTo("#s5-k", { opacity: 0, y: 160, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power3.out" }, 23.0);
      tl.fromTo("#s5-img", { scale: 1.12 }, { scale: 1, duration: 3.5, ease: "power1.out" }, 23.0);
      tl.to("#s5-k", { filter: "blur(10px) grayscale(.7)", duration: 0.4 }, 24.3);
      fx.pop("#s5-lock", 24.35, { from: 1.8, e: "expo.out", d: 0.35 });
      fx.stamp("#s5-st", 24.75, "#s5-cam");
      fx.maskUp("#s5-h2", 24.4);
      fx.maskUp("#s5-h3", 25.5);
""", blob=("#136052", 540, 800))
cue(22.55, "whoosh-short", 0.5); cue(24.35, "error", 0.6); cue(24.75, "impact-bass-2", 0.7)

# ================================================================= STORY 01 · DOTS
bumper("s6", 1, "OPENAI", "DOTS", 29.9, """
    #s6-sh { left: 90px; top: 760px; width: 900px; height: 509px; } #s6-sh img { width: 900px; }
""", f"""
      {shot("s6-sh", 90, 760, 900, 509, '<img id="s6-img" src="assets/images/dots_avatars.png" />')}
      {line("s6-h", 1330, "الخاصية الجديدة", "t-h2")}
      {src("s6-src", 1470, "REAL · <b>OPENAI.COM</b> · INTRODUCING DOTS · SEP 29, 2026")}
""", """
      tl.fromTo("#s6-sh", { opacity: 0, y: 140, rotation: -3 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "power3.out" }, 26.9);
      tl.fromTo("#s6-img", { scale: 1.15 }, { scale: 1, duration: 3.4, ease: "power1.out" }, 26.9);
      fx.maskUp("#s6-h", 27.0);
      fx.rise("#s6-src", 27.4, { y: 10, b: 0 });
""", size=190)

# ---------------------------------------------------------------- s7 like Muse Spark, like Grok
make("s7", """
    #s7-eq1, #s7-eq2 { position: absolute; font-family: var(--font-en); font-weight: 900; font-size: 90px; color: var(--fg-muted); }
""", f"""
      {line("s7-h1", 260, "ببساطة حاجة زي", "t-h2")}
      {blobby("s7-b", 390, 520, 300)}
      <div id="s7-eq1" style="left:505px; top:880px">≈</div>
      <div id="s7-m" class="co" style="top:1010px"><span style="height:110px; font-size:46px; letter-spacing:.06em; border-color:var(--yellow); color:var(--yellow)">MUSE SPARK · META</span></div>
      <div id="s7-eq2" style="left:505px; top:1140px">≈</div>
      <div id="s7-g" class="co" style="top:1270px"><span style="height:110px; font-size:46px; letter-spacing:.06em">GROK · xAI</span></div>
      {line("s7-h2", 1460, "<span class='lat'>Agent</span> سهل وبسيط", "t-h2", "color:var(--lime)")}
""", """
      fx.maskUp("#s7-h1", 30.6);
      fx.pop("#s7-b", 30.3, { from: 0.3 });
      fx.breathe("#s7-b", 30.8, 5.5, 0.04, 1.4);
      fx.pop("#s7-eq1", 32.1); fx.pop("#s7-m", 32.3, { from: 0.4 });
      fx.pop("#s7-eq2", 35.3); fx.pop("#s7-g", 35.7, { from: 0.4 });
      fx.maskUp("#s7-h2", 36.65);
""", blob=("#0f4f44", 540, 760))
cue(30.3, "pop", 0.6); cue(32.3, "pop", 0.55); cue(35.7, "pop", 0.55)

# ---------------------------------------------------------------- s8 own computer + your apps
TILES = [("mail", 120, 1210), ("cal", 290, 1290), ("doc", 460, 1330), ("chat", 630, 1290), ("cloud", 800, 1210)]
make("s8", """
    #s8-w { left: 90px; top: 520px; width: 900px; height: 565px; }
    #s8-w .body { position: absolute; left: 0; right: 0; top: 56px; bottom: 0; overflow: hidden; }
    #s8-w img { position: absolute; left: 0; top: 0; width: 900px; }
    #s8-n { position: absolute; left: 0; right: 0; top: 1480px; text-align: center; font-size: 120px; line-height: 1.2; }
    #s8-nl { top: 1640px; }
""", f"""
      {line("s8-h1", 260, "شغّال في الخلفية", "t-h2")}
      {line("s8-h2", 375, "وعنده كمبيوتر خاص بيه", "t-h3", "color:var(--yellow)")}
      <div id="s8-w" class="win2"><div class="bar"><i></i><i></i><i></i><b>YOUR DOT'S CLOUD COMPUTER</b></div><div class="body"><img id="s8-img" src="assets/images/dots_computer.png" /></div></div>
      {"".join(f'<div id="s8-t{i}" class="tile" style="left:{x}px; top:{y}px">{ic(n, 64)}</div>' for i, (n, x, y) in enumerate(TILES))}
      <div id="s8-n" class="en y"><span id="s8-nn">0</span>+</div>
      <div id="s8-nl" class="src">APPS · <b>OPENAI.COM</b></div>
""", """
      fx.maskUp("#s8-h1", 37.9);
      fx.maskUp("#s8-h2", 39.2);
      tl.fromTo("#s8-w", { opacity: 0, y: 140, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "power3.out" }, 39.3);
      tl.fromTo("#s8-img", { scale: 1.1 }, { scale: 1, duration: 3.6, ease: "power1.out" }, 39.3);
      fx.pop("#s8-t0, #s8-t1, #s8-t2, #s8-t3, #s8-t4", 40.4, { st: 0.12 });
      fx.counter("#s8-nn", 40.6, 41.8, 0, 4000, { ar: false });
      fx.rise("#s8-nl", 41.0, { y: 10, b: 0 });
""", blob=("#136052", 540, 860))
cue(39.3, "whoosh-short", 0.6); cue(40.4, "pop", 0.45); cue(40.64, "pop", 0.45); cue(40.88, "pop", 0.45); cue(41.8, "chime", 0.5)

# ---------------------------------------------------------------- s9 no model picker
MODELS = ["GPT-6 Astra", "GPT-6.1 Sol", "GPT-6 Luna"]
make("s9", """
    #s9-dd { position: absolute; left: 190px; top: 560px; width: 700px; border-radius: 30px; background: #f4f4f1; color: #0d0d0d; overflow: hidden;
      box-shadow: 0 30px 70px rgba(0,0,0,.45); direction: ltr; }
    #s9-dd .hd { height: 100px; padding: 0 36px; display: flex; align-items: center; justify-content: space-between; font-family: var(--font-en); font-weight: 800; font-size: 34px;
      border-bottom: 2px solid #e1e1dc; color: #6b6b66; }
    #s9-dd .op { height: 96px; padding: 0 36px; display: flex; align-items: center; font-family: var(--font-en); font-weight: 700; font-size: 38px; border-bottom: 2px solid #ececea; }
    #s9-x { position: absolute; left: 170px; top: 560px; width: 740px; height: 390px; }
    #s9-auto { position: absolute; left: 0; right: 0; top: 1090px; display: flex; justify-content: center; }
    #s9-auto span { height: 120px; padding: 0 50px; border-radius: 60px; background: var(--lime); color: var(--ink); font-family: var(--font-ar); font-weight: 900; font-size: 52px;
      display: flex; align-items: center; gap: 18px; white-space: nowrap; }
""", f"""
      {line("s9-h1", 260, "مش هتختار موديل", "t-h2")}
      <div id="s9-dd"><div class="hd"><span>Model</span><span>▾</span></div>{"".join(f'<div class="op">{m}</div>' for m in MODELS)}</div>
      <svg id="s9-x" viewBox="0 0 740 390" style="overflow:visible"><path id="s9-x1" d="M20 20 L720 370" stroke="#ff5a33" stroke-width="18" stroke-linecap="round" fill="none" pathLength="1" />
        <path id="s9-x2" d="M720 20 L20 370" stroke="#ff5a33" stroke-width="18" stroke-linecap="round" fill="none" pathLength="1" /></svg>
      <div id="s9-auto"><span id="s9-a">{blobby("s9-ab", 0, 0, 80).replace('style="left:0px; top:0px;', 'style="position:relative;')} هو اللي بيختار</span></div>
      {line("s9-h2", 1290, "على حسب الـــ<span class='lat'>task</span>", "t-h1", "font-size:94px; color:var(--yellow)")}
""", """
      fx.maskUp("#s9-h1", 43.4);
      tl.fromTo("#s9-dd", { opacity: 0, y: 100 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 43.6);
      fx.strike("#s9-x1", 44.3); fx.strike("#s9-x2", 44.45);
      tl.to("#s9-dd", { opacity: 0.35, scale: 0.94, duration: 0.3 }, 44.8);
      fx.pop("#s9-auto", 45.7, { from: 0.4 });
      fx.maskUp("#s9-h2", 47.4);
""", blob=("#0f4f44", 540, 860))
cue(43.6, "whoosh-short", 0.5); cue(44.3, "error", 0.55); cue(45.7, "pop", 0.6); cue(47.5, "chime", 0.45)

# ---------------------------------------------------------------- s10 plans
PLANS = [("PRO", 51.85), ("BUSINESS PREMIUM", 52.35), ("ENTERPRISE", 53.35)]
make("s10", """
    .s10-p { position: absolute; left: 140px; width: 800px; height: 150px; border-radius: 34px; border: 3px solid rgba(179,206,101,.35); background: #0b2f29;
      display: flex; align-items: center; justify-content: space-between; padding: 0 44px; direction: ltr; }
    .s10-p b { font-family: var(--font-en); font-weight: 900; font-size: 46px; letter-spacing: .06em; color: var(--fg); }
    .s10-p .ck { width: 74px; height: 74px; border-radius: 50%; background: var(--lime); color: var(--ink); display: flex; align-items: center; justify-content: center; }
    #s10-f { border-color: rgba(255,90,51,.6); background: rgba(255,255,255,.03); }
    #s10-f .ck { background: var(--orange); color: #fff; }
""", f"""
      {line("s10-h1", 260, "بس للأسف مش للكل", "t-h2")}
      {"".join(f'<div id="s10-p{i}" class="s10-p" style="top:{480 + i * 180}px"><b>{n}</b><span class="ck" id="s10-c{i}">{ic("check", 46)}</span></div>' for i, (n, _) in enumerate(PLANS))}
      <div id="s10-f" class="s10-p" style="top:1060px"><b>FREE</b><span class="ck" id="s10-fc">{ic("x", 46)}</span></div>
      {line("s10-h2", 1290, "مش في الخطط المجانية", "t-h2", "color:var(--orange)")}
      {src("s10-src", 1430, "<b>OPENAI.COM</b> · PRO + BUSINESS PREMIUM · ENTERPRISE BETA")}
""", """
      fx.maskUp("#s10-h1", 50.2);
""" + "".join(f"""      fx.rise("#s10-p{i}", {t - 0.25}, {{ y: 40 }}); fx.pop("#s10-c{i}", {t}, {{ from: 0.2 }});
""" for i, (_, t) in enumerate(PLANS)) + """
      fx.rise("#s10-f", 54.4, { y: 40 }); fx.pop("#s10-fc", 55.3, { from: 0.2 });
      tl.to("#s10-f", { opacity: 0.5, duration: 0.3 }, 55.5);
      fx.shake("#s10-f", 55.35, 12, 6);
      fx.maskUp("#s10-h2", 55.2);
      fx.rise("#s10-src", 53.6, { y: 10, b: 0 });
""", blob=("#136052", 540, 800))
for _, t in PLANS:
    cue(t, "pop", 0.5)
cue(55.3, "error", 0.6)

# ================================================================= STORY 02 · GPT-6.1 SOL
bumper("s11", 2, "OPENAI", "GPT-6.1 SOL", 59.4, """
    #s11-sh { left: 190px; top: 760px; width: 700px; height: 626px; } #s11-sh img { width: 700px; }
""", f"""
      {shot("s11-sh", 190, 760, 700, 626, '<img id="s11-img" src="assets/images/sol_card.png" />')}
      {src("s11-src", 1430, "REAL · <b>OPENAI.COM</b> · INTRODUCING GPT-6.1 SOL")}
""", """
      tl.fromTo("#s11-sh", { opacity: 0, y: 160 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 57.6);
      tl.fromTo("#s11-img", { scale: 1.1 }, { scale: 1, duration: 4.5, ease: "power1.out" }, 57.6);
      fx.rise("#s11-src", 58.0, { y: 10, b: 0 });
""", size=118)

# ---------------------------------------------------------------- s12 a fifth of the price
make("s12", """
    .s12-r { position: absolute; left: 110px; width: 860px; }
    .s12-r .nm { position: absolute; right: 0; top: 0; font-family: var(--font-en); font-weight: 900; font-size: 44px; direction: ltr; }
    .s12-r .pr { position: absolute; left: 0; top: 0; font-family: var(--font-en); font-weight: 800; font-size: 40px; direction: ltr; color: var(--fg-muted); }
    .s12-r .bar2 { top: 76px; left: 0; right: 0; }
    #s12-big { position: absolute; left: 0; right: 0; top: 1180px; text-align: center; font-size: 260px; line-height: 1.1; }
""", f"""
      {line("s12-h1", 260, "تقريبًا نفس ذكاء <span class='lat'>Astra</span>", "t-h2")}
      <div class="s12-r" id="s12-a" style="top:520px"><span class="nm">GPT-6 Astra</span><span class="pr">$10 / $50</span><div class="bar2"><i id="s12-af" style="background:var(--orange)"></i></div></div>
      <div class="s12-r" id="s12-s" style="top:740px"><span class="nm y">GPT-6.1 Sol</span><span class="pr">$2 / $10</span><div class="bar2"><i id="s12-sf" style="background:var(--lime)"></i></div></div>
      <div class="src" style="top:900px">PRICE PER 1M TOKENS · INPUT / OUTPUT · <b>OPENAI.COM</b></div>
      {line("s12-h2", 1010, "بس بـــ", "t-h2", "color:var(--fg-muted)")}
      <div id="s12-big" class="en y"><span id="s12-b">1/5</span></div>
      {line("s12-h3", 1500, "خُمس السعر", "t-h1", "font-size:120px")}
""", """
      fx.maskUp("#s12-h1", 62.2);
      fx.rise("#s12-a", 62.4, { y: 30 }); fx.meter("#s12-af", 62.6, 0.6, 1, { e: "power3.out" });
      fx.rise("#s12-s", 63.6, { y: 30 }); fx.meter("#s12-sf", 63.8, 0.6, 1, { e: "power3.out" });
      tl.to("#s12-sf", { scaleX: 0.2, duration: 0.7, ease: "power3.inOut" }, 65.3);
      fx.maskUp("#s12-h2", 65.1);
      tl.fromTo("#s12-b", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }, 65.75);
      fx.shake("#s12-cam", 65.85, 14, 6);
      fx.maskUp("#s12-h3", 66.1);
""", blob=("#136052", 540, 900))
cue(62.6, "whoosh-short", 0.5); cue(63.8, "whoosh-short", 0.5); cue(65.75, "impact-bass-1", 0.9)

# ---------------------------------------------------------------- s13 price war
make("s13", """
    #s13-tr { position: absolute; left: 110px; top: 1140px; width: 860px; height: 22px; border-radius: 11px; background: rgba(255,255,255,.12); }
    #s13-mk { position: absolute; left: 470px; top: 1095px; width: 140px; height: 112px; }
    #s13-cl { position: absolute; right: 60px; top: 520px; width: 420px; text-align: center; }
    #s13-oa { position: absolute; left: 60px; top: 520px; width: 420px; text-align: center; }
    .s13-pn { font-family: var(--font-en); font-weight: 900; font-size: 52px; letter-spacing: .08em; }
    #s13-st { left: 330px; top: 1290px; }
    .s13-u { position: absolute; width: 36px; height: 44px; color: var(--fg-muted); }
""", f"""
      {line("s13-h1", 250, "حرب الأسعار", "t-h1", "font-size:116px")}
      <div id="s13-cl">{spark("s13-sp", 110, 0, 200)}<div class="s13-pn" style="margin-top:230px; color:#e8977c">CLAUDE</div></div>
      <div id="s13-oa"><div style="width:200px; height:200px; margin:0 auto; border-radius:50%; border:8px solid #f6f8f0; display:flex; align-items:center; justify-content:center"><span class="en" style="font-size:44px">AI</span></div><div class="s13-pn" style="margin-top:30px">OPENAI</div></div>
      {chipn("s13-c1", 0, 860, "<span class='lat'>Opus 5.5</span> بسعر أقل", "check", "", "right:80px; left:auto")}
      {chipn("s13-c2", 0, 980, "<span class='lat'>Sonnet 5.5</span> أوفر", "check", "y", "right:80px; left:auto")}
      <div id="s13-tr"></div>
      <svg id="s13-mk" viewBox="0 0 48 56" style="color:var(--yellow)"><use href="#i-person" /></svg>
      <div id="s13-st" class="stamp" style="font-size:56px">ما تخسرش العملاء</div>
      {line("s13-h2", 1500, "فـــ<span class='lat'>OpenAI</span> لازم ترد", "t-h2", "color:var(--yellow)")}
""", """
      fx.maskUp("#s13-h1", 67.1);
      fx.rise("#s13-cl", 68.2, { y: 40 }); fx.rise("#s13-oa", 68.4, { y: 40 });
      tl.fromTo("#s13-sp-svg", { rotation: 0 }, { rotation: 120, duration: 4, ease: "power1.out" }, 68.2);
      fx.pop("#s13-c1", 70.0, { from: 0.4 }); fx.pop("#s13-c2", 72.25, { from: 0.4 });
      fx.rise("#s13-tr", 70.4, { y: 20 }); fx.pop("#s13-mk", 70.5, { from: 0.3 });
      tl.to("#s13-mk", { x: 300, duration: 0.8, ease: "power2.inOut" }, 70.9);
      tl.to("#s13-mk", { x: 360, duration: 0.5, ease: "power2.inOut" }, 72.4);
      fx.maskUp("#s13-h2", 74.1);
      tl.to("#s13-oa", { scale: 1.12, duration: 0.3, ease: "back.out(2)" }, 74.7);
      tl.to("#s13-mk", { x: -280, duration: 0.9, ease: "power3.inOut" }, 75.1);
      fx.stamp("#s13-st", 76.4, "#s13-cam");
""", blob=("#0f4f44", 540, 760))
cue(68.2, "whoosh-short", 0.5); cue(70.0, "pop", 0.5); cue(72.25, "pop", 0.5); cue(75.1, "whoosh", 0.5); cue(76.4, "impact-bass-2", 0.7)

# ---------------------------------------------------------------- s14 DevDay: 20+ more launches
make("s14", """
    #s14-sh { left: 90px; top: 560px; width: 900px; height: 507px; } #s14-sh img { width: 900px; }
    #s14-n { position: absolute; left: 0; right: 0; top: 1120px; text-align: center; font-size: 180px; line-height: 1.1; }
    #s14-p { position: absolute; left: 0; right: 0; top: 1490px; display: flex; justify-content: center; }
    #s14-p span { height: 90px; padding: 0 40px; border-radius: 45px; background: var(--yellow); color: var(--ink); font-family: var(--font-ar); font-weight: 900; font-size: 42px;
      display: flex; align-items: center; white-space: nowrap; }
""", f"""
      {line("s14-h1", 260, "وإطلاقات تانية كتير", "t-h2")}
      {co("s14-co", 400, "DEVDAY 2026")}
      {shot("s14-sh", 90, 560, 900, 507, '<img id="s14-img" src="assets/images/devday_grid.png" />')}
      <div id="s14-n" class="en y"><span id="s14-nn">0</span>+</div>
      {src("s14-src", 1340, "ANNOUNCEMENTS · <b>OPENAI.COM</b> · DEVDAY 2026 RECAP")}
      <div id="s14-p"><span>في الحلقة الكاملة</span></div>
""", """
      fx.maskUp("#s14-h1", 77.7);
      fx.pop("#s14-co", 78.0, { from: 0.4 });
      tl.fromTo("#s14-sh", { opacity: 0, y: 140 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 78.1);
      tl.fromTo("#s14-img", { scale: 1.15 }, { scale: 1, duration: 4.5, ease: "power1.out" }, 78.1);
      fx.counter("#s14-nn", 78.3, 79.3, 0, 20, { ar: false });
      fx.rise("#s14-src", 79.0, { y: 10, b: 0 });
      fx.pop("#s14-p", 80.9, { from: 0.4 });
""", blob=("#136052", 540, 820))
cue(78.1, "whoosh-short", 0.5); cue(79.3, "chime", 0.45); cue(80.9, "pop", 0.55)

# ================================================================= STORY 03 · GEMINI 4 ARGON
bumper("s15", 3, "GOOGLE", "ARGON", 84.85, """
    #s15-sh { left: 90px; top: 760px; width: 900px; height: 508px; } #s15-sh img { width: 900px; }
    #s15-g { position: absolute; left: 0; right: 0; top: 420px; }
""", f"""
      {shot("s15-sh", 90, 760, 900, 508, '<img id="s15-img" src="assets/images/argon_key.png" />')}
      {line("s15-h", 1320, "<span class='lat'>Gemini 4 Argon</span>", "t-h2", "direction:ltr")}
      {src("s15-src", 1460, "REAL · <b>BLOG.GOOGLE</b> · SEP 30, 2026")}
""", """
      tl.fromTo("#s15-sh", { opacity: 0, y: 140 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 83.1);
      tl.fromTo("#s15-img", { scale: 1.15 }, { scale: 1, duration: 3, ease: "power1.out" }, 83.1);
      fx.maskUp("#s15-h", 83.75);
      fx.rise("#s15-src", 83.9, { y: 10, b: 0 });
""", size=190)

# ---------------------------------------------------------------- s16 Google's own benchmarks
# argon_bench.png is 560x562 (table from @GoogleDeepMind's post). Shown at 900 px (x1.607). Argon column x 258..330 -> 415..530
make("s16", """
    #s16-sh { left: 90px; top: 480px; width: 900px; height: 903px; background: #fff; } #s16-sh img { width: 900px; }
    #s16-col { position: absolute; left: 408px; top: 18px; width: 130px; height: 870px; border-radius: 12px; border: 6px solid var(--orange); box-shadow: 0 0 30px rgba(255,90,51,.5); }
    #s16-v { position: absolute; left: 0; right: 0; top: 1430px; display: flex; justify-content: center; gap: 22px; direction: ltr; }
    #s16-v span { height: 84px; padding: 0 30px; border-radius: 42px; background: #0b2f29; border: 3px solid rgba(255,255,255,.2); font-family: var(--font-en); font-weight: 900;
      font-size: 36px; display: flex; align-items: center; white-space: nowrap; }
""", f"""
      {line("s16-h1", 250, "بنشماركس جوجل بتقول", "t-h2")}
      {shot("s16-sh", 90, 480, 900, 903, '<img id="s16-img" src="assets/images/argon_bench.png" /><div id="s16-col"></div>')}
      <div id="s16-v"><span id="s16-v0" class="o">ARGON</span><span id="s16-v1">&gt; OPUS 5.5</span><span id="s16-v2">&gt; GPT-6 ASTRA</span></div>
      {src("s16-src", 1560, "GOOGLE'S OWN BENCHMARKS · <b>@GOOGLEDEEPMIND</b> ON X")}
""", """
      fx.maskUp("#s16-h1", 85.65);
      tl.fromTo("#s16-sh", { opacity: 0, y: 160 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 85.9);
      fx.pop("#s16-col", 86.7, { from: 1.3, e: "power3.out", d: 0.35 });
      fx.pop("#s16-v0", 87.6, { from: 0.4 }); fx.pop("#s16-v1", 88.95, { from: 0.4 }); fx.pop("#s16-v2", 90.1, { from: 0.4 });
      fx.rise("#s16-src", 86.6, { y: 10, b: 0 });
""", blob=("#136052", 540, 900), push=1.02)
cue(85.9, "whoosh-short", 0.5); cue(86.7, "click", 0.6); cue(88.95, "pop", 0.5); cue(90.1, "pop", 0.5)

# ---------------------------------------------------------------- s17 Artificial Analysis: not #1 (REAL index, captured 3 Oct 2026)
AA = [("Claude Opus 5.5", 58, "#e8977c"), ("Claude Sonnet 5.5", 56, "#e8977c"), ("GPT-6 Astra", 53, "#f6f8f0"), ("Gemini 4 Argon", 53, "#ff5a33")]
rows = ""
for i, (n, v, c) in enumerate(AA):
    y = 520 + i * 200
    rows += (f'<div class="s17-r" id="s17-r{i}" style="top:{y}px"><span class="nm" style="color:{c}">{n}</span><span class="rk">#{i + 1 if i < 3 else "5"}</span>'
             f'<div class="bar2"><i id="s17-f{i}" style="background:{"var(--orange)" if i == 3 else "var(--lime)" if i == 0 else "rgba(179,206,101,.55)"}"></i></div>'
             f'<span class="v" id="s17-v{i}">{v}</span></div>')
make("s17", """
    .s17-r { position: absolute; left: 110px; width: 860px; height: 170px; direction: ltr; }
    .s17-r .nm { position: absolute; left: 0; top: 0; font-family: var(--font-en); font-weight: 900; font-size: 42px; }
    .s17-r .rk { position: absolute; right: 0; top: 0; font-family: var(--font-en); font-weight: 900; font-size: 42px; color: var(--fg-muted); }
    .s17-r .bar2 { left: 0; right: 130px; top: 76px; }
    .s17-r .bar2 > i { left: 0; right: auto; transform-origin: 0 50%; }
    .s17-r .v { position: absolute; right: 0; top: 70px; font-family: var(--font-en); font-weight: 900; font-size: 54px; color: var(--yellow); }
    #s17-st { left: 600px; top: 1300px; }
""", f"""
      {line("s17-h1", 250, "بس <span class='lat'>Artificial Analysis</span>", "t-h2", "font-size:82px")}
      {line("s17-h2", 365, "عندهم رأي تاني", "t-h3", "color:var(--fg-muted)")}
      {rows}
      <div id="s17-st" class="stamp en" style="font-size:52px">NOT #1</div>
      {src("s17-src", 1420, "REAL DATA · <b>ARTIFICIALANALYSIS.AI</b> · OCT 3, 2026")}
      {line("s17-h3", 1500, "مش رقم واحد", "t-h1", "font-size:116px; color:var(--orange)")}
""", "\n".join([
    '      fx.maskUp("#s17-h1", 91.5);', '      fx.maskUp("#s17-h2", 93.0);',
    *[f'      fx.rise("#s17-r{i}", {92.6 + i * 0.25}, {{ y: 30 }}); fx.meter("#s17-f{i}", {92.75 + i * 0.25}, 0.6, {v / 60:.3f}, {{ e: "power3.out" }});' for i, (_, v, _) in enumerate(AA)],
    '      tl.to("#s17-r3", { scale: 1.04, duration: 0.25, ease: "back.out(2)" }, 95.3);',
    '      fx.stamp("#s17-st", 95.4, "#s17-cam");', '      fx.maskUp("#s17-h3", 95.45);', '      fx.rise("#s17-src", 93.6, { y: 10, b: 0 });']),
    blob=("#0f4f44", 540, 860))
cue(92.6, "whoosh-short", 0.5); cue(95.4, "impact-bass-2", 0.75)

# ---------------------------------------------------------------- s18 focus: cybersecurity
make("s18", """
    #s18-ic { position: absolute; left: 340px; top: 470px; width: 400px; height: 400px; color: var(--lime); }
    #s18-gl { position: absolute; left: 240px; top: 370px; width: 600px; height: 600px; border-radius: 50%; background: radial-gradient(circle, rgba(179,206,101,.32), transparent 65%); }
""", f"""
      {line("s18-h1", 250, "المختلف إن جوجل مركّزة على", "t-h3")}
      <div id="s18-gl"></div>
      <svg id="s18-ic" viewBox="0 0 64 64"><use href="#i-shield" /></svg>
      {line("s18-h2", 930, "<span class='lat'>Cybersecurity</span>", "t-h1", "font-size:104px; direction:ltr; color:var(--lime)")}
      {line("s18-h3", 1100, "الأمن السيبراني", "t-h2")}
      {chipn("s18-c1", 0, 1270, "متاح الأول لمتخصصين الأمن · <span class='lat'>Fairwind</span>", "lock2", "y", "right:90px; left:auto; font-size:34px")}
      {chipn("s18-c2", 0, 1390, "<span class='lat'>CWE-bench v1: 68%</span> · الأول (تعادل)", "shield", "", "right:90px; left:auto; font-size:34px")}
      {src("s18-src", 1530, "REAL · <b>BLOG.GOOGLE</b> · GEMINI 4 ARGON")}
""", """
      fx.maskUp("#s18-h1", 97.6);
      fx.pop("#s18-ic", 100.6, { from: 0.3 }); fx.pop("#s18-gl", 100.6, { from: 0.5 });
      fx.breathe("#s18-gl", 101.0, 3, 0.08, 1.2);
      fx.maskUp("#s18-h2", 102.3);
      fx.maskUp("#s18-h3", 103.1);
      fx.rise("#s18-c1", 101.3, { y: 40 }); fx.rise("#s18-c2", 101.7, { y: 40 });
      fx.rise("#s18-src", 101.9, { y: 10, b: 0 });
""", blob=("#136052", 540, 680))
cue(100.6, "sparkle", 0.5); cue(101.3, "pop", 0.45); cue(101.7, "pop", 0.45); cue(102.3, "whoosh-short", 0.5)

# ---------------------------------------------------------------- s19 focus: scientific research (+ the 3D sim from X)
make("s19", """
    #s19-v { left: 90px; top: 470px; width: 450px; height: 615px; }
    #s19-v img, #s19-v video { width: 450px; }
    #s19-ic { position: absolute; left: 680px; top: 470px; width: 220px; height: 220px; color: var(--yellow); }
    .s19-f { position: absolute; left: 580px; width: 420px; text-align: center; }
    .s19-f .n { font-family: var(--font-en); font-weight: 900; font-size: 84px; white-space: nowrap; color: var(--yellow); line-height: 1.1; direction: ltr; }
    .s19-f .t { font-family: var(--font-ar); font-weight: 800; font-size: 32px; color: var(--fg); line-height: 1.35; }
""", f"""
      {line("s19-h1", 250, "<span class='lat'>Scientific Research</span>", "t-h2", "font-size:80px; direction:ltr")}
      {shot("s19-v", 90, 470, 450, 615, '<img src="assets/images/argon_ocean.png" /><video id="s19-vid" src="assets/videos/argon_ocean.mp4" data-start="0" data-duration="6.6" data-media-start="0" data-hf-media-start-basis="local" muted playsinline></video>')}
      <div class="src" style="top:1100px; left:90px; right:auto; width:450px; font-size:18px">3D SIM · ARGON VS CLAUDE · <b>@AI_SCREENING</b></div>
      <svg id="s19-ic" viewBox="0 0 64 64"><use href="#i-flask" /></svg>
      <div class="s19-f" id="s19-f1" style="top:720px"><div class="n" data-layout-allow-overlap>40%</div><div class="t" data-layout-allow-overlap>أحسن من الـــ<span class="lat">baseline</span> في الكوانتم</div></div>
      <div class="s19-f" id="s19-f2" style="top:920px"><div class="n" data-layout-allow-overlap>300 TiB</div><div class="t" data-layout-allow-overlap>ذاكرة اتوفرت في جوجل</div></div>
      {line("s19-h2", 1240, "ليه مساهمات فعلًا", "t-h2")}
      {line("s19-h3", 1370, "في البحث العلمي", "t-h1", "font-size:110px; color:var(--yellow)")}
      {src("s19-src", 1560, "REAL · <b>BLOG.GOOGLE</b> · INTERNAL RESULTS")}
""", """
      fx.maskUp("#s19-h1", 104.2);
      tl.fromTo("#s19-v", { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 104.4);
      fx.pop("#s19-ic", 105.2, { from: 0.3 });
      fx.rise("#s19-f1", 106.6, { y: 40 }); fx.rise("#s19-f2", 107.6, { y: 40 });
      fx.maskUp("#s19-h2", 107.1);
      fx.maskUp("#s19-h3", 109.4);
      fx.rise("#s19-src", 106.8, { y: 10, b: 0 });
""", blob=("#0f4f44", 540, 800))
cue(104.4, "whoosh-short", 0.5); cue(105.2, "sparkle", 0.45); cue(106.6, "pop", 0.45); cue(107.6, "pop", 0.45)

# ---------------------------------------------------------------- s20 output: 1M tokens
make("s20", """
    .s20-r { position: absolute; left: 110px; width: 860px; direction: ltr; }
    .s20-r .nm { position: absolute; left: 0; top: 0; font-family: var(--font-en); font-weight: 900; font-size: 40px; }
    .s20-r .bar2 { left: 0; right: 0; top: 64px; height: 70px; border-radius: 35px; }
    .s20-r .bar2 > i { left: 0; right: auto; transform-origin: 0 50%; border-radius: 35px; }
    #s20-n { position: absolute; left: 0; right: 0; top: 520px; text-align: center; font-size: 170px; line-height: 1.1; }
""", f"""
      {line("s20-h1", 250, "والـــ<span class='lat'>Output</span> بيوصل", "t-h2")}
      <div id="s20-n" class="en y"><span id="s20-nn">0</span></div>
      <div class="src" style="top:730px">OUTPUT TOKENS · ONE RESPONSE</div>
      <div class="s20-r" id="s20-r0" style="top:860px"><span class="nm m">64K · USUAL</span><div class="bar2"><i id="s20-f0" style="background:rgba(255,255,255,.4)"></i></div></div>
      <div class="s20-r" id="s20-r1" style="top:1030px"><span class="nm m">132K</span><div class="bar2"><i id="s20-f1" style="background:rgba(255,255,255,.55)"></i></div></div>
      <div class="s20-r" id="s20-r2" style="top:1200px"><span class="nm y">GEMINI 4 ARGON · 1M</span><div class="bar2"><i id="s20-f2" style="background:var(--yellow)"></i></div></div>
      {line("s20-h2", 1400, "مليون <span class='lat'>token</span>", "t-h1", "font-size:120px")}
      {src("s20-src", 1580, "<b>BLOG.GOOGLE</b> · 1M, UP FROM 64K · 132K = NARRATOR'S EXAMPLE")}
""", """
      fx.maskUp("#s20-h1", 110.7);
      fx.counter("#s20-nn", 111.5, 113.2, 0, 1000000, { ar: false, e: "power3.in" });
      fx.rise("#s20-r0, #s20-r1, #s20-r2", 112.0, { y: 30, st: 0.12 });
      fx.meter("#s20-f2", 112.3, 0.9, 1, { e: "power3.out" });
      fx.meter("#s20-f0", 114.4, 0.3, 0.064, { e: "power3.out" });
      fx.meter("#s20-f1", 115.25, 0.3, 0.132, { e: "power3.out" });
      fx.shake("#s20-r2", 113.25, 12, 6);
      fx.maskUp("#s20-h2", 113.25);
      fx.rise("#s20-src", 114.0, { y: 10, b: 0 });
""", blob=("#136052", 540, 900))
cue(111.5, "riser", 0.35); cue(113.25, "impact-bass-1", 0.9); cue(114.4, "click", 0.5); cue(115.25, "click", 0.5)

# ================================================================= STORY 04 · ANTHROPIC
bumper("s21", 4, "ANTHROPIC", "SONNET 5.5", 120.3, """
    #s21-sh { left: 170px; top: 760px; width: 740px; height: 555px; background: #f0eee6; } #s21-sh img { width: 740px; }
    #s21-half { position: absolute; left: 0; right: 0; top: 1350px; display: flex; justify-content: center; }
    #s21-half > span { height: 110px; padding: 0 44px; border-radius: 55px; background: var(--yellow); color: var(--ink); font-family: var(--font-ar); font-weight: 900;
      font-size: 52px; display: flex; align-items: center; white-space: nowrap; }
""", f"""
      {shot("s21-sh", 170, 760, 740, 555, '<img id="s21-img" src="assets/images/sonnet_pricing.png" />')}
      <div id="s21-half"><span>نُص سعر الـــ<span class="lat">Opus</span></span></div>
      {src("s21-src", 1500, "REAL · <b>ANTHROPIC.COM</b> · $2 / $10 VS OPUS 5.5 $4 / $20")}
""", """
      tl.fromTo("#s21-sh", { opacity: 0, y: 140 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 119.2);
      fx.pop("#s21-half", 122.7, { from: 0.4 });
      fx.rise("#s21-src", 121.2, { y: 10, b: 0 });
""", size=118, blob=("#3a2a22", 540, 900))
cue(122.7, "pop", 0.6)

# ---------------------------------------------------------------- s22 my Sonnet 5.5 reel
make("s22", """
    #s22-ph { position: absolute; left: 300px; top: 470px; width: 480px; height: 854px; border-radius: 60px; background: #050505; padding: 16px;
      box-shadow: 0 50px 100px rgba(0,0,0,.6), 0 0 0 3px rgba(255,255,255,.1); }
    #s22-scr { position: absolute; inset: 16px; border-radius: 46px; overflow: hidden; background: #111; }
    #s22-scr img, #s22-scr video { position: absolute; left: 0; top: 0; width: 448px; }
    #s22-p { position: absolute; left: 0; right: 0; top: 1400px; display: flex; justify-content: center; }
    #s22-p span { height: 110px; padding: 0 46px; border-radius: 55px; background: var(--lime); color: var(--ink); font-family: var(--font-ar); font-weight: 900; font-size: 50px;
      display: flex; align-items: center; gap: 14px; white-space: nowrap; }
""", f"""
      {line("s22-h1", 260, "عملتلكم ريل عنه", "t-h2")}
      <div id="s22-ph"><div id="s22-scr"><img src="assets/images/sonnet_reel.png" /><video id="s22-v" src="assets/videos/sonnet_reel.mp4" data-start="0" data-duration="3.7" data-media-start="0" data-hf-media-start-basis="local" muted playsinline></video></div></div>
      <div id="s22-p"><span>شوف الريل ←</span></div>
""", """
      fx.maskUp("#s22-h1", 124.15);
      tl.fromTo("#s22-ph", { opacity: 0, y: 260, rotation: 5 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "power3.out" }, 124.1);
      fx.pop("#s22-p", 125.4, { from: 0.4 });
      tl.to("#s22-p", { x: -24, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 3 }, 125.9);
""", blob=("#3a2a22", 540, 900))
cue(124.1, "whoosh-short", 0.55); cue(125.4, "pop", 0.55)

# ---------------------------------------------------------------- s23 Claude Code mods
make("s23", """
    #s23-sh { left: 90px; top: 450px; width: 900px; height: 600px; background: #f0eee6; } #s23-sh img { width: 900px; top: -60px; }
    #s23-t { left: 90px; top: 1090px; width: 900px; height: 300px; }
    #s23-t .body { position: absolute; left: 0; right: 0; top: 56px; bottom: 0; padding: 26px 32px; font-family: var(--font-en); font-size: 34px; font-weight: 700; color: #e9e7df; direction: ltr; line-height: 1.6; }
    #s23-t .pr { color: #e8977c; }
    #s23-lp { position: absolute; left: 0; right: 0; top: 1420px; display: flex; justify-content: center; gap: 18px; direction: ltr; }
    #s23-lp span { height: 84px; padding: 0 30px; border-radius: 42px; background: #0b2f29; border: 3px solid var(--lime); color: var(--lime); font-family: var(--font-en);
      font-weight: 900; font-size: 32px; display: flex; align-items: center; white-space: nowrap; }
""", f"""
      {line("s23-h1", 250, "<span class='lat'>Claude</span> بيعدّل في <span class='lat'>Claude Code</span>", "t-h3", "font-size:66px")}
      {shot("s23-sh", 90, 450, 900, 600, '<img id="s23-img" src="assets/images/mods_head.png" />')}
      <div id="s23-t" class="win2"><div class="bar"><i></i><i></i><i></i><b>CLAUDE CODE</b></div><div class="body"><span class="pr">&gt; </span><span id="s23-ty"></span><span class="caret"></span><br/><span id="s23-ok" style="color:#b3ce65">✓ mod installed · hot reloaded</span></div></div>
      <div id="s23-lp"><span id="s23-l1">+ NEW UI</span><span id="s23-l2">+ NEW FEATURES</span><span id="s23-l3">+ YOUR WAY</span></div>
      {src("s23-src", 1540, "REAL · <b>CLAUDE.COM/BLOG</b> · CLAUDE CODE MODS · OCT 1, 2026")}
""", """
      fx.maskUp("#s23-h1", 127.6);
      tl.fromTo("#s23-sh", { opacity: 0, y: 140 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 128.2);
      tl.fromTo("#s23-img", { y: 0 }, { y: -120, duration: 7, ease: "none" }, 128.2);
      fx.rise("#s23-t", 129.6, { y: 60 });
      fx.typeText("#s23-ty", 130.2, "write a mod that adds a new button", 22);
      fx.hide("#s23-ok"); fx.rise("#s23-ok", 132.4, { y: 10, b: 0 });
      fx.pop("#s23-l1", 133.6, { from: 0.4 }); fx.pop("#s23-l2", 134.0, { from: 0.4 }); fx.pop("#s23-l3", 134.5, { from: 0.4 });
      fx.rise("#s23-src", 128.8, { y: 10, b: 0 });
""", blob=("#3a2a22", 540, 900))
cue(128.2, "whoosh-short", 0.5); cue(130.2, "typing", 0.5); cue(131.2, "typing", 0.5); cue(132.4, "chime", 0.55); cue(133.6, "pop", 0.45); cue(134.0, "pop", 0.45); cue(134.5, "pop", 0.45)
# illustrative: the typed request is an example (the blog: "ask Claude to create a mod… hot reload it")

# ================================================================= STORY 05 · META MUSE CHARM (device drawn in code: no official image captured)
CHARM = """<div id="{p}-dev" class="abs" style="left:{x}px; top:{y}px; width:{s}px; height:{s}px">
        <svg class="abs" style="left:{lx}px; top:{ly}px; width:{lw}px; height:{lh}px; overflow:visible" viewBox="0 0 100 100"><path d="M50 100 C 20 60, 30 10, 50 0 C 70 10, 80 60, 50 100" fill="none" stroke="#b3ce65" stroke-width="6" /></svg>
        <div class="abs" style="inset:0; border-radius:{r}px; background:linear-gradient(150deg,#f7f5ec,#d9d6c8); box-shadow:0 40px 80px rgba(0,0,0,.5), inset 0 -8px 20px rgba(0,0,0,.12)"></div>
        <div class="abs" style="left:{sm}px; top:{sm}px; width:{si}px; height:{si}px; border-radius:50%; background:radial-gradient(circle at 50% 40%,#1b5a4e,#06201c)">{blob}</div></div>"""


def charm(p, x, y, s):
    si = int(s * 0.72)
    return CHARM.format(p=p, x=x, y=y, s=s, r=int(s * 0.28), sm=int((s - si) / 2), si=si, lx=int(s * 0.32), ly=-int(s * 0.62), lw=int(s * 0.36), lh=int(s * 0.66),
                        blob=blobby(f"{p}-bb", int(si * 0.22), int(si * 0.2), int(si * 0.56)))


bumper("s24", 5, "META", "MUSE CHARM", 138.9, """
    #s24-f { position: absolute; left: 0; right: 0; top: 1470px; display: flex; justify-content: center; gap: 20px; direction: ltr; }
    #s24-f span { height: 84px; padding: 0 32px; border-radius: 42px; background: #0b2f29; border: 3px solid var(--yellow); color: var(--yellow); font-family: var(--font-en);
      font-weight: 900; font-size: 32px; display: flex; align-items: center; white-space: nowrap; }
""", f"""
      {charm("s24", 400, 940, 280)}
      <div id="s24-f"><span id="s24-f1">POCKET SIZE</span><span id="s24-f2">5G</span><span id="s24-f3">DEC 2026</span></div>
      {src("s24-src", 1600, "ILLUSTRATION · FACTS: <b>META.COM</b> · CNBC · AXIOS")}
""", """
      tl.fromTo("#s24-dev", { opacity: 0, y: -300, rotation: -20 }, { opacity: 1, y: 0, rotation: 0, duration: 0.9, ease: "back.out(1.4)" }, 137.4);
      tl.fromTo("#s24-dev", { rotation: 0 }, { rotation: 6, duration: 0.8, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false }, 138.3);
      fx.pop("#s24-f1", 139.3, { from: 0.4 }); fx.pop("#s24-f2", 139.55, { from: 0.4 }); fx.pop("#s24-f3", 139.8, { from: 0.4 });
      fx.rise("#s24-src", 139.4, { y: 10, b: 0 });
""", size=110, blob=("#136052", 540, 1080))
cue(139.3, "pop", 0.4); cue(139.55, "pop", 0.4); cue(139.8, "pop", 0.4)

# ---------------------------------------------------------------- s25 Muse Spark, but a dedicated device
make("s25", """
    .s25-i { position: absolute; top: 560px; width: 260px; height: 260px; color: var(--fg-muted); }
    #s25-i1 { left: 600px; } #s25-i2 { left: 220px; }
    .s25-x { position: absolute; top: 560px; width: 260px; height: 260px; }
    #s25-x1 { left: 600px; } #s25-x2 { left: 220px; }
    #s25-w { position: absolute; left: 640px; top: 1120px; width: 200px; height: 200px; color: var(--lime); }
""", f"""
      {line("s25-h1", 250, "هو <span class='lat'>Muse Spark</span>", "t-h2")}
      {line("s25-h2", 370, "بس في جهاز صغير", "t-h3", "color:var(--yellow)")}
      <svg id="s25-i1" class="s25-i" viewBox="0 0 64 64"><use href="#i-mobile" /></svg>
      <svg id="s25-i2" class="s25-i" viewBox="0 0 64 64"><use href="#i-laptop" /></svg>
      <svg id="s25-x1" class="s25-x" viewBox="0 0 100 100"><path id="s25-xp1" d="M10 90 L90 10" stroke="#ff5a33" stroke-width="9" stroke-linecap="round" pathLength="1" /></svg>
      <svg id="s25-x2" class="s25-x" viewBox="0 0 100 100"><path id="s25-xp2" d="M10 90 L90 10" stroke="#ff5a33" stroke-width="9" stroke-linecap="round" pathLength="1" /></svg>
      {charm("s25", 290, 1060, 300)}
      <svg id="s25-w" viewBox="0 0 64 64"><use href="#i-wave" /></svg>
      {line("s25-h3", 1460, "جهاز خاص تكلّمه منه", "t-h2")}
""", """
      fx.maskUp("#s25-h1", 140.5);
      fx.maskUp("#s25-h2", 142.5);
      fx.pop("#s25-i1", 145.6, { from: 0.4 }); fx.pop("#s25-i2", 146.3, { from: 0.4 });
      fx.strike("#s25-xp1", 147.25); fx.strike("#s25-xp2", 147.4);
      tl.to("#s25-i1, #s25-i2", { opacity: 0.3, duration: 0.3 }, 147.5);
      tl.fromTo("#s25-dev", { opacity: 0, y: 260, scale: 0.7 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "back.out(1.6)" }, 147.6);
      fx.pop("#s25-w", 148.6, { from: 0.3 });
      fx.breathe("#s25-w", 148.9, 1.4, 0.15, 0.7);
      fx.maskUp("#s25-h3", 148.1);
""", blob=("#0f4f44", 540, 1100))
cue(145.6, "pop", 0.45); cue(146.3, "pop", 0.45); cue(147.25, "error", 0.5); cue(147.6, "whoosh-short", 0.55); cue(148.6, "sparkle", 0.45)

# ---------------------------------------------------------------- s26 Muse Spark: easiest to connect
HUB = [("mail", 540, 580), ("cal", 830, 760), ("doc", 830, 1100), ("chat", 540, 1270), ("cloud", 250, 1100), ("gear", 250, 760)]
lines_svg = "".join(f'<path id="s26-l{i}" d="M540 930 L{x} {y}" stroke="#b3ce65" stroke-width="5" stroke-dasharray="1" pathLength="1" fill="none" />' for i, (_, x, y) in enumerate(HUB))
make("s26", """
    #s26-svg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    #s26-hub { position: absolute; left: 420px; top: 810px; width: 240px; height: 240px; border-radius: 50%; background: #0b2f29; border: 5px solid var(--yellow);
      display: flex; align-items: center; justify-content: center; font-family: var(--font-en); font-weight: 900; font-size: 46px; color: var(--yellow); }
""", f"""
      {line("s26-h1", 250, "من أسهل أدوات الـــ<span class='lat'>AI</span>", "t-h2")}
      <svg id="s26-svg" viewBox="0 0 1080 1920">{lines_svg}</svg>
      {"".join(f'<div id="s26-t{i}" class="tile" style="left:{x - 60}px; top:{y - 60}px">{ic(n, 64)}</div>' for i, (n, x, y) in enumerate(HUB))}
      <div id="s26-hub">MUSE</div>
      {line("s26-h2", 1440, "وتربطها بأدواتك", "t-h1", "font-size:110px; color:var(--lime)")}
""", "\n".join([
    '      fx.maskUp("#s26-h1", 151.5);', '      fx.pop("#s26-hub", 150.9, { from: 0.3 });',
    *[f'      fx.pop("#s26-t{i}", {152.6 + i * 0.15}, {{ from: 0.3 }});' for i in range(len(HUB))],
    *[f'      fx.draw("#s26-l{i}", {154.6 + i * 0.08}, 0.35);' for i in range(len(HUB))],
    '      tl.to("#s26-t0, #s26-t1, #s26-t2, #s26-t3, #s26-t4, #s26-t5", { borderColor: "#b3ce65", background: "#1d4d3c", duration: 0.2, stagger: 0.08 }, 154.9);',
    '      fx.maskUp("#s26-h2", 154.6);']), blob=("#136052", 540, 930))
cue(150.9, "pop", 0.55); cue(152.6, "pop", 0.4); cue(153.0, "pop", 0.4); cue(154.6, "chime", 0.55)

# ================================================================= STORY 06 · WHITE HOUSE
WH = ('<svg id="s27-wh" class="abs" viewBox="0 0 400 220" style="left:190px; top:820px; width:700px; height:385px; overflow:visible" fill="none" stroke="#f6f8f0" stroke-width="5" stroke-linejoin="round">'
      '<path id="s27-w1" pathLength="1" d="M20 210 H380 M40 210 V120 H360 V210" />'
      '<path id="s27-w2" pathLength="1" d="M130 120 L200 70 L270 120" />'
      '<path id="s27-w3" pathLength="1" d="M145 120 V200 M172 120 V200 M200 120 V200 M228 120 V200 M255 120 V200" />'
      '<path id="s27-w4" pathLength="1" d="M60 140 h30 v30 h-30 z M310 140 h30 v30 h-30 z" />'
      '<path id="s27-w5" pathLength="1" d="M200 70 V30 L230 38 L200 46" stroke="#ff5a33" /></svg>')
SEATS = [(260, 1300), (380, 1350), (500, 1370), (620, 1350), (740, 1300)]
make("s27", "", f"""
      {flap("s27-n", 250, "STORY 06", 92, "l")}
      {co("s27-co", 392, "WHITE HOUSE")}
      {line("s27-h1", 520, "قادة شركات الـــ<span class='lat'>AI</span>", "t-h2")}
      {line("s27-h2", 640, "اجتمعوا في البيت الأبيض", "t-h3", "color:var(--fg-muted)")}
      {WH}
      {"".join(f'<svg id="s27-p{i}" class="abs" viewBox="0 0 48 56" style="left:{x}px; top:{y}px; width:80px; height:94px; color:var(--lime)"><use href="#i-person" /></svg>' for i, (x, y) in enumerate(SEATS))}
      {line("s27-h3", 1500, "علشان اسم جديد للـــ<span class='lat'>AI</span>", "t-h2", "color:var(--yellow)")}
""", "\n".join([
    '      window.HF_FLAP(fx, "#s27-n", 156.1, { st: 0.035, cyc: 5 });', '      fx.pop("#s27-co", 156.5, { from: 0.4 });',
    '      fx.maskUp("#s27-h1", 156.9);', '      fx.maskUp("#s27-h2", 157.7);',
    *[f'      fx.draw("#s27-w{i}", {157.9 + (i - 1) * 0.18}, 0.6);' for i in range(1, 6)],
    *[f'      fx.pop("#s27-p{i}", {158.7 + i * 0.1}, {{ from: 0.3 }});' for i in range(len(SEATS))],
    '      fx.maskUp("#s27-h3", 160.6);']), blob=("#136052", 540, 1000))
cue(156.05, "whoosh", 0.8); cue(156.1, "typing", 0.45); cue(158.7, "pop", 0.4); cue(160.6, "whoosh-short", 0.5)

# ---------------------------------------------------------------- s28 ARTIFICIAL -> SUPER (signature payoff)
make("s28", """
    #s28-q { position: absolute; left: 90px; top: 1380px; width: 900px; border-radius: 26px; background: #f6f4ea; color: #0d0d0d; padding: 30px 40px; direction: ltr; }
    #s28-q b { display: block; font-family: var(--font-en); font-weight: 900; font-size: 22px; letter-spacing: .2em; color: #d93a2b; margin-bottom: 10px; }
    #s28-q p { margin: 0; font-family: var(--font-en); font-weight: 800; font-size: 38px; line-height: 1.25; }
""", f"""
      {line("s28-h1", 260, "وسمّوه", "t-h2")}
      {flap("s28-a", 520, "ARTIFICIAL", 96, "o", 8)}
      {flap("s28-b", 660, "INTELLIGENCE", 84, "", 6)}
      {line("s28-h2", 860, "الذكاء الخارق", "t-h1", "font-size:124px; color:var(--yellow)")}
      <div id="s28-q"><b>THE VERGE · SEP 30, 2026</b><p>“Trump orders US government to call AI ‘Super Intelligence’”</p></div>
""", """
      fx.maskUp("#s28-h1", 162.8);
      window.HF_FLAP(fx, "#s28-a", 162.7, { st: 0.03, cyc: 4, d: 0.3 });
      window.HF_FLAP(fx, "#s28-b", 162.85, { st: 0.03, cyc: 4, d: 0.3 });
      window.HF_REFLAP(fx, "#s28-a", 163.4, "  SUPER   ", { st: 0.03 });
      tl.to("#s28-a .fl", { color: "#ffec5c", duration: 0.1 }, 163.6);
      fx.shake("#s28-cam", 163.75, 12, 6);
      fx.maskUp("#s28-h2", 164.7);
      tl.fromTo("#s28-q", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 164.0);
""", blob=("#0f4f44", 540, 760))
cue(162.7, "typing", 0.55); cue(163.4, "typing", 0.6); cue(163.7, "impact-bass-1", 1.0); cue(164.0, "whoosh-short", 0.45)

# ---------------------------------------------------------------- s29 safety commitments
make("s29", """
    #s29-sh { position: absolute; left: 380px; top: 460px; width: 320px; height: 320px; color: var(--lime); }
    .s29-l { position: absolute; left: 170px; width: 740px; height: 96px; border-radius: 28px; background: #0b2f29; border: 2px solid rgba(179,206,101,.3); }
    .s29-l i { position: absolute; right: 30px; top: 23px; width: 50px; height: 50px; border-radius: 50%; background: var(--lime); color: var(--ink); display: flex; align-items: center; justify-content: center; }
    .s29-l b { position: absolute; right: 110px; top: 38px; height: 20px; border-radius: 10px; background: rgba(255,255,255,.18); }
    #s29-tg { position: absolute; left: 0; right: 0; top: 1300px; display: flex; justify-content: center; }
    #s29-tg span { height: 76px; padding: 0 30px; border-radius: 38px; border: 3px solid var(--orange); color: var(--orange); font-family: var(--font-en); font-weight: 900;
      font-size: 28px; letter-spacing: .14em; display: flex; align-items: center; direction: ltr; white-space: nowrap; }
""", f"""
      {line("s29-h1", 260, "واتفقوا على التزامات", "t-h2")}
      <svg id="s29-sh" viewBox="0 0 64 64"><use href="#i-shield" /></svg>
      {"".join(f'<div class="s29-l" id="s29-l{i}" style="top:{840 + i * 130}px"><i id="s29-c{i}">{ic("check", 30)}</i><b style="width:{[420, 340, 470][i]}px"></b></div>' for i in range(3))}
      <div id="s29-tg"><span>SELF-POLICED · NOT BINDING</span></div>
      {line("s29-h2", 1440, "لأمان الذكاء الاصطناعي", "t-h2", "color:var(--lime)")}
      {src("s29-src", 1580, "<b>THE VERGE</b> · HOW TECH LEADERS WILL SELF-POLICE AI SAFETY")}
""", "\n".join([
    '      fx.maskUp("#s29-h1", 166.4);', '      fx.pop("#s29-sh", 166.9, { from: 0.3 });',
    *[f'      fx.rise("#s29-l{i}", {168.0 + i * 0.3}, {{ y: 30 }}); fx.pop("#s29-c{i}", {169.0 + i * 0.35}, {{ from: 0.2 }});' for i in range(3)],
    '      fx.maskUp("#s29-h2", 170.8);', '      fx.pop("#s29-tg", 171.4, { from: 0.4 });', '      fx.rise("#s29-src", 171.6, { y: 10, b: 0 });']),
    blob=("#136052", 540, 800))
cue(166.9, "pop", 0.5); cue(169.0, "click", 0.5); cue(169.35, "click", 0.5); cue(169.7, "click", 0.5); cue(170.85, "chime", 0.45)

# ---------------------------------------------------------------- s30 the gate
SMALL = [(140 + (i % 6) * 150, 1180 + (i // 6) * 110) for i in range(12)]
make("s30", """
    .s30-d { position: absolute; width: 60px; height: 60px; border-radius: 50%; background: var(--lime); }
    #s30-g1, #s30-g2 { position: absolute; top: 560px; width: 30px; height: 520px; border-radius: 15px; background: #f6f8f0; }
    #s30-g1 { left: 380px; } #s30-g2 { left: 670px; }
    #s30-bar { position: absolute; left: 395px; top: 720px; width: 290px; height: 30px; border-radius: 15px; background: var(--orange); transform-origin: 0 50%; }
    .s30-big { position: absolute; left: 430px; width: 220px; height: 120px; border-radius: 26px; background: var(--yellow); color: var(--ink); font-family: var(--font-ar);
      font-weight: 900; font-size: 34px; display: flex; align-items: center; justify-content: center; white-space: nowrap; }
""", f"""
      {line("s30-h1", 250, "ده هيحجّم ناس كتير", "t-h2")}
      <div id="s30-g1"></div><div id="s30-g2"></div><div id="s30-bar"></div>
      {"".join(f'<div class="s30-d" id="s30-d{i}" style="left:{x}px; top:{y}px"></div>' for i, (x, y) in enumerate(SMALL))}
      <div class="s30-big" id="s30-b1" style="top:820px">شركات كبيرة</div>
      <div class="s30-big" id="s30-b2" style="top:960px">حكومات</div>
      {line("s30-h2", 1440, "وتبقى حكر عليهم", "t-h1", "font-size:116px; color:var(--orange)")}
      {line("s30-h3", 1600, "للأسف", "t-h3", "color:var(--fg-muted)")}
""", "\n".join([
    '      fx.maskUp("#s30-h1", 172.7);', '      fx.rise("#s30-g1, #s30-g2", 172.8, { y: 60 });',
    '      fx.rise("' + ", ".join(f"#s30-d{i}" for i in range(12)) + '", 173.2, { y: 40, st: 0.05 });',
    '      tl.fromTo("#s30-bar", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "expo.out" }, 174.6);',
    '      fx.shake("#s30-cam", 174.9, 10, 6);',
    '      tl.to("' + ", ".join(f"#s30-d{i}" for i in range(12)) + '", { y: -120, duration: 0.6, ease: "power2.inOut", stagger: 0.04 }, 175.4);',
    '      tl.to("' + ", ".join(f"#s30-d{i}" for i in range(12)) + '", { y: 0, background: "#4a5d57", duration: 0.5, ease: "back.out(2)", stagger: 0.04 }, 176.2);',
    '      fx.pop("#s30-b1", 178.6, { from: 0.4 }); fx.pop("#s30-b2", 179.6, { from: 0.4 });',
    '      fx.maskUp("#s30-h2", 177.9);', '      fx.maskUp("#s30-h3", 180.9);']), blob=("#3a2a22", 540, 900))
cue(173.2, "pop", 0.4); cue(174.6, "impact-bass-2", 0.7); cue(176.2, "error", 0.45); cue(178.6, "pop", 0.5); cue(179.6, "pop", 0.5)

# ================================================================= YOUR TURN
PILLS = [("01 DOTS", 120, 560), ("02 SOL", 620, 610), ("03 ARGON", 160, 720), ("04 SONNET", 560, 780), ("05 MUSE", 180, 880), ("06 SUPER AI", 540, 950)]
make("s31", """
    .s31-p { position: absolute; height: 84px; padding: 0 30px; border-radius: 42px; background: #0b2f29; border: 3px solid rgba(179,206,101,.6); color: var(--fg);
      font-family: var(--font-en); font-weight: 900; font-size: 32px; letter-spacing: .06em; display: flex; align-items: center; direction: ltr; white-space: nowrap; }
    #s31-in { position: absolute; left: 90px; top: 1160px; width: 900px; height: 130px; border-radius: 65px; background: #f4f4f1; color: #0d0d0d; }
    #s31-ty { position: absolute; right: 50px; top: 30px; font-family: var(--font-ar); font-weight: 800; font-size: 44px; direction: rtl; white-space: nowrap; }
""", f"""
      {line("s31-h1", 250, "قولّي إيه أكتر خبر عجبك؟", "t-h2", "font-size:84px")}
      {"".join(f'<div class="s31-p" id="s31-p{i}" style="left:{x}px; top:{y}px">{t}</div>' for i, (t, x, y) in enumerate(PILLS))}
      <div id="s31-in"><span id="s31-ty"></span></div>
      {line("s31-h2", 1360, "ورأيك في السلسلة دي", "t-h2", "color:var(--yellow)")}
""", "\n".join([
    '      fx.maskUp("#s31-h1", 182.3);',
    *[f'      fx.pop("#s31-p{i}", {182.9 + i * 0.12}, {{ from: 0.4 }});' for i in range(len(PILLS))],
    '      fx.rise("#s31-in", 183.4, { y: 40 });', '      fx.typeText("#s31-ty", 183.7, "أكتر خبر عجبني: ...", 14);',
    '      tl.to("#s31-p2", { scale: 1.15, background: "#b3ce65", color: "#0d0d0d", duration: 0.25, ease: "back.out(2)" }, 184.2);',
    '      fx.maskUp("#s31-h2", 184.6);']), blob=("#136052", 540, 800))
cue(182.9, "pop", 0.4); cue(183.3, "pop", 0.4); cue(183.7, "typing", 0.45); cue(184.2, "click", 0.55)

make("s32", """
    #s32-h { position: absolute; left: 230px; top: 820px; width: 620px; height: 1102px; }
    #s32-h img { position: absolute; left: 0; top: 0; width: 620px; filter: drop-shadow(0 30px 50px rgba(0,0,0,.55)); }
    #s32-nm { position: absolute; left: 0; right: 0; top: 1420px; text-align: center; }
    #s32-btn { position: absolute; left: 0; right: 0; top: 1580px; display: flex; justify-content: center; }
    #s32-btn span { height: 110px; padding: 0 60px; border-radius: 55px; background: var(--red); color: #fff; font-family: var(--font-ar); font-weight: 900; font-size: 48px;
      display: flex; align-items: center; white-space: nowrap; box-shadow: 0 20px 50px rgba(217,58,43,.4); }
""", f"""
      {flap("s32-a", 250, "AI NEWS", 120, "")}
      {line("s32-h1", 420, "كل أسبوع · حلقة سريعة", "t-h2")}
      {line("s32-h2", 545, "ملخص الأخبار في دقايق", "t-h3", "color:var(--yellow)")}
      <div id="s32-h"><img src="assets/images/hossam_suit.png" /></div>
      <div id="s32-nm"><span style="display:inline-block; padding:6px 40px; border-radius:30px; background:rgba(4,22,20,.85); font-size:64px; font-weight:900">حسام الدين حسن</span></div>
      <div id="s32-btn"><span id="s32-b">تابعني</span></div>
""", """
      window.HF_FLAP(fx, "#s32-a", 185.9, { st: 0.05 });
      fx.maskUp("#s32-h1", 186.3);
      fx.maskUp("#s32-h2", 187.9);
      tl.fromTo("#s32-h", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, 186.6);
      fx.rise("#s32-nm", 188.8, { y: 20 });
      fx.pop("#s32-btn", 189.4, { from: 0.4 });
      tl.to("#s32-b", { scale: 0.92, duration: 0.08, yoyo: true, repeat: 1 }, 190.6);
      tl.to("#s32-b", { background: "#2b2a28", duration: 0.1 }, 190.75);
""", blob=("#136052", 540, 1100), exit=False)
cue(185.9, "typing", 0.5); cue(186.6, "whoosh-short", 0.5); cue(189.4, "pop", 0.55); cue(190.6, "click", 0.7)

CUES.sort(key=lambda c: c["t"])
# thin the mix: drop a soft SFX that lands < 0.35 s after the previous kept one (keeps the root file small too)
kept, last = [CUES[0]], -9
for c in CUES[1:]:
    if c["t"] - last < 0.35 and c["accent"] < 0.7:
        continue
    kept.append(c); last = c["t"]
CUES[:] = kept
(HERE / "cues.json").write_text(json.dumps(CUES, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"scenes {len(scenes)} · cues {len(CUES) - 1} · end {END}")
