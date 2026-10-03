---
workflow: general-video
flow: automation
storyboard: no
message: "A podcast that stalled after two episodes comes back to life when AI works as a full production team — Vibe Automation, in 6 steps."
destination: youtube
aspect: "16:9"
language: ar-EG
audience: Arabic creators and professionals curious about practical AI
length: "intro ~67s + outro ~21s"
angle: narrative
---

# Vibe Automation — YouTube intro + outro

## Intent
Hossam's own voice (edited: repeats, false starts and dead air removed) drives two 100% motion-graphics
pieces for a long YouTube video: an intro that hooks with the stalled-podcast story, shows the
human-heavy production pipeline, flips it into an AI team, reveals "Vibe Automation · 6 steps",
then the channel intro + subscribe; and an outro with like/share/comment CTAs ending on an end-screen
layout pointing at two related videos.

## Stated by user
- Premium Arabic motion graphics, no talking head, use my voice, cut silences/repetitions.
- Effects: zoom in/out, parallax, bloom, motion blur. Think like a motion-graphics artist.
- SFX allowed, **no music**.
- Stop at Studio preview approval before rendering.
- Format: 16:9 intro + outro (answered in chat).

## Inferred / defaulted (receipts)
- Brand from `prompts/brand.md`: Tropical Fruit Punch palette, Noto Kufi Arabic + Manrope, light premium
  editorial canvas, RTL; avoid robots/computers/offices/money/blue/purple/black backgrounds.
- No `rawreel` / `fonts/` supplied → fonts taken from brand (OFL files bundled locally).
- Visuals are code-drawn vector (crisp Arabic, on-brand); no generated imagery needed.
- SFX from the bundled HyperFrames library.
- Outro holds ~5s after the voice so YouTube end-screen elements have ≥10s on the end-screen layout.

## Assets
- `assets/voice/intro.wav` (66.39s), `assets/voice/outro.wav` (16.91s) — produced by `../edit.py`.
- Word timings: `../transcript/intro_words.json`, `../transcript/outro_words.json`.
