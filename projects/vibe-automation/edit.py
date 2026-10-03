"""Voice edit for vibe-automation: cut repeats/false starts, tighten pauses, split intro/outro,
remap word timings. Source: assets/voice/voiceover_clean.wav (intro 0-78.06 + outro 78.06-99.42).
Outputs: assets/voice/{intro,outro}.wav + transcript/{intro,outro}_words.json
"""
import json, re, subprocess
from pathlib import Path

P = Path(__file__).resolve().parent
SRC = P / "assets/voice/voiceover_clean.wav"
SPLIT = 78.06

# Manual editorial cuts (source seconds)
MANUAL = [
    (12.40, 15.72),   # repeated "علشان كده" (first take 14.35-14.96)
    (45.75, 49.72),   # false start "فهنا قررت إزاي أستخدم AI؟"
    (89.62, 91.02),   # false start "وطبعاً لو عايز تستـ"
]
MAX_PAUSE, KEEP_PAUSE = 0.38, 0.24

# Word timings: whisper-1 (no prompt covers 0-6s; prompted run is cleaner elsewhere)
np_ = json.load(open(P / "transcript/openai_whisper-1_noprompt.json", encoding="utf-8"))["words"]
pr_ = json.load(open(P / "transcript/openai_whisper-1.json", encoding="utf-8"))["words"]
words = [w for w in np_ if w["start"] < 5.84] + [w for w in pr_ if w["start"] >= 5.84]

# Spelling fixes against the Gemini verbatim reference (Egyptian dialect + Latin keywords)
FIX = {"انا": "أنا", "كررت": "قررت", "ابدأ": "أبدأ", "اغلبنا": "أغلبنا", "ويصرعها": "ويسرعها",
       "وعنعرف": "وهنعرف", "اللقايق": "الـAI", "اتأكدكم": "اتأكد", "واشتراكم": "تكون مشترك",
       "وفعل": "ومفعّل", "أفاتكم": "أفادكم", "قراءتكم": "آرائكم", "ولا": None,
       "يفيدوك": "هيفيدوك", "لك": "ليك", "قلنا": "قولنا", "AI؟": "AI", "يساعدني؟": "يساعدني؟"}
out = []
for w in words:
    t = w["word"]
    if t == "ولا" and w["start"] > 90:
        t = "واللي"
    elif t in FIX and FIX[t]:
        t = FIX[t]
    if t == "الفايب":
        t = "vibe"
    if t == "أوتوميشن":
        t = "automation"
    if t == "AI":
        t = "الـAI"
    out.append({"w": t, "s": w["start"], "e": w["end"]})
words = out

# Whisper merged the repeated takes; re-time the kept retakes from the energy map.
PATCH = {  # (source window) -> replacement words
    (14.3, 16.6): [("علشان", 15.84, 16.10), ("كده", 16.10, 16.35), ("سألت", 16.35, 16.66)],
    (89.8, 91.9): [("وطبعاً", 91.10, 91.40), ("لو", 91.40, 91.52), ("عايز", 91.52, 91.75),
                    ("تعرف", 91.75, 91.96)],
}
for (a, b), rep in PATCH.items():
    words = [w for w in words if not (a <= w["s"] < b)] + [{"w": t, "s": s, "e": e} for t, s, e in rep]
words.sort(key=lambda w: w["s"])


def silences(th=-38, d=0.12):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(SRC), "-af",
                        f"silencedetect=noise={th}dB:d={d}", "-f", "null", "-"],
                       capture_output=True, text=True)
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(st, en))


def build(lo, hi, lead=0.15, tail=0.6):
    cuts = [(max(lo, s), min(hi, e)) for s, e in MANUAL if e > lo and s < hi]
    for s, e in silences():
        s, e = max(s, lo), min(e, hi)
        if e - s <= MAX_PAUSE:
            continue
        if s <= lo + 0.01:
            cuts.append((lo, e - lead)); continue
        if e >= hi - 0.01:
            cuts.append((s + tail, hi)); continue
        cuts.append((s + KEEP_PAUSE / 2, e - KEEP_PAUSE / 2))
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


def remap(t, keep):
    acc = 0.0
    for s, e in keep:
        if t < s:
            return acc
        if t <= e:
            return acc + (t - s)
        acc += e - s
    return acc


def render(name, lo, hi):
    keep = build(lo, hi)
    parts = [f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,"
             f"afade=t=in:d=0.012,afade=t=out:st={e - s - 0.012:.3f}:d=0.012[a{i}]"
             for i, (s, e) in enumerate(keep)]
    fc = ";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(len(keep))) + \
        f"concat=n={len(keep)}:v=0:a=1[out]"
    dest = P / f"assets/voice/{name}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-filter_complex", fc,
                    "-map", "[out]", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(dest)], check=True)
    ws = []
    for w in words:
        if not (lo <= w["s"] < hi):
            continue
        if any(s <= w["s"] and w["e"] <= e + 0.05 for s, e in MANUAL):
            continue  # word inside an editorial cut
        ws.append({"w": w["w"], "s": round(remap(w["s"], keep), 3), "e": round(remap(w["e"], keep), 3)})
    dur = sum(e - s for s, e in keep)
    (P / f"transcript/{name}_words.json").write_text(json.dumps(
        {"duration": round(dur, 3), "keep": [[round(s, 3), round(e, 3)] for s, e in keep], "words": ws},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{name}: {hi - lo:.2f}s -> {dur:.2f}s, {len(keep)} kept ranges, {len(ws)} words")


render("intro", 0.0, SPLIT)
render("outro", SPLIT, 99.42)
