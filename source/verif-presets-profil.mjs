import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome', headless: false });
const p = await nav.newPage({ viewport: { width: 1500, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
await p.goto(new URL('studio.html', import.meta.url).href); await p.waitForTimeout(500);
await p.click('#lecture');
const nb = await p.evaluate(() => PRESETS_INTEGRES.length);
for (let i = 0; i < nb; i++) {
  await p.evaluate((i) => { etat = fusion(DEFAUT, PRESETS_INTEGRES[i].etat); toutRendre(); }, i);
  await p.waitForTimeout(150);
  const clip = await p.evaluate(() => { const r = document.querySelector('#apercu svg').getBoundingClientRect(); return { x: r.x + r.width / 2 - 50, y: r.y + r.height / 2 - 90, width: 100, height: 180 }; });
  for (const f of [0.246, 0.249, 0.251, 0.254]) {
    await p.evaluate((f) => { const t = f * etat.animation.duree * 1000; anims().forEach((a) => { a.pause(); a.currentTime = t; }); }, f);
    await p.waitForTimeout(60);
    await p.screenshot({ path: `caps/pp-${i}-${f}.png`, clip });
  }
}
await nav.close();
console.log(nb);
