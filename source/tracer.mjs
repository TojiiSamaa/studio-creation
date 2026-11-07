// Vectorise les couches (masque, moyen, lumière) de chaque main → mains.json { nom: { l, h, couches: { fond, moyen, lumiere } } }
import potrace from 'potrace';
import { writeFileSync, existsSync } from 'node:fs';
import { promisify } from 'node:util';
const trace = promisify(potrace.trace);
const sortie = {};
const dir = process.argv[2] || '.';
for (const main of ['main-adam', 'main-dieu']) {
  sortie[main] = { couches: {} };
  for (const [couche, f] of [['fond', ''], ['moyen', '-moyen'], ['clair', '-clair'], ['lumiere', '-lumiere']].map(([c, s]) => [c, `${dir}/${main}${s}.png`]).filter(([, f]) => existsSync(f))) {
    const svg = await trace(f, { turdSize: Number(process.env.TURD || 40), optTolerance: 0.35, alphaMax: 1.1, threshold: 128 });
    const [, l, h] = svg.match(/width="(\d+)" height="(\d+)"/);
    Object.assign(sortie[main], { l: +l, h: +h });
    sortie[main].couches[couche] = [...svg.matchAll(/ d="([^"]+)"/g)].map((m) => m[1]).join(' ');
  }
  console.log(main, sortie[main].l, 'x', sortie[main].h, Object.entries(sortie[main].couches).map(([k, v]) => `${k}:${(v.length / 1024).toFixed(0)}Ko`).join(' '));
}
writeFileSync(`${dir}/mains.json`, JSON.stringify(sortie));
