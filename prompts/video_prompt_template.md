# Video Prompt Template (AI video generation — Omni Flash / Veo class)

Every AI video prompt in the storyboard follows this contract.

## Structure
1. **Scene** — what we see (subject, environment, palette hexes pinned).
2. **Motion** — camera move + how each layer moves, pacing, and what happens at the END of the clip (clips ≤ 10s, one continuous shot).
3. **Voiceover context** — "This clip plays under an Arabic voiceover saying: '<narration snippet>'. Motion must match that meaning."
4. **Audio rule** — NO voiceover, NO speech, NO music. Ambient sound effects ONLY (whooshes, soft clicks, room tone, nature, mechanical), kept subtle — a human voiceover is layered on top later.
5. **Negative** — text overlays, watermark, logo, subtitles, music, distorted anatomy, morphing artifacts (plus per-scene negatives).

## Example
> Ultra-clean premium 3D render, 9:16 vertical, 720p. A warm off-white studio space with a soft receding grid floor in #136052. Center: a cluster of geometric nodes in #437F3E and #FF5A33 slowly rotates and pulses in sequence, connected by thin light lines with a #FFEC5C glow core; camera does a slow 15% push-in with gentle parallax; at second 7 the cluster collapses into a single bright point that flares softly and holds. Plays under an Arabic voiceover about how AI amplifies human work — the pulsing network must feel alive and cooperative, not menacing. No voice, no speech, no music — only a faint electrical hum and one soft whoosh at the flare. Avoid: text, watermark, faces, hands, robots, blue, purple, glitch.

## Cost discipline
- 720p by default (config `video.gemini_video.resolution`); 1080p only for hero shots the user flags.
- ≤10s per generation. A longer scene chains 2 clips or uses image + code motion instead.
- Never generate what code can render (typography, data, diagrams).

## First/last frame variant
Write the two image prompts separately (same style/palette!), then the video prompt describes ONLY the transition motion between them. Consistent lighting/composition between frames is critical — say so in both image prompts.
