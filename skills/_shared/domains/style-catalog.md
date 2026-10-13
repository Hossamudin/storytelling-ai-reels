# Style Catalog

Each scene in a storyboard picks exactly one style. Styles drive both code-built motion graphics and AI image/video prompts. All styles obey the creator's brand (`brand-profile.md`).

## 1. motion_graphics (default workhorse)
Premium Apple/SaaS editorial minimal 2D vector. Geometric figures, grids, beams, staged typography reveals, progress paths lighting up sequentially. Built in code (HyperFrames) for crisp text and cheap credits. Use for: concepts, workflows, transformations, lists, CTAs.

## 2. vox_animation
Vox-video essay look: archival-style imagery, zooms/panns on stills, bold caption blocks, editorial cuts, magazine-style collages. Use for: storytelling, history of a topic, narrative arcs, commentary. Often mixes screenshots + generated stills + zoom moves.

## 3. whiteboard_explainer
Hand-drawn illustration on white/off-white, marker strokes, items being "drawn in" sequence. Friendly, didactic. Use for: step-by-step teaching, process explanations, beginner-friendly segments.

## 4. scientific_infographic
Data-viz forward: charts, counters, comparison matrices, timelines, annotated diagrams on light background. Use for: benchmarks, numbers, model comparisons, cost/credit breakdowns, stats.

## 5. 3d_animation
Soft 3D shapes, clay-like renders or clean CGI, gentle camera moves, studio lighting in brand palette. Use sparingly (AI video or complex code): hero moments, premium feel, product metaphors.

## 6. clay_animation
Stop-motion claymation feel, tactile, warm, charming imperfection. Use for: human moments, humor, friendly analogies. AI video only.

## 7. stop_motion
Physical cut-paper / object animation feel, snappy frame cadence. Use for: playful sequences, transitions, pattern interrupts in hooks.

## 8. cinematic_broll (AI video territory)
Semi-realistic generated footage: abstract macro shots, flowing materials, light streaks, landscapes of data. NO humans/faces by default. Use for: emotional beats, breathing room between dense explainers, hook impact shots.

---

## Method catalog (how a scene gets its footage)
| method | meaning | credits |
|--------|---------|---------|
| `code` | Motion graphics written as HyperFrames HTML by the agent | free |
| `direct_image` | One generated/downloaded image, animated in code (ken burns / parallax) | image cost |
| `image_animate` | Generate image → animate via AI video (image as first frame) | image + video |
| `first_last_frame` | Generate 2 images → AI video interpolates between them | 2 images + video |
| `text_to_video` | Direct AI video from prompt (no input images) | video |
| `screenshot` | Agent captures/downloads real screenshots or resource images | free |
| `person_image` | A photo/cutout of the creator from the library (`person-photo` / `person-cutout`), animated in code | free |
| `screen_recording` | The presenter's own screen capture, edited (`screen_edit.py`) and annotated (`assets/js/screen.js`): zoom, spotlight, circle, callout, click, blur, steps, quiz/recap — see the screen-tutorial playbook (Kashaf / Hakawati skills) | free |
| `ui_mock` | Believable mock product screen built in code (window, rows, buttons, typing, cursor, toasts) with REAL names/data from the brief | free |
| `gen_sfx` | Bespoke sound effect via an AI-generation MCP (e.g. Higgsfield `mirelo_text_to_audio`) (hero moments only; no music) | credits |
| `gen_image` | Texture / plate / 3D-clay metaphor object via an AI-generation MCP (GPT Image 2.5, medium, aspect per asset); never text inside | credits |
| `gen_video` | 3–6 s abstract/hero clip (text→video or image→video), muted under code typography | credits |

Full motion-graphics mode (no footage): `motion-director.md` + `style-presets.md` + the kit.
Generated assets: `tools-connection.md` (approval gate + ledger).

## Choosing (agent intuition, encoded)
- Number/process/comparison → `code` (scientific_infographic or motion_graphics).
- Emotional or realistic visual → `image_animate` (control + quality).
- Transformation "from X to Y" → `first_last_frame`.
- Hook impact shot, abstract beauty → `text_to_video`.
- Mentioning a product/model/site → `screenshot` (real UI beats generated UI).
- The creator as authority/quote → `person_image` + typography.
- Quote card, CTA, outro → `code`.
- AI video clips are ≤10s (typical clip-model limit): longer scenes = multiple clips or image+code extension.
