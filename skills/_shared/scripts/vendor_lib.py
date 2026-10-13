"""Vendor a JS animation library into a HyperFrames part so renders never touch the internet.

Usage:
  python vendor_lib.py three  <part dir> [--version 0.181.2]   -> assets/js/three/three.module.min.js + a few addons (GLTFLoader, RoomEnvironment, ...)
  python vendor_lib.py lottie <part dir> [--version 5.12.2]    -> assets/js/lottie.min.js

Downloads the package once from the npm registry (`npm pack`) into a cache (~/.video-studio-cache) and copies
the needed files. Then reference them locally, e.g.

  <script type="importmap">{"imports": {"three": "./assets/js/three/three.module.min.js",
                                         "three/addons/": "./assets/js/three/addons/"}}</script>
  <script src="assets/js/lottie.min.js"></script>
"""
import argparse
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

CACHE = Path.home() / ".video-studio-cache"
PKG = {"three": ("three", "0.181.2"), "lottie": ("lottie-web", "5.12.2")}
ADDONS = ["loaders/GLTFLoader.js", "utils/BufferGeometryUtils.js", "utils/SkeletonUtils.js", "environments/RoomEnvironment.js",
          "geometries/RoundedBoxGeometry.js", "geometries/TextGeometry.js", "loaders/FontLoader.js", "loaders/SVGLoader.js",
          "math/SimplexNoise.js", "lines/Line2.js", "lines/LineMaterial.js", "lines/LineSegments2.js", "lines/LineSegmentsGeometry.js",
          "lines/LineGeometry.js"]


def fetch(pkg, version):
    dest = CACHE / f"{pkg}-{version}"
    if (dest / "package").exists():
        return dest / "package"
    dest.mkdir(parents=True, exist_ok=True)
    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        sys.exit("npm not found — install Node.js first (env_check.py shows the command).")
    r = subprocess.run([npm, "pack", f"{pkg}@{version}", "--pack-destination", str(dest)], capture_output=True, text=True)
    tgz = next(dest.glob("*.tgz"), None)
    if r.returncode or not tgz:
        sys.exit(f"npm pack failed: {r.stderr[-800:]}")
    with tarfile.open(tgz) as t:
        try:
            t.extractall(dest, filter="data")
        except TypeError:  # Python < 3.12
            t.extractall(dest)
    tgz.unlink()
    return dest / "package"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lib", choices=list(PKG))
    ap.add_argument("part")
    ap.add_argument("--version")
    ap.add_argument("--addon", action="append", default=[], help="extra three addon path under examples/jsm/")
    a = ap.parse_args()
    name, ver = PKG[a.lib]
    src = fetch(name, a.version or ver)
    js = Path(a.part) / "assets/js"
    js.mkdir(parents=True, exist_ok=True)
    if a.lib == "three":
        out = js / "three"
        out.mkdir(exist_ok=True)
        for f in ("three.module.min.js", "three.core.min.js"):
            if (src / "build" / f).exists():
                shutil.copy2(src / "build" / f, out / f)
        # the addons videos actually use (small); add more with --addon examples/jsm/<path>
        jsm = src / "examples/jsm"
        for rel in ADDONS + a.addon:
            rel = rel.replace("examples/jsm/", "")
            if (jsm / rel).exists():
                (out / "addons" / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(jsm / rel, out / "addons" / rel)
            else:
                print(f"  ! addon not found: {rel}")
        idx = Path(a.part) / "index.html"
        if idx.exists():  # the importmap must sit in the ROOT document, before any module script
            html = idx.read_text(encoding="utf-8")
            if "importmap" not in html:
                imap = ('    <script type="importmap">{"imports": {"three": "./assets/js/three/three.module.min.js", '
                        '"three/addons/": "./assets/js/three/addons/"}}</script>\n')
                html = html.replace('    <script src="assets/js/gsap.min.js"></script>', imap + '    <script src="assets/js/gsap.min.js"></script>', 1)
                idx.write_text(html, encoding="utf-8")
                print(f"  importmap added to {idx}")
        print(f"OK: three {a.version or ver} -> {out}")
        print('  importmap: {"imports": {"three": "./assets/js/three/three.module.min.js", "three/addons/": "./assets/js/three/addons/"}}')
    else:
        shutil.copy2(src / "build/player/lottie.min.js", js / "lottie.min.js")
        print(f"OK: lottie-web {a.version or ver} -> {js / 'lottie.min.js'}")


if __name__ == "__main__":
    main()
