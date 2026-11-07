p = 'studio-gabarit.html'; s = open(p, encoding='utf8').read()
CURSEUR = lambda cle, titre, mini, maxi, pas, unite: f'<fieldset><legend>{titre} <span class="valeur" id="v-{cle}"></span></legend><input type="range" data-curseur="{cle}" data-unite="{unite}" min="{mini}" max="{maxi}" step="{pas}" aria-label="{titre}"></fieldset>'
r = [
('''  <fieldset id="f-piece"><legend>Style de la pièce</legend><div class="choix" data-cle="piece"></div></fieldset>''',
'''  <fieldset id="f-piece"><legend>Style de la pièce</legend><div class="choix" data-cle="piece"></div></fieldset>
  <div id="f-bord">''' + CURSEUR('bord', 'Épaisseur du bord de la pièce', 0, 12, 0.5, ' px') + '''</div>
  ''' + CURSEUR('grasL', 'Épaisseur du logo', 0, 3, 0.1, ' px') + '''
  ''' + CURSEUR('tailleL', 'Taille du logo', 60, 140, 5, ' %')),
('''  <fieldset><legend>Mains</legend><div class="choix" data-cle="mains"></div></fieldset>''',
'''  <fieldset><legend>Mains</legend><div class="choix" data-cle="mains"></div></fieldset>
  ''' + CURSEUR('trait', 'Épaisseur du contour des mains', 0.5, 6, 0.1, ' px') + '''
  <fieldset><legend>Effet néon (plusieurs choix)</legend><div class="choix" data-cle="neon"></div></fieldset>'''),
("mains: [['relief', 'Relief'], ['silhouette', 'Silhouette'], ['contour', 'Contour'], ['neon', 'Néon']],",
 "mains: [['relief', 'Relief'], ['silhouette', 'Silhouette'], ['contour', 'Contour']],\n  neon: [['adam', 'Main gauche'], ['dieu', 'Main droite'], ['fa', 'Face avant'], ['fb', 'Face arrière']],"),
("support: 'piece', teinte: 'blanc' };", "support: 'piece', teinte: 'blanc', trait: 1.3, neon: [], bord: 3, grasL: 0, tailleL: 100 };"),
("rotation: 'piece', duree: 3.5, support: 'piece', mains: 'relief', piece: 'classique', fond: 'halo' }],", "rotation: 'piece', duree: 3.5, support: 'piece', mains: 'relief', piece: 'classique', fond: 'halo', neon: [] }],"),
("teinte: 'marque', mains: 'silhouette', fond: 'halo' }],", "teinte: 'marque', mains: 'silhouette', fond: 'halo', neon: ['fa'] }],"),
("mains: 'neon', piece: 'verre', fond: 'halo' }],", "mains: 'contour', trait: 1.6, piece: 'verre', fond: 'halo', neon: ['adam', 'dieu'] }],"),
("mains: 'silhouette', piece: 'classique', fond: 'noir' }],", "mains: 'silhouette', piece: 'classique', fond: 'noir', neon: [] }],"),
("mains: 'contour', fond: 'halo' }],", "mains: 'contour', trait: 1, fond: 'halo', neon: ['fa', 'fb'] }],"),
("mains: 'relief', piece: 'verre', fond: 'noir' }],", "mains: 'relief', piece: 'verre', fond: 'noir', neon: [] }],"),
('''  const sw = (1.3 / s).toFixed(2);
  const main = (nom) => {
    const c = MAINS[nom].couches;
    if (o.mains === 'relief') return `<path d="${c.fond}" fill="#3a3d42"/><path d="${c.moyen}" fill="#a7abb2"/><path d="${c.lumiere}" fill="#f6f7f9"/>`;
    if (o.mains === 'silhouette') return `<path d="${c.fond}" fill="#f6f7f9"/>`;
    if (o.mains === 'contour') return `<path d="${c.fond}" fill="none" stroke="#f6f7f9" stroke-width="${sw}"/><path d="${c.lumiere}" fill="#f6f7f9" opacity=".18"/>`;
    return `<path d="${c.fond}" fill="none" stroke="${accent}" stroke-width="${(6 / s).toFixed(2)}" filter="url(#lueur)"/><path d="${c.fond}" fill="none" stroke="${accent}" stroke-width="${(2.4 / s).toFixed(2)}"/><path d="${c.fond}" fill="none" stroke="#fff" stroke-width="${(0.9 / s).toFixed(2)}"/>`;
  };''',
'''  const px = (v) => (v / s).toFixed(2); // épaisseurs en pixels de scène : les mains sont mises à l'échelle s
  const main = (nom, cle) => {
    const c = MAINS[nom].couches, neon = o.neon.includes(cle);
    const trait = (coul, ep) => `<path d="${c.fond}" fill="none" stroke="${coul}" stroke-width="${px(ep)}" stroke-linejoin="round"/>`;
    const corps = o.mains === 'relief' ? `<path d="${c.fond}" fill="#3a3d42"/><path d="${c.moyen}" fill="#a7abb2"/><path d="${c.lumiere}" fill="#f6f7f9"/>`
      : o.mains === 'silhouette' ? `<path d="${c.fond}" fill="#f6f7f9"/>`
      : `<path d="${c.lumiere}" fill="#f6f7f9" opacity=".18"/>` + trait('#f6f7f9', o.trait);
    if (!neon) return corps;
    // néon : halo flou dessous, trait couleur + âme blanche dessus
    return `<path d="${c.fond}" fill="none" stroke="${accent}" stroke-width="${px(o.trait * 3 + 2)}" filter="url(#lueur)"/>` + corps + trait(accent, o.trait) + trait('#fff', Math.max(0.6, o.trait / 3));
  };'''),
("  const L = o.support === 'logo' ? R * 1.75 : R * 1.12;", "  const L = (o.support === 'logo' ? R * 1.75 : R * 1.12) * o.tailleL / 100, k = L / 24;"),
('''    if (o.support === 'logo') return `<g class="${cls}"${m0}><path d="${LOGOS[slug].d}" fill="${o.teinte === 'marque' ? hex : '#f6f7f9'}" transform="translate(${(cx - L / 2).toFixed(1)} ${(cy - L / 2).toFixed(1)}) scale(${(L / 24).toFixed(3)})"/></g>`;''',
'''    const neon = o.neon.includes(cls), pose = `transform="translate(${(cx - L / 2).toFixed(1)} ${(cy - L / 2).toFixed(1)}) scale(${k.toFixed(3)})"`;
    // épaisseur du logo = trait de la même couleur autour du tracé (en pixels de scène, d'où / k)
    const logo = (coul) => `<path d="${LOGOS[slug].d}" fill="${coul}" ${pose}${o.grasL ? ` stroke="${coul}" stroke-width="${(o.grasL * 2 / k).toFixed(3)}" stroke-linejoin="round"` : ''}/>`;
    const lueur = neon ? `<path d="${LOGOS[slug].d}" fill="${hex}" ${pose} filter="url(#lueurL)"/>` : '';
    if (o.support === 'logo') return `<g class="${cls}"${m0}>${lueur}${logo(o.teinte === 'marque' ? hex : '#f6f7f9')}</g>`;'''),
('''    return `<g class="${cls}"${m}><circle cx="${cx}" cy="${cy}" r="${R}" fill="${fondP}" stroke="${bord}" stroke-width="3"/>` +
      `<path d="${LOGOS[slug].d}" fill="${logo}" transform="translate(${(cx - L / 2).toFixed(1)} ${(cy - L / 2).toFixed(1)}) scale(${(L / 24).toFixed(3)})"/></g>`;''',
'''    const halo = neon ? `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${hex}" stroke-width="${o.bord + 8}" filter="url(#lueurP)"/>` : '';
    return `<g class="${cls}"${m}>${halo}<circle cx="${cx}" cy="${cy}" r="${R}" fill="${fondP}"${o.bord || neon ? ` stroke="${neon ? hex : bord}" stroke-width="${Math.max(o.bord, neon ? 2 : 0)}"` : ''}/>` + logo(logoC) + '</g>';'''),
("const [fondP, bord, logo] = o.piece", "const [fondP, bord, logoC] = o.piece"),
('''<filter id="lueur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="${(3 / s).toFixed(1)}"/></filter></defs>''',
'''<filter id="lueur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="${px(4)}"/></filter>
<filter id="lueurP" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="lueurL" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="${(5 / k).toFixed(2)}"/></filter></defs>'''),
("${main('main-adam')}", "${main('main-adam', 'adam')}"),
("${main('main-dieu')}", "${main('main-dieu', 'dieu')}"),
("forEach((b) => b.setAttribute('aria-pressed', String(etat[g.dataset.cle]) === b.dataset.v))",
 "forEach((b) => b.setAttribute('aria-pressed', g.dataset.cle === 'neon' ? etat.neon.includes(b.dataset.v) : String(etat[g.dataset.cle]) === b.dataset.v))"),
("if (cle) { etat[cle] = cle === 'duree' ? +b.dataset.v : b.dataset.v; rendre(); }",
 "if (cle === 'neon') etat.neon = etat.neon.includes(b.dataset.v) ? etat.neon.filter((x) => x !== b.dataset.v) : [...etat.neon, b.dataset.v];\n  else if (cle) etat[cle] = cle === 'duree' ? +b.dataset.v : b.dataset.v;\n  if (cle) rendre();"),
("document.getElementById('duree').addEventListener('input', (e) => { etat.duree = +e.target.value; rendre(); });",
 "document.getElementById('duree').addEventListener('input', (e) => { etat.duree = +e.target.value; rendre(); });\ndocument.querySelectorAll('[data-curseur]').forEach((c) => c.addEventListener('input', () => { etat[c.dataset.curseur] = +c.value; rendre(); }));"),
("  document.getElementById('duree').value = etat.duree;",
 "  document.getElementById('duree').value = etat.duree;\n  document.querySelectorAll('[data-curseur]').forEach((c) => { c.value = etat[c.dataset.curseur]; document.getElementById('v-' + c.dataset.curseur).textContent = etat[c.dataset.curseur] + c.dataset.unite; });\n  document.getElementById('f-bord').hidden = etat.support !== 'piece';\n  document.querySelector('[data-cle=\"neon\"] [data-v=\"fb\"]').hidden = etat.rotation !== 'piece';"),
]
for a, b in r:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
open(p, 'w', encoding='utf8').write(s)
print('ok', len(r))
