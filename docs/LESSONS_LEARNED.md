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
| UI SFX land late after their visual (error buzz ~0.6 s, ping ~0.3 s, chime/typing ~0.4 s) | Kit files start with silence or a slow attack; cues place the file start, not the attack (whooshes: the peak, ~0.15 s in) | Shift each cue earlier by the file's attack/peak offset. Prototype: `projects/ai-4years-60s/reel/sound_ab/` (A/B vs the real render). Not in `motion_sync.py` yet |
| "Varied" whooshes/clicks sound identical; stacked cues phase | `whoosh.mp3` = `whoosh-short.mp3` and `click.mp3` = `click-soft.mp3` (byte-identical). Cues 30–80 ms apart double the same sample | Treat each pair as one sound; vary with pitch/speed variants (±1–2 semitones) and round-robin; merge same-family cues < 0.12 s apart |
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

## 11. Mixed full-screen + windowed screen recording (game HUD) — n8n AI Agents, Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| Browser tabs/bookmarks (private history, banking URLs) + a game HUD bar at the bottom in some stretches only | Presenter switched between full-screen and windowed browser while a game overlay ran | Detect per 0.5 s (bookmark-row + extension-icon variance, brown HUD strip), then render a normalized source: ffmpeg `split` → crop+scale the windowed ranges → `overlay=enable='between(t,a,b)'`. One timeline, no sync risk; `screen_edit.json "source": "input/screen_norm.mp4"` |
| Captions showed "and Message" / "publicly chat Make" | each English word was its own LTR span inside RTL text, so bidi reversed the word order | Merge consecutive Latin words into ONE `.lat` span (`'</span> <span class="lat">' -> ' '`) |
| "الـagent" token rendered with the Arabic prefix on the wrong side | whole token wrapped in an LTR span | Split: Arabic prefix outside (`الـــ`), Latin part in the span |
| Annotation camera wrong in 9:16 | `screen.js` hard-coded 1920×1080 | `screen.js` now reads `A.fw/A.fh` (viewport size); `annotations.json "window": {"fw","fh"}` → `screen_annot.py` passes them |
| Reel needs a different cut of the same recording | `screen_edit.py` reads one fixed spec | Keep `screen_edit_reel.json`, swap it in, run, move outputs to `assets/screen_reel/`, restore the long spec + outputs |

## 12. Short screen-share tip (2.5 min → 1:43) — n8n Node + Templates trick, Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| Windowed browser (tabs, private self-hosted n8n URL, bookmarks) in two stretches only | presenter switched between the full-screen templates site and a windowed editor | When the app's own header colour continues the chrome band, a time-gated ffmpeg `drawbox` (fill = header colour, `enable='between(t,a,b)+…'`) over the top 122 px is enough — no crop/scale, so annotation pixels stay identical across the whole source |
| Narration explains settings / input / output while the node dialog is still closed (it opens 1 s after the sentence) | presenter talks ahead of the clicks | `freeze` the voice over a frame where the dialog IS open (`"at"` later than the audio) and spotlight its panels one by one |
| Spotlight on a search-suggestions dropdown pointed at "Searching…" | dropdown closes ~0.5 s after Enter | Check dropdown/close times on 0.2 s frame strips before timing a spot on transient UI |
| Retake finder cut only the first half of a repeated CTA (left "…في التعليقات" + the clean retake) | its cut ended at a chunk boundary inside the botched take | Read the window words around every proposed cut; extend it to the clean take's first word |

