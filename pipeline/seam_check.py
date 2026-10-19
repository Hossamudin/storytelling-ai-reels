"""Seam QA for a merged multi-part video: repeated openers / closers across part boundaries.

Usage:
  python pipeline/seam_check.py <merged.mp4> <chapters.txt | offsets> [--window 8] [--refresh]
    chapters.txt  "mm:ss title" lines (merge script output; the 00:00 line is skipped)
    offsets       comma list of seam times in seconds, e.g. 55.2,113.4  (or a .json list)

Why (LESSONS §23): each part is cut by its own agent, so nobody listens across a boundary. Part 02 ended
"دلوقتي بقى تعالوا نبدأ" and part 03 opened "وقبل ما نبدأ نبني…" — a repeat the review had to catch.
This script verbatim-transcribes ±window s around every seam (split at the pause nearest the seam, so a
word never lands on the wrong side), prints the end of part N and the start of part N+1 in order, and flags:
  - shared content words between the closer and the opener («نبدأ» / «نبدأ»)
  - the same 2-token opener, or the closer's words said again in the opener (find_retakes rules)
  - a goodbye / CTA line at a middle seam (one CTA per video; the intro's subscribe ask is fine)
Writes <merged>_seams.json (cached transcripts + flags) and prints a report. Cut the weaker of the two lines.
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
from find_retakes import FILLERS, silences, tok_eq, tok_like, toks, transcribe  # noqa: E402

# words too common to signal a repeat on their own
STOP = FILLERS | {"اللي", "دلوقتي", "عشان", "علشان", "كده", "كمان", "بقي", "حاجه", "حاجات", "يعني", "انا", "احنا", "انت",
                  "انتو", "هو", "هي", "هما", "هم", "ده", "دي", "دول", "في", "من", "علي", "على", "الي", "عن", "مع", "لو",
                  "ان", "انه", "او", "ولا", "لا", "مش", "ما", "بس", "تمام", "طيب", "خلاص", "بتاع", "بتاعي", "بتاعنا",
                  "بتاعت", "هنا", "هناك", "زي", "كل", "اول", "تاني", "جدا", "فعلا", "بصراحه", "مثلا", "برضه", "شويه", "the", "a", "to", "and", "of", "is"}
CTA = re.compile(r"اشترك|لايك|شير|الجرس|الكومنت|كومنتات|فيدباك|نشوفكم|اشوفكم|سلام عليكم|في الفيديو الجاي|الحلقة الجاية|subscribe", re.I)


def parse_seams(arg):
    p = Path(arg)
    if p.exists() and p.suffix == ".json":
        return [float(x) for x in json.loads(p.read_text(encoding="utf-8"))]
    if p.exists():
        out = []
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)\s*(.*)", line)
            if m:
                h, mm, ss, title = m.groups()
                out.append((int(h or 0) * 3600 + int(mm) * 60 + float(ss), title.strip()))
        return out
    return [float(x) for x in arg.split(",") if x.strip()]


def content(T):
    return [t for t in T if len(t) >= 3 and t not in STOP and re.sub(r"^[وف]", "", t) not in STOP]


def sentences(text):
    return [s for s in (x.strip() for x in re.split(r"(?<=[.؟?!…])\s+", text)) if toks(s)]


def judge(before, after, first):
    """Flags for one seam. before/after = verbatim text ending at / starting from the seam."""
    flags = []
    bs, as_ = sentences(before), sentences(after)
    closer = " ".join(bs[-2:]) if bs else ""
    opener = " ".join(as_[:2]) if as_ else ""
    # only the words right at the boundary: the last clause's tail and the next part's first clause head
    tail, head = (toks(bs[-1])[-5:] if bs else []), (toks(as_[0])[:6] if as_ else [])
    shared = sorted({b for b in content(tail) for a in content(head) if tok_like(b, a)})
    if shared:
        flags.append(f"closer and opener share {', '.join(shared)} — repeated line across the seam?")
    if bs and as_:
        L, F = toks(bs[-1]), toks(as_[0])
        if len(L) >= 2 and len(F) >= 2 and tok_eq(L[0], F[0]) and tok_eq(L[1], F[1]):
            flags.append("same 2-word opener on both sides of the seam")
        if len(L) >= 3 and sum(any(tok_like(t, f) for f in F[:len(L) + 4]) for t in L) / len(L) >= 0.8:
            flags.append("the last line before the seam is said again after it")
    if not first and CTA.search(closer):  # every closer here ends a part that is not the last one
        flags.append("goodbye / CTA line before the last part — one CTA per video")
    return flags, closer, opener


def split_at_pause(src, t, win, th=-38):
    """Seam time nearest pause within ±1 s (chapters are rounded to whole seconds)."""
    lo = max(0.0, t - win)
    best, bd = t, 1.01
    for s, e in silences(src, th, 0.12):
        if e < lo or s > t + win:
            continue
        mid = (max(s, lo) + e) / 2
        if abs(mid - t) < bd:
            best, bd = mid, abs(mid - t)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("merged")
    ap.add_argument("seams", help="chapters .txt, offsets .json, or comma list of seconds")
    ap.add_argument("--window", type=float, default=8.0)
    ap.add_argument("--refresh", action="store_true", help="re-transcribe cached windows")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    src = Path(a.merged)
    dur = C.ffprobe_duration(src)
    seams = [s if isinstance(s, tuple) else (s, "") for s in parse_seams(a.seams)]
    seams = [(t, title) for t, title in seams if 1.0 < t < dur - 1.0]
    if not seams:
        sys.exit("no seams inside the video (chapters file / offsets?)")
    cfg = C.load_config()
    rc = {"model": "gpt-transcribe", "language": "ar", **cfg.get("retakes", {})}
    key = C.get_key("OPENAI_API_KEY")
    out = src.with_name(src.stem + "_seams.json")
    cache = {} if a.refresh or not out.exists() else {
        (s["t"], s["model"]): s for s in json.loads(out.read_text(encoding="utf-8")).get("seams", [])}
    tmp = Path(tempfile.mkdtemp(prefix="seams_"))

    res = []
    for k, (t, title) in enumerate(seams):
        hit = cache.get((round(t, 3), rc["model"]))
        if hit:
            before, after, cut = hit["before"], hit["after"], hit["split"]
        else:
            lo, hi = max(0.0, t - a.window), min(dur, t + a.window)
            win = tmp / f"s{k:02d}.wav"
            C.ffmpeg(["-ss", f"{lo:.3f}", "-to", f"{hi:.3f}", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", str(win)])
            cut = round(lo + split_at_pause(win, t - lo, a.window), 3)
            pb, pa = tmp / f"s{k:02d}_before.m4a", tmp / f"s{k:02d}_after.m4a"
            for p, x, y in ((pb, lo, cut), (pa, cut, hi)):
                C.ffmpeg(["-ss", f"{x:.3f}", "-to", f"{y:.3f}", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000",
                          "-c:a", "aac", "-b:a", "64k", str(p)])
            before, after = transcribe(pb, key, rc["model"], rc["language"]), transcribe(pa, key, rc["model"], rc["language"])
        flags, closer, opener = judge(before, after, k == 0)
        res.append({"t": round(t, 3), "split": cut, "title": title, "model": rc["model"], "before": before, "after": after,
                    "closer": closer, "opener": opener, "flags": flags})
    out.write_text(json.dumps({"video": src.name, "window": a.window, "seams": res}, ensure_ascii=False, indent=1), encoding="utf-8")

    n = 0
    for k, s in enumerate(res):
        m = int(s["t"] // 60)
        print(f"\n[{k + 1}] seam {m:02d}:{s['t'] - 60 * m:05.2f}  → {s['title']}")
        print(f"   end of part : …{s['closer']}")
        print(f"   next part   : {s['opener']}…")
        for f in s["flags"]:
            print(f"   !! {f}")
        n += bool(s["flags"])
    print(f"\n{n}/{len(res)} seams flagged -> {out}\nListen to each flagged seam and cut the weaker line in that PART's edit, then re-merge.")


if __name__ == "__main__":
    main()
