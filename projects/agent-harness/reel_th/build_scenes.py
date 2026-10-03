# Talking-head version: reused v1 scene builders (+ guard) — new scenes live in build_th.py.
# Builds compositions/sN.html for the Agent Harness reel (9:16, dark preset).
# All times are GLOBAL seconds on the edited voice (transcript/reel_words.json).
# Spine: the AI model is an ENGINE core; the harness is the CHASSIS (lime brackets) built around it.
# Re-run after edits:  python build_scenes.py
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCENES = {s["id"]: s for s in json.loads((HERE / "scenes.json").read_text(encoding="utf-8"))}


def make(sid, css, body, js, blob=("#136052", 640, 760), exit_t=None, push=1.035):
    if sid not in SCENES:
        return
    s = SCENES[sid]
    st, du = s["start"], s["duration"]
    et = exit_t if exit_t is not None else round(st + du - 0.32, 2)
    bc, bx, by = blob
    html = f"""<!doctype html>
<html lang="ar"><head><meta charset="UTF-8" /></head><body>
<template id="{sid}-template">
  <style>
{css}
  </style>
  <div id="{sid}" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{du}">
    <div class="bg"></div>
    <div id="{sid}-blob" class="blob" style="left:{bx - 380}px; top:{by - 380}px; width:760px; height:760px; background:{bc}; opacity:.55"></div>
    <div id="{sid}-bgp" class="dots"></div>
    <div id="{sid}-cam" class="cam">
{body}
    </div>
  </div>
  <script>
    (function () {{
      const fx = window.HF_SCENE({st});
      const {{ tl }} = fx;
      fx.drift("#{sid}-bgp", {st}, {du}, 70, -40);
      fx.drift("#{sid}-blob", {st}, {du}, -120, 60);
      {"" if push is None else f'fx.pushIn("#{sid}-cam", {st}, {du}, {push});'}
{js}
      tl.to("#{sid}-cam", {{ opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power2.in" }}, {et});
      window.__timelines["{sid}"] = tl.real;
    }})();
  </script>
</template></body></html>
"""
    (HERE / "compositions" / f"{sid}.html").write_text(html, encoding="utf-8")


def core(id_, x, y, size, label=None, label_top=None):
    """Engine core = the AI model. x,y = top-left."""
    lab = ""
    if label:
        lt = label_top if label_top is not None else size + 26
        lab = f'<div class="ah-mod" id="{id_}-lab" style="left:50%; top:{lt}px; transform:translateX(-50%); font-size:30px; height:64px"><span class="lat">{label}</span></div>'
    return (f'<div id="{id_}" class="abs" style="left:{x}px; top:{y}px; width:{size}px; height:{size}px">'
            f'<div class="ah-bloom" id="{id_}-bl" style="left:-60%; top:-60%; width:220%; height:220%"></div>'
            f'<svg class="ah-gear" id="{id_}-g"><use href="#i-gear" /></svg>'
            f'<div class="ah-core" style="inset:0"></div><div class="ring" id="{id_}-r1" style="border-radius:50%"></div>'
            f'<div class="ring" id="{id_}-r2" style="border-radius:50%"></div>{lab}</div>')


def brackets(prefix, x, y, w, h, size=150):
    return "".join([
        f'<div class="ah-brk a" id="{prefix}-a" style="left:{x}px; top:{y}px; width:{size}px; height:{size}px"></div>',
        f'<div class="ah-brk b" id="{prefix}-b" style="left:{x + w - size}px; top:{y}px; width:{size}px; height:{size}px"></div>',
        f'<div class="ah-brk c" id="{prefix}-c" style="left:{x}px; top:{y + h - size}px; width:{size}px; height:{size}px"></div>',
        f'<div class="ah-brk d" id="{prefix}-d" style="left:{x + w - size}px; top:{y + h - size}px; width:{size}px; height:{size}px"></div>'])


def lines(prefix, specs):
    return "".join(f'<span class="ah-ln" id="{prefix}{i}" style="width:{w}%; background:{c}"></span>' for i, (w, c) in enumerate(specs, 1))


L, Y, O, T, W = "var(--lime)", "var(--yellow)", "var(--orange)", "#2c8a76", "rgba(246,248,240,.55)"

# ---------------------------------------------------------------- s1 hook
make("s1", """
    #s1-k { top: 250px; } #s1-h { top: 330px; }
    #s1-tag { left: 0; right: 0; top: 1130px; text-align: center; }
    #s1-code { left: 150px; top: 1250px; width: 780px; height: 360px; }
    #s1-mod { left: 640px; top: 600px; }
""", f"""
      <div id="s1-k" class="row t-h3 muted"><span class="mask"><span class="in" id="s1-k1">كلنا بنسمع عن</span></span></div>
      <div id="s1-h" class="row" style="font-size:150px"><span class="ah-en" id="s1-h1" style="display:inline-block">AI Model</span></div>
      {core("s1-core", 380, 640, 320)}
      <div id="s1-tag" class="ah-tag">THE ENGINE</div>
      <div id="s1-code" class="ah-code">{lines("s1-l", [(62, L), (84, W), (40, Y), (74, W), (55, T), (30, O)])}</div>
      <div id="s1-mod" class="ah-mod"><span class="ic"><svg width="28" height="28"><use href="#i-bolt" /></svg></span><span class="lat">Claude Fable</span></div>
""", """
      fx.punch("#s1-cam", 0, 1.25);
      fx.pop("#s1-core", 0.05, { from: 0.15, d: 0.9, e: "expo.out" });
      tl.fromTo("#s1-core-bl", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 1.2, ease: "power2.out" }, 0.1);
      fx.breathe("#s1-core-bl", 1.3, 3.8, 0.08, 1.2);
      tl.fromTo("#s1-core-g", { rotation: 0 }, { rotation: 140, duration: 5.4, ease: "none" }, 0);
      fx.maskUp("#s1-k1", 0.1);
      fx.letterDrop("#s1-h1", 1.15, { st: 0.04 });
      fx.rise("#s1-tag", 1.5, { y: 20 });
      fx.pop("#s1-code", 1.9, { from: 0.8, e: "power3.out" });
      tl.fromTo("#s1-code .ah-ln", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.3, ease: "power2.out", stagger: 0.16 }, 2.3);
      fx.pop("#s1-mod", 4.0, { from: 0.3 });
      fx.ringPulse("#s1-core-r1, #s1-core-r2", 4.1);
""", blob=("#136052", 540, 800), push=None, exit_t=5.05)

# ---------------------------------------------------------------- s2 slam
make("s2", """
    #s2-q { left: 0; right: 0; top: 260px; text-align: center; font-size: 1300px; line-height: 1; }
    #s2-lab { top: 520px; } #s2-k { top: 580px; }
    #s2-a { top: 800px; font-size: 170px; } #s2-b { top: 990px; font-size: 185px; }
    #s2-u { left: 150px; width: 780px; top: 1250px; height: 22px; border-radius: 11px; background: var(--yellow); transform-origin: 100% 50%; }
""", """
      <div id="s2-q" class="ah-q">؟</div>
      <div id="s2-lab" class="row"><span class="t-label">THE MISSING PIECE</span></div>
      <div id="s2-k" class="row t-h3"><span class="mask"><span class="in" id="s2-k1">بس كتير مننا ما يعرفش</span></span></div>
      <div id="s2-a" class="row ah-en" style="line-height:1.05">AGENT</div>
      <div id="s2-b" class="row ah-en ah-l" style="line-height:1.05; text-shadow:0 0 60px rgba(179,206,101,.55)">HARNESS</div>
      <div id="s2-u" class="abs"></div>
""", """
      fx.drift("#s2-q", 5.2, 3.85, -60, 30);
      tl.fromTo("#s2-q", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 1.2, ease: "power2.out" }, 5.2);
      fx.rise("#s2-lab", 5.3, { y: 16 });
      fx.maskUp("#s2-k1", 5.35);
      tl.fromTo("#s2-a", { opacity: 0, scale: 2.6, filter: "blur(18px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.28, ease: "expo.out" }, 7.78);
      tl.fromTo("#s2-b", { opacity: 0, scale: 2.6, filter: "blur(18px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.28, ease: "expo.out" }, 8.2);
      fx.shake("#s2-cam", 8.3, 16, 7);
      fx.band("#s2-u", 8.45, 0.3);
      fx.zoomThrough("#s2-cam", 8.75, 1.5);
""", blob=("#1a7564", 540, 1000), exit_t=9.2)

# ---------------------------------------------------------------- s3 model = machine
make("s3", """
    #s3-lab { top: 210px; } #s3-h { top: 250px; }
    #s3-p { left: 110px; top: 560px; width: 860px; height: 150px; }
    #s3-pt { position: absolute; right: 34px; top: 40px; font-size: 46px; font-weight: 700; white-space: nowrap; direction: rtl; }
    #s3-arr { left: 520px; top: 720px; width: 40px; height: 150px; }
    #s3-code { left: 170px; top: 1330px; width: 740px; height: 330px; }
    #s3-ot { left: 0; right: 0; top: 1690px; text-align: center; }
""", f"""
      <div id="s3-lab" class="row"><span class="t-label">THE AI MODEL</span></div>
      <div id="s3-h" class="row t-h1" data-layout-allow-overlap><span class="mask"><span class="in" id="s3-h1">الموديل = <span class="hl"><span class="band" id="s3-band"></span><span class="txt" id="s3-txt" style="color:var(--yellow)">الآلة</span></span></span></span></div>
      <div id="s3-p" class="window"><div id="s3-pt"><span id="s3-pt1"></span><span class="caret" id="s3-car"></span></div></div>
      <svg id="s3-arr" class="abs" viewBox="0 0 40 150"><path id="s3-ap" pathLength="1" d="M20 0 V135 M6 120 L20 140 L34 120" fill="none" stroke="#b3ce65" stroke-width="6" stroke-linecap="round" /></svg>
      {core("s3-core", 400, 890, 280)}
      <div id="s3-code" class="ah-code">{lines("s3-l", [(70, L), (52, W), (88, Y), (44, W), (66, T)])}</div>
      <div id="s3-ot" class="ah-tag">OUTPUT · CODE</div>
""", """
      fx.rise("#s3-lab", 8.9, { y: 16 });
      fx.maskUp("#s3-h1", 9.0);
      fx.band("#s3-band", 10.3);
      tl.to("#s3-txt", { color: "#0d0d0d", duration: 0.15 }, 10.4);
      fx.pop("#s3-core", 9.4, { from: 0.3, d: 0.6, e: "expo.out" });
      tl.fromTo("#s3-core-g", { rotation: 0 }, { rotation: 300, duration: 7.6, ease: "power1.in" }, 8.85);
      fx.breathe("#s3-core-bl", 9.6, 6.4, 0.1, 0.9);
      fx.ringPulse("#s3-core-r1, #s3-core-r2", 11.5);
      fx.pop("#s3-p", 13.35, { from: 0.85, e: "power3.out" });
      fx.typeText("#s3-pt1", 13.55, "اكتب لي كود يعمل…", 22);
      tl.fromTo("#s3-car", { opacity: 1 }, { opacity: 0.15, duration: 0.2, ease: "steps(1)", yoyo: true, repeat: 7 }, 13.4);
      fx.draw("#s3-ap", 14.4, 0.35);
      fx.ringPulse("#s3-core-r1, #s3-core-r2", 14.7);
      fx.pop("#s3-code", 14.85, { from: 0.7, e: "power3.out" });
      tl.fromTo("#s3-code .ah-ln", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.25, ease: "power2.out", stagger: 0.12 }, 15.0);
      fx.rise("#s3-ot", 15.3, { y: 14 });
""", blob=("#136052", 540, 1030))

