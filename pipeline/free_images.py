"""free_images.py - find and download FREE real photos (CC0 / public domain / CC BY / CC BY-SA) with credits.

Sources (no key): Openverse (api.openverse.org) first, Wikimedia Commons as fallback. Two steps, because a human or
agent must LOOK at candidates before use (no people, nothing indecent, the right subject, good quality):

  python pipeline/free_images.py <project> search camel "camel desert" [--n 12] [--source openverse|commons] [--any-aspect]
      -> assets/images/real/_cand/camel/NN.jpg thumbnails + _sheet.jpg (numbered contact sheet) + candidates.json
  python pipeline/free_images.py <project> pick camel 3 [--as camel]
      -> assets/images/real/camel.jpg (max 2400 px, JPEG q90) + an entry in assets/images/real/credits.json
  python pipeline/free_images.py <project> credits
      -> prints the credits block for the video description (CC BY / BY-SA REQUIRE attribution)

<project> may be "name" or "name/part" (assets go under that folder).
"""
import argparse
import io
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

UA = {"User-Agent": "HossamVideoFactory/1.0 (free-images; educational kids videos)"}
OK_LICENSES = {"cc0", "pdm", "by", "by-sa"}
# kids content: keep artworks, nudity and people out of the candidate pool (still LOOK at every sheet)
EXCLUDE = "-nude -naked -painting -surfer -surfing"  # short: long exclusion lists empty Commons results; titles are filtered below
BLOCK_WORDS = ("nude", "naked", "painting", "bouguereau", "woman", "women", "girl", "boy", "man ", "men ", "people", "person",
               "surfer", "surfing", "swimmer", "bikini", "portrait", "selfie")


def get(url, raw=False, tries=4, timeout=60):
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                data = r.read()
            return data if raw else json.loads(data.decode("utf-8"))
        except Exception as e:  # slow / flaky links and 429 rate limits: back off and retry
            last = e
            time.sleep((15 if "429" in str(e) else 2) * (i + 1))
    raise RuntimeError(f"GET failed: {url} ({last})")


def search_openverse(q, n, wide):
    p = {"q": q, "license": ",".join(sorted(OK_LICENSES)), "category": "photograph", "size": "large",
         "mature": "false", "page_size": str(min(40, n * 2))}
    if wide:
        p["aspect_ratio"] = "wide"
    d = get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(p))
    out = []
    for r in d.get("results", []):
        if r.get("license") not in OK_LICENSES:
            continue
        if any(w in ((r.get("title") or "") + " " + " ".join(x.get("name", "") for x in r.get("tags") or [])).lower() for w in BLOCK_WORDS):
            continue
        out.append({"source": "openverse/" + (r.get("source") or ""), "title": r.get("title") or "",
                    "creator": r.get("creator") or "unknown", "license": r["license"].upper().replace("PDM", "Public Domain"),
                    "license_version": r.get("license_version") or "", "license_url": r.get("license_url") or "",
                    "page": r.get("foreign_landing_url") or "", "url": r["url"], "thumb": r.get("thumbnail") or r["url"],
                    "w": r.get("width"), "h": r.get("height")})
    return out[:n]


def search_commons(q, n, wide):
    p = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": "6",
         "gsrsearch": f"{q} filetype:bitmap {EXCLUDE}", "gsrlimit": str(min(50, n * 3)), "prop": "imageinfo",
         "iiprop": "url|size|extmetadata", "iiurlwidth": "1920"}  # standard thumb size (Wikimedia asks for these)
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p))
    out = []
    for pg in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 0)):
        ii = pg["imageinfo"][0]
        md = ii.get("extmetadata", {})
        lic = (md.get("LicenseShortName", {}).get("value") or "").lower()
        key = "cc0" if "cc0" in lic else "pdm" if "public domain" in lic else "by-sa" if "by-sa" in lic else "by" if "cc by" in lic else None
        if any(w in pg["title"].lower() for w in BLOCK_WORDS):
            continue
        if not key or (wide and ii["width"] < ii["height"] * 1.2) or ii["width"] < 1600:
            continue
        creator = md.get("Artist", {}).get("value", "unknown")
        creator = __import__("re").sub("<[^>]+>", "", creator).strip()
        out.append({"source": "wikimedia commons", "title": pg["title"].replace("File:", ""), "creator": creator,
                    "license": md.get("LicenseShortName", {}).get("value", key), "license_version": "",
                    "license_url": md.get("LicenseUrl", {}).get("value", ""), "page": ii.get("descriptionurl", ""),
                    "url": ii.get("thumburl") or ii["url"],
                    "thumb": (ii.get("thumburl") or ii["url"]).replace("/1920px-", "/500px-").split("?")[0],
                    "w": ii["width"], "h": ii["height"]})
        if len(out) >= n:
            break
    return out


