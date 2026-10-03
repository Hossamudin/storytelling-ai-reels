// Hossam motion kit — screen-recording annotation engine (v1).
//
// Generated data (pipeline/screen_annot.py) sets window.HF_ANNOT = { k, x, y, w, h, items: [...] }
// with OUTPUT times and SOURCE-pixel rects ([x, y, w, h] in the cropped recording).
// Inside the "screen" sub-composition:
//   const fx = window.HF_SCENE(0);
//   window.HF_SCREEN(fx, { cam: "#scr-cam", layer: "#scr-annot" });
//   window.__timelines["screen"] = fx.tl.real;
//
// Item types (all deterministic, seek-safe):
//   zoom   {t, d, rect, s}           camera frames rect at scale s (s:1 + no rect = full view)
//   spot   {t0, t1, rect, ar, en, pos, circle, dim}   highlight box + optional dim + callout
//   circle {t0, t1, rect}            hand-drawn ellipse drawn on
//   click  {t, x, y}                 ripple at a point
//   label  {t0, t1, x, y, ar, en}    free callout
//   blur   {rect, t0?, t1?}          privacy blur (whole video when no times)
//   badge  {t0, t1, text}            e.g. "×4" speed-ramp badge (top-left of the window)
(function () {
  window.HF_SCREEN = function (fx, opt) {
    const A = window.HF_ANNOT;
    const { tl, Q } = fx;
    const layer = Q(opt.layer);
    const k = A.k, ox = A.x, oy = A.y;
    const mk = (cls, css, html) => { const e = document.createElement("div"); e.className = cls; e.style.cssText = css; if (html) e.innerHTML = html; layer.appendChild(e); return e; };
    const box = (r, pad = 0) => `left:${r[0] - pad}px;top:${r[1] - pad}px;width:${r[2] + 2 * pad}px;height:${r[3] + 2 * pad}px`;

    // ---- camera (sequential, each move starts from the previous state) ----
    let cam = { x: 0, y: 0, s: 1 };
    const view = (r, s) => {
      const cx = ox + (r[0] + r[2] / 2) * k, cy = oy + (r[1] + r[3] / 2) * k;
      let x = 960 - cx * s, y = 540 - cy * s;
      // keep the window edges from drifting far into frame
      const minX = 1920 - (ox + A.w * k) * s - 40, maxX = -ox * s + 40;
      const minY = 1080 - (oy + A.h * k) * s - 40, maxY = -oy * s + 40;
      if (s > 1) { x = Math.min(maxX, Math.max(minX, x)); y = Math.min(maxY, Math.max(minY, y)); }
      return { x, y, s };
    };
    const zooms = A.items.filter((a) => a.type === "zoom").sort((a, b) => a.t - b.t);
    zooms.forEach((z) => {
      const v = z.rect && z.s > 1 ? view(z.rect, z.s) : { x: 0, y: 0, s: 1 };
      tl.fromTo(opt.cam, { x: cam.x, y: cam.y, scale: cam.s }, { x: v.x, y: v.y, scale: v.s, duration: z.d ?? 0.8, ease: z.ease ?? "power3.inOut", immediateRender: false }, z.t);
      cam = v;
    });

    let n = 0;
    A.items.forEach((a) => {
      n++;
      if (a.type === "blur") {
        const e = mk("scr-blur", box(a.rect));
        if (a.t0 !== undefined) { fx.hide(e); tl.fromTo(e, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, a.t0); tl.to(e, { opacity: 0, duration: 0.2 }, a.t1); }
      }
      if (a.type === "spot") {
        const r = a.rect, pad = a.pad ?? 10;
        const e = mk("scr-spot" + (a.dim === false ? " nodim" : ""), box(r, pad));
        tl.fromTo(e, { opacity: 0, scale: 1.08 }, { opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }, a.t0);
        tl.to(e, { opacity: 0, duration: 0.3 }, a.t1);
        if (a.circle) circle(r, a.t0 + 0.1, a.t1);
        if (a.ar || a.en) callout(r, a.pos || "bottom", a.ar, a.en, a.t0 + 0.15, a.t1);
      }
      if (a.type === "circle") circle(a.rect, a.t0, a.t1);
      if (a.type === "label") callout([a.x, a.y, 0, 0], a.pos || "bottom", a.ar, a.en, a.t0, a.t1);
      if (a.type === "click") {
        const e = mk("scr-ripple", `left:${a.x - 45}px;top:${a.y - 45}px`);
        fx.hide(e);
        tl.fromTo(e, { opacity: 0.95, scale: 0.2 }, { opacity: 0, scale: 1.6, duration: 0.55, ease: "power2.out", immediateRender: false }, a.t);
      }
      if (a.type === "badge") {
        const e = mk("scr-badge", "left:24px;top:24px", `<span>⏩</span><b class="lat">${a.text}</b><i>${a.ar || ""}</i>`);
        tl.fromTo(e, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, a.t0);
        tl.to(e, { opacity: 0, duration: 0.25 }, a.t1);
      }
    });

    function circle(r, t0, t1) {
      const w = r[2] + 60, h = r[3] + 44;
      const e = mk("scr-circle", `left:${r[0] - 30}px;top:${r[1] - 22}px;width:${w}px;height:${h}px`,
        `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none"><path d="M ${w * 0.52} ${h * 0.04} C ${w * 0.95} ${h * 0.02}, ${w * 1.0} ${h * 0.9}, ${w * 0.5} ${h * 0.96} C ${w * 0.04} ${h * 1.0}, ${w * -0.01} ${h * 0.12}, ${w * 0.6} ${h * 0.09}" pathLength="1" /></svg>`);
      const p = e.querySelector("path");
      tl.fromTo(p, { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, t0);
      tl.to(e, { opacity: 0, duration: 0.3 }, t1);
    }
    function callout(r, pos, ar, en, t0, t1) {
      const html = (en ? `<div class="en" data-layout-allow-overlap>${en}</div>` : "") + (ar ? `<div class="ar" data-layout-allow-overlap>${ar}</div>` : "");
      const gap = 26;
      let css, xp = -50, yp = 0;
      if (pos === "bottom") css = `left:${r[0] + r[2] / 2}px;top:${r[1] + r[3] + gap}px`;
      else if (pos === "top") { css = `left:${r[0] + r[2] / 2}px;top:${r[1] - gap}px`; yp = -100; }
      else if (pos === "left") { css = `left:${r[0] - gap}px;top:${r[1] + r[3] / 2}px`; xp = -100; yp = -50; }
      else { css = `left:${r[0] + r[2] + gap}px;top:${r[1] + r[3] / 2}px`; xp = 0; yp = -50; }
      const e = mk("scr-callout", css, `<div class="in" data-layout-allow-overlap>${html}</div>`);
      const inner = e.querySelector(".in");
      tl.fromTo(inner, { opacity: 0, scale: 0.6, xPercent: xp, yPercent: yp }, { opacity: 1, scale: 1, xPercent: xp, yPercent: yp, duration: 0.4, ease: "back.out(2)" }, t0);
      tl.to(inner, { opacity: 0, duration: 0.25 }, t1);
    }
  };
})();
