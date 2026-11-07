p='studio-gabarit.html'; s=open(p,encoding='utf8').read()
a='''      const disque = (cls, cle) => `<g class="${cls}" data-calque="piece"><g class="vp"><circle cx="${cx}" cy="${cy}" r="${n(R)}" fill="${bordT(teinte(cle))}"/></g></g>`;
      const demi = (cls, cle) => `<g class="${cls}" data-calque="piece"><rect x="${cx}" y="${n(cy - R)}" width="${n(d / 2)}" height="${n(2 * R)}" fill="${bordT(teinte(cle))}"/></g>`;'''
b='''      // rayon extérieur = disque + moitié de son liseré, sinon le contour de la face dépasse de l'épaisseur près du profil
      const Re = (cle) => R + ((e.faces[cle].neon || e.piece.neon) ? Math.max(e.piece.bord, 2) : e.piece.bord) / 2;
      const disque = (cls, cle) => `<g class="${cls}" data-calque="piece"><g class="vp"><circle cx="${cx}" cy="${cy}" r="${n(Re(cle))}" fill="${bordT(teinte(cle))}"/></g></g>`;
      const demi = (cls, cle) => `<g class="${cls}" data-calque="piece"><rect x="${cx}" y="${n(cy - Re(cle))}" width="${n(d / 2)}" height="${n(2 * Re(cle))}" fill="${bordT(teinte(cle))}"/></g>`;'''
assert s.count(a)==1; s=s.replace(a,b); open(p,'w',encoding='utf8').write(s)
