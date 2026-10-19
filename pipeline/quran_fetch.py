"""quran_fetch.py - fetch Quran ayat (text + recitation audio) and hadith from free public APIs.

Rule: ayat and hadith are NEVER typed by hand into a script or composition. Every verse/hadith on screen or in the
voice track comes from this tool's output.

Sources (free, no key):
  - Text:   api.quran.com v4  (text_uthmani per verse + per word)
  - Audio:  api.quran.com v4 chapter_recitations (qdc files on download.quranicaudio.com) with word segments,
            cut with ffmpeg -> exact verse or word-range fragment
  - Tafsir: api.quran.com v4 tafsir 16 (التفسير الميسر) - for the writer to check the meaning, never shown as Quran
  - Hadith: fawazahmed0/hadith-api via cdn.jsdelivr.net (ara-bukhari / ara-muslim; numbering = that edition's)

Usage:
  python pipeline/quran_fetch.py <project>            # reads projects/<project>/quran.json
  python pipeline/quran_fetch.py <project> --no-audio # text only

quran.json:
  {"reciter": 6,                                      # 6 = Husary murattal (12 = Husary muallim, 7 = Alafasy)
   "items": [
     {"id": "ikhlas", "key": "112:1-4"},                 # whole verses (range inside one surah)
     {"id": "kursi_sleep", "key": "2:255", "words": [5, 9]},   # word range inside ONE verse (1-based, inclusive)
     {"id": "fitra", "hadith": "bukhari", "number": 1385,      # hadith excerpt: from/to are matched ignoring tashkeel
      "from": "كل مولود", "to": "الفطرة"}
   ]}

Output in projects/<project>/assets/quran/:
  <id>.wav            recitation clip (48 kHz stereo, short fades) - Quran items only
  quran.json          per item: text (Uthmani), surah name, verse keys, words with clip-relative times,
                      tafsir (writer reference), audio source + attribution, hadith source
  script placeholders: if the project has script.md, writes script.rendered.md with {{Q:<id>}} / {{H:<id>}}
                      replaced by the fetched text (+ reference)
"""
import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

QAPI = "https://api.quran.com/api/v4"
HAPI = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions"
TAFSIR_ID = 16
PAD_IN_MS, PAD_OUT_MS = 150, 450
HADITH_NAMES = {"bukhari": "صحيح البخاري", "muslim": "صحيح مسلم"}
TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
_cache = {}


def get_json(url, tries=4):
    if url in _cache:
        return _cache[url]
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "hossam-video-factory/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                data = json.loads(r.read().decode("utf-8"))
            _cache[url] = data
            return data
        except Exception as e:  # 503 from the quran.com edge happens; back off and retry
            last = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"GET failed after {tries} tries: {url} ({last})")


def parse_key(key):
    s, v = key.split(":")
    a, _, b = v.partition("-")
    return int(s), int(a), int(b or a)


def verse(key):
    d = get_json(f"{QAPI}/verses/by_key/{key}?fields=text_uthmani&words=true&word_fields=text_uthmani")["verse"]
    words = [w for w in d["words"] if w["char_type_name"] == "word"]
    return d["text_uthmani"].strip(), words


def norm(s):
    s = TASHKEEL.sub("", s)
    s = re.sub("[إأآٱ]", "ا", s).replace("ى", "ي").replace("ة", "ه")
    return s


def excerpt(text, frm, to):
    """Return the original (with tashkeel) substring of text spanning frm..to, matched ignoring tashkeel."""
    keep = [(i, ch) for i, ch in enumerate(text) if not TASHKEEL.match(ch)]
    flat = norm("".join(ch for _, ch in keep))
    # norm() never changes length of the tashkeel-free string, so indices line up with keep
    a = flat.find(norm(frm))
    if a < 0:
        raise ValueError(f"'{frm}' not found in hadith text")
    b = flat.find(norm(to), a + len(norm(frm)))
    if b < 0:
        raise ValueError(f"'{to}' not found after '{frm}'")
    b += len(norm(to))
    start = keep[a][0]
    end = keep[b - 1][0] + 1
    while end < len(text) and TASHKEEL.match(text[end]):
        end += 1
    return text[start:end]


