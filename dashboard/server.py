"""Hossam Video Factory — local dashboard server (zero dependencies).

Run:  python dashboard/server.py [--port 8788]
Open: http://localhost:8788

Endpoints (JSON):
  GET  /api/state                         -> projects overview + key status
  GET  /api/config      POST /api/config  -> read / deep-merge-write config.json
  GET  /api/keys        POST /api/keys    -> key status / set a key (values never returned)
  GET  /api/project/<name>                -> project + storyboard + ledger + log tail
  POST /api/project/<name>/storyboard     -> save edited storyboard (status -> edited)
  POST /api/project/<name>/approve        -> mark storyboard approved (unblocks generation)
  POST /api/project/<name>/reject         -> back to draft
"""
import argparse
import json
import re
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote, parse_qs

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
import common as C  # noqa: E402

DASH = Path(__file__).resolve().parent
NAME_RE = re.compile(r"^[a-zA-Z0-9_\-.]+$")


def project_overview(name):
    try:
        p = C.load_project(name)
    except SystemExit:
        return None
    sb_path = C.project_path(name) / "storyboard.json"
    sb = {}
    if sb_path.exists():
        try:
            sb = json.loads(sb_path.read_text(encoding="utf-8"))
        except Exception:
            sb = {}
    tpath = C.project_path(name) / "transcript" / "transcript.json"
    return {
        "name": name,
        "title": p.get("title", name),
        "stage": p.get("stage"),
        "updated": p.get("updated"),
        "created": p.get("created"),
        "aspect": p.get("aspect"),
        "duration_s": p.get("duration_s"),
        "approved": sb.get("status") == "approved" or p.get("approved", False),
        "storyboard_status": sb.get("status", "none"),
        "scene_count": len(sb.get("scenes", [])),
        "estimated_cost_usd": sb.get("estimated_cost_usd", 0),
        "actual_cost_usd": p.get("total_cost_usd", 0),
        "has_transcript": tpath.exists(),
        "has_voiceover": (C.project_path(name) / "assets" / "voice" / "voiceover_clean.wav").exists(),
        "has_composition": (C.project_path(name) / "composition" / "index.html").exists(),
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    # ------------------------------------------------------------- helpers
    def _send(self, code, obj, ctype="application/json"):
        body = (json.dumps(obj, ensure_ascii=False, indent=2) if not isinstance(obj, str) else obj)
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith("text/") or ctype == "application/json" else ""))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        if not n:
            return {}
        raw = self.rfile.read(n).decode("utf-8")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"_raw": raw}

    def _static(self, name, ctype):
        p = DASH / name
        if not p.exists():
            return self._send(404, {"error": "not found"})
        self._send(200, p.read_text(encoding="utf-8"), ctype)

    # ------------------------------------------------------------- GET
    def do_GET(self):
        url = urlparse(self.path)
        parts = [unquote(x) for x in url.path.strip("/").split("/") if x]
        try:
            if url.path in ("/", "/index.html"):
                return self._static("index.html", "text/html")
            if url.path == "/app.js":
                return self._static("app.js", "text/javascript")
            if url.path == "/style.css":
                return self._static("style.css", "text/css")
            if url.path == "/api/state":
                return self._send(200, {
                    "projects": [o for o in (project_overview(n) for n in C.list_projects()) if o],
                    "keys": C.key_status(),
                    "stages": C.STAGES,
                })
            if url.path == "/api/config":
                return self._send(200, C.load_config())
            if url.path == "/api/keys":
                return self._send(200, C.key_status())
            if len(parts) >= 3 and parts[0] == "api" and parts[1] == "project":
                name = parts[2]
                if not NAME_RE.match(name):
                    return self._send(400, {"error": "bad name"})
                pp = C.project_path(name)
                if not (pp / "project.json").exists():
                    return self._send(404, {"error": "no project"})
                detail = {"overview": project_overview(name)}
                for key, rel in [("storyboard", "storyboard.json"),
                                 ("transcript", "transcript/transcript.json"),
                                 ("captions", "transcript/captions.json"),
                                 ("voice_analysis", "assets/voice/voice_analysis.json"),
                                 ("ledger", "assets/ledger.json")]:
                    f = pp / rel
                    if f.exists():
                        try:
                            detail[key] = json.loads(f.read_text(encoding="utf-8"))
                        except Exception:
                            detail[key] = None
                q = parse_qs(url.query)
                lines = int(q.get("lines", ["250"])[0])
                detail["log"] = C.tail_log(name, lines)
                return self._send(200, detail)
            return self._send(404, {"error": "not found"})
        except Exception as e:
            return self._send(500, {"error": str(e)})

    # ------------------------------------------------------------- POST
    def do_POST(self):
        url = urlparse(self.path)
        parts = [unquote(x) for x in url.path.strip("/").split("/") if x]
        try:
            if url.path == "/api/config":
                body = self._body()
                cfg = C.load_config()

                def merge(dst, src):
                    for k, v in src.items():
                        if isinstance(v, dict) and isinstance(dst.get(k), dict):
                            merge(dst[k], v)
                        else:
                            dst[k] = v
                merge(cfg, body)
                C.save_config(cfg)
                return self._send(200, {"ok": True})
            if url.path == "/api/keys":
                body = self._body()
                name, value = str(body.get("name", "")), str(body.get("value", ""))
                if not re.match(r"^[A-Z0-9_]+$", name):
                    return self._send(400, {"error": "bad key name"})
                keys = {}
                if C.KEYS_PATH.exists():
                    try:
                        keys = json.loads(C.KEYS_PATH.read_text(encoding="utf-8"))
                    except Exception:
                        keys = {}
                keys[name] = value
                C.KEYS_PATH.write_text(json.dumps(keys, indent=2), encoding="utf-8")
                return self._send(200, {"ok": True, "status": C.key_status()})
            if len(parts) == 4 and parts[0] == "api" and parts[1] == "project":
                name, action = parts[2], parts[3]
                if not NAME_RE.match(name):
                    return self._send(400, {"error": "bad name"})
                pp = C.project_path(name)
                if not (pp / "project.json").exists():
                    return self._send(404, {"error": "no project"})
                if action == "storyboard":
                    body = self._body()
                    sb = body.get("storyboard")
                    if not isinstance(sb, dict) or not sb.get("scenes"):
                        return self._send(400, {"error": "storyboard.scenes missing"})
                    sb["status"] = "edited"
                    (pp / "storyboard.json").write_text(
                        json.dumps(sb, indent=2, ensure_ascii=False), encoding="utf-8")
                    C.log(name, "storyboard edited via dashboard")
                    return self._send(200, {"ok": True, "status": "edited"})
                if action == "approve":
                    sb_path = pp / "storyboard.json"
                    if not sb_path.exists():
                        return self._send(400, {"error": "no storyboard to approve"})
                    sb = json.loads(sb_path.read_text(encoding="utf-8"))
                    sb["status"] = "approved"
                    sb_path.write_text(json.dumps(sb, indent=2, ensure_ascii=False), encoding="utf-8")
                    proj = C.load_project(name)
                    proj["approved"] = True
                    C.save_project(name, proj)
                    C.update_stage(name, "approval", "storyboard approved via dashboard")
                    C.log(name, f"STORYBOARD APPROVED — {len(sb.get('scenes', []))} scenes, "
                                f"est ${sb.get('estimated_cost_usd', 0)}")
                    return self._send(200, {"ok": True})
                if action == "reject":
                    sb_path = pp / "storyboard.json"
                    if sb_path.exists():
                        sb = json.loads(sb_path.read_text(encoding="utf-8"))
                        sb["status"] = "draft"
                        sb_path.write_text(json.dumps(sb, indent=2, ensure_ascii=False), encoding="utf-8")
                    proj = C.load_project(name)
                    proj["approved"] = False
                    C.save_project(name, proj)
                    C.log(name, "storyboard rejected — back to draft")
                    return self._send(200, {"ok": True})
                return self._send(404, {"error": "unknown action"})
            return self._send(404, {"error": "not found"})
        except Exception as e:
            return self._send(500, {"error": str(e)})


def main():
    cfg = C.load_config()
    dcfg = cfg.get("dashboard", {})
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=dcfg.get("port", 8788))
    ap.add_argument("--host", default=dcfg.get("host", "127.0.0.1"))
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Hossam Video Factory dashboard -> http://{args.host}:{args.port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
