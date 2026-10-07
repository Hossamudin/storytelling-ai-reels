---
workflow: motion-from-voice
storyboard: no
message: "AI predicts the next word; it doesn't *know*. Treat it as a smart assistant, not a final source."
destination: course handout (QR) + reels
aspect: "9:16"
language: ar (white dialect) + English keywords
preset: light
series: "AI FOR STUDENTS · 01"
voice: Higgsfield TTS (pending audition)
---

# AI for Students 01 — الـ AI بيفكر إزاي؟

Script: `input/script.md` (v2, white dialect). Timings are set after the voiceover exists.

## Step 1 — Understand
- **Remember:** AI predicts the next word; it doesn't *know*, so verify what it says.
- **Arc:** curiosity → "aha" → healthy caution.
- **Hook:** "هل هو فعلاً يعرف الإجابة؟" · **Payoff:** "مساعد شاطر، وليس مرجع نهائي".
- **Concrete things to show:** phone keyboard suggestions · Large Language Model · huge text corpus · "not a book lookup" · predict, word by word · strengths (write / explain / summarize) · weakness (convincing but wrong) · next episode: prompt.
- **Avoid the generic AI explainer:** no glowing brains, robots, neural-net spaghetti or blue sci-fi screens. Use the phone keyboard the students already know.

## Step 2 — Concepts

### A. "The Autocomplete Machine" ★ recommended
- **Spine:** a phone's keyboard suggestion bar (3 chips above the keys). The whole video lives in this one object.
- **Motif:** three suggestion chips. The winning chip turns lime and flies up into the sentence.
- **Signature move:** "word-by-word build". The answer to the hook question is written live, one word per beat. Each word appears as 3 candidate chips with relative bars (illustrative only, no percentages), and the winner drops into place.
- **Hook (0–3 s):** a chat bubble with "هل يعرف الإجابة؟" and a blinking caret; the question mark wobbles.
- **Middle:** zoom out from one phone to a wall of text pages streaming into a single model block labelled **LARGE LANGUAGE MODEL**. Then a book icon with "NOT A LOOKUP", struck through in orange.
- **Turn:** three green chips pop in for the strengths (**WRITE · EXPLAIN · SUMMARIZE**). Then the machine confidently builds a wrong sentence; a stamp slams **CONVINCING ≠ CORRECT** in orange.
- **Payoff:** the sentence settles into a card "مساعد شاطر ✓ / مرجع نهائي ✗", then a teaser chip "NEXT: PROMPT →" plus the QR/handout reminder.
- **Risk:** the word-by-word beats need careful timing so captions and chips don't collide. Keep captions minimal (keywords only).

### B. "The Library That Isn't"
- **Spine:** the student expects the AI to walk to a shelf and pull out the right book. Instead, the shelf dissolves into a river of words that re-forms into an answer.
- **Signature move:** books flipping into flowing text.
- **Risk:** books/library is a common cliché, and it explains what AI *isn't* better than what it *is*.

### C. "The Forecast"
- **Spine:** a weather-forecast board predicting the next word ("70 % chance of 'الكلمة'"), with a forecaster's pointer.
- **Signature move:** forecast cards flipping per word.
- **Risk:** it needs real-looking percentages (we'd be inventing numbers) and an extra layer of explanation, which is hard in 70 s.

**Recommendation: A.** Students recognise the keyboard instantly, so the idea lands without explanation, and the same chip motif can return in video 2 (prompt pieces) to tie the series together.

## Rhythm (A)
`hook wobble · zoom-out · text stream · STRIKE · word-by-word build (hero) · green pops · STAMP · warm close`

## Section labels (light chrome)
THE QUESTION · THE TRICK · HOW IT LEARNS · PREDICT · STRENGTH · WEAKNESS · TAKEAWAY

## Sound
Library only: key-press/typing for the keyboard, pop for chips, whoosh for the zoom-out, sparkle for "predict", error + impact-bass for the stamp, chime for the payoff. No generated SFX needed.

## Generation plan (paid → needs your approval)
| # | What | Model | Why |
|---|---|---|---|
| 1 | Voice audition: the line "تخيّل لوحة المفاتيح في جوالك…" in 2–3 voices | Higgsfield TTS (`inworld_text_to_speech` / `seed_audio` / `text2speech_v2`) | you pick the series voice by ear |
| 2 | Full voiceover (~70 s) in the chosen voice | same | the video is timed to it |
| — | Images / clips / bespoke SFX | none | all visuals are code; library SFX cover it |

## Invented / placeholder strings to flag at handoff
- The candidate words and bars in the word-by-word build are illustrative, not real model probabilities (an on-screen tag will say "ILLUSTRATIVE").
- Handout page number for the closing reminder: **needs your input**.
