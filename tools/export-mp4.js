const { chromium } = require('playwright'); const { spawn } = require('child_process');
const [,, html, wav, mp4, ffmpeg] = process.argv, FPS = 30;
(async () => {
  const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  pg.on('pageerror', e => console.log('PAGEERROR', e.message));
  await pg.goto('file://' + html + '?t=0&export=1');
  const dur = await pg.evaluate(() => DUR), n = Math.round(dur * FPS);
  const ff = spawn(ffmpeg, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', wav,
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = 0; i < n; i++){
    const url = await pg.evaluate(t => { renderAt(t); return document.getElementById('c').toDataURL('image/png'); }, i / FPS);
    if (!ff.stdin.write(Buffer.from(url.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await br.close(); console.log('frames', n);
})();
