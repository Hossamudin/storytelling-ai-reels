"""Find retakes, false starts, stutters and fillers automatically -> input/edit.proposed.json + review page.

Usage:
  python pipeline/find_retakes.py <name> [--no-llm] [--refresh]

Why: whisper-1 "cleans" speech: it drops repeated words and merges two takes into one span, so a
transcript-driven edit can't see the mistakes it should cut. This script works from a VERBATIM
source instead:
  1. split assets/voice/voiceover_clean.wav into speech chunks at pauses (silencedetect)
  2. transcribe every chunk with a verbatim model (config retakes.model, default gpt-transcribe)
     -> transcript/chunks.json (chunk timing + verbatim text). Chunk edges are pauses, so every
     cut proposed here starts and ends in silence (no clipped syllables).
  3. deterministic rules: repeated phrase starts (keep the LATER take), stutters, filler-only
     chunks, empty/non-speech chunks
  4. LLM editor pass (config retakes.llm_model) over the numbered chunk list: paraphrased restarts
     and abandoned sentences; in-chunk restarts are refined by re-splitting that chunk at shorter dips
  5. transcript/transcript_verbatim.json: whisper-1 word TIMINGS from <=10 s pause-bounded windows (long-file
     whisper loops and skips) + verbatim SPELLING;
     voice_edit.py uses it automatically (no hand-written "fix" maps for Latin terms)
Writes:
  input/edit.proposed.json     same schema as edit.json + "proposals" (kind / reason / confidence / text)
  review/cuts.html             listen to each cut (before / after with context), tick, export edit.json
Then: review, copy to input/edit.json (or accept all), run voice_edit.py <name> --verify.
"""
import argparse
import concurrent.futures as cf
import difflib
import html
import json
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

FILLERS = {"اه", "ااه", "ام", "امم", "اممم", "ايه", "يعني", "uh", "um", "hmm", "eh", "ah", "مم", "ممم", "هه"}
AR_DIAC = re.compile(r"[ً-ْٰـ]")


def norm(t):
    t = AR_DIAC.sub("", t.lower())
    t = re.sub("[أإآٱ]", "ا", t).replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    return re.sub(r"[^\w%.$]", "", t).strip(".")


def toks(text):
    return [n for n in (norm(x) for x in re.split(r"[\s،,؟?!.…:;]+", text)) if n]


# ------------------------------------------------------------------ audio
def silences(src, th, d):
    r = C.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", f"silencedetect=noise={th}dB:d={d}", "-f", "null", "-"])
    st = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(st, en))


def speech_chunks(src, dur, th=-38, d=0.15, lo=0.0, hi=None, min_len=0.12):
    hi = dur if hi is None else hi
    out, t = [], lo
    for s, e in silences(src, th, d):
        s, e = max(s, lo), min(e, hi)
        if e <= lo or s >= hi:
            continue
        if s - t >= min_len:
            out.append([round(t, 3), round(s, 3)])
        t = max(t, e)
    if hi - t >= min_len:
        out.append([round(t, 3), round(hi, 3)])
    return out


def cut_clip(src, a, b, dest, pad=0.08):
    C.ffmpeg(["-ss", f"{max(0, a - pad):.3f}", "-to", f"{b + pad:.3f}", "-i", str(src), "-ar", "16000", "-ac", "1",
              "-c:a", "aac", "-b:a", "64k", str(dest)])


# ------------------------------------------------------------------ OpenAI
def transcribe(path, key, model, lang):
    def call():
        with open(path, "rb") as fh:
            r = requests.post("https://api.openai.com/v1/audio/transcriptions", headers={"Authorization": f"Bearer {key}"},
                              data={"model": model, "language": lang, "response_format": "json"},
                              files={"file": fh}, timeout=180)
        if r.status_code != 200:
            raise RuntimeError(f"{model} HTTP {r.status_code}: {r.text[:300]}")
        return r.json().get("text", "").strip()
    return C.retry(call, attempts=3, delay=3, label=f"transcribe {path.name}")


