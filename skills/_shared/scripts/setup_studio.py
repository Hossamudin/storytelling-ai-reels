"""Create / upgrade / inspect the creator's Video Studio — one folder shared by every video skill.

Usage:
  python setup_studio.py status                         # is there a studio? where? engine version, keys, profile
  python setup_studio.py init [--home DIR] [--language ar]
                                                        # create it (default ~/VideoStudio) or upgrade its engine
  python setup_studio.py brand                          # brand/brand.json -> brand/brand.css + config brand block
  python setup_studio.py keys                           # which keys are set (presence only) + where to put them

The studio location is remembered in ~/.video-studio.json, so every skill finds the same studio.
Set VIDEO_STUDIO_HOME to use a specific studio instead (it is not written to the pointer).
All later commands run from the studio folder:  python engine/pipeline/<script>.py ...
"""
import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SKILL = Path(__file__).resolve().parent.parent           # <skill>/
ENGINE_SRC = SKILL / "engine"
ASSETS = SKILL / "assets"
PTR = Path.home() / ".video-studio.json"
KEYS = ["OPENAI_API_KEY", "GEMINI_API_KEY", "ELEVENLABS_API_KEY"]


def ver(p):
    try:
        return tuple(int(x) for x in (p / "VERSION").read_text().strip().split("."))
    except Exception:
        return (0,)


def find_home():
    import os
    if os.environ.get("VIDEO_STUDIO_HOME"):  # explicit studio (tests, several studios on one machine)
        h = Path(os.environ["VIDEO_STUDIO_HOME"]).expanduser().resolve()
        return h if (h / "studio.json").exists() else None
    if PTR.exists():
        try:
            h = Path(json.loads(PTR.read_text(encoding="utf-8"))["home"])
            if (h / "studio.json").exists():
                return h
        except Exception:
            pass
    return None


def status():
    h = find_home()
    if not h:
        print("NO STUDIO YET. Run: python setup_studio.py init  (after the onboarding conversation)")
        return 1
    st = json.loads((h / "studio.json").read_text(encoding="utf-8"))
    cfg = json.loads((h / "config/config.json").read_text(encoding="utf-8")) if (h / "config/config.json").exists() else {}
    prof = (h / "profile.md").read_text(encoding="utf-8") if (h / "profile.md").exists() else ""
    todo = prof.count("<fill")
    lib = h / "library/index.jsonl"
    n_lib = sum(1 for l in lib.read_text(encoding="utf-8").splitlines() if l.strip()) if lib.exists() else 0
    projects = [p.name for p in (h / "projects").iterdir() if p.is_dir()] if (h / "projects").exists() else []
    print(f"STUDIO: {h}")
    print(f"  engine {'.'.join(map(str, ver(h / 'engine')))} (this skill ships {'.'.join(map(str, ver(ENGINE_SRC)))})"
          + ("  -> run init to upgrade" if ver(ENGINE_SRC) > ver(h / "engine") else ""))
    print(f"  language: {cfg.get('language', '?')} · brand: {cfg.get('brand', {}).get('name') or '(not set)'}")
    print(f"  profile.md: {'complete' if prof and not todo else f'{todo} field(s) still to fill' if prof else 'missing'}")
    print(f"  library: {n_lib} assets · projects: {len(projects)} {projects[-5:] if projects else ''}")
    print(f"  created {st.get('created')} · skills used: {', '.join(st.get('skills', [])) or '-'}")
    keys(h, quiet=True)
    return 0


def keys(h=None, quiet=False):
    import os
    h = h or find_home()
    kf = h / "config/api_keys.json" if h else None
    data = json.loads(kf.read_text(encoding="utf-8")) if kf and kf.exists() else {}
    have = {k: bool(os.environ.get(k) or data.get(k)) for k in KEYS}
    print("  keys: " + "  ".join(f"{'✓' if v else '✗'} {k}" for k, v in have.items()))
    if not quiet and kf:
        print(f"  Put keys in {kf} (this file is gitignored) or set them as environment variables.")
        print("  Never paste a key into chat if you can avoid it — edit the file yourself.")


