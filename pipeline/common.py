"""Shared utilities for the Hossam Video Factory pipeline."""
import base64
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "config.json"
KEYS_PATH = ROOT / "config" / "api_keys.json"

# Windows console: force UTF-8 so Arabic/arrow output never crashes print()
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

STAGES = ["ingest", "audio_clean", "transcribe", "plan", "approval",
          "generation", "assembly", "render", "done"]

AUDIO_EXT = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma", ".opus"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi"}
MIME_BY_EXT = {
    ".mp3": "audio/mpeg", ".wav": "audio/wav", ".m4a": "audio/mp4",
    ".aac": "audio/aac", ".ogg": "audio/ogg", ".flac": "audio/flac",
    ".opus": "audio/ogg", ".mp4": "video/mp4", ".webm": "video/webm",
    ".mov": "video/quicktime", ".mkv": "video/x-matroska",
}


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


# Pinned HyperFrames CLI for check/render (0.8.153+ check hits "did not finish within its deadline"; LESSONS §21/§23).
# Override: set HF_CLI=hyperframes@<version>.
HF_CLI = os.environ.get("HF_CLI", "hyperframes@0.8.152")


def load_keys():
    keys = {}
    if KEYS_PATH.exists():
        try:
            with open(KEYS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            keys.update({k: v for k, v in data.items() if not k.startswith("_")})
        except Exception:
            pass
    # environment wins
    for name in list(keys) + ["GEMINI_API_KEY", "OPENAI_API_KEY"]:
        env = os.environ.get(name)
        if env:
            keys[name] = env
    return keys


def get_key(name):
    return load_keys().get(name, "")


def key_status():
    keys = load_keys()
    return {name: bool(keys.get(name)) for name in ["GEMINI_API_KEY", "OPENAI_API_KEY"]}


def projects_dir(cfg=None):
    cfg = cfg or load_config()
    return ROOT / cfg.get("paths", {}).get("projects_dir", "projects")


def sanitize_name(name):
    name = re.sub(r"[^a-zA-Z0-9_\-.]", "-", name.strip()).strip("-.")
    if not name:
        raise SystemExit("Invalid project name")
    return name


def project_path(name, cfg=None):
    return projects_dir(cfg) / sanitize_name(name)


def list_projects():
    pd = projects_dir()
    out = []
    if pd.exists():
        for p in sorted(pd.iterdir()):
            if p.is_dir() and (p / "project.json").exists() and not p.name.startswith("_"):
                out.append(p.name)
    return out


def load_project(name):
    pp = project_path(name)
    pf = pp / "project.json"
    if not pf.exists():
        raise SystemExit(f"Project '{name}' not found. Create it: python pipeline/new_project.py {name}")
    with open(pf, "r", encoding="utf-8") as f:
        return json.load(f)


def save_project(name, data):
    pp = project_path(name)
    with open(pp / "project.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_stage(name, stage, note=""):
    data = load_project(name)
    prev = data.get("stage")
    data["stage"] = stage
    data["updated"] = now_iso()
    hist = data.setdefault("stage_history", [])
    hist.append({"stage": stage, "at": now_iso(), "note": note, "from": prev})
    save_project(name, data)
    return data


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def log(name, msg):
    pp = project_path(name)
    pp.mkdir(parents=True, exist_ok=True)
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    with open(pp / "pipeline.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def tail_log(name, lines=200):
    pp = project_path(name) / "pipeline.log"
    if not pp.exists():
        return ""
    try:
        content = pp.read_text(encoding="utf-8", errors="replace")
        return "\n".join(content.splitlines()[-lines:])
    except Exception:
        return ""


def run(cmd, cwd=None, timeout=600):
    """Run a subprocess command, return CompletedProcess (raises on timeout).
    On Windows, resolves .cmd/.bat shims (npx, npm...) to their full path."""
    import shutil
    exe = str(cmd[0])
    if os.name == "nt" and not Path(exe).suffix:
        resolved = shutil.which(exe)
        if resolved:
            cmd = [resolved] + list(cmd[1:])
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout)


def ffmpeg(args, timeout=1800):
    cmd = ["ffmpeg", "-hide_banner", "-y"] + args
    r = run(cmd, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{r.stderr[-3000:]}")
    return r


def ffprobe_duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)])
    if r.returncode != 0:
        raise RuntimeError(f"ffprobe failed on {path}: {r.stderr}")
    return float(r.stdout.strip())


