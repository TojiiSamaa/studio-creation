import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome', headless: false });
const p = await nav.newPage({ viewport: { width: 1500, height: 900 }, deviceScaleFactor: 4, reducedMotion: 'reduce' });
await p.goto(new URL('studio.html', import.meta.url).href); await p.waitForTimeout(500);
await p.click('#lecture');
const clip = await p.evaluate(() => { const r = document.querySelector('#apercu svg').getBoundingClientRect(); return { x: r.x + r.width / 2 - 15, y: r.y + r.height / 2 - 60, width: 30, height: 120 }; });
const cas = { tout: '', sansFaces: '.va,.vb', sansOmbre: '[data-calque=piece].pa,[data-calque=piece].pb', sansTranche: '.tr', facesSeules: '.tr,[data-calque=piece].pa,[data-calque=piece].pb' };
for (const f of [0.252]) for (const [nom, sel] of Object.entries(cas)) {
  await p.evaluate(([f, sel]) => { document.querySelectorAll('#apercu *').forEach((x) => x.style && (x.style.visibility = '')); if (sel) document.querySelectorAll('#apercu ' + sel.split(',').join(',#apercu ')).forEach((x) => (x.style.visibility = 'hidden')); const t = f * etat.animation.duree * 1000; anims().forEach((a) => (a.currentTime = t)); }, [f, sel]);
  await p.waitForTimeout(80);
  await p.screenshot({ path: `caps/is-${nom}.png`, clip });
}
await nav.close();
