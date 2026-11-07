p='studio-gabarit.html'; s=open(p,encoding='utf8').read()
r=[("""      for (const [id, cle] of [['tra', 'faceA'], ['trb', 'faceB']]) defs.push(`<linearGradient id="${id}"><stop offset="0" stop-color="${teinte(cle)}"/><stop offset="1" stop-color="${bordT(teinte(cle))}"/></linearGradient>`);
""", ""),
("const demi = (cls, id) => `<g class=\"${cls}\" data-calque=\"piece\"><rect x=\"${cx}\" y=\"${n(cy - R)}\" width=\"${n(d / 2)}\" height=\"${n(2 * R)}\" fill=\"url(#${id})\"/></g>`;",
 "const demi = (cls, cle) => `<g class=\"${cls}\" data-calque=\"piece\"><rect x=\"${cx}\" y=\"${n(cy - R)}\" width=\"${n(d / 2)}\" height=\"${n(2 * R)}\" fill=\"${bordT(teinte(cle))}\"/></g>`;"),
("demi('ha', 'tra') + demi('hb', 'trb')", "demi('ha', 'faceA') + demi('hb', 'faceB')"),
("bordT = (c) => melange(c, '#000000', 0.22)", "bordT = (c) => melange(c, '#000000', 0.12)"),
]
for a,b in r:
    assert s.count(a)==1,a[:70]; s=s.replace(a,b)
open(p,'w',encoding='utf8').write(s)
