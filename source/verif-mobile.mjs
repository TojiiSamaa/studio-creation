import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome' });
for (const cs of ['light', 'dark']) {
  const p = await nav.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: cs });
  await p.goto(new URL('studio.html', import.meta.url).href); await p.waitForTimeout(600);
  await p.screenshot({ path: `caps/mobile-${cs}.png`, fullPage: true });
  await p.close();
}
await nav.close();
