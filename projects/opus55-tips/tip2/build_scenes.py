# Part 2 — "Package it into a SKILL" (9:16, dark). Times = GLOBAL seconds on assets/voice/tip2.wav.
# Signature (part 2): learnings / mistakes / fixes fly into the clay package, the lime tape seals it -> SKILL.
# Payoff: the token bar drains from 100% (first time) to 25–30% (Hossam's own example, "مثلا").
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from build_lib import Part, patch_root, spark, ic, label, head, claude_input, chip, hossam  # noqa: E402

P = Part(HERE)
patch_root(HERE, flashes=(39.97, 57.38))
make = P.make
PKG = "assets/images/package_cut.png"


def card_n(id_, x, y, w, h, top_label, num, sub="", cls="", sp=None, extra=""):
    spk = spark(f"{id_}-sp", (w - sp) // 2, 36, sp, bloom=False) if sp else ""
    return (f'<div id="{id_}" class="op-card {cls}" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px">{spk}'
            f'<div class="op-n op-en" data-layout-allow-overlap style="top:{int(h * .33)}px; font-size:{int(w * .1)}px; letter-spacing:.3em; color:var(--lime)">{top_label}</div>'
            f'<div class="op-n op-en op-y" data-layout-allow-overlap style="top:{int(h * .42)}px; font-size:{int(w * .5)}px; line-height:1">{num}</div>'
            f'<div class="op-n op-en" data-layout-allow-overlap style="top:{int(h * .84)}px; font-size:{int(w * .075)}px; color:var(--fg-muted)">{sub}</div>{extra}</div>')


CARDCSS = """
    .op-n { position: absolute; left: 0; right: 0; text-align: center; white-space: nowrap; }
    .op-lk { position: absolute; left: 50%; top: 50%; width: 80px; height: 80px; margin: -40px 0 0 -40px; color: rgba(179,206,101,.55); }
    .op-done { position: absolute; right: 18px; top: 18px; width: 56px; height: 56px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
"""
DONE = f'<div class="op-done">{ic("check", 36)}</div>'

# ---------------------------------------------------------------- s1 hook: Opus made this video
make("s1", """
    #s1-win { left: 40px; top: 860px; width: 1000px; height: 526px; }
    #s1-vw { position: absolute; left: 0; top: 0; width: 1000px; height: 472px; transform-origin: 49% 32%; }
    #s1-tt { position: absolute; left: 0; right: 0; top: 480px; text-align: center; font-size: 100px; white-space: nowrap; direction: ltr; line-height: 1.15; }
    #s1-tt2 { color: #e8977c; }
""", f"""
      {spark("s1-sp", 440, 250, 200)}
      <div id="s1-tt" class="op-en" data-layout-allow-overlap><span id="s1-tt1">Claude</span> <span id="s1-tt2">Opus 5.5</span></div>
      <div class="row t-h2" style="top:640px"><span class="mask"><span class="in" id="s1-h1">هو اللي عمل الفيديو ده</span></span></div>
      <div id="s1-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>HyperFrames Studio</b></div>
        <div class="body"><div id="s1-vw"><video id="s1-v" class="abs" src="assets/videos/hf_studio.mp4" style="width:1000px; height:472px" data-start="0" data-duration="3.1" data-media-start="0.5" muted playsinline></video></div></div></div>
""", """
      fx.punch("#s1-cam", 0, 1.15);
      fx.pop("#s1-sp", 0.0, { from: 0.2, e: "expo.out", d: 0.8 });
      tl.fromTo("#s1-sp-svg", { rotation: -60 }, { rotation: 90, duration: 3.1, ease: "power2.out" }, 0);
      fx.letterDrop("#s1-tt1", 0.45, { st: 0.03 }); fx.letterDrop("#s1-tt2", 0.95, { st: 0.035 });
      fx.maskUp("#s1-h1", 2.0);
      tl.fromTo("#s1-win", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 2.3);
      tl.fromTo("#s1-vw", { scale: 1 }, { scale: 1.6, duration: 0.8, ease: "power3.inOut" }, 2.3);
""", blob=("#136052", 540, 500), exit_t=2.95)

# ---------------------------------------------------------------- s2 series: part 2
make("s2", CARDCSS + """
    #s2-c2b, #s2-c2 { left: 370px; top: 560px; width: 340px; height: 500px; }
""", f"""
      {label("s2-lab", 280, "THE SERIES · 3 TIPS")}
      <div class="row t-h3" style="top:330px"><span class="mask"><span class="in" id="s2-h1">عشان تطلّع منه نتايج كويسة</span></span></div>
      {card_n("s2-c1", 80, 610, 260, 400, "TIP", "01", "", extra=DONE)}
      <div id="s2-c3" class="op-card back" style="left:740px; top:610px; width:260px; height:400px"><svg class="op-lk"><use href="#i-lock" /></svg></div>
      <div id="s2-c2b" class="op-card back"><svg class="op-lk"><use href="#i-lock" /></svg></div>
      {card_n("s2-c2", 370, 560, 340, 500, "PART", "02", "TODAY", sp=100)}
      <div class="row t-h1" style="top:1180px"><span class="mask"><span class="in" id="s2-k1">السلسلة دي</span></span></div>
""", """
      fx.rise("#s2-lab", 2.9, { y: 12 }); fx.maskUp("#s2-h1", 2.95);
      fx.rise("#s2-c1", 2.9, { y: 80 }); fx.rise("#s2-c3", 2.95, { y: 80 }); fx.rise("#s2-c2b", 3.0, { y: 120 });
      fx.maskUp("#s2-k1", 5.2);
      fx.hide("#s2-c2");
      tl.to("#s2-c2b", { scaleX: 0, duration: 0.16, ease: "power2.in" }, 6.25);
      tl.fromTo("#s2-c2", { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.22, ease: "power2.out", immediateRender: false }, 6.41);
      tl.fromTo("#s2-c2-sp-svg", { rotation: 0 }, { rotation: 120, duration: 0.6, ease: "power2.out" }, 6.41);
""", blob=("#136052", 540, 800))

# ---------------------------------------------------------------- s3 recap tip 1, tip 2 maybe more important
make("s3", CARDCSS + """
    #s3-t1 { left: 560px; top: 560px; width: 420px; height: 560px; }
    #s3-t2 { left: 100px; top: 560px; width: 420px; height: 560px; }
    .s3-ar { position: absolute; left: 0; right: 0; top: 400px; text-align: center; font-family: var(--font-ar); font-weight: 800; font-size: 40px; }
    #s3-gt { left: 150px; top: 1150px; }
""", f"""
      <div class="row t-h3" style="top:250px"><span class="mask"><span class="in" id="s3-h1">في بارت ١ قلنا</span></span></div>
      <div id="s3-t1" class="op-card" style="opacity:.9">
        <div class="op-n op-en" style="top:60px; font-size:34px; letter-spacing:.3em; color:var(--lime)">TIP 01</div>
        <div class="op-n" style="top:140px">{ic("expand", 170, "var(--lime)")}</div>
        <div class="s3-ar">ما تحجّمهوش</div>{DONE}</div>
      <div id="s3-t2" class="op-card" style="border-color:var(--yellow)">
        <div class="op-n op-en" style="top:60px; font-size:34px; letter-spacing:.3em; color:var(--yellow)">TIP 02</div>
        <div class="op-n op-en op-y" style="top:130px; font-size:220px; line-height:1">?</div>
        <div class="s3-ar">النهارده</div></div>
      {chip("s3-gt", 150, 1150, "يمكن أهم من الأولى", "!", "y")}
      <div class="row t-h2" style="top:1380px"><span class="mask"><span class="in" id="s3-k1">واحدة من أهم التيبس</span></span></div>
""", """
      fx.maskUp("#s3-h1", 7.0);
      tl.fromTo("#s3-t1", { opacity: 0, x: 300, rotation: 8 }, { opacity: 1, x: 0, rotation: 0, duration: 0.55, ease: "power3.out" }, 9.8);
      fx.maskUp("#s3-k1", 10.4);
      tl.fromTo("#s3-t2", { opacity: 0, x: -300, rotation: -8 }, { opacity: 1, x: 0, rotation: 0, duration: 0.55, ease: "power3.out" }, 12.45);
      tl.to("#s3-t1", { scale: 0.86, opacity: 0.6, duration: 0.6, ease: "power2.inOut" }, 13.3);
      tl.to("#s3-t2", { scale: 1.08, duration: 0.6, ease: "back.out(1.6)" }, 13.3);
      fx.pop("#s3-gt", 13.4, { from: 0.4 });
""", blob=("#0f4f44", 540, 840))

# ---------------------------------------------------------------- s4 good result -> package it
make("s4", """
    #s4-res { left: 240px; top: 540px; width: 600px; height: 420px; }
    #s4-rt { position: absolute; left: 0; right: 0; top: 260px; text-align: center; }
    #s4-ok { position: absolute; right: 26px; top: 26px; width: 72px; height: 72px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
    #s4-pk { left: 270px; top: 820px; width: 540px; height: 540px; }
    #s4-en { top: 1380px; font-size: 120px; color: var(--yellow); }
""", f"""
      <div class="row t-h3" style="top:250px"><span class="mask"><span class="in" id="s4-h1">بعد ما تطلّع نتيجة كويسة</span></span></div>
      <div class="row t-h3 muted" style="top:340px"><span class="mask"><span class="in" id="s4-h2">مع <span class="lat">Claude Opus 5.5</span></span></span></div>
      <div id="s4-res" class="op-card">{spark("s4-sp", 230, 60, 140, bloom=False)}<div id="s4-rt" class="t-h3">النتيجة الكويسة</div><div id="s4-ok">{ic("check", 46)}</div></div>
      <img id="s4-pk" class="abs" src="{PKG}" />
      <div id="s4-en" class="op-big"><span id="s4-en1">PACKAGE IT</span></div>
""", """
      fx.maskUp("#s4-h1", 14.85); fx.maskUp("#s4-h2", 17.2);
      tl.fromTo("#s4-res", { opacity: 0, y: 140, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.5)" }, 16.0);
      fx.pop("#s4-ok", 16.6, { from: 0 });
      tl.fromTo("#s4-pk", { opacity: 0, y: 260, scale: 0.6 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.6)" }, 19.35);
      tl.to("#s4-res", { y: 420, scale: 0.25, opacity: 0, duration: 0.5, ease: "power3.in" }, 19.9);
      tl.to("#s4-pk", { scale: 1.06, duration: 0.15, yoyo: true, repeat: 1 }, 20.35);
      fx.letterDrop("#s4-en1", 19.5, { st: 0.035 });
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s5 every similar task = burn tokens again
make("s5", """
    .s5-r { position: absolute; left: 110px; width: 860px; height: 150px; border-radius: 26px; background: rgba(255,255,255,.05); border: 2px solid var(--edge); }
    .s5-r b { position: absolute; left: 30px; top: 22px; font-family: var(--font-en); font-weight: 900; font-size: 26px; letter-spacing: .2em; color: var(--fg-muted); }
    .s5-r .op-track { left: 30px; right: 30px; top: 78px; height: 40px; }
    #s5-r1 { top: 560px; } #s5-r2 { top: 740px; } #s5-r3 { top: 920px; }
""", f"""
      <div class="row t-h2" style="top:280px"><span class="mask"><span class="in" id="s5-h1">مش كل مرة</span></span></div>
      <div class="row t-h3 muted" style="top:400px"><span class="mask"><span class="in" id="s5-h2">تطلّع حاجة مشابهة</span></span></div>
      {"".join(f'<div class="s5-r" id="s5-r{i}"><b>RUN {i} · TOKENS</b><div class="op-track"><div class="op-fill s5-f" id="s5-f{i}" style="background:var(--yellow)"></div></div></div>' for i in (1, 2, 3))}
      <div class="row t-h2" style="top:1150px"><span class="mask"><span class="in" id="s5-k1">الموديل يقعد يحرق</span></span></div>
      <div class="row t-h1 op-o" style="top:1290px"><span class="mask"><span class="in" id="s5-k2"><span class="lat">tokens</span> كتير</span></span></div>
""", """
      fx.maskUp("#s5-h1", 20.8); fx.maskUp("#s5-h2", 22.3);
      fx.rise("#s5-r1", 21.5, { y: 40 }); fx.rise("#s5-r2", 21.9, { y: 40 }); fx.rise("#s5-r3", 22.3, { y: 40 });
      fx.meter("#s5-f1", 21.7, 0.9, 1, { e: "power2.out" }); fx.meter("#s5-f2", 22.1, 0.9, 1, { e: "power2.out" }); fx.meter("#s5-f3", 22.5, 0.9, 1, { e: "power2.out" });
      tl.to(".s5-f", { background: "#ff5a33", duration: 0.25 }, 26.3);
      fx.shake("#s5-r1, #s5-r2, #s5-r3", 26.35, 10, 6);
      fx.maskUp("#s5-k1", 25.2); fx.maskUp("#s5-k2", 26.3);
""", blob=("#3a1a12", 540, 760))

# ---------------------------------------------------------------- s6 simple: once you're happy with the result
make("s6", """
    #s6-st { left: 330px; top: 470px; font-size: 96px; color: var(--lime); border-color: var(--lime); }
    #s6-res { left: 240px; top: 800px; width: 600px; height: 420px; }
    #s6-rt { position: absolute; left: 0; right: 0; top: 260px; text-align: center; }
    #s6-like { left: 760px; top: 760px; width: 150px; height: 150px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
""", f"""
      {label("s6-lab", 280, "THE FIX")}
      <div class="row t-h3" style="top:330px"><span class="mask"><span class="in" id="s6-h1">والموضوع</span></span></div>
      <div id="s6-st" class="stamp">بسيط</div>
      <div id="s6-res" class="op-card">{spark("s6-sp", 230, 60, 140, bloom=False)}<div id="s6-rt" class="t-h3">النتيجة</div></div>
      <div id="s6-like" class="abs">{ic("like", 80)}<div class="ring" id="s6-r" style="border-radius:50%"></div></div>
      <div class="row t-h2" style="top:1300px"><span class="mask"><span class="in" id="s6-k1">اللي انت راضي عنها</span></span></div>
""", """
      fx.rise("#s6-lab", 27.5, { y: 12 }); fx.maskUp("#s6-h1", 27.6);
      fx.stamp("#s6-st", 28.15, "#s6-cam");
      tl.fromTo("#s6-res", { opacity: 0, y: 140 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 28.9);
      fx.maskUp("#s6-k1", 29.6);
      fx.pop("#s6-like", 29.85, { from: 0 }); fx.ringPulse("#s6-r", 29.95);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s7 don't continue same chat, don't restart
make("s7", """
    .s7-col { position: absolute; top: 470px; width: 440px; height: 820px; border-radius: 30px; background: #1f1e1d; border: 2px solid #3d3c39; overflow: hidden; }
    #s7-a { left: 570px; } #s7-b { left: 70px; }
    .s7-bub { position: absolute; height: 46px; border-radius: 23px; }
    .s7-me { right: 26px; background: #3d3c39; } .s7-ai { left: 26px; background: #2b2a28; border: 2px solid #3d3c39; }
    .s7-t { position: absolute; left: 0; right: 0; bottom: 30px; text-align: center; font-family: var(--font-ar); font-weight: 800; font-size: 36px; }
    #s7-tm { position: absolute; left: 26px; right: 26px; top: 24px; height: 26px; }
    .s7-x { position: absolute; width: 140px; height: 140px; border-radius: 50%; background: var(--orange); color: #fff; display: flex; align-items: center; justify-content: center; }
    #s7-xa { left: 720px; top: 780px; } #s7-xb { left: 220px; top: 780px; }
    #s7-q { position: absolute; left: 0; right: 0; top: 300px; text-align: center; font-family: var(--font-ar); font-weight: 900; font-size: 200px; color: rgba(255,255,255,.18); }
""", f"""
      <div class="row t-h2" style="top:280px"><span class="mask"><span class="in" id="s7-h1">بدل ما</span></span></div>
      <div id="s7-a" class="s7-col"><div id="s7-tm" class="op-track"><div class="op-fill" id="s7-tf" style="background:var(--orange)"></div></div>
        {"".join(f'<i class="s7-bub {"s7-me" if i % 2 == 0 else "s7-ai"} s7-b{i}" style="top:{80 + i * 62}px; width:{[220, 330, 180, 300, 250, 340, 200, 310, 230, 290][i]}px"></i>' for i in range(10))}
        <div class="s7-t">تكمل في نفس الشات</div></div>
      <div id="s7-b" class="s7-col"><div id="s7-q">؟</div><div class="s7-t">تبدأ معاه من الصفر</div></div>
      <div id="s7-xa" class="s7-x">{ic("x", 90)}</div><div id="s7-xb" class="s7-x">{ic("x", 90)}</div>
      <div class="row t-h3 op-o" style="top:1360px"><span class="mask"><span class="in" id="s7-k1">فتحرق <span class="lat">tokens</span></span></span></div>
      <div class="row t-h3 op-o" style="top:1460px"><span class="mask"><span class="in" id="s7-k2">وتفهّمه من الأول</span></span></div>
""", """
      fx.maskUp("#s7-h1", 32.15);
      tl.fromTo("#s7-a", { opacity: 0, y: 100 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 32.2);
      tl.fromTo("#s7-a i", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.2, stagger: 0.12 }, 32.5);
      fx.meter("#s7-tf", 32.6, 1.7, 1, { e: "power1.in" });
      fx.maskUp("#s7-k1", 34.0);
      fx.pop("#s7-xa", 34.4, { from: 0.2 });
      tl.to("#s7-a", { filter: "grayscale(1) brightness(.6)", duration: 0.3 }, 34.45);
      tl.fromTo("#s7-b", { opacity: 0, y: 100 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 35.05);
      fx.pop("#s7-q", 35.6, { from: 0.4 });
      fx.maskUp("#s7-k2", 36.45);
      fx.pop("#s7-xb", 37.55, { from: 0.2 });
      tl.to("#s7-b", { filter: "grayscale(1) brightness(.6)", duration: 0.3 }, 37.6);
""", blob=("#3a1a12", 540, 880))

# ---------------------------------------------------------------- s8 SLAM: ask for a SKILL
make("s8", """
    #s8-pk { left: 240px; top: 640px; width: 600px; height: 600px; }
    #s8-en { top: 1220px; font-size: 230px; color: var(--lime); text-shadow: 0 0 80px rgba(179,206,101,.55); }
    #s8-ring { left: 240px; top: 640px; width: 600px; height: 600px; border-radius: 50%; }
""", f"""
      <div class="row t-h2" style="top:280px"><span class="mask"><span class="in" id="s8-h1">اطلب من</span></span></div>
      <div class="row op-en" style="top:400px; font-size:100px; color:#e8977c"><span class="mask"><span class="in" id="s8-h2">Claude Opus</span></span></div>
      <img id="s8-pk" class="abs" src="{PKG}" />
      <div id="s8-ring" class="abs"><div class="ring" id="s8-r1" style="border-radius:50%"></div><div class="ring" id="s8-r2" style="border-radius:50%"></div></div>
      {spark("s8-sp", 470, 600, 140, bloom=False)}
      <div id="s8-en" class="op-big"><span id="s8-en1" style="display:inline-block">SKILL</span></div>
""", """
      fx.maskUp("#s8-h1", 38.35); fx.maskUp("#s8-h2", 38.85);
      tl.fromTo("#s8-pk", { opacity: 0, scale: 0.5, rotation: -10 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.6, ease: "back.out(1.6)" }, 38.5);
      fx.pop("#s8-sp", 39.2, { from: 0.2 });
      tl.fromTo("#s8-sp-svg", { rotation: 0 }, { rotation: 220, duration: 2.5, ease: "none" }, 39.2);
      tl.fromTo("#s8-en1", { opacity: 0, scale: 2.6, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }, 39.95);
      fx.shake("#s8-cam", 40.05, 18, 7);
      fx.ringPulse("#s8-r1, #s8-r2", 40.0, { scale: 1.8 });
      fx.breathe("#s8-pk", 40.4, 1.3, 0.03, 0.65);
""", blob=("#136052", 540, 940), push=1.03)

# ---------------------------------------------------------------- s9 open Claude, open the good session, ask
make("s9", """
    #s9-win { left: 150px; top: 470px; width: 780px; height: 580px; }
    #s9-v { left: -60px; top: -260px; width: 900px; height: 1062px; }
    #s9-ses { left: 110px; top: 470px; width: 860px; height: 200px; }
    #s9-st { position: absolute; right: 34px; top: 26px; direction: rtl; text-align: right; font-size: 46px; white-space: nowrap; }
    #s9-sl { position: absolute; right: 34px; top: 138px; font-family: var(--font-en); font-weight: 800; font-size: 22px; letter-spacing: .18em; color: var(--lime); direction: ltr; }
    #s9-ok { position: absolute; left: 34px; top: 60px; width: 80px; height: 80px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
    #s9-cur { left: 860px; top: 1000px; }
""", f"""
      <div class="row t-h2" style="top:260px"><span class="mask"><span class="in" id="s9-h1">افتح <span class="lat">Claude</span></span></span></div>
      <div id="s9-win" class="op-win"><div class="bar"><i></i><i></i><i></i><b>Claude</b></div>
        <div class="body"><video id="s9-v" src="assets/videos/claude_app.mp4" data-start="0" data-duration="1.7" data-media-start="0.1" muted playsinline></video></div></div>
      <div id="s9-ses" class="op-card"><div id="s9-st" class="t-h3">السيشن اللي طلّعت النتيجة</div><div id="s9-sl">SESSION · GOOD RESULT</div><div id="s9-ok">{ic("check", 50)}</div></div>
      {claude_input("s9-in", 70, 760, 940, 250)}
      <div class="row t-h3 muted" style="top:1110px"><span class="mask"><span class="in" id="s9-k1">وقوله</span></span></div>
      <svg id="s9-cur" class="cursor"><use href="#i-cursor" /></svg>
""", """
      fx.maskUp("#s9-h1", 41.7);
      tl.fromTo("#s9-win", { opacity: 0, y: 140, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "power3.out" }, 41.6);
      tl.to("#s9-win", { opacity: 0, scale: 0.9, y: -80, duration: 0.3, ease: "power2.in" }, 42.95);
      tl.to("#s9-h1", { yPercent: -115, duration: 0.25 }, 43.0);
      tl.fromTo("#s9-ses", { opacity: 0, y: 100 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.5)" }, 43.15);
      fx.pop("#s9-ok", 44.1, { from: 0 });
      tl.fromTo("#s9-in", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 44.5);
      fx.maskUp("#s9-k1", 44.75);
      fx.typeText("#s9-in-t", 45.2, "عايزك تطلّعلي skill أو prompt", 18);
      tl.fromTo("#s9-cur", { opacity: 0, x: 80, y: 140 }, { opacity: 1, x: 0, y: 0, duration: 0.45, ease: "power3.out" }, 46.4);
      fx.click("#s9-cur", 47.0, "#s9-in-s");
""", blob=("#136052", 540, 800), push=1.025)

# ---------------------------------------------------------------- s10 new session + skill = reliable every time
make("s10", """
    #s10-ns { position: absolute; left: 110px; top: 460px; width: 860px; height: 380px; border-radius: 30px; background: #1f1e1d; border: 2px dashed #5a5953; }
    #s10-nl { position: absolute; left: 30px; top: 24px; font-family: var(--font-en); font-weight: 800; font-size: 24px; letter-spacing: .18em; color: #9a988f; direction: ltr; }
    #s10-pk { left: 380px; top: 470px; width: 320px; height: 320px; }
    .s10-r { position: absolute; top: 1000px; width: 270px; height: 300px; }
    #s10-a { left: 750px; } #s10-b { left: 405px; } #s10-c { left: 60px; }
    .s10-ok { position: absolute; left: 50%; top: 180px; width: 74px; height: 74px; margin-left: -37px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; }
""", f"""
      <div id="s10-ns"><div id="s10-nl">NEW SESSION</div></div>
      <img id="s10-pk" class="abs" src="{PKG}" />
      <div class="row t-h3" style="top:880px"><span class="mask"><span class="in" id="s10-h1">نتيجة يُعتمد عليها</span></span></div>
      {"".join(f'<div id="s10-{k}" class="op-card s10-r">{spark(f"s10-{k}-sp", 85, 40, 100, bloom=False)}<div class="s10-ok">{ic("check", 46)}</div></div>' for k in "abc")}
      <div class="row t-h1 op-y" style="top:1380px"><span class="mask"><span class="in" id="s10-k1">كل مرة</span></span></div>
""", """
      tl.fromTo("#s10-ns", { opacity: 0, y: 100 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 47.4);
      tl.fromTo("#s10-pk", { opacity: 0, y: -500, rotation: -20 }, { opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "bounce.out" }, 48.5);
      tl.to("#s10-ns", { borderColor: "#b3ce65", duration: 0.2 }, 49.0);
      fx.maskUp("#s10-h1", 50.0);
      fx.pop("#s10-a", 50.5, { from: 0.3 }); fx.pop("#s10-b", 51.0, { from: 0.3 }); fx.pop("#s10-c", 51.5, { from: 0.3 });
      fx.maskUp("#s10-k1", 51.6);
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s11 learnings + mistakes + fixes -> sealed (SIGNATURE)
make("s11", """
    #s11-pk { left: 290px; top: 860px; width: 500px; height: 500px; }
    #s11-tape { left: 495px; top: 900px; width: 92px; height: 400px; background: var(--lime); border-radius: 8px; transform-origin: 50% 0; box-shadow: 0 0 30px rgba(179,206,101,.6); }
    #s11-c1 { left: 600px; top: 520px; } #s11-c2 { left: 330px; top: 640px; } #s11-c3 { left: 70px; top: 520px; }
    #s11-tag { left: 360px; top: 1380px; }
""", f"""
      <div class="row t-h3" style="top:260px"><span class="mask"><span class="in" id="s11-h1">وهنا اذكر كل</span></span></div>
      <img id="s11-pk" class="abs" src="{PKG}" />
      {chip("s11-c1", 600, 520, "اللي اتعلمته", ic("book", 32))}
      {chip("s11-c2", 330, 640, "الأخطاء", ic("x", 34), "o")}
      {chip("s11-c3", 70, 520, "الإصلاحات", ic("check", 34), "y")}
      <div id="s11-tape" class="abs"></div>
      <div id="s11-tag" class="stamp" style="color:var(--lime); border-color:var(--lime); font-family:var(--font-en); font-size:70px; background:rgba(4,22,20,.9)">SKILL.md</div>
""", """
      fx.maskUp("#s11-h1", 52.45);
      tl.fromTo("#s11-pk", { opacity: 0, y: 160 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 52.4);
      fx.pop("#s11-c1", 54.1); fx.pop("#s11-c2", 55.6); fx.pop("#s11-c3", 56.8);
      tl.to("#s11-c1", { x: -200, y: 450, scale: 0.2, opacity: 0, duration: 0.35, ease: "power3.in" }, 54.9);
      tl.to("#s11-c2", { x: 60, y: 380, scale: 0.2, opacity: 0, duration: 0.35, ease: "power3.in" }, 56.3);
      tl.to("#s11-c3", { x: 300, y: 450, scale: 0.2, opacity: 0, duration: 0.3, ease: "power3.in" }, 57.1);
      tl.fromTo("#s11-tape", { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.28, ease: "power3.out" }, 57.35);
      fx.shake("#s11-cam", 57.4, 14, 6);
      fx.stamp("#s11-tag", 57.6);
""", blob=("#136052", 540, 1000), exit_t=57.9)

# ---------------------------------------------------------------- s12 more complex -> more value (illustration)
make("s12", """
    #s12-ch { left: 110px; top: 520px; width: 860px; height: 780px; }
    #s12-src { top: 1330px; }
""", f"""
      <div class="row t-h2" style="top:280px"><span class="mask"><span class="in" id="s12-h1">كل ما يكون أعقد</span></span></div>
      <svg id="s12-ch" class="abs" viewBox="0 0 860 780" style="direction:ltr">
        <path d="M80 40V700H830" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="4" />
        <path id="s12-ln" d="M90 690C300 670 520 560 820 70" fill="none" stroke="#b3ce65" stroke-width="12" stroke-linecap="round" pathLength="1" />
        <circle id="s12-dot" cx="820" cy="70" r="22" fill="#ffec5c" />
        <text x="830" y="750" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="26" letter-spacing="5" fill="#8cb2a6">COMPLEXITY</text>
        <text x="40" y="40" transform="rotate(-90 40 40)" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="26" letter-spacing="5" fill="#8cb2a6">VALUE</text>
      </svg>
      <div id="s12-src" class="op-src">ILLUSTRATION</div>
      <div class="row t-h1 op-l" style="top:1400px"><span class="mask"><span class="in" id="s12-k1">هتفيدك أكتر</span></span></div>
""", """
      fx.maskUp("#s12-h1", 58.15);
      tl.fromTo("#s12-ch", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 58.3);
      fx.draw("#s12-ln", 59.0, 1.6, "power2.in");
      fx.pop("#s12-dot", 60.6, { from: 0 });
      fx.maskUp("#s12-k1", 60.4);
      fx.rise("#s12-src", 58.5, { y: 8, b: 0 });
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s13 my example: first result had mistakes
make("s13", """
    #s13-ph { left: 300px; top: 470px; width: 480px; height: 860px; }
    #s13-v { position: absolute; left: -1673px; top: -195px; width: 3858px; height: 1822px; }
    #s13-v1 { left: 250px; top: 470px; }
    .s13-m { position: absolute; width: 120px; height: 120px; border-radius: 50%; border: 7px solid var(--orange); box-shadow: 0 0 24px rgba(255,90,51,.6); }
    #s13-m1 { left: 360px; top: 600px; } #s13-m2 { left: 610px; top: 860px; } #s13-m3 { left: 400px; top: 1120px; }
    #s13-w { left: 640px; top: 1180px; }
""", f"""
      {label("s13-lab", 250, "MY EXAMPLE · THESE VIDEOS")}
      <div class="row t-h3" style="top:300px"><span class="mask"><span class="in" id="s13-h1">أول نتيجة ماكانتش وحشة</span></span></div>
      <div id="s13-ph" class="op-phone"><div class="scr"><video id="s13-v" src="assets/videos/hf_studio.mp4" data-start="0" data-duration="6.65" data-media-start="1.6" muted playsinline></video></div></div>
      <div id="s13-v1" class="tag" style="position:absolute; background:#0b2f29; color:var(--lime); font-family:var(--font-en); font-weight:900; font-size:26px; letter-spacing:.2em; direction:ltr">V1</div>
      <div class="s13-m" id="s13-m1"></div><div class="s13-m" id="s13-m2"></div><div class="s13-m" id="s13-m3"></div>
      {chip("s13-w", 600, 1180, "مش دقيقة", "!", "o")}
      <div class="row t-h2 op-o" style="top:1400px"><span class="mask"><span class="in" id="s13-k1">لكن فيها أخطاء</span></span></div>
""", """
      fx.rise("#s13-lab", 61.3, { y: 12 }); fx.maskUp("#s13-h1", 62.4);
      tl.fromTo("#s13-ph", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.55, ease: "back.out(1.3)" }, 61.4);
      fx.pop("#s13-v1", 63.9);
      fx.maskUp("#s13-k1", 65.4);
      fx.pop("#s13-m1", 65.6, { from: 1.8, e: "power3.out" }); fx.pop("#s13-m2", 65.9, { from: 1.8, e: "power3.out" }); fx.pop("#s13-m3", 66.2, { from: 1.8, e: "power3.out" });
      fx.pop("#s13-w", 66.6, { from: 0.3 });
""", blob=("#0f4f44", 540, 900))

# ---------------------------------------------------------------- s14 feedback loop, burned many tokens
make("s14", """
    .s14-b { position: absolute; height: 92px; padding: 0 34px; border-radius: 46px; display: flex; align-items: center; gap: 14px; font-family: var(--font-ar); font-weight: 700; font-size: 36px; white-space: nowrap; }
    .s14-me { right: 90px; background: #3d3c39; color: #ecebe4; }
    .s14-ai { left: 90px; background: #0b2f29; border: 3px solid rgba(217,119,87,.7); }
    #s14-b1 { top: 480px; } #s14-b2 { top: 610px; } #s14-b3 { top: 740px; } #s14-b4 { top: 870px; }
    #s14-tl { top: 1080px; } #s14-tr { left: 110px; top: 1140px; width: 860px; height: 56px; border-radius: 28px; }
""", f"""
      <div class="row t-h2" style="top:280px"><span class="mask"><span class="in" id="s14-h1">ادّيت <span class="lat">feedback</span></span></span></div>
      <div id="s14-b1" class="s14-b s14-me">في حاجات مش مظبوطة</div>
      <div id="s14-b2" class="s14-b s14-ai">{spark("s14-sa", 0, 0, 50, bloom=False, extra="position:relative")}<span>اتعلّمت · هجرّب تاني</span></div>
      <div id="s14-b3" class="s14-b s14-me">لسه في غلطة هنا</div>
      <div id="s14-b4" class="s14-b s14-ai">{spark("s14-sb", 0, 0, 50, bloom=False, extra="position:relative")}<span>صلّحتها</span></div>
      {label("s14-tl", 1080, "TOKENS · FIRST TIME")}
      <div id="s14-tr" class="op-track"><div id="s14-tf" class="op-fill" style="background:linear-gradient(270deg, var(--yellow), var(--orange)); border-radius:28px"></div></div>
      <div class="row t-h2 op-o" style="top:1300px"><span class="mask"><span class="in" id="s14-k1">وحرق <span class="lat">tokens</span> كتير</span></span></div>
""", """
      fx.maskUp("#s14-h1", 67.8);
      tl.fromTo("#s14-b1", { opacity: 0, x: 120 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 67.85);
      tl.fromTo("#s14-b2", { opacity: 0, x: -120 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 68.6);
      tl.fromTo("#s14-b3", { opacity: 0, x: 120 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 69.5);
      tl.fromTo("#s14-b4", { opacity: 0, x: -120 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 70.25);
      fx.rise("#s14-tl, #s14-tr", 68.2, { y: 20 });
      fx.meter("#s14-tf", 68.4, 3.0, 1, { e: "power1.in" });
      fx.maskUp("#s14-k1", 70.7);
""", blob=("#3a1a12", 540, 900))

# ---------------------------------------------------------------- s15 then I made the skill
make("s15", """
    #s15-pk { left: 240px; top: 560px; width: 600px; height: 600px; }
    #s15-st { left: 300px; top: 1170px; color: var(--lime); border-color: var(--lime); font-family: var(--font-en); font-size: 90px; background: rgba(4,22,20,.9); }
""", f"""
      <div class="row t-h2" style="top:280px"><span class="mask"><span class="in" id="s15-h1">بعد كده</span></span></div>
      <div class="row t-h3 muted" style="top:400px"><span class="mask"><span class="in" id="s15-h2">عملت التيب دي</span></span></div>
      <img id="s15-pk" class="abs" src="{PKG}" />
      <div id="s15-st" class="stamp">SKILL ✓</div>
""", """
      fx.maskUp("#s15-h1", 72.3); fx.maskUp("#s15-h2", 73.2);
      tl.fromTo("#s15-pk", { opacity: 0, scale: 0.4, rotation: 12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.7)" }, 72.4);
      fx.stamp("#s15-st", 73.6, "#s15-cam");
""", blob=("#136052", 540, 860))

# ---------------------------------------------------------------- s16 PAYOFF: 100% -> 25–30%
make("s16", """
    .s16-l { position: absolute; right: 110px; font-family: var(--font-en); font-weight: 900; font-size: 28px; letter-spacing: .2em; direction: ltr; }
    #s16-l1 { top: 560px; color: var(--orange); } #s16-l2 { top: 820px; color: var(--lime); }
    .s16-t { left: 110px; width: 860px; height: 90px; border-radius: 45px; }
    #s16-t1 { top: 610px; } #s16-t2 { top: 870px; }
    .s16-p { position: absolute; left: 110px; font-family: var(--font-en); font-weight: 900; font-size: 44px; direction: ltr; }
    #s16-p1 { top: 560px; top: 550px; color: var(--fg); } #s16-p2 { top: 810px; color: var(--yellow); }
    #s16-big { position: absolute; left: 0; right: 0; top: 1030px; text-align: center; font-family: var(--font-ar); font-weight: 900; font-size: 160px; line-height: 1.3; color: var(--yellow); direction: rtl; }
    #s16-c1 { left: 600px; top: 1430px; } #s16-c2 { left: 160px; top: 1430px; }
    #s16-src { top: 1600px; }
""", f"""
      {label("s16-lab", 250, "EVERY NEW VIDEO")}
      <div class="row t-h3" style="top:300px"><span class="mask"><span class="in" id="s16-h1">بيحرق بس</span></span></div>
      <div id="s16-l1" class="s16-l">FIRST TIME</div><div id="s16-p1" class="s16-p">100%</div>
      <div id="s16-t1" class="op-track s16-t"><div id="s16-f1" class="op-fill" style="background:var(--orange); border-radius:45px"></div></div>
      <div id="s16-l2" class="s16-l">WITH THE SKILL</div><div id="s16-p2" class="s16-p">~25–30%</div>
      <div id="s16-t2" class="op-track s16-t"><div id="s16-f2" class="op-fill" style="background:var(--lime); border-radius:45px"></div></div>
      <div id="s16-big" data-layout-allow-overlap>٢٥–٣٠٪</div>
      <div class="row t-h3" style="top:1260px"><span class="mask"><span class="in" id="s16-k1">من الـــ<span class="lat">tokens</span> بتاعة أول مرة</span></span></div>
      {chip("s16-c1", 600, 1430, "توفير tokens", ic("token", 34))}
      {chip("s16-c2", 160, 1430, "ووقت", ic("clock", 34), "y")}
      <div id="s16-src" class="op-src">HOSSAM'S EXAMPLE · APPROXIMATE</div>
""", """
      fx.rise("#s16-lab", 74.85, { y: 12 }); fx.maskUp("#s16-h1", 76.8);
      fx.rise("#s16-l1, #s16-p1, #s16-t1", 75.0, { y: 20 });
      fx.meter("#s16-f1", 75.2, 0.6, 1, { e: "power2.out" });
      fx.rise("#s16-l2, #s16-t2", 75.6, { y: 20 });
      fx.meter("#s16-f2", 75.8, 0.5, 1, { e: "power2.out" });
      fx.hide("#s16-p2");
      tl.to("#s16-f2", { scaleX: 0.275, duration: 1.3, ease: "power2.inOut" }, 77.6);
      tl.to("#s16-p2", { opacity: 1, duration: 0.2 }, 78.6);
      tl.fromTo("#s16-big", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 77.65);
      fx.maskUp("#s16-k1", 79.2);
      fx.pop("#s16-c1", 82.35); fx.pop("#s16-c2", 84.0);
      fx.rise("#s16-src", 78.0, { y: 8, b: 0 });
""", blob=("#136052", 540, 900))

# ---------------------------------------------------------------- s17 next: part 3
make("s17", CARDCSS + """
    #s17-c3b, #s17-c3 { left: 370px; top: 470px; width: 340px; height: 500px; }
""", f"""
      {label("s17-lab", 250, "NEXT EPISODE")}
      <div class="row t-h2" style="top:300px"><span class="mask"><span class="in" id="s17-h1">في البارت الجاي</span></span></div>
      {card_n("s17-c1", 80, 520, 260, 400, "TIP", "01", "", extra=DONE)}
      {card_n("s17-c2", 740, 520, 260, 400, "TIP", "02", "", extra=DONE)}
      <div id="s17-c3b" class="op-card back"><svg class="op-lk"><use href="#i-lock" /></svg></div>
      {card_n("s17-c3", 370, 470, 340, 500, "PART", "03", "COMING NEXT", sp=100)}
      <div class="row t-h2" style="top:1080px"><span class="mask"><span class="in" id="s17-k1">تيب كمان هتفرق معاك</span></span></div>
      <div class="row t-h3 muted" style="top:1240px"><span class="mask"><span class="in" id="s17-k2">لو بتستخدم <span class="lat">Claude Opus 5.5</span></span></span></div>
""", """
      fx.rise("#s17-lab", 84.45, { y: 12 }); fx.maskUp("#s17-h1", 84.6);
      fx.rise("#s17-c1", 84.5, { y: 80 }); fx.rise("#s17-c2", 84.6, { y: 80 }); fx.rise("#s17-c3b", 84.7, { y: 120 });
      fx.hide("#s17-c3");
      tl.to("#s17-c3b", { scaleX: 0, duration: 0.16, ease: "power2.in" }, 85.1);
      tl.fromTo("#s17-c3", { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.22, ease: "power2.out", immediateRender: false }, 85.26);
      tl.fromTo("#s17-c3-sp-svg", { rotation: 0 }, { rotation: 220, duration: 5.4, ease: "none" }, 85.26);
      fx.maskUp("#s17-k1", 86.0); fx.maskUp("#s17-k2", 87.7);
      fx.breathe("#s17-c3", 86.0, 4.4, 0.02, 1.4);
""", blob=("#136052", 540, 760))

# ---------------------------------------------------------------- s18 CTA
make("s18", """
    #s18-plate { left: 120px; top: 1300px; width: 840px; height: 170px; border-radius: 30px; background: rgba(4,22,20,.82); border: 2px solid rgba(179,206,101,.45); }
    #s18-nm { position: absolute; left: 0; right: 0; top: 18px; text-align: center; }
    #s18-en { position: absolute; left: 0; right: 0; top: 112px; text-align: center; }
    #s18-btn, #s18-btn2 { left: 300px; top: 1530px; }
    #s18-cur { left: 640px; top: 1600px; } #s18-rip { left: 560px; top: 1580px; }
    #s18-glow { left: 90px; top: 520px; width: 900px; height: 900px; border-radius: 50%; background: radial-gradient(circle, rgba(19,96,82,.9), transparent 68%); }
""", f"""
      <div class="row t-h3" style="top:240px"><span class="mask"><span class="in" id="s18-h1">لو عايز تعرف كل جديد في</span></span></div>
      <div class="row t-h2 op-l" style="top:330px"><span class="mask"><span class="in" id="s18-h2">عالم الذكاء الاصطناعي</span></span></div>
      <div id="s18-glow" class="abs"></div>
      {hossam("s18-hs", 170, 560, 740, "assets/images/hossam_grey.png")}
      <div id="s18-plate" class="abs"><div id="s18-nm" class="t-h3">حسام الدين حسن</div><div id="s18-en" class="t-label" style="color:var(--lime)">HOSSAMUDIN HASSAN · AI</div></div>
      <div id="s18-btn" class="op-btn">{ic("person", 44, "#fff")} اعمل فولو</div>
      <div id="s18-btn2" class="op-btn on">{ic("check", 44, "var(--lime)")} متابِع</div>
      <div id="s18-rip" class="ripple"></div>
      <svg id="s18-cur" class="cursor"><use href="#i-cursor" /></svg>
""", """
      fx.maskUp("#s18-h1", 90.8); fx.maskUp("#s18-h2", 91.95);
      tl.fromTo("#s18-glow", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.8, ease: "power2.out" }, 90.7);
      tl.fromTo("#s18-hs", { opacity: 0, y: 260 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, 90.8);
      fx.pop("#s18-btn", 92.6, { from: 0.4 });
      tl.fromTo("#s18-plate", { opacity: 0, y: 60, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 93.7);
      fx.hide("#s18-btn2");
      tl.fromTo("#s18-cur", { opacity: 0, x: 200, y: 160 }, { opacity: 1, x: 0, y: 0, duration: 0.45, ease: "power3.out" }, 93.9);
      fx.click("#s18-cur", 94.5, "#s18-btn", "#s18-rip");
      tl.to("#s18-btn", { opacity: 0, duration: 0.1 }, 94.6);
      tl.to("#s18-btn2", { opacity: 1, duration: 0.1 }, 94.6);
""", blob=("#136052", 540, 1000), push=1.02, exit_t=95.66)

print("tip2 scenes written")