# ---------------------------------------------------------------- s4 balance scale
make("s4", """
    #s4-lab { top: 210px; } #s4-h { top: 250px; font-size: 120px; } #s4-k { top: 430px; }
    #s4-post { left: 528px; top: 1010px; width: 24px; height: 470px; border-radius: 12px; background: rgba(246,248,240,.25); }
    #s4-base { left: 380px; top: 1470px; width: 320px; height: 26px; border-radius: 13px; background: rgba(246,248,240,.25); }
    #s4-beam { left: 150px; top: 1000px; width: 780px; height: 18px; border-radius: 9px; background: var(--fg); transform-origin: 50% 50%; }
    #s4-piv { left: 515px; top: 984px; width: 50px; height: 50px; border-radius: 50%; background: var(--yellow); }
    .s4-pan { position: absolute; width: 300px; height: 300px; }
    #s4-pr { left: 630px; top: 1010px; } #s4-pl { left: 150px; top: 1010px; }
    .s4-str { position: absolute; left: 148px; top: 0; width: 4px; height: 70px; background: rgba(246,248,240,.5); }
    .s4-dish { position: absolute; left: 0; top: 70px; width: 300px; height: 230px; border-radius: 0 0 150px 150px; background: rgba(255,255,255,.06); border: 3px solid rgba(246,248,240,.3); }
    .s4-cap { position: absolute; left: 0; right: 0; top: 315px; text-align: center; font-size: 26px; }
    #s4-lets { top: 1640px; }
""", f"""
      <div id="s4-lab" class="row"><span class="t-label">MODEL VS HARNESS</span></div>
      <div id="s4-h" class="row ah-en ah-l"><span class="mask"><span class="in" id="s4-h1">Agent Harness</span></span></div>
      <div id="s4-k" class="row t-h2"><span class="mask"><span class="in" id="s4-k1">بنفس الأهمية… أو أعلى</span></span></div>
      <div id="s4-post" class="abs"></div><div id="s4-base" class="abs"></div>
      <div id="s4-beam" class="abs"></div><div id="s4-piv" class="abs"></div>
      <div id="s4-pr" class="s4-pan"><div class="s4-str"></div><div class="s4-dish"></div>
        {core("s4-c", 85, 120, 130)}<div class="s4-cap ah-tag" style="position:absolute">MODEL</div></div>
      <div id="s4-pl" class="s4-pan"><div class="s4-str"></div><div class="s4-dish" id="s4-dl"></div>
        {brackets("s4-bk", 70, 100, 160, 160, 60)}<div class="s4-cap ah-tag" style="position:absolute">HARNESS</div>
        <div class="ring" id="s4-ring" style="border-radius:0 0 150px 150px; top:70px; height:230px"></div></div>
      <div id="s4-lets" class="row"><span class="t-label" style="color:var(--yellow)">LET ME SHOW YOU ↓</span></div>
""", """
      fx.rise("#s4-lab", 16.35, { y: 16 });
      fx.maskUp("#s4-h1", 16.5);
      fx.rise("#s4-post, #s4-base, #s4-beam, #s4-piv", 16.4, { y: 40, st: 0.05 });
      fx.rise("#s4-pr, #s4-pl", 16.6, { y: -60, st: 0.1 });
      // model side heavy first (right pan down)
      tl.fromTo("#s4-beam", { rotation: 0 }, { rotation: 12, duration: 0.6, ease: "power2.out", immediateRender: false }, 16.9);
      tl.to("#s4-pr", { y: 81, duration: 0.6, ease: "power2.out" }, 16.9);
      tl.to("#s4-pl", { y: -81, duration: 0.6, ease: "power2.out" }, 16.9);
      fx.maskUp("#s4-k1", 18.35);
      tl.to("#s4-beam", { rotation: 0, duration: 0.9, ease: "elastic.out(1, 0.5)" }, 18.45);
      tl.to("#s4-pr, #s4-pl", { y: 0, duration: 0.9, ease: "elastic.out(1, 0.5)" }, 18.45);
      tl.to("#s4-beam", { rotation: -10, duration: 0.7, ease: "back.out(2)" }, 20.5);
      tl.to("#s4-pl", { y: 68, duration: 0.7, ease: "back.out(2)" }, 20.5);
      tl.to("#s4-pr", { y: -68, duration: 0.7, ease: "back.out(2)" }, 20.5);
      fx.ringPulse("#s4-ring", 20.7);
      fx.rise("#s4-lets", 21.15, { y: 20 });
      tl.to("#s4-cam", { scale: 1.9, x: 520, y: -150, filter: "blur(14px)", duration: 0.45, ease: "power3.in" }, 22.6);
""", blob=("#136052", 540, 1200), exit_t=22.9)

# ---------------------------------------------------------------- s5 core + files
make("s5", """
    #s5-lab { top: 210px; } #s5-h { top: 250px; } #s5-k { top: 400px; }
    #s5-svg { left: 0; top: 0; width: 1080px; height: 1920px; }
    .s5-ch { position: absolute; left: 500px; top: 900px; width: 80px; height: 80px; border-radius: 50%; background: #0b2f29; border: 2px solid var(--lime); color: var(--lime); display: flex; align-items: center; justify-content: center; }
    #s5-ed { left: 760px; top: 1200px; } #s5-ed2 { left: 425px; top: 1200px; }
    .s5-edt { position: absolute; padding: 4px 16px; border-radius: 16px; background: var(--yellow); color: var(--ink); font-family: var(--font-en); font-weight: 900; font-size: 22px; letter-spacing: .12em; direction: ltr; }
    #s5-cap { top: 1640px; }
""", f"""
      <div id="s5-lab" class="row"><span class="t-label">WHAT THE MODEL NEEDS</span></div>
      <div id="s5-h" class="row t-h2"><span class="mask"><span class="in" id="s5-h1">الموديل بيولّد كود</span></span></div>
      <div id="s5-k" class="row t-h2 ah-y"><span class="mask"><span class="in" id="s5-k1">بس يوصل للملفات إزاي؟</span></span></div>
      <svg id="s5-svg" class="abs" viewBox="0 0 1080 1920">
        <path id="s5-p1" pathLength="1" d="M600 960 C 760 1040, 875 1100, 875 1240" fill="none" stroke="#b3ce65" stroke-width="5" stroke-dasharray="1" />
        <path id="s5-p2" pathLength="1" d="M540 1000 L 540 1240" fill="none" stroke="#b3ce65" stroke-width="5" />
        <path id="s5-p3" pathLength="1" d="M480 960 C 320 1040, 205 1100, 205 1240" fill="none" stroke="#b3ce65" stroke-width="5" />
      </svg>
      {core("s5-core", 440, 760, 200)}
      <div class="s5-ch" id="s5-c1"><svg width="40" height="40"><use href="#i-code" /></svg></div>
      <div class="s5-ch" id="s5-c2"><svg width="40" height="40"><use href="#i-code" /></svg></div>
      <div class="s5-ch" id="s5-c3"><svg width="40" height="40"><use href="#i-code" /></svg></div>
      <div class="ah-file" id="s5-f1" style="left:760px; top:1250px"><b>app.js</b></div>
      <div class="ah-file" id="s5-f2" style="left:425px; top:1250px"><b>api.js</b></div>
      <div class="ah-file" id="s5-f3" style="left:90px; top:1250px"><b>style.css</b></div>
      <div class="s5-edt" id="s5-e1" style="left:800px; top:1230px">EDIT</div>
      <div class="s5-edt" id="s5-e2" style="left:465px; top:1230px">EDIT</div>
      <div id="s5-cap" class="row"><span class="t-label" style="color:var(--lime)">FILES · EDITS</span></div>
""", """
      fx.rise("#s5-lab", 23.15, { y: 16 });
      fx.maskUp("#s5-h1", 23.25);
      fx.pop("#s5-core", 23.3, { from: 0.4, e: "expo.out", d: 0.6 });
      tl.fromTo("#s5-core-g", { rotation: 0 }, { rotation: 200, duration: 6, ease: "none" }, 23.1);
      // code chips burst out of the engine
      [["#s5-c1", 260, -200], ["#s5-c2", -280, -160], ["#s5-c3", 40, -300]].forEach(([s, x, y], i) => {
        tl.fromTo(s, { opacity: 0, x: 0, y: 0, scale: 0.3 }, { opacity: 1, x, y, scale: 1, duration: 0.55, ease: "back.out(1.6)" }, 24.4 + i * 0.1);
        tl.to(s, { opacity: 0, scale: 0.5, duration: 0.3 }, 25.9 + i * 0.05);
      });
      fx.maskUp("#s5-k1", 25.15);
      fx.draw("#s5-p1, #s5-p2, #s5-p3", 26.2, 0.45);
      fx.pop("#s5-f1, #s5-f2, #s5-f3", 26.35, { from: 0.4, st: 0.12 });
      fx.pop("#s5-e1", 27.2, { from: 0.2 });
      tl.to("#s5-f1", { borderColor: "#ffec5c", duration: 0.2 }, 27.2);
      fx.pop("#s5-e2", 28.2, { from: 0.2 });
      tl.to("#s5-f2", { borderColor: "#ffec5c", duration: 0.2 }, 28.2);
      fx.rise("#s5-cap", 27.4, { y: 16 });
      fx.whipOut("#s5-cam", 28.85, -900);
""", blob=("#136052", 540, 900), exit_t=28.95)

# ---------------------------------------------------------------- s6 split code into files
make("s6", """
    #s6-lab { top: 210px; } #s6-h { top: 250px; }
    #s6-code { left: 190px; top: 520px; width: 700px; height: 470px; }
    #s6-f1 { left: 700px; top: 1250px; } #s6-f2 { left: 150px; top: 1250px; }
    .s6-n { position: absolute; top: -26px; left: 50%; transform: translateX(-50%); width: 56px; height: 56px; border-radius: 50%; background: var(--lime); color: var(--ink); font-family: var(--font-en); font-weight: 900; font-size: 24px; display: flex; align-items: center; justify-content: center; }
    #s6-cap { top: 1640px; }
""", f"""
      <div id="s6-lab" class="row"><span class="t-label">ONE CODE · MANY FILES</span></div>
      <div id="s6-h" class="row t-h2"><span class="mask"><span class="in" id="s6-h1">جزء هنا… وجزء هناك</span></span></div>
      <div id="s6-code" class="ah-code">
        <div id="s6-ga">{lines("s6-a", [(70, L), (52, L), (84, L)])}</div>
        <div id="s6-gb" style="margin-top:20px">{lines("s6-b", [(60, Y), (78, Y), (40, Y)])}</div>
      </div>
      <div class="ah-file" id="s6-f1"><div class="s6-n">01</div><b>app.js</b></div>
      <div class="ah-file" id="s6-f2"><div class="s6-n">02</div><b>api.js</b></div>
      <div class="ring" id="s6-r1" style="left:700px; top:1250px; width:230px; height:280px; border-radius:22px"></div>
      <div class="ring" id="s6-r2" style="left:150px; top:1250px; width:230px; height:280px; border-radius:22px"></div>
""", """
      fx.rise("#s6-lab", 29.05, { y: 16 });
      fx.maskUp("#s6-h1", 29.15);
      fx.pop("#s6-code", 29.1, { from: 0.85, e: "power3.out" });
      fx.pop("#s6-f1, #s6-f2", 29.4, { from: 0.5, st: 0.1 });
      tl.fromTo("#s6-ga", { boxShadow: "0 0 0 0 rgba(179,206,101,0)" }, { boxShadow: "0 0 0 6px rgba(179,206,101,.6)", duration: 0.2 }, 30.4);
      tl.fromTo("#s6-ga", { x: 0, y: 0, scale: 1, opacity: 1 }, { x: 330, y: 720, scale: 0.3, opacity: 0, duration: 0.6, ease: "power3.in", immediateRender: false }, 30.9);
      fx.ringPulse("#s6-r1", 31.5);
      tl.fromTo("#s6-gb", { x: 0, y: 0, scale: 1, opacity: 1 }, { x: -220, y: 600, scale: 0.3, opacity: 0, duration: 0.6, ease: "power3.in", immediateRender: false }, 32.4);
      fx.ringPulse("#s6-r2", 33.0);
      tl.to("#s6-code", { opacity: 0.25, duration: 0.3 }, 33.0);
""", blob=("#136052", 540, 1300), exit_t=33.45)

