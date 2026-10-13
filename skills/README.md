# Video Studio Skills · مهارات استوديو الفيديو

Five AI skills that turn voice notes, recordings and ideas into finished, branded videos — for **any creator, any
language** (Arabic RTL done right). They share one studio on your computer, so your brand, preferences, asset library
and lessons carry over from skill to skill and video to video.

خمس مهارات ذكاء اصطناعي بتحوّل الفويس نوت والتسجيلات والأفكار لفيديوهات كاملة بهوية براندك — لأي صانع محتوى
وبأي لغة (والعربي من اليمين للشمال مظبوط). كلهم بيشتغلوا على استوديو واحد على جهازك، فبراندك وتفضيلاتك ومكتبة
ملفاتك والدروس المستفادة بتنتقل من مهارة لمهارة ومن فيديو لفيديو.

| Skill | الاسم | What it does | بتعمل إيه |
|---|---|---|---|
| **Hakawati** `hakawati-video-studio` | **الحكواتي** | The all-in-one studio: picks the right format (faceless motion, talking head + graphics, screen tutorial, 2D, 3D) and makes the whole video | الاستوديو الكامل: بيختار الشكل المناسب ويعمل الفيديو كله |
| **Kashaf** `kashaf-screen-editor` | **كشّاف** | Pro editor for screen recordings: tight cuts, smooth zooms, spotlights, callouts, privacy blur, chapters, quizzes | مونتير محترف لتسجيلات الشاشة: قص، زووم، إضاءة، تعليقات، تمويه البيانات، فصول، أسئلة |
| **Nabd** `nabd-motion-graphics` | **نبض** | Motion graphics where every visual lands on the spoken word: kinetic type, UI mockups, counters, intros/outros | موشن جرافيك كل حركة فيه على الكلمة: نصوص متحركة، واجهات، عدادات، انترو وأوترو |
| **Risha** `risha-2d-animation` | **ريشة** | 2D animation: talking characters with lip-sync, whiteboard, cut-out, doodles, Lottie | انيميشن 2D: شخصيات بتتكلم بمزامنة الشفايف، سبورة، قص ولزق، دودلز |
| **Ab'aad** `abaad-3d-animation` | **أبعاد** | 3D: brand-colored hero objects, 3D logos, product spins, Blender and AI 3D | ثري دي: مجسمات بألوان البراند، لوجو 3D، عرض منتجات، بلندر و3D بالذكاء الاصطناعي |

## What every skill does for you · كل مهارة بتعمل لك إيه

1. **Setup** — checks your computer (CPU, memory, graphics card, disk, ffmpeg, Node.js, Python) and guides you to install
   what's missing, one command at a time. · **التجهيز**: بتفحص جهازك وتساعدك تنزّل الناقص خطوة بخطوة.
2. **Your brand & taste** — a short friendly interview: colors, fonts, logo, style, what to avoid, budget. Saved once.
   · **براندك وذوقك**: أسئلة قليلة مرة واحدة بس.
3. **Library** — catalogs what you already have (logo, photos, past videos, recordings, sounds) and reuses it before
   making anything new. · **المكتبة**: بتفهرس ملفاتك وتعيد استخدامها قبل ما تعمل جديد.
4. **Tools** — works at $0 (free local transcription, code-built graphics); explains what an OpenAI key or an AI
   generator (e.g. Higgsfield) would add, and never spends money without your OK. · **الأدوات**: شغالة ببلاش، ومش بتصرف
   ولا مليم من غير موافقتك.
5. **Your language** — talks to you in your language and dialect; beginner or pro mode. · **لغتك**: بتكلمك بلهجتك.
6. **Explains & learns** — after every video: what it did, what it couldn't verify, 3 suggestions, and one feedback
   question — and it remembers your answer next time. · **بتشرح وبتتعلم**: بتقولك عملت إيه، وتقترح، وتسألك رأيك وتفتكره.

## Install · التثبيت

**Claude Code / Claude desktop (Code tab):** copy a skill folder from `dist/` into `~/.claude/skills/` (all users) or
`<your project>/.claude/skills/`, then restart. Or install the `.skill` file from `dist/` where your Claude app offers
"Save skill". Then just say what you want: *"make a reel from this voice note"* · *"اعمل لي فيديو من الفويس ده"*.

انسخ فولدر المهارة من `dist/` لـ `~/.claude/skills/` وأعد تشغيل Claude، أو ثبّت ملف `.skill`. وبعدين قول اللي
عايزه عادي.

Requirements (the skill checks and helps install): Python 3.10+, Node.js 18+, ffmpeg. Optional: `faster-whisper`
(free transcription), an OpenAI key (best transcription + automatic retake finder), Blender (cinematic 3D), an AI
generation MCP such as Higgsfield (images, SFX, clips).

## Where things live · فين الحاجات

`~/VideoStudio/` (you can choose another folder): `profile.md` (what the AI remembers about you) · `brand/` ·
`library/` · `projects/<video>/` · `inbox/` (drop raw files here) · `engine/` (the scripts) · `lessons.md`.

## For maintainers · للمطوّرين

Edit sources, not `dist/`: `_shared/SKILL_CORE.md` (rules every skill follows), `_shared/references/` (shared
know-how), `_shared/domains/` (craft playbooks), `_shared/engine/` (pipeline + motion kit), `<skill>/SKILL.md`.
Rebuild + package: `python skills/build_skills.py`. Test evals: `eval-workspace/`.
Built from the production lessons of the Hossam Story Telling factory (`docs/LESSONS_LEARNED.md`).
