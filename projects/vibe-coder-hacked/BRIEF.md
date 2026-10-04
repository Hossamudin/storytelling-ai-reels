# قصة Vibe Coder اتخترق في ليلة — demos

- Format: reel 9:16, ~75 s, Story / 2D animation · CTA: comment SECURITY
- Links for the description: https://www.youtube.com/watch?v=LwZ8xyQI1h0 · Facebook video (see input/brief.json)
- Parts:
  - `demo_flat/`: full story, flat cartoon on the dark preset (night → morning → teal "fix" world). TEMP subtitles from the script.
  - `style_line/`: hook only (6 s), paper + ink outlines (light preset).
  - `style_noir/`: hook only (6 s), silhouettes with an orange rim, comic-noir.
- Timing follows the script blocks (0–4 / 4–16 / 16–30 / 30–42 / 42–52 / 52–67 / 67–75). After the voice is recorded:
  `find_retakes.py` → `voice_edit.py` → re-time `build_demo.py` from the words, swap the subtitle scene for captions.
- Rebuild: `python projects/vibe-coder-hacked/build_demo.py && python pipeline/motion_sync.py vibe-coder-hacked --part demo_flat`

## Invented / placeholder strings to flag at handoff
- Code card `const PAY_KEY = "sk_live_8f2…Q9x"`, repo name `KARIM / CLINIC-APP`, file names, URL `clinic-app.com/patient?id=41`: illustrative, not real.
- Invoice shows `$$$$` + "آلاف الدولارات" (the script gives no number).
- "صاحبي الدكتور" message sender label; the doctor character has no name.
- CTA uses a text wordmark `MAHARAAI.COM`: no Mahara logo file in the library yet. Hossam appears by name only (the avatar is not built yet).
- Robots, laptops and money appear because the story needs them (brand "avoids" lifted for story videos).
