# v4 : néon de tranche en deux moitiés + inspecteur compact façon Figma
import re
p = 'studio-gabarit.html'; s = open(p, encoding='utf8').read()

def entre(debut, fin, nouveau):
    global s
    i = s.index(debut); j = s.index(fin, i)
    s = s[:i] + nouveau + s[j:]

# ---------- 1. retournement : lueur de la silhouette, tranche partagée à mi-épaisseur
entre("  if (A === 'retournement') {", "  } else {\n    piece = `<g class=\"piece\">", r"""  if (A === 'retournement') {
    const d = e.piece.support === 'piece' ? e.piece.epaisseur : 0, cos = (a) => Math.cos(a).toFixed(3), sin = (a, k = 1) => (k * Math.sin(a)).toFixed(3);
    css.push(kf('pa', (a) => `translateX(${n(d / 2 * Math.sin(a))}px) scaleX(${cos(a)})`), kf('pb', (a) => `translateX(${n(-d / 2 * Math.sin(a))}px) scaleX(${cos(a)})`),
      `.pa,.pb,.tr,.ha,.hb{${centre}}.pa{animation:pa ${T}s linear infinite}.pb{animation:pb ${T}s linear infinite}.va{animation:va ${T}s step-end infinite}.vb{animation:vb ${T}s step-end infinite}@keyframes va{0%{opacity:1}25%{opacity:0}75%{opacity:1}}@keyframes vb{0%{opacity:0}25%{opacity:1}75%{opacity:0}}`);
    const sil = e.piece.support === 'piece';
    const lueur = (cle) => { const f = e.faces[cle], p = e.piece; return f.neon ? [f.neonCouleur, f.neonForce] : p.neon ? [p.neonCouleur, p.neonForce] : null; };
    const la = sil && lueur('faceA'), lb = sil && lueur('faceB');
    // chaque moitié de la tranche appartient à une face : la moitié A suit sin(angle), la B suit -sin(angle) ; les couleurs se rejoignent au milieu
    if (d && (la || lb)) css.push(kf('ha', (a) => `scaleX(${sin(a)})`), kf('hb', (a) => `scaleX(${sin(a, -1)})`), `.ha{animation:ha ${T}s linear infinite}.hb{animation:hb ${T}s linear infinite}`);
    const moitie = (cls, l, y, h, plus = '') => (l ? `<g class="${cls}"><rect x="${cx}" y="${n(y)}" width="${n(d / 2)}" height="${n(h)}" fill="${l[0]}"${plus}/></g>` : '');
    if (la || lb) { // une seule lueur floutée d'un bloc sur la silhouette animée : continue sur la tranche, sans saut au changement de face
      const force = Math.max(la ? la[1] : 0, lb ? lb[1] : 0), marge = n(3 + 2 * force);
      defs.push(`<filter id="flou-piece" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="${n(6 * force)}"/><feMerge><feMergeNode/><feMergeNode/></feMerge></filter>`);
      const disque = (cls, l) => (l ? `<g class="${cls}"><circle cx="${cx}" cy="${cy}" r="${n(R + marge)}" fill="${l[0]}"/></g>` : '');
      piece += `<g filter="url(#flou-piece)" data-calque="piece">${disque('pa', la)}${disque('pb', lb)}${d ? moitie('ha', la, cy - R - marge, 2 * (R + marge)) + moitie('hb', lb, cy - R - marge, 2 * (R + marge)) : ''}</g>`;
    }
    if (d) {
      const ombre = melange(e.piece.tranche, '#000000', 0.55);
      defs.push(`<linearGradient id="tranche"><stop offset="0" stop-color="${ombre}"/><stop offset=".5" stop-color="${e.piece.tranche}"/><stop offset="1" stop-color="${ombre}"/></linearGradient>`);
      css.push(kf('tr', (a) => `scaleX(${Math.abs(Math.sin(a)).toFixed(3)})`), `.tr{animation:tr ${T}s linear infinite}`);
      const disque = (cls) => `<g class="${cls}" data-calque="piece"><circle cx="${cx}" cy="${cy}" r="${n(R)}" fill="${ombre}"/></g>`;
      piece += disque('pa') + disque('pb') + `<g class="tr" data-calque="piece"><rect x="${n(cx - d / 2)}" y="${n(cy - R)}" width="${d}" height="${n(2 * R)}" fill="url(#tranche)"/></g>`;
      // arêtes de la tranche au néon, nettes, chaque moitié dans la couleur de sa face
      const arete = (l) => (l ? ` opacity=".9"` : '');
      piece += moitie('ha', la, cy - R - 1, 3, arete(la)) + moitie('ha', la, cy + R - 2, 3, arete(la)) + moitie('hb', lb, cy - R - 1, 3, arete(lb)) + moitie('hb', lb, cy + R - 2, 3, arete(lb));
    }
    piece += `<g class="pa"><g class="va" data-calque="faceA">${face('faceA', sil)}</g></g><g class="pb"><g class="vb" data-calque="faceB"><g transform="translate(${cx} 0) scale(-1 1) translate(${-cx} 0)">${face('faceB', sil)}</g></g></g>`;
""")

