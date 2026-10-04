# Builds the "Vibe Coder hacked in one night" cartoon demos (no voice yet: TEMP subtitles from the script).
#   python projects/vibe-coder-hacked/build_demo.py            -> all parts
#   python projects/vibe-coder-hacked/build_demo.py demo_flat  -> one part
# Then: python pipeline/motion_sync.py vibe-coder-hacked --part <part>
# Times are GLOBAL seconds of the script timing (Hook 0-4, ... CTA 67-75). When the real voice exists,
# re-time from voice_edit.py words and keep the beat order.
# Kit: kit/cartoon/js/cartoon.js (HF_CHAR rig + HF_PROP props), kit/motion/js/fx.js (HF_SCENE helpers).
import json
import re
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent
W, H = 1080, 1920

TPL = """<!doctype html>
<html lang="ar"><head><meta charset="UTF-8" /></head><body>
<template id="{id}-template">
  <style>
{css}
  </style>
  <div id="{id}" data-composition-id="{id}" data-width="{W}" data-height="{H}" data-duration="{dur}">
{body}
  </div>
  <script>
    (function () {{
      const fx = window.HF_SCENE({start});
      const {{ tl, Q }} = fx;
{js}
      window.__timelines["{id}"] = tl.real;
    }})();
  </script>
</template></body></html>
"""

# shared classes (each scene repeats them: a sub-composition only sees its own <style> + base.css)
BASE_CSS = """
    .cv-abs { position: absolute; }
    .cv-head { position: absolute; left: 50px; right: 50px; text-align: center; font-weight: 900; line-height: 1.25; white-space: nowrap; }
    .cv-chip { position: absolute; display: inline-flex; align-items: center; gap: 16px; height: 96px; padding: 0 40px; border-radius: 48px;
      font-size: 46px; font-weight: 900; white-space: nowrap; box-shadow: 0 16px 34px rgba(0,0,0,.35); }
    .cv-lat { font-family: var(--font-en); direction: ltr; unicode-bidi: isolate; }
    .cv-tag { position: absolute; font-family: var(--font-en); font-weight: 900; letter-spacing: .18em; font-size: 30px; direction: ltr; white-space: nowrap; }
    .cv-card { position: absolute; border-radius: 30px; background: #fbfbf7; color: #0d0d0d; box-shadow: 0 24px 50px rgba(0,0,0,.4); overflow: hidden; }
    .cv-floor { position: absolute; left: 0; right: 0; bottom: 0; }
    .cv-mount { position: absolute; }
"""


def lat(text):
    """Wrap Latin runs (AI, GitHub, 48 ...) in .cv-lat spans so RTL bidi never scrambles them."""
    return re.sub(r"([A-Za-z0-9$][A-Za-z0-9 .$'_\-→#/?=:]*[A-Za-z0-9$]|[A-Za-z0-9$])", r'<span class="cv-lat">\1</span>', text)


def scene(sid, start, dur, css, body, js, beat=""):
    return {"id": sid, "start": start, "duration": dur, "beat": beat,
            "html": TPL.format(id=sid, W=W, H=H, dur=dur, start=start, css=BASE_CSS + css, body=body, js=js)}


def ch_mount(x, feet_y, h):
    """CSS box for a character mount: x = left, feet_y = where the feet stand, h = mount height (w = h*300/330)."""
    w = round(h * 300 / 330)
    return f"left:{x}px; top:{feet_y - h}px; width:{w}px; height:{h}px;"


# ======================================================================== S1 · Hook (0 - 4.2)
def s1(skin="flat", start=0.0, dur=4.2):
    """Night room, Karim at the laptop, the light turns red, freeze on his shocked face."""
    p = "s1"
    light, noir = skin == "line", skin == "noir"
    css = f"""
    #{p}-wall {{ position:absolute; inset:0; background:{"linear-gradient(180deg,#f6f4ea 0%,#eceee0 100%)" if light else "radial-gradient(ellipse 80% 60% at 50% 45%, #10352f 0%, #07221e 55%, #041614 100%)"}; }}
    #{p}-win {{ position:absolute; left:90px; top:520px; width:260px; height:330px; border-radius:24px; background:{"#cfe3a0" if light else "#041614"};
      border:{"10px solid #0d0d0d" if light else "14px solid #1d3a34"}; overflow:hidden; }}
    #{p}-moon {{ position:absolute; left:100px; top:40px; width:130px; height:130px; }}
    #{p}-shelf {{ position:absolute; right:90px; top:620px; width:230px; height:16px; border-radius:8px; background:{"#0d0d0d" if light else "#1d3a34"}; }}
    #{p}-glow {{ position:absolute; left:140px; top:560px; width:800px; height:800px; border-radius:50%;
      background: radial-gradient(circle, rgba(255,236,92,.45) 0%, rgba(255,236,92,.14) 40%, transparent 70%); }}
    #{p}-redg {{ position:absolute; left:40px; top:460px; width:1000px; height:1000px; border-radius:50%;
      background: radial-gradient(circle, rgba(217,58,43,.75) 0%, rgba(217,58,43,.25) 45%, transparent 72%); opacity:0; }}
    #{p}-k {{ {ch_mount(160, 1560, 830)} }}
    #{p}-desk {{ position:absolute; left:0; right:0; top:1300px; bottom:0; background:{"#136052" if light else "#0d1f1b"};
      border-top:{"10px solid #0d0d0d" if light else "8px solid #1d3a34"}; }}
    #{p}-lid {{ position:absolute; left:250px; top:1060px; width:580px; height:300px; border-radius:24px 24px 8px 8px;
      background:{"#fbfbf7" if light else "#1d2a27"}; border:{"8px solid #0d0d0d" if light else "4px solid #2f4741"}; }}
    #{p}-logo {{ position:absolute; left:255px; top:115px; width:70px; height:70px; border-radius:50%; background:#b3ce65; opacity:.85; }}
    #{p}-mug {{ position:absolute; left:110px; top:1250px; width:110px; height:120px; border-radius:12px 12px 26px 26px; background:{"#ff5a33" if not noir else "#1d2a27"};
      border:{"8px solid #0d0d0d" if light else "0"}; }}
    #{p}-note {{ position:absolute; left:880px; top:1270px; width:120px; height:110px; background:#ffec5c; transform:rotate(-8deg); border-radius:6px; }}
    #{p}-warn {{ position:absolute; left:760px; top:640px; width:220px; height:200px; }}
    #{p}-red {{ position:absolute; inset:0; background:#d93a2b; opacity:0; mix-blend-mode:{"multiply" if light else "screen"}; }}
    #{p}-t1 {{ top:170px; font-size:92px; color:{"#136052" if light else "#b3ce65"}; }}
    #{p}-t2 {{ top:330px; font-size:84px; }}
    #{p}-band {{ position:absolute; left:0; right:0; top:1390px; height:150px; background:#d93a2b; display:flex; align-items:center; justify-content:center;
      color:#fff; font-size:64px; letter-spacing:.32em; opacity:0; }}
    #{p}-frame {{ position:absolute; inset:26px; border:12px solid #fbfbf7; border-radius:30px; opacity:0; }}
    #{p}-stars i {{ position:absolute; width:8px; height:8px; border-radius:50%; background:#fff6b8; }}
"""
    stars = "".join(f'<i style="left:{x}px;top:{y}px;opacity:{o}"></i>' for x, y, o in
                    [(30, 210, .8), (190, 230, .6), (80, 270, .5), (200, 120, .7), (24, 50, .5)])
    body = f"""
    <div id="{p}-wall"></div>
    <div id="{p}-cam" class="cam">
      <div id="{p}-win"><div id="{p}-stars">{stars}</div><div id="{p}-moon"></div></div>
      <div id="{p}-shelf"></div>
      <div id="{p}-glow"></div>
      <div id="{p}-redg"></div>
      <div id="{p}-k" class="cv-mount"></div>
      <div id="{p}-desk"></div>
      <div id="{p}-lid"><div id="{p}-logo"></div></div>
      <div id="{p}-mug"></div><div id="{p}-note"></div>
      <div id="{p}-warn" class="cv-abs"></div>
    </div>
    <div id="{p}-red"></div>
    <div id="{p}-band" class="cv-lat" style="font-weight:900">ALERT</div>
    <div id="{p}-frame"></div>
    <div id="{p}-t1" class="cv-head">{lat("بُني في 48 ساعة")}</div>
    <div id="{p}-t2" class="cv-head"><span id="{p}-t2in" style="display:inline-block;background:{"#ffec5c" if light else "#d93a2b"};color:{"#0d0d0d" if light else "#fff"};border:{"8px solid #0d0d0d" if light else "0"};border-radius:26px;padding:14px 40px 18px;line-height:1.3">{lat("اتخترق في 3 دقايق")}</span></div>
"""
    T = lambda x: round(start + x, 3)
    js = f"""
      Q("#{p}-moon").innerHTML = HF_PROP.moon("{p}m");
      Q("#{p}-warn").innerHTML = '<svg viewBox="0 0 200 180" width="100%" height="100%"><path d="M100 8 L192 170 L8 170 Z" fill="#ffec5c" stroke="#0d0d0d" stroke-width="10" stroke-linejoin="round"/><rect x="90" y="58" width="20" height="62" rx="9" fill="#0d0d0d"/><circle cx="100" cy="142" r="12" fill="#0d0d0d"/></svg>';
      const k = HF_CHAR(fx, "#{p}-k", {{ id: "{p}k", look: "karim", skin: "{skin}", pose: "type", face: "smile" }});
      for (let i = 0; i < 8; i++) k.pose({T(0.15)} + i * 0.2, i % 2 ? {{ aL: [24, -70], aR: [-24, 86], hd: 4 }} : {{ aL: [24, -86], aR: [-24, 70], hd: 4 }}, 0.18, "sine.inOut");
      k.blink({T(0.9)});
      fx.breathe("#{p}-glow", {T(0)}, 1.8, 0.04, 0.9);
      fx.rise("#{p}-t1", {T(0.2)}, {{ y: 40 }});
      // the light turns red
      k.face({T(1.9)}, "shock").pose({T(1.95)}, "shock", 0.25, "back.out(2.4)").hop({T(1.95)}, 26, 0.36);
      tl.fromTo("#{p}-glow", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.15, immediateRender: false }}, {T(1.9)});
      tl.fromTo("#{p}-redg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12 }}, {T(1.9)});
      for (let i = 0; i < 4; i++) tl.fromTo("#{p}-red", {{ opacity: 0 }}, {{ opacity: 0.3, duration: 0.14, yoyo: true, repeat: 1, immediateRender: false }}, {T(1.9)} + i * 0.36);
      fx.pop("#{p}-warn", {T(1.95)}, {{ from: 0.2, e: "back.out(3)" }});
      fx.shake("#{p}-cam", {T(1.95)}, 16, 8);
      tl.fromTo("#{p}-band", {{ opacity: 0, scaleY: 0 }}, {{ opacity: 1, scaleY: 1, duration: 0.2, ease: "power3.out" }}, {T(2.05)});
      fx.stamp("#{p}-t2in", {T(2.45)}, "#{p}-cam");
      // freeze-frame on the shocked face
      tl.fromTo("#{p}-cam", {{ scale: 1, transformOrigin: "50% 42%" }}, {{ scale: 1.5, duration: 0.18, ease: "expo.out", immediateRender: false }}, {T(3.05)});
      tl.fromTo("#{p}-cam", {{ filter: "grayscale(0) contrast(1)" }}, {{ filter: "grayscale(0.75) contrast(1.15)", duration: 0.12, immediateRender: false }}, {T(3.05)});
      tl.fromTo("#{p}-frame", {{ opacity: 0, scale: 1.06 }}, {{ opacity: 1, scale: 1, duration: 0.16 }}, {T(3.05)});
"""
    return scene(p, start, dur, css, body, js, "hook: built in 48h, hacked in 3 min")


