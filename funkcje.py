import numpy as np 

def subdivide_iter(i0, i1, i2, poziom, wezly, nowe_sciany):
    stos = [(i0, i1, i2, poziom)]
    while stos:
        a, b, c, lvl = stos.pop()
        if lvl == 0:
            nowe_sciany.append([a + 1, b + 1, c + 1])
            continue
        p0, p1, p2 = np.array(wezly[a]), np.array(wezly[b]), np.array(wezly[c])
        for m in [(p0+p1)/2, (p1+p2)/2, (p0+p2)/2]:
            wezly.append([m[0], m[1], m[2], 1.0])
        im01, im12, im02 = len(wezly)-3, len(wezly)-2, len(wezly)-1
        stos.extend([
            (a,    im01, im02, lvl-1),
            (im01, b,    im12, lvl-1),
            (im02, im12, c,    lvl-1),
            (im01, im12, im02, lvl-1),
        ])


def podziel_na_trojkaty(obiekt, poziom_subdivizji=1):
    wezly = [list(w) for w in obiekt.wezly]
    nowe_sciany = []

    for sciana in obiekt.krawedzie:
        # usuń powtórzony pierwszy wierzchołek z końca
        unikalne = sciana[:-1] if len(sciana) > 1 and sciana[0] == sciana[-1] else sciana
        idx0 = [i - 1 for i in unikalne]
        for j in range(1, len(idx0) - 1):
            subdivide_iter(idx0[0], idx0[j], idx0[j+1], poziom_subdivizji, wezly, nowe_sciany)
    obiekt.wezly = np.array(wezly)
    obiekt.krawedzie = nowe_sciany

