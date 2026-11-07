p = 'studio-gabarit.html'; s = open(p, encoding='utf8').read()
r = [
# boîte englobante réelle d'un tracé (les logos n'occupent pas tous leur carré 24×24)
("const esc = (s) =>",
 """const BOITES = new Map();
const boite = (d) => {
  if (!BOITES.has(d)) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'), t = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    svg.style.cssText = 'position:absolute;visibility:hidden'; t.setAttribute('d', d); svg.append(t); document.body.append(svg);
    const b = t.getBBox(); svg.remove();
    BOITES.set(d, b.width && b.height ? { x: b.x, y: b.y, w: b.width, h: b.height } : { x: 0, y: 0, w: 24, h: 24 });
  }
  return BOITES.get(d);
};
const esc = (s) =>"""),
# logo seul : chaque logo est cadré sur sa vraie boîte, à la même taille, centré → les deux faces se superposent
("""    const f = e.faces[cle], p = e.piece, k = (p.support === 'logo' ? R * 1.75 : R * 1.12) * f.taille / 100 / 24, L = k * 24;
    const pose = `transform="translate(${n(cx - L / 2)} ${n(cy - L / 2)}) scale(${k.toFixed(4)})"`;
""",
"""    const f = e.faces[cle], p = e.piece, { k, pose } = cadre(f);
"""),
("  const face = (cle, silhouette = false) =>",
 """  const cadre = (f) => {
    if (e.piece.support !== 'logo') { const k = R * 1.12 * f.taille / 100 / 24, L = k * 24; return { k, pose: `transform="translate(${n(cx - L / 2)} ${n(cy - L / 2)}) scale(${k.toFixed(4)})"` }; }
    const b = boite(f.d), k = R * 1.75 * f.taille / 100 / Math.max(b.w, b.h);
    return { k, pose: `transform="translate(${n(cx - (b.x + b.w / 2) * k)} ${n(cy - (b.y + b.h / 2) * k)}) scale(${k.toFixed(4)})"` };
  };
  const face = (cle, silhouette = false) =>"""),
# épaisseur pour les deux supports ; faces masquées un instant pile de profil (Chrome y dessine des traits parasites qui dépassent de la tranche)
("const d = e.piece.support === 'piece' ? e.piece.epaisseur : 0,", "const d = e.piece.epaisseur,"),
("@keyframes va{0%{opacity:1}25%{opacity:0}75%{opacity:1}}@keyframes vb{0%{opacity:0}25%{opacity:1}75%{opacity:0}}",
 "@keyframes va{0%{opacity:1}24.4%{opacity:0}75.6%{opacity:1}}@keyframes vb{0%{opacity:0}25.6%{opacity:1}74.4%{opacity:0}}.vp{animation:vp ${T}s step-end infinite}@keyframes vp{0%{opacity:1}24.4%{opacity:0}25.6%{opacity:1}74.4%{opacity:0}75.6%{opacity:1}}"),
("    if (d) {\n      const ombre", "    if (d && sil) {\n      const ombre"),
("const disque = (cls) => `<g class=\"${cls}\" data-calque=\"piece\"><circle cx=\"${cx}\" cy=\"${cy}\" r=\"${n(R)}\" fill=\"${ombre}\"/></g>`;",
 "const disque = (cls) => `<g class=\"${cls}\" data-calque=\"piece\"><g class=\"vp\"><circle cx=\"${cx}\" cy=\"${cy}\" r=\"${n(R)}\" fill=\"${ombre}\"/></g></g>`;"),
("    piece += `<g class=\"pa\"><g class=\"va\" data-calque=\"faceA\">",
 """    if (d && !sil) { // logo seul extrudé : des tranches du logo empilées dans l'épaisseur, côté A la forme A, côté B la forme B
      const miroir = `translate(${cx} 0) scale(-1 1) translate(${-cx} 0)`;
      const forme = (cle) => { const f = e.faces[cle], { k, pose } = cadre(f); return `<path d="${f.d}" fill="currentColor" ${pose}${f.gras ? ` stroke="currentColor" stroke-width="${(f.gras * 2 / k).toFixed(3)}" stroke-linejoin="round"` : ''}/>`; };
      defs.push(`<g id="xa">${forme('faceA')}</g><g id="xb"><g transform="${miroir}">${forme('faceB')}</g></g>`);
      // profondeur z : translateX(z·sin) scaleX(cos) obtenu avec deux animations communes, l'amplitude z venant d'une échelle fixe autour
      css.push(kf('dx', (a) => `translateX(${Math.sin(a).toFixed(4)}px)`), kf('pc', (a) => `scaleX(${cos(a)})`),
        `.dx{animation:dx ${T}s linear infinite}.pc{${centre};animation:pc ${T}s linear infinite}.sa{animation:sa ${T}s step-end infinite}.sb{animation:sb ${T}s step-end infinite}@keyframes sa{0%{opacity:1}25%{opacity:0}75%{opacity:1}}@keyframes sb{0%{opacity:0}25%{opacity:1}75%{opacity:0}}`);
      const m = Math.min(48, Math.max(2, Math.ceil(d))), pas = d / m, x = (v) => `translate(${cx} 0) scale(${v.toFixed(4)} 1) translate(${-cx} 0)`;
      const couche = (i) => {
        const z = -d / 2 + (i + 0.5) * pas, t = Math.abs(z) / (d / 2);
        return `<g transform="${x(z)}"><g class="dx"><g transform="${x(1 / z)}"><g class="pc"><use href="#${z > 0 ? 'xa' : 'xb'}" color="${melange(e.piece.tranche, '#000000', 0.5 - 0.35 * t)}"/></g></g></g>`;
      };
      const ordre = Array.from({ length: m }, (_, i) => i); // de l'arrière vers l'avant selon la face tournée vers nous
      piece += `<g data-calque="piece"><g class="sa">${ordre.map(couche).join('')}</g><g class="sb">${ordre.reverse().map(couche).join('')}</g></g>`;
    }
    piece += `<g class="pa"><g class="va" data-calque="faceA">"""),
# inspecteur : l'épaisseur vaut aussi pour le logo seul
("""      note((e) => (e.animation.type === 'retournement' ? '' : 'Visible seulement avec le retournement.')), condition((e) => e.piece.support === 'piece')),""",
 """      note((e) => (e.animation.type !== 'retournement' ? 'Visible seulement avec le retournement.' : e.piece.support === 'logo' ? 'Logo extrudé : chaque moitié de l\'épaisseur prend la forme de sa face.' : ''))),"""),
("resume: (e) => (e.piece.support === 'logo' ? 'Logo seul' :", "resume: (e) => (e.piece.support === 'logo' ? 'Logo seul' + (e.piece.epaisseur ? ` · extrudé ${e.piece.epaisseur} px` : '') :"),
# barre d'espace = lecture/pause, sauf dans un champ de saisie
("btnLecture.onclick = () => pause(!enPause);",
 """btnLecture.onclick = () => pause(!enPause);
document.addEventListener('keydown', (ev) => {
  if (ev.code !== 'Space' || ev.target.closest('textarea,select,[contenteditable]') || (ev.target.matches('input') && !['range', 'checkbox', 'radio', 'color'].includes(ev.target.type))) return;
  ev.preventDefault(); pause(!enPause);
});"""),
]
for a, b in r:
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)
open(p, 'w', encoding='utf8').write(s)
print('ok', len(r))
