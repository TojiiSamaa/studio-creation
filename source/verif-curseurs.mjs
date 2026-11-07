import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome' }); const p = await nav.newPage({ viewport: { width: 1200, height: 520 } });
const err = []; p.on('pageerror', (e) => err.push(e.message));
await p.goto(new URL('studio.html', import.meta.url).href);
for (const [c, v] of [['grasL', 2], ['bord', 10], ['tailleL', 130]]) await p.locator(`[data-curseur="${c}"]`).fill(String(v));
await p.click('[data-cle="neon"] [data-v="fa"]'); await p.click('[data-cle="neon"] [data-v="dieu"]');
await p.waitForTimeout(400); await p.locator('.scene').screenshot({ path: 'cap-curseurs.png' });
console.log(await p.evaluate(() => JSON.stringify({ grasL: etat.grasL, bord: etat.bord, tailleL: etat.tailleL, neon: etat.neon })), err.length ? err : 'aucune erreur');
await nav.close();
