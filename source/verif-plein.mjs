import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome', headless: false });
const p = await nav.newPage({ viewport: { width: 1500, height: 900 }, deviceScaleFactor: 3, reducedMotion: 'reduce' });
const err = []; p.on('pageerror', (e) => err.push(e.message));
await p.goto(new URL('studio.html', import.meta.url).href); await p.waitForTimeout(500);
for (const i of [0, 3]) {
  await p.evaluate((i) => { etat = fusion(DEFAUT, PRESETS_INTEGRES[i].etat); if (i === 0) etat.piece.epaisseur = 24; toutRendre(); }, i);
  const clip = await p.evaluate(() => { const r = document.querySelector('#apercu svg').getBoundingClientRect(); return { x: r.x + r.width / 2 - 70, y: r.y + r.height / 2 - 80, width: 140, height: 160 }; });
  for (const f of [0.19, 0.21, 0.23, 0.24, 0.26, 0.29]) { await p.evaluate((f) => { const t = f * etat.animation.duree * 1000; anims().forEach((a) => { a.pause(); a.currentTime = t; }); }, f); await p.waitForTimeout(60); await p.screenshot({ path: `caps/pl-${i}-${f}.png`, clip }); }
}
console.log('erreurs :', err.length ? err : 'aucune');
await nav.close();
