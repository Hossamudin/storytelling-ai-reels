"""Offline end-to-end selftest (mock mode, no API keys needed).

Creates a temp project (_selftest), generates a 14s test tone voiceover,
runs: clean_audio -> transcribe(mock) -> plan_scenes(mock) -> captions ->
assemble, then validates the composition with `npx hyperframes check`.

Usage: python pipeline/selftest.py [--keep] [--skip-check]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

NAME = "_selftest"


def step(label, fn):
    print(f"\n--- {label} ---")
    fn()
    print(f"OK: {label}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--skip-check", action="store_true")
    args = ap.parse_args()

    pp = C.project_path(NAME)
    if pp.exists():
        import shutil
        shutil.rmtree(pp, ignore_errors=True)

    results = []

    def run_script(label, cmd):
        r = C.run([sys.executable] + cmd, cwd=C.ROOT, timeout=600)
        ok = r.returncode == 0
        results.append((label, ok))
        print(r.stdout[-2500:] if ok else f"STDOUT:\n{r.stdout[-1500:]}\nSTDERR:\n{r.stderr[-2500:]}")
        if not ok:
            raise SystemExit(f"FAILED at {label}")

    try:
        step("create project", lambda: run_script("new_project", ["pipeline/new_project.py", NAME, "--title", "Selftest"]))
        step("synth voiceover", lambda: (
            (pp / "input").mkdir(parents=True, exist_ok=True),
            C.ffmpeg(["-f", "lavfi", "-i", "sine=frequency=190:duration=14",
                      "-c:a", "pcm_s16le", str(pp / "input" / "voice.wav")], timeout=120),
        ))
    except Exception as e:
        raise SystemExit(f"FAILED to synth test voiceover: {e}")

    step("clean audio", lambda: run_script("clean_audio", ["pipeline/clean_audio.py", NAME]))
    step("transcribe (mock)", lambda: run_script("transcribe", ["pipeline/transcribe.py", NAME, "--provider", "mock"]))
    step("plan scenes (mock)", lambda: run_script("plan_scenes", ["pipeline/plan_scenes.py", NAME, "--provider", "mock"]))
    step("captions", lambda: run_script("captions", ["pipeline/captions.py", NAME]))

    # storyboard auto-approval for the offline test only
    sb_path = pp / "storyboard.json"
    sb = json.loads(sb_path.read_text(encoding="utf-8"))
    sb["status"] = "approved"
    sb_path.write_text(json.dumps(sb, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n--- approve storyboard (offline auto) ---\nOK")

    step("generate assets (mock)", lambda: run_script("generate_assets",
          ["pipeline/generate_assets.py", NAME, "--mock", "--no-video"]))
    step("assemble", lambda: run_script("assemble", ["pipeline/assemble.py", NAME]))

    ok_all = True
    if not args.skip_check:
        print("\n--- npx hyperframes check ---")
        r = C.run(["npx", "-y", "hyperframes", "check"], cwd=pp / "composition", timeout=420)
        print((r.stdout or "")[-3000:])
        print((r.stderr or "")[-1000:])
        findings = "?"
        ok_all = r.returncode == 0
        results.append(("hyperframes check", ok_all))

    print("\n========== SELFTEST SUMMARY ==========")
    for label, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not args.keep:
        import shutil
        shutil.rmtree(pp, ignore_errors=True)
        print(f"(test project cleaned; keep with --keep)")
    print("======================================")
    if not ok_all:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
