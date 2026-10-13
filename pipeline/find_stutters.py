"""Find stutters / micro false starts INSIDE speech chunks (the ones find_retakes.py cannot see).

Usage: python pipeline/find_stutters.py <name> [--src assets/voice/voiceover_raw.wav] [--dip-db -38] [--dip 0.06]

Why: a transcription model given a whole chunk "cleans" it — "والنانو… والنانو بلانا 2.1" comes back as one
clean phrase, so the stutter is never proposed (Nano Banana 2.1 at 05:43). Splitting the chunk at micro-pauses
(>= 60 ms) and transcribing each PIECE separately exposes it: a short piece that the next piece restarts.

Rules (per pair of consecutive pieces A -> B inside one chunk):
  restart   A is short (<= 3 words or <= 1.6 s) and A's words match the start of B   -> cut A (keep the later take)
  fragment  A is one word that is a prefix-ish of B's first word (e.g. "والنحو" -> "والنانو")  -> cut A
  repeat    A ends with the same 1-3 words that B starts with (A long)               -> review (times printed)
Writes input/stutters.proposed.json: [{"cut": [a, b], "kind", "a_text", "b_text", "confidence"}] in SOURCE seconds.
Apply: split the matching keep range in input/screen_edit.json (or add to input/edit.json cuts) — keep the later take.
"""
import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
from find_retakes import norm, toks, transcribe  # noqa: E402


def sim(a, b):
    return SequenceMatcher(None, a, b).ratio()


