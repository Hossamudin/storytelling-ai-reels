"""Reusable asset library: one place for every asset worth reusing across videos.

  library/
    INDEX.md          compact catalog (one line per asset) -> the ONLY file an agent reads first
    index.jsonl       full records: id, file, type, subject, desc, tags, w/h/dur, aspect, source, prompt,
                      model, cost, sha1, added, used_in
    _sheets/<type>.jpg contact sheets (numbered thumbs) -> pick visually with ONE image read
    <type>/<file>     the assets, named  <type>_<subject>_<descriptor>[_<aspect>][_<dur>s]_v<N>.<ext>
                      (lowercase ascii, '-' inside a field, '_' between fields)

Types: person-photo · person-cutout · person-clip (the creator) · logo · img · broll · sfx · music · screen · capture · 3d · code ·
       episode (finished videos: cite / show "watch the previous reel" thumbnails) · qr (verified, white quiet zone; record the decoded URL)

Usage (from repo root):
  python engine/pipeline/lib.py find "claude logo" [--type logo] [-n 15]      search (name/tags/desc/prompt)
  python engine/pipeline/lib.py add <file> --type img --subject engine-core --desc "glowing engine core, dark bg" \
         [--tags a,b] [--source higgsfield] [--prompt "..."] [--model gpt_image_2_5] [--cost 0.04] [--move]
  python engine/pipeline/lib.py use <id> <project-or-part dir> [--as name.ext]  copy into <dir>/assets/lib/ (or --to), record use
  python engine/pipeline/lib.py harvest <project>                             import a project's generated/captured assets
  python engine/pipeline/lib.py index                                         rebuild INDEX.md + contact sheets
  python engine/pipeline/lib.py describe [ids…] [--all]                       vision model writes subject/desc/tags + renames
  python engine/pipeline/lib.py seed                                          one-time import of the bundled kit SFX
  python engine/pipeline/lib.py import <folder> [--type T] [--tags a,b]       bulk-add a folder of existing assets (type guessed per file)
Rules: before any paid generation run `find`; after any generation or capture worth keeping run `add`
(or `harvest` at delivery). Duplicates are detected by sha1.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

ROOT = C.ROOT
LIB = ROOT / "library"
IDX = LIB / "index.jsonl"
TYPES = ["person-photo", "person-cutout", "person-clip", "logo", "img", "broll", "sfx", "music", "screen", "capture", "3d", "code", "episode", "qr"]
IMG = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
VID = {".mp4", ".mov", ".webm", ".mkv"}
AUD = {".mp3", ".wav", ".m4a", ".ogg"}


# ------------------------------------------------------------------ records
def load():
    if not IDX.exists():
        return []
    return [json.loads(l) for l in IDX.read_text(encoding="utf-8").splitlines() if l.strip()]


def save(recs):
    LIB.mkdir(exist_ok=True)
    IDX.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs), encoding="utf-8")


def slug(s, n=40):
    s = re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")
    return s[:n].strip("-") or "x"


def sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def probe(p):
    ext = p.suffix.lower()
    if ext == ".svg" or ext in {".py", ".js", ".css", ".html", ".json"}:
        return {}
    if ext in IMG:
        try:
            from PIL import Image, ImageOps
            with Image.open(p) as im:
                im = ImageOps.exif_transpose(im)
                return {"w": im.width, "h": im.height, "alpha": im.mode in ("RGBA", "LA")}
        except Exception:
            return {}
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration", "-of", "json", str(p)],
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except Exception:
        return {}
    out = {"dur": round(float(d.get("format", {}).get("duration", 0) or 0), 2)}
    for s in d.get("streams", []):
        if s.get("width"):
            out.update(w=s["width"], h=s["height"])
            break
    return out


def aspect(m):
    w, h = m.get("w"), m.get("h")
    if not w or not h:
        return ""
    r = w / h
    for name, v in (("16x9", 16 / 9), ("9x16", 9 / 16), ("1x1", 1), ("4x5", 0.8), ("3x4", 0.75), ("2x3", 2 / 3), ("3x2", 1.5), ("4x3", 4 / 3)):
        if abs(r - v) < 0.04:
            return name
    return f"{w}x{h}"


def add(path, type_, subject, desc, tags=(), source="", prompt="", model="", cost=0.0, move=False, recs=None, quiet=False):
    p = Path(path)
    if type_ not in TYPES:
        raise SystemExit(f"type must be one of {TYPES}")
    own = recs is None
    recs = load() if own else recs
    h = sha1(p)
    for r in recs:
        if r["sha1"] == h:
            if not quiet:
                print(f"duplicate of {r['id']} ({r['file']})")
            return r
    m = probe(p)
    asp = aspect(m)
    dur = f"{m['dur']:.0f}s" if m.get("dur") and type_ in ("broll", "person-clip", "screen", "music", "episode") else ""
    base = "_".join(x for x in (type_.split("-")[0] if type_.startswith("person") else type_, slug(subject, 30), slug(desc, 36), asp, dur) if x)
    if type_.startswith("person"):
        base = "person_" + type_.split("-")[1] + base[len("person"):]
    d = LIB / type_
    d.mkdir(parents=True, exist_ok=True)
    v = 1
    while (d / f"{base}_v{v}{p.suffix.lower()}").exists():
        v += 1
    dest = d / f"{base}_v{v}{p.suffix.lower()}"
    (shutil.move if move else shutil.copy2)(str(p), dest)
    rid = f"{type_.split('-')[0][:3]}-{h[:6]}"
    rec = {"id": rid, "file": dest.relative_to(LIB).as_posix(), "type": type_, "subject": subject, "desc": desc,
           "tags": sorted({t.strip().lower() for t in tags if t.strip()}), **m, "aspect": asp, "source": source,
           "prompt": prompt, "model": model, "cost": cost, "sha1": h, "added": dt.date.today().isoformat(), "used_in": []}
    recs.append(rec)
    if own:
        save(recs)
        write_index(recs)
    if not quiet:
        print(f"added {rid}: {rec['file']}")
    return rec


# ------------------------------------------------------------------ find / use
def score(r, q):
    hay = " ".join([r["file"], r["subject"], r["desc"], " ".join(r["tags"]), r.get("prompt", "")[:300]]).lower()
    s = 0
    for t in q:
        if t in r["tags"] or t == r["subject"]:
            s += 3
        elif re.search(rf"\b{re.escape(t)}", hay):
            s += 2
        elif t in hay:
            s += 1
    return s


def line(r):
    meta = r.get("aspect") or ""
    if r.get("dur"):
        meta += f" {r['dur']}s"
    if r.get("alpha"):
        meta += " alpha"
    used = f" used:{len(r['used_in'])}" if r.get("used_in") else ""
    return f"{r['id']:<11} {r['type']:<13} {meta:<14} {r['desc'][:70]}  [{', '.join(r['tags'][:6])}]{used}  {r['file']}"


def find(query, type_=None, n=15):
    q = [t for t in re.split(r"[\s,]+", query.lower()) if t]
    recs = [r for r in load() if not type_ or r["type"] == type_]
    hits = sorted(((score(r, q), r) for r in recs), key=lambda x: -x[0])
    hits = [r for s, r in hits if s > 0][:n]
    for r in hits:
        print(line(r))
    if not hits:
        print("no match — generate (after approval), then `lib.py add` it")
    return hits


def use(rid, target, as_name=None, to="assets/lib"):
    recs = load()
    r = next((x for x in recs if x["id"] == rid or x["file"].endswith(rid)), None)
    if not r:
        raise SystemExit(f"unknown id {rid}")
    t = Path(target)
    t = t if t.is_absolute() else ROOT / t
    dest = t / to / (as_name or Path(r["file"]).name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(LIB / r["file"], dest)
    tag = t.relative_to(ROOT).as_posix() if t.is_relative_to(ROOT) else str(t)
    if tag not in r["used_in"]:
        r["used_in"].append(tag)
        save(recs)
        write_index(recs)
    print(f"{rid} -> {dest.relative_to(t).as_posix()}")
    return dest


# ------------------------------------------------------------------ index + contact sheets
def write_index(recs=None):
    recs = load() if recs is None else recs
    out = ["# Asset library index (auto-generated by `python engine/pipeline/lib.py index` — do not edit)",
           "", "Search: `python engine/pipeline/lib.py find \"<words>\" [--type T]` · copy into a project: `lib.py use <id> <dir>` ·",
           "visual pick: `library/_sheets/<type>.jpg` (thumb numbers = order below).", ""]
    for t in TYPES:
        rs = [r for r in recs if r["type"] == t]
        if not rs:
            continue
        out.append(f"## {t} ({len(rs)})")
        for k, r in enumerate(rs, 1):
            out.append(f"{k:>2}. {line(r)}")
        out.append("")
    (LIB / "INDEX.md").write_text("\n".join(out), encoding="utf-8")


def sheets(recs=None):
    from PIL import Image, ImageDraw, ImageOps
    recs = load() if recs is None else recs
    sd = LIB / "_sheets"
    sd.mkdir(parents=True, exist_ok=True)
    for t in TYPES:
        rs = [r for r in recs if r["type"] == t and Path(r["file"]).suffix.lower() in (IMG | VID) - {".svg"}]
        if not rs:
            continue
        cell, cols = 220, 6
        rows = (len(rs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell, rows * (cell + 22)), (30, 30, 30))
        dr = ImageDraw.Draw(sheet)
        for k, r in enumerate(rs):
            src = LIB / r["file"]
            try:
                if src.suffix.lower() in VID:
                    tmp = sd / "_frame.jpg"
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str((r.get("dur") or 2) / 2), "-i", str(src),
                                    "-frames:v", "1", str(tmp)], check=True)
                    im = Image.open(tmp)
                else:
                    im = ImageOps.exif_transpose(Image.open(src))
                im = im.convert("RGBA")
                im.thumbnail((cell - 8, cell - 8))
                bg = Image.new("RGBA", im.size, (90, 90, 90, 255))
                bg.alpha_composite(im)
                x, y = (k % cols) * cell, (k // cols) * (cell + 22)
                sheet.paste(bg.convert("RGB"), (x + (cell - im.width) // 2, y + (cell - im.height) // 2))
                dr.text((x + 4, y + cell + 3), f"{k + 1}. {r['id']}", fill=(230, 230, 230))
            except Exception as ex:
                print(f"  sheet skip {r['file']}: {ex}")
        sheet.save(sd / f"{t}.jpg", quality=80)
    (sd / "_frame.jpg").unlink(missing_ok=True)


# ------------------------------------------------------------------ auto-describe (vision)
DESCRIBE = """You catalog assets for a video studio's reusable library .
Look at the image and return JSON: {"subject": "2-4 word kebab-case noun, e.g. engine-core / claude-logo / chess-board",
"desc": "<= 12 plain English words: what it shows + style + background", "tags": ["6-10 lowercase single words:
objects, style (clay/3d/flat/photo/ui/chart), mood, colors, use (hook/cta/background/b-roll/icon)"]}"""


def describe(rids=None, model=None, generic_only=True):
    import base64
    import io
    import requests
    from PIL import Image, ImageOps
    recs = load()
    key = C.need_key("OPENAI_API_KEY", "describe uses a vision model to name and tag assets")
    model = model or C.load_config().get("library", {}).get("describe_model", "gpt-5.4-mini")
    todo = [r for r in recs if (not rids or r["id"] in rids) and r["type"] in ("img", "broll", "capture", "screen", "logo", "3d")
            and (not generic_only or len(r["desc"].split()) < 4 or re.match(r"^s\d+ first", r["desc"].lower()))]
    for r in todo:
        src = LIB / r["file"]
        if src.suffix.lower() in VID:
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str((r.get("dur") or 2) / 2), "-i", str(src), "-frames:v", "1",
                                  "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            im = Image.open(io.BytesIO(raw))
        else:
            im = ImageOps.exif_transpose(Image.open(src))
        im = im.convert("RGB")
        im.thumbnail((768, 768))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=80)
        b64 = base64.b64encode(buf.getvalue()).decode()
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, timeout=120,
                             json={"model": model, "response_format": {"type": "json_object"}, "messages": [
                                 {"role": "system", "content": DESCRIBE},
                                 {"role": "user", "content": [{"type": "text", "text": f"Prompt it was made from (may be empty): {r.get('prompt', '')[:400]}"},
                                                              {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]})
        if resp.status_code != 200:
            print(f"  describe {r['id']}: HTTP {resp.status_code} {resp.text[:200]}")
            continue
        d = json.loads(resp.json()["choices"][0]["message"]["content"])
        r["subject"], r["desc"] = slug(d.get("subject", r["subject"]), 30), d.get("desc", r["desc"])
        r["tags"] = sorted(set(r["tags"]) | {slug(t, 20) for t in d.get("tags", [])})
        stem = Path(r["file"]).name
        m = re.match(r"^(.*?)_v(\d+)(\.\w+)$", stem)
        parts = [r["type"].split("-")[0] if not r["type"].startswith("person") else "person_" + r["type"].split("-")[1],
                 r["subject"], slug(r["desc"], 36), r.get("aspect", "")]
        if r.get("dur") and r["type"] in ("broll", "screen", "person-clip", "music"):
            parts.append(f"{r['dur']:.0f}s")
        base = "_".join(x for x in parts if x)
        v = 1
        while (src.parent / f"{base}_v{v}{m.group(3)}").exists() and src.parent / f"{base}_v{v}{m.group(3)}" != src:
            v += 1
        dest = src.parent / f"{base}_v{v}{m.group(3)}"
        if dest != src:
            src.rename(dest)
            r["file"] = dest.relative_to(LIB).as_posix()
        print(f"  {r['id']}: {r['desc']}  -> {Path(r['file']).name}")
    save(recs)
    write_index(recs)
    sheets(recs)


# ------------------------------------------------------------------ harvest / seed
def harvest(project, recs):
    pp = C.project_path(project)
    n = 0
    lp = pp / "assets/ledger.json"
    led = json.loads(lp.read_text(encoding="utf-8")) if lp.exists() else {}
    for e in led.get("entries", []) if isinstance(led, dict) else []:
        f = e.get("file", "")
        if "*" in f or "/" not in f and not (pp / "assets/images" / f).exists():
            continue
        cands = [pp / f, pp / "assets" / f, pp / "assets/images" / f]
        src = next((c for c in cands if c.is_file()), None)
        if not src:
            continue
        kind = e.get("kind")
        type_ = {"sfx": "sfx", "video": "broll", "image": "img", "screenshot": "capture"}.get(kind)
        if not type_:
            continue
        prompt = e.get("prompt", "")
        desc = (prompt.split(",")[0] if prompt else src.stem.replace("_", " "))[:80]
        add(src, type_, slug(src.stem.replace("broll_", ""), 30), desc, tags=[project, e.get("provider", ""), kind],
            source=f"{project}:{e.get('provider', '')}", prompt=prompt, model=e.get("model", ""),
            cost=e.get("cost_usd", e.get("cost", 0)) or 0, recs=recs, quiet=True)
        n += 1
    return n


def seed():
    recs = load()
    sfx = C.KIT / "sfx/library"
    for f in sorted(sfx.glob("*.mp3")):
        add(f, "sfx", f.stem.rsplit("-", 1)[0] if f.stem[-1].isdigit() else f.stem, f"{f.stem.replace('-', ' ')} (bundled kit SFX)",
            tags=["bundled", *f.stem.split("-")], source="engine/kit/motion/sfx/library", recs=recs, quiet=True)
    save(recs)
    write_index(recs)
    sheets(recs)
    print(f"library: {len(recs)} assets")


def guess_type(f: Path):
    n, ext = f.stem.lower(), f.suffix.lower()
    if ext in AUD:
        return "music" if any(k in n for k in ("music", "bgm", "song", "track")) else "sfx"
    if ext in VID:
        return "screen" if any(k in n for k in ("screen", "record", "capture", "obs")) else "broll"
    if ext in IMG:
        if "logo" in n:
            return "logo"
        if "qr" in n:
            return "qr"
        if any(k in n for k in ("screenshot", "capture", "screen")):
            return "capture"
        return "img"
    return None


def import_folder(folder, type_=None, tags=""):
    """Library building from what the creator already has: every media file in <folder> (recursive)."""
    recs, n = load(), 0
    for f in sorted(Path(folder).rglob("*")):
        t = type_ or guess_type(f)
        if not f.is_file() or not t:
            continue
        subj = slug(f.stem, 30) or "asset"
        add(f, t, subj, f.stem.replace("_", " ").replace("-", " ")[:80], tags=[x for x in tags.split(",") if x] + [t],
            source=str(f), recs=recs, quiet=True)
        n += 1
    save(recs)
    write_index(recs)
    sheets(recs)
    print(f"imported {n} files from {folder} (duplicates skipped). Next: python engine/pipeline/lib.py describe  (AI names + tags)")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    f = sp.add_parser("find"); f.add_argument("query"); f.add_argument("--type"); f.add_argument("-n", type=int, default=15)
    a = sp.add_parser("add"); a.add_argument("file"); a.add_argument("--type", required=True); a.add_argument("--subject", required=True)
    a.add_argument("--desc", required=True); a.add_argument("--tags", default=""); a.add_argument("--source", default="")
    a.add_argument("--prompt", default=""); a.add_argument("--model", default=""); a.add_argument("--cost", type=float, default=0.0)
    a.add_argument("--move", action="store_true")
    u = sp.add_parser("use"); u.add_argument("id"); u.add_argument("target"); u.add_argument("--as", dest="as_name")
    u.add_argument("--to", default="assets/lib", help="subfolder of target (e.g. assets/sfx/lib for SFX cues)")
    h = sp.add_parser("harvest"); h.add_argument("project")
    sp.add_parser("index"); sp.add_parser("seed")
    im = sp.add_parser("import"); im.add_argument("folder"); im.add_argument("--type"); im.add_argument("--tags", default="")
    dsc = sp.add_parser("describe"); dsc.add_argument("ids", nargs="*"); dsc.add_argument("--all", action="store_true",
                                                                                       help="re-describe even assets that have a good desc")
    x = ap.parse_args()
    if x.cmd == "find":
        find(x.query, x.type, x.n)
    elif x.cmd == "add":
        add(x.file, x.type, x.subject, x.desc, x.tags.split(","), x.source, x.prompt, x.model, x.cost, x.move)
        sheets()
    elif x.cmd == "use":
        use(x.id, x.target, x.as_name, x.to)
    elif x.cmd == "harvest":
        recs = load()
        n = harvest(x.project, recs)
        save(recs); write_index(recs); sheets(recs)
        print(f"harvested {n} ledger entries from {x.project} (duplicates skipped)")
    elif x.cmd == "index":
        write_index(); sheets()
    elif x.cmd == "seed":
        seed()
    elif x.cmd == "import":
        import_folder(x.folder, x.type, x.tags)
    elif x.cmd == "describe":
        describe(x.ids or None, generic_only=not (x.all or x.ids))


if __name__ == "__main__":
    main()
