# "برامج ذكاء اصطناعي بفلوس ازاي تاخدها ببلاش؟" — part 1 (9:16, dark). Times = GLOBAL seconds on assets/voice/voice.wav (133.17 s).
# Spine: "the price tag" — every tool arrives like a product with a monthly price tag.
# Signature move (new): the tag RIPS in two (jagged tear) and a lime $0 / ببلاش tag is underneath.
# Components from the library (build_lib.py, cod-8c330e). Re-run: python build_scenes.py (then motion_sync.py)
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from build_lib import Part, patch_root, spark, ic, label, head, hossam  # noqa: E402

P = Part(HERE)
patch_root(HERE, flashes=(6.2, 76.55))
make = P.make
OPUS_C = "#e8977c"


def src(id_, top, t):
    return f'<div id="{id_}" class="op-src" style="top:{top}px">{t}</div>'


def pill(id_, x, y, text, color, fs=30):
    return (f'<div id="{id_}" class="abs" style="left:{x}px; top:{y}px; height:64px; padding:0 28px; border-radius:32px; display:flex; '
            f'align-items:center; border:3px solid {color}; color:{color}; background:rgba(4,22,20,.75); font-family:var(--font-en); '
            f'font-weight:900; font-size:{fs}px; letter-spacing:.08em; white-space:nowrap; direction:ltr">{text}</div>')


TAG_CSS = """
    .tg { position: absolute; }
    .tg .str { position: absolute; left: 50%; top: -90px; width: 4px; height: 100px; margin-left: -2px; background: rgba(246,248,240,.5); }
    .tg .lay { position: absolute; inset: 0; border-radius: 28px 28px 28px 28px; display: flex; flex-direction: column; align-items: center; justify-content: center;
      font-family: var(--font-en); font-weight: 900; direction: ltr; white-space: nowrap; }
    .tg .lay::before { content: ""; position: absolute; left: 50%; top: 22px; width: 30px; height: 30px; margin-left: -15px; border-radius: 50%; background: var(--bg); }
    .tg .under { background: var(--lime); color: var(--ink); }
    .tg .top { background: #f3efe2; color: #8c3a22; box-shadow: 0 18px 40px rgba(0,0,0,.4); }
    .tg .ta { clip-path: polygon(0 0, 52% 0, 46% 18%, 55% 34%, 45% 52%, 54% 70%, 47% 86%, 52% 100%, 0 100%); }
    .tg .tb { clip-path: polygon(52% 0, 100% 0, 100% 100%, 52% 100%, 47% 86%, 54% 70%, 45% 52%, 55% 34%, 46% 18%); }
"""


QR_CSS = """
    .qr { position: absolute; background: #fff; border-radius: 22px; padding: 12px; box-shadow: 0 20px 40px rgba(0,0,0,.45); }
    .qr img { display: block; width: 100%; height: 100%; }
    .qr-l { position: absolute; left: -40px; right: -40px; bottom: -46px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 22px;
      letter-spacing: .14em; color: var(--fg); direction: ltr; white-space: nowrap; }
"""


def tag(id_, x, y, w, h, top_html, under_html, rot=0):
    """Price tag: torn top layer (two halves) over a lime $0 layer (layers overlap by design)."""
    top_html = top_html.replace("<span", "<span data-layout-allow-overlap")
    under_html = under_html.replace("<span", "<span data-layout-allow-overlap")
    return (f'<div id="{id_}" class="tg" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px; transform-origin:50% -90px" data-layout-allow-overlap>'
            f'<div class="str"></div><div class="lay under" data-layout-allow-overlap style="font-size:{h // 3}px">{under_html}</div>'
            f'<div id="{id_}-a" class="lay top ta" data-layout-allow-overlap style="font-size:{h // 4}px">{top_html}</div>'
            f'<div id="{id_}-b" class="lay top tb" data-layout-allow-overlap style="font-size:{h // 4}px">{top_html}</div></div>')


def rip_js(id_, t, shake_sel=None):
    """SIGNATURE: tear the tag in two halves that fall away, the $0 layer pops."""
    js = (f'tl.to("#{id_}-a", {{ x: -260, y: 520, rotation: -38, opacity: 0, duration: 0.7, ease: "power2.in" }}, {t});\n'
          f'      tl.to("#{id_}-b", {{ x: 260, y: 560, rotation: 42, opacity: 0, duration: 0.7, ease: "power2.in" }}, {t});\n'
          f'      tl.fromTo("#{id_}", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }}, {t + 0.05:.2f});')
    if shake_sel:
        js += f'\n      fx.shake("{shake_sel}", {t + 0.05:.2f}, 10, 6);'
    return js


def num_badge(id_, x, y, n):
    return (f'<div id="{id_}" class="abs" style="left:{x}px; top:{y}px; width:150px; height:150px; border-radius:50%; background:var(--yellow); color:var(--ink); '
            f'display:flex; align-items:center; justify-content:center; font-family:var(--font-en); font-weight:900; font-size:72px">{n}</div>')


def shot(id_, x, y, w, h, img, img_w=None, img_top=0):
    iw = img_w or w
    return (f'<div id="{id_}" class="op-shot" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px">'
            f'<img id="{id_}-i" src="{img}" style="width:{iw}px; top:{img_top}px" /></div>')


