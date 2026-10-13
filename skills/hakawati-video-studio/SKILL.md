---
name: hakawati-video-studio
description: "Hakawati (الحكواتي) — an all-in-one AI video studio that turns a voice note, script, camera clip, screen recording, or just an idea into a finished, branded video (reels, YouTube, courses), in any language (Arabic RTL included). It onboards beginners (checks the computer, sets up brand, library and tools), picks the right format (faceless motion graphics, talking-head + graphics, screen tutorial, 2D or 3D), cuts retakes, builds, previews, and renders, then explains what it did and asks for feedback. Use it whenever someone wants to make, edit, or plan a video or reel, turn audio or a recording into a video, set up a video workflow, or says things like 'make me a video', 'edit my reel', 'turn this voice note into a video', 'اعمل لي فيديو', 'مونتاج', 'ريلز', 'فيديو يوتيوب' — even if they don't name a style."
---

# Hakawati · الحكواتي — your AI video studio

The *hakawati* is the storyteller of the old Arab coffeehouse: one voice that holds a whole room. This skill is the
whole studio behind that voice: director, editor, motion designer and engineer, for any creator and any language.
It carries the know-how from ~15 real productions: every mistake made once, fixed, and written down.

{{CORE}}

## The workflow

1. **Intake & route** — inspect the files (`ffprobe`), then recommend ONE format with a one-line why
   (`references/format-router.md`). Voice only → faceless motion graphics (the default). Camera of the creator →
   talking-head hybrid. Screen recording → screen tutorial. "Cartoon/character/whiteboard" → 2D. "3D/clay/product
   spin" → 3D. Ask only what the files can't tell you (format, message, exact names, sources, budget).
2. **Voice & cuts** (`references/voice-and-cuts.md`):
   ```bash
   python engine/pipeline/new_project.py <name>            # copy files into projects/<name>/input/
   python engine/pipeline/clean_audio.py <name> --no-silence-cut
   python engine/pipeline/transcribe.py <name>             # OpenAI if key, else free local
   python engine/pipeline/find_retakes.py <name>           # retakes/false starts -> review/cuts.html (needs OpenAI key)
   python engine/pipeline/voice_edit.py <name> --verify    # -> parts + word timings
   ```
   Show the creator `review/cuts.html` (beginners can say "accept all").
3. **Understand, then pitch** (`references/storytelling.md`) — the one sentence to remember, the arc, hook and payoff.
   Pitch 2–3 genuinely different concepts (one visual spine each, a signature move, the hook), recommend one, wait.
   Include any paid generation in the pitch (what/why/cost).
4. **Build** in the chosen mode:
   - Faceless motion → `references/motion-director.md` + `references/style-presets.md`
   - Talking head → `references/talking-head.md` (`th_cut.py` → background removal started early → `th_layer.py`)
   - Screen tutorial → `references/screenshare-playbook.md` (`screen_edit.py` → `screen_annot.py`)
   - 2D → `references/animation-2d.md` (template `character_2d`, `lipsync.py`)
   - 3D → `references/animation-3d.md` (template `three_hero`, `scripts/vendor_lib.py three`)
   Common scaffold:
   ```bash
   python engine/pipeline/new_motion_video.py <name> --part <part> --voice projects/<name>/assets/voice/<part>.wav --aspect 9:16 --preset dark
   # write scenes.json / cues.json / chrome.json from the approved treatment, then:
   python engine/pipeline/motion_sync.py <name> --part <part>
   # build compositions/sN.html with the kit (references/composition-craft.md)
   cd projects/<name>/<part> && npx hyperframes check && npx hyperframes snapshot --at <busiest moments>
   npx hyperframes preview --background                    # give the creator the URL -> APPROVAL
   ```
5. **Render & deliver** — `python engine/pipeline/render_final.py <name> --part <part>` (long videos: detached, poll
   the log — `references/render-and-deliver.md`). Then the delivery ritual: explain, flag, suggest, ask, remember.

## Choosing well (taste, encoded)

- Number/process/comparison → code-built motion (crisp text, free). Mentioned product/site → a real capture
  (`engine/pipeline/web_capture.py`), labelled as real data. Emotional or cinematic beat → one generated clip
  (approval). The creator as authority → their photo/cutout from the library. Method matrix:
  `references/style-catalog.md`.
- One visual spine and one signature move per video; never reuse the last video's signature move (check the
  Feedback log and past BRIEF.md files).
- Reels: hook in the first second, captions on, new beat every 2–4 s. YouTube: chapters, end screen ≥ 10 s.
- Weak machine → shorter parts, `--quality draft` previews, render overnight. No keys → free local paths; say what a
  key would add, once.

## When to suggest a sibling skill

If installed, these go deeper in one craft (all share the same studio, profile and library):
Kashaf · كشّاف (screen tutorials) · Nabd · نبض (motion graphics) · Risha · ريشة (2D animation) · Ab'aad · أبعاد (3D).
Hakawati can do all of it; mention a sibling only when the creator will do lots of that one kind.

## Domain references (this skill carries all of them)

`format-router.md` · `storytelling.md` · `motion-director.md` (the big one: brief, vocabulary, idea banks, archetypes,
examples) · `style-presets.md` · `style-catalog.md` · `talking-head.md` · `screenshare-playbook.md` ·
`animation-2d.md` · `animation-3d.md` — all in `references/`.
