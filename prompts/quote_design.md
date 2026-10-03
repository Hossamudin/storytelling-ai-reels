# Quote Card Design (house style)

For belief statements, mottos, and closing lines. Rendered in CODE (HyperFrames) — never via image model.

## Anatomy
- Background: warm off-white (#FAF7F0) or deep punch1 (#136052) — alternate by context.
- Giant Arabic quotation glyph "❝" in punch3 (#B3CE65), top-right, oversized (bleeds off-frame allowed).
- Quote text: Noto Kufi Arabic, punch1 on light / white on dark, 3–6 words per line, RTL, center-left aligned, staged line-by-line reveal (fade + slide up, 0.25s stagger).
- One keyword (English or Arabic) colored punch5 (#FF5A33) with a scale-punch entrance.
- Attribution: "— حسام الدين حسن" in punch2 (#437F3E), smaller, Manrope-latin "AI Storyteller" beneath in punch3.
- Accent: thin punch5 underline that draws in (scaleX 0→1) under the keyword, 0.4s, power3.out.
- Motion: card breathes (scale 1.00→1.02), quote glyph rotates in −8°→0°, attribution fades last. Exit: whole card pushes up +4% and fades if followed by another scene.

## Example quote (EN source, rendered AR)
"You're in a great time! AI allows you to explore and learn further beyond your age"
→ Arabic card: «إنت في أحسن وقت… الـ AI يخليك تستكشف وتتعلم أكتر من عمرك» — حسام الدين حسن
English keyword "AI" styled punch5 with underline draw.

## Rules
- Max ~14 words on screen. One keyword highlighted. One accent animation. Nothing else.
- 3–5s duration, matches narration of the quote.
