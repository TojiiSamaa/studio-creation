p='studio-gabarit.html'; s=open(p,encoding='utf8').read()
a='''defs.push(`<filter id="flou-piece" x="-60%" y="-60%" width="220%" height="220%">'''
b='''// zone du flou fixe en coordonnées de scène : relative à la boîte englobante, elle rétrécit avec la pièce de profil et coupe le néon net
      const zone = n(R + marge + d + 18 * force + 10);
      defs.push(`<filter id="flou-piece" filterUnits="userSpaceOnUse" x="${n(cx - zone)}" y="${n(cy - zone)}" width="${n(2 * zone)}" height="${n(2 * zone)}">'''
assert s.count(a)==1; s=s.replace(a,b); open(p,'w',encoding='utf8').write(s)