# ---------------------------------------------------------------- s7 order + progress
make("s7", """
    #s7-lab { top: 210px; } #s7-h { top: 250px; } #s7-k { top: 1080px; }
    #s7-line { left: 225px; top: 798px; width: 630px; height: 8px; border-radius: 4px; background: rgba(246,248,240,.2); }
    #s7-lf { position: absolute; inset: 0; background: var(--lime); transform-origin: 100% 50%; border-radius: 4px; }
    .s7-st { position: absolute; top: 725px; width: 150px; height: 150px; border-radius: 50%; border: 5px solid rgba(246,248,240,.3); background: #0b2f29; color: var(--fg); font-family: var(--font-en); font-weight: 900; font-size: 52px; display: flex; align-items: center; justify-content: center; }
    #s7-tr { left: 110px; top: 1300px; width: 860px; }
    #s7-pct { left: 0; right: 0; top: 1380px; text-align: center; font-family: var(--font-en); font-size: 120px; font-weight: 900; direction: ltr; }
    #s7-ck { left: 470px; top: 1560px; width: 140px; height: 140px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
""", """
      <div id="s7-lab" class="row"><span class="t-label">ORDER · PROGRESS</span></div>
      <div id="s7-h" class="row t-h1"><span class="mask"><span class="in" id="s7-h1">بترتيب معيّن</span></span></div>
      <div id="s7-line" class="abs"><div id="s7-lf"></div></div>
      <div class="s7-st" id="s7-s1" style="left:780px">01</div>
      <div class="s7-st" id="s7-s2" style="left:465px">02</div>
      <div class="s7-st" id="s7-s3" style="left:150px">03</div>
      <div id="s7-k" class="row t-h2"><span class="mask"><span class="in" id="s7-k1">ويتابع الـ<span class="lat">Progress</span></span></span></div>
      <div id="s7-tr" class="ah-track"><div class="ah-fill" id="s7-fill" style="background:linear-gradient(270deg, #b3ce65, #ffec5c)"></div></div>
      <div id="s7-pct" class="abs num"><span id="s7-n">0</span>%</div>
      <div id="s7-ck" class="abs"><svg width="80" height="80"><use href="#i-check" /></svg></div>
""", """
      fx.rise("#s7-lab", 33.65, { y: 16 });
      fx.maskUp("#s7-h1", 33.7);
      fx.pop("#s7-s1, #s7-s2, #s7-s3", 33.8, { from: 0.4, st: 0.08 });
      tl.fromTo("#s7-line", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 33.8);
      fx.meter("#s7-lf", 34.2, 0.8, 1, { e: "power1.inOut" });
      ["#s7-s1", "#s7-s2", "#s7-s3"].forEach((s, i) => {
        tl.to(s, { backgroundColor: "#b3ce65", color: "#0d0d0d", borderColor: "#b3ce65", scale: 1.12, duration: 0.18 }, 34.2 + i * 0.36);
        tl.to(s, { scale: 1, duration: 0.2 }, 34.38 + i * 0.36);
      });
      fx.maskUp("#s7-k1", 35.05);
      tl.fromTo("#s7-tr", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 35.1);
      fx.meter("#s7-fill", 35.2, 1.3, 1, { e: "power2.inOut" });
      fx.counter("#s7-n", 35.2, 36.5, 0, 100, { ar: false });
      fx.pop("#s7-ck", 36.55, { from: 0.2 });
""", blob=("#136052", 540, 800), exit_t=37.2)

# ---------------------------------------------------------------- s8 SIGNATURE: harness lock
make("s8", """
    #s8-lab { top: 210px; } #s8-h { top: 250px; }
    .s8-chip { position: absolute; padding: 0 26px; height: 66px; border-radius: 33px; border: 3px solid var(--lime); background: #0b2f29; color: var(--lime);
      font-family: var(--font-en); font-weight: 900; font-size: 26px; letter-spacing: .14em; display: flex; align-items: center; direction: ltr; white-space: nowrap; }
    #s8-q1 { left: 120px; top: 600px; } #s8-q2 { left: 700px; top: 600px; } #s8-q3 { left: 120px; top: 1290px; } #s8-q4 { left: 660px; top: 1290px; }
    #s8-k { top: 1420px; } #s8-big { top: 1500px; font-size: 170px; }
    #s8-glow { left: 140px; top: 560px; width: 800px; height: 800px; border-radius: 80px; background: radial-gradient(circle, rgba(179,206,101,.35), transparent 70%); }
""", f"""
      <div id="s8-lab" class="row"><span class="t-label">THE HARNESS</span></div>
      <div id="s8-h" class="row t-h2"><span class="mask"><span class="in" id="s8-h1">لازم يبقى جوّه برنامج</span></span></div>
      <div id="s8-glow" class="abs"></div>
      {core("s8-core", 400, 820, 280)}
      <div class="s8-chip" id="s8-q1">FILES</div><div class="s8-chip" id="s8-q2">EDIT</div>
      <div class="s8-chip" id="s8-q3">ORDER</div><div class="s8-chip" id="s8-q4">PROGRESS</div>
      <div id="s8-frame" class="abs" style="left:0; top:0; width:1080px; height:1920px">{brackets("s8-b", 220, 640, 640, 640, 160)}</div>
      <div id="s8-k" class="row t-h3"><span class="mask"><span class="in" id="s8-k1">البرنامج ده هو الـ</span></span></div>
      <div id="s8-big" class="row ah-en ah-l" style="text-shadow:0 0 70px rgba(179,206,101,.6)"><span id="s8-big1">HARNESS</span></div>
""", """
      fx.rise("#s8-lab", 37.35, { y: 16 });
      fx.maskUp("#s8-h1", 37.4);
      fx.pop("#s8-core", 37.35, { from: 0.5, e: "expo.out", d: 0.6 });
      tl.fromTo("#s8-core-g", { rotation: 0 }, { rotation: 240, duration: 5.2, ease: "none" }, 37.3);
      fx.pop("#s8-q1, #s8-q2, #s8-q3, #s8-q4", 37.7, { from: 0.4, st: 0.1 });
      // chips get pulled into the corners and the brackets slam shut around the engine
      tl.to("#s8-q1", { x: 160, y: 120, scale: 0.4, opacity: 0, duration: 0.3, ease: "power3.in" }, 38.55);
      tl.to("#s8-q2", { x: -80, y: 120, scale: 0.4, opacity: 0, duration: 0.3, ease: "power3.in" }, 38.6);
      tl.to("#s8-q3", { x: 160, y: -120, scale: 0.4, opacity: 0, duration: 0.3, ease: "power3.in" }, 38.65);
      tl.to("#s8-q4", { x: -40, y: -120, scale: 0.4, opacity: 0, duration: 0.3, ease: "power3.in" }, 38.7);
      [["#s8-b-a", -260, -260], ["#s8-b-b", 260, -260], ["#s8-b-c", -260, 260], ["#s8-b-d", 260, 260]].forEach(([s, x, y], i) => {
        tl.fromTo(s, { opacity: 0, x, y, scale: 1.6, filter: "blur(14px)" }, { opacity: 1, x: 0, y: 0, scale: 1, filter: "blur(0px)", duration: 0.26, ease: "expo.out" }, 38.82 + i * 0.04);
      });
      fx.shake("#s8-cam", 39.05, 18, 7);
      tl.fromTo("#s8-glow", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power2.out" }, 39.0);
      fx.ringPulse("#s8-core-r1, #s8-core-r2", 39.1);
      fx.breathe("#s8-frame", 39.4, 2.6, 0.015, 1.3);
      fx.maskUp("#s8-k1", 40.05);
      fx.letterDrop("#s8-big1", 41.75, { st: 0.04 });
""", blob=("#136052", 540, 960), exit_t=42.2)

# ---------------------------------------------------------------- s9 sources + harness lineup
make("s9", """
    #s9-lab { top: 210px; } #s9-h { top: 250px; }
    .s9-src { position: absolute; top: 420px; width: 400px; height: 120px; border-radius: 24px; border: 3px dashed rgba(179,206,101,.6); display: flex; align-items: center; justify-content: center; gap: 16px;
      font-family: var(--font-en); font-weight: 900; font-size: 28px; letter-spacing: .14em; color: var(--lime); direction: ltr; }
    #s9-s1 { left: 580px; } #s9-s2 { left: 100px; }
    #s9-k { top: 610px; }
    .s9-h { position: absolute; left: 110px; width: 860px; height: 190px; border-radius: 34px; border: 4px solid var(--lime); background: linear-gradient(270deg, rgba(179,206,101,.14), rgba(179,206,101,.02));
      display: flex; align-items: center; justify-content: space-between; padding: 0 50px; direction: ltr; }
    .s9-h b { font-family: var(--font-en); font-weight: 900; font-size: 74px; color: var(--fg); }
    .s9-h i { font-style: normal; font-family: var(--font-en); font-weight: 900; font-size: 26px; letter-spacing: .2em; color: var(--lime); }
    #s9-h1 { top: 790px; } #s9-h2 { top: 1010px; } #s9-h3 { top: 1230px; }
    #s9-more { left: 0; right: 0; top: 1480px; text-align: center; }
""", """
      <div id="s9-lab" class="row"><span class="t-label">HOW TO CHOOSE</span></div>
      <div id="s9-h" class="row t-h3"><span class="mask"><span class="in" id="s9-ht">مصدرين يساعدوك تختار</span></span></div>
      <div class="s9-src" id="s9-s1"><span>SOURCE</span><span style="color:var(--yellow)">01</span></div>
      <div class="s9-src" id="s9-s2"><span>SOURCE</span><span style="color:var(--yellow)">02</span></div>
      <div id="s9-k" class="row t-h3 muted"><span class="mask"><span class="in" id="s9-k1">أنهي <span class="lat" style="color:var(--lime)">Agent Harness</span> تستخدم؟</span></span></div>
      <div class="s9-h" id="s9-h1"><b>Claude Code</b><i>HARNESS 01</i></div>
      <div class="s9-h" id="s9-h2"><b>OpenCode</b><i>HARNESS 02</i></div>
      <div class="s9-h" id="s9-h3"><b>Pi</b><i>HARNESS 03</i></div>
      <div id="s9-more" class="abs"><span class="pill">أو غيرهم…</span></div>
""", """
      fx.rise("#s9-lab", 42.35, { y: 16 });
      fx.maskUp("#s9-ht", 42.5);
      fx.pop("#s9-s1", 42.95, { from: 0.4 });
      fx.pop("#s9-s2", 43.15, { from: 0.4 });
      fx.maskUp("#s9-k1", 45.1);
      [["#s9-h1", 47.1], ["#s9-h2", 47.75], ["#s9-h3", 48.3]].forEach(([s, t]) => {
        tl.fromTo(s, { opacity: 0, x: 700, filter: "blur(16px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, t);
      });
      fx.pop("#s9-more", 48.9, { from: 0.4 });
""", blob=("#136052", 540, 1000), exit_t=49.15)

# ---------------------------------------------------------------- s10 benchmarks flip
def rows(prefix, n, widths, color, icon):
    out = []
    for i in range(n):
        out.append(f'<div class="s10-row" style="top:{150 + i * 120}px"><span class="s10-rk">0{i + 1}</span>'
                   f'<span class="s10-ic" style="background:{color}"><svg width="26" height="26"><use href="#{icon}" /></svg></span>'
                   f'<div class="ah-track" style="position:relative; flex:1; height:30px"><div class="ah-fill {prefix}-bar" style="background:{color}; width:{widths[i]}%"></div></div></div>')
    return "".join(out)


