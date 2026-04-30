import numpy as np

def podziel(obiekt):
    wezly = obiekt.wezly.tolist()
    sciany = []

    for s in obiekt.krawedzie:
        wierzcholki = s[:-1]

        for j in range(1, len(wierzcholki) - 1):
            sciany.append([wierzcholki[0], wierzcholki[j], wierzcholki[j+1]])

    #print("sciany", sciany)
    
    obiekt.wezly = np.array(wezly)
    obiekt.krawedzie = sciany