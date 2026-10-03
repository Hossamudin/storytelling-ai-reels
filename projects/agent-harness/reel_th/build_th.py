# Talking-head version of the Agent Harness reel: new full-screen / canvas scenes.
# Reused v1 scenes (s4 s5 s6 s7 s11 s17 s19 s21) come from build_scenes.py (guarded by scenes.json).
# The presenter layer (video, text-behind, matte, captions, front overlays) is built by build_root.py.
# Real data only: Artificial Analysis coding-agents page + Arena AI "HarnessTax" (captured 2026-10-01).
from build_scenes import make, core, brackets, lines, L, Y, O, T, W  # noqa: F401  (importing also builds the reused scenes)

# ---------------------------------------------------------------- b1 b-roll: engine core = the machine
make("b1", """
    #b1-v { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
    #b1-sh { position: absolute; left: 0; right: 0; top: 0; height: 620px; background: linear-gradient(180deg, rgba(4,22,20,.92), rgba(4,22,20,0)); }
    #b1-lab { top: 210px; } #b1-h { top: 250px; }
    #b1-tg { left: 0; right: 0; top: 1600px; text-align: center; }
""", """
      <video id="b1-v" src="assets/higgsfield/broll_engine_core.mp4" data-start="0" data-duration="4.6" muted playsinline></video>
      <div id="b1-sh"></div>
      <div id="b1-lab" class="row"><span class="t-label">THE AI MODEL</span></div>
      <div id="b1-h" class="row t-h1" data-layout-allow-overlap><span class="mask"><span class="in" id="b1-h1">الموديل = <span class="hl"><span class="band" id="b1-band"></span><span class="txt" id="b1-txt" style="color:var(--yellow)">الآلة</span></span></span></span></div>
      <div id="b1-tg" class="ah-tag">THE ENGINE · GENERATES CODE</div>
""", """
      fx.rise("#b1-lab", 8.95, { y: 16 });
      fx.maskUp("#b1-h1", 9.0);
      fx.band("#b1-band", 10.3);
      tl.to("#b1-txt", { color: "#0d0d0d", duration: 0.15 }, 10.4);
      fx.rise("#b1-tg", 11.6, { y: 16 });
""", blob=("#136052", 540, 900), push=1.06)

# ---------------------------------------------------------------- c1 canvas: prompt -> engine -> code (presenter card on top)
make("c1", """
    #c1-p { left: 110px; top: 960px; width: 860px; height: 130px; }
    #c1-pt { position: absolute; right: 34px; top: 32px; font-size: 44px; font-weight: 700; white-space: nowrap; direction: rtl; }
    #c1-img { position: absolute; left: 430px; top: 1120px; width: 220px; height: 220px; border-radius: 50%;
      -webkit-mask-image: radial-gradient(circle, #000 58%, transparent 71%); mask-image: radial-gradient(circle, #000 58%, transparent 71%); }
    #c1-code { left: 190px; top: 1390px; width: 700px; height: 300px; }
    #c1-ar { left: 520px; top: 1092px; width: 40px; height: 40px; }
""", f"""
      <div id="c1-p" class="window"><div id="c1-pt"><span id="c1-pt1"></span><span class="caret" id="c1-car"></span></div></div>
      <svg id="c1-ar" class="abs" viewBox="0 0 40 40"><path id="c1-ap" pathLength="1" d="M20 2 V30 M8 20 L20 34 L32 20" fill="none" stroke="#b3ce65" stroke-width="5" stroke-linecap="round" /></svg>
      <img id="c1-img" src="assets/higgsfield/engine_core.png" alt="" />
      <div id="c1-code" class="ah-code">{lines("c1-l", [(70, L), (52, W), (88, Y), (44, W), (66, T)])}</div>
""", """
      fx.pop("#c1-p", 13.45, { from: 0.85, e: "power3.out" });
      fx.typeText("#c1-pt1", 13.6, "اكتب لي كود يعمل…", 22);
      tl.fromTo("#c1-car", { opacity: 1 }, { opacity: 0.15, duration: 0.2, ease: "steps(1)", yoyo: true, repeat: 7 }, 13.5);
      fx.draw("#c1-ap", 14.3, 0.25);
      fx.pop("#c1-img", 14.35, { from: 0.4, e: "back.out(2)" });
      fx.breathe("#c1-img", 14.8, 1.4, 0.06, 0.7);
      fx.pop("#c1-code", 14.85, { from: 0.7, e: "power3.out" });
      tl.fromTo("#c1-code .ah-ln", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.25, ease: "power2.out", stagger: 0.12 }, 15.0);
""", blob=("#136052", 540, 1300), push=None, exit_t=16.2)

