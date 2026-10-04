# Roadmap: review findings + plan (Oct 2026)

Status: **PLAN**, apart from the bug fixes in `LESSONS_LEARNED.md` §11 and the first cartoon kit (§C, built Oct 2026).

## Decisions (Hossam, Oct 2026)
- **OCR for redaction:** hybrid. Local **PaddleOCR (PP-OCRv5, Arabic + English)** finds every text box, because its
  detector is language-agnostic, so nothing is missed even when an Arabic word is misread. Regex rules and the
  always-hide list classify the boxes. **Gemini 2.5+** is the optional second pass on flagged frames only: it returns
  boxes and reads Arabic well, and it judges faces, avatars and chat sidebars. Paid key only, because free-tier data
  may be used for training. Not chosen: free online OCR (uploads unredacted secrets to a third party) and OpenAI
  vision (no reliable pixel boxes).
- **AI B-roll with Hossam's face: allowed, used smartly.** Library first (real clips, then earlier generations).
  Generate only for shots that can't be filmed cheaply. Never fake events, places, endorsements or quotes; keep
  them stylised over photoreal where the claim matters. Use the hi-res photos as references for consistency, flag
  every clip for the platform's synthetic-content label, and save each one to the library (`hossam-clip`,
  tag `ai-generated`) for reuse.
- **Visual style: fits the content.** Story → cartoon kit. Tool/news → editorial motion. Tutorial → screen-share.
  The treatment names the style and why.
- **B-roll repo:** Hossam supplies raw B-roll; the agent ingests it with `lib.py add` (type `hossam-clip` /
  `broll`, tags: action, emotion, place, framing, orientation) and `lib.py describe`. Each module below lists
the problem, the chosen method, the files it adds or changes, and how we know it works. Build order is at the end.

---

## A. Privacy redaction for screen recordings (note 1)

**Today:** `annotations.json {"type": "blur", "rect": …}` puts a CSS `backdrop-filter` box over the screen in the
composition. Problems with that:
- It is an overlay, not a redaction. The raw pixels are still in `edited.mp4`, in library copies, in article
  screenshots and in any reel cut from the same recording.
- The fallback is a 55 % tint. If `backdrop-filter` doesn't render (software GPU, a new Chrome), the text stays readable.
- Coordinates are typed by hand from ruler frames, the box is static (scrolling content escapes it), and missing a
  spot is easy (Lessons §6b and §9 list 4 real leaks: task names, search history, account name, podcast guests).

**Method: bake the redaction into the source pixels before anything else touches the recording.**

1. **Detect:** `pipeline/redact.py <name> --scan`
   - Sample frames only when the screen changes, using the existing `screen_edit.activity()` detector (about 10×
     fewer frames than a fixed fps), plus one frame per second as a floor.
   - Local OCR on each frame (EasyOCR or RapidOCR, ar + en, CPU, free). Regex classes: e-mail, phone, API keys
     (`sk-…`, `AIza…`, `ghp_…`, `Bearer …`, long hex/base64), card/IBAN, URLs with tokens, money balances.
   - A personal **always-hide list** in `config.json → privacy.always_hide` (your name variants, e-mails, workspace
     and client names, guest names) plus a per-video list from the brief (`FOOTAGE NOTES: hide …`).
   - Optional second pass with the vision model `lib.py describe` already uses: "list anything personal on this
     frame", for faces, avatars and sidebars of chat history or tasks that OCR rules miss.
   - Track boxes across frames (IoU merge) into time ranges. Output: `input/redactions.proposed.json`.
2. **Review:** `review/redact.html` (same pattern as `cuts.html`). It shows a contact sheet with every hit boxed and
   tagged by reason. You tick or untick hits, draw extra boxes and export `input/redactions.json`
   (`"approved": true`).
3. **Apply:** `redact.py --apply` builds an ffmpeg graph: for each box, `crop → gblur=40 + pixelize` (or a solid fill
   for keys and passwords) `→ overlay=enable='between(t,a,b)'`, with linear keyframes for moving boxes. The output
   `input/screen_redacted.mp4` becomes `screen_edit.json "source"`. It is source time and source pixels, so the
   rest of the pipeline is unchanged.
4. **Gate:** `preflight.py` fails a screen project whose edit source isn't the approved redacted file, and
   `lib.py add/harvest` refuses an unredacted screen recording (`privacy: raw` tag).
5. Keep the CSS `blur` for timed, cosmetic hiding only, and make its fallback opaque.
6. Optional: bleep or duck spoken sensitive data (phone numbers read aloud), found in the verbatim transcript.

**Done when:** a synthetic test recording with a fake e-mail, API key and name list is fully caught by `--scan`, and
the applied file has no readable hit when the scan is run again (added to `selftest.py`).

---

## B. Reviewer handoff pack after every render (note 2)

**Today:** "flag it in the handoff" is in many lessons, but it lives in the agent's memory, so items get lost.

