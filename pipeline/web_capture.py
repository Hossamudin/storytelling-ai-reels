"""Capture real-source visuals (benchmark pages, articles, charts) as crisp PNGs for a video.

Usage:
  python pipeline/web_capture.py <url> --out projects/<name>/assets/images/<slug> [--full] [--iframes] [--imgs]
         [--selector "css"]... [--scale 2] [--width 1280] [--dark]

  --full       full-page screenshot  (full.png; scroll-loads lazy charts first)
  --iframes    screenshot every iframe taller than 300 px (interactive charts often live in iframes: chartN.png)
  --imgs       screenshot every <img> wider than 400 px (hero / figure images: imgN.png)
  --selector   screenshot the first element matching each CSS selector (sel1.png, sel2.png …)
Also writes page.txt (visible text) so numbers on screen can be quoted exactly, and capture.json (url, date, files).
Crop a region of full.png with PIL when a chart has no own element. Log each capture in assets/ledger.json
as {"provider": "web-capture", "source": url, "captured": date}, and label real data on screen ("REAL DATA · <source>").
Charts render blank in headless mode until scrolled into view: this tool scrolls and waits before each shot.
"""
import argparse
import asyncio
import datetime
import json
from pathlib import Path


async def run(a):
    from playwright.async_api import async_playwright
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    files = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": a.width, "height": 1500}, device_scale_factor=a.scale,
                              color_scheme="dark" if a.dark else "light")
        try:
            await pg.goto(a.url, wait_until="networkidle", timeout=45000)
        except Exception:  # sites with live sockets / polling never go idle (whacka.app): settle for load + a pause
            print("  networkidle timed out -> using load + 4 s settle")
            await pg.goto(a.url, wait_until="load", timeout=90000)
            await pg.wait_for_timeout(4000)
        for _ in range(30):
            await pg.mouse.wheel(0, 1200)
            await pg.wait_for_timeout(200)
        await pg.evaluate("window.scrollTo(0, 0)")
        await pg.wait_for_timeout(2000)
        if a.full:
            await pg.screenshot(path=str(out / "full.png"), full_page=True)
            files.append("full.png")
        if a.iframes:
            fr = pg.locator("iframe")
            for i in range(await fr.count()):
                f = fr.nth(i)
                await f.scroll_into_view_if_needed()
                await pg.wait_for_timeout(4000)
                bb = await f.bounding_box()
                if bb and bb["height"] > 300:
                    await f.screenshot(path=str(out / f"chart{i}.png"))
                    files.append(f"chart{i}.png")
        if a.imgs:
            im = pg.locator("img")
            k = 0
            for i in range(await im.count()):
                e = im.nth(i)
                bb = await e.bounding_box()
                if bb and bb["width"] > 400:
                    await e.scroll_into_view_if_needed()
                    await pg.wait_for_timeout(500)
                    await e.screenshot(path=str(out / f"img{k}.png"))
                    files.append(f"img{k}.png")
                    k += 1
        for i, sel in enumerate(a.selector or [], 1):
            e = pg.locator(sel).first
            await e.scroll_into_view_if_needed()
            await pg.wait_for_timeout(2500)
            await e.screenshot(path=str(out / f"sel{i}.png"))
            files.append(f"sel{i}.png")
        (out / "page.txt").write_text(await pg.inner_text("body"), encoding="utf-8")
        await b.close()
    meta = {"url": a.url, "captured": datetime.date.today().isoformat(), "files": files}
    (out / "capture.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"OK: {len(files)} file(s) -> {out}  (+ page.txt, capture.json)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", required=True)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--iframes", action="store_true")
    ap.add_argument("--imgs", action="store_true")
    ap.add_argument("--selector", action="append")
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--dark", action="store_true")
    asyncio.run(run(ap.parse_args()))


if __name__ == "__main__":
    main()
