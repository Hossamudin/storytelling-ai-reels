# kit/motion — reusable motion-graphics kit (Video Studio engine)

Copied into every motion project by `engine/pipeline/new_motion_video.py` (as `assets/`), together with the
creator's `brand/brand.css` + `brand/fonts/`. Improve the kit in the skill source, not in projects.

| Path | What |
|---|---|
| `css/base.css` | design system: brand tokens, `light` / `dark` presets on `#root[data-preset]`, type scale, components (card, pill, tag, label, highlighter, stamp, window, toast, cursor, ripple, ring, node), chrome, wipe, grain, vignette |
| `js/fx.js` | `HF_SCENE(t0)` scene helpers (global-time API) + root helpers `HF_WIPE`, `HF_CHROME`, `HF_GRAIN` |
| `js/screen.js` | screen-recording annotation engine `HF_SCREEN` (zoom, spotlight, circle, callout, click, blur, badge) fed by `engine/pipeline/screen_annot.py` |
| `templates/quiz.html` · `templates/recap.html` | learning-aid scenes, used via `scenes.json {"template": ..., "data": {...}}` |
| `templates/character_2d.html` | 2D puppet rig (blink, gestures, lip-sync from `lipsync.py`), mirrors for RTL |
| `templates/three_hero.html` | Three.js hero object in brand colors (needs `vendor_lib.py three`) |
| `templates/screen.html` | screen-recording scene (created by `screen_annot.py`) |
| `css/brand.css` | placeholder; replaced per project by the creator's brand |
| `js/gsap.min.js` | GSAP 3.14.2, vendored — renders never depend on a CDN (`preflight.py` rejects remote URLs) |
| `js/motion-blur.js` | HyperFrames registry shutter motion blur (`data-hf-motion-blur`) |
| `templates/root.html` | root composition: icon library, markers for hosts/audio/chrome/wipes |
| `templates/scene.html` | sub-composition skeleton (mask reveal + parallax + push-in) |
| `fonts/` | Noto Kufi Arabic, Manrope (light) · Cairo, Montserrat (dark) — OFL, from google/fonts |
| `sfx/library/` | HyperFrames bundled SFX (19 files) |
| `sfx/generated/` | put bespoke generated SFX here (then run `sfx_levels.py`) |
| `sfx/levels.json` | measured loudness + recommended gain per file (`python engine/pipeline/sfx_levels.py`) |

Root helpers in `fx.js`: `HF_WIPE`, `HF_CHROME`, `HF_STEPS` (step tracker), `HF_GRAIN` (grain is off for screen recordings: `chrome.json "grain": false`).
Run `python engine/pipeline/sfx_levels.py` after adding any SFX here.
Knowledge: the skill's `references/motion-director.md`, `references/style-presets.md`, `references/composition-craft.md`.
