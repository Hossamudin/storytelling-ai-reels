# Format router — from "here are my files" to the right kind of video

Look at what the creator gives you, then recommend ONE mode (with a one-line why) and let them confirm. When two
modes fit, say so and offer both (one recording can become a faceless reel AND a talking-head hybrid).

## 1. Read the inputs (intake)

```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height -of compact <file>
```
For every file: audio only or video? camera or screen? duration? resolution/aspect? Is it complete ("moov atom
not found" = interrupted recording → ask for a re-export)? Several voice notes = one series? Then ask only what the
files can't tell you: format/platform, message, names to spell, sources, budget (see `NEW_VIDEO` brief below).

## 2. Route

| They give you… | Recommended mode | Playbook |
|---|---|---|
| Voice note only (or "no face") | **Faceless motion graphics** — 100% code-built, synced to the voice | `motion-director.md` + `style-presets.md` |
| Script only, no voice | Ask: record it (best) / local TTS / paid voice → then faceless motion | `voice-and-cuts.md` → motion |
| Camera video of the creator talking | **Talking-head hybrid** — face for opinions, graphics for what to inspect | `talking-head.md` |
| Screen recording of a tool / tutorial | **Screen tutorial** — cuts, zooms, spotlights, callouts, chapters, quizzes | `screenshare-playbook.md` |
| Camera + screen recordings | Hybrid: camera beats + screen clips as full-screen visuals | `talking-head.md` + `screenshare-playbook.md` |
| Topic / article / notes, no media | Script first (with them), then voice, then faceless motion | `storytelling.md` → motion |
| "A cartoon / character / whiteboard" | **2D animation** | `animation-2d.md` |
| "3D / clay / product spin / logo in 3D" | **3D** | `animation-3d.md` |
| Long video → reels | Cut per section (30–60 s), 9:16 reframe, captions, new hook per reel | `render-and-deliver.md` |
| Many short news items / a weekly recap | News reel: headline stack, real captures per story, fast rhythm | `storytelling.md` + motion |
| A logo / brand | Logo sting (2D draw-on or 3D extrude) for the library, reused in every video | 2D / 3D playbooks |

Faceless motion stays the default for voice-only input. If a camera file exists and the brief is ambiguous, ask (or
build both — they share the voice edit and assets).

## 3. The brief (give beginners this to fill, or ask it conversationally)

```text
FILES: <folder>  (voice · screen recordings · camera · images · QR codes)
FORMAT: <reel 9:16 | YouTube 16:9 | both> · STYLE: <faceless motion | talking head | screen tutorial | 2D | 3D>
MESSAGE (one sentence the viewer must remember): …
AUDIENCE: <who + what they know>
NAMES (exact spelling): <tools, people, brands>
SOURCES (official pages for real numbers): <urls>
LINKS / QR (what each opens, where it appears): …
FOOTAGE NOTES (best moments, things to hide): <file: use 0:40–1:05; hide my email at 0:12>
CTA: <follow | subscribe | comment keyword> · WATCH NEXT: <url | none>
PAID GENERATION: <none | ask me first | up to $X>
AVOID / MUST INCLUDE: …
```
Skippable: audience, sources (you'll find official pages), footage notes, watch next. Anything unclear (a name, a
price) gets flagged instead of guessed.

## 4. Universal production flow

```
intake → studio check → voice clean + transcript → cuts (review page) → [concepts → APPROVAL]
→ scaffold part(s) → build scenes (library first, generate only with approval) → check + snapshots
→ preview → APPROVAL → render_final → deliver + explain + suggestions + feedback → harvest library
```
