"""Check this computer for video production: hardware, tools, Python packages, keys (presence only).

Usage:
  python env_check.py            # friendly report + what to install (with the exact command for this OS)
  python env_check.py --json     # machine-readable (the agent stores a summary in <studio>/profile.md)

Never prints key values. Safe to run any time; it only reads.
"""
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

OS = platform.system()  # Windows / Darwin / Linux
KEYS = ["OPENAI_API_KEY", "GEMINI_API_KEY", "ELEVENLABS_API_KEY"]

INSTALL = {
    "python": {"Windows": "winget install Python.Python.3.12", "Darwin": "brew install python@3.12", "Linux": "sudo apt install python3 python3-pip"},
    "node": {"Windows": "winget install OpenJS.NodeJS.LTS", "Darwin": "brew install node", "Linux": "curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt install -y nodejs"},
    "ffmpeg": {"Windows": "winget install Gyan.FFmpeg", "Darwin": "brew install ffmpeg", "Linux": "sudo apt install ffmpeg"},
    "git": {"Windows": "winget install Git.Git", "Darwin": "xcode-select --install", "Linux": "sudo apt install git"},
    "blender": {"Windows": "winget install BlenderFoundation.Blender", "Darwin": "brew install --cask blender", "Linux": "sudo snap install blender --classic"},
}
PIP = {
    "numpy": "numpy", "PIL": "pillow", "requests": "requests",
    "faster_whisper": "faster-whisper", "playwright": "playwright",
}
WHY = {
    "python": "runs the studio engine scripts",
    "node": "runs HyperFrames (the HTML-to-video renderer) via npx",
    "ffmpeg": "cuts, cleans and encodes audio/video",
    "git": "optional: version history for your projects",
    "blender": "optional: real 3D modelling/rendering (the 3D skill can also work without it)",
    "numpy": "audio analysis for cuts", "PIL": "image work (contact sheets, cutouts)", "requests": "API calls",
    "faster_whisper": "FREE offline transcription (no API key needed)",
    "playwright": "optional: captures real web pages as evidence screenshots",
}


def run(cmd, timeout=60):
    exe = shutil.which(cmd[0])
    if not exe:
        return None
    try:
        r = subprocess.run([exe] + cmd[1:], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        return (r.stdout or r.stderr or "").strip()
    except Exception:
        return None


def ram_gb():
    try:
        if OS == "Windows":
            import ctypes

            class MS(ctypes.Structure):
                _fields_ = [("l", ctypes.c_ulong), ("load", ctypes.c_ulong), ("total", ctypes.c_ulonglong), ("avail", ctypes.c_ulonglong),
                            ("tp", ctypes.c_ulonglong), ("ap", ctypes.c_ulonglong), ("tv", ctypes.c_ulonglong), ("av", ctypes.c_ulonglong),
                            ("ae", ctypes.c_ulonglong)]
            m = MS()
            m.l = ctypes.sizeof(MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return round(m.total / 2**30, 1)
        if OS == "Darwin":
            return round(int(run(["sysctl", "-n", "hw.memsize"]) or 0) / 2**30, 1)
        with open("/proc/meminfo") as f:
            return round(int(f.readline().split()[1]) / 2**20, 1)
    except Exception:
        return None


def gpu():
    out = run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], timeout=20)
    if out and "failed" not in out.lower():
        return {"kind": "nvidia", "name": out.splitlines()[0]}
    if OS == "Darwin" and platform.machine() == "arm64":
        return {"kind": "apple", "name": "Apple Silicon (Metal / CoreML)"}
    if OS == "Windows":
        o = run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_VideoController).Name"], timeout=30)
        if o:
            return {"kind": "other", "name": "; ".join(x.strip() for x in o.splitlines() if x.strip())}
    return {"kind": "none", "name": "no dedicated GPU detected"}


def studio_keys():
    present = {k: bool(os.environ.get(k)) for k in KEYS}
    ptr = Path.home() / ".video-studio.json"
    if ptr.exists():
        try:
            home = Path(json.loads(ptr.read_text(encoding="utf-8"))["home"])
            kf = home / "config" / "api_keys.json"
            if kf.exists():
                data = json.loads(kf.read_text(encoding="utf-8"))
                for k in KEYS:
                    present[k] = present[k] or bool(data.get(k))
        except Exception:
            pass
    return present


