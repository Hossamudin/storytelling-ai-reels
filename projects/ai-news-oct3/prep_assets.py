# Prepare the reel's real-source assets (crops of captures, clips from the X recordings, library items).
# Run from repo root:  python projects/ai-news-oct3/prep_assets.py
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

P = Path(__file__).resolve().parent
CAP = P / "assets" / "images" / "cap"
OUT = P / "reel" / "assets" / "images"
VID = P / "reel" / "assets" / "videos"
RAW = P / "assets" / "videos" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
VID.mkdir(parents=True, exist_ok=True)


def crop(src, box, dst, width=None):
    im = Image.open(src).convert("RGB").crop(box)
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(OUT / dst)
    print(dst, im.size)


crop(CAP / "dots" / "img0.png", (0, 0, 1146, 648), "dots_avatars.png")
crop(CAP / "dots" / "img3.png", (0, 0, 1146, 648), "dots_ui.png")
crop(CAP / "dots" / "img1.png", (0, 0, 1146, 648), "dots_computer.png")
crop(CAP / "sol" / "img0.png", (0, 1075, 1146, 2100), "sol_card.png")
crop(CAP / "sol" / "img0.png", (0, 560, 1146, 1050), "astra_price.png")
crop(CAP / "argon" / "img0.png", (0, 0, 1218, 687), "argon_key.png")
crop(CAP / "devday" / "img15.png", (0, 0, 1140, 642), "devday_grid.png")

# full-page captures: headline regions (mobile 430 px x3)
for name, d in (("verge", "verge"), ("mods", "mods")):
    im = Image.open(CAP / d / "full.png")
    print(name, "full", im.size)

subprocess.run([sys.executable, "-c", "pass"])

def ff(args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)

X = str(RAW / "Gemini 4 (X)  seeing what people built.mp4")
ff(["-ss", "11.2", "-i", X, "-frames:v", "1", "-vf", "crop=560:562:72:270", str(OUT / "argon_bench.png")])
ff(["-ss", "35.4", "-t", "4.4", "-i", X, "-an", "-vf", "crop=460:600:66:300,scale=920:-2", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(VID / "argon_jeep.mp4")])
ff(["-ss", "35.6", "-i", X, "-frames:v", "1", "-vf", "crop=460:600:66:300,scale=920:-2", str(OUT / "argon_jeep.png")])
ff(["-ss", "53.8", "-t", "11", "-i", X, "-an", "-vf", "crop=410:560:70:300,scale=820:-2", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(VID / "argon_ocean.mp4")])
ff(["-ss", "54.0", "-i", X, "-frames:v", "1", "-vf", "crop=410:560:70:300,scale=820:-2", str(OUT / "argon_ocean.png")])

LIB = P.parent.parent / "library"
for rel, dst in (("capture/capture_sonnet55-pricing_anthropic-pricing-table-sonnet-5-5-2_4x3_v1.png", OUT / "sonnet_pricing.png"),
                 ("capture/capture_sonnet55-hero_anthropic-claude-sonnet-5-5-launch-h_3x4_v1.png", OUT / "sonnet_hero.png"),
                 ("hossam-cutout/hossam_cutout_suit_hi-res-transparent-cutout-suit-waist_9x16_v1.png", OUT / "hossam_suit.png"),
                 ("episode/episode_opus55-tip1_opus-5-5-tips-reel-part-1-of-3-facel_9x16_89s_v1.mp4", None)):
    if dst:
        shutil.copy(LIB / rel, dst)
        print("lib ->", dst.name)
