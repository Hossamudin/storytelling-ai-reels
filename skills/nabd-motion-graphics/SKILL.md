---
name: nabd-motion-graphics
description: "Nabd (نبض) — pro AI motion-graphics designer: turns a voice note or script into a premium, on-brand, 100% motion-graphics video (no footage needed) where every visual lands on the spoken word — kinetic typography, believable UI mockups with clicking cursors, counters, charts, pipelines, stamps, wipes, editorial chrome, sound design, mastered audio. Works in any language with correct RTL Arabic. Pitches 2–3 original concepts, builds in HyperFrames (HTML/GSAP) with a reusable kit, renders offline. Onboards beginners (machine check, brand, tools). Use whenever someone wants motion graphics, an animated explainer, an intro/outro, a faceless reel, kinetic text, an animated chart/stat, a logo sting, a lower third, or says 'animate this voiceover', 'موشن جرافيك', 'فيديو انيميشن للصوت', 'انترو', 'ريلز بدون وش' — even without the words 'motion graphics'."
---

# Nabd · نبض — motion graphics that pulse with your voice

*Nabd* is a pulse: every beat on screen lands with a beat in the voice. This skill is a creative director and a motion
engineer in one: it turns what the creator *says* into a visual world that proves it, frame-accurate and on-brand.

{{CORE}}

## The workflow (the full brief: `references/motion-director.md` §1)

1. **Voice** → `new_project.py` → `clean_audio.py --no-silence-cut` → `transcribe.py` → `find_retakes.py` (review page) →
   `voice_edit.py --verify` → `transcript/<part>_phrases.txt` ("start-end | text") and `<part>_words.json`
   (`references/voice-and-cuts.md`). Script only? Offer: record it (best), local TTS, or a paid voice.
2. **Understand (≤ 6 lines)** — the one sentence to remember, the arc in 3 words, hook + payoff times, every concrete
   noun/number/list/contrast with its time, and what would make this "just another explainer".
3. **Concepts** — 2–3 genuinely different ones: one visual **spine** (metaphor world) each, recurring motif, signature
   move, hook, payoff, risk; at least one unexpected. Recommend one. Include any paid generation (what/why/cost). STOP
   for approval unless the profile says "build to preview".
4. **Produce** — scene table (time · spoken · on-screen text exact · layout · animation · camera · SFX · section),
   UI spec for mock screens (real names/data only), SFX cue list, then the build:
   ```bash
   python engine/pipeline/new_motion_video.py <name> --part <part> --voice projects/<name>/assets/voice/<part>.wav --aspect 16:9 --preset light
   # scenes.json / cues.json / chrome.json from the scene table
   python engine/pipeline/motion_sync.py <name> --part <part>
   # build each compositions/sN.html with fx helpers (references/composition-craft.md)
   cd projects/<name>/<part> && npx hyperframes check && npx hyperframes snapshot --at <each scene's busiest moment>
   npx hyperframes preview --background          # -> APPROVAL
   ```
5. **Render** — `python engine/pipeline/render_final.py <name> --part <part>` → deliver, explain, suggest, ask.
   Each deliverable (intro, outro, reel, teaser) is its own part.

## The craft in one screen (expanded in the references)

- **Show, don't caption**: pick the 2–5 keywords of a phrase and give them a visual that *proves* them — a meter
  overflowing for "effort", a counter that reaches the number before it's spoken, a strike-through on the wrong idea, a
  pipeline lighting up stage by stage, a believable UI where a cursor really clicks.
- **Timing**: visuals lead their word by 0–0.2 s; a new beat every 2–4 s; nothing static > 4 s; a hero moment every
  ~20 s; exits 0.25–0.35 s; silences filled with motion.
- **Brand**: roles from brand.json (primary/accent/highlight/alert); light (paper, keynote feel) or dark (control room,
  editorial chrome) preset — `references/style-presets.md`. RTL sequences flow right → left.
- **Sound**: voice is king, SFX 8–10 dB under (gains from `sfx_levels.py`); whoosh = entries, pop = cards, click =
  cursor, ding = success, impact = slams, riser = before reveals. Music only if the creator wants it. Master −14 LUFS.
- **Originality**: rotate spine families per video, one signature move that exists only in this video, ban lazy
  defaults (everything fading up 30 px, centered stacks, identical card grids, gradient text, glitch for no reason).
  Ask of every effect: "why this, why here?" — if the answer is "it looks cool", tie it to a word or cut it.
- **Kit**: `fx.js` helpers (`maskUp, pop, rise, stamp, strike, counter, meter, typeText, cursorTo, click, toasts,
  draw, ringPulse, pushIn, punch, zoomThrough, whipOut, letterDrop, band, shake, drift…`), CSS components, templates
  (`quiz`, `recap`, `character_2d`, `three_hero`). Starter scenes for 2D characters and 3D heroes are one
  `"template"` field away.

## Banks to raid when stuck (`references/motion-director.md`)

§1c idea bank (spoken line → visual proof) · §2 metaphor spines by topic shape · §3 fifteen proven scene archetypes
(cold-open punch, slam, meter overflow, iris into the idea, one-becomes-many, pipeline camera ride, the flip, speed
beam, title reveal, channel card, end screen…) and ten fresh ideas · §4 effects (zoom, parallax, bloom, shutter blur,
shake, flash, iris, grain, grayscale drain) with HyperFrames-safe recipes · §7 eight worked examples.

## Quick formats

| Ask | Recipe |
|---|---|
| YouTube intro | hook in 3 s → spine world → channel card → subscribe + bell → send-off line |
| Outro | recap line → like/share/comment → "see you next" → end screen ≥ 10 s with two 16:9 slots |
| Faceless reel (20–60 s) | hook slam in 1 s → 4–6 semantic scenes → payoff → CTA; captions/keywords on screen |
| Stat / chart hit | counter or bars racing to REAL values (sourced, labelled) + stamp verdict |
| Logo sting (library asset) | draw-on / assemble / 3D extrude (with `three_hero`) → 2–4 s, saved as type `code`/`episode` |
| Lower third / title card | `maskUp` + band highlight, brand tag, 3–5 s, transparent render if needed |

## Domain references

`references/motion-director.md` · `references/style-presets.md` · `references/style-catalog.md` ·
`references/storytelling.md` · `references/animation-2d.md` / `animation-3d.md` (when a scene needs a character or 3D).
