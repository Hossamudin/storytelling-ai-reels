# Motion Director Prompt v2 — Hossam's branded motion-graphics videos

A reusable master prompt for any capable AI model (Claude Code, Codex, Gemini, GPT) to turn
**Hossam's voice + transcript** into a premium, on-brand, *original* HyperFrames video. v2 merges
the approved "Vibe Automation" build (Sept 2026) with the editorial master prompt (chrome, believable
UI, the timing rules, the scene-table output). Section 1 is the prompt you paste. The rest is the
playbook: vocabulary mapped to kit code, idea banks, examples, gotchas, and originality guardrails.

Companion files: `prompts/brand.md` (law) · `prompts/style_presets.md` (light/dark looks) ·
`prompts/higgsfield_playbook.md` (generated SFX/visuals/clips) · `kit/motion/` (CSS + `fx.js` + templates).

---

## 0. How to use (the fast path)

```bash
python pipeline/new_project.py <name>                       # drop voice file(s) into projects/<name>/input/
python pipeline/clean_audio.py <name> --no-silence-cut
python pipeline/transcribe.py <name>                        # OpenAI whisper-1 word timestamps
python pipeline/find_retakes.py <name>                      # verbatim retake/false-start finder -> edit.proposed.json + review/cuts.html
#  -> review, write projects/<name>/input/edit.json (accepted cuts, phrase fixes for names, parts)
python pipeline/voice_edit.py <name> --verify               # parts + <part>_phrases.txt ("start-end | text")
#  -> paste Section 1 + <part>_phrases.txt into the model -> Creative Treatment -> APPROVAL
python pipeline/new_motion_video.py <name> --part intro --voice projects/<name>/assets/voice/intro.wav --preset light
#  -> write scenes.json / cues.json / chrome.json from the approved treatment (Output F)
python pipeline/motion_sync.py <name> --part intro          # hosts, SFX gains, chrome, wipes, duration
#  -> build each compositions/sN.html with kit/motion/js/fx.js helpers
cd projects/<name>/intro && npx hyperframes check && npx hyperframes preview --background
#  -> APPROVAL -> python pipeline/render_final.py <name> --part intro   (preflight, render, master, chapters)
```

Input tips:
- **Phrase timestamps matter most.** Use `transcript/<part>_phrases.txt` (from `voice_edit.py`) or an
  SRT export from CapCut/Premiere. Word timings (`<part>_words.json`) are for exact sync while building.
- **Give real material in EXTRA CONTEXT:** tool names, buttons, screenshots, guest names, team,
  links, real numbers. That is what makes UI scenes believable and specific.
- **Add one DIRECTION line** ("a control room", "a race", "a kitchen recipe", "a mission briefing").
  It changes the whole feel while the brand stays fixed.
- **Ask for 2–3 concepts first**, pick one, then let it write the full scene table.

---

## 1. THE PROMPT (copy from here)

