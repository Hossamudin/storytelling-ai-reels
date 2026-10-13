# Screen-share playbook — tutorials, tool tours, walkthroughs

Goal: **help the viewer understand.** Every edit and every graphic must make the explanation easier to
follow. Nothing may compete with the screen while you're explaining it. Proven on a SaaS UI tour
(5:10 raw → 2:50 edited) and several tool tutorials.

---

## 1. Workflow

```bash
python engine/pipeline/new_project.py <name>                                  # recording -> input/screen.mp4
python engine/pipeline/clean_audio.py <name> --input projects/<name>/input/screen.mp4 --no-silence-cut
python engine/pipeline/transcribe.py <name>                                   # OpenAI word timestamps
# ANALYSE (agent): transcript gaps, per-second screen activity, brightness popups, contact sheets,
#                  ruler frames at every moment you will annotate (see §3)
# write input/screen_edit.json  (keep / ramp / hold / freeze timeline)
python engine/pipeline/screen_edit.py <name> --preview                        # edited.mp4 + edit_map.json + words.json
# verify: A/V durations match; re-transcribe edited.wav (no doubled/clipped words)
python engine/pipeline/new_motion_video.py <name> --part composition --voice projects/<name>/assets/screen/edited.wav --aspect 16:9 --preset dark
# write input/annotations.json (SOURCE time + SOURCE pixels) -> output-time data + cutaway windows
python engine/pipeline/screen_annot.py <name>
# scenes.json (screen + cutaways + quiz/recap templates), chrome.json (sections, wipes, steps, "grain": false), cues.json
python engine/pipeline/motion_sync.py <name> --part composition
cd projects/<name>/composition && npx hyperframes check && npx hyperframes snapshot --at ... && npx hyperframes preview --background
# APPROVAL -> python engine/pipeline/screen_edit.py <name>   (full quality, no --preview) -> copy edited.mp4 + edited.wav into the part
python engine/pipeline/render_final.py <name>                                 # preflight -> render -> verify -> master -> chapters -> deliverables/
```

The scaffold copies `screen.js` + `base.css` into the part's `assets/`. Composition files:
`compositions/screen.html` (window + camera + annotation layer — created for you by `screen_annot.py`, see §9) + cutaway scenes.

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
7. **Freeze-and-explain:** (pick the frozen frame BEFORE the UI changes — a freeze placed after a keep that ran past
   a dialog closing shows the wrong state; split keep → freeze → keep at the moment that matters)
    `{"freeze": [a, b], "at": src_t}` = your voice `[a,b]` plays over one frozen frame.
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
- **Callout:** main-language message (`"ar"` field — any language) ≤ ~22 characters at zoom + a small English caps tag. Place it away from the
  nearest frame edge. Real UI text only. Never invent numbers.
- **Click ripple** on real clicks; the "×4" badge on ramps.
- **Privacy blur** (opaque from its first frame — the kit never fades blurs in) on account names, emails, credits, API keys, phone numbers, and anything personal, for the whole video.
- **Timing:** appear 0–0.2 s before the word; leave when the topic changes. One focus at a time.
- **Coordinates:** take them from **ruler frames at the exact moment** (UI layouts shift when panels open
  or close; dialogs close sooner than you think).

## 4. Cutaways (motion-graphics interludes)

Use them only where the screen adds nothing: a concept, a "why it matters", a map of what's coming, a recap.
Keep each 3–12 s with a new beat every 2–4 s. Enter and exit with the brand wipe. Ideas: the section map, before/after (two systems →
one umbrella), "your AI team lives here", "routines = schedule", recap pills.

## 5. Learning aids (ready in the kit)

| Aid | How | When |
|---|---|---|
| **Chapters** | `chrome.json` sections with `"title"` → `python engine/pipeline/chapters.py <name>` | every long video (YouTube: first at 00:00, ≥ 3 chapters, each ≥ 10 s) |
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
- Say section names clearly ("Section one…" / "القسم الأول…"). They become chapters and on-screen labels.

## 7. After delivery — always offer

1. **Reels / mobile version:** a 9:16 cut per section (auto-crop on the zoom targets + captions), 30–60 s each.
2. **Article pack for the website:** key summary + ordered screenshots
   (`deliverables/article/NN_section-slug.png`, captions, alt text) + an outline in the creator's language.