# ---------------------------------------------------------------- b2 b-roll: the harness locks around the core
make("b2", """
    #b2-v { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
    #b2-sh { position: absolute; left: 0; right: 0; bottom: 0; height: 760px; background: linear-gradient(0deg, rgba(4,22,20,.95), rgba(4,22,20,0)); }
    #b2-lab { top: 1380px; } #b2-h { top: 1420px; }
""", """
      <video id="b2-v" src="assets/higgsfield/broll_harness_lock.mp4" data-start="0" data-duration="2.35" data-media-start="2.5" muted playsinline></video>
      <div id="b2-sh"></div>
      <div id="b2-lab" class="row"><span class="t-label" style="color:var(--lime)">THE HARNESS</span></div>
      <div id="b2-h" class="row t-h2"><span class="mask"><span class="in" id="b2-h1">لازم يبقى جوّه برنامج</span></span></div>
""", """
      fx.rise("#b2-lab", 37.35, { y: 16 });
      fx.maskUp("#b2-h1", 37.4);
""", blob=("#136052", 540, 900), push=1.05, exit_t=39.45)

# ---------------------------------------------------------------- l1 harness lineup
make("l1", """
    #l1-k { top: 330px; }
    .l1-h { position: absolute; left: 110px; width: 860px; height: 190px; border-radius: 34px; border: 4px solid var(--lime); background: linear-gradient(270deg, rgba(179,206,101,.14), rgba(179,206,101,.02));
      display: flex; align-items: center; justify-content: space-between; padding: 0 50px; direction: ltr; }
    .l1-h b { font-family: var(--font-en); font-weight: 900; font-size: 74px; color: var(--fg); }
    .l1-h i { font-style: normal; font-family: var(--font-en); font-weight: 900; font-size: 26px; letter-spacing: .2em; color: var(--lime); }
    #l1-h1 { top: 560px; } #l1-h2 { top: 790px; } #l1-h3 { top: 1020px; }
    #l1-more { left: 0; right: 0; top: 1280px; text-align: center; }
""", """
      <div id="l1-k" class="row t-h3"><span class="mask"><span class="in" id="l1-k1">أنهي <span class="lat" style="color:var(--lime)">Agent Harness</span> تستخدم؟</span></span></div>
      <div class="l1-h" id="l1-h1"><b>Claude Code</b><i>HARNESS 01</i></div>
      <div class="l1-h" id="l1-h2"><b>OpenCode</b><i>HARNESS 02</i></div>
      <div class="l1-h" id="l1-h3"><b>Pi</b><i>HARNESS 03</i></div>
      <div id="l1-more" class="abs"><span class="pill">أو غيرهم…</span></div>
""", """
      fx.maskUp("#l1-k1", 47.1);
      [["#l1-h1", 47.12], ["#l1-h2", 47.75], ["#l1-h3", 48.3]].forEach(([s, t]) => {
        tl.fromTo(s, { opacity: 0, x: 700, filter: "blur(16px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, t);
      });
      fx.pop("#l1-more", 48.9, { from: 0.4 });
""", blob=("#136052", 540, 900), exit_t=49.15)