**Method: steps write flags as they work, and one script assembles them.**

- `review/flags.jsonl`: one line per item `{t, t_basis: src|out, kind, msg, source, severity}`. Writers:
  `find_retakes.py` (low-confidence cuts), `voice_edit.py` (seams), `redact.py` (each redaction + rejected hits),
  `web_capture.py` (source URLs), `lib.py use` (asset provenance and licence), `generate_assets.py` / Higgsfield
  logging (AI-generated shots), plus the agent through `python pipeline/flag.py <name> --t 12.3 --kind claim "…"`
  for narrated numbers, invented strings and name spellings.
- `pipeline/handoff.py <name> [--part]` becomes step 6 of `render_final.py`. It maps every flag to output time
  through `edit_map.json` / the voice keep ranges and writes:
  - `deliverables/REVIEW.md` + `review/handoff.html` (a player where each timestamp seeks the video)
  - **Description draft:** hook line, chapters (from `chapters.py`), a **Links** section (brief LINKS/QR, decoded QR
    URLs from the library, captured source URLs, tools named in the video) and hashtags.
  - **Check before publishing, with timestamps:** sensitive moments (redactions, OCR hits you rejected, unreviewed
    screen spans), claims and numbers shown on screen with their source, invented on-screen text, name spellings,
    cut seams to listen to, QR codes (decoded URL + when shown), and AI-generated realistic people or scenes
    (→ YouTube "altered or synthetic content" toggle).
  - **Facts:** duration, loudness, resolution, file size, total spend (ledger), assets reused vs generated.
  - **Thumbnail candidates:** 3 frames chosen by sharpness and face/headline presence.
- The brief from `prompts/NEW_VIDEO_TEMPLATE.md` is saved as `input/brief.json` at intake. Links, names, CTA and
  hide-lists then come from data, not memory.

**Done when:** `render_final.py` on `screenshare-v1` produces a REVIEW.md where every timestamp lands on the right moment.

---

## C. 2D cartoon / After Effects-style explainer module (note 3)

**Built (v1, Oct 2026):** `kit/cartoon/` (rig + props, see its README) and `new_motion_video.py --kit cartoon`.
Demo: `projects/vibe-coder-hacked/`. `demo_flat` is the full 75 s story; `style_line` and `style_noir` are style
alternatives of the hook. Still to do: Hossam avatar, visemes, Lottie, scene templates.

Options weighed:

| Option | Quality | Cost | Control / determinism | Verdict |
|---|---|---|---|---|
| **SVG character rigs + GSAP (code)** | good → very good with a solid rig | free | full; brand palette; crisp Arabic text | **Foundation** |
| Lottie (AE exports via lottie-web, seek by frame) | very good | free / marketplace licences | good (recolour JSON to the palette) | **Add for props and characters we don't draw** |
| AI image → video (Higgsfield) | high, but inconsistent | paid | low (no text, character drift) | **1–2 hero shots per video at most** |
| Rive | very good | free | state machines are hard to seek frame by frame | Skip |

**Build: `kit/cartoon/`**
- `rig.js`, `window.HF_RIG(fx, svg, opts)`: a character made of SVG part groups with pivots at the joints. API:
  `pose(t, "point"|"think"|"shrug"|"celebrate"|"idle", dur)`, `walk(t0, t1, from, to)`, `look(t, target)`,
  `talk(t0, t1)`, auto-blink and breathing. All moves go through the same seek-safe `fromTo` rules the kit already
  follows.
- AE vocabulary as helpers: squash and stretch, anticipation, overshoot, follow-through, trim paths (DrawSVG),
  shape morph (MorphSVG; GSAP plugins are free now, vendor them next to `gsap.min.js`), camera push and pan with
  parallax layers, circle and shape wipes, and the existing `motion-blur.js`.
- `pipeline/visemes.py`: voice wav + word timings → mouth shape per frame (energy envelope, gated by word spans).
  No paid API, approximate lip-sync that is good enough for 2D.
- Library: characters (a **flat-vector Hossam avatar**, a "viewer" character, an AI/robot character), props
  (laptop, phone, coin, bulb, server, doc, chat bubble, money), backgrounds (desk, office, street, abstract), all
  in the brand palette. Store them in `library/` as type `code` so they're reused.
- `prompts/cartoon_director.md`: story beat → shot list (establishing / medium / close-up / reaction / insert),
  staging and silhouette rules, Arabic speech-bubble rules, and archetypes: **story** (goal → obstacle → turn →
  lesson), **concept-as-world** metaphor, before/after, a day in the life.
- `motion_sync.py` templates: `"template": "cartoon-scene"` with a characters + beats data block.

**Avatar consistency:** make the Hossam avatar once. Use a GPT Image flat-vector reference from your real photos,
then build or vectorise it to SVG (vtracer), split it into parts and save it as the master asset. Everything else
reuses it.

