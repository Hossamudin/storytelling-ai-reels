# Composition craft — building scenes with HyperFrames + the motion kit

HyperFrames renders HTML/CSS/JS to video, frame by frame, deterministically. If the HyperFrames skills are
installed (`hyperframes`, `hyperframes-core`, `hyperframes-animation`, `media-use`…), load them for deep API
questions; if not, `npx hyperframes skills` installs them, and `npx hyperframes docs` shows docs in the terminal.
This file is the distilled, production-tested subset.

## Project shape (made by `new_motion_video.py`)

```
projects/<name>/<part>/            one HyperFrames project per deliverable (intro, outro, reel… are siblings)
  index.html                       root: chrome, wipes, flash, vignette, grain, scene hosts, audio  (markers are regenerated)
  compositions/sN.html             one sub-composition per scene (created from the kit template, never overwritten)
  scenes.json                      [{"id":"s1","start":0,"duration":5.35,"beat":"...","title":"...","template":"quiz|recap"?}]
  cues.json                        voice + SFX: [{"t":10.37,"sfx":"library/impact-bass-1","accent":1.7}]
  chrome.json                      {"enabled", "series", "sections":[{"t","label","title"?}], "wipes":[t…], "steps":[…], "grain": bool}
  assets/{css,js,fonts,sfx,voice,images,…}   kit copy + brand.css + brand fonts
  BRIEF.md                         the approved treatment, invented strings to flag, generation plan
```
`python engine/pipeline/motion_sync.py <name> --part <part>` regenerates hosts, audio tags (SFX gains from
`levels.json` × accent, each SFX on its own track), chrome, wipes, steps and the root duration. **Re-run it after
any timing change** — durations live in one place.

## Kit reference (`assets/js/fx.js`, `assets/css/base.css`)

Inside a scene: `const fx = window.HF_SCENE(<scene start>)` — all times are GLOBAL voice seconds.
Helpers: `rise, maskUp, pop, out, hide, letterDrop, band, draw, strike, ringPulse, stamp, shake, breathe, drift,
counter, meter, typeText, cursorTo, click, toasts, pushIn, punch, zoomThrough, whipOut` (+ `fx.tl` for raw tweens).
Root helpers: `HF_WIPE`, `HF_CHROME`, `HF_STEPS` (step tracker), `HF_GRAIN`.
CSS: `.card .pill(.on/.bad) .tag .t-label .t-hero/.t-h1/.t-h2/.t-h3/.t-body .hl>.band+.txt .xbadge .stamp
.window>.bar .toast .cursor .ripple .caret .node .ring .dots .blob .glow .mask>.in .lat .num`.
Templates: `quiz`, `recap` (learning aids) via `scenes.json "template"` + `"data"`.
Presets: `light` (paper, Apple-keynote feel) / `dark` (control room, editorial chrome) on `#root[data-preset]`.

## The contract (break it and the render fails or drifts)

- Root `#root` has `data-composition-id`, `data-start="0"`, `data-duration`, `data-width/height`. Scene hosts are
  direct children with `class="clip"`-style timing attributes (motion_sync writes them).
- One paused GSAP timeline per composition, registered in `window.__timelines`. No `repeat: -1`, no wall-clock time
  (`Date.now`, `performance.now`), no `Math.random()` without a seed — renders must be identical every time.
- **No network at render time.** GSAP is vendored (`assets/js/gsap.min.js`); fonts are local; images/clips are
  local files. A CDN script once blocked a final render with `sub_timeline_script_failure`. `preflight.py` rejects
  any remote URL. Fonts like `Georgia, serif` can make `check` fetch Google Fonts — use only vendored fonts.
- `<video>` and `<audio>` are framework-owned: muted video with its own `data-start/data-duration`, sound on a
  separate `<audio>`; inside a scene with nonzero `data-start` add `data-hf-media-start-basis="local"`.
  Put a still frame of the clip's best/last frame under every `<video>` (clips can end early or go black while loading).

