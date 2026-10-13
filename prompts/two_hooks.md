# Two hooks → two versions (Hossam's rule, Oct 2026)

Hossam sometimes records **two hooks** in one voice note, often announced ("ده الهوك رقم واحد، والهوك رقم اتنين أهو").
Deliver **two videos**: the **MAIN version** with hook 1, and a **2nd version**, the same video with hook 2.
Never merge the two hooks into one opening, and never silently drop one. If it's unclear which hook is main, use the
one he numbered (or recorded) first, and say so in the handoff.

`find_retakes.py` prints `!! TWO HOOKS?` when a chunk mentions a hook. Its LLM editor usually proposes cutting one hook
as a "retake". Don't accept that proposal: split the video into versions instead.

## 1. Voice: per-part cuts (one body, two hooks)
`input/edit.json` parts may carry their own `cuts`, which are added to the global cuts (`voice_edit.py`):
```json
"cuts": [ ...cuts shared by both (stutters, fillers in the body)... ],
"parts": [
  {"name": "voice",    "from": 0, "to": 233.07, "cuts": [[7.17, 9.0, "false start"], [12.06, 31.5, "hook 2 + announcement"]]},
  {"name": "voice_h2", "from": 0, "to": 233.07, "cuts": [[0, 23.32, "hook 1 + announcement"]]}
]
```
Cut the gap before the body loosely, ending inside the silence, so the silence rule sets the body's first edge in both
parts. Then check that the body keep ranges are **identical** (`transcript/<part>_words.json "keep"` for source ≥ the
body start). Both bodies are then sample-identical, offset by a constant.

## 2. Build the body once
- `scenes_master.json` holds the body scenes in their **authoring** times. `build_lib.Part` reads `scenes_master.json` +
  `hooks.json` and uses each scene's `t0` as the `HF_SCENE` origin. A sub-composition's timeline is local, so a body
  scene can be placed at any start without a rebuild.
- `hooks.json` holds the hook scenes per version, in version time: `{"id": "s2m", "version": "reel", ...}`.
- `cues_<agent>.json` holds body SFX in authoring time. `cues_hook_<version>.json` holds hook SFX in version time.
- `chrome_master.json` holds sections, wipes and steps in authoring time.

## 3. Place every version
`python <part>/make_versions.py` builds `reel/` (MAIN) and `reel_h2/` (version 2). For each version it:
- measures the body offset from the keep ranges;
- writes `scenes.json` (placement = `t0` + offset);
- copies compositions;
- shifts and thins SFX (≥ 0.75 s apart);
- shifts the chrome;
- copies the voice;
- patches the root;
- runs `motion_sync.py`.

Re-run it after any scene rebuild. Reference: `projects/ai-how-people-use/reel/make_versions.py`.

## 4. Hook craft
- Frame 0 of each version must already be busy, because the viewer decides in the first second.
- Each hook gets its own scene(s) that hand off cleanly to the first body scene.
- Snapshot both versions at 0.0 s, at the hook's key words, and across the hand-off.

## 5. Deliver both
`python pipeline/render_final.py <name> --part reel` and `--part reel_h2`. Name them clearly in `deliverables/`
(`…_main.mp4`, `…_hook2.mp4`) and say which hook each one opens with.
