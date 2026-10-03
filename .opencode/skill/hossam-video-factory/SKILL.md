---
name: hossam-video-factory
description: Turn Hossam's script + voiceover into a finished professional video end to end. Trigger when the user wants to create/produce/render a video, continue a video project, edit a storyboard, add scenes/captions, or check video factory status. Orchestrates the pipeline in pipeline/, the approval gate, asset generation (code / GPT Image / Gemini Omni Flash), HyperFrames assembly, and rendering.
---

# Hossam Video Factory — agent operating manual

You are the director, editor, and engineer. The repo is a video production factory:
`input (script + voice)` → `clean audio` → `transcribe (Gemini)` → `plan storyboard` →
**[APPROVAL GATE — mandatory]** → `generate assets` → `captions` → `assemble HyperFrames` →
`refine scenes` → `render` → `deliver`.

Everything runs from the repo root. Config: `config/config.json` (editable via dashboard).
API keys: `config/api_keys.json` or env (`GEMINI_API_KEY`, `OPENAI_API_KEY`). Check with
`python -c "import sys; sys.path.insert(0,'pipeline'); import common as C; print(C.key_status())"`.

## Before every run
Read `docs/LESSONS_LEARNED.md` (issues → fixes → prevention). When you hit a new problem, add it there.

## Asset library (check it before generating anything)
`library/INDEX.md` lists every reusable asset (Hossam photos/cutouts, logos, generated images, b-roll, SFX, real
captures, screen recordings, finished episodes, code components). `python pipeline/lib.py find "<words>"` →
`lib.py use <id> <project-or-part> [--to assets/sfx/lib] [--as name]`. Before any paid generation: `find`. After a
generation, capture or recording worth keeping: `lib.py add …` (or `lib.py harvest <project>` at delivery);
`lib.py describe` captions new images with a vision model. Raw inputs from `videos/` that may recur go in too.

## Hard laws
1. **Never generate paid assets before the user approves the storyboard** (dashboard Approve button, or explicit "approved" in chat). `generate_assets.py` enforces this; `--force` only after explicit chat approval.
2. Never modify `config/api_keys.json` contents in chat output; keys are secret.
3. Each video = one folder under `projects/<name>/` holding ALL its assets.
4. Use `Hossam Images/` (repo root) for photos of Hossam (speaking / podcast / full body / transparent cutouts). Copy the chosen file into the project's `assets/images/`.
5. Arabic is the main language; English keywords stay Latin-script. Brand: palette + fonts in `prompts/brand.md` — obey everywhere.
6. Don't commit unless asked.

## Pipeline commands (run from repo root)
```
python pipeline/new_project.py <name> --title "..."     # scaffold
# copy user's voiceover (+ script.md if any) into projects/<name>/input/
python pipeline/clean_audio.py <name>                   # ffmpeg cleanup, timing preserved
python pipeline/transcribe.py <name>                    # openai_whisper word timestamps (default); gemini_api needs a PAID key
python pipeline/plan_scenes.py <name> [--aspect 9:16]   # storyboard.json + storyboard.md
# >>> APPROVAL GATE: user reviews (dashboard) <<<
python pipeline/generate_assets.py <name>               # images + AI videos, cost ledger
python pipeline/captions.py <name>                      # keyword-styled chunks
python pipeline/assemble.py <name>                      # composition/index.html scaffold
cd projects/<name>/composition && npx hyperframes check # must pass 0 findings
npx hyperframes preview --background                    # give user the URL
npx hyperframes render                                  # only after user approves preview
```

## Phase-by-phase judgment

### 0. Intake
- Voice file may be audio OR video (extracted automatically). Script optional (improves planning).
- If user gives **script only (no voice)**: produce voiceover via the `media-use` skill audio engine (TTS), save to `input/`, then continue. If user gives **voice only**: transcription IS the script.
- If user provides screen recordings of AI tools: extract frames/segments with ffmpeg into `assets/videos/` and use them as scene footage (`screenshot` method).

### 1–2. Audio + transcript
- `clean_audio.py` preserves timing (no silence cuts) — transcript timestamps stay valid.
- Default provider `openai_whisper` (whisper-1 verbose_json) = real word timings. Never add a
  `prompt` hint (it makes Whisper skip matching speech). A free-tier Gemini key returns 503/429,
  truncated JSON and fake 0.5 s timings — only use `gemini_api` with a paid key.
