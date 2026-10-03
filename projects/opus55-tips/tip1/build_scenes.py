# Part 1 — "Don't box it in" (9:16, dark). Times = GLOBAL seconds on assets/voice/tip1.wav.
# Spine (series): the Claude spark is the hero. Signature (part 1): a box squeezes the spark and bursts open.
# Re-run after edits:  python build_scenes.py  (then motion_sync.py)
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from build_lib import Part, patch_root, spark, ic, label, head, claude_input, chip, phone, hossam  # noqa: E402

P = Part(HERE)
patch_root(HERE, flashes=(21.42, 71.9))
make = P.make

# ---------------------------------------------------------------- s1 hook
make("s1", """
    #s1-k { top: 1000px; }
    #s1-title { position: absolute; left: 0; right: 0; top: 1100px; text-align: center; font-size: 170px; line-height: 1.12; white-space: nowrap; direction: ltr; }
    #s1-t1, #s1-t2 { display: block; } #s1-t2 { color: #e8977c; }
    .s1-b { position: absolute; width: 150px; height: 104px; border-radius: 52px; background: #0b2f29; border: 3px solid rgba(179,206,101,.6);
      display: flex; align-items: center; justify-content: center; color: var(--lime); }
    #s1-b1 { left: 120px; top: 420px; } #s1-b2 { left: 820px; top: 470px; } #s1-b3 { left: 90px; top: 800px; } #s1-b4 { left: 850px; top: 820px; }
""", f"""
      {spark("s1-sp", 380, 470, 320)}
      <div class="s1-b" id="s1-b1">{ic("chat", 62)}</div><div class="s1-b" id="s1-b2">{ic("chat", 62)}</div>
      <div class="s1-b" id="s1-b3">{ic("chat", 62)}</div><div class="s1-b" id="s1-b4">{ic("chat", 62)}</div>
      {head("s1-k", 1000, ["كل الناس بتتكلم عن"], "t-h3")}
      <div id="s1-title" class="op-en" data-layout-allow-overlap><span id="s1-t1">Claude</span><span id="s1-t2">Opus 5.5</span></div>
""", """
      fx.punch("#s1-cam", 0, 1.18);
      fx.pop("#s1-sp", 0.0, { from: 0.2, e: "expo.out", d: 0.9 });
      tl.fromTo("#s1-sp-svg", { rotation: -90 }, { rotation: 40, duration: 3.3, ease: "power2.out" }, 0);
      fx.breathe("#s1-sp-bl", 0.6, 2.6, 0.08, 1.3);
      fx.pop("#s1-b1", 0.6); fx.pop("#s1-b2", 0.85); fx.pop("#s1-b3", 1.1); fx.pop("#s1-b4", 1.35);
      fx.drift("#s1-b1, #s1-b3", 0.6, 2.7, 30, -24); fx.drift("#s1-b2, #s1-b4", 0.85, 2.4, -30, -20);
      fx.maskUp("#s1-k1", 0.1);
      fx.letterDrop("#s1-t1", 1.5, { st: 0.035 });
      fx.letterDrop("#s1-t2", 1.95, { st: 0.04 });
""", blob=("#136052", 540, 640))

# ---------------------------------------------------------------- s2 nobody tells you
make("s2", """
    #s2-q { left: 120px; top: 260px; font-size: 1200px; line-height: 1; }
    #s2-hl { position: absolute; left: 0; right: 0; top: 960px; text-align: center; }
    #s2-tr { left: 150px; top: 1320px; width: 780px; } #s2-trl { top: 1260px; }
""", f"""
      <div id="s2-q" class="abs" aria-hidden="true" data-layout-ignore style="font-family:var(--font-ar); font-weight:900; color:rgba(179,206,101,.07)">؟</div>
      {head("s2-a", 560, ["محدش بيقولك"], "t-h1")}
      {head("s2-b", 760, ["ازاي تطلع منه"], "t-h2")}
      <div id="s2-hl" class="t-h1"><span class="hl" id="s2-hlw"><span class="band" id="s2-band"></span><span class="txt">أحسن نتائج</span></span></div>
      {label("s2-trl", 1260, "YOUR RESULTS")}
      <div id="s2-tr" class="op-track"><div id="s2-fill" class="op-fill" style="background:var(--lime)"></div></div>
""", """
      fx.drift("#s2-q", 3.0, 2.75, -40, 30);
      fx.maskUp("#s2-a1", 3.3);
      fx.maskUp("#s2-b1", 4.05);
      fx.pop("#s2-hlw", 4.75, { from: 0.6 }); fx.band("#s2-band", 4.75, 0.25);
      fx.rise("#s2-trl, #s2-tr", 3.6, { y: 20 });
      fx.meter("#s2-fill", 3.8, 0.5, 0.3, { e: "power2.out" });
      tl.to("#s2-fill", { background: "#ff5a33", duration: 0.2 }, 4.3);
      fx.shake("#s2-tr", 4.35, 10, 5);
      tl.to("#s2-fill", { scaleX: 1, background: "#b3ce65", duration: 0.5, ease: "power3.out" }, 4.95);
""", blob=("#0f4f44", 540, 900))

# ---------------------------------------------------------------- s3 series deck
CARD = 'style="left:{x}px; top:{y}px; width:{w}px; height:{h}px"'
make("s3", """
    #s3-c2b, #s3-c3b { transform-origin: 50% 100%; }
    .s3-lk { position: absolute; left: 50%; top: 50%; width: 90px; height: 90px; margin: -45px 0 0 -45px; color: rgba(179,206,101,.55); }
    .s3-n { position: absolute; left: 0; right: 0; text-align: center; }
    #s3-lab { top: 330px; }
""", f"""
      {label("s3-lab", 330, "THE SERIES · 3 TIPS")}
      <div id="s3-c3b" class="op-card back" {CARD.format(x=110, y=520, w=330, h=470)}><svg class="s3-lk"><use href="#i-lock" /></svg></div>
      <div id="s3-c2b" class="op-card back" {CARD.format(x=640, y=520, w=330, h=470)}><svg class="s3-lk"><use href="#i-lock" /></svg></div>
      <div id="s3-c1b" class="op-card back" {CARD.format(x=330, y=440, w=420, h=600)}></div>
      <div id="s3-c1" class="op-card" {CARD.format(x=330, y=440, w=420, h=600)}>
        {spark("s3-sp", 150, 50, 120, bloom=False)}
        <div class="s3-n op-en" data-layout-allow-overlap style="top:186px; font-size:40px; letter-spacing:.3em; color:var(--lime)">TIP</div>
        <div class="s3-n op-en op-y" data-layout-allow-overlap style="top:250px; font-size:210px; line-height:1">01</div>
        <div class="s3-n op-en" data-layout-allow-overlap style="top:480px; font-size:34px; color:var(--fg-muted)">OF 03</div>
      </div>
      {head("s3-h", 1150, ["في الفيديو ده هقولك على تيب"], "t-h3")}
      <div class="row t-h1" style="top:1260px"><span class="mask"><span class="in" id="s3-k1">هتفرق معاك</span></span></div>
      <div class="row t-h1 op-y" style="top:1430px"><span class="mask"><span class="in" id="s3-k2">كتير</span></span></div>
""", """
      fx.rise("#s3-lab", 5.6, { y: 16 });
      fx.rise("#s3-c3b", 5.6, { y: 120 }); fx.rise("#s3-c2b", 5.68, { y: 120 }); fx.rise("#s3-c1b", 5.76, { y: 160 });
      tl.fromTo("#s3-c3b", { rotation: 0 }, { rotation: -8, duration: 0.5, ease: "power3.out" }, 5.9);
      tl.fromTo("#s3-c2b", { rotation: 0 }, { rotation: 8, duration: 0.5, ease: "power3.out" }, 5.9);
      fx.hide("#s3-c1");
      tl.to("#s3-c1b", { scaleX: 0, duration: 0.16, ease: "power2.in" }, 6.25);
      tl.fromTo("#s3-c1", { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.22, ease: "power2.out", immediateRender: false }, 6.41);
      tl.fromTo("#s3-sp-svg", { rotation: 0 }, { rotation: 180, duration: 3.5, ease: "power1.out" }, 6.4);
      fx.maskUp("#s3-h1", 6.6);
      fx.maskUp("#s3-k1", 8.1);
      tl.fromTo("#s3-k2", { yPercent: 115, scale: 1 }, { yPercent: 0, duration: 0.45, ease: "back.out(2)" }, 9.0);
""", blob=("#136052", 540, 760))