def sheet(files, dst):
    from PIL import Image, ImageDraw
    cols, tw, th = 4, 480, 300
    rows = (len(files) + cols - 1) // cols
    im = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
    d = ImageDraw.Draw(im)
    for i, f in enumerate(files):
        try:
            t = Image.open(f).convert("RGB")
            t.thumbnail((tw - 8, th - 8))
            x, y = (i % cols) * tw + 4, (i // cols) * th + 4
            im.paste(t, (x, y))
            d.rectangle([x, y, x + 44, y + 34], fill=(255, 90, 51))
            d.text((x + 10, y + 8), Path(f).stem, fill=(255, 255, 255))  # candidate index = file name
        except Exception:
            pass
    im.save(dst, quality=85)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("cmd", choices=["search", "pick", "credits", "clean"])
    ap.add_argument("slug", nargs="?")
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--source", default="openverse", choices=["openverse", "commons"])
    ap.add_argument("--any-aspect", action="store_true")
    ap.add_argument("--as", dest="as_", default=None)
    a = ap.parse_args()
    base = C.ROOT / "projects" / a.project / "assets/images/real"
    base.mkdir(parents=True, exist_ok=True)
    credits_f = base / "credits.json"
    credits = json.loads(credits_f.read_text(encoding="utf-8")) if credits_f.exists() else {}

    if a.cmd == "search":
        q = a.arg or a.slug
        wide = not a.any_aspect
        try:
            res = search_openverse(q, a.n, wide) if a.source == "openverse" else search_commons(q, a.n, wide)
        except RuntimeError as e:
            print(f"  {a.source} failed ({e}); trying the other source")
            res = []
        if not res:
            try:
                res = search_commons(q, a.n, wide) if a.source == "openverse" else search_openverse(q, a.n, wide)
            except RuntimeError as e:
                raise SystemExit(f"both sources failed or empty ({e}); wait a minute (rate limit) or change the query")
        cd = base / "_cand" / a.slug
        cd.mkdir(parents=True, exist_ok=True)
        files = []
        for i, r in enumerate(res):
            f = cd / f"{i:02d}.jpg"
            try:
                f.write_bytes(get(r["thumb"], raw=True))
                files.append(f)
                time.sleep(1.0)  # be gentle: both sources rate-limit bursts
            except RuntimeError as e:
                print(f"  thumb {i} failed: {e}")
        (cd / "candidates.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        sheet(files, cd / "_sheet.jpg")
        for i, r in enumerate(res):
            print(f"  {i:02d}  {r['license']:<14} {r['w']}x{r['h']}  {r['title'][:60]}  — {r['creator'][:30]}")
        print(f"-> LOOK at {cd / '_sheet.jpg'} (no people, right subject), then: free_images.py {a.project} pick {a.slug} <NN>")

    elif a.cmd == "pick":
        from PIL import Image
        cd = base / "_cand" / a.slug
        r = json.loads((cd / "candidates.json").read_text(encoding="utf-8"))[int(a.arg)]
        name = a.as_ or a.slug
        im = Image.open(io.BytesIO(get(r["url"], raw=True, timeout=180))).convert("RGB")
        im.thumbnail((2400, 2400))
        dst = base / f"{name}.jpg"
        im.save(dst, quality=90)
        credits[name] = {k: r[k] for k in ("title", "creator", "license", "license_version", "license_url", "page", "source")}
        credits[name]["size"] = list(im.size)
        credits_f.write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"-> {dst} {im.size}  ({r['license']} — {r['creator']})")

    elif a.cmd == "clean":  # after picking: drop every candidate thumbnail (never keep unreviewed images around)
        import shutil
        shutil.rmtree(base / "_cand", ignore_errors=True)
        print("removed", base / "_cand")

    else:
        for name, c in credits.items():
            v = f" {c['license_version']}" if c.get("license_version") else ""
            print(f"- {name}: \"{c['title']}\" by {c['creator']}, {c['license']}{v} — {c['page']}")


if __name__ == "__main__":
    main()
