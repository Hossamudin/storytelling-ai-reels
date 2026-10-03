# Talking-Head Director — Hossam on camera + editorial motion graphics (hybrid reels / long videos)

The **camera-footage** sibling of `prompts/motion_director_prompt.md` (faceless, 100% motion graphics).
Same brand, kit, scene vocabulary, SFX rules and approval gate. What changes: Hossam's face carries the
opinions and credibility, and the graphics carry what the viewer must *inspect*.
Reference build: `projects/agent-harness/reel_th/` (9:16, 171 s, dark preset), the talking-head twin of the
faceless `projects/agent-harness/reel/`. A screen-recording workflow is a separate mode, developed by another
agent (`pipeline/screen_edit.py`, `screen_annot.py`). Don't mix the two.

---

## 1. When to use which mode

| Input | Mode |
|---|---|
| voice only, or the user asks for "no talking head / 100% motion" | faceless: `motion_director_prompt.md` |
| camera video of Hossam (`rawreel.*`, talking head) | **this file** |
| screen recording of a tool | screen-share workflow (other agent) |
| camera + screen recording | this file for the camera beats; screen clips become full-screen visuals |

One raw camera file can yield both versions: the faceless cut from its audio, and the hybrid from its picture and audio.
They share the edited voice (`voice_edit.py`), the scene builders and every asset.

## 2. Formats (choose per beat, from the transcript)

| Format | Looks like | Use for | Kit / code |
|---|---|---|---|
| **Clean talking head** | full frame; a short label, pill or icon in open space (wall above the head, desk below) | direct explanations, opinions, hooks | `full` mode + `th_front.html` rows |
| **Text behind you** | big words sit between the footage and the person matte, so they read behind the shoulders | hook keyword, key phrase, chapter turn, a number slam ("×2") — never dense text | `th_behind.html` `.bt` + matte video |
| **Presenter + canvas** | upper body cropped into a rounded card at the top; diagram / UI / evidence below | teaching a framework, a prompt→result demo, a bonus/product card | `card` mode + a canvas sub-composition (opaque `.bg`) |
| **Circular presenter** | face in a lime-ringed circle over a designed scene | brief explanations over a process, timeline, chart or engine-swap the viewer must watch | `circle` mode {cx, cy, s} over any scene |
| **Full-screen visual** | presenter leaves; voice continues over b-roll, a real screenshot, a chart ride, a diagram | anything the viewer must inspect, or a cinematic b-roll beat | `hide` mode + scene host |
| **Layered depth** | brackets, arrows or a frame pass *behind* him (matte) while a small label stays in front | spatial ideas ("he's inside the harness"), the signature move | `th_behind.html` shapes + `th_front.html` label |

**Return to the face** when the speech turns personal, interpretive or credibility-critical: myths, "I'm not
telling you X", "investigate", CTA, outro. Never cover such a line with b-roll.

## 3. Rhythm rules

- Ratio: **45–55 % face** (full + card + circle) vs **45–55 % full-screen** interludes. Adapt to the transcript.
- Interlude length: short 1.8–2.5 s · normal 2.8–4.0 s · list/process ≤ ~4.5 s. Long chart rides (> 8 s) get a
  circle-presenter break in the middle so the face returns.
- Group adjacent speech into purposeful beats. Reels of 20–35 s: about 4–6 semantic scenes. Long videos: one
  format change every 3–7 s, a hero every ~20 s.
- Every format switch sits on a word boundary (0–0.15 s before the keyword) and carries a whoosh.
- **Hide every jump cut**: a cut seam (`<part>_th_seams.json`) must fall inside a full-screen interlude, or get a hard
  punch (`punch` entry with dur 0) exactly on the seam.
- Punch-ins: alternate 1.0 / 1.1 / 1.12 across consecutive face windows. Slow 1.0→1.06 creeps on calm lines. Snap
  punches (0.2 s) plus a presenter shake on slams. Hard punches on seams.
- Captions: burned-in Arabic captions only while the face is full-frame (≤ 3 words, Latin terms in lime, dark pill at
  y≈1600). Turn them off with `nocap` when a front card or CTA occupies the lower half.

## 4. Real sources beat illustration

When the speech names a source ("artificialanalysis.ai", "an article from Arena AI", "their chart shows…"):
1. Capture it: `python pipeline/web_capture.py <url> --out projects/<name>/assets/images/<slug> --full --iframes --imgs`
   (2× PNGs, page.txt for exact numbers, capture.json). Crop chart regions from `full.png` with PIL.
2. Show it as **evidence**: a browser-frame window (`.window` + the URL in the bar), a slow pan or zoom (ken burns),
   then annotation in brand colours: rings on the exact data points, `↑ أذكى` / `أغلى →` tags, drawn arrows,
   a crown on the winner. Map image px to frame px with the display scale (see `build_th.py` `P()`).
