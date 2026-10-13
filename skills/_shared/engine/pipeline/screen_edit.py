"""Screen-recording edit engine: cuts, pause tightening, speed ramps, holds, automatic J/L cuts.

Usage: python engine/pipeline/screen_edit.py <name> [--preview]

Reads projects/<name>/input/screen_edit.json, e.g.
{
  "source": "input/screen.mp4",
  "crop": [0, 178, 1918, 852],               # app region (drop browser chrome + taskbar); null = full frame
  "timeline": [                               # in order; SOURCE seconds
    {"keep": [7.30, 17.14], "label": "signup"},
    {"keep": [75.28, 78.30]}, {"hold": 1.5},  # hold = silent extra time (e.g. under a cutaway)
    {"ramp": [104.0, 112.9], "speed": 4},     # silent sped-up navigation (badge it in the composition)
    {"freeze": [130.0, 141.5], "at": 131.2},  # freeze-and-explain: voice plays over one frozen frame
    {"hold": 6, "at": 160.0, "label": "quiz"},# silent pause on a chosen frame (quiz / recap card on top)
    {"keep": [112.98, 160.62]}
  ],
  "max_pause": 0.9, "keep_pause": 0.4,        # tighten speech pauses longer than max_pause to keep_pause
  "busy_pause_keep": 1.2,                     # ...but keep up to this much when the screen is changing
  "jl": {"l_max": 0.5, "j": 0.2, "busy": 0.6} # L-cut (picture leads) when the gap ends busy, else J-cut
}
Writes (projects/<name>/assets/screen/):
  edited.mp4   video (cropped, 30 fps) with the edited audio muxed in (for preview / Studio)
  edited.wav   edited voice (48 kHz mono)
  edit_map.json  {"segments": [...], "duration": D}  each: kind, src_audio[a,b] | null,
                 src_video[a,b], out[a,b], speed, jl
  words.json   transcript words remapped to output time (from transcript/transcript.json)
Map any source time to output time with map_time() (also used by screen_annot.py).

Why J/L cuts are safe here: within a segment picture and voice keep the same source offset (sync);
only the cut point of the picture moves (by <= 0.6 s) into the removed gap, where the recording
still has valid frames. On screen recordings nobody sees lips, so this reads as a smooth edit.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

FPS = 30


def q(t):  # quantize to frame grid
    return round(t * FPS) / FPS


def silences(src, th=-38, d=0.25):
    r = C.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", f"silencedetect=noise={th}dB:d={d}", "-f", "null", "-"])
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(st, en))


def activity(src, crop, fps=4):
    """Mean abs frame difference per 1/fps s on a small gray proxy (screen change detector)."""
    import numpy as np
    W, H = 320, 142
    vf = (f"crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]}," if crop else "") + f"fps={fps},scale={W}:{H},format=gray"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-vf", vf, "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)
    return [0.0] + list(np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))), fps


def busy(act, fps, a, b, th=0.6):
    i, j = int(a * fps), max(int(a * fps) + 1, int(b * fps))
    vals = act[i:j]
    return bool(vals) and max(vals) > th


def map_time(segments, t):
    """Source time -> output time (audio-anchored; a time inside a removed region snaps to the next segment)."""
    for s in segments:
        if s["kind"] in ("speech", "freeze") and s["src_audio"][0] - 1e-3 <= t <= s["src_audio"][1] + 1e-3:
            return round(s["out0"] + (t - s["src_audio"][0]), 3)
        if s["kind"] == "ramp" and s["src_video"][0] <= t <= s["src_video"][1]:
            return round(s["out0"] + (t - s["src_video"][0]) / s["speed"], 3)
    nxt = [s for s in segments if s["kind"] != "hold" and (s["src_audio"] or s["src_video"])[0] > t]
    return nxt[0]["out0"] if nxt else segments[-1]["out"][1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--preview", action="store_true", help="faster encode (crf 26, ultrafast)")
    a = ap.parse_args()
    pp = C.project_path(a.name)
    spec = json.loads((pp / "input/screen_edit.json").read_text(encoding="utf-8"))
    src = pp / spec["source"]
    crop = spec.get("crop")
    wav = pp / "assets/voice/voiceover_clean.wav"
    out_dir = pp / "assets/screen"
    out_dir.mkdir(parents=True, exist_ok=True)
    sil = silences(wav)
    act, afps = activity(src, crop)
    mp, kp, bk = spec.get("max_pause", 0.9), spec.get("keep_pause", 0.4), spec.get("busy_pause_keep", 1.2)
    jl = spec.get("jl", {"l_max": 0.5, "j": 0.2, "busy": 0.6})

    # 1) expand timeline into atomic pieces with boundary types
    pieces = []  # dict(kind, a, b, speed, boundary_before)
    for item in spec["timeline"]:
        if "keep" in item:
            s, e = item["keep"]
            cuts = []
            for x, y in sil:
                x, y = max(x, s), min(y, e)
                if y - x <= mp:
                    continue
                keep = bk if busy(act, afps, x, y) else kp
                if y - x > keep:
                    cuts.append((x + keep / 2, y - keep / 2))
            t = s
            first = True
            for x, y in cuts:
                pieces.append({"kind": "speech", "a": t, "b": x, "speed": 1, "boundary": "cut" if first else "pause"})
                first = False
                t = y
            pieces.append({"kind": "speech", "a": t, "b": e, "speed": 1, "boundary": "cut" if first else "pause"})
        elif "ramp" in item:
            s, e = item["ramp"]
            pieces.append({"kind": "ramp", "a": s, "b": e, "speed": item.get("speed", 4), "boundary": "hard"})
        elif "hold" in item:  # silent pause (cutaway, quiz, recap); "at" = source frame to freeze on
            pieces.append({"kind": "hold", "a": None, "b": None, "dur": item["hold"], "at": item.get("at"), "speed": 1, "boundary": "hard"})
        elif "freeze" in item:  # freeze-and-explain: voice [a,b] keeps playing over one frozen frame
            s, e = item["freeze"]
            pieces.append({"kind": "freeze", "a": s, "b": e, "at": item.get("at", s), "speed": 1, "boundary": "cut"})

    # 2) quantize, place on output timeline, decide J/L offsets at "cut" boundaries
    T = 0.0
    segs = []
    for i, p in enumerate(pieces):
        if p["kind"] in ("speech", "freeze"):
            L = q(p["b"] - p["a"])
        elif p["kind"] == "ramp":
            L = q((p["b"] - p["a"]) / p["speed"])
        else:
            L = q(p["dur"])
        d = 0.0
        prev = pieces[i - 1] if i else None
        if i and p["boundary"] == "cut" and p["kind"] == "speech" and prev["kind"] == "speech":
            gap_a, gap_b = prev["b"], p["a"]
            if gap_b - gap_a > 0.15:
                if busy(act, afps, max(gap_a, gap_b - jl.get("busy", 0.6)), gap_b):
                    d = -q(min(jl.get("l_max", 0.5), (gap_b - gap_a) * 0.5))   # L-cut: picture leads
                else:
                    d = q(min(jl.get("j", 0.2), (gap_b - gap_a) * 0.5))          # J-cut: voice leads
        segs.append({"kind": p["kind"], "src_a": p["a"], "at": p.get("at"), "L": L, "out0": q(T), "d": d, "speed": p["speed"],
                     "boundary": p["boundary"] if i else "start"})
        T += L
    for i, s in enumerate(segs):
        d_in = s["d"]
        d_out = segs[i + 1]["d"] if i + 1 < len(segs) else 0.0
        if s["kind"] == "speech":
            s["src_video"] = [round(s["src_a"] + d_in, 3), round(s["src_a"] + s["L"] + d_out, 3)]
            s["src_audio"] = [round(s["src_a"], 3), round(s["src_a"] + s["L"], 3)]
        elif s["kind"] == "ramp":
            s["src_video"] = [round(s["src_a"], 3), round(s["src_a"] + s["L"] * s["speed"], 3)]
            s["src_audio"] = None
        elif s["kind"] == "freeze":
            s["src_video"] = [round(s["at"], 3), round(s["at"], 3)]
            s["src_audio"] = [round(s["src_a"], 3), round(s["src_a"] + s["L"], 3)]
        else:  # hold: still of "at" (or the previous picture's last frame)
            prev_end = s["at"] if s.get("at") is not None else (segs[i - 1]["src_video"][1] if i else 0)
            s["src_video"] = [round(prev_end, 3), round(prev_end, 3)]
            s["src_audio"] = None
        s["out"] = [round(s["out0"] + d_in, 3), round(s["out0"] + s["L"] + d_out, 3)]
        s["jl"] = "L" if d_in < 0 else ("J" if d_in > 0 else "")
    total = q(T)

    # 3) render video segments (exact frame counts) then concat
    tmp = out_dir / "_segs"
    tmp.mkdir(exist_ok=True)
    crf, preset = ("26", "ultrafast") if a.preview else ("16", "medium")
    cropf = f"crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]}," if crop else ""
    lst = []
    src_dur = C.ffprobe_duration(src)
    for i, s in enumerate(segs):
        va, vb = s["src_video"]
        n = int(round((s["out"][1] - s["out"][0]) * FPS))
        if n <= 0:
            continue
        f = tmp / f"v{i:03d}.mp4"
        if s["kind"] in ("hold", "freeze"):  # still frame (never reads past the end of the source)
            still = tmp / f"h{i:03d}.png"
            C.ffmpeg(["-ss", f"{min(va, src_dur - 0.1):.3f}", "-i", str(src), "-vf", cropf.rstrip(",") or "null", "-frames:v", "1", str(still)])
            C.ffmpeg(["-loop", "1", "-i", str(still), "-vf", f"fps={FPS},format=yuv420p", "-frames:v", str(n), "-an",
                      "-c:v", "libx264", "-crf", crf, "-preset", preset, "-r", str(FPS), str(f)])
            lst.append(f"file '{f.as_posix()}'")
            continue
        sp = s["speed"] if s["kind"] == "ramp" else 1
        vf = cropf + (f"setpts=PTS/{sp}," if sp != 1 else "") + f"fps={FPS},format=yuv420p"
        C.ffmpeg(["-ss", f"{va:.3f}", "-i", str(src), "-vf", vf, "-frames:v", str(n), "-an",
                  "-c:v", "libx264", "-crf", crf, "-preset", preset, "-r", str(FPS), str(f)])
        lst.append(f"file '{f.as_posix()}'")
    (tmp / "list.txt").write_text("\n".join(lst), encoding="utf-8")
    vonly = out_dir / "_video.mp4"
    C.ffmpeg(["-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-c", "copy", str(vonly)])

    # 4) audio: speech pieces with 10 ms seam fades, silence for ramps/holds
    parts, refs = [], []
    for i, s in enumerate(segs):
        L = s["L"]
        if s["src_audio"]:
            x, y = s["src_audio"]
            parts.append(f"[0:a]atrim={x:.3f}:{y:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, L - 0.01):.3f}:d=0.01[a{i}]")
        else:
            parts.append(f"anullsrc=r=48000:cl=mono,atrim=0:{L:.3f}[a{i}]")
        refs.append(f"[a{i}]")
    fc = ";".join(parts) + ";" + "".join(refs) + f"concat=n={len(refs)}:v=0:a=1[out]"
    ewav = out_dir / "edited.wav"
    C.ffmpeg(["-i", str(wav), "-filter_complex", fc, "-map", "[out]", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(ewav)])
    C.ffmpeg(["-i", str(vonly), "-i", str(ewav), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out_dir / "edited.mp4")])

    # 5) maps
    em = {"duration": total, "fps": FPS, "crop": crop, "quality": "preview" if a.preview else "final",
          "segments": [{k: s.get(k) for k in ("kind", "src_audio", "src_video", "out", "out0", "speed", "jl", "boundary", "at")} for s in segs]}
    (out_dir / "edit_map.json").write_text(json.dumps(em, indent=1), encoding="utf-8")
    tr = pp / "transcript/transcript.json"
    if tr.exists():
        words = [w for sg in json.loads(tr.read_text(encoding="utf-8"))["segments"] for w in sg["words"]]
        out_words = []
        for w in words:
            for s in em["segments"]:
                if s["src_audio"] and s["src_audio"][0] - 0.02 <= w["s"] < s["src_audio"][1]:
                    out_words.append({"w": w["w"], "src": w["s"], "s": round(s["out0"] + max(0, w["s"] - s["src_audio"][0]), 3),
                                      "e": round(s["out0"] + min(w["e"], s["src_audio"][1]) - s["src_audio"][0], 3)})
                    break
        (out_dir / "words.json").write_text(json.dumps(out_words, ensure_ascii=False, indent=1), encoding="utf-8")
    n_j = sum(1 for s in segs if s["jl"] == "J")
    n_l = sum(1 for s in segs if s["jl"] == "L")
    src_d = C.ffprobe_duration(src)
    print(f"OK: {src_d:.1f}s -> {total:.2f}s | {len(segs)} segments | J-cuts {n_j}, L-cuts {n_l} | "
          f"ramps {sum(1 for s in segs if s['kind'] == 'ramp')} | holds {sum(1 for s in segs if s['kind'] == 'hold')}")
    print(f"  -> {out_dir / 'edited.mp4'}")


if __name__ == "__main__":
    main()
