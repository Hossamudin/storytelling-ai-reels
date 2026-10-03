# OPUS 5.5 TIPS — 3-part faceless reel series (9:16, dark preset)

Source: videos/Claude opus 5.5/ (3 voice notes + 2 screen recordings). One project, three parts: tip1 / tip2 / tip3.
Shared code: build_lib.py (Claude spark symbol, mock Claude composer, cards, Hossam CTA). Each part: <part>/build_scenes.py.

## Edit (input/edit.json → voice_edit.py --verify, re-transcribed clean)
- tip1 109.4 → 87.7 s: cut retake "ولكن قلتله انا عايزك تفيل فري…", filler "اه", retake "الفيديو الجاي بقى هقولك…".
- tip2 104.5 → 95.2 s: pauses only; restored a line Whisper skipped ("وقول له أنا عايزك تطلعلي skill أو prompt").
- tip3 106.4 → 95.8 s: cut retake "بدل ما تبدأ في الصفر"; restored "وتحاول تتعلم من الـprompt بتاعه… for free".
- All pauses > 0.38 s tightened to 0.24 s, 12 ms seam fades.

## Series system
- Hero: the Claude spark (drawn in code, terracotta #D97757 used only for Claude marks). Deck of 3 tip cards; each part flips its card and teases the next.
- Part 1 signature: a box squeezes the spark and bursts on "وما تحدّهوش".
- Part 2 signature: learnings / mistakes / fixes fly into the clay package → lime tape seals it → SKILL.md; token bar 100% → 25–30%.
- Part 3 signature: clay road — winding path from zero vs. lime shortcut; marker jumps to 95% on "٩٥٪ من المشوار".

## Real material used
- Claude app screen recording (model picker → Opus 5.5) with a baked privacy blur on the sidebar task list.
- HyperFrames Studio recording (the previous Agent Harness reel).
- anthropic.com/claude-opus-5-5 (captured 2026-10-02): benchmark table, "costs 40% less to run than Opus 5".
- remotion.dev + hyperframes.heygen.com mobile captures; install command `npx skills add heygen-com/hyperframes` (from the site).

## Invented / illustrative strings to flag
- Mock chat text: "عايز أعمل فيديو موشن جرافيكس احترافي", "عايزك تطلّعلي skill أو prompt", "حمّل HyperFrames واستخدمها", feedback bubbles (tip2 s14).
- "PLAN.md", "SKILL.md", "THEIR PROMPT", "V1" labels and the orange error rings on the v1 preview (tip2 s13) are illustrative.
- tip2 complexity chart is labelled ILLUSTRATION. 25–30% is Hossam's own approximate figure ("مثلا"), labelled APPROXIMATE.
- tip3 "someone who made videos" card is a generic avatar (no real creator).

## Higgsfield (logged in assets/ledger.json)
6 SFX (spark-ignite, box-burst, tape-seal, token-drain, shortcut-zoom, series-sting) + 3 GPT Image 2.5 medium images (open box, package, road).
