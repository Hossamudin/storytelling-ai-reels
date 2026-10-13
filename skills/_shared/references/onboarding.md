# Onboarding — the first conversation (and the 30-second check on every later one)

Goal: in one friendly conversation, leave the creator with (1) a machine that can make videos, (2) a studio
folder with their brand and preferences, (3) their existing assets catalogued, (4) the tools they want
connected — and (5) a first small win, so they see results before investing more time.

All five video skills share ONE studio (`~/VideoStudio` by default, remembered in `~/.video-studio.json`).
If another skill already ran onboarding, don't repeat it — read `profile.md` and go.

---

## Step 0 — every session (30 seconds, silent unless something is wrong)

```bash
python <skill>/scripts/setup_studio.py status
```
- **"NO STUDIO YET"** → run the full onboarding below.
- Studio exists → read `<studio>/profile.md` (language, level, preferences, feedback log) and
  `<studio>/lessons.md`. Talk in the profile's chat language. If the engine is older than the skill's, run
  `setup_studio.py init` (it upgrades the engine; projects are untouched) and say so in one line.
- `profile.md` still has `<fill>` fields → ask only for the ones this task needs.

## Step 1 — language first

Detect the language of the user's first message and answer in it (dialect too: Egyptian, Gulf, Levantine,
Moroccan, French, Spanish…). Ask once, briefly, if it's ambiguous: "Shall we talk in English or العربية?"
Then separate three things, because they often differ:
- **chat language** (how you talk to them),
- **spoken language** of their videos (drives transcription + captions),
- **on-screen text language** (e.g. Arabic with English tech words kept in Latin script).

## Step 2 — the machine

```bash
python <skill>/scripts/env_check.py
```
Translate the result into plain words. Don't paste the raw report to a beginner. Example:

> Your laptop is strong enough: 16 GB memory, a graphics card, 120 GB free. Two things are missing:
> **ffmpeg** (it cuts and joins video) and **Node.js** (it runs the video renderer). Shall I install them?
> It's one command each and takes about 3 minutes.

Rules:
- Install only with permission, one tool at a time, and confirm it worked (re-run `env_check.py`).
- Windows: `winget …` · macOS: `brew …` (install Homebrew first if missing; explain it) · Linux: `apt …`.
- If a command fails, read the error and fix the cause (PATH not refreshed → open a new terminal;
  Python "externally managed" → use a venv; winget missing → Microsoft Store "App Installer").
- **Weak machine?** Adapt, don't refuse: shorter parts, render overnight, `--quality draft` previews,
  local transcription with the `base` model, background removal started early. Note it in the profile.
- Write a one-line machine summary into `profile.md` ("Windows 11 · 8 cores · 16 GB · RTX 3060 · ffmpeg ✓ node ✓").

## Step 3 — create the studio

```bash
python <skill>/scripts/setup_studio.py init --language <ar|en|fr|…> [--home "<folder they choose>"]
```
Tell them where it lives and what's inside, in one sentence each:
`projects/` (one folder per video) · `library/` (reusable assets) · `brand/` (colors, fonts, logo) ·
`inbox/` (drop raw files here) · `profile.md` (what I remember about you).

## Step 4 — the creator & their brand (short interview)

One TOPIC per message (who · look · boundaries), at most 3 short questions inside it, each with a default they can
accept with "ok". Beginners get multiple-choice and can answer "ok to all"; pros get open questions. Never ask what you can infer (a logo file
tells you colors; a past video tells you pace and format).

Round 1 — who & what:
1. Your name / channel / brand? What topics?
2. Who watches (and what do they already know)?
3. Where do you publish? (→ default aspect: TikTok/Reels/Shorts = 9:16, YouTube = 16:9)

Round 2 — look & feel (offer to read their logo or a screenshot of their channel to propose a palette):
4. Brand colors? (no brand yet → propose 2–3 palettes as swatches, they pick)
5. Fonts? (none → propose a pair that supports their script: Arabic → Noto Kufi Arabic / Cairo + Manrope /
   Montserrat (bundled); Latin → Inter / Manrope; download .ttf into `brand/fonts/` — never load fonts online)
6. Light, dark, or both? Calm teacher, punchy creator, or cinematic?

Round 3 — boundaries:
7. Music? SFX? Captions? Anything to always avoid (colors, imagery, topics, faces, religious rules)?
8. Budget for paid AI generation per video: $0 (code only) · ask me first · up to $X.
9. Do you want 2–3 concepts before I build, or should I build straight to a preview?

Then write `brand/brand.json` (see `brand-profile.md`), run `python <skill>/scripts/setup_studio.py brand`,
and fill `profile.md`. Show them a 3-line summary and ask "anything wrong?".

## Step 5 — library building (if they already have material)

Ask: "Do you have a folder of things you reuse — logo, photos of you, past videos, screen recordings,
sound effects, thumbnails?" If yes:
```bash
cd <studio> && python engine/pipeline/lib.py import "<their folder>"
python engine/pipeline/lib.py describe      # optional, needs OPENAI_API_KEY: AI names + tags each image
```
Photos of the creator → type `person-photo` (they'll appear on camera in hybrids and end cards).
Mention privacy: recordings with emails, tabs, or names get tagged so future builds crop them.
Details: `library.md`.

## Step 6 — connect tools (only what this person needs)

Walk through `tools-connection.md` at their level. Order of value:
1. Nothing at all → still works: free local transcription, code-built motion graphics, local TTS.
2. `OPENAI_API_KEY` → best transcription + automatic retake finder (≈ $0.01–0.05 per video).
3. An AI generation MCP (e.g. Higgsfield) → images, SFX, short clips, 3D — paid, always behind approval.
Keys go in `<studio>/config/api_keys.json` — ask them to paste it there themselves. Never echo a key.

## Step 7 — first win (5 minutes)

Offer a tiny real result before the big project: a 10-second branded title card, their logo sting, or a
15-second clip from a voice note. It proves the setup and teaches the review loop
(preview → feedback → change). Then: "Ready for the real video? Send me the files."

## What to remember (write to `profile.md`)

Language(s) · level · machine line · keys present (✓/✗ only) · MCPs · budget · style defaults · avoid list ·
approval style. After every delivery, append to the **Feedback log**: date · video · what they liked ·
what to change next time. Read it before every new video — this is how the skill "learns" them.