# ---------------------------------------------------------------- s4 real Claude app: model picker
# window body shows src crop x100..780, y300..860 at 1.45x
make("s4", """
    #s4-win { left: 47px; top: 560px; width: 986px; height: 866px; }
    #s4-v { left: -145px; top: -435px; width: 1259px; height: 1485px; }
    #s4-hl { left: 420px; top: 415px; width: 438px; height: 72px; border-radius: 16px; border: 5px solid var(--lime); box-shadow: 0 0 30px rgba(180,207,102,.6); }
    #s4-src { top: 1460px; }
""", f"""
      {head("s4-h", 250, ["الموديل ده"], "t-h2")}
      <div class="row t-h1 op-l" style="top:350px"><span class="mask"><span class="in" id="s4-k1">ذكي جدًا</span></span></div>
      <div id="s4-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>Claude</b></div>
        <div class="body"><video id="s4-v" src="assets/videos/claude_app.mp4" data-start="0" data-duration="2.7" data-media-start="2.7" muted playsinline></video>
        <div id="s4-hl" class="abs"></div></div></div>
      <div id="s4-src" class="op-src">REAL SCREEN · CLAUDE APP · MODEL PICKER</div>
""", """
      fx.maskUp("#s4-h1", 9.85);
      fx.maskUp("#s4-k1", 11.0);
      tl.fromTo("#s4-win", { opacity: 0, y: 140, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, 9.75);
      fx.pop("#s4-hl", 10.15, { from: 1.3, d: 0.3, e: "power3.out" });
      tl.to("#s4-hl", { opacity: 0, duration: 0.15 }, 10.9);
      fx.rise("#s4-src", 10.0, { y: 10, b: 0 });
""", blob=("#0f4f44", 540, 1000), push=1.03)

# ---------------------------------------------------------------- s5 real benchmarks + 40%
# opus_bench.png is 1075 px wide; shown at 760 px (x0.707). Opus 5.5 column = x 60..266, header from y 94.
make("s5", """
    #s5-shot { left: 160px; top: 430px; width: 760px; height: 880px; }
    #s5-col { left: 40px; top: 50px; width: 150px; height: 830px; border-radius: 14px; border: 6px solid var(--lime); box-shadow: 0 0 34px rgba(180,207,102,.55); }
    #s5-card { left: 110px; top: 1350px; width: 860px; height: 300px; }
    #s5-num { position: absolute; left: 40px; top: 30px; width: 380px; text-align: center; font-family: var(--font-ar); font-weight: 900; font-size: 170px; line-height: 1.3; color: var(--yellow); }
    #s5-t1 { position: absolute; right: 44px; top: 60px; width: 470px; text-align: right; white-space: nowrap; font-size: 52px; }
    #s5-t2 { position: absolute; right: 44px; top: 200px; width: 420px; text-align: right; }
    #s5-src { top: 1690px; }
""", f"""
      <div class="row t-h2" style="top:250px; font-size:76px"><span class="mask"><span class="in" id="s5-h1">حتى في الـــ<span class="lat">Benchmarks</span></span></span></div>
      <div id="s5-shot" class="op-shot"><img id="s5-img" src="assets/images/opus_bench.png" style="width:760px" /><div id="s5-col" class="abs"></div></div>
      <div id="s5-card" class="op-card">
        <div id="s5-num" class="num">٤٠٪</div>
        <div id="s5-t1" class="t-h3">تكلفة تشغيل أقل</div>
        <div id="s5-t2" class="t-label" style="color:var(--lime); font-size:26px">VS CLAUDE OPUS 5</div>
      </div>
      <div id="s5-src" class="op-src">REAL DATA · ANTHROPIC.COM · SEP 22, 2026</div>
""", """
      fx.maskUp("#s5-h1", 12.35);
      tl.fromTo("#s5-shot", { opacity: 0, y: 160, rotation: 3 }, { opacity: 1, y: 0, rotation: 0, duration: 0.55, ease: "power3.out" }, 12.4);
      tl.fromTo("#s5-col", { opacity: 0, scaleY: 0.2 }, { opacity: 1, scaleY: 1, duration: 0.45, ease: "power3.out" }, 13.15);
      tl.fromTo("#s5-img", { y: 0 }, { y: -40, duration: 5, ease: "none" }, 13.6);
      tl.to("#s5-shot", { scale: 0.94, y: -30, duration: 0.5, ease: "power2.inOut" }, 15.2);
      tl.fromTo("#s5-card", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.6)" }, 15.45);
      fx.counter("#s5-num", 15.6, 17.6, 0, 40, { suffix: "٪" });
      fx.rise("#s5-t1", 16.2, { y: 20 }); fx.rise("#s5-t2", 16.5, { y: 14, b: 0 });
      fx.rise("#s5-src", 12.8, { y: 10, b: 0 });
""", blob=("#136052", 540, 900), push=1.02)

