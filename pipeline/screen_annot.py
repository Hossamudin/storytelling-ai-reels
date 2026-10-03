"""Convert source-time screen annotations into output-time data for the composition.

Usage: python pipeline/screen_annot.py <name> [--part composition] [--times 77.06 159.68 ...]

Reads  projects/<name>/input/annotations.json   (authored in SOURCE seconds / SOURCE pixels)
       projects/<name>/assets/screen/edit_map.json  (from screen_edit.py)
Writes projects/<name>/<part>/assets/screen/annot.js   (window.HF_ANNOT for kit/motion/js/screen.js)
       projects/<name>/<part>/assets/screen/cutaways.json  (output windows for scenes.json)

annotations.json:
{
  "window": {"x": 64, "y": 140, "k": 0.9343},          # where the recording sits in the 1920x1080 frame
  "items": [
    {"type": "zoom",  "src": 47.0, "d": 0.8, "rect": [750, 272, 422, 310], "s": 1.8},
    {"type": "spot",  "src": [49.4, 55.6], "rect": [820, 352, 326, 38], "ar": "اسم المشروع", "en": "NAME", "pos": "bottom", "circle": false},
    {"type": "click", "src": 70.9, "x": 1109, "y": 540},
    {"type": "blur",  "rect": [8, 728, 264, 72]},
    {"type": "badge", "out": [53.13, 55.37], "text": "×4", "ar": "تسريع"}     # "out" = already output time
  ],
  "cutaways": [{"id": "c1", "src": [75.28, null], "until_out": 53.13, "label": "5 sections"}]
}
--times prints the output time of any source times (handy while authoring).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C
from screen_edit import map_time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--part", default="composition")
    ap.add_argument("--times", nargs="*", type=float)
    a = ap.parse_args()
    pp = C.project_path(a.name)
    em = json.loads((pp / "assets/screen/edit_map.json").read_text(encoding="utf-8"))
    segs = em["segments"]
    M = lambda t: map_time(segs, t)
    if a.times:
        for t in a.times:
            print(f"src {t:8.2f} -> out {M(t):8.3f}")
        return
    spec = json.loads((pp / "input/annotations.json").read_text(encoding="utf-8"))
    crop = em["crop"] or [0, 0, 1920, 1080]
    win = spec["window"]
    out_items = []
    for it in spec["items"]:
        o = {k: v for k, v in it.items() if k not in ("src", "out")}
        if "out" in it:
            v = it["out"]
        elif "src" in it:
            v = it["src"]
            v = [M(v[0]), M(v[1])] if isinstance(v, list) else M(v)
        else:
            v = None
        if isinstance(v, list):
            o["t0"], o["t1"] = round(v[0], 3), round(v[1], 3)
        elif v is not None:
            o["t"] = round(v, 3)
        out_items.append(o)
    data = {"k": win["k"], "x": win["x"], "y": win["y"], "w": crop[2], "h": crop[3], "duration": em["duration"], "items": out_items}
    dest = pp / a.part / "assets/screen"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "annot.js").write_text("window.HF_ANNOT = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    cws = []
    for c in spec.get("cutaways", []):
        s0 = M(c["src"][0]) if c["src"][0] is not None else c["out"][0]
        s1 = c.get("until_out") or (M(c["src"][1]) if c["src"][1] is not None else em["duration"])
        cws.append({"id": c["id"], "start": round(s0, 3), "duration": round(s1 - s0, 3), "beat": c.get("label", "")})
    (dest / "cutaways.json").write_text(json.dumps(cws, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK: {len(out_items)} annotations, {len(cws)} cutaways -> {dest}")
    for c in cws:
        print(f"  {c['id']}: {c['start']:.2f} + {c['duration']:.2f}s  {c['beat']}")


if __name__ == "__main__":
    main()