# ======================================================================== S2 · Start (4.2 - 16)
def s2(start=4.2, dur=11.8):
    p = "s2"
    css = f"""
    #{p}-sky {{ position:absolute; inset:0; background: radial-gradient(ellipse 90% 70% at 50% 40%, #1a7564 0%, #136052 50%, #0f4f44 100%); }}
    #{p}-floor {{ top:1430px; background: linear-gradient(180deg,#0d2b23,#07221e); }}
    #{p}-tag {{ left:0; right:0; top:200px; text-align:center; color:#ffec5c; font-size:34px; }}
    #{p}-h1 {{ top:260px; font-size:84px; color:#fff; }}
    #{p}-k {{ {ch_mount(40, 1450, 700)} }}
    #{p}-doc {{ {ch_mount(520, 1450, 600)} }}
    #{p}-bub {{ position:absolute; left:330px; top:520px; width:690px; padding:30px 40px; border-radius:40px; background:#fbfbf7; color:#0d0d0d;
      font-size:42px; font-weight:800; line-height:1.5; box-shadow:0 18px 40px rgba(0,0,0,.35); text-align:right; }}
    #{p}-bub:after {{ content:""; position:absolute; left:60px; bottom:-34px; border:22px solid transparent; border-top:36px solid #fbfbf7; }}
    #{p}-house {{ position:absolute; left:470px; top:840px; width:560px; height:560px; }}
    #{p}-pa {{ left:0; right:0; top:420px; text-align:center; font-size:58px; color:#b3ce65; }}
    #{p}-day {{ left:600px; top:560px; background:#ffec5c; color:#0d0d0d; }}
    #{p}-claps i {{ position:absolute; width:16px; height:16px; border-radius:50%; background:#ffec5c; }}
"""
    body = f"""
    <div id="{p}-sky"></div>
    <div id="{p}-cam" class="cam">
      <div id="{p}-floor" class="cv-floor"></div>
      <div id="{p}-house"></div>
      <div id="{p}-doc" class="cv-mount"></div>
      <div id="{p}-k" class="cv-mount"></div>
      <div id="{p}-bub">{lat("«اعملي أبلكيشن حجوزات للعيادة… بتسجيل دخول ودفع»")}</div>
      <div id="{p}-day" class="cv-chip">يوم <span id="{p}-dn" class="cv-lat">1</span></div>
    </div>
    <div id="{p}-tag" class="cv-tag">VIBE CODER</div>
    <div id="{p}-h1" class="cv-head">كريم مش مبرمج</div>
    <div id="{p}-pa" class="cv-tag" style="letter-spacing:.06em">PROMPT → APP</div>
"""
    T = lambda x: round(x, 3)
    blocks = ",".join(f'"#{p}h-b{i}"' for i in range(12))
    js = f"""
      Q("#{p}-house").innerHTML = HF_PROP.house("{p}h");
      const k = HF_CHAR(fx, "#{p}-k", {{ id: "{p}k", look: "karim", pose: "idle", face: "smile", cape: true }});
      const d = HF_CHAR(fx, "#{p}-doc", {{ id: "{p}d", look: "doctor", pose: "idle", face: "smile" }});
      fx.hide("#{p}-doc"); fx.hide("[id^='{p}h-']");
      k.blinks({T(4.2)}, {T(16)}, 2.9);
      fx.rise("#{p}-tag", {T(4.35)}, {{ y: 20, b: 0 }});
      fx.rise("#{p}-h1", {T(4.5)}, {{ y: 50 }});
      k.pose({T(4.6)}, "shrug").face({T(4.6)}, "grin").pose({T(6.0)}, "idle");
      // the prompt: Karim talks, the bubble pops
      k.pose({T(7.0)}, "point").face({T(7.0)}, "smile").talk({T(7.0)}, {T(9.4)});
      fx.pop("#{p}-bub", {T(7.05)}, {{ from: 0.4 }});
      fx.out("#{p}-tag, #{p}-h1", {T(9.45)}, {{ y: -30 }});
      // words -> blocks: the bubble collapses into the house site, blocks drop in row by row
      tl.to("#{p}-bub", {{ scale: 0.1, x: 260, y: 520, opacity: 0, duration: 0.45, ease: "power3.in" }}, {T(9.6)});
      fx.rise("#{p}-pa", {T(9.8)}, {{ y: 20 }});
      tl.fromTo([{blocks}], {{ opacity: 0, y: -420 }}, {{ opacity: 1, y: 0, duration: 0.42, ease: "bounce.out", stagger: 0.14 }}, {T(10.0)});
      tl.fromTo(["#{p}h-roof", "#{p}h-chim"], {{ opacity: 0, y: -300 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.6)", stagger: 0.1 }}, {T(11.8)});
      tl.fromTo(["#{p}h-door", "#{p}h-win", "#{p}h-bwin", "#{p}h-sash"], {{ opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.08 }}, {T(12.3)});
      fx.hide("#{p}h-blocks"); tl.fromTo("#{p}h-blocks", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01, immediateRender: false }}, {T(10.0)});
      k.pose({T(10.0)}, "think").face({T(10.0)}, "happy");
      // day counter
      fx.pop("#{p}-day", {T(10.5)}, {{ from: 0.3 }});
      tl.set("#{p}-dn", {{ textContent: "2" }}, {T(11.9)});
      fx.pop("#{p}-day", {T(11.9)}, {{ from: 0.8, d: 0.25 }});
      fx.out("#{p}-day, #{p}-pa", {T(12.6)});
      // the doctor friend arrives, claps; Karim becomes superman
      tl.fromTo("#{p}-doc", {{ opacity: 0, x: 420 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }}, {T(12.7)});
      d.walk({T(12.7)}, {T(13.3)});
      d.face({T(13.3)}, "grin").clap({T(13.4)}, {T(15.6)});
      tl.to("#{p}-house", {{ x: 130, y: -120, scale: 0.72, duration: 0.6, ease: "power2.inOut" }}, {T(12.7)});
      k.cape({T(14.0)}, {T(15.9)}).pose({T(14.0)}, "hero", 0.3).face({T(14.0)}, "grin").hop({T(14.0)}, 46);
      tl.fromTo("#{p}-k", {{ x: 0 }}, {{ x: 30, duration: 0.5, ease: "power2.out" }}, {T(12.7)});
"""
    return scene(p, start, dur, css, body, js, "Karim the vibe coder builds the app in 2 days")