## 13. Sponsored model review: intro VO + 2 narrated screenshares + outro VO — Nano Banana 2.1 × Higgsfield, Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| Four separate inputs (intro VO, 2 screen recordings with live narration, outro VO) | Recorded in pieces | Concatenate into ONE source (`input/screen.mp4`: VO over black + screens + VO over black, 1 s gaps, 1920×1080) with `SOURCE_MAP.md`; one transcript, one `screen_edit.json`, cutaways cover the VO-only stretches |
| Whisper transcript became one phrase repeated 90× after 466 s | long-file whisper-1 loop | Ignore `transcript.json` for long files; use `find_retakes.py` chunks (verbatim) + `window_words.json` (timings). Map words to output with `screen_edit.map_time` |
| On-screen model names were risky (narrator said "GPT" over which image?) | Comparisons shown one image at a time | Check 1–1.5 s frame strips at every comparison before placing model-name pills; pills only where image + speech agree |
| Captions would show "GPT-4.5", "حرامبلور" | ASR mangles product names | Skip word captions on screen-share reviews; carry names in model pills, callouts and cutaways |
| User asked to "use the Media Kit" but none was public | kit lives in the Creator Dashboard | Use the official glyph SVG from the brand's own site (`hf-logo__glyph`) + `/icon.png`; note the swap in the publish checklist |
| Higgsfield MCP could not upload local files | no upload tool in that connection | Existing account Elements expose `media_input` ids (`manage_reference_elements list`) usable as `medias` references; prior job ids work too |
| "Broken Arabic" effect re-joined into a word | separate inline spans still shape together | Use isolated presentation forms (U+FE95 ت, U+FEB9 ص, U+FEE1 م, U+FEF1 ي) |
| Sponsor deliverables forgotten until the end | requirements arrive with the footage | Keep `deliverables/YOUTUBE_PUBLISH.md`: title options, UTM link in line 1, keyword list, pinned comment, checklist |

## 14. Audio integrity, dead air, hidden stutters — Nano Banana 2.1 review fixes, Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| "sh" hiss on the voice; the user's original files were clean | (1) the 4 inputs were joined in ONE ffmpeg concat graph with the video: irregular screen-recorder audio timestamps made it insert/drop samples (body drifted 0 → +312 samples) → broadband hiss (>16 kHz band −63 → −35 dB). (2) `clean_audio.py` then ran denoise + de-esser + compressor on an already-clean voice | **`pipeline/join_inputs.py`**: video joined alone; each original's audio decoded straight to PCM and placed at its offset with numpy, verified per file (HF band ±1.5 dB). **`clean_audio.py`**: measures the pause floor; ≤ −65 dB → lossless pass-through (`voiceover_raw.wav`, no filters, no loudnorm); `--force-process` to override. **`screen_edit.py`** cuts from `voiceover_raw.wav`. **`preflight.py`** fails if the composition voice's >12 kHz share is > +2 dB above its lossless source (catches both failure modes: +6.8 and +2.7 dB here) |
| A fix "didn't work" in Studio | the browser cached the old `edited.wav` (same filename) | When replacing media for a preview, give it a NEW filename (`vo_clean.wav`) |
| My first null tests said the join was badly damaged | a 1-sample offset makes the >4 kHz residual huge | Align by cross-correlation per window (and look at the lag over time) before judging; compare band-energy SHARES, not residuals, for "is there added hiss?" |
| Pauses felt long (05:38–05:39, 05:54–05:56, 06:36: 1.5–2.3 s) | `busy_pause_keep` 1.2 s kept long pauses whenever the screen moved, and trailing + leading silence STACKED at every keep-range seam | `screen_edit.py "edge_pad": 0.15` trims silence at both ends of every keep range; narrated screen reviews: `max_pause 0.6 / keep_pause 0.35 / busy_pause_keep 0.7` → no speech pause > 0.8 s left (10:01 → 9:15) |
| Re-editing shifted every hand-timed intro/outro beat | motion beats authored in OUTPUT seconds | Keep a copy of the old `edit_map` (`edit_map_v1.json`) and remap old output → source → new output (`R()` in the project build.py). Better: author beats in SOURCE seconds from the start |
| Stutter at 05:43 ("والن…" → "والنانو بانانا 2.1") never proposed | the false start ended one pause-chunk; whole-chunk ASR silently DROPS it (verbatim text "…رائعة جداً." / whisper words end 463.07, resume 464.70) | **`pipeline/find_stutters.py`** (run after `find_retakes.py`): (a) split chunks at ≥ 60 ms micro-pauses, transcribe pieces, flag a short piece the next one restarts — also ACROSS chunk boundaries; (b) "unworded speech": voiced ≥ 0.25 s with < 15 % ASR word coverage → transcribe alone → if it prefixes the following words = stutter (0.9), else review (Latin-script ASR on Arabic = real word missed by whisper, e.g. "Levez dio" = الفيديو) |
| Acoustic (MFCC + DTW) prefix matching could not separate the stutter from normal speech | false starts are clipped/partial syllables | Don't rely on it; keep `pipeline/acoustic_match.py` only as a helper |
| find_retakes "noise" proposals (415.5, 449.5) were not applied | screen projects edit keep ranges by hand | After find_retakes + find_stutters, apply EVERY proposal ≥ 0.6 or write down why not |
| Windowed browser (tabs, bookmarks, taskbar) visible while naming an extension | presenter turned on HaramBlur before going full screen | Brightness of the tab strip (top 40 px) per 0.25 s finds windowed stretches; blur tabs / bookmarks / extension icons / taskbar but keep the thing being explained |

