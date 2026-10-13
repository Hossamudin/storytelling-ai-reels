"""Talking-head hybrid: build the presenter layer of a motion project's index.html (idempotent).

Usage:
  python pipeline/th_layer.py <name> --part <part>        # then: python pipeline/motion_sync.py <name> --part <part>

Inputs in projects/<name>/<part>/:
  th.json          {"video": "assets/video/reel_th.mp4",
                    "matte": "assets/video/reel_th_matte.webm" | [{"src", "start", "end"}, ...] | null,
                          (prefer segments: cut only the text-behind windows from the full matte:
                           ffmpeg -c:v libvpx-vp9 -ss A -to B -i full.webm -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 3M -auto-alt-ref 0 seg.webm)
                    "duration": 170.667, "words": "../transcript/reel_words.json",
                    "modes":  [[t, "full"|"card"|"circle"|"hide", {opts}], ...],
                    "punch":  [[t, scale, dur], ...],          # dur 0 = hard punch (also hides jump-cut seams)
                    "nocap":  [[a, b], ...],                   # caption-free stretches inside full windows
                    "captions": {"enabled": true, "top": 1600, "max_words": 3}}
     modes opts: full {"z": 1.0, "d": 0.35} · circle {"cx", "cy", "s"} (presenter disc + lime ring) ·
                 card {} (upper body cropped into a rounded card at the top; the scene below is the canvas) ·
                 hide (a full-screen sub-composition covers the frame; scenes come from scenes.json as usual)
  th_behind.html   optional: elements between the camera and the person matte ("text behind you", layered depth)
  th_front.html    optional: overlays in front of the presenter (labels, cards, CTA)
  th_front.js      optional: root-timeline choreography for those elements, global seconds. Helpers in scope:
                   tl, sh(t, amp, n) shake presenter, slam(sel, t, from), off(sel, t, d), on(sel, t, y),
                   mask(sel, t), show(sel, t), pop(sel, t, from)
Layer stack: scenes (hosts) < #thw [camera video, #thgrade, #behind, matte video, #thvig] < #front (+ captions) < chrome.
Camera + voice share one timeline: th_cut.py cuts the camera with voice_edit.py's keep ranges.
Matte: npx hyperframes remove-background assets/video/<part>_th.mp4 -o assets/video/<part>_th_matte.webm (CPU ~0.3-0.8 s/frame:
start it right after th_cut.py).
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

HELPERS = """      const sh = (t, amp = 16, n = 7) => { for (let i = 0; i < n; i++) { const k = 1 - i / n; tl.to("#thw", { x: (i % 2 ? -1 : 1) * amp * k, duration: 0.035, ease: "none" }, t + i * 0.035); } tl.to("#thw", { x: 0, duration: 0.05 }, t + n * 0.035); };
      const slam = (sel, t, from = 2.4) => tl.fromTo(sel, { opacity: 0, scale: from, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.28, ease: "expo.out" }, t);
      const off = (sel, t, d = 0.25) => tl.to(sel, { opacity: 0, duration: d, ease: "power2.in" }, t);
      const on = (sel, t, y = 24) => tl.fromTo(sel, { opacity: 0, y }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, t);
      const mask = (sel, t) => tl.fromTo(sel, { yPercent: 115 }, { yPercent: 0, duration: 0.5, ease: "power4.out" }, t);
      const show = (sel, t) => tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t);
      const pop = (sel, t, from = 0.4) => tl.fromTo(sel, { opacity: 0, scale: from }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.2)" }, t);
      document.querySelectorAll("#front .mask").forEach((e) => e.setAttribute("data-layout-allow-overflow", ""));"""


def full_windows(modes, end):
    w, cur = [], None
    for t, m, _ in modes + [[end, "end", {}]]:
        if cur is not None:
            w.append((cur, t))
            cur = None
        if m == "full":
            cur = t
    return w


def captions(words, fw, nocap, max_words=3):
    def ok(t):
        return any((a + 0.05 if a else -1) <= t < b - 0.1 for a, b in fw) and not any(a <= t < b for a, b in nocap)
    isl = lambda x: bool(re.search(r"[A-Za-z0-9]", x["w"]))
    ws = [w for w in words if w["w"].strip() and ok(w["s"])]
    chunks, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        nxt = ws[i + 1] if i + 1 < len(ws) else None
        join = cur[-1]["w"] in ("الـ", "بـ", "لـ") or (nxt is not None and isl(cur[-1]) and isl(nxt) and len(cur) < max_words + 1)
        if not nxt or (not join and (len(cur) >= max_words or nxt["s"] - w["e"] > 0.28 or not ok(nxt["s"]) or nxt["s"] - cur[0]["s"] > 1.4)):
            chunks.append(cur)
            cur = []
    out = []
    for i, c in enumerate(chunks):
        t0 = max(0.0, c[0]["s"] - 0.06)
        nxt = chunks[i + 1][0]["s"] - 0.06 if i + 1 < len(chunks) else c[-1]["e"] + 0.4
        t1 = min(nxt, c[-1]["e"] + 0.45)
        for a, b in fw:
            if a <= t0 < b:
                t1 = min(t1, b - 0.05)
        html = ""
        for j, w in enumerate(c):
            txt = w["w"].replace("_", " ")
            glue = "" if (j and c[j - 1]["w"] in ("الـ", "بـ", "لـ")) else (" " if j else "")
            html += glue + (f'<span class="lat ah-l" style="color:var(--lime)">{txt}</span>' if isl(w) else txt)
        # one LTR span per run of Latin words, or bidi reverses them ("automation AI")
        html = html.replace('</span> <span class="lat ah-l" style="color:var(--lime)">', ' ')
        out.append((round(t0, 2), round(t1, 2), html))
    return out


def mode_js(modes, punch):
    L = ['      tl.fromTo("#thw", { scale: 1.25, x: 0, y: 0, opacity: 1, clipPath: "circle(1400px at 540px 760px)" }, { scale: 1, duration: 1.0, ease: "expo.out" }, 0);']
    a = L.append
    cur = "full"
    for t, m, o in modes:
        if t == 0:
            continue
        d = o.get("d", 0.35)
        if m == "hide":
            a(f'      tl.to("#thw", {{ opacity: 0, filter: "blur(8px)", duration: 0.22, ease: "power2.in" }}, {t - 0.12});')
            if cur == "circle":
                a(f'      tl.to("#fr-ring", {{ opacity: 0, duration: 0.2 }}, {t - 0.12});')
        elif m == "full":
            z = o.get("z", 1.0)
            if cur == "hide":
                a(f'      tl.set("#thw", {{ clipPath: "circle(1400px at 540px 760px)", x: 0, y: 0 }}, {t - 0.15});')
                a(f'      tl.fromTo("#thw", {{ opacity: 0, scale: {z + 0.08}, filter: "blur(10px)" }}, {{ opacity: 1, scale: {z}, filter: "blur(0px)", duration: 0.3, ease: "power3.out", immediateRender: false }}, {t - 0.15});')
            elif cur == "card":
                # inset() and circle() can't interpolate: tween the card open to a full inset, then swap to the equivalent full circle
                a(f'      tl.to("#thw", {{ clipPath: "inset(0px 0px 0px 0px round 0px)", scale: {z}, x: 0, y: 0, duration: {d}, ease: "power3.inOut" }}, {t});')
                a(f'      tl.set("#thw", {{ clipPath: "circle(1400px at 540px 760px)" }}, {t + d + 0.01});')
            elif cur == "circle":
                a(f'      tl.to("#thw", {{ clipPath: "circle(1400px at 540px 760px)", scale: {z}, x: 0, y: 0, duration: {d}, ease: "power3.inOut" }}, {t});')
                a(f'      tl.to("#fr-ring", {{ opacity: 0, duration: 0.2 }}, {t});')
        elif m == "card":
            if cur == "circle":  # the presenter ring must not linger over the canvas
                a(f'      tl.to("#fr-ring", {{ opacity: 0, duration: 0.15 }}, {t - 0.15});')
            a(f'      tl.set("#thw", {{ clipPath: "inset(330px 40px 560px 40px round 56px)", scale: 0.62, x: 0, y: -253, filter: "blur(0px)" }}, {t - 0.15});')
            a(f'      tl.fromTo("#thw", {{ opacity: 0, y: -173 }}, {{ opacity: 1, y: -253, duration: 0.4, ease: "expo.out", immediateRender: false }}, {t - 0.15});')
        elif m == "circle":
            s, cx, cy = o["s"], o["cx"], o["cy"]
            r = round(380 * s)
            a(f'      tl.set("#thw", {{ clipPath: "circle(380px at 540px 760px)", x: {cx - 540}, y: {cy - 760}, filter: "blur(0px)" }}, {t - 0.15});')
            a(f'      tl.fromTo("#thw", {{ opacity: 0, scale: {round(s * 0.6, 3)} }}, {{ opacity: 1, scale: {s}, duration: 0.45, ease: "back.out(1.8)", immediateRender: false }}, {t - 0.15});')
            a(f'      tl.set("#fr-ring", {{ left: {cx - r - 6}, top: {cy - r - 6}, width: {2 * r + 12}, height: {2 * r + 12} }}, {t - 0.15});')
            a(f'      tl.fromTo("#fr-ring", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)", immediateRender: false }}, {t - 0.1});')
        cur = m
    for t, z, d in punch:
        if d == 0:
            a(f'      tl.set("#thw", {{ scale: {z} }}, {t});')
        else:
            a(f'      tl.to("#thw", {{ scale: {z}, duration: {d}, ease: "{"power2.out" if d < 1 else "sine.inOut"}" }}, {t});')
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--part", required=True)
    a = ap.parse_args()
    out = C.project_path(a.name) / a.part
    cfg = json.loads((out / "th.json").read_text(encoding="utf-8"))
    rd = lambda f: (out / f).read_text(encoding="utf-8") if (out / f).exists() else ""
    p = out / "index.html"
    h = p.read_text(encoding="utf-8")
    root = re.search(r'<div[^>]*\sid="root"[^>]*>', h)  # Studio may add data-hf-id / reorder attributes
    end = float(re.search(r'data-duration="([\d.]+)"', root.group(0)).group(1))
    modes, punch, nocap = cfg.get("modes", [[0, "full", {}]]), cfg.get("punch", []), cfg.get("nocap", [])
    words = json.loads((out / cfg["words"]).read_text(encoding="utf-8"))["words"] if cfg.get("words") else []
    cc = cfg.get("captions", {})
    caps = captions(words, full_windows(modes, end), nocap, cc.get("max_words", 3)) if cc.get("enabled", True) and words else []
    top = cc.get("top", 1600)
    mt = cfg.get("matte")
    if isinstance(mt, str):
        matte = f'\n        <video id="thm" class="thm" src="{mt}" data-start="0" data-duration="{cfg["duration"]}" data-track-index="11" muted playsinline></video>'
    else:  # segments [{"src", "start", "end"}] cut from the full matte: far lighter to decode than one long alpha video
        matte = "".join(f'\n        <video id="thm{i}" class="thm" src="{m["src"]}" data-start="{m["start"]}" data-duration="{round(m["end"] - m["start"], 3)}" '
                        f'data-track-index="{11 + i}" muted playsinline></video>' for i, m in enumerate(mt or []))
    cap_html = "\n".join(f'        <div class="cap" id="cap{i:03d}" style="top:{top}px"><span>{x}</span></div>' for i, (_, _, x) in enumerate(caps))
    layer = f"""      <!-- TH:BEGIN (generated by pipeline/th_layer.py from th.json + th_behind.html + th_front.html) -->
      <div id="thw" data-layout-allow-overflow>
        <video id="thv" src="{cfg["video"]}" data-start="0" data-duration="{cfg["duration"]}" data-track-index="10" muted playsinline></video>
        <div id="thgrade"></div>
        <div id="behind">{rd("th_behind.html").rstrip()}
        </div>{matte}
        <div id="thvig"></div>
      </div>
      <div id="front">{rd("th_front.html").rstrip()}
        <div id="fr-ring" class="abs"></div>
{cap_html}
      </div>
      <!-- TH:END -->"""
    js = ["        // TH:BEGIN (generated by pipeline/th_layer.py) -- presenter formats, punches, custom choreography, captions",
          mode_js(modes, punch), HELPERS, rd("th_front.js").rstrip()]
    for i, (t0, t1, _) in enumerate(caps):
        js.append(f'      tl.fromTo("#cap{i:03d}", {{ opacity: 0, scale: 0.86, y: 10 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.12, ease: "back.out(2)" }}, {t0}); '
                  f'tl.to("#cap{i:03d}", {{ opacity: 0, duration: 0.06 }}, {max(t0 + 0.13, t1 - 0.06):.2f});')
    # the choreography lives in assets/js/th_layer.js (keeps index.html under the composition size limit that
    # preflight enforces); the root timeline just calls it.
    (out / "assets/js").mkdir(parents=True, exist_ok=True)
    (out / "assets/js/th_layer.js").write_text(
        "// generated by pipeline/th_layer.py -- do not edit; edit th.json / th_front.js and re-run\n"
        "window.HF_TH = function (tl) {\n" + "\n".join(js[1:]) + "\n};\n", encoding="utf-8")
    js = [js[0], "        window.HF_TH(tl);", "        // TH:END"]
    if 'src="assets/js/th_layer.js"' not in h:
        h = re.sub(r'(<script[^>]*src="assets/js/fx\.js"[^>]*></script>)', r'\1\n    <script src="assets/js/th_layer.js"></script>', h, count=1)
    if 'href="assets/css/th.css"' not in h:
        h = h.replace('<link rel="stylesheet" href="assets/css/base.css" />',
                      '<link rel="stylesheet" href="assets/css/base.css" />\n    <link rel="stylesheet" href="assets/css/th.css" />', 1)
    h = re.sub(r"\s*<!-- TH:BEGIN.*?<!-- TH:END -->", "", h, flags=re.S)
    h = h.replace("      <!-- HOSTS:END -->", "      <!-- HOSTS:END -->\n" + layer, 1)
    h = re.sub(r"\s*// TH:BEGIN.*?// TH:END", "", h, flags=re.S)
    h = re.sub(r'(\n\s*window\.__timelines\["main"\] = tl;)', lambda m: "\n" + "\n".join(js) + m.group(1), h, count=1)
    p.write_text(h, encoding="utf-8")
    print(f"OK: presenter layer -> {p} ({len(modes)} format switches, {len(punch)} punches, {len(caps)} caption chunks)")
    C.log(a.name, f"th_layer: {a.part}")


if __name__ == "__main__":
    main()