def init(home, language, skill_name):
    import os
    env_home = os.environ.get("VIDEO_STUDIO_HOME")
    h = find_home() or Path(home or env_home or Path.home() / "VideoStudio").expanduser().resolve()
    new = not (h / "studio.json").exists()
    for d in ["config", "brand/fonts", "brand/logo", "library", "projects", "inbox"]:
        (h / d).mkdir(parents=True, exist_ok=True)
    # engine: install or upgrade (projects never live inside engine/, so replacing it is safe)
    eng = h / "engine"
    if not eng.exists() or ver(ENGINE_SRC) > ver(eng):
        if eng.exists():
            shutil.rmtree(eng)
        shutil.copytree(ENGINE_SRC, eng, ignore=shutil.ignore_patterns("__pycache__"))
        print(f"  engine {'installed' if new else 'upgraded'} -> {eng}")
    cfgp = h / "config/config.json"
    cfg = json.loads(cfgp.read_text(encoding="utf-8")) if cfgp.exists() else {}
    if language:
        cfg["language"] = language
    cfgp.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    kf = h / "config/api_keys.json"
    if not kf.exists():
        kf.write_text(json.dumps({"_note": "Secrets. Never commit or share this file. Empty = not used.",
                                  **{k: "" for k in KEYS}}, indent=2), encoding="utf-8")
    gi = h / ".gitignore"
    if not gi.exists():
        gi.write_text("config/api_keys.json\nprojects/*/renders/\nprojects/*/**/renders/\nlibrary/*/\n!library/INDEX.md\n__pycache__/\n", encoding="utf-8")
    for name in ("profile.md", "lessons.md"):
        if not (h / name).exists() and (ASSETS / f"{name.split('.')[0]}_template.md").exists():
            shutil.copy2(ASSETS / f"{name.split('.')[0]}_template.md", h / name)
    if not (h / "brand/brand.json").exists() and (ASSETS / "brand_template.json").exists():
        bt = json.loads((ASSETS / "brand_template.json").read_text(encoding="utf-8"))
        bt["language"] = cfg.get("language", "")
        (h / "brand/brand.json").write_text(json.dumps(bt, indent=2, ensure_ascii=False), encoding="utf-8")
    stp = h / "studio.json"
    st = json.loads(stp.read_text(encoding="utf-8")) if stp.exists() else {"created": str(date.today())}
    st["engine"] = ".".join(map(str, ver(eng)))
    st["skills"] = sorted(set(st.get("skills", [])) | ({skill_name} if skill_name else set()))
    stp.write_text(json.dumps(st, indent=2), encoding="utf-8")
    if not env_home:  # remember it for every skill (an explicit VIDEO_STUDIO_HOME is never written to the pointer)
        PTR.write_text(json.dumps({"home": str(h)}), encoding="utf-8")
    if new:  # seed the library with the bundled SFX so `lib.py find whoosh` works on day one
        import subprocess
        subprocess.run([sys.executable, str(eng / "pipeline/lib.py"), "seed"], cwd=str(h), capture_output=True)
    print(f"STUDIO {'CREATED' if new else 'READY'}: {h}")
    print("  Next: fill profile.md + brand/brand.json with the creator (onboarding), then: python setup_studio.py brand")