## 15. Long windowed screen review with live API keys — Decisions API vs Jev, Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| Real API keys readable on screen (OpenAI `sk-proj-…` pasted into an n8n HTTP header; TypeSafe `apikey_…` in three later stretches) | presenter pasted keys live while recording | Crop one reference frame of the key field, then frame-match that rect over the whole video (mean abs diff < 2 = visible) → exact windows → baked `boxblur` overlays in a normalized source (`prep/make_norm.py`). Tell the presenter to rotate the keys, because the raw file still has them |
| Personal Gmail headers (own address, real emails) inside an n8n node's INPUT panel | an old execution's data showed in the panel | Signature-match the panel header across the video at 2 fps; blur the whole INPUT panel with timed `blur` annotations |
| `boxblur=18:3` failed ("chroma_param radius … must be <= 13") on a 370×54 crop | the chroma radius defaults to the luma radius, and the chroma plane is half size | Use named params: `luma_radius=18:luma_power=3:chroma_radius=10:chroma_power=3` |
| whisper-1 repeated one word for the last 9 minutes (19-min file) | long-file loop (again) | Use `find_retakes` chunks + `window_words.json` for anything over ~8 min; never read `transcript.json` past the first loop |
| find_stutters flagged spoken "n8n" ("إن إيت إن"), list items ("مبيعات… توظيف") and "مختلفة شوية ×2" as restarts | the restart heuristic matches similar-sounding short pieces | Read the window words around each ≥ 0.6 proposal; reject different content and brand names spelled out letter by letter |
| A spotlight pointed at an empty area | the n8n log panel flickered closed for 0.5 s inside the spot window | Check the target's visibility at 2 fps across the WHOLE spot window, not just at its start |
| A 19-min windowed recording (tabs, bookmarks, taskbar visible throughout) | recorded in a normal browser window | One `crop` to the content area (y 122–1030) in the normalized source → no per-stretch masks, and annotation pixels stay constant |

## 16. News episode recorded piece by piece (one session per story) — AI News 10 Oct 2026, STORY 01 TestSprite

