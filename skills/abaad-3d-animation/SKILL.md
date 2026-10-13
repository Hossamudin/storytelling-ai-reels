---
name: abaad-3d-animation
description: "Ab'aad (أبعاد) — 3D animation studio for videos: brand-colored 3D hero objects, clay/plastic/glass looks, 3D logo stings, product spins, camera fly-throughs, particles and data in 3D, GLB models with animation clips, CSS 3D card/page flips, cinematic Blender renders, and AI-generated 3D (clay renders, image-to-3D, 3D scene builders) — all synced to a voice and composited with crisp text in any language (Arabic RTL included), rendered offline and deterministic. Picks the right path for the machine and budget, and onboards beginners (machine check incl. GPU/Blender, brand, tools). Use whenever someone wants 3D animation, a 3D logo or intro, a product render, clay/isometric 3D visuals, Three.js or Blender for a video, or says 'make it 3D', 'انيميشن ثري دي', 'تصميم 3D', 'لوجو 3D', 'مجسم' — even if they only say 'more depth' or 'premium look'."
---

# Ab'aad · أبعاد — the 3D animation studio

*Ab'aad* means "dimensions". This skill adds depth where it earns its place: a hero object that carries the video's
metaphor, a logo that turns in light, a product spin, a camera flight through an idea — always on-brand, always in
sync with the voice, always rendered the same way twice.

{{CORE}}

## Choose the path honestly (details: `references/animation-3d.md`)

| Path | Gives | Needs |
|---|---|---|
| A. CSS 3D | card flips, page folds, tilted UI | nothing |
| **B. Three.js in the composition** (default) | real-time clay/plastic/glass objects, logos, particles, camera moves | `vendor_lib.py three` |
| C. GLB models | specific objects, animated characters | a licensed/own/AI `.glb` |
| D. Blender | cinematic path-traced shots, physics | Blender + GPU + time (`env_check.py` shows both) |
| E. AI 3D (paid) | stylized 3D renders/clips without modelling | a generation MCP + approval |

Start with B (free, controllable, brand colors automatic). Use D/E for the one shot that must look cinematic, after the
creator approves time/cost. Weak machine → B with fewer objects, or E.

## The workflow

1. **Voice** → `new_project.py` → `clean_audio.py --no-silence-cut` → `transcribe.py` → `find_retakes.py` (review page)
   → `input/edit.json` → `voice_edit.py` (`references/voice-and-cuts.md`); the 3D beats hit word times.
2. **Concept** — which 1–3 moments deserve 3D and why (the metaphor object, the logo, the product); camera grammar
   (one hero move per scene); look (clay / glass / toon / metal accents). Approval (+ any paid assets with cost).
3. **Build (path B)**:
   ```bash
   python engine/pipeline/new_motion_video.py <name> --part <part> --voice projects/<name>/assets/voice/<part>.wav --aspect 16:9 --preset light
   python <skill-dir>/scripts/vendor_lib.py three projects/<name>/<part>     # local three.js + addons + importmap
   # scenes.json: {"id":"s2","start":4,"duration":4.8,"title":"…","template":"three_hero"}
   python engine/pipeline/motion_sync.py <name> --part <part>
   # shape compositions/s2.html: replace the hero group with the video's object; keep renderAt(time) pure
   cd projects/<name>/<part> && npx hyperframes check && npx hyperframes snapshot --at <start+0.05>,<busiest>,<end>
   ```
4. **Preview → approval → `render_final.py`** → deliver, explain, suggest, ask. Save the hero object/logo to the library
   (`--type 3d` or `code`) so the next video starts from it.

## The 3D contract (break it and frames flicker or renders hang)

- Render from time only: `hf-seek` gives GLOBAL seconds → `t = time - sceneStart`; no `requestAnimationFrame`, no
  clocks, seeded randomness; animation clips via `mixer.setTime(t)`.
- Pixel ratio 1, fixed size; `preserveDrawingBuffer: true`.
- Everything local: three.js + addons vendored, importmap in the ROOT `index.html`, models in `assets/3d/`.
- Text lives in HTML above the canvas (crisp, any language) and sits OFF the object (contrast is checked).
- Colors from brand tokens (the template reads them), soft studio light (`RoomEnvironment`), contact-shadow planes
  instead of shadow maps, `InstancedMesh` beyond ~50 copies.

## Look recipes

Clay: roughness 0.45–0.6, metalness 0, rounded bevels, pastel brand colors · Glass: `MeshPhysicalMaterial`
transmission 1 · Metal accents: metalness 0.8–1, roughness 0.2–0.35, small doses · Toon: `MeshToonMaterial` +
back-face ink shell. Camera: slow push-in, gentle orbit, one hero move per scene, eased — never constant spinning.
3D logo: extrude the creator's SVG with `SVGLoader` + `ExtrudeGeometry` (never retype a logo).

## Blender path (when it's worth it)

Write a Python scene script, render headless (`blender -b -P scene.py -- …`) to PNG frames (RGBA if composited),
10-frame low-sample draft first, then the full shot detached; encode with ffmpeg; place as a muted `<video>` with a
still underneath; text in HTML on top. Frame for a word = round(seconds × fps).

## Domain references

`references/animation-3d.md` (paths, contract, looks, GLB, Blender, AI 3D, performance, checklist) ·
`references/motion-director.md` (timing, spines, archetypes) · `references/style-presets.md` ·
`references/storytelling.md`.