# ======================================================================== S3 · What nobody saw (16 - 30)
def s3(start=16.0, dur=14.0):
    p = "s3"
    css = f"""
    #{p}-sky {{ position:absolute; inset:0; background: radial-gradient(ellipse 90% 70% at 50% 40%, #10352f 0%, #07221e 60%, #041614 100%); }}
    #{p}-floor {{ top:1340px; background: linear-gradient(180deg,#0d2b23,#041614); }}
    #{p}-h1 {{ top:170px; font-size:84px; color:#ffec5c; }}
    #{p}-world {{ position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin: 50% 60%; }}
    #{p}-house {{ position:absolute; left:190px; top:640px; width:700px; height:700px; }}
    #{p}-key {{ position:absolute; left:546px; top:1040px; width:150px; height:66px; transform-origin: 20px 50%; }}
    #{p}-code {{ left:70px; top:400px; width:940px; padding:34px 40px; direction:ltr; font-family:var(--font-en); font-size:34px; line-height:1.6; }}
    #{p}-code .k {{ background:#ff5a33; color:#fff; border-radius:10px; padding:2px 10px; }}
    #{p}-gh {{ left:0; right:0; top:690px; text-align:center; color:#ffec5c; font-size:30px; }}
    #{p}-url {{ left:90px; top:400px; width:900px; height:300px; direction:ltr; }}
    #{p}-url .bar {{ height:84px; background:#eceee0; display:flex; align-items:center; padding:0 30px; font-family:var(--font-en); font-weight:800; font-size:36px; color:#2f4741; }}
    #{p}-url .row {{ display:flex; align-items:center; gap:30px; padding:30px 36px; }}
    #{p}-url .av {{ width:110px; height:110px; border-radius:50%; flex:none; }}
    #{p}-url .ln {{ height:22px; border-radius:11px; background:#c9cfc0; margin:14px 0; }}
    #{p}-id {{ color:#ff5a33; }}
    #{p}-k {{ {ch_mount(-10, 1500, 520)} }}
    #{p}-flash {{ position:absolute; left:200px; top:1010px; width:120px; height:120px; border-radius:50%; background:#fff; opacity:0; filter:blur(8px); }}
    #{p}-c1 {{ right:60px; top:410px; background:#ffec5c; color:#0d0d0d; }}
    #{p}-c2 {{ right:60px; top:530px; background:#ff5a33; color:#fff; }}
    .{p}-ic {{ width:58px; height:58px; display:block; }}
"""
    body = f"""
    <div id="{p}-sky"></div>
    <div id="{p}-cam" class="cam">
      <div id="{p}-floor" class="cv-floor"></div>
      <div id="{p}-world">
        <div id="{p}-house"></div>
        <div id="{p}-key"></div>
      </div>
      <div id="{p}-k" class="cv-mount"></div>
      <div id="{p}-flash"></div>
    </div>
    <div id="{p}-h1" class="cv-head">بس اللي كريم ماشافوش…</div>
    <div id="{p}-code" class="cv-card"><span style="color:#5a6b62">// payments.js · written by AI</span><br/>const PAY_KEY = <span id="{p}-kv" class="k">"sk_live_8f2…Q9x"</span>;</div>
    <div id="{p}-gh" class="cv-tag">↑ PUSHED TO GITHUB · PUBLIC</div>
    <div id="{p}-url" class="cv-card"><div class="bar">clinic-app.com/patient?id=<span id="{p}-id">41</span></div>
      <div class="row"><div id="{p}-av" class="av" style="background:#b3ce65"></div><div style="flex:1"><div class="ln" style="width:70%"></div><div class="ln" style="width:92%"></div><div class="ln" style="width:55%"></div></div></div></div>
    <div id="{p}-c1" class="cv-chip"><svg class="{p}-ic" viewBox="0 0 160 70"><circle cx="36" cy="35" r="24" fill="none" stroke="#0d0d0d" stroke-width="12"/><path d="M60 29 L150 29 L150 41 L136 41 L136 53 L124 53 L124 41 L60 41 Z" fill="#0d0d0d"/></svg>مفتاح مكشوف</div>
    <div id="{p}-c2" class="cv-chip"><svg class="{p}-ic" viewBox="0 0 64 64"><rect x="14" y="6" width="36" height="54" rx="4" fill="none" stroke="#fff" stroke-width="6"/><path d="M14 6 L40 14 L40 60 L14 60 Z" fill="#fff"/></svg>باب مفتوح</div>
"""
    T = lambda x: round(x, 3)
    js = f"""
      Q("#{p}-house").innerHTML = HF_PROP.house("{p}h");
      Q("#{p}-key").innerHTML = HF_PROP.key("{p}kk");
      const k = HF_CHAR(fx, "#{p}-k", {{ id: "{p}k", look: "karim", pose: "selfie", face: "grin", prop: "phone" }});
      fx.hide("#{p}-k"); fx.hide("#{p}-key");
      fx.rise("#{p}-h1", {T(16.15)}, {{ y: 40 }});
      fx.pushIn("#{p}-world", {T(16.0)}, 3.0, 1.06);
      // the key in the code -> pushed to GitHub -> hangs on the front door
      fx.rise("#{p}-code", {T(17.9)}, {{ y: 60 }});
      tl.fromTo("#{p}-kv", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {T(18.6)});
      fx.rise("#{p}-gh", {T(19.6)}, {{ y: 20, b: 0 }});
      fx.out("#{p}-code, #{p}-gh", {T(21.2)}, {{ y: -40 }});
      tl.fromTo("#{p}-key", {{ opacity: 0, x: -200, y: -560, rotation: -200, scale: 1.6 }}, {{ opacity: 1, x: 0, y: 0, rotation: 90, scale: 1, duration: 0.7, ease: "power3.out" }}, {T(21.3)});
      tl.fromTo("#{p}-key", {{ rotation: 90 }}, {{ rotation: 72, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 7, immediateRender: false }}, {T(22.0)});
      // the data page: change one number, see another patient
      fx.rise("#{p}-url", {T(22.5)}, {{ y: 60 }});
      tl.fromTo("#{p}h-sash", {{ scaleX: 1, transformOrigin: "100% 50%" }}, {{ scaleX: 0.18, duration: 0.5, ease: "back.out(1.5)" }}, {T(22.6)});
      tl.set("#{p}-id", {{ textContent: "42" }}, {T(24.2)});
      tl.fromTo("#{p}-id", {{ scale: 1.6 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }}, {T(24.2)});
      tl.fromTo("#{p}-av", {{ backgroundColor: "#b3ce65" }}, {{ backgroundColor: "#ff5a33", duration: 0.2, immediateRender: false }}, {T(24.25)});
      tl.set("#{p}-id", {{ textContent: "43" }}, {T(25.2)});
      tl.fromTo("#{p}-av", {{ backgroundColor: "#ff5a33" }}, {{ backgroundColor: "#ffec5c", duration: 0.2, immediateRender: false }}, {T(25.25)});
      fx.out("#{p}-url, #{p}-h1", {T(26.1)}, {{ y: -40 }});
      // Karim takes a selfie with the house, oblivious
      tl.to("#{p}-world", {{ x: 150, scale: 0.86, duration: 0.6, ease: "power2.inOut" }}, {T(26.1)});
      tl.fromTo("#{p}-k", {{ opacity: 0, x: -360 }}, {{ opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }}, {T(26.3)});
      k.walk({T(26.3)}, {T(26.85)}).face({T(26.9)}, "grin");
      tl.fromTo("#{p}-flash", {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 2.2, duration: 0.12, yoyo: true, repeat: 1, immediateRender: false }}, {T(27.4)});
      k.hop({T(28.6)}, 20);
      fx.pop("#{p}-c1", {T(27.2)}, {{ from: 0.4 }});
      fx.pop("#{p}-c2", {T(28.0)}, {{ from: 0.4 }});
"""
    return scene(p, start, dur, css, body, js, "exposed key + open door; Karim takes a selfie")