def fetch_hadith(item):
    col, num = item["hadith"], int(item["number"])
    try:
        h = get_json(f"{HAPI}/ara-{col}/{num}.json", tries=2)["hadiths"][0]
    except RuntimeError:  # some single-hadith files are missing on the CDN: use the full edition (cached)
        cache = C.ROOT / ".cache" / "hadith" / f"ara-{col}.min.json"
        if not cache.exists():
            cache.parent.mkdir(parents=True, exist_ok=True)
            req = urllib.request.Request(f"{HAPI}/ara-{col}.min.json", headers={"User-Agent": "hossam-video-factory/1.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                cache.write_bytes(r.read())
        ed = json.loads(cache.read_text(encoding="utf-8"))
        h = next(x for x in ed["hadiths"] if int(x["hadithnumber"]) == num)
    full = h["text"].strip()
    if not full:
        raise ValueError(f"empty hadith text for {col} {num} (edition numbering differs - check arabicnumber)")
    text = excerpt(full, item["from"], item["to"]) if item.get("from") else full
    ref = item.get("ref") or f"{HADITH_NAMES.get(col, col)} ({h.get('arabicnumber') or num})"
    return {"id": item["id"], "type": "hadith", "text": text, "full_text": full, "ref": ref,
            "source": f"{HAPI}/ara-{col}/{num}.json", "grades": h.get("grades", [])}


def local_audio(url, reciter, surah):
    """Whole-surah recitation file, downloaded once into .cache/quran/."""
    dst = C.ROOT / ".cache" / "quran" / f"r{reciter}_{surah:03d}{Path(url).suffix or '.mp3'}"
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "hossam-video-factory/1.0"})
        with urllib.request.urlopen(req, timeout=600) as r:
            dst.with_suffix(".part").write_bytes(r.read())
        dst.with_suffix(".part").replace(dst)
    return dst


def fetch_quran(item, reciter, audio_dir, want_audio):
    s, a, b = parse_key(item["key"])
    chapter = get_json(f"{QAPI}/chapters/{s}?language=ar")["chapter"]
    wr = item.get("words")
    if wr and a != b:
        raise ValueError(f"{item['id']}: 'words' needs a single verse key")
    verses, texts, all_words = [], [], []
    for n in range(a, b + 1):
        key = f"{s}:{n}"
        vtext, words = verse(key)
        if wr:
            words = [w for w in words if wr[0] <= w["position"] <= wr[1]]
            vtext = " ".join(w["text_uthmani"] for w in words)
        tafsir = get_json(f"{QAPI}/tafsirs/{TAFSIR_ID}/by_ayah/{key}")["tafsir"]["text"]
        verses.append({"key": key, "text": vtext, "tafsir_muyassar": re.sub("<[^>]+>", "", tafsir)})
        texts.append(vtext)
        all_words += [{"key": key, "pos": w["position"], "text": w["text_uthmani"]} for w in words]
    full_fragment = bool(wr)
    ref = f"سورة {chapter['name_arabic']} " + (f"({a})" if a == b else f"({a}–{b})")
    out = {"id": item["id"], "type": "quran", "key": item["key"], "words_range": wr,
           "is_fragment": full_fragment, "surah": chapter["name_arabic"], "ref": ref,
           "text": " ".join(texts), "verses": verses, "words": all_words,
           "text_source": f"{QAPI}/verses/by_key/<key>?fields=text_uthmani"}

    rec = get_json(f"{QAPI}/chapter_recitations/{reciter}/{s}?segments=true")["audio_file"]
    if item.get("whole_surah"):  # e.g. "kids repeat" recitations have no word segments: take the whole file
        out["audio"] = {"file": f"assets/quran/{item['id']}.wav", "reciter_id": reciter,
                        "source": rec["audio_url"], "clip_ms": None, "duration_s": None}
        if want_audio:
            dst = audio_dir / f"{item['id']}.wav"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(local_audio(rec["audio_url"], reciter, s)), "-ar", "48000", "-ac", "2",
                            str(dst)], check=True)
            p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(dst)], capture_output=True, text=True)
            out["audio"]["duration_s"] = round(float(p.stdout.strip() or 0), 3)
        return out
    stamps = {t["verse_key"]: t for t in rec["timestamps"]}
    seg = []
    for w in all_words:
        t = stamps[w["key"]]
        hit = [g for g in t.get("segments", []) if len(g) >= 3 and int(g[0]) == w["pos"]]
        if not hit:
            raise ValueError(f"{item['id']}: reciter {reciter} has no segment for word {w['key']}#{w['pos']}")
        seg.append((float(hit[0][1]), float(hit[0][2])))
    if wr:
        t0, t1 = seg[0][0], seg[-1][1]
    else:  # whole verses: use the verse boundaries (they include the full madd / waqf)
        t0 = float(stamps[f"{s}:{a}"]["timestamp_from"])
        t1 = float(stamps[f"{s}:{b}"]["timestamp_to"])
    # The qdc word segments can sit 0.5-1 s off the audio, so the clip edges snap to the reciter's real pauses
    # (fragments are chosen to start/end on a waqf, where Husary always pauses).
    src = local_audio(rec["audio_url"], reciter, s) if want_audio else None
    clip0, clip1 = t0 - PAD_IN_MS, t1 + PAD_OUT_MS
    if src:
        sil = silences(src, (t0 - 2500) / 1000, (t1 + 3000) / 1000)
        pre = [x for x in sil if (t0 - 2500) / 1000 <= x[1] <= (t0 + 1200) / 1000 and x[1] - x[0] >= 0.3]
        if pre:
            clip0 = (min(pre, key=lambda x: abs(x[1] - t0 / 1000))[1] - 0.12) * 1000
        # end = the FIRST real pause after the last word begins (a later pause would carry the next words)
        lw0 = seg[-1][0] / 1000 - 0.2
        post = [x for x in sil if x[0] >= lw0 and x[1] - x[0] >= 0.3 and x[0] * 1000 > clip0 + 600]
        if post:
            clip1 = (min(post, key=lambda x: x[0])[0] + 0.35) * 1000
        # leading pause longer than 0.15 s is dead air; a sliver (< 0.35 s) of sound before a pause is the
        # previous word's tail
        lead = [x for x in sil if x[0] <= clip0 / 1000 + 0.35 and x[1] > clip0 / 1000 + 0.15
                and (x[0] <= clip0 / 1000 + 0.05 or x[1] - x[0] >= 0.3)]
        if lead:
            clip0 = (lead[0][1] - 0.12) * 1000
        if not post:
            print(f"  !! {item['id']}: no pause found near the end - check the clip by ear")
    clip0 = max(0.0, clip0)
    for w, (g0, g1) in zip(all_words, seg):  # approximate (segment accuracy), for highlight timing only
        w["start"] = round(max(0.0, (g0 - clip0) / 1000), 3)
        w["end"] = round(max(0.0, (g1 - clip0) / 1000), 3)
    out["audio"] = {"file": f"assets/quran/{item['id']}.wav", "reciter_id": reciter,
                    "source": rec["audio_url"], "clip_ms": [round(clip0), round(clip1)],
                    "duration_s": round((clip1 - clip0) / 1000, 3), "word_times": "approximate"}
    if want_audio:
        dst = audio_dir / f"{item['id']}.wav"
        dur = (clip1 - clip0) / 1000
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
               "-af", f"atrim=start={clip0 / 1000:.3f}:duration={dur:.3f},asetpts=PTS-STARTPTS,"
                      f"afade=t=in:d=0.04,afade=t=out:st={max(0, dur - 0.25):.3f}:d=0.25",
               "-ar", "48000", "-ac", "2", str(dst)]
        subprocess.run(cmd, check=True)
    return out


