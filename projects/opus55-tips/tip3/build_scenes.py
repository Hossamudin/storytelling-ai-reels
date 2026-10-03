# Part 3 — "Learn from others" (9:16, dark). Times = GLOBAL seconds on assets/voice/tip3.wav.
# Signature (part 3): the clay road. From zero = the long winding path; learning from others = the lime shortcut.
# Payoff: the marker jumps along the shortcut to 95% on "٩٥٪ من المشوار".
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from build_lib import Part, patch_root, spark, ic, label, head, claude_input, chip, hossam  # noqa: E402

P = Part(HERE)
patch_root(HERE, flashes=(60.88, 78.1))
make = P.make
ROAD = "assets/images/road.png"
# road.png shown at 700 px wide (x0.931) from (190, 470): start disc ~(533, 1596), flag ~(694, 539)

CARDCSS = """
    .op-n { position: absolute; left: 0; right: 0; text-align: center; white-space: nowrap; }
    .op-lk { position: absolute; left: 50%; top: 50%; width: 80px; height: 80px; margin: -40px 0 0 -40px; color: rgba(179,206,101,.55); }
    .op-done { position: absolute; right: 18px; top: 18px; width: 56px; height: 56px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
"""
DONE = f'<div class="op-done">{ic("check", 36)}</div>'


