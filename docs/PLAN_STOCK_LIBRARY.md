# Plan — free stock assets for the library (2026-10-11)

Goal: pre-load `library/` with free, legally downloadable assets the AI-news / explainer videos reuse constantly,
so builds pull them with `lib.py find/use` instead of generating or hunting per video.

## What and from where

| Batch | Type | Source (license) | Target |
|---|---|---|---|
| A. AI-company logos | `logo` | LobeHub icons `@lobehub/icons-static-svg` + `-png` via jsDelivr (MIT; marks are trademarks of their owners — editorial/nominative use) | ~40 brands: OpenAI, Anthropic/Claude, Gemini, DeepMind, Meta AI, Mistral, DeepSeek, Qwen, xAI/Grok, Perplexity, Midjourney, Runway, ElevenLabs, Hugging Face, Cohere, Kimi, Copilot, Ollama, … — colour SVG + mono SVG + colour PNG |
| B. Big tech + tool logos | `logo` | Simple Icons (CC0 SVG) + LobeHub; Wikimedia Commons for brands missing there | Google, Microsoft, Apple, Nvidia, Amazon/AWS, Meta, Tesla, GitHub, n8n, Zapier, Make, Notion, Figma, Cursor, Vercel, Supabase, YouTube, X, LinkedIn, Instagram, TikTok, WhatsApp, Telegram, Slack, Discord, … |
| C. B-roll footage | `broll` | Mixkit (Mixkit free license), NASA (public domain), Wikimedia Commons (PD/CC0 only) | ~25 clips: data centre/servers, coding/typing, circuit macro, abstract network/particles loops, robot arm, office teamwork, phone/app use, city timelapse, Earth from space — trimmed ≤15 s, H.264, no audio, ≤1080p |
| D. Editorial photos | `img` | Wikimedia Commons (CC BY / BY-SA / PD — author + license recorded) | AI leaders (Altman, Amodei, Hassabis, Huang, Pichai, Nadella, Zuckerberg, Musk, Suleyman, LeCun…) + hardware (GPU, data centre, chip wafer) |

No paid generation — approval gate not triggered. No Pexels/Pixabay/Unsplash (need API keys we don't have).

## How

1. Four Haiku 5.5 agents run in parallel, each downloads into its own staging dir
   (`<scratchpad>/stock/<batch>/`) and writes `manifest.jsonl` (`file, type, subject, desc, tags, source`).
   They never touch `library/index.jsonl` (parallel `lib.py add` would race on the index).
2. Ingest serially: `lib.py add <file> ... --move` per manifest line (sha1 dedup, auto-naming), then `lib.py index`.
3. Verify: counts per type, contact sheets render, spot-check a few files, licences recorded in `source`.

## Tagging conventions for these batches
- every item: `stock` + license tag (`cc0`, `mit`, `mixkit-license`, `public-domain`, `cc-by`, `cc-by-sa`)
- logos: `trademark`, brand name, `color` / `mono`, `svg` / `png`
- CC-BY(-SA) photos: `attribution-required`, author + license in `source`
