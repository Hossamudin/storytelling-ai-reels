"""Master a rendered MP4's audio to the delivery target (default -14 LUFS, true peak -1.2 dB).

Usage: python pipeline/master_audio.py <input.mp4> [--lufs -14] [--tp -1.2] [--out <file>]

Two-pass ffmpeg loudnorm (measure, then linear normalize); the video stream is copied untouched.
Output defaults to <input>_master.mp4. Run it on every final render before upload.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    cfg = C.load_config().get("motion", {})
    ap.add_argument("--lufs", type=float, default=cfg.get("master_lufs", -14))
    ap.add_argument("--tp", type=float, default=cfg.get("master_true_peak", -1.2))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    src = Path(a.input)
    dest = Path(a.out) if a.out else src.with_name(src.stem + "_master.mp4")
    ln = f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11"
    r = C.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", ln + ":print_format=json", "-f", "null", "-"])
    meas = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))
    f2 = (f"{ln}:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:measured_LRA={meas['input_lra']}"
          f":measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    C.ffmpeg(["-i", str(src), "-c:v", "copy", "-af", f2, "-ar", "48000", "-c:a", "aac", "-b:a", "256k", str(dest)])
    r2 = C.run(["ffmpeg", "-hide_banner", "-i", str(dest), "-af", "ebur128=peak=true", "-f", "null", "-"])
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r2.stderr)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r2.stderr)
    print(f"in {meas['input_i']} LUFS / TP {meas['input_tp']}  ->  out {i[-1] if i else '?'} LUFS / peak {p[-1] if p else '?'} dBFS")
    print(f"OK: {dest}")


if __name__ == "__main__":
    main()
