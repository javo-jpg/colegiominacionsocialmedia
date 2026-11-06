# How the Colegio Mi Nación social media system works

This document describes the pipeline that plans, designs, renders, schedules and previews the monthly social content for Colegio Mi Nación (Instagram + Facebook). It reflects the state of November 2026.

## 1. Big picture

```
brand assets + real photos/videos
        │
        ▼
 Python design system (PIL)  ──►  JPG posts / carousels
        │                    ──►  MP4 reels (frames → ffmpeg + music)
        │                    ──►  MP4 stories (animated)
        ▼
 GitHub repo (public raw URLs)
        │
        ▼
 Metricool (schedules IG + FB)      ──►  Preview page (artifact) for the team
```

Everything is code. Re-running a script regenerates the files; committing and pushing makes them reachable by Metricool; updating the scheduled post in Metricool swaps the media.

## 2. Repository layout

| Path | What it holds |
|---|---|
| `brand/` | Logos, seal, and `zonas-seguras.md` (safe-zone rules) |
| `media/` | Real photos used in designs (ofrendas, playground, books, etc.) |
| `assets/2026-11/<slug>/` | Rendered post slides (`01.jpg`, `02.jpg`, …) |
| `assets/2026-11/stories-v2/` | Rendered animated stories (`.mp4` + poster `.jpg`) |
| `plan/2026-11/` | Data: `posts.json`, `stories_v2.json`, `calendario.json`, `metricool.json`, preview HTML, preview videos in `v/` |
| `scripts/` | All generators (see below) |

## 3. Scripts

| Script | Role |
|---|---|
| `design.py` | Shared design toolkit: palette, fonts, text wrapping and fitting, pills, sparkles, icons, logo loader, watermark system (`wm_mark`, `watermark`, `WM_KINDS`), `canvas()`, decoration helper `deco()` |
| `posts.py` | Layout functions for feed and reel covers: full-bleed photo (`L_photo_full`, `L_photo_panel` now delegates to it), type-only (`L_type`), list, phone mockup, CTA, polaroid, circles, big number, reel cover and reel card |
| `build.py` | Defines every November post (copy, slides, layouts), renders the JPGs and writes `posts.json` |
| `motion.py`, `reels.py`, `reels_end.py`, `reel.sh`, `reel_ov.py`, `recap2.py`, `recap_cover.py`, `asr.py` | Reels: full-screen motion graphics, the ofrendas recap, end cards, overlays, speech-to-text helper |
| `motion_stories.py` | Animated stories (three templates, see §6) and `stories_v2.json` |
| `stories.py`, `stories2.py`, `highlights.py` | Earlier static stories and highlight covers (superseded by `motion_stories.py` for scheduling) |
| `solicitudes.py` | The "requests for the agency" list (footage and photos we need) shown in the preview |
| `preview2.py` + `preview2.tpl.html` | Builds the single-file preview page of the month |
| `slides.py` | Slide helpers |

## 4. Brand and design rules (enforced in code or by convention)

- **Palette:** green `#235D4E`, light green `#DCE5B6`, yellow `#EDCC6F`, blue `#549EBB`, cream `#FCF8EF`, coral `#E8836B`, ink `#1F2B27`.
- **Fonts:** Mija (display) and Söhne Kräftig/Leicht (text). Söhne has no "→" glyph, so arrows are drawn as shapes.
- **Safe zones:** feed 4:5 with 80 px margins; Reels text inside x 80–960, y 270–1500; Stories y 250–1580; covers must survive the 3:4 profile-grid crop. Some layouts assert and fail if text leaves the zone.
- **Never put text over children.**
- **Clean layouts:** no split screens (photo on top, color panel below). Photos are full-bleed with a soft gradient and short text.
- **Papel picado only for Día de Muertos.** Other posts use neutral design with watermark-style elements (seal, smiley, "Aa", sun, hearts, pencil scribbles).
- **Variety:** the feed must not be mostly green; colors and layouts rotate.
- **Real evidence over pure graphics:** use real school photos and video wherever available; replace placeholders when the agency delivers footage.
- **No AI-generated children.**
- **No invented facts:** no costs, scholarships, promos, quotas, dates or certifications beyond what the school confirmed. Cambridge: the school covers the cost, and the grade is confirmed with admissions. The free experience week is "sujeta a disponibilidad".
- **Music:** only Epidemic Sound tracks, mixed low. The track `guerita_34` is only for Día de Muertos.

