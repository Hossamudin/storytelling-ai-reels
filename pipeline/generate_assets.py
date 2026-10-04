"""04 - Generate assets for an APPROVED storyboard (AI images + AI videos), with cost ledger.

Usage: python pipeline/generate_assets.py <name> [--force] [--only S03,S05] [--no-video]

Approval gate: refuses to run unless storyboard.status == "approved"
(override with --force ONLY after the user explicitly approved in chat).
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


# ---------------------------------------------------------------- image providers
def placeholder_png(dest: Path, rgb=(19, 96, 82), size=(96, 96)):
    """Tiny solid-color PNG for mock/offline mode (no dependencies)."""
    import struct
    import zlib
    w, h = size
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))

    png = (b"\x89PNG\r\n\x1a\n" +
           chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) +
           chunk(b"IDAT", zlib.compress(raw)) +
           chunk(b"IEND", b""))
    dest.write_bytes(png)
    return str(dest)


MOCK_IMAGES = {"_mode": False}


def gen_image(prompt, aspect, dest, cfg):
    if MOCK_IMAGES["_mode"]:
        colors = [(19, 96, 82), (255, 90, 51), (179, 206, 101), (255, 236, 92)]
        return placeholder_png(Path(dest), colors[hash(dest.name) % len(colors)])
    provider = cfg["image"]["provider"]
    fn = gen_image_openai if provider == "openai" else gen_image_gemini
    return C.retry(lambda: fn(prompt, aspect, dest, cfg), attempts=3, delay=8, label=f"image {dest.name}")


def gen_image_openai(prompt, aspect, dest: Path, cfg):
    key = C.get_key("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    ic = cfg["image"]["openai"]
    size = ic.get("size_map", {}).get(aspect, "1024x1024")
    url = f"{ic['api_base']}/images/generations"
    body = {"model": ic["model"], "prompt": prompt, "size": size,
            "quality": ic.get("quality", "medium"), "n": 1}
    status, resp = C.http_json(url, headers={"Authorization": f"Bearer {key}"},
                               body=body, timeout=300)
    if status != 200:
        err = f"OpenAI image error {status}: {str(resp)[:400]}"
        raise C.PermanentError(err) if 400 <= status < 500 and status != 429 else RuntimeError(err)
    item = resp["data"][0]
    b64 = item.get("b64_json") or ""
    if not b64 and item.get("url"):
        import urllib.request
        with urllib.request.urlopen(item["url"], timeout=300) as r:
            dest.write_bytes(r.read())
        return str(dest)
    if not b64:
        raise RuntimeError(f"No image data in response: {str(resp)[:300]}")
    C.b64_decode(b64, dest)
    return str(dest)


def gen_image_gemini(prompt, aspect, dest: Path, cfg):
    key = C.get_key("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set")
    ic = cfg["image"]["gemini"]
    url = f"{ic['api_base']}/v1beta/models/{ic['model']}:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
    status, resp = C.http_json(url, headers={"x-goog-api-key": key}, body=body, timeout=300)
    if status != 200:
        err = f"Gemini image error {status}: {str(resp)[:400]}"
        raise C.PermanentError(err) if 400 <= status < 500 and status != 429 else RuntimeError(err)
    for part in resp.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        d = part.get("inlineData") or part.get("inline_data")
        if d:
            C.b64_decode(d["data"], dest)
            return str(dest)
    raise RuntimeError("Gemini image response contained no image part")


# ---------------------------------------------------------------- video provider
def extract_video_b64(op: dict):
    """Find base64 mp4 data anywhere in a predictLongRunning operation response."""
    def hunt(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                kl = k.lower()
                if kl in ("bytesbase64encoded", "b64_json", "videobase64") and isinstance(v, str) and len(v) > 1000:
                    return v
                r = hunt(v)
                if r:
                    return r
        elif isinstance(obj, list):
            for v in obj:
                r = hunt(v)
                if r:
                    return r
        return None
    return hunt(op)


def gen_video_gemini(prompt, negative, aspect, first_frame: Path, last_frame: Path,
                     dest: Path, cfg, scene_id):
    key = C.get_key("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set")
    vc = cfg["video"]["gemini_video"]
    url = f"{vc['api_base']}/v1beta/models/{vc['model']}:{vc['method']}"
    inst = {"prompt": prompt}
    if first_frame and Path(first_frame).exists():
        inst["image"] = {"bytesBase64Encoded": C.b64_file(first_frame),
                         "mimeType": C.mime_for(first_frame)}
    if last_frame and Path(last_frame).exists():
        inst["lastFrame"] = {"bytesBase64Encoded": C.b64_file(last_frame),
                             "mimeType": C.mime_for(last_frame)}
    params = {"aspectRatio": aspect, "resolution": vc.get("resolution", "720p")}
    if negative:
        params["negativePrompt"] = negative
    body = {"instances": [inst], "parameters": params}
    status, resp = C.http_json(url, headers={"x-goog-api-key": key}, body=body, timeout=300)
    if status != 200:
        raise RuntimeError(f"Video gen submit error {status}: {str(resp)[:400]}")
    op_name = resp.get("name")
    if not op_name:
        raise RuntimeError(f"No operation name in response: {str(resp)[:300]}")

    C.log(scene_id, f"video operation submitted: {op_name}")
    t0 = time.time()
    while time.time() - t0 < vc.get("timeout_s", 600):
        time.sleep(vc.get("poll_interval_s", 10))
        st, op = C.http_json(f"{vc['api_base']}/v1beta/{op_name}",
                             method="GET", headers={"x-goog-api-key": key}, timeout=120)
        if st != 200:
            C.log(scene_id, f"poll error {st}: {str(op)[:200]}")
            continue
        if isinstance(op, dict) and op.get("done"):
            if op.get("error"):
                raise RuntimeError(f"Video operation failed: {op['error']}")
            b64 = extract_video_b64(op)
            if not b64:
                raise RuntimeError(f"Operation done but no video data: {str(op)[:400]}")
            C.b64_decode(b64, dest)
            return str(dest)
    raise TimeoutError(f"Video generation timed out after {vc.get('timeout_s', 600)}s")


# ---------------------------------------------------------------- ledger
def ledger_add(pp, entry):
    lp = pp / "assets" / "ledger.json"
    data = {"entries": []}
    if lp.exists():
        try:
            data = json.loads(lp.read_text(encoding="utf-8"))
        except Exception:
            pass
    entry["at"] = C.now_iso()
    data["entries"].append(entry)
    data["total_cost_usd"] = round(sum(e.get("cost_usd", 0) for e in data["entries"]), 3)
    lp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--force", action="store_true", help="bypass approval gate (explicit user approval only)")
    ap.add_argument("--only", default="", help="comma-separated scene ids")
    ap.add_argument("--no-video", action="store_true")
    ap.add_argument("--mock", action="store_true", help="offline: placeholder images, no API calls")
    args = ap.parse_args()

    MOCK_IMAGES["_mode"] = args.mock
    if args.mock:
        args.no_video = True  # mock mode must never reach a paid video API

    cfg = C.load_config()
    pp = C.project_path(args.name)
    sb_path = pp / "storyboard.json"
    if not sb_path.exists():
        raise SystemExit("No storyboard. Run plan_scenes.py first.")
    sb = json.loads(sb_path.read_text(encoding="utf-8"))

    if sb.get("status") != "approved" and not args.force:
        raise SystemExit("STORYBOARD NOT APPROVED — generation blocked to save credits.\n"
                         "Approve via dashboard (python dashboard/server.py) then re-run, "
                         "or use --force only if the user explicitly approved in chat.")

    aspect = sb.get("aspect") or cfg["video_defaults"]["aspect"]
    only = {s.strip() for s in args.only.split(",") if s.strip()}
    img_dir, vid_dir = pp / "assets" / "images", pp / "assets" / "videos"
    img_dir.mkdir(parents=True, exist_ok=True)
    vid_dir.mkdir(parents=True, exist_ok=True)

    C.update_stage(args.name, "generation", "asset generation started")
    generated, failed = 0, []
    per_img = 0.0 if args.mock else C.cost(cfg, "per_image_usd")
    per_vid_s = C.cost(cfg, "per_video_second_usd")

    for s in sb["scenes"]:
        if only and s["id"] not in only:
            continue
        m, sid = s["method"], s["id"]
        if m not in (C.IMAGE_METHODS | C.AI_VIDEO_METHODS):
            continue

        # ---- images first
        first_path = last_path = None
        if m in C.IMAGE_METHODS:
            prompt = s["image_prompt"]
            first_path = img_dir / f"{sid}_first.png"
            if not first_path.exists():
                C.log(args.name, f"{sid}: generating image -> {first_path.name}")
                try:
                    gen_image(prompt, aspect, first_path, cfg)
                    ledger_add(pp, {"scene": sid, "kind": "image", "file": str(first_path.name),
                                    "model": cfg["image"][cfg["image"]["provider"]]["model"],
                                    "cost_usd": per_img})
                    generated += 1
                except Exception as e:
                    C.log(args.name, f"{sid}: IMAGE FAILED: {e}")
                    failed.append(f"{sid}:image")
                    continue
            if m == "first_last_frame":
                last_path = img_dir / f"{sid}_last.png"
                if not last_path.exists():
                    try:
                        gen_image(s.get("last_image_prompt") or s["image_prompt"],
                                  aspect, last_path, cfg)
                        ledger_add(pp, {"scene": sid, "kind": "image", "file": str(last_path.name),
                                        "model": cfg["image"][cfg["image"]["provider"]]["model"],
                                        "cost_usd": per_img})
                        generated += 1
                    except Exception as e:
                        C.log(args.name, f"{sid}: LAST IMAGE FAILED: {e}")
                        failed.append(f"{sid}:last_image")
                        continue

        # ---- videos
        if m in C.AI_VIDEO_METHODS and not args.no_video:
            vpath = vid_dir / f"{sid}.mp4"
            if not vpath.exists():
                secs = C.clip_seconds(s)  # same rule as the approved estimate
                vp = (s["video_prompt"] +
                      f" Duration: about {secs:.0f} seconds. Aspect ratio {aspect}.")
                C.log(args.name, f"{sid}: generating video ({m}, {secs:.0f}s) -> {vpath.name}")
                try:
                    gen_video_gemini(vp, s.get("negative_prompt") or
                                     cfg["video"]["gemini_video"].get("negative_prompt", ""),
                                     aspect, first_path, last_path, vpath, cfg, args.name)
                    ledger_add(pp, {"scene": sid, "kind": "video", "file": str(vpath.name),
                                    "model": cfg["video"]["gemini_video"]["model"],
                                    "seconds": secs, "cost_usd": round(secs * per_vid_s, 3)})
                    generated += 1
                except Exception as e:
                    C.log(args.name, f"{sid}: VIDEO FAILED: {e}")
                    failed.append(f"{sid}:video")
                    continue

        # record asset paths in storyboard
        s.setdefault("assets", {})
        if first_path and first_path.exists():
            s["assets"]["first_frame"] = str(first_path.relative_to(pp))
        if last_path and last_path.exists():
            s["assets"]["last_frame"] = str(last_path.relative_to(pp))
        if (vid_dir / f"{sid}.mp4").exists():
            s["assets"]["video"] = str((vid_dir / f"{sid}.mp4").relative_to(pp))
        sb_path.write_text(json.dumps(sb, indent=2, ensure_ascii=False), encoding="utf-8")

    ledger = json.loads((pp / "assets" / "ledger.json").read_text(encoding="utf-8")) \
        if (pp / "assets" / "ledger.json").exists() else {"total_cost_usd": 0}
    proj = C.load_project(args.name)
    proj["total_cost_usd"] = ledger.get("total_cost_usd", 0)
    C.save_project(args.name, proj)
    C.log(args.name, f"generation done: {generated} assets, "
                     f"${ledger.get('total_cost_usd', 0)} total, failures: {failed or 'none'}")

    print(f"\nGenerated: {generated} assets | Ledger total: ${ledger.get('total_cost_usd', 0)}")
    if failed:
        print(f"FAILED (retry with: python pipeline/generate_assets.py {args.name} --only "
              f"{','.join(f.split(':')[0] for f in failed)}): {failed}")
    print(f"Next: python pipeline/captions.py {args.name} && python pipeline/assemble.py {args.name}")


if __name__ == "__main__":
    main()
