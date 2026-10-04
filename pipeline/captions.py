"""04b - Build keyword-aware caption chunks from the transcript.

Usage: python pipeline/captions.py <name> [--style punch|minimal|karaoke] [--max-words 4]

Arabic words render plain (white); English keywords get brand-color pop styling.
Output: transcript/captions.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

LATIN_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9'.+\-]*$")
PUNCT_BREAK = re.compile(r"[،,.!?؟:;]$")


def is_keyword(word, extra):
    w = word.strip("«»\"'()[]{}،,.!?؟:;")
    if w.lower() in extra:  # extra holds lowercased storyboard caption_keywords
        return True
    return bool(LATIN_TOKEN.match(w)) and len(w) >= 2 and not w.isdigit()


def build_chunks(transcript, extra_keywords, max_words, break_gap):
    chunks = []
    current = []

    def flush():
        nonlocal current
        if current:
            start = current[0]["s"]
            end = current[-1]["e"]
            chunks.append({
                "i": len(chunks),
                "start": round(start, 2),
                "end": round(end, 2),
                "words": current,
            })
            current = []

    for seg in transcript["segments"]:
        words = seg.get("words") or []
        if not words:  # distribute evenly
            toks = seg["text"].split()
            n = max(1, len(toks))
            words = [{"w": t, "s": seg["start"] + (seg["end"] - seg["start"]) * j / n,
                      "e": seg["start"] + (seg["end"] - seg["start"]) * (j + 1) / n}
                     for j, t in enumerate(toks)]
        prev = None
        for wd in words:
            w = str(wd.get("w", "")).strip()
            if not w:
                continue
            s, e = float(wd.get("s", seg["start"])), float(wd.get("e", seg["end"]))
            if prev is not None and (s - prev > break_gap):
                flush()
            token = {"w": w, "s": round(s, 2), "e": round(e, 2), "kw": is_keyword(w, extra_keywords)}
            current.append(token)
            if len(current) >= max_words or PUNCT_BREAK.search(w):
                flush()
            prev = e
    flush()
    # merge ultra-short chunks (<0.25s) forward
    merged = []
    for ch in chunks:
        if merged and (ch["end"] - ch["start"]) < 0.25:
            last = merged[-1]
            last["words"] += ch["words"]
            last["end"] = ch["end"]
        else:
            merged.append(ch)
    for i, ch in enumerate(merged):
        ch["i"] = i
    return merged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--style", default=None)
    ap.add_argument("--max-words", type=int, default=None)
    args = ap.parse_args()

    cfg = C.load_config()
    ccfg = cfg["captions"]
    if not ccfg.get("enabled", True):
        print("Captions disabled in config.")
        return

    pp = C.project_path(args.name)
    transcript = json.loads((pp / "transcript" / "transcript.json").read_text(encoding="utf-8"))

    sb_path = pp / "storyboard.json"
    extra = set()
    if sb_path.exists():
        sb = json.loads(sb_path.read_text(encoding="utf-8"))
        for s in sb.get("scenes", []):
            extra.update(k.lower() for k in s.get("caption_keywords", []) if k)

    style = args.style or ccfg["style"]
    max_words = args.max_words or ccfg["max_words_per_chunk"]
    chunks = build_chunks(transcript, extra, max_words, ccfg["break_gap_s"])

    out = {
        "style": style,
        "keyword_colors": ccfg["keyword_colors"],
        "position": ccfg.get("position", "bottom"),
        "font_arabic": cfg["brand"]["fonts"]["arabic"],
        "font_latin": cfg["brand"]["fonts"]["latin"],
        "chunks": chunks,
    }
    (pp / "transcript" / "captions.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    n_kw = sum(1 for ch in chunks for w in ch["words"] if w["kw"])
    C.log(args.name, f"Captions: {len(chunks)} chunks, {n_kw} keywords styled ({style})")
    print(f"OK: {len(chunks)} caption chunks ({n_kw} keywords) -> transcript/captions.json")


if __name__ == "__main__":
    main()