| Symptom | Cause | Fix / prevention |
|---|---|---|
| Pieces made in separate sessions drift apart (canvas, chrome, loudness, edges) and won't concat cleanly | each session decides on its own | One `SERIES.md` next to the recordings locks canvas/preset/chrome/edges/export + status table; one project per piece (`screen_edit.py` handles one recording per project); every session reads it first |
| Research note said "$3,000 + $1,000"; narration said "$1,500 / $750 … 5th" | both true: $3,000 project pool split 1,500/750/450/150/150 + separate $1,000 CLI bonus | Read the real page in the recording (prize frame) before flagging a mismatch |
| Zoomed screen pushed the window top under the chrome; chrome text unreadable over a light page (contrast 2.95:1) | `screen.js` clamps zoomed windows to 40 px from the frame edge, so every zoom > 1 reaches the chrome band | Project CSS: dark backing pill on `#chrome .tl, #chrome .tr` (`rgba(4,22,20,.82)`); zoom YouTube players at 1.15 instead of 1.38 |
| `lib.py use <id> news-…/composition` created a stray folder at the repo root | target is resolved relative to the repo root | Always pass `projects/<name>/…`; `--as` needs the file extension (`series-sting.mp3`) |
| Dashboard showed the account name + email (bottom-left) and "Hello, <name>" (chat panel) | presenter's logged-in TestSprite workspace | Timed `blur` items over both rects for every dashboard stretch (same rects in the projects and test-case views) |
| QR link chip (root overlay, z 83) covered the last rows of a cutaway checklist (STORY 02, c4) | chips sit at a fixed bottom-right rect while cutaways lay out freely | Run `hyperframes check` (it flags `content_overlap` inside `#lk*`); park the chip lower (`top:880px`) or keep cutaway content above y ≈ 820 while a chip is up |
| Speaker said "موديل L" for the third question type | ASR mangled "predicate" in whole-chunk transcription | Re-transcribe `edited.wav` (words.json) and read it; the screen dropdown confirmed it — label with the real UI name |
| Page-only recording (1904×908 browser, no UI to point at for 40 s) → callouts landed on top of the page text and read as noise | `spot` callout `pos: top/bottom` sits on the neighbouring text of a dense article | Spot the whole text line/block and use `pos: "right"` (empty page margin) with dim on; STORY 07 EmbeddingGemma 2 |
| ASR wrote "Cohere embedding 8B" / "Gemini 2"; the page chart says Qwen3-Embedding-8B and the model is EmbeddingGemma 2 | whole-chunk ASR guesses brand names | Label from the page (read the chart frame), never from the transcript; non-16:9 recordings: set `SW, SH` + window `k` in build.py and annotations.json `window` (here k 0.9 at 103,130) |
| Windowed Chrome frame (tab strip, profile avatar) leaked for 0.1 s after cutting 10 s of silent navigation | `screen_edit.py` J/L lead (`l_max` 0.5) shows the picture up to 0.5 s before the kept audio | Check the first frames after every cut into a fullscreen stretch (top-60 px brightness); lower `jl.l_max` (0.38) or move the keep start |
| Privacy blur missing for the first frames after a cut | annotation times are audio-anchored (`map_time`), the picture starts earlier with an L-cut; the blur also fades in | In build.py pad every `blur` t0/t1 by 0.4 s (0.9 s before a stretch that starts right after a cut) and cap t1 before any overlay that must stay sharp |
| `render_final` preflight failed on lint warning `nested_media_start_basis_ambiguous` for a second `<video>` inside the screen sub-composition | nonzero `data-start` in a sub-composition | Add `data-hf-media-start-basis="global"` (screen host starts at 0) |
| 46-s tweet clip (656×822) as a cutaway | no media-in-cutaway precedent | Trim to H.264 (-g 15, no audio) into `assets/videos/`, place as a `class="clip"` video + dark backing inside `#scr-inner` for the last seconds, Arabic metric/source tags either side |
| `render_final` preflight failed on a layout WARNING (`panel_out_of_canvas #scr-win`, 78 px) after a `zoom` s 1.2 on a form at the window's right side | `screen.js` clamps the zoom to 40 px from the frame edge, but the window itself (k 0.85 at x 145) slides off the canvas when the zoom centre is right of ≈ x 980 | Zoom only when `145·s + (960 − cx·s) ≥ 0` (centre ≤ ~980 src px at s 1.15) or skip the zoom and use spots; STORY 09 n8n Agents (also: browser status-bar hover URLs show the instance name → detect with a 14 px strip brightness scan at 4 fps and blur only those windows) |
| Highlighted word invisible for 2 s before its band (`check` contrast 1.1:1) | dark preset `.hl > .txt` is ink-coloured, the band starts at scaleX 0 | Give the `.txt` an id and tween `color` off-white → ink when the band sweeps (INTRO s1/s3) |
| End-screen slot outline came out yellow on both slots | `stroke="var(--lime)"` — CSS variables don't resolve in SVG presentation attributes | Hex colours in SVG attributes (or set `stroke` via a CSS rule) |
| Stutter finder + whole-chunk ASR said "في في التعليقات"; the cut clipped "رأيكم" | it was "رأيكم فيه في التعليقات" | Always read `voice_edit --verify` "replace:" lines after a cut; if the heard text changes a neighbouring word, drop the cut |