# ---------------------------------------------------------------- s6 SIGNATURE: the box squeezes, then bursts
make("s6", """
    .s6-w { position: absolute; background: var(--lime); border-radius: 12px; box-shadow: 0 0 30px rgba(180,207,102,.6); }
    #s6-wt { left: 350px; top: 610px; width: 380px; height: 24px; } #s6-wb { left: 350px; top: 966px; width: 380px; height: 24px; }
    #s6-wl { left: 350px; top: 610px; width: 24px; height: 380px; } #s6-wr { left: 706px; top: 610px; width: 24px; height: 380px; }
    .s6-ring { position: absolute; left: 340px; top: 600px; width: 400px; height: 400px; border-radius: 50%; border: 6px solid #e8977c; opacity: 0; }
""", f"""
      {head("s6-h", 280, ["ولما يكون ذكي بالشكل ده"], "t-h3")}
      {spark("s6-sp", 400, 660, 280)}
      <div class="s6-ring" id="s6-r1"></div><div class="s6-ring" id="s6-r2"></div>
      <div id="s6-wt" class="s6-w"></div><div id="s6-wb" class="s6-w"></div><div id="s6-wl" class="s6-w"></div><div id="s6-wr" class="s6-w"></div>
      <div class="row t-h1 op-o" style="top:1180px"><span class="mask"><span class="in" id="s6-a1">ما تحجّمهوش</span></span></div>
      <div class="row t-h1" style="top:1370px"><span class="mask"><span class="in" id="s6-b1">وما تحدّهوش</span></span></div>
""", """
      fx.maskUp("#s6-h1", 18.7);
      fx.pop("#s6-sp", 18.6, { from: 0.4, e: "expo.out", d: 0.6 });
      tl.fromTo("#s6-sp-svg", { rotation: 0 }, { rotation: 90, duration: 3.3, ease: "none" }, 18.6);
      // walls close in around the spark
      tl.fromTo("#s6-wt", { opacity: 0, y: -300 }, { opacity: 1, y: 0, duration: 1.4, ease: "power2.in" }, 18.9);
      tl.fromTo("#s6-wb", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 1.4, ease: "power2.in" }, 18.9);
      tl.fromTo("#s6-wl", { opacity: 0, x: -300 }, { opacity: 1, x: 0, duration: 1.4, ease: "power2.in" }, 18.9);
      tl.fromTo("#s6-wr", { opacity: 0, x: 300 }, { opacity: 1, x: 0, duration: 1.4, ease: "power2.in" }, 18.9);
      tl.to("#s6-sp", { scale: 0.72, duration: 1.0, ease: "power2.in" }, 19.4);
      tl.to("#s6-sp-bl", { opacity: 0.25, duration: 1.0 }, 19.4);
      fx.maskUp("#s6-a1", 20.45);
      fx.shake("#s6-wt, #s6-wb, #s6-wl, #s6-wr", 20.5, 8, 6);
      fx.maskUp("#s6-b1", 21.2);
      // BURST
      tl.to("#s6-wt", { y: -1300, rotation: -25, opacity: 0, filter: "blur(10px)", duration: 0.5, ease: "power3.out" }, 21.42);
      tl.to("#s6-wb", { y: 1300, rotation: 20, opacity: 0, filter: "blur(10px)", duration: 0.5, ease: "power3.out" }, 21.42);
      tl.to("#s6-wl", { x: -900, rotation: 30, opacity: 0, filter: "blur(10px)", duration: 0.5, ease: "power3.out" }, 21.42);
      tl.to("#s6-wr", { x: 900, rotation: -30, opacity: 0, filter: "blur(10px)", duration: 0.5, ease: "power3.out" }, 21.42);
      tl.to("#s6-sp", { scale: 1.7, duration: 0.45, ease: "expo.out" }, 21.42);
      tl.to("#s6-sp-bl", { opacity: 1, scale: 1.4, duration: 0.45, ease: "expo.out" }, 21.42);
      fx.ringPulse("#s6-r1, #s6-r2", 21.45, { scale: 2.6 });
      fx.shake("#s6-cam", 21.45, 18, 7);
""", blob=("#0f4f44", 540, 800), push=None, exit_t=21.5)

# ---------------------------------------------------------------- s7 don't lock its creativity
make("s7", """
    #s7-lock { left: 440px; top: 470px; width: 200px; height: 200px; }
    #s7-box { left: 230px; top: 720px; width: 620px; height: 620px; }
    #s7-glow { left: 140px; top: 620px; width: 800px; height: 800px; border-radius: 50%; background: radial-gradient(circle, rgba(255,160,70,.35), transparent 65%); }
    #s7-en { top: 1380px; font-size: 128px; color: var(--lime); text-shadow: 0 0 60px rgba(179,206,101,.5); }
""", f"""
      {head("s7-h", 260, ["يعني إيه؟ ما تقفلش على"], "t-h3")}
      <div id="s7-glow" class="abs"></div>
      <div id="s7-lock" class="abs" style="color:var(--yellow)"><svg id="s7-l1" style="position:absolute; inset:0; width:100%; height:100%"><use href="#i-lock" /></svg><svg id="s7-l2" style="position:absolute; inset:0; width:100%; height:100%; color:var(--lime)"><use href="#i-unlock" /></svg></div>
      <img id="s7-box" class="abs" src="assets/images/open_box_cut.png" />
      {spark("s7-sp", 470, 830, 140, bloom=False)}
      <div id="s7-en" class="op-big"><span id="s7-en1">CREATIVITY</span></div>
      <div class="row t-h3" style="top:1560px"><span class="mask"><span class="in" id="s7-k1">الإبداع بتاعه</span></span></div>
""", """
      fx.maskUp("#s7-h1", 21.85);
      fx.pop("#s7-lock", 22.7, { from: 0.3 });
      fx.hide("#s7-l2");
      fx.shake("#s7-lock", 23.4, 12, 6);
      tl.to("#s7-l1", { opacity: 0, duration: 0.12 }, 23.95);
      tl.to("#s7-l2", { opacity: 1, duration: 0.12 }, 23.95);
      tl.to("#s7-lock", { y: -40, duration: 0.3, ease: "back.out(2)" }, 23.95);
      tl.fromTo("#s7-box", { opacity: 0, y: 200, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "back.out(1.5)" }, 23.95);
      tl.fromTo("#s7-glow", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.8, ease: "power2.out" }, 24.1);
      tl.fromTo("#s7-sp", { opacity: 0, y: 120, scale: 0.3 }, { opacity: 1, y: -150, scale: 1, duration: 0.9, ease: "power3.out" }, 24.25);
      tl.fromTo("#s7-sp-svg", { rotation: 0 }, { rotation: 200, duration: 2.8, ease: "none" }, 24.25);
      fx.letterDrop("#s7-en1", 24.1, { st: 0.04 });
      fx.maskUp("#s7-k1", 26.8);
      fx.breathe("#s7-glow", 25.0, 2.0, 0.06, 1.0);
""", blob=("#136052", 540, 1000))