# ---------------------------------------------------------------- aa1 real: Artificial Analysis Coding Agent Index (pan R->L)
make("aa1", """
    #aa1-lab { top: 210px; } #aa1-h { top: 250px; font-size: 64px; }
    #aa1-win { left: 50px; top: 430px; width: 980px; height: 820px; }
    #aa1-vp { position: absolute; left: 0; right: 0; top: 56px; bottom: 0; overflow: hidden; background: #fff; }
    #aa1-img { position: absolute; left: 0; top: 40px; width: 1500px; height: 772px; }
    #aa1-k { top: 1300px; font-size: 64px; }
    #aa1-src { top: 1430px; }
""", """
      <div id="aa1-lab" class="row"><span class="t-label">SOURCE 01 · ARTIFICIAL ANALYSIS</span></div>
      <div id="aa1-h" class="row ah-en"><span class="mask"><span class="in" id="aa1-h1">Coding Agent Index</span></span></div>
      <div id="aa1-win" class="window"><div class="bar"><i></i><i></i><i></i><b>ARTIFICIALANALYSIS.AI/AGENTS/CODING-AGENTS</b></div>
        <div id="aa1-vp" data-layout-allow-overflow><img id="aa1-img" src="assets/images/aa/index_bars.png" alt="" /></div></div>
      <div id="aa1-k" class="row t-h2"><span class="mask"><span class="in" id="aa1-k1">الـ<span class="lat ah-l">Harness</span> كمان ليه ترتيب</span></span></div>
      <div id="aa1-src" class="row"><span class="t-label">REAL DATA · CAPTURED OCT 2026</span></div>
""", """
      fx.rise("#aa1-lab", 52.35, { y: 16 });
      fx.maskUp("#aa1-h1", 52.4);
      tl.fromTo("#aa1-win", { opacity: 0, y: 260 }, { opacity: 1, y: 0, duration: 0.55, ease: "expo.out" }, 52.45);
      tl.fromTo("#aa1-img", { x: 0 }, { x: -520, duration: 3.3, ease: "power1.inOut" }, 52.6);
      fx.maskUp("#aa1-k1", 53.3);
      fx.rise("#aa1-src", 53.8, { y: 10 });
""", blob=("#136052", 540, 900), exit_t=55.65)

