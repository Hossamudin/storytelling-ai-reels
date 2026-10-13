"""Tiny numpy-only acoustic matcher: does short clip A sound like the START of clip B? (stutter / restart detection)

mfcc(x) -> (frames, 13) with per-clip mean/var normalisation; prefix_cost(A, B) = DTW cost of A against B's first
1.6 x len(A) frames, open end, normalised by path length. Same word spoken twice ~ 0.5-0.75; different words ~ 0.9+.
"""
import subprocess

import numpy as np

SR = 16000


def load(src, a, b):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(src), "-ac", "1", "-ar", str(SR),
                        "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.float32).astype(np.float64)


def _mel_fb(n_fft=512, n_mels=40, fmin=60, fmax=7600):
    hz = lambda m: 700 * (10 ** (m / 2595) - 1)
    mel = lambda f: 2595 * np.log10(1 + f / 700)
    pts = hz(np.linspace(mel(fmin), mel(fmax), n_mels + 2))
    bins = np.floor((n_fft + 1) * pts / SR).astype(int)
    fb = np.zeros((n_mels, n_fft // 2 + 1))
    for i in range(n_mels):
        l, c, r = bins[i], bins[i + 1], bins[i + 2]
        fb[i, l:c] = (np.arange(l, c) - l) / max(c - l, 1)
        fb[i, c:r] = (r - np.arange(c, r)) / max(r - c, 1)
    return fb


_FB = _mel_fb()
_DCT = np.cos(np.pi / 40 * (np.arange(40) + 0.5)[None, :] * np.arange(13)[:, None])


def mfcc(x):
    win, hop = 400, 160
    if len(x) < win:
        x = np.pad(x, (0, win - len(x)))
    n = 1 + (len(x) - win) // hop
    fr = np.stack([x[i * hop:i * hop + win] for i in range(n)]) * np.hamming(win)
    P = np.abs(np.fft.rfft(fr, 512)) ** 2
    m = np.log(P @ _FB.T + 1e-10)
    c = m @ _DCT.T
    e = 10 * np.log10(np.mean(fr ** 2, axis=1) + 1e-12)
    c = c[e > e.max() - 35]  # drop near-silent frames
    return (c - c.mean(0)) / (c.std(0) + 1e-6)


def prefix_cost(A, B):
    if len(A) < 5 or len(B) < 5:
        return 9.0
    B = B[: int(len(A) * 1.6) + 2]
    D = np.sqrt(((A[:, None, :] - B[None, :, :]) ** 2).sum(-1)) / np.sqrt(A.shape[1])
    n, m = D.shape
    acc = np.full((n + 1, m + 1), np.inf)
    ln = np.zeros((n + 1, m + 1))
    acc[0, 0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            opts = ((acc[i - 1, j - 1], ln[i - 1, j - 1]), (acc[i - 1, j], ln[i - 1, j]), (acc[i, j - 1], ln[i, j - 1]))
            k = min(range(3), key=lambda q: opts[q][0])
            acc[i, j] = D[i - 1, j - 1] + opts[k][0]
            ln[i, j] = opts[k][1] + 1
    lo = min(max(1, int(n * 0.6)), m)
    cost = acc[n, lo:] / np.maximum(ln[n, lo:], 1)
    return float(np.min(cost)) if len(cost) else 9.0