# ---------------------------------------------------------------- s8 goal + ideas + space -> result
make("s8", """
    .s8-t { position: absolute; width: 230px; text-align: center; }
    .s8-c { width: 230px; height: 230px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 18px; }
    #s8-t1 { left: 770px; top: 520px; } #s8-t2 { left: 425px; top: 520px; } #s8-t3 { left: 80px; top: 520px; }
    .s8-plus { position: absolute; top: 590px; font-family: var(--font-en); font-weight: 900; font-size: 80px; color: var(--fg-muted); }
    #s8-p1 { left: 705px; } #s8-p2 { left: 352px; }
    #s8-arr { left: 520px; top: 960px; width: 40px; height: 150px; }
    .s8-pill { position: absolute; top: 1010px; height: 76px; padding: 0 30px; border-radius: 38px; border: 3px solid var(--edge); background: rgba(255,255,255,.05);
      font-family: var(--font-ar); font-weight: 800; font-size: 36px; display: flex; align-items: center; white-space: nowrap; }
    #s8-q1 { left: 700px; } #s8-q2 { left: 180px; }
    #s8-res { left: 400px; top: 1160px; width: 280px; height: 280px; border-radius: 50%; }
    #s8-rl { top: 1470px; }
""", f"""
      <div class="row t-h3" style="top:280px"><span class="mask"><span class="in" id="s8-h1">ادّيله</span></span></div>
      <div id="s8-t1" class="s8-t"><div class="s8-c" style="background:var(--lime); color:var(--ink)">{ic("target", 120)}</div><div class="t-h3">هدف</div></div>
      <div id="s8-p1" class="s8-plus">+</div>
      <div id="s8-t2" class="s8-t"><div class="s8-c" style="background:var(--yellow); color:var(--ink)">{ic("bulb", 120)}</div><div class="t-h3">أفكار</div></div>
      <div id="s8-p2" class="s8-plus">+</div>
      <div id="s8-t3" class="s8-t"><div class="s8-c" style="background:transparent; border:6px dashed var(--lime); color:var(--lime)">{ic("expand", 120)}</div><div class="t-h3">مساحة</div></div>
      <div id="s8-q1" class="s8-pill">يجرّب</div><div id="s8-q2" class="s8-pill">ويبدأ لوحده</div>
      <div id="s8-res" class="abs" style="background:radial-gradient(circle, rgba(217,119,87,.35), transparent 70%)">{spark("s8-sp", 60, 60, 160, bloom=False)}<div class="ring" id="s8-r1" style="border-radius:50%"></div></div>
      <div id="s8-rl" class="row t-h1 op-y"><span class="mask"><span class="in" id="s8-rl1">النتيجة</span></span></div>
""", """
      fx.maskUp("#s8-h1", 27.15);
      fx.pop("#s8-t1", 27.8, { from: 0.3 });
      fx.pop("#s8-p1", 29.1); fx.pop("#s8-t2", 29.3, { from: 0.3 });
      fx.pop("#s8-p2", 30.35); fx.pop("#s8-t3", 30.55, { from: 0.3 });
      tl.fromTo("#s8-t3 .s8-c", { scale: 0.7 }, { scale: 1.08, duration: 0.8, ease: "power2.out", immediateRender: false }, 30.7);
      fx.rise("#s8-q1", 31.3, { y: 30 }); fx.rise("#s8-q2", 31.9, { y: 30 });
      tl.to("#s8-t1, #s8-t2, #s8-t3, #s8-p1, #s8-p2", { y: -60, scale: 0.86, duration: 0.6, ease: "power2.inOut" }, 32.4);
      tl.to("#s8-q1, #s8-q2", { y: -40, duration: 0.6, ease: "power2.inOut" }, 32.4);
      fx.pop("#s8-res", 33.35, { from: 0.2, e: "expo.out", d: 0.6 });
      tl.fromTo("#s8-sp-svg", { rotation: 0 }, { rotation: 160, duration: 0.8, ease: "power3.out" }, 33.35);
      fx.ringPulse("#s8-r1", 33.5, { scale: 1.6 });
      fx.maskUp("#s8-rl1", 33.45);
""", blob=("#0f4f44", 540, 760))

# ---------------------------------------------------------------- s9 example: this video; NOT a detailed prompt
make("s9", """
    #s9-ph { left: 330px; top: 470px; width: 420px; height: 800px; }
    #s9-v { position: absolute; left: -1461px; top: -171px; width: 3376px; height: 1595px; }
    #s9-doc { left: 190px; top: 450px; width: 700px; height: 880px; }
    #s9-dt { position: absolute; left: 44px; top: 34px; font-family: var(--font-en); font-weight: 900; font-size: 30px; letter-spacing: .2em; color: #6b6a62; direction: ltr; }
    #s9-x { left: 140px; top: 420px; width: 800px; height: 940px; }
    #s9-st { left: 360px; top: 760px; color: var(--orange); border-color: var(--orange); font-size: 110px; background: rgba(4,22,20,.85); }
""", f"""
      {label("s9-lab", 250, "EXAMPLE · THE VIDEO YOU'RE WATCHING")}
      <div class="row t-h1" style="top:290px"><span class="mask"><span class="in" id="s9-h1">مثال</span></span></div>
      <div id="s9-ph" class="op-phone"><div class="scr"><video id="s9-v" src="assets/videos/hf_studio.mp4" data-start="0" data-duration="3.9" data-media-start="0.2" muted playsinline></video></div></div>
      <div id="s9-doc" class="op-doc"><div id="s9-dt">DETAILED PROMPT</div>
        {"".join(f'<i class="ln s9-ln" style="top:{110 + i * 46}px; width:{[600, 540, 610, 480, 590, 560, 400, 610, 520, 580, 450, 600, 530, 570, 490, 610][i]}px"></i>' for i in range(16))}</div>
      <svg id="s9-x" class="abs" viewBox="0 0 800 940"><path id="s9-x1" d="M60 60L740 880" pathLength="1" stroke="#ff5a33" stroke-width="40" stroke-linecap="round" fill="none" /><path id="s9-x2" d="M740 60L60 880" pathLength="1" stroke="#ff5a33" stroke-width="40" stroke-linecap="round" fill="none" /></svg>
      <div id="s9-st" class="stamp">لأ</div>
      <div class="row t-h3" data-layout-allow-overlap style="top:1400px"><span class="mask" data-layout-allow-overlap><span class="in" data-layout-allow-overlap id="s9-k1">اللي بتتفرج عليه ده</span></span></div>
      <div class="row t-h3" data-layout-allow-overlap style="top:1400px"><span class="mask" data-layout-allow-overlap><span class="in" data-layout-allow-overlap id="s9-k2">ما كتبتلوش <span class="lat">prompt</span> تفصيلي</span></span></div>
""", """
      fx.rise("#s9-lab", 34.1, { y: 14 });
      fx.maskUp("#s9-h1", 34.15);
      tl.fromTo("#s9-ph", { opacity: 0, y: 200, rotation: -6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "back.out(1.4)" }, 34.3);
      fx.maskUp("#s9-k1", 36.2);
      tl.to("#s9-k1", { yPercent: -115, duration: 0.3, ease: "power2.in" }, 37.6);
      tl.to("#s9-ph", { x: 700, rotation: 12, opacity: 0, duration: 0.45, ease: "power3.in" }, 37.6);
      tl.fromTo("#s9-doc", { opacity: 0, y: 160 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 37.75);
      tl.fromTo(".s9-ln", { scaleX: 0, transformOrigin: "100% 50%" }, { scaleX: 1, duration: 0.25, ease: "power2.out", stagger: 0.08 }, 38.0);
      fx.maskUp("#s9-k2", 37.9);
      tl.to("#s9-doc", { scale: 1.04, duration: 0.6, ease: "power2.inOut" }, 39.2);
      fx.draw("#s9-x1", 40.35, 0.22, "power2.out"); fx.draw("#s9-x2", 40.5, 0.22, "power2.out");
      tl.to("#s9-doc", { filter: "grayscale(1) brightness(.6)", duration: 0.3 }, 40.4);
      fx.stamp("#s9-st", 40.55, "#s9-cam");
""", blob=("#136052", 540, 880), exit_t=40.42)

