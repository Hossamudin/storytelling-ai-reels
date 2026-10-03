# Hossam Video Factory

Turn a script + voiceover into a finished professional video — storyboarding, approval gate,
AI image/video generation, branded Arabic captions, motion graphics, and rendering — operated
by your AI agent (opencode).

## Quick start

Requirements already satisfied on this machine: Python 3.13+, Node 24, ffmpeg.

1. **Add API keys** (once):
   - Start the dashboard: `python dashboard/server.py` → open http://localhost:8788 → **Keys** tab
   - Or: `copy config\api_keys.example.json config\api_keys.json` and fill it in
   - `GEMINI_API_KEY` (transcription + planning + video gen), `OPENAI_API_KEY` (GPT Image)
2. **Create a project** (the agent does this for you, or manually):
   ```
   python pipeline/new_project.py my-video --title "عنوان الفيديو"
   # drop voiceover.* (and optional script.md) into projects/my-video/input/
   ```
3. **Run the pipeline** — or just tell the agent: *"create a video from this voiceover"*:
   ```
   python pipeline/clean_audio.py my-video
   python pipeline/transcribe.py my-video        # Gemini, Egyptian Arabic + English keywords
   python pipeline/plan_scenes.py my-video       # storyboard with timing + costs
   ```
4. **Approve the storyboard** in the dashboard (Projects → project → review scenes → **Approve**).
   This is the credit-saving gate: nothing paid is generated before approval.
5. **Generate + assemble**:
   ```
   python pipeline/generate_assets.py my-video   # GPT Image 2.5 / Gemini Omni Flash clips + cost ledger
   python pipeline/captions.py my-video          # Arabic captions, English keyword pops
   python pipeline/assemble.py my-video          # HyperFrames composition scaffold
   ```
   The agent then refines each scene (motion graphics code, screenshots, Hossam images) and runs
   `npx hyperframes check` inside `projects/my-video/composition/`.
6. **Preview & render**: `npx hyperframes preview --background` (review), then `npx hyperframes render`.
   Final MP4 lands in `projects/my-video/renders/`.

## Offline test (no keys needed)

```
python pipeline/selftest.py
```
Runs the whole chain in mock mode on a generated test tone and validates the composition.

## Dashboard

`python dashboard/server.py` → http://localhost:8788

- **Projects** — stage stepper per project (ingest → … → done), storyboard status, estimated vs spent cost
- **Storyboard** — timeline bar colored by method, inline scene editing (time/beat/style/method/prompts), Approve/Reject
- **Config** — model names (transcribe / plan / image / video), resolutions, hook rules, caption style, unit costs. Model upgrades = edit one field.
- **Keys** — set API keys locally (stored in `config/api_keys.json`, gitignored, never displayed back)

## How footage is chosen (per scene)

| Method | What | Cost |
|---|---|---|
| `code` | Motion graphics written as HyperFrames HTML | free |
| `direct_image` | Generated/downloaded image + code motion | image |
| `image_animate` | Image → AI video (first frame) | image + video |
| `first_last_frame` | Two images → AI video interpolation | 2 images + video |
| `text_to_video` | Direct AI video | video |
| `screenshot` | Real UI captured by the agent | free |
| `hossam_image` | Photo of Hossam from `Hossam Images/` | free |

The planner enforces the **hook rule** (first 15s = 3–5 rapid mixed-method cuts) and keeps ≥40–60%
of body scenes on free methods. AI video clips are ≤10s (Omni Flash limit), 720p default.

## Providers & model upgrades

- Transcription: `gemini-3.5-transcribe` via Gemini API (or your n8n webhook — set
  `transcription.provider: "n8n"`; use `localhost:5678` from Windows, `host.docker.internal:5678` from docker)
- Planning: `gemini-3.5-pro`
- Images: `gpt-image-2.5` (medium quality; size map per aspect in config)
- Video: `gemini-omni-flash-1.1` (`predictLongRunning`, 720p, ≤10s)
- Higgsfield or other MCPs: when connected, the agent generates through them and logs to the ledger.

All model names/urls live in `config/config.json` — change them in the dashboard Config tab.

## Repo layout

```
config/          config.json (behaviour+models) · api_keys.json (yours, gitignored)
pipeline/        new_project · clean_audio · transcribe · plan_scenes · generate_assets · captions · assemble · selftest
prompts/         brand kit · style catalog · planner system prompt · image/video prompt templates · quote design
dashboard/       server.py + UI (projects · storyboard approval · config · keys · logs)
projects/<name>/ input · assets(voice/images/videos+ledger) · transcript · storyboard · composition · renders
Hossam Images/   photos of Hossam for on-camera scenes
.opencode/skill/hossam-video-factory/   the agent's operating manual
```
