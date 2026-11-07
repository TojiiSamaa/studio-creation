import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome' }); const p = await nav.newPage({ viewport: { width: 1500, height: 900 } });
const err = []; p.on('pageerror', (e) => err.push(e.message));
await p.goto(new URL('studio.html', import.meta.url).href);
await p.evaluate(() => { etat = fusion(DEFAUT, PRESETS_INTEGRES[3].etat); etat.piece.epaisseur = 34; etat.faces.faceA.neon = true; etat.faces.faceA.neonCouleur = '#ff6a1a'; etat.faces.faceB.neon = true; etat.faces.faceB.neonCouleur = '#3d8bff'; toutRendre(); });
await p.click('#lecture');
for (const f of [0.05, 0.15, 0.22, 0.25, 0.3, 0.4]) {
  await p.evaluate((f) => { const t = f * cycle(); anims().forEach((a) => (a.currentTime = t)); }, f);
  await p.locator('#apercu').screenshot({ path: `caps/neon-${f}.png`, clip: undefined });
}
console.log(err.length ? err : 'aucune erreur');
await nav.close();