# ---------------------------------------------------------------- s10 goal + ideas -> it worked
make("s10", """
    #s10-ring { left: 290px; top: 630px; width: 500px; height: 500px; }
    #s10-g { left: 700px; top: 470px; } #s10-i1 { left: 60px; top: 520px; } #s10-i2 { left: 70px; top: 1220px; } #s10-i3 { left: 680px; top: 1240px; }
    #s10-wk { top: 1420px; }
""", f"""
      <div class="row t-h2" style="top:250px"><span class="mask"><span class="in" id="s10-h1">ادّيته هدف + أفكار</span></span></div>
      <svg id="s10-ring" class="abs" viewBox="0 0 500 500"><circle cx="250" cy="250" r="230" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="14" />
        <circle id="s10-arc" cx="250" cy="250" r="230" fill="none" stroke="#b3ce65" stroke-width="14" stroke-linecap="round" pathLength="1" transform="rotate(-90 250 250)" /></svg>
      {spark("s10-sp", 390, 730, 300)}
      {chip("s10-g", 700, 470, "هدف", ic("target", 34))}
      {chip("s10-i1", 60, 520, "فكرة", ic("bulb", 34), "y")}
      {chip("s10-i2", 70, 1220, "فكرة", ic("bulb", 34), "y")}
      {chip("s10-i3", 680, 1240, "فكرة", ic("bulb", 34), "y")}
      <div id="s10-wk" class="row t-h1 op-l"><span class="mask"><span class="in" id="s10-wk1">وهو اشتغل</span></span></div>
""", """
      fx.maskUp("#s10-h1", 40.5);
      fx.pop("#s10-sp", 40.45, { from: 0.5, e: "expo.out", d: 0.5 });
      fx.pop("#s10-g", 40.85);
      tl.to("#s10-g", { x: -260, y: 330, scale: 0.2, opacity: 0, duration: 0.4, ease: "power3.in" }, 41.6);
      fx.pop("#s10-i1", 42.55); fx.pop("#s10-i2", 42.65); fx.pop("#s10-i3", 42.75);
      tl.to("#s10-i1", { x: 380, y: 300, scale: 0.2, opacity: 0, duration: 0.4, ease: "power3.in" }, 42.95);
      tl.to("#s10-i2", { x: 380, y: -320, scale: 0.2, opacity: 0, duration: 0.4, ease: "power3.in" }, 43.0);
      tl.to("#s10-i3", { x: -200, y: -330, scale: 0.2, opacity: 0, duration: 0.4, ease: "power3.in" }, 43.05);
      tl.fromTo("#s10-sp-svg", { rotation: 0 }, { rotation: 720, duration: 3.6, ease: "power2.in" }, 40.6);
      fx.draw("#s10-arc", 43.25, 0.9, "power2.inOut");
      fx.maskUp("#s10-wk1", 43.2);
      fx.breathe("#s10-sp-bl", 43.3, 1.0, 0.12, 0.5);
""", blob=("#0f4f44", 540, 900))

# ---------------------------------------------------------------- s11 the brief, typed into Claude
make("s11", """
    .s11-slot { position: absolute; left: 110px; width: 860px; height: 110px; border-radius: 26px; border: 3px dashed rgba(179,206,101,.35); }
    #s11-cur { left: 920px; top: 860px; }
""", f"""
      {label("s11-lab", 300, "THE BRIEF")}
      <div class="row t-h2" style="top:350px"><span class="mask"><span class="in" id="s11-h1">قلتله:</span></span></div>
      {claude_input("s11-in", 70, 600, 940, 250, placeholder="How can I help you today?")}
      <div class="s11-slot" id="s11-q1" style="top:960px"></div><div class="s11-slot" id="s11-q2" style="top:1100px"></div><div class="s11-slot" id="s11-q3" style="top:1240px"></div>
      <svg id="s11-cur" class="cursor"><use href="#i-cursor" /></svg>
""", """
      fx.rise("#s11-lab", 44.3, { y: 12 });
      fx.maskUp("#s11-h1", 44.35);
      tl.fromTo("#s11-in", { opacity: 0, y: 120, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, 44.3);
      fx.typeText("#s11-in-t", 45.06, "عايز أعمل فيديو موشن جرافيكس احترافي", 21);
      fx.rise("#s11-q1, #s11-q2, #s11-q3", 47.3, { y: 30, st: 0.12 });
      tl.fromTo("#s11-cur", { opacity: 0, x: 80, y: 120 }, { opacity: 1, x: 0, y: 0, duration: 0.5, ease: "power3.out" }, 47.0);
""", blob=("#136052", 540, 800), push=1.025)

# ---------------------------------------------------------------- s12 idea chips attach
make("s12", """
    .s12-c { position: absolute; left: 110px; width: 860px; height: 110px; border-radius: 26px; background: #0b2f29; border: 3px solid var(--lime);
      display: flex; align-items: center; gap: 24px; padding: 0 30px; direction: rtl; }
    .s12-c .ic { width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--ink); flex: none; }
    .s12-c .ar { font-family: var(--font-ar); font-weight: 800; font-size: 40px; white-space: nowrap; }
    .s12-c .en { margin-right: auto; font-family: var(--font-en); font-weight: 800; font-size: 22px; letter-spacing: .2em; color: var(--fg-muted); direction: ltr; }
    #s12-c1 { top: 960px; } #s12-c2 { top: 1100px; border-color: var(--yellow); } #s12-c3 { top: 1240px; border-color: #e8977c; }
    #s12-cur { left: 920px; top: 860px; }
    #s12-rip { left: 930px; top: 790px; }
    #s12-k { top: 1420px; }
""", f"""
      {label("s12-lab", 300, "IDEAS · NOT INSTRUCTIONS")}
      <div class="row t-h2" style="top:350px"><span class="mask"><span class="in" id="s12-h1">+ شوية أفكار</span></span></div>
      {claude_input("s12-in", 70, 600, 940, 250)}
      <div id="s12-c1" class="s12-c"><span class="ic" style="background:var(--lime)">{ic("film", 40)}</span><span class="ar">أفكار للمشاهد</span><span class="en">SCENES</span></div>
      <div id="s12-c2" class="s12-c"><span class="ic" style="background:var(--yellow)">{ic("sound", 40)}</span><span class="ar">المؤثرات الصوتية</span><span class="en">SFX</span></div>
      <div id="s12-c3" class="s12-c"><span class="ic" style="background:#e8977c">{ic("wand", 40)}</span><span class="ar">المؤثرات البصرية</span><span class="en">VISUALS</span></div>
      <div id="s12-k" class="row t-h3 muted"><span class="mask"><span class="in" id="s12-k1">مش تعليمات خطوة بخطوة</span></span></div>
      <div id="s12-rip" class="ripple"></div>
      <svg id="s12-cur" class="cursor"><use href="#i-cursor" /></svg>
""", """
      fx.Q("#s12-in-t").textContent = "عايز أعمل فيديو موشن جرافيكس احترافي";
      fx.rise("#s12-lab", 48.5, { y: 12 }); fx.maskUp("#s12-h1", 48.5);
      tl.fromTo("#s12-c1", { opacity: 0, x: -200, scale: 0.9 }, { opacity: 1, x: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 48.7);
      tl.fromTo("#s12-c2", { opacity: 0, x: -200, scale: 0.9 }, { opacity: 1, x: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 50.8);
      tl.fromTo("#s12-c3", { opacity: 0, x: -200, scale: 0.9 }, { opacity: 1, x: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 53.45);
      fx.maskUp("#s12-k1", 54.4);
      tl.fromTo("#s12-cur", { opacity: 0, x: 60, y: 160 }, { opacity: 1, x: 0, y: 0, duration: 0.6, ease: "power3.out" }, 55.2);
      fx.click("#s12-cur", 55.95, "#s12-in-s", "#s12-rip");
      tl.to("#s12-in", { boxShadow: "0 0 0 6px rgba(217,119,87,.7), 0 24px 60px rgba(0,0,0,.45)", duration: 0.2 }, 56.0);
""", blob=("#136052", 540, 800), push=1.02, exit_t=55.92)

