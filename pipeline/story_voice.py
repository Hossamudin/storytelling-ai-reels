"""story_voice.py - build a narrated story voice track from a line-by-line plan (TTS + fetched Quran clips + pauses).

For script-only videos (no recorded voice), e.g. the "حكايات فطّوم" kids series. Every line is voiced on its own, so
the exact start/end of every line is known: scenes are timed from voice_timeline.json, no transcription needed.

Usage:
  python pipeline/story_voice.py <project> [--part ep] [--check] [--only L07]

<project>/voice_plan.json:
  {"voices": {"narrator": {"voice": "ballad", "instructions": "..."},
              "fatoom":   {"voice": "coral",  "instructions": "..."}},
   "model": "gpt-4o-mini-tts",
   "lines": [
     {"id": "L01", "who": "narrator", "text": "بسمِ اللهِ الرحمنِ الرحيم.", "gap": 0.8},
     {"id": "P01", "pause": 3.0},                                    # silence for the child to answer
     {"id": "Q01", "quran": "ghashiya_17_20", "gap": 1.0},           # clip from assets/quran (quran_fetch.py)
     ...]}
  gap = silence after the item (default 0.45 s). "lead" = silence before the very first item (default 0.6 s).

Output:
  assets/voice/tts/<id>_<hash>.wav    cached TTS takes (re-voiced only when text/voice/instructions change)
  assets/voice/story_voice.wav        48 kHz stereo track (speech normalised per line, Quran clips matched in level)
  voice_timeline.json                 [{"id","who","text","start","end"}] in seconds on the track
  --check: transcribes every TTS line (whisper-1) and prints a similarity score; < 0.8 = listen / re-voice.
"""
import argparse
import difflib
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

SR = 48000
TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟـ]")


def tts(text, voice, instructions, model, dst, key):
    body = json.dumps({"model": model, "voice": voice, "input": text, "instructions": instructions,
                       "response_format": "wav"}).encode()
    last = None
    for i in range(5):
        try:
            req = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=body,
                                         headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
            data = urllib.request.urlopen(req, timeout=120).read()
            raw = dst.with_suffix(".raw.wav")
            raw.write_bytes(data)
            # trim the model's leading/trailing silence, normalise speech level (-18 LUFS ~ comfortable narration)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                            "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
                            "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.12,areverse,"
                            "loudnorm=I=-18:TP=-2:LRA=11", "-ar", str(SR), "-ac", "2", str(dst)], check=True)
            raw.unlink()
            return
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:300]!r}"
            if e.code in (400, 401, 403):
                break
        except Exception as e:  # timeouts happen; retry
            last = repr(e)
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"TTS failed for {dst.name}: {last}")


def dur(p):
    return C.ffprobe_duration(p)


