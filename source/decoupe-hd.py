# Version HD de decoupe.py : fresque 14090 px, 4 tons, bouts des doigts calculés.
#   python -I decoupe-hd.py <image> <dossier-sortie>
import cv2, numpy as np, sys, json, os
src = cv2.imread(sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
H, W = src.shape[:2]
k = W / 1200          # coordonnées repérées sur l'aperçu 1200 px
PX = 4.5              # résolution de travail : 4,5 px par unité d'aperçu (≈ 1,5× l'ancienne source)
bouts = {}

def masque(x0, y0, x1, y1, nom, bout):
    roi = src[int(y0 * k):int(y1 * k), int(x0 * k):int(x1 * k)]
    roi = cv2.resize(roi, (int((x1 - x0) * PX), int((y1 - y0) * PX)), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    peau = ((hsv[..., 0] < 25) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 55) & (hsv[..., 2] > 70)
    gc = np.where(peau, cv2.GC_PR_FGD, cv2.GC_PR_BGD).astype('uint8')
    bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(roi, gc, None, bgd, fgd, 10, cv2.GC_INIT_WITH_MASK)
    m = np.where((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD), 255, 0).astype('uint8')
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        m = np.where(lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA]), 255, 0).astype('uint8')
    cont, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m = np.zeros_like(m); cv2.drawContours(m, cont, -1, 255, -1)
    m = cv2.GaussianBlur(m, (21, 21), 0); m = np.where(m > 127, 255, 0).astype('uint8')
    cv2.imwrite(f'{out}/{nom}.png', 255 - m)
    lum = cv2.GaussianBlur(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY), (9, 9), 0)
    dedans = lum[m > 0]
    for couche, q in (('moyen', 30), ('clair', 55), ('lumiere', 78)):  # percentiles de luminance DANS la main
        c = np.where((m > 0) & (lum > np.percentile(dedans, q)), 255, 0).astype('uint8')
        c = cv2.morphologyEx(c, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        cv2.imwrite(f'{out}/{nom}-{couche}.png', 255 - c)
    ys, xs = np.nonzero(m)
    x = xs.max() if bout == 'droite' else xs.min()
    bouts[nom] = {'x': int(x), 'y': int(ys[xs == x].mean())}
    print(nom, m.shape, int(m.mean() / 2.55), '% de main, bout', bouts[nom])

masque(255, 236, 458, 314, 'main-adam', 'droite')
masque(454, 232, 574, 312, 'main-dieu', 'gauche')
json.dump(bouts, open(f'{out}/bouts.json', 'w'))
