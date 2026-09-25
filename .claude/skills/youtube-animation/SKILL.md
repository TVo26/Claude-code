---
name: youtube-animation
description: Turn a finished YouTube script into a code-animated video, step by step. Covers optional niche research, a scene-by-scene shot list, style lock, Remotion animation synced to a voiceover, MP4 render, thumbnail, title, description and chapters. Use when the user has a video idea or script and wants animations or a finished video for YouTube, or types /youtube-animation.
---

# YouTube animation workflow

The user has an idea and a script and wants code-drawn animations for it. Work through
the steps in order. Stop at each **checkpoint** for the user's approval before going on;
redoing later steps costs far more than a quick check.

The user is not a developer. Explain in plain words, show results as screenshots or clips
rather than code, and never ask them to edit code themselves.

## Step 0: Gather inputs

Ask only for what is missing:

1. The script (final or near final).
2. Target length (e.g. 2 min, 10 min).
3. Style: the house style below (Robo, pastel sketch) or something new.
4. Voiceover: their own voice or an AI voice. If they already have audio, get the file.

If they have no script yet, help them write one first, then continue.

## Step 1: Idea check (optional, ask first)

If the TubeLab tools are connected, offer to research the niche. Only the search tools
cost credits, so say so before searching.
- Find outlier videos (ones that far outperformed their channel) on the topic.
- Pull 1–2 transcripts to study the hook and pacing.
- Report back briefly: typical length, hook style, title patterns, and 2–3 concrete
  script suggestions. Don't rewrite their script unless asked.

## Step 2: Shot list  (checkpoint)

Split the script into scenes and save it as `videos/<slug>/shotlist.md`:

| # | Narration | On screen | Seconds |
|---|-----------|-----------|---------|

- About 130–150 spoken words ≈ 1 minute. Scenes are usually 3–10 s.
- Every scene needs one clear visual idea that *shows* the narration and doesn't just
  repeat it as text.
- Add chapter markers where the topic shifts; they become YouTube chapters later.

Show the table and wait for approval.

## Step 3: Voiceover first

Timing visuals to real narration looks far better than the other way round.
- Own voice: tell them to record one take per scene (or one long take), export
  WAV/MP3, and add it to `videos/<slug>/audio/`. Suggest Audacity (free).
- AI voice: suggest ElevenLabs or similar. It happens outside this session.
- No audio yet: build using the shot-list timings and re-time when the audio arrives.

Once you have audio, measure each scene's length and update the shot list.

## Step 4: Style lock  (checkpoint)

Build **one** representative scene first (character, palette, fonts, title-card
look), render 2–3 still frames and show them. Get approval before building the rest.

House style (reference: `how-browsers-work.html` at the repo root):
- Robo: a red square robot with an antenna, face screen, blinking eyes, pink cheeks and
  noodle arms. Reuse the `robot()` function and its poses.
- Pastel palette on notebook paper, with jittered "boiling" lines redrawn about 8×/s from
  a seeded RNG (`shape`, `rect`, `circ`, `poly`, `line`, `arrow` helpers).
- A numbered stage label top-left with a wavy underline, and a caption pill at the bottom.
- Embed a real font file (e.g. a Google handwriting font) so text looks the same on every
  machine. Don't rely on system fonts.

## Step 5: Build the animation (main work)

Use **Remotion** (React to MP4). It has a real timeline, audio sync and direct MP4
export.

```bash
cd videos/<slug>
npx create-video@latest --yes --blank --no-tailwind .   # or scaffold by hand
npm i
```

- Size 1920×1080, 30 fps (60 only if motion needs it).
- One `<Sequence>` per scene, with lengths from the measured audio. Put the voiceover in
  an `<Audio>` at the root.
- Draw each scene on a `<canvas>` or in SVG, driven only by `useCurrentFrame()`. No
  `Date.now()` or `requestAnimationFrame`, so every frame renders the same way each time.
- Port the sketch helpers from the reference file into a shared module.
- Build scenes in batches of 3–5. After each batch, render stills
  (`npx remotion still`) or a short draft clip, show the user, and apply their notes.

Rendering in this cloud container:
- If Remotion can't download its own browser, pass
  `--browser-executable=/opt/pw-browsers/chromium`.
- Playwright + Chromium are preinstalled for quick screenshots. Don't run
  `playwright install`.

## Step 6: Sound

- Background music at about 10–20% volume under the voice. Recommend the YouTube Audio
  Library (free and safe for YouTube). Never use music the user doesn't have rights to.
- Optional sound effects (pops, whooshes) on key moments, placed as `<Audio>` in the
  matching `<Sequence>`.
- If the user prefers, hand off a silent MP4 plus timings for them to mix in DaVinci
  Resolve or CapCut.

## Step 7: Render  (checkpoint)

```bash
npx remotion render <CompositionId> out/<slug>.mp4 --codec=h264
```

Watch-check it yourself by sampling stills across the timeline, then send the MP4 to the
user and ask them to watch it all the way through with sound.

## Step 8: Packaging

- **Thumbnail:** 1280×720 PNG in the same style: large readable text of 3–5 words and
  an expressive Robo. Render it as a Remotion still.
- **Titles:** 3–5 options under 60 characters.
- **Description:** 2–3 sentence summary, chapters from the shot list (`0:00 Intro`
  format; the first chapter must start at 0:00, at least 3 chapters, each ≥10 s), and
  music credits if the licence needs them.

Save these in `videos/<slug>/publish.md`.

## Step 9: Upload (the user does this)

Uploading happens in YouTube Studio: title, description, thumbnail, and captions
(auto-generated, then corrected). You can't upload for them.

## Housekeeping

- The cloud container is temporary. **Commit and push after every step** so nothing is
  lost. Keep large renders (`out/`, `node_modules/`) out of git with `.gitignore` and
  send MP4s to the user directly.
- Suggest a fresh session per video; long sessions use more of the plan's limits.
- Start with a 1–2 minute video before attempting a long one.