make("s10", """
    #s10-lab { top: 210px; } #s10-h { top: 250px; font-size: 120px; }
    #s10-board { left: 90px; top: 500px; width: 900px; height: 820px; perspective: 1600px; }
    .s10-face { position: absolute; inset: 0; border-radius: 30px; background: rgba(255,255,255,.05); border: 2px solid var(--edge); backface-visibility: hidden; }
    .s10-hd { position: absolute; left: 40px; right: 40px; top: 46px; display: flex; justify-content: space-between; direction: ltr; font-family: var(--font-en); font-weight: 900; font-size: 30px; letter-spacing: .16em; }
    .s10-row { position: absolute; left: 40px; right: 40px; height: 80px; display: flex; align-items: center; gap: 22px; direction: ltr; }
    .s10-rk { font-family: var(--font-en); font-weight: 900; font-size: 34px; color: var(--fg-muted); width: 56px; }
    .s10-ic { width: 54px; height: 54px; border-radius: 50%; color: var(--ink); display: flex; align-items: center; justify-content: center; flex: none; }
    .s10-ft { position: absolute; left: 40px; bottom: 30px; font-size: 18px; }
    #s10-k { top: 1420px; }
""", f"""
      <div id="s10-lab" class="row"><span class="t-label">THE LEADERBOARD</span></div>
      <div id="s10-h" class="row ah-en"><span id="s10-h1">Benchmarks</span></div>
      <div id="s10-board" class="abs">
        <div class="s10-face" id="s10-fa"><div class="s10-hd"><span style="color:var(--yellow)">AI MODELS</span><span class="muted">SCORE</span></div>
          {rows("s10a", 5, [92, 84, 71, 63, 50], "var(--yellow)", "i-bolt")}<div class="s10-ft t-label">ILLUSTRATION</div></div>
        <div class="s10-face" id="s10-fb"><div class="s10-hd"><span style="color:var(--lime)">CODING HARNESSES</span><span class="muted">SCORE</span></div>
          {rows("s10b", 5, [88, 80, 74, 60, 47], "var(--lime)", "i-code")}<div class="s10-ft t-label">ILLUSTRATION</div></div>
      </div>
      <div id="s10-k" class="row t-h2"><span class="mask"><span class="in" id="s10-k1">والـ<span class="lat ah-l">Harness</span> كمان ليه ترتيب</span></span></div>
""", """
      fx.rise("#s10-lab", 49.35, { y: 16 });
      fx.letterDrop("#s10-h1", 49.9, { st: 0.035 });
      fx.pop("#s10-board", 50.3, { from: 0.85, e: "power3.out" });
      tl.fromTo("#s10-fb", { rotationX: -90, opacity: 0 }, { rotationX: -90, opacity: 0, duration: 0.01 }, 49.3);
      tl.fromTo(".s10a-bar", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out", stagger: 0.12 }, 50.6);
      tl.to("#s10-fa", { rotationX: 90, opacity: 0, duration: 0.28, ease: "power2.in" }, 52.95);
      tl.to("#s10-fb", { rotationX: 0, opacity: 1, duration: 0.35, ease: "back.out(1.6)" }, 53.22);
      tl.fromTo(".s10b-bar", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out", stagger: 0.12, immediateRender: false }, 53.4);
      fx.maskUp("#s10-k1", 53.3);
""", blob=("#136052", 540, 900), exit_t=55.8)

# ---------------------------------------------------------------- s11 test bench engine swap
make("s11", """
    #s11-lab { top: 210px; } #s11-h { top: 250px; }
    #s11-ch { left: 190px; top: 560px; width: 700px; height: 700px; }
    #s11-slot { left: 390px; top: 760px; width: 300px; height: 300px; border-radius: 50%; border: 4px dashed rgba(246,248,240,.3); }
    #s11-ea, #s11-eb { left: 410px; top: 780px; width: 260px; height: 260px; }
    #s11-tl { top: 1340px; }
    #s11-tr { left: 190px; top: 1400px; width: 600px; }
    #s11-ck { left: 820px; top: 1380px; width: 74px; height: 74px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
    .s11-q { position: absolute; top: 1560px; width: 54px; height: 54px; border-radius: 50%; }
""", f"""
      <div id="s11-lab" class="row"><span class="t-label">TEST BENCH</span></div>
      <div id="s11-h" class="row t-h3"><span class="mask"><span class="in" id="s11-h1">نفس الـ<span class="lat ah-l">Harness</span>… ونبدّل الموديل</span></span></div>
      <div id="s11-ch" class="ah-chassis"><span class="nm">Claude Code</span></div>
      <div id="s11-slot" class="abs"></div>
      <div id="s11-ea" class="abs">{core("s11-ca", 0, 0, 260, "Fable", 280)}</div>
      <div id="s11-eb" class="abs">{core("s11-cb", 0, 0, 260, "GPT-6 Astra", 280)}</div>
      <div id="s11-tl" class="row"><span class="t-label">TEST RUN</span></div>
      <div id="s11-tr" class="ah-track"><div class="ah-fill" id="s11-fill" style="background:var(--lime)"></div></div>
      <div id="s11-ck" class="abs"><svg width="44" height="44"><use href="#i-check" /></svg></div>
      <div class="s11-q ah-core" id="s11-q1" style="left:600px"></div><div class="s11-q ah-core" id="s11-q2" style="left:510px"></div><div class="s11-q ah-core" id="s11-q3" style="left:420px"></div>
""", """
      fx.rise("#s11-lab", 55.95, { y: 16 });
      fx.maskUp("#s11-h1", 56.05);
      fx.pop("#s11-ch", 56.7, { from: 0.8, e: "power3.out" });
      fx.rise("#s11-slot", 56.9, { y: 0, s: 0.8 });
      tl.fromTo("#s11-ca-g, #s11-cb-g", { rotation: 0 }, { rotation: 400, duration: 9, ease: "none" }, 55.9);
      tl.fromTo("#s11-ea", { opacity: 0, x: 900 }, { opacity: 1, x: 0, duration: 0.42, ease: "power3.out" }, 58.5);
      fx.shake("#s11-ch", 58.92, 8, 5);
      fx.ringPulse("#s11-ca-r1, #s11-ca-r2", 58.95);
      fx.rise("#s11-tl, #s11-tr", 59.4, { y: 16 });
      fx.meter("#s11-fill", 59.7, 0.6, 1, { e: "power2.inOut" });
      fx.pop("#s11-ck", 60.3, { from: 0.2 });
      tl.to("#s11-ea", { x: -900, opacity: 0, duration: 0.4, ease: "power3.in" }, 60.5);
      tl.to("#s11-fill", { scaleX: 0, duration: 0.3 }, 60.6);
      tl.to("#s11-ck", { opacity: 0, scale: 0.4, duration: 0.2 }, 60.6);
      tl.fromTo("#s11-eb", { opacity: 0, x: 900 }, { opacity: 1, x: 0, duration: 0.42, ease: "power3.out" }, 62.05);
      tl.fromTo("#s11-cb", { filter: "hue-rotate(0deg)" }, { filter: "hue-rotate(-28deg)", duration: 0.01 }, 61.9);
      fx.shake("#s11-ch", 62.46, 8, 5);
      fx.ringPulse("#s11-cb-r1, #s11-cb-r2", 62.5);
      tl.to("#s11-fill", { scaleX: 1, duration: 0.6, ease: "power2.inOut" }, 63.45);
      tl.to("#s11-ck", { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 64.05);
      fx.pop("#s11-q1, #s11-q2, #s11-q3", 64.15, { from: 0.2, st: 0.08 });
""", blob=("#136052", 540, 900), exit_t=64.6)

# ---------------------------------------------------------------- s12 dashboard time + cost
def bars(prefix, ws, color):
    return "".join(f'<div class="s12-r"><span class="s12-d" style="background:{c}"></span><div class="ah-track" style="position:relative; flex:1; height:30px">'
                   f'<div class="ah-fill" id="{prefix}{i}" style="background:{color}; width:{w}%"></div></div></div>'
                   for i, (w, c) in enumerate(ws, 1))


make("s12", """
    #s12-lab { top: 210px; } #s12-h { top: 250px; }
    #s12-win { left: 80px; top: 440px; width: 920px; height: 1180px; }
    .s12-sec { position: absolute; left: 50px; right: 50px; }
    .s12-hd { display: flex; align-items: center; gap: 16px; direction: rtl; margin-bottom: 26px; }
    .s12-hd .ic { width: 64px; height: 64px; border-radius: 50%; background: var(--teal); color: #fff; display: flex; align-items: center; justify-content: center; }
    .s12-hd b { font-size: 46px; font-weight: 800; color: var(--ink); }
    .s12-hd i { font-style: normal; font-family: var(--font-en); font-size: 20px; font-weight: 800; letter-spacing: .16em; color: #5a6b62; direction: ltr; margin-right: auto; }
    .s12-r { display: flex; align-items: center; gap: 18px; height: 70px; direction: ltr; }
    .s12-d { width: 34px; height: 34px; border-radius: 50%; flex: none; }
    #s12-win .ah-track { background: #e4e7d8; }
    #s12-sa { top: 100px; } #s12-sb { top: 560px; }
    #s12-ft { position: absolute; left: 50px; bottom: 34px; font-family: var(--font-en); font-size: 18px; font-weight: 800; letter-spacing: .2em; color: #8a9a90; direction: ltr; }
    .s12-tg { position: absolute; padding: 4px 16px; border-radius: 16px; font-weight: 800; font-size: 28px; }
""", f"""
      <div id="s12-lab" class="row"><span class="t-label">SOURCE 01 · BENCHMARK</span></div>
      <div id="s12-h" class="row t-h2"><span class="mask"><span class="in" id="s12-h1">مصدر هيفيدك جدًا</span></span></div>
      <div id="s12-win" class="window"><div class="bar"><i></i><i></i><i></i><b>CODING HARNESS BENCHMARK</b></div>
        <div class="s12-sec" id="s12-sa"><div class="s12-hd"><span class="ic"><svg width="36" height="36"><use href="#i-clock" /></svg></span><b>الوقت لكل تاسك</b><i>TIME / TASK</i></div>
          {bars("s12-a", [(78, "#b3ce65"), (52, "#ffec5c"), (91, "#ff5a33"), (40, "#2c8a76")], "#136052")}</div>
        <div class="s12-sec" id="s12-sb"><div class="s12-hd"><span class="ic"><svg width="36" height="36"><use href="#i-bolt" /></svg></span><b>التكلفة لكل تاسك</b><i>COST / TASK</i></div>
          {bars("s12-b", [(46, "#b3ce65"), (88, "#ffec5c"), (64, "#ff5a33"), (30, "#2c8a76")], "#136052")}</div>
        <div class="s12-tg" id="s12-hi" style="left:110px; top:733px; background:#ff5a33; color:#fff">أكتر</div>
        <div class="s12-tg" id="s12-lo" style="left:110px; top:873px; background:#b3ce65; color:#0d0d0d">أقل</div>
        <div id="s12-ft">ILLUSTRATION · NOT REAL DATA</div>
      </div>
""", """
      fx.rise("#s12-lab", 64.85, { y: 16 });
      fx.maskUp("#s12-h1", 64.95);
      fx.pop("#s12-win", 65.6, { from: 0.85, e: "power3.out" });
      fx.rise("#s12-sa", 67.3, { y: 30 });
      tl.fromTo("#s12-a1, #s12-a2, #s12-a3, #s12-a4", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.out", stagger: 0.12 }, 67.7);
      fx.rise("#s12-sb", 69.5, { y: 30 });
      tl.fromTo("#s12-b1, #s12-b2, #s12-b3, #s12-b4", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.out", stagger: 0.12 }, 70.2);
      tl.to("#s12-b2", { backgroundColor: "#ff5a33", duration: 0.2 }, 70.95);
      fx.pop("#s12-hi", 70.95, { from: 0.3 });
      tl.to("#s12-b4", { backgroundColor: "#437f3e", duration: 0.2 }, 71.55);
      fx.pop("#s12-lo", 71.55, { from: 0.3 });
""", blob=("#136052", 540, 1000), exit_t=72.5)