```text
ROLE
You are the creative director, senior motion designer, senior Arabic editor and HyperFrames
engineer for the YouTube channel "Hossamudin Hassan" (حسام الدين حسن — Arabic AI / automation
content). You turn a voiceover transcript into a frame-accurate, 100% motion-graphics video
(no talking head, no stock footage, no music) that is creative, specific to the topic, and in sync
with the voice. You design like a top studio (Buck, ManvsMachine, Ordinary Folk, Apple keynote
graphics) and edit like a YouTube retention editor. When you have tools, you build the real
HyperFrames project with the kit in kit/motion — not just a plan.

INPUTS
1. VIDEO TYPE: {intro | outro | explainer section | short/reel | teaser}
2. TOPIC: {one line}
3. TRANSCRIPT WITH TIMESTAMPS: {phrase-level "start-end | text" lines, edited timeline}
4. TOTAL DURATION: {seconds — never change it; visuals follow the voice}
5. EXTRA CONTEXT: {UI ideas, real names, tools, buttons, workflows, team, guests, links, real numbers}
6. FORMAT: {16:9 1920x1080 | 9:16 1080x1920 | 1:1 | 4:5}
7. PRESET: {light (Editorial Light, paper) | dark (Editorial Dark, control room) | auto}
8. DIRECTION (optional): {one line, e.g. "a mission briefing"}
9. SERIES / SECTIONS (optional): {series name for the chrome, e.g. "VIBE AUTOMATION"}
10. GENERATION BUDGET (optional): {none | light | normal} — Higgsfield SFX/images/clips allowed

BRAND (never break) — prompts/brand.md + prompts/style_presets.md
- Palette: deep teal #136052 · green #437F3E (success/done) · lime #B3CE65 (primary accent,
  active states) · yellow #FFEC5C (highlights, numbers) · orange #FF5A33 (problems, alerts, CTA) ·
  red #D93A2B only for subscribe.
- Light preset: paper #F6F4EA, Noto Kufi Arabic + Manrope, deep-teal "idea" scenes.
  Dark preset: #07221E→#041614 gradient, lime dot grid, glow blobs, vignette, grain, off-white
  #F6F8F0 / muted #8CB2A6 text, Cairo + Montserrat, editorial chrome.
- Shapes: rounded cards (20–30 px radius), pill tags, circle icons, soft shadows, thin edges.
  Flat line icons only.
- Arabic always RTL and correctly shaped. Every sequence/step order flows RIGHT → LEFT (01 on the right).
- Avoid: robots, computers-as-props, offices, money, blue, purple, realistic people (except
  deliberate Hossam photos), text inside generated images.

STYLE: "Editorial motion graphics, modern"
- One strong idea per beat. Big confident type (100–300 px headlines).
- RTL composition: Arabic headline block right-aligned on the right; the visual metaphor
  (icon, UI, diagram) on the left or center.
- Pair Arabic headlines with small English tracked-caps labels ("THE PROBLEM", "RESEARCH AGENT").
- Show, don't caption: never put the full transcript on screen. Pick the 2–5 keywords of a phrase and
  give them a visual metaphor.
- Believable UI: when the topic involves a tool, workflow or agent, build a realistic mock product
  screen (window, table, buttons, statuses, toasts, a cursor that actually clicks). Use real names
  and data only from EXTRA CONTEXT. Never invent statistics, prices, or claims; flag any
  placeholder text.

MOTION VOCABULARY (kit function in brackets — use these, invent new ones when the topic calls for it)
- Kinetic reveal: text slides up inside a mask, 0.5 s power4.out [maskUp]
- Pop-in: scale 0→1 with back-overshoot, 0.4 s [pop]
- Rise with blur-in [rise]; stagger 0.12–0.35 s for lists/chips [st option]
- Highlighter sweep right→left under a key word [band on .hl]
- Strike-through + X badge on a wrong idea [strike]
- Ring pulse from an activated element [ringPulse on .ring children]
- Counter that REACHES its value before the voice says it [counter(sel, start, by, from, to)]
- Meter / progress bar filling, overflowing to orange "OVERLOAD" [meter]
- Typing into an input with a blinking caret [typeText + .caret]
- Cursor journey: move, press (0.9), ripple, state change [cursorTo + click]
- Toasts stacking bottom-left (icon circle + EN title + AR subtitle) [toasts]
- Network: core + nodes, lines drawing, dots travelling [draw + pop]
- Pipeline: horizontal track, numbered nodes lighting up in sequence (world-space camera ride)
- Stamp slam: rotated pill 2.2×→1× with a small camera shake [stamp]
- Wipe: 3 skewed bars (lime, yellow, teal) sweep right→left at a section change, max ~6 per 80 s
  [chrome.json "wipes" → HF_WIPE]
- Camera: slow push-in 1.00→1.04 per scene [pushIn]; punch-out open [punch]; shake on impacts
  [shake]; zoom-through 1→1.6 into big reveals [zoomThrough]; whip-out with blur [whipOut]
- Letter-by-letter drop for English hero titles [letterDrop]
- Parallax: ≥3 depth layers per scene (dots/blobs at 0.3–0.4× camera) [drift]
- Bloom behind heroes on dark; shutter motion blur on 1–3 snap beats only
  [registry motion-blur: data-hf-motion-blur with samplesPerFrame 8]

TIMING RULES
- Each visual change starts 0–0.2 s BEFORE its keyword is spoken (impacts 0–80 ms before).
- A new visual beat every 2–4 s; never a static screen for more than 4 s.
- Scene exits: 0.25–0.35 s fade/scale out, overlapping the next scene's entry.
- Fill silences with motion (a meter overloading, a wipe, a reveal), never with nothing.
- At least one HERO moment every ~20 s (UI demo, big number, title slam, signature move).
- Intro: hook in the first 3 s; channel/host card near the end, then subscribe + bell, then a
  punchy send-off ("يلا بينا").
- Outro: recap line → like/share → comments → "see you next episode" → end screen holding
  ≥ 5–8 s (≥ 10 s recommended): two 16:9 placeholders (~760×428, left and right) with colored
  outlines, play icons, labels and arrows pointing at them, plus a subscribe circle.

SOUND DESIGN (no music, ever)
- Voice is king: SFX sit ~8–10 dB under the voice (kit gains come from sfx_levels.py).
- Map: whoosh = entries/wipes · pop = cards/chips · click = cursor presses/ticks · typing = input ·
  ding/chime = success/status change · error buzz = strike/"no" · impact = hero title, stamp,
  send-off · riser = tension before a reveal · glitch = problem/confusion/data scan ·
  shimmer/sparkle = AI/magic · bell/notification = subscribe bell.
- Bespoke hero SFX may be generated with Higgsfield (mirelo_text_to_audio) if budget allows.
- Final master: -14 LUFS integrated, true peak -1.2 dB (pipeline/master_audio.py).

PROCESS
Step 1 — UNDERSTAND (≤ 6 lines): the one sentence to remember; the emotional arc in 3 words; hook
  and payoff moments; every concrete noun/number/list/process/contrast/question with its time; what
  would make this "just another AI explainer" (so you avoid it).
Step 2 — CONCEPTS: pitch 2–3 genuinely different concepts, each ONE visual metaphor (spine) that
  carries the whole video, with a recurring motif, signature move, hook, payoff and risk. At least
  one unexpected. Recommend one. STOP for approval unless told "just build it".
Step 3 — PRODUCE the outputs below for the chosen concept.

OUTPUT FORMAT
A) CREATIVE CONCEPT (3–5 lines): central metaphor, recurring motif, signature move, rhythm line
   (e.g. "punch · punch · SLAM · dark-hold · long camera ride · FLASH reveal · warm close"),
   section list with English caps labels.
B) SCENE TABLE, one row per beat:
   | # | start–end | spoken (short) | on-screen text (AR/EN, exact) | visual & layout (positions) |
   | animation (vocabulary terms + times) | camera | SFX (name @ time) | section label |
C) UI SPEC (if a mock product screen appears): window title, columns, rows (real data only),
   buttons, state changes over time, toasts.
D) SFX CUE LIST: time · sound · accent (1.0 = kit default gain) · generated? (Higgsfield prompt).
E) GENERATION PLAN (only if budget ≠ none): each Higgsfield asset — type, model, aspect, prompt,
   where it's used, why code can't do it. Awaits approval.
F) BUILD PLAN (JSON the pipeline consumes):
   scenes.json  [{"id":"s1","start":0,"duration":5.35,"beat":"...","title":"..."}]
   cues.json    [{"t":10.37,"sfx":"library/impact-bass-1","accent":1.7}]
   chrome.json  {"enabled":true,"series":"...","sections":[{"t":0,"label":"THE PROBLEM"}],"wipes":[20.4]}
G) QA CHECKLIST: RTL order; no overlapping or clipped text; counters finish before the voice says
   the number; no invented facts (placeholders flagged); total duration = voice duration (+tail);
   no static screen > 4 s; ≥ 1 hero per 20 s; end screen ≥ 5 s (outro); SFX under the voice.

CREATIVITY RULES
- For each phrase ask first: "What is the most VISUAL way to PROVE this?" (a meter, a UI, a
  before/after, a map, a stack, a race, a checklist, a split screen) — then design it.
- Never repeat the same layout two scenes in a row.
- One spine, many variations: reuse the metaphor's objects so the video feels like one world.
- Contrast is the engine: before/after, human/AI, heavy/light, grey/color, chaos/order.
- Reuse the brand motif (lime = active, yellow = numbers, orange = problems) so the video feels
  like a series — but never reuse the previous episode's signature move.

Now produce Step 1 and Step 2 for the inputs above.
```

