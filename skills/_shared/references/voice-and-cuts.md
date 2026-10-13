# Voice, transcript and cuts — the foundation of every narrated video

Timing comes from the voice. Get this stage right and everything downstream syncs.

## Pipeline (run from the studio folder)

```bash
python engine/pipeline/new_project.py <name>                    # then copy the voice/camera file into projects/<name>/input/
python engine/pipeline/clean_audio.py <name> --no-silence-cut   # ffmpeg cleanup (HPF, denoise, de-ess, compress, loudnorm) — timing preserved
python engine/pipeline/transcribe.py <name>                     # auto: OpenAI whisper-1 if key, else local faster-whisper
python engine/pipeline/find_retakes.py <name>                   # retakes / false starts / fillers -> edit.proposed.json + review/cuts.html
                                                                #   (OpenAI key: verbatim model + LLM editor; no key: FREE local mode, rules only)
#  creator reviews review/cuts.html (listen before/after, tick, export) -> input/edit.json
python engine/pipeline/voice_edit.py <name> --verify            # parts: assets/voice/<part>.wav + transcript/<part>_words.json + _phrases.txt
```
Input file naming: the voice is found by preference `voice*` / `voiceover*` / `rawreel*`, then any audio, never
`screen*`/`clip*`/`broll*`. Check new inputs with `ffprobe` at intake ("moov atom not found" = interrupted recording).
Several voice notes for one video/series → concatenate with 2 s gaps into one input, then split with `parts`.

## `input/edit.json`

```json
{
  "parts": [{"name": "intro", "from": 0, "to": 78.06}, {"name": "outro", "from": 78.06, "to": 99.42}],
  "cuts": [[12.40, 15.72, "repeated phrase"], [45.75, 49.72, "false start"]],
  "retime": [{"window": [14.3, 16.6], "words": [["word", 15.84, 16.10], ["word2", 16.10, 16.35]]}],
  "fix": {"misheard": "right", "vibe": "vibe"},
  "max_pause": 0.38, "keep_pause": 0.24, "silence_db": -38
}
```
- `fix` can also be a list of phrase fixes `{"from": "two words", "to": "new words", "at": 185.0}` — the way to
  fix names every model mishears (brand names, the creator's own name).
- Cut edges snap to the quietest 10 ms; keep ranges sit on the 1/30 s frame grid (so a camera cut stays in sync);
  10–12 ms fades on every seam (no clicks).
- `--verify` re-transcribes each edited part and prints a diff: proof that no word is doubled or clipped.

**Check the spoken language at intake** (listen to 5 s, or read the first transcript lines). A wrong
`language` makes Whisper *translate* instead of transcribe; the local provider detects and warns. Spoken and
on-screen languages can differ (`language` vs `text_language` in config).

## Hard-won rules

| Rule | Why |
|---|---|
| Never look for retakes in the whisper transcript | whisper-1 "cleans" speech: drops repeats, merges two takes into one span. Use `find_retakes.py` (verbatim chunks) or listen |
| Keep the LATER, complete take | The second attempt is almost always the better one — even if the cut is long (34 s once) |
| Never pass a `prompt` hint to Whisper | A hint that matches the opening makes Whisper skip it |
| Word timings from ≤ 10 s pause-bounded windows | Long-file whisper loops on early retakes and skips stretches (once: 103 words for 162 s, one "word" lasting 23 s) |
| Gemini free tier is not a transcription engine | 503/429, truncated JSON, fake uniform 0.5 s timings |
| Compare segment gaps with `silencedetect` | Whisper can silently skip a 3 s sentence with energy in it; transcribe that gap separately and add a `retime` |
| Trailing "thanks for watching / subscribe" over silence | Classic hallucination — check the last segment against silencedetect |
| Loud non-speech at the start transcribed as words | If two models disagree on a short span → treat it as noise, cut it, flag it |
| Back up `transcript/` before a verify run | A verify pass on another file used to overwrite `transcript.json` |
| Local model quality | `small` misspells names and dialect; use `medium`/`large-v3` on a GPU, or the OpenAI path, for Arabic and proper nouns |

## Without an OpenAI key (free path)

`find_retakes.py` runs in FREE local mode: faster-whisper transcribes each pause-bounded chunk separately (so a
repeated take can't be merged away), deterministic rules propose repeats, stutters, fillers and noise, and the same
`review/cuts.html` page is built. It cannot catch *paraphrased* restarts (that's the LLM pass) — listen around long
pauses for those. `voice_edit.py --verify` needs the key: without it, re-run `transcribe.py --provider local --input
assets/voice/<part>.wav` on the edited part and read it end to end. `voice_edit.py` prints any word that fell out of
the keep ranges without being cut — act on that warning (a `retime` entry, or a lower `max_pause`).

## Model downloads (tell the creator before the first run)

faster-whisper downloads its model on first use: `small` ≈ 0.5 GB, `medium` ≈ 1.5 GB, `large-v3` ≈ 3 GB. On a slow
connection start with `small` (fast, misspells dialect and names) and download the bigger one in the background
for next time; an interrupted download leaves a broken cache — delete it from `~/.cache/huggingface/hub/` and retry.

## Script only, no voice

Options to offer: (1) the creator records it (best — their voice is their brand; give recording tips),
(2) local TTS `npx hyperframes tts` (English/European languages), (3) a paid TTS/voice clone (approval).
Then continue as if it were a voice file.

## Recording tips to give (one at a time, when relevant)

Quiet room, phone/mic 15–20 cm away, Do-Not-Disturb on · pause 2 s between sections and after a mistake, then
repeat the whole sentence (clean cut points) · say names slowly once · record a 5-second silence at the start
(noise profile) · stop the recorder cleanly.