def micro_pieces(src, a, b, th, d, min_len=0.25):
    r = C.run(["ffmpeg", "-hide_banner", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(src),
               "-af", f"silencedetect=noise={th}dB:d={d}", "-f", "null", "-"])
    st = [a + float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    en = [a + float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    edges, t = [], a
    for x, y in zip(st, en):
        if x - t >= 0.05:
            edges.append([t, x])
        t = y
    if b - t >= 0.05:
        edges.append([t, b])
    out = []
    for p in edges:  # merge slivers into the following piece
        if out and out[-1][1] - out[-1][0] < min_len:
            out[-1][1] = p[1]
        else:
            out.append(p)
    if len(out) > 1 and out[-1][1] - out[-1][0] < min_len:
        out[-2][1] = out[-1][1]
        out.pop()
    return out


def judge(A, B):
    ta, tb = toks(A["text"]), toks(B["text"])
    if not ta or not tb:
        return None
    short = len(ta) <= 3 or (A["b"] - A["a"]) <= 1.6
    k = min(len(ta), len(tb))
    if short and k and all(sim(ta[i], tb[i]) >= 0.7 for i in range(k)):
        return "restart", 0.9
    if short and len(ta) == 1 and len(ta[0]) >= 3 and sim(ta[0], tb[0][: len(ta[0]) + 1]) >= 0.6:
        return "fragment", 0.75
    if short and sim(" ".join(ta), " ".join(tb[: len(ta)])) >= 0.75:
        return "restart", 0.8
    for n in (3, 2, 1):
        if len(ta) >= n and len(tb) >= n and all(len(w) >= 3 for w in ta[-n:]) \
                and all(sim(x, y) >= 0.8 for x, y in zip(ta[-n:], tb[:n])):
            return "repeat", 0.6
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--src", default=None)
    ap.add_argument("--dip-db", type=float, default=-38)
    ap.add_argument("--dip", type=float, default=0.06)
    ap.add_argument("--model", default="gpt-4o-transcribe")
    ap.add_argument("--lang", default="ar")
    a = ap.parse_args()
    pp = C.project_path(a.name)
    src = pp / (a.src or next(p for p in ("assets/voice/voiceover_raw.wav", "assets/voice/voiceover_clean.wav")
                              if (pp / p).exists()))
    chunks = json.loads((pp / "transcript/chunks.json").read_text(encoding="utf-8"))["chunks"]
    key = C.get_key("OPENAI_API_KEY")
    tmp = pp / "transcript/stutter_pieces"
    tmp.mkdir(parents=True, exist_ok=True)
    cache_p = pp / "transcript/stutter_pieces.json"
    cache = json.loads(cache_p.read_text(encoding="utf-8")) if cache_p.exists() else {}

    jobs = []
    seq = []  # every piece in time order, across chunks (a stutter often ends one chunk and restarts the next)
    for c in chunks:
        if not c["text"].strip():
            continue
        ps = micro_pieces(src, c["s"], c["e"], a.dip_db, a.dip) if c["e"] - c["s"] >= 1.0 else []
        if len(ps) < 2:  # single piece: the chunk's verbatim text is already per-piece
            seq.append({"a": c["s"], "b": c["e"], "id": None, "text": c["text"]})
            continue
        for x, y in ps:
            kid = f"{x:.2f}-{y:.2f}"
            seq.append({"a": x, "b": y, "id": kid})
            if kid not in cache:
                jobs.append((kid, x, y))

    def work(j):
        kid, x, y = j
        f = tmp / f"p_{kid}.wav"
        C.ffmpeg(["-ss", f"{max(0, x - 0.04):.3f}", "-t", f"{y - x + 0.08:.3f}", "-i", str(src), "-ac", "1", "-ar", "16000", str(f)])
        try:
            return kid, transcribe(f, key, a.model, a.lang)
        finally:
            f.unlink(missing_ok=True)

    print(f"{len(seq)} pieces, {len(jobs)} to transcribe ({len(cache)} cached)")
    with ThreadPoolExecutor(max_workers=6) as ex:
        for kid, text in ex.map(work, jobs):
            cache[kid] = text
    cache_p.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")

    props = []
    for p in seq:
        if p["id"]:
            p["text"] = cache.get(p["id"], "")
    for A, B in zip(seq, seq[1:]):
            if B["a"] - A["b"] > 1.5:  # a real pause/cut in between: not a stutter
                continue
            j = judge(A, B)
            if not j:
                continue
            kind, conf = j
            cut = [round(A["a"] - 0.02, 3), round(B["a"] - 0.03, 3)]
            props.append({"cut": cut, "kind": kind if kind != "repeat" else "review_repeat", "a_text": A["text"],
                          "b_text": B["text"], "confidence": conf})
    # detector 2: "unworded speech" — voiced audio (>= 0.25 s) that no ASR word covers. Transcribers silently
    # DROP stutters/false starts ("والنا…" at 463.4 in Nano Banana 2.1: words end 463.07, resume 464.70).
    ww_p = pp / "transcript/window_words.json"
    if ww_p.exists():
        ww = json.loads(ww_p.read_text(encoding="utf-8"))
        ww = ww.get("words", ww) if isinstance(ww, dict) else ww
        spans = sorted((w["s"], w["e"]) for w in ww)
        dur = C.ffprobe_duration(src)
        for x, y in micro_pieces(src, 0.0, dur, a.dip_db, a.dip, min_len=0.0):
            if y - x < 0.25:
                continue
            cov = sum(max(0.0, min(y, e) - max(x, s)) for s, e in spans if e > x and s < y)
            if cov / (y - x) < 0.15:
                # don't re-propose what detector 1 already has
                if any(c["cut"][0] - 0.1 <= x and y <= c["cut"][1] + 0.1 for c in props):
                    continue
                # confirm: transcribe the stretch alone; if its words ARE in the chunk's verbatim text, whisper just
                # missed a real word (e.g. "الفيديو") -> keep it
                kid = f"u{x:.2f}-{y:.2f}"
                if kid not in cache:
                    cache[kid] = work((kid, x, y))[1]
                said = toks(cache[kid])
                ctext = " ".join(c["text"] for c in chunks if c["e"] > x - 0.3 and c["s"] < y + 0.3)
                ref = toks(ctext)
                real = said and all(max((sim(t, r) for r in ref), default=0) >= 0.8 for t in said)
                if real:
                    continue
                nxt = " ".join(w["w"] for w in ww if y - 0.05 <= w["s"] <= y + 2.0)
                tn = toks(nxt)
                arabic = bool(re.search(r"[؀-ۿ]", cache[kid]))
                restart = arabic and said and tn and (sim(said[0], tn[0][: len(said[0]) + 1]) >= 0.7 or tn[0].startswith(said[0]))
                if restart:
                    kind, conf, note = "stutter", 0.9, f"restarted as: {nxt[:40]}"
                else:
                    kind, conf, note = "review_unworded", 0.5, f"unclear ({'non-Arabic ASR' if not arabic else 'no match'}), coverage {cov / (y - x):.0%}"
                props.append({"cut": [round(x - 0.03, 3), round(y + 0.03, 3)], "kind": kind, "a_text": cache[kid],
                              "b_text": note, "confidence": conf})
        cache_p.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")
    props.sort(key=lambda c: c["cut"][0])
    (pp / "input/stutters.proposed.json").write_text(json.dumps(props, ensure_ascii=False, indent=1), encoding="utf-8")
    for p in props:
        print(f"  {p['cut'][0]:8.2f}-{p['cut'][1]:8.2f}  {p['kind']:13s} {p['confidence']:.2f}  [{p['a_text']}] -> [{p['b_text']}]")
    print(f"-> input/stutters.proposed.json ({len(props)} proposals). Keep the LATER take; check 'review_repeat' by ear.")


if __name__ == "__main__":
    main()