# ---------------------------------------------------------------- aa2 real: time per task -> cost per task
make("aa2", """
    #aa2-lab { top: 210px; } #aa2-h { top: 250px; } #aa2-h2 { top: 250px; }
    .aa2-card { position: absolute; left: 90px; top: 440px; width: 900px; height: 968px; border-radius: 30px; overflow: hidden; background: #fff; box-shadow: 0 30px 70px rgba(0,0,0,.45); }
    .aa2-card img { position: absolute; left: 0; top: 0; width: 900px; height: 968px; }
    .aa2-ring { position: absolute; border-radius: 22px; border: 7px solid var(--orange); }
    #aa2-src { top: 1460px; }
    .aa2-tg { position: absolute; padding: 6px 22px; border-radius: 22px; font-weight: 800; font-size: 36px; }
""", """
      <div id="aa2-lab" class="row"><span class="t-label">ARTIFICIAL ANALYSIS · REAL DATA</span></div>
      <div id="aa2-h" class="row t-h3"><span class="mask"><span class="in" id="aa2-h1">مين بياخد وقت أكتر؟</span></span></div>
      <div id="aa2-h2" class="row t-h3"><span class="mask"><span class="in" id="aa2-h21">ومين بيكلّف أكتر… أو أقل؟</span></span></div>
      <div class="aa2-card" id="aa2-t"><img src="assets/images/aa/time_card.png" alt="" />
        <div class="aa2-ring" id="aa2-r1" style="left:768px; top:300px; width:90px; height:390px"></div></div>
      <div class="aa2-card" id="aa2-c"><img src="assets/images/aa/cost_card.png" alt="" />
        <div class="aa2-ring" id="aa2-r2" style="left:765px; top:300px; width:92px; height:390px"></div>
        <div class="aa2-ring" id="aa2-r3" style="left:92px; top:620px; width:90px; height:60px; border-color:#437f3e"></div></div>
      <div class="aa2-tg" id="aa2-g1" style="left:640px; top:1430px; background:var(--orange); color:#fff">أغلى · <span class="lat">$14.2</span></div>
      <div class="aa2-tg" id="aa2-g2" style="left:110px; top:1430px; background:var(--lime); color:#0d0d0d">أرخص · <span class="lat">$1.04</span></div>
      <div id="aa2-src" class="row" style="top:1560px"><span class="t-label">COST PER TASK · USD · LOWER IS BETTER</span></div>
""", """
      fx.rise("#aa2-lab", 66.65, { y: 16 });
      fx.maskUp("#aa2-h1", 66.7);
      tl.fromTo("#aa2-t", { opacity: 0, y: 300, rotation: -3 }, { opacity: 1, y: 0, rotation: 0, duration: 0.55, ease: "expo.out" }, 66.75);
      tl.fromTo("#aa2-r1", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 68.7);
      // flip to cost
      tl.to("#aa2-h1", { yPercent: -115, duration: 0.3, ease: "power3.in" }, 69.4);
      tl.to("#aa2-h", { opacity: 0, duration: 0.01 }, 69.7);
      tl.fromTo("#aa2-h2", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 69.72);
      tl.to("#aa2-t", { rotationY: 90, opacity: 0, duration: 0.28, ease: "power2.in" }, 69.4);
      tl.fromTo("#aa2-c", { rotationY: -90, opacity: 0 }, { rotationY: 0, opacity: 1, duration: 0.35, ease: "back.out(1.4)" }, 69.68);
      fx.maskUp("#aa2-h21", 69.75);
      tl.fromTo("#aa2-r2", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 70.95);
      fx.pop("#aa2-g1", 71.0, { from: 0.4 });
      tl.fromTo("#aa2-r3", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 71.55);
      fx.pop("#aa2-g2", 71.6, { from: 0.4 });
      fx.rise("#aa2-src", 70.0, { y: 10 });
""", blob=("#136052", 540, 900), exit_t=72.45)

# ---------------------------------------------------------------- ar1 real: Arena AI HarnessTax article
make("ar1", """
    #ar1-lab { top: 210px; } #ar1-h { top: 250px; }
    #ar1-win { left: 70px; top: 440px; width: 940px; height: 584px; }
    #ar1-win img { position: absolute; left: 0; top: 56px; width: 940px; height: 528px; }
    #ar1-new { left: 70px; top: 1060px; }
    #ar1-dt { left: 230px; top: 1066px; font-family: var(--font-en); font-weight: 800; font-size: 32px; color: var(--fg-muted); direction: ltr; }
    #ar1-name { top: 1150px; font-size: 120px; }
    #ar1-q { left: 70px; top: 1330px; width: 940px; height: 300px; }
    #ar1-qa { position: absolute; right: 40px; left: 40px; top: 40px; font-size: 54px; font-weight: 800; line-height: 1.4; direction: rtl; }
    #ar1-qe { position: absolute; left: 40px; right: 40px; top: 200px; font-family: var(--font-en); font-size: 28px; font-weight: 600; font-style: italic; color: var(--fg-muted); direction: ltr; }
""", """
      <div id="ar1-lab" class="row"><span class="t-label">SOURCE 02 · ARENA AI · RESEARCH</span></div>
      <div id="ar1-h" class="row t-h2"><span class="mask"><span class="in" id="ar1-h1">مصدر تاني… لسه طالع</span></span></div>
      <div id="ar1-win" class="window"><div class="bar"><i></i><i></i><i></i><b>ARENA.AI/BLOG/CODING-AGENTS-HARNESS-TAX</b></div><img src="assets/images/arena/hero.png" alt="" /></div>
      <div id="ar1-new" class="abs"><span class="pill bad" style="font-family:var(--font-en); font-size:28px; height:60px; letter-spacing:.12em">NEW</span></div>
      <div id="ar1-dt" class="abs">16 SEPT 2026</div>
      <div id="ar1-name" class="row ah-en"><span class="mask"><span class="in" id="ar1-n1">Arena AI</span></span></div>
      <div id="ar1-q" class="card"><div id="ar1-qa">اختيار الـ<span class="hl"><span class="band" id="ar1-band" style="background:var(--lime)"></span><span class="txt lat" id="ar1-ht" style="color:var(--lime)">Harness</span></span> بيأثر جدًا على التكلفة</div>
        <div id="ar1-qe">“harness choice can significantly impact cost” — Arena AI</div></div>
""", """
      fx.rise("#ar1-lab", 78.05, { y: 16 });
      fx.maskUp("#ar1-h1", 78.1);
      tl.fromTo("#ar1-win", { opacity: 0, y: 400, rotation: 4 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "expo.out" }, 79.1);
      fx.pop("#ar1-new", 79.95, { from: 0.3 });
      fx.rise("#ar1-dt", 80.15, { y: 10 });
      fx.maskUp("#ar1-n1", 81.6);
      fx.rise("#ar1-q", 82.55, { y: 30 });
      fx.band("#ar1-band", 83.85);
      tl.to("#ar1-ht", { color: "#0d0d0d", duration: 0.15 }, 83.95);
""", blob=("#136052", 540, 900), exit_t=84.05)

