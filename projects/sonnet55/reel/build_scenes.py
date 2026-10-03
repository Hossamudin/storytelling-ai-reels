# Claude Sonnet 5.5 reel (9:16, dark). Times = GLOBAL seconds on assets/voice/voice.wav (155.53 s edited voice).
# Spine: "the family scale" — Opus 5.5 (big spark) and its little brother Sonnet 5.5 weighed on a balance.
# Signature move (new): the sorting conveyor — task cards drop into a SONNET tray or an OPUS tray.
# Hero: a receipt printer prints the real price. Components come from the library (build_lib.py, cod-8c330e).
# Re-run after edits:  python build_scenes.py  (then motion_sync.py)
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from build_lib import Part, patch_root, spark, ic, label, head, chip, hossam, CLAUDE  # noqa: E402

P = Part(HERE)
patch_root(HERE, flashes=(49.3, 99.45))
make = P.make
SRC = '<div id="{id}" class="op-src" style="top:{top}px">{t}</div>'
OPUS_C = "#e8977c"


def src(id_, top, t):
    return SRC.format(id=id_, top=top, t=t)


def pill(id_, x, y, text, color, w=None):
    ww = f" width:{w}px; justify-content:center;" if w else ""
    return (f'<div id="{id_}" class="abs" style="left:{x}px; top:{y}px; height:64px; padding:0 28px; border-radius:32px; display:flex; '
            f'align-items:center;{ww} border:3px solid {color}; color:{color}; background:rgba(4,22,20,.75); font-family:var(--font-en); '
            f'font-weight:900; font-size:30px; letter-spacing:.08em; white-space:nowrap; direction:ltr">{text}</div>')


# ---------------------------------------------------------------- s1 hook: small spark beats Opus, half price
make("s1", """
    #s1-lab { top: 300px; }
    #s1-vs { left: 470px; top: 640px; width: 140px; height: 140px; border-radius: 50%; background: var(--yellow); color: var(--ink);
      font-family: var(--font-en); font-weight: 900; font-size: 54px; display: flex; align-items: center; justify-content: center; }
    #s1-cd { left: 380px; top: 1000px; }
    #s1-tag { left: 300px; top: 1500px; font-size: 92px; padding: 14px 54px; border-color: var(--yellow); color: var(--yellow); white-space: nowrap; }
""", f"""
      {label("s1-lab", 300, "ANTHROPIC · NEW MODEL")}
      {spark("s1-op", 600, 470, 400)}
      {pill("s1-opp", 690, 900, "OPUS 5.5", OPUS_C)}
      {spark("s1-so", 140, 560, 250)}
      {pill("s1-sop", 150, 860, "NEW · ???", "var(--lime)")}
      <div id="s1-vs" class="abs">VS</div>
      {chip("s1-cd", 380, 1000, "في الكودينج", "&lt;/&gt;")}
      {head("s1-a", 1150, ["موديل جديد بيكسب"], "t-h2")}
      <div class="row t-h1 op-en" style="top:1270px"><span class="mask"><span class="in op-c" id="s1-b1">Opus 5.5</span></span></div>
      <div id="s1-tag" class="stamp" data-layout-allow-overlap>بنُص السعر</div>
""", """
      fx.punch("#s1-cam", 0, 1.18);
      fx.rise("#s1-lab", 0.05, { y: 16 });
      fx.pop("#s1-op", 0.0, { from: 0.3, e: "expo.out", d: 0.8 });
      tl.fromTo("#s1-op-svg", { rotation: -60 }, { rotation: 30, duration: 5.4, ease: "power1.out" }, 0);
      fx.breathe("#s1-op-bl", 0.6, 4.4, 0.06, 1.4);
      fx.rise("#s1-opp", 0.4, { y: 20 });
      fx.pop("#s1-so", 1.1, { from: 0.2 });
      tl.fromTo("#s1-so-svg", { rotation: 0 }, { rotation: -160, duration: 4.3, ease: "power1.out" }, 1.1);
      fx.rise("#s1-sop", 1.3, { y: 20 });
      fx.maskUp("#s1-a1", 1.1);
      fx.pop("#s1-vs", 1.8, { from: 2.2, e: "expo.out", d: 0.3 });
      // the small spark wins: it grows, Opus recoils and greys
      tl.to("#s1-so", { scale: 1.3, x: 40, duration: 0.5, ease: "back.out(2)" }, 2.6);
      tl.to("#s1-op", { scale: 0.82, x: 40, filter: "grayscale(0.85) brightness(0.7)", duration: 0.5, ease: "power3.out" }, 2.6);
      fx.shake("#s1-op", 2.65, 10, 6);
      fx.maskUp("#s1-b1", 2.6);
      fx.pop("#s1-cd", 3.65, { from: 0.4 });
      fx.stamp("#s1-tag", 4.42, "#s1-cam");
""", blob=("#136052", 540, 700))

# ---------------------------------------------------------------- s2 two weeks ago: Opus built a 3D game; today: this video
CUBE_A = 64


def iso_cubes():
    """Isometric voxel level drawn as SVG (one <g> per cube, animated on the g)."""
    cells = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0),
             (0, 0, 1), (1, 0, 1), (0, 1, 1), (0, 0, 2), (2, 2, 1)]
    cols = {0: ("#437F3E", "#2f5d2c", "#B3CE65"), 1: ("#136052", "#0c4239", "#3f9a86"), 2: ("#c9693f", "#9c4c2b", "#D97757")}
    a, cx, cy = CUBE_A, 320, 250
    out = []
    order = sorted(range(len(cells)), key=lambda n: (cells[n][0] + cells[n][1], cells[n][2]))
    for k, n in enumerate(order):
        i, j, h = cells[n]
        x, y = cx + (i - j) * a, cy + (i + j) * a / 2 - h * a
        L, R, T = cols[2 if (i, j, h) == (2, 2, 1) else (1 if h else 0)]
        top = f"{x},{y - a / 2} {x + a},{y} {x},{y + a / 2} {x - a},{y}"
        left = f"{x - a},{y} {x},{y + a / 2} {x},{y + a * 1.5} {x - a},{y + a}"
        right = f"{x + a},{y} {x},{y + a / 2} {x},{y + a * 1.5} {x + a},{y + a}"
        out.append(f'<g id="s2-q{k}"><polygon points="{left}" fill="{L}"/><polygon points="{right}" fill="{R}"/>'
                   f'<polygon points="{top}" fill="{T}"/></g>')
    return f'<svg id="s2-iso" class="abs" viewBox="0 0 640 520" style="left:220px; top:560px; width:640px; height:520px; overflow:visible">{"".join(out)}</svg>', len(cells)


ISO, NQ = iso_cubes()
make("s2", """
    #s2-lab { top: 300px; }
    #s2-tag { left: 300px; top: 1130px; }
    #s2-win { left: 40px; top: 560px; width: 1000px; height: 560px; }
    #s2-v { left: -16px; top: 0; width: 1032px; height: 487px; }
    #s2-lab2 { top: 1170px; }
""", f"""
      {label("s2-lab", 300, "2 WEEKS AGO · CLAUDE OPUS 5.5")}
      {spark("s2-sp", 820, 390, 150, bloom=False)}
      {head("s2-a", 390, ["لعبة ثلاثية الأبعاد"], "t-h3")}
      {ISO}
      {pill("s2-tag", 330, 1130, "3D GAME · 100% CODE", "var(--lime)")}
      <div id="s2-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>HyperFrames Studio</b></div>
        <div class="body"><video id="s2-v" src="assets/videos/hf_studio.mp4" data-start="5.85" data-duration="3.2" data-media-start="0" data-hf-media-start-basis="local" muted playsinline></video></div></div>
      {label("s2-lab2", 1170, "TODAY · THIS VIDEO · BUILT WITH OPUS 5.5")}
      <div class="row t-h2" style="top:1300px"><span class="mask"><span class="in" id="s2-b1">والنهاردة بيعمل</span></span></div>
      <div class="row t-h1" style="top:1440px"><span class="hl" id="s2-hlw"><span class="band" id="s2-band"></span><span class="txt" style="color:var(--ink)">نفس الفيديو ده</span></span></div>
""", f"""
      fx.rise("#s2-lab", 5.5, {{ y: 16 }});
      fx.pop("#s2-sp", 5.6, {{ from: 0.3 }});
      tl.fromTo("#s2-sp-svg", {{ rotation: 0 }}, {{ rotation: 160, duration: 5.6, ease: "none" }}, 5.6);
      fx.maskUp("#s2-a1", 8.6);
      for (let k = 0; k < {NQ}; k++) tl.fromTo("#s2-q" + k, {{ opacity: 0, y: -260 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "bounce.out" }}, 8.65 + k * 0.1);
      fx.pop("#s2-tag", 10.55, {{ from: 0.5 }});
      tl.fromTo("#s2-iso", {{ scale: 1 }}, {{ scale: 1.06, duration: 2.6, ease: "none" }}, 8.65);
      // whip to TODAY
      fx.out("#s2-iso, #s2-tag, #s2-a1", 11.2, {{ x: 700, b: 14, d: 0.3 }});
      tl.fromTo("#s2-win", {{ opacity: 0, x: -900 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, 11.3);
      tl.fromTo("#s2-v", {{ scale: 1 }}, {{ scale: 1.12, duration: 2.8, ease: "none" }}, 11.3);
      fx.rise("#s2-lab2", 11.5, {{ y: 14, b: 0 }});
      fx.maskUp("#s2-b1", 11.95);
      fx.pop("#s2-hlw", 12.85, {{ from: 0.6 }}); fx.band("#s2-band", 12.85, 0.3);
""", blob=("#0f4f44", 540, 820))

