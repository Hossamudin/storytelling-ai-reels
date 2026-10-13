"""Assemble and package the five video skills from one shared source.

Usage:  python skills/build_skills.py [--no-package]

Source of truth:
  skills/_shared/SKILL_CORE.md     injected into every SKILL.md at {{CORE}}
  skills/_shared/references/*.md   shared know-how (every skill)
  skills/_shared/domains/*.md      craft playbooks (per-skill selection below)
  skills/_shared/scripts/          env_check.py, setup_studio.py, vendor_lib.py
  skills/_shared/assets/           profile / lessons / brand templates
  skills/_shared/engine/           the portable studio engine (pipeline + motion kit) installed into the user's studio
  skills/<skill>/SKILL.md          per-skill instructions
Output: skills/dist/<skill>/ (installable folders) + skills/dist/<skill>.skill (zip packages)
Edit the sources, never dist/.
"""
import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "_shared"
DIST = HERE / "dist"
DOMAINS = {
    "hakawati-video-studio": ["format-router", "storytelling", "motion-director", "style-presets", "style-catalog",
                              "talking-head", "screenshare-playbook", "animation-2d", "animation-3d"],
    "kashaf-screen-editor": ["screenshare-playbook", "motion-director", "style-presets", "storytelling"],
    "nabd-motion-graphics": ["motion-director", "style-presets", "style-catalog", "storytelling", "animation-2d", "animation-3d"],
    "risha-2d-animation": ["animation-2d", "motion-director", "style-presets", "storytelling"],
    "abaad-3d-animation": ["animation-3d", "motion-director", "style-presets", "storytelling"],
}
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")


def check_refs(skill_dir):
    """Every `references/x.md` mentioned in the skill must exist in it."""
    text = "\n".join(p.read_text(encoding="utf-8") for p in skill_dir.rglob("*.md"))
    missing = sorted({m for m in re.findall(r"references/([\w\-]+\.md)", text) if not (skill_dir / "references" / m).exists()})
    for name in re.findall(r"`([\w\-]+\.md)`", text):
        if name not in ("SKILL.md", "BRIEF.md", "INDEX.md", "profile.md", "lessons.md", "SKILL_CORE.md") \
                and not (skill_dir / "references" / name).exists():
            missing.append(name)
    return sorted(set(missing))


def build(skill):
    src = HERE / skill
    out = DIST / skill
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    core = (SH / "SKILL_CORE.md").read_text(encoding="utf-8").strip()
    body = (src / "SKILL.md").read_text(encoding="utf-8").replace("{{CORE}}", core)
    (out / "SKILL.md").write_text(body, encoding="utf-8")
    refs = out / "references"
    refs.mkdir()
    for f in sorted((SH / "references").glob("*.md")):
        shutil.copy2(f, refs / f.name)
    for d in DOMAINS[skill]:
        shutil.copy2(SH / "domains" / f"{d}.md", refs / f"{d}.md")
    shutil.copytree(SH / "scripts", out / "scripts", ignore=IGNORE)
    shutil.copytree(SH / "assets", out / "assets", ignore=IGNORE)
    shutil.copytree(SH / "engine", out / "engine", ignore=IGNORE)
    for extra in ("references", "assets", "scripts"):  # optional per-skill extras
        if (src / extra).exists():
            shutil.copytree(src / extra, out / extra, dirs_exist_ok=True, ignore=IGNORE)
    m = re.match(r"---\nname: (.+)\ndescription: \"(.+)\"\n---", body, re.S)
    if not m or m.group(1).strip() != skill:
        sys.exit(f"{skill}: bad frontmatter")
    desc = m.group(2)
    missing = check_refs(out)
    lines = len(body.splitlines())
    size = sum(p.stat().st_size for p in out.rglob("*") if p.is_file()) / 1e6
    print(f"{skill:<24} SKILL.md {lines:>3} lines · description {len(desc):>4} chars · {size:.1f} MB"
          + (f" · MISSING refs: {missing}" if missing else ""))
    if len(desc) > 1024:
        print(f"  ! description longer than 1024 chars")
    return out


def package(out):
    z = DIST / f"{out.name}.skill"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out.rglob("*")):
            if p.is_file():
                zf.write(p, Path(out.name) / p.relative_to(out))
    return z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-package", action="store_true")
    a = ap.parse_args()
    DIST.mkdir(exist_ok=True)
    for skill in DOMAINS:
        out = build(skill)
        if not a.no_package:
            z = package(out)
            print(f"  -> {z.relative_to(HERE.parent)} ({z.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
