"""03 - Plan scenes: transcript -> storyboard (LLM or mock) + validation + cost estimate.

Usage: python pipeline/plan_scenes.py <name> [--provider gemini_api|mock] [--aspect 9:16|16:9]

Output: storyboard.json + storyboard.md (status=draft). GENERATION REFUSES TO RUN
until the storyboard is approved via dashboard or approve_storyboard.py.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

VALID_STYLES = {"motion_graphics", "vox_animation", "whiteboard_explainer",
                "scientific_infographic", "3d_animation", "clay_animation",
                "stop_motion", "cinematic_broll"}


def build_system_prompt(cfg, aspect):
    tpl = C.read_prompt(cfg["planning"]["system_prompt_file"])
    fills = {
        "{hook_max_s}": str(cfg["hook"]["max_duration_s"]),
        "{video_max_s}": str(cfg["video"]["gemini_video"]["max_clip_duration_s"]),
        "{cost_image}": str(cfg["costs"]["per_image_usd"]),
        "{cost_video_per_s}": str(cfg["costs"]["per_video_second_usd"]),
        "{budget_hint}": "8",
        "{aspect}": aspect,
    }
    for k, v in fills.items():
        tpl = tpl.replace(k, v)
    return tpl


def build_user_prompt(cfg, transcript, aspect, script_text=""):
    lines = [
        "## TRANSCRIPT (JSON, word-level timestamps)",
        json.dumps(transcript["segments"], ensure_ascii=False),
        "",
        f"Total audio duration: {transcript['duration_s']}s. Target aspect: {aspect}.",
    ]
    if script_text:
        lines += ["", "## SCRIPT NOTES (from the creator)", script_text]
    return "\n".join(lines)


def call_gemini_planner(cfg, system, user, api_key, model=None):
    p = cfg["planning"]
    model = model or p["model"]
    url = f"{p['api_base']}/v1beta/models/{model}:generateContent"
    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"parts": [{"text": user}]}],
        "generationConfig": {"temperature": p.get("temperature", 0.4),
                             "responseMimeType": "application/json",
                             "maxOutputTokens": 32768},
    }
    status, resp = C.http_json(url, headers={"x-goog-api-key": api_key}, body=body, timeout=300)
    if status != 200:
        err = f"Gemini planner error {status} ({model}): {json.dumps(resp)[:400]}"
        raise C.PermanentError(err) if 400 <= status < 500 and status != 429 else RuntimeError(err)
    try:
        text = resp["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise C.PermanentError(f"Unexpected Gemini response: {json.dumps(resp)[:400]}")
    return C.extract_json(text)


def mock_plan(transcript, aspect):
    """Deterministic offline storyboard used by selftest / dry runs."""
    dur = transcript["duration_s"]
    segs = transcript["segments"]
    hook_end = min(12.0, dur * 0.15)
    scenes = []
    sid = 1
    # hook: 3 rapid cuts
    for i in range(3):
        s = hook_end * i / 3
        e = hook_end * (i + 1) / 3
        seg = segs[min(i, len(segs) - 1)]
        method = ["code", "text_to_video", "code"][i]
        scenes.append({
            "id": f"S{sid:02d}", "start": round(s, 2), "end": round(e, 2),
            "narration": seg["text"][:60], "beat": "hook",
            "style": "motion_graphics" if method == "code" else "cinematic_broll",
            "method": method,
            "headline": seg["text"].split()[0] if seg["text"] else "",
            "image_prompt": "", "video_prompt": "" if method == "code" else
            "Ultra-clean premium abstract shot, " + aspect + ", slow push-in on a glowing geometric network in #136052/#FF5A33, plays under Arabic narration hook, no voice, no music, soft whoosh only.",
            "negative_prompt": "", "video_clip_seconds": 0 if method == "code" else round(e - s, 1),
            "sfx": "impact" if i == 0 else "whoosh", "caption_keywords": ["AI"],
            "hossam_image_hint": "", "screenshot_hint": "", "notes": "mock hook scene",
        })
        sid += 1
    # body scenes aligned to remaining transcript segments
    for seg in segs[1:]:
        s = max(hook_end, seg["start"])
        e = seg["end"]
        if e - s < 1.0:
            continue
        method = "code" if sid % 2 == 0 else "direct_image"
        scenes.append({
            "id": f"S{sid:02d}", "start": round(s, 2), "end": round(e, 2),
            "narration": seg["text"], "beat": "explain",
            "style": "motion_graphics" if method == "code" else "scientific_infographic",
            "method": method,
            "headline": " ".join(seg["text"].split()[:3]),
            "image_prompt": "" if method == "code" else f"Premium minimal 2D vector editorial illustration, {aspect}, layered z-depth for parallax, palette strictly #136052 #437F3E #B3CE65 #FFEC5C #FF5A33 on warm off-white, generous negative space.",
            "video_prompt": "", "negative_prompt": "", "video_clip_seconds": 0,
            "sfx": "none", "caption_keywords": ["AI"],
            "hossam_image_hint": "", "screenshot_hint": "", "notes": "mock body scene",
        })
        sid += 1
    # closing quote card (never overlaps body scenes)
    quote_start = max(scenes[-1]["end"] - 0.0, dur - 4.0)
    if dur - quote_start >= 1.2:
        scenes.append({
            "id": f"S{sid:02d}", "start": round(quote_start, 2), "end": round(dur, 2),
        "narration": segs[-1]["text"] if segs else "", "beat": "quote",
        "style": "motion_graphics", "method": "code", "headline": "ابدأ النهاردة",
        "image_prompt": "", "video_prompt": "", "negative_prompt": "",
        "video_clip_seconds": 0, "sfx": "riser", "caption_keywords": [],
        "hossam_image_hint": "", "screenshot_hint": "",
        "notes": "closing quote card per prompts/quote_design.md",
    })
    return {"title": "Mock Title", "logline": "mock storyboard", "aspect": aspect,
            "scenes": scenes}


def validate_and_fix(sb, transcript, cfg):
    """Enforce storyboard invariants; returns (storyboard, warnings)."""
    warns = []
    dur = transcript["duration_s"]
    scenes = sorted(sb.get("scenes", []), key=lambda s: float(s.get("start", 0)))
    if not scenes:
        raise RuntimeError("Storyboard has no scenes")

    # renumber, clamp, kill overlaps/gaps by snapping boundaries
    for i, s in enumerate(scenes):
        s["id"] = f"S{i + 1:02d}"
        s["start"] = round(float(s.get("start", 0)), 2)
        s["end"] = round(float(s["end"], ) if isinstance(s.get("end"), (int, float)) else s["start"] + 5, 2)
        if s["end"] <= s["start"]:
            s["end"] = round(s["start"] + 2.0, 2)
        if s.get("method") not in C.METHODS:
            warns.append(f"{s['id']}: invalid method '{s.get('method')}' -> code")
            s["method"] = "code"
        if s.get("style") not in VALID_STYLES:
            warns.append(f"{s['id']}: invalid style '{s.get('style')}' -> motion_graphics")
            s["style"] = "motion_graphics"
        for field in ["narration", "headline", "image_prompt", "video_prompt",
                      "negative_prompt", "notes", "screenshot_hint", "hossam_image_hint"]:
            s[field] = str(s.get(field, "") or "")
        if s["method"] in C.IMAGE_METHODS and not s["image_prompt"]:
            warns.append(f"{s['id']}: image method without image_prompt -> downgraded to code")
            s["method"] = "code"
        if s["method"] in C.AI_VIDEO_METHODS and not s["video_prompt"]:
            warns.append(f"{s['id']}: video method without video_prompt -> downgraded to direct_image")
            s["method"] = "direct_image"
        vmax = float(cfg["video"]["gemini_video"]["max_clip_duration_s"])
        v = float(s.get("video_clip_seconds") or 0)
        s["video_clip_seconds"] = round(min(v, vmax), 1) if v else 0
        s["caption_keywords"] = [str(k) for k in (s.get("caption_keywords") or [])][:8]
        s["sfx"] = s.get("sfx", "none") or "none"
        s["estimated_cost_usd"] = C.scene_cost(s, cfg)

    # tile 0 -> duration from intended durations (robust to bad LLM arithmetic)
    starts = [0.0]
    for s in scenes[:-1]:
        starts.append(starts[-1] + (s["end"] - s["start"]))
    kept = []
    for s, st in zip(scenes, starts):
        d = s["end"] - s["start"]
        if st >= dur - 0.3 and kept:
            warns.append(f"{s['id']}: dropped (overruns audio duration {dur}s)")
            continue
        s["start"] = round(st, 2)
        s["end"] = round(min(st + d, dur), 2)
        if s["end"] - s["start"] < 0.3:
            s["end"] = round(s["start"] + 0.3, 2)
        kept.append(s)
    scenes = kept
    last = scenes[-1]
    if abs(last["end"] - dur) > 0.05:
        warns.append(f"last scene end {last['end']} snapped to audio duration {dur}")
        last["end"] = round(dur, 2)
        if last["end"] <= last["start"]:
            last["start"] = round(max(0.0, last["end"] - 1.5), 2)
    for i, s in enumerate(scenes):
        s["id"] = f"S{i + 1:02d}"

    # hook bookkeeping
    hook_end = 0.0
    for s in scenes:
        if s.get("beat") == "hook":
            hook_end = max(hook_end, s["end"])
    hook_ids = [s["id"] for s in scenes if s.get("beat") == "hook"]
    if not hook_ids:
        for s in scenes:
            if s["start"] < min(cfg["hook"]["max_duration_s"], dur * 0.2):
                s["beat"] = "hook"
                hook_ids.append(s["id"])
                hook_end = max(hook_end, s["end"])
        warns.append("no hook beat detected; early scenes tagged as hook — review advised")

    total = round(sum(s["estimated_cost_usd"] for s in scenes), 2)
    sb.update({"scenes": scenes, "status": "draft",
               "total_duration": round(dur, 2),
               "hook": {"end_s": round(hook_end, 2), "scene_ids": hook_ids},
               "estimated_cost_usd": total})
    return sb, warns


def storyboard_md(sb):
    lines = [
        f"# Storyboard — {sb.get('title', '')}", "",
        f"*{sb.get('logline', '')}*", "",
        f"- Aspect: **{sb.get('aspect')}** | Duration: **{sb.get('total_duration')}s** | "
        f"Scenes: **{len(sb['scenes'])}** | Est. cost: **${sb.get('estimated_cost_usd', 0)}** | "
        f"Status: **{sb.get('status', 'draft').upper()}**",
        f"- Hook window: 0 → {sb.get('hook', {}).get('end_s', 0)}s "
        f"({', '.join(sb.get('hook', {}).get('scene_ids', []))})",
        "",
        "| # | Time | Beat | Style | Method | Headline | Cost | Notes |",
        "|---|------|------|-------|--------|----------|------|-------|",
    ]
    for s in sb["scenes"]:
        notes = (s.get("notes", "") or s.get("screenshot_hint", "") or s.get("hossam_image_hint", ""))[:60]
        lines.append(f"| {s['id']} | {s['start']:.1f}–{s['end']:.1f} | {s.get('beat', '')} | "
                     f"{s.get('style', '')} | `{s['method']}` | {s.get('headline', '')} | "
                     f"${s.get('estimated_cost_usd', 0)} | {notes} |")
    lines.append("")
    for s in sb["scenes"]:
        lines += [f"## {s['id']} · {s['start']:.1f}–{s['end']:.1f}s · `{s['method']}` · {s['style']}",
                  f"**Narration:** {s.get('narration', '')}"]
        if s.get("headline"):
            lines.append(f"**Headline:** {s['headline']}")
        if s.get("image_prompt"):
            lines += ["**Image prompt:**", f"> {s['image_prompt']}"]
        if s.get("video_prompt"):
            lines += ["**Video prompt:**", f"> {s['video_prompt']}"]
        if s.get("caption_keywords"):
            lines.append(f"**Keywords:** {', '.join(s['caption_keywords'])}")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--provider", default=None, choices=["gemini_api", "mock"])
    ap.add_argument("--aspect", default=None, choices=["9:16", "16:9", "1:1"])
    args = ap.parse_args()

    cfg = C.load_config()
    pp = C.project_path(args.name)
    tpath = pp / "transcript" / "transcript.json"
    if not tpath.exists():
        raise SystemExit("No transcript. Run transcribe.py first.")
    transcript = json.loads(tpath.read_text(encoding="utf-8"))

    aspect = args.aspect or C.load_project(args.name).get("aspect") or cfg["video_defaults"]["aspect"]
    provider = args.provider or cfg["planning"]["provider"]
    script_text = ""
    sf = C.find_script(args.name)
    if sf:
        script_text = sf.read_text(encoding="utf-8")[:6000]

    C.log(args.name, f"Planning scenes ({provider}) for {transcript['duration_s']}s @{aspect}")

    if provider == "mock":
        sb = mock_plan(transcript, aspect)
    else:
        key = C.get_key("GEMINI_API_KEY")
        if not key:
            raise SystemExit("GEMINI_API_KEY not set (dashboard Keys tab / api_keys.json / env). "
                             "Use --provider mock for offline testing.")
        system = build_system_prompt(cfg, aspect)
        user = build_user_prompt(cfg, transcript, aspect, script_text)
        try:
            sb = C.retry(lambda: call_gemini_planner(cfg, system, user, key),
                         attempts=3, label="planner")
        except (RuntimeError, C.PermanentError):
            fb = cfg["planning"].get("fallback_model")
            if not fb:
                raise
            C.log(args.name, f"planner {cfg['planning']['model']} unavailable -> fallback {fb}")
            sb = C.retry(lambda: call_gemini_planner(cfg, system, user, key, model=fb),
                         attempts=4, delay=10, label="planner-fallback")

    sb, warns = validate_and_fix(sb, transcript, cfg)
    (pp / "storyboard.json").write_text(json.dumps(sb, indent=2, ensure_ascii=False), encoding="utf-8")
    (pp / "storyboard.md").write_text(storyboard_md(sb), encoding="utf-8")

    proj = C.load_project(args.name)
    proj["aspect"] = aspect
    proj["duration_s"] = transcript["duration_s"]
    C.save_project(args.name, proj)
    C.update_stage(args.name, "plan", f"{len(sb['scenes'])} scenes, est ${sb['estimated_cost_usd']}")

    print(f"\nOK: {len(sb['scenes'])} scenes -> {pp / 'storyboard.json'}")
    print(f"Estimated AI generation cost: ${sb['estimated_cost_usd']}")
    for w in warns:
        print(f"  WARN: {w}")
    print("\n=== STORYBOARD ===")
    print(storyboard_md(sb))
    print("REVIEW & APPROVE before generation:")
    print(f"  - Dashboard: python dashboard/server.py  -> http://localhost:{cfg['dashboard']['port']}")
    print(f"  - Then: python pipeline/generate_assets.py {args.name}")


if __name__ == "__main__":
    main()