# ---------------------------------------------------------------- s13 launch, be creative
make("s13", """
    #s13-big { top: 370px; font-family: var(--font-ar); font-weight: 900; font-size: 210px; line-height: 1.25; color: var(--fg); }
    .s13-ray { position: absolute; left: 538px; top: 1110px; width: 6px; height: 260px; background: linear-gradient(var(--lime), transparent); transform-origin: 50% 0; }
""", f"""
      <div class="row t-h3 muted" style="top:220px"><span class="mask"><span class="in" id="s13-h1">بس قلتله</span></span></div>
      <div id="s13-big" class="row" data-layout-allow-overlap><span id="s13-b1" data-layout-allow-overlap style="display:inline-block">انطلق</span></div>
      <div class="row t-h2 op-l" data-layout-allow-overlap style="top:660px"><span class="mask" data-layout-allow-overlap><span class="in" data-layout-allow-overlap id="s13-k1">وكون مبدع</span></span></div>
      {"".join(f'<i class="s13-ray" id="s13-r{i}" style="transform:rotate({i * 45}deg)"></i>' for i in range(8))}
      {spark("s13-sp", 400, 1000, 280)}
      {chip("s13-c1", 600, 1320, "مؤثرات أكتر", "+", "")}
      {chip("s13-c2", 90, 1360, "خطة", "+", "y")}
      {chip("s13-c3", 380, 1560, "أفكار", "+", "o")}
""", """
      fx.maskUp("#s13-h1", 56.3);
      fx.pop("#s13-sp", 56.3, { from: 0.4, e: "expo.out", d: 0.6 });
      tl.fromTo("#s13-sp-svg", { rotation: 0 }, { rotation: 360, duration: 5.2, ease: "none" }, 56.3);
      tl.fromTo("#s13-b1", { opacity: 0, scale: 2.6, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }, 57.85);
      fx.shake("#s13-cam", 57.95, 16, 7);
      tl.to("#s13-sp", { scale: 1.35, duration: 0.4, ease: "expo.out" }, 57.9);
      tl.fromTo(".s13-ray", { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.4, ease: "expo.out" }, 57.9);
      tl.to(".s13-ray", { opacity: 0, duration: 0.6 }, 58.5);
      fx.maskUp("#s13-k1", 58.45);
      fx.pop("#s13-c1", 59.8, { from: 0.2 }); fx.pop("#s13-c2", 60.7, { from: 0.2 }); fx.pop("#s13-c3", 61.25, { from: 0.2 });
""", blob=("#136052", 540, 1100))

# ---------------------------------------------------------------- s14 it writes the plan first
make("s14", """
    #s14-card { left: 150px; top: 560px; width: 780px; height: 820px; }
    #s14-ti { position: absolute; left: 44px; top: 36px; font-family: var(--font-en); font-weight: 900; font-size: 34px; letter-spacing: .14em; color: var(--lime); direction: ltr; }
    .s14-r { position: absolute; right: 50px; width: 680px; height: 90px; display: flex; align-items: center; gap: 26px; direction: rtl; }
    .s14-b { width: 64px; height: 64px; border-radius: 50%; border: 4px solid rgba(179,206,101,.5); flex: none; position: relative; }
    .s14-k { position: absolute; inset: -4px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
    .s14-l { height: 22px; border-radius: 11px; background: rgba(255,255,255,.2); transform-origin: 100% 50%; }
    #s14-sug { left: 340px; top: 430px; }
""", f"""
      <div class="row t-h2" style="top:250px"><span class="mask"><span class="in" id="s14-h1">اعمل انت الخطة الأول</span></span></div>
      {chip("s14-sug", 360, 420, "اقترح", ic("bulb", 32), "y")}
      <div id="s14-card" class="op-card"><div id="s14-ti">PLAN.md</div>
        {"".join(f'<div class="s14-r" style="top:{150 + i * 150}px"><span class="s14-b"><span class="s14-k" id="s14-k{i}">{ic("check", 40)}</span></span><span class="s14-l s14-ln" style="width:{[520, 440, 560, 380][i]}px"></span></div>' for i in range(4))}
      </div>
      <div class="row t-h3 op-l" style="top:1440px"><span class="mask"><span class="in" id="s14-w1">واشتغل عليها</span></span></div>
""", """
      fx.pop("#s14-sug", 61.4);
      tl.to("#s14-sug", { y: -60, opacity: 0, duration: 0.3 }, 62.3);
      fx.maskUp("#s14-h1", 62.4);
      tl.fromTo("#s14-card", { opacity: 0, y: 140 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 61.36);
      tl.fromTo(".s14-ln", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out", stagger: 0.22 }, 62.6);
      fx.pop("#s14-k0", 63.85, { from: 0 }); fx.pop("#s14-k1", 64.1, { from: 0 }); fx.pop("#s14-k2", 64.35, { from: 0 }); fx.pop("#s14-k3", 64.6, { from: 0 });
      fx.maskUp("#s14-w1", 63.9);
""", blob=("#0f4f44", 540, 900))

