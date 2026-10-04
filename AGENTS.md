# Hossam Story Telling — Agent Instructions

This repo is a **video production factory** run by you (the agent). The full workflow lives in
`.opencode/skill/hossam-video-factory/SKILL.md` — read it before producing any video.

## Ground rules
- Pipeline scripts in `pipeline/` do the deterministic work — use them, don't reimplement.
- **Approval gate is law**: no paid asset generation before storyboard approval (dashboard or explicit chat approval).
- Keys: `config/api_keys.json` (gitignored) or env vars. Never print key values.
- Config: `config/config.json` — model names are plain fields so upgrading (e.g. new Gemini or GPT Image model) is a one-line change (dashboard Config tab or direct edit).
- Motion-graphics videos from voice (house style): `prompts/motion_director_prompt.md` + `prompts/style_presets.md`,
  code kit `kit/motion/`, scripts `new_motion_video.py` → `motion_sync.py` → `master_audio.py`.
- Screen-share tutorials: `prompts/screenshare_playbook.md` (`screen_edit.py` → `screen_annot.py` → kit `screen.js`).
- Talking-head hybrids (Hossam on camera + graphics): `prompts/talking_head_director.md` (`th_cut.py` → matte →
  `web_capture.py` → `th_layer.py` + kit `th.css`). Faceless motion stays the default for voice-only input.
- Cuts (retakes / false starts / fillers): `find_retakes.py` → review `review/cuts.html` → `input/edit.json` →
  `voice_edit.py --verify`. Never look for retakes in the whisper transcript (it hides them).
- Reusable assets: `library/INDEX.md` + `pipeline/lib.py` (find before generating, add/harvest after); rules: `docs/LIBRARY.md`.
- New-video prompt template for Hossam: `prompts/NEW_VIDEO_TEMPLATE.md`.
- Read `docs/LESSONS_LEARNED.md` before building; add new issues + fixes to it.
- Planned modules (redaction, reviewer handoff, 2D cartoon, B-roll, speed-ups): `docs/ROADMAP.md`.
- Final renders: `python pipeline/render_final.py <name>` (runs `preflight.py`; never final-render from Studio). Compositions must not load anything from the internet (GSAP is vendored in `assets/js/`).
- Generated SFX / images (GPT Image 2.5, medium) / clips via Higgsfield MCP: `prompts/higgsfield_playbook.md` (paid → approval gate).
- Brand (palette/fonts/RTL/avoids): `prompts/brand.md`. Style catalog + method matrix: `prompts/style_catalog.md`.
- Each video is one folder in `projects/<name>/` containing all assets, transcript, storyboard, composition, renders.
- `Hossam Images/` contains photos of Hossam for on-camera scenes (speaking / podcast / full body / transparent cutouts).
- Dashboard: `python dashboard/server.py` → http://localhost:8788.
- Verification commands: `python pipeline/selftest.py` (offline end-to-end), and inside a project's `composition/`: `npx hyperframes check`.
- Do not commit unless asked. Never commit `config/api_keys.json`.