3. **Ideas + recommendations:** what to add next time (learning aids, recording fixes, follow-up topics).
Also hand over the YouTube chapters (`deliverables/<part>_youtube_chapters.txt`).

## 8. Ideas backlog (explore in upcoming projects)

- Cursor spotlight that follows the mouse (needs cursor tracking from the recording).
- Keyword captions (2–4 words per sentence) and glossary pop-ups for the first use of a term.
- Before/after split screens (empty vs filled project, manual vs automated).
- Auto 9:16 reframe per section from the annotation zoom targets.
- Interactive chapter map card at each chapter start ("you are here").

## 9. File formats (what you write) and wiring (what the engine does)

**`input/screen_edit.json`** — the cut, in SOURCE seconds, in order:
```json
{
  "source": "input/screen.mp4",
  "crop": [0, 178, 1918, 852],
  "timeline": [
    {"keep": [7.30, 17.14], "label": "signup"},
    {"ramp": [104.0, 112.9], "speed": 4},
    {"hold": 1.5, "at": 18.5},
    {"freeze": [130.0, 141.5], "at": 131.2},
    {"keep": [112.98, 160.62]}
  ],
  "max_pause": 0.9, "keep_pause": 0.4, "busy_pause_keep": 1.2,
  "jl": {"l_max": 0.5, "j": 0.2, "busy": 0.6}
}
```
`crop` = the app region [x, y, w, h] (drop browser chrome, bookmarks, taskbar — privacy and focus); `null` = full frame.
`hold` = silent extra time on a frame (cutaway, quiz, title) · `ramp` = silent sped-up navigation · `freeze` = voice over
one frozen frame. Output: `assets/screen/edited.mp4/.wav`, `edit_map.json`, `words.json` (output-time words).

**`input/annotations.json`** — SOURCE seconds and SOURCE pixels (inside the crop); the engine maps them:
```json
{
  "window": {"x": 64, "y": 140, "k": 0.9343},
  "items": [
    {"type": "blur",  "rect": [8, 728, 264, 72]},
    {"type": "zoom",  "src": 47.0, "d": 0.8, "rect": [750, 272, 422, 310], "s": 1.8},
    {"type": "spot",  "src": [49.4, 55.6], "rect": [820, 352, 326, 38], "ar": "Project name", "en": "NAME", "pos": "bottom", "circle": false, "dim": true},
    {"type": "circle", "src": [21.6, 25.6], "rect": [844, 320, 236, 234]},
    {"type": "click", "src": 70.9, "x": 1109, "y": 540},
    {"type": "label", "src": [60, 63], "x": 400, "y": 200, "ar": "…", "en": "…"},
    {"type": "badge", "out": [53.13, 55.37], "text": "×4"},
    {"type": "zoom",  "src": 58.0, "d": 0.6, "s": 1}
  ],
  "cutaways": [{"id": "c1", "src": [75.28, null], "until_out": 53.13, "label": "5 sections"}]
}
```
- `window`: where the cropped recording sits in the frame. 16:9 with chrome: x 64, y 140, k = 1792 / crop width.
  9:16 reels: add `"fw": 1080, "fh": 1920` (viewport size) and pick x/y/k so the recording fills the width.
- `"ar"` is the main-language text field (any language); `"en"` the small caps tag. Zoom `s: 1` without rect = full view.
- Use `"out"` instead of `"src"` for times already on the output timeline (e.g. badges on ramps).
- `python engine/pipeline/screen_annot.py <name> --times 47.0 49.4` prints output times while you author.

**What `screen_annot.py` wires for you:** `annot.js` (output-time data), `cutaways.json` (output windows → copy into
`scenes.json` after the `screen` entry), links `screen.js` + `annot.js` in `index.html`, copies the edit into the part,
grabs a still (shown under the video so the frame never goes black) and creates `compositions/screen.html` from the
kit template. You then add `{"id": "screen", "start": 0, "duration": <printed>}` as the FIRST `scenes.json` entry,
set `chrome.json "grain": false`, and run `motion_sync.py`.

**Finding coordinates:** extract ruler frames at the exact moments you annotate
(`ffmpeg -ss <t> -i input/screen.mp4 -vf "crop=…,drawgrid=w=100:h=100:t=1:c=red@0.5" -frames:v 1 ruler_<t>.png`),
read pixel positions from them, and re-check each moment — dialogs close sooner than you think.