def card_n(id_, x, y, w, h, top_label, num, sub="", sp=None, extra=""):
    spk = spark(f"{id_}-sp", (w - sp) // 2, 36, sp, bloom=False) if sp else ""
    return (f'<div id="{id_}" class="op-card" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px">{spk}'
            f'<div class="op-n op-en" data-layout-allow-overlap style="top:{int(h * .33)}px; font-size:{int(w * .1)}px; letter-spacing:.3em; color:var(--lime)">{top_label}</div>'
            f'<div class="op-n op-en op-y" data-layout-allow-overlap style="top:{int(h * .42)}px; font-size:{int(w * .5)}px; line-height:1">{num}</div>'
            f'<div class="op-n op-en" data-layout-allow-overlap style="top:{int(h * .84)}px; font-size:{int(w * .075)}px; color:var(--fg-muted)">{sub}</div>{extra}</div>')


# ---------------------------------------------------------------- s1 hook
make("s1", """
    #s1-tt { position: absolute; left: 0; right: 0; top: 1060px; text-align: center; font-size: 190px; color: #e8977c; white-space: nowrap; direction: ltr; }
""", f"""
      {spark("s1-sp", 370, 470, 340)}
      <div id="s1-tt" class="op-en"><span id="s1-tt1">Opus 5.5</span></div>
      <div class="row t-h1 op-l" style="top:1330px"><span class="mask"><span class="in" id="s1-k1">رائع جدًا</span></span></div>
""", """
      fx.punch("#s1-cam", 0, 1.2);
      fx.pop("#s1-sp", 0.0, { from: 0.2, e: "expo.out", d: 0.9 });
      tl.fromTo("#s1-sp-svg", { rotation: -90 }, { rotation: 60, duration: 3.0, ease: "power2.out" }, 0);
      fx.breathe("#s1-sp-bl", 0.6, 2.4, 0.1, 1.2);
      fx.letterDrop("#s1-tt1", 0.4, { st: 0.04 });
      fx.maskUp("#s1-k1", 1.45);
""", blob=("#136052", 540, 640))

# ---------------------------------------------------------------- s2 videos, pro files, almost anything
make("s2", """
    .s2-t { position: absolute; top: 560px; width: 280px; text-align: center; }
    .s2-c { width: 220px; height: 220px; border-radius: 50%; margin: 0 auto 16px; display: flex; align-items: center; justify-content: center; color: var(--ink); }
    #s2-a { left: 730px; } #s2-b { left: 400px; } #s2-c { left: 70px; }
    .s2-mini { position: absolute; width: 96px; height: 96px; border-radius: 26px; background: rgba(255,255,255,.06); border: 2px solid var(--edge); display: flex; align-items: center; justify-content: center; color: var(--lime); }
""", f"""
      <div class="row t-h2" style="top:280px"><span class="mask"><span class="in" id="s2-h1">تقدر تعمل بيه</span></span></div>
      <div id="s2-a" class="s2-t"><div class="s2-c" style="background:var(--lime)">{ic("film", 110)}</div><div class="t-h3">فيديوهات</div></div>
      <div id="s2-b" class="s2-t"><div class="s2-c" style="background:var(--yellow)">{ic("plan", 110)}</div><div class="t-h3">ملفات احترافية</div></div>
      <div id="s2-c" class="s2-t"><div class="s2-c" style="background:#e8977c">{ic("wand", 110)}</div><div class="t-h3">أي حاجة</div></div>
      {"".join(f'<div class="s2-mini s2-m" style="left:{70 + (i % 7) * 140}px; top:{1100 + (i // 7) * 140}px">{ic(["film", "plan", "sound", "book", "bulb", "chat", "wand"][(i * 3) % 7], 50)}</div>' for i in range(21))}
      <div class="row t-h3 muted" style="top:1540px"><span class="mask"><span class="in" id="s2-k1">تقريبًا أي حاجة بتفكر فيها</span></span></div>
""", """
      fx.maskUp("#s2-h1", 2.9);
      fx.pop("#s2-a", 3.7, { from: 0.3 }); fx.pop("#s2-b", 4.15, { from: 0.3 }); fx.pop("#s2-c", 6.45, { from: 0.3 });
      tl.fromTo(".s2-m", { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.03 }, 6.7);
      fx.maskUp("#s2-k1", 6.9);
""", blob=("#0f4f44", 540, 800))

# ---------------------------------------------------------------- s3 best results: this tip
make("s3", """
    #s3-hl { position: absolute; left: 0; right: 0; top: 900px; text-align: center; }
""", f"""
      <div class="row t-h2" style="top:600px"><span class="mask"><span class="in" id="s3-h1">بس عشان تطلّع منه</span></span></div>
      <div id="s3-hl" class="t-h1"><span class="hl" id="s3-hw"><span class="band" id="s3-band"></span><span class="txt">أحسن نتائج</span></span></div>
      <div class="row t-h2 op-l" style="top:1160px"><span class="mask"><span class="in" id="s3-k1">تعالى أقولك التيب دي</span></span></div>
""", """
      fx.maskUp("#s3-h1", 8.0);
      fx.pop("#s3-hw", 9.15, { from: 0.6 }); fx.band("#s3-band", 9.2);
      fx.maskUp("#s3-k1", 10.0);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s4 series: part 3
make("s4", CARDCSS + """
    #s4-c3b, #s4-c3 { left: 370px; top: 470px; width: 340px; height: 500px; }
    .s4-sp { position: absolute; height: 8px; border-radius: 4px; background: var(--lime); }
""", f"""
      {label("s4-lab", 280, "VIDEO 3 OF 3")}
      {card_n("s4-c1", 80, 520, 260, 400, "TIP", "01", "", extra=DONE)}
      {card_n("s4-c2", 740, 520, 260, 400, "TIP", "02", "", extra=DONE)}
      <div id="s4-c3b" class="op-card back"><svg class="op-lk"><use href="#i-lock" /></svg></div>
      {card_n("s4-c3", 370, 470, 340, 500, "PART", "03", "TODAY", sp=100)}
      <div class="row t-h3" style="top:1070px"><span class="mask"><span class="in" id="s4-k1">ازاي تستخدم <span class="lat">Opus 5.5</span></span></span></div>
      <div class="row t-h2" style="top:1180px"><span class="mask"><span class="in" id="s4-k2">وتطلّع أحسن نتايج</span></span></div>
      <div class="row t-h1 op-y" style="top:1330px"><span class="mask"><span class="in" id="s4-k3">بسرعة</span></span></div>
      {"".join(f'<i class="s4-sp" id="s4-s{i}" style="left:{80 + i * 40}px; top:{1400 + i * 50}px; width:{240 - i * 50}px"></i>' for i in range(3))}
""", """
      fx.rise("#s4-lab", 11.2, { y: 12 });
      fx.rise("#s4-c1", 11.1, { y: 80 }); fx.rise("#s4-c2", 11.2, { y: 80 }); fx.rise("#s4-c3b", 11.3, { y: 120 });
      fx.hide("#s4-c3");
      tl.to("#s4-c3b", { scaleX: 0, duration: 0.16, ease: "power2.in" }, 12.35);
      tl.fromTo("#s4-c3", { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.22, ease: "power2.out", immediateRender: false }, 12.51);
      tl.fromTo("#s4-c3-sp-svg", { rotation: 0 }, { rotation: 300, duration: 5.8, ease: "none" }, 12.51);
      fx.maskUp("#s4-k1", 13.7); fx.maskUp("#s4-k2", 16.3);
      fx.maskUp("#s4-k3", 17.6);
      tl.fromTo(".s4-sp", { opacity: 0, x: 300, scaleX: 0.2 }, { opacity: 1, x: 0, scaleX: 1, duration: 0.3, ease: "power3.out", stagger: 0.05 }, 17.6);
      tl.to(".s4-sp", { opacity: 0, x: -200, duration: 0.3 }, 18.0);
""", blob=("#136052", 540, 760))

# ---------------------------------------------------------------- s5 saves tokens + time
make("s5", """
    #s5-st { left: 300px; top: 560px; color: var(--yellow); border-color: var(--yellow); font-size: 96px; }
    .s5-b { position: absolute; top: 880px; width: 400px; height: 400px; border-radius: 40px; text-align: center; }
    #s5-a { left: 580px; } #s5-b { left: 100px; }
    .s5-b .i { margin: 60px auto 20px; width: 170px; height: 170px; }
""", f"""
      <div class="row t-h3" style="top:280px"><span class="mask"><span class="in" id="s5-h1">والتيب اللي معانا النهارده</span></span></div>
      <div id="s5-st" class="stamp">مهمة جدًا</div>
      <div class="row t-h3 muted" style="top:790px"><span class="mask"><span class="in" id="s5-k1">لأنها هتوفّر عليك</span></span></div>
      <div id="s5-a" class="op-card s5-b"><div class="i" style="color:var(--lime)">{ic("token", 170)}</div><div class="t-h3 lat">tokens</div></div>
      <div id="s5-b" class="op-card s5-b" style="border-color:var(--yellow)"><div class="i" style="color:var(--yellow)">{ic("clock", 170)}</div><div class="t-h3">ووقت</div></div>
      <div class="row t-h3" style="top:1360px"><span class="mask"><span class="in" id="s5-k2">مع الـــ<span class="lat">AI</span></span></span></div>
""", """
      fx.maskUp("#s5-h1", 18.6);
      fx.stamp("#s5-st", 20.0, "#s5-cam");
      fx.maskUp("#s5-k1", 21.1);
      fx.pop("#s5-a", 22.45, { from: 0.4 }); fx.pop("#s5-b", 23.2, { from: 0.4 });
      fx.maskUp("#s5-k2", 23.7);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s6 videos like this one
make("s6", """
    #s6-ph { left: 330px; top: 520px; width: 420px; height: 800px; }
    #s6-v { position: absolute; left: -1461px; top: -171px; width: 3376px; height: 1595px; }
""", f"""
      <div class="row t-h3" style="top:260px"><span class="mask"><span class="in" id="s6-h1">تعالى نفترض إنك عايز الـــ<span class="lat">AI</span></span></span></div>
      <div class="row t-h2" style="top:360px"><span class="mask"><span class="in" id="s6-h2">يعملك فيديوهات زي دي</span></span></div>
      <div id="s6-ph" class="op-phone"><div class="scr"><video id="s6-v" src="assets/videos/hf_studio.mp4" data-start="0" data-duration="3.55" data-media-start="4.5" muted playsinline></video></div></div>
""", """
      fx.maskUp("#s6-h1", 24.75); fx.maskUp("#s6-h2", 26.3);
      tl.fromTo("#s6-ph", { opacity: 0, y: 220, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.55, ease: "back.out(1.4)" }, 26.5);
""", blob=("#0f4f44", 540, 900))

# ---------------------------------------------------------------- s7 the road: from zero vs the shortcut (SIGNATURE intro)
make("s7", """
    #s7-road { left: 190px; top: 470px; width: 700px; height: 1251px; border-radius: 30px; }
    #s7-z { left: 470px; top: 1530px; width: 130px; height: 130px; border-radius: 50%; background: var(--orange); color: #fff; display: flex; align-items: center; justify-content: center;
      font-family: var(--font-ar); font-weight: 900; font-size: 70px; box-shadow: 0 0 40px rgba(255,90,51,.6); }
    #s7-hl { left: 0; top: 0; width: 1080px; height: 1920px; filter: drop-shadow(0 0 18px rgba(179,206,101,.9)); }
    #s7-tag { left: 60px; top: 1060px; }
""", f"""
      <div class="row t-h2" data-layout-allow-overlap style="top:280px"><span class="mask" data-layout-allow-overlap><span class="in" data-layout-allow-overlap id="s7-h1">بدل ما تبدأ من الصفر</span></span></div>
      <div class="row t-h2 op-l" data-layout-allow-overlap style="top:280px"><span class="mask" data-layout-allow-overlap><span class="in" data-layout-allow-overlap id="s7-h2">اتعلّم من غيرك</span></span></div>
      <img id="s7-road" class="abs" src="{ROAD}" />
      <div id="s7-z" class="abs op-en">0</div>
      <svg id="s7-hl" class="abs" viewBox="0 0 1080 1920"><path id="s7-hp" d="M309 1167L640 545" pathLength="1" stroke="#e9ff9a" stroke-width="16" stroke-linecap="round" fill="none" /></svg>
      {chip("s7-tag", 60, 1060, "SHORTCUT", ic("flag", 32))}
""", """
      fx.maskUp("#s7-h1", 28.15);
      tl.fromTo("#s7-road", { opacity: 0, y: 200, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power3.out" }, 28.05);
      fx.pop("#s7-z", 29.35, { from: 0.2 });
      tl.to("#s7-h1", { yPercent: -115, duration: 0.25, ease: "power2.in" }, 31.6);
      fx.maskUp("#s7-h2", 31.85);
      fx.draw("#s7-hp", 31.85, 0.5, "power2.out");
      fx.pop("#s7-tag", 32.0, { from: 0.4 });
""", blob=("#136052", 540, 1000), push=1.02)

# ---------------------------------------------------------------- s8 same AI + same purpose
make("s8", """
    #s8-a { left: 590px; top: 560px; width: 400px; height: 360px; } #s8-b { left: 90px; top: 560px; width: 400px; height: 360px; }
    .s8-in { position: absolute; left: 0; right: 0; top: 230px; text-align: center; }
    #s8-plus { left: 500px; top: 660px; font-family: var(--font-en); font-weight: 900; font-size: 90px; color: var(--fg-muted); }
    #s8-eq { left: 340px; top: 1000px; width: 400px; height: 120px; border-radius: 60px; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; gap: 16px;
      font-family: var(--font-ar); font-weight: 900; font-size: 46px; }
    #s8-k { top: 1220px; }
""", f"""
      <div class="row t-h3" style="top:280px"><span class="mask"><span class="in" id="s8-h1">حد استخدم</span></span></div>
      <div id="s8-a" class="op-card">{spark("s8-sp", 140, 50, 120, bloom=False)}<div class="s8-in t-h3">نفس الـــ<span class="lat">AI</span></div></div>
      <div id="s8-plus" class="abs">+</div>
      <div id="s8-b" class="op-card" style="border-color:var(--yellow)"><div style="position:absolute; left:140px; top:50px; color:var(--yellow)">{ic("target", 120)}</div><div class="s8-in t-h3">نفس الغرض</div></div>
      <div id="s8-eq" class="abs">{ic("check", 50)} MATCH</div>
      <div id="s8-k" class="row t-h3"><span class="mask"><span class="in" id="s8-k1">عايز فيديوهات بـــ<span class="lat">Claude Opus 5.5</span>؟</span></span></div>
""", """
      fx.maskUp("#s8-h1", 33.2);
      fx.pop("#s8-a", 34.2, { from: 0.4 }); fx.pop("#s8-plus", 34.8); fx.pop("#s8-b", 35.1, { from: 0.4 });
      fx.pop("#s8-eq", 35.6, { from: 0.3 });
      fx.maskUp("#s8-k1", 36.9);
""", blob=("#136052", 540, 840))

# ---------------------------------------------------------------- s9 someone made videos with Claude Opus, good results
make("s9", """
    #s9-pr { left: 110px; top: 470px; width: 860px; height: 220px; }
    #s9-av { position: absolute; right: 40px; top: 40px; width: 140px; height: 140px; border-radius: 50%; background: #0f4f44; border: 4px solid var(--lime); color: var(--lime); display: flex; align-items: center; justify-content: center; }
    #s9-nm { position: absolute; right: 210px; top: 36px; }
    #s9-sub { position: absolute; right: 210px; top: 150px; font-family: var(--font-en); font-weight: 800; font-size: 24px; letter-spacing: .14em; color: var(--fg-muted); direction: ltr; }
    .s9-v { position: absolute; top: 760px; width: 260px; height: 460px; border-radius: 26px; background: linear-gradient(170deg, #0f3d35, #04201b); border: 2px solid var(--edge); overflow: hidden; }
    #s9-v1 { left: 720px; } #s9-v2 { left: 410px; } #s9-v3 { left: 100px; }
    .s9-ok { position: absolute; left: 50%; bottom: 26px; width: 66px; height: 66px; margin-left: -33px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
    .s9-pl { position: absolute; left: 50%; top: 150px; width: 90px; height: 90px; margin-left: -45px; color: rgba(255,255,255,.75); }
""", f"""
      <div id="s9-pr" class="op-card"><div id="s9-av">{ic("person", 80)}</div><div id="s9-nm" class="t-h3">حد عمل فيديوهات</div><div id="s9-sub">MADE WITH CLAUDE OPUS</div></div>
      {"".join(f'<div class="s9-v" id="s9-v{i}">{spark(f"s9-s{i}", 90, 40, 80, bloom=False)}<svg class="s9-pl"><use href="#i-play" /></svg><div class="s9-ok" id="s9-ok{i}">{ic("check", 40)}</div></div>' for i in (1, 2, 3))}
      <div class="row t-h1 op-l" style="top:1300px"><span class="mask"><span class="in" id="s9-k1">ونتايجه كويسة</span></span></div>
""", """
      tl.fromTo("#s9-pr", { opacity: 0, y: 100 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 38.5);
      fx.pop("#s9-av", 39.35, { from: 0.3 });
      fx.pop("#s9-v1", 40.25, { from: 0.4 }); fx.pop("#s9-v2", 40.55, { from: 0.4 }); fx.pop("#s9-v3", 40.85, { from: 0.4 });
      fx.pop("#s9-ok1, #s9-ok2, #s9-ok3", 42.9, { from: 0, st: 0.1 });
      fx.maskUp("#s9-k1", 42.7);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s10 learn from their prompt; free = great
make("s10", """
    #s10-doc { left: 190px; top: 470px; width: 700px; height: 860px; }
    #s10-dt { position: absolute; left: 44px; top: 34px; font-family: var(--font-en); font-weight: 900; font-size: 30px; letter-spacing: .2em; color: #6b6a62; direction: ltr; }
    #s10-fr { left: 330px; top: 1180px; color: var(--lime); border-color: var(--lime); font-family: var(--font-en); font-size: 100px; background: rgba(4,22,20,.92); }
""", f"""
      <div class="row t-h2" style="top:280px; font-size:76px; white-space:nowrap"><span class="mask"><span class="in" id="s10-h1">اتعلّم من الـــ<span class="lat">prompt</span> بتاعه</span></span></div>
      <div id="s10-doc" class="op-doc"><div id="s10-dt">THEIR PROMPT</div>
        {"".join(f'<i class="ln s10-ln" style="top:{110 + i * 46}px; width:{[600, 540, 610, 480, 590, 560, 400, 610, 520, 580, 450, 600, 530, 570, 490][i]}px"></i>' for i in range(15))}</div>
      <div id="s10-fr" class="stamp">FREE</div>
      <div class="row t-h1 op-y" style="top:1420px"><span class="mask"><span class="in" id="s10-k1">ممتاز</span></span></div>
""", """
      fx.maskUp("#s10-h1", 43.55);
      tl.fromTo("#s10-doc", { opacity: 0, y: 200, rotation: -4 }, { opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "power3.out" }, 44.7);
      tl.fromTo(".s10-ln", { scaleX: 0, transformOrigin: "100% 50%" }, { scaleX: 1, duration: 0.25, stagger: 0.05 }, 44.9);
      fx.stamp("#s10-fr", 47.15, "#s10-cam");
      fx.maskUp("#s10-k1", 47.25);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s11 take parts, edit them; saves time + effort
make("s11", """
    #s11-doc { left: 190px; top: 470px; width: 700px; height: 760px; }
    .s11-sel { position: absolute; right: 30px; width: 640px; height: 40px; border-radius: 10px; background: rgba(179,206,101,.55); transform-origin: 100% 50%; }
    #s11-cp { left: 90px; top: 600px; width: 110px; height: 110px; border-radius: 50%; background: var(--lime); color: var(--ink); display: flex; align-items: center; justify-content: center; }
    #s11-c1 { left: 560px; top: 1300px; } #s11-c2 { left: 150px; top: 1300px; }
""", f"""
      <div class="row t-h2" style="top:280px"><span class="mask"><span class="in" id="s11-h1">خد بعض الأجزاء وعدّل</span></span></div>
      <div id="s11-doc" class="op-doc">
        <div class="s11-sel" id="s11-s1" style="top:140px"></div><div class="s11-sel" id="s11-s2" style="top:186px"></div><div class="s11-sel" id="s11-s3" style="top:416px"></div>
        {"".join(f'<i class="ln s11-ln{" s11-ed" if i in (1, 2, 7) else ""}" style="top:{150 + i * 46}px; width:{[600, 540, 610, 480, 590, 560, 400, 610, 520, 580, 450, 600][i]}px"></i>' for i in range(12))}</div>
      <div id="s11-cp" class="abs">{ic("copy", 60)}</div>
      {chip("s11-c1", 560, 1300, "وقت أقل", ic("clock", 32))}
      {chip("s11-c2", 150, 1300, "مجهود أقل", "−", "y")}
""", """
      fx.maskUp("#s11-h1", 47.95);
      tl.fromTo("#s11-doc", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 47.85);
      tl.fromTo("#s11-s1, #s11-s2, #s11-s3", { scaleX: 0 }, { scaleX: 1, duration: 0.25, stagger: 0.12, ease: "power2.out" }, 48.65);
      fx.pop("#s11-cp", 48.75);
      tl.to(".s11-ed", { background: "#136052", duration: 0.25, stagger: 0.25 }, 49.3);
      tl.to("#s11-s1, #s11-s2, #s11-s3", { opacity: 0, duration: 0.3 }, 49.9);
      fx.pop("#s11-c1", 50.95); fx.pop("#s11-c2", 51.2);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s12 sometimes not the prompt: the libraries
make("s12", """
    #s12-doc { left: 340px; top: 480px; width: 400px; height: 440px; }
    #s12-x { left: 470px; top: 610px; }
    .s12-bk { position: absolute; left: 290px; width: 500px; height: 90px; border-radius: 18px; display: flex; align-items: center; justify-content: center; gap: 20px;
      font-family: var(--font-en); font-weight: 900; font-size: 38px; color: var(--ink); direction: ltr; }
    #s12-b1 { top: 1320px; background: var(--lime); } #s12-b2 { top: 1215px; background: var(--yellow); left: 320px; width: 440px; } #s12-b3 { top: 1110px; background: #e8977c; left: 350px; width: 380px; }
""", f"""
      <div class="row t-h3" style="top:280px"><span class="mask"><span class="in" id="s12-h1">ساعات الـــ<span class="lat">prompt</span> نفسه</span></span></div>
      <div class="row t-h2 op-o" style="top:370px"><span class="mask"><span class="in" id="s12-h2">مش هو المهم</span></span></div>
      <div id="s12-doc" class="op-doc">{"".join(f'<i class="ln" style="top:{60 + i * 44}px; width:{[300, 260, 310, 240, 290, 270, 220, 300][i]}px"></i>' for i in range(8))}</div>
      <div id="s12-x" class="xbadge" style="width:140px; height:140px; color:#fff">{ic("x", 90)}</div>
      <div class="s12-bk" id="s12-b3">&lt;/&gt; LIBRARY</div><div class="s12-bk" id="s12-b2">&lt;/&gt; LIBRARY</div><div class="s12-bk" id="s12-b1">&lt;/&gt; LIBRARY</div>
      <div class="row t-h2 op-l" style="top:1480px"><span class="mask"><span class="in" id="s12-k1">المكتبات البرمجية</span></span></div>
""", """
      fx.maskUp("#s12-h1", 52.45); fx.maskUp("#s12-h2", 54.55);
      tl.fromTo("#s12-doc", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 53.5);
      fx.pop("#s12-x", 54.6, { from: 0.2 });
      tl.to("#s12-doc", { scale: 0.8, opacity: 0.35, filter: "grayscale(1)", duration: 0.5 }, 55.2);
      tl.fromTo("#s12-b1", { opacity: 0, y: -400 }, { opacity: 1, y: 0, duration: 0.4, ease: "bounce.out" }, 57.25);
      tl.fromTo("#s12-b2", { opacity: 0, y: -400 }, { opacity: 1, y: 0, duration: 0.4, ease: "bounce.out" }, 57.55);
      tl.fromTo("#s12-b3", { opacity: 0, y: -400 }, { opacity: 1, y: 0, duration: 0.4, ease: "bounce.out" }, 57.85);
      fx.maskUp("#s12-k1", 57.3);
""", blob=("#136052", 540, 1000), exit_t=57.95)

# ---------------------------------------------------------------- s13 libraries matter most; two famous ones
make("s13", """
    #s13-big { position: absolute; left: 0; right: 0; top: 760px; text-align: center; font-family: var(--font-ar); font-weight: 900; font-size: 230px; line-height: 1.3; color: var(--lime); text-shadow: 0 0 80px rgba(179,206,101,.5); }
    .s13-sl { position: absolute; top: 1240px; width: 380px; height: 220px; border-radius: 30px; border: 4px dashed rgba(179,206,101,.5); display: flex; align-items: center; justify-content: center;
      font-family: var(--font-en); font-weight: 900; font-size: 110px; color: rgba(179,206,101,.6); }
    #s13-s1 { left: 580px; } #s13-s2 { left: 120px; }
""", f"""
      <div class="row t-h2" style="top:300px; font-size:64px; white-space:nowrap"><span class="mask"><span class="in" id="s13-h1">اللي <span class="lat">Claude</span> ممكن يستخدمها</span></span></div>
      <div class="row t-h3 muted" style="top:470px"><span class="mask"><span class="in" id="s13-h2">بتكون هي</span></span></div>
      <div id="s13-big"><span id="s13-b1" style="display:inline-block">الأهم</span></div>
      <div class="row t-h3" style="top:1120px"><span class="mask"><span class="in" id="s13-k1">في صناعة الفيديوهات: مكتبتين</span></span></div>
      <div id="s13-s1" class="s13-sl">1</div><div id="s13-s2" class="s13-sl">2</div>
""", """
      fx.maskUp("#s13-h1", 58.05); fx.maskUp("#s13-h2", 60.25);
      tl.fromTo("#s13-b1", { opacity: 0, scale: 2.6, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }, 60.85);
      fx.shake("#s13-cam", 60.95, 16, 7);
      tl.to("#s13-b1", { scale: 0.7, y: -120, duration: 0.5, ease: "power2.inOut" }, 62.0);
      fx.maskUp("#s13-k1", 62.2);
      fx.pop("#s13-s1", 63.55, { from: 0.4 }); fx.pop("#s13-s2", 63.95, { from: 0.4 });
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s14 Remotion vs HyperFrames (real sites) — my pick
make("s14", """
    #s14-r { left: 560px; top: 520px; width: 440px; height: 622px; }
    #s14-h { left: 80px; top: 520px; width: 440px; height: 450px; }
    .s14-n { position: absolute; top: 1170px; width: 440px; text-align: center; font-family: var(--font-en); font-weight: 900; font-size: 50px; direction: ltr; }
    #s14-rn { left: 560px; } #s14-hn { left: 80px; top: 1000px; color: var(--lime); }
    #s14-pk { left: 110px; top: 1090px; color: var(--lime); border-color: var(--lime); font-family: var(--font-en); font-size: 58px; background: rgba(4,22,20,.92); }
    #s14-src { top: 1500px; }
""", f"""
      <div class="row t-h3" style="top:300px"><span class="mask"><span class="in" id="s14-h1">مكتبتين مشهورتين</span></span></div>
      <div id="s14-r" class="op-shot"><img src="assets/images/rem_card.png" style="width:440px" /></div>
      <div id="s14-rn" class="s14-n">Remotion</div>
      <div id="s14-h" class="op-shot"><img src="assets/images/hf_card.png" style="width:440px" /></div>
      <div id="s14-hn" class="s14-n">HyperFrames</div>
      <div id="s14-pk" class="stamp">MY PICK ✓</div>
      <div class="row t-h2 op-l" style="top:1330px"><span class="mask"><span class="in" id="s14-k1">ودي اللي بعتمد عليها</span></span></div>
      <div id="s14-src" class="op-src">REAL SITES · REMOTION.DEV · HYPERFRAMES.HEYGEN.COM</div>
""", """
      fx.maskUp("#s14-h1", 64.75);
      tl.fromTo("#s14-r", { opacity: 0, y: 160, rotation: 4 }, { opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "power3.out" }, 65.4);
      fx.rise("#s14-rn", 65.6, { y: 20 });
      tl.fromTo("#s14-h", { opacity: 0, y: 160, rotation: -4 }, { opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "power3.out" }, 67.2);
      fx.rise("#s14-hn", 67.4, { y: 20 });
      tl.to("#s14-r, #s14-rn", { opacity: 0.35, scale: 0.92, filter: "grayscale(.8)", duration: 0.5 }, 68.0);
      tl.to("#s14-h", { scale: 1.06, boxShadow: "0 0 0 6px #b3ce65, 0 30px 80px rgba(0,0,0,.55)", duration: 0.45, ease: "back.out(1.6)" }, 68.0);
      fx.maskUp("#s14-k1", 68.7);
      fx.stamp("#s14-pk", 69.3);
      fx.rise("#s14-src", 65.8, { y: 8, b: 0 });
""", blob=("#136052", 540, 900), push=1.02)

# ---------------------------------------------------------------- s15 tell Claude Opus to load + use it
make("s15", """
    #s15-term { left: 70px; top: 1000px; width: 940px; height: 120px; border-radius: 22px; background: #050a09; border: 2px solid rgba(179,206,101,.45);
      font-family: "Courier New", monospace; font-weight: 700; font-size: 32px; color: var(--lime); direction: ltr; display: flex; align-items: center; padding: 0 30px; white-space: nowrap; overflow: hidden; }
    #s15-ok { left: 480px; top: 1180px; width: 120px; height: 120px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
    #s15-src { top: 1150px; }
""", f"""
      <div class="row t-h3" style="top:260px"><span class="mask"><span class="in" id="s15-h1">مجرد إنك تعرف الـــ<span class="lat">library</span></span></span></div>
      <div class="row t-h3 muted" style="top:350px"><span class="mask"><span class="in" id="s15-h2">وتقول لـــ<span class="lat">Claude Opus 5.5</span></span></span></div>
      {claude_input("s15-in", 70, 560, 940, 250)}
      <div id="s15-term" class="abs"><span>$&nbsp;</span><span id="s15-tt"></span></div>
      <div id="s15-ok" class="abs">{ic("check", 70)}</div>
      <div id="s15-src" class="op-src">REAL INSTALL COMMAND · HYPERFRAMES.HEYGEN.COM</div>
      <div class="row t-h2 op-l" style="top:1360px"><span class="mask"><span class="in" id="s15-k1">يحمّلها ويستخدمها</span></span></div>
""", """
      fx.maskUp("#s15-h1", 70.6); fx.maskUp("#s15-h2", 73.0);
      tl.fromTo("#s15-in", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 70.5);
      fx.typeText("#s15-in-t", 73.55, "حمّل HyperFrames واستخدمها", 20);
      tl.fromTo("#s15-term", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 75.3);
      fx.typeText("#s15-tt", 75.45, "npx skills add heygen-com/hyperframes", 50);
      fx.maskUp("#s15-k1", 75.5);
      fx.pop("#s15-ok", 76.2, { from: 0 });
      fx.rise("#s15-src", 75.6, { y: 8, b: 0 });
""", blob=("#136052", 540, 800))

# ---------------------------------------------------------------- s16 PAYOFF: 95% of the journey
make("s16", """
    #s16-road { left: 220px; top: 470px; width: 640px; height: 1144px; border-radius: 30px; }
    #s16-mk { left: 494px; top: 1459px; width: 80px; height: 80px; border-radius: 50%; background: var(--yellow); box-shadow: 0 0 0 10px rgba(255,236,92,.3), 0 0 50px rgba(255,236,92,.8); }
    #s16-card { left: 70px; top: 230px; width: 940px; height: 210px; }
    #s16-num { position: absolute; right: 40px; top: 10px; font-family: var(--font-ar); font-weight: 900; font-size: 150px; line-height: 1.3; color: var(--yellow); }
    #s16-t { position: absolute; left: 40px; top: 60px; text-align: left; }
""", f"""
      <img id="s16-road" class="abs" src="{ROAD}" />
      <div id="s16-mk" class="abs"><div class="ring" id="s16-r1" style="border-radius:50%; border-color:var(--yellow)"></div></div>
      <div id="s16-card" class="op-card"><div id="s16-num" class="num">٩٥٪</div><div id="s16-t" class="t-h3">من المشوار</div></div>
      <div class="row t-h3" style="top:1650px; font-size:44px"><span class="mask"><span class="in" id="s16-k1">اتعلّم من تجارب غيرك مع نفس الموديل</span></span></div>
""", """
      tl.fromTo("#s16-road", { opacity: 0, scale: 1.1 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 76.85);
      fx.pop("#s16-mk", 77.0, { from: 0.2 });
      tl.fromTo("#s16-card", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.6)" }, 77.1);
      fx.counter("#s16-num", 77.2, 78.0, 0, 95, { suffix: "٪" });
      tl.to("#s16-mk", { x: -205, y: -392, duration: 0.3, ease: "power2.in" }, 77.25);
      tl.to("#s16-mk", { x: 82, y: -932, duration: 0.5, ease: "power3.out" }, 77.55);
      fx.ringPulse("#s16-r1", 78.1, { scale: 2.6 });
      fx.shake("#s16-cam", 78.12, 14, 6);
      fx.rise("#s16-t", 78.3, { y: 16 });
      fx.maskUp("#s16-k1", 79.8);
""", blob=("#136052", 540, 1000), push=1.02)

# ---------------------------------------------------------------- s17 big difference; series complete
make("s17", CARDCSS + """
    #s17-lab { top: 1060px; }
""", f"""
      <div class="row t-h2" style="top:280px"><span class="mask"><span class="in" id="s17-h1">هيفرق معاك</span></span></div>
      <div class="row t-h1 op-y" style="top:400px"><span class="mask"><span class="in" id="s17-h2">بشكل كبير جدًا</span></span></div>
      {card_n("s17-c1", 740, 640, 260, 380, "TIP", "01", "", extra=DONE)}
      {card_n("s17-c2", 410, 640, 260, 380, "TIP", "02", "", extra=DONE)}
      {card_n("s17-c3", 80, 640, 260, 380, "TIP", "03", "", extra=DONE)}
      {label("s17-lab", 1060, "SERIES COMPLETE · OPUS 5.5 TIPS")}
      {spark("s17-sp", 460, 1140, 160)}
""", """
      fx.maskUp("#s17-h1", 83.1); fx.maskUp("#s17-h2", 84.3);
      fx.pop("#s17-c1", 84.25, { from: 0.3 }); fx.pop("#s17-c2", 84.5, { from: 0.3 }); fx.pop("#s17-c3", 84.75, { from: 0.3 });
      fx.rise("#s17-lab", 85.0, { y: 14 });
      fx.pop("#s17-sp", 85.0, { from: 0.2, e: "expo.out", d: 0.6 });
      tl.fromTo("#s17-sp-svg", { rotation: 0 }, { rotation: 180, duration: 3.2, ease: "none" }, 85.0);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s18 CTA subscribe + bell
make("s18", """
    #s18-plate { left: 120px; top: 1300px; width: 840px; height: 170px; border-radius: 30px; background: rgba(4,22,20,.82); border: 2px solid rgba(179,206,101,.45); }
    #s18-nm { position: absolute; left: 0; right: 0; top: 18px; text-align: center; }
    #s18-en { position: absolute; left: 0; right: 0; top: 112px; text-align: center; }
    #s18-btn, #s18-btn2 { left: 230px; top: 1530px; }
    #s18-bell { left: 760px; top: 1520px; width: 124px; height: 124px; border-radius: 50%; background: #2b2a28; border: 3px solid var(--yellow); color: var(--yellow); display: flex; align-items: center; justify-content: center; }
    #s18-cur { left: 560px; top: 1600px; } #s18-rip { left: 480px; top: 1580px; }
    #s18-glow { left: 90px; top: 520px; width: 900px; height: 900px; border-radius: 50%; background: radial-gradient(circle, rgba(19,96,82,.9), transparent 68%); }
""", f"""
      <div class="row t-h3" style="top:240px"><span class="mask"><span class="in" id="s18-h1">هعلّمك أكتر عن الـــ<span class="lat">AI</span></span></span></div>
      <div class="row t-h2 op-l" style="top:330px"><span class="mask"><span class="in" id="s18-h2">في حياتك وشغلك</span></span></div>
      <div id="s18-glow" class="abs"></div>
      {hossam("s18-hs", 170, 560, 740)}
      <div id="s18-plate" class="abs"><div id="s18-nm" class="t-h3">حسام الدين حسن</div><div id="s18-en" class="t-label" style="color:var(--lime)">SEE YOU IN THE NEXT VIDEOS</div></div>
      <div id="s18-btn" class="op-btn">اشترك</div>
      <div id="s18-btn2" class="op-btn on">{ic("check", 44, "var(--lime)")} مشترك</div>
      <div id="s18-bell" class="abs">{ic("bell", 70)}</div>
      <div id="s18-rip" class="ripple"></div>
      <svg id="s18-cur" class="cursor"><use href="#i-cursor" /></svg>
""", """
      fx.maskUp("#s18-h1", 88.35); fx.maskUp("#s18-h2", 89.5);
      tl.fromTo("#s18-glow", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.8, ease: "power2.out" }, 88.2);
      tl.fromTo("#s18-hs", { opacity: 0, y: 260 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, 88.3);
      tl.fromTo("#s18-plate", { opacity: 0, y: 60, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 90.6);
      fx.pop("#s18-btn", 91.7, { from: 0.4 }); fx.pop("#s18-bell", 91.9, { from: 0.4 });
      fx.hide("#s18-btn2");
      tl.fromTo("#s18-cur", { opacity: 0, x: 200, y: 160 }, { opacity: 1, x: 0, y: 0, duration: 0.4, ease: "power3.out" }, 92.0);
      fx.click("#s18-cur", 92.4, "#s18-btn", "#s18-rip");
      tl.to("#s18-btn", { opacity: 0, duration: 0.1 }, 92.5);
      tl.to("#s18-btn2", { opacity: 1, duration: 0.1 }, 92.5);
      tl.to("#s18-cur", { x: 280, y: -20, duration: 0.4, ease: "power3.inOut" }, 92.7);
      fx.click("#s18-cur", 93.15, "#s18-bell");
      for (let i = 0; i < 8; i++) tl.to("#s18-bell", { rotation: (i % 2 ? -1 : 1) * 18 * (1 - i / 8), duration: 0.07, ease: "none" }, 93.25 + i * 0.07);
      tl.to("#s18-bell", { rotation: 0, background: "#ffec5c", color: "#0d0d0d", duration: 0.15 }, 93.85);
""", blob=("#136052", 540, 1000), push=1.02, exit_t=96.3)

print("tip3 scenes written")