# ---------------------------------------------------------------- s13 myth strike
make("s13", """
    #s13-lab { top: 360px; }
    #s13-card { left: 90px; top: 440px; width: 900px; height: 380px; }
    #s13-a { top: 70px; } #s13-b { top: 200px; }
    #s13-st { left: 60px; top: 560px; width: 960px; height: 140px; }
    #s13-x { left: 900px; top: 400px; width: 120px; height: 120px; }
    #s13-big { top: 1060px; font-size: 170px; } #s13-k { top: 1290px; }
""", """
      <div id="s13-lab" class="row"><span class="t-label" style="color:var(--orange)">MYTH</span></div>
      <div id="s13-card" class="card">
        <div id="s13-a" class="row t-h2"><span class="mask"><span class="in" id="s13-a1">الموديل الأرخص</span></span></div>
        <div id="s13-b" class="row t-h2 muted"><span class="mask"><span class="in" id="s13-b1">= أرخص في المهام؟</span></span></div>
      </div>
      <svg id="s13-st" class="abs" viewBox="0 0 960 140"><path id="s13-sp" pathLength="1" d="M20 100 C 300 40, 620 110, 940 30" fill="none" stroke="#ff5a33" stroke-width="14" stroke-linecap="round" /></svg>
      <div id="s13-x" class="xbadge" style="width:120px; height:120px"><svg width="70" height="70" style="color:#fff"><use href="#i-x" /></svg></div>
      <div id="s13-big" class="row ah-en ah-l" style="text-shadow:0 0 60px rgba(179,206,101,.5)"><span id="s13-big1" style="display:inline-block">HARNESS</span></div>
      <div id="s13-k" class="row t-h1"><span id="s13-k1" style="display:inline-block">بيفرق</span></div>
""", """
      fx.rise("#s13-lab", 72.75, { y: 16 });
      fx.pop("#s13-card", 72.8, { from: 0.85, e: "power3.out" });
      fx.maskUp("#s13-a1", 73.4);
      fx.maskUp("#s13-b1", 75.0);
      fx.strike("#s13-sp", 75.85, "#s13-x");
      tl.to("#s13-card", { filter: "grayscale(0.9) brightness(0.6)", duration: 0.4 }, 76.0);
      tl.fromTo("#s13-big1", { opacity: 0, scale: 2.4, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.28, ease: "expo.out" }, 76.65);
      tl.fromTo("#s13-k1", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.28, ease: "expo.out" }, 77.3);
      fx.shake("#s13-cam", 77.4, 16, 7);
""", blob=("#5a2a1c", 540, 700), exit_t=77.9)

# ---------------------------------------------------------------- s14 Arena AI article
make("s14", """
    #s14-lab { top: 210px; } #s14-h { top: 250px; }
    #s14-win { left: 110px; top: 470px; width: 860px; height: 820px; }
    #s14-new { position: absolute; right: 50px; top: 100px; padding: 6px 22px; border-radius: 22px; background: var(--orange); color: #fff; font-family: var(--font-en); font-weight: 900; font-size: 24px; letter-spacing: .14em; direction: ltr; }
    #s14-days { position: absolute; right: 200px; top: 98px; font-size: 30px; font-weight: 700; color: #5a6b62; }
    #s14-t { position: absolute; right: 50px; left: 50px; top: 200px; font-size: 58px; font-weight: 900; line-height: 1.35; color: var(--ink); direction: rtl; }
    #s14-t .hl > .band { background: var(--lime); }
    #s14-body { position: absolute; left: 50px; right: 50px; top: 480px; }
    #s14-body span { display: block; height: 18px; border-radius: 9px; background: #e1e4d4; margin-bottom: 26px; margin-left: auto; }
    #s14-name { top: 1380px; font-size: 130px; }
    #s14-q { left: 0; right: 0; top: 1590px; text-align: center; }
""", """
      <div id="s14-lab" class="row"><span class="t-label">SOURCE 02 · ARTICLE</span></div>
      <div id="s14-h" class="row t-h2"><span class="mask"><span class="in" id="s14-h1">مصدر تاني… لسه طالع</span></span></div>
      <div id="s14-win" class="window"><div class="bar"><i></i><i></i><i></i><b>ARENA AI · BLOG</b></div>
        <div id="s14-new">NEW</div><div id="s14-days">من كام يوم</div>
        <div id="s14-t">اختيار الـ<span class="hl"><span class="band" id="s14-band"></span><span class="txt lat">Harness</span></span><br/>بيغيّر التكلفة</div>
        <div id="s14-body"><span style="width:100%"></span><span style="width:86%"></span><span style="width:94%"></span><span style="width:70%"></span><span style="width:88%"></span><span style="width:60%"></span></div>
      </div>
      <div id="s14-name" class="row ah-en"><span class="mask"><span class="in" id="s14-n1">Arena AI</span></span></div>
      <div id="s14-q" class="t-label">PARAPHRASED</div>
""", """
      fx.rise("#s14-lab", 78.0, { y: 16 });
      fx.maskUp("#s14-h1", 78.1);
      tl.fromTo("#s14-win", { opacity: 0, y: 400, rotation: 4 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "expo.out" }, 79.15);
      fx.pop("#s14-new", 79.95, { from: 0.3 });
      fx.rise("#s14-days", 80.2, { y: 10 });
      fx.maskUp("#s14-n1", 81.6);
      fx.rise("#s14-t", 82.5, { y: 20 });
      fx.band("#s14-band", 83.85);
      fx.rise("#s14-q", 83.0, { y: 10 });
""", blob=("#136052", 540, 900), exit_t=84.2)

# ---------------------------------------------------------------- s15 cost gauge
make("s15", """
    #s15-lab { top: 210px; } #s15-h { top: 250px; } #s15-k { top: 390px; }
    #s15-g { left: 140px; top: 620px; width: 800px; height: 420px; }
    #s15-nd { left: 532px; top: 640px; width: 16px; height: 400px; border-radius: 8px; background: var(--fg); transform-origin: 50% 100%; }
    #s15-hub { left: 500px; top: 1000px; width: 80px; height: 80px; border-radius: 50%; background: var(--yellow); }
    .s15-hc { position: absolute; top: 1160px; }
    #s15-ha { left: 590px; } #s15-hb { left: 150px; }
    #s15-ax { left: 140px; top: 1330px; width: 800px; height: 330px; }
    #s15-cl { top: 1690px; }
""", """
      <div id="s15-lab" class="row"><span class="t-label">COST METER</span></div>
      <div id="s15-h" class="row t-h2"><span class="mask"><span class="in" id="s15-h1">لما الـ<span class="lat ah-l">Harness</span> يختلف</span></span></div>
      <div id="s15-k" class="row t-h1"><span class="mask"><span class="in" id="s15-k1"><span class="hl"><span class="band" id="s15-band" style="background:var(--orange)"></span><span class="txt" style="color:#fff">التكلفة</span></span> بتفرق</span></span></div>
      <svg id="s15-g" class="abs" viewBox="0 0 800 420">
        <defs><linearGradient id="s15-grad" x1="0" x2="1"><stop offset="0" stop-color="#b3ce65" /><stop offset=".55" stop-color="#ffec5c" /><stop offset="1" stop-color="#ff5a33" /></linearGradient></defs>
        <path id="s15-arc" pathLength="1" d="M40 400 A 360 360 0 0 1 760 400" fill="none" stroke="url(#s15-grad)" stroke-width="44" stroke-linecap="round" />
      </svg>
      <div id="s15-nd" class="abs"></div><div id="s15-hub" class="abs"></div>
      <div class="ah-mod s15-hc" id="s15-ha"><span class="lat">HARNESS A</span></div>
      <div class="ah-mod s15-hc" id="s15-hb" style="border-color:var(--orange)"><span class="lat">HARNESS B</span></div>
      <svg id="s15-ax" class="abs" viewBox="0 0 800 330"><path id="s15-axp" pathLength="1" d="M20 0 V310 H800" fill="none" stroke="rgba(246,248,240,.6)" stroke-width="6" stroke-linecap="round" /></svg>
      <div id="s15-cl" class="row"><span class="t-label" style="color:var(--yellow)">THEY HAVE A CHART ↓</span></div>
""", """
      fx.rise("#s15-lab", 84.35, { y: 16 });
      fx.maskUp("#s15-h1", 84.4);
      fx.draw("#s15-arc", 84.6, 0.7);
      fx.pop("#s15-hub", 84.9, { from: 0.2 });
      tl.fromTo("#s15-nd", { opacity: 0, rotation: -80 }, { opacity: 1, rotation: -55, duration: 0.5, ease: "power2.out" }, 84.9);
      fx.pop("#s15-ha", 85.6, { from: 0.4 });
      tl.to("#s15-nd", { rotation: 62, duration: 0.45, ease: "back.out(2.5)" }, 86.4);
      fx.pop("#s15-hb", 86.4, { from: 0.4 });
      tl.to("#s15-nd", { rotation: -40, duration: 0.4, ease: "back.out(2.5)" }, 87.0);
      tl.to("#s15-nd", { rotation: 72, duration: 0.5, ease: "back.out(3)" }, 87.6);
      fx.maskUp("#s15-k1", 87.45);
      fx.band("#s15-band", 87.7);
      fx.draw("#s15-axp", 88.4, 0.6);
      fx.rise("#s15-cl", 88.6, { y: 16 });
""", blob=("#5a2a1c", 540, 900), exit_t=89.85)

