import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome' });
const p = await nav.newPage({ reducedMotion: 'reduce' });
await p.goto(new URL('studio.html', import.meta.url).href);
await p.waitForTimeout(800);
console.log('aperçu :', await p.evaluate(() => anims().map((a) => a.playState).join(',')));
await p.evaluate(() => { document.getElementById('apercu').innerHTML = svgCourant; });
console.log('export (défaut) :', await p.evaluate(() => anims().map((a) => a.playState).join(',') || 'aucune'));
await nav.close();