# ---------------------------------------------------------------- s1 hook: monthly tags pile up -> all $0
TAGS = [(90, 560, -8), (400, 510, 5), (720, 580, -4), (240, 880, 7), (580, 900, -6)]
make("s1", TAG_CSS + """
    #s1-q { left: 0; right: 0; top: 260px; }
""", "".join(tag(f"s1-t{k}", x, y, 260, 200, '$$$<span style="font-size:22px; letter-spacing:.12em">/ MONTH</span>', "$0", r)
             for k, (x, y, r) in enumerate(TAGS)) + f"""
      <div class="row t-h2" style="top:260px; white-space:nowrap"><span class="mask"><span class="in" id="s1-a1">تصدق أو لا تصدق؟</span></span></div>
      <div class="row t-h3" style="top:1220px"><span class="mask"><span class="in" id="s1-b1">برامج الذكاء الاصطناعي</span></span></div>
      <div class="row t-h3" style="top:1320px"><span class="mask"><span class="in" id="s1-c1">اللي بندفع فيها كل شهر</span></span></div>
      <div class="row t-h1 op-l" style="top:1460px"><span class="mask"><span class="in" id="s1-d1">ببلاش تمامًا</span></span></div>
""", "\n      ".join([
    'fx.punch("#s1-cam", 0, 1.15);',
    'fx.maskUp("#s1-a1", 0.0);',
    *[f'tl.fromTo("#s1-t{k}", {{ opacity: 0, y: -700, rotation: {r * 3} }}, {{ opacity: 1, y: 0, rotation: {r}, duration: 0.55, ease: "bounce.out" }}, {3.7 + k * 0.28:.2f});'
      for k, (_, _, r) in enumerate(TAGS)],
    'fx.maskUp("#s1-b1", 2.3);', 'fx.maskUp("#s1-c1", 3.75);',
    *[rip_js(f"s1-t{k}", round(6.2 + k * 0.08, 2)) for k in range(len(TAGS))],
    'fx.shake("#s1-cam", 6.25, 12, 6);',
    'fx.maskUp("#s1-d1", 6.15);',
]), blob=("#136052", 540, 800))

# ---------------------------------------------------------------- s2 PART 1 · 3 tools; 01 Whacka
make("s2", """
    .s2-st { position: absolute; top: 640px; width: 220px; height: 220px; border-radius: 40px; border: 4px dashed rgba(179,206,101,.5);
      display: flex; align-items: center; justify-content: center; font-family: var(--font-en); font-weight: 900; font-size: 90px; color: var(--fg-muted); }
    #s2-n1 { left: 760px; } #s2-n2 { left: 430px; } #s2-n3 { left: 100px; }
    #s2-nm { left: 0; right: 0; top: 1300px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 170px; color: var(--fg); direction: ltr; }
""", f"""
      {label("s2-lab", 300, "FREE AI TOOLS · PART 1")}
      {head("s2-a", 350, ["أدوات AI ببلاش"], "t-h2")}
      <div id="s2-n1" class="s2-st">01</div><div id="s2-n2" class="s2-st">02</div><div id="s2-n3" class="s2-st">03</div>
      {head("s2-b", 1000, ["والأولى معانا اسمها"], "t-h3")}
      <div id="s2-nm" class="abs">Whacka</div>
""", """
      fx.rise("#s2-lab", 7.5, { y: 16 });
      fx.maskUp("#s2-a1", 9.0);
      fx.pop("#s2-n1", 7.9); fx.pop("#s2-n2", 8.05); fx.pop("#s2-n3", 8.2);
      tl.to("#s2-n1", { borderStyle: "solid", borderColor: "#ffec5c", background: "#ffec5c", color: "#0d0d0d", scale: 1.12, duration: 0.3, ease: "back.out(2)" }, 10.7);
      fx.maskUp("#s2-b1", 10.7);
      fx.letterDrop("#s2-nm", 12.1, { st: 0.05 });
""", blob=("#0f4f44", 540, 900))