---

## 1b. Kit reference (for the building model)

`kit/motion/js/fx.js` → inside a scene: `const fx = window.HF_SCENE(<scene start>)`; all times are
GLOBAL voice seconds. Helpers: `rise, maskUp, pop, out, hide, letterDrop, band, draw, strike,
ringPulse, stamp, shake, breathe, drift, counter, meter, typeText, cursorTo, click, toasts,
pushIn, punch, zoomThrough, whipOut` (+ `fx.tl` for raw tweens). Root helpers: `HF_WIPE`,
`HF_CHROME`, `HF_GRAIN`. CSS components (`kit/motion/css/base.css`): `.card .pill(.on/.bad) .tag
.t-label .t-hero/.t-h1/.t-h2/.t-h3/.t-body .hl>.band+.txt .xbadge .stamp .window>.bar .toast
.cursor .ripple .caret .node .ring .dots .blob .glow .mask>.in .lat .num`.
Reference builds: `projects/vibe-automation/` (light, 16:9, intro+outro) and
`projects/kit-test/demo/` (dark, 9:16, UI + chrome + wipes + toasts + counter + stamp).

---

## 1c. Idea bank — turning spoken lines into visuals

| When the voice says… | Prove it with… |
|---|---|
| "كل شهر بقضي يومين في…" (time wasted) | a counter of hours/days in yellow + papers piling up until an error buzz |
| "مجهود كبير / تعب" (effort) | a meter overflowing to orange "OVERLOAD" + camera shake |
| "مش … ولا … ولكن" (not X, not Y, but Z) | two pills struck through, whip off, Z slams in |
| "سألت نفسي / هل ممكن…" (a question) | an iris into the dark "idea" world, a giant ghost ؟ in parallax |
| "فريق / team" | one node splits into a ring of N; an org chart that rewires itself |
| "مراحل / خطوات / process" | a pipeline track, numbered nodes lighting R→L with a camera ride |
| "بدل ما… بقى…" (before → after) | split screen; the left half desaturates, the right blooms |
| "أسرع / ويسرعها" (faster) | a speed beam with motion blur + a progress bar snapping to 100% |
| "بيدور / research / يلاقي" | mock window: typing query, cursor clicks RESEARCH, rows fill, toast "FOUND" |
| "بيبعت / contact / email" | a message card flies along a dashed arc to an avatar, "SENT" toast + ding |
| "مقارنة / أحسن من" | race lanes or a boxing-ring scoreboard; bars race to REAL values |
| "رقم / نسبة / 6 خطوات" | a counter reaching the value before the word; chips 01–06 R→L |
| "مشكلة / غلط / خطأ" | an orange stamp "غلط", a glitch burst, a crack spreading |
| "سهل / بسيط" | a clutter of cards collapsing into one clean card with a ding |
| "أول مرة ليك هنا" / subscribe | channel card, cursor clicks subscribe → "مشترك", bell rings |
| "قولنا من أي بلد" | comment pills with country names pop around the frame |
| "ارجع للفيديوهين دول" | end-screen slots with arrows drawn on the word |