## Gotchas that cost hours (all solved — follow these)

| Symptom | Fix |
|---|---|
| Blank video | `direction: rtl` on `#root`/text containers, never `<html dir="rtl">` |
| GSAP "target not found" in a scene | A sub-composition's inner root merges into its host — select `#s3-title`, never `#s3 .title` |
| `invalid_parent_traversal_in_asset_path` | `@font-face` lives in the root `<style>` with `assets/fonts/...` (no `../`) |
| Elements visible before their entrance | Hide with a `fromTo` at build (`fx.hide`); later re-tweens get `immediateRender: false` |
| `gsap_css_transform_conflict` | Don't put a CSS `transform` and GSAP transforms on the same node; center with `xPercent/yPercent` |
| Element jumps to the top of the frame | Every block placed with `top:` also needs `position: absolute` (or `.abs`/`.row`) |
| Bars/shapes invisible though `check` passed | An absolute child with only `bottom: 0` has no height — give it one; **snapshots catch what check can't** |
| Text flagged as overlapping (tall Arabic glyphs, EN caps over AR) | line-height 1.2–1.3, verify in a snapshot, then `data-layout-allow-overlap` on the flagged child elements themselves |
| Off-canvas motion flagged | `data-layout-allow-overflow` (HF_WIPE and maskUp add it) |
| `subcomposition_blanks_before_host` | The base/closing scene runs to the root's end |
| `gsap_relative_value_second_writer` | Absolute values only when two tweens can overlap (no `"+=…"`) |
| Overlapping SFX warnings | Each `<audio>` its own `data-track-index` (motion_sync does it) |
| `composition_file_too_large` | Too many SFX tags: drop a soft SFX < 0.35 s after the previous one; ≤ ~0.6 SFX/s |
| Scene exits overlap the next scene → audio/visual 2-sample overlaps | Exit fades end before the next scene starts |
| Highlighter band becomes a big block | `.hl` is `nowrap`; keep highlighted phrases short; parent `isolation: isolate`, never `z-index:-1` |
| Orange/yellow text unreadable on paper | Use bright accents for shapes/bands; text ≥ 90 px or dark text on them |
| Logo from `<symbol viewBox="-50 -50 100 100">` off-center | Outer `<svg viewBox="0 0 100 100">` + `<use width="100" height="100">`; only the symbol has the centered viewBox |
| Callouts run off the frame when zoomed | Short text (≤ ~22 chars at zoom), position away from the nearest edge |
| Template scenes clipped in 9:16 | Use `{{W}}/{{H}}` + responsive CSS; never hard-code 1920×1080 |
| Patch scripts miss tags after Studio edits | Studio inserts `data-hf-id` and reorders attributes: attribute-order-tolerant regexes; strip `data-hf-id` from copied markup |
| Shell heredocs with Arabic/quotes break (Windows) | Write patch scripts to a file and run them with Python |
| `check` "Navigation timeout" once | Machine busy — re-run with `--timeout 30000` |

## Quality loop (every scene)

1. `npx hyperframes check` → 0 errors, 0 warnings (run inside the part folder).
2. `npx hyperframes snapshot --at <t1> <t2> …` at each scene's **busiest** moment → look at every PNG. Snapshots
   caught 7 issues `check` passed (missing heights, spotlights on closed dialogs, clipped callouts).
3. `npx hyperframes preview --background` → give the creator the URL; Studio reloads on file changes.
4. Re-snapshot after each fix round.

## Timing rules (feel professional)

- Each visual change starts 0–0.2 s BEFORE its keyword (impacts 0–80 ms before). Counters reach their value
  before the number is spoken.
- A new visual beat every 2–4 s; nothing static > 4 s; a hero moment every ~20 s.
- Scene exits 0.25–0.35 s. Fill silences with motion, never with nothing.
- Sound: voice is king; SFX ~8–10 dB under it (gains come from `sfx_levels.py`); final master −14 LUFS / −1.2 dBTP.