**Prototype first:** a 25–30 s 9:16 story reel (1 character, 3 poses, 2 backgrounds) to validate the look and
the rig workflow before building the full library.

---

## D. B-roll of Hossam (note 4)

**Sources, in order of preference**
1. **Your evergreen B-roll bank (best value).** One shoot of 30–50 short silent shots: typing close-up, pointing at
   a screen, walking in, writing on a whiteboard, thinking at the desk, scrolling a phone, nodding, coffee + laptop,
   reacting surprised or happy, hands on a keyboard and mouse. Shoot 4K 16:9 with the action centred so 9:16 crops
   work, 6–8 s each, 2–3 variants. Save in `library/` as `hossam-clip` (the type already exists) with tags for
   action, emotion, place and framing.
2. **Per-video shot list.** At treatment time the agent writes `deliverables/broll_shotlist.md`: 3–6 specific shots
   for this script, to film in 10 minutes with your phone.
3. **Stock B-roll (non-Hossam).** Pexels / Pixabay free APIs for generic scenes, with a halal-compliance filter.
   Licence and source go into the library record.
4. **AI B-roll of you (Higgsfield image → video from your photos).** Only for stylised or obvious shots, behind the
   approval gate, flagged for the synthetic-content label (likeness and trust risk).

**Pipeline: `pipeline/broll.py <name>`**
- **Plan:** find "boredom windows" (the same visual for more than 6 s in a reel or 10 s in long-form, screen
  activity ≈ 0, long holds, talking-head jump-cut seams from `th_seams.json`) and concrete verbs and nouns in the
  narration. Write `input/broll_plan.json [{t0, t1, query, kind, why}]`.
- **Match:** `lib.py find` over `hossam-clip` + `broll` (tags + vision descriptions) → stock search → propose AI (paid).
- **Place:** as cutaways in `scenes.json`, full-screen, picture-in-picture or split with the screen. Crop to the
  aspect, conform the speed, light colour match, muted. Rules: 2–5 s each, never over a moment where the screen
  is teaching, and B-roll on every talking-head seam (this also hides jump cuts).

---

## E. Speed-ups and structural improvements

| # | Change | Why / gain |
|---|---|---|
| E1 | **Scene component library**: move `build_lib.py` (copied verbatim into 3 projects) and the repeated builders from the per-project `build_scenes.py` files (500–1,000 lines each) into `kit/motion/py/` (title, stat counter, pill list, chart, quote, logo reveal, CTA with cutout, QR card, source-capture card, recap) | Biggest time saver: the target is about 200 lines per video, and fixes land once instead of per project |
| E2 | **One assembly path**: port the storyboard flow (`assemble.py`, single-file scaffold with 34 lint warnings, so it can never pass `preflight.py`) onto `new_motion_video.py` + `motion_sync.py` sub-compositions | Every flow gets the same preflight, `render_final`, chapters and handoff |
| E3 | **Auto snapshots**: `pipeline/snapshots.py <name>` takes each scene's busiest moment (after the last entrance) → `npx hyperframes snapshot` → `review/snapshots.jpg` contact sheet | Lessons: snapshots caught 7 issues `check` missed; today this is manual |
| E4 | **Parallel generation**: `generate_assets.py` runs images in a small thread pool and submits all video operations first, then polls | Wall clock goes from the sum of the jobs to the slowest job |
| E5 | **Preflight additions**: non-vendored `font-family`, SFX density (≤ 0.6/s), redaction approved, attribute-order-tolerant host regex | Moves recurring lessons into automatic gates |
| E6 | **Brief intake**: `input/brief.json` from the template (names → caption `fix`, links → handoff, hide → redact) | One source of truth per video |
| E7 | **Selftest coverage**: add the motion flow (scaffold → sync → check) and the redaction test; today only the old storyboard flow is tested | Catches regressions in the house-style path |
| E8 | **Dashboard**: tabs for Cuts review, Redaction review, Handoff; run buttons for the safe (free) steps | Fewer terminal round-trips for you |

---

## Build order (proposal)

1. **A (redaction)**: privacy risk is live today; includes the selftest case. *about 1–2 sessions*
2. **B (handoff)** + E6 brief intake: small, and every later module writes flags into it. *1 session*
3. **E1 + E3** (component library + auto snapshots): speeds up everything after it. *1–2 sessions*
4. **D (B-roll)**: plan / match / place, plus your B-roll bank shoot (you), in parallel. *1 session + shoot*
5. **C (cartoon)**: prototype reel first, then the library. *2–3 sessions*
6. E2, E4, E5, E7, E8 as follow-ups.

Decisions needed from you: OCR engine (EasyOCR vs RapidOCR; both free and local), whether AI B-roll of your
likeness is allowed at all, and the avatar style for the cartoon module (flat geometric vs. rounded "Kurzgesagt"-like).