# ======================================================================== S4 · The breach (30 - 42)
def s4(start=30.0, dur=12.0):
    p = "s4"
    rows = ["README.md", "index.html", "login.js", "src/payments.js", "styles.css", "package.json"]
    css = f"""
    #{p}-sky {{ position:absolute; inset:0; background: radial-gradient(ellipse 90% 70% at 50% 40%, #0d2e29 0%, #041614 70%); }}
    #{p}-morn {{ position:absolute; inset:0; background: linear-gradient(180deg, #ffec5c 0%, #f6f4ea 45%, #eceee0 100%); opacity:0; }}
    #{p}-clock {{ position:absolute; left:340px; top:300px; width:400px; height:400px; }}
    #{p}-am {{ left:0; right:0; top:730px; text-align:center; font-size:96px; color:#ffec5c; letter-spacing:.08em; }}
    #{p}-list {{ left:250px; top:600px; width:760px; direction:ltr; }}
    #{p}-list .r {{ height:104px; display:flex; align-items:center; gap:22px; padding:0 34px; border-bottom:2px solid #e3e6d6;
      font-family:var(--font-en); font-weight:800; font-size:34px; color:#2f4741; }}
    #{p}-list .r i {{ width:34px; height:40px; border-radius:6px; background:#c9cfc0; display:block; }}
    #{p}-list .hd {{ height:90px; background:#0d2b23; color:#b3ce65; display:flex; align-items:center; padding:0 34px; font-family:var(--font-en); font-weight:900; font-size:30px; letter-spacing:.14em; }}
    #{p}-hit {{ position:absolute; left:0; right:0; top:{90 + 3 * 104}px; height:104px; background:rgba(255,90,51,.25); border:5px solid #ff5a33; opacity:0; }}
    #{p}-bot {{ position:absolute; left:20px; top:560px; width:300px; height:360px; }}
    #{p}-key {{ position:absolute; left:820px; top:{600 + 90 + 3 * 104 + 18}px; width:150px; height:66px; }}
    #{p}-ha {{ left:40px; top:470px; color:#ff5a33; font-size:64px; transform:rotate(-8deg); }}
    #{p}-k {{ {ch_mount(250, 1560, 640)} }}
    #{p}-msg {{ left:70px; top:330px; width:940px; padding:34px 40px; text-align:right; }}
    #{p}-msg .who {{ display:flex; align-items:center; gap:20px; font-size:36px; font-weight:900; color:#136052; margin-bottom:16px; }}
    #{p}-msg .who i {{ width:70px; height:70px; border-radius:50%; background:#136052; display:block; }}
    #{p}-msg .tx {{ font-size:44px; font-weight:800; line-height:1.5; }}
    #{p}-inv {{ left:610px; top:640px; width:400px; padding:30px; transform:rotate(6deg); text-align:center; }}
    #{p}-inv b {{ display:block; font-size:42px; line-height:1.3; color:#2f4741; }}
    #{p}-inv .amt {{ font-size:84px; line-height:1.15; margin:10px 0; font-weight:900; color:#d93a2b; font-family:var(--font-en); }}
    #{p}-ring i {{ position:absolute; width:160px; height:160px; border-radius:50%; border:6px solid #d93a2b; opacity:0; }}
"""
    rows_html = "".join(f'<div class="r"><i></i>{r}</div>' for r in rows)
    body = f"""
    <div id="{p}-sky"></div>
    <div id="{p}-morn"></div>
    <div id="{p}-cam" class="cam">
      <div id="{p}-clock"></div>
      <div id="{p}-list" class="cv-card"><div class="hd">KARIM / CLINIC-APP · PUBLIC</div>{rows_html}<div id="{p}-hit"></div></div>
      <div id="{p}-key"></div>
      <div id="{p}-bot"></div>
      <div id="{p}-k" class="cv-mount"></div>
      <div id="{p}-ring"><i style="left:590px;top:1080px"></i></div>
    </div>
    <div id="{p}-am" class="cv-tag">03:00 AM</div>
    <div id="{p}-ha" class="cv-tag">HA HA!</div>
    <div id="{p}-msg" class="cv-card"><div class="who"><i></i>صاحبي الدكتور</div><div class="tx">«كريم، المرضى بيكلموني إن بياناتهم اتسربت…»</div></div>
    <div id="{p}-inv" class="cv-card"><b data-layout-allow-overlap>فاتورة</b><div class="amt" data-layout-allow-overlap>$$$$</div><b data-layout-allow-overlap>آلاف الدولارات</b></div>
"""
    T = lambda x: round(x, 3)
    js = f"""
      Q("#{p}-clock").innerHTML = HF_PROP.clock("{p}c");
      Q("#{p}-bot").innerHTML = HF_PROP.bot("{p}b", {{ variant: "scanner" }});
      Q("#{p}-key").innerHTML = HF_PROP.key("{p}kk");
      const k = HF_CHAR(fx, "#{p}-k", {{ id: "{p}k", look: "karim", pose: "phone", face: "neutral", prop: "phone" }});
      fx.hide("#{p}-k"); fx.hide("#{p}-list"); fx.hide("#{p}-bot"); fx.hide("#{p}-key");
      // 3:00 AM
      fx.pop("#{p}-clock", {T(30.1)}, {{ from: 0.5 }});
      tl.fromTo("#{p}c-mh", {{ rotation: -300, svgOrigin: "110 110" }}, {{ rotation: 0, svgOrigin: "110 110", duration: 1.0, ease: "power3.out" }}, {T(30.15)});
      tl.fromTo("#{p}c-hh", {{ rotation: 0, svgOrigin: "110 110" }}, {{ rotation: 90, svgOrigin: "110 110", duration: 1.0, ease: "power3.out" }}, {T(30.15)});
      fx.rise("#{p}-am", {T(30.6)}, {{ y: 30 }});
      tl.to("#{p}-clock", {{ x: 330, y: -150, scale: 0.42, duration: 0.5, ease: "power3.inOut" }}, {T(31.3)});
      fx.out("#{p}-am", {T(31.3)});
      // the bot scans the public repo and finds the key
      tl.fromTo("#{p}-list", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }}, {T(31.4)});
      tl.fromTo("#{p}-bot", {{ opacity: 0, x: -300 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out", immediateRender: false }}, {T(31.6)});
      tl.fromTo("#{p}-bot", {{ y: 0 }}, {{ y: 312, duration: 1.6, ease: "steps(4)", immediateRender: false }}, {T(32.0)});
      tl.fromTo("#{p}b-arm", {{ rotation: 0, svgOrigin: "46 -110" }}, {{ rotation: -14, svgOrigin: "46 -110", duration: 0.2, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {T(32.0)});
      tl.fromTo("#{p}-hit", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15, yoyo: true, repeat: 3, immediateRender: false }}, {T(33.5)});
      tl.fromTo("#{p}-key", {{ opacity: 0, scale: 0.2 }}, {{ opacity: 1, scale: 1.25, duration: 0.35, ease: "back.out(3)", immediateRender: false }}, {T(33.6)});
      tl.fromTo("#{p}-bot", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.12, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, {T(34.0)});
      fx.stamp("#{p}-ha", {T(34.0)});
      tl.to("#{p}-key", {{ x: -560, y: -60, scale: 0.8, duration: 0.45, ease: "power3.in" }}, {T(34.5)});
      // morning: phone rings
      tl.fromTo("#{p}-morn", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power2.inOut" }}, {T(35.0)});
      fx.out("#{p}-list, #{p}-bot, #{p}-key, #{p}-ha, #{p}-clock", {T(35.0)}, {{ d: 0.35 }});
      tl.fromTo("#{p}-k", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }}, {T(35.3)});
      tl.fromTo("#{p}-k", {{ rotation: -2 }}, {{ rotation: 2, duration: 0.07, yoyo: true, repeat: 9, ease: "none", immediateRender: false }}, {T(35.8)});
      tl.fromTo("#{p}-ring i", {{ opacity: 0.9, scale: 0.4 }}, {{ opacity: 0, scale: 1.8, duration: 0.6, repeat: 2, ease: "power2.out", immediateRender: false }}, {T(35.8)});
      fx.hide("#{p}-ring i");
      k.blink({T(35.6)}).face({T(36.4)}, "shock").pose({T(36.4)}, {{ aL: [130, 30], aR: [-26, -150], hd: 0 }}, 0.25);
      fx.rise("#{p}-msg", {T(36.3)}, {{ y: -60 }});
      tl.fromTo("#{p}-inv", {{ opacity: 0, x: 500, rotation: 30 }}, {{ opacity: 1, x: 0, rotation: 6, duration: 0.5, ease: "back.out(1.6)", immediateRender: false }}, {T(38.9)});
      fx.hide("#{p}-inv");
      k.face({T(39.1)}, "worried").hop({T(39.1)}, 18);
"""
    return scene(p, start, dur, css, body, js, "3 AM: a bot finds the key; morning: leak + invoice")