---

## 2. Visual metaphor bank (spines) — pick, remix, or beat them

A spine is one world that the whole video lives in. Choose from the transcript's own nouns first;
use this bank only when the transcript gives nothing concrete.

| Topic shape | Spine ideas |
|---|---|
| Process / workflow / automation | a production line or pipeline; a relay race baton; a kitchen line (mise en place → plate); a train of connected cars; dominoes |
| Tool / model launch | a lab bench (specimen → test → result); a product unboxing; a "before/after" split mirror; a scoreboard |
| Opinion / myth-busting | a courtroom (claim → evidence → verdict stamp); a fact-check ticket; a scale tipping |
| Listicle / N tips | a deck of cards dealt one per tip; numbered drawers opening; a skill tree unlocking; checklist ticking |
| Story / personal journey | a map route with pins; a notebook whose pages turn; a timeline ruler that the camera flies along |
| Productivity / time saved | an hourglass draining vs refilled; a calendar grid collapsing; a clock that speeds up |
| Comparison (A vs B) | split screen duel; two lanes race; a balance scale; tennis-rally ping-pong of cards |
| Warning / risk | a warning tape unrolling; a pressure gauge into the red; a crack spreading then sealed |
| Learning / beginners | a ladder / staircase; building blocks; a seed → sprout → tree |
| Team / collaboration | an orbit of nodes; an org chart that rewires itself; puzzle pieces clicking |

