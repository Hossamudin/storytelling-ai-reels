---
name: risha-2d-animation
description: "Risha (ريشة) — 2D animation studio: brings drawings to life synced to a voice — talking/gesturing vector characters with automatic lip-sync and blinks, whiteboard and sketch explainers that draw themselves, paper cut-out and stop-motion styles, doodle overlays on footage, animated infographics, Lottie files, and AI-generated 2D frames. Designs the character sheet, rigs it, acts it to the words, and renders offline in any language (Arabic RTL mirrored correctly). Onboards beginners (machine check, brand, tools). Use whenever someone wants a cartoon, an animated character or mascot, a whiteboard video, hand-drawn or doodle animation, cut-out/collage animation, kids/educational animation, or says 'animate a character', 'كرتون', 'رسوم متحركة', 'انيميشن 2D', 'شخصية كرتونية', 'وايت بورد' — even if they just say 'make it animated'."
---

# Risha · ريشة — the 2D animation studio

*Risha* is the artist's quill: it draws, then breathes life into the drawing. This skill designs characters that read
well small, rigs them so they can act, syncs their mouths to the voice, and stages them so the message — not the
animation — is the hero.

{{CORE}}

## The workflow (details: `references/animation-2d.md`)

1. **Pick the technique with the creator** (show 2–3 options as one-line descriptions or quick snapshots): puppet
   character · whiteboard/sketch · paper cut-out/stop-motion · doodle overlay · animated infographic · Lottie ·
   AI-generated frames · sprite-sheet loops. Mixes are great (a host presenting a whiteboard that draws itself).
2. **Voice** (word times drive the acting — `references/voice-and-cuts.md`):
   ```bash
   python engine/pipeline/new_project.py <name>               # copy the voice into projects/<name>/input/
   python engine/pipeline/clean_audio.py <name> --no-silence-cut
   python engine/pipeline/transcribe.py <name>
   python engine/pipeline/find_retakes.py <name>              # free local mode without a key -> review/cuts.html
   # input/edit.json: accepted cuts + "parts" (one part per deliverable, e.g. trim to a complete phrase)
   python engine/pipeline/voice_edit.py <name>                # -> assets/voice/<part>.wav + transcript/<part>_words.json
   ```
   Listen to the voice first: if it doesn't match the brief (wrong line, cut mid-word), say so before animating.
3. **Design** — character sheet first for anything recurring: front pose, 4 expressions, the mouth set (X/M/A/O),
   brand colors on clothes/props, simple shapes that read on a phone. No realistic people (unless it's the creator's own
   photo), no copied IP, respect the avoid list (some creators prefer object-characters: a talking mic, a cup).
   Save the sheet to the library so episode 2 matches episode 1.
4. **Concepts → approval** (staging, style, the signature moment; any paid generation with cost).
5. **Build**:
   ```bash
   python engine/pipeline/new_motion_video.py <name> --part <part> --voice projects/<name>/assets/voice/<part>.wav --aspect 16:9 --preset light
   # scenes.json: {"id":"s1","start":0,"duration":8.8,"title":"…","template":"character_2d"}  (+ other scenes)
   python engine/pipeline/motion_sync.py <name> --part <part>
   python engine/pipeline/lipsync.py <name> --part <part>       # mouth keys from the voice (any language), auto-linked
   # restyle the rig in compositions/s1.html (keep the ids), add gestures at word times - 0.15 s
   cd projects/<name>/<part> && npx hyperframes check && npx hyperframes snapshot --at <gesture peaks>
   ```
   Lottie files: `python <skill-dir>/scripts/vendor_lib.py lottie projects/<name>/<part>`.
6. **Preview → approval → `render_final.py`** → deliver, explain, suggest, ask.

## Acting rules that make cheap animation look expensive

- Anticipation before big moves; overlap (hands finish after arms); ease everything; holds of 0.3–0.6 s after a big
  gesture; breathing + head sway + irregular blinks as constant secondary life.
- Gestures land 0.1–0.2 s before the stressed word; the character points or looks at what the voice names.
- Staging: character on one side, the idea on the other; mirrored automatically for RTL (the template does it).
- The mouth moves only while the voice speaks; closed in pauses.

## Rig rules (each cost time once)

- Every moving part is its own SVG group. GSAP ignores CSS `transform-origin` on SVG: use `svgOrigin`, or a
  `translate(joint)` wrapper + transparent pivot disc (as in the template).
- Limbs carry `data-layout-allow-orbit` (they rotate about joints on purpose; otherwise `check` flags them as gauge needles).
- Layout decisions inside scene files are made in the scene script (`getComputedStyle(...).direction`), because scene
  styles are scoped. Text never covers the face; the character never covers the text.
- Deterministic: finite repeats, seeded "randomness", no clocks.

## Paid options (approval gate, `references/tools-connection.md`)

AI character sheets and keyframes (consistent prompt family, plain background, no text) → cut out with
`npx hyperframes remove-background` → animate in code (cheap and controllable). Image→video only for 3–5 s hero shots.

## Domain references

`references/animation-2d.md` (techniques, character design, acting, whiteboard/cut-out/Lottie/AI recipes, checklist) ·
`references/motion-director.md` (timing, vocabulary, idea banks) · `references/style-presets.md` ·
`references/storytelling.md`.
