# Vibe Automation — storyboard (dispatch record, storyboard: no)

Concept: **one production pipeline is the spine of the intro.** We watch a podcast die on the shelf,
see why (effort), lay out its six stages, watch human teams pile up under them, then flip every team
into a glowing AI node and fire a speed beam through the line — and only then reveal the name:
**Vibe Automation · 6 خطوات**. Light premium-editorial paper for the "real world", deep-teal for the
"idea" beats (question, AI team, title reveal, end screen) so bloom has somewhere to glow.

Rhythm (intro): hook-punch · strike-strike-SLAM · DARK question · DARK multiply · long continuous
pipeline camera move (build → teams → FLIP → speed beam) · FLASH reveal · channel card + subscribe · zoom-through out.

Design: paper `#F6F4EA`, ink `#0D0D0D`, teal `#136052`, green `#437F3E`, lime `#B3CE65`,
yellow `#FFEC5C`, orange `#FF5A33` (shapes/beams/highlighter only — fails AA as text on paper),
red `#D93A2B` (subscribe only). Noto Kufi Arabic 400–900, Manrope 800 for Latin keywords.
Effects vocabulary: camera zoom/punch (`multi-phase-camera`, `viewport-change`), parallax depth
layers on every scene, bloom (`ambient-glow-bloom`), shutter motion blur on 1–3 snap beats
(`motion-blur` registry component), `svg-path-draw` strikes/tracks, `asr-keyword-glow`-style
word-synced emphasis. SFX from the bundled library; no music.

## INTRO (`index.html`, 67.2s) — times are edited-voice seconds

## Frame 1 — Hook: the shelved podcast
status: built · src: index.html#s1 · 0.00–5.25
rules: multi-phase-camera, ambient-glow-bloom, center-outward-expansion
Mic glyph blooms on; "قررت أبدأ بودكاست" words land on 0.41/0.87/1.27; two episode cards
(الحلقة ١/٢ ✓) snap in on "حلقتين" 3.63 with three ghost cards; on "وركنت" 4.23 everything drops onto
a shelf, desaturates, mic tips over. SFX: pop ×2, impact thud.

## Frame 2 — Not motivation, not usefulness: effort
status: built · src: index.html#s2 · 5.25–11.70
rules: svg-path-draw, kinetic-beat-slam, stat-bars-and-fills
Two doubt pills struck through in orange (مش متحمس / مش مفيد); "ولكن" whips them out (motion blur);
"مجهود" SLAMS 10.39, "كبير جداً" + effort meter overfills past the frame edge with shake.

## Frame 3 — The question (teal)
status: built · src: index.html#s3 · 11.70–15.95
rules: viewport-change, asr-keyword-glow, ambient-glow-bloom
Circle iris into teal. "سألت نفسي" kicker; the question builds; "الذكاء الاصطناعي" glows yellow on 13.97;
giant ghost "؟" parallax behind; slow push-in.

## Frame 4 — A team made of AI (teal)
status: built · src: index.html#s4 · 15.95–20.55
rules: orbit-3d-entry, avatar-cloud-network, ambient-glow-bloom
One AI node blooms on "الـAI" 17.04; splits into six nodes on a ring on "أبني فريق" 17.92–18.28,
links draw, ring turns. Title "فريق من الـAI".

## Frame 5 — The pipeline world (one continuous camera move)
status: built · src: index.html#s5 · 20.55–44.65
rules: viewport-change, svg-path-draw, center-outward-expansion, depth-of-field-blur
5a "الفكرة ببساطة" card → six stage slots draw on the track (22.28–25.31), episode card at the destination.
5b stages fill word-synced: اختيار الضيف 27.81 · البحث عنه 28.61 · التواصل معاه 29.51 · تحديد موعد 30.49 ·
التصوير 32.34 · إنتاج المحتوى 32.88; camera tracks RTL, then pulls back.
5c human-team glyphs stack under each stage (35.08–36.9), "فِرق كاملة من البشر", episode progress crawls.
5d THE FLIP 40.64: teams morph into glowing AI nodes right→left; mesh links on "كفريق متكامل" 42.14;
speed beam with motion blur on "ويسرعها" 44.28; progress snaps to 100%.

## Frame 6 — Title reveal: Vibe Automation (teal)
status: built · src: index.html#s6 · 44.65–54.90
rules: kinetic-beat-slam, ambient-glow-bloom, center-outward-expansion
Flash + zoom-through. "Vibe Automation" assembles with bloom on 46.74; six step chips count in on
"6 خطوات" 48.50; idea spark (فكرة 50.81) explodes into a system network (نظام متكامل 51.94) whose nodes
ignite on "فريق من الذكاء الاصطناعي" 52.73.

## Frame 7 — Channel card + subscribe
status: built · src: index.html#s7 · 54.90–67.20
rules: center-outward-expansion, svg-icon-enrichment, kinetic-beat-slam
"أول مرة ليك هنا؟" kicker; avatar + "حسام الدين حسن" lockup 56.29; topic line with "المجنون" wobble;
cursor clicks subscribe 61.51 → "مشترك", bell rings 61.89; country bubbles on "من أي بلد" 64.19;
"يلا بينا" zoom-through to white at 66.4.

## OUTRO (`outro.html`, 22.0s)

## Frame O1 — Thanks + like/share
status: built · src: outro.html#o1 · 0.00–5.90
Like button fills on "لايك" 4.06; share arrow flies on "وشاركوا" 4.30.

## Frame O2 — Comments, see you, salam
status: built · src: outro.html#o2 · 5.90–11.00
Comment box types, question bubbles stack; next-episode cards slide; "سلام عليكم" 10.22.

## Frame O3 — End screen (teal) — holds ≥10s for YouTube end-screen elements
status: built · src: outro.html#o3 · 11.00–22.00
Two 16:9 video slots + subscribe circle slot; arrows point on "للفيديوهين دول" 13.38.