# ---------------------------------------------------------------- s15 the cost: tokens overflow, long time, mistakes
make("s15", """
    #s15-tr { left: 110px; top: 610px; width: 860px; height: 64px; border-radius: 32px; }
    #s15-tl { top: 540px; }
    #s15-ov { left: 330px; top: 700px; font-size: 54px; padding: 6px 30px; }
    #s15-clk { left: 160px; top: 900px; width: 220px; height: 220px; color: var(--yellow); }
    #s15-hand { left: 160px; top: 900px; width: 220px; height: 220px; }
    #s15-ct { right: 120px; top: 950px; position: absolute; }
    .s15-x { position: absolute; width: 110px; height: 110px; border-radius: 50%; background: var(--orange); display: flex; align-items: center; justify-content: center; color: #fff; }
    #s15-x1 { left: 160px; top: 1300px; } #s15-x2 { left: 485px; top: 1250px; } #s15-x3 { left: 810px; top: 1300px; }
""", f"""
      {label("s15-lab", 250, "FIRST RUN · THE PRICE")}
      <div class="row t-h2" style="top:300px"><span class="mask"><span class="in" id="s15-h1">حرق <span class="lat">tokens</span> كتير جدًا</span></span></div>
      {label("s15-tl", 540, "TOKENS")}
      <div id="s15-tr" class="op-track" data-layout-allow-overflow><div id="s15-fill" class="op-fill" style="background:linear-gradient(270deg, var(--yellow), var(--orange)); border-radius:32px" data-layout-allow-overflow></div></div>
      <div id="s15-ov" class="stamp">OVERLOAD</div>
      <svg id="s15-clk" class="abs"><use href="#i-clock" /></svg>
      <svg id="s15-hand" class="abs" viewBox="0 0 64 64"><path d="M32 32V12" stroke="#ff5a33" stroke-width="4" stroke-linecap="round" /></svg>
      <div id="s15-ct" class="t-h2"><span class="mask"><span class="in" id="s15-c1">وقت طويل</span></span></div>
      <div class="s15-x" id="s15-x1">{ic("x", 70)}</div><div class="s15-x" id="s15-x2">{ic("x", 70)}</div><div class="s15-x" id="s15-x3">{ic("x", 70)}</div>
      <div class="row t-h2 op-o" style="top:1460px"><span class="mask"><span class="in" id="s15-k1">وغلط في حاجات</span></span></div>
""", """
      fx.rise("#s15-lab", 65.0, { y: 12 }); fx.maskUp("#s15-h1", 65.4);
      fx.rise("#s15-tl, #s15-tr", 65.1, { y: 20 });
      tl.fromTo("#s15-fill", { scaleX: 0 }, { scaleX: 1.12, duration: 1.0, ease: "power2.in" }, 65.45);
      fx.stamp("#s15-ov", 66.35, "#s15-cam");
      fx.pop("#s15-clk, #s15-hand", 66.6, { from: 0.3 });
      tl.fromTo("#s15-hand", { rotation: 0 }, { rotation: 1080, duration: 1.6, ease: "power1.inOut", immediateRender: false }, 66.7);
      fx.maskUp("#s15-c1", 66.75);
      fx.pop("#s15-x1", 67.85, { from: 0.2 }); fx.pop("#s15-x2", 68.0, { from: 0.2 }); fx.pop("#s15-x3", 68.15, { from: 0.2 });
      fx.maskUp("#s15-k1", 67.9);
""", blob=("#3a1a12", 540, 700))

# ---------------------------------------------------------------- s16 orbit spiral into the goal
make("s16", """
    #s16-tg { left: 410px; top: 770px; width: 260px; height: 260px; color: var(--yellow); }
    #s16-orb { left: 210px; top: 570px; width: 660px; height: 660px; }
    #s16-arm { left: 540px; top: 900px; width: 0; height: 0; }
    #s16-tgr { left: 410px; top: 770px; width: 260px; height: 260px; border-radius: 50%; }
""", f"""
      <div class="row t-h2" style="top:280px"><span class="mask"><span class="in" id="s16-h1">بس لفّ في إطار</span></span></div>
      <svg id="s16-orb" class="abs" viewBox="0 0 660 660"><circle id="s16-oc" cx="330" cy="330" r="320" fill="none" stroke="rgba(179,206,101,.45)" stroke-width="5" stroke-dasharray="14 18" /></svg>
      <svg id="s16-tg" class="abs"><use href="#i-target" /></svg>
      <div id="s16-tgr" class="abs"><div class="ring" id="s16-r1" style="border-radius:50%; border-color:var(--yellow)"></div><div class="ring" id="s16-r2" style="border-radius:50%; border-color:var(--yellow)"></div></div>
      <div id="s16-arm" class="abs"><div id="s16-off" class="abs" style="left:0; top:0">{spark("s16-sp", -60, -60, 120, bloom=False)}</div></div>
      <div class="row t-h2" style="top:1300px"><span class="mask"><span class="in" id="s16-k1">عشان يحقق</span></span></div>
      <div class="row t-h1 op-y" style="top:1430px"><span class="mask"><span class="in" id="s16-k2">الهدف</span></span></div>
""", """
      fx.maskUp("#s16-h1", 68.6);
      fx.pop("#s16-tg", 68.6, { from: 0.4 });
      tl.fromTo("#s16-orb", { opacity: 0, scale: 0.6, rotation: 0 }, { opacity: 1, scale: 1, rotation: 60, duration: 3.4, ease: "power1.out" }, 68.7);
      tl.fromTo("#s16-off", { x: 320 }, { x: 0, duration: 2.4, ease: "power2.in" }, 69.5);
      tl.fromTo("#s16-arm", { rotation: 0, opacity: 0 }, { rotation: -900, opacity: 1, duration: 2.4, ease: "power1.in" }, 69.5);
      tl.fromTo("#s16-sp-svg", { rotation: 0 }, { rotation: 900, duration: 2.4, ease: "power1.in" }, 69.5);
      tl.to("#s16-sp", { scale: 1.6, duration: 0.3, ease: "expo.out" }, 71.9);
      fx.ringPulse("#s16-r1, #s16-r2", 71.92, { scale: 2.4 });
      tl.to("#s16-orb", { opacity: 0, duration: 0.3 }, 71.9);
      fx.shake("#s16-cam", 71.92, 12, 6);
      fx.maskUp("#s16-k1", 70.95);
      fx.maskUp("#s16-k2", 71.85);
""", blob=("#136052", 540, 900), push=1.02)

# ---------------------------------------------------------------- s17 the real result
make("s17", """
    #s17-win { left: 40px; top: 600px; width: 1000px; height: 526px; }
    #s17-vw { position: absolute; left: 0; top: 0; width: 1000px; height: 472px; transform-origin: 49% 32%; }
    #s17-v { left: 0; top: 0; width: 1000px; height: 472px; }
    #s17-st { left: 250px; top: 1230px; color: var(--lime); border-color: var(--lime); font-size: 72px; background: rgba(4,22,20,.9); }
    #s17-src { top: 1420px; }
""", f"""
      <div class="row t-h2" style="top:300px"><span class="mask"><span class="in" id="s17-h1">وبالفعل طلّعلي</span></span></div>
      <div id="s17-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>HyperFrames Studio</b></div>
        <div class="body"><div id="s17-vw"><video id="s17-v" class="abs" src="assets/videos/hf_studio.mp4" data-start="0" data-duration="2.85" data-media-start="0.8" muted playsinline></video></div></div></div>
      <div id="s17-st" class="stamp">نتيجة ممتازة</div>
      <div id="s17-src" class="op-src">REAL PROJECT · BUILT WITH CLAUDE OPUS 5.5</div>
""", """
      fx.maskUp("#s17-h1", 72.2);
      tl.fromTo("#s17-win", { opacity: 0, y: 160, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, 72.05);
      tl.fromTo("#s17-vw", { scale: 1 }, { scale: 1.9, duration: 0.9, ease: "power3.inOut" }, 72.8);
      fx.stamp("#s17-st", 73.6, "#s17-cam");
      fx.rise("#s17-src", 73.9, { y: 10, b: 0 });
""", blob=("#136052", 540, 900), push=None)