## 17. Talking-head reel, round 1 feedback — "سنتين ونص في 60 ثانية", Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| **"Text behind me" covered Hossam's face** | `remove-background` ran as an agent background shell; the session ended at 99.7 %, leaving only `.tmp-*-matte.webm`. With no matte, every `#behind` element draws over the person | Launch the matte **detached** (`Start-Process … remove-background … > matte.log`), confirm the final `.webm` exists, cut segments (`reel/cut_matte.py`), snapshot every behind-window. `check` reports `missing_local_asset` for missing matte segments: treat it as a blocker, never preview without it. Place behind-text beside the head/shoulders, not centred on the face |
| Graphics felt theoretical | concept animations for things that have real visuals | Real logos (library has n8n/Make/Zapier/Claude/OpenAI), real n8n footage (`projects/n8n-node-templates/input/screen.mp4` 21–25 s first workflow, 64–68 s template canvas; crop out tabs/URL), 2D people for stories |
| Face on screen only ~55–65 % | full-screen scenes of 4–9 s | 70–80 % face: full-screen cutaways 1.5–3.3 s, the rest in card / circle mode |
| Lime circle ring stayed visible after circle → card | `th_layer.py` hid the ring only on circle → hide/full | Fixed: circle → card fades `#fr-ring` |
| `th_layer.py` crashed `'NoneType' … group` | Studio added `data-hf-id` before `id="root"` | Fixed: attribute-order-tolerant root regex |
| New icon symbols silently missing | patch anchored on `<symbol id="i-cursor"`, which Studio had rewritten | Insert new `<symbol>`s before `</defs>` and assert the count after patching |
| Higgsfield: a prompt was bounced with "preset recommended" | the batch tool auto-recommends presets | Resubmit with `declined_preset_id` |
| B-roll of Hossam without uploading photos | MCP has no upload tool | Element `hossamudin` (`cb88ff02-…`) via `<<<id>>>` in a `seedance_2_0` prompt gave a faithful likeness |

## 18. 2D story reel built by parallel sub-agents — "ناس كتير مش عارفة تستخدم الـ AI", Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| Voice note held two alternative hooks + "ده الهوك رقم واحد…"; I merged them into one opening | presenter recorded options | **Hossam's rule: two hooks = two videos** — MAIN (hook 1) + 2nd version (hook 2), same body. Per-part cuts in `edit.json`, `hooks.json` + `make_versions.py` (`prompts/two_hooks.md`); `find_retakes` now prints `!! TWO HOOKS?` |
| Sub-agents would collide on shared files | one index.html / build_lib for 18 scenes | Director owns `build_lib.py`, `index.html` (`build_root.py`), `scenes.json`, `chrome.json`, `cues.json`; each agent owns `build_<x>.py` + its `compositions/sN.html` + `cues_<x>.json`; `merge_cues.py` merges + thins (≥ 0.75 s between SFX) and runs motion_sync |
| Shared visuals must look identical across agents | character + signature object reused in many scenes | Phase 1: one agent builds the kit (`char.py` 2D characters, poses, IK reach, idle JS) while UI-only scenes run in parallel; the signature object's owner writes `chain.py`; dependent scenes launch only after the module exists |
| Step tracker overflowed the 9:16 frame and sat under the reels UI | 5 pills at kit size, bottom placement | Project CSS: `#root .steps { top:150px }` + smaller pills; scenes keep y 140–250 clear |
| A sub-agent drew banknotes for "before you pay" | brand avoid list (money) not checked | Director reviews every contact sheet; replaced with subscription tickets |
| Supporting cast drawn smaller than the hero read as children | different `h` per agent | Same standing height for adults in one shot (char.py `h`) |
| `assets/lib/meta.svg` (library log-af262f) is the **Llama** wordmark | library caption says Meta | Label it Llama on screen, or fetch the Meta mark |

