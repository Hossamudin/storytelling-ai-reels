// Hossam motion kit — shared GSAP helpers for HyperFrames scenes (v2).
//
// Usage inside a sub-composition <template> script:
//   const fx = window.HF_SCENE(20.5);          // 20.5 = this scene's data-start (global seconds)
//   const { tl, rise, maskUp, counter, ... } = fx;
//   rise("#x", 21.3);                           // ALL times are GLOBAL (edited-voice) seconds
//   window.__timelines["s5"] = tl.real;
//
// Rules baked in: one paused timeline, fromTo with explicit from-states, finite repeats,
// deterministic (no Math.random / Date.now), transforms + paint props only.
// Selector note: a sub-composition's inner root merges into its host (#<id>-host), so never
// select "#s3 .x" — use ids/classes of the elements themselves.

(function () {
  const AR_DIGITS = "٠١٢٣٤٥٦٧٨٩";
  const toAr = (s) => String(s).replace(/[0-9]/g, (d) => AR_DIGITS[+d]);

  window.HF_SCENE = function (t0) {
    const real = gsap.timeline({ paused: true });
    const sh = (p) => (typeof p === "number" ? p - t0 : p);
    const tl = {
      real,
      to: (a, b, p) => real.to(a, b, sh(p)),
      fromTo: (a, b, c, p) => real.fromTo(a, b, c, sh(p)),
      set: (a, b, p) => real.set(a, b, sh(p)),
    };
    const Q = (s) => document.querySelector(s);
    const QA = (s) => Array.from(document.querySelectorAll(s));

    // ---------- entrances / exits ----------
    function rise(sel, t, o = {}) {
      tl.fromTo(sel,
        { opacity: 0, y: o.y ?? 50, scale: o.s ?? 1, filter: `blur(${o.b ?? 10}px)` },
        { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: o.d ?? 0.5, ease: o.e ?? "power3.out", stagger: o.st ?? 0 }, t);
    }
    // kinetic reveal: text slides up inside a .mask wrapper (markup: <span class="mask"><span class="in" id=..>)
    function maskUp(sel, t, o = {}) {
      QA(sel).forEach((e) => e.setAttribute("data-layout-allow-overflow", "")); // clipping is the effect
      tl.fromTo(sel, { yPercent: 115 }, { yPercent: 0, duration: o.d ?? 0.5, ease: o.e ?? "power4.out", stagger: o.st ?? 0 }, t);
    }
    function pop(sel, t, o = {}) {
      tl.fromTo(sel, { opacity: 0, scale: o.from ?? 0 }, { opacity: 1, scale: 1, duration: o.d ?? 0.4, ease: o.e ?? "back.out(2.2)", stagger: o.st ?? 0 }, t);
    }
    function out(sel, t, o = {}) {
      tl.to(sel, { opacity: 0, y: o.y ?? 0, x: o.x ?? 0, scale: o.s ?? 1, filter: `blur(${o.b ?? 8}px)`, duration: o.d ?? 0.3, ease: o.e ?? "power2.in", stagger: o.st ?? 0 }, t);
    }
    // hide at build (fromTo renders its from-state immediately) — for elements revealed later by .to()
    function hide(sel, t0h = t0) {
      tl.fromTo(sel, { opacity: 0 }, { opacity: 0, duration: 0.01 }, t0h);
    }
    // letter-by-letter drop for English hero titles: splits text into .ch spans at build
    function letterDrop(sel, t, o = {}) {
      const el = Q(sel);
      if (!el.dataset.split) {
        el.innerHTML = el.textContent.split("").map((c) => `<span class="ch" style="display:inline-block">${c === " " ? "&nbsp;" : c}</span>`).join("");
        el.dataset.split = "1";
      }
      tl.fromTo(el.querySelectorAll(".ch"),
        { opacity: 0, y: o.y ?? -120, rotationX: -70, transformPerspective: 700, filter: "blur(12px)" },
        { opacity: 1, y: 0, rotationX: 0, filter: "blur(0px)", duration: o.d ?? 0.55, ease: o.e ?? "back.out(1.8)", stagger: o.st ?? 0.035 }, t);
    }

    // ---------- emphasis ----------
    function band(sel, t, d = 0.4) { tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: d, ease: "power3.out" }, t); } // highlighter sweep (RTL origin)
    function draw(sel, t, d = 0.5, e = "power2.inOut") { tl.fromTo(sel, { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: d, ease: e }, t); } // needs pathLength="1"
    function strike(pathSel, t, badgeSel) { draw(pathSel, t, 0.35, "power2.out"); if (badgeSel) pop(badgeSel, t + 0.25, { from: 0.2 }); }
    function ringPulse(sel, t, o = {}) { // sel = .ring element(s) inside the activated element
      tl.fromTo(sel, { opacity: 0.9, scale: 1 }, { opacity: 0, scale: o.scale ?? 1.9, duration: o.d ?? 0.7, ease: "power2.out", stagger: o.st ?? 0.18, immediateRender: false }, t);
      hide(sel);
    }
    function stamp(sel, t, camSel) {
      tl.fromTo(sel, { opacity: 0, scale: 2.2, rotation: -14 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.28, ease: "expo.out" }, t);
      if (camSel) shake(camSel, t + 0.08, 14, 6);
    }
    function shake(sel, t, amp = 18, n = 7) {
      for (let i = 0; i < n; i++) {
        const k = 1 - i / n;
        tl.to(sel, { x: (i % 2 ? -1 : 1) * amp * k, y: (i % 3 === 0 ? 1 : -1) * amp * 0.5 * k, duration: 0.035, ease: "none" }, t + i * 0.035);
      }
      tl.to(sel, { x: 0, y: 0, duration: 0.05, ease: "none" }, t + n * 0.035);
    }
    function breathe(sel, t, dur, amp = 0.05, period = 1.6) {
      const reps = Math.max(0, Math.floor(dur / period) - 1);
      tl.fromTo(sel, { scale: 1 }, { scale: 1 + amp, duration: period / 2, ease: "sine.inOut", yoyo: true, repeat: reps * 2 + 1 }, t);
    }
    function drift(sel, t, dur, x, y) { tl.fromTo(sel, { x: 0, y: 0 }, { x, y, duration: dur, ease: "none" }, t); }

    // ---------- data / UI ----------
    // counter that REACHES its value by `byT` (before the voice says the number)
    function counter(sel, startT, byT, from, to, o = {}) {
      const el = Q(sel), p = { v: from };
      const fmt = (v) => { let s = (o.dec ? v.toFixed(o.dec) : Math.round(v)) + (o.suffix ?? ""); return o.ar === false ? s : toAr(s); };
      el.textContent = fmt(from);
      tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.15 }, startT); // hidden until it starts counting
      tl.fromTo(p, { v: from }, { v: to, duration: Math.max(0.2, byT - startT), ease: o.e ?? "power2.out", onUpdate: () => (el.textContent = fmt(p.v)) }, startT);
    }
    function meter(fillSel, t, d, to = 1, o = {}) { tl.fromTo(fillSel, { scaleX: o.from ?? 0 }, { scaleX: to, duration: d, ease: o.e ?? "power2.in", immediateRender: o.from === undefined }, t); }
    // typing into an input: el gets the substring; caret element optional
    function typeText(sel, t, text, cps = 18) {
      const el = Q(sel), p = { n: 0 };
      el.textContent = "";
      tl.fromTo(p, { n: 0 }, { n: text.length, duration: text.length / cps, ease: "none", onUpdate: () => (el.textContent = text.slice(0, Math.round(p.n))) }, t);
    }
    // cursor journey: moves the .cursor by x/y offsets (from its authored left/top), press + ripple
    function cursorTo(sel, t, x, y, d = 0.6) { tl.to(sel, { x, y, duration: d, ease: "power3.inOut" }, t); }
    function click(cursorSel, t, targetSel, rippleSel) {
      tl.to(cursorSel, { scale: 0.85, duration: 0.08, yoyo: true, repeat: 1 }, t);
      if (targetSel) tl.to(targetSel, { scale: 0.93, duration: 0.08, yoyo: true, repeat: 1 }, t);
      if (rippleSel) { hide(rippleSel); tl.fromTo(rippleSel, { opacity: 0.9, scale: 0.3 }, { opacity: 0, scale: 1.6, duration: 0.45, ease: "power2.out", immediateRender: false }, t + 0.04); }
    }
    // toast stack bottom-left: items slide in from the left and push older ones up
    function toasts(list, o = {}) { // list = [{sel, t}], newest at the bottom
      const base = o.bottom ?? 150, gap = o.gap ?? 120;
      list.forEach((it, i) => {
        tl.fromTo(it.sel, { opacity: 0, x: -620 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, it.t);
        for (let j = 0; j < i; j++) tl.to(list[j].sel, { y: -(i - j) * gap, duration: 0.35, ease: "power2.out" }, it.t);
        Q(it.sel).style.bottom = `${base}px`;
      });
    }

    // ---------- camera ----------
    function pushIn(camSel, t, dur, to = 1.04) { tl.fromTo(camSel, { scale: 1 }, { scale: to, duration: dur, ease: "none" }, t); }
    function punch(camSel, t, from = 1.2) { tl.fromTo(camSel, { scale: from }, { scale: 1, duration: 1.0, ease: "expo.out" }, t); }
    function zoomThrough(camSel, t, to = 1.6) { tl.to(camSel, { scale: to, opacity: 0, filter: "blur(16px)", duration: 0.35, ease: "power3.in" }, t); }
    function whipOut(camSel, t, x = 900) { tl.to(camSel, { x, filter: "blur(14px)", duration: 0.4, ease: "power3.in" }, t); }

    return { tl, Q, QA, toAr, rise, maskUp, pop, out, hide, letterDrop, band, draw, strike, ringPulse, stamp, shake, breathe, drift,
             counter, meter, typeText, cursorTo, click, toasts, pushIn, punch, zoomThrough, whipOut };
  };

  // ---------- ROOT helpers (index.html timeline, global time) ----------
  // 3 skewed bars (lime, yellow, teal) sweep right -> left over a section change. Max ~6 per 80 s.
  window.HF_WIPE = function (tl, t, colors = ["var(--lime)", "var(--yellow)", "var(--teal)"]) {
    const w = document.getElementById("wipe");
    w.setAttribute("data-layout-allow-overflow", "");
    colors.forEach((c, i) => {
      const b = document.createElement("i");
      b.style.background = c;
      b.setAttribute("data-layout-allow-overflow", ""); // bars live off-canvas by design
      w.appendChild(b);
      const W = document.getElementById("root").offsetWidth || 1920;
      tl.fromTo(b, { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0); // parked bars stay invisible
      tl.fromTo(b, { x: 0, skewX: -18, opacity: 1 }, { x: -(W * 2.6), skewX: -18, opacity: 1, duration: 0.62, ease: "power3.inOut", immediateRender: false }, t + i * 0.06);
      tl.to(b, { opacity: 0, duration: 0.01 }, t + i * 0.06 + 0.63);
    });
  };
  // editorial chrome driver: section label + "03 / 10" counter + progress line + timecode
  window.HF_CHROME = function (tl, cfg) {
    const root = document.getElementById("chrome");
    if (!root || cfg.enabled === false) { if (root) root.style.display = "none"; return; }
    root.querySelector(".ser").textContent = cfg.series || "";
    const lab = root.querySelector(".lab"), cnt = root.querySelector(".cnt"), tc = root.querySelector(".tc"), bar = root.querySelector(".prog b");
    const secs = cfg.sections || [], total = cfg.duration, pad = (n) => String(n).padStart(2, "0");
    const p = { t: 0 };
    tl.fromTo(p, { t: 0 }, { t: total, duration: total, ease: "none", onUpdate: () => {
      let k = 0; for (let i = 0; i < secs.length; i++) if (p.t >= secs[i].t) k = i;
      if (secs.length) { lab.textContent = secs[k].label; cnt.textContent = `${pad(k + 1)} / ${pad(secs.length)}`; }
      const s = Math.floor(p.t);
      tc.textContent = `${pad(Math.floor(s / 60))}:${pad(s % 60)}`;
      bar.style.transform = `scaleX(${(p.t / total).toFixed(4)})`;
    } }, 0);
  };
  // step tracker: {"t0","t1","items":[{"t","label"}]} -> a right-to-left step bar above the progress line.
  // Done steps turn green with a check, the active step is lime, upcoming steps are muted.
  window.HF_STEPS = function (tl, cfg) {
    const root = document.getElementById("root");
    const bar = document.createElement("div");
    bar.className = "steps";
    bar.setAttribute("data-layout-allow-overlap", "");
    const items = cfg.items || [];
    bar.innerHTML = items.map((it, i) => `<div class="st"><b>${String(i + 1).replace(/[0-9]/g, (d) => "٠١٢٣٤٥٦٧٨٩"[+d])}</b><span>${it.label}</span></div>`).join('<i class="sep"></i>');
    root.appendChild(bar);
    const els = Array.from(bar.querySelectorAll(".st"));
    tl.fromTo(bar, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, cfg.t0);
    tl.to(bar, { opacity: 0, y: 40, duration: 0.35, ease: "power2.in" }, cfg.t1);
    const p = { t: cfg.t0 };
    let last = -2;
    tl.fromTo(p, { t: cfg.t0 }, { t: cfg.t1, duration: cfg.t1 - cfg.t0, ease: "none", onUpdate: () => {
      let k = -1;
      items.forEach((it, i) => { if (p.t >= it.t) k = i; });
      if (k === last) return;
      last = k;
      els.forEach((e, i) => { e.className = "st" + (i < k ? " done" : i === k ? " on" : ""); });
    } }, cfg.t0);
  };
  // stepped film grain (finite, deterministic)
  window.HF_GRAIN = function (tl, total) {
    const G = [[0, 0], [-5, -5], [-10, 5], [5, -10], [-5, 15], [-10, 5], [15, 0], [0, 10], [-15, 0], [10, 5]];
    const g = document.getElementById("grain"), p = { i: 0 };
    tl.fromTo(p, { i: 0 }, { i: Math.floor(total / 0.1), duration: total, ease: "none", onUpdate: () => {
      const v = G[Math.floor(p.i) % G.length]; g.style.transform = `translate(${v[0]}%, ${v[1]}%)`;
    } }, 0);
  };
})();
