import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome' }); const p = await nav.newPage({ viewport: { width: 1500, height: 900 }, reducedMotion: 'reduce' });
await p.goto(new URL('studio.html', import.meta.url).href);
await p.waitForTimeout(300);
console.log(await p.evaluate(() => JSON.stringify(etat.piece)));
await p.click('#lecture');
for (const f of [0.2, 0.24, 0.25, 0.26, 0.3, 0.74, 0.75, 0.76]) {
  await p.evaluate((f) => { const t = f * etat.animation.duree * 1000; anims().forEach((a) => (a.currentTime = t)); }, f);
  await p.screenshot({ path: `caps/tr-${f}.png`, clip: await p.evaluate(() => { const r = document.querySelector('#apercu').getBoundingClientRect(); return { x: r.x + r.width / 2 - 70, y: r.y + r.height / 2 - 110, width: 140, height: 220 }; }) });
}
await nav.close();