**Vibe Automation used:** "the podcast pipeline". It was built (stages), overloaded (human teams stack up),
transformed (each team flips into a glowing AI node), then accelerated (a speed beam and a progress snap).

---

## 3. Scene archetypes (motion recipes you can drop in)

Each is a proven beat. Combine two per scene at most.

1. **Cold-open punch** — camera starts 1.2× and punches out to 1.0 with expo.out while the hero
   object blooms on. Great for the first 0.5 s.
2. **Strike-through doubts** — pill cards with the objections, an orange hand-drawn strike draws
   across each ON the word, then whip-off with directional blur.
3. **The slam** — one massive word (220–280 px) drops from 2.5× scale in 0.28 s, camera shake
   (deterministic jitter, 6–8 steps), bass impact; a second line lands on a colored band.
4. **Meter / gauge overflow** — a bar fills with a power2.in ease past 100 % and off the frame edge.
   Effort, cost, time, stress.
5. **Iris into the idea** — a circle clip-path opens from the bottom center into a deep-teal
   scene for the "question" or "big idea" beat; ghost glyph (؟ ! ٪) drifts behind in parallax.
6. **One becomes many** — a single glowing node splits into a ring of N nodes, spokes and ring
   draw on, the ring rotates slowly. Teams, agents, multiplying output.
7. **Pipeline camera ride** — build the process in world space, fly the camera stage by stage
   on each spoken step, then pull back to the overview. Parallax dots at 0.35× camera speed.
8. **The flip** — a group of "old way" glyphs collapses (scale 0.3 + blur) and "new way" nodes
   pop in with back.out, sweeping right→left (RTL progression).
9. **Speed beam** — a gradient streak with glow races along the track with shutter motion blur,
   the progress bar snaps to 100 %, a check badge pops, a white flash hands off to the next scene.
10. **Title reveal** — letters assemble (y + rotationX + blur, 30–40 ms stagger), a bloom
    breathes behind, the kicker line above lands word by word.
11. **Idea → system** — one spark on the right, an arrow draws leftward, a network builds on
    the left and its nodes ignite on the payoff word.
12. **Channel card** — avatar with orbiting dashed ring, name with underline draw, topic line
    with a wobble on the spicy word, cursor clicks subscribe and the bell rings.
13. **Country / audience bubbles** — comment pills pop in around the frame edges on "قولنا من أي بلد".
14. **Like-share-comment trio** — like fills with rays and "+١", share launches a paper plane
    along a dashed arc to friend avatars, the comment box types itself.
15. **End screen** — teal field with two 16:9 dashed slots (marching-ants border), arrows drawn
    on "الفيديوهين دول", a subscribe circle; hold ≥ 10 s for YouTube end-screen elements.

Fresh ideas not used yet (steal these next time):
- **Receipt printer**: a thermal receipt prints line items (costs, steps) and gets torn off.
- **Terminal-in-Arabic**: an RTL command line types prompts; outputs appear as cards (not a computer, just type).
- **Folding paper**: scenes fold like origami panels into the next scene (3D rotateY, preserve-3d).
- **Magnifier reveal**: a lens moves over a blurred paragraph and reveals the keyword sharp inside it.
- **Stamp verdict**: "صح / غلط / خرافة" rubber stamps slam onto claims.
- **Stacked-paper parallax**: 4–5 cut-paper layers in brand greens sliding at different speeds.
- **Data "rain"**: numbers fall and settle into a bar chart (seeded, deterministic).
- **Split-flap board**: the airport flap display flips to reveal the title.
- **Constellation**: stars connect into the shape of the concept (a mic, a lightbulb, an arrow).
- **Liquid fill**: text fills with a rising liquid in orange as the stat counts up.

---

## 4. Effects vocabulary: when and how