# ---------------------------------------------------------------- s18 next: part 2
make("s18", """
    #s18-c1 { left: 80px; top: 520px; width: 260px; height: 400px; }
    #s18-c2b, #s18-c2 { left: 370px; top: 470px; width: 340px; height: 510px; }
    #s18-c3 { left: 740px; top: 520px; width: 260px; height: 400px; }
    .s18-n { position: absolute; left: 0; right: 0; text-align: center; }
    .s18-lk { position: absolute; left: 50%; top: 50%; width: 80px; height: 80px; margin: -40px 0 0 -40px; color: rgba(179,206,101,.55); }
    #s18-dn { position: absolute; right: 20px; top: 20px; width: 60px; height: 60px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
    #s18-loop { left: 465px; top: 1560px; width: 150px; height: 150px; color: var(--orange); }
    #s18-lx { left: 570px; top: 1545px; }
    #s18-lt { position: absolute; left: 0; right: 0; text-align: center; top: 1410px; }
""", f"""
      {label("s18-lab", 250, "NEXT EPISODE")}
      <div class="row t-h2" style="top:300px"><span class="mask"><span class="in" id="s18-h1">في الفيديو الجاي</span></span></div>
      <div id="s18-c1" class="op-card" style="opacity:.75">
        <div class="s18-n op-en" data-layout-allow-overlap style="top:110px; font-size:30px; letter-spacing:.3em; color:var(--lime)">TIP</div>
        <div class="s18-n op-en op-y" data-layout-allow-overlap style="top:165px; font-size:130px; line-height:1">01</div><div id="s18-dn">{ic("check", 40)}</div></div>
      <div id="s18-c3" class="op-card back"><svg class="s18-lk"><use href="#i-lock" /></svg></div>
      <div id="s18-c2b" class="op-card back"><svg class="s18-lk"><use href="#i-lock" /></svg></div>
      <div id="s18-c2" class="op-card">
        {spark("s18-sp", 115, 40, 110, bloom=False)}
        <div class="s18-n op-en" data-layout-allow-overlap style="top:170px; font-size:36px; letter-spacing:.3em; color:var(--lime)">PART</div>
        <div class="s18-n op-en op-y" data-layout-allow-overlap style="top:230px; font-size:190px; line-height:1">02</div>
        <div class="s18-n op-en" data-layout-allow-overlap style="top:450px; font-size:28px; color:var(--fg-muted)">COMING NEXT</div></div>
      <div class="row t-h2" style="top:1060px"><span class="mask"><span class="in" id="s18-k1">ازاي تطلّع النتايج دي</span></span></div>
      <div class="row t-h1" style="top:1210px"><span class="hl" id="s18-hl"><span class="band" id="s18-band"></span><span class="txt">كل مرة</span></span></div>
      <svg id="s18-loop" class="abs"><use href="#i-loop" /></svg>
      <div id="s18-lx" class="xbadge" style="width:80px; height:80px; color:#fff">{ic("x", 54)}</div>
      <div id="s18-lt" class="t-h3"><span class="mask"><span class="in" id="s18-l1">من غير ما تعيد كل حاجة</span></span></div>
""", """
      fx.rise("#s18-lab", 74.85, { y: 12 }); fx.maskUp("#s18-h1", 74.9);
      fx.rise("#s18-c1", 75.0, { y: 80 }); fx.rise("#s18-c3", 75.1, { y: 80 }); fx.rise("#s18-c2b", 75.2, { y: 120 });
      fx.hide("#s18-c2");
      tl.to("#s18-c2b", { scaleX: 0, duration: 0.16, ease: "power2.in" }, 76.95);
      tl.fromTo("#s18-c2", { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.22, ease: "power2.out", immediateRender: false }, 77.11);
      tl.fromTo("#s18-sp-svg", { rotation: 0 }, { rotation: 200, duration: 5.5, ease: "none" }, 77.1);
      fx.breathe("#s18-c2", 77.6, 5.0, 0.02, 1.6);
      fx.maskUp("#s18-k1", 78.15);
      fx.pop("#s18-hl", 79.95, { from: 0.6 }); fx.band("#s18-band", 80.05);
      fx.pop("#s18-loop", 81.1, { from: 0.3 });
      tl.fromTo("#s18-loop", { rotation: 0 }, { rotation: 360, duration: 1.0, ease: "power1.inOut", immediateRender: false }, 81.2);
      fx.maskUp("#s18-l1", 81.2);
      fx.pop("#s18-lx", 82.0, { from: 0.2 });
""", blob=("#136052", 540, 760))

# ---------------------------------------------------------------- s19 CTA: Hossam + follow
make("s19", """
    #s19-plate { left: 120px; top: 1300px; width: 840px; height: 170px; border-radius: 30px; background: rgba(4,22,20,.82); border: 2px solid rgba(179,206,101,.45); }
    #s19-nm { position: absolute; left: 0; right: 0; top: 18px; text-align: center; }
    #s19-en { position: absolute; left: 0; right: 0; top: 112px; text-align: center; }
    #s19-btn { left: 300px; top: 1530px; }
    #s19-btn2 { left: 300px; top: 1530px; }
    #s19-cur { left: 640px; top: 1600px; }
    #s19-rip { left: 560px; top: 1580px; }
    #s19-glow { left: 90px; top: 520px; width: 900px; height: 900px; border-radius: 50%; background: radial-gradient(circle, rgba(19,96,82,.9), transparent 68%); }
""", f"""
      <div class="row t-h3" style="top:240px"><span class="mask"><span class="in" id="s19-h1">لو عايز تعرف كل جديد في</span></span></div>
      <div class="row t-h2 op-l" style="top:330px"><span class="mask"><span class="in" id="s19-h2">عالم الذكاء الاصطناعي</span></span></div>
      <div id="s19-glow" class="abs"></div>
      {hossam("s19-hs", 170, 560, 740)}
      <div id="s19-plate" class="abs"><div id="s19-nm" class="t-h3">حسام الدين حسن</div><div id="s19-en" class="t-label" style="color:var(--lime)">HOSSAMUDIN HASSAN · AI</div></div>
      <div id="s19-btn" class="op-btn">{ic("person", 44, "#fff")} اعمل فولو</div>
      <div id="s19-btn2" class="op-btn on">{ic("check", 44, "var(--lime)")} متابِع</div>
      <div id="s19-rip" class="ripple"></div>
      <svg id="s19-cur" class="cursor"><use href="#i-cursor" /></svg>
""", """
      fx.maskUp("#s19-h1", 83.05); fx.maskUp("#s19-h2", 84.6);
      tl.fromTo("#s19-glow", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.8, ease: "power2.out" }, 83.0);
      tl.fromTo("#s19-hs", { opacity: 0, y: 260 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, 83.1);
      tl.fromTo("#s19-plate", { opacity: 0, y: 60, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 85.35);
      fx.pop("#s19-btn", 85.9, { from: 0.4 });
      fx.hide("#s19-btn2");
      tl.fromTo("#s19-cur", { opacity: 0, x: 200, y: 160 }, { opacity: 1, x: 0, y: 0, duration: 0.45, ease: "power3.out" }, 85.95);
      fx.click("#s19-cur", 86.35, "#s19-btn", "#s19-rip");
      tl.to("#s19-btn", { opacity: 0, duration: 0.1 }, 86.45);
      tl.to("#s19-btn2", { opacity: 1, duration: 0.1 }, 86.45);
""", blob=("#136052", 540, 1000), push=1.02, exit_t=88.25)

print("tip1 scenes written")
