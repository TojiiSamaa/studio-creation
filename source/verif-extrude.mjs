import assert from 'node:assert';
import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome', headless: false });
const p = await nav.newPage({ viewport: { width: 1500, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
const err = []; p.on('pageerror', (e) => err.push(e.message));
await p.goto(new URL('studio.html', import.meta.url).href); await p.waitForTimeout(500);
// espace : lecture/pause, même avec le focus sur un bouton de calque, sans le recliquer
await p.click('#p-calques [data-calque="piece"]');
await p.keyboard.press('Space'); assert.equal(await p.evaluate(() => enPause), true, 'espace → pause');
assert.equal(await p.evaluate(() => selection), 'piece');
await p.keyboard.press('Space'); assert.equal(await p.evaluate(() => enPause), false, 'espace → lecture');
await p.fill('[data-recherche]', 'a b').catch(() => {});
await p.evaluate(() => document.activeElement.blur());
await p.keyboard.press('Space'); // pause pour les captures
const planche = async (nom, fs, demi = 90) => {
  const clip = await p.evaluate((demi) => { const r = document.querySelector('#apercu svg').getBoundingClientRect(); return { x: r.x + r.width / 2 - demi, y: r.y + r.height / 2 - 90, width: 2 * demi, height: 180 }; }, demi);
  for (const f of fs) { await p.evaluate((f) => { const t = f * etat.animation.duree * 1000; anims().forEach((a) => { a.pause(); a.currentTime = t; }); }, f); await p.waitForTimeout(60); await p.screenshot({ path: `caps/${nom}-${f}.png`, clip }); }
};
const F = [0, 0.12, 0.2, 0.24, 0.25, 0.26, 0.3, 0.5, 0.7, 0.75, 0.8, 0.95];
await p.evaluate(() => { etat = fusion(DEFAUT, PRESETS_INTEGRES[4].etat); etat.piece.epaisseur = 24; toutRendre(); });
await planche('ex', F);
await p.evaluate(() => { etat = fusion(DEFAUT, {}); toutRendre(); });
await planche('pf', [0.246, 0.249, 0.251, 0.254, 0.746, 0.749, 0.751, 0.754], 50);
console.log('erreurs :', err.length ? err : 'aucune', '· poids', await p.evaluate(() => (svgCourant.length / 1024).toFixed(0) + ' Ko'));
await nav.close();