# ======================================================================== S5 · The lesson (42 - 52)
def s5(start=42.0, dur=10.0):
    p = "s5"
    css = f"""
    #{p}-sky {{ position:absolute; inset:0; background: radial-gradient(ellipse 90% 70% at 50% 40%, #2a3c37 0%, #12201d 70%); }}
    #{p}-floor {{ top:1380px; background: linear-gradient(180deg,#1d2a27,#0d1614); }}
    #{p}-house {{ position:absolute; left:240px; top:620px; width:640px; height:640px; filter: saturate(.45) brightness(.85); }}
    #{p}-crack {{ position:absolute; left:240px; top:620px; width:640px; height:640px; }}
    #{p}-k {{ {ch_mount(60, 1470, 520)} }}
    #{p}-split {{ position:absolute; inset:0; }}
    #{p}-L, #{p}-R {{ position:absolute; top:380px; width:540px; height:1000px; overflow:hidden; }}
    #{p}-L {{ right:0; background:#136052; }}
    #{p}-R {{ left:0; background:#2a1a17; }}
    #{p}-hL, #{p}-hR {{ position:absolute; left:40px; top:240px; width:460px; height:460px; }}
    #{p}-lbL, #{p}-lbR {{ position:absolute; left:0; right:0; top:60px; text-align:center; font-size:30px; }}
    #{p}-vL, #{p}-vR {{ position:absolute; left:0; right:0; top:760px; text-align:center; font-size:70px; font-weight:900; }}
    #{p}-in i {{ position:absolute; display:block; background:#0d0d0d; }}
    #{p}-eq {{ top:200px; font-size:120px; color:#fff; }}
    #{p}-eq .ne {{ color:#ff5a33; }}
"""
    body = f"""
    <div id="{p}-sky"></div>
    <div id="{p}-cam" class="cam">
      <div id="{p}-floor" class="cv-floor"></div>
      <div id="{p}-house"></div>
      <div id="{p}-crack"></div>
      <div id="{p}-k" class="cv-mount"></div>
    </div>
    <div id="{p}-split">
      <div id="{p}-L"><div id="{p}-lbL" class="cv-tag" style="color:#b3ce65">FROM OUTSIDE</div><div id="{p}-hL"></div><div id="{p}-vL" style="color:#b3ce65">شغال ✓</div></div>
      <div id="{p}-R"><div id="{p}-lbR" class="cv-tag" style="color:#ff5a33">FROM INSIDE</div><div id="{p}-hR"></div>
        <div id="{p}-in"><i style="left:210px;top:525px;width:80px;height:130px;background:#ff5a33;opacity:.9"></i><i style="left:340px;top:440px;width:84px;height:70px;background:#ff5a33;opacity:.9"></i></div>
        <div id="{p}-vR" style="color:#ff5a33">آمن؟ ✗</div></div>
    </div>
    <div id="{p}-eq" class="cv-head">شغال <span class="ne">≠</span> آمن</div>
"""
    T = lambda x: round(x, 3)
    js = f"""
      Q("#{p}-house").innerHTML = HF_PROP.house("{p}h", {{ open: true }});
      Q("#{p}-crack").innerHTML = HF_PROP.crack("{p}x");
      Q("#{p}-hL").innerHTML = HF_PROP.house("{p}hl", {{ lit: true }});
      Q("#{p}-hR").innerHTML = HF_PROP.house("{p}hr", {{ open: true }});
      const k = HF_CHAR(fx, "#{p}-k", {{ id: "{p}k", look: "karim", pose: "sitFloor", face: "sad" }});
      k.blinks({T(42)}, {T(45)}, 1.6);
      fx.draw("#{p}x-c1", {T(42.3)}, 0.5); fx.draw("#{p}x-c2", {T(42.6)}, 0.4);
      tl.fromTo("#{p}h-door", {{ rotation: 0, svgOrigin: "186 300" }}, {{ rotation: 14, svgOrigin: "186 300", duration: 0.6, ease: "bounce.out" }}, {T(42.7)});
      fx.shake("#{p}-cam", {T(42.35)}, 10, 6);
      k.pose({T(43.6)}, {{ aL: [40, -120], aR: [-40, 120], lL: 78, lR: -78, hd: 22, by: 90 }}, 0.6, "power2.inOut");
      // split: the same house from outside vs from inside
      tl.fromTo("#{p}-L", {{ xPercent: 100 }}, {{ xPercent: 0, duration: 0.5, ease: "power3.out" }}, {T(45.0)});
      tl.fromTo("#{p}-R", {{ xPercent: -100 }}, {{ xPercent: 0, duration: 0.5, ease: "power3.out" }}, {T(45.1)});
      fx.pop("#{p}-vL", {T(45.8)}, {{ from: 0.5 }});
      fx.pop("#{p}-vR", {T(46.4)}, {{ from: 0.5 }});
      tl.fromTo("#{p}-in i", {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.2, stagger: 0.15 }}, {T(46.0)});
      fx.rise("#{p}-eq", {T(47.2)}, {{ y: -60, s: 1.3 }});
      tl.fromTo("#{p}-eq .ne", {{ scale: 1 }}, {{ scale: 1.35, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {T(47.8)});
"""
    return scene(p, start, dur, css, body, js, "working is not secure")