# ---------- 2. définitions des réglages + inspecteur
entre("const groupe = (titre, ...champs)", "// ---------- recherche de logos", r"""const groupe = (titre, ...champs) => ({ groupe: titre, champs });
const seg = (chemin, lib, options, plus = {}) => ({ type: 'seg', chemin, lib, options, ...plus });
const liste = (chemin, lib, options, plus = {}) => ({ type: 'liste', chemin, lib, options, ...plus });
const couleur = (chemin, lib, plus = {}) => ({ type: 'couleur', chemin, lib, ...plus });
const curseur = (chemin, lib, min, max, pas, unite, plus = {}) => ({ type: 'curseur', chemin, lib, min, max, pas, unite, ...plus });
const inter = (chemin, lib, plus = {}) => ({ type: 'inter', chemin, lib, ...plus });
const bascule = (chemin) => ({ bascule: chemin }); // interrupteur dans l'en-tête de section : coupé, la section se replie
const note = (texte) => ({ note: texte });
const condition = (si) => ({ condition: si });

function champs(id) {
  if (id === 'scene') return [
    groupe('Format', seg('scene.format', 'Taille', [['banniere', '1200×500'], ['carre', '800×800']])),
    groupe('Fond', seg('scene.fond', 'Type', [['noir', 'Noir'], ['couleur', 'Couleur'], ['transparent', 'Aucun']]),
      couleur('scene.fondCouleur', 'Couleur', { si: (e) => e.scene.fond === 'couleur' })),
  ];
  if (id === 'animation') return [
    groupe('Mouvement', liste('animation.type', 'Type', OPT.type), liste('animation.duree', 'Vitesse', OPT.vitesse, { num: true }),
      curseur('animation.duree', 'Durée', 1, 12, 0.1, ' s'), couleur('animation.ondeCouleur', 'Ondes', { si: (e) => e.animation.type === 'onde' })),
    groupe('Options', inter('animation.souffle', 'Les mains respirent'),
      liste('animation.reduit', 'Animations coupées', [['ignorer', 'Jouer quand même'], ['respecter', 'Rester immobile']])),
  ];
  if (id === 'gauche' || id === 'droite') {
    const p = `mains.${id}`, m = (e) => e.mains[id], montree = (e) => m(e).style !== 'masquee';
    return [
      groupe('Apparence', liste(`${p}.style`, 'Style', OPT.style), couleur(`${p}.couleur`, 'Couleur', { si: montree }),
        curseur(`${p}.lum`, 'Luminosité', 0.15, 1.6, 0.05, '', { si: montree, pourcent: true }),
        curseur(`${p}.contour`, 'Trait', 0.5, 8, 0.1, ' px', { si: (e) => m(e).style === 'contour' || m(e).neon })),
      groupe('Néon', bascule(`${p}.neon`), seg(`${p}.neonZone`, 'Zone', OPT.zone), couleur(`${p}.neonCouleur`, 'Couleur'),
        curseur(`${p}.neonForce`, 'Intensité', 0.3, 3, 0.1, '×'), condition(montree)),
      groupe('Synchronisation', inter('mains.lier', 'Mêmes réglages des deux côtés')),
    ];
  }
  if (id === 'piece') return [
    groupe('Forme', seg('piece.support', 'Support', [['piece', 'Pièce'], ['logo', 'Logo seul']]), curseur('piece.taille', 'Taille', 60, 160, 5, ' %')),
    groupe('Épaisseur', curseur('piece.epaisseur', 'Épaisseur', 0, 40, 1, ' px'), couleur('piece.tranche', 'Tranche'),
      note((e) => (e.animation.type === 'retournement' ? '' : 'Visible seulement avec le retournement.')), condition((e) => e.piece.support === 'piece')),
    groupe('Liseré', curseur('piece.bord', 'Épaisseur', 0, 12, 0.5, ' px'), couleur('piece.bordCouleur', 'Couleur', { si: (e) => e.piece.bord > 0 }),
      condition((e) => e.piece.support === 'piece')),
    groupe('Aura', bascule('aura.actif'), couleur('aura.couleur', 'Couleur'), curseur('aura.taille', 'Taille', 1.5, 9, 0.1, '×'),
      curseur('aura.force', 'Luminosité', 0.05, 1, 0.05, '', { pourcent: true }), inter('aura.pulsation', 'Pulsation')),
    groupe('Néon de la pièce', bascule('piece.neon'), couleur('piece.neonCouleur', 'Couleur'), curseur('piece.neonForce', 'Intensité', 0.3, 3, 0.1, '×'),
      note(() => 'Le néon propre à une face passe devant.')),
  ];
  const p = `faces.${id}`;
  return [
    groupe('Logo', { type: 'icone', face: id }, couleur(`${p}.logo`, 'Couleur', { marque: id }),
      curseur(`${p}.gras`, 'Trait', 0, 3, 0.1, ' px'), curseur(`${p}.taille`, 'Taille', 50, 150, 5, ' %')),
    groupe('Face', couleur(`${p}.fond`, 'Couleur', { marque: id }), condition((e) => e.piece.support === 'piece')),
    groupe('Néon', bascule(`${p}.neon`), couleur(`${p}.neonCouleur`, 'Couleur', { marque: id }), curseur(`${p}.neonForce`, 'Intensité', 0.3, 3, 0.1, '×')),
  ];
}

// ---------- inspecteur
const $ = (s, r = document) => r.querySelector(s);
const ico = (nom, cls = '') => `<svg class="ico ${cls}"><use href="#i-${nom}"/></svg>`;
const valeurAffichee = (c, v) => (c.pourcent ? `${Math.round(v * 100)} %` : `${v}${c.unite}`);
const replies = new Set(); // sections repliées, par élément
let paletteOuverte = null, idChamp = 0;
const rangee = (lib, ctrl, id) => `<div class="rangee"><label class="nom"${id ? ` for="${id}"` : ''}>${lib}</label><div class="ctrl">${ctrl}</div></div>`;
function champHtml(c) {
  if (c.condition || c.bascule) return '';
  if (c.note) { const t = c.note(etat); return t ? `<p class="note">${esc(t)}</p>` : ''; }
  if (c.si && !c.si(etat)) return '';
  const v = c.chemin ? lire(etat, c.chemin) : null, id = `c${idChamp++}`;
  if (c.type === 'seg') return rangee(c.lib, `<div class="seg" role="group" aria-label="${c.lib}">${c.options.map(([o, l]) =>
    `<button data-chemin="${c.chemin}" data-v="${o}"${c.num ? ' data-num' : ''} aria-pressed="${v === o}">${l}</button>`).join('')}</div>`);
  if (c.type === 'liste') {
    const perso = c.num && !c.options.some(([o]) => o === v) ? `<option selected value="${v}">Personnalisée (${v} s)</option>` : '';
    return rangee(c.lib, `<select id="${id}" data-chemin="${c.chemin}"${c.num ? ' data-num' : ''}>${perso}${c.options.map(([o, l]) => `<option value="${o}"${o === v ? ' selected' : ''}>${l}</option>`).join('')}</select>`, id);
  }
  if (c.type === 'curseur') return rangee(c.lib, `<div class="curseur"><input type="range" id="${id}" data-chemin="${c.chemin}" data-unite="${c.unite}"${c.pourcent ? ' data-pourcent' : ''} min="${c.min}" max="${c.max}" step="${c.pas}" value="${v}"><output>${valeurAffichee(c, v)}</output></div>`, id);
  if (c.type === 'inter') return `<label class="rangee inter"><span class="nom">${c.lib}</span><input type="checkbox" role="switch" data-chemin="${c.chemin}"${v ? ' checked' : ''}></label>`;
  if (c.type === 'couleur') {
    const ouverte = paletteOuverte === c.chemin, marque = c.marque ? etat.faces[c.marque].hex : null;
    const pastille = (hex, plus = '') => `<button class="pastille${plus ? ' marque' : ''}" style="--c:${hex}" data-chemin="${c.chemin}" data-v="${hex}" aria-pressed="${hex === v}" aria-label="${plus || 'Couleur ' + hex}" title="${plus || hex}"></button>`;
    return rangee(c.lib, `<button class="puce" data-palette="${c.chemin}" aria-expanded="${ouverte}"><i style="background:${v}"></i><span>${v}</span>${ico('chevron')}</button>`) +
      (ouverte ? `<div class="palette">
        <div class="perso"><input type="color" data-chemin="${c.chemin}" value="${v}" aria-label="Couleur personnalisée"><input class="hex" data-hex="${c.chemin}" value="${v}" maxlength="7" spellcheck="false" aria-label="Code hexadécimal"></div>
        <div class="pastilles">${marque ? pastille(marque, 'Couleur de la marque') : ''}${PASTILLES.map((h) => pastille(h)).join('')}</div></div>` : '');
  }
  if (c.type === 'icone') {
    const f = etat.faces[c.face];
    return `<div class="logo-actuel"><svg viewBox="0 0 24 24" fill="${lumineux(f.hex) < 60 ? 'currentColor' : f.hex}"><path d="${f.d}"/></svg><div><b>${esc(f.titre)}</b><span class="mono">${esc(f.slug)}</span></div></div>
      <div class="recherche">${ico('chercher')}<input type="search" data-recherche="${c.face}" placeholder="Chercher parmi ${catalogue ? catalogue.length.toLocaleString('fr-FR') : '3 400+'} logos" aria-label="Chercher un logo"></div>
      <div class="resultats" data-resultats="${c.face}"></div><p class="note" data-etat-recherche="${c.face}"></p>`;
  }
  return '';
}
function rendreInspecteur() {
  const c = CALQUES.find((x) => x.id === selection);
  idChamp = 0;
  const defile = $('#inspecteur').scrollTop;
  $('#inspecteur').innerHTML = `<div class="entete-insp">${ico(c.icone, c.miroir ? 'miroir' : '')}<h2>${c.nom}</h2></div>` +
    champs(selection).filter((g) => !g.champs.some((x) => x.condition && !x.condition(etat))).map((g) => {
      const cle = `${selection}:${g.groupe}`, b = g.champs.find((x) => x.bascule), actif = b ? lire(etat, b.bascule) : true;
      const ouvert = !replies.has(cle) && actif, corps = ouvert ? g.champs.map(champHtml).join('') : '';
      return `<section class="groupe"><div class="tete"><button class="plier" data-plier="${cle}" aria-expanded="${ouvert}"${actif ? '' : ' disabled'}>${ico('chevron')}${g.groupe}</button>` +
        `${b ? `<input type="checkbox" role="switch" data-chemin="${b.bascule}" aria-label="Activer : ${g.groupe}"${actif ? ' checked' : ''}>` : ''}</div>${corps ? `<div class="corps">${corps}</div>` : ''}</section>`;
    }).join('');
  $('#inspecteur').scrollTop = defile;
  const r = $('[data-recherche]'); if (r) afficherResultats(r.dataset.recherche, '');
}
function rendreCalques() {
  $('#p-calques').innerHTML = CALQUES.filter((c) => !c.si || c.si(etat)).map((c) =>
    `<button class="calque" data-calque="${c.id}" aria-current="${c.id === selection}">${ico(c.icone, c.miroir ? 'miroir' : '')}<span><b>${c.nom}</b><small>${esc(c.resume(etat))}</small></span></button>`).join('');
}
function choisir(id) { selection = id; paletteOuverte = null; toutRendre(false); }

function modifier(chemin, v) {
  ecrire(etat, chemin, v);
  const m = chemin.match(/^mains\.(gauche|droite)\.(.+)$/);
  if (m && etat.mains.lier) ecrire(etat, `mains.${m[1] === 'gauche' ? 'droite' : 'gauche'}.${m[2]}`, v);
  if (chemin === 'mains.lier' && v) { const src = selection === 'droite' ? 'droite' : 'gauche'; etat.mains[src === 'droite' ? 'gauche' : 'droite'] = clone(etat.mains[src]); }
}
const insp = $('#inspecteur');
insp.addEventListener('click', (e) => {
  const pl = e.target.closest('[data-plier]');
  if (pl) { replies.has(pl.dataset.plier) ? replies.delete(pl.dataset.plier) : replies.add(pl.dataset.plier); return rendreInspecteur(); }
  const pa = e.target.closest('[data-palette]');
  if (pa) { paletteOuverte = paletteOuverte === pa.dataset.palette ? null : pa.dataset.palette; return rendreInspecteur(); }
  const b = e.target.closest('button[data-chemin]'); if (!b) return;
  modifier(b.dataset.chemin, 'num' in b.dataset ? +b.dataset.v : b.dataset.v);
  toutRendre();
});
insp.addEventListener('input', (e) => {
  const t = e.target;
  if (t.dataset.recherche) return chercherPlusTard(t.dataset.recherche, t.value);
  if (!t.dataset.chemin || t.type === 'checkbox' || t.tagName === 'SELECT') return;
  const v = t.type === 'range' ? +t.value : t.value;
  modifier(t.dataset.chemin, v);
  // pas de re-rendu de l'inspecteur pendant un glisser : le contrôle sous la souris doit rester en place
  if (t.type === 'range') t.nextElementSibling.textContent = 'pourcent' in t.dataset ? `${Math.round(v * 100)} %` : v + t.dataset.unite;
  if (t.type === 'color') { const puce = insp.querySelector(`[data-palette="${t.dataset.chemin}"]`); puce.querySelector('i').style.background = v; puce.querySelector('span').textContent = v; t.nextElementSibling.value = v; }
  rendreScene(); rendreCalques();
});
insp.addEventListener('change', (e) => {
  const t = e.target;
  if (t.type === 'checkbox') { modifier(t.dataset.chemin, t.checked); toutRendre(); }
  else if (t.tagName === 'SELECT') { modifier(t.dataset.chemin, 'num' in t.dataset ? +t.value : t.value); toutRendre(); }
  else if (t.dataset.hex) {
    const v = t.value.trim().toLowerCase().replace(/^#?/, '#');
    if (/^#[0-9a-f]{6}$/.test(v)) { modifier(t.dataset.hex, v); toutRendre(); } else { t.value = lire(etat, t.dataset.hex); retour('Code couleur invalide : il faut 6 chiffres hexadécimaux'); }
  } else if (t.type === 'range' || t.type === 'color') rendreInspecteur(); // visibilités qui dépendent de la valeur (ex. liseré à 0)
});

""")