def mix(hex_a, hex_b, t):
    a = [int(hex_a.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(hex_b.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def rgba(hex_, a):
    r, g, b = (int(hex_.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {a})"


def contrast(a, b):
    def lum(h):
        v = [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def brand():
    h = find_home()
    if not h:
        sys.exit("No studio. Run init first.")
    b = json.loads((h / "brand/brand.json").read_text(encoding="utf-8"))
    c = {k: v for k, v in (b.get("colors") or {}).items() if isinstance(v, str) and v.startswith("#")}
    f = {k: v for k, v in (b.get("fonts") or {}).items() if v}
    lines = ["/* GENERATED by setup_studio.py brand from brand/brand.json — edit brand.json, not this file. */", ":root {"]
    m = {"--teal": "primary", "--green": "secondary", "--lime": "accent", "--yellow": "highlight", "--orange": "alert",
         "--red": "subscribe", "--ink": "text_dark", "--white": "text_light"}
    for var, key in m.items():
        if c.get(key):
            lines.append(f"  {var}: {c[key]};")
    if c.get("primary"):
        lines.append(f"  --teal2: {mix(c['primary'], '#000000', 0.18)};")
    lines.append("}")
    light, dark = [], []
    if c.get("background_light"):
        light += [f"  --bg: {c['background_light']};", f"  --bg-2: {mix(c['background_light'], c.get('primary', '#000000'), 0.06)};"]
    if c.get("primary"):
        paper = c.get("background_light") or "#f6f4ea"
        head = c["primary"]
        if contrast(head, paper) < 3.0:  # a light brand primary (sky blue, yellow) can't be headline text on paper
            head = c.get("text_dark") or mix(c["primary"], "#000000", 0.6)
            print(f"  ! primary {c['primary']} on {paper} is {contrast(c['primary'], paper):.1f}:1 -> headlines use {head}"
                  " (primary stays for shapes/bands)")
        light += [f"  --fg-head: {head};", f"  --edge: {rgba(c['primary'], 0.35)};", f"  --dot: {rgba(c['primary'], 0.2)};",
                  f"  --num: {c['primary']};"]
        bgd = c.get("background_dark") or mix(c["primary"], "#000000", 0.78)
        dark += [f"  --bg: {bgd};", f"  --bg-2: {mix(bgd, '#000000', 0.4)};", f"  --glow-b: {rgba(c['primary'], 0.55)};",
                 f"  --fg-muted: {mix(c.get('text_light') or '#f6f8f0', c['primary'], 0.45)};"]
        light += [f"  --fg-muted: {mix(c.get('text_dark') or '#0d0d0d', c['primary'], 0.55)};"]
    if c.get("accent"):
        dark += [f"  --dot: {rgba(c['accent'], 0.14)};", f"  --glow-a: {rgba(c['accent'], 0.22)};"]
        light += [f"  --glow-b: {rgba(c['accent'], 0.28)};"]
    if c.get("highlight"):
        dark += [f"  --num: {c['highlight']};"]
        light += [f"  --glow-a: {rgba(c['highlight'], 0.6)};"]
    if f.get("main"):
        light.append(f'  --font-ar: "{f["main"]}", sans-serif;')
        dark.append(f'  --font-ar: "{f.get("main_dark") or f["main"]}", sans-serif;')
    if f.get("latin"):
        light.append(f'  --font-en: "{f["latin"]}", sans-serif;')
        dark.append(f'  --font-en: "{f.get("latin_dark") or f["latin"]}", sans-serif;')
    if light:
        lines += ['#root[data-preset="light"] {', *light, "}"]
    if dark:
        lines += ['#root[data-preset="dark"] {', *dark, "}"]
    (h / "brand/brand.css").write_text("\n".join(lines) + "\n", encoding="utf-8")
    cfgp = h / "config/config.json"
    cfg = json.loads(cfgp.read_text(encoding="utf-8")) if cfgp.exists() else {}
    cfg["brand"] = {"name": b.get("name", ""), "tag": b.get("tag") or b.get("name", ""), "palette": c, "fonts": f}
    if b.get("language"):
        cfg["language"] = b["language"]            # spoken (transcription)
    if b.get("text_language"):
        cfg["text_language"] = b["text_language"]  # on-screen text (RTL/LTR); empty = same as spoken
    cfgp.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    fonts_dir = h / "brand/fonts"
    have = [p.name for p in fonts_dir.iterdir()] if fonts_dir.exists() else []
    print(f"OK: brand.css written ({len(c)} colors). Font files in brand/fonts: {have or 'none'}")
    if any(f.values()) and not have:
        print("  ! Fonts named in brand.json but no files in brand/fonts. Download the .ttf (Google Fonts) into brand/fonts/ —"
              " compositions must never load fonts from the internet. Bundled: Noto Kufi Arabic, Cairo, Manrope, Montserrat.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["status", "init", "brand", "keys"])
    ap.add_argument("--home")
    ap.add_argument("--language")
    ap.add_argument("--skill", default=SKILL.name)
    a = ap.parse_args()
    if a.cmd == "status":
        sys.exit(status())
    if a.cmd == "init":
        init(a.home, a.language, a.skill)
    elif a.cmd == "brand":
        brand()
    elif a.cmd == "keys":
        keys()


if __name__ == "__main__":
    main()