def silences(src, a, b, db=-35, d=0.25):
    """[(start_s, end_s)] of pauses in src between a and b seconds (absolute times)."""
    a = max(0.0, a)
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af",
                        f"atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,silencedetect=noise={db}dB:d={d}",
                        "-f", "null", "-"], capture_output=True, text=True)
    st = [float(x) + a for x in re.findall(r"silence_start: ([\d.]+)", p.stderr)]
    en = [float(x) + a for x in re.findall(r"silence_end: ([\d.]+)", p.stderr)]
    en += [b] * (len(st) - len(en))
    return list(zip(st, en))


def render_script(pp, items):
    src = pp / "script.md"
    if not src.exists():
        return None
    by = {i["id"]: i for i in items}

    def sub(m):
        kind, iid = m.group(1), m.group(2)
        it = by.get(iid)
        if not it:
            return f"[[MISSING {kind}:{iid}]]"
        if it["type"] == "quran":
            return f"﴿{it['text']}﴾ [{it['ref']}]" + (" — مقطع من الآية" if it["is_fragment"] else "")
        return f"«{it['text']}» [{it['ref']}]"

    txt = re.sub(r"\{\{([QH]):([\w-]+)\}\}", sub, src.read_text(encoding="utf-8"))
    dst = pp / "script.rendered.md"
    dst.write_text(txt, encoding="utf-8")
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--no-audio", action="store_true")
    args = ap.parse_args()
    pp = C.project_path(args.project)
    spec = json.loads((pp / "quran.json").read_text(encoding="utf-8"))
    reciter = int(spec.get("reciter", 6))
    audio_dir = pp / "assets" / "quran"
    audio_dir.mkdir(parents=True, exist_ok=True)
    items = []
    for it in spec["items"]:
        if "hadith" in it:
            r = fetch_hadith(it)
        else:
            r = fetch_quran(it, int(it.get("reciter", reciter)), audio_dir, not args.no_audio)
        items.append(r)
        extra = f"  {r['audio']['duration_s']}s" if r.get("audio") else ""
        print(f"  {r['id']:<18} {r['ref']}{extra}")
    out = {"fetched": C.now_iso(), "reciter": reciter,
           "attribution": "Text + audio: quran.com API (Quran Foundation); recitation files: quranicaudio.com; "
                          "tafsir: التفسير الميسر; hadith: fawazahmed0/hadith-api",
           "items": items}
    (audio_dir / "quran.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    r = render_script(pp, items)
    print(f"-> {audio_dir / 'quran.json'}" + (f"\n-> {r}" if r else ""))


if __name__ == "__main__":
    main()
