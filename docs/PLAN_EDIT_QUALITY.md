# Plan — edit quality: clean audio, no dead air, no missed stutters (Oct 2026)

Trigger: Nano Banana 2.1 review. Hossam heard "sh" hiss, long pauses, and a stutter at 05:43 that was never cut.
Root causes and fixes are in `LESSONS_LEARNED.md` §14. This file is the system plan: what is done, what is next.

## Done (in the pipeline now)

| Area | Change | File |
|---|---|---|
| Audio — joining | Multi-file inputs joined with video-only concat; voice decoded losslessly per file and placed sample-exact; per-file HF verification | `pipeline/join_inputs.py` (new) |
| Audio — cleanup | Noise-floor test; clean sources (≤ −65 dB pauses) pass through untouched → `voiceover_raw.wav`; `--force-process` to override | `pipeline/clean_audio.py` |
| Audio — cutting | Cuts from `voiceover_raw.wav` (falls back to `voiceover_clean.wav`) | `pipeline/screen_edit.py` |
| Audio — gate | Preflight fails if the composition voice's >12 kHz share is > +2 dB above its lossless source | `pipeline/preflight.py` |
| Dead air | `edge_pad` trims silence at every keep-range edge (no stacked seam pauses); tighter pause defaults for narrated screen reviews | `pipeline/screen_edit.py` |
| Stutters | Micro-piece restarts (across chunk edges) + "unworded speech" detector with restart confirmation | `pipeline/find_stutters.py` (new) |

New standard order for voice + screen projects:
```
python pipeline/join_inputs.py <name> <files…>            # only when there are several input files
python pipeline/clean_audio.py <name> --input …/voice_joined.wav --no-silence-cut   # pass-through if clean
python pipeline/transcribe.py <name>
python pipeline/find_retakes.py <name>                     # retakes, false starts, noise (chunk level)
python pipeline/find_stutters.py <name>                    # stutters inside / across chunks
# apply EVERY proposal >= 0.6 (or note why not) -> input/screen_edit.json or input/edit.json
python pipeline/screen_edit.py <name> --preview            # edge_pad 0.15, pauses 0.6/0.35/0.7 for narrated reviews
```

## Next (proposed — not built yet)

1. **One review page for all cuts.** Merge `stutters.proposed.json` into `review/cuts.html` (listen before/after,
   tick, export) so retakes, noise and stutters are approved in one place. *Effort: small.*
2. **Auto-apply proposals to `screen_edit.json`.** A helper that splits keep ranges at every approved cut, so no
   proposal is forgotten (415.5 / 449.5 were). *Effort: small.*
3. **Dead-air report in preflight.** Measure every pause in the final voice; warn > 0.8 s (outside holds), fail
   > 1.5 s, and list them with timestamps. *Effort: small.*
4. **Author motion beats in SOURCE seconds.** Builders write `S(src_t)` instead of output seconds so a re-cut
   never desyncs the intro/outro (this project needed an old→new remap). *Effort: medium (kit + template).*
5. **J/L cuts on pause tightening too.** Today J/L applies only at keep-range seams. For pause cuts with a screen
   change in the removed gap, let the picture lead by up to 0.3 s (L-cut). Reliable because picture and voice keep
   the same source offset inside a segment. *Effort: medium; test on one project first.*
6. **Stutter detector v2.** Add a 3rd signal: word-duration outliers in whisper timings (a "word" lasting > 2.5×
   its expected length often hides a repeat). Score all signals together; keep acoustic matching out (it failed). 
   *Effort: medium.*
7. **Listening QA artifact.** `deliverables/audio_check.wav`: the final mix (voice + SFX) rendered with ffmpeg
   from `cues.json`, so the user can check audio in any player before the long video render. *Effort: small.*
8. **Preview cache-busting.** `motion_sync.py` appends a content hash to media URLs (`vo.wav?v=abc123`) so Studio
   never plays a stale file. *Effort: small.*
