"""Pre-render gate: catch everything that can block or degrade a final render BEFORE it starts.

Usage: python pipeline/preflight.py <name> [--part composition] [--no-check]

Fails (exit 1) on:
  - any remote URL in scripts/styles/media/url() (renders must not depend on a CDN — a transient
    jsDelivr failure blocked a render with `sub_timeline_script_failure`)
  - referenced local files that don't exist (assets/...)
  - screen projects: edited recording is the --preview encode, or the copy in the part is stale
  - screen projects: film grain enabled over the recording (chrome.json "grain" must be false)
  - root duration shorter than the last scene / voice end
  - `npx hyperframes check` not clean (0 errors, 0 warnings)
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

REMOTE = re.compile(r'''(?:src|href)\s*=\s*["'](https?://[^"']+)["']|url\(\s*["']?(https?://[^)"']+)''', re.I)
LOCAL = re.compile(r'''(?:src|href)\s*=\s*["'](assets/[^"'#?]+)["']''', re.I)


def run_check(part_dir):
    r = C.run(["npx", "hyperframes", "check", "--timeout", "30000"], cwd=str(part_dir), timeout=1800)
    out = (r.stdout or "") + (r.stderr or "")
    errs = sum(int(x) for x in re.findall(r"(\d+) error\(s\)", out))
    warns = sum(int(x) for x in re.findall(r"(\d+) warning\(s\)", out))
    return errs, warns, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--part", default="composition")
    ap.add_argument("--no-check", action="store_true")
    a = ap.parse_args()
    pp = C.project_path(a.name)
    part = pp / a.part
    problems, notes = [], []

    files = [part / "index.html"] + sorted((part / "compositions").glob("*.html")) + sorted((part / "assets/css").glob("*.css"))
    for f in files:
        if not f.exists():
            continue
        s = f.read_text(encoding="utf-8", errors="replace")
        s_nocomment = re.sub(r"<!--.*?-->", "", s, flags=re.S)
        for m in REMOTE.finditer(s_nocomment):
            url = m.group(1) or m.group(2)
            if "hyperframes.heygen.com/schema" in url or url.startswith("http://www.w3.org"):
                continue
            problems.append(f"remote dependency in {f.relative_to(pp)}: {url}  -> vendor it into assets/")
        for m in LOCAL.finditer(s_nocomment):
            if not (part / m.group(1)).exists():
                problems.append(f"missing file referenced in {f.relative_to(pp)}: {m.group(1)}")

    # screen-recording projects
    em_p = pp / "assets/screen/edit_map.json"
    if (part / "compositions/screen.html").exists() and em_p.exists():
        em = json.loads(em_p.read_text(encoding="utf-8"))
        if em.get("quality", "preview") != "final":
            problems.append("screen edit is the PREVIEW encode -> run: python pipeline/screen_edit.py "
                            f"{a.name}  (no --preview), then copy assets/screen/edited.mp4 into {a.part}/assets/screen/")
        src, dst = pp / "assets/screen/edited.mp4", part / "assets/screen/edited.mp4"
        if src.exists() and dst.exists() and src.stat().st_size != dst.stat().st_size:
            problems.append(f"{a.part}/assets/screen/edited.mp4 is stale (differs from assets/screen/edited.mp4) -> copy it")
        ch = json.loads((part / "chrome.json").read_text(encoding="utf-8")) if (part / "chrome.json").exists() else {}
        if ch.get("grain", True) is not False:
            problems.append('grain is ON over a screen recording -> chrome.json "grain": false, then motion_sync.py')

    # durations
    html = (part / "index.html").read_text(encoding="utf-8")
    root = re.search(r'<div[^>]*?\sid="root"[^>]*>', html).group(0)
    total = float(re.search(r'data-duration="([\d.]+)"', root).group(1))
    ends = [float(st) + float(du) for st, du in re.findall(r'data-composition-src="[^"]+"[^>]*?data-start="([\d.]+)"[^>]*?data-duration="([\d.]+)"', html)]
    vo = re.search(r'<audio[^>]*\sid="vo"[^>]*>', html)
    if vo:
        st = float(re.search(r'data-start="([\d.]+)"', vo.group(0)).group(1))
        du = float(re.search(r'data-duration="([\d.]+)"', vo.group(0)).group(1))
        ends.append(st + du)
    if ends and total + 0.05 < max(ends):
        problems.append(f"root duration {total}s < content end {max(ends):.2f}s -> run motion_sync.py")
    notes.append(f"duration {total}s, {len(ends)} timed hosts/voice")

    if not a.no_check:
        errs, warns, out = run_check(part)
        if errs or warns:
            tail = "\n".join(l for l in out.splitlines() if "✗" in l or "⚠" in l)[:1500]
            problems.append(f"hyperframes check: {errs} error(s), {warns} warning(s)\n{tail}")
        else:
            notes.append("hyperframes check: clean")

    for n in notes:
        print("  ·", n)
    if problems:
        print("\nPREFLIGHT FAILED:")
        for p in problems:
            print("  ✗", p)
        sys.exit(1)
    print("\nPREFLIGHT OK")


if __name__ == "__main__":
    main()
