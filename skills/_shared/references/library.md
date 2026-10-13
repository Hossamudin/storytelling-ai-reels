# Asset library — find before you generate, add after you make

One shared store for everything worth reusing across videos: logo files, photos of the creator, generated
images, b-roll, SFX, real web captures, screen recordings, finished episodes, verified QR codes, reusable
scene components. Media lives in `<studio>/library/<type>/`; the catalog is `library/index.jsonl` +
`library/INDEX.md` (one line per asset — read this first) + `library/_sheets/` (numbered contact sheets per type,
so you can pick visually with one image read).

All commands run from the studio folder.

| Do | Command |
|---|---|
| Search | `python engine/pipeline/lib.py find "logo dark" [--type logo]` |
| Bulk-import a folder the creator already has | `python engine/pipeline/lib.py import "<folder>" [--type T] [--tags a,b]` |
| Add one file | `python engine/pipeline/lib.py add <file> --type <type> --subject <2-4 words> --desc "<what it shows>" --tags "a,b,c" --source "<where from>"` |
| A generated asset | add `--prompt "<prompt>" --model <model id> --cost 0.04` |
| Copy into a project | `python engine/pipeline/lib.py use <id> projects/<name>/<part> [--to assets/images] [--as file.png]` |
| Import a finished project's generated/captured assets | `python engine/pipeline/lib.py harvest <project>` |
| AI-describe + rename vague images/clips (needs OPENAI key) | `python engine/pipeline/lib.py describe [ids…]` |
| Rebuild INDEX.md + contact sheets | `python engine/pipeline/lib.py index` |

Types: `person-photo` · `person-cutout` · `person-clip` (the creator) · `logo` · `img` · `broll` · `sfx` · `music` ·
`screen` (recordings) · `capture` (real web/app screenshots) · `3d` · `code` (reusable scene components) ·
`episode` (finished videos, thumbnails) · `qr` (verified QR codes). Duplicates are detected by content and skipped.

## Rules

1. **Search first.** Before any paid generation, `find`. A reel once reused 18 library assets and generated nothing.
2. `--subject`: the thing itself, 2–4 words (`brand-logo-dark`, `presenter-suit`, `whoosh-soft`).
3. `--desc`: one plain sentence a stranger can picture — content + style + background; for videos the useful
   time ranges ("clean 111–126 s; zoom at 109 s").
4. `--tags`: 5–10 lowercase single words: brand/tool names, objects, style (clay/3d/flat/photo/ui), mood,
   colors, use (hook/cta/b-roll/background), and warnings (`privacy-guest-names`, `account-name-visible`).
5. `--source`: URL + date for captures, original path for recordings, the project for generations.
6. **Real data** (benchmarks, prices, pages): type `capture`, tag `real-data`, source = URL + capture date.
7. **QR codes**: flatten onto white with a ≥ 4-module margin, decode to verify (a transparent QR looked fine
   but no phone could read it), put the URL in `--desc`, type `qr`.
8. **Screen recordings**: note private content (names, emails, search history, tabs) in tags + desc so builds crop it.
9. **Finished videos** go in as `episode` — useful for "watch the previous video" end cards.
10. **Photos of the creator**: fix EXIF rotation before cutting out (`ImageOps.exif_transpose`); high-res JPGs cut
    out far better than small PNGs (`npx hyperframes remove-background photo.jpg -o cutout.png`).

## At delivery

`lib.py harvest <project>` (everything generated or captured is cataloged), then add anything hand-made
that will recur (a lower-third component, a logo sting) as type `code` or `episode`. Tell the creator what
was added: "Saved to your library for next time: 3 SFX, 1 logo sting, the final video."
