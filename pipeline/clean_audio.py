"""02 - Clean the raw voiceover with an ffmpeg chain, preserving timing.

Usage: python pipeline/clean_audio.py <name> [--input <file>] [--no-loudnorm]

Timing is ALWAYS preserved (no silence removal) so transcript timestamps stay valid.
Output: projects/<name>/assets/voice/voiceover_clean.wav + voice_analysis.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def build_filter(cfg):
    a = cfg["audio_cleanup"]
    parts = [
        f"highpass=f={a['highpass_hz']}",
        f"lowpass=f={a['lowpass_hz']}",
        f"afftdn=nf={a['denoise_nf_db']}:tn=1",
    ]
    if a.get("deesser", True):
        parts.append("deesser")
    parts.append(f"acompressor={a['compressor']}")
    return parts


def detect_silences(path: Path, threshold_db: float, min_s: float):
    """Return [(start, end)] silence intervals via ffmpeg silencedetect."""
    r = C.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
               f"silencedetect=noise={threshold_db}dB:d={min_s}", "-f", "null", "-"])
    err = r.stderr or ""
    starts = [float(m) for m in re.findall(r"silence_start:\s*(-?[\d.]+)", err)]
    ends = [float(m) for m in re.findall(r"silence_end:\s*(-?[\d.]+)", err)]
    dur = C.ffprobe_duration(path)
    pairs = []
    for i, s in enumerate(starts):
        e = ends[i] if i < len(ends) else dur
        pairs.append((max(0.0, s), min(dur, e)))
    return pairs


def parse_cuts_file(pp: Path):
    """input/cuts.txt — manual wrong-take cuts, one 'start-end' per line.
    Formats: seconds (12.3-15.8) or mm:ss.ms (00:12.3-00:15.8)."""
    f = pp / "input" / "cuts.txt"
    if not f.exists():
        return []
    cuts = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].strip()
        if not line or "-" not in line:
            continue
        def to_s(tok):
            tok = tok.strip()
            if ":" in tok:
                mm, ss = tok.split(":", 1)
                return int(mm) * 60 + float(ss)
            return float(tok)
        a_, b_ = line.split("-", 1)
        cuts.append((to_s(a_), to_s(b_)))
    return cuts


def build_cut_list(dur, silences, manual_cuts, keep_s):
    """Cuts to remove: silence middles (keeping keep_s on each side) + manual cuts."""
    cuts = []
    for s, e in silences:
        head_keep = 0.12 if s <= 0.01 else keep_s     # lead-in: nearly full cut
        tail_keep = 0.25 if e >= dur - 0.01 else keep_s
        cs, ce = s + head_keep, e - tail_keep
        if ce - cs > 0.08:
            cuts.append((cs, ce))
    cuts += manual_cuts
    if not cuts:
        return []
    cuts.sort()
    merged = [list(cuts[0])]
    for s, e in cuts[1:]:
        if s <= merged[-1][1] + 0.02:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [(max(0.0, s), min(dur, e)) for s, e in merged if e - s > 0.05]


def apply_cuts(src: Path, dest: Path, cuts, sample_rate):
    """Concatenate kept intervals -> dest (PCM)."""
    dur = C.ffprobe_duration(src)
    kept = []
    t = 0.0
    for s, e in cuts:
        if s > t:
            kept.append((t, s))
        t = max(t, e)
    if t < dur:
        kept.append((t, dur))
    parts, refs = [], []
    for i, (s, e) in enumerate(kept):
        parts.append(f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS[a{i}]")
        refs.append(f"[a{i}]")
    C.ffmpeg(["-i", str(src), "-filter_complex",
              ";".join(parts) + ";" + "".join(refs) + f"concat=n={len(kept)}:v=0:a=1",
              "-ar", str(sample_rate), "-c:a", "pcm_s16le", str(dest)])
    return kept


def noise_floor_db(src, sr=48000):
    """10th-percentile RMS of 50 ms frames (dBFS) = the level of the pauses. <= -65 dB means a clean recording."""
    import numpy as np
    import subprocess
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-map", "0:a:0", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                       capture_output=True)
    x = np.frombuffer(r.stdout, np.float32)
    if len(x) < sr:
        return None
    n = sr // 20
    fr = x[: len(x) // n * n].reshape(-1, n).astype(np.float64)
    db = 10 * np.log10(np.mean(fr ** 2, axis=1) + 1e-12)
    return float(np.percentile(db, 10))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--input", default=None, help="raw audio/video file (default: auto-detect in input/)")
    ap.add_argument("--no-loudnorm", action="store_true")
    ap.add_argument("--recut", action="store_true",
                    help="re-run ONLY the silence/manual-cut stage on the existing voiceover_clean.wav")
    ap.add_argument("--no-silence-cut", action="store_true")
    ap.add_argument("--force-process", action="store_true", help="run denoise/de-ess/compress even on an already-clean source")
    args = ap.parse_args()

    cfg = C.load_config()
    a = cfg["audio_cleanup"]
    pp = C.project_path(args.name)
    out_dir = pp / "assets" / "voice"
    out_dir.mkdir(parents=True, exist_ok=True)
    work = out_dir / "voice_full_quality.wav"
    clean = out_dir / "voiceover_clean.wav"

    if args.recut:
        # retrofit path: cut the already-clean file, keep everything else
        manual = parse_cuts_file(pp)
        dur = C.ffprobe_duration(clean)
        silences = detect_silences(clean, a.get("silence_threshold_db", -35),
                                   a.get("silence_min_s", 0.5))
        cuts = build_cut_list(dur, silences, manual, a.get("keep_silence_s", 0.3))
        if not cuts:
            print("Nothing to cut.")
            return
        tmp = out_dir / "voiceover_cut.wav"
        kept = apply_cuts(clean, tmp, cuts, a["sample_rate"])
        backup = out_dir / "voiceover_precut.wav"
        if not backup.exists():
            clean.replace(backup)
        tmp.replace(clean)
        removed = dur - C.ffprobe_duration(clean)
        (out_dir / "cutmap.json").write_text(json.dumps({
            "duration_before": round(dur, 3),
            "duration_after": round(C.ffprobe_duration(clean), 3),
            "removed_s": round(removed, 3),
            "cuts": [[round(s, 3), round(e, 3)] for s, e in cuts],
            "kept": [[round(s, 3), round(e, 3)] for s, e in kept],
        }, indent=2), encoding="utf-8")
        for stale in [out_dir / "voice_for_api.m4a", out_dir / "chunks"]:
            if stale.is_file():
                stale.unlink()
            elif stale.is_dir():
                import shutil
                shutil.rmtree(stale, ignore_errors=True)
        C.log(args.name, f"RECUT: removed {removed:.1f}s "
                         f"({len(cuts)} cuts) -> {C.ffprobe_duration(clean):.1f}s; RE-TRANSCRIBE now")
        print(f"\nOK: cut {removed:.1f}s -> {clean}")
        print(f"Next: python pipeline/transcribe.py {args.name}   (timings changed!)")
        return

    src = Path(args.input) if args.input else C.find_input_audio(args.name)
    if not src or not Path(src).exists():
        C.log(args.name, "ERROR no input audio found in input/ (and none passed via --input)")
        raise SystemExit("No input audio. Drop the voiceover into projects/<name>/input/ first.")

    C.log(args.name, f"Audio cleanup: {Path(src).name}")

    # Pass 0: is the source already clean? Denoise / de-ess / compress on a clean voice ADDS artifacts
    # ("shh" hiss heard in Nano Banana 2.1). Clean source -> lossless pass-through (voiceover_raw.wav),
    # loudness is set once at the end by master_audio.py.
    floor = noise_floor_db(src, a["sample_rate"])
    passthrough = (floor is not None and floor <= a.get("clean_floor_db", -65)) and not args.force_process
    raw = out_dir / "voiceover_raw.wav"
    if passthrough:
        C.ffmpeg(["-i", str(src), "-map", "0:a:0", "-ac", "1", "-ar", str(a["sample_rate"]), "-c:a", "pcm_s16le", str(raw)])
        import shutil
        shutil.copy2(raw, work)
        C.log(args.name, f"source noise floor {floor:.1f} dB -> already clean: pass-through, no filters, no loudnorm")
    else:
        raw.unlink(missing_ok=True)  # screen_edit prefers voiceover_raw.wav: never leave a stale/noisy one
        # Pass 1: filter chain -> full-quality wav (mono, 48k)
        filters = build_filter(cfg)
        C.ffmpeg(["-i", str(src), "-af", ",".join(filters),
                  "-ac", "1", "-ar", str(a["sample_rate"]),
                  "-c:a", "pcm_s16le", str(work)])

    # Pass 2: loudness normalization (EBU R128, voiceover standard)
    if passthrough or args.no_loudnorm or not a.get("loudnorm"):
        work.replace(clean)
    else:
        C.ffmpeg(["-i", str(work), "-af", f"loudnorm={a['loudnorm']}",
                  "-ar", str(a["sample_rate"]), "-c:a", "pcm_s16le", str(clean)])
        work.unlink(missing_ok=True)

    # Pass 3: tighten silences (+ manual wrong-take cuts from input/cuts.txt)
    recut_note = ""
    if not args.no_silence_cut and a.get("remove_silence", True):
        manual = parse_cuts_file(pp)
        dur = C.ffprobe_duration(clean)
        silences = detect_silences(clean, a.get("silence_threshold_db", -35),
                                   a.get("silence_min_s", 0.5))
        cuts = build_cut_list(dur, silences, manual, a.get("keep_silence_s", 0.3))
        if cuts:
            tmp = out_dir / "voiceover_cut.wav"
            kept = apply_cuts(clean, tmp, cuts, a["sample_rate"])
            tmp.replace(clean)
            removed = dur - C.ffprobe_duration(clean)
            (out_dir / "cutmap.json").write_text(json.dumps({
                "duration_before": round(dur, 3),
                "duration_after": round(C.ffprobe_duration(clean), 3),
                "removed_s": round(removed, 3),
                "cuts": [[round(s, 3), round(e, 3)] for s, e in cuts],
                "kept": [[round(s, 3), round(e, 3)] for s, e in kept],
            }, indent=2), encoding="utf-8")
            recut_note = f", tightened {removed:.1f}s ({len(cuts)} cuts)"
            C.log(args.name, f"silence/manual cuts removed {removed:.1f}s")

    duration = C.ffprobe_duration(clean)

    # quick loudness stats
    r = C.run(["ffmpeg", "-hide_banner", "-i", str(clean), "-af", "volumedetect",
               "-f", "null", "-"])
    import re
    mean_m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr or "")
    max_m = re.search(r"max_volume:\s*(-?[\d.]+) dB", r.stderr or "")
    analysis = {
        "source": str(src),
        "clean_file": str(clean.relative_to(pp)),
        "duration_s": round(duration, 3),
        "mean_volume_db": float(mean_m.group(1)) if mean_m else None,
        "max_volume_db": float(max_m.group(1)) if max_m else None,
        "loudnorm": a.get("loudnorm", ""),
        "timing_preserved": True,
        "noise_floor_db": round(floor, 1) if floor is not None else None,
        "passthrough": passthrough,
    }
    (out_dir / "voice_analysis.json").write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")

    proj = C.load_project(args.name)
    proj["duration_s"] = round(duration, 3)
    C.save_project(args.name, proj)
    C.update_stage(args.name, "audio_clean", f"cleaned voiceover, {duration:.1f}s")
    print(f"\nOK: {clean}")
    print(f"Duration: {duration:.2f}s | mean {analysis['mean_volume_db']} dB | peak {analysis['max_volume_db']} dB")
    print(f"Next: python pipeline/transcribe.py {args.name}")


if __name__ == "__main__":
    main()