# ---------------------------------------------------------------- ar2 real: Arena Pareto chart ride
# chart0.png 1530x1452 shown at k=0.6536 -> 1000x949 at (40,560). Point px -> frame: (40+x*k, 560+y*k)
K, OX, OY = 1000 / 1530, 40, 560
def P(x, y):
    return round(OX + x * K), round(OY + y * K)
luna = P(348, 722); fcx = P(1145, 488); fcc = P(1244, 482); fpi = P(1073, 488)
make("ar2", f"""
    #ar2-lab {{ top: 210px; }} #ar2-h {{ top: 250px; }}
    #ar2-world {{ position: absolute; inset: 0; transform-origin: 540px 1030px; }}
    #ar2-card {{ left: 30px; top: 545px; width: 1020px; height: 980px; border-radius: 30px; background: #fafaf7; box-shadow: 0 30px 70px rgba(0,0,0,.45); }}
    #ar2-img {{ position: absolute; left: {OX}px; top: {OY}px; width: 1000px; height: 949px; }}
    .ar2-ring {{ position: absolute; width: 74px; height: 74px; margin: -37px 0 0 -37px; border-radius: 50%; border: 6px solid var(--orange); }}
    .ar2-pl {{ position: absolute; white-space: nowrap; padding: 8px 20px; border-radius: 22px; font-family: var(--font-en); font-weight: 900; font-size: 28px; direction: ltr; }}
    .ar2-tag {{ position: absolute; white-space: nowrap; padding: 6px 20px; border-radius: 20px; font-weight: 800; font-size: 34px; }}
    #ar2-svg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    #ar2-cr {{ position: absolute; left: {fpi[0] - 40}px; top: {fpi[1] - 140}px; width: 80px; height: 80px; color: var(--yellow); }}
    #ar2-k {{ top: 1560px; }}
    #ar2-top {{ position: absolute; left: 0; right: 0; top: 0; height: 400px; background: linear-gradient(180deg, #041614 70%, rgba(4,22,20,0)); }}
    #ar2-k .in {{ background: rgba(4,22,20,.85); border-radius: 30px; padding: 0 40px; }}
    #ar2-src {{ top: 1720px; }}
""", f"""
      <div id="ar2-world">
        <div id="ar2-card" class="abs"></div>
        <img id="ar2-img" src="assets/images/arena/chart0.png" alt="" />
        <svg id="ar2-svg" viewBox="0 0 1080 1920">
          <path id="ar2-l" pathLength="1" d="M{fcx[0] - 60} {fcx[1] + 260} H{luna[0] + 40}" fill="none" stroke="#437f3e" stroke-width="12" stroke-linecap="round" />
          <path id="ar2-lh" pathLength="1" d="M{luna[0] + 80} {fcx[1] + 225} L{luna[0] + 36} {fcx[1] + 260} L{luna[0] + 80} {fcx[1] + 295}" fill="none" stroke="#437f3e" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" />
          <path id="ar2-u" pathLength="1" d="M{fpi[0] - 120} {fcx[1] + 240} V{fpi[1] + 40}" fill="none" stroke="#437f3e" stroke-width="12" stroke-linecap="round" />
          <path id="ar2-uh" pathLength="1" d="M{fpi[0] - 155} {fpi[1] + 80} L{fpi[0] - 120} {fpi[1] + 36} L{fpi[0] - 85} {fpi[1] + 80}" fill="none" stroke="#437f3e" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <div class="ar2-ring" id="ar2-r1" style="left:{luna[0]}px; top:{luna[1]}px"></div>
        <div class="ar2-pl" id="ar2-p1" style="left:{luna[0] - 40}px; top:{luna[1] + 50}px; background:#0d0d0d; color:#fff">Codex + GPT-5.6</div>
        <div class="ar2-ring" id="ar2-r2" style="left:{fcx[0]}px; top:{fcx[1]}px"></div>
        <div class="ar2-pl" id="ar2-p2" style="left:{fcx[0] - 300}px; top:{fcx[1] + 60}px; background:#0d0d0d; color:#fff">Codex + Fable 5</div>
        <div class="ar2-tag" id="ar2-t1" style="left:{fcx[0] - 120}px; top:{fcx[1] + 130}px; background:var(--lime); color:#0d0d0d">↑ أذكى</div>
        <div class="ar2-tag" id="ar2-t2" style="left:{fcx[0] + 10}px; top:{fcx[1] + 130}px; background:var(--orange); color:#fff">أغلى →</div>
        <div class="ar2-tag" id="ar2-t3" style="left:{luna[0] + 90}px; top:{fcx[1] + 290}px; background:#437f3e; color:#fff">← أوفر</div>
        <div class="ar2-ring" id="ar2-r3" style="left:{fpi[0]}px; top:{fpi[1]}px; border-color:#437f3e; width:92px; height:92px; margin:-46px 0 0 -46px"></div>
        <svg id="ar2-cr"><use href="#i-crown" /></svg>
      </div>
      <div id="ar2-top"></div>
      <div id="ar2-lab" class="row"><span class="t-label">ARENA AI · SWE-BENCH LITE · REAL DATA</span></div>
      <div id="ar2-h" class="row t-h3"><span class="mask"><span class="in" id="ar2-h1">الموديل + الـ<span class="lat ah-l">Harness</span></span></span></div>
      <div id="ar2-k" class="row t-h1"><span class="mask"><span class="in" id="ar2-k1"><span class="lat ah-l">Pi</span> هو الأفضل</span></span></div>
      <div id="ar2-src" class="row"><span class="t-label">ARENA.AI · HARNESSTAX · FIG. 1</span></div>
""", f"""
      fx.rise("#ar2-lab", 88.45, {{ y: 16 }});
      tl.fromTo("#ar2-card, #ar2-img", {{ opacity: 0, y: 300 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }}, 88.5);
      fx.maskUp("#ar2-h1", 91.1);
      fx.rise("#ar2-src", 89.4, {{ y: 10 }});
      // Codex + GPT-5.6 (left, cheap)
      tl.to("#ar2-world", {{ scale: 1.55, x: {round((540 - luna[0]) * 1.55 * 0.6)}, y: {round((1030 - luna[1]) * 1.55 * 0.6)}, duration: 0.9, ease: "power3.inOut" }}, 93.3);
      fx.pop("#ar2-r1", 93.65, {{ from: 2 }});
      fx.rise("#ar2-p1", 93.8, {{ y: 14 }});
      // Codex + Fable 5 (up and right)
      tl.to("#ar2-world", {{ scale: 1.55, x: {round((540 - fcx[0]) * 1.55 * 0.7)}, y: {round((1030 - fcx[1]) * 1.55 * 0.5)}, duration: 0.9, ease: "power3.inOut" }}, 96.2);
      fx.pop("#ar2-r2", 96.95, {{ from: 2 }});
      fx.rise("#ar2-p2", 97.1, {{ y: 14 }});
      fx.pop("#ar2-t1", 98.75, {{ from: 0.3 }});
      fx.pop("#ar2-t2", 100.65, {{ from: 0.3 }});
      // pull back for the circle presenter, then go left (cheaper) and up (smarter)
      tl.to("#ar2-world", {{ scale: 1, x: 0, y: -80, duration: 0.9, ease: "power3.inOut" }}, 101.2);
      fx.draw("#ar2-l", 104.75, 0.5); fx.draw("#ar2-lh", 105.2, 0.2);
      fx.pop("#ar2-t3", 105.1, {{ from: 0.3 }});
      fx.draw("#ar2-u", 106.8, 0.5); fx.draw("#ar2-uh", 107.25, 0.2);
      // Pi + Fable 5 wins
      tl.to("#ar2-world", {{ scale: 1.45, x: {round((540 - fpi[0]) * 1.45 * 0.8)}, y: {round((1030 - fpi[1]) * 1.45 * 0.8)}, duration: 1.0, ease: "power3.inOut" }}, 107.9);
      fx.pop("#ar2-r3", 108.15, {{ from: 2.4 }});
      tl.fromTo("#ar2-cr", {{ opacity: 0, y: -80, rotation: -20 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "back.out(2)" }}, 108.4);
      fx.maskUp("#ar2-k1", 109.3);
""", blob=("#136052", 540, 900), push=None, exit_t=110.15)