- Editorial cut (repeats, false starts, dead air) — ONE engine, no per-project edit.py:
  `python pipeline/find_retakes.py <name>` (verbatim chunk transcription with gpt-transcribe + an LLM editor pass;
  whisper-1 hides retakes, so never hunt for them in transcript.json) → `input/edit.proposed.json` +
  `review/cuts.html` (listen before/after, tick, export) → copy to `input/edit.json` (+ phrase `fix` entries for
  names) → `python pipeline/voice_edit.py <name> --verify` (edges snapped to the quietest 10 ms, frame-grid keep
  ranges, caption words re-timed on the EDITED audio with verbatim spelling, diff of planned vs heard).

### 3. Planning review (you are the director)
Read `storyboard.md` and sanity-check before showing the user:
- Hook: 3–5 rapid cuts inside first `hook.max_duration_s` (15s), mixed methods. If the LLM output is weak, edit `storyboard.json` yourself (you have taste) — fix weak image prompts, upgrade screenshot opportunities, add the closing quote card per `prompts/quote_design.md`.
- Methods follow `prompts/style_catalog.md` selection matrix. Code scenes ≥ 40–60% of body (free + crisp Arabic text).
- AI video clips ≤ 10s (Omni Flash limit); scenes longer than the clip get image+code motion or chained clips.
- Present to user: scene table (time / method / headline / cost) + total estimated cost + dashboard URL (`python dashboard/server.py` → http://localhost:8788). WAIT.

### 4. Asset generation
- Run `generate_assets.py`; failures print retry commands (`--only S03`).
- `screenshot` scenes: YOU capture them — use the browser tools on the real URL the narration names (model UI, tool, article). Save to `assets/images/<SID>_first.png`, then re-run `assemble.py`. Show prompt/result/cost on screen when the video is ABOUT an AI model (fetch real examples; halal-compliant imagery only).
- `hossam_image` scenes: pick the best match from `Hossam Images/` and copy it in.
- Downloaded/generated resource images (blog post figures, model outputs) go to `assets/images/`; record provenance in `assets/ledger.json` via a manual entry if not generated by script.

### 5. Captions
`captions.py` auto-detects English keywords (Latin tokens + storyboard `caption_keywords`) and styles them with brand colors. Style presets in config: `punch` (default) / `minimal` / `karaoke`.

### 6. Assembly + refinement (the craft)
`assemble.py` builds a valid scaffold: scenes, voiceover track, low-volume SFX from AI videos, caption track. Then YOU refine using the hyperframes skills:
- `code` scenes → real motion graphics (load `/hyperframes-animation`, `/motion-graphics` patterns; follow `prompts/image_prompt_template.md` composition thinking but rendered in HTML/GSAP).
- Image scenes → ken burns/parallax already scaffolded; upgrade if warranted.
- Follow `hyperframes-core` contract: root `data-start="0"`, `class="clip"` direct children, one paused timeline in `window.__timelines`, `fromTo` (never CSS transform + tween), unique ids, no `repeat:-1`, no network in composition JS.
- RTL Arabic typography: Noto Kufi Arabic; English keywords Manrope with keyword color pop.
- `npx hyperframes check` until 0 findings. Check ASSEMBLY_NOTES.md for per-scene TODOs.

### 7. Deliver (motion / screen-share projects)
- **Final renders only via `python pipeline/render_final.py <name> [--part …]`** (preflight → render
  `--quality delivery --strict` → verify → master −14 LUFS → chapters → `projects/<name>/deliverables/`).
  Never final-render from Studio (no gates). Launch it detached for long videos and poll its log.
- `python pipeline/preflight.py <name>` on its own whenever you want to know if a project is render-ready:
  no remote URLs (GSAP is vendored), no missing assets, full-quality screen edit, grain off on screen
  recordings, durations consistent, `hyperframes check` clean.

### 7b. Deliver (storyboard pipeline)
- `npx hyperframes render` in `composition/` → move MP4 to `projects/<name>/renders/`.
- QC: duration ≈ voiceover + tail; captions legible; loudness (voiceover loudnorm'd already); videos' SFX ducked at 0.22 under voice.
- Report: total spend from `assets/ledger.json`, scenes by method, file path.

## Special modes
- **100% motion graphics from voice (no footage)** — the house style (approved Sept 2026).
  Knowledge: `prompts/motion_director_prompt.md` (v2 master prompt, vocabulary→kit map, idea bank,
  metaphor bank, archetypes, gotchas, originality rules, examples) · `prompts/style_presets.md`
  (`light` paper look / `dark` control-room look with editorial chrome) · `prompts/higgsfield_playbook.md`.
  Code: `kit/motion/` (base.css design system, `js/fx.js` helpers, root + scene templates, fonts,
  SFX library + `levels.json`). Flow:
  ```
  python pipeline/new_project.py <name>          # voice -> input/
  python pipeline/clean_audio.py <name> --no-silence-cut
  python pipeline/transcribe.py <name>           # openai_whisper words
  python pipeline/find_retakes.py <name>        # -> input/edit.proposed.json + review/cuts.html (retakes, false starts)
  # review, copy to input/edit.json (cuts / fix phrases / parts)
  python pipeline/voice_edit.py <name> --verify  # <part>.wav, <part>_words.json, <part>_phrases.txt
  # master prompt Step 1-2 -> Creative Treatment (2-3 concepts + Higgsfield generation plan) -> APPROVAL
  python pipeline/new_motion_video.py <name> --part intro --voice projects/<name>/assets/voice/intro.wav --aspect 16:9 --preset light
  # scenes.json / cues.json / chrome.json from the treatment
  python pipeline/motion_sync.py <name> --part intro
  # build compositions/sN.html with fx helpers; generated SFX -> assets/sfx/higgsfield + sfx_levels.py --dir
  cd projects/<name>/intro && npx hyperframes check && npx hyperframes preview --background   # -> APPROVAL
  npx hyperframes render && python ../../../pipeline/master_audio.py renders/<file>.mp4       # -14 LUFS / -1.2 dBTP
  ```
  Each deliverable (intro, outro, reel) is its own part/project. References:
  `projects/vibe-automation/` (light, 16:9) and `projects/kit-test/demo/` (dark, 9:16, UI/chrome/wipes).
- **Screen-share videos (tutorials, tool tours)** — `prompts/screenshare_playbook.md`. Flow:
  transcribe → analyse (gaps, screen activity, popups, ruler frames) → `input/screen_edit.json` →
  `screen_edit.py` (cuts, best take, J/L cuts, ramps, holds, freeze-and-explain) → `input/annotations.json`
  (SOURCE time/pixels) → `screen_annot.py` → scaffold (`--preset dark`, `"grain": false`) → `motion_sync.py`
  → check + snapshots → preview → APPROVAL → full-quality edit → render → `master_audio.py` → `chapters.py`.
  Non-distracting rule: the screen is the hero. No grain over recordings, one focus at a time, calm zooms.
  Learning aids: chapters, step tracker (`chrome.json "steps"`), recap + quiz templates over silent holds.
  Reference: `projects/screenshare-v1/`.
- **Talking-head hybrid (Hossam on camera + motion graphics)** — `prompts/talking_head_director.md`. Use it when the
  input is a camera video of Hossam and the user wants him on screen. Faceless stays the default for voice-only input
  or "no talking head". Flow: `voice_edit.py` → `th_cut.py` (camera cut on the same keep ranges + seams) →
  `remove-background` matte (start early, slow on CPU) → `web_capture.py` for named sources (real data beats
  illustration) → treatment with a FORMAT per beat (clean / text-behind / presenter+canvas / circle / full-screen /
  layered depth; 45–55 % face) → scaffold → scenes for the full-screen + canvas windows → `th.json` + `th_behind.html`
  + `th_front.html` + `th_front.js` → `th_layer.py` → `motion_sync.py` → check + snapshots → preview → APPROVAL.
  Reference: `projects/agent-harness/reel_th/` (twin of the faceless `projects/agent-harness/reel/`).
- **Higgsfield (MCP)** — bespoke SFX (`mirelo_text_to_audio`), images (GPT Image 2.5, medium, aspect per
  asset), short clips, 3D objects. Paid: include them in the treatment, generate after approval,
  batch + `jobs_wait`, download to `assets/higgsfield/`, log in `assets/ledger.json`. Never music,
  never text inside images. See `prompts/higgsfield_playbook.md`.
- **New AI model showcase**: when narration covers an image/video model, prefer real outputs over generated explanations — screenshots/downloads of actual results, show the prompt used, the result, and cost. If a generation MCP (Higgsfield etc.) is connected, use it and log usage to the ledger manually.
- **n8n transcription**: config `transcription.provider: "n8n"` (faster local workflow). From host Windows use `localhost:5678`, from docker `host.docker.internal:5678`.
- **Aspect**: default 9:16. `--aspect 16:9` for YouTube landscape.

## After delivery — always offer (one short list)
1. Reels / mobile version (9:16 cut per section, captions).
2. Article pack: key summary + ordered, named screenshots (`deliverables/article/NN_slug.png`) + Arabic outline.
3. Ideas + recommendations for the next video (learning aids, recording fixes, follow-ups).
Plus YouTube chapters (`python pipeline/chapters.py <name>`) for every long-form video.

## Monitoring
Dashboard: `python dashboard/server.py` → http://localhost:8788 — projects/stages, storyboard editing + approve, config (models, prompts behaviour, costs), keys, logs. Run it in background when the user wants to watch progress.
