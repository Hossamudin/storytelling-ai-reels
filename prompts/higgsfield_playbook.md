# Higgsfield playbook — generated SFX, visuals and clips that assist the motion graphics

Code-built HyperFrames motion stays the **backbone**: it gives crisp Arabic, exact timing, zero
cost and full brand control. Higgsfield (MCP, connected in Claude Code) adds what code can't:
bespoke sound design, photoreal or 3D textures and objects, and short cinematic clips.
**Every Higgsfield generation is paid → approval gate applies.** List the planned generations
(what, why, model, count) in the Creative Treatment and generate only after the user approves.
Log every job in `projects/<name>/assets/ledger.json` (job id, model, prompt, cost, file).

---

## 1. Tools and flow (MCP)

| Need | Tool | Notes |
|---|---|---|
| Group this video's outputs | `create_project` → use `default_folder_id` as `folder_id` on every generation | one Higgsfield project per video |
| 1–12 SFX / TTS clips | `generate_audio_batch` | SFX model: **`mirelo_text_to_audio`** (needs `duration`). TTS models: `inworld_text_to_speech`, `seed_audio`, `text2speech_v2` (only if the user asks — Hossam's own voice is the default). `sonilo_music` exists but **brand rule: no music** |
| 1–12 images | `generate_image_batch` | **Model preference: GPT Image 2.5 at medium quality.** Choose `aspect_ratio` per asset (table below). If the catalog lacks it, use the best listed image model and say so |
| 1–12 video clips | `generate_video_batch` | set `aspect_ratio` ("16:9" / "9:16"); keep `duration` short (3–6 s); image → video by passing a prior image job id in `medias` |
| Wait for jobs | `jobs_wait` (≤ 12 per call, ≤ 15 s per poll) | then download the result URLs into `assets/higgsfield/` |
| Show results to user | `show_generation_by_ids` (once, for the whole set) | |
| Viral effects / motion presets | `get_presets` (`source:'viral'` or `category:'motion'`) | browsing never authorizes `execute_preset`; ask first |
| 3D scenes / objects | `scene_builder_3d_*` | for a hero 3D object render (e.g. a clay podcast mic), exported as image/video |
| Free-trial allowance | `use_unlim` | omit it; if the tool returns `unlim_choice`, ask the user which balance to spend |

Batch rules: never retry a whole batch after a partial failure. Keep the returned job ids, resolve
the unknown ones, and retry only the affected items.

**Aspect per asset (images):**

| Asset | aspect |
|---|---|
| full-frame background plate, 16:9 video | 16:9 (1536×1024) |
| full-frame plate, 9:16 video | 9:16 (1024×1536) |
| icon / object / sticker to cut out | 1:1 (1024×1024) |
| portrait card, tall UI panel | 2:3 or 9:16 |
| wide banner / strip, parallax far layer | 16:9 or 21:9 if supported |
| seamless texture tile | 1:1 |

---

## 2. What to generate (and what not to)

**Great uses**
1. **Bespoke SFX** for hero moments the 19-file library can't sell: a paper stack collapsing, a
   podcast mic tipping onto a shelf, a stamp thud with room tone, a UI confirmation chime in brand
   character, a soft data "shimmer" for AI moments, a bell that matches the brand.
2. **Textures and plates**: paper grain, soft studio light gradients in brand teal, macro
   texture of a notebook or a desk in brand colors. Use them as slow parallax background layers.
3. **3D / clay objects** for the video's spine metaphor (a clay microphone, an isometric kitchen,
   a chess piece, a gavel). Cut them out with `npx hyperframes remove-background`, then animate them in code.
4. **Short abstract clips** (3–6 s) for breathing beats: light streaks, flowing liquid in brand
   green, particles forming a shape. Play them muted behind code typography.
5. **Image → video** for one premium hero shot per video (e.g. the clay mic slowly rotating).

**Don't**
- Don't generate **text inside images**. Arabic renders wrong. All text stays in code.
- Don't generate realistic people (brand avoid). Hossam appears only via `Hossam Images/`.
- Don't generate robots, computers, offices, money, or blue/purple palettes (brand avoids).
- Don't replace a diagram, UI, counter or list with generated media. Code does those better.
- Don't use music, ever.

---

## 3. Prompt templates

**SFX (`mirelo_text_to_audio`, duration 0.4–3 s):**
```
<action> sound effect, <material/texture>, <space>, <character>, clean studio recording,
no music, no voice, no background noise, single hit, tight tail
```
Examples:
- `short airy whoosh, soft paper swipe, close mic, modern UI motion-graphics style, no music, no voice, 0.6 s`
- `heavy wooden stamp thud on a desk, subtle room tone, satisfying, single hit, no music, 1.2 s`
- `microphone falls over onto a wooden shelf, dull thump and small rattle, no music, 1.5 s`
- `soft magical shimmer, glassy high sparkles rising, AI activation, no music, 1.8 s`
- `friendly UI success ding, warm marimba tone, single note, no music, 0.8 s`
- `tension riser, filtered noise swelling into a reveal, ends abruptly, no music, 3 s`
- `short digital glitch burst, data scan error, crisp, no music, 0.7 s`
After download: `python pipeline/sfx_levels.py --dir projects/<name>/<part>/assets/sfx`
(put files in `assets/sfx/higgsfield/`), then reference them in `cues.json` as `higgsfield/<file>`.

**Image (GPT Image 2.5, medium quality):**
```
<subject as the video's metaphor object>, minimal premium 3D/clay/vector style,
brand palette deep teal #136052, green #437F3E, lime #B3CE65, warm yellow #FFEC5C,
orange accent #FF5A33, soft studio lighting, generous negative space,
<plain background color for cut-out | seamless background plate>, no text, no letters,
no people, no logos, no blue, no purple
```
Examples:
- `a clay podcast microphone on a small wooden shelf, dusty, slightly tipped over, minimal premium clay style, deep teal background #136052, soft light, no text, no people` (1:1, cut out)
- `seamless paper texture, warm off-white #F6F4EA, subtle fibers, flat light, no text` (1:1 tile)
- `isometric miniature production line with six small stations connected by an orange conveyor, clay style, brand palette, empty background` (16:9)

**Video (3–6 s, muted in the composition):**
```
<slow camera move> over <abstract/object subject>, brand palette …, minimal, premium,
soft light, loopable, no text, no people, no logos
```
Examples:
- `slow push-in on glowing lime and yellow light streaks flowing through deep teal space, abstract, loopable, no text` (16:9, 5 s)
- image → video: the clay microphone job id in `medias` + `the microphone slowly rotates, dust particles drift, gentle light sweep, no text` (4 s)

---

## 4. Integrating generated media in HyperFrames

- Images: `<img>` inside a scene's parallax layer. Animate the **wrapper**
  (ken burns / parallax), never the timed element itself.
- Video: `<video muted playsinline>` with its own `data-start/data-duration`, and **no timed ancestor**.
  Any sound goes on a separate `<audio>`.
- Cut-outs: `npx hyperframes remove-background <file>` → transparent PNG/WebM.
- Grade to brand if needed via `/media-use` media treatments (never ad-hoc CSS filters).
- Keep a text overlay on generated media readable. Check contrast with `npx hyperframes check`.
- Budget heuristic per 60–90 s video: ≤ 6 SFX, ≤ 4 images, ≤ 2 clips. More only when the
  concept is built on them (e.g. a clay-world video).
