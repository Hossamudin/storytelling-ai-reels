# Brand profile — colors, fonts, logo, voice, avoids

`<studio>/brand/brand.json` is the single source of truth. `setup_studio.py brand` turns it into
`brand/brand.css` (CSS variables the motion kit reads) and copies the essentials into `config/config.json`.
Every new composition gets the brand automatically (`new_motion_video.py` copies `brand.css` + `brand/fonts/*`).

## Fields

| Field | Meaning | Kit token it drives |
|---|---|---|
| `name`, `tag` | brand / channel name; `tag` = the short caps label in the editorial chrome | chrome top-left |
| `language` | SPOKEN language of the videos (ISO code: `ar`, `en`, `fr`…) | transcription |
| `text_language` | ON-SCREEN text language when different (e.g. Arabic voice, English labels); empty = same | RTL/LTR, `lang` |
| `colors.primary` | the brand's main color (surfaces, headlines) | `--teal` |
| `colors.secondary` | support color (steps, "done") | `--green` |
| `colors.accent` | active state, the color that moves | `--lime` |
| `colors.highlight` | numbers, emphasis flashes | `--yellow` |
| `colors.alert` | problems, beams, CTA shapes | `--orange` |
| `colors.subscribe` | subscribe button only | `--red` |
| `colors.background_light` / `background_dark` | paper / night surfaces | light/dark preset `--bg` |
| `fonts.main` / `fonts.latin` | main-script font + Latin font (`*_dark` variants optional) | `--font-ar` / `--font-en` |
| `logo` | folder with logo files (SVG best, PNG with transparency next) | used by scenes |
| `voice` | tone words ("warm, direct, funny") | scripts, captions, CTAs |
| `avoid` | hard no's (colors, imagery, words, faces, music…) | every prompt + review |

Empty fields keep the default theme (teal #136052 · green #437F3E · lime #B3CE65 · yellow #FFEC5C ·
orange #FF5A33 · Noto Kufi Arabic + Manrope on light · Cairo + Montserrat on dark).

## Getting a palette from a beginner

- **They have a logo** → open it, read its 2–3 dominant colors, propose roles (primary / accent / alert),
  show swatches as a tiny HTML or a snapshot, confirm.
- **They have nothing** → propose 3 palettes that fit their topic and audience (e.g. calm teal + lime;
  confident navy + gold; warm terracotta + cream). One sentence on the feeling of each. They pick.
- Check contrast before locking: body text ≥ 4.5:1 on its background, big headlines ≥ 3:1. Bright
  accents (orange, yellow) usually fail as small text on light paper — use them for shapes and bands,
  or as text only at ≥ 90 px. `npx hyperframes check` reports contrast problems.

## Fonts

- Compositions must never load fonts from the internet (a CDN hiccup blocks the render). Download the
  `.ttf` once (Google Fonts → "Download family") into `brand/fonts/`. File name stem = family name
  (`Inter.ttf` → "Inter", `IBM_Plex_Sans_Arabic.ttf` → "IBM Plex Sans Arabic").
- Pick fonts that cover the script: Arabic → Noto Kufi Arabic, Cairo, Tajawal, IBM Plex Sans Arabic,
  Almarai; Persian/Urdu → Vazirmatn, Noto Nastaliq Urdu; Latin → Inter, Manrope, Montserrat, Poppins.
- Variable fonts (one file, all weights) are ideal.

## Right-to-left languages (Arabic, Persian, Urdu, Hebrew)

- The kit sets `direction: rtl` on `#root` — **never** `dir="rtl"` on `<html>` (it renders a blank video).
- Sequences and progress flow right → left (step 01 on the right). Headline block on the right, visual on the left.
- Latin words inside RTL text go in ONE `<span class="lat">` per run of Latin words (one span per word
  reverses their order). A lone Arabic letter glued to a Latin span (و + "AI") renders wrong — use a full word.
- "الـAI": use a long tatweel `الـــ` + `<span class="lat">AI</span>`.
- Prices/currency in RTL: wrap `$1.04` in `.lat`, or bidi prints "1.04$".
- Charts (SVG) inside RTL: `style="direction:ltr"` on the `<svg>`, or axis labels flip and clip.
- Arabic display fonts have tall glyph boxes: line-height 1.2–1.3; verify stacked lines in a snapshot.
- Arabic-Indic digits: the zero (٠) is a dot — hide counters until they start.

## Logo usage

SVG > transparent PNG > JPG (then `npx hyperframes remove-background logo.jpg -o logo.png`). Keep clear space
≈ the logo's height/4. Never recolor a logo the creator didn't approve. For a 3D or animated logo, see the
3D / 2D skills.

## Brand "avoid" list — apply it everywhere

Read `avoid` before writing any prompt, scene, or SFX plan. Typical: specific colors (e.g. "no blue/purple"),
realistic people or faces, robots/computers-as-props clichés, money imagery, music, glitch effects,
alcohol, immodest imagery. When a request conflicts with the avoid list, say so and offer an alternative.
