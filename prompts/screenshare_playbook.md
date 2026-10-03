# Screen-share playbook — tutorials, tool tours, walkthroughs

Goal: **help the viewer understand.** Every edit and every graphic must make the explanation easier to
follow. Nothing may compete with the screen while you're explaining it. Reference build:
`projects/screenshare-v1/` (SureThing UI tour, 5:10 → 2:50).

---

## 1. Workflow

```bash
python pipeline/new_project.py <name>                                  # recording -> input/screen.mp4
python pipeline/clean_audio.py <name> --input projects/<name>/input/screen.mp4 --no-silence-cut
python pipeline/transcribe.py <name>                                   # OpenAI word timestamps
# ANALYSE (agent): transcript gaps, per-second screen activity, brightness popups, contact sheets,
#                  ruler frames at every moment you will annotate (see §3)
# write input/screen_edit.json  (keep / ramp / hold / freeze timeline)
python pipeline/screen_edit.py <name> --preview                        # edited.mp4 + edit_map.json + words.json
# verify: A/V durations match; re-transcribe edited.wav (no doubled/clipped words)
python pipeline/new_motion_video.py <name> --part composition --voice projects/<name>/assets/screen/edited.wav --aspect 16:9 --preset dark
# write input/annotations.json (SOURCE time + SOURCE pixels) -> output-time data + cutaway windows
python pipeline/screen_annot.py <name>
# scenes.json (screen + cutaways + quiz/recap templates), chrome.json (sections, wipes, steps, "grain": false), cues.json
python pipeline/motion_sync.py <name> --part composition
cd projects/<name>/composition && npx hyperframes check && npx hyperframes snapshot --at ... && npx hyperframes preview --background
# APPROVAL -> python pipeline/screen_edit.py <name>   (full quality, no --preview) -> copy edited.mp4 + edited.wav into the part
python pipeline/render_final.py <name>                                 # preflight -> render -> verify -> master -> chapters -> deliverables/
```

Copy `kit/motion/js/screen.js` + `kit/motion/css/base.css` into the project's `assets/` (the scaffold
does this). Composition files: `compositions/screen.html` (window + camera + annotation layer) +
cutaway scenes. See the reference build.

## 2. Editing rules (the cut)

1. **Dead air:** cut speech pauses > 0.9 s down to 0.4 s, but keep up to 1.2 s where the screen is changing.
   Remove silences longer than ~4 s entirely unless the screen action teaches something.
2. **Silent navigation:** cut it, or speed-ramp ×3–4 (`{"ramp": [a,b], "speed": 4}`) with the "×4" badge.
3. **Repetitions / retakes:** keep the best take, usually the later one. Re-explanations of a whole
   section count too: keep the version on the real/complete example.
4. **J/L cuts:** automatic in `screen_edit.py` (`jl` settings). Picture leads when the screen changes
   in the gap; voice leads otherwise. Max ±0.5 s.
5. **Junk:** OS dialogs, notifications, wrong windows, loading skeletons. Detect with the brightness/green
   detector and contact sheets; cut, or freeze over them.
6. **Holds:** `{"hold": s, "at": src_t}` = a silent pause on a chosen frame (cutaway breathing room, quiz,
   recap, opening title).
7. **Freeze-and-explain:** `{"freeze": [a, b], "at": src_t}` = your voice `[a,b]` plays over one frozen frame.
   Use it when the screen is busy or messy, or when you want to annotate a still piece by piece.
8. Verify: picture and sound durations equal (±1 frame); re-transcribe the edit and read it end to end.

## 3. Annotation rules (non-distracting by design)

**Principle: the screen is the hero.** Annotations point; they never perform.

- **Do not:** film grain or noise over the recording (`"grain": false`), constant camera motion, flashy
  transitions inside an explanation, more than one callout at a time, text over the thing you point at.