## 5. Feed posts and carousels

1. `build.py` declares each post: slug, caption, hashtags, publication date/time and a list of slide layouts.
2. Each slide is drawn with PIL at 1080×1350 and saved as a JPG.
3. `posts.json` stores the metadata, which is reused for the stories and the preview.
4. Instagram crops a carousel to the first image's ratio, so all slides keep the same size.

## 6. Stories

`motion_stories.py` renders each story as a 1080×1920, 24 fps video: PIL draws every frame, ffmpeg encodes H.264 and mixes music (fade in 0.4 s, fade out 1.2 s, volume 0.55). There are three templates:

- **text:** icon pop, pill label, staggered title and body lines, contact rows. Used for evergreen highlight stories and the Friday "Pide informes" reminders.
- **photo:** full-bleed photo with slow zoom, logo at the top, label and title at the bottom.
- **teaser:** a title and a tilted card that swipes through the post's real slides, with dots and a "Desliza para ver todo" or "Mírala en el perfil" pill. Scheduled 45 minutes after the post.

Thirty stories are defined: 11 evergreen (for highlights), 15 teasers and 4 Friday reminders. Output goes to `assets/2026-11/stories-v2/` and is listed in `plan/2026-11/stories_v2.json`.

## 7. Reels

Reels are full-screen motion graphics (no half-screen banners). Frames come from PIL, are piped to ffmpeg, and the audio is a licensed track. The ofrendas recap combines the school's footage with the students' original audio. Reel covers (`L_reel_cover`) are full-bleed and kept inside the safe zone and the 3:4 grid crop.

## 8. Publishing to Metricool

- Brand id `7825187`, networks Instagram + Facebook, time zone `America/Mexico_City`.
- Media is referenced by raw GitHub URLs, for example `https://raw.githubusercontent.com/javo-jpg/colegiominacionsocialmedia/main/assets/2026-11/stories-v2/<name>.mp4?v=N`. Change `N` to bypass caching after re-rendering.
- Posts use `createScheduledPost` / `updateScheduledPost`. An update changes the post id; the uuid is stable.
- Stories use `STORY` type for both networks with empty text.
- Reels use `REEL` with an optional cover (`videoThumbnailUrl`).
- Draft posts mark pieces that need real footage (maestras, familias).

## 9. Preview page

`preview2.py` fills `preview2.tpl.html` with the post thumbnails, stories posters, highlights and the requests list, and writes a single HTML file. That file is published as a private-link artifact for the team and the agency (My Name Is Yellow), and a copy is stored in `plan/2026-11/preview-noviembre.html`. It must be regenerated and republished after design changes.

## 10. Typical workflows

**Change a design**
1. Edit the layout in `posts.py` / `design.py` (or a template in `motion_stories.py`).
2. Run `python3 scripts/build.py` (posts) or `python3 scripts/motion_stories.py [names…]` (stories; no names = all).
3. Check a contact sheet of the results for safe zones and legibility.
4. Commit and push.
5. Update the affected scheduled posts in Metricool with a new `?v=N`.
6. Run `python3 scripts/preview2.py` and republish the preview.

**When the agency delivers footage**
1. Replace the placeholder photos in `media/` or add new clips.
2. Regenerate the affected covers, stories and reels.
3. Swap drafts in Metricool for the real pieces and update the recap with kids' voices and subtitles.

**Add a new month**
1. Copy the November definitions in `build.py` and `motion_stories.py` to a new date folder and edit the copy.
2. Keep content fresh: do not repeat the previous month's posts or visuals.

## 11. Known limits

- Metricool cannot add interactive stickers (polls, questions, links) to stories. Add them manually in the Instagram app.
- Metricool cannot change the profile bio or photo.
- The preview shows story posters, not the animations.
- The preescolar reel's cover was redesigned, but the video body was not re-checked for the old split layout.
- The two posts that use a book photo (Papás Presentes opener and the November closing) put the title over the book, which reads less cleanly than the other photo posts. A real photo of families reading would be better.
- Several pieces are placeholders until the agency's shoot on 10–12 November (preescolar 10–11, primaria 12).
