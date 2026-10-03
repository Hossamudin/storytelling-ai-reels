"""Talking-head cut: apply a voice_edit.py part's keep ranges to the raw camera video.

Usage:
  python pipeline/th_cut.py <name> --part reel [--src input/rawreel.mov] [--w 1080 --h 1920 --fps 30]

Reads  transcript/<part>_words.json  ("keep" ranges written by voice_edit.py)
Writes assets/video/<part>_th.mp4    (H.264, no audio, exactly the edited voice timeline)
       assets/video/<part>_th_seams.json  (edited-timeline seconds of every jump cut -> hide them with
                                            punch-ins / graphic interludes in the composition)
The voice track stays assets/voice/<part>.wav, so picture and voice share one timeline.
Background removal (for "text behind you" / circle presenter / layered depth):
  npx hyperframes remove-background assets/video/<part>_th.mp4 -o assets/video/<part>_th_matte.webm
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--part", required=True)
    ap.add_argument("--src", default=None, help="raw camera video (default: first input/rawreel.* or input/*.mov/mp4)")
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--h", type=int, default=1920)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, default=18)
    a = ap.parse_args()
    pp = C.project_path(a.name)
    if a.src:
        src = pp / a.src
    else:
        cands = sorted(pp.glob("input/rawreel.*")) or sorted(list(pp.glob("input/*.mov")) + list(pp.glob("input/*.mp4")))
        if not cands:
            sys.exit("no camera video in input/ (pass --src)")
        src = cands[0]
    spec = json.loads((pp / f"transcript/{a.part}_words.json").read_text(encoding="utf-8"))
    keep = spec["keep"]
    vf = (f"scale={a.w}:{a.h}:force_original_aspect_ratio=increase:flags=lanczos,crop={a.w}:{a.h},"
          f"fps={a.fps},format=yuv420p")
    parts = ";".join(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS[v{i}]" for i, (s, e) in enumerate(keep))
    fc = parts + ";" + "".join(f"[v{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=1:a=0,{vf}[out]"
    out = pp / f"assets/video/{a.part}_th.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    C.ffmpeg(["-i", str(src), "-filter_complex", fc, "-map", "[out]", "-an", "-c:v", "libx264", "-preset", "medium",
              "-crf", str(a.crf), "-g", str(a.fps), "-movflags", "+faststart", str(out)])
    seams, acc = [], 0.0
    for s, e in keep[:-1]:
        acc += e - s
        seams.append(round(acc, 3))
    (pp / f"assets/video/{a.part}_th_seams.json").write_text(json.dumps({"seams": seams, "duration": round(acc + keep[-1][1] - keep[-1][0], 3)}, indent=1), encoding="utf-8")
    print(f"OK: {out} ({C.ffprobe_duration(out):.2f}s, voice {spec['duration']}s), seams at {seams}")
    C.log(a.name, f"th_cut: {a.part} -> {out.name}")


if __name__ == "__main__":
    main()
