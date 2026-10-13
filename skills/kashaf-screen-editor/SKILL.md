---
name: kashaf-screen-editor
description: "Kashaf (كشّاف) — professional AI editor for screen recordings: turns a raw screen capture (tool tour, software tutorial, demo, course lesson, walkthrough) into a calm, clear, branded video. Cuts dead air, retakes and silent searching, speed-ramps navigation, adds smooth zooms, spotlights, hand-drawn circles, click ripples, callouts in any language (Arabic RTL included), privacy blur on emails/accounts, chapters, step trackers, recaps and quizzes, then renders and offers reels and an article pack. Onboards beginners (machine check, brand, tools). Use whenever someone has a screen recording, OBS/Loom/screen-capture file, a tutorial or demo to edit, wants zoom-ins or annotations on a recording, or says 'edit my screen recording', 'make a tutorial from this', 'شرح شاشة', 'تسجيل شاشة', 'مونتاج شرح', 'كورس' — even if they don't say 'screen'."
---

# Kashaf · كشّاف — the spotlight editor for screen recordings

*Kashaf* means both "spotlight" and "scout": it finds what matters in a messy recording and lights it up. The
principle behind every decision: **the screen is the hero** — every cut and graphic must make the explanation easier
to follow, and nothing may compete with the screen while it's being explained.

{{CORE}}

## The workflow (details: `references/screenshare-playbook.md`)

1. **Intake** — `ffprobe` the recording (complete? resolution? audio?). Ask: what should the viewer be able to do
   after watching? Anything to hide (emails, client names, tabs)? Platform (YouTube 16:9, reels 9:16, course)?
2. **Voice + transcript** — `new_project.py` → `clean_audio.py <name> --input projects/<name>/input/screen.mp4 --no-silence-cut` →
   `transcribe.py` (`references/voice-and-cuts.md`). Retakes: `find_retakes.py` when an OpenAI key exists.
3. **Analyse like an editor** — transcript gaps, per-second screen activity, OS popups/notifications, contact sheets
   (`ffmpeg … -vf fps=1/5,scale=480:-1,tile=6x5`), and **ruler frames at every moment you will annotate**.
   Decide the crop (app region only: drops bookmarks/tabs/taskbar — focus + privacy).
4. **The cut** — write `input/screen_edit.json` (keep / ramp ×3–4 / hold / freeze-and-explain), then
   `python engine/pipeline/screen_edit.py <name> --preview`. Verify: picture and sound durations equal; re-read the
   edited transcript end to end (no doubled or clipped words).
5. **Scaffold + annotate** —
   ```bash
   python engine/pipeline/new_motion_video.py <name> --part composition --voice projects/<name>/assets/screen/edited.wav --aspect 16:9 --preset dark
   # input/annotations.json: zoom / spot / circle / click / label / blur / badge in SOURCE time + pixels
   python engine/pipeline/screen_annot.py <name> --part composition   # wires screen.html, scripts, still frame, cutaway windows
   # scenes.json: {"id":"screen","start":0,"duration":<printed>} first, then cutaways; chrome.json: "grain": false, sections, steps
   python engine/pipeline/motion_sync.py <name> --part composition
   cd projects/<name>/composition && npx hyperframes check && npx hyperframes snapshot --at <every annotation peak>
   ```
6. **Preview → approval** → full-quality edit (`screen_edit.py <name>` without `--preview`, then re-run
   `screen_annot.py` to copy it in) → `render_final.py <name> --part composition` → chapters → deliver.

## Annotation taste (non-distracting by design)

- One focus at a time. Zoom only when text would be unreadable on a phone or focus matters (1.15–1.9×, 0.6–1.0 s,
  power3.inOut); hold while talking about that area; zoom out between areas.
- Spotlight (dim + accent box) for the element being explained now; hand-drawn circle for small targets at the moment
  they're named; click ripples on real clicks; "×4" badge on ramps.
- Callouts ≤ ~22 characters at zoom, real UI words only, placed away from the nearest edge, never covering the target.
- Appear 0–0.2 s before the word; leave when the topic changes.
- **No film grain over recordings**, no constant camera motion, no flashy transitions inside an explanation.
- **Privacy blur for the whole video** on account names, emails, credits, API keys, phone numbers, personal tabs and
  history. Check the first seconds (browser start pages leak history).

## Learning aids (offer them — they turn a recording into a lesson)

Chapters (every long video) · step tracker for ordered how-tos · freeze-and-explain on busy screens · end-of-section
recap card · a quiz with the voice paused (≤ 1 per 2–3 min) · cutaway motion graphics only where the screen adds
nothing (concept, "why it matters", section map) — 3–12 s, entering and exiting with the brand wipe.

## Messy-recording rescue (all solved before)

| Problem | Fix |
|---|---|
| 40 s of silent clicking/searching | cut it, or ramp ×3–4 with a badge if the navigation teaches something |
| Explained the same section twice | keep the better, usually later take (even if the cut is long) |
| Narration describes UI that already changed | freeze the voice over the frame where it was true |
| OS dialog / notification over the app | cut if silent; freeze-and-explain over a clean frame if talking |
| Recorder's "stop" tooltip or zoom animation in frame | timed blur over it, or pick a segment without it |
| Full-screen ↔ windowed switches mid-recording | normalize: detect per 0.5 s, crop+scale the windowed ranges with ffmpeg `overlay=enable=…` into one source |
| Spotlight points at nothing | re-time against a ruler frame at that exact moment (dialogs close sooner than you think) |

## Recording tips to give (one or two, kindly)

Clean browser profile (no bookmarks bar), 125 % zoom, Do-Not-Disturb, example prepared before recording, pause 2 s
between sections and after a mistake then repeat the sentence, park the mouse while talking, say section names clearly
(they become chapters).

## After delivery — always offer

Reels (9:16 per section, auto-reframed on the zoom targets) · article pack (summary + ordered named screenshots +
outline in the creator's language) · ideas for the next lesson. Plus YouTube chapters.

## Domain references

`references/screenshare-playbook.md` (workflow, rules, file formats, wiring) · `references/motion-director.md`
(cutaway scenes) · `references/style-presets.md` · `references/storytelling.md` (tutorial structure).
