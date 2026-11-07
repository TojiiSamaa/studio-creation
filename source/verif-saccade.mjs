import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome', headless: false }); const p = await nav.newPage({ viewport: { width: 1500, height: 900 }, reducedMotion: 'reduce' });
await p.goto(new URL('studio.html', import.meta.url).href);
await p.waitForTimeout(800);
for (const preset of [0, 2, 3]) {
  await p.evaluate((i) => { etat = fusion(DEFAUT, PRESETS_INTEGRES[i].etat); toutRendre(); }, preset);
  await p.waitForTimeout(300);
  const r = await p.evaluate(() => new Promise((ok) => {
    const T = etat.animation.duree * 1000, a = anims().find((x) => x.animationName === 'pa' || (x.effect && x.effect.target && x.effect.target.classList && x.effect.target.classList.contains('pa')));
    const gaps = []; let prev = performance.now(); const fin = prev + 2 * T;
    const tick = (now) => { const g = now - prev; if (g > 40) gaps.push([Math.round(g), a ? +((a.currentTime % T) / T).toFixed(3) : null]); prev = now; now < fin ? requestAnimationFrame(tick) : ok({ T, gaps, n: anims().length }); };
    requestAnimationFrame(tick);
  }));
  console.log('preset', preset, JSON.stringify(r));
}
await nav.close();
