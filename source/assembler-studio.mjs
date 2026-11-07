// Injecte mains/bouts/logos dans le gabarit → studio.html autonome ; puis parcours de contrôle complet avec captures.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import assert from 'node:assert';
const ici = new URL('.', import.meta.url);
const lire = (f) => readFileSync(new URL(f, ici), 'utf8');
const j = (f) => JSON.stringify(JSON.parse(lire(f))).replace(/</g, '\\u003c');
const html = lire('studio-gabarit.html').replace('/*MAINS*/{}', j('mains.json')).replace('/*BOUTS*/{}', j('bouts.json')).replace('/*LOGOS*/{}', j('logos.json'));
const sortie = new URL('studio.html', ici);
writeFileSync(sortie, html);
console.log('studio.html', (html.length / 1024).toFixed(0), 'Ko');
if (process.argv.includes('--sans-test')) process.exit(0);

mkdirSync(new URL('caps/', ici), { recursive: true });
const cap = (nom) => new URL(`caps/${nom}.png`, ici).pathname.slice(1);
import { chromium } from 'playwright-core';
const nav = await chromium.launch({ channel: 'chrome' });
const page = await nav.newPage({ viewport: { width: 1500, height: 900 }, reducedMotion: 'reduce' }); // comme le poste de Toji
const erreurs = [];
page.on('pageerror', (e) => erreurs.push(e.message));
page.on('console', (m) => m.type() === 'error' && erreurs.push(m.text()));
await page.goto(sortie.href);
await page.waitForTimeout(500);
assert.ok((await page.evaluate(() => anims().filter((a) => a.playState === 'running').length)) > 0, 'l’aperçu doit jouer au chargement');
await page.screenshot({ path: cap('studio') });

// chaque élément : l'inspecteur s'affiche sans erreur
for (const id of ['scene', 'animation', 'gauche', 'droite', 'piece', 'faceA', 'faceB']) {
  await page.click(`#p-calques [data-calque="${id}"]`);
  assert.equal(await page.evaluate(() => selection), id);
}
await page.click('#p-calques [data-calque="piece"]'); await page.screenshot({ path: cap('insp-piece') });
await page.click('#p-calques [data-calque="gauche"]');
await page.click('[data-chemin="mains.gauche.neon"]');
assert.ok(await page.evaluate(() => etat.mains.gauche.neon && etat.mains.droite.neon), 'mains liées : le néon suit');
await page.click('[data-chemin="mains.lier"]');
await page.click('[data-chemin="mains.gauche.neonZone"][data-v="tout"]');
assert.equal(await page.evaluate(() => etat.mains.droite.neonZone), 'contour', 'mains déliées : la droite ne bouge plus');
await page.locator('[data-chemin="mains.gauche.lum"]').fill('0.4');
await page.waitForTimeout(200);
await page.screenshot({ path: cap('insp-main') });
// palette de couleur : ouverture, code hexadécimal saisi à la main, pastille
await page.click('[data-palette="mains.gauche.neonCouleur"]');
await page.fill('[data-hex="mains.gauche.neonCouleur"]', '3d8bff');
await page.press('[data-hex="mains.gauche.neonCouleur"]', 'Enter');
await page.locator('[data-hex="mains.gauche.neonCouleur"]').evaluate((el) => el.dispatchEvent(new Event('change', { bubbles: true })));
assert.equal(await page.evaluate(() => etat.mains.gauche.neonCouleur), '#3d8bff');
await page.screenshot({ path: cap('insp-palette') });
await page.click('.pastilles [data-v="#3fb950"]');
assert.equal(await page.evaluate(() => etat.mains.gauche.neonCouleur), '#3fb950');
// section repliée, liste déroulante
await page.click('[data-plier="gauche:Apparence"]');
assert.equal(await page.locator('[data-chemin="mains.gauche.lum"]').count(), 0, 'section repliée');
await page.click('#p-calques [data-calque="animation"]');
await page.selectOption('select[data-chemin="animation.duree"]', '8');
assert.equal(await page.evaluate(() => etat.animation.duree), 8);

// préréglages intégrés
await page.click('[data-onglet="presets"]');
const nb = await page.locator('[data-preset^="int:"]').count();
for (let i = 0; i < nb; i++) {
  await page.click(`[data-preset="int:${i}"]`);
  await page.waitForTimeout(250);
  await page.locator('.toile').screenshot({ path: cap(`preset${i}`) });
}
await page.screenshot({ path: cap('presets') });

// pièce épaisse : instants du retournement
await page.click('[data-preset="int:3"]');
await page.click('#lecture');
for (const f of [0.1, 0.2, 0.3, 0.6]) {
  await page.evaluate((f) => { const t = f * cycle(); anims().forEach((a) => (a.currentTime = t)); }, f);
  await page.locator('#apercu').screenshot({ path: cap(`tour-${f}`) });
}
await page.click('#lecture');

// enregistrement d'un préréglage, lien de partage aller-retour
await page.fill('#nomPreset', 'Test auto');
await page.click('#enregistrer');
assert.equal(await page.evaluate(() => mesPresets[0].nom), 'Test auto');
const lien = await page.evaluate(() => b64.enc(JSON.stringify(etat)));
assert.deepEqual(await page.evaluate((l) => JSON.parse(b64.dec(l)), lien), await page.evaluate(() => etat));
await page.evaluate(() => { mesPresets.shift(); stockage.ecrire(CLE_PRESETS, mesPresets); });

// recherche de logo dans le catalogue complet (réseau)
await page.click('[data-onglet="calques"]');
await page.click('#p-calques [data-calque="faceA"]');
await page.fill('[data-recherche="faceA"]', 'rust');
await page.waitForSelector('[data-resultats="faceA"] img', { timeout: 20000 });
await page.waitForTimeout(800);
await page.screenshot({ path: cap('recherche') });
await page.click('[data-resultats="faceA"] [data-logo="rust"]');
await page.waitForFunction(() => etat.faces.faceA.slug === 'rust', null, { timeout: 15000 });
console.log('recherche : faceA =', await page.evaluate(() => etat.faces.faceA.titre));

// thème clair
await page.click('#theme');
await page.waitForTimeout(200);
await page.screenshot({ path: cap('clair') });

console.log('erreurs :', erreurs.length ? erreurs : 'aucune');
await nav.close();