def whisper_words(path, key):
    """whisper-1 word timings for one short clip (no prompt: a hint makes it skip speech)."""
    def call():
        with open(path, "rb") as fh:
            r = requests.post("https://api.openai.com/v1/audio/transcriptions", headers={"Authorization": f"Bearer {key}"},
                              data=[("model", "whisper-1"), ("language", "ar"), ("response_format", "verbose_json"),
                                    ("timestamp_granularities[]", "word"), ("temperature", "0")],
                              files={"file": fh}, timeout=180)
        if r.status_code != 200:
            raise RuntimeError(f"whisper-1 HTTP {r.status_code}: {r.text[:300]}")
        return [{"w": w["word"].strip(), "s": w["start"], "e": w["end"]} for w in r.json().get("words") or []]
    return C.retry(call, attempts=3, delay=3, label=f"whisper {path.name}")


def windows(chunks, max_len=10.0):
    """Group consecutive speech chunks into <= max_len s windows that start and end in pauses."""
    out, cur = [], None
    for c in chunks:
        s, e = (c["s"], c["e"]) if isinstance(c, dict) else c
        if cur and e - cur[0] <= max_len:
            cur[1] = e
        else:
            if cur:
                out.append(cur)
            cur = [s, e]
    if cur:
        out.append(cur)
    return out


def window_word_timings(src, chunks, key, tmpdir, tag="w", pad=0.08):
    """Word timings from whisper-1 on short pause-bounded windows instead of one long-file pass.
    Long-file whisper loops / skips stretches (openrouter-free: 103 words for 162 s, one word 23 s long);
    on 2-10 s windows it is reliable. A window whisper returns nothing for is reported (never silently dropped)."""
    tmpdir.mkdir(parents=True, exist_ok=True)
    wins = windows(chunks)

    def job(kw):
        k, (s, e) = kw
        p = tmpdir / f"{tag}{k:03d}.m4a"
        cut_clip(src, s, e, p, pad=pad)
        ws = whisper_words(p, key)
        base = max(0.0, s - pad)
        return k, [{"w": w["w"], "s": round(min(max(base + w["s"], s), e), 3), "e": round(min(max(base + w["e"], s), e), 3)} for w in ws if w["w"]]

    with cf.ThreadPoolExecutor(8) as ex:
        res = dict(ex.map(job, enumerate(wins)))
    words, empty = [], []
    for k, (s, e) in enumerate(wins):
        if not res[k]:
            empty.append((s, e))
        words += res[k]
    if empty:
        print(f"  ! whisper returned no words for {len(empty)} window(s): {[(round(s, 2), round(e, 2)) for s, e in empty]}")
    return sorted(words, key=lambda w: w["s"]), empty


def llm_json(key, model, system, user):
    def call():
        r = requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {key}"},
                          json={"model": model, "response_format": {"type": "json_object"},
                                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
                          timeout=600)
        if r.status_code != 200:
            raise RuntimeError(f"{model} HTTP {r.status_code}: {r.text[:400]}")
        return json.loads(r.json()["choices"][0]["message"]["content"])
    return C.retry(call, attempts=2, delay=5, label=f"llm {model}")


LLM_SYSTEM = """You are the dialogue editor of an Egyptian-Arabic tech video. You get the raw voice recording as
numbered speech chunks (split at pauses) with VERBATIM text, plus a clean full-text reference.
Find everything a professional editor cuts:
- retake: the speaker abandons a sentence (or part of it) and says it again / rephrases it. KEEP THE LATER,
  complete take; cut the earlier attempt. Paraphrased restarts count ("كنت بستخدم ..." then "كنت عمال بعتمد على ...").
- false_start: a cut-off word or phrase that goes nowhere ("أحسن طبعًا من..." followed by a new sentence).
- stutter: the same word twice in a row by accident.
- filler: a chunk that is only a filler sound (اه / امم / يعني as hesitation).
- noise: a chunk that is not speech.
Do NOT cut content, opinions, examples, or intentional repetition for emphasis. Be precise, not greedy.
Each cut is a contiguous range of WHOLE chunks [from, to] (inclusive), OR — when the abandoned words share a
chunk with kept words — an "inside" cut: give the chunk index and the exact verbatim words to remove
("drop_text"); the tool will locate them.
Return JSON: {"cuts": [{"from": i, "to": j, "kind": "...", "reason": "short English", "confidence": 0-1}],
"inside": [{"chunk": i, "drop_text": "...", "kind": "...", "reason": "...", "confidence": 0-1}],
"spelling": {"wrong": "right", ...}  // brand / product names misheard in BOTH sources, e.g. a tool name
}"""


