"""Retrofit: re-time transcript.json + storyboard.json to a CUT voiceover.

Usage: python pipeline/retime.py <name>   (requires assets/voice/cutmap.json)

Maps every timestamp through the cut list, drops words fully inside cuts,
shrinks/drops scenes that lost their time, keeps scene IDs stable (assets stay wired).
Backs up originals as *.pre-retime.json.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def load_cutmap(pp):
    cm = pp / "assets" / "voice" / "cutmap.json"
    if not cm.exists():
        raise SystemExit("No cutmap.json — run clean_audio.py <name> --recut first.")
    return json.loads(cm.read_text(encoding="utf-8"))


def mapper(cuts):
    def f(t):
        return t - sum(max(0.0, min(t, e) - s) for s, e in cuts)
    return f


def main():
    args = sys.argv[1:]
    sb_only = "--sb-only" in args
    args = [a for a in args if not a.startswith("--")]
    name = args[0]
    pp = C.project_path(name)
    cm = load_cutmap(pp)
    cuts = cm["cuts"]
    f = mapper(cuts)
    new_dur = round(cm["duration_after"], 2)
    C.log(name, f"retiming: {len(cuts)} cuts, {cm['removed_s']}s removed, new duration {new_dur}s")

    # ---- transcript (skip if it was re-transcribed from the cut audio)
    if not sb_only:
        tpath = pp / "transcript" / "transcript.json"
        t = json.loads(tpath.read_text(encoding="utf-8"))
        shutil.copy2(tpath, pp / "transcript" / "transcript.pre-retime.json")
        segs_out = []
        for seg in t["segments"]:
            words = []
            for w in seg.get("words") or []:
                s2, e2 = f(float(w["s"])), f(float(w["e"]))
                if e2 - s2 < 0.02:      # word fell inside a cut
                    continue
                words.append({"w": w["w"], "s": round(s2, 2), "e": round(e2, 2)})
            if not words:
                continue
            segs_out.append({
                "start": words[0]["s"], "end": words[-1]["e"],
                "text": " ".join(w["w"] for w in words), "words": words,
            })
        t["segments"] = segs_out
        t["duration_s"] = new_dur
        t["full_text"] = " ".join(s["text"] for s in segs_out)
        tpath.write_text(json.dumps(t, indent=2, ensure_ascii=False), encoding="utf-8")
        kept_words = sum(len(s["words"]) for s in segs_out)
        print(f"transcript: {len(segs_out)} segments, {kept_words} words retimed")

    # ---- storyboard
    spath = pp / "storyboard.json"
    sb = json.loads(spath.read_text(encoding="utf-8"))
    shutil.copy2(spath, pp / "storyboard.pre-retime.json")
    out = []
    for s in sb["scenes"]:
        s2s, s2e = round(f(float(s["start"])), 2), round(f(float(s["end"])), 2)
        if s2e - s2s < 0.45 and out:          # scene lost its time -> fold into previous
            out[-1]["end"] = max(out[-1]["end"], s2e)
            C.log(name, f"{s['id']}: folded into {out[-1]['id']} (too short after cut)")
            continue
        s["start"], s["end"] = s2s, s2e
        out.append(s)
    if out:
        out[-1]["end"] = new_dur
    hook_ids = [s["id"] for s in out if s.get("beat") == "hook"]
    sb["scenes"] = out
    sb["total_duration"] = new_dur
    sb["hook"] = {"end_s": round(max((s["end"] for s in out if s.get("beat") == "hook"), default=0.0), 2),
                  "scene_ids": hook_ids}
    spath.write_text(json.dumps(sb, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"storyboard: {len(out)} scenes retimed (ids stable)")

    proj = C.load_project(name)
    proj["duration_s"] = new_dur
    C.save_project(name, proj)
    C.log(name, f"retimed to {new_dur}s — now re-run captions + assemble")
    print(f"\nNext: python pipeline/captions.py {name} && python pipeline/assemble.py {name}")


if __name__ == "__main__":
    main()
