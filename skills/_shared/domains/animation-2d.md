# 2D animation playbook — characters, whiteboard, cut-out, doodles, Lottie, AI frames

2D here means drawn worlds that move: characters that talk and gesture, whiteboard explainers that draw
themselves, paper cut-out collages, doodle overlays, animated infographics with personality. Everything renders
through HyperFrames (deterministic, frame-exact, offline), so it syncs to the voice like the motion graphics do.

## 1. Pick the technique (ask what the video needs, not what is fashionable)

| Technique | Looks like | Best for | Built with | Cost |
|---|---|---|---|---|
| **Puppet character (SVG rig)** | flat vector mascot/host that blinks, talks, waves, points | a recurring host, kids/education, explainers with a guide | kit `character_2d` template + `lipsync.py` | free |
| **Whiteboard / sketch** | lines draw themselves on paper, a marker reveals items in order | step-by-step teaching, processes, beginners | SVG paths + `fx.draw` (stroke-dashoffset), hand-drawn filter | free |
| **Cut-out / paper collage** | layered paper pieces slide, flip, wobble; stop-motion feel | storytelling, history, playful hooks | images/SVG layers + stepped eases (`steps(n)`), slight rotations | free / images |
| **Doodle overlay** | arrows, circles, stars, underlines scribbled over footage or photos | talking heads, screen recordings, thumbnails come alive | SVG paths drawn on with `fx.draw` | free |
| **Animated infographic** | icons, charts and characters in one flat world | numbers with a story, comparisons | kit + SVG icons + counters | free |
| **Lottie** | designer-made After Effects animation (mascot walk cycle, logo, icons) | when a designer/file exists or a licensed library file fits | `vendor_lib.py lottie` + `window.__hfLottie` | free (license!) |
| **AI-generated frames** | painterly/anime/clay keyframes, moved by image→video | a cinematic hero shot, a style code can't draw | AI image (character sheet) → image→video clip (paid, approval) | credits |
| **Frame-by-frame (sprite sheet)** | hand-drawn boiling lines, classic cel feel | short loops (fire, blink, splash) | sprite sheet `<img>` + `steps()` background-position | free |

Mix freely: e.g. a puppet host (rig) presenting a whiteboard diagram that draws itself, with one AI-generated
painted hero shot for the hook.

## 2. Character design that animates well

- **Separate every moving part** into its own SVG group: body, head, eyes, eyelids, brows, mouth shapes, each arm
  (upper/lower if it bends), hands, legs. Draw limbs pointing DOWN from the joint — easy pivots.
- **Pivots:** GSAP ignores CSS `transform-origin` on SVG. Either `gsap.set(el, {svgOrigin: "x y"})` (viewBox coords) or
  wrap a limb in `<g transform="translate(jointX jointY)">` with a transparent disc centered on 0,0 and rotate about
  `50% 50%` (the kit template does this). Put `data-layout-allow-orbit` on limbs (they rotate about joints on purpose).
- **Mouth set** (energy lip-sync): `X` closed/rest · `M` pressed (consonant closures) · `A` mid-open · `O` wide. Add
  more shapes (E smile, F/V teeth on lip, U round) for close-ups.
- **Style:** brand colors on clothes/props (tokens: `var(--teal)` etc.), neutral flat skin tones, 2–3 shades per
  part max, thick friendly outlines or none. Simple faces read better small (9:16 phones).
- **No realistic people** unless it's the creator's own photo; no characters copied from existing IP; check the brand
  avoid list (some creators avoid drawing faces at all → use objects as characters: a talking mic, a coffee cup).
- Make a **character sheet** before animating a series: a scene with the rig in 4 poses/expressions side by side
  (front, wave, point, surprised) + the mouth set + color swatches → `npx hyperframes snapshot --at <t>` → save the PNG
  AND the rig markup to the library (`lib.py add sheet.png --type img --subject <name>-character-sheet`,
  `lib.py add s1.html --type code --subject <name>-rig`) so episode 2 looks like episode 1.
- Head gestures (nod, shake, tilt) go on `#<id>-headIn`; the idle sway stays on `#<id>-head` — they never fight.

## 3. Acting — the 12 principles that matter most on a deadline

