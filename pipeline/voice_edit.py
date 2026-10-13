"""Editorial voice cut: remove repeats / false starts / dead air, split into parts, remap words.

Usage:
  python pipeline/voice_edit.py <name> [--verify]

Reads:
  assets/voice/voiceover_clean.wav            (clean_audio.py --no-silence-cut)
  transcript/transcript.json                  (transcribe.py, openai_whisper word timings)
  input/edit.json                             (your / the agent's edit decisions), e.g.
  {
    "parts": [{"name": "intro", "from": 0, "to": 78.06}, {"name": "outro", "from": 78.06, "to": 99.42}],
    "cuts": [[12.40, 15.72, "repeated 'علشان كده'"], [45.75, 49.72, "false start"]],
    (a part may carry its own "cuts" too — added to the global ones. Two recorded hooks -> two parts over the
     same range: {"name": "voice", "from": 0, "to": 233, "cuts": [[hook2]]} = MAIN, and
     {"name": "voice_h2", "from": 0, "to": 233, "cuts": [[hook1]]} = 2nd version; see prompts/two_hooks.md)
    "retime": [{"window": [14.3, 16.6], "words": [["علشان", 15.84, 16.10], ["كده", 16.10, 16.35]]}],
    "fix": {"كررت": "قررت", "الفايب": "vibe", "أوتوميشن": "automation"},
    "max_pause": 0.38, "keep_pause": 0.24, "silence_db": -38
  }
Writes per part:
  assets/voice/<part>.wav, transcript/<part>_words.json,
  transcript/<part>_phrases.txt  ("start-end | text" lines — the master-prompt input format)

Start from `python pipeline/find_retakes.py <name>` -> input/edit.proposed.json (+ review/cuts.html):
verbatim chunk transcription finds retakes / false starts automatically, and
transcript/transcript_verbatim.json (whisper timings + verbatim spelling) is used here when present.
"fix" may be a dict (whole-word, everywhere; "" deletes the word) or a list of
{"from": "two words", "to": "new words", "at": 185.0?} phrase fixes (optional "at" = only near that time).
Cut edges are snapped to the quietest 10 ms within +-snap s (default 0.12); keep ranges sit on the
1/fps frame grid (default 30) so th_cut.py stays in sync with the voice; a word is dropped when its
midpoint falls in a cut.

Finding cut points by hand: Whisper merges repeated takes into one span. Look at silencedetect gaps and
transcribe <=1.5 s excerpts (gpt-4o-transcribe) to find where a retake really starts, then
add "retime" entries for the kept take. --verify re-transcribes each output part (OpenAI) so you
can confirm there are no doubled or clipped words.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def silences(src, th, d=0.12):
    r = C.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", f"silencedetect=noise={th}dB:d={d}", "-f", "null", "-"])
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(st, en))


def keep_ranges(lo, hi, manual, sil, max_pause, keep_pause, lead=0.15, tail=0.6):
    cuts = [(max(lo, s), min(hi, e)) for s, e, *_ in manual if e > lo and s < hi]
    for s, e in sil:
        s, e = max(s, lo), min(e, hi)
        if e - s <= max_pause:
            continue
        if s <= lo + 0.01:
            cuts.append((lo, e - lead))
        elif e >= hi - 0.01:
            cuts.append((s + tail, hi))
        else:
            cuts.append((s + keep_pause / 2, e - keep_pause / 2))
    cuts.sort()
    merged = []
    for s, e in cuts:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    keep, t = [], lo
    for s, e in merged:
        if s > t + 0.02:
            keep.append((t, s))
        t = max(t, e)
    if t < hi - 0.02:
        keep.append((t, hi))
    return keep


def rms_strip(src, hop=0.01):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = int(16000 * hop)
    x = x[: len(x) // n * n].reshape(-1, n)
    return np.sqrt((x ** 2).mean(axis=1) + 1e-12), hop


def snap(t, strip, win):
    import numpy as np
    env, hop = strip
    i0, i1 = max(0, int((t - win) / hop)), min(len(env), int((t + win) / hop) + 1)
    if i1 <= i0:
        return t
    return round((i0 + int(np.argmin(env[i0:i1]))) * hop + hop / 2, 3)


def on_grid(keep, fps):
    g = [(round(s * fps) / fps, round(e * fps) / fps) for s, e in keep]
    return [(round(s, 4), round(e, 4)) for s, e in g if e - s >= 1 / fps]


def apply_fixes(words, fix):
    if isinstance(fix, dict):
        fix = [{"from": k, "to": v} for k, v in fix.items()]
    for f in fix:
        src_t, dst_t = f["from"].split(), f["to"].split()
        n, i = len(src_t), 0
        while i + n <= len(words):
            seg = words[i:i + n]
            if [w["w"].strip("،,.؟?!") for w in seg] == [x.strip("،,.؟?!") for x in src_t] and ("at" not in f or abs(seg[0]["s"] - f["at"]) < 3):
                tail = seg[-1]["w"][len(seg[-1]["w"].rstrip("،,.؟?!")):]
                s0, e0 = seg[0]["s"], seg[-1]["e"]
                step = (e0 - s0) / max(1, len(dst_t))
                new = [{"w": t + (tail if k == len(dst_t) - 1 and t == t.rstrip("،,.؟?!") else ""), "s": round(s0 + k * step, 3), "e": round(s0 + (k + 1) * step, 3)}
                       for k, t in enumerate(dst_t)]
                words[i:i + n] = new
                i += len(new)  # empty "to" deletes: list shrinks, so i stays
            else:
                i += 1
    return [w for w in words if w["w"].strip()]


def remap(t, keep):
    acc = 0.0
    for s, e in keep:
        if t < s:
            return acc
        if t <= e:
            return acc + (t - s)
        acc += e - s
    return acc


def phrases(words, gap=0.35, max_words=9):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_punct = w["w"].endswith(("،", ".", "؟", "?", "!"))
        if not nxt or nxt["s"] - w["e"] > gap or end_punct or len(cur) >= max_words:
            out.append(f"{cur[0]['s']:.2f}-{cur[-1]['e']:.2f} | " + " ".join(x["w"] for x in cur))
            cur = []
    return out


def verify_and_retime(pp, part, dest, ws, total, fix):
    """Transcribe the EDITED part (no retakes left to confuse whisper): whisper-1 word timings +
    verbatim spelling (retakes.model) -> the part's caption words. Prints a diff against the plan."""
    import difflib
    import shutil
    import find_retakes as FR
    import transcribe as T
    cfg = C.load_config()
    key = C.get_key("OPENAI_API_KEY")
    vd = pp / "assets/voice/_verify"
    vd.mkdir(parents=True, exist_ok=True)
    tmp = vd / f"{part}.m4a"
    C.ffmpeg(["-i", str(dest), "-ar", "16000", "-ac", "1", "-c:a", "aac", "-b:a", "48k", str(tmp)])
    heard = FR.transcribe(tmp, key, cfg.get("retakes", {}).get("model", "gpt-transcribe"), "ar")
    wwords, empty = FR.window_word_timings(dest, FR.speech_chunks(dest, total), key, vd, tag=part)
    shutil.rmtree(vd, ignore_errors=True)
    print(f"  verify ({part}): {heard}")
    nz = lambda t: [x for x in re.sub(r"[^\w\s%]", " ", t.lower().replace("الـ", "ال")).split() if x]
    # spelling reference = the planned words (reviewed, fixed) + whatever the edit says that the plan lacked
    pt, ht = [w["w"] for w in ws], heard.split()
    sm = difflib.SequenceMatcher(None, [FR.norm(x) for x in pt], [FR.norm(x) for x in ht], autojunk=False)
    ref = []  # planned spelling where it matches what the edit says; heard words where the plan is missing or wrong
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            ref += pt[i1:i2]
        elif op == "insert":
            ref += ht[j1:j2]
        elif op == "replace":
            close = i2 - i1 == j2 - j1 and all(difflib.SequenceMatcher(None, FR.norm(x), FR.norm(y)).ratio() >= 0.5
                                                 for x, y in zip(pt[i1:i2], ht[j1:j2]))
            ref += pt[i1:i2] if close else ht[j1:j2]
        # delete: planned words the edit doesn't contain -> dropped
    new = apply_fixes(FR.respell(wwords, [], " ".join(ref), keep_unmatched=False), fix)
    new = [{**w, "s": round(min(w["s"], total), 3), "e": round(min(w["e"], total), 3)} for w in new]
    exp, got = nz(" ".join(w["w"] for w in ws)), nz(heard)
    sm = difflib.SequenceMatcher(None, exp, got, autojunk=False)
    print(f"  verify similarity {sm.ratio():.3f} (planned kept words vs what the edit sounds like)")
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal" and (i2 - i1 > 1 or j2 - j1 > 1):
            print(f"    {op}: planned '{' '.join(exp[i1:i2])}' | heard '{' '.join(got[j1:j2])}'")
    print(f"  caption words re-timed on the edited audio (pause-bounded whisper windows): {len(ws)} planned -> {len(new)} words"
          + (f", {len(empty)} empty window(s)" if empty else ""))
    return new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    pp = C.project_path(args.name)
    src = pp / "assets/voice/voiceover_clean.wav"
    spec = json.loads((pp / "input/edit.json").read_text(encoding="utf-8"))
    trp = pp / "transcript/transcript_verbatim.json"
    trp = trp if trp.exists() and spec.get("verbatim", True) else pp / "transcript/transcript.json"
    tr = json.loads(trp.read_text(encoding="utf-8"))
    print(f"words from {trp.name}")
    words = [dict(w) for s in tr["segments"] for w in s["words"]]
    words = apply_fixes(words, spec.get("fix", {}))
    for rt in spec.get("retime", []):
        a, b = rt["window"]
        words = [w for w in words if not (a <= w["s"] < b)] + [{"w": t, "s": s, "e": e} for t, s, e in rt["words"]]
    words.sort(key=lambda w: w["s"])
    words = [w for i, w in enumerate(words) if i == 0 or (w["s"], w["w"]) != (words[i - 1]["s"], words[i - 1]["w"])]
    dur = C.ffprobe_duration(src)
    parts = spec.get("parts") or [{"name": "voice", "from": 0, "to": dur}]
    strip = rms_strip(src)
    sw, fps = spec.get("snap", 0.12), spec.get("fps", 30)
    manual = [[snap(c[0], strip, sw), snap(c[1], strip, sw), *c[2:]] for c in spec.get("cuts", [])] if sw else spec.get("cuts", [])
    for c0, c1 in zip(spec.get("cuts", []), manual):
        if abs(c0[0] - c1[0]) > 0.02 or abs(c0[1] - c1[1]) > 0.02:
            print(f"  snapped cut {c0[0]:.2f}-{c0[1]:.2f} -> {c1[0]:.2f}-{c1[1]:.2f}")
    sil = silences(src, spec.get("silence_db", -38))
    for part in parts:
        lo, hi = part["from"], min(part["to"], dur)
        pcuts = [[snap(c[0], strip, sw), snap(c[1], strip, sw), *c[2:]] for c in part.get("cuts", [])] if sw else part.get("cuts", [])
        pm = sorted(manual + pcuts, key=lambda c: c[0])
        keep = on_grid(keep_ranges(lo, hi, pm, sil, spec.get("max_pause", 0.38), spec.get("keep_pause", 0.24)), fps)
        fc = ";".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,"
                      f"afade=t=out:st={max(0, e - s - 0.012):.3f}:d=0.012[a{i}]" for i, (s, e) in enumerate(keep))
        fc += ";" + "".join(f"[a{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[out]"
        dest = pp / f"assets/voice/{part['name']}.wav"
        C.ffmpeg(["-i", str(src), "-filter_complex", fc, "-map", "[out]", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(dest)])
        ws = [{"w": w["w"], "s": round(remap(w["s"], keep), 3), "e": round(remap(w["e"], keep), 3)}
              for w in words if lo <= w["s"] < hi and not any(s <= (w["s"] + w["e"]) / 2 <= e for s, e, *_ in pm)
              and any(s - 0.05 <= (w["s"] + w["e"]) / 2 <= e + 0.05 for s, e in keep)]
        total = sum(e - s for s, e in keep)
        if args.verify:
            ws = verify_and_retime(pp, part["name"], dest, ws, total, spec.get("fix", {}))
        (pp / f"transcript/{part['name']}_words.json").write_text(json.dumps(
            {"duration": round(total, 3), "keep": [[round(s, 3), round(e, 3)] for s, e in keep], "words": ws},
            ensure_ascii=False, indent=1), encoding="utf-8")
        (pp / f"transcript/{part['name']}_phrases.txt").write_text("\n".join(phrases(ws)), encoding="utf-8")
        print(f"{part['name']}: {hi - lo:.2f}s -> {total:.2f}s ({len(keep)} ranges, {len(ws)} words)")
    C.log(args.name, f"voice_edit: {len(parts)} part(s), {len(manual)} manual cuts")


if __name__ == "__main__":
    main()