# ======================================================================== S6 · The fix (52 - 67)
def s6(start=52.0, dur=15.0):
    p = "s6"
    items = ["المفاتيح المكشوفة · حتى في تاريخ GitHub", "المكتبات اللي فيها ثغرات", "الكود", "إعدادات الأمان"]
    steps = ["SCAN", "FIX", "VERIFY", "REPORT"]
    css = f"""
    #{p}-sky {{ position:absolute; inset:0; background: radial-gradient(ellipse 90% 70% at 50% 40%, #1a7564 0%, #136052 55%, #0f4f44 100%); }}
    #{p}-floor {{ top:1400px; background: linear-gradient(180deg,#0d2b23,#07221e); }}
    #{p}-rw {{ position:absolute; inset:0; overflow:hidden; opacity:0; }}
    #{p}-rw i {{ position:absolute; left:-200px; height:10px; width:1500px; background:rgba(255,255,255,.18); display:block; }}
    #{p}-rwi {{ position:absolute; left:380px; top:330px; width:320px; height:200px; }}
    #{p}-rwt {{ left:0; right:0; top:560px; text-align:center; color:#fff; font-size:44px; letter-spacing:.4em; }}
    #{p}-world {{ position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin: 60% 70%; }}
    #{p}-house {{ position:absolute; left:120px; top:720px; width:680px; height:680px; }}
    #{p}-crack {{ position:absolute; left:120px; top:720px; width:680px; height:680px; }}
    #{p}-key {{ position:absolute; left:470px; top:1120px; width:150px; height:66px; transform-origin: 20px 50%; }}
    #{p}-safe {{ position:absolute; left:820px; top:1210px; width:200px; height:200px; }}
    #{p}-cctv {{ position:absolute; left:110px; top:910px; width:190px; height:114px; }}
    #{p}-shield {{ position:absolute; left:400px; top:640px; width:120px; height:138px; }}
    #{p}-bot {{ position:absolute; left:700px; top:1060px; width:280px; height:336px; }}
    #{p}-h1 {{ top:190px; font-size:58px; color:#fff; }}
    #{p}-h2 {{ top:280px; font-size:110px; color:#b3ce65; letter-spacing:.04em; }}
    #{p}-list {{ left:70px; top:380px; width:940px; padding:26px 36px; }}
    #{p}-list .r {{ display:flex; align-items:center; gap:24px; height:82px; font-size:38px; font-weight:800; }}
    #{p}-list .b {{ width:52px; height:52px; border-radius:12px; border:5px solid #136052; flex:none; position:relative; }}
    #{p}-list svg {{ position:absolute; left:-4px; top:-10px; width:60px; height:60px; overflow:visible; }}
    #{p}-pipe {{ position:absolute; left:40px; right:40px; top:400px; display:flex; justify-content:center; gap:12px; direction:ltr; }}
    #{p}-pipe .s {{ height:88px; padding:0 26px; border-radius:44px; display:flex; align-items:center; font-family:var(--font-en); font-weight:900; font-size:32px;
      letter-spacing:.06em; background:rgba(255,255,255,.12); color:#cfe3a0; }}
    #{p}-pipe .a {{ color:#b3ce65; font-family:var(--font-en); font-weight:900; font-size:34px; display:flex; align-items:center; }}
    #{p}-k {{ {ch_mount(-20, 1490, 560)} }}
    #{p}-rep {{ position:absolute; left:170px; top:1190px; width:130px; height:162px; }}
    #{p}-chip {{ right:50px; top:560px; background:#ffec5c; color:#0d0d0d; }}
"""
    lines = "".join(f'<i style="top:{120 + i * 150}px"></i>' for i in range(12))
    list_html = "".join(
        f'<div class="r"><div class="b"><svg viewBox="0 0 60 60"><path id="{p}-ck{i}" d="M8 32 L24 48 L54 10" fill="none" stroke="#ff5a33" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg></div>{lat(t)}</div>'
        for i, t in enumerate(items))
    pipe_html = '<div class="a">→</div>'.join(f'<div id="{p}-p{i}" class="s">{s}</div>' for i, s in enumerate(steps))
    body = f"""
    <div id="{p}-sky"></div>
    <div id="{p}-cam" class="cam">
      <div id="{p}-floor" class="cv-floor"></div>
      <div id="{p}-world">
        <div id="{p}-house"></div><div id="{p}-crack"></div>
        <div id="{p}-key"></div><div id="{p}-safe"></div><div id="{p}-cctv"></div><div id="{p}-shield"></div>
        <div id="{p}-bot"></div>
      </div>
      <div id="{p}-k" class="cv-mount"></div>
      <div id="{p}-rep"></div>
    </div>
    <div id="{p}-rw">{lines}<div id="{p}-rwi"></div><div id="{p}-rwt" class="cv-tag">REWIND</div></div>
    <div id="{p}-h1" class="cv-head">{lat("عشان كده عملت Skill اسمها")}</div>
    <div id="{p}-h2" class="cv-head cv-lat">SECURITY AUDIT</div>
    <div id="{p}-list" class="cv-card">{list_html}</div>
    <div id="{p}-pipe">{pipe_html}</div>
    <div id="{p}-chip" class="cv-chip">تقرير بلغتك · في دقيقتين</div>
"""
    T = lambda x: round(x, 3)
    js = f"""
      Q("#{p}-house").innerHTML = HF_PROP.house("{p}h", {{ open: true }});
      Q("#{p}-crack").innerHTML = HF_PROP.crack("{p}x");
      Q("#{p}-key").innerHTML = HF_PROP.key("{p}kk");
      Q("#{p}-safe").innerHTML = HF_PROP.safe("{p}s");
      Q("#{p}-cctv").innerHTML = HF_PROP.cctv("{p}c");
      Q("#{p}-shield").innerHTML = HF_PROP.shield("{p}sh");
      Q("#{p}-bot").innerHTML = HF_PROP.bot("{p}b", {{ variant: "guard" }});
      Q("#{p}-rep").innerHTML = HF_PROP.paper("{p}r", {{ badge: true, accent: "#b3ce65" }});
      Q("#{p}-rwi").innerHTML = '<svg viewBox="0 0 320 200" width="100%" height="100%"><path d="M150 20 L20 100 L150 180 Z" fill="#fff"/><path d="M300 20 L170 100 L300 180 Z" fill="#fff"/></svg>';
      const k = HF_CHAR(fx, "#{p}-k", {{ id: "{p}k", look: "karim", pose: "idle", face: "neutral" }});
      fx.hide("#{p}-bot"); fx.hide("#{p}-safe"); fx.hide("#{p}-cctv"); fx.hide("#{p}-shield"); fx.hide("#{p}-k"); fx.hide("#{p}-rep");
      // REWIND: stripes + the cracks un-draw
      tl.fromTo("#{p}-rw", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {T(52.0)});
      tl.fromTo("#{p}-rw i", {{ x: 0 }}, {{ x: 900, duration: 1.2, ease: "none", stagger: 0.03 }}, {T(52.0)});
      tl.fromTo("#{p}-rwi", {{ scale: 0.6 }}, {{ scale: 1.1, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {T(52.0)});
      tl.fromTo(["#{p}x-c1", "#{p}x-c2"], {{ strokeDasharray: 1, strokeDashoffset: 0 }}, {{ strokeDashoffset: 1, duration: 1.0, ease: "power2.in" }}, {T(52.1)});
      tl.fromTo("#{p}-cam", {{ filter: "blur(6px) saturate(.4)" }}, {{ filter: "blur(0px) saturate(1)", duration: 1.2, ease: "power2.out" }}, {T(52.0)});
      tl.to("#{p}-rw", {{ opacity: 0, duration: 0.2 }}, {T(53.3)});
      tl.fromTo("#{p}-key", {{ rotation: 90 }}, {{ rotation: 74, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {T(52.0)});
      fx.rise("#{p}-h1", {T(53.4)}, {{ y: 30 }});
      fx.letterDrop("#{p}-h2", {T(53.6)}, {{ st: 0.03 }});
      // the guard (the Skill) walks in
      tl.fromTo("#{p}-bot", {{ opacity: 0, x: 420 }}, {{ opacity: 1, x: 0, duration: 0.8, ease: "power2.out", immediateRender: false }}, {T(53.8)});
      tl.fromTo("#{p}-bot", {{ y: 0 }}, {{ y: -12, duration: 0.16, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, {T(53.8)});
      fx.out("#{p}-h1, #{p}-h2", {T(55.4)}, {{ y: -40 }});
      // checklist synced with the narration
      fx.rise("#{p}-list", {T(55.6)}, {{ y: -40 }});
      [57.0, 58.0, 59.0, 60.0].forEach((t, i) => fx.draw("#{p}-ck" + i, t, 0.35, "power2.out"));
      // the guard's actions: key -> safe, close the window, camera, shield
      fx.pop("#{p}-safe", {T(56.6)}, {{ from: 0.3 }});
      tl.to("#{p}-bot", {{ x: -200, duration: 0.4, ease: "power2.inOut" }}, {T(56.6)});
      tl.to("#{p}-key", {{ x: 400, y: 150, rotation: 0, scale: 0.6, duration: 0.5, ease: "power3.inOut" }}, {T(57.0)});
      tl.to("#{p}-key", {{ opacity: 0, duration: 0.1 }}, {T(57.5)});
      tl.fromTo("#{p}s-door", {{ scaleX: 0.15, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, {T(57.5)});
      tl.fromTo("#{p}s-dial", {{ rotation: 0, svgOrigin: "100 100" }}, {{ rotation: 270, svgOrigin: "100 100", duration: 0.5, ease: "power2.out" }}, {T(57.75)});
      tl.fromTo("#{p}h-sash", {{ scaleX: 0.18, transformOrigin: "100% 50%" }}, {{ scaleX: 1, duration: 0.35, ease: "power3.out" }}, {T(58.0)});
      fx.pop("#{p}-cctv", {T(59.0)}, {{ from: 0.3 }});
      tl.fromTo("#{p}c-led", {{ opacity: 1 }}, {{ opacity: 0.2, duration: 0.3, yoyo: true, repeat: 7, ease: "none" }}, {T(59.3)});
      fx.pop("#{p}-shield", {T(60.0)}, {{ from: 0.2 }}); fx.draw("#{p}sh-ck", {T(60.2)}, 0.35);
      tl.to("#{p}-bot", {{ x: 0, duration: 0.4, ease: "power2.inOut" }}, {T(59.6)});
      // order of work: scan -> fix -> verify -> report; Karim gets the report
      fx.out("#{p}-list", {T(60.75)}, {{ y: -40 }});
      tl.to("#{p}-world", {{ x: 160, scale: 0.84, duration: 0.6, ease: "power2.inOut" }}, {T(60.8)});
      [60.9, 61.9, 62.9, 64.2].forEach((t, i) => {{
        fx.pop("#{p}-p" + i, t, {{ from: 0.5 }});
        tl.fromTo("#{p}-p" + i, {{ backgroundColor: "rgba(255,255,255,0.12)", color: "#cfe3a0" }}, {{ backgroundColor: "#b3ce65", color: "#0d0d0d", duration: 0.2, immediateRender: false }}, t + 0.15);
      }});
      fx.hide("#{p}-pipe .a"); tl.fromTo("#{p}-pipe .a", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, stagger: 1.0, immediateRender: false }}, {T(61.6)});
      tl.fromTo("#{p}-k", {{ opacity: 0, x: -300 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out", immediateRender: false }}, {T(63.6)});
      k.walk({T(63.6)}, {T(64.1)}).pose({T(64.6)}, "hold").face({T(64.9)}, "happy");
      tl.fromTo("#{p}-rep", {{ opacity: 0, x: 520, y: -40, rotation: 40 }}, {{ opacity: 1, x: 0, y: 0, rotation: -6, duration: 0.55, ease: "back.out(1.6)", immediateRender: false }}, {T(64.4)});
      fx.pop("#{p}-chip", {T(65.0)}, {{ from: 0.4 }});
      k.hop({T(65.6)}, 24);
"""
    return scene(p, start, dur, css, body, js, "rewind: the Security Audit skill locks the house")


