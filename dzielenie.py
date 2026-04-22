import numpy as np

def podziel_na_trojkaty(obiekt, poziom_subdivizji=1):

    wezly = [list(w) for w in obiekt.wezly]
    nowe_sciany = []

    def podziel_trojkat(a, b, c, poziom):
        if poziom == 0:
            nowe_sciany.append([a + 1, b + 1, c + 1])
            return
            
        p_a = np.array(wezly[a])
        p_b = np.array(wezly[b])
        p_c = np.array(wezly[c])
        
        # Oblicz środki trzech krawędzi
        m_ab = (p_a + p_b) / 2.0
        m_bc = (p_b + p_c) / 2.0
        m_ca = (p_c + p_a) / 2.0
        
        # Dodaj nowe węzły do listy węzłów
        wezly.append([m_ab[0], m_ab[1], m_ab[2], 1.0])
        idx_ab = len(wezly) - 1
        
        wezly.append([m_bc[0], m_bc[1], m_bc[2], 1.0])
        idx_bc = len(wezly) - 1
        
        wezly.append([m_ca[0], m_ca[1], m_ca[2], 1.0])
        idx_ca = len(wezly) - 1
        
        # Rekurencyjny podział na 4 mniejsze trójkąty
        podziel_trojkat(a, idx_ab, idx_ca, poziom - 1)
        podziel_trojkat(b, idx_bc, idx_ab, poziom - 1)
        podziel_trojkat(c, idx_ca, idx_bc, poziom - 1)
        podziel_trojkat(idx_ab, idx_bc, idx_ca, poziom - 1)

    for sciana in obiekt.krawedzie:
        # Pozbądź się powielonego ostatniego węzła (jeśli ściana jest zamknięta)
        zamknieta = len(sciana) > 1 and sciana[0] == sciana[-1]
        unikalne = sciana[:-1] if zamknieta else sciana
        aktualna_sciana = [i - 1 for i in unikalne] # Na indeksowanie 0-based
        
        # Triangulacja wielokąta w wachlarz trójkątów
        for j in range(1, len(aktualna_sciana) - 1):
            podziel_trojkat(aktualna_sciana[0], aktualna_sciana[j], aktualna_sciana[j+1], poziom_subdivizji)

    obiekt.wezly = np.array(wezly)
    obiekt.krawedzie = nowe_sciany
