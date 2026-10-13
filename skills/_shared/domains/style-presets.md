# Style presets — one brand, two looks

Both presets use the creator's brand roles (brand.json → brand.css; default theme: teal, green, lime, yellow,
orange; red only for subscribe). A preset changes **surface, type and chrome**, never the brand.
Set per project: `python engine/pipeline/new_motion_video.py <name> --preset light|dark`.
In code, the preset lives on `<div id="root" data-preset="…">`. Every token is a CSS variable in
`assets/css/base.css`, overridden by `assets/css/brand.css`. Hex values below are the default theme.

| | **Editorial Light** (`light`) | **Editorial Dark** (`dark`) |
|---|---|---|
| Proven on | an approved YouTube intro + outro | tool demos, reels, news recaps (control-room look) |
| Background | warm paper `#F6F4EA`, teal dot grid (48 px), grain 0.07 | dark teal gradient `#07221E → #041614`, lime dot grid (48 px), drifting glow blobs, vignette, grain 0.09 |
| "Idea" scenes | switch to a deep-teal radial for questions, reveals, end screens | the whole video is dark; lime marks active states |
| Text | ink `#0D0D0D`, headings teal | off-white `#F6F8F0`, muted `#8CB2A6` |
| Arabic font | Noto Kufi Arabic 700–900 | Cairo 700–900 |
| English font | Manrope 800 | Montserrat 800–900 (tracked caps for labels) |
| Numbers | teal / yellow on teal | yellow `#FFEC5C` |
| Editorial chrome | off by default | on: brand tag + series (top-left), section label + `03 / 10` (top-right), crop marks, lime progress line + timecode |
| Feels like | Apple keynote / premium SaaS explainer | Bloomberg / Netflix-doc motion graphics, "mission control" |
| Best for | story intros, warm channel moments, broad audiences | tool demos, agents and workflows, tech deep dives, series episodes |

**Rules for both:**
- RTL languages: `direction: rtl` on `#root` (the kit does it), **never** `dir="rtl"` on `<html>` (blank video).
  Sequences flow **right → left** (step 01 on the right). LTR languages: the kit sets `data-dir="ltr"`; flow left → right.
- Headline block on the reading-start side; the visual metaphor on the other side or center.
- Pair main-language headlines with small **English tracked-caps labels** ("THE PROBLEM", "RESEARCH AGENT") for the editorial feel.
- Orange is for problems, alerts, beams and CTA shapes. It fails AA as small text on paper, so
  use it at ≥ 90 px or as a band behind white/ink text.
- Safe area: 64 px margins, and nothing important within 110 px of the chrome.
- 9:16 and 1:1 automatically drop the chrome's series name (`@media (max-aspect-ratio: 1/1)`).

**Mixing:** a light video may contain dark "idea" scenes (a proven pattern). A dark video
may flash to paper for one contrast beat, e.g. "the old manual way". Choose it deliberately and
note it in the Creative Treatment.
