"""01 - Transcribe the cleaned voiceover with Gemini (or n8n webhook, or mock).

Usage:
  python pipeline/transcribe.py <name> [--provider openai_whisper|gemini_api|n8n|mock] [--input <file>]

Default input: assets/voice/voiceover_clean.wav (falls back to input/ raw file).
Output: transcript/transcript.json + transcript.md
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

MOCK_SEGMENTS = [
    "إحنا عايشين في أحسن وقت ممكن، الـ AI بقى في إيدك",
    "الناس بتخاف إن الـ AI هيستبدلها، بس الحقيقة مختلفة",
    "إنت مش محتاج تبقى خبير، محتاج تبدأ بس",
    "الـ prompt هو المفتاح، لو عرفت تسأل صح، هتجاوب صح",
    "خد الفكرة وجرّب بنفسك، النتيجة هتكون أكبر من تخيلك",
    "لو عايز تسبق غيرك، ابدأ النهاردة قبل بكرة",
    "دي فرصتك، متضيعهاش، المستقبل للي بيشتغل دلوقتي",
    "وأنا هكون معاك خطوة بخطوة في الرحلة دي كلها",
]


def to_wav16k(src: Path, dest: Path):
    C.ffmpeg(["-i", str(src), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(dest)])
    return dest


def compact_for_api(src: Path, out_dir: Path) -> Path:
    """16kHz mono AAC 32k (~1.2MB per 5 min instead of ~29MB WAV).
    No temporal changes — transcript timestamps stay valid."""
    # cache per source file: --input <other.wav> must never reuse another file's upload copy
    dest = out_dir / ("voice_for_api.m4a" if src.name == "voiceover_clean.wav" else f"{src.stem}_for_api.m4a")
    if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
        C.ffmpeg(["-i", str(src), "-ac", "1", "-ar", "16000",
                  "-c:a", "aac", "-b:a", "32k", str(dest)])
    return dest


def _extract_text(resp):
    try:
        parts = resp["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError):
        raise C.PermanentError(
            f"Unexpected Gemini response shape: {json.dumps(resp, ensure_ascii=False)[:500]}")
    texts = []
    for p in parts:
        if isinstance(p.get("text"), str):
            texts.append(p["text"])
        elif isinstance(p.get("audioTranscription"), dict):
            texts.append(p["audioTranscription"].get("text", ""))
    if not texts:
        raise C.PermanentError(
            f"No text part in Gemini response: {json.dumps(resp, ensure_ascii=False)[:500]}")
    return "\n".join(texts)


def call_gemini(cfg, audio_path: Path, prompt: str, api_key: str):
    t = cfg["transcription"]["gemini"]
    url = f"{t['api_base']}/v1beta/models/{t['model']}:generateContent"
    body = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": C.mime_for(audio_path), "data": C.b64_file(audio_path)}},
            ]
        }],
        "generationConfig": {"temperature": t.get("temperature", 0),
                             "responseMimeType": "application/json",
                             "maxOutputTokens": 32768},
    }
    headers = {"x-goog-api-key": api_key}
    status, resp = C.http_json(url, headers=headers, body=body, timeout=300)
    if status == 400 and ("JSON mode" in str(resp) or "max_output_tokens" in str(resp)
                          or "maxOutputTokens" in str(resp)):
        # model rejects JSON mode and/or the token cap — degrade gracefully
        gc = body["generationConfig"]
        gc.pop("responseMimeType", None)
        gc["maxOutputTokens"] = 8192
        status, resp = C.http_json(url, headers=headers, body=body, timeout=300)
    if status != 200:
        err = f"Gemini API error {status}: {json.dumps(resp, ensure_ascii=False)[:500]}"
        raise C.PermanentError(err) if 400 <= status < 500 and status != 429 else RuntimeError(err)
    text = _extract_text(resp)
    try:
        return C.extract_json(text)
    except ValueError:
        raise C.PermanentError(
            "Model returned plain transcription without JSON timestamps. Dedicated transcribe "
            "models cannot produce timestamps — set transcription.gemini.model to a general "
            f"multimodal model (e.g. gemini-3.5-flash) in config. First 300 chars:\n{text[:300]}")


def chunk_audio(src: Path, out_dir: Path, chunk_s: float = 75.0):
    """Split into ~chunk_s pieces (re-encoded for exact cuts). Returns [(path, start_offset)]."""
    dest = out_dir / "chunks"
    dest.mkdir(parents=True, exist_ok=True)
    existing = sorted(dest.glob("chunk_*.m4a"))
    if not existing:
        C.ffmpeg(["-i", str(src), "-f", "segment", "-segment_time", str(chunk_s),
                  "-c:a", "aac", "-b:a", "32k", str(dest / "chunk_%03d.m4a")])
        existing = sorted(dest.glob("chunk_*.m4a"))
    chunks, total = [], 0.0
    for ch in existing:
        chunks.append((ch, round(total, 2)))
        total += C.ffprobe_duration(ch)
    return chunks


def transcribe_chunked(cfg, src_api: Path, prompt: str, key: str, out_dir: Path,
                       chunk_s: float = 75.0):
    """Long audio -> per-chunk transcription with word timestamps -> offset merge."""
    chunks = chunk_audio(src_api, out_dir, chunk_s)
    n = len(chunks)
    all_segments = []
    for i, (ch_path, offset) in enumerate(chunks, 1):
        part_prompt = (prompt +
                       f"\n\nIMPORTANT: This is part {i} of {n} of a longer recording. "
                       f"All timestamps must be RELATIVE TO THIS PART (0.00 = start of this "
                       f"part). The first segment starts at 0.00.")
        C.log_stream = None
        print(f"  chunk {i}/{n} (+{offset:.1f}s offset, {ch_path.stat().st_size/1e6:.2f}MB)")
        data = C.retry(lambda: call_gemini(cfg, ch_path, part_prompt, key),
                       attempts=6, delay=15, label=f"chunk {i}/{n}")
        segs = data.get("segments") or []
        for s in segs:
            s["start"] = round(float(s.get("start", 0)) + offset, 2)
            s["end"] = round(float(s.get("end", 0)) + offset, 2)
            for w in s.get("words") or []:
                w["s"] = round(float(w.get("s", 0)) + offset, 2)
                w["e"] = round(float(w.get("e", 0)) + offset, 2)
            all_segments.append(s)
    all_segments.sort(key=lambda s: s["start"])
    return {"language": "ar-EG", "segments": all_segments}


def call_openai_whisper(cfg, audio_path: Path, key: str):
    """OpenAI whisper-1 verbose_json: real word-level timestamps (the reliable path for cut
    decisions + caption sync). NO `prompt` hint on purpose: a hint that matches the opening
    words makes Whisper skip that speech. Spelling (Egyptian dialect, Latin keywords) is fixed
    afterwards by the agent against a text-only pass if needed."""
    import requests  # key goes in a header, never on a command line (visible in the process list)
    o = cfg["transcription"].get("openai", {})
    fields = [("model", o.get("model", "whisper-1")), ("language", o.get("language", "ar")),
              ("response_format", "verbose_json"), ("timestamp_granularities[]", "word"),
              ("timestamp_granularities[]", "segment"), ("temperature", "0")]
    with open(audio_path, "rb") as fh:
        r = requests.post(o.get("api_url", "https://api.openai.com/v1/audio/transcriptions"),
                          headers={"Authorization": f"Bearer {key}"}, data=fields,
                          files={"file": (audio_path.name, fh, C.mime_for(audio_path))}, timeout=900)
    try:
        d = r.json()
    except Exception:
        raise RuntimeError(f"OpenAI transcription: non-JSON response ({r.status_code}): {r.text[:300]}")
    if "error" in d:
        raise RuntimeError(f"OpenAI transcription error: {d['error'].get('message')}")
    words = d.get("words") or []
    segs = []
    raw_segs = d.get("segments") or []
    wi = 0
    for k, sg in enumerate(raw_segs):
        nxt = raw_segs[k + 1]["start"] if k + 1 < len(raw_segs) else float("inf")
        ws = []
        while wi < len(words) and (words[wi]["start"] < nxt or k == len(raw_segs) - 1):
            w = words[wi]  # each word belongs to exactly one segment (no boundary duplicates)
            ws.append({"w": w["word"], "s": round(w["start"], 2), "e": round(w["end"], 2)})
            wi += 1
        segs.append({"start": round(sg["start"], 2), "end": round(sg["end"], 2),
                     "text": sg["text"].strip(), "words": ws})
    (audio_path.parent / "openai_raw.json").write_text(json.dumps(d, ensure_ascii=False, indent=1),
                                                       encoding="utf-8")
    return {"language": "ar-EG", "segments": segs, "provider": "openai_whisper"}


def call_n8n(cfg, audio_path: Path, prompt: str):
    n = cfg["transcription"]["n8n"]
    url = n["webhook_url"]
    body = {"audio_base64": C.b64_file(audio_path), "prompt": prompt,
            "mime_type": C.mime_for(audio_path), "filename": audio_path.name}
    status, resp = C.http_json(url, body=body, timeout=600)
    if status != 200:
        raise RuntimeError(f"n8n webhook error {status}: {str(resp)[:500]}")
    return parse_n8n(resp)


def parse_n8n(resp):
    """Defensively locate a transcript object inside an arbitrary n8n response."""
    def looks_like(d):
        return isinstance(d, dict) and "segments" in d

    def find(obj, depth=0):
        if depth > 5:
            return None
        if looks_like(obj):
            return obj
        if isinstance(obj, dict):
            for v in obj.values():
                r = find(v, depth + 1)
                if r:
                    return r
        elif isinstance(obj, list):
            for v in obj:
                r = find(v, depth + 1)
                if r:
                    return r
        elif isinstance(obj, str):
            try:
                return find(C.extract_json(obj), depth + 1)
            except Exception:
                return None
        return None

    found = find(resp)
    if not found:
        raise RuntimeError(f"Could not find transcript JSON in n8n response: {str(resp)[:500]}")
    return found


def mock_transcript(duration: float):
    n = len(MOCK_SEGMENTS)
    segs = []
    for i, text in enumerate(MOCK_SEGMENTS):
        start = duration * i / n
        end = duration * (i + 1) / n
        words = text.split()
        ws = []
        for j, w in enumerate(words):
            s = start + (end - start) * j / len(words)
            e = start + (end - start) * (j + 1) / len(words)
            ws.append({"w": w, "s": round(s, 2), "e": round(e, 2)})
        segs.append({"start": round(start, 2), "end": round(end, 2), "text": text, "words": ws})
    return {"language": "ar-EG", "duration_s": round(duration, 2), "segments": segs}


def normalize_transcript(data, duration: float):
    """Validate/repair transcript: clamp to duration, drop overlaps, ensure words."""
    segs = data.get("segments") or []
    if not segs:
        raise RuntimeError("Transcript has no segments")
    out = []
    last_end = 0.0
    for s in segs:
        start = max(0.0, float(s.get("start", 0)))
        end = min(duration if duration else 1e9, float(s.get("end", 0)))
        if end <= start:
            continue
        start = max(start, last_end)  # no overlaps
        if end <= start:
            continue
        words = s.get("words") or []
        if not words:
            toks = s.get("text", "").split()
            ws = []
            for j, w in enumerate(toks):
                s0 = start + (end - start) * j / max(1, len(toks))
                e0 = start + (end - start) * (j + 1) / max(1, len(toks))
                ws.append({"w": w, "s": round(s0, 2), "e": round(e0, 2)})
            words = ws
        out.append({"start": round(start, 2), "end": round(end, 2),
                    "text": s.get("text", ""), "words": words})
        last_end = end
    if not out:
        raise RuntimeError("Transcript empty after normalization")
    full = " ".join(o["text"] for o in out)
    return {"language": data.get("language", "ar-EG"),
            "duration_s": round(duration, 2) if duration else out[-1]["end"],
            "full_text": full, "segments": out,
            "provider": data.get("provider", "")}


def transcript_md(t):
    lines = [f"# Transcript — {t['language']} — {t['duration_s']}s", ""]
    for i, s in enumerate(t["segments"], 1):
        lines.append(f"**[{s['start']:.2f} → {s['end']:.2f}]** {s['text']}")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--provider", default=None, choices=["openai_whisper", "gemini_api", "n8n", "mock"])
    ap.add_argument("--input", default=None)
    args = ap.parse_args()

    cfg = C.load_config()
    pp = C.project_path(args.name)

    # prefer the cleaned voice; fall back to raw input
    clean = pp / "assets" / "voice" / "voiceover_clean.wav"
    if args.input:
        src = Path(args.input)
    elif clean.exists():
        src = clean
    else:
        src = C.find_input_audio(args.name)
    if not src or not Path(src).exists():
        raise SystemExit("No audio to transcribe. Run clean_audio.py first or pass --input.")

    duration = C.ffprobe_duration(src)
    provider = args.provider or cfg["transcription"]["provider"]

    # compact upload copy (tiny payload, identical timings)
    src_api = compact_for_api(src, pp / "assets" / "voice") if provider != "mock" else src
    C.log(args.name, f"Transcribing ({provider}) {Path(src).name} ({duration:.1f}s, "
                     f"upload {src_api.stat().st_size/1e6:.2f}MB)")

    prompt = C.read_prompt(cfg["transcription"]["prompt_file"])

    if provider == "mock":
        data = mock_transcript(duration)
    elif provider == "n8n":
        data = call_n8n(cfg, src_api, prompt)
    elif provider == "openai_whisper":
        key = C.get_key("OPENAI_API_KEY")
        if not key:
            raise SystemExit("OPENAI_API_KEY not set (config/api_keys.json or env).")
        data = call_openai_whisper(cfg, src_api, key)
    else:
        key = C.get_key("GEMINI_API_KEY")
        if not key:
            raise SystemExit("GEMINI_API_KEY not set. Add it via dashboard (Keys tab), "
                             "config/api_keys.json, or env var. Or use --provider mock for testing.")
        data = transcribe_chunked(cfg, src_api, prompt, key, pp / "assets" / "voice")

    t = normalize_transcript(data, duration)
    t["provider"] = provider

    tdir = pp / "transcript"
    tdir.mkdir(parents=True, exist_ok=True)
    (tdir / "transcript.json").write_text(json.dumps(t, indent=2, ensure_ascii=False), encoding="utf-8")
    (tdir / "transcript.md").write_text(transcript_md(t), encoding="utf-8")

    proj = C.load_project(args.name)
    proj["duration_s"] = t["duration_s"]
    C.save_project(args.name, proj)
    C.update_stage(args.name, "transcribe", f"{provider}: {len(t['segments'])} segments")
    print(f"\nOK: {len(t['segments'])} segments, {t['duration_s']}s -> {tdir / 'transcript.json'}")
    print(f"Next: python pipeline/plan_scenes.py {args.name}")


if __name__ == "__main__":
    main()