# ======================================================================== S7 · CTA (67 - 75.6)
def s7(start=67.0, dur=8.6):
    p = "s7"
    css = f"""
    #{p}-sky {{ position:absolute; inset:0; background: radial-gradient(ellipse 90% 70% at 50% 45%, #1f8a75 0%, #136052 55%, #0f4f44 100%); }}
    #{p}-floor {{ top:1400px; background: linear-gradient(180deg,#0d2b23,#07221e); }}
    #{p}-world {{ position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin: 50% 60%; }}
    #{p}-dome {{ position:absolute; left:250px; top:620px; width:760px; height:760px; border-radius:50%; border:10px solid #b3ce65;
      background: radial-gradient(circle, rgba(179,206,101,.08) 40%, rgba(179,206,101,.32) 100%); }}
    #{p}-house {{ position:absolute; left:330px; top:700px; width:600px; height:600px; }}
    #{p}-k {{ {ch_mount(10, 1500, 560)} }}
    #{p}-h1 {{ top:180px; font-size:84px; color:#fff; }}
    #{p}-h2 {{ top:340px; font-size:64px; color:#ffec5c; }}
    #{p}-cm {{ left:70px; top:470px; width:940px; padding:30px 36px; display:flex; align-items:center; gap:26px; direction:rtl; }}
    #{p}-cm i {{ width:96px; height:96px; border-radius:50%; background:#136052; display:block; flex:none; }}
    #{p}-cm .t {{ font-size:36px; font-weight:800; color:#5a6b62; }}
    #{p}-sec {{ font-family:var(--font-en); font-weight:900; font-size:96px; color:#136052; letter-spacing:.06em; direction:ltr; }}
    #{p}-name {{ left:0; right:0; top:900px; text-align:center; font-size:72px; font-weight:900; color:#fff; }}
    #{p}-av {{ position:absolute; left:440px; top:740px; width:200px; height:140px; }}
    #{p}-url {{ left:0; right:0; top:1010px; text-align:center; font-size:42px; color:#b3ce65; letter-spacing:.1em; }}
    #{p}-fol {{ left:400px; top:1110px; background:#ff5a33; color:#fff; height:90px; font-size:42px; }}
"""
    body = f"""
    <div id="{p}-sky"></div>
    <div id="{p}-cam" class="cam">
      <div id="{p}-floor" class="cv-floor"></div>
      <div id="{p}-world"><div id="{p}-dome"></div><div id="{p}-house"></div></div>
      <div id="{p}-k" class="cv-mount"></div>
    </div>
    <div id="{p}-h1" class="cv-head">افحص قبل ما تنشر</div>
    <div id="{p}-h2" class="cv-head">مش بعد ما تتخترق</div>
    <div id="{p}-cm" class="cv-card"><i></i><div><div class="t">اكتب في الكومنتس</div><div id="{p}-sec">SECURITY</div></div></div>
    <div id="{p}-name" class="cv-head" style="position:absolute">حسام الدين حسن</div>
    <div id="{p}-url" class="cv-tag">MAHARAAI.COM</div>
    <div id="{p}-fol" class="cv-chip">+ فولو</div>
"""
    T = lambda x: round(x, 3)
    js = f"""
      Q("#{p}-house").innerHTML = HF_PROP.house("{p}h", {{ lit: true }});
      const k = HF_CHAR(fx, "#{p}-k", {{ id: "{p}k", look: "karim", pose: "idle", face: "happy" }});
      k.blinks({T(67)}, {T(75.6)}, 2.4);
      tl.fromTo("#{p}-dome", {{ scale: 0.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.7, ease: "back.out(1.4)" }}, {T(67.2)});
      fx.breathe("#{p}-dome", {T(68)}, 7.4, 0.025, 1.6);
      fx.rise("#{p}-h1", {T(67.3)}, {{ y: 50 }});
      fx.rise("#{p}-h2", {T(68.7)}, {{ y: 30 }});
      k.pose({T(67.4)}, "wave").face({T(67.4)}, "grin");
      k.pose({T(68.0)}, {{ aR: [-120, -60] }}, 0.25, "sine.inOut").pose({T(68.3)}, "wave", 0.25, "sine.inOut").pose({T(68.6)}, {{ aR: [-120, -60] }}, 0.25, "sine.inOut").pose({T(68.9)}, "idle");
      fx.out("#{p}-h1, #{p}-h2", {T(70.4)}, {{ y: -30 }});
      tl.to("#{p}-world", {{ y: 160, scale: 0.8, duration: 0.6, ease: "power2.inOut" }}, {T(70.5)});
      fx.rise("#{p}-cm", {T(70.6)}, {{ y: 60 }});
      fx.letterDrop("#{p}-sec", {T(71.0)}, {{ st: 0.06 }});
      tl.fromTo("#{p}-sec", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {T(71.8)});
      k.pose({T(71.0)}, "pointUp").face({T(71.0)}, "smile").talk({T(71.0)}, {T(72.6)});
      fx.out("#{p}-world, #{p}-k", {T(72.5)}, {{ y: 120, d: 0.35 }});
      fx.rise("#{p}-name", {T(72.8)}, {{ y: 40 }});
      fx.rise("#{p}-url", {T(73.1)}, {{ y: 20, b: 0 }});
      fx.pop("#{p}-fol", {T(73.6)}, {{ from: 0.3 }});
"""
    return scene(p, start, dur, css, body, js, "CTA: comment SECURITY")