# ---------- 3. styles de l'inspecteur
entre("  aside { background", "  @media (max-width: 1000px)", r"""  aside { background: var(--panneau); border-left: 1px solid var(--trait); overflow-y: auto; min-height: 0; }
  .entete-insp { display: flex; align-items: center; gap: var(--e2); padding: var(--e3) var(--e4); border-bottom: 1px solid var(--trait); position: sticky; top: 0; background: var(--panneau); z-index: 1; }
  .entete-insp h2 { margin: 0; font-size: var(--t-l); }
  .entete-insp .ico { color: var(--accent); }
  .groupe { border-bottom: 1px solid var(--trait); }
  .tete { display: flex; align-items: center; gap: var(--e2); padding: 4px var(--e3) 4px var(--e2); }
  .plier { flex: 1; display: flex; align-items: center; gap: 6px; height: 32px; padding: 0 var(--e2); border: 0; border-radius: var(--r-s); background: none; font-weight: 600; font-size: var(--t-s); text-align: left; }
  .plier:hover:not(:disabled) { background: var(--surface); }
  .plier:disabled { cursor: default; color: var(--texte-3); }
  .plier .ico { width: 14px; height: 14px; color: var(--texte-3); transition: transform .15s; }
  .plier[aria-expanded="false"] .ico { transform: rotate(-90deg); }
  .corps { display: grid; gap: 6px; padding: 0 var(--e4) var(--e3); }
  .rangee { display: grid; grid-template-columns: 84px minmax(0, 1fr); align-items: center; gap: var(--e2); min-height: 30px; }
  .rangee.inter { grid-template-columns: 1fr auto; cursor: pointer; }
  .nom { color: var(--texte-2); font-size: var(--t-s); }
  .ctrl { min-width: 0; }
  .seg { display: flex; gap: 2px; padding: 2px; background: var(--surface); border: 1px solid var(--trait); border-radius: var(--r-s); }
  .seg button { flex: 1 1 0; min-width: 0; height: 24px; padding: 0 4px; border: 0; border-radius: 4px; background: transparent; color: var(--texte-2); font-size: var(--t-s); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .seg button:hover { color: var(--texte); }
  .seg button[aria-pressed="true"] { background: var(--surface-2); color: var(--texte); font-weight: 600; box-shadow: inset 0 0 0 1px var(--trait); }
  select { width: 100%; height: 28px; padding: 0 var(--e2); border: 1px solid var(--trait); border-radius: var(--r-s); background: var(--surface); font: inherit; font-size: var(--t-s); color: var(--texte); }
  .curseur { display: grid; grid-template-columns: minmax(0, 1fr) 44px; align-items: center; gap: var(--e2); }
  .curseur output { font: var(--t-xs) var(--mono); color: var(--texte-2); text-align: right; }
  input[type=range] { width: 100%; accent-color: var(--accent); margin: 0; }
  input[role=switch] { appearance: none; width: 30px; height: 18px; border-radius: 9px; background: var(--surface-2); border: 1px solid var(--trait); position: relative; margin: 0; cursor: pointer; transition: background-color .15s; flex: none; }
  input[role=switch]::after { content: ''; position: absolute; top: 2px; left: 2px; width: 12px; height: 12px; border-radius: 50%; background: var(--texte-3); transition: transform .15s, background-color .15s; }
  input[role=switch]:checked { background: var(--accent); border-color: var(--accent); }
  input[role=switch]:checked::after { transform: translateX(12px); background: #fff; }
  .puce { width: 100%; height: 28px; display: flex; align-items: center; gap: var(--e2); padding: 0 var(--e2) 0 4px; border: 1px solid var(--trait); border-radius: var(--r-s); background: var(--surface); font: var(--t-xs) var(--mono); color: var(--texte); }
  .puce i { width: 20px; height: 20px; border-radius: 4px; box-shadow: inset 0 0 0 1px rgba(128,128,128,.4); }
  .puce .ico { margin-left: auto; width: 14px; height: 14px; color: var(--texte-3); transition: transform .15s; }
  .puce[aria-expanded="true"] { border-color: var(--accent); }
  .puce[aria-expanded="true"] .ico { transform: rotate(180deg); }
  .palette { display: grid; gap: var(--e2); padding: var(--e2); border: 1px solid var(--trait); border-radius: var(--r-m); background: var(--surface); }
  .perso { display: grid; grid-template-columns: minmax(0, 1fr) 80px; gap: 6px; }
  .perso input[type=color] { width: 100%; height: 28px; padding: 0; border: 1px solid var(--trait); border-radius: var(--r-s); background: none; cursor: pointer; }
  .perso .hex { height: 28px; padding: 0 var(--e2); border: 1px solid var(--trait); border-radius: var(--r-s); background: var(--panneau); font: var(--t-s) var(--mono); }
  .pastilles { display: flex; gap: 4px; }
  .pastille { flex: 1 1 0; min-width: 0; aspect-ratio: 1; max-width: 26px; padding: 0; border: 0; border-radius: 5px; background: var(--c); box-shadow: inset 0 0 0 1px rgba(128,128,128,.4); }
  .pastille.marque { position: relative; }
  .pastille.marque::after { content: ''; position: absolute; inset: auto 3px 3px auto; width: 6px; height: 6px; border-radius: 50%; background: var(--panneau); box-shadow: 0 0 0 1px var(--trait); }
  .pastille[aria-pressed="true"] { outline: 2px solid var(--accent); outline-offset: 1px; }
  .note { color: var(--texte-3); font-size: var(--t-xs); margin: 0; }
  .logo-actuel { display: flex; align-items: center; gap: var(--e3); padding: var(--e2); border: 1px solid var(--trait); border-radius: var(--r-m); background: var(--surface); }
  .logo-actuel svg { width: 26px; height: 26px; flex: none; }
  .logo-actuel b { display: block; }
  .recherche { position: relative; }
  .recherche .ico { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); color: var(--texte-3); }
  .recherche input, .champ-texte { width: 100%; height: 32px; padding: 0 var(--e3) 0 32px; border-radius: var(--r-s); border: 1px solid var(--trait); background: var(--surface); }
  .champ-texte { padding-left: var(--e3); }
  .resultats { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; max-height: 200px; overflow-y: auto; }
  .resultats button { aspect-ratio: 1; border: 1px solid transparent; border-radius: var(--r-s); background: var(--surface); padding: 6px; display: grid; place-items: center; color: var(--texte); }
  .resultats button:hover { border-color: var(--texte-3); }
  .resultats button[aria-pressed="true"] { border-color: var(--accent); background: var(--accent-doux); }
  .resultats img, .resultats svg { width: 100%; height: 100%; }
  :root:not([data-theme="clair"]) .resultats img { filter: invert(1); }

""")
s = s.replace('<symbol id="i-face"', '<symbol id="i-chevron" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></symbol>\n  <symbol id="i-face"', 1)
# anciens styles devenus inutiles (champ/lib/couleur/inter) : retirés s'ils traînent ailleurs
open(p, 'w', encoding='utf8').write(s)
print('ok')