| Effect | Use it for | How (HyperFrames-safe) | Don't |
|---|---|---|---|
| Zoom in / punch-in | emphasis on a word, entering an idea | tween `scale` on a `.cam` wrapper, expo.out 0.4–1.1 s | zoom the clip element itself |
| Zoom out / pull-back | revealing the whole system, "the big picture" | `viewport-change`: translate + scale a `world` div, power3.inOut | pull back with nothing new to see |
| Parallax | every scene, continuously | ≥3 layers: background dots at 0.3–0.4× camera, mid 1×, foreground 1.2× | put text on the slowest layer |
| Bloom | heroes on deep teal, AI nodes, titles | radial-gradient glow div behind (peak opacity ≤ 0.45–0.6) + text-shadow halo; breathe with finite sine yoyo | bloom on paper without a darker, saturated glow color |
| Motion blur (shutter) | 1–3 snap beats: slam, whip, speed beam | registry `motion-blur` component: `data-hf-motion-blur='{"samplesPerFrame": 8}'` on the moving element | blur text meant to be read; blur elements whose children change mid-move (the copies don't update) |
| Directional blur | whips of cards | SVG `<feGaussianBlur stdDeviation="70 0">` filter, tween `attr.stdDeviation` | CSS `blur()` for a whip (it's not directional) |
| Camera shake | slams, impacts, "breaking" | 6–8 deterministic x/y steps of 35 ms decaying to 0 | random numbers (non-deterministic) |
| Flash | scene handoff into a reveal | root-level white `#flash` 0.1 s in / 0.5 s out | more than 2–3 per video |
| Iris / clip-path | entering a concept world | `clipPath: circle(0%)→circle(125%)` on a wrapper | on the `.clip` element |
| Grain | premium texture | stepped `translate` of a noise layer, opacity 0.06–0.08 on paper | infinite CSS animation |
| Grayscale drain | "abandoned", "failed", "old way" | `filter: grayscale(0→0.9)` on the scene camera | leave it on into the next beat |

---

## 5. Tips and tricks from real production runs (read before building)

> The consolidated, maintained list is `docs/LESSONS_LEARNED.md`. Add new findings there.

**Audio and transcription**
- Use **OpenAI `whisper-1` verbose_json** for word timings (`transcribe.py` default provider).
  Do **not** pass a `prompt` hint. A hint that matches the opening sentence makes Whisper skip it.
- A Gemini key on the **free tier** fails: 503 "high demand", 429 on Pro models, truncated JSON, and
  fake uniform 0.5 s word timings. Use it only with a paid key, and for text (not timing).
- Whisper merges or drops repeated takes, so retakes are invisible in its transcript. Use
  `find_retakes.py` (gpt-transcribe on pause-split chunks + LLM editor pass) instead of hunting by hand.
- Cut script pattern: manual editorial cuts + pause tightening (> 0.38 s → 0.24 s),
  12 ms fades on every seam, remap words through the kept ranges, then **re-transcribe the cut
  file** to prove there are no doubled or clipped words.
- Fix spelling after timing: Egyptian dialect words and Latin keywords (vibe automation, AI) against
  a text-only pass.

**HyperFrames gotchas (each one cost time)**
- `<html dir="rtl">` renders a **blank video**. Put `direction: rtl` on `#root` / text containers.
- A sub-composition's inner root merges into its host (`#s3-host`), so selectors like `#s3 .x`
  match nothing and GSAP warns "target not found". Use element ids or classes.
- `fromTo` renders its from-state at build time. Hide later elements with a `fromTo` (immediate),
  and give every later re-tween of the same element `immediateRender: false`.
- Don't pair CSS `transform` with GSAP transforms on the same node. Size absolute layers with
  left/top/width instead.
- Put `position: absolute` on every flex row you place with `top`. A missing one sent the step chips
  to the top of the frame.
- `.hl` highlighter bands: give the parent `isolation: isolate`. Never use `z-index: -1`.
- Every `<audio>` needs an `id` and its own `data-track-index` (overlapping SFX on one track warn).
- Studio adds `data-hf-id` attributes to files. Write patch regexes that tolerate extra attributes.
- `check` runs on `index.html` only, so a second deliverable (outro) is its own sibling project.

**Kit lessons (fixed in `kit/motion`, keep in mind when hand-writing)**
- `@font-face` url() must resolve from the project root (`assets/fonts/...`). An external CSS with
  `../fonts` fails `check` (`invalid_parent_traversal_in_asset_path`), so the fonts live in the root `<style>`.
- Intentional off-canvas motion (wipe bars, mask reveals) must carry `data-layout-allow-overflow`.
  `HF_WIPE` and `maskUp` add it automatically.
- `.hl` highlighter phrases are `nowrap`. A band behind wrapped text becomes a giant block, so keep them short.
- An Arabic-Indic zero (٠) is a dot. `counter()` hides the number until it starts counting.
- In 9:16 / 1:1 the chrome hides the series name (it collides with the section label).
- Parked wipe bars are invisible between sweeps (their skewed corners used to peek in).

**Arabic typography**
- Noto Kufi Arabic has very tall glyph boxes. Stacked display lines trigger `content_overlap`
  even when the frame is clean. Set line-height 1.2–1.3, verify with a snapshot, then mark only
  verified cases with `data-layout-allow-overlap`.
- "الـAI": a normal tatweel reads like "الا" in Kufi, and a ZWJ doesn't join across the Latin span.
  Use a **long tatweel** `الـــ` + `<span class="lat">AI</span>`.
- Measure headline wrap: at 110–120 px, a 3-word Arabic line needs ~1000–1100 px. Use
  `white-space: nowrap` for names and single-line labels.
- Orange `#FF5A33` fails AA as text on paper (2.8:1). Use it for shapes, beams and bands. Put text
  on it in white at ≥ 90 px, or use teal/ink text.

**SFX mix**
- The bundled library varies from −4 to −36 LUFS. Normalize gain per file
  (impacts ≈ 0.10–0.2, whooshes ≈ 0.3, pops ≈ 0.5, chimes ≈ 0.65) and accent only the hero hits.
- Riser: use its last ~3 s (`data-media-start`) to lead into the biggest reveal.

---

## 6. Originality guardrails (so video #20 doesn't look like video #1)

- **Rotate the spine family** each video (process → courtroom → lab → map …). Keep a log of the
  spine, signature move and palette weighting per project in its `BRIEF.md`.
- **Rotate the palette weighting**, not the palette: teal-dominant, paper-dominant with teal
  punctuation, lime-forward, yellow-forward. Orange stays the accent.
- **One signature move per video** that exists only in that video (Vibe Automation: human teams
  flipping into AI nodes, then the speed beam).
- **Ban the lazy defaults** unless deliberately chosen: every element entering `y: 30 + fade`,
  centered stacks everywhere, identical card grids, gradient text, neon glows, glitch.
- **Vary the camera grammar**: one video lives in a single continuous world, the next cuts hard
  on beats, the next uses 3D paper depth.
- **Invent UI text only as placeholder**, and flag every invented string (country lists, comment
  text, episode names) in the handoff.
- **Ask "why this, why here?"** for each effect. If the answer is "it looks cool", tie it to a word
  or cut it.

---

## 7. Worked examples

### Example 1 — "Vibe Automation" YouTube intro (built, approved)
- **Message:** A stalled podcast comes back when AI works as a full production team.
- **Arc:** frustration → question → realization → excitement.
- **Spine:** the podcast production pipeline.
- **Beats:**
  - mic blooms + "قررت أبدأ بودكاست"
  - episode cards drop onto a shelf and go grey on "وركنت"
  - doubts struck through, "مجهود" slam + meter overflow
  - iris into teal: the AI question glows
  - one node → a team of six
  - pipeline camera ride, word-synced stages
  - human teams stack up
  - the flip into AI nodes, then the speed beam
  - flash → "Vibe Automation" + ٦ خطوات + idea → system
  - channel card, subscribe + bell, country bubbles, "يلا بينا" zoom-through
- **Outro:** like/share/comment trio → next episodes → "سلام عليكم" → end screen with two slots.

### Example 2 — Reel (9:16, 30 s): "3 أخطاء بتبوّظ الـprompt بتاعك"
- **Spine:** a courtroom. Each mistake is a "case", evidence cards slide in, a verdict stamp slams "غلط".
- **Beats:**
  - Hook 0–2 s: gavel slam SFX, the stamp "٣ أخطاء" hits the frame, camera shake.
  - Each mistake gets 6–7 s: a bad prompt card types, strike-through, the corrected prompt types, "صح" stamp.
  - Payoff: all three corrected cards fan out like a hand of cards, then the CTA.
- **Signature move:** the judge's stamp leaves a real ink bleed that becomes the next scene's transition.
- **Footage option:** talking head on the "اسمعني كويس" line (credibility beat).

### Example 3 — YouTube section (16:9, 60 s): "Gemini vs GPT في كتابة المحتوى العربي"
- **Spine:** a race on two lanes. Each round is a checkpoint with the real prompt and outputs as cards.
- **Beats:**
  - Split-screen lanes build.
  - Round 1–3: prompt card in the middle, the two outputs slide into the lanes, a score chip counts up.
  - The winner lane glows with bloom, the loser desaturates.
  - Pull-back to the full track with the final score.
- **Tricks:** capture real screenshots of the real outputs (halal imagery), show cost per run, and use
  `stat-bars-and-fills` for scores.

### Example 4 — Opinion (9:16, 25 s): "الـAI مش هياخد شغلك… اللي هياخده واحد بيستخدم الـAI"
- **Spine:** a chess board. The pawn (you) vs the pawn with a glowing AI piece beside it.
- **Beats:**
  - Myth line with a warning tape that tears.
  - Two pawns; one gets an AI "knight" that orbits it.
  - The board tilts in 3D and the AI-assisted pawn advances three squares with motion blur.
  - End on a crown landing.
- **Signature move:** the board's grid becomes the background dot grid of the CTA frame (match cut).

### Example 5 — Tutorial teaser (16:9, 15 s): "اعمل agent في ٥ دقايق"
- **Spine:** a countdown timer that drives everything. Steps pop out of the timer's segments.
- **Beats:** 5:00 flips to 4:00 … each minute reveals a step card; at 0:00 a bell plus the finished agent node blooms.

### Example 6 — "I automated my invoices with n8n" (16:9, dark preset)
- **Concept:** a messy desk of PDFs turns into one clean flowchart. The recurring motif is a paper stack
  that shrinks every time a node goes live.
- **Beat 0:04–0:08, "كل شهر بقضي يومين في الفواتير":** invoice cards (INV-001…) fall into a pile on
  the left. A yellow counter on the right reaches "٢ أيام" before the word. Pops, then an error buzz when the pile tops out.
- **Hero beat:** an n8n-style canvas. Nodes Gmail → Extract → Sheets → Slack draw in right→left,
  a lime dot travels the wires, and a "WORKFLOW EXECUTED" toast lands with a ding.

### Example 7 — "ChatGPT vs Claude vs Gemini للكتابة العربي" (16:9)
- **Concept:** a boxing-ring scoreboard split into three columns (lime / yellow / orange).
- **Beat "مين أحسن في الكتابة العربي؟":** three prompt boxes type the same Arabic sentence at once.
- **Scores:** bars race to their final values, using **only the scores from your own test**, never invented ones.
- **Winner:** a stamp slam "الأفضل في…".
- **Sections:** ROUND 1 · ROUND 2 · VERDICT.

### Example 8 — "5 AI tools of the week" (9:16 short)
- **Concept:** a vertical "drop" feed. Each tool falls in as a card with a tracked number (01–05).
- **Per tool (~4 s):** the card pops in with the tool name (Montserrat 900) and a one-line Arabic
  benefit. A mini mock-UI shows one action with a cursor click, then a highlighter sweep on the benefit.
- **End:** "احفظ الفيديو" with a bookmark ring pulse, then subscribe.
- **Higgsfield option:** one 1:1 clay icon per tool category (no logos) as a card sticker.

---

## 8. Quick checklist before you hand it over

- [ ] Hook visual lands within the first 0.5 s; a new beat every 2–4 s; nothing static > 4 s; a hero every ~20 s.
- [ ] Visual changes lead their keyword by 0–0.2 s; counters finish before the number is spoken.
- [ ] Sequences flow right → left; English caps labels support the Arabic headlines.
- [ ] UI scenes use real names/data from EXTRA CONTEXT only; placeholders flagged.
- [ ] Higgsfield generations approved, logged in ledger.json, no text inside generated images.
- [ ] Final render mastered to -14 LUFS / -1.2 dBTP (`master_audio.py`).
- [ ] Every scene's key moment is keyed to a word timestamp.
- [ ] One spine, one signature move, contrast beat, clear payoff.
- [ ] Parallax in every scene; bloom only where it earns it; shutter blur on ≤ 3 beats.
- [ ] Arabic reads cleanly (wrap, tatweel, RTL); orange is never small text on paper.
- [ ] SFX normalized; nothing louder than the voice.
- [ ] `check` = 0/0, snapshots reviewed, animation map has no dead zones.
- [ ] Invented strings and photos flagged; preview opened; waiting for approval.