- **Zoom** only when UI text would be unreadable on a phone or when focus matters. Scale 1.15–1.9,
  0.6–1.0 s `power3.inOut`. Hold the zoom while you talk about that area; zoom out between areas.
- **Spotlight** (dim the rest + lime box) for the element being explained right now. `"dim": false` when
  the surrounding context matters.
- **Hand-drawn circle** for small targets (tabs, buttons, toggles) at the moment you name them.
- **Callout:** Arabic message ≤ ~22 characters at zoom + a small English caps tag. Place it away from the
  nearest frame edge. Real UI text only. Never invent numbers.
- **Click ripple** on real clicks; the "×4" badge on ramps.
- **Privacy blur** on account names, emails, credits, API keys, phone numbers, and anything personal, for the whole video.
- **Timing:** appear 0–0.2 s before the word; leave when the topic changes. One focus at a time.
- **Coordinates:** take them from **ruler frames at the exact moment** (UI layouts shift when panels open
  or close; dialogs close sooner than you think).

## 4. Cutaways (motion-graphics interludes)

Use them only where the screen adds nothing: a concept, a "why it matters", a map of what's coming, a recap.
Keep each 3–12 s with a new beat every 2–4 s. Enter and exit with the brand wipe. Reference: c0–c5 in
`projects/screenshare-v1/composition/compositions/`. Ideas: the section map, before/after (two systems →
one umbrella), "your AI team lives here", "routines = schedule", recap pills.

## 5. Learning aids (ready in the kit)

| Aid | How | When |
|---|---|---|
| **Chapters** | `chrome.json` sections with `"title"` → `python pipeline/chapters.py <name>` | every long video (YouTube: first at 00:00, ≥ 3 chapters, each ≥ 10 s) |
| **Step tracker** | `chrome.json "steps": [{"t0","t1","items":[{"t","label"}]}]` → `HF_STEPS` bar (RTL, done = green check, current = lime) | any how-to with ordered steps |
| **Freeze-and-explain** | `screen_edit.json {"freeze": [a,b], "at": t}` + spotlights on the still | busy screens, dense UI, messy moments |
| **End-of-section recap** | `scenes.json {"template": "recap", "data": {LABEL, TITLE, P1..P3}}` over a `hold` | end of each major section |
| **Quiz (voice paused)** | `screen_edit.json {"hold": 7, "at": t}` + `{"template": "quiz", "data": {Q, A, B, C, CORRECT, COUNT, LABEL}}` + tick/chime cues | after key concepts (≤ 1 per 2–3 min) |

## 6. Recording tips (give these to the presenter)

- A clean browser profile: no bookmarks bar, no banners, few tabs. 125 % zoom so text survives phones.
- Do Not Disturb on, so no OS dialogs or notifications. Close other apps.
- Prepare the example project **before** recording; don't search on camera.
- Pause 2 s between sections and after a mistake (clean cut points), then repeat the sentence.
- Move the mouse deliberately; park it when you talk.
- Say section names clearly ("القسم الأول…"). They become chapters and on-screen labels.

## 7. After delivery — always offer

1. **Reels / mobile version:** a 9:16 cut per section (auto-crop on the zoom targets + captions), 30–60 s each.
2. **Article pack for the website:** key summary + ordered screenshots
   (`deliverables/article/NN_section-slug.png`, captions, alt text) + an outline in Arabic.
3. **Ideas + recommendations:** what to add next time (learning aids, recording fixes, follow-up topics).
Also hand over the YouTube chapters (`deliverables/<part>_youtube_chapters.txt`).

## 8. Ideas backlog (explore in upcoming projects)

- Cursor spotlight that follows the mouse (needs cursor tracking from the recording).
- Keyword captions (2–4 words per sentence) and glossary pop-ups for the first use of a term.
- Before/after split screens (empty vs filled project, manual vs automated).
- Auto 9:16 reframe per section from the annotation zoom targets.
- Interactive chapter map card at each chapter start ("you are here").
