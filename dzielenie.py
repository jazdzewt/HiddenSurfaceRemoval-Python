import numpy as np

def podziel_sciany(wezly, sciany):
    nowe_sciany = []

    for a, b, c in sciany:
        wezel_A = wezly[a - 1]
        wezel_B = wezly[b - 1] 
        wezel_C = wezly[c - 1]

        wezel_AB = [(wezel_A[0] + wezel_B[0]) / 2, (wezel_A[1] + wezel_B[1]) / 2, (wezel_A[2] + wezel_B[2]) / 2, 1.0]
        wezel_BC = [(wezel_B[0] + wezel_C[0]) / 2, (wezel_B[1] + wezel_C[1]) / 2, (wezel_B[2] + wezel_C[2]) / 2, 1.0]
        wezel_CA = [(wezel_C[0] + wezel_A[0]) / 2, (wezel_C[1] + wezel_A[1]) / 2, (wezel_C[2] + wezel_A[2]) / 2, 1.0]

        index_AB = len(wezly) + 1
        wezly.append(wezel_AB)

        index_BC = len(wezly) + 1
        wezly.append(wezel_BC)

        index_CA = len(wezly) + 1
        wezly.append(wezel_CA)

        nowe_sciany.append([a, index_AB, index_CA])
        nowe_sciany.append([b, index_BC, index_AB])
        nowe_sciany.append([c, index_CA, index_BC])
        nowe_sciany.append([index_AB, index_BC, index_CA])
        #print("nowe_sciany: ", nowe_sciany)
    return nowe_sciany

def podziel(obiekt):
    wezly = obiekt.wezly.tolist()
    sciany = []

    for s in obiekt.krawedzie:
        wierzcholki = s[:-1]

        for j in range(1, len(wierzcholki) - 1):
            sciany.append([wierzcholki[0], wierzcholki[j], wierzcholki[j+1]])

    #print("sciany", sciany)
    
    sciany = podziel_sciany(wezly, sciany)
    sciany = podziel_sciany(wezly, sciany)

    obiekt.wezly = np.array(wezly)
    obiekt.krawedzie = sciany