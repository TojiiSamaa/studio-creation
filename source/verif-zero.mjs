import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome' });
const p = await nav.newPage({ viewport: { width: 390, height: 844 }, colorScheme: 'light' });
await p.goto(new URL('studio.html', import.meta.url).href); await p.waitForTimeout(500);
console.log('thème :', await p.evaluate(() => document.documentElement.dataset.theme));
console.log('échelles nulles :', await p.evaluate(() => (document.querySelector('#apercu').innerHTML.match(/scaleX\(-?0\.000\)/g) || []).length),
  'échelles 0.001 :', await p.evaluate(() => (document.querySelector('#apercu').innerHTML.match(/scaleX\(-?0\.001\)/g) || []).length));
await nav.close();