# ---------------------------------------------------------------- s3 the little brother: Sonnet 5.5
make("s3", """
    #s3-hero { left: 160px; top: 860px; width: 760px; height: 760px; }
    #s3-hero img { width: 760px; top: -40px; }
    #s3-src { top: 1650px; }
""", f"""
      {spark("s3-op", 600, 290, 300, bloom=False)}
      {spark("s3-so", 330, 420, 170)}
      {pill("s3-lb", 180, 610, "LITTLE BROTHER", "var(--lime)")}
      {head("s3-a", 670, ["أخوه الصغير"], "t-h2")}
      <div id="s3-hero" class="op-shot"><img src="assets/images/hero.png" /></div>
      {src("s3-src", 1650, "REAL · ANTHROPIC.COM · SEP 28, 2026")}
""", """
      fx.pop("#s3-op", 14.2, { from: 0.5 });
      tl.fromTo("#s3-op-svg", { rotation: 0 }, { rotation: 90, duration: 4.6, ease: "none" }, 14.2);
      fx.pop("#s3-so", 15.7, { from: 0.1, e: "back.out(3)", d: 0.5 });
      tl.fromTo("#s3-so-svg", { rotation: 0 }, { rotation: -180, duration: 3.1, ease: "power1.out" }, 15.7);
      fx.rise("#s3-lb", 16.0, { y: 20 });
      fx.maskUp("#s3-a1", 15.72);
      tl.fromTo("#s3-hero", { opacity: 0, y: 260, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power3.out" }, 17.45);
      tl.to("#s3-op, #s3-so, #s3-lb", { y: -60, opacity: 0.35, duration: 0.5, ease: "power2.out" }, 17.45);
      fx.rise("#s3-src", 17.8, { y: 10, b: 0 });
""", blob=("#136052", 540, 1100))

# ---------------------------------------------------------------- s4 up to 30% cheaper per task
make("s4", """
    #s4-lab { top: 300px; }
    #s4-num { position: absolute; left: 0; right: 0; top: 500px; text-align: center; font-family: var(--font-ar); font-weight: 900; font-size: 300px; line-height: 1.2; color: var(--yellow); }
    #s4-lb1 { top: 960px; } #s4-lb2 { top: 1100px; }
    #s4-t1 { left: 140px; top: 1020px; width: 800px; } #s4-t2 { left: 140px; top: 1160px; width: 800px; }
    #s4-ok { left: 0; right: 0; top: 1420px; display: flex; justify-content: center; }
    #s4-src { top: 1300px; }
""", f"""
      {label("s4-lab", 300, "COST PER TASK")}
      {head("s4-a", 350, ["أرخص لحد"], "t-h3")}
      <div id="s4-num" class="num" data-layout-allow-overlap>٣٠٪</div>
      {label("s4-lb1", 960, "SONNET 5")}
      <div id="s4-t1" class="op-track"><div id="s4-f1" class="op-fill" style="background:#5d7d73"></div></div>
      {label("s4-lb2", 1100, "SONNET 5.5")}
      <div id="s4-t2" class="op-track"><div id="s4-f2" class="op-fill" style="background:var(--lime)"></div></div>
      {src("s4-src", 1250, "REAL · UP TO 30% LESS PER TASK VS SONNET 5 · ANTHROPIC")}
      <div id="s4-ok" class="abs"><div class="pill on" id="s4-okp" style="font-size:52px; height:110px; border-radius:55px; padding:0 50px">{ic("check", 54, "var(--ink)")} نتائج ممتازة</div></div>
""", """
      fx.rise("#s4-lab", 18.9, { y: 16 });
      fx.maskUp("#s4-a1", 19.4);
      fx.counter("#s4-num", 19.6, 20.9, 0, 30, { suffix: "٪" });
      fx.rise("#s4-lb1, #s4-t1", 19.3, { y: 20 });
      fx.meter("#s4-f1", 19.4, 0.5, 1, { e: "power2.out" });
      fx.rise("#s4-lb2, #s4-t2", 19.6, { y: 20 });
      fx.meter("#s4-f2", 19.7, 0.5, 1, { e: "power2.out" });
      tl.to("#s4-f2", { scaleX: 0.7, duration: 0.6, ease: "power3.inOut" }, 20.6);
      fx.rise("#s4-src", 21.0, { y: 10, b: 0 });
      fx.pop("#s4-okp", 23.4, { from: 0.4 });
""", blob=("#0f4f44", 540, 700))

# ---------------------------------------------------------------- s5 far better than Sonnet 5 (Terminal-Bench 4.0)
BAR_H = 900
make("s5", """
    #s5-lab { top: 300px; }
    .s5-col { position: absolute; bottom: 300px; width: 260px; }
    .s5-bar { position: absolute; left: 0; right: 0; top: 0; bottom: 0; border-radius: 24px 24px 8px 8px; transform-origin: 50% 100%; }
    .s5-v { position: absolute; left: -40px; right: -40px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 74px; direction: ltr; }
    .s5-n { position: absolute; left: -60px; right: -60px; bottom: -84px; text-align: center; font-family: var(--font-en); font-weight: 800; font-size: 30px; letter-spacing: .12em; direction: ltr; }
    #s5-c1 { left: 640px; height: 93px; } #s5-c2 { left: 180px; height: 635px; }
    #s5-x { left: 420px; top: 760px; width: 230px; height: 120px; border-radius: 60px; background: var(--yellow); color: var(--ink); font-family: var(--font-en);
      font-weight: 900; font-size: 64px; display: flex; align-items: center; justify-content: center; direction: ltr; }
    #s5-src { top: 1730px; }
""", f"""
      {label("s5-lab", 300, "AGENTIC CODING · TERMINAL-BENCH 4.0")}
      <div class="row t-h2" style="top:370px"><span class="mask"><span class="in" id="s5-a1">أحسن من <span class="lat">Sonnet 5</span></span></span></div>
      <div class="row t-h1 op-y" style="top:490px"><span class="mask"><span class="in" id="s5-b1">بكتير جدًا</span></span></div>
      <div id="s5-c1" class="s5-col"><div id="s5-b1b" class="s5-bar" style="background:#5d7d73"></div><div class="s5-v" style="top:-100px; color:#9fbfb4" id="s5-v1">10.3%</div><div class="s5-n" style="color:var(--fg-muted)">SONNET 5</div></div>
      <div id="s5-c2" class="s5-col"><div id="s5-b2b" class="s5-bar" style="background:var(--lime); box-shadow:0 0 50px rgba(179,206,101,.45)"></div><div class="s5-v op-y" style="top:-100px" id="s5-v2">70.6%</div><div class="s5-n" style="color:var(--lime)">SONNET 5.5</div></div>
      <div id="s5-x" class="abs">×7</div>
      {src("s5-src", 1730, "REAL DATA · ANTHROPIC.COM")}
""", """
      fx.rise("#s5-lab", 24.5, { y: 16 });
      fx.maskUp("#s5-a1", 25.35);
      tl.fromTo("#s5-b1b", { scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: "power3.out" }, 26.3);
      fx.rise("#s5-v1", 26.6, { y: 20 });
      tl.fromTo("#s5-b2b", { scaleY: 0 }, { scaleY: 1, duration: 0.9, ease: "expo.out" }, 27.15);
      fx.rise("#s5-v2", 27.7, { y: 30 });
      fx.maskUp("#s5-b1", 27.65);
      fx.stamp("#s5-x", 28.1, "#s5-cam");
      fx.rise("#s5-src", 26.5, { y: 10, b: 0 });
""", blob=("#136052", 540, 1100))

# ---------------------------------------------------------------- shared: the balance scale (spine)
SCALE_CSS = """
    .sc-post { position: absolute; left: 530px; width: 20px; border-radius: 10px; background: linear-gradient(#cfe08f, #5d7d73); }
    .sc-base { position: absolute; left: 400px; width: 280px; height: 26px; border-radius: 13px; background: #5d7d73; }
    .sc-beam { position: absolute; left: 150px; width: 780px; height: 22px; border-radius: 11px; background: var(--lime); box-shadow: 0 0 30px rgba(179,206,101,.4); transform-origin: 50% 50%; }
    .sc-piv { position: absolute; left: 512px; width: 56px; height: 56px; border-radius: 50%; background: var(--yellow); }
    .sc-pan { position: absolute; width: 300px; height: 300px; }
    .sc-pan .str { position: absolute; left: 148px; top: 0; width: 4px; height: 150px; background: rgba(246,248,240,.45); }
    .sc-pan .dish { position: absolute; left: 0; top: 150px; width: 300px; height: 40px; border-radius: 0 0 150px 150px; background: #0f3d35; border: 3px solid rgba(179,206,101,.6); }
    .sc-pan .wt { position: absolute; left: 50%; bottom: 158px; transform-origin: 50% 100%; }
"""


def scale_html(p, top, left_lab, right_lab, left_w="", right_w=""):
    """Beam centre at y=top; pans hang from x=150 (left) and x=930 (right)."""
    return f"""
      <div class="sc-post" style="top:{top}px; height:{560 if top < 900 else 500}px"></div>
      <div class="sc-base" style="top:{top + (560 if top < 900 else 500)}px"></div>
      <div id="{p}-pl" class="sc-pan" style="left:0; top:{top}px"><div class="str"></div><div class="dish"></div>{left_w}
        <div class="abs" style="left:0; right:0; top:206px; display:flex; justify-content:center">{left_lab}</div></div>
      <div id="{p}-pr" class="sc-pan" style="left:780px; top:{top}px"><div class="str"></div><div class="dish"></div>{right_w}
        <div class="abs" style="left:0; right:0; top:206px; display:flex; justify-content:center">{right_lab}</div></div>
      <div id="{p}-beam" class="sc-beam" style="top:{top - 11}px"></div>
      <div class="sc-piv" style="top:{top - 28}px"></div>"""