# ---------------------------------------------------------------- s3 idea -> app (REAL: Hossam builds PotionPop in Whacka); 8 credits/day
make("s3", QR_CSS + """
    #s3-ph { left: 330px; top: 470px; width: 420px; height: 760px; }
    #s3-v { position: absolute; left: 0; top: 0; width: 388px; height: 776px; }
    #s3-bulb { left: 110px; top: 560px; width: 150px; height: 150px; color: var(--yellow); }
    #s3-c { left: 0; right: 0; top: 1290px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 150px; color: var(--yellow); direction: ltr; }
    #s3-src { top: 1530px; }
    .s3-coin { position: absolute; width: 80px; height: 80px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fff59a, #e6c63a); border: 4px solid #b89a1e;
      display: flex; align-items: center; justify-content: center; font-family: var(--font-en); font-weight: 900; font-size: 34px; color: #6b5400; }
""", f"""
      {label("s3-lab", 300, "01 · WHACKA · AI APP BUILDER")}
      {head("s3-a", 340, ["فكرة تطبيق؟"], "t-h2")}
      <svg id="s3-bulb" class="abs"><use href="#i-bulb" /></svg>
      <div id="s3-ph" class="op-phone"><div class="scr"><img src="assets/images/whacka_hero.png" />
        <video id="s3-v" src="assets/videos/whacka_build.mp4" data-start="1.65" data-duration="7.1" data-media-start="0" data-hf-media-start-basis="local" muted playsinline></video></div></div>
      {"".join(f'<div id="s3-k{k}" class="s3-coin" style="left:{820 + (k % 2) * 60}px; top:{620 + k * 70}px">C</div>' for k in range(6))}
      <div id="s3-c" class="abs"><span id="s3-cn">8</span> <span style="font-size:70px">CREDITS / DAY</span></div>
      {src("s3-src", 1530, "REAL · HOSSAM'S WHACKA BUILD · WHACKA.APP/PRICING")}
""", """
      fx.rise("#s3-lab", 12.8, { y: 16 });
      fx.maskUp("#s3-a1", 13.3);
      fx.pop("#s3-bulb", 13.6, { from: 0.3 }); fx.breathe("#s3-bulb", 13.9, 2.5, 0.08, 0.8);
      tl.fromTo("#s3-ph", { opacity: 0, y: 300, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.55, ease: "power3.out" }, 14.4);
      tl.to("#s3-bulb", { x: 260, y: 160, scale: 0.3, opacity: 0, duration: 0.5, ease: "power3.in" }, 15.3);
      for (let k = 0; k < 6; k++) tl.fromTo("#s3-k" + k, { opacity: 0, y: -500, rotation: 0 }, { opacity: 1, y: 0, rotation: 360, duration: 0.5, ease: "bounce.out" }, 16.5 + k * 0.12);
      fx.counter("#s3-cn", 16.7, 17.3, 0, 8, { ar: false });
      fx.rise("#s3-src", 17.5, { y: 10, b: 0 });
      for (let k = 0; k < 6; k++) tl.to("#s3-k" + k, { y: -20, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }, 19.85 + k * 0.06);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s4 build 1, 2, 3 apps; publish free (REAL "You're live", live through Oct 1) — SIGNATURE rip + Whacka QR
make("s4", TAG_CSS + QR_CSS + """
    .s4-app { position: absolute; top: 520px; width: 240px; height: 240px; border-radius: 56px; display: flex; align-items: center; justify-content: center;
      font-family: var(--font-en); font-weight: 900; font-size: 110px; color: var(--ink); box-shadow: 0 20px 40px rgba(0,0,0,.4); }
    #s4-p1 { left: 760px; background: var(--lime); } #s4-p2 { left: 420px; background: var(--yellow); } #s4-p3 { left: 80px; background: #e8977c; }
    .s4-cr { position: absolute; top: 790px; width: 240px; text-align: center; font-family: var(--font-en); font-weight: 800; font-size: 28px; color: var(--fg-muted); direction: ltr; }
    #s4-win { left: 60px; top: 900px; width: 620px; height: 605px; }
    #s4-v, #s4-still { position: absolute; left: 0; top: 0; width: 620px; height: 551px; }
    #s4-hl { left: 378px; top: 222px; width: 236px; height: 34px; border-radius: 8px; border: 5px solid var(--yellow); }
    #s4-src { top: 1600px; }
""", f"""
      {label("s4-lab", 300, "ON THE FREE PLAN")}
      {head("s4-a", 340, ["تبني تطبيق و٢ و٣"], "t-h2")}
      <div id="s4-p1" class="s4-app">1</div><div id="s4-p2" class="s4-app">2</div><div id="s4-p3" class="s4-app">3</div>
      <div id="s4-c1" class="s4-cr" style="left:760px">~2 CREDITS</div><div id="s4-c2" class="s4-cr" style="left:420px">~2 CREDITS</div><div id="s4-c3" class="s4-cr" style="left:80px">~2 CREDITS</div>
      <div id="s4-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>whacka.app · PotionPop</b></div>
        <div class="body"><img id="s4-still" src="assets/images/whacka_live_still.png" />
        <video id="s4-v" src="assets/videos/whacka_live.mp4" data-start="6.8" data-duration="3.55" data-media-start="4.3" data-hf-media-start-basis="local" muted playsinline></video>
        <div id="s4-hl" class="abs"></div></div></div>
      {tag("s4-tg", 730, 960, 290, 220, 'PUBLISH<span style="font-size:28px">$ / MONTH</span>', 'ببلاش<span style="font-size:38px; font-family:var(--font-en)">14 DAYS</span>', -6)}
      <div id="s4-qr" class="qr" style="left:770px; top:1270px; width:210px; height:210px"><img src="assets/images/qr_whacka.png" /><div class="qr-l">WHACKA</div></div>
      {src("s4-src", 1600, "REAL · HOSSAM'S APP · LIVE SEP 17 → OCT 1")}
""", f"""
      fx.rise("#s4-lab", 21.5, {{ y: 16 }});
      fx.maskUp("#s4-a1", 23.6);
      fx.pop("#s4-p1", 23.9, {{ from: 0.2 }}); fx.pop("#s4-p2", 24.5, {{ from: 0.2 }}); fx.pop("#s4-p3", 24.75, {{ from: 0.2 }});
      fx.rise("#s4-c1, #s4-c2, #s4-c3", 26.9, {{ y: 16, st: 0.08 }});
      tl.fromTo("#s4-win", {{ opacity: 0, x: -300 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, 28.2);
      tl.fromTo("#s4-tg", {{ opacity: 0, y: -400, rotation: -30 }}, {{ opacity: 1, y: 0, rotation: -6, duration: 0.6, ease: "elastic.out(1, 0.5)" }}, 28.6);
      {rip_js("s4-tg", 29.8, "#s4-cam")}
      tl.fromTo("#s4-hl", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }}, 30.5);
      fx.pop("#s4-qr", 30.2, {{ from: 0.4 }});
      fx.rise("#s4-src", 28.8, {{ y: 10, b: 0 }});
""", blob=("#0f4f44", 540, 1000))
# whacka_live.mp4 (900x800) at 620 px (x0.689): the "Live through Oct 1 — publishing renews it" line sits at ~x 550..890, y 320..340

# ---------------------------------------------------------------- s5 02 SureThing AI -> Vibe Automation
make("s5", """
    #s5-ph { left: 300px; top: 560px; width: 480px; height: 860px; }
    #s5-win { left: 60px; top: 760px; width: 960px; height: 590px; }
    #s5-v { left: 0; top: 0; width: 960px; height: 540px; }
    #s5-src { top: 1460px; }
""", f"""
      {label("s5-lab", 300, "02 · SURETHING AI · I USE IT DAILY")}
      <div class="row op-en" style="top:350px; font-size:120px"><span class="mask"><span class="in" id="s5-a1">SureThing <span class="op-l">AI</span></span></span></div>
      {num_badge("s5-n", 860, 520, "02")}
      <div id="s5-ph" class="op-phone"><div class="scr"><img src="assets/images/surething_hero.png" /></div></div>
      <div id="s5-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>MY VIBE AUTOMATION INTRO</b></div>
        <div class="body"><video id="s5-v" src="assets/videos/vibe_intro.mp4" data-start="6.4" data-duration="2.65" data-media-start="40" data-hf-media-start-basis="local" muted playsinline></video></div></div>
      {src("s5-src", 1460, "REAL · SURETHING.IO")}
""", """
      fx.rise("#s5-lab", 31.6, { y: 16 });
      fx.maskUp("#s5-a1", 34.6);
      fx.pop("#s5-n", 31.75, { from: 2, e: "expo.out", d: 0.3 });
      tl.fromTo("#s5-ph", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 34.7);
      fx.rise("#s5-src", 35.0, { y: 10, b: 0 });
      tl.to("#s5-ph", { x: 0, y: 80, scale: 0.6, opacity: 0, duration: 0.4, ease: "power3.in" }, 37.9);
      tl.fromTo("#s5-win", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 38.0);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s6 talk -> team / system (REAL: SureThing agent builds the Podcast Command Center); cloud; free credits
make("s6", """
    #s6-win { left: 60px; top: 480px; width: 960px; height: 662px; }
    #s6-v { position: absolute; left: 0; top: 0; width: 960px; height: 608px; }
    #s6-kpi { left: 60px; top: 1170px; width: 960px; height: 220px; border-radius: 20px; overflow: hidden; box-shadow: 0 24px 50px rgba(0,0,0,.5); border: 3px solid var(--lime); }
    #s6-kpi img { position: absolute; right: 0; top: 0; width: 1490px; height: 220px; }
    #s6-kl { top: 1405px; }
    #s6-cl { left: 340px; top: 1480px; width: 260px; height: 100px; }
    #s6-cl2 { top: 1600px; }
""", f"""
      {label("s6-lab", 300, "VIBE AUTOMATION · SURETHING")}
      {head("s6-a", 340, ["بكلم الـــ<span class='lat'>AI</span>"], "t-h2")}
      <div id="s6-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>SureThing · Project Agent</b></div>
        <div class="body"><img class="abs" src="assets/images/sure_agent_end.png" style="left:0; top:0; width:960px; height:608px" />
        <video id="s6-v" src="assets/videos/sure_agent.mp4" data-start="0.2" data-duration="8.0" data-media-start="0" data-hf-media-start-basis="local" muted playsinline></video></div></div>
      <div id="s6-kpi" class="abs"><img src="assets/images/sure_kpi.png" /></div>
      {label("s6-kl", 1405, "THE RESULT · HOSSAM'S PODCAST GUEST COMMAND CENTER")}
      <svg id="s6-cl" class="abs" viewBox="0 -14 400 164" style="left:410px; top:1480px"><path d="M90 140 a60 60 0 0 1 10 -118 a80 80 0 0 1 150 -4 a62 62 0 0 1 60 122 z" fill="rgba(179,206,101,.18)" stroke="var(--lime)" stroke-width="6"/></svg>
      {label("s6-cl2", 1600, "RUNS IN THE CLOUD · WITHOUT ME")}
      <div class="row t-h3 op-y" style="top:1670px"><span class="mask"><span class="in" id="s6-b1">وبيديني credits مجانية</span></span></div>
""", """
      fx.rise("#s6-lab", 40.25, { y: 16 });
      tl.fromTo("#s6-win", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 40.3);
      fx.maskUp("#s6-a1", 46.4);
      tl.fromTo("#s6-kpi", { opacity: 0, y: 120, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.5)" }, 45.5);
      fx.rise("#s6-kl", 45.8, { y: 10, b: 0 });
      fx.pop("#s6-cl", 49.4, { from: 0.4 });
      fx.rise("#s6-cl2", 49.9, { y: 14 });
      fx.maskUp("#s6-b1", 52.0);
""", blob=("#0f4f44", 540, 960))

# ---------------------------------------------------------------- s7 +500 credits (REAL "Share SureThing · Each get 500 credits") + SureThing QR; paid plan free (rip); more credits
make("s7", TAG_CSS + QR_CSS + """
    #s7-code { left: 120px; top: 500px; width: 840px; height: 340px; border-radius: 34px; background: #f6f4ea; color: var(--ink); }
    #s7-qr { left: 30px; top: 30px; width: 280px; height: 280px; }
    #s7-cv { position: absolute; right: 50px; top: 60px; font-family: var(--font-en); font-weight: 900; font-size: 120px; color: #437F3E; direction: ltr; }
    #s7-cl { position: absolute; right: 50px; top: 210px; font-family: var(--font-en); font-weight: 800; font-size: 30px; letter-spacing: .1em; color: #6d6a5d; direction: ltr; }
    #s7-sh { left: 190px; top: 880px; width: 700px; height: 150px; border-radius: 22px; overflow: hidden; border: 3px solid var(--lime); }
    #s7-sh img { width: 700px; height: 150px; }
    #s7-shl { top: 1045px; }
""", f"""
      {label("s7-lab", 300, "02 · SURETHING AI · FREE CREDITS")}
      {head("s7-a", 340, ["استخدم الكود ده"], "t-h2")}
      <div id="s7-code" class="abs"><div id="s7-qr" class="qr" style="position:absolute"><img src="assets/images/qr_surething.png" /></div>
        <div id="s7-cv">+<span id="s7-cn">500</span></div><div id="s7-cl">CREDITS · SURETHING</div></div>
      <div id="s7-sh" class="abs"><img src="assets/images/sure_share.png" /></div>
      {src("s7-shl", 1045, "REAL · SURETHING APP · INVITE BONUS")}
      {tag("s7-tg", 340, 1130, 400, 290, 'PAID PLAN<span style="font-size:30px">$ / MONTH</span>', 'ببلاش', 4)}
      <div class="row t-h3" style="top:1530px"><span class="mask"><span class="in" id="s7-b1">وكل ما تدخل أكتر</span></span></div>
      <div class="row t-h2 op-y" style="top:1620px"><span class="mask"><span class="in" id="s7-c1"><span class="lat">credits</span> زيادة</span></span></div>
""", f"""
      fx.rise("#s7-lab", 53.45, {{ y: 16 }});
      fx.maskUp("#s7-a1", 54.0);
      tl.fromTo("#s7-code", {{ opacity: 0, y: 200, rotation: -3 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "back.out(1.5)" }}, 54.3);
      fx.counter("#s7-cn", 54.9, 55.45, 0, 500, {{ ar: false }});
      tl.fromTo("#s7-sh", {{ opacity: 0, x: 300 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, 55.7);
      fx.rise("#s7-shl", 56.0, {{ y: 10, b: 0 }});
      tl.fromTo("#s7-tg", {{ opacity: 0, y: -500, rotation: 30 }}, {{ opacity: 1, y: 0, rotation: 4, duration: 0.6, ease: "elastic.out(1, 0.5)" }}, 60.6);
      {rip_js("s7-tg", 62.65, "#s7-cam")}
      fx.maskUp("#s7-b1", 63.95);
      fx.maskUp("#s7-c1", 66.3);
""", blob=("#136052", 540, 1000))

# ---------------------------------------------------------------- s8 best deal: free + strong + Opus 5.5
make("s8", """
    #s8-st { left: 230px; top: 470px; font-size: 96px; border-color: var(--yellow); color: var(--yellow); }
    #s8-ck { left: 0; right: 0; top: 760px; display: flex; justify-content: center; gap: 26px; direction: rtl; }
    #s8-op { left: 0; right: 0; top: 1240px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 110px; color: #e8977c; direction: ltr; }
    #s8-weak { left: 330px; top: 1480px; }
    #s8-x { position: absolute; left: 300px; top: 1500px; width: 480px; height: 8px; background: var(--orange); transform-origin: 0 50%; }
""", f"""
      <div id="s8-st" class="stamp">أفضل <span class="lat">deal</span></div>
      <div id="s8-ck" class="abs"><div class="pill on" id="s8-c1" style="font-size:46px">{ic("check", 44, "var(--ink)")} مجاني</div><div class="pill on" id="s8-c2" style="font-size:46px">{ic("check", 44, "var(--ink)")} قوي جدًا</div></div>
      {spark("s8-sp", 430, 930, 220)}
      <div id="s8-op" class="abs">Opus 5.5</div>
      {pill("s8-weak", 330, 1470, "WEAK MODEL", "var(--fg-muted)", 36)}<div id="s8-x"></div>
""", """
      fx.stamp("#s8-st", 68.7, "#s8-cam");
      fx.pop("#s8-c1", 70.8); fx.pop("#s8-c2", 71.35);
      fx.pop("#s8-sp", 72.6, { from: 0.2, e: "expo.out", d: 0.6 });
      tl.fromTo("#s8-sp-svg", { rotation: 0 }, { rotation: 140, duration: 4, ease: "power1.out" }, 72.6);
      fx.letterDrop("#s8-op", 73.1, { st: 0.04 });
      fx.rise("#s8-weak", 74.6, { y: 20 });
      tl.fromTo("#s8-x", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, 75.55);
      tl.to("#s8-weak", { opacity: 0.4, duration: 0.2 }, 75.6);
""", blob=("#0f4f44", 540, 1050))

# ---------------------------------------------------------------- s9 03 OpenRouter: real recording, 500+ models
# openrouter.mp4 1904x912: window shows x 380..1520 (1140 px) at 0.842 -> 960 px wide
make("s9", """
    #s9-win { left: 60px; top: 760px; width: 960px; height: 590px; }
    #s9-v { left: -320px; top: -80px; width: 1603px; height: 768px; }
    #s9-c { left: 0; right: 0; top: 1400px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 150px; color: var(--yellow); direction: ltr; }
    #s9-src { top: 1600px; }
""", f"""
      {label("s9-lab", 300, "03 · OPENROUTER")}
      {head("s9-a", 340, ["تختار الموديل اللي يناسبك"], "t-h3")}
      {num_badge("s9-n", 465, 470, "03")}
      <div class="row op-en" style="top:620px; font-size:100px"><span class="mask"><span class="in" id="s9-b1">OpenRouter</span></span></div>
      <div id="s9-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>openrouter.ai</b></div>
        <div class="body"><img class="abs" src="assets/images/or_home.png" style="left:-320px; top:-80px; width:1603px; height:768px" />
        <video id="s9-v" src="assets/videos/openrouter.mp4" data-start="6.5" data-duration="3.0" data-media-start="5.8" data-hf-media-start-basis="local" muted playsinline></video></div></div>
      <div id="s9-c" class="abs"><span id="s9-cn">500</span>+ <span style="font-size:60px">MODELS</span></div>
      {src("s9-src", 1600, "REAL SCREEN · OPENROUTER.AI · 500+ MODELS · 80+ PROVIDERS")}
""", """
      fx.rise("#s9-lab", 76.6, { y: 16 });
      fx.pop("#s9-n", 77.1, { from: 2, e: "expo.out", d: 0.3 });
      fx.maskUp("#s9-a1", 79.4);
      tl.to("#s9-n", { y: -60, scale: 0.6, opacity: 0, duration: 0.3, ease: "power2.in" }, 83.4);
      fx.maskUp("#s9-b1", 83.6);
      tl.fromTo("#s9-win", { opacity: 0, y: 260 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 83.0);
      fx.counter("#s9-cn", 85.4, 86.4, 0, 500, { ar: false });
      fx.rise("#s9-src", 85.6, { y: 10, b: 0 });
""", blob=("#136052", 540, 1000))

# ---------------------------------------------------------------- s10 search "free": real list at $0/M
make("s10", QR_CSS + """
    #s10-win { left: 60px; top: 520px; width: 960px; height: 520px; }
    #s10-v { left: -120px; top: -60px; width: 1400px; height: 671px; }
    #s10-ph { left: 250px; top: 1060px; width: 580px; height: 640px; }
    #s10-ph img { top: -40px; }
    #s10-z { left: 0; right: 0; top: 1720px; display: flex; justify-content: center; gap: 20px; }
""", f"""
      <div class="row t-h3" style="top:300px"><span class="mask"><span class="in" id="s10-a1">اعمل <span class="lat">search</span> على</span></span></div>
      <div class="row op-en op-l" style="top:380px; font-size:110px"><span class="mask"><span class="in" id="s10-b1">“free”</span></span></div>
      <div id="s10-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>openrouter.ai/models?q=free</b></div>
        <div class="body"><img class="abs" src="assets/images/or_list.png" style="left:-120px; top:-60px; width:1400px; height:671px" />
        <video id="s10-v" src="assets/videos/openrouter.mp4" data-start="0.4" data-duration="6.6" data-media-start="18.4" data-hf-media-start-basis="local" muted playsinline></video></div></div>
      <div id="s10-qr" class="qr" style="left:850px; top:1290px; width:190px; height:190px"><img src="assets/images/qr_openrouter.png" /><div class="qr-l">OPENROUTER</div></div>
      <div id="s10-ph" class="op-phone"><div class="scr"><img id="s10-img" src="assets/images/openrouter_free_list.png" /></div></div>
      <div id="s10-z" class="abs">{pill("s10-z1", 0, 0, "$0/M INPUT", "var(--lime)").replace('class="abs" ', '').replace("left:0px; top:0px; ", "position:relative; ")}{pill("s10-z2", 0, 0, "$0/M OUTPUT", "var(--lime)").replace('class="abs" ', '').replace("left:0px; top:0px; ", "position:relative; ")}</div>
""", """
      fx.maskUp("#s10-a1", 88.2);
      fx.maskUp("#s10-b1", 89.4);
      tl.fromTo("#s10-win", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 88.0);
      tl.fromTo("#s10-ph", { opacity: 0, y: 400 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 90.5);
      tl.fromTo("#s10-img", { y: 0 }, { y: -420, duration: 7.5, ease: "power1.inOut" }, 91.2);
      fx.pop("#s10-z1", 91.4); fx.pop("#s10-z2", 91.6);
      fx.pop("#s10-qr", 92.2, { from: 0.4 });
""", blob=("#0f4f44", 540, 1100), push=1.02)

# ---------------------------------------------------------------- s11 OpenCode: a coding agent, switch free models
MODELS = ["Nemotron 3 Ultra (free)", "Laguna S 2.1 (free)", "Ling 3.0 Flash Sante (free)"]
make("s11", """
    #s11-term { left: 90px; top: 560px; width: 900px; height: 560px; border-radius: 30px; background: #0a0f0e; border: 3px solid rgba(179,206,101,.4); overflow: hidden; }
    #s11-term .ln { position: absolute; left: 40px; right: 40px; font-family: "Courier New", monospace; font-weight: 700; font-size: 34px; color: #cfe08f; direction: ltr; white-space: nowrap; }
    #s11-slot { position: absolute; left: 40px; top: 300px; width: 820px; height: 100px; border-radius: 22px; border: 4px solid var(--lime); overflow: hidden; }
    .s11-m { position: absolute; left: 0; right: 0; top: 0; height: 100px; display: flex; align-items: center; justify-content: center; font-family: var(--font-en); font-weight: 900; font-size: 40px; color: var(--fg); direction: ltr; white-space: nowrap; }
""", f"""
      {label("s11-lab", 300, "PLUG IT INTO OPENCODE")}
      <div class="row t-h2" style="top:350px"><span class="mask"><span class="in" id="s11-a1"><span class="lat">coding agent</span> ببلاش</span></span></div>
      <div id="s11-term" class="abs"><div class="ln" style="top:40px; color:#8cb2a6">$ opencode</div>
        <div class="ln" id="s11-t2" style="top:120px">● provider: OpenRouter</div><div class="ln" id="s11-t3" style="top:190px">● model:</div>
        <div id="s11-slot">{"".join(f'<div id="s11-m{k}" class="s11-m">{m}</div>' for k, m in enumerate(MODELS))}</div></div>
      <div class="row t-h3" style="top:1220px"><span class="mask"><span class="in" id="s11-b1">وتبدّل بين الموديلز زي ما إنت حابب</span></span></div>
      {src("s11-src", 1330, "REAL FREE MODELS · SETUP ILLUSTRATED")}
""", """
      fx.rise("#s11-lab", 99.0, { y: 16 });
      tl.fromTo("#s11-term", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 101.3);
      fx.rise("#s11-t2", 101.9, { y: 10, b: 0 }); fx.rise("#s11-t3", 102.3, { y: 10, b: 0 });
      fx.maskUp("#s11-a1", 103.6);
      fx.hide("#s11-m1"); fx.hide("#s11-m2");
      fx.rise("#s11-m0", 103.9, { y: 60, b: 0 });
      tl.to("#s11-m0", { y: -100, opacity: 0, duration: 0.25, ease: "power2.in" }, 105.95);
      tl.fromTo("#s11-m1", { opacity: 1, y: 100 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out", immediateRender: false }, 106.0);
      tl.to("#s11-m1", { y: -100, opacity: 0, duration: 0.25, ease: "power2.in" }, 106.75);
      tl.fromTo("#s11-m2", { opacity: 1, y: 100 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out", immediateRender: false }, 106.8);
      fx.maskUp("#s11-b1", 106.0);
      fx.rise("#s11-src", 102.0, { y: 10, b: 0 });
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s12 caution: compressed models
make("s12", """
    #s12-tape { left: -60px; top: 470px; width: 1200px; height: 90px; background: repeating-linear-gradient(-45deg, #ffec5c 0 50px, #0d0d0d 50px 100px); transform-origin: 50% 50%; }
    #s12-tx { left: 0; right: 0; top: 489px; text-align: center; }
    #s12-tx span { background: #0d0d0d; color: var(--yellow); font-family: var(--font-en); font-weight: 900; font-size: 40px; letter-spacing: .2em; padding: 6px 26px; }
    #s12-box { left: 340px; top: 720px; width: 400px; height: 400px; border-radius: 40px; background: #0b2f29; border: 5px solid var(--lime); display: flex; align-items: center; justify-content: center; }
    #s12-tr { left: 190px; top: 1260px; width: 700px; }
    #s12-tl { top: 1200px; }
""", f"""
      <div id="s12-tape" class="abs"></div><div id="s12-tx" class="abs"><span>CAUTION</span></div>
      <div id="s12-box" class="abs">{spark("s12-sp", 100, 100, 200, bloom=False)}</div>
      {label("s12-tl", 1200, "QUALITY")}
      <div id="s12-tr" class="op-track"><div id="s12-f" class="op-fill" style="background:var(--lime)"></div></div>
      <div class="row t-h3" style="top:1380px"><span class="mask"><span class="in" id="s12-a1">بعض الموديلز مضغوطة</span></span></div>
      <div class="row t-h3 op-o" style="top:1480px"><span class="mask"><span class="in" id="s12-b1">مش هتديك الكفاءة الكاملة</span></span></div>
""", """
      tl.fromTo("#s12-tape", { scaleX: 0, rotation: -4 }, { scaleX: 1, rotation: -4, duration: 0.35, ease: "power3.out" }, 107.6);
      tl.fromTo("#s12-tx", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 107.8);
      tl.to("#s12-tx", { rotation: -4, duration: 0.01 }, 107.8);
      fx.pop("#s12-box", 108.0, { from: 0.4 });
      fx.rise("#s12-tl, #s12-tr", 108.4, { y: 20 });
      fx.meter("#s12-f", 108.5, 0.4, 1, { e: "power2.out" });
      tl.to("#s12-box", { scaleY: 0.55, scaleX: 1.2, duration: 0.35, ease: "power3.in" }, 109.9);
      fx.maskUp("#s12-a1", 109.0);
      tl.to("#s12-f", { scaleX: 0.6, background: "#ff5a33", duration: 0.5, ease: "power3.inOut" }, 110.5);
      fx.maskUp("#s12-b1", 110.6);
""", blob=("#0f4f44", 540, 900))

# ---------------------------------------------------------------- s13 part 1 done, part 2 soon
make("s13", TAG_CSS + """
    .s13-c { position: absolute; top: 560px; width: 400px; height: 520px; border-radius: 34px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px;
      font-family: var(--font-en); font-weight: 900; direction: ltr; }
    #s13-p1 { left: 600px; background: #0b2f29; border: 4px solid var(--lime); color: var(--lime); }
    #s13-p2 { left: 80px; background: repeating-linear-gradient(45deg, #0b332c 0 18px, #0d3a32 18px 36px); border: 4px dashed rgba(179,206,101,.5); color: var(--fg-muted); }
""", f"""
      {label("s13-lab", 300, "THE SERIES")}
      <div id="s13-p1" class="s13-c"><span style="font-size:44px">PART 1</span><span id="s13-ok" style="width:140px; height:140px; border-radius:50%; background:var(--lime); display:flex; align-items:center; justify-content:center">{ic("check", 90, "var(--ink)")}</span><span style="font-size:30px">3 TOOLS</span></div>
      <div id="s13-p2" class="s13-c"><span style="font-size:44px">PART 2</span>{ic("lock", 110, "rgba(179,206,101,.6)")}<span style="font-size:30px">MORE FREE TOOLS</span></div>
      {tag("s13-tg", 390, 1160, 300, 220, 'SUBSCRIPTIONS<span style="font-size:24px">$$$ / MONTH</span>', '$0', -5)}
      <div class="row t-h3" style="top:1500px"><span class="mask"><span class="in" id="s13-a1">بدل ما تدفع اشتراكات</span></span></div>
""", f"""
      fx.rise("#s13-lab", 112.0, {{ y: 16 }});
      tl.fromTo("#s13-p1", {{ opacity: 0, y: 200 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 112.3);
      fx.pop("#s13-ok", 112.9, {{ from: 0.2 }});
      tl.fromTo("#s13-p2", {{ opacity: 0, y: 200 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 113.5);
      tl.to("#s13-p2", {{ rotation: -3, duration: 0.15, yoyo: true, repeat: 3, ease: "sine.inOut" }}, 114.4);
      tl.fromTo("#s13-tg", {{ opacity: 0, y: -400 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "elastic.out(1, 0.5)" }}, 116.4);
      fx.maskUp("#s13-a1", 116.75);
      {rip_js("s13-tg", 117.4, "#s13-cam")}
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s14 CTA: Hossam, subscribe + bell, comments, the three tool QRs
QRS = [("whacka", "WHACKA"), ("surething", "SURETHING"), ("openrouter", "OPENROUTER")]
make("s14", QR_CSS + """
    #s14-sub { left: 300px; top: 1660px; }
    #s14-bell { left: 700px; top: 1666px; width: 92px; height: 92px; border-radius: 50%; background: var(--yellow); display: flex; align-items: center; justify-content: center; color: var(--ink); }
    #s14-cm { left: 60px; top: 1390px; width: 440px; height: 110px; border-radius: 30px; background: #f6f4ea; color: var(--ink); display: flex; align-items: center; gap: 18px; padding: 0 26px;
      font-family: var(--font-ar); font-weight: 800; font-size: 36px; direction: rtl; }
    #s14-ql { top: 760px; }
    #s14-nm { top: 1530px; }
""", f"""
      <div class="row t-h3" style="top:320px"><span class="mask"><span class="in" id="s14-a1">كل جديد في عالم الذكاء الاصطناعي</span></span></div>
      {hossam("s14-ho", 240, 800, 600)}
      {"".join(f'<div id="s14-q{k}" class="qr" style="left:{790 - k * 350}px; top:470px; width:220px; height:220px"><img src="assets/images/qr_{q}.png" /><div class="qr-l">{n}</div></div>' for k, (q, n) in enumerate(QRS))}
      {src("s14-ql", 760, "SCAN FOR THE LINKS")}
      <div id="s14-cm" class="abs">{ic("chat", 52, "#136052")} اكتبلي أسئلتك</div>
      <div id="s14-nm" class="op-name t-h2" style="top:1530px">حسام الدين حسن</div>
      <div id="s14-sub" class="op-btn">اشترك</div>
      <div id="s14-bell" class="abs">{ic("bell", 54, "var(--ink)")}</div>
""", """
      tl.fromTo("#s14-ho", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, 119.2);
      fx.rise("#s14-nm", 119.6, { y: 30 });
      fx.maskUp("#s14-a1", 120.5);
      fx.pop("#s14-sub", 123.1, { from: 0.4 });
      tl.to("#s14-sub", { background: "#2b2a28", color: "#b3ce65", duration: 0.15 }, 123.6);
      fx.pop("#s14-bell", 123.95, { from: 0.2 });
      tl.fromTo("#s14-bell", { rotation: 0 }, { rotation: 18, duration: 0.09, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false }, 124.2);
      tl.fromTo("#s14-cm", { opacity: 0, x: -300 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 125.0);
      fx.pop("#s14-q0", 127.5, { from: 0.4 }); fx.pop("#s14-q1", 127.7, { from: 0.4 }); fx.pop("#s14-q2", 127.9, { from: 0.4 });
      fx.rise("#s14-ql", 128.1, { y: 10, b: 0 });
      tl.to("#s14-cm", { scale: 1.06, duration: 0.2, yoyo: true, repeat: 1 }, 129.8);
""", blob=("#136052", 540, 1000))

# ---------------------------------------------------------------- s15 WATCH NEXT end card (after the voice)
make("s15", QR_CSS + """
    #s15-th { left: 90px; top: 520px; width: 900px; height: 506px; border-radius: 28px; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,.55); border: 4px solid var(--lime); }
    #s15-th img { width: 900px; height: 506px; }
    #s15-pl { left: 470px; top: 703px; width: 140px; height: 140px; border-radius: 50%; background: var(--red); display: flex; align-items: center; justify-content: center; }
    #s15-t { left: 90px; right: 90px; top: 1060px; text-align: center; font-family: var(--font-ar); font-weight: 800; font-size: 46px; line-height: 1.45; color: var(--fg); direction: rtl; }
    #s15-qr { left: 400px; top: 1300px; width: 280px; height: 280px; }
""", f"""
      {label("s15-lab", 300, "WATCH NEXT · FULL VIDEO")}
      {head("s15-a", 350, ["كمّل في الفيديو ده"], "t-h2")}
      <div id="s15-th" class="abs"><img src="assets/images/watch_next_thumb.jpg" /></div>
      <div id="s15-pl" class="abs">{ic("play", 70, "#fff")}</div>
      <div id="s15-t" class="abs" data-layout-allow-overlap>كنز في عالم الذكاء الاصطناعي محدش بيتكلم عنه — ٧ أدوات مجانية غيّرت شغلي</div>
      <div id="s15-qr" class="qr"><img src="assets/images/qr_watch_next.png" /><div class="qr-l">SCAN TO WATCH</div></div>
""", """
      fx.rise("#s15-lab", 132.6, { y: 16 });
      fx.maskUp("#s15-a1", 132.7);
      tl.fromTo("#s15-th", { opacity: 0, y: 200, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.4)" }, 132.8);
      fx.pop("#s15-pl", 133.3, { from: 0.3 });
      fx.rise("#s15-t", 133.4, { y: 30 });
      fx.pop("#s15-qr", 133.9, { from: 0.4 });
      tl.to("#s15-pl", { scale: 1.12, duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }, 134.6);
""", blob=("#136052", 540, 900), exit=False)

# ---------------------------------------------------------------- cues + chrome
cues = [c for c in json.loads((HERE / "cues.json").read_text(encoding="utf-8")) if c.get("voice")]
RIP = "library/whoosh-short"
S = [
    (0.0, "lib/title-slam", 0.7), *[(3.7 + k * 0.28, "library/pop", 0.45) for k in range(5)], (6.2, "lib/box-burst", 0.9), (6.25, RIP, 0.6),
    (7.5, "library/whoosh", 0.5), (7.9, "library/pop", 0.5), (10.7, "library/click", 0.8), (12.1, "lib/title-slam", 0.6),
    (12.8, "library/whoosh-short", 0.5), (13.6, "lib/spark-ignite", 0.6), (14.4, "library/whoosh-short", 0.5), (16.5, "library/sparkle", 0.6), (19.85, "library/chime", 0.4),
    (21.5, "library/whoosh", 0.5), (23.9, "library/pop", 0.6), (24.5, "library/pop", 0.6), (24.75, "library/pop", 0.6), (28.6, "lib/cartridge-click", 0.6), (29.8, "lib/box-burst", 1.0), (30.5, "library/ping", 0.5),
    (31.6, "library/whoosh", 0.5), (31.75, "lib/title-slam", 0.6), (34.6, "library/whoosh-short", 0.5), (38.0, "library/whoosh-short", 0.6),
    (40.4, "library/pop", 0.6), (41.8, "lib/core-powerup", 0.7), (43.6, "library/chime", 0.5), (49.4, "library/whoosh-short", 0.4), (52.0, "library/sparkle", 0.6),
    (53.45, "library/whoosh", 0.5), (54.3, "library/pop", 0.6), (54.9, "library/typing", 0.5), (60.6, "lib/cartridge-click", 0.6), (62.65, "lib/box-burst", 1.0), (66.3, "library/sparkle", 0.6),
    (68.7, "lib/tape-seal", 1.0), (70.8, "library/pop", 0.6), (71.35, "library/pop", 0.6), (72.6, "lib/spark-ignite", 0.8), (75.55, "library/error", 0.4),
    (76.6, "library/whoosh-cinematic", 0.5), (77.1, "lib/title-slam", 0.6), (83.0, "library/whoosh-short", 0.5), (85.4, "library/typing", 0.5),
    (88.0, "library/whoosh", 0.5), (89.4, "library/key-press", 0.8), (90.5, "library/whoosh-short", 0.5), (91.4, "library/pop", 0.5),
    (99.0, "library/whoosh", 0.5), (101.3, "library/typing", 0.6), (103.9, "library/click", 0.7), (105.95, "library/click-soft", 0.8), (106.75, "library/click-soft", 0.8),
    (107.6, "library/error", 0.5), (109.9, "library/glitch-1", 0.35), (110.5, "library/error", 0.35),
    (112.0, "library/whoosh", 0.5), (112.9, "library/chime", 0.6), (113.5, "library/whoosh-short", 0.4), (116.4, "lib/cartridge-click", 0.5), (117.4, "lib/box-burst", 0.9),
    (30.2, "library/pop", 0.6), (45.5, "library/pop", 0.6), (55.7, "library/whoosh-short", 0.5), (92.2, "library/pop", 0.6),
    (127.5, "library/pop", 0.5), (127.7, "library/pop", 0.5), (127.9, "library/pop", 0.5),
    (132.6, "library/whoosh", 0.6), (133.3, "library/pop", 0.6), (133.9, "library/chime", 0.6),
    (119.2, "library/whoosh-cinematic", 0.5), (123.1, "library/click", 1.0), (124.2, "library/notification", 0.7), (125.0, "library/whoosh-short", 0.5), (127.6, "library/pop", 0.6),
]
for t, s, acc in sorted(S):
    cues.append({"t": round(t, 2), "sfx": s, "accent": acc})
(HERE / "cues.json").write_text(json.dumps(cues, ensure_ascii=False, indent=1), encoding="utf-8")
(HERE / "chrome.json").write_text(json.dumps({
    "enabled": True, "series": "FREE AI · PART 1", "grain": False,
    "sections": [{"t": 0, "label": "THE HOOK"}, {"t": 7.45, "label": "01 · WHACKA"}, {"t": 31.55, "label": "02 · SURETHING"},
                 {"t": 76.55, "label": "03 · OPENROUTER"}, {"t": 107.5, "label": "CAUTION"}, {"t": 111.95, "label": "NEXT · PART 2"},
                 {"t": 119.1, "label": "SUBSCRIBE"}, {"t": 132.5, "label": "WATCH NEXT"}],
    "wipes": [7.35, 31.45, 76.45, 111.85]}, indent=1), encoding="utf-8")
print("built", len(P.scenes), "scenes,", len(cues) - 1, "sfx cues")