def http_json(url, method="POST", headers=None, body=None, timeout=180):
    """body: bytes or str or dict(JSON). Returns (status, parsed-or-text)."""
    if isinstance(body, dict):
        body = json.dumps(body).encode("utf-8")
    elif isinstance(body, str):
        body = body.encode("utf-8")
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, raw


def http_download(url, dest: Path, headers=None, timeout=600):
    req = urllib.request.Request(url)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(dest, "wb") as f:
        while True:
            chunk = resp.read(65536)
            if not chunk:
                break
            f.write(chunk)


def b64_file(path):
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


def b64_decode(data: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(base64.b64decode(data))


def extract_json(text):
    """Robustly extract the first JSON object from LLM output."""
    if isinstance(text, dict):
        return text
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in output: {text[:300]}")
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError(f"Unbalanced JSON in output: {text[:300]}")


def find_input_audio(name):
    """Locate the raw voice file in a project's input/ folder."""
    inp = project_path(name) / "input"
    if not inp.exists():
        return None
    files = [f for f in sorted(inp.iterdir())
             if f.suffix.lower() in (AUDIO_EXT | VIDEO_EXT) and not f.name.startswith(".")]
    # prefer an explicit voice file, then audio-only files; screen clips (screen_*.mp4) are never the voice
    def rank(f):
        n = f.stem.lower()
        return (0 if n.startswith(("voice", "voiceover", "rawreel")) else 1,
                0 if f.suffix.lower() in AUDIO_EXT else 1,
                1 if n.startswith(("screen", "clip", "broll")) else 0)
    files.sort(key=rank)
    return files[0] if files else None


def find_script(name):
    inp = project_path(name) / "input"
    if not inp.exists():
        return None
    for f in sorted(inp.iterdir()):
        if f.suffix.lower() in (".md", ".txt") and not f.name.startswith("."):
            return f
    return None


def mime_for(path: Path):
    return MIME_BY_EXT.get(Path(path).suffix.lower(), "application/octet-stream")


def read_prompt(rel_path, cfg=None):
    p = ROOT / rel_path
    return p.read_text(encoding="utf-8")


class PermanentError(RuntimeError):
    """Non-retryable failure (4xx etc.) — retry() must not re-send the payload."""


def retry(fn, attempts=3, delay=5, label="call"):
    last = None
    for i in range(attempts):
        try:
            return fn()
        except PermanentError:
            raise
        except Exception as e:
            last = e
            if i < attempts - 1:
                time.sleep(delay * (i + 1))
    raise RuntimeError(f"{label} failed after {attempts} attempts: {last}")


def cost(cfg, key, default=0.0):
    return float(cfg.get("costs", {}).get(key, default))


def scene_cost(scene, cfg):
    """Estimate USD cost of a storyboard scene."""
    img = cost(cfg, "per_image_usd")
    vids = cost(cfg, "per_video_second_usd")
    m = scene.get("method")
    secs = float(scene.get("video_clip_seconds") or 0) or min(8.0, (scene.get("end", 0) - scene.get("start", 0)))
    if m in ("direct_image", "image_animate"):
        c = img
    elif m == "first_last_frame":
        c = 2 * img
    elif m == "text_to_video":
        c = 0.0
    else:
        return 0.0
    if m in ("image_animate", "first_last_frame", "text_to_video"):
        c += secs * vids
    return round(c, 3)


METHODS = ["code", "direct_image", "image_animate", "first_last_frame",
           "text_to_video", "screenshot", "hossam_image"]
AI_VIDEO_METHODS = {"image_animate", "first_last_frame", "text_to_video"}
IMAGE_METHODS = {"direct_image", "image_animate", "first_last_frame"}
