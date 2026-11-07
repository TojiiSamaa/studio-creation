import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome', headless: false });
const p = await nav.newPage({ viewport: { width: 1500, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
const err = []; p.on('pageerror', (e) => err.push(e.message));
await p.goto(new URL('studio.html', import.meta.url).href); await p.waitForTimeout(500);
await p.evaluate(() => { etat.piece.neon = true; etat.piece.neonForce = 1.5; toutRendre(); });
const clip = await p.evaluate(() => { const r = document.querySelector('#apercu svg').getBoundingClientRect(); return { x: r.x + r.width / 2 - 90, y: r.y + r.height / 2 - 100, width: 180, height: 200 }; });
for (const f of [0.1, 0.2, 0.235, 0.25, 0.265, 0.4]) { await p.evaluate((f) => { const t = f * etat.animation.duree * 1000; anims().forEach((a) => { a.pause(); a.currentTime = t; }); }, f); await p.waitForTimeout(60); await p.screenshot({ path: `caps/nf-${f}.png`, clip }); }
console.log('erreurs :', err.length ? err : 'aucune');
await nav.close();