# ---------------------------------------------------------------- src: the two sources (real screenshots)
make("src", """
    #src-lab { top: 210px; } #src-h { top: 250px; }
    .src-c { position: absolute; left: 90px; width: 900px; height: 600px; border-radius: 30px; overflow: hidden; background: #fff; box-shadow: 0 30px 70px rgba(0,0,0,.45); }
    .src-c img { position: absolute; left: 0; top: 0; width: 900px; height: 470px; object-fit: cover; object-position: 0 0; }
    .src-c .ft { position: absolute; left: 0; right: 0; bottom: 0; height: 130px; background: #0b2f29; display: flex; align-items: center; gap: 22px; padding: 0 36px; direction: ltr; }
    .src-c b { font-family: var(--font-en); font-size: 54px; font-weight: 900; color: #fff; }
    .src-c i { font-style: normal; font-family: var(--font-en); font-size: 20px; font-weight: 800; letter-spacing: .16em; color: var(--lime); }
    #src-a { top: 440px; } #src-b { top: 1100px; }
""", """
      <div id="src-lab" class="row"><span class="t-label" style="color:var(--yellow)">GREAT SOURCES</span></div>
      <div id="src-h" class="row t-h3"><span class="mask"><span class="in" id="src-h1">مصادر رائعة تساعدك</span></span></div>
      <div class="src-c" id="src-a"><img src="assets/images/aa/scatter.png" alt="" /><div class="ft"><b>Artificial Analysis</b><i>BENCHMARKS</i></div></div>
      <div class="src-c" id="src-b"><img src="assets/images/arena/hero.png" alt="" /><div class="ft"><b>Arena AI</b><i>HARNESSTAX STUDY</i></div></div>
""", """
      fx.rise("#src-lab", 149.05, { y: 16 });
      tl.fromTo("#src-a", { opacity: 0, x: 800 }, { opacity: 1, x: 0, duration: 0.5, ease: "expo.out" }, 149.05);
      fx.maskUp("#src-h1", 150.2);
      tl.fromTo("#src-b", { opacity: 0, x: 800 }, { opacity: 1, x: 0, duration: 0.5, ease: "expo.out" }, 152.35);
""", blob=("#136052", 540, 1000), exit_t=153.55)

