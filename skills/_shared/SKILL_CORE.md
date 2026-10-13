## Every session starts here (30 seconds)

1. **Language** — reply in the language and dialect the creator writes in. Keep tool names in Latin script.
2. **Studio check** — `python <skill-dir>/scripts/setup_studio.py status`
   (`<skill-dir>` = the folder containing this SKILL.md; all later commands run from the studio folder it prints).
   - "NO STUDIO YET" → run onboarding: read `references/onboarding.md` and follow it (machine check → studio →
     brand & preferences → library → tools → a 5-minute first win). Don't skip it — it's what makes every later video
     fast and on-brand. A creator in a hurry can do the 2-minute version (language, format, colors) and finish later.
   - Studio exists → read `<studio>/profile.md` (language, level, preferences, **Feedback log**) and
     `<studio>/lessons.md`. If the engine is older than this skill's, `setup_studio.py init` upgrades it (projects untouched).
3. **Level** — beginner: plain words, one topic per message (≤ 3 short questions, each with a default), a recommended default for every choice.
   Pro: brief, scene tables, paths and commands. Long jobs: one-line status at each phase.

## Ground rules (they protect the creator)

- **Approval gates:** paid generation (images, clips, SFX, voices) only after a "yes" on a list of what/why/cost ·
  concepts before building (unless the profile says "build to preview") · preview before the final render ·
  anything that posts or sends is always asked.
- **Never invent facts.** Numbers, prices, quotes and names on screen come from the creator's material or a captured
  official source (labelled). Placeholders are allowed only when flagged at handoff. Blur private data.
- **Library first:** `python engine/pipeline/lib.py find "<words>"` before generating anything; harvest after delivery.
- **No internet at render time:** fonts, scripts (GSAP, Three.js, Lottie) and media are local. `preflight.py` enforces it.
- **Final renders only via** `python engine/pipeline/render_final.py <name> --part <part>` (preflight → render →
  verify → master −14 LUFS → chapters → `deliverables/`). Never from the Studio render button.
- **Snapshots beat checks:** `npx hyperframes check` clean AND `npx hyperframes snapshot --at t1,t2,…` reviewed at each
  scene's busiest moment.
- Keys stay secret (presence only, never echo values). Don't commit or publish unless asked.

## Every delivery ends the same way

Explain what the AI did → flag anything invented or uncertain → offer 3 suggestions (reels cut / article pack /
next-video idea or recording tip) → ask one specific feedback question → write the answer to `profile.md`
(Feedback log) and new problems to `<studio>/lessons.md`. Template: `references/working-with-the-creator.md` §4.

## Shared references (read when the task touches them)

| File | Read when |
|---|---|
| `references/onboarding.md` | first session, or profile gaps |
| `references/working-with-the-creator.md` | approvals, explaining, handoff template, feedback memory |
| `references/brand-profile.md` | brand colors/fonts/logo, RTL typography |
| `references/tools-connection.md` | keys, AI-generation MCPs (models, prompts, budgets), free alternatives, API errors |
| `references/library.md` | finding / adding / reusing assets |
| `references/voice-and-cuts.md` | any narrated video: clean, transcribe, retakes, edit.json |
| `references/composition-craft.md` | building scenes: kit API, contract, gotchas, timing |
| `references/render-and-deliver.md` | final render, long renders, delivery package, follow-up offers |
| `references/lessons-learned.md` | before building — every past problem and its fix, by topic |
| `references/engine-commands.md` | command lookup |
