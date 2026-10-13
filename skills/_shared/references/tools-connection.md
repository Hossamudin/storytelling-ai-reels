# Connecting tools — keys, AI generators, and the free alternatives

Principle: **everything works at $0**, and each connection unlocks more quality or speed. Never push a paid tool;
explain what it adds and what it costs, and let the creator decide. Record the result (✓/✗ only, never values)
in `profile.md`.

## The free baseline (nothing to connect)

| Need | Free path |
|---|---|
| Rendering | HyperFrames (`npx hyperframes …`) — HTML/CSS/GSAP → MP4, runs locally |
| Transcription with word timings | `transcribe.py --provider local` (faster-whisper; `pip install faster-whisper`). Model in `config.json → transcription.local.model`: `small` (laptop default, 0.5 GB), `medium` (1.5 GB) / `large-v3` (3 GB download; GPU; much better for Arabic and names) |
| Voiceover from a script | `npx hyperframes tts "text" -o voice.wav` (Kokoro, English + a few European/Asian languages; `pip install kokoro-onnx soundfile`). No Arabic voice locally → record yourself, or use a paid TTS |
| Background removal (person / logo) | `npx hyperframes remove-background in.mp4 -o matte.webm` (CPU is slow: start early) |
| SFX | 19 bundled kit sounds (`library/sfx`), plus `/media-use` if HyperFrames skills are installed |
| Real-page evidence | `python engine/pipeline/web_capture.py <url> --out <dir> --full` (`pip install playwright && playwright install chromium`) |
| Graphics, diagrams, UI mocks, charts, captions | code (the motion kit) — crisp text in any language, exact timing, free |

## API keys (stored in `<studio>/config/api_keys.json` or environment variables)

| Key | Unlocks | Typical cost | Notes |
|---|---|---|---|
| `OPENAI_API_KEY` | whisper-1 word timings (best), the retake finder's verbatim model + LLM editor (catches paraphrased restarts; the free mode uses rules), edit verification, `lib.py describe` | $0.01–0.10 per video | platform.openai.com → API keys → add $5 credit. Model names are plain config fields — upgrade them in `config.json` |
| `GEMINI_API_KEY` | optional text/vision tasks | free tier exists | **Free-tier Gemini fails for transcription**: 503 "high demand", 429 on Pro, truncated JSON, fake uniform 0.5 s word timings. Use only with a paid key, and never for timing |
| `ELEVENLABS_API_KEY` | high-quality TTS / voice clone (Arabic included) | per character | only if the creator wants a synthetic voice; their own voice is the default |

How to guide a beginner: open the provider's key page with them (browser), let *them* copy the key and paste
it into `config/api_keys.json` with a text editor. If they paste a key into chat, store it, then advise them
to rotate it later. Check presence with `python <skill>/scripts/setup_studio.py keys`.

## AI generation through MCP (images, SFX, clips, 3D) — e.g. Higgsfield

If an MCP server for media generation is connected (look for tools like `generate_image_batch`,
`generate_video_batch`, `generate_audio_batch`, `jobs_wait`, `scene_builder_3d_*`), it adds what code can't:
bespoke SFX, photoreal/clay/3D objects and plates, short cinematic clips, 3D scenes.

**Paid → approval gate.** List planned generations (what · why · model · count · est. cost) in the creative
treatment; generate only after the creator approves. Log every job in `projects/<name>/assets/ledger.json`
(job id, model, prompt, cost, file).

Working ids seen in production (Oct 2026; re-check the catalog, ids change): images `gpt_image_2_5`
(`quality: "medium"`, aspect per asset), video `seedance_2_0` (image→video: `medias: [{value: <image job id>,
role: "start_image"}]`, 5 s), SFX `mirelo_text_to_audio` (needs `duration`). Guessed ids fail with "unknown model".

Flow: `create_project` (one per video, use its `default_folder_id`) → batch generate (≤ 12 per call) →
`jobs_wait` → download results into `assets/higgsfield/` (or `assets/generated/`) → `lib.py add` the keepers.
Never retry a whole batch after a partial failure — retry only the failed items. If a tool asks which balance to
spend (free trial vs credits), ask the creator.

Aspect per image: full-frame plate 16:9 → 1536×1024 · 9:16 → 1024×1536 · icon/object/sticker/tile → 1:1 ·
portrait card → 2:3. Budget heuristic per 60–90 s video: ≤ 6 SFX, ≤ 4 images, ≤ 2 clips (more only when the
concept is built on them).

**Never generate:** text inside images (wrong letters, especially Arabic) — all text stays in code · realistic
people (the creator appears via their own photos) · anything on the brand avoid list · music unless the creator
wants it · a diagram, UI, counter or list (code does those better).

Prompt templates:
- SFX: `<action> sound effect, <material>, <space>, <character>, clean studio recording, no music, no voice, single hit, tight tail` (0.4–3 s)
- Image: `<metaphor object>, minimal premium 3D/clay/vector style, brand palette <hexes>, soft studio lighting, generous negative space, <plain background for cut-out | seamless plate>, no text, no letters, no people, no logos`
- Clip: `<slow camera move> over <abstract/object subject>, brand palette…, minimal, premium, soft light, loopable, no text, no people` (3–6 s, muted)

After download: SFX → `python engine/pipeline/sfx_levels.py --dir <part>/assets/sfx` (per-file gain);
images to cut out → `npx hyperframes remove-background`.

## Other connections worth offering

- **n8n / automation**: transcription via webhook (`transcription.provider: "n8n"`; from Windows use
  `localhost:5678`, from inside Docker `host.docker.internal:5678`).
- **Social scheduling MCPs** (posting the finished video) — only with explicit approval per post.
- **Blender** (3D skill) — free, local; `env_check.py` detects it.
- **Figma / design files** — if the creator's brand lives in Figma, import tokens and assets from there.

## When an API fails

Diagnose before switching: read the HTTP status and message. 401 → wrong/expired key · 429 → rate/quota
(free tier?) · 400 → wrong parameter or model id (e.g. `gpt-4o-transcribe` rejects `verbose_json` word
timestamps) · 5xx → retry with backoff, then report. Tell the creator what happened in one plain sentence and
the fix. Fall back to the free path only when they agree.