## 19. "The video is code" reel (Claude Code + HyperFrames), two hooks — Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| `font_family_without_font_face: cascadia mono` in two scenes only | the linter checks each sub-composition's own CSS; the root `@font-face` doesn't count for a family named literally in a scene `<style>` | Declare `--font-mono` on `#root` (series CSS) and use `var(--font-mono)` in scenes; vendored Cascadia Mono (OFL) from `C:/Windows/Fonts` for code/terminal text |
| `content_overlap` between a "code peel" layer and the frame it covers | the peel (opaque, clip-path wipe) leaves the covered text in the DOM | Fade the covered elements to 0 right after the wipe ends |
| Talking-head example clip opened on a graphic card, not the face | picked the cut window from a 2 s contact sheet | Strip the chosen 5 s window at 1 fps before using it; `-ss` timestamps ≠ the on-video timer |
| Inline `left:` on chips ignored | a leftover scene-CSS `#id { left }` rule overrode the inline style | Position in one place only (inline OR CSS) |

## 20. Infinite-sheet motion explainer (one zoomable world, 20 scenes) — How LLMs work, Oct 2026

| Symptom | Cause | Fix / prevention |
|---|---|---|
| A whole scene went blank for 12 s (`check` passed) | an element was given the id `s15-in`, which `make()` already uses for the scene's inner camera; `tl.fromTo("#s15-in", {opacity:0})` hid the camera | Scene ids `<sid>-cam / -in / -ov` are reserved. Never name content `<sid>-in*`; snapshot every scene |
| `[id^=s15-c]` faded out the entire scene | the prefix also matched `s15-cam` | Use classes for groups (`.s15-card`), never `[id^=<sid>-c…]` / `-i…` / `-o…` prefixes |
| Minimap missing → preflight `GSAP target #mm-m not found` | opening Studio added `data-hf-id` to `<div id="wipe">`, so an exact-string insert silently failed | Insert into index.html with attribute-tolerant regexes (as for the root tag) and assert the element exists after patching |
| `composition_file_too_large` (index.html > ~300 lines) | 150 SFX tags + ~100 lines of root camera tweens | Generate the root camera into `assets/js/sheet.js` (`window.LLM_SHEET(tl)`) and thin SFX to ≥ 0.85 s apart with a priority (impacts/chimes win) |
| `clip_media_fit` warning | `typing.mp3` is 1.5 s but the cue asked for 1.6–2.0 s | Cap cue `dur` at the file length (`ffprobe`); the riser is 10 s: play its LAST 1.5 s (`media_start` 8.5) |
| `duplicate_media_discovery_risk` | the same logo `<img>` twice in one scene | One `<img>` per source per scene |
| Narration said "17 tokens / 4 tokens" | checked, not assumed | `tiktoken` in the scratchpad (`pip install --target`): cl100k_base = GPT-3.5, o200k_base = GPT-4o/GPT-5; show the real token pieces |
| The narrator credited Attention to DeepMind | memory | Cut the clause, keep the term; put the real source (Google, 2017) on screen |