# ---------------------------------------------------------------- s16 the chart (hero)
make("s16", """
    #s16-lab { top: 210px; } #s16-h { top: 250px; }
    #s16-world { position: absolute; inset: 0; transform-origin: 50% 50%; }
    #s16-ch { left: 110px; top: 470px; width: 860px; height: 900px; }
    #s16-zone { left: 140px; top: 480px; width: 400px; height: 420px; border-radius: 40px; background: radial-gradient(circle at 30% 30%, rgba(179,206,101,.45), rgba(179,206,101,.06) 70%); border: 3px dashed var(--lime); }
    #s16-zl { position: absolute; left: 24px; top: 20px; font-family: var(--font-en); font-weight: 900; letter-spacing: .16em; font-size: 22px; color: var(--lime); direction: ltr; }
    .s16-p { position: absolute; width: 50px; height: 50px; margin: -25px 0 0 -25px; border-radius: 50%; }
    .s16-pl { position: absolute; white-space: nowrap; padding: 8px 20px; border-radius: 22px; background: #0b2f29; border: 2px solid var(--edge);
      font-family: var(--font-en); font-weight: 800; font-size: 28px; direction: ltr; }
    #s16-yl { left: 40px; top: 430px; font-size: 34px; font-weight: 800; }
    #s16-xl1 { left: 800px; top: 1400px; font-size: 34px; font-weight: 800; color: var(--orange); }
    #s16-xl2 { left: 130px; top: 1400px; font-size: 34px; font-weight: 800; color: var(--lime); }
    #s16-ar { left: 140px; top: 520px; width: 820px; height: 860px; }
    #s16-best { left: 330px; top: 520px; color: var(--yellow); width: 90px; height: 90px; }
    #s16-k { top: 1500px; }
    #s16-ill { top: 1690px; }
""", """
      <div id="s16-lab" class="row"><span class="t-label">MODEL × HARNESS</span></div>
      <div id="s16-h" class="row t-h3"><span class="mask"><span class="in" id="s16-h1">الموديل مع الـ<span class="lat ah-l">Harness</span></span></span></div>
      <div id="s16-world">
        <div id="s16-zone" class="abs"><span id="s16-zl">SWEET SPOT</span></div>
        <svg id="s16-ch" class="abs" viewBox="0 0 860 900">
          <path id="s16-axis" pathLength="1" d="M30 0 V870 H860" fill="none" stroke="rgba(246,248,240,.7)" stroke-width="6" stroke-linecap="round" />
          <path id="s16-grid" d="M30 290 H860 M30 580 H860 M317 0 V870 M603 0 V870" stroke="rgba(246,248,240,.08)" stroke-width="2" />
        </svg>
        <div id="s16-yl" class="abs">↑ أذكى</div>
        <div id="s16-xl1" class="abs">أغلى ←</div>
        <div id="s16-xl2" class="abs">→ أوفر</div>
        <svg id="s16-ar" class="abs" viewBox="0 0 820 860">
          <path id="s16-a1" pathLength="1" d="M440 500 L650 250" fill="none" stroke="#ffec5c" stroke-width="5" stroke-dasharray="0.02 0.02" />
          <path id="s16-a2" pathLength="1" d="M560 700 H200" fill="none" stroke="#b3ce65" stroke-width="10" stroke-linecap="round" />
          <path id="s16-a2h" pathLength="1" d="M240 670 L196 700 L240 730" fill="none" stroke="#b3ce65" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" />
          <path id="s16-a3" pathLength="1" d="M150 700 V300" fill="none" stroke="#b3ce65" stroke-width="10" stroke-linecap="round" />
          <path id="s16-a3h" pathLength="1" d="M120 340 L150 296 L180 340" fill="none" stroke="#b3ce65" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <div class="s16-p" id="s16-p1" style="left:580px; top:1020px; background:var(--yellow)"></div>
        <div class="s16-pl" id="s16-l1" style="left:470px; top:1060px">Codex + GPT-5.6</div>
        <div class="s16-p" id="s16-p2" style="left:790px; top:770px; background:var(--orange)"></div>
        <div class="s16-pl" id="s16-l2" style="left:610px; top:660px">Codex + Fable 5</div>
        <div class="s16-p ah-core" id="s16-p3" style="left:300px; top:740px; width:70px; height:70px; margin:-35px 0 0 -35px"></div>
        <div class="ring" id="s16-r3" style="left:265px; top:705px; width:70px; height:70px; border-radius:50%"></div>
        <div class="s16-pl" id="s16-l3" style="left:200px; top:800px; border-color:var(--lime); color:var(--lime)">Pi + Fable 5</div>
        <svg id="s16-best" class="abs"><use href="#i-crown" /></svg>
      </div>
      <div id="s16-k" class="row t-h1"><span class="mask"><span class="in" id="s16-k1"><span class="lat ah-l">Pi</span> هو الأفضل</span></span></div>
      <div id="s16-ill" class="row"><span class="t-label">ILLUSTRATION · POSITIONS NOT TO SCALE</span></div>
""", """
      fx.rise("#s16-lab", 90.05, { y: 16 });
      fx.draw("#s16-axis", 90.1, 0.8);
      tl.fromTo("#s16-grid", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 90.5);
      fx.rise("#s16-yl, #s16-xl1, #s16-xl2", 90.6, { y: 14, st: 0.08 });
      fx.rise("#s16-ill", 90.8, { y: 10 });
      fx.maskUp("#s16-h1", 91.5);
      // Codex + GPT-5.6
      fx.pop("#s16-p1", 93.6, { from: 0 });
      fx.rise("#s16-l1", 93.75, { y: 14 });
      tl.to("#s16-world", { scale: 1.18, x: -60, y: -140, duration: 0.9, ease: "power3.inOut" }, 93.4);
      // Codex + Fable 5: smarter and pricier
      tl.to("#s16-world", { scale: 1.12, x: -140, y: 60, duration: 0.9, ease: "power3.inOut" }, 96.2);
      fx.pop("#s16-p2", 96.9, { from: 0 });
      fx.rise("#s16-l2", 97.05, { y: 14 });
      fx.draw("#s16-a1", 98.0, 0.6);
      tl.fromTo("#s16-yl", { scale: 1 }, { scale: 1.35, duration: 0.2, yoyo: true, repeat: 1, immediateRender: false }, 98.75);
      tl.fromTo("#s16-xl1", { scale: 1 }, { scale: 1.35, duration: 0.2, yoyo: true, repeat: 1, immediateRender: false }, 100.65);
      // pull back, then: go left (cheaper) and up (smarter)
      tl.to("#s16-world", { scale: 1, x: 0, y: 0, duration: 0.9, ease: "power3.inOut" }, 101.3);
      fx.draw("#s16-a2", 104.7, 0.5); fx.draw("#s16-a2h", 105.15, 0.2);
      fx.draw("#s16-a3", 106.75, 0.5); fx.draw("#s16-a3h", 107.2, 0.2);
      tl.fromTo("#s16-zone", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, 107.3);
      // Pi wins
      fx.pop("#s16-p3", 108.1, { from: 0, d: 0.5 });
      fx.ringPulse("#s16-r3", 108.2, { scale: 3 });
      fx.rise("#s16-l3", 108.25, { y: 14 });
      tl.fromTo("#s16-best", { opacity: 0, y: -80, rotation: -20 }, { opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "back.out(2)" }, 108.5);
      tl.to("#s16-world", { scale: 1.15, x: 120, y: 40, duration: 1.2, ease: "power3.inOut" }, 108.2);
      tl.to("#s16-yl, #s16-xl1, #s16-xl2, #s16-ill", { opacity: 0, duration: 0.3 }, 108.9);
      fx.maskUp("#s16-k1", 109.3);
""", blob=("#136052", 540, 900), exit_t=110.3)

# ---------------------------------------------------------------- s17 same engine, two chassis
def lane(p, name, top, succ, cost):
    return f"""
      <div id="{p}" class="ah-chassis" style="left:90px; top:{top}px; width:900px; height:470px"><span class="nm">{name}</span>
        <div style="position:absolute; right:40px; top:110px; width:220px; height:220px">{core(p + "-c", 0, 0, 220)}</div>
        <div class="s17-lb" style="top:100px">نسبة النجاح</div><div class="s17-v" id="{p}-iv" style="top:96px">{succ}</div>
        <div class="ah-track" style="left:40px; top:160px; width:540px"><div class="ah-fill" id="{p}-i" style="background:var(--lime)"></div></div>
        <div class="s17-lb" style="top:240px">التكلفة / تاسك</div><div class="s17-v" id="{p}-kv" style="top:236px">{cost}</div>
        <div class="ah-track" style="left:40px; top:300px; width:540px"><div class="ah-fill" id="{p}-k" style="background:var(--orange)"></div></div>
        <div class="s17-en">FABLE 5</div>
      </div>"""


make("s17", """
    #s17-lab { top: 210px; } #s17-h { top: 250px; }
    .s17-lb { position: absolute; right: 300px; font-size: 38px; font-weight: 800; }
    .s17-v { position: absolute; left: 40px; font-family: var(--font-en); font-weight: 900; font-size: 40px; color: var(--yellow); direction: ltr; }
    #s17-src { top: 1700px; }
    .s17-en { position: absolute; right: 64px; top: 360px; font-family: var(--font-en); font-weight: 900; font-size: 26px; letter-spacing: .16em; color: var(--yellow); direction: ltr; }
    #s17-eq { left: 470px; top: 1035px; width: 140px; height: 90px; border-radius: 45px; background: var(--yellow); color: var(--ink); font-family: var(--font-en); font-weight: 900; font-size: 64px; display: flex; align-items: center; justify-content: center; }
    #s17-tg { position: absolute; left: 60px; padding: 4px 18px; border-radius: 18px; background: var(--lime); color: var(--ink); font-weight: 800; font-size: 30px; }
""", f"""
      <div id="s17-lab" class="row"><span class="t-label">SAME ENGINE · DIFFERENT HARNESS</span></div>
      <div id="s17-h" class="row t-h3"><span class="mask"><span class="in" id="s17-h1">نفس الموديل… نتيجة تانية</span></span></div>
      {lane("s17-a", "Claude Code", 470, "97.8%", "$1.33")}
      {lane("s17-b", "Pi", 1180, "96.7%", "$0.67")}
      <div id="s17-eq" class="abs">≈</div>
      <div id="s17-tg" style="top:1600px">النص تقريبًا</div>
      <div id="s17-src" class="row"><span class="t-label">SOURCE · ARENA AI HARNESSTAX · SWE-BENCH LITE</span></div>
""", """
      fx.rise("#s17-lab", 110.45, { y: 16 });
      fx.maskUp("#s17-h1", 110.5);
      fx.pop("#s17-a", 110.6, { from: 0.85, e: "power3.out" });
      fx.pop("#s17-a-c", 110.8, { from: 0.3 });
      tl.fromTo("#s17-a-c-g, #s17-b-c-g", { rotation: 0 }, { rotation: 300, duration: 10, ease: "none" }, 110.4);
      fx.meter("#s17-a-i", 112.4, 0.6, 0.978, { e: "power3.out" });
      fx.meter("#s17-a-k", 114.1, 0.6, 1.0, { e: "power3.out" });
      fx.pop("#s17-b", 114.7, { from: 0.85, e: "power3.out" });
      fx.pop("#s17-b-c", 114.9, { from: 0.3 });
      tl.fromTo("#s17-b-k", { backgroundColor: "#ffec5c" }, { backgroundColor: "#ffec5c", duration: 0.01 }, 110.4);
      fx.meter("#s17-b-k", 117.2, 0.6, 0.504, { e: "power3.out" });
      fx.pop("#s17-tg", 117.4, { from: 0.3 });
      fx.meter("#s17-b-i", 119.2, 0.6, 0.967, { e: "power3.out" });
      fx.pop("#s17-eq", 119.4, { from: 0.2 });
      fx.rise("#s17-a-iv", 112.6, { y: 10 }); fx.rise("#s17-a-kv", 114.3, { y: 10 });
      fx.rise("#s17-b-kv", 117.4, { y: 10 }); fx.rise("#s17-b-iv", 119.4, { y: 10 });
      fx.rise("#s17-src", 110.8, { y: 10 });
""", blob=("#136052", 540, 1000), exit_t=120.2)

# ---------------------------------------------------------------- s18 x2 slam
make("s18", """
    #s18-lab { top: 360px; } #s18-h { top: 420px; }
    #s18-ring { left: 190px; top: 610px; width: 700px; height: 700px; }
    #s18-x { left: 0; right: 0; top: 700px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 400px; line-height: 1; color: var(--yellow); direction: ltr;
      text-shadow: 0 0 80px rgba(255,236,92,.55); }
    #s18-bl { left: 140px; top: 560px; width: 800px; height: 800px; }
    #s18-k { top: 1400px; }
""", """
      <div id="s18-lab" class="row"><span class="t-label">SOMETIMES…</span></div>
      <div id="s18-h" class="row t-h2"><span class="mask"><span class="in" id="s18-h1">الفرق ممكن يوصل</span></span></div>
      <div id="s18-bl" class="ah-bloom"></div>
      <svg id="s18-ring" class="abs" viewBox="0 0 700 700"><circle id="s18-rc" pathLength="1" cx="350" cy="350" r="320" fill="none" stroke="#ff5a33" stroke-width="10" transform="rotate(-90 350 350)" /></svg>
      <div id="s18-x" class="abs"><span id="s18-x1" style="display:inline-block">×2</span></div>
      <div id="s18-k" class="row t-h1"><span class="mask"><span class="in" id="s18-k1">ضعف <span class="hl"><span class="band" id="s18-band" style="background:var(--orange)"></span><span class="txt" style="color:#fff">التكلفة</span></span></span></span></div>
""", """
      fx.rise("#s18-lab", 120.35, { y: 16 });
      fx.maskUp("#s18-h1", 120.6);
      fx.draw("#s18-rc", 121.4, 2.0, "power1.in");
      tl.fromTo("#s18-x1", { opacity: 0, scale: 3, filter: "blur(20px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }, 123.42);
      tl.fromTo("#s18-bl", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power2.out" }, 123.45);
      fx.shake("#s18-cam", 123.5, 22, 8);
      fx.maskUp("#s18-k1", 123.6);
      fx.band("#s18-band", 123.85);
""", blob=("#5a2a1c", 540, 960), exit_t=124.3)

