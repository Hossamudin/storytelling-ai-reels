# Asset library — how it works and how to add to it

One shared store for everything worth reusing across videos. Media lives in `library/` on this machine
(gitignored); the catalog (`library/index.jsonl` + `library/INDEX.md`) is in git.

```
library/
  INDEX.md        one line per asset (id · type · aspect/duration · description · tags · path) — read this first
  index.jsonl     full records: id, file, type, subject, desc, tags, w/h/dur, source, prompt, model, cost, sha1, used_in
  _sheets/        contact sheets per type (numbered thumbnails) — pick visually with one image read
  <type>/         the files, auto-named: <type>_<subject>_<description>_<aspect>_<dur>_vN.<ext>
```

Types: `hossam-photo` · `hossam-cutout` · `hossam-clip` · `logo` · `img` · `broll` · `sfx` · `music` · `screen`
(screen recordings) · `capture` (real web/app screenshots) · `3d` · `code` (reusable scene components) ·
`episode` (finished videos, thumbnails) · `qr` (verified QR codes).

## Commands (run from the repo root)

| Do | Command |
|---|---|
| Search | `python pipeline/lib.py find "claude logo" [--type logo]` |
| Add a file | `python pipeline/lib.py add <file> --type <type> --subject <2-4 words> --desc "<what it shows>" --tags "a,b,c" --source "<where from>"` |
| Generated asset | add `--prompt "<prompt>" --model <model id> --cost 0.04` |
| Put it in a project | `python pipeline/lib.py use <id> projects/<name>/<part> [--to assets/images] [--as file.png]` |
| Import a project's generated/captured assets | `python pipeline/lib.py harvest <project>` |
| Auto-describe + rename images/clips | `python pipeline/lib.py describe [ids…]` (vision model; only vague ones unless ids given) |
| Rebuild INDEX.md + sheets | `python pipeline/lib.py index` |

The original file is copied (use `--move` to move it). Duplicates are detected by content (sha1) and skipped.

## Rules for whoever adds assets (human or AI)

1. **Search first** (`find`) — never add or generate something the library already has.
2. **`--subject`**: the thing itself, 2–4 words (`whacka-publish-live`, `claude-spark`, `suit-confident`).
3. **`--desc`**: one plain sentence a stranger can picture: content + style + background, and for videos the useful
   time ranges (`clean 111-126 s; zoom 109-110 s`).
4. **`--tags`**: 5–10 lowercase single words: tool/brand names, objects, style (clay/3d/flat/photo/ui), mood, colors,
   use (hook/cta/b-roll/background), and warnings (`privacy-guest-names`, `account-name-visible`).
5. **`--source`**: URL + date for captures, the original path for recordings, the project for generations.
6. **Real data** (benchmarks, prices, pages): type `capture`, tag `real-data`, source = URL + capture date.
7. **QR codes**: flatten onto white with a margin, decode to verify, put the URL in `--desc`, type `qr`.
8. **Screen recordings**: note private content (names, emails, search history, tabs) in tags + desc so builds crop it.
9. **Finished videos** go in as `episode` (for "watch the previous reel" / end cards).

## Free stock already in the library (2026-10-11, see `docs/PLAN_STOCK_LIBRARY.md`)

- **Logos** (~300): AI brands from LobeHub (MIT) and tech/social/tool brands from Simple Icons (CC0), in `-color` / `-mono` /
  `-wordmark` variants. Search them with `find "<brand> logo" --type logo`. They are trademarks, so use them only to
  name the company, never to imply it endorses the video.
- **B-roll** (27): Mixkit (free licence, no credit needed) plus NASA (public domain), ≤15 s, H.264, no audio. Tag `stock`.
- **Editorial photos** (36): AI leaders, HQs, chips, from Wikimedia Commons. Anything tagged `attribution-required` needs a
  credit line (author + licence, both in `source`) in the video description or on screen. `multi-person` = not a solo portrait.
- More sources once we have keys: Pexels / Pixabay APIs (free keys) for more footage.

## Example prompt to give an AI

> Add these files to the asset library in `C:\Users\H-Eld\Downloads\Code\Hossam Story telling` using
> `python pipeline/lib.py` and the rules in `docs/LIBRARY.md`: <paths>. For each, choose the type, write subject /
> desc / tags / source, check for duplicates with `find` first, verify any QR code by decoding it, note private content
> in the tags, then run `python pipeline/lib.py index` and show me the new INDEX.md lines.