# ---------------------------------------------------------------- z1 canvas: Zadloop bonus (presenter card on top)
make("z1", """
    #z1-bn { left: 0; right: 0; top: 930px; text-align: center; }
    #z1-top { left: 140px; top: 1020px; width: 800px; height: 190px; border-radius: 34px; background: linear-gradient(135deg, #1a7564, #136052); border: 4px solid var(--lime);
      display: flex; align-items: center; justify-content: center; box-shadow: 0 30px 60px rgba(0,0,0,.4); }
    #z1-top b { font-family: var(--font-en); font-weight: 900; font-size: 96px; direction: ltr; }
    #z1-base { left: 100px; top: 1250px; width: 880px; height: 120px; border-radius: 28px; background: rgba(255,255,255,.06); border: 3px dashed rgba(246,248,240,.5);
      display: flex; align-items: center; justify-content: center; gap: 16px; direction: ltr; }
    #z1-base b { font-family: var(--font-en); font-weight: 900; font-size: 46px; color: var(--fg-muted); }
    #z1-ar { left: 850px; top: 960px; width: 130px; height: 130px; border-radius: 50%; background: var(--yellow); color: var(--ink); font-size: 80px; font-weight: 900; display: flex; align-items: center; justify-content: center; }
    .z1-p { position: absolute; left: 0; right: 0; text-align: center; }
    .z1-p .pill { font-size: 40px; height: 88px; padding: 0 36px; border-radius: 44px; }
    .z1-p .ic { width: 54px; height: 54px; border-radius: 50%; background: var(--lime); color: var(--ink); display: inline-flex; align-items: center; justify-content: center; }
    #z1-p1 { top: 1420px; } #z1-p2 { top: 1530px; } #z1-p3 { top: 1640px; }
""", """
      <div id="z1-bn" class="abs"><span class="pill bad" style="font-family:var(--font-en); letter-spacing:.14em; font-size:28px; height:60px">BONUS</span></div>
      <div id="z1-top" class="abs"><b>Zadloop</b></div>
      <div id="z1-base" class="abs"><b>DeepSeek</b><b style="color:var(--lime)">Harness</b></div>
      <div id="z1-ar" class="abs">ع</div>
      <div class="z1-p" id="z1-p1"><span class="pill">معمول باللغة العربية</span></div>
      <div class="z1-p" id="z1-p2"><span class="pill"><span class="ic"><svg width="30" height="36"><use href="#i-person" /></svg></span>وراه مبرمج عربي</span></div>
      <div class="z1-p" id="z1-p3"><span class="pill"><span class="ic"><svg width="32" height="32"><use href="#i-mic" /></svg></span>بودكاست أخبار الذكاء الاصطناعي</span></div>
""", """
      fx.pop("#z1-bn", 154.0, { from: 0.3 });
      tl.fromTo("#z1-top", { opacity: 0, scale: 1.6, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out" }, 155.3);
      tl.fromTo("#z1-base", { opacity: 0, y: 140 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 156.95);
      fx.pop("#z1-ar", 158.7, { from: 0, e: "back.out(2.6)" });
      fx.pop("#z1-p1", 158.9, { from: 0.5 });
      fx.pop("#z1-p2", 160.4, { from: 0.5 });
      fx.pop("#z1-p3", 162.5, { from: 0.5 });
""", blob=("#136052", 540, 1300), push=None, exit_t=164.0)

print("built talking-head scenes")