def tilt_js(p, t, deg, d=0.8, e="elastic.out(1, 0.55)"):
    import math
    dy = round(390 * math.sin(math.radians(deg)), 1)
    return (f'tl.to("#{p}-beam", {{ rotation: {deg}, duration: {d}, ease: "{e}" }}, {t});\n'
            f'      tl.to("#{p}-pl", {{ y: {-dy}, duration: {d}, ease: "{e}" }}, {t});\n'
            f'      tl.to("#{p}-pr", {{ y: {dy}, duration: {d}, ease: "{e}" }}, {t});')


def weight(id_, size, color, text, fs=None):
    fs = fs or size // 4
    return (f'<div id="{id_}" class="wt" style="width:{size}px; height:{size}px; margin-left:-{size // 2}px; border-radius:24px; background:{color}; '
            f'display:flex; align-items:center; justify-content:center; font-family:var(--font-en); font-weight:900; font-size:{fs}px; '
            f'color:var(--ink); direction:ltr">{text}</div>')


# ---------------------------------------------------------------- s6 the scale tips: beats Opus 5.5 (Terminal-Bench 4.0)
make("s6", SCALE_CSS + """
    #s6-lab { top: 300px; }
    #s6-world { position: absolute; inset: 0; transform-origin: 50% 30%; }
    #s6-win { left: 600px; top: 520px; width: 210px; }
    #s6-shot { left: 60px; top: 1060px; width: 960px; height: 439px; }
    #s6-shot img { width: 960px; }
    #s6-hl { left: 52px; top: 264px; width: 236px; height: 168px; border-radius: 12px; border: 7px solid var(--yellow); box-shadow: 0 0 30px rgba(255,236,92,.6); }
    #s6-src { top: 1520px; }
""", f"""
      {label("s6-lab", 300, "EVEN VS OPUS 5.5")}
      <div class="row t-h3" style="top:350px"><span class="mask"><span class="in" id="s6-a1">بيتغلب على <span class="lat op-c">Opus 5.5</span> نفسه</span></span></div>
      <div id="s6-world">
      {scale_html("s6", 760, pill("s6-l1", 0, 0, "SONNET 5.5", "var(--lime)").replace('class="abs" ', 'class="" ').replace("left:0px; top:0px; ", "position:relative; "),
                  pill("s6-r1", 0, 0, "OPUS 5.5", OPUS_C).replace('class="abs" ', 'class="" ').replace("left:0px; top:0px; ", "position:relative; "),
                  weight("s6-wl", 170, "var(--lime)", "70.6"), weight("s6-wr", 150, OPUS_C, "66.4"))}
      </div>
      <div id="s6-shot" class="op-shot"><img src="assets/images/bench_top.png" /><div id="s6-hl" class="abs"></div></div>
      {src("s6-src", 1520, "REAL DATA · ANTHROPIC.COM · TERMINAL-BENCH 4.0")}
""", f"""
      fx.rise("#s6-lab", 29.7, {{ y: 16 }});
      fx.maskUp("#s6-a1", 29.9);
      tl.fromTo("#s6-world", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 29.65);
      tl.fromTo("#s6-wr", {{ opacity: 0, y: -400 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "bounce.out" }}, 30.8);
      {tilt_js("s6", 31.0, -7, 0.5, "power3.out")}
      tl.fromTo("#s6-wl", {{ opacity: 0, y: -400 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "bounce.out" }}, 31.6);
      {tilt_js("s6", 31.95, 9)}
      fx.shake("#s6-cam", 32.0, 10, 6);
      // zoom the scale up and bring in the real table
      tl.to("#s6-world", {{ scale: 0.58, y: -110, duration: 0.6, ease: "power3.inOut" }}, 32.75);
      tl.fromTo("#s6-shot", {{ opacity: 0, y: 300 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }}, 32.85);
      fx.rise("#s6-src", 33.2, {{ y: 10, b: 0 }});
      tl.fromTo("#s6-hl", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, 35.0);
      tl.fromTo("#s6-shot", {{ scale: 1 }}, {{ scale: 1.08, duration: 2.6, ease: "power1.inOut", immediateRender: false }}, 35.2);
""", blob=("#0f4f44", 540, 900), push=None)
# (the highlight sits on the 70.6% cell: src x 75..381, y 360..576 of bench_top.png -> x0.744 at 960 px)

# ---------------------------------------------------------------- s7 daily work: almost the same (scale levels)
make("s7", SCALE_CSS + """
    #s7-lab { top: 300px; }
    #s7-eq { left: 0; right: 0; top: 520px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 190px; color: var(--yellow); line-height: 1; }
    #s7-c1 { left: 120px; top: 1520px; } #s7-c2 { left: 580px; top: 1520px; }
    #s7-src { top: 1630px; }
""", f"""
      {label("s7-lab", 300, "EVERYDAY WORK")}
      {head("s7-a", 350, ["في الشغل اليومي"], "t-h2")}
      <div id="s7-eq" class="abs">≈</div>
      {scale_html("s7", 880, spark("s7-sl", 0, 0, 120, bloom=False, extra="position:relative"), spark("s7-sr", 0, 0, 170, bloom=False, extra="position:relative"),
                  weight("s7-wl", 150, "var(--lime)", "SONNET", 28), weight("s7-wr", 150, OPUS_C, "OPUS", 30))}
      <div class="row t-h2" style="top:1475px"><span class="mask"><span class="in" id="s7-b1">تقريبًا نفس الحاجة</span></span></div>
      {pill("s7-c1", 110, 1620, "GDPval-AA · 1844", "var(--lime)")}
      {pill("s7-c2", 580, 1620, "1846 · OPUS 5.5", OPUS_C)}
      {src("s7-src", 1715, "REAL DATA · ANTHROPIC.COM · KNOWLEDGE WORK")}
""", f"""
      fx.rise("#s7-lab", 38.2, {{ y: 16 }});
      fx.maskUp("#s7-a1", 39.4);
      tl.set("#s7-beam", {{ rotation: 9 }}, 38.15); tl.set("#s7-pl", {{ y: -61 }}, 38.15); tl.set("#s7-pr", {{ y: 61 }}, 38.15);
      fx.rise("#s7-wl, #s7-wr", 38.3, {{ y: -40 }});
      {tilt_js("s7", 41.4, -3, 0.7)}
      {tilt_js("s7", 42.4, 1.5, 0.5)}
      {tilt_js("s7", 43.3, 0, 0.9)}
      fx.pop("#s7-eq", 43.3, {{ from: 0.2 }});
      fx.maskUp("#s7-b1", 42.3);
      fx.pop("#s7-c1", 43.1, {{ from: 0.5 }}); fx.pop("#s7-c2", 43.3, {{ from: 0.5 }});
      fx.rise("#s7-src", 43.5, {{ y: 10, b: 0 }});
""", blob=("#136052", 540, 1000))

# ---------------------------------------------------------------- s8 computer use: 80% (OSWorld 2.1)
make("s8", """
    #s8-lab { top: 300px; }
    #s8-desk { left: 140px; top: 470px; width: 800px; height: 500px; border-radius: 30px; background: #0b2f29; border: 3px solid rgba(179,206,101,.45); overflow: hidden; }
    .s8-ico { position: absolute; width: 120px; height: 120px; border-radius: 28px; background: rgba(255,255,255,.08); display: flex; align-items: center; justify-content: center; color: var(--lime); }
    #s8-i1 { left: 90px; top: 80px; } #s8-i2 { left: 340px; top: 80px; } #s8-i3 { left: 590px; top: 80px; } #s8-i4 { left: 90px; top: 290px; } #s8-i5 { left: 340px; top: 290px; }
    #s8-cur { left: 700px; top: 380px; color: #fff; }
    #s8-rp { left: 400px; top: 140px; }
    #s8-num { position: absolute; left: 0; right: 0; top: 1030px; text-align: center; font-family: var(--font-ar); font-weight: 900; font-size: 230px; line-height: 1.2; color: var(--yellow); }
    #s8-shot { left: 90px; top: 1360px; width: 900px; height: 314px; }
    #s8-shot img { width: 900px; }
    #s8-hl { left: 50px; top: 150px; width: 218px; height: 154px; border-radius: 12px; border: 7px solid var(--yellow); }
""", f"""
      {label("s8-lab", 300, "COMPUTER USE · OSWORLD 2.1")}
      {head("s8-a", 350, ["بيستخدم الكمبيوتر زينا"], "t-h3")}
      <div id="s8-desk" class="abs">
        <div id="s8-i1" class="s8-ico">{ic("search", 60)}</div><div id="s8-i2" class="s8-ico">{ic("chat", 60)}</div>
        <div id="s8-i3" class="s8-ico">{ic("copy", 60)}</div><div id="s8-i4" class="s8-ico">{ic("book", 60)}</div><div id="s8-i5" class="s8-ico">{ic("plan", 60)}</div>
        <div id="s8-rp" class="ripple"></div>
        <svg id="s8-cur" class="cursor"><use href="#i-cursor" /></svg>
      </div>
      <div id="s8-num" class="num">٨٠٪</div>
      <div id="s8-shot" class="op-shot"><img src="assets/images/osworld.png" /><div id="s8-hl" class="abs"></div></div>
""", """
      fx.rise("#s8-lab", 44.3, { y: 16 });
      fx.maskUp("#s8-a1", 44.4);
      tl.fromTo("#s8-desk", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }, 44.3);
      fx.pop("#s8-i1, #s8-i2, #s8-i3, #s8-i4, #s8-i5", 44.45, { st: 0.07 });
      fx.cursorTo("#s8-cur", 44.9, -300, -240, 0.55);
      fx.click("#s8-cur", 45.5, "#s8-i2", "#s8-rp");
      tl.to("#s8-i2", { background: "rgba(179,206,101,.35)", duration: 0.15 }, 45.55);
      fx.cursorTo("#s8-cur", 45.85, -550, -30, 0.5);
      tl.to("#s8-i4", { background: "rgba(179,206,101,.35)", duration: 0.15 }, 46.4);
      fx.counter("#s8-num", 46.3, 47.35, 0, 80, { suffix: "٪" });
      tl.fromTo("#s8-shot", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 47.5);
      tl.fromTo("#s8-hl", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }, 48.0);
""", blob=("#0f4f44", 540, 760))

