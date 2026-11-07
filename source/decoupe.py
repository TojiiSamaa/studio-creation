# Isole les deux mains de la fresque (domaine public) en masques noir/blanc pour potrace.
import cv2, numpy as np, sys
src = cv2.imread(sys.argv[1])
H, W = src.shape[:2]
k = W / 1200  # coordonnées repérées sur l'aperçu 1200 px

def masque(x0, y0, x1, y1, nom):
    x0, y0, x1, y1 = [int(v * k) for v in (x0, y0, x1, y1)]
    roi = src[y0:y1, x0:x1].copy()
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # peau : teinte orangée, saturation nette ; ciel/mur : gris-bleu peu saturé
    peau = ((hsv[..., 0] < 25) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 55) & (hsv[..., 2] > 70)
    gc = np.where(peau, cv2.GC_PR_FGD, cv2.GC_PR_BGD).astype('uint8')
    bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(roi, gc, None, bgd, fgd, 10, cv2.GC_INIT_WITH_MASK)
    m = np.where((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD), 255, 0).astype('uint8')
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    # garder la plus grande composante (la main + l'avant-bras), boucher les trous
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        m = np.where(lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA]), 255, 0).astype('uint8')
    cont, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m = np.zeros_like(m); cv2.drawContours(m, cont, -1, 255, -1)
    m = cv2.GaussianBlur(m, (5, 5), 0); m = np.where(m > 127, 255, 0).astype('uint8')
    cv2.imwrite(f'{nom}.png', 255 - m)  # potrace trace le noir
    lum = cv2.GaussianBlur(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY), (7, 7), 0)
    dedans = lum[m > 0]
    for couche, q in (('moyen', 40), ('lumiere', 72)):  # percentiles de luminance DANS la main
        t = np.percentile(dedans, q)
        c = np.where((m > 0) & (lum > t), 255, 0).astype('uint8')
        c = cv2.morphologyEx(c, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        cv2.imwrite(f'{nom}-{couche}.png', 255 - c)
    print(nom, m.shape, int(m.mean() / 2.55), '% de main')

masque(255, 205, 458, 278, 'main-adam')
masque(452, 200, 578, 285, 'main-dieu')