1. **Anticipation**: a small move opposite before the big one (arm dips before the wave).
2. **Squash & stretch**: on landings and pops (scaleY 0.9 → 1.05 → 1), never on faces.
3. **Overlap / follow-through**: hands and hair finish 0.05–0.15 s after the arm.
4. **Ease in/out** everywhere (`power2.inOut`); `back.out` for pops; never linear except mechanical things.
5. **Arcs**: limbs travel on arcs (rotation does it for free).
6. **Secondary action**: breathing (scaleY 1.012), head sway ±2°, blinks every 3–4.5 s (irregular, seeded).
7. **Timing to the voice**: gestures land 0.1–0.2 s BEFORE the stressed word; point at what the voice names.
8. **Holds**: a still pose for 0.3–0.6 s after a big gesture reads as confidence; constant motion reads as nervous.
9. **Staging**: character on one side, the thing they talk about on the other; mirror for RTL (the template does).
10. **Eye-lines**: pupils look at the element being introduced (tween the pupil group x/y a few px).

## 4. Workflow

```bash
python engine/pipeline/new_motion_video.py <name> --part <part> --voice <wav> --aspect 16:9 --preset light
# scenes.json: {"id":"s1","start":0,"duration":8.8,"title":"…","template":"character_2d"}  (+ other scenes)
python engine/pipeline/motion_sync.py <name> --part <part>
python engine/pipeline/lipsync.py <name> --part <part>          # mouth keys from the voice -> assets/js/lipsync.js (auto-linked)
# edit compositions/s1.html: swap shapes for your character, add gestures on word times (transcript/<part>_words.json)
cd projects/<name>/<part> && npx hyperframes check && npx hyperframes snapshot --at 1,2.6,5
```
- Gesture timing: read word times from `transcript/<part>_words.json` and place `tl.to(...)` at `word.s - 0.15`.
- Several scenes with the same character: copy the rig markup into each scene (unique ids per scene: the template
  prefixes everything with the scene id) or keep the character in one long base scene and swap backgrounds above/below it.
- Walk cycles: animate legs/arms in place with a 0.5–0.6 s yoyo cycle and move the whole character with `x` at a
  speed matched to the stride (feet must not slide). Lottie is better for complex walks.

## 5. Whiteboard / sketch recipe

- Paper background (light preset), ink color for lines, brand accent for highlights.
- Draw SVG paths with `fx.draw(sel, t, d)` (stroke-dashoffset). Order: outline → details → label → color fill fades in.
- Hand-drawn wobble: an SVG `<filter>` with `feTurbulence` + `feDisplacementMap` (static seed = deterministic), or
  draw slightly imperfect paths.
- A hand/marker cursor following the stroke: animate a marker image along the path with `MotionPathPlugin` only if
  it is vendored; otherwise skip the hand — the drawing line alone reads fine.
- Pace: one idea drawn per sentence; erase/wipe between sections (paper slides away or a fresh sheet slides in).

## 6. Cut-out / stop-motion recipe

- Layers (background paper, mid props, foreground pieces) at different parallax speeds.
- Stop-motion cadence: `ease: "steps(6)"` on moves, or snap positions every 2 frames (`Math.round(t*12)/12`).
- Tiny random rotations (seeded) per "frame" for the handmade jitter; paper texture + soft drop shadows.
- AI images make great cut-out pieces (clay/paper style, plain background → `remove-background`). Approval gate.

## 7. Lottie

```bash
python <skill>/scripts/vendor_lib.py lottie projects/<name>/<part>     # assets/js/lottie.min.js
```
Then in a scene: `<div id="sX-lottie"></div>` + `lottie.loadAnimation({container, renderer: "svg", loop: false,
autoplay: false, path: "assets/lottie/file.json"})` and `window.__hfLottie.push(anim)`. Every registered animation
plays on composition time (no per-file offset): author the performance at the right time inside the file, or one file
per beat with its own timing. Always set `loop`. Only use files the creator owns or may redistribute; say the source.

## 8. AI-generated 2D (paid → approval)

- Generate a **character sheet** first (same seed/prompt family), then keyframes from it, then image→video for 3–5 s
  hero shots. Keep text out of images. Cut out characters with `remove-background` and animate them in code (cheap,
  controllable) rather than generating every shot as video.
- Prompt skeleton: `<character>, flat 2D vector illustration | cut paper collage | soft clay | anime cel, brand palette
  <hexes>, simple shapes, clean outlines, plain <color> background, full body, no text, no logos`.

## 9. Quality checklist

- [ ] Character never covers the text; text never covers the face. Mirrored for RTL.
- [ ] Mouth moves only while the voice speaks; closed in pauses. Blinks irregular.
- [ ] Every gesture tied to a word; holds after big gestures; nothing jitters unintentionally.
- [ ] `check` clean (limbs carry `data-layout-allow-orbit`), snapshots at gesture peaks reviewed.
- [ ] Character sheet saved to the library for the next episode.