# ---------------------------------------------------------------- s9 HERO: receipt printer
make("s9", """
    #s9-lab { top: 300px; }
    #s9-prn { left: 150px; top: 540px; width: 780px; height: 120px; border-radius: 30px; background: linear-gradient(#2c4a43, #13302a); border: 3px solid rgba(179,206,101,.4); box-shadow: 0 30px 70px rgba(0,0,0,.5); }
    #s9-slot { left: 210px; top: 640px; width: 660px; height: 14px; border-radius: 7px; background: #020c0a; }
    #s9-led { left: 840px; top: 580px; width: 26px; height: 26px; border-radius: 50%; background: var(--lime); box-shadow: 0 0 20px var(--lime); }
    #s9-pap { left: 230px; top: 648px; width: 620px; height: 900px; background: #f6f4ea; border-radius: 0 0 16px 16px; color: var(--ink);
      box-shadow: 0 30px 60px rgba(0,0,0,.4); font-family: var(--font-en); direction: ltr; overflow: hidden; }
    #s9-pap .ln { position: absolute; left: 46px; right: 46px; display: flex; justify-content: space-between; font-weight: 800; font-size: 40px; letter-spacing: .02em; }
    #s9-pap .ln b { font-weight: 900; }
    #s9-pap .rule { position: absolute; left: 46px; right: 46px; border-top: 4px dashed #b9b6a7; }
    #s9-stamp { left: 560px; top: 1290px; font-size: 80px; border-color: var(--orange); color: var(--orange); background: rgba(246,244,234,.9); }
    #s9-src { top: 1700px; }
""", f"""
      {label("s9-lab", 300, "THE PRICE · PER 1M TOKENS")}
      {head("s9-a", 350, ["إنت متخيل؟"], "t-h2")}
      <div id="s9-pap" class="abs">
        <div class="ln" style="top:40px; font-size:24px; color:#6d6a5d; letter-spacing:.14em; white-space:nowrap"><span>CLAUDE · PRICE PER 1M TOKENS</span></div>
        <div class="ln" style="top:100px; font-size:56px"><b>SONNET 5.5</b></div>
        <div class="rule" style="top:190px"></div>
        <div class="ln" id="s9-l1" style="top:230px; font-size:52px"><span>INPUT</span><b id="s9-p1">$2</b></div>
        <div class="ln" id="s9-l2" style="top:320px; font-size:52px"><span>OUTPUT</span><b id="s9-p2">$10</b></div>
        <div class="rule" style="top:420px"></div>
        <div class="ln" id="s9-l3" style="top:460px; color:#8a877a"><span>OPUS 5.5</span><span id="s9-o">$4 / $20</span></div>
        <div id="s9-strike" class="abs" style="left:300px; top:488px; width:230px; height:6px; background:var(--orange); transform-origin:0 50%"></div>
        <div class="ln" id="s9-l4" style="top:560px; font-size:34px; color:#437F3E"><span>YOU SAVE</span><b>50%</b></div>
      </div>
      <div id="s9-prn" class="abs"></div><div id="s9-slot" class="abs"></div><div id="s9-led" class="abs"></div>
      <div id="s9-stamp" class="stamp">½ السعر</div>
      <div class="row t-h3" style="top:1580px"><span class="mask"><span class="in" id="s9-b1">ونتائج مبهرة بالشكل ده!</span></span></div>
      {src("s9-src", 1690, "REAL PRICING · ANTHROPIC.COM")}
""", """
      fx.rise("#s9-lab", 49.35, { y: 16 });
      fx.maskUp("#s9-a1", 49.5);
      fx.rise("#s9-prn, #s9-slot, #s9-led", 49.4, { y: -60 });
      // paper feeds out of the slot (clip from the top), line by line on the spoken prices
      tl.fromTo("#s9-pap", { clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 78% 0)", duration: 0.7, ease: "steps(8)" }, 51.2);
      tl.to("#s9-pap", { clipPath: "inset(0 0 58% 0)", duration: 0.5, ease: "steps(6)" }, 53.3);
      tl.to("#s9-pap", { clipPath: "inset(0 0 48% 0)", duration: 0.4, ease: "steps(5)" }, 55.3);
      tl.to("#s9-pap", { clipPath: "inset(0 0 30% 0)", duration: 0.5, ease: "steps(6)" }, 56.4);
      tl.to("#s9-pap", { clipPath: "inset(0 0 0% 0)", duration: 0.5, ease: "steps(6)" }, 57.4);
      fx.breathe("#s9-led", 51.2, 7, 0.25, 0.4);
      fx.pop("#s9-p1", 53.3, { from: 2 }); fx.pop("#s9-p2", 55.3, { from: 2 });
      tl.fromTo("#s9-strike", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, 57.0);
      fx.stamp("#s9-stamp", 57.6, "#s9-cam");
      fx.maskUp("#s9-b1", 58.4);
      fx.rise("#s9-src", 54.0, { y: 10, b: 0 });
""", blob=("#136052", 540, 1000))

# ---------------------------------------------------------------- s10 the real X feed
PH = 'style="left:{x}px; top:{y}px; width:{w}px; height:{h}px"'
make("s10", """
    #s10-ph { left: 190px; top: 520px; width: 700px; height: 1000px; }
    .s10-v { position: absolute; left: 0; top: -40px; width: 668px; height: 882px; }
    #s10-src { top: 1560px; }
""", f"""
      <div class="row t-h2" style="top:290px"><span class="mask"><span class="in" id="s10-a1">دخلت على <span class="lat">X</span></span></span></div>
      <div class="row t-h3" style="top:410px"><span class="hl" id="s10-hlw"><span class="band" id="s10-band"></span><span class="txt" style="color:var(--ink)">وشفت حاجات مبهرة</span></span></div>
      <div id="s10-ph" class="op-phone"><div class="scr">
        <video id="s10-v1" class="s10-v" src="assets/videos/x_feed.mp4" data-start="0.1" data-duration="1.8" data-media-start="6.2" data-hf-media-start-basis="local" muted playsinline></video>
        <video id="s10-v2" class="s10-v" src="assets/videos/x_feed.mp4" data-start="1.9" data-duration="1.6" data-media-start="25.5" data-hf-media-start-basis="local" muted playsinline></video>
        <video id="s10-v3" class="s10-v" src="assets/videos/x_feed.mp4" data-start="3.5" data-duration="1.65" data-media-start="40.5" data-hf-media-start-basis="local" muted playsinline></video>
      </div></div>
      {src("s10-src", 1560, "REAL POSTS · X.COM · SEARCH “CLAUDE SONNET 5.5”")}
""", """
      fx.maskUp("#s10-a1", 59.75);
      tl.fromTo("#s10-ph", { opacity: 0, y: 300, rotation: -4 }, { opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "power3.out" }, 59.65);
      tl.fromTo("#s10-v2", { y: 300 }, { y: 0, duration: 0.25, ease: "power3.out" }, 61.5);
      tl.fromTo("#s10-v3", { y: 300 }, { y: 0, duration: 0.25, ease: "power3.out" }, 63.1);
      fx.pop("#s10-hlw", 62.25, { from: 0.6 }); fx.band("#s10-band", 62.3, 0.3);
      fx.rise("#s10-src", 60.0, { y: 10, b: 0 });
""", blob=("#0f4f44", 540, 1000), push=1.03)

