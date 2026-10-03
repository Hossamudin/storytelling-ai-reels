# kit/motion — reusable motion-graphics kit

Copied into every motion project by `pipeline/new_motion_video.py` (as `assets/`).
Edit the kit here, not in projects, so improvements reach future videos.

| Path | What |
|---|---|
| `css/base.css` | design system: brand tokens, `light` / `dark` presets on `#root[data-preset]`, type scale, components (card, pill, tag, label, highlighter, stamp, window, toast, cursor, ripple, ring, node), chrome, wipe, grain, vignette |
| `js/fx.js` | `HF_SCENE(t0)` scene helpers (global-time API) + root helpers `HF_WIPE`, `HF_CHROME`, `HF_GRAIN` |
| `js/screen.js` | screen-recording annotation engine `HF_SCREEN` (zoom, spotlight, circle, callout, click, blur, badge) fed by `pipeline/screen_annot.py` |
| `templates/quiz.html` · `templates/recap.html` | learning-aid scenes, used via `scenes.json {"template": ..., "data": {...}}` |
| `js/gsap.min.js` | GSAP 3.14.2, vendored — renders never depend on a CDN (`preflight.py` rejects remote URLs) |
| `js/motion-blur.js` | HyperFrames registry shutter motion blur (`data-hf-motion-blur`) |
| `templates/root.html` | root composition: icon library, markers for hosts/audio/chrome/wipes |
| `templates/scene.html` | sub-composition skeleton (mask reveal + parallax + push-in) |
| `fonts/` | Noto Kufi Arabic, Manrope (light) · Cairo, Montserrat (dark) — OFL, from google/fonts |
| `sfx/library/` | HyperFrames bundled SFX (19 files) |
| `sfx/higgsfield/` | bespoke SFX generated via Higgsfield (see `prompts/higgsfield_playbook.md`) |
| `sfx/levels.json` | measured loudness + recommended gain per file (`python pipeline/sfx_levels.py`) |

Root helpers in `fx.js`: `HF_WIPE`, `HF_CHROME`, `HF_STEPS` (step tracker), `HF_GRAIN` (grain is off for screen recordings: `chrome.json "grain": false`).
Run `python pipeline/sfx_levels.py` after adding any SFX here.
Knowledge: `prompts/motion_director_prompt.md`, `prompts/style_presets.md`.
