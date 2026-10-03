"""Measure every SFX in the motion kit and write recommended gains (kit/motion/sfx/levels.json).

Usage: python pipeline/sfx_levels.py [--dir kit/motion/sfx]

Why: library/generated SFX range from -4 to -36 LUFS. A flat data-volume lets impacts drown the
voice. Gains here put each effect near config motion.sfx_target_lufs (~10 dB under a -16 LUFS
voice). Very short clips (< 0.4 s gate) fall back to a peak target. motion_sync.py multiplies these
base gains by the per-cue accent in cues.json.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def measure(path: Path):
    r = C.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"])
    err = r.stderr or ""
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)
    lufs = float(i[-1]) if i else -70.0
    peak = float(p[-1]) if p else 0.0
    return lufs, peak


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="kit/motion/sfx")
    args = ap.parse_args()
    cfg = C.load_config()
    m = cfg.get("motion", {})
    target = m.get("sfx_target_lufs", -27)
    peak_target = m.get("sfx_peak_target_dbfs", -12)
    root = Path(args.dir)
    out = {}
    for f in sorted(list(root.rglob("*.mp3")) + list(root.rglob("*.wav"))):
        lufs, peak = measure(f)
        if lufs > -60:
            gain_db = target - lufs
        else:  # too short for gated loudness: use peak
            gain_db = peak_target - peak
        gain = round(min(1.0, max(0.03, 10 ** (gain_db / 20))), 3)
        key = f.relative_to(root).as_posix()
        out[key] = {"lufs": lufs, "peak_dbfs": peak, "gain": gain,
                    "duration": round(C.ffprobe_duration(f), 3)}
        print(f"{key:40s} {lufs:7.1f} LUFS  peak {peak:6.1f}  -> gain {gain}")
    (root / "levels.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nOK: {len(out)} files -> {root / 'levels.json'}")


if __name__ == "__main__":
    main()