# ------------------------------------------------------------------ detection
def rule_proposals(chunks):
    props = []
    n = len(chunks)
    for i, c in enumerate(chunks):
        A = toks(c["text"])
        dur = c["e"] - c["s"]
        if not A:
            props.append({"from": i, "to": i, "kind": "noise", "reason": "no speech in verbatim transcript", "confidence": 0.6})
            continue
        if all(t in FILLERS for t in A) and dur < 1.6:
            props.append({"from": i, "to": i, "kind": "filler", "reason": f"filler only: {c['text']}", "confidence": 0.8})
            continue
        for j in range(i + 1, min(n, i + 4)):
            if chunks[j]["s"] - c["e"] > 6:
                break
            B = toks(chunks[j]["text"])
            if not B:
                continue
            k = min(len(A), len(B))
            head = difflib.SequenceMatcher(None, A, B[:len(A) + 2]).ratio()
            if len(A) >= 2 and head >= 0.6 and len(B) >= len(A) * 0.8:
                props.append({"from": i, "to": j - 1, "kind": "retake",
                              "reason": f"chunk {j} restarts chunk {i} (similarity {head:.2f}); keep the later take",
                              "confidence": round(min(0.95, head), 2)})
                break
            if len(A) == 1 and A[0] == B[0] and dur < 1.2 and k:
                props.append({"from": i, "to": j - 1, "kind": "stutter", "reason": f"'{c['text']}' repeated", "confidence": 0.7})
                break
    return props


def locate_inside(src, chunk, drop_text, key, model, lang, tmpdir):
    """Re-split one chunk at shorter dips, transcribe the pieces, return [a, b] covering drop_text."""
    pieces = speech_chunks(src, None, th=-32, d=0.06, lo=chunk["s"], hi=chunk["e"], min_len=0.05)
    if len(pieces) < 2:
        return None
    texts = []
    for k, (a, b) in enumerate(pieces):
        p = tmpdir / f"in_{chunk['i']}_{k}.m4a"
        cut_clip(src, a, b, p, pad=0.03)
        texts.append(transcribe(p, key, model, lang))
    D = toks(drop_text)
    best, span = 0.0, None
    for x in range(len(pieces)):
        for y in range(x, len(pieces)):
            T = [t for z in range(x, y + 1) for t in toks(texts[z])]
            r = difflib.SequenceMatcher(None, D, T).ratio()
            if r > best:
                best, span = r, (x, y)
    if not span or best < 0.6:
        return None
    x, y = span
    a = pieces[x][0] - 0.03
    b = pieces[y + 1][0] - 0.04 if y + 1 < len(pieces) else pieces[y][1] + 0.03
    return [round(a, 3), round(b, 3), round(best, 2), [texts[z] for z in range(x, y + 1)]]