# ---------------------------------------------------------------- s19 equation -> half
make("s19", """
    #s19-lab { top: 210px; }
    .s19-r { position: absolute; left: 0; right: 0; text-align: center; }
    .s19-r .pill { font-size: 48px; height: 100px; padding: 0 44px; border-radius: 50px; }
    .s19-r .ok { width: 54px; height: 54px; border-radius: 50%; background: var(--green); color: #fff; display: inline-flex; align-items: center; justify-content: center; }
    #s19-r1 { top: 290px; } #s19-r2 { top: 420px; } #s19-r3 { top: 560px; }
    #s19-l1 { top: 840px; } #s19-l2 { top: 1100px; }
    .s19-lb { position: absolute; right: 110px; font-size: 40px; font-weight: 800; }
    #s19-t1 { left: 110px; top: 920px; width: 860px; height: 70px; border-radius: 35px; } #s19-t2 { left: 110px; top: 1180px; width: 860px; height: 70px; border-radius: 35px; }
    #s19-t1 .ah-fill, #s19-t2 .ah-fill { border-radius: 35px; }
    #s19-cut { left: 528px; top: 1150px; width: 24px; height: 130px; border-radius: 12px; background: var(--yellow); }
    #s19-half { left: 0; right: 0; top: 1330px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 200px; color: var(--yellow); direction: ltr; line-height: 1; }
    #s19-k { top: 1580px; }
    .s19-val { position: absolute; left: 110px; font-family: var(--font-en); font-weight: 900; font-size: 44px; color: var(--yellow); direction: ltr; }
""", """
      <div id="s19-lab" class="row"><span class="t-label">THE FORMULA</span></div>
      <div class="s19-r" id="s19-r1"><span class="pill"><span class="ok"><svg width="34" height="34"><use href="#i-check" /></svg></span>نفس النموذج</span></div>
      <div class="s19-r" id="s19-r2"><span class="pill"><span class="ok"><svg width="34" height="34"><use href="#i-check" /></svg></span>نفس التاسك</span></div>
      <div class="s19-r" id="s19-r3"><span class="pill on">+ <span class="lat">Harness</span> مختلف</span></div>
      <div class="s19-lb" id="s19-l1">قبل</div>
      <div class="ah-track" id="s19-t1"><div class="ah-fill" id="s19-f1" style="background:var(--orange)"></div></div>
      <div class="s19-lb" id="s19-l2">بعد</div>
      <div class="ah-track" id="s19-t2"><div class="ah-fill" id="s19-f2" style="background:var(--lime)"></div></div>
      <div id="s19-cut" class="abs"></div>
      <div class="s19-val" id="s19-v1" style="top:850px">$1.33</div><div class="s19-val" id="s19-v2" style="top:1110px">$0.67</div>
      <div id="s19-half" class="abs">½</div>
      <div id="s19-k" class="row t-h2"><span class="mask"><span class="in" id="s19-k1">التكلفة توصل للنص</span></span></div>
""", """
      fx.rise("#s19-lab", 124.45, { y: 16 });
      fx.pop("#s19-r1", 124.7, { from: 0.5 });
      fx.pop("#s19-r2", 125.5, { from: 0.5 });
      fx.pop("#s19-r3", 127.0, { from: 0.3, e: "back.out(3)" });
      fx.rise("#s19-l1, #s19-t1", 127.85, { y: 20 });
      fx.meter("#s19-f1", 128.0, 0.6, 1, { e: "power3.out" });
      fx.rise("#s19-l2, #s19-t2", 128.9, { y: 20 });
      fx.meter("#s19-f2", 129.0, 0.4, 1, { e: "power3.out" });
      tl.fromTo("#s19-cut", { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.2, ease: "expo.out" }, 129.9);
      tl.to("#s19-f2", { scaleX: 0.5, duration: 0.5, ease: "expo.out" }, 130.1);
      tl.to("#s19-cut", { opacity: 0, duration: 0.2 }, 130.5);
      tl.fromTo("#s19-half", { opacity: 0, scale: 2.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }, 130.3);
      fx.maskUp("#s19-k1", 130.35);
      fx.rise("#s19-v1", 128.2, { y: 10 }); fx.rise("#s19-v2", 130.35, { y: 10 });
""", blob=("#136052", 540, 1200), exit_t=130.8)

# ---------------------------------------------------------------- s20 sources in comments
make("s20", """
    #s20-lab { top: 210px; } #s20-h { top: 250px; }
    #s20-win { left: 110px; top: 470px; width: 860px; height: 760px; }
    #s20-pin { position: absolute; right: 40px; top: 90px; display: flex; gap: 18px; align-items: center; direction: rtl; }
    #s20-av { width: 80px; height: 80px; border-radius: 50%; background: var(--teal); color: #fff; font-weight: 900; font-size: 40px; display: flex; align-items: center; justify-content: center; }
    #s20-nm { font-size: 36px; font-weight: 800; color: var(--ink); }
    #s20-pt { font-family: var(--font-en); font-size: 18px; font-weight: 800; letter-spacing: .16em; color: #5a6b62; direction: ltr; }
    #s20-tx { position: absolute; right: 40px; top: 210px; font-size: 40px; font-weight: 700; color: var(--ink); direction: rtl; }
    .s20-lk { position: absolute; left: 40px; right: 40px; height: 110px; border-radius: 22px; background: #eceee0; display: flex; align-items: center; gap: 20px; padding: 0 28px; direction: ltr; }
    .s20-lk b { font-family: var(--font-en); font-weight: 900; font-size: 30px; color: var(--teal); }
    .s20-lk .ic { width: 56px; height: 56px; border-radius: 50%; background: var(--lime); color: var(--ink); display: flex; align-items: center; justify-content: center; }
    #s20-k1 { top: 320px; } #s20-k2 { top: 460px; }
    #s20-dn { left: 490px; top: 1280px; width: 100px; height: 100px; color: var(--yellow); }
    #s20-live { left: 0; right: 0; top: 1450px; text-align: center; }
    #s20-ref { width: 56px; height: 56px; }
""", """
      <div id="s20-lab" class="row"><span class="t-label">CHECK THE BENCHMARKS</span></div>
      <div id="s20-h" class="row t-h2"><span class="mask"><span class="in" id="s20-h1">المصادر في التعليقات</span></span></div>
      <div id="s20-win" class="window"><div class="bar"><i></i><i></i><i></i><b>COMMENTS · PINNED</b></div>
        <div id="s20-pin"><div id="s20-av">ح</div><div><div id="s20-nm">حسام الدين حسن</div><div id="s20-pt">PINNED</div></div></div>
        <div id="s20-tx"><span id="s20-tt"></span></div>
        <div class="s20-lk" id="s20-k1"><span class="ic"><svg width="30" height="30"><use href="#i-list" /></svg></span><b>SOURCE 01 · BENCHMARK</b></div>
        <div class="s20-lk" id="s20-k2"><span class="ic"><svg width="30" height="30"><use href="#i-list" /></svg></span><b>SOURCE 02 · ARENA AI</b></div>
      </div>
      <svg id="s20-dn" class="abs"><use href="#i-down" /></svg>
      <div id="s20-live" class="abs"><span class="pill on"><svg id="s20-ref" style="color:#0d0d0d"><use href="#i-refresh" /></svg><span class="lat" style="font-weight:900; letter-spacing:.1em">UPDATED</span> أول بأول</span></div>
""", """
      fx.rise("#s20-lab", 130.95, { y: 16 });
      fx.maskUp("#s20-h1", 131.6);
      tl.fromTo("#s20-win", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.55, ease: "expo.out" }, 132.0);
      fx.typeText("#s20-tt", 132.6, "المصادر هنا", 16);
      fx.rise("#s20-k1, #s20-k2", 133.2, { y: 20, st: 0.15 });
      tl.fromTo("#s20-dn", { opacity: 0, y: -30 }, { opacity: 1, y: 20, duration: 0.35, ease: "power2.inOut", yoyo: true, repeat: 3 }, 133.0);
      fx.pop("#s20-live", 135.3, { from: 0.3 });
      tl.fromTo("#s20-ref", { rotation: 0 }, { rotation: 720, duration: 2.2, ease: "power2.inOut" }, 135.4);
""", blob=("#136052", 540, 900), exit_t=137.8)

# ---------------------------------------------------------------- s21 leaderboard is temporary
make("s21", """
    #s21-lab { top: 210px; } #s21-h { top: 250px; }
    .s21-row { position: absolute; left: 110px; width: 860px; height: 170px; border-radius: 30px; display: flex; align-items: center; gap: 30px; padding: 0 40px; direction: ltr; }
    .s21-row .rk { font-family: var(--font-en); font-weight: 900; font-size: 60px; width: 90px; }
    .s21-row .nm { font-family: var(--font-en); font-weight: 900; font-size: 64px; }
    #s21-pi { top: 560px; background: rgba(179,206,101,.14); border: 4px solid var(--lime); }
    #s21-r2 { top: 770px; background: rgba(255,255,255,.04); border: 2px solid var(--edge); }
    #s21-r3 { top: 980px; background: rgba(255,255,255,.04); border: 2px solid var(--edge); }
    #s21-nw { top: 1500px; background: rgba(255,236,92,.14); border: 4px solid var(--yellow); }
    #s21-cr { left: 760px; top: 600px; width: 90px; height: 90px; color: var(--yellow); }
    #s21-td { position: absolute; right: 330px; padding: 4px 16px; border-radius: 16px; background: var(--lime); color: var(--ink); font-family: var(--font-en); font-weight: 900; font-size: 22px; letter-spacing: .14em; }
    #s21-k { top: 1250px; }
""", """
      <div id="s21-lab" class="row"><span class="t-label">TODAY'S #1</span></div>
      <div id="s21-h" class="row t-h3"><span class="mask"><span class="in" id="s21-h1">مش هقولك «خليك في <span class="lat">Pi</span>»</span></span></div>
      <div class="s21-row" id="s21-pi"><span class="rk" style="position:relative; display:inline-block"><span id="s21-pr">01</span><span id="s21-pr2" style="position:absolute; left:0; top:0; opacity:0">02</span></span><span class="nm ah-l">Pi</span><span id="s21-td">TODAY</span></div>
      <div class="s21-row" id="s21-r2"><span class="rk muted" style="position:relative; display:inline-block"><span id="s21-q1">02</span><span id="s21-q2" style="position:absolute; left:0; top:0; opacity:0">03</span></span><span class="nm muted" style="opacity:.4">· · ·</span></div>
      <div class="s21-row" id="s21-r3"><span class="rk muted">03</span><span class="nm muted" style="opacity:.4">· · ·</span></div>
      <div class="s21-row" id="s21-nw"><span class="rk ah-y">01</span><span class="nm ah-y">NEXT ?</span></div>
      <svg id="s21-cr" class="abs"><use href="#i-crown" /></svg>
      <div id="s21-k" class="row t-h3 muted"><span class="mask"><span class="in" id="s21-k1">ممكن يطلع أحسن منه بعدين</span></span></div>
""", """
      fx.rise("#s21-lab", 137.95, { y: 16 });
      fx.maskUp("#s21-h1", 138.0);
      fx.rise("#s21-pi, #s21-r2, #s21-r3", 138.3, { y: 40, st: 0.1 });
      tl.fromTo("#s21-cr", { opacity: 0, y: -80, rotation: -20 }, { opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "back.out(2)" }, 138.6);
      fx.pop("#s21-td", 141.2, { from: 0.3 });
      fx.maskUp("#s21-k1", 142.9);
      tl.fromTo("#s21-nw", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 143.3);
      tl.to("#s21-nw", { y: -940, duration: 0.6, ease: "power3.inOut" }, 144.0);
      tl.to("#s21-pi", { y: 210, duration: 0.6, ease: "power3.inOut" }, 144.0);
      tl.to("#s21-r2", { y: 210, opacity: 0.6, duration: 0.6, ease: "power3.inOut" }, 144.0);
      tl.to("#s21-r3", { y: 210, opacity: 0, duration: 0.6, ease: "power3.inOut" }, 144.0);
      tl.to("#s21-cr", { y: -20, x: -40, rotation: 15, duration: 0.6, ease: "power3.inOut" }, 144.0);
      tl.to("#s21-pi", { borderColor: "rgba(255,255,255,0.1)", backgroundColor: "rgba(255,255,255,0.04)", duration: 0.4 }, 144.2);
      tl.to("#s21-pr, #s21-q1", { opacity: 0, duration: 0.2 }, 144.3);
      tl.to("#s21-pr2, #s21-q2", { opacity: 1, duration: 0.2 }, 144.3);
      tl.to("#s21-k", { y: 300, duration: 0.6, ease: "power3.inOut" }, 144.0);
""", blob=("#136052", 540, 900), exit_t=145.8)