3. Use the **real numbers** in your own motion scenes too (e.g. `$1.33 → $0.67`, `97.8 % vs 96.7 %`). Label them:
   `REAL DATA · <source> · captured <month>`. Quote at most one short English line, with attribution.
4. Log the capture in `assets/ledger.json` (`provider: web-capture`). Never invent data; mark illustrative
   graphics `ILLUSTRATION`.

## 5. Higgsfield (paid; approval gate; see `higgsfield_playbook.md`)

Model ids that work in the MCP (Oct 2026): images `gpt_image_2_5` (pass `quality: "medium"`, aspect per asset);
video `seedance_2_0` (image→video via `medias: [{value: <image job id>, role: "start_image"}]`, 5 s, 9:16);
SFX `mirelo_text_to_audio`.
Typical budget for a 2–3 min hybrid: 2 images (hero object + its "rig/scene"), 2 image→video b-rolls, ≤ 6 SFX.
- Generate the spine object first (e.g. the engine core), then a second image that puts it in context (the
  harness rig), then animate both. The stills double as canvas assets (masked with a radial `mask-image`).
- B-roll goes full-screen with a gradient shade behind the headline. Use `data-media-start` to pick the part of the
  5 s clip where the action happens.

## 6. Build steps

```
python pipeline/new_project.py <name>                    # copy the camera file to input/rawreel.<ext>
python pipeline/clean_audio.py <name> --no-silence-cut
python pipeline/transcribe.py <name>                     # + gpt-4o-transcribe excerpt passes for names
# input/edit.json: cut repeats, false starts, screen-only lines ("لو نزلنا تحت")
python pipeline/voice_edit.py <name> --verify            # <part>.wav + <part>_words.json (keep ranges)
python pipeline/th_cut.py <name> --part <part>           # camera cut on the same keep ranges + seams.json
npx hyperframes remove-background projects/<name>/assets/video/<part>_th.mp4 -o projects/<name>/assets/video/<part>_th_matte.webm   # start NOW (slow on CPU)
python pipeline/web_capture.py <url> --out projects/<name>/assets/images/<slug> --full --iframes   # real sources
# Creative treatment: format per beat (table below) + Higgsfield plan -> APPROVAL
python pipeline/new_motion_video.py <name> --part <th_part> --voice projects/<name>/assets/voice/<part>.wav --aspect 9:16 --preset dark
# copy video/matte/images/higgsfield into <th_part>/assets ; scenes.json = full-screen + canvas windows only
# scene builders (build_th.py style), th.json, th_behind.html, th_front.html, th_front.js
python pipeline/th_layer.py <name> --part <th_part>      # presenter layer (formats, punches, captions, matte)
python pipeline/motion_sync.py <name> --part <th_part>   # hosts, audio, chrome, wipes
cd projects/<name>/<th_part> && npx hyperframes check && npx hyperframes snapshot --at ... && npx hyperframes preview --background
# APPROVAL -> npx hyperframes render -> python pipeline/master_audio.py renders/<file>.mp4
```

Treatment table columns: `# | start–end | spoken | FORMAT | on-screen (exact) | assets (real / generated / code) | SFX`.

## 7. Gotchas (each cost time on the first build)

- `th_layer` keeps camera, behind-layer and matte **inside one wrapper** (`#thw`), so every punch, card or circle
  transform keeps them aligned. Never transform the `<video>` itself.
- `clip-path` can't interpolate `inset()` ↔ `circle()`. Full frame is `circle(1400px at 540px 760px)`. Card mode opens
  to `inset(0 … round 0)`, then swaps to the equivalent circle (handled in `th_layer.py`).
- Don't use relative tweens (`scale: "+=…"`) on `#thw`. `check` errors `gsap_relative_value_second_writer` when a punch
  overlaps a hide.
- Text-behind only works where it overlaps the person: put it at y≈380–480 (head line) at 9:16, ≤ ~180 px for words
  of 7+ letters. Above the head it just reads as normal text.
- The matte (`u2net_human_seg`) cuts the person only: the mic arm and desk stay *behind* the text. Keep behind-text
  above the mic line.
- Studio adds `data-hf-id` attributes to files it touches. Regexes that copy markup between projects must tolerate
  them (and strip them from copies).
- CPU background removal runs at 0.3–0.8 s/frame (≈ 25–60 min for 3 min at 30 fps). Start it right after `th_cut.py`.
- Headless charts (iframes, canvas) render blank until scrolled into view. `web_capture.py` scrolls and waits.
- Dark preset `.hl` text is ink-coloured: give it a visible colour until the band sweeps in, then tween it to ink.
- Prices in RTL pills: wrap `$1.04` in `<span class="lat">`, or bidi prints "1.04$".
- Keep the chart headline and verdict in the DOM *after* a zooming world, with a backdrop, or the zoom covers them.
