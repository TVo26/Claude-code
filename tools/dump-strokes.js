const { chromium } = require('playwright');
(async () => { const br = await chromium.launch(); const pg = await br.newPage();
  await pg.goto('file:///home/user/Claude-code/samples/hendersonville-whiteboard.html?t=0');
  require('fs').writeFileSync(process.argv[2], JSON.stringify(await pg.evaluate(() => ({ TL: STROKES, CUTS, DUR, END })))); await br.close(); })();