# ======================================================================== TEMP subtitles (until the voice exists)
SUBS = [
    (0.2, 4.1, "كريم بنى أبلكيشن في ويك إند واحد بالـ AI… وخسره في ليلة واحدة."),
    (4.3, 7.0, "كريم مش مبرمج. هو Vibe Coder:"),
    (7.0, 9.6, "بيوصف للـ AI اللي هو عايزه، والـ AI يكتب الكود."),
    (9.6, 12.6, "قاله: «اعملي أبلكيشن حجوزات للعيادة بتاعة صاحبي، بتسجيل دخول ودفع.»"),
    (12.6, 15.9, "وفي يومين الأبلكيشن كان شغال. وصاحبه فرحان، وكريم حاسس إنه سوبرمان."),
    (16.1, 18.0, "بس اللي كريم ماشافوش:"),
    (18.0, 22.4, "الـ AI حط مفتاح الـ API بتاع الدفع جوه الكود نفسه، ورفعه على GitHub."),
    (22.4, 27.0, "وصفحة البيانات ماكانش عليها أي حماية، أي حد يغيّر رقم في اللينك يشوف بيانات مريض تاني."),
    (27.0, 29.9, "كريم ماسألش. والـ AI ماقالش."),
    (30.1, 32.6, "الساعة 3 الفجر. بوت بيلف على GitHub بيدور على مفاتيح."),
    (32.6, 35.0, "لقى المفتاح في أقل من دقايق."),
    (35.0, 41.9, "والصبح: رسالة من صاحبه… وفي فاتورة جاية بآلاف الدولارات."),
    (42.1, 47.0, "المشكلة مش في الـ Vibe Coding. الـ AI بيكتب كود شغال، بس مش لازم يكون كود آمن."),
    (47.0, 51.9, "أنت سألته يبني. ماسألتهوش يأمّن."),
    (52.1, 55.6, "عشان كده عملت Skill اسمها Security Audit."),
    (55.6, 60.8, "تديها لأي Coding Agent على مشروعك، وهي تفحص: المفاتيح، والمكتبات، والكود، وإعدادات الأمان."),
    (60.8, 64.2, "وبعدين تصلّح بالترتيب: المفاتيح الأول، وبعدين الثغرات الخطيرة. وتراجع إن كل حاجة اتصلحت."),
    (64.2, 66.9, "وفي الآخر تديك تقرير بلغتك تقراه في دقيقتين."),
    (67.1, 70.6, "لو بتبني بالـ AI، افحص قبل ما تنشر، مش بعد ما تتخترق."),
    (70.6, 75.4, "اكتبلي SECURITY في الكومنتس وأبعتلك الـ Skill. أنا حسام الدين حسن، اعملي فولو."),
]


def subs(total):
    p = "sub"
    css = f"""
    .{p}-l {{ position:absolute; left:60px; right:60px; bottom:120px; text-align:center; }}
    .{p}-l span.t {{ display:inline-block; max-width:960px; padding:16px 30px; border-radius:22px; background:rgba(4,22,20,.84);
      color:#fff; font-size:40px; font-weight:700; line-height:1.55; }}
"""
    body = "\n".join(f'    <div id="{p}{i}" class="{p}-l" data-layout-allow-overlap><span class="t">{lat(t)}</span></div>' for i, (_, _, t) in enumerate(SUBS))
    js = "\n".join(f'      fx.hide("#{p}{i}"); tl.fromTo("#{p}{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12, immediateRender: false }}, {a}); tl.to("#{p}{i}", {{ opacity: 0, duration: 0.1 }}, {b - 0.1:.2f});'
                   for i, (a, b, _) in enumerate(SUBS))
    sc = scene(p, 0, total, css, body, js, "TEMP subtitles from the script (replace with captions from the real voice)")
    sc["track"] = 3
    return sc


def write_part(part, scenes, cues, chrome=None):
    out = PROJ / part
    (out / "compositions").mkdir(parents=True, exist_ok=True)
    for sc in scenes:
        (out / "compositions" / f"{sc['id']}.html").write_text(sc["html"], encoding="utf-8")
    meta = []
    for sc in scenes:
        m = {k: sc[k] for k in ("id", "start", "duration", "beat")}
        if "track" in sc:
            m["track"] = sc["track"]
        meta.append(m)
    (out / "scenes.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "cues.json").write_text(json.dumps(cues, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "chrome.json").write_text(json.dumps(chrome or {"enabled": False, "series": "", "sections": [], "wipes": []},
                                                ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{part}: {len(scenes)} scenes")


HOOK_CUES = [{"t": 0.15, "sfx": "library/typing", "dur": 1.5, "accent": 0.8},
             {"t": 1.9, "sfx": "library/error", "accent": 1.2}, {"t": 1.92, "sfx": "library/glitch-2", "accent": 0.8},
             {"t": 2.45, "sfx": "library/impact-bass-1", "accent": 1.1}, {"t": 3.05, "sfx": "library/whoosh-short", "accent": 0.9}]


def part_style(name, skin):
    sc = s1(skin=skin, dur=6.0)
    write_part(name, [sc], HOOK_CUES)


def part_full():
    total = 75.6
    scenes = [s1(), s2(), s3(), s4(), s5(), s6(), s7(), subs(total)]
    cues = HOOK_CUES + [
        {"t": 4.4, "sfx": "library/whoosh", "accent": 0.8}, {"t": 7.05, "sfx": "library/pop", "accent": 0.9},
        {"t": 9.6, "sfx": "library/whoosh-short", "accent": 0.8}, {"t": 10.0, "sfx": "library/click-soft", "accent": 1.0},
        {"t": 10.6, "sfx": "library/click-soft", "accent": 1.0}, {"t": 11.2, "sfx": "library/click-soft", "accent": 1.0},
        {"t": 11.8, "sfx": "library/pop", "accent": 0.9}, {"t": 13.4, "sfx": "library/sparkle", "accent": 0.8},
        {"t": 14.0, "sfx": "library/whoosh-cinematic", "accent": 0.8},
        {"t": 17.9, "sfx": "library/pop", "accent": 0.8}, {"t": 19.6, "sfx": "library/notification", "accent": 0.8},
        {"t": 21.3, "sfx": "library/whoosh", "accent": 0.9}, {"t": 22.6, "sfx": "library/click", "accent": 0.8},
        {"t": 24.2, "sfx": "library/key-press", "accent": 1.0}, {"t": 25.2, "sfx": "library/key-press", "accent": 1.0},
        {"t": 27.4, "sfx": "library/ping", "accent": 0.8}, {"t": 28.0, "sfx": "library/pop", "accent": 0.8},
        {"t": 30.15, "sfx": "library/riser", "accent": 0.7, "dur": 1.2}, {"t": 31.4, "sfx": "library/whoosh-short", "accent": 0.8},
        {"t": 33.5, "sfx": "library/error", "accent": 1.0}, {"t": 34.0, "sfx": "library/glitch-1", "accent": 0.9},
        {"t": 35.8, "sfx": "library/notification", "accent": 1.2}, {"t": 36.3, "sfx": "library/notification", "accent": 1.0},
        {"t": 38.9, "sfx": "library/impact-bass-2", "accent": 1.0},
        {"t": 42.3, "sfx": "library/glitch-3", "accent": 0.9}, {"t": 45.0, "sfx": "library/whoosh", "accent": 0.8},
        {"t": 47.2, "sfx": "library/impact-bass-1", "accent": 1.0},
        {"t": 52.0, "sfx": "library/whoosh-cinematic", "accent": 1.0}, {"t": 53.8, "sfx": "library/sparkle", "accent": 0.8},
        {"t": 55.6, "sfx": "library/pop", "accent": 0.8}, {"t": 57.0, "sfx": "library/chime", "accent": 0.8},
        {"t": 58.0, "sfx": "library/chime", "accent": 0.8}, {"t": 59.0, "sfx": "library/chime", "accent": 0.8},
        {"t": 60.0, "sfx": "library/chime", "accent": 0.9}, {"t": 60.9, "sfx": "library/click-soft", "accent": 1.0},
        {"t": 61.9, "sfx": "library/click-soft", "accent": 1.0}, {"t": 62.9, "sfx": "library/click-soft", "accent": 1.0},
        {"t": 64.4, "sfx": "library/whoosh-short", "accent": 0.8}, {"t": 65.0, "sfx": "library/sparkle", "accent": 0.8},
        {"t": 67.2, "sfx": "library/riser", "accent": 0.6, "dur": 1.0}, {"t": 71.0, "sfx": "library/typing", "dur": 0.8, "accent": 0.7},
        {"t": 73.6, "sfx": "library/sparkle", "accent": 1.0},
    ]
    write_part("demo_flat", scenes, cues, {"enabled": False, "series": "", "sections": [], "wipes": [15.85, 29.85, 41.85, 66.85], "grain": True})


PARTS = {
    "demo_flat": part_full,
    "style_line": lambda: part_style("style_line", "line"),
    "style_noir": lambda: part_style("style_noir", "noir"),
}

if __name__ == "__main__":
    for name in (sys.argv[1:] or list(PARTS)):
        PARTS[name]()