def norm(s):
    s = TASHKEEL.sub("", s)
    s = re.sub("[إأآٱ]", "ا", s).replace("ى", "ي").replace("ة", "ه")
    return re.sub(r"[^\w\s]", "", s).split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--part", default="ep")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", default=None, help="re-voice this line id even if cached")
    a = ap.parse_args()
    pp = C.project_path(a.project)
    plan = json.loads((pp / "voice_plan.json").read_text(encoding="utf-8"))
    key = C.get_key("OPENAI_API_KEY")
    if not key:
        raise SystemExit("OPENAI_API_KEY missing (config/api_keys.json or env)")
    model = plan.get("model", "gpt-4o-mini-tts")
    tdir = pp / "assets/voice/tts"
    tdir.mkdir(parents=True, exist_ok=True)
    qmeta = {}
    qj = pp / "assets/quran/quran.json"
    if qj.exists():
        qmeta = {i["id"]: i for i in json.loads(qj.read_text(encoding="utf-8"))["items"]}

    pieces, timeline, t = [], [], float(plan.get("lead", 0.6))
    pieces.append(("sil", t))
    for ln in plan["lines"]:
        gap = float(ln.get("gap", 0.45))
        if "pause" in ln:
            timeline.append({"id": ln["id"], "who": "pause", "start": round(t, 3), "end": round(t + ln["pause"], 3)})
            pieces.append(("sil", ln["pause"]))
            t += ln["pause"]
            continue
        if "quran" in ln:
            src = pp / qmeta[ln["quran"]]["audio"]["file"]
            # level-match the recitation to the narration (it stays untouched otherwise)
            dst = tdir / f"{ln['id']}_quran.wav"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af", "loudnorm=I=-19:TP=-2:LRA=11",
                            "-ar", str(SR), "-ac", "2", str(dst)], check=True)
            d = dur(dst)
            timeline.append({"id": ln["id"], "who": "quran", "quran": ln["quran"], "start": round(t, 3),
                             "end": round(t + d, 3), "text": qmeta[ln["quran"]]["text"]})
        else:
            v = plan["voices"][ln["who"]]
            h = hashlib.sha1(json.dumps([model, v, ln["text"]], ensure_ascii=False).encode()).hexdigest()[:10]
            dst = tdir / f"{ln['id']}_{h}.wav"
            if not dst.exists() or a.only == ln["id"]:
                for old in tdir.glob(f"{ln['id']}_*.wav"):
                    if old != dst and not old.name.endswith("_quran.wav"):
                        old.unlink()
                print(f"  voicing {ln['id']} ({ln['who']})")
                tts(ln["text"], v["voice"], v.get("instructions", ""), model, dst, key)
            d = dur(dst)
            timeline.append({"id": ln["id"], "who": ln["who"], "text": ln["text"], "start": round(t, 3),
                             "end": round(t + d, 3), "file": str(dst.relative_to(pp)).replace("\\", "/")})
        pieces.append(("file", dst))
        t += d
        pieces.append(("sil", gap))
        t += gap

    # concat via the concat demuxer on uniform 48k stereo PCM (sample exact, no re-encode artefacts)
    sil_dir = tdir / "_sil"
    sil_dir.mkdir(exist_ok=True)
    lst = []
    for kind, v in pieces:
        if kind == "sil":
            f = sil_dir / f"sil_{int(round(v * 1000))}.wav"
            if not f.exists():
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                                f"anullsrc=r={SR}:cl=stereo", "-t", f"{v:.3f}", "-c:a", "pcm_s16le", str(f)], check=True)
            lst.append(f)
        else:
            lst.append(v)
    lf = tdir / "_concat.txt"
    lf.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in lst), encoding="utf-8")
    out = pp / "assets/voice/story_voice.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lf),
                    "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(out)], check=True)
    (pp / "voice_timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
    # keep every scaffolded part's copy in sync (new_motion_video.py copies the voice once)
    import shutil
    for part_copy in pp.glob("*/assets/voice/story_voice.wav"):
        shutil.copy2(out, part_copy)
        print(f"   synced {part_copy.relative_to(pp)}")
    print(f"-> {out}  ({dur(out):.2f} s, {len(timeline)} items)")

    if a.check:
        bad = 0
        for it in timeline:
            if it["who"] in ("pause", "quran"):
                continue
            r = subprocess.run(["curl", "-s", "https://api.openai.com/v1/audio/transcriptions", "-H",
                                "Authorization: Bearer " + key, "-F", "model=whisper-1", "-F", "language=ar",
                                "-F", "file=@" + str(pp / it["file"])], capture_output=True)
            heard = json.loads(r.stdout.decode("utf-8", "replace")).get("text", "")
            score = difflib.SequenceMatcher(None, norm(it["text"]), norm(heard)).ratio()
            flag = "  <-- listen" if score < 0.8 else ""
            bad += bool(flag)
            print(f"  {it['id']:<5} {score:.2f}  {heard}{flag}")
        print(f"check: {bad} line(s) to listen to")


if __name__ == "__main__":
    main()
