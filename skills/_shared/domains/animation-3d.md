# 3D animation playbook — five ways to get depth, from free and instant to cinematic

Be honest with the creator about what each path gives. All paths end in the same HyperFrames composition, so 3D
shots sit next to motion graphics, captions and the voice, and render offline through `render_final.py`.

## 1. Choose the path

| Path | Looks like | Needs | Speed | Best for |
|---|---|---|---|---|
| **A. CSS 3D** (`perspective`, `rotateY`, `preserve-3d`) | cards flipping, folding paper, 3D carousels, tilted UI screens | nothing | instant | UI showcases, page folds, "deck of cards" |
| **B. Three.js in the composition** (kit `three_hero`) | real-time 3D: clay/plastic objects, logos, particles, product spins, camera flights | `vendor_lib.py three` | fast renders | hero objects, abstract metaphors, data in 3D, logo stings |
| **C. GLB models** (Three.js + GLTFLoader) | any model: devices, characters, props | a `.glb` (creator-made, licensed library, or AI-generated) | fast | specific objects, animated characters with clips |
| **D. Blender** (headless Python render → image sequence/video) | film quality: path-traced light, physics, cloth, real materials | Blender installed (free), a decent GPU, time | slow (minutes–hours) | the one cinematic hero shot, product ads |
| **E. AI 3D** (generation MCP: image→3D, 3D scene builders, clay renders, image→video) | stylized 3D renders/clips without modelling | a generation MCP + budget (approval) | minutes | spines/metaphors as clay objects, quick hero clips |

Rule of thumb: start with **B** (free, controllable, on-brand automatically). Reach for **D/E** only for a shot that
must look cinematic, and budget it.

## 2. Path B — Three.js inside HyperFrames (the default)

```bash
python engine/pipeline/new_motion_video.py <name> --part <part> --voice <wav> --aspect 16:9 --preset light
python <skill>/scripts/vendor_lib.py three projects/<name>/<part>     # three.module.min.js + addons, importmap in index.html
# scenes.json: {"id":"s2","start":4,"duration":4.8,"title":"…","template":"three_hero"}
python engine/pipeline/motion_sync.py <name> --part <part>
cd projects/<name>/<part> && npx hyperframes check && npx hyperframes snapshot --at 4.05,5,8
```
The contract (from the HyperFrames three adapter — break it and frames flicker or the render hangs):
- Render from **time**, never a clock or `requestAnimationFrame`: listen to `hf-seek` (`e.detail.time` = GLOBAL seconds)
  and compute everything from `t = time - sceneStart`.
- Seeded randomness only. Pin `renderer.setPixelRatio(1)` and `setSize(W, H, false)`.
- All models/textures/HDRIs local (`assets/3d/…`), loaded before render; heavy CPU setup → register a promise on
  `window.__hf.buildReady["name"]`.
- The importmap lives in the ROOT `index.html` (vendor_lib adds it). No CDN imports.
- Keep text in HTML layers above the canvas (crisp, any language, RTL-safe), positioned OFF the object (contrast).
- Brand colors: read CSS tokens (`getComputedStyle(root).getPropertyValue("--teal")`) — the template does.

Look recipes (MeshStandardMaterial + `RoomEnvironment` for soft studio light):
- **Clay/plastic**: roughness 0.45–0.6, metalness 0, slight bevel (`RoundedBoxGeometry`), pastel brand colors.
- **Glass**: `MeshPhysicalMaterial({transmission: 1, thickness: 0.5, roughness: 0.05})`.
- **Metal accents**: metalness 0.8–1, roughness 0.2–0.35, small doses.
- **Toon**: `MeshToonMaterial` + an outline pass-free trick: back-face scaled shell in ink color.
Camera grammar: slow push-in (6.4 → 5.6 over the scene), gentle orbit (±0.6 units), one hero move per scene
(fly-through, reveal from behind, top-down drop). Ease camera moves (cubic out). Avoid constant spinning.

3D text: prefer HTML text over the canvas. For a 3D logo, extrude the creator's SVG logo with `SVGLoader` +
`ExtrudeGeometry` (bevel on) — never retype a logo.

## 3. Path C — GLB models and characters

- Sources: the creator's own models, licensed libraries (check redistribution + attribution), AI image→3D tools via MCP
  (approval). Store models in the library (`--type 3d`).
- Load with `GLTFLoader` from `assets/3d/model.glb` before the first render; animated clips: `mixer.setTime(t)` in
  `renderAt` (never `mixer.update(delta)`).
- Large models: compress (`gltf-transform optimize` via npx) to keep renders fast.

## 4. Path D — Blender (cinematic)

When Blender is installed (`env_check.py` shows it), write a Python script and render headless:
```bash
blender -b -P scene.py -- --out projects/<name>/assets/3d/shot01_ --frames 1-150 --fps 30 --res 1920x1080
ffmpeg -framerate 30 -i projects/<name>/assets/3d/shot01_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 16 shot01.mp4
```
- Script builds/opens the scene, sets brand colors on materials, keyframes the camera in Python, sets Eevee (fast) or
  Cycles (quality, GPU), renders PNG frames (alpha if the shot sits over motion graphics: RGBA + transparent film).
- Time the shot to the voice: frame = round(seconds × fps) of the target word.
- Place the result in a scene as a muted `<video>` (with a still frame underneath) — text stays in HTML on top.
- Render a 10-frame draft first (`--frames 1-10`, low samples), show it, then the full shot. Long renders: run detached.

## 5. Path E — AI 3D (paid → approval)

- Clay/3D object images (GPT Image class models, medium quality): `<object>, minimal premium 3D clay render, brand
  palette <hexes>, soft studio lighting, plain <color> background, no text, no people` → `remove-background` → animate
  in code (parallax, rotation, float) — the cheapest "3D" that looks premium.
- Image→video for a 3–5 s hero clip (e.g. the clay object slowly rotates) — muted, text in HTML over it.
- 3D scene builders (e.g. `scene_builder_3d_*` tools) can generate/import assets and render angles or a short video;
  export stills/clips into `assets/3d/`. Read the tool's own instructions first.
- Log every job in `assets/ledger.json`; harvest keepers into the library.

## 6. Performance & render safety

- Many draw calls/particles slow renders: instanced meshes (`InstancedMesh`) for > 50 copies.
- Shadows are expensive; use contact-shadow planes (a blurred dark ellipse texture) instead of shadow maps.
- `preserveDrawingBuffer: true` on the renderer avoids blank captures in some environments.
- Post-processing that depends on previous frames (motion blur trails, TAA) breaks seeking — avoid or rebuild from `t`.
- Test snapshot at the scene's first 0.1 s (pop-in from zero) and its busiest moment.

## 7. Quality checklist

- [ ] One clear hero object/idea per 3D scene, tied to the voice; text readable and off the object.
- [ ] Brand palette on materials; lighting soft and consistent across shots.
- [ ] Deterministic: same frame every render (no clocks, seeded randomness, mixers set by time).
- [ ] No network: three/addons vendored, models local.
- [ ] `check` clean, snapshots reviewed, draft render watched before the final.
