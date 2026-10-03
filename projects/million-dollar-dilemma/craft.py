# -*- coding: utf-8 -*-
"""Craft layer for million-dollar-dilemma (v3 — dynamic timings from storyboard).
Re-runnable AFTER any `python pipeline/assemble.py million-dollar-dilemma`.
Scene times are read from storyboard.json, so retiming never breaks this."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
sys.stdout.reconfigure(encoding="utf-8")

COMP = Path(__file__).resolve().parent / "composition" / "index.html"
SB = Path(__file__).resolve().parent / "storyboard.json"
sb = json.loads(SB.read_text(encoding="utf-8"))
S = {s["id"]: s for s in sb["scenes"]}
html = COMP.read_text(encoding="utf-8")
orig = html


def sub1(pattern, repl, label=""):
    global html
    new, n = re.subn(pattern, repl, html, count=1, flags=re.S)
    if n != 1:
        print(f"WARN: pattern not found ({label})")
        return False
    html = new
    return True


def T(sid, off=0.0):
    return round(S[sid]["start"] + off, 2)


# ---------------- code scenes: inner content ----------------
INNERS = {
"S01": ('''
      <div class="s01-wrap" id="s01-inner">
        <div class="s01-kicker" id="s01-kicker">خبر بيقلب الموازين</div>
        <div class="s01-big" id="s01-big" dir="rtl"><span class="w">معضلة</span><span class="w">بمليون</span><span class="w">دولار</span></div>
        <div class="s01-bar" id="s01-bar"></div>
        <div class="s01-sub" id="s01-sub" dir="rtl">حلّها الذكاء الاصطناعي <span class="s01-hl">AI</span></div>
        <div class="s01-chip" id="s01-chip" dir="rtl">90 سنة محدش عرف يحلها</div>
      </div>''', "#0D2B23"),
"S05": ('''
      <div class="s05-wrap" id="s05-inner">
        <div class="s13-kicker" id="s05-kicker" dir="rtl">جايزة معهد كلاي للرياضيات</div>
        <div class="s05-money" id="s05-money" dir="ltr">$<span id="s05-num">0</span></div>
        <div class="s05-bar" id="s05-bar"></div>
        <div class="s05-sub" id="s05-sub" dir="rtl">لأي حد يحل معادلات <span class="kw-latin">Navier–Stokes</span></div>
      </div>''', "#FFFFFF"),
"S08": ('''
      <div class="s05-wrap" id="s08-inner">
        <div class="s13-kicker" id="s08-kicker" dir="rtl"><span class="kw-latin">OpenAI</span> أعلنت</div>
        <div class="s05-money s08-num" id="s08-num-wrap" dir="ltr"><span id="s08-num">0</span></div>
        <div class="s05-sub" id="s08-sub" dir="rtl">موظف ذكاء اصطناعي شغالين بموديل واحد</div>
        <div class="s08-chip" id="s08-chip" dir="rtl">بنفس الطريقة اللي فريق بشري بيشتغل بيها</div>
      </div>''', "#FAF7F0"),
"S13": ('''
      <div class="s13-wrap" id="s13-inner">
        <div class="s13-kicker" id="s13-kicker" dir="rtl">اللي حصل بالأرقام</div>
        <div class="s13-card" id="s13-card1"><div class="s13-num" id="s13-n1">0</div><div class="s13-lbl" dir="rtl">وكيل AI شغالين مع بعض</div></div>
        <div class="s13-card" id="s13-card2"><div class="s13-num" id="s13-n2">0</div><div class="s13-lbl" dir="rtl">ساعة شغل متواصل</div></div>
        <div class="s13-card" id="s13-card3"><div class="s13-num s13-gpt" id="s13-n3">GPT-6</div><div class="s13-lbl" dir="rtl">الموديل اللي خلّى ده يحصل</div></div>
        <div class="s13-result" id="s13-result" dir="rtl">النتيجة: مسألة بمليون دولار اتحلّت</div>
      </div>''', "#FAF7F0"),
"S15": ('''
      <div class="q-wrap" id="s15-inner">
        <div class="q-mark" id="s15-mark">❝</div>
        <div class="q-line1" id="s15-l1" dir="rtl">مش عشان يستبدلك…</div>
        <div class="q-line2" id="s15-l2" dir="rtl">علشان يساعدك</div>
        <div class="q-underline" id="s15-ul"></div>
        <div class="q-attr" id="s15-attr" dir="rtl">— حسام الدين حسن</div>
        <div class="q-role" id="s15-role">AI Storyteller</div>
      </div>''', "#FAF7F0"),
"S30": ('''
      <div class="s30-wrap" id="s30-inner">
        <div class="s30-q" id="s30-q" dir="rtl">عندك هدف عايز تحققه بـ <span class="kw-orange">AI</span>؟</div>
        <div class="s30-big" id="s30-big" dir="rtl">اكتبهولي في الكومنتات</div>
        <div class="s01-bar" id="s30-bar"></div>
        <div class="s30-chip" id="s30-chip" dir="rtl">أرد على كل الكومنتات واحد واحد</div>
      </div>''', "#0D2B23"),
"S31": ('''
      <div class="s31-wrap" id="s31-inner">
        <div class="s31-kicker" id="s31-kicker" dir="rtl">بودكاست أخبار التقنية</div>
        <div class="s31-big" id="s31-big" dir="rtl">أخبار الـ <span class="kw-orange">AI</span> الأسبوعية</div>
        <div class="s31-when" id="s31-when" dir="rtl">كل يوم سبت — <span class="kw-green">7 مساءً</span></div>
        <div class="s31-chip" id="s31-chip" dir="rtl">فولو عشان ماتفوتش حلقة</div>
      </div>''', "#136052"),
}

for sid, (inner, fill) in INNERS.items():
    sub1(rf'(<div id="sc-{sid}" class="clip"[^>]*>\n    <div class="scene-fill" style="background:)#[0-9A-F]{{6}}(">)',
         lambda m, f=fill: m.group(1) + f + m.group(2), f"{sid} fill")
    sub1(rf'(<div class="scene-inner" id="sc-{sid}-inner">)\n(.*?)(\n    </div>)',
         lambda m, i=inner: m.group(1) + i + m.group(3), f"{sid} inner")
    html = re.sub(rf'  tl\.fromTo\("#sc-{sid}-inner[^;]*;\n', "", html)

# ---------------- S29: replace hossam img scene with quote overlay ----------------
s29 = S["S29"]
start29, dur29 = s29["start"], round(s29["end"] - s29["start"], 2)
S29_BLOCK = f'''<div id="sc-S29" class="clip" data-start="{start29}" data-duration="{dur29}" data-track-index="3" data-layout-allow-overflow>
    <div class="scene-fill" style="background:linear-gradient(150deg,#0D2B23 0%,#136052 100%)"></div>
    <div class="s29-wrap" id="s29-inner">
      <div class="s29-txt">
        <div class="s29-l1" id="s29-l1" dir="rtl">مش عشان يستبدلك</div>
        <div class="s29-l2" id="s29-l2" dir="rtl">علشان <span class="s29-hl">يساعدك</span></div>
        <div class="s29-underline" id="s29-ul"></div>
        <div class="s29-attr" id="s29-attr" dir="rtl">— حسام الدين حسن</div>
      </div>
      <img class="s29-person" id="s29-person" src="assets/images/S29_first.png" alt="" />
    </div>
  </div>'''
sub1(r'  <img id="sc-S29" class="clip"[^>]*/>\n', "", "S29 img")
sub1(r'  <div id="sc-S29-grad" class="clip"[^>]*></div>\n', "", "S29 grad")
html = re.sub(r'  tl\.fromTo\("#sc-S29"[^;]*;\n', "", html)
sub1(r'(  <audio id="voiceover")', S29_BLOCK + r"\n\1", "S29 block")

# ---------------- tweens (dynamic times) ----------------
TW = f'''
  // ---- craft v3 (timings from storyboard) ----
  tl.fromTo("#s01-inner", {{scale:1.05}}, {{scale:1, duration:{round(S['S01']['end']-S['S01']['start'],2)}, ease:"power1.out"}}, {T('S01')});
  tl.fromTo("#s01-kicker", {{autoAlpha:0, y:-24}}, {{autoAlpha:1, y:0, duration:0.4, ease:"power2.out"}}, {T('S01', 0.1)});
  tl.fromTo("#s01-big .w", {{y:90, autoAlpha:0}}, {{y:0, autoAlpha:1, duration:0.5, ease:"back.out(1.7)", stagger:0.14}}, {T('S01', 0.3)});
  tl.fromTo("#s01-sub", {{autoAlpha:0, scale:0.8}}, {{autoAlpha:1, scale:1, duration:0.45, ease:"back.out(2)"}}, {T('S01', 1.1)});
  tl.fromTo("#s01-bar", {{scaleX:0}}, {{scaleX:1, duration:0.5, ease:"power3.out"}}, {T('S01', 1.45)});
  tl.fromTo("#s01-chip", {{autoAlpha:0, y:30}}, {{autoAlpha:1, y:0, duration:0.4, ease:"power2.out"}}, {T('S01', 1.8)});

  tl.fromTo("#s05-kicker", {{autoAlpha:0, y:-20}}, {{autoAlpha:1, y:0, duration:0.45, ease:"power2.out"}}, {T('S05', 0.3)});
  const m1 = {{ v: 0 }};
  tl.to(m1, {{v: 1000000, duration: 2.6, ease: "power2.out", onUpdate: () => {{ document.getElementById("s05-num").textContent = Math.round(m1.v).toLocaleString("en-US"); }}}}, {T('S05', 0.6)});
  tl.fromTo("#s05-money", {{scale:0.85}}, {{scale:1, duration:2.6, ease:"power2.out"}}, {T('S05', 0.6)});
  tl.fromTo("#s05-bar", {{scaleX:0}}, {{scaleX:1, duration:0.5, ease:"power3.out"}}, {T('S05', 3.2)});
  tl.fromTo("#s05-sub", {{autoAlpha:0, y:34}}, {{autoAlpha:1, y:0, duration:0.5, ease:"power3.out"}}, {T('S05', 3.5)});

  tl.fromTo("#s08-kicker", {{autoAlpha:0, y:-20}}, {{autoAlpha:1, y:0, duration:0.45, ease:"power2.out"}}, {T('S08', 0.3)});
  const a1 = {{ v: 0 }};
  tl.to(a1, {{v: 10000, duration: 2.4, ease: "power2.out", onUpdate: () => {{ document.getElementById("s08-num").textContent = Math.round(a1.v).toLocaleString("en-US"); }}}}, {T('S08', 0.7)});
  tl.fromTo("#s08-num-wrap", {{scale:0.85}}, {{scale:1, duration:2.4, ease:"power2.out"}}, {T('S08', 0.7)});
  tl.fromTo("#s08-sub", {{autoAlpha:0, y:30}}, {{autoAlpha:1, y:0, duration:0.5, ease:"power3.out"}}, {T('S08', 3.0)});
  tl.fromTo("#s08-chip", {{autoAlpha:0, scale:0.85}}, {{autoAlpha:1, scale:1, duration:0.45, ease:"back.out(1.8)"}}, {T('S08', 4.0)});

  tl.fromTo("#s13-kicker", {{autoAlpha:0, y:-20}}, {{autoAlpha:1, y:0, duration:0.45, ease:"power2.out"}}, {T('S13', 0.3)});
  tl.fromTo("#s13-card1", {{autoAlpha:0, y:70}}, {{autoAlpha:1, y:0, duration:0.5, ease:"power3.out"}}, {T('S13', 0.7)});
  const c1 = {{ v: 0 }};
  tl.to(c1, {{v: 10000, duration: 2.4, ease: "power2.out", onUpdate: () => {{ document.getElementById("s13-n1").textContent = Math.round(c1.v).toLocaleString("en-US"); }}}}, {T('S13', 1.0)});
  tl.fromTo("#s13-card2", {{autoAlpha:0, y:70}}, {{autoAlpha:1, y:0, duration:0.5, ease:"power3.out"}}, {T('S13', 3.2)});
  const c2 = {{ v: 0 }};
  tl.to(c2, {{v: 180, duration: 1.8, ease: "power2.out", onUpdate: () => {{ document.getElementById("s13-n2").textContent = Math.round(c2.v).toLocaleString("en-US"); }}}}, {T('S13', 3.5)});
  tl.fromTo("#s13-card3", {{autoAlpha:0, scale:0.75}}, {{autoAlpha:1, scale:1, duration:0.5, ease:"back.out(2.2)"}}, {T('S13', 5.6)});
  tl.fromTo("#s13-result", {{autoAlpha:0, y:40}}, {{autoAlpha:1, y:0, duration:0.55, ease:"power3.out"}}, {T('S13', 7.4)});

  tl.fromTo("#s15-mark", {{autoAlpha:0, rotation:-12}}, {{autoAlpha:0.95, rotation:0, duration:0.7, ease:"power2.out"}}, {T('S15', 0.2)});
  tl.fromTo("#s15-l1", {{y:70, autoAlpha:0}}, {{y:0, autoAlpha:1, duration:0.55, ease:"power3.out"}}, {T('S15', 0.45)});
  tl.fromTo("#s15-l2", {{scale:0.7, autoAlpha:0}}, {{scale:1, autoAlpha:1, duration:0.5, ease:"back.out(2)"}}, {T('S15', 1.2)});
  tl.fromTo("#s15-ul", {{scaleX:0}}, {{scaleX:1, duration:0.45, ease:"power3.out"}}, {T('S15', 1.75)});
  tl.fromTo("#s15-attr", {{autoAlpha:0}}, {{autoAlpha:1, duration:0.5}}, {T('S15', 2.4)});
  tl.fromTo("#s15-role", {{autoAlpha:0}}, {{autoAlpha:1, duration:0.5}}, {T('S15', 2.8)});
  tl.fromTo("#s15-inner", {{scale:1}}, {{scale:1.02, duration:{round(S['S15']['end']-S['S15']['start']-0.5,2)}, ease:"sine.inOut"}}, {T('S15')});

  tl.fromTo("#s29-person", {{y:90, autoAlpha:0}}, {{y:0, autoAlpha:1, duration:0.9, ease:"power3.out"}}, {T('S29', 0.2)});
  tl.fromTo("#s29-l1", {{x:70, autoAlpha:0}}, {{x:0, autoAlpha:1, duration:0.55, ease:"power3.out"}}, {T('S29', 0.5)});
  tl.fromTo("#s29-l2", {{scale:0.75, autoAlpha:0}}, {{scale:1, autoAlpha:1, duration:0.5, ease:"back.out(2)"}}, {T('S29', 1.2)});
  tl.fromTo("#s29-ul", {{scaleX:0}}, {{scaleX:1, duration:0.45, ease:"power3.out"}}, {T('S29', 1.75)});
  tl.fromTo("#s29-attr", {{autoAlpha:0}}, {{autoAlpha:1, duration:0.5}}, {T('S29', 2.4)});
  tl.fromTo("#s29-inner", {{scale:1}}, {{scale:1.02, duration:{round(dur29-1,2)}, ease:"sine.inOut"}}, {T('S29')});

  tl.fromTo("#s30-q", {{autoAlpha:0, y:40}}, {{autoAlpha:1, y:0, duration:0.5, ease:"power3.out"}}, {T('S30', 0.3)});
  tl.fromTo("#s30-big", {{y:80, autoAlpha:0}}, {{y:0, autoAlpha:1, duration:0.55, ease:"back.out(1.6)"}}, {T('S30', 1.0)});
  tl.fromTo("#s30-bar", {{scaleX:0}}, {{scaleX:1, duration:0.5, ease:"power3.out"}}, {T('S30', 2.2)});
  tl.fromTo("#s30-chip", {{autoAlpha:0, y:30}}, {{autoAlpha:1, y:0, duration:0.45, ease:"power2.out"}}, {T('S30', 2.8)});

  tl.fromTo("#s31-kicker", {{autoAlpha:0, y:-20}}, {{autoAlpha:1, y:0, duration:0.45, ease:"power2.out"}}, {T('S31', 0.3)});
  tl.fromTo("#s31-big", {{y:80, autoAlpha:0}}, {{y:0, autoAlpha:1, duration:0.55, ease:"power3.out"}}, {T('S31', 0.7)});
  tl.fromTo("#s31-when", {{scale:0.8, autoAlpha:0}}, {{scale:1, autoAlpha:1, duration:0.5, ease:"back.out(2)"}}, {T('S31', 1.6)});
  tl.fromTo("#s31-chip", {{autoAlpha:0, y:30}}, {{autoAlpha:1, y:0, duration:0.45, ease:"power2.out"}}, {T('S31', 2.4)});
'''
sub1(r'(\n  window\.__timelines\["main"\] = tl;)', "\n" + TW + r"\1", "tweens")

CSS = '''
  /* ---- craft v3 ---- */
  .s01-wrap { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:34px; padding:80px 60px; }
  .s01-kicker { font-size:34px; font-weight:600; color:#E8F3C8; background:rgba(19,96,82,.55); padding:10px 30px; border-radius:999px; border:1px solid #B3CE65; }
  .s01-big { font-weight:800; font-size:150px; line-height:1.25; color:#FFEC5C; text-align:center; }
  .s01-big .w { display:inline-block; margin:0 14px; }
  .s01-bar { width:340px; height:10px; border-radius:6px; background:#FF5A33; transform-origin:center; }
  .s01-sub { font-size:64px; font-weight:700; color:#FFFFFF; }
  .s01-hl { font-family:'Manrope','Noto Kufi Arabic',sans-serif; color:#FF7A50; font-weight:800; }
  .s01-chip { font-size:36px; color:#0D2B23; background:#B3CE65; font-weight:700; padding:12px 34px; border-radius:14px; }
  .s05-wrap { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:36px; padding:80px 60px; }
  .s05-money { font-family:'Manrope',sans-serif; font-size:170px; font-weight:800; color:#136052; line-height:1.05; }
  .s05-bar { width:420px; height:10px; border-radius:6px; background:#FF5A33; }
  .s05-sub { font-size:46px; font-weight:700; color:#2E6B4F; text-align:center; }
  .s08-num { color:#D93A2B; font-size:190px; }
  .s08-chip { font-size:36px; font-weight:700; color:#2E6B4F; background:#FFFFFF; border:2px solid #B3CE65; border-radius:14px; padding:14px 34px; }
  .kw-latin { font-family:'Manrope',sans-serif; font-weight:800; color:#D93A2B; }
  .s13-wrap { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:30px; padding:70px 70px; }
  .s13-kicker { font-size:42px; font-weight:800; color:#2E6B4F; }
  .s13-card { width:100%; background:#FFFFFF; border:2px solid #B3CE65; border-radius:22px; padding:34px 40px; text-align:center; }
  .s13-num { font-family:'Manrope',sans-serif; font-size:120px; font-weight:800; color:#136052; line-height:1.1; }
  .s13-gpt { color:#D93A2B; font-size:104px; }
  .s13-lbl { font-size:34px; color:#2E6B4F; font-weight:600; margin-top:8px; }
  .s13-result { margin-top:12px; font-size:44px; font-weight:800; color:#D93A2B; background:#FFF; border:2px solid #FF5A33; border-radius:16px; padding:16px 36px; }
  .q-wrap { position:absolute; inset:0; display:flex; flex-direction:column; align-items:flex-start; justify-content:center; padding:110px 90px; }
  .q-mark { position:absolute; top:70px; right:70px; font-size:300px; line-height:1; color:#B3CE65; font-family:Georgia,serif; }
  .q-line1 { font-size:88px; font-weight:700; color:#136052; line-height:1.5; }
  .q-line2 { font-size:120px; font-weight:800; color:#D93A2B; line-height:1.35; }
  .q-underline { width:300px; height:9px; border-radius:6px; background:#FF5A33; margin:26px 0 40px; transform-origin:right center; }
  .q-attr { font-size:44px; font-weight:700; color:#2E6B4F; }
  .q-role { font-size:30px; font-weight:700; color:#2E6B4F; opacity:.8; margin-top:8px; font-family:'Manrope',sans-serif; letter-spacing:.18em; }
  .s30-wrap { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:38px; padding:80px 60px; }
  .s30-q { font-size:60px; font-weight:700; color:#FFFFFF; }
  .s30-big { font-size:110px; font-weight:800; color:#FFEC5C; text-align:center; line-height:1.3; }
  .s30-chip { font-size:36px; font-weight:700; color:#0D2B23; background:#B3CE65; border-radius:14px; padding:14px 34px; }
  .s31-wrap { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:34px; padding:80px 60px; }
  .s31-kicker { font-size:34px; font-weight:600; color:#E8F3C8; border:1px solid #B3CE65; border-radius:999px; padding:10px 30px; }
  .s31-big { font-size:104px; font-weight:800; color:#FFFFFF; text-align:center; line-height:1.3; }
  .s31-when { font-size:64px; font-weight:800; color:#FFEC5C; }
  .s31-chip { font-size:38px; font-weight:700; color:#136052; background:#B3CE65; border-radius:14px; padding:14px 36px; }
  .kw-orange { font-family:'Manrope','Noto Kufi Arabic',sans-serif; color:#FF7A50; font-weight:800; }
  .kw-green { color:#B3CE65; }
  .s29-wrap { position:absolute; inset:0; display:flex; align-items:flex-end; justify-content:space-between; padding:70px 60px; }
  .s29-txt { flex:1; display:flex; flex-direction:column; align-items:flex-start; padding-bottom:150px; }
  .s29-l1 { font-size:92px; font-weight:700; color:#FFFFFF; line-height:1.45; }
  .s29-l2 { font-size:126px; font-weight:800; color:#FFEC5C; line-height:1.3; }
  .s29-hl { color:#FF7A50; }
  .s29-underline { width:280px; height:9px; border-radius:6px; background:#FF5A33; margin:26px 0 36px; transform-origin:right center; }
  .s29-attr { font-size:40px; font-weight:700; color:#E8F3C8; }
  .s29-person { height:88%; object-fit:contain; object-position:bottom; }
'''
sub1(r'(\n</style>)', "\n" + CSS + r"\1", "css")

if html != orig:
    COMP.write_text(html, encoding="utf-8")
    print(f"craft v3 applied (S01@{T('S01')}s, S29@{T('S29')}s, S31@{T('S31')}s)")
else:
    print("NO CHANGES — run assemble.py first")
