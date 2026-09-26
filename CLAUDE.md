# Code-drawn animations for YouTube

Single-file HTML/JS canvas animations. Every frame is drawn in code: no image assets, no libraries.
The owner is not a developer and makes YouTube videos. Explain in plain words and show results, not code.

## How to reply
- Keep replies brief: what was made, where it is, anything to watch out for. No long recaps.
- Batch questions. Ask only if a choice really changes the result; otherwise pick a sensible default and say so.
- Flag anything invented. Label sample or fictional data on screen, and say when a scene takes creative licence with history.

## Saving tokens
- The HTML files are large (20–60 KB each). Don't read a whole file to reuse one part.
  `grep -n` for the function you need and read only those lines.
- Checks default to **light**: one contact sheet (a grid of frames from the whole animation) in a single screenshot pass, fix what's broken, done.
  Do a full per-scene review only when asked ("full checks"). Skip checks when asked ("no checks").
- Reuse building blocks (below) instead of rewriting them.

## Files
| File | What it is | Reusable parts |
|---|---|---|
| `how-browsers-work.html` | 40 s pastel sketch explainer with Robo, the red square robot | `robot()`, sketchy `shape/rect/circ/poly/line`, `bubble()` |
| `samples/pixel-data-story.html` | Pixel art + data | pixel `ROBO` sprite, brick bar chart |
| `samples/pixel-map-voyage.html` | Pixel world map (Magellan) | **5×7 pixel font `G`** (the most complete copy), **`LAND` world coastlines**, ship sprite, route wrap past 180° |
| `samples/neon-pixel-cables.html` | Neon synthwave + pixel map | `synth()` backdrop, bloom pass, tilted-map strips |
| `samples/pixel-stickman.html` | Pixel stick-figure comic | skeleton `stick()` + `POSE` table, `bubble()`, `sfx()` |
| `samples/oregon-trail.html` | 60 s pixel story (man, ox, wagon) | `man()` with poses, `ox()`, `wagon()`, `caravan()`, parchment trail map, `tiltBlit()` for slopes |
| `samples/ink-brush-haiku.html` | Ink / sumi-e brush | `brush()` stroke, `blob()`, `wash()`, paper texture |
| `samples/style-reel.html` | 25 styles × 4 s | one quick version of each style (`s01`–`s25`) |

The pixel font `G` and `LAND` are copied into several files; when building a new file, splice them in from `samples/pixel-map-voyage.html`.

## Conventions
- One self-contained `.html` per animation, saved in `samples/`. Open it in a browser to play.
- Pixel styles draw into a 320×180 buffer that is scaled up with smoothing off. Other styles use a 1280×720 logical canvas.
- Every file has: click / space to pause, `?t=SECONDS` to open paused at a time, `window.renderAt(t)` for screenshots, and a loop at the end.
- Animation must depend only on time `t`, never `Math.random()` or wall-clock time, so frames are reproducible. Film grain is the one exception.
- Keep text readable at phone size: pixel text scale ≥ 1 on the 320×180 buffer, captions on a solid box.

## Checking frames
Playwright and Chromium are preinstalled (never run `playwright install`). Run with `NODE_PATH=$(npm root -g) node script.js`.
Load `file:///home/user/Claude-code/samples/<file>.html?t=0`, call `window.renderAt(t)` for several times, draw each frame into one big canvas,
and save a single PNG to the scratchpad. Look at that one image. Also report any `pageerror`.

## Video workflow
For turning a script into a finished YouTube video, use the `/youtube-animation` skill (`.claude/skills/youtube-animation/SKILL.md`).

## Git
Commit and push after each finished piece; the cloud container is temporary.
