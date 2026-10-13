# Engine command reference (run from the studio folder)

`<skill>/scripts/…` = files inside this skill. `engine/pipeline/…` = the studio's installed engine (same code,
copied by `setup_studio.py init`). Every script prints a "Next:" hint.

## Setup & housekeeping
| Command | What |
|---|---|
| `python <skill>/scripts/env_check.py [--json]` | machine report: hardware, tools, packages, keys (presence), what to install |
| `python <skill>/scripts/setup_studio.py status \| init \| brand \| keys` | studio state / create-upgrade / apply brand.json / key presence |
| `python <skill>/scripts/vendor_lib.py three\|lottie <part dir>` | copy Three.js or lottie-web into a part's `assets/js/` (no CDN at render) |
| `npx hyperframes doctor` | HyperFrames' own dependency check (Chrome, ffmpeg, optional models) |

## Voice & transcript
| Command | What |
|---|---|
| `engine/pipeline/new_project.py <name>` | project folder (input/, assets/, transcript/, renders/) |
| `engine/pipeline/clean_audio.py <name> [--input f]` | cleanup chain, timing preserved → `assets/voice/voiceover_clean.wav` |
| `engine/pipeline/transcribe.py <name> [--provider auto\|openai_whisper\|local]` | word timings → `transcript/transcript.json/.md` |
| `engine/pipeline/find_retakes.py <name>` | retakes / false starts / fillers → `input/edit.proposed.json` + `review/cuts.html` (OpenAI key) |
| `engine/pipeline/voice_edit.py <name> [--verify]` | apply `input/edit.json` → parts `<part>.wav`, `<part>_words.json`, `<part>_phrases.txt` |

## Motion composition
| Command | What |
|---|---|
| `engine/pipeline/new_motion_video.py <name> --part P --voice <wav> --aspect 16:9\|9:16\|1:1\|4:5 --preset light\|dark [--series S] [--no-chrome]` | scaffold a HyperFrames part from the kit (+ brand) |
| `engine/pipeline/motion_sync.py <name> --part P` | regenerate hosts/audio/chrome/wipes/steps/duration from scenes/cues/chrome.json |
| `engine/pipeline/sfx_levels.py --dir <part>/assets/sfx` | measure SFX loudness → per-file gains (`levels.json`) |
| `engine/pipeline/web_capture.py <url> --out <dir> [--full --iframes --imgs --selector css]` | real-page evidence PNGs + page.txt |

## Screen recordings
| Command | What |
|---|---|
| `engine/pipeline/screen_edit.py <name> [--preview]` | `input/screen_edit.json` → `assets/screen/edited.mp4/.wav`, `edit_map.json`, `words.json` |
| `engine/pipeline/screen_annot.py <name> --part P [--times t…]` | `input/annotations.json` (source time/pixels) → `annot.js` + cutaway windows |

## Talking head
| Command | What |
|---|---|
| `engine/pipeline/th_cut.py <name> --part P [--src input/rawreel.mov]` | camera cut on the voice edit's keep ranges + `<part>_th_seams.json` |
| `npx hyperframes remove-background <in> -o <out.webm\|.png>` | person/logo matte (slow on CPU: start early, in the background) |
| `engine/pipeline/th_layer.py <name> --part P` | presenter layer from `th.json` (+ `th_behind.html`, `th_front.html`, `th_front.js`) |

## QA, render, deliver
| Command | What |
|---|---|
| `npx hyperframes check` / `snapshot --at t1,t2,…` / `preview --background` | (inside the part) validate / stills / Studio URL |
| `engine/pipeline/preflight.py <name> --part P` | render-readiness gate |
| `engine/pipeline/render_final.py <name> --part P [--quality draft\|delivery]` | preflight → render → verify → master → chapters → `deliverables/` |
| `engine/pipeline/master_audio.py <mp4> [--out f]` | −14 LUFS / −1.2 dBTP two-pass loudnorm |
| `engine/pipeline/chapters.py <name> --part P` | YouTube chapters from chrome.json sections |

## Library
`engine/pipeline/lib.py find | add | import | use | harvest | describe | index | seed` — see `library.md`.
