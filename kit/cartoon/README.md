# kit/cartoon — 2D character rig + props (story / explainer animation)

Code-drawn SVG characters and props animated with GSAP. Free, deterministic, brand palette, crisp Arabic text.
First used on `projects/vibe-coder-hacked/` (`build_demo.py` is the reference: 7 story scenes + subtitles).

## Use it
```
python pipeline/new_motion_video.py <name> --part <part> --aspect 9:16 --preset dark --no-chrome --kit cartoon
```
`--kit cartoon` copies `js/cartoon.js` into the part's `assets/js/` and loads it after `fx.js`.

```js
const fx = window.HF_SCENE(4.2);                               // scene start (global seconds)
const k = HF_CHAR(fx, "#s2-k", { id: "s2k", look: "karim", pose: "idle", face: "smile", cape: true });
k.pose(5.0, "point").face(5.0, "happy").talk(5.0, 7.2);        // chainable, CHRONOLOGICAL order
k.blinks(4.2, 16).hop(14, 40).cape(14, 16);
Q("#s2-house").innerHTML = HF_PROP.house("s2h");               // props are SVG strings with prefixed ids
tl.fromTo("#s2h-roof", { y: -300 }, { y: 0, duration: 0.5 }, 11.8);
```
Mount = an absolutely positioned div; the character's feet sit on its bottom edge (`viewBox -150 -320 300 330`,
so width = height × 300/330). `build_demo.py:ch_mount(x, feet_y, h)` computes the box.

## Character API (`HF_CHAR`)
| Method | What |
|---|---|
| `pose(t, name \| {aL:[upper,fore], aR, lL, lR, hd, tr, by}, d, ease)` | joint angles in degrees; `by` drops the body (sitting) |
| `face(t, "neutral\|happy\|grin\|smile\|shock\|sad\|worried\|smirk\|angry")` | mouth + eyes + brows |
| `talk(t0, t1, rate)` | mouth flaps (use the voice word timings when a voice exists) |
| `blink(t)` / `blinks(t0, t1, every)` | lids |
| `hop(t, h)` · `squash(t)` · `breathe(t0, t1)` · `walk(t0, t1, step)` · `clap(t0, t1)` | body motion (move the mount with GSAP for travel) |
| `cape(t, until)` | needs `{ cape: true }` |

Looks: `karim` (hoodie), `doctor` (coat, glasses), `hossam` (beard, teal; placeholder until the real avatar is made).
Skins: `flat` (default) · `line` (ink outlines, light preset) · `noir` (silhouette + orange rim, dark preset).
Poses: idle, type, shock, point, pointUp, think, shrug, hero, fly, clapA/B, selfie, phone, hold, wave, sad, sitFloor, cheer.

## Props (`HF_PROP`)
`laptop` · `house` (12 blocks `-b0..b11`, `-roof`, `-door`, `-win`, `-bwin`/`-sash`; `{open, lit}`) · `key` · `clock`
(`-hh`, `-mh`) · `phone` · `shield` (`-ck` check) · `bot` (`{variant: "scanner"|"guard"}`, `-arm`, `-eye`) · `safe`
(`-door`, `-dial`) · `cctv` (`-led`) · `paper` (`{badge, accent}`) · `moon` · `crack` (`-c1`, `-c2`, draw them).

## Rules
- Every move tweens from the previous state on proxy objects (`immediateRender: false`), so seeking is exact.
  Call a character's methods in time order.
- Use `svgOrigin` for GSAP rotations of prop parts (clock hands, arms) — values are prop viewBox units.
- Emoji don't render reliably in headless Chrome: draw icons as SVG.
- Keep text out of the subtitle zone (bottom ~320 px in 9:16) when captions are on.
- Brand avoids (robots, computers, money) are lifted for story videos only when the script needs them;
  keep them in brand colours and say so in the treatment.

## Next (see docs/ROADMAP.md §C)
Hossam flat avatar (from real photos), more looks (hacker/viewer/team), side/3-4 view heads, `visemes.py` (mouth
shapes from the voice), Lottie loader for marketplace props, scene templates in `motion_sync.py`.