def main():
    as_json = "--json" in sys.argv
    tools = {
        "python": sys.version.split()[0],
        "node": run(["node", "--version"]),
        "npx": run(["npx", "--version"]),
        "ffmpeg": (run(["ffmpeg", "-version"]) or "").split("\n")[0][:60] or None,
        "ffprobe": bool(shutil.which("ffprobe")),
        "git": run(["git", "--version"]),
        "blender": (run(["blender", "--version"], timeout=60) or "").split("\n")[0] or None,
        "chrome": bool(shutil.which("chrome") or shutil.which("google-chrome") or Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe").exists()
                       or Path("/Applications/Google Chrome.app").exists()),
    }
    hf = run(["npx", "--yes", "hyperframes", "--version"], timeout=240) if tools["npx"] else None
    tools["hyperframes"] = hf.splitlines()[-1] if hf else None
    py = {}
    for mod in PIP:
        try:
            __import__(mod)
            py[mod] = True
        except Exception:
            py[mod] = False
    disk = shutil.disk_usage(str(Path.home()))
    info = {
        "os": f"{OS} {platform.release()} ({platform.machine()})",
        "cpu_cores": os.cpu_count(),
        "ram_gb": ram_gb(),
        "gpu": gpu(),
        "disk_free_gb": round(disk.free / 2**30, 1),
        "tools": tools,
        "python_packages": py,
        "keys_present": studio_keys(),
    }
    # what this machine can comfortably do
    ram = info["ram_gb"] or 0
    g = info["gpu"]["kind"]
    info["capability"] = {
        "render_1080p": "comfortable" if (info["cpu_cores"] or 0) >= 8 and ram >= 16 else "ok but slow (render overnight / shorter parts)",
        "local_transcription": ("fast (GPU)" if g in ("nvidia", "apple") else "ok on CPU (~real time with the 'small' model)") if py["faster_whisper"]
        else "not installed (free): pip install faster-whisper",
        "background_removal": "fast (GPU)" if g in ("nvidia", "apple") else "slow on CPU (0.3–0.8 s/frame: start it early, in the background)",
        "3d": "Blender available" if tools["blender"] else "browser 3D (Three.js) or AI 3D only — Blender optional",
        "disk": "ok" if info["disk_free_gb"] >= 20 else "LOW: video work needs 20+ GB free",
    }
    missing = []
    for t in ("node", "ffmpeg"):
        if not tools[t]:
            missing.append({"what": t, "why": WHY[t], "install": INSTALL[t].get(OS, "")})
    for mod in ("numpy", "PIL", "requests"):
        if not py[mod]:
            missing.append({"what": PIP[mod], "why": WHY[mod], "install": f"{sys.executable} -m pip install {PIP[mod]}"})
    optional = []
    if not py["faster_whisper"]:
        optional.append({"what": "faster-whisper", "why": WHY["faster_whisper"], "install": f"{sys.executable} -m pip install faster-whisper"})
    if not py["playwright"]:
        optional.append({"what": "playwright", "why": WHY["playwright"], "install": f"{sys.executable} -m pip install playwright && {sys.executable} -m playwright install chromium"})
    if not tools["blender"]:
        optional.append({"what": "blender", "why": WHY["blender"], "install": INSTALL["blender"].get(OS, "")})
    if tools["npx"] and not tools["hyperframes"]:
        missing.append({"what": "hyperframes", "why": "renders HTML compositions to MP4", "install": "npx --yes hyperframes doctor"})
    info["missing_required"] = missing
    info["optional"] = optional

    if as_json:
        print(json.dumps(info, indent=2, ensure_ascii=False))
        return
    ok = lambda b: "✓" if b else "✗"
    print("=== Your machine ===")
    print(f"  System   {info['os']} · {info['cpu_cores']} CPU cores · {info['ram_gb']} GB RAM · {info['disk_free_gb']} GB free")
    print(f"  GPU      {info['gpu']['name']}")
    print("=== Tools ===")
    for k in ("python", "node", "ffmpeg", "hyperframes", "git", "blender"):
        print(f"  {ok(tools.get(k))} {k:<12} {tools.get(k) or 'not found'}")
    print("=== Python packages ===")
    print("  " + "  ".join(f"{ok(v)} {PIP[k]}" for k, v in py.items()))
    print("=== Keys (presence only) ===")
    print("  " + "  ".join(f"{ok(v)} {k}" for k, v in info["keys_present"].items()))
    print("=== What this machine can do ===")
    for k, v in info["capability"].items():
        print(f"  · {k.replace('_', ' ')}: {v}")
    if missing:
        print("=== REQUIRED — install these first ===")
        for m in missing:
            print(f"  · {m['what']} — {m['why']}\n      {m['install']}")
    if optional:
        print("=== Optional (nice to have) ===")
        for m in optional:
            print(f"  · {m['what']} — {m['why']}\n      {m['install']}")
    print("\nREADY" if not missing else "\nNOT READY YET — install the required items above, then run this again.")
    sys.exit(0 if not missing else 1)


if __name__ == "__main__":
    main()