# ---------------------------------------------------------------- s22 investigate + sources
make("s22", """
    #s22-lab { top: 210px; } #s22-h { top: 250px; }
    #s22-mg { left: 160px; top: 290px; width: 140px; height: 140px; color: var(--yellow); }
    .s22-ck { position: absolute; left: 0; right: 0; text-align: center; }
    .s22-ck .pill { font-size: 50px; height: 104px; padding: 0 44px; border-radius: 52px; }
    .s22-ck .bx { width: 56px; height: 56px; border-radius: 14px; border: 4px solid var(--lime); display: inline-flex; align-items: center; justify-content: center; color: var(--lime); }
    #s22-c1 { top: 520px; } #s22-c2 { top: 660px; }
    #s22-sl { top: 880px; }
    .s22-src { position: absolute; left: 110px; width: 860px; height: 220px; border-radius: 34px; background: #fbfbf7; color: var(--ink); display: flex; align-items: center; gap: 30px; padding: 0 44px; direction: ltr; box-shadow: 0 20px 50px rgba(0,0,0,.35); }
    .s22-src .ic { width: 100px; height: 100px; border-radius: 50%; background: var(--teal); color: #fff; display: flex; align-items: center; justify-content: center; flex: none; }
    .s22-src b { font-family: var(--font-en); font-size: 62px; font-weight: 900; display: block; }
    .s22-src i { font-style: normal; font-family: var(--font-en); font-size: 22px; font-weight: 800; letter-spacing: .18em; color: #5a6b62; }
    #s22-a { top: 960px; } #s22-b { top: 1220px; }
""", """
      <div id="s22-lab" class="row"><span class="t-label">DO YOUR RESEARCH</span></div>
      <div id="s22-h" class="row t-h1"><span class="mask"><span class="in" id="s22-h1">اتحرّى</span></span></div>
      <svg id="s22-mg" class="abs"><use href="#i-search" /></svg>
      <div class="s22-ck" id="s22-c1"><span class="pill"><span class="bx"><svg id="s22-k1" width="40" height="40"><use href="#i-check" /></svg></span>مش بس الموديل</span></div>
      <div class="s22-ck" id="s22-c2"><span class="pill on"><span class="bx" style="border-color:#0d0d0d; color:#0d0d0d"><svg id="s22-k2" width="40" height="40"><use href="#i-check" /></svg></span>كمان الـ<span class="lat">Harness</span></span></div>
      <div id="s22-sl" class="row"><span class="t-label" style="color:var(--yellow)">GREAT SOURCES</span></div>
      <div class="s22-src" id="s22-a"><span class="ic"><svg width="56" height="56"><use href="#i-list" /></svg></span><span><b>Artificial Analysis</b><i>BENCHMARKS</i></span></div>
      <div class="s22-src" id="s22-b"><span class="ic" style="background:var(--green)"><svg width="56" height="56"><use href="#i-list" /></svg></span><span><b>Arena AI</b><i>ARTICLE · CHART</i></span></div>
""", """
      fx.rise("#s22-lab", 145.95, { y: 16 });
      fx.maskUp("#s22-h1", 145.95);
      tl.fromTo("#s22-mg", { opacity: 0, x: 120, rotation: -30 }, { opacity: 1, x: 0, rotation: 0, duration: 0.5, ease: "back.out(2)" }, 146.1);
      fx.pop("#s22-c1", 146.6, { from: 0.5 });
      fx.pop("#s22-k1", 147.0, { from: 0 });
      fx.pop("#s22-c2", 147.6, { from: 0.5 });
      fx.pop("#s22-k2", 148.3, { from: 0 });
      tl.fromTo("#s22-a", { opacity: 0, x: 800 }, { opacity: 1, x: 0, duration: 0.5, ease: "expo.out" }, 148.85);
      fx.rise("#s22-sl", 150.2, { y: 14 });
      tl.fromTo("#s22-b", { opacity: 0, x: 800 }, { opacity: 1, x: 0, duration: 0.5, ease: "expo.out" }, 152.35);
""", blob=("#136052", 540, 1000), exit_t=153.5)

# ---------------------------------------------------------------- s23 bonus Zadloop
make("s23", """
    #s23-bn { left: 0; right: 0; top: 230px; text-align: center; }
    #s23-h { top: 320px; }
    #s23-top { left: 140px; top: 600px; width: 800px; height: 230px; border-radius: 36px; background: linear-gradient(135deg, #1a7564, #136052); border: 4px solid var(--lime);
      display: flex; align-items: center; justify-content: center; box-shadow: 0 30px 60px rgba(0,0,0,.4); }
    #s23-top b { font-family: var(--font-en); font-weight: 900; font-size: 110px; direction: ltr; }
    #s23-base { left: 100px; top: 880px; width: 880px; height: 150px; border-radius: 30px; background: rgba(255,255,255,.06); border: 3px dashed rgba(246,248,240,.5);
      display: flex; align-items: center; justify-content: center; gap: 16px; direction: ltr; }
    #s23-base b { font-family: var(--font-en); font-weight: 900; font-size: 52px; color: var(--fg-muted); }
    #s23-on { position: absolute; left: 0; right: 0; top: 836px; text-align: center; }
    #s23-ar { left: 820px; top: 520px; width: 160px; height: 160px; border-radius: 50%; background: var(--yellow); color: var(--ink); font-size: 96px; font-weight: 900; display: flex; align-items: center; justify-content: center; }
    .s23-p { position: absolute; left: 0; right: 0; text-align: center; }
    .s23-p .pill { font-size: 44px; height: 96px; padding: 0 40px; border-radius: 48px; }
    .s23-p .ic { width: 58px; height: 58px; border-radius: 50%; background: var(--lime); color: var(--ink); display: inline-flex; align-items: center; justify-content: center; }
    #s23-p1 { top: 1130px; } #s23-p2 { top: 1270px; } #s23-p3 { top: 1410px; }
    #s23-fl { top: 1690px; }
""", """
      <div id="s23-bn" class="abs"><span class="pill bad" style="font-family:var(--font-en); letter-spacing:.14em; font-size:30px; height:64px">BONUS</span></div>
      <div id="s23-h" class="row t-h3"><span class="mask"><span class="in" id="s23-h1">حابب ألفت انتباهك لـ</span></span></div>
      <div id="s23-top" class="abs"><b>Zadloop</b></div>
      <div id="s23-on" class="abs"><span class="t-label">BUILT ON</span></div>
      <div id="s23-base" class="abs"><b>DeepSeek</b><b style="color:var(--lime)">Harness</b></div>
      <div id="s23-ar" class="abs">ع</div>
      <div class="s23-p" id="s23-p1"><span class="pill">معمول باللغة العربية</span></div>
      <div class="s23-p" id="s23-p2"><span class="pill"><span class="ic"><svg width="34" height="40"><use href="#i-person" /></svg></span>وراه مبرمج عربي</span></div>
      <div class="s23-p" id="s23-p3"><span class="pill"><span class="ic"><svg width="36" height="36"><use href="#i-mic" /></svg></span>في بودكاست أخبار الذكاء الاصطناعي</span></div>
""", """
      fx.pop("#s23-bn", 153.85, { from: 0.3 });
      fx.maskUp("#s23-h1", 154.0);
      tl.fromTo("#s23-top", { opacity: 0, scale: 1.6, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out" }, 155.3);
      tl.to("#s23-top", { y: -40, duration: 0.5, ease: "power3.out" }, 156.7);
      tl.fromTo("#s23-base", { opacity: 0, y: 160 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 156.95);
      fx.rise("#s23-on", 157.1, { y: 10 });
      fx.pop("#s23-ar", 158.7, { from: 0, e: "back.out(2.6)" });
      fx.pop("#s23-p1", 158.9, { from: 0.5 });
      fx.pop("#s23-p2", 160.4, { from: 0.5 });
      fx.pop("#s23-p3", 162.5, { from: 0.5 });
""", blob=("#136052", 540, 900), exit_t=164.1)

# ---------------------------------------------------------------- s24 outro
make("s24", """
    #s24-em { left: 380px; top: 330px; width: 320px; height: 320px; }
    #s24-tg { left: 0; right: 0; top: 690px; text-align: center; }
    #s24-h { top: 800px; }
    #s24-fol { left: 0; right: 0; top: 960px; text-align: center; }
    #s24-bell { width: 48px; height: 48px; }
    #s24-cb { left: 110px; top: 1130px; width: 860px; height: 150px; border-radius: 30px; background: #fbfbf7; color: var(--ink); display: flex; align-items: center; gap: 24px; padding: 0 36px; direction: rtl; }
    #s24-cb .ic { width: 70px; height: 70px; border-radius: 50%; background: var(--teal); color: #fff; display: flex; align-items: center; justify-content: center; flex: none; }
    #s24-ct { font-size: 42px; font-weight: 700; white-space: nowrap; }
    #s24-k { top: 1360px; font-size: 74px; } #s24-s { top: 1500px; }
""", f"""
      <div id="s24-em" class="abs">{core("s24-c", 90, 90, 140)}{brackets("s24-b", 0, 0, 320, 320, 90)}</div>
      <div id="s24-tg" class="abs ah-tag">MODEL + HARNESS</div>
      <div id="s24-h" class="row t-h3"><span class="mask"><span class="in" id="s24-h1">عايز تعرف كل جديد في الـ<span class="lat">AI</span>؟</span></span></div>
      <div id="s24-fol" class="abs"><span class="pill on"><svg id="s24-bell" style="color:#0d0d0d"><use href="#i-bell" /></svg>تابعني</span></div>
      <div id="s24-cb" class="abs"><span class="ic"><svg width="40" height="40"><use href="#i-chat" /></svg></span><span id="s24-ct"><span id="s24-tt"></span><span class="caret" id="s24-car"></span></span></div>
      <div id="s24-k" class="row t-h2"><span class="mask"><span class="in" id="s24-k1">نشوفك في الفيديو الجاي</span></span></div>
      <div id="s24-s" class="row t-h1 ah-l"><span class="mask"><span class="in" id="s24-s1">سلام عليكم</span></span></div>
""", """
      fx.pop("#s24-c", 164.25, { from: 0.3 });
      tl.fromTo("#s24-c-g", { rotation: 0 }, { rotation: 200, duration: 7.3, ease: "none" }, 164.2);
      [["#s24-b-a", -120, -120], ["#s24-b-b", 120, -120], ["#s24-b-c", -120, 120], ["#s24-b-d", 120, 120]].forEach(([s, x, y], i) => {
        tl.fromTo(s, { opacity: 0, x, y }, { opacity: 1, x: 0, y: 0, duration: 0.3, ease: "expo.out" }, 164.5 + i * 0.04);
      });
      fx.rise("#s24-tg", 164.8, { y: 14 });
      fx.maskUp("#s24-h1", 165.45);
      fx.pop("#s24-fol", 166.3, { from: 0.4 });
      tl.fromTo("#s24-bell", { rotation: 0 }, { rotation: 18, duration: 0.08, yoyo: true, repeat: 7, ease: "sine.inOut" }, 166.6);
      fx.rise("#s24-cb", 167.1, { y: 30 });
      fx.typeText("#s24-tt", 167.4, "اكتب سؤالك هنا…", 16);
      tl.fromTo("#s24-car", { opacity: 1 }, { opacity: 0.15, duration: 0.25, ease: "steps(1)", yoyo: true, repeat: 9 }, 167.1);
      fx.maskUp("#s24-k1", 168.6);
      fx.maskUp("#s24-s1", 169.7);
      fx.breathe("#s24-em", 165.0, 6.0, 0.03, 1.5);
""", blob=("#136052", 540, 600), exit_t=171.15)

print("built", len(SCENES), "scenes")
