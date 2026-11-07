import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome', headless: false });
const p = await nav.newPage({ viewport: { width: 1500, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
await p.goto(new URL('studio.html', import.meta.url).href); await p.waitForTimeout(500);
await p.click('#lecture');
const fs = process.argv.slice(2).map(Number);
const clip = await p.evaluate(() => { const r = document.querySelector('#apercu svg').getBoundingClientRect(); return { x: r.x + r.width / 2 - 50, y: r.y + r.height / 2 - 80, width: 100, height: 160 }; });
for (const f of fs) {
  await p.evaluate((f) => { const t = f * etat.animation.duree * 1000; anims().forEach((a) => (a.currentTime = t)); }, f);
  await p.waitForTimeout(80);
  await p.screenshot({ path: `caps/pr-${f}.png`, clip });
}
await nav.close();