# ---------------------------------------------------------------- s11 switching to Sonnet in the real Claude app
# claude_picker.png 672x1024 shown at 2.4x; window body shows src x 300.., y 840..; rows: Opus y=871, Sonnet y=895
make("s11", """
    #s11-win { left: 90px; top: 560px; width: 900px; height: 500px; }
    #s11-img { left: -720px; top: -2016px; width: 1613px; }
    #s11-hl { left: 40px; top: 50px; width: 580px; height: 62px; border-radius: 14px; border: 6px solid var(--lime); box-shadow: 0 0 30px rgba(180,207,102,.6); }
    #s11-cur { left: 700px; top: 330px; color: #fff; }
    #s11-l1 { top: 1180px; } #s11-l2 { top: 1320px; }
    #s11-t1 { left: 140px; top: 1240px; width: 800px; } #s11-t2 { left: 140px; top: 1380px; width: 800px; }
    #s11-ok { left: 0; right: 0; top: 1540px; display: flex; justify-content: center; }
    #s11-ill { top: 1460px; }
""", f"""
      <div class="row t-h3" style="top:290px"><span class="mask"><span class="in" id="s11-a1">كنت بعتمد على <span class="lat op-c">Opus</span></span></span></div>
      <div class="row t-h2" style="top:390px"><span class="mask"><span class="in" id="s11-b1">دلوقتي <span class="lat op-l">Sonnet</span> أكتر</span></span></div>
      <div id="s11-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>Claude</b></div>
        <div class="body"><img id="s11-img" class="abs" src="assets/images/claude_picker.png" /><div id="s11-hl" class="abs"></div>
        <svg id="s11-cur" class="cursor"><use href="#i-cursor" /></svg></div></div>
      {label("s11-l1", 1180, "TOKENS LEFT · WITH OPUS")}
      <div id="s11-t1" class="op-track"><div id="s11-f1" class="op-fill" style="background:{OPUS_C}"></div></div>
      {label("s11-l2", 1320, "TOKENS LEFT · WITH SONNET")}
      <div id="s11-t2" class="op-track"><div id="s11-f2" class="op-fill" style="background:var(--lime)"></div></div>
      {src("s11-ill", 1450, "ILLUSTRATION")}
      <div id="s11-ok" class="abs"><div class="pill on" id="s11-okp" style="font-size:46px; height:100px; border-radius:50px; padding:0 46px">≈ كفاءة مشابهة</div></div>
""", """
      fx.maskUp("#s11-a1", 64.5);
      tl.fromTo("#s11-win", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 64.6);
      fx.pop("#s11-hl", 66.7, { from: 1.3, d: 0.3, e: "power3.out" });
      fx.maskUp("#s11-b1", 68.0);
      fx.cursorTo("#s11-cur", 68.6, -260, -200, 0.6);
      fx.click("#s11-cur", 69.35, null, null);
      tl.to("#s11-hl", { y: 58, duration: 0.35, ease: "power3.inOut" }, 69.4);
      tl.to("#s11-win", { scale: 0.86, y: -60, duration: 0.5, ease: "power2.inOut" }, 70.3);
      fx.rise("#s11-l1, #s11-t1, #s11-l2, #s11-t2, #s11-ill", 70.4, { y: 20, st: 0.06 });
      tl.fromTo("#s11-f1", { scaleX: 1 }, { scaleX: 0.12, duration: 2.6, ease: "power1.in" }, 71.0);
      tl.fromTo("#s11-f2", { scaleX: 1 }, { scaleX: 0.62, duration: 2.6, ease: "power1.in" }, 71.0);
      tl.to("#s11-f1", { background: "#ff5a33", duration: 0.2 }, 73.3);
      fx.pop("#s11-okp", 75.2, { from: 0.4 });
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s12 my test is coming soon
make("s12", """
    #s12-card { left: 190px; top: 560px; width: 700px; height: 640px; border-radius: 34px; background: #f6f4ea; color: var(--ink); box-shadow: 0 30px 70px rgba(0,0,0,.45); }
    #s12-card .h { position: absolute; left: 50px; right: 50px; top: 50px; font-family: var(--font-en); font-weight: 900; font-size: 34px; letter-spacing: .06em; direction: ltr; white-space: nowrap; }
    .s12-r { position: absolute; left: 50px; right: 50px; height: 90px; display: flex; align-items: center; gap: 26px; direction: ltr; font-family: var(--font-en); font-weight: 800; font-size: 40px; }
    .s12-r i { width: 56px; height: 56px; border-radius: 12px; border: 5px solid #9c998b; }
    #s12-st { left: 300px; top: 1100px; font-size: 96px; }
""", f"""
      {label("s12-lab", 300, "MY OWN TEST · COMING SOON")}
      {head("s12-a", 350, ["هجيلك بالتجربة"], "t-h2")}
      <div id="s12-card" class="abs"><div class="h">SONNET 5.5 vs OPUS 5.5</div>
        <div class="s12-r" style="top:170px"><i></i>REAL PROJECT</div><div class="s12-r" style="top:290px"><i></i>TOKENS USED</div>
        <div class="s12-r" style="top:410px"><i></i>QUALITY</div></div>
      <div id="s12-st" class="stamp">قريب</div>
""", """
      fx.rise("#s12-lab", 76.3, { y: 16 });
      fx.maskUp("#s12-a1", 77.8);
      tl.fromTo("#s12-card", { opacity: 0, y: 200, rotation: 4 }, { opacity: 1, y: 0, rotation: -2, duration: 0.5, ease: "back.out(1.4)" }, 76.4);
      fx.stamp("#s12-st", 78.6, "#s12-cam");
""", blob=("#0f4f44", 540, 900))

# ---------------------------------------------------------------- s13 1M context: a whole project, no new session
DOCS = "".join(f'<div id="s13-d{k}" class="s13-doc" style="left:{120 + (k % 6) * 140}px; top:{560 + (k // 6) * 150}px"><i></i><i></i><i></i></div>' for k in range(12))
make("s13", """
    #s13-big { left: 0; right: 0; top: 400px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 210px; color: var(--yellow); direction: ltr; line-height: 1; }
    .s13-doc { position: absolute; width: 100px; height: 124px; border-radius: 14px; background: #f3f1e7; box-shadow: 0 10px 24px rgba(0,0,0,.35); }
    .s13-doc i { position: absolute; left: 16px; right: 16px; height: 9px; border-radius: 5px; background: #c9c6b6; }
    .s13-doc i:nth-child(1) { top: 26px; } .s13-doc i:nth-child(2) { top: 50px; right: 34px; } .s13-doc i:nth-child(3) { top: 74px; }
    #s13-box { left: 140px; top: 900px; width: 800px; height: 260px; border-radius: 40px; border: 6px solid var(--lime); background: rgba(179,206,101,.08); }
    #s13-tr { left: 190px; top: 1200px; width: 700px; }
    #s13-toast { left: 150px; top: 1420px; width: 780px; height: 120px; border-radius: 26px; background: #f6f4ea; color: var(--ink); display: flex; align-items: center; gap: 24px;
      padding: 0 30px; direction: ltr; font-family: var(--font-en); font-weight: 800; font-size: 36px; box-shadow: 0 20px 50px rgba(0,0,0,.4); }
    #s13-x { left: 860px; top: 1380px; }
    #s13-ill { top: 1580px; }
""", f"""
      {label("s13-lab", 300, "CONTEXT WINDOW")}
      <div id="s13-big" class="abs">1M <span style="font-size:90px">TOKENS</span></div>
      {DOCS}
      <div id="s13-box" class="abs"></div>
      <div id="s13-tr" class="op-track"><div id="s13-f" class="op-fill" style="background:var(--lime)"></div></div>
      <div class="row t-h3" style="top:1265px"><span class="mask"><span class="in" id="s13-a1">مشروع كامل · من غير ما يعطّل</span></span></div>
      <div id="s13-toast" class="abs">{ic("x", 48, "#D93A2B")} Start a new session?</div>
      <div id="s13-x" class="xbadge" style="width:110px; height:110px">{ic("x", 64, "#fff")}</div>
      {src("s13-ill", 1580, "ILLUSTRATION")}
""", """
      fx.rise("#s13-lab", 79.7, { y: 16 });
      fx.pop("#s13-big", 81.1, { from: 0.4 });
      for (let k = 0; k < 12; k++) tl.fromTo("#s13-d" + k, { opacity: 0, y: -120 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 82.3 + k * 0.05);
      fx.rise("#s13-box", 82.5, { y: 40 });
      for (let k = 0; k < 12; k++) tl.to("#s13-d" + k, { x: 80 - 35 * (k % 6), y: 400 - 70 * Math.floor(k / 6), scale: 0.55, duration: 0.5, ease: "power3.in" }, 83.3 + k * 0.04);
      fx.maskUp("#s13-a1", 83.3);
      fx.rise("#s13-tr", 84.0, { y: 20 });
      fx.meter("#s13-f", 84.1, 2.4, 1, { e: "none" });
      tl.fromTo("#s13-toast", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }, 87.3);
      fx.pop("#s13-x", 88.0, { from: 2 });
      tl.to("#s13-toast", { opacity: 0.35, filter: "grayscale(1)", duration: 0.2 }, 88.1);
      fx.rise("#s13-ill", 85.0, { y: 10, b: 0 });
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s14 Anthropic: Opus 5.5 is still the strongest (real quote)
make("s14", """
    #s14-q { left: 90px; top: 960px; width: 900px; height: 560px; border-radius: 34px; background: #f6f4ea; color: var(--ink); box-shadow: 0 30px 70px rgba(0,0,0,.45); }
    #s14-q .qt { position: absolute; left: 60px; right: 60px; top: 60px; font-family: var(--font-en); font-weight: 700; font-size: 46px; line-height: 1.36; direction: ltr; }
    #s14-q .mk { position: absolute; left: 40px; top: -70px; font-family: var(--font-en); font-weight: 900; font-size: 200px; color: #D97757; }
    .s14-u { position: relative; display: inline-block; }
    .s14-u { background: linear-gradient(var(--yellow), var(--yellow)) no-repeat 0 88% / 0% 34%; }
    #s14-src { top: 1560px; }
""", f"""
      {label("s14-lab", 300, "ANTHROPIC SAYS")}
      {spark("s14-sp", 420, 380, 240)}
      <div class="row t-h2" style="top:660px"><span class="mask"><span class="in" id="s14-a1"><span class="lat op-c">Opus 5.5</span> ما زال</span></span></div>
      <div class="row t-h1 op-y" style="top:770px"><span class="mask"><span class="in" id="s14-b1">الأقوى</span></span></div>
      <div id="s14-q" class="abs"><div class="mk" data-layout-allow-overlap data-layout-allow-overflow>“</div><div class="qt" id="s14-qt">Opus 5.5 remains clearly stronger at
        <span class="s14-u" id="s14-u1">complex, open-ended work</span> requiring <span class="s14-u" id="s14-u2">sustained judgment.</span></div></div>
      {src("s14-src", 1560, "REAL QUOTE · ANTHROPIC.COM/CLAUDE-SONNET-5-5")}
""", """
      fx.rise("#s14-lab", 89.0, { y: 16 });
      fx.pop("#s14-sp", 91.2, { from: 0.3, e: "expo.out", d: 0.7 });
      tl.fromTo("#s14-sp-svg", { rotation: 0 }, { rotation: 120, duration: 8, ease: "none" }, 91.2);
      fx.breathe("#s14-sp-bl", 92.0, 7, 0.08, 1.4);
      fx.maskUp("#s14-a1", 91.25);
      fx.maskUp("#s14-b1", 93.1);
      tl.fromTo("#s14-q", { opacity: 0, y: 220, rotation: -2 }, { opacity: 1, y: 0, rotation: 0, duration: 0.55, ease: "power3.out" }, 93.9);
      tl.fromTo("#s14-u1", { backgroundSize: "0% 34%" }, { backgroundSize: "100% 34%", duration: 0.5, ease: "power2.out" }, 94.9);
      tl.fromTo("#s14-u2", { backgroundSize: "0% 34%" }, { backgroundSize: "100% 34%", duration: 0.5, ease: "power2.out" }, 97.6);
      fx.rise("#s14-src", 94.4, { y: 10, b: 0 });
""", blob=("#0f4f44", 540, 700))

# ---------------------------------------------------------------- s15/s16 SIGNATURE: the sorting conveyor
SORT_CSS = """
    .so-belt { position: absolute; left: 60px; top: 640px; width: 960px; height: 40px; border-radius: 20px;
      background: repeating-linear-gradient(90deg, #1d4a41 0 40px, #153a33 40px 80px); border: 3px solid rgba(179,206,101,.35); }
    .so-tray { position: absolute; top: 1220px; width: 470px; height: 470px; border-radius: 0 0 40px 40px; border: 6px solid; border-top: none; }
    .so-tray .nm { position: absolute; left: 0; right: 0; bottom: -80px; display: flex; justify-content: center; }
    .so-card { position: absolute; width: 430px; height: 110px; border-radius: 26px; background: #f6f4ea; color: var(--ink); display: flex; align-items: center;
      gap: 18px; padding: 0 22px; box-shadow: 0 16px 36px rgba(0,0,0,.4); font-family: var(--font-ar); font-weight: 800; font-size: 36px; direction: rtl; white-space: nowrap; }
    .so-card .ic { width: 66px; height: 66px; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-family: var(--font-en); font-weight: 900; font-size: 26px; color: #fff; flex: none; }
"""


def so_card(id_, text, icon, color, x, y):
    return f'<div id="{id_}" class="so-card" style="left:{x}px; top:{y}px"><span class="ic" style="background:{color}">{icon}</span><span>{text}</span></div>'


def trays(p):
    return (f'<div class="so-belt" id="{p}-belt"></div>'
            f'<div id="{p}-ts" class="so-tray" style="left:560px; border-color:var(--lime)"><div class="nm">{pill(p + "-tsn", 0, 0, "SONNET 5.5", "var(--lime)").replace("class=\"abs\" ", "").replace("left:0px; top:0px; ", "position:relative; ")}</div></div>'
            f'<div id="{p}-to" class="so-tray" style="left:50px; border-color:{OPUS_C}"><div class="nm">{pill(p + "-ton", 0, 0, "OPUS 5.5", OPUS_C).replace("class=\"abs\" ", "").replace("left:0px; top:0px; ", "position:relative; ")}</div></div>')


S_TASKS = [("so-f", "إنشاء الملفات", ic("copy", 38, "#fff"), 102.3), ("so-c", "كود بسيط", "&lt;/&gt;", 103.95),
           ("so-x", "Excel sheet", "XLS", 106.2), ("so-p", "Presentation", "PPT", 107.25)]
O_TASKS = [("so-pl", "الخطط", ic("plan", 38, "#fff"), 109.85), ("so-cx", "المهام المعقدة", ic("target", 38, "#fff"), 110.55),
           ("so-iq", "ذكاء أعلى", ic("bulb", 38, "#fff"), 113.8)]


def drop_js(p, tasks, tray_x, start_y=1560):
    js = []
    for n, (cid, _, _, t) in enumerate(tasks):
        land = start_y - n * 122
        js.append(f'tl.fromTo("#{p}-{cid}", {{ opacity: 0, x: 500, y: 0, rotation: 0 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {t - 0.25:.2f});')
        js.append(f'tl.to("#{p}-{cid}", {{ x: {tray_x + 20 - 340}, y: {land - 520}, rotation: {(-1) ** n * 4}, duration: 0.55, ease: "power2.in" }}, {t + 0.15:.2f});')
        js.append(f'fx.shake("#{p}-t{"s" if tray_x > 300 else "o"}", {t + 0.7:.2f}, 6, 4);')
    return "\n      ".join(js)


s15_cards = "".join(so_card(f"s15-{c}", txt, icn, "#437F3E", 340, 520) for c, txt, icn, _ in S_TASKS)
make("s15", SORT_CSS, f"""
      {label("s15-lab", 300, "WHO DOES WHAT")}
      <div class="row t-h2" style="top:340px"><span class="mask"><span class="in" id="s15-a1"><span class="lat op-l">Sonnet</span> للمهام اليومية</span></span></div>
      {trays("s15")}
      {s15_cards}
""", f"""
      fx.rise("#s15-lab", 99.5, {{ y: 16 }});
      fx.maskUp("#s15-a1", 100.2);
      fx.rise("#s15-belt", 99.6, {{ y: 30 }});
      tl.fromTo("#s15-belt", {{ backgroundPositionX: 0 }}, {{ backgroundPositionX: -640, duration: 8.6, ease: "none" }}, 99.6);
      fx.rise("#s15-ts, #s15-to", 99.7, {{ y: 120, st: 0.1 }});
      tl.to("#s15-ts", {{ boxShadow: "0 0 60px rgba(179,206,101,.45)", duration: 0.4 }}, 100.6);
      {drop_js("s15", S_TASKS, 560)}
""", blob=("#136052", 540, 1300), push=1.02)
# card lands: tray x 560 -> card x 340 + (560-340)=560+35 inside tray; Opus tray x 50

s16_cards = ("".join(so_card(f"s16-{c}", txt, icn, "#437F3E", 580, 1560 - n * 122) for n, (c, txt, icn, _) in enumerate(S_TASKS))
             + "".join(so_card(f"s16-{c}", txt, icn, "#c9693f", 340, 520) for c, txt, icn, _ in O_TASKS))
make("s16", SORT_CSS, f"""
      {label("s16-lab", 300, "WHO DOES WHAT")}
      <div class="row t-h2" style="top:340px"><span class="mask"><span class="in" id="s16-a1"><span class="lat op-c">Opus</span> للمهام المعقدة</span></span></div>
      {trays("s16")}
      {s16_cards}
""", f"""
      fx.maskUp("#s16-a1", 108.3);
      tl.fromTo("#s16-belt", {{ backgroundPositionX: -640 }}, {{ backgroundPositionX: -1140, duration: 6.4, ease: "none" }}, 108.15);
      tl.to("#s16-to", {{ boxShadow: "0 0 60px rgba(232,151,124,.5)", duration: 0.4 }}, 108.9);
      {drop_js("s16", O_TASKS, 50)}
      tl.to("#s16-ts, #s16-to", {{ scale: 1.03, duration: 0.3, yoyo: true, repeat: 1, ease: "power2.inOut" }}, 114.0);
""", blob=("#0f4f44", 540, 1300), push=1.02, bg=True)

# ---------------------------------------------------------------- s17 the previous reel + same model, better harness
make("s17", """
    #s17-ph { left: 300px; top: 520px; width: 480px; height: 850px; }
    #s17-v { position: absolute; left: 0; top: 0; width: 448px; height: 796px; }
    #s17-rig { left: 140px; top: 560px; width: 800px; height: 1000px; object-fit: cover; border-radius: 40px; }
    #s17-g { left: 140px; top: 1620px; width: 800px; }
    #s17-gl { top: 1570px; }
""", f"""
      {label("s17-lab", 300, "PREVIOUS REEL · THE HARNESS")}
      <div class="row t-h3" style="top:350px"><span class="mask"><span class="in" id="s17-a1">زي ما قلتلك في الريل</span></span></div>
      <div id="s17-ph" class="op-phone"><div class="scr"><video id="s17-v" src="assets/videos/harness_reel.mp4" data-start="0.9" data-duration="3.6" data-media-start="14" data-hf-media-start-basis="local" muted playsinline></video></div></div>
      <img id="s17-rig" class="abs" src="assets/images/harness_rig.png" />
      <div class="row t-h3" style="top:360px; font-size:72px"><span class="mask"><span class="in" id="s17-b1">نفس الموديل · أداء أحسن</span></span></div>
      {label("s17-gl", 1570, "PERFORMANCE")}
      <div id="s17-g" class="op-track"><div id="s17-f" class="op-fill" style="background:var(--lime)"></div></div>
""", """
      fx.rise("#s17-lab", 114.65, { y: 16 });
      fx.maskUp("#s17-a1", 114.8);
      tl.fromTo("#s17-ph", { opacity: 0, y: 260, rotation: 5 }, { opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "power3.out" }, 115.4);
      // to the rig: the same engine in a better harness
      fx.out("#s17-ph, #s17-a1", 117.95, { y: -100, d: 0.3 });
      fx.hide("#s17-rig");
      tl.fromTo("#s17-rig", { opacity: 0, scale: 1.15 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.out", immediateRender: false }, 118.1);
      fx.maskUp("#s17-b1", 118.2);
      fx.rise("#s17-gl, #s17-g", 119.0, { y: 20 });
      fx.meter("#s17-f", 119.3, 0.4, 0.55, { e: "power2.out" });
      tl.to("#s17-f", { scaleX: 0.95, duration: 0.5, ease: "back.out(2)" }, 120.5);
""", blob=("#136052", 540, 1000))

# ---------------------------------------------------------------- s18 harness swap + model + good harness = results
make("s18", """
    .h-fr { position: absolute; width: 300px; height: 300px; border-radius: 40px; border: 6px dashed rgba(179,206,101,.55); }
    .h-nm[data-x] { }
    .h-nm { position: absolute; left: -40px; right: -40px; top: 316px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 40px; color: var(--fg); direction: ltr; white-space: nowrap; }
    #s18-h1 { left: 720px; top: 560px; } #s18-h2 { left: 390px; top: 560px; } #s18-h3 { left: 60px; top: 560px; }
    #s18-eq { left: 0; right: 0; top: 1160px; display: flex; justify-content: center; align-items: center; gap: 14px; direction: rtl; }
    .eq-b { height: 100px; padding: 0 24px; border-radius: 50px; display: flex; align-items: center; gap: 10px; font-family: var(--font-en); font-weight: 900; font-size: 30px; direction: ltr; white-space: nowrap; }
    .eq-op { font-family: var(--font-en); font-weight: 900; font-size: 60px; color: var(--fg-muted); }
""", f"""
      {label("s18-lab", 300, "CODING HARNESS")}
      <div class="row t-h3" style="top:350px"><span class="mask"><span class="in" id="s18-a1">غيّر الـــ<span class="lat">harness</span></span></span></div>
      <div id="s18-h1" class="h-fr"><div class="h-nm" data-layout-allow-overflow>OpenCode</div></div>
      <div id="s18-h2" class="h-fr"><div class="h-nm" data-layout-allow-overflow>Claude Code</div></div>
      <div id="s18-h3" class="h-fr"><div class="h-nm" data-layout-allow-overflow>Pi</div></div>
      {spark("s18-sp", 770, 610, 200)}
      <div id="s18-eq" class="abs">
        <div id="s18-e1" class="eq-b" style="background:#0b2f29; border:4px solid #e8977c; color:#e8977c">MODEL</div><div id="s18-p1" class="eq-op">+</div>
        <div id="s18-e2" class="eq-b" style="background:#0b2f29; border:4px solid var(--lime); color:var(--lime)">GOOD HARNESS</div><div id="s18-p2" class="eq-op">=</div>
        <div id="s18-e3" class="eq-b" style="background:var(--lime); color:var(--ink)">{ic("check", 48, "var(--ink)")} RESULTS</div></div>
      <div class="row t-h3" style="top:1400px; font-size:76px"><span class="mask"><span class="in" id="s18-b1">الموديل + <span class="lat">harness</span> كويس</span></span></div>
""", """
      fx.rise("#s18-lab", 121.95, { y: 16 });
      fx.maskUp("#s18-a1", 121.95);
      fx.pop("#s18-h1", 123.6, { from: 0.5 }); fx.pop("#s18-h2", 124.4, { from: 0.5 }); fx.pop("#s18-h3", 125.4, { from: 0.5 });
      fx.pop("#s18-sp", 122.4, { from: 0.2 });
      tl.fromTo("#s18-sp-svg", { rotation: 0 }, { rotation: 360, duration: 9, ease: "none" }, 122.4);
      // the engine slides into each harness on its name
      tl.to("#s18-sp", { x: 0, duration: 0.3, ease: "back.out(2)" }, 123.7);
      tl.to("#s18-h1", { borderStyle: "solid", borderColor: "#b3ce65", duration: 0.1 }, 123.95);
      tl.to("#s18-sp", { x: -330, duration: 0.35, ease: "back.out(2)" }, 124.45);
      tl.to("#s18-h1", { borderColor: "rgba(179,206,101,.35)", duration: 0.1 }, 124.5);
      tl.to("#s18-h2", { borderStyle: "solid", borderColor: "#b3ce65", duration: 0.1 }, 124.75);
      tl.to("#s18-sp", { x: -660, duration: 0.35, ease: "back.out(2)" }, 125.45);
      tl.to("#s18-h2", { borderColor: "rgba(179,206,101,.35)", duration: 0.1 }, 125.5);
      tl.to("#s18-h3", { borderStyle: "solid", borderColor: "#b3ce65", duration: 0.1 }, 125.75);
      fx.pop("#s18-e1", 127.7, { from: 0.5 }); fx.pop("#s18-p1", 128.1);
      fx.pop("#s18-e2", 130.35, { from: 0.5 }); fx.pop("#s18-p2", 130.6); fx.pop("#s18-e3", 130.8, { from: 0.5 });
      fx.maskUp("#s18-b1", 128.2);
""", blob=("#0f4f44", 540, 900))

# ---------------------------------------------------------------- s19 go back to that reel
make("s19", """
    #s19-ph { left: 330px; top: 520px; width: 420px; height: 746px; }
    #s19-v { position: absolute; left: 0; top: 0; width: 388px; height: 690px; }
    #s19-pl { left: 470px; top: 820px; width: 140px; height: 140px; border-radius: 50%; background: var(--red); display: flex; align-items: center; justify-content: center; color: #fff; }
    #s19-arr { left: 760px; top: 640px; width: 220px; height: 260px; }
""", f"""
      {label("s19-lab", 300, "WATCH · THE HARNESS REEL")}
      <div id="s19-ph" class="op-phone"><div class="scr"><video id="s19-v" src="assets/videos/harness_reel.mp4" data-start="0" data-duration="3.15" data-media-start="2" data-hf-media-start-basis="local" muted playsinline></video></div></div>
      <div id="s19-pl" class="abs">{ic("play", 70, "#fff")}</div>
      <svg id="s19-arr" class="abs" viewBox="0 0 220 260" style="overflow:visible"><path id="s19-ap" d="M200 20 C 210 150, 120 230, 20 220" fill="none" stroke="var(--yellow)" stroke-width="12" stroke-linecap="round"/>
        <path d="M44 190 L16 222 L56 240" fill="none" stroke="var(--yellow)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div class="row t-h1" style="top:1330px"><span class="mask"><span class="in" id="s19-a1">ارجع له</span></span></div>
""", """
      fx.rise("#s19-lab", 131.55, { y: 16 });
      tl.fromTo("#s19-ph", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 131.6);
      fx.pop("#s19-pl", 132.2);
      fx.draw("#s19-ap", 132.6, 0.5);
      fx.rise("#s19-arr", 132.6, { y: 0, b: 0, d: 0.2 });
      fx.maskUp("#s19-a1", 133.1);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s20 available everywhere
TILE = 'style="left:{x}px; top:{y}px"'
make("s20", """
    .t20 { position: absolute; width: 440px; height: 300px; border-radius: 34px; background: #0b2f29; border: 3px solid rgba(179,206,101,.45); }
    .t20 .nm { position: absolute; left: 0; right: 0; top: 190px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 46px; direction: ltr; white-space: nowrap; }
    .t20 .bd { position: absolute; right: -18px; top: -22px; height: 58px; padding: 0 20px; border-radius: 29px; background: var(--lime); color: var(--ink); display: flex; align-items: center;
      font-family: var(--font-en); font-weight: 900; font-size: 24px; letter-spacing: .1em; direction: ltr; }
    #s20-t1 { left: 580px; top: 580px; } #s20-t2 { left: 60px; top: 580px; } #s20-t3 { left: 580px; top: 960px; } #s20-t4 { left: 60px; top: 960px; }
    .s20-dev { position: absolute; top: 60px; width: 110px; height: 110px; border-radius: 26px; background: rgba(255,255,255,.06); display: flex; align-items: center; justify-content: center;
      font-family: var(--font-en); font-weight: 900; font-size: 22px; color: var(--fg-muted); }
    #s20-ok { left: 0; right: 0; top: 1380px; display: flex; justify-content: center; gap: 26px; }
""", f"""
      {label("s20-lab", 300, "TRY IT TODAY")}
      <div class="row t-h2" style="top:340px"><span class="mask"><span class="in" id="s20-a1">في كل الأدوات تقريبًا</span></span></div>
      <div id="s20-t1" class="t20">{spark("s20-sp", 160, 40, 120, bloom=False)}<div class="nm">Claude</div><div class="bd" id="s20-b1">UPDATED</div></div>
      <div id="s20-t2" class="t20"><div class="s20-dev" id="s20-m" style="left:90px">{ic("chat", 56, "var(--lime)")}</div><div class="s20-dev" id="s20-w" style="left:240px">WEB</div>
        <div class="nm" style="font-size:38px">MOBILE · WEB</div></div>
      <div id="s20-t3" class="t20"><div class="nm" style="top:110px">SureThing AI</div><div class="bd" id="s20-b3">UPDATED</div></div>
      <div id="s20-t4" class="t20"><div class="nm" style="top:110px">Perplexity</div><div class="bd" id="s20-b4">UPDATED</div></div>
      <div id="s20-ok" class="abs"><div class="pill" id="s20-o1" style="font-size:42px">أوفر عليهم</div><div class="pill on" id="s20-o2" style="font-size:42px">نتائج أحسن</div></div>
""", """
      fx.rise("#s20-lab", 134.4, { y: 16 });
      fx.maskUp("#s20-a1", 136.2);
      fx.pop("#s20-t1", 137.45, { from: 0.5 });
      tl.fromTo("#s20-sp-svg", { rotation: 0 }, { rotation: 200, duration: 10, ease: "none" }, 137.45);
      fx.pop("#s20-t2", 138.3, { from: 0.5 });
      fx.pop("#s20-m", 138.6); fx.pop("#s20-w", 139.25);
      fx.pop("#s20-t3", 141.0, { from: 0.5 });
      fx.pop("#s20-t4", 141.95, { from: 0.5 });
      fx.pop("#s20-b1", 144.1, { from: 1.8 }); fx.pop("#s20-b3", 144.3, { from: 1.8 }); fx.pop("#s20-b4", 144.5, { from: 1.8 });
      fx.pop("#s20-o1", 145.1, { from: 0.5 }); fx.pop("#s20-o2", 146.35, { from: 0.5 });
""", blob=("#136052", 540, 1000))

# ---------------------------------------------------------------- s21 CTA: follow
make("s21", """
    #s21-k1 { left: 640px; top: 640px; } #s21-k2 { left: 360px; top: 560px; } #s21-k3 { left: 80px; top: 640px; }
    #s21-btn { left: 290px; top: 1690px; }
    #s21-cur { left: 640px; top: 1760px; color: #fff; }
    #s21-nm { top: 1530px; }
""", f"""
      <div class="row t-h3" style="top:330px"><span class="mask"><span class="in" id="s21-a1">كل موديل جديد وإزاي تستفيد منه</span></span></div>
      {pill("s21-k1", 640, 640, "NEW MODELS", "var(--lime)")}
      {pill("s21-k2", 360, 560, "HOW TO USE", "var(--yellow)")}
      {pill("s21-k3", 80, 640, "REAL VALUE", OPUS_C)}
      {hossam("s21-ho", 240, 760, 600)}
      <div id="s21-nm" class="op-name t-h2" style="top:1530px">حسام الدين حسن</div>
      <div id="s21-btn" class="op-btn">{ic("person", 44, "#fff")} تابعني</div>
      <div id="s21-ok" class="abs" style="left:770px; top:1704px; width:76px; height:76px; border-radius:50%; background:var(--lime); display:flex; align-items:center; justify-content:center">{ic("check", 46, "var(--ink)")}</div>
      <svg id="s21-cur" class="cursor"><use href="#i-cursor" /></svg>
""", """
      fx.maskUp("#s21-a1", 148.8);
      fx.pop("#s21-k1", 149.0); fx.pop("#s21-k2", 150.6); fx.pop("#s21-k3", 151.9);
      tl.fromTo("#s21-ho", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, 147.7);
      fx.rise("#s21-nm", 153.7, { y: 30 });
      fx.pop("#s21-btn", 152.4, { from: 0.4 });
      fx.cursorTo("#s21-cur", 152.7, -150, -40, 0.4);
      fx.click("#s21-cur", 153.15, "#s21-btn", null);
      tl.to("#s21-btn", { background: "#2b2a28", color: "#b3ce65", duration: 0.15 }, 153.2);
      fx.pop("#s21-ok", 153.25, { from: 0.2 });
""", blob=("#136052", 540, 1100), exit=False)

# ---------------------------------------------------------------- cues (voice + SFX) and chrome
cues = [c for c in json.loads((HERE / "cues.json").read_text(encoding="utf-8")) if c.get("voice")]
S = [  # (t, sfx, accent)
    (0.0, "lib/spark-ignite", 1.0), (1.1, "library/pop", 0.6), (1.8, "library/whoosh-short", 0.7), (2.62, "lib/title-slam", 0.8), (3.65, "library/pop", 0.6), (4.42, "library/impact-bass-1", 0.9),
    (5.45, "library/whoosh", 0.6), (8.65, "library/click-soft", 0.6), (9.2, "library/click-soft", 0.6), (10.55, "library/pop", 0.6), (11.2, "library/whoosh-short", 0.8), (12.85, "library/sparkle", 0.6),
    (14.2, "library/whoosh", 0.5), (15.7, "lib/spark-ignite", 0.8), (17.45, "library/whoosh-short", 0.6),
    (18.8, "library/whoosh", 0.6), (19.6, "library/typing", 0.4), (20.6, "library/click", 0.7), (23.4, "library/chime", 0.6),
    (24.5, "library/whoosh-short", 0.5), (26.3, "library/pop", 0.5), (27.15, "library/riser", 0.0), (28.1, "lib/title-slam", 0.8),
    (29.65, "library/whoosh", 0.6), (30.8, "lib/harness-lock", 0.8), (31.6, "lib/harness-lock", 0.9), (32.75, "library/whoosh-short", 0.6), (35.0, "library/ping", 0.6),
    (38.2, "library/whoosh-short", 0.5), (41.4, "lib/gauge-swing", 0.8), (43.3, "library/chime", 0.6),
    (44.3, "library/whoosh-short", 0.5), (45.5, "library/click", 0.9), (46.4, "library/click", 0.8), (47.5, "library/pop", 0.6),
    (49.3, "library/whoosh-cinematic", 0.6), (51.2, "library/typing", 0.7), (53.3, "library/key-press", 0.9), (55.3, "library/key-press", 0.9), (57.0, "library/error", 0.4), (57.6, "lib/tape-seal", 1.0),
    (59.65, "library/whoosh-short", 0.6), (61.5, "library/whoosh-short", 0.4), (62.25, "library/sparkle", 0.6), (63.1, "library/whoosh-short", 0.4),
    (64.6, "library/whoosh", 0.5), (66.7, "library/click-soft", 0.7), (69.35, "library/click", 0.9), (71.0, "library/glitch-1", 0.0), (73.3, "library/error", 0.35), (75.2, "library/chime", 0.6),
    (76.4, "library/whoosh-short", 0.5), (78.6, "lib/tape-seal", 0.9),
    (79.7, "library/whoosh", 0.5), (81.1, "lib/title-slam", 0.7), (82.3, "library/pop", 0.5), (83.3, "library/whoosh-short", 0.5), (87.3, "library/notification", 0.5), (88.0, "library/error", 0.5),
    (89.0, "library/whoosh-cinematic", 0.5), (91.2, "lib/spark-ignite", 0.8), (93.1, "library/impact-bass-2", 0.7), (93.9, "library/whoosh-short", 0.5),
    (99.5, "library/whoosh", 0.6), (100.6, "library/chime", 0.4),
] + [(t + 0.7, "library/pop", 0.55) for *_, t in S_TASKS + O_TASKS] + [(t - 0.25, "library/whoosh-short", 0.35) for *_, t in S_TASKS + O_TASKS] + [
    (114.0, "lib/winner-sparkle", 0.6),
    (114.65, "library/whoosh", 0.5), (115.4, "library/whoosh-short", 0.5), (118.1, "lib/harness-lock", 0.8), (119.3, "lib/gauge-swing", 0.7),
    (122.0, "library/whoosh", 0.5), (123.95, "lib/cartridge-click", 0.9), (124.75, "lib/cartridge-click", 0.9), (125.75, "lib/cartridge-click", 0.9), (127.7, "library/pop", 0.6), (130.35, "library/pop", 0.6), (130.8, "library/chime", 0.7),
    (131.6, "library/whoosh-short", 0.5), (132.2, "library/pop", 0.6),
    (134.4, "library/whoosh", 0.5), (137.45, "library/pop", 0.6), (138.3, "library/pop", 0.5), (141.0, "library/pop", 0.6), (141.95, "library/pop", 0.6), (144.1, "library/notification", 0.6), (146.35, "library/chime", 0.6),
    (147.7, "library/whoosh-cinematic", 0.5), (149.0, "library/pop", 0.5), (150.6, "library/pop", 0.5), (151.9, "library/pop", 0.5), (153.15, "library/click", 1.0), (153.3, "library/notification", 0.7),
]
for t, s, acc in sorted(S):
    if acc <= 0:
        continue
    cues.append({"t": round(t, 2), "sfx": s, "accent": acc})
(HERE / "cues.json").write_text(json.dumps(cues, ensure_ascii=False, indent=1), encoding="utf-8")
(HERE / "chrome.json").write_text(json.dumps({
    "enabled": True, "series": "CLAUDE 5.5", "grain": False,
    "sections": [{"t": 0, "label": "THE NEWS"}, {"t": 18.85, "label": "THE PROOF"}, {"t": 49.3, "label": "THE PRICE"},
                 {"t": 59.6, "label": "MY TAKE"}, {"t": 88.85, "label": "SONNET VS OPUS"}, {"t": 114.6, "label": "THE HARNESS"},
                 {"t": 134.35, "label": "WHERE TO TRY"}, {"t": 147.55, "label": "FOLLOW"}],
    "wipes": [18.75, 49.2, 88.75, 114.5, 134.25]}, indent=1), encoding="utf-8")
print("built", len(P.scenes), "scenes,", len(cues) - 1, "sfx cues")
