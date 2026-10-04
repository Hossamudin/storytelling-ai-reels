// Hossam cartoon kit — 2D character rig + props for HyperFrames scenes (v1).
//
// Loaded by the root index.html after fx.js (new_motion_video.py --kit cartoon adds the tag).
// Inside a scene <template> script:
//   const fx = window.HF_SCENE(4.2);
//   const k = window.HF_CHAR(fx, "#s2-karim", { id: "s2k", look: "karim", skin: "flat", pose: "idle", t0: 4.2 });
//   k.pose(5.0, "point"); k.face(5.0, "happy"); k.talk(5.0, 7.2); k.blinks(4.2, 16);
//   document.querySelector("#s2-house").innerHTML = HF_PROP.house("s2h");
//
// Rules: call a character's methods in CHRONOLOGICAL order (each move tweens from the previous
// state, the way screen.js chains camera moves). Everything is fromTo/immediateRender:false on proxy
// objects that write SVG transform attributes: deterministic and seek-safe, no Math.random.
// Skins: "flat" (default, no outlines) · "line" (ink outlines, paper preset) · "noir" (silhouettes + orange rim).
(function () {
  const INK = "#0d0d0d";
  const LOOKS = {
    karim: { skin: "#e6b08a", hair: "#2a1f1a", top: "#437f3e", top2: "#b3ce65", pants: "#0f4f44", shoes: "#0d0d0d", hood: true },
    doctor: { skin: "#c98f68", hair: "#4a3426", top: "#ffffff", top2: "#136052", pants: "#21423b", shoes: "#3b2a20", coat: true, glasses: true, hairStyle: "short" },
    hossam: { skin: "#d9a37f", hair: "#1c1916", top: "#136052", top2: "#ffec5c", pants: "#0d2b23", shoes: "#0d0d0d", beard: true },
  };
  // pose = joint angles (deg): [upper, fore] per arm, legs, head tilt, torso lean
  const POSES = {
    idle: { aL: [8, -8], aR: [-8, 8], lL: 0, lR: 0, hd: 0, tr: 0 },
    type: { aL: [24, -78], aR: [-24, 78], lL: 0, lR: 0, hd: 4, tr: 0 },
    shock: { aL: [148, 26], aR: [-148, -26], lL: 6, lR: -6, hd: 0, tr: 0 },
    point: { aL: [10, -10], aR: [-96, -4], lL: 0, lR: 0, hd: -6, tr: -2 },
    pointUp: { aL: [10, -10], aR: [-160, -6], lL: 0, lR: 0, hd: -4, tr: 0 },
    think: { aL: [26, -96], aR: [-28, -138], lL: 0, lR: 0, hd: 8, tr: 0 },
    shrug: { aL: [62, -104], aR: [-62, 104], lL: 0, lR: 0, hd: -8, tr: 0 },
    hero: { aL: [34, 96], aR: [-34, -96], lL: 8, lR: -8, hd: -4, tr: 0 }, // fists on hips
    fly: { aL: [10, -10], aR: [-172, 0], lL: 4, lR: -4, hd: -8, tr: 0 },
    clapA: { aL: [34, -112], aR: [-34, 112], lL: 0, lR: 0, hd: 0, tr: 0 },
    clapB: { aL: [30, -96], aR: [-30, 96], lL: 0, lR: 0, hd: 0, tr: 0 },
    selfie: { aL: [8, -8], aR: [-128, -36], lL: 0, lR: 0, hd: -10, tr: -3 },
    phone: { aL: [10, -10], aR: [-26, -150], lL: 0, lR: 0, hd: 10, tr: 0 },
    hold: { aL: [16, -84], aR: [-16, 84], lL: 0, lR: 0, hd: 6, tr: 0 },
    wave: { aL: [8, -8], aR: [-142, -30], lL: 0, lR: 0, hd: -6, tr: 0 },
    sad: { aL: [18, -40], aR: [-18, 40], lL: 0, lR: 0, hd: 14, tr: 4 },
    sitFloor: { aL: [30, -70], aR: [-30, 70], lL: 78, lR: -78, hd: 16, tr: 0, by: 90 }, // by = body drop (sits on the floor)
    cheer: { aL: [156, 10], aR: [-156, -10], lL: 0, lR: 0, hd: -6, tr: 0 },
  };
  const SH = { L: [-46, -176], R: [46, -176] };            // shoulders
  const EL = { L: [-50, -128], R: [50, -128] };            // elbows (rest)
  const WR = { L: [-52, -86], R: [52, -86] };              // wrists (rest)
  const HIP = { L: [-18, -92], R: [18, -92] };
  const NECK = [0, -190];

  function skinColors(look, skin) {
    const c = Object.assign({}, LOOKS[look] || LOOKS.karim);
    if (skin === "noir") {
      const s = "#041614";
      Object.assign(c, { skin: s, hair: s, top: s, top2: s, pants: s, shoes: s, coatFill: s, rim: "#ff5a33", eye: "#ffec5c" });
    }
    c.line = skin === "line" ? INK : skin === "noir" ? "#ff5a33" : "none";
    c.lw = skin === "line" ? 5 : skin === "noir" ? 3 : 0;
    c.eye = c.eye || INK;
    return c;
  }

  // limb = an ink "outline" line under a colored line when the skin has outlines
  function limb(x1, y1, x2, y2, w, col, c) {
    const out = c.lw ? `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c.line}" stroke-width="${w + c.lw * 2}" stroke-linecap="round"/>` : "";
    return out + `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`;
  }
  const st = (c) => (c.lw ? ` stroke="${c.line}" stroke-width="${c.lw}" stroke-linejoin="round"` : "");

  function characterSVG(id, c, o) {
    const arm = (s) => {
      const [sx, sy] = SH[s], [ex, ey] = EL[s], [wx, wy] = WR[s];
      return `<g id="${id}-a${s}">${limb(sx, sy, ex, ey, 24, c.top, c)}
        <g id="${id}-f${s}">${limb(ex, ey, wx, wy, 21, c.top, c)}<circle cx="${wx}" cy="${wy + 4}" r="12.5" fill="${c.skin}"${st(c)}/>
        ${s === "R" && o.prop === "phone" ? `<rect x="${wx - 9}" y="${wy - 22}" width="18" height="30" rx="4" fill="#0d2b23" stroke="#b3ce65" stroke-width="3"/>` : ""}</g></g>`;
    };
    const leg = (s) => {
      const [hx, hy] = HIP[s], fx = hx * 1.15;
      return `<g id="${id}-l${s}">${limb(hx, hy, fx, -16, 27, c.pants, c)}<ellipse cx="${fx + (s === "L" ? -6 : 6)}" cy="-9" rx="21" ry="11" fill="${c.shoes}"${st(c)}/></g>`;
    };
    const torso = c.coat
      ? `<path d="M -46 -178 Q -48 -188 -30 -190 L 30 -190 Q 48 -188 46 -178 L 50 -70 L -50 -70 Z" fill="${c.coatFill || c.top}"${st(c)}/>
         <path d="M -14 -190 L 0 -150 L 14 -190 Z" fill="${c.top2}"/><line x1="0" y1="-150" x2="0" y2="-74" stroke="${c.lw ? c.line : "#cfd6cf"}" stroke-width="3"/>
         <path d="M -22 -188 Q -34 -150 -14 -128" fill="none" stroke="#5a6b62" stroke-width="4" stroke-linecap="round"/><circle cx="-14" cy="-126" r="6" fill="#8aa39b"/>`
      : `<path d="M -46 -178 Q -48 -190 -30 -192 L 30 -192 Q 48 -190 46 -178 L 42 -98 Q 42 -86 30 -86 L -30 -86 Q -42 -86 -42 -98 Z" fill="${c.top}"${st(c)}/>
         ${c.hood ? `<path d="M -30 -192 Q 0 -168 30 -192" fill="none" stroke="${c.top2}" stroke-width="7" stroke-linecap="round"/><line x1="-8" y1="-180" x2="-10" y2="-150" stroke="${c.top2}" stroke-width="4" stroke-linecap="round"/><line x1="8" y1="-180" x2="10" y2="-150" stroke="${c.top2}" stroke-width="4" stroke-linecap="round"/>` : ""}
         <rect x="-40" y="-104" width="80" height="12" rx="6" fill="${c.top2}" opacity="${c.lw && !c.rim ? 1 : 0.55}"/>`;
    const hair = c.hairStyle === "short"
      ? `<path d="M -46 -246 Q -46 -290 0 -290 Q 46 -290 46 -246 Q 40 -270 0 -268 Q -40 -270 -46 -246 Z" fill="${c.hair}"${st(c)}/>`
      : `<path d="M -49 -238 Q -54 -296 2 -296 Q 54 -294 49 -240 Q 44 -262 22 -266 Q 26 -254 12 -250 Q 2 -266 -18 -262 Q -38 -262 -49 -238 Z" fill="${c.hair}"${st(c)}/>`;
    const face = `
      <circle cx="-45" cy="-236" r="9" fill="${c.skin}"${st(c)}/><circle cx="45" cy="-236" r="9" fill="${c.skin}"${st(c)}/>
      <circle cx="0" cy="-238" r="46" fill="${c.skin}"${st(c)}/>
      ${c.beard ? `<path d="M -40 -232 Q -38 -196 0 -192 Q 38 -196 40 -232 Q 30 -210 0 -208 Q -30 -210 -40 -232 Z" fill="${c.hair}"/>` : ""}
      ${hair}
      ${c.rim ? `<path d="M 30 -270 Q 50 -250 44 -214" fill="none" stroke="${c.rim}" stroke-width="4" stroke-linecap="round"/>` : ""}
      <g id="${id}-eyes"><ellipse cx="-16" cy="-238" rx="6" ry="8.5" fill="${c.eye}"/><ellipse cx="16" cy="-238" rx="6" ry="8.5" fill="${c.eye}"/>
        ${c.rim ? "" : `<circle cx="-14" cy="-241" r="2.2" fill="#fff"/><circle cx="18" cy="-241" r="2.2" fill="#fff"/>`}</g>
      <g id="${id}-eyesH" style="opacity:0"><path d="M -23 -236 Q -16 -246 -9 -236" fill="none" stroke="${c.eye}" stroke-width="5" stroke-linecap="round"/><path d="M 9 -236 Q 16 -246 23 -236" fill="none" stroke="${c.eye}" stroke-width="5" stroke-linecap="round"/></g>
      ${c.glasses ? `<g fill="none" stroke="${INK}" stroke-width="3.5"><circle cx="-16" cy="-238" r="14"/><circle cx="16" cy="-238" r="14"/><line x1="-2" y1="-238" x2="2" y2="-238"/></g>` : ""}
      <line id="${id}-bL" x1="-25" y1="-258" x2="-8" y2="-258" stroke="${c.rim ? c.rim : INK}" stroke-width="5" stroke-linecap="round"/>
      <line id="${id}-bR" x1="8" y1="-258" x2="25" y2="-258" stroke="${c.rim ? c.rim : INK}" stroke-width="5" stroke-linecap="round"/>
      ${c.rim ? "" : `<path d="M -3 -228 Q 0 -222 4 -226" fill="none" stroke="#b8805c" stroke-width="3" stroke-linecap="round"/>`}
      <g fill="none" stroke="${c.rim ? c.rim : "#3a1410"}" stroke-width="5" stroke-linecap="round">
        <path id="${id}-m-smile" d="M -14 -216 Q 0 -204 14 -216"/>
        <path id="${id}-m-frown" d="M -12 -207 Q 0 -217 12 -207" style="opacity:0"/>
        <path id="${id}-m-flat" d="M -10 -212 L 10 -212" style="opacity:0"/>
        <path id="${id}-m-smirk" d="M -10 -213 Q 4 -210 14 -218" style="opacity:0"/>
      </g>
      <path id="${id}-m-grin" d="M -17 -219 Q 0 -196 17 -219 Z" fill="#3a1410" style="opacity:0"/>
      <ellipse id="${id}-m-open" cx="0" cy="-211" rx="9" ry="12" fill="#3a1410" style="opacity:0"/>
      <ellipse id="${id}-m-talk" cx="0" cy="-213" rx="10" ry="8" fill="#3a1410" style="opacity:0"/>`;
    const cape = o.cape ? `<g id="${id}-cape" style="opacity:0"><path d="M -40 -186 L 40 -186 Q 74 -110 84 -30 Q 0 -10 -84 -30 Q -74 -110 -40 -186 Z" fill="#ff5a33"${st(c)}/><path d="M -40 -186 L 40 -186 L 30 -172 L -30 -172 Z" fill="#d93a2b"/></g>` : "";
    return `<svg id="${id}" viewBox="-150 -320 300 330" width="100%" height="100%" overflow="visible" style="overflow:visible">
      <ellipse id="${id}-sh" cx="0" cy="-2" rx="66" ry="11" fill="rgba(0,0,0,.22)"/>
      <g id="${id}-body">${cape}${leg("L")}${leg("R")}<g id="${id}-torso">${torso}<rect x="-10" y="-200" width="20" height="16" fill="${c.skin}"/>
        <g id="${id}-head">${face}</g>${arm("L")}${arm("R")}</g></g></svg>`;
  }

  // ---------------------------------------------------------------- rig
  window.HF_CHAR = function (fx, mountSel, o = {}) {
    const id = o.id, tl = fx.tl, Q = fx.Q;
    const c = skinColors(o.look || "karim", o.skin || "flat");
    Q(mountSel).innerHTML = characterSVG(id, c, o);
    Q(mountSel).setAttribute("data-layout-allow-overflow", "");
    const g = (n) => Q(`#${id}-${n}`);
    const p0 = Object.assign({}, POSES.idle, POSES[o.pose || "idle"] || {}, { by: (POSES[o.pose] || {}).by || 0 });
    // joints: proxy objects whose onUpdate writes the SVG transform attribute
    const J = {};
    const joint = (key, el, init, render) => { J[key] = { el, v: Object.assign({}, init), render }; render(el, J[key].v); };
    const rot = (ox, oy) => (el, v) => el.setAttribute("transform", `rotate(${v.a.toFixed(2)} ${ox} ${oy})`);
    joint("aL", g("aL"), { a: p0.aL[0] }, rot(...SH.L));
    joint("fL", g("fL"), { a: p0.aL[1] }, rot(...EL.L));
    joint("aR", g("aR"), { a: p0.aR[0] }, rot(...SH.R));
    joint("fR", g("fR"), { a: p0.aR[1] }, rot(...EL.R));
    joint("lL", g("lL"), { a: p0.lL }, rot(...HIP.L));
    joint("lR", g("lR"), { a: p0.lR }, rot(...HIP.R));
    joint("hd", g("head"), { a: p0.hd }, rot(...NECK));
    joint("tr", g("torso"), { a: p0.tr }, rot(0, -92));
    joint("bd", g("body"), { x: 0, y: p0.by, sx: 1, sy: 1 }, (el, v) => el.setAttribute("transform", `translate(${v.x.toFixed(2)} ${v.y.toFixed(2)}) scale(${v.sx.toFixed(3)} ${v.sy.toFixed(3)})`));
    // eyes: s = size (expressions), k = lid (blinks); one joint so the two never overwrite each other
    joint("ey", g("eyes"), { s: 1, k: 1 }, (el, v) => el.setAttribute("transform", `translate(0 -238) scale(${v.s.toFixed(3)} ${(v.s * v.k).toFixed(3)}) translate(0 238)`));
    joint("bLr", g("bL"), { a: 0 }, rot(-16, -258));
    joint("bRr", g("bR"), { a: 0 }, rot(16, -258));

    function tw(key, t, to, d = 0.35, ease = "power2.inOut") {
      const j = J[key];
      const from = Object.assign({}, j.v);
      Object.assign(j.v, to);
      const proxy = Object.assign({}, from);
      tl.fromTo(proxy, from, Object.assign({}, to, { duration: d, ease, immediateRender: false, onUpdate: () => j.render(j.el, proxy) }), t);
    }
    // opacity switch on SVG parts (mouths, eyes, cape), tracked so every switch has an explicit from-state
    const vis = {};
    ["m-smile", "m-frown", "m-flat", "m-smirk", "m-grin", "m-open", "m-talk", "eyesH", "eyes", "cape"].forEach((n) => (vis[n] = (n === "m-smile" || n === "eyes") ? 1 : 0));
    function show(n, t, on, d = 0.06) {
      if (!g(n) || vis[n] === (on ? 1 : 0)) return;
      tl.fromTo(g(n), { opacity: vis[n] }, { opacity: on ? 1 : 0, duration: d, immediateRender: false }, t);
      vis[n] = on ? 1 : 0;
    }
    const FACES = { // mouth, eyes, brow angles, eye scale
      neutral: ["m-flat", "eyes", 0, 0, 1], happy: ["m-smile", "eyesH", 0, 0, 1], grin: ["m-grin", "eyesH", -6, 6, 1],
      shock: ["m-open", "eyes", -16, 16, 1.32], sad: ["m-frown", "eyes", -18, 18, 0.92], worried: ["m-frown", "eyes", -12, 12, 1.05],
      smirk: ["m-smirk", "eyes", 8, -10, 1], smile: ["m-smile", "eyes", 0, 0, 1], angry: ["m-frown", "eyes", 16, -16, 1],
    };
    let mouth = "m-smile", eyes = "eyes";
    if (o.face && FACES[o.face]) { // initial expression (static markup state, no tween)
      const f = FACES[o.face];
      [["m-smile", 0], [f[0], 1]].forEach(([n, on]) => { g(n).style.opacity = on; vis[n] = on; });
      if (f[1] === "eyesH") { g("eyes").style.opacity = 0; g("eyesH").style.opacity = 1; vis.eyes = 0; vis.eyesH = 1; }
      mouth = f[0]; eyes = f[1];
      J.bLr.v.a = f[2]; J.bRr.v.a = f[3]; J.bLr.render(J.bLr.el, J.bLr.v); J.bRr.render(J.bRr.el, J.bRr.v);
      J.ey.v.s = f[4]; J.ey.render(J.ey.el, J.ey.v);
    }
    const api = {
      id, colors: c,
      pose(t, name, d = 0.35, ease = "back.out(1.6)") {
        const p = Object.assign({}, POSES.idle, typeof name === "string" ? POSES[name] : name);
        tw("aL", t, { a: p.aL[0] }, d, ease); tw("fL", t, { a: p.aL[1] }, d, ease);
        tw("aR", t, { a: p.aR[0] }, d, ease); tw("fR", t, { a: p.aR[1] }, d, ease);
        tw("lL", t, { a: p.lL }, d, ease); tw("lR", t, { a: p.lR }, d, ease);
        tw("hd", t, { a: p.hd }, d, ease); tw("tr", t, { a: p.tr }, d, ease);
        if ((p.by || 0) !== J.bd.v.y) tw("bd", t, { y: p.by || 0 }, d, "power2.inOut");
        return api;
      },
      face(t, name) {
        const f = FACES[name] || FACES.neutral;
        if (f[0] !== mouth) { show(mouth, t, false); show(f[0], t, true); mouth = f[0]; }
        if (f[1] !== eyes) { show(eyes, t, false); show(f[1], t, true); eyes = f[1]; }
        tw("bLr", t, { a: f[2] }, 0.2); tw("bRr", t, { a: f[3] }, 0.2);
        tw("ey", t, { s: f[4] }, 0.18, "back.out(2)");
        return api;
      },
      // mouth flaps between t0 and t1 (expression mouth hidden meanwhile); deterministic rhythm
      talk(t0, t1, rate = 0.11) {
        show(mouth, t0, false, 0.03); show("m-talk", t0, true, 0.03);
        const m = g("m-talk"), n = Math.max(1, Math.floor((t1 - t0) / rate));
        const p = { s: 0.3 };
        const r = () => m.setAttribute("transform", `translate(0 -213) scale(1 ${p.s.toFixed(3)}) translate(0 213)`);
        r();
        tl.fromTo(p, { s: 0.3 }, { s: 1.15, duration: rate, ease: "sine.inOut", yoyo: true, repeat: n - 1, immediateRender: false, onUpdate: r }, t0);
        show("m-talk", t1, false, 0.03); show(mouth, t1, true, 0.03);
        return api;
      },
      blink(t) { tw("ey", t, { k: 0.08 }, 0.06, "power1.in"); tw("ey", t + 0.07, { k: 1 }, 0.08, "power1.out"); return api; },
      blinks(t0, t1, every = 2.7) { for (let t = t0 + 0.9; t < t1 - 0.2; t += every) api.blink(t); return api; },
      hop(t, h = 40, d = 0.42) {
        tw("bd", t, { sy: 0.9, sx: 1.06 }, 0.08); tw("bd", t + 0.08, { y: -h, sy: 1.06, sx: 0.96 }, d / 2, "power2.out");
        tw("bd", t + 0.08 + d / 2, { y: 0, sy: 1, sx: 1 }, d / 2, "bounce.out");
        return api;
      },
      squash(t) { tw("bd", t, { sy: 0.92, sx: 1.06 }, 0.07); tw("bd", t + 0.07, { sy: 1, sx: 1 }, 0.35, "elastic.out(1,0.4)"); return api; },
      // breathing bob (finite)
      breathe(t0, t1, period = 1.8) { for (let t = t0; t + period <= t1; t += period) { tw("bd", t, { sy: 1.012 }, period / 2, "sine.inOut"); tw("bd", t + period / 2, { sy: 1 }, period / 2, "sine.inOut"); } return api; },
      walk(t0, t1, step = 0.32) {
        let k = 0;
        for (let t = t0; t + step <= t1; t += step, k++) {
          const s = k % 2 ? 1 : -1;
          tw("lL", t, { a: 22 * s }, step, "sine.inOut"); tw("lR", t, { a: -22 * s }, step, "sine.inOut");
          tw("aL", t, { a: 8 - 16 * s }, step, "sine.inOut"); tw("aR", t, { a: -8 - 16 * s }, step, "sine.inOut");
          tw("bd", t, { y: -6 }, step / 2, "sine.out"); tw("bd", t + step / 2, { y: 0 }, step / 2, "sine.in");
        }
        const tEnd = t0 + k * step;
        tw("lL", tEnd, { a: 0 }, 0.15); tw("lR", tEnd, { a: 0 }, 0.15);
        return api;
      },
      clap(t0, t1, beat = 0.22) { let k = 0; for (let t = t0; t + beat <= t1; t += beat, k++) api.pose(t, k % 2 ? "clapB" : "clapA", beat * 0.9, "power2.inOut"); return api; },
      cape(t, flutterUntil) {
        if (!g("cape")) { console.warn(`HF_CHAR ${id}: cape() needs { cape: true } in the options`); return api; }
        show("cape", t, true, 0.2);
        const el = g("cape"), p = { k: 0 };
        const r = () => el.setAttribute("transform", `translate(0 -186) skewX(${p.k.toFixed(2)}) translate(0 186)`);
        r();
        const n = Math.max(1, Math.floor((flutterUntil - t) / 0.5));
        tl.fromTo(p, { k: -6 }, { k: 8, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: n - 1, immediateRender: false, onUpdate: r }, t);
        return api;
      },
    };
    return api;
  };

  // ---------------------------------------------------------------- props (SVG strings; ids prefixed)
  const P = {};
  P.laptop = (id, o = {}) => `<svg viewBox="0 0 420 280" width="100%" height="100%" overflow="visible" style="overflow:visible">
    <path d="M 40 30 Q 40 14 56 14 L 364 14 Q 380 14 380 30 L 380 226 L 40 226 Z" fill="#1d2a27" stroke="${o.line || "none"}" stroke-width="${o.lw || 0}"/>
    <rect id="${id}-scr" x="58" y="32" width="304" height="178" rx="6" fill="#0e3a33"/>
    <g id="${id}-code">${[0, 1, 2, 3, 4, 5].map((i) => `<rect x="${76 + (i % 3) * 18}" y="${50 + i * 26}" width="${[150, 110, 190, 80, 140, 120][i]}" height="11" rx="5" fill="${["#b3ce65", "#ffec5c", "#8cb2a6", "#ff5a33", "#b3ce65", "#8cb2a6"][i]}" opacity=".85"/>`).join("")}</g>
    <rect id="${id}-red" x="58" y="32" width="304" height="178" rx="6" fill="#d93a2b" style="opacity:0"/>
    <g id="${id}-warn" style="opacity:0"><path d="M 210 70 L 262 160 L 158 160 Z" fill="#ffec5c"/><rect x="204" y="98" width="12" height="36" rx="5" fill="#0d0d0d"/><circle cx="210" cy="147" r="7" fill="#0d0d0d"/></g>
    <path d="M 0 226 L 420 226 L 400 262 Q 396 270 384 270 L 36 270 Q 24 270 20 262 Z" fill="#2f4741" stroke="${o.line || "none"}" stroke-width="${o.lw || 0}"/>
    <rect x="170" y="230" width="80" height="10" rx="5" fill="#1d2a27"/></svg>`;
  // house built from blocks: ids -b0..-b11 (drop them in), -roof, -door, -win, -bwin (back window, open), -key slot at the door
  P.house = (id, o = {}) => {
    const blocks = [];
    const cols = 4, rows = 3, bw = 90, bh = 70, x0 = 40, y0 = 210;
    for (let r = 0; r < rows; r++) for (let q = 0; q < cols; q++) {
      const k = r * cols + q, col = ["#437f3e", "#136052", "#b3ce65"][(r + q) % 3];
      blocks.push(`<rect id="${id}-b${k}" x="${x0 + q * bw}" y="${y0 + (rows - 1 - r) * bh}" width="${bw - 4}" height="${bh - 4}" rx="8" fill="${col}" stroke="${o.line || "none"}" stroke-width="${o.lw || 0}"/>`);
    }
    return `<svg viewBox="0 0 440 440" width="100%" height="100%" overflow="visible" style="overflow:visible">
      <g id="${id}-blocks">${blocks.join("")}</g>
      <path id="${id}-roof" d="M 20 214 L 220 70 L 420 214 Z" fill="#ff5a33" stroke="${o.line || "none"}" stroke-width="${o.lw || 0}" stroke-linejoin="round"/>
      <rect id="${id}-chim" x="320" y="104" width="38" height="70" fill="#d93a2b"/>
      <g id="${id}-door"><rect x="186" y="300" width="70" height="116" rx="8" fill="#0d2b23"/><circle cx="242" cy="360" r="6" fill="#ffec5c"/></g>
      <g id="${id}-win"><rect x="66" y="240" width="74" height="60" rx="6" fill="#ffec5c"/><line x1="103" y1="240" x2="103" y2="300" stroke="#0d2b23" stroke-width="6"/><line x1="66" y1="270" x2="140" y2="270" stroke="#0d2b23" stroke-width="6"/></g>
      <g id="${id}-bwin"><rect x="300" y="240" width="74" height="60" rx="6" fill="#0d2b23"/>
        <rect id="${id}-sash" x="300" y="240" width="74" height="60" rx="6" fill="#8cb2a6" stroke="#0d2b23" stroke-width="4" style="${o.open ? "transform:scaleX(.18)" : ""}"/></g>
      ${o.lit ? `<rect x="66" y="240" width="74" height="60" rx="6" fill="#ffec5c" opacity=".35"/>` : ""}
    </svg>`;
  };
  P.key = (id) => `<svg viewBox="0 0 160 70" width="100%" height="100%" overflow="visible" style="overflow:visible">
    <circle cx="36" cy="35" r="26" fill="none" stroke="#ffd23f" stroke-width="13"/><path d="M 60 30 L 150 30 L 150 42 L 136 42 L 136 54 L 124 54 L 124 42 L 110 42 L 110 50 L 98 50 L 98 42 L 60 42 Z" fill="#ffd23f"/>
    <circle cx="36" cy="35" r="26" fill="none" stroke="#fff6b8" stroke-width="3" opacity=".7"/></svg>`;
  P.clock = (id) => `<svg viewBox="0 0 220 220" width="100%" height="100%"><circle cx="110" cy="110" r="100" fill="#f6f4ea" stroke="#0d2b23" stroke-width="12"/>
    ${Array.from({ length: 12 }, (_, i) => { const a = (i * 30 * Math.PI) / 180; return `<line x1="${110 + 78 * Math.sin(a)}" y1="${110 - 78 * Math.cos(a)}" x2="${110 + 88 * Math.sin(a)}" y2="${110 - 88 * Math.cos(a)}" stroke="#0d2b23" stroke-width="${i % 3 ? 4 : 8}" stroke-linecap="round"/>`; }).join("")}
    <line id="${id}-hh" x1="110" y1="110" x2="110" y2="62" stroke="#0d0d0d" stroke-width="11" stroke-linecap="round"/>
    <line id="${id}-mh" x1="110" y1="110" x2="110" y2="38" stroke="#ff5a33" stroke-width="7" stroke-linecap="round"/><circle cx="110" cy="110" r="10" fill="#0d0d0d"/></svg>`;
  P.phone = (id) => `<svg viewBox="0 0 150 280" width="100%" height="100%" overflow="visible" style="overflow:visible"><rect x="5" y="5" width="140" height="270" rx="24" fill="#0d0d0d"/>
    <rect id="${id}-scr" x="15" y="22" width="120" height="236" rx="12" fill="#0e3a33"/><rect x="55" y="12" width="40" height="6" rx="3" fill="#2f4741"/>
    <rect id="${id}-alert" x="15" y="22" width="120" height="236" rx="12" fill="#d93a2b" style="opacity:0"/></svg>`;
  P.shield = (id, o = {}) => `<svg viewBox="0 0 200 230" width="100%" height="100%" overflow="visible" style="overflow:visible">
    <path d="M 100 8 L 186 40 Q 186 150 100 222 Q 14 150 14 40 Z" fill="${o.fill || "#b3ce65"}" stroke="#0d2b23" stroke-width="10" stroke-linejoin="round"/>
    <path id="${id}-ck" d="M 62 112 L 92 142 L 144 86" fill="none" stroke="#0d2b23" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>`;
  // little robot: variant "scanner" (magnifier, orange eye) or "guard" (lime, shield badge)
  P.bot = (id, o = {}) => {
    const guard = o.variant === "guard", body = guard ? "#b3ce65" : "#5a6b62", eye = guard ? "#136052" : "#ff5a33";
    return `<svg viewBox="-100 -230 200 240" width="100%" height="100%" overflow="visible" style="overflow:visible">
      <ellipse cx="0" cy="-2" rx="58" ry="10" fill="rgba(0,0,0,.25)"/>
      <g id="${id}-body"><rect x="-14" y="-40" width="10" height="34" rx="5" fill="#2f4741"/><rect x="4" y="-40" width="10" height="34" rx="5" fill="#2f4741"/>
      <rect x="-50" y="-130" width="100" height="96" rx="26" fill="${body}" stroke="#0d2b23" stroke-width="6"/>
      ${guard ? `<path d="M 0 -116 L 26 -106 Q 26 -70 0 -52 Q -26 -70 -26 -106 Z" fill="#136052"/><path d="M -10 -86 L -2 -78 L 12 -96" fill="none" stroke="#b3ce65" stroke-width="6" stroke-linecap="round"/>` : `<rect x="-26" y="-108" width="52" height="10" rx="5" fill="#2f4741"/><rect x="-26" y="-88" width="34" height="10" rx="5" fill="#2f4741"/>`}
      <g id="${id}-head"><line x1="0" y1="-196" x2="0" y2="-214" stroke="#0d2b23" stroke-width="6"/><circle id="${id}-ant" cx="0" cy="-218" r="9" fill="${guard ? "#ffec5c" : "#ff5a33"}"/>
        <rect x="-44" y="-196" width="88" height="62" rx="22" fill="${body}" stroke="#0d2b23" stroke-width="6"/>
        <rect x="-32" y="-182" width="64" height="32" rx="14" fill="#0d2b23"/>
        <g id="${id}-eye"><circle cx="-12" cy="-166" r="7" fill="${eye}"/><circle cx="12" cy="-166" r="7" fill="${eye}"/></g></g>
      <g id="${id}-arm"><line x1="46" y1="-110" x2="86" y2="-136" stroke="#0d2b23" stroke-width="12" stroke-linecap="round"/>
        ${guard ? "" : `<circle cx="100" cy="-150" r="22" fill="rgba(255,236,92,.25)" stroke="#0d2b23" stroke-width="8"/>`}</g>
      <line x1="-46" y1="-110" x2="-70" y2="-76" stroke="#0d2b23" stroke-width="12" stroke-linecap="round"/></g></svg>`;
  };
  P.safe = (id) => `<svg viewBox="0 0 200 200" width="100%" height="100%" overflow="visible" style="overflow:visible"><rect x="10" y="10" width="180" height="180" rx="18" fill="#2f4741" stroke="#0d2b23" stroke-width="8"/>
    <rect x="28" y="28" width="144" height="144" rx="12" fill="#1d2a27"/>
    <g id="${id}-door"><rect x="28" y="28" width="144" height="144" rx="12" fill="#5a6b62" stroke="#0d2b23" stroke-width="6"/><circle cx="100" cy="100" r="34" fill="none" stroke="#ffec5c" stroke-width="10"/>
    <g id="${id}-dial"><line x1="100" y1="100" x2="100" y2="70" stroke="#ffec5c" stroke-width="8" stroke-linecap="round"/></g></g></svg>`;
  P.cctv = (id) => `<svg viewBox="0 0 200 120" width="100%" height="100%" overflow="visible" style="overflow:visible"><rect x="150" y="20" width="16" height="70" rx="6" fill="#2f4741"/>
    <g id="${id}-head"><rect x="30" y="20" width="130" height="56" rx="14" fill="#f6f4ea" stroke="#0d2b23" stroke-width="6"/><circle cx="46" cy="48" r="16" fill="#0d2b23"/><circle id="${id}-led" cx="138" cy="34" r="7" fill="#ff5a33"/></g></svg>`;
  P.paper = (id, o = {}) => `<svg viewBox="0 0 160 200" width="100%" height="100%" overflow="visible" style="overflow:visible"><path d="M 10 10 L 120 10 L 150 40 L 150 190 L 10 190 Z" fill="#fbfbf7" stroke="#0d2b23" stroke-width="6" stroke-linejoin="round"/>
    <path d="M 120 10 L 120 40 L 150 40" fill="#e3e6d6" stroke="#0d2b23" stroke-width="6" stroke-linejoin="round"/>
    ${[0, 1, 2, 3].map((i) => `<rect x="30" y="${62 + i * 30}" width="${[90, 70, 96, 60][i]}" height="10" rx="5" fill="${o.accent || "#8cb2a6"}"/>`).join("")}
    ${o.badge ? `<circle cx="118" cy="160" r="22" fill="#b3ce65"/><path d="M 107 160 L 115 168 L 130 152" fill="none" stroke="#0d2b23" stroke-width="6" stroke-linecap="round"/>` : ""}</svg>`;
  P.moon = (id, o = {}) => `<svg viewBox="0 0 200 200" width="100%" height="100%" overflow="visible"><defs><mask id="${id}-mk"><rect x="0" y="0" width="200" height="200" fill="#fff"/><circle cx="132" cy="78" r="64" fill="#000"/></mask></defs>
    <circle cx="100" cy="100" r="80" fill="${o.fill || "#fff6b8"}" mask="url(#${id}-mk)"/></svg>`; // crescent via mask: works on any sky colour
  P.crack = (id) => `<svg viewBox="0 0 440 440" width="100%" height="100%" overflow="visible" style="overflow:visible"><path id="${id}-c1" d="M 220 70 L 200 150 L 236 196 L 204 270 L 240 330 L 214 420" fill="none" stroke="#0d0d0d" stroke-width="9" stroke-linejoin="round" pathLength="1"/>
    <path id="${id}-c2" d="M 90 220 L 140 262 L 120 318 L 166 362" fill="none" stroke="#0d0d0d" stroke-width="7" stroke-linejoin="round" pathLength="1"/></svg>`;

  window.HF_PROP = P;
  window.HF_POSES = POSES;
})();
