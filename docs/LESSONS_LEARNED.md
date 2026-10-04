# Lessons learned — issues, fixes, and how to avoid them

Running log from real production runs (Vibe Automation intro/outro, kit test, SureThing screen tour).
**Read before every build.** When you hit a new problem, add it here: symptom → cause → fix → prevention.

---

## 1. Audio & transcription

| Symptom | Cause | Fix / prevention |
|---|---|---|
| Gemini transcription returns 503 "high demand", 429 on Pro models, or truncated JSON | The Gemini key is **free tier** (quota metric `generate_content_free_tier_*`, Pro limit 0) | Use `transcription.provider: openai_whisper` (default). Gemini only with a paid key |
| Gemini word timestamps are uniform 0.50 s steps | The model guesses timings | Never use Gemini for timing. Use whisper-1 `verbose_json` + `timestamp_granularities[]=word` |
| Whisper drops the opening sentence | A `prompt` hint that matches the speech makes Whisper skip it | Never pass a hint prompt (the code doesn't) |
| Words appear twice ("وده وده") after the provider merge | Words on segment boundaries were assigned to two segments | Fixed in `transcribe.py` (each word belongs to one segment) + dedupe in `voice_edit.py` |
| A repeated take ("علشان كده ×2") shows up as one long word span | Whisper merges retakes | Map energy (`silencedetect` + 50 ms RMS strip), transcribe ≤ 1.5 s excerpts with `gpt-4o-transcribe`, then add `retime` entries for the kept take |
| Loud non-speech at the start transcribes as "Thank you" / Japanese | Hallucination on clicks / room noise | If two models disagree on a short span → treat it as non-speech, cut it, and flag it to the user |
| SFX drown the voice; some effects inaudible | The bundled library spans −4 … −36 LUFS | `python pipeline/sfx_levels.py` → per-file gains (`levels.json`); `motion_sync.py` applies them × accent |
| Final loudness inconsistent between videos | No master stage | `python pipeline/master_audio.py <mp4>` → −14 LUFS, −1.2 dBTP (two-pass loudnorm) |
| Verifying an edit with `transcribe.py --input edited.wav` returned the **original** transcript | `compact_for_api` cached `voice_for_api.m4a` regardless of the source file | Fixed: the upload copy is cached per source file (and rebuilt when the source is newer). Back up `transcript/` before a verify run, since it overwrites `transcript.json` |
| Cuts click/pop | Hard sample edges | 10–12 ms fades on every seam (`voice_edit.py` / `screen_edit.py` do this) |

## 2. Editing (voice & screen)

| Symptom | Cause | Fix / prevention |
|---|---|---|
| Edited video shorter than the plan (missing tail) | A hold read frames past the end of the source | Holds/freezes are rendered as looped stills (`screen_edit.py`) |
| A screen cut feels jumpy | Picture and voice cut at the same instant | Automatic J/L cuts: picture leads (L) when the screen changes in the gap, voice leads (J) otherwise |
| 40 s of silent clicking | Searching for an example on camera | Cut it, or speed-ramp ×3–4 with a "×4" badge only if the navigation itself teaches something |
| Explained the same section twice | Natural re-takes while recording | Keep the **better, usually later** take; cut the earlier pass even if it is long (34 s here) |
| OS dialogs / notifications pop over the app | Recording artefacts | Brightness/green detector on frames; cut if silent, or freeze-and-explain over a clean frame if you're talking |
| The narration describes UI state that changed seconds earlier ("it recommends skills" over an already-empty list) | The presenter kept clicking while talking | `freeze` the voice over the frame where the state was true (Mahara: list at src 40.3), then return to live for the next sentence |
| The screen recorder's own "Stop recording" tooltip sits in the frame | The cursor rested near the recorder bar | Timed `blur` item over the tooltip rect (or keep the zoom away from it) |
| A spotlight points at nothing | The UI changed (dialog closed, tab switched) inside the annotation window | Time every annotation against **ruler frames at that exact moment**; check dialog open/close times |

## 3. HyperFrames composition gotchas

| Symptom | Cause | Fix / prevention |
|---|---|---|
| **Blank video** | `<html dir="rtl">` | Put `direction: rtl` on `#root` / text containers only |
| `GSAP target not found` | A sub-composition's inner root merges into its host (`#s3-host`), so `#s3 .x` matches nothing | Select element ids/classes directly (`#s3-title`), never through the scene root id |
| `invalid_parent_traversal_in_asset_path` | `url("../fonts/…")` in an external CSS | `@font-face` lives in the root `<style>` with `assets/fonts/...` |
| Elements visible before their entrance | `.to()` on an element without a from-state | Hide with a `fromTo` at build (`fx.hide`) and give later re-tweens `immediateRender: false` |
| `gsap_css_transform_conflict` | CSS `transform` + GSAP transform on the same node | Center with GSAP `xPercent/yPercent` (see `screen.js` callouts) |
| Element jumps to the top of the frame | Missing `position: absolute` on a box placed with `top` | Every `#id { top: … }` block also says `position: absolute` (or uses `.abs/.row`) |
| Callout/label stacked text flagged as overlap | EN-caps over AR lines inside one bubble | Put `data-layout-allow-overlap` on the **flagged child elements themselves** (a parent attribute isn't enough) |
| Kufi/Cairo headlines flagged as overlapping | Very tall Arabic glyph boxes | Line-height 1.2–1.3, verify with a snapshot, then mark only verified cases |
| `subcomposition_blanks_before_host` | A full-frame scene ends before the root | The base scene (screen) and the closing scene run to the root's end |
| Overlapping SFX warnings | Several `<audio>` on one track | Each SFX gets its own `data-track-index` (`motion_sync.py` does it) |
| Patch scripts miss the root tag | Studio inserts `data-hf-id` and reorders attributes | Match tags with attribute-order-tolerant regexes (fixed in `motion_sync.py`, `chapters.py`) |
| Bash heredocs with Arabic/quotes break | Shell quoting + Windows | Write patch scripts to the scratchpad with the file tool and run them with Python (raw strings) |
| `check` says "Navigation timeout" once | Machine busy (previews running) | Re-run with `--timeout 30000` |

## 4. Design & typography

| Symptom | Cause | Fix / prevention |
|---|---|---|
| "الـAI" reads as "الا" | A short tatweel in Kufi; ZWJ doesn't join across the Latin span | Use a long tatweel `الـــ` + `<span class="lat">AI</span>` |
| Orange text unreadable on paper | #FF5A33 on #F6F4EA = 2.8:1 | Orange for shapes/bands; text on it white ≥ 90 px, or ink/teal text |
| Highlighter band becomes a big block | `.hl` around wrapped text | `.hl` is `nowrap`; keep highlighted phrases short |
| Counter shows a dot before it starts | The Arabic-Indic zero ٠ is a dot | `counter()` hides the number until it starts |
| Chrome series name collides with the section label in 9:16 | Narrow canvas | Chrome hides the series name at `max-aspect-ratio: 1/1` |
| Parked wipe-bar corners peek into frame | Skewed bars too close to the edge | Bars are invisible between sweeps and parked at −120 % |
| Template scenes clipped in 9:16 | Hard-coded 1920×1080 | Templates use `{{W}}/{{H}}` + responsive CSS (quiz stacks vertically) |
| Callouts run off the frame when zoomed | Long text near the frame edge at zoom ≥ 1.4 | Short callout text (≤ ~22 Arabic chars at zoom); choose `pos` away from the nearest edge |
| **Grain over a screen recording looks dirty/distracting** | The film-grain overlay sits on the UI text | Screen-share projects: `chrome.json "grain": false` (default for screen recordings) |

## 5. Process

- Always pitch 2–3 concepts before building (motion videos); always ask before paid generations (Higgsfield / GPT Image).
- Snapshot every scene at its **busiest** moment; `check` passing ≠ looking right (missing `position:absolute`, spotlights on closed dialogs, clipped callouts were only visible in snapshots).
- Keep durations in one place: re-run `motion_sync.py` after any timing change. It recomputes the root duration, chrome, wipes, steps and audio.
- Flag every invented string (placeholder comments, country lists, quiz answers) in the handoff.
- Studio preview reloads on file changes. Re-snapshot after each fix round.

## 6. Talking-head hybrid (camera + motion graphics) — Agent Harness, Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| User asked for "talking head" but got a faceless video | The prompt mixed two briefs; the faceless line came last | When a camera file exists, ask yourself which mode is meant, or build both: faceless (`reel/`) + hybrid (`reel_th/`) share the voice edit and assets |
| Camera and voice drift apart after the edit | Video and audio cut separately | `th_cut.py` applies `voice_edit.py`'s keep ranges to the camera, so there is one timeline |
| Jump cuts visible on the face | Seams from the voice edit | `<part>_th_seams.json`: place a full-screen interlude over each seam or a hard punch (`punch` dur 0) on it |
| Matte took ~45 min | `remove-background` runs on CPU (0.3–0.8 s/frame) | Start it right after `th_cut.py`, in the background |
| `gsap_relative_value_second_writer` error | A `scale: "+=…"` exit overlapped a punch-in | Absolute values only on `#thw` |
| Card ↔ circle transitions jump | `clip-path` can't interpolate `inset()` ↔ `circle()` | Full frame = `circle(1400px at 540px 760px)`; card opens to `inset(0 round 0)`, then a `set` swaps to the circle (`th_layer.py`) |
| "Text behind you" looks like normal text | Placed above the head, so the matte never covers it | Head line y≈380–480 at 9:16; ≤ 180 px for long words |
| Copying markup from another project failed | Studio adds `data-hf-id` attributes | Regexes tolerate extra attributes and strip `data-hf-id` from copies |
| Charts blank in screenshots | Lazy iframes/canvas in headless mode | `web_capture.py` scrolls, waits and screenshots each iframe |
| "1.04$" in an RTL pill | Bidi reorders the currency | Wrap numbers with currency in `<span class="lat">` |
| Headline hidden by a zooming chart | Header sat under the camera world | Put the header + verdict after the world in the DOM, with a backdrop |
| Higgsfield `unknown model` | Guessed ids | Working ids: `gpt_image_2_5` (+`quality: medium`), `seedance_2_0` (image→video, `role: start_image`), `mirelo_text_to_audio` |

## 6b. Reel series from several voice notes + screen clips — Opus 5.5 Tips, Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| A logo drawn from an `<svg><symbol viewBox="-50 -50 100 100">` sat half a size down-right of its glow | The outer `<svg>` also had a negative viewBox, so the `<use>` viewport started at its origin | Outer svg `viewBox="0 0 100 100"` + `<use width="100" height="100">`; only the symbol carries the centred viewBox |
| SVG axis labels clipped at the frame edge | `text-anchor="end"` flips under the inherited RTL direction | Put `style="direction:ltr"` on chart SVGs |
| Preflight fails on 2-sample overlaps at every scene boundary | Scene exits (0.3 s) ran past the next scene's start (0.2 s overlap) | Exit fades end before the next scene starts (`build_lib.make`: exit at end − 0.44 s, 0.22 s fade) |
| Whisper silently skipped a 3 s sentence in the middle | Not a silence (energy present) but no words | Compare segment gaps with `silencedetect`; transcribe the gap with gpt-4o-transcribe, add a `retime` entry |
| Hossam JPGs appear rotated | EXIF orientation | `ImageOps.exif_transpose` before `remove-background` (the 6000 px JPGs cut out far better than the 400 px PNG cutouts) |
| Desktop page captures look tiny in 9:16 | 1280 px layout | Capture real sources at a mobile viewport (430 px, dsf 2.5, reject cookies) and crop sections |
| Personal task names visible in a screen recording | Sidebar list in the Claude app | Bake a time-gated `boxblur` with ffmpeg before using the clip (split around open menus) |
| Several voice notes for one series | Separate files | Concatenate with 2 s gaps into one input → one transcript → `edit.json` parts; one shared `build_lib.py` |

## 7. Rendering & delivery — "best version on the first render"

| Symptom | Cause | Fix / prevention |
|---|---|---|
| **Render blocked: `sub_timeline_script_failure … cdn.jsdelivr.net/…/gsap.min.js`** | GSAP loaded from a CDN at render time; one transient network failure blocks the render (an earlier render of the same project had worked) | GSAP is vendored: `kit/motion/js/gsap.min.js` → `<script src="assets/js/gsap.min.js">` (kit template, `assemble.py`, all projects). **No remote URLs in compositions.** `preflight.py` fails on any |
| Final render looked soft | The composition still used the `screen_edit.py --preview` encode (crf 26, ultrafast) | `edit_map.json` records `"quality"`; `preflight.py` blocks a preview edit or a stale copy in the part |
| Rendered from Studio → no gates, no mastering | Studio's render button skips the pipeline | **Final renders only via `python pipeline/render_final.py <name> [--part …]`**: preflight → render `--quality delivery --strict` → verify duration + audio → master −14 LUFS/−1.2 dBTP → chapters → `deliverables/` |
| A long render got killed | The agent's background shell is capped at 10 min | Launch long renders detached (`Start-Process … -RedirectStandardOutput deliverables/render_final.log`) and poll the log |

**First-time-right checklist (run in this order):** snapshots of every scene at its busiest moment →
`npx hyperframes check` clean → user approves the Studio preview → full-quality edit (screen projects) →
`python pipeline/render_final.py <name>` → watch the mastered file's first and last 10 s → deliver
(`deliverables/`: video + chapters) → offer reels / article pack / ideas.

## 8. Transcript cuts + asset library — Sonnet 5.5 reel, Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| Retakes survived every past edit (2–4 cuts per video) | whisper-1 "cleans" speech: it drops repeats and merges two takes, so the agent never saw them in `transcript.json` | `find_retakes.py`: pause-split chunks transcribed verbatim with `gpt-transcribe` + LLM editor pass (gpt-5.5) → `edit.proposed.json` + `review/cuts.html`. Sonnet 5.5: found both hidden retakes + a false start on the first run |
| `gpt-transcribe` rejects word timings | `verbose_json` → HTTP 400 (json/text only) | Timings come from silence-split chunks (cuts land in pauses) and whisper-1 words; spelling comes from gpt-transcribe |
| Captions missing the kept take ("ويعتبر أحسن من…") | whisper had timed only the first (cut) take | `voice_edit.py --verify` re-transcribes the EDITED part (no retakes left) and re-times caption words on it |
| One verify pass misspells ("سوليتير أبعاد") | a single verbatim sample is noisy | Spelling reference = planned words + only the words the verify pass heard that the plan lacked |
| Names misheard by every model (SureThing AI, Pi, حسام الدين حسن) | proper nouns | `edit.json "fix"` accepts phrase entries `{"from": "هوصلك لحسن.", "to": "حسام الدين حسن."}` (optional `"at"`) |
| `clean_audio.py` processed a silent screen clip (−91 dB) | it took the first file in `input/` alphabetically | `find_input_audio` prefers `voice*/voiceover*/rawreel*`, then audio files; `screen*` never wins |
| A raw recording unusable ("moov atom not found") | the screen recording was interrupted before it finalized | Stop recordings cleanly; check new inputs with `ffprobe` at intake |
| Bars invisible though `check` passed | absolute child with only `bottom: 0` had no height | Snapshots at the busiest moment of every scene — they caught 7 issues `check` didn't |
| `nested_media_start_basis_ambiguous` blocks preflight | nonzero `data-start` on `<video>` inside a scene | Add `data-hf-media-start-basis="local"` (times are scene-local) |
| Same assets re-generated / copied per project | no shared store | `library/` + `pipeline/lib.py` (find → use → add/harvest, vision `describe`, contact sheets). The Sonnet reel reused 18 library assets and generated nothing |
| A narrated number has no source (1M context window) | not on the official page | Show it as the narrator's claim and flag it in the handoff, never as "REAL DATA" |

## 9. Second run of the new cut flow — "AI ببلاش" part 1, Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| Captions had 103 words for 162 s of speech; one word lasted 23 s; outro missing | long-file whisper-1 looped on the opening retakes ("صدق او لا" ×3) and skipped stretches | Word timings now come from whisper-1 on ≤ 10 s pause-bounded windows (`find_retakes.window_word_timings`) for both the raw and the edited voice → 391 words, verify similarity 0.974. Empty windows are printed, never silently dropped |
| Verify pass "kept" words the edit no longer contains ("ولكن تقدر") | spelling reference = planned words + inserts only | Reference: planned spelling where it matches what the edit says, heard words where the plan is missing/wrong, planned-only words dropped |
| A 7.6 s opening retake was labelled "noise" in the review page | merged proposal kept the first kind | Merge prefers retake/false_start over noise/filler |
| `web_capture.py` timed out on whacka.app | live sockets: the page never reaches `networkidle` | Falls back to `load` + 4 s settle |
| Screen-recording window went black mid-scene | the recording itself is blank while the site loads / the clip ran out | Put a still frame of the best moment under every `<video>` (the clip plays over it; the still holds after) |
| Personal Google search history in the first 5 s of a recording | recorded from the browser start page | Never use those frames; note the privacy trim in the library record (`privacy-trim-0-5s` tag) |
| Narration contradicts the live source (SureThing "$20 plan"; site says Basic $30, 1,000 free credits) | prices change / memory | Don't put the contested number on screen; flag it at handoff with the source |
| Unclear product name (WokeApp / Wokka App) | 3 models agree on the sound, not the brand | Web-search the sound + the narrated facts (credits, 14 days) → Whacka (whacka.app), then verify on its pricing page |
| Supplied QR PNGs looked fine but no decoder could read them | transparent background (all pixels black, only alpha varies) and no quiet zone; on the dark preset they'd be black-on-green | Flatten on white with a ≥ 4-module margin, verify by decoding (jsQR), show on a white card; library type `qr` records the decoded URL |
| Screen-recorder auto-zoom moved the crop target mid-clip | recorder zoom animation (whacka candy 109–110 s) | Scan the crop window at 1 fps before cutting; choose a segment without zoom |
| Real screenshares exposed private data (account name, podcast guests + statuses, bookmarks) | full-window recordings | Pre-cut clips with an ffmpeg crop to the content area (and speed via setpts) instead of placing the raw recording |
| Preflight failed: timecode "00:07" 1.48:1 contrast | a lime wipe bar sweeps behind the chrome timecode | Kit: `#chrome .tc` has a dark backing pill (base.css) |
| A clip ends before its scene | short source / sped-up clip | Still frame of the clip's last (or best) frame underneath every `<video>` |

## 10. Weekly news reel (7 stories, 32 scenes) — AI News 3 Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| `web_capture.py` saved a "Verify you are human" page for openai.com | Cloudflare challenge on headless Chromium | Headed Chrome (`channel="chrome"`, `headless=False`, mobile UA, 430 px × 3) loaded the pages without a challenge. Never solve a challenge; if headed fails too, ask the user for screenshots |
| Whisper transcript ended with "اشتركوا في القناة" over silence | classic Whisper hallucination on trailing silence | Compare the last segment with `silencedetect`; the verbatim chunks didn't contain it |
| 28 s gap in the middle with no words | long pause/noise while recording | `silencedetect` + one gpt-4o-transcribe pass on the gap ("."), then an explicit cut |
| Preflight failed on `composition_file_too_large` (311 lines) | 132 SFX `<audio>` tags in the root | Thin cues: drop a soft SFX < 0.35 s after the previous one (118 cues passed). Keep ≤ ~0.6 SFX/s |
| A pill rendered "الـــ" and "Opus" far apart | `#id span { padding… }` also styled the inner `.lat` span | Use child selectors (`#id > span`) on pills that contain `.lat` |
| `check` fetched "EB Garamond" from Google Fonts | `font-family: Georgia, serif` in a quote card | Only the vendored fonts (Cairo/Montserrat/Kufi/Manrope) in compositions |
| "و" + Latin span rendered as a stray glyph after the English word | bidi: a lone Arabic letter before an LTR span | Don't glue a single Arabic letter to an English span; drop it or use a full Arabic word |
| Narrated fact differs from the source (Dots "phone number" vs "call your dot in ChatGPT") | narrator memory | On screen use wording true to both ("VOICE CALL"), flag it in the handoff |

## 11. Project review — Oct 2026 (bugs found by reading the code, fixed)

| Symptom | Cause | Fix / prevention |
|---|---|---|
| `selftest.py` failed at `hyperframes check` (`request_failed … css2`) | `assemble.py` loaded Noto Kufi / Manrope from Google Fonts — a render that depends on the network | Fonts vendored: `@font-face` → `assets/fonts/*.ttf` copied from `kit/motion/fonts` |
| `assemble.py --captions on` crashed when `captions.json` was missing | `capbg`/`kwc`/`pos` were only defined inside the captions branch | Defaults set before the branch |
| Storyboard `caption_keywords` with capitals (e.g. "ChatGPT") never styled | keywords stored lowercased, compared case-sensitively | `is_keyword` compares `w.lower()` |
| Any website open in the browser could approve a storyboard (= spend credits) or rewrite `config.json` (e.g. `api_base` → keys sent elsewhere) via the dashboard | no CSRF / DNS-rebinding protection on `localhost:8788` | Host must be local; POSTs must be `application/json` with a local (or no) `Origin` |
| Dashboard still showed "approved" after the storyboard was edited | `project.json approved` was never reset on edit | Edit resets it; overview uses the storyboard status (the same rule as `generate_assets.py`) |
| `generate_assets.py --mock` booked $0.04/image and would call the paid video API without `--no-video` | mock only covered images | Mock implies `--no-video` and books $0 |
| Approved estimate ≠ spend for AI clips | estimate used min(8, scene length), the generator used 8 s | One rule: `common.clip_seconds()` |
| A 4xx image error was retried 3× | generic `RuntimeError` | 4xx (not 429) → `PermanentError` (no retry) |
| OpenAI key visible in the process list during transcription | key passed to `curl` on the command line | `requests` with a header + 15 min timeout |
| `voice_analysis.json` said `timing_preserved: true` after silences were cut | hard-coded | Real value recorded; docs say: `--no-silence-cut` for anything synced to video |
| Timed privacy `blur` without `t1` added a tween at an undefined position | missing guard in `screen.js` | No `t1` = stays to the end |
| Screen recordings rendered with lossy frame extraction | `render_final.py` didn't pass `--video-frame-format png` | Passed automatically when `compositions/screen.html` exists |
