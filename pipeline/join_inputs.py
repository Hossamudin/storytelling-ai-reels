"""Join several inputs (voice-only files + screen recordings) into ONE source timeline without touching the voice.

Usage: python pipeline/join_inputs.py <name> <file1> <file2> ... [--gap 1.0]
  audio-only files (m4a/wav/mp3) get a black picture; videos are scaled to 1920x1080 @30.

Writes (projects/<name>/input/):
  screen.mp4        picture timeline (+ a preview AAC track; never cut voice from it)
  voice_joined.wav  48 kHz mono PCM: each file's audio decoded straight from the ORIGINAL and placed at its offset
  SOURCE_MAP.md     where each file starts
Then: python pipeline/clean_audio.py <name> --input projects/<name>/input/voice_joined.wav --no-silence-cut
(clean sources pass through untouched -> assets/voice/voiceover_raw.wav, which screen_edit.py cuts from).

Why: joining audio inside an ffmpeg concat graph together with video inserted/dropped samples whenever the
screen recorder's audio timestamps were irregular -> broadband "shh" hiss (Nano Banana 2.1, Oct 2026).
The voice is verified piece by piece: >12 kHz band energy must match the original within 1.5 dB.
"""
import argparse
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

SR = 48000
AUDIO_EXT = {".m4a", ".wav", ".mp3", ".aac", ".flac", ".ogg", ".opus"}


def dur(f):
    return C.ffprobe_duration(f)


def decode(f):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).astype(np.float64)


def hf_db(s):
    S = np.abs(np.fft.rfft(s)) ** 2
    f = np.fft.rfftfreq(len(s), 1 / SR)
    return 10 * np.log10(S[f >= 12000].sum() / (S.sum() + 1e-20) + 1e-20)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--gap", type=float, default=1.0)
    a = ap.parse_args()
    pp = C.project_path(a.name)
    files = [Path(f) for f in a.files]
    inp = pp / "input"
    inp.mkdir(parents=True, exist_ok=True)

    # 1) offsets (video length for videos, audio length for audio-only), frame-aligned
    offs, t, lens = [], 0.0, []
    for f in files:
        L = dur(f)
        L = round(L * 30) / 30
        offs.append(round(t, 3))
        lens.append(L)
        t += L + a.gap
    total = round(t - a.gap, 3)

    # 2) picture: video-only concat (audio NEVER goes through this graph)
    args, fc, k = [], [], 0
    for f, L in zip(files, lens):
        if f.suffix.lower() in AUDIO_EXT:
            args += ["-f", "lavfi", "-t", f"{L:.3f}", "-i", "color=c=black:s=1920x1080:r=30"]
        else:
            args += ["-i", str(f)]
        fc.append(f"[{k}:v]scale=1920:1080:flags=lanczos,fps=30,setsar=1,trim=duration={L:.3f},setpts=PTS-STARTPTS[v{k}]")
        k += 1
    gap_i = k
    args += ["-f", "lavfi", "-t", f"{a.gap:.3f}", "-i", "color=c=black:s=1920x1080:r=30"]
    ng = len(files) - 1  # gaps: one black clip split into n-1 copies
    if ng:
        fc.append(f"[{gap_i}:v]split={ng}" + "".join(f"[g{i}]" for i in range(ng)))
    seq = "".join(f"[v{i}]" + (f"[g{i}]" if i < ng else "") for i in range(len(files)))
    fc.append(f"{seq}concat=n={len(files) + ng}:v=1:a=0[v]")
    vtmp = inp / "_picture.mp4"
    C.ffmpeg([*args, "-filter_complex", ";".join(fc), "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
              "-pix_fmt", "yuv420p", str(vtmp)], timeout=3600)

    # 3) voice: decode each original, place at its offset (sample exact), verify
    out = np.zeros(int(round(total * SR)) + SR)
    rep = []
    for f, off, L in zip(files, offs, lens):
        x = decode(f)
        i0 = int(round(off * SR))
        n = min(len(x), int(round(L * SR)), len(out) - i0)
        out[i0:i0 + n] = x[:n]
        m = n // 2
        w0, w1 = x[m:m + 6 * SR], out[i0 + m:i0 + m + 6 * SR]
        d = hf_db(w1) - hf_db(w0)
        rep.append((f.name, off, L, d))
        if abs(d) > 1.5:
            raise SystemExit(f"voice check failed for {f.name}: HF band differs by {d:+.1f} dB")
    out = out[: int(round(total * SR))]
    pk = np.max(np.abs(out))
    if pk > 0.99:
        out *= 0.966 / pk * min(pk, 1.035)  # tame AAC decode overshoot only
    vwav = inp / "voice_joined.wav"
    with wave.open(str(vwav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.clip(np.round(out * 32767), -32768, 32767).astype("<i2").tobytes())

    # 4) preview mux (AAC is fine for previews; cutting always uses voice_joined.wav -> voiceover_raw.wav)
    C.ffmpeg(["-i", str(vtmp), "-i", str(vwav), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
              "-shortest", str(inp / "screen.mp4")])
    vtmp.unlink(missing_ok=True)
    lines = ["# input/screen.mp4 + input/voice_joined.wav — source map (seconds)", "", "| range | file |", "|---|---|"]
    for name, off, L, d in rep:
        lines.append(f"| {off:.3f}–{off + L:.3f} | {name} (voice HF check {d:+.2f} dB) |")
    (inp / "SOURCE_MAP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for r in rep:
        print(f"  {r[1]:8.3f}s  {r[2]:8.3f}s  HF {r[3]:+.2f} dB  {r[0]}")
    print(f"OK: {total:.3f}s -> input/screen.mp4 + input/voice_joined.wav")
    print(f"Next: python pipeline/clean_audio.py {a.name} --input projects/{a.name}/input/voice_joined.wav --no-silence-cut")


if __name__ == "__main__":
    main()
