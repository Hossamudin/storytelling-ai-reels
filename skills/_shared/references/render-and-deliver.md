# Render and deliver — the best version on the first render

## First-time-right checklist (in this order)

1. Snapshots of every scene at its busiest moment, reviewed.
2. `npx hyperframes check` clean (inside the part folder).
3. The creator approved the Studio preview.
4. Screen projects: full-quality edit (`screen_edit.py` without `--preview`), copied into the part.
5. `python engine/pipeline/render_final.py <name> --part <part>` — never the Studio render button for a final.
6. Watch/listen to the mastered file's first and last 10 s.
7. Deliver from `projects/<name>/deliverables/` and offer the follow-ups below.

`render_final.py` = preflight → `hyperframes render --quality delivery --strict` → verify duration + audio →
master −14 LUFS / −1.2 dBTP → YouTube chapters (videos > 60 s with sections) → `deliverables/`.
`preflight.py <name> --part <part>` alone tells you if a project is render-ready: no remote URLs, no missing
files, full-quality screen edit, grain off on recordings, durations consistent, `check` clean.

## Long renders

An agent's background shell may be capped (~10 min). Launch long renders detached and poll the log:
- Windows (PowerShell): `Start-Process python -ArgumentList 'engine/pipeline/render_final.py','<name>','--part','<part>' -RedirectStandardOutput projects/<name>/deliverables/render_final.log -NoNewWindow`
- macOS/Linux: `nohup python engine/pipeline/render_final.py <name> --part <part> > projects/<name>/deliverables/render_final.log 2>&1 &`
Slow machine: `--quality draft` for review renders, split long videos into parts, render overnight.

## Delivery package

- `deliverables/<name>-<part>.mp4` (mastered) · `<part>_youtube_chapters.txt` (long videos: first chapter 00:00,
  ≥ 3 chapters, each ≥ 10 s) · the raw render stays in `<part>/renders/`.
- Report: duration, format, spend from `assets/ledger.json`, what was reused/generated, flagged items.
- `python engine/pipeline/lib.py harvest <name>` — keepers go into the library.
- Append the creator's feedback to `profile.md`; new problems to `lessons.md`.

## Always offer after delivery (one short list)

1. **Reels / mobile version** — a 9:16 cut per section (30–60 s each, captions, hook in the first second).
2. **Article / post pack** — key summary + ordered, named screenshots (`deliverables/article/NN_slug.png`, captions,
   alt text) + an outline in the creator's language.
3. **Ideas for next time** — a follow-up topic, a learning aid, one recording tip.
Plus a thumbnail concept and a title/description draft if they publish on YouTube.