# ------------------------------------------------------------------ verbatim spelling on whisper timings
def respell(words, chunks, full_ref="", keep_unmatched=True):
    """Whisper words keep their timings; their text is replaced by aligned verbatim tokens.
    Uses the full-file verbatim pass when available (more context = better spelling than short chunks)."""
    out = []
    groups = [(words, full_ref)] if full_ref else [
        ([w for w in words if c["s"] - 0.05 <= (w["s"] + w["e"]) / 2 < c["e"] + 0.05], c["text"]) for c in chunks]
    for ws, text in groups:
        vt = [t for t in re.split(r"\s+", text) if t and norm(t)]
        if not ws:
            continue
        sm = difflib.SequenceMatcher(None, [norm(w["w"]) for w in ws], [norm(t) for t in vt], autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
                for a, b in zip(range(i1, i2), range(j1, j2)):
                    out.append({**ws[a], "w": vt[b].strip("،,")})
            elif op == "replace":
                n, m = i2 - i1, j2 - j1
                for a in range(n):  # spread verbatim tokens over whisper slots
                    seg = vt[j1 + a * m // n: j1 + (a + 1) * m // n]
                    if seg:
                        out.append({**ws[i1 + a], "w": " ".join(seg).strip("،,")})
                    elif out:
                        out[-1]["e"] = ws[i1 + a]["e"]
            elif op == "delete":
                if keep_unmatched:  # whisper-only words: kept on the raw pass, dropped when the reference is complete
                    out.extend(ws[i1:i2])
            # insert: verbatim-only words (usually inside a retake) have no timing -> skipped
    seen, res = set(), []
    for w in sorted(out, key=lambda w: w["s"]):
        if (w["s"], w["w"]) not in seen:
            seen.add((w["s"], w["w"]))
            res.append(w)
    return res


# ------------------------------------------------------------------ review page
def review_page(pp, src, cuts, chunks):
    rv = pp / "review"
    (rv / "clips").mkdir(parents=True, exist_ok=True)
    rows = []
    for k, c in enumerate(cuts):
        a, b = c["cut"]
        ctx0, ctx1 = max(0, a - 2.0), b + 2.0
        C.ffmpeg(["-ss", f"{ctx0:.3f}", "-to", f"{ctx1:.3f}", "-i", str(src), "-c:a", "libmp3lame", "-q:a", "4", str(rv / f"clips/c{k:02d}_before.mp3")])
        fc = (f"[0:a]atrim={ctx0:.3f}:{a:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={max(0, a - ctx0 - 0.012):.3f}:d=0.012[x];"
              f"[0:a]atrim={b:.3f}:{ctx1:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012[y];[x][y]concat=n=2:v=0:a=1[o]")
        C.ffmpeg(["-i", str(src), "-filter_complex", fc, "-map", "[o]", "-c:a", "libmp3lame", "-q:a", "4", str(rv / f"clips/c{k:02d}_after.mp3")])
        conf = c.get("confidence", 0.5)
        rows.append(f"""<tr data-k="{k}"><td><input type="checkbox" {'checked' if conf >= 0.6 else ''}></td>
<td>{a:.2f}–{b:.2f}<br><small>{b - a:.2f}s</small></td><td><b>{html.escape(c['kind'])}</b><br><small>{conf:.2f} · {html.escape(c['source'])}</small></td>
<td dir="rtl" class="t">{html.escape(c.get('text', ''))}</td><td>{html.escape(c.get('reason', ''))}</td>
<td><audio controls preload="none" src="clips/c{k:02d}_before.mp3"></audio><br><audio controls preload="none" src="clips/c{k:02d}_after.mp3"></audio></td></tr>""")
    data = json.dumps([{"cut": c["cut"], "kind": c["kind"], "reason": c.get("reason", "")} for c in cuts], ensure_ascii=False)
    page = f"""<!doctype html><meta charset="utf-8"><title>Cut review</title>
<style>body{{font:14px system-ui;margin:16px;background:#f6f4ea;color:#0d0d0d}}table{{border-collapse:collapse;width:100%}}
td{{border-bottom:1px solid #ccc;padding:6px;vertical-align:top}}.t{{font-size:16px;max-width:420px}}audio{{height:28px;width:260px}}
button{{padding:8px 14px;margin:8px 0;background:#136052;color:#fff;border:0;border-radius:6px}}</style>
<h2>Proposed cuts — {pp.name}</h2><p>Top player = original with 2 s context, bottom = after the cut. Tick what to cut, then export.</p>
<button onclick="exp()">Copy accepted cuts as JSON</button><pre id="o"></pre>
<table><tr><th></th><th>time</th><th>kind</th><th>verbatim</th><th>why</th><th>listen</th></tr>{''.join(rows)}</table>
<script>const D={data};function exp(){{const c=[...document.querySelectorAll('tr[data-k]')].filter(r=>r.querySelector('input').checked)
.map(r=>{{const d=D[+r.dataset.k];return [d.cut[0],d.cut[1],d.kind+': '+d.reason]}});const s=JSON.stringify({{cuts:c}},null,1);
document.getElementById('o').textContent=s;navigator.clipboard&&navigator.clipboard.writeText(s)}}</script>"""
    (rv / "cuts.html").write_text(page, encoding="utf-8")
    return rv / "cuts.html"


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--refresh", action="store_true", help="re-transcribe chunks even if cached")
    a = ap.parse_args()
    cfg = C.load_config()
    rc = {"model": "gpt-transcribe", "llm_model": "gpt-5.5", "language": "ar", "silence_db": -38, "min_pause": 0.15,
          **cfg.get("retakes", {})}
    pp = C.project_path(a.name)
    src = pp / "assets/voice/voiceover_clean.wav"
    dur = C.ffprobe_duration(src)
    key = C.get_key("OPENAI_API_KEY")
    tmp = pp / "assets/voice/_chunks"
    tmp.mkdir(parents=True, exist_ok=True)

    cache = pp / "transcript/chunks.json"
    spans = speech_chunks(src, dur, rc["silence_db"], rc["min_pause"])
    old = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() and not a.refresh else {"chunks": []}
    known = {(c["s"], c["e"]): c["text"] for c in old.get("chunks", []) if c.get("model") == rc["model"]}

    def job(i_span):
        i, (s, e) = i_span
        if (s, e) in known:
            return {"i": i, "s": s, "e": e, "text": known[(s, e)], "model": rc["model"]}
        p = tmp / f"c{i:03d}.m4a"
        cut_clip(src, s, e, p)
        return {"i": i, "s": s, "e": e, "text": transcribe(p, key, rc["model"], rc["language"]), "model": rc["model"]}

    with cf.ThreadPoolExecutor(8) as ex:
        chunks = sorted(ex.map(job, enumerate(spans)), key=lambda c: c["i"])
    full_ref = ""
    fr = pp / "transcript/verbatim_full.txt"
    if fr.exists():
        full_ref = fr.read_text(encoding="utf-8")
    else:
        api = next(iter(sorted((pp / "assets/voice").glob("voice_for_api*.m4a"))), None)
        if api:
            full_ref = transcribe(api, key, rc["model"], rc["language"])
            fr.write_text(full_ref, encoding="utf-8")
    cache.write_text(json.dumps({"model": rc["model"], "chunks": chunks}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(chunks)} speech chunks transcribed verbatim ({rc['model']})")

    props = [{**p, "source": "rules"} for p in rule_proposals(chunks)]
    spelling = {}
    if not a.no_llm:
        listing = "\n".join(f"[{c['i']}] {c['s']:.2f}-{c['e']:.2f} | {c['text']}" for c in chunks)
        try:
            res = llm_json(key, rc["llm_model"], LLM_SYSTEM, f"CHUNKS:\n{listing}\n\nFULL VERBATIM REFERENCE:\n{full_ref}")
            props += [{**p, "source": rc["llm_model"]} for p in res.get("cuts", [])]
            spelling = res.get("spelling", {}) or {}
            for ins in res.get("inside", []):
                ch = chunks[ins["chunk"]]
                loc = locate_inside(src, ch, ins.get("drop_text", ""), key, rc["model"], rc["language"], tmp)
                if loc:
                    props.append({"cut": loc[:2], "kind": ins.get("kind", "retake"), "reason": ins.get("reason", "") + f" (located {loc[2]})",
                                  "confidence": ins.get("confidence", 0.6), "source": rc["llm_model"] + "+refine", "text": " | ".join(loc[3])})
                else:
                    props.append({"cut": None, "kind": "review", "reason": f"could not locate '{ins.get('drop_text')}' inside chunk {ins['chunk']} — cut by hand",
                                  "confidence": 0.0, "source": rc["llm_model"], "text": ch["text"], "chunk": ins["chunk"]})
        except Exception as ex:  # report, never silently degrade
            print(f"LLM pass failed: {ex}")

    # chunk ranges -> time cuts that start/end inside pauses; merge rules + llm
    cuts = []
    for p in props:
        if "cut" not in p:
            i, j = p["from"], p["to"]
            if j < i:
                continue
            a0 = chunks[i]["s"] - 0.04
            b0 = chunks[j + 1]["s"] - 0.06 if j + 1 < len(chunks) else chunks[j]["e"] + 0.05
            p = {**p, "cut": [round(a0, 3), round(b0, 3)], "text": " | ".join(c["text"] for c in chunks[i:j + 1])}
        cuts.append(p)
    review = [c for c in cuts if c["cut"] is None]
    cuts = sorted((c for c in cuts if c["cut"]), key=lambda c: c["cut"][0])
    merged = []
    for c in cuts:
        if merged and c["cut"][0] <= merged[-1]["cut"][1] + 0.02:
            m = merged[-1]
            m["cut"][1] = max(m["cut"][1], c["cut"][1])
            m["confidence"] = max(m["confidence"], c["confidence"])
            if c["source"] not in m["source"]:
                m["source"] += " + " + c["source"]  # agreement of rules + LLM
                m["confidence"] = min(0.98, m["confidence"] + 0.1)
            m["reason"] += " / " + c.get("reason", "")
            if m["kind"] in ("noise", "filler") and c["kind"] not in ("noise", "filler"):
                m["kind"] = c["kind"]  # a retake/false start that swallowed a noise chunk is reported as the retake
            if c.get("text") and c["text"] not in m.get("text", ""):
                m["text"] = " | ".join(x for x in (m.get("text"), c["text"]) if x)
        else:
            merged.append({**c, "cut": list(c["cut"])})

    # verbatim spelling on whisper timings
    wc = pp / "transcript/window_words.json"
    if wc.exists() and not a.refresh and json.loads(wc.read_text(encoding="utf-8")).get("chunks") == len(chunks):
        words = json.loads(wc.read_text(encoding="utf-8"))["words"]
    else:
        words, _ = window_word_timings(src, chunks, key, tmp, tag="w")
        wc.write_text(json.dumps({"chunks": len(chunks), "words": words}, ensure_ascii=False, indent=1), encoding="utf-8")
    tr_n = sum(len(sg["words"]) for sg in json.loads((pp / "transcript/transcript.json").read_text(encoding="utf-8"))["segments"])
    print(f"word timings: {len(words)} words from pause-bounded windows (long-file whisper had {tr_n})")
    vw = respell(words, chunks, full_ref)
    if spelling:
        vw = [{**w, "w": spelling.get(w["w"], w["w"])} for w in vw]
    (pp / "transcript/transcript_verbatim.json").write_text(json.dumps(
        {"source": f"whisper timings + {rc['model']} spelling", "segments": [{"words": vw}]}, ensure_ascii=False, indent=1), encoding="utf-8")

    prop = {"parts": [{"name": "voice", "from": 0, "to": round(dur, 3)}],
            "cuts": [[c["cut"][0], c["cut"][1], f"{c['kind']}: {c.get('reason', '')}"] for c in merged if c["confidence"] >= 0.6],
            "fix": spelling, "max_pause": 0.38, "keep_pause": 0.24, "silence_db": -38,
            "proposals": merged + review}
    (pp / "input/edit.proposed.json").write_text(json.dumps(prop, ensure_ascii=False, indent=1), encoding="utf-8")
    page = review_page(pp, src, merged, chunks)
    removed = sum(c["cut"][1] - c["cut"][0] for c in merged if c["confidence"] >= 0.6)
    print(f"{len(merged)} proposed cuts ({removed:.1f}s at confidence>=0.6), {len(review)} need a manual look")
    for c in merged + review:
        cut = f"{c['cut'][0]:7.2f}-{c['cut'][1]:7.2f}" if c["cut"] else "   (manual)    "
        print(f"  {cut}  {c['kind']:<11} {c['confidence']:.2f}  {c['source']:<22} {c.get('text', '')[:70]}")
    print(f"-> {pp / 'input/edit.proposed.json'}\n-> {page}")
    C.log(a.name, f"find_retakes: {len(chunks)} chunks, {len(merged)} cuts proposed, {len(review)} manual")


if __name__ == "__main__":
    main()
