import numpy as np

def podziel_liste_trojkatow(wezly, trojkaty):
    nowe_trojkaty = []
    for a, b, c in trojkaty:
        p_a, p_b, p_c = np.array(wezly[a]), np.array(wezly[b]), np.array(wezly[c])
        
        # Środki trzech krawędzi
        m_ab = ((p_a + p_b) / 2.0).tolist()
        m_bc = ((p_b + p_c) / 2.0).tolist()
        m_ca = ((p_c + p_a) / 2.0).tolist()
        
        idx_ab = len(wezly)
        wezly.append(m_ab)
        
        idx_bc = len(wezly)
        wezly.append(m_bc)
        
        idx_ca = len(wezly)
        wezly.append(m_ca)
        
        # Z jednego trójkąta robimy 4 mniejsze
        nowe_trojkaty.extend([
            [a, idx_ab, idx_ca],
            [b, idx_bc, idx_ab],
            [c, idx_ca, idx_bc],
            [idx_ab, idx_bc, idx_ca]
        ])
    return nowe_trojkaty


def podziel(obiekt):
    wezly = obiekt.wezly.tolist()
    sciany = []

    # 1. Wstępne dzielenie ścian wielokątnych na trójkąty (wachlarz)
    for s in obiekt.krawedzie:
        wierzcholki = [i - 1 for i in s[:-1]]
        print("wierzcholki", wierzcholki)
        print("s", s)
        for j in range(0, len(wierzcholki)-1):
            sciany.append([wierzcholki[0], wierzcholki[j], wierzcholki[j+1]])
            print([wierzcholki[0], wierzcholki[j-1], wierzcholki[j]])
            print("sciana", sciany)
# Poziom 1 (z 1 trójkąta robią się 4)
    sciany = podziel_liste_trojkatow(wezly, sciany)
    
    # Poziom 2 (z 4 trójkątów robi się 16)
    sciany = podziel_liste_trojkatow(wezly, sciany)

    obiekt.wezly = np.array(wezly)
    # 3. Powrót na indeksowanie 1-based
    obiekt.krawedzie = [[a + 1, b + 1, c + 1] for a, b, c in sciany]
